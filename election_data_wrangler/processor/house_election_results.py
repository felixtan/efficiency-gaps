"""Defines a class for processing congressional election results from the FEC
"""


import csv
import json
import config
import math
import election_results.utils as utils
from fixtures.states import states
from election_results.national import NationalElectionResults
from election_results.state import StateElectionResults
from election_results.district import DistrictElectionResults

class HouseElectionsProcessor:
    """Reads csv of election results into ElectionResults objects

    Attributes:
        year (Int) - Election year
        only_check_for_unhandled_elections (Bool) - Option indicating the processor will only check for unhandled
            elections and not create any ElectionResults objects
        print_modifications (Bool) - Option indicating whether potential modifications to unhandled elections
            will be printed during checking

    Notes
        Unhandled elections are elections where at least one major party was unrepresented. Examples are

            When a candidate is unopposed

                If an election was not held, then the average number of votes per district is gotten by
                dividing the total votes cast among other districts in the state where elections were held
                by the number of such districts.

                If an election was held and the candidate won >= 75% of the vote, then modify the votes such
                that if a Republican was unopposed, partition the votes such that the Republican gets 68% of
                the vote total and a hypothetical Democrat gets 32%. If a Democrat was unopposed, then partition
                the votes such that the Democrat gets 70% of the vote total and a hypothetical Republican gets
                30%.

                This modification of votes is done because, in the words of Nicholas O. Stephanopoulos and Eric M. McGhee,
                the authors of the paper Partisan Gerrymandering and the Efficiency Gap in which the efficiency gap was
                defined:

                    "We strongly discourage analysts from either dropping uncontested races from the computation
                    or treating them as if they produced unanimous support for a party. The former approach
                    eliminates important information about a plan, while the latter assumes that coerced votes
                    accurately reflect political support."

                    “For congressional races, we obtained presidential vote share data at the district level, and
                    then ran regressions of vote choice in contested seats on incumbency status and district
                    presidential vote separately for each election year. From this information, we imputed values
                    for uncontested seats. For uncontested Democrats, this procedure resulted in a mean Democratic
                    vote share of 70 percent, with 90 percent of values falling between 56 percent and 87 percent.
                    For uncontested Republicans, it produced a mean Democratic vote share of 32 percent, with 90
                    percent of values falling between 22 percent and 43 percent."


            When only one major party is represented and the candidate won < 75% of the vote

                The election and its minor party or independent candidates are analyzed in order to estimate
                their ideological proximity to either major party and thereby group their votes into the
                corresponding major party.
    """

    def __init__(self, year, only_check_for_unhandled_elections=False, print_modifications=False, verbose_read=False):
        """Initializes a HouseElectionsProcessor

        Attributes:
            year (Int) - The election year
            only_check_for_unhandled_elections (Bool) - Option indicating the processor will only check for unhandled
                elections and not create any ElectionResults objects
            print_modifications (Bool) - Option indicating whether potential modifications to unhandled elections
                will be printed during checking
            current_district_results (Dict) - Accumulates the votes in a congressional election
            legislative_body_code (Int) - Corresponds to a legislative body, the House of Representatives in this case
            current_state (String) - The current state's two-letter abbreviation
            current_district (Int) - The current congressional district
            districts_results (List) - Collection of DistrictElectionResults for the current_state
            state_results (Dict) - Keys are two-letter state abbreviations and values are the state's corresponding districts_results list
        """
        self.current_district_results = {
            'votes_dem': 0,
            'votes_rep': 0,
            'votes_other': 0,
            'votes_scattered': 0,
            'votes_total': 0,
            'winner': {
                'party': '',
                'last_name': '',
                'first_name': ''
            }
        }
        self.current_district = None
        self.district_results = []
        self.state_results = {}
        self.current_state = None
        self.legislative_body_code = 0
        self.year = year

        # Options
        self.only_check_for_unhandled_elections = only_check_for_unhandled_elections
        self.print_modifications = print_modifications
        self.verbose_read = verbose_read

    def to_int(self, x):
        """Converts x to int if it's numeric

        Examples
            123,456 => 123456
            01      => 1
        """
        try:
            return int(x.replace(",", ""))
        except ValueError:
            return None

    def to_int_votes(self, v):
        try:
            return self.to_int(v)
        except Exception as e:
            print("Don't know how to handle string vote value {} in {} {}".format(
                v, self.current_state, self.current_district
            ))
            raise e

    def to_int_district(self, d):
        """Converts single-district states' district number from 0 to 1
        """
        x = self.to_int(d)
        return 1 if x == 0 else x

    def reset_district_results(self):
        self.district_results = []

    def reset_current_district_results(self):
        self.current_district_results = {
            'votes_dem': 0,
            'votes_rep': 0,
            'votes_other': 0,
            'votes_scattered': 0,
            'votes_total': 0,
            'winner': {
                'party': '',
                'last_name': '',
                'first_name': ''
            }
        }

    def push_current_district_results(self):
        """Raise exception if election is unhandled. If it's okay, pust to districts_results list.
        """
        # print('current state={} dist={}\n'.format(self.current_state, self.current_district))

        self.check_for_unhandled_elections()

        r = DistrictElectionResults(
            year=self.year,
            state=self.current_state,
            legislative_body_code=self.legislative_body_code,
            district=self.current_district,
            data=self.current_district_results
        )

        if self.verbose_read:
            print('pushed district: {}\n'.format(r.__dict__))

        self.district_results.append(r)

    def push_current_state_results(self):
        """When all of a state's district congressional elections have been read,
            append it to state_results.
        """
        r = StateElectionResults(
            year=self.year,
            state=self.current_state,
            legislative_body_code=self.legislative_body_code,
            district_results=self.district_results
        )

        if self.verbose_read:
            print('current state={} dist={}'.format(self.current_state, self.current_district))
            print('pushed state: {}\n'.format(r.__dict__))

        self.state_results[self.current_state] = r

    def set_winner(self, party, candidate_last_name, candidate_first_name):
        self.current_district_results['winner'] = {}
        self.current_district_results['winner']['party'] = party
        self.current_district_results['winner']['last_name'] = candidate_last_name
        self.current_district_results['winner']['first_name'] = candidate_first_name

    def read_votes(self, ge_votes, ge_votes_runoff, ge_votes_combined):
        """Some states combine some minor party votes with that of a major party's
            because they endorese the major party candidate. Louisiana holds runoff
            elections if no candidate wins >=50% of the vote in the jungle primary.
            These vote totals have priority.
        """
        return ge_votes_combined if ge_votes_combined is not None else (
            ge_votes_runoff if ge_votes_runoff is not None else (
                ge_votes if ge_votes is not None else 0
            )
        )

    def read_row_data(self, i, state, district, party, winner_indicator, candidate_last_name, candidate_first_name, ge_votes, ge_votes_runoff, ge_votes_combined, total_votes_label):
        """Read votes to the correct party
        """
        try:
            votes = self.read_votes(ge_votes, ge_votes_runoff, ge_votes_combined)
            p = party.strip().lower()
            field = None

            if p == 'r' or p == 'rep':
                field = 'votes_rep'

            elif p == 'd' or p == 'dem':
                field = 'votes_dem'

            elif p == 'w':
                field = 'votes_scattered'

            elif p != '':
                field = 'votes_other'

            elif 'District Votes' in total_votes_label:
                field = 'votes_total'

            if field is not None:
                self.current_district_results[field] += votes

        except Exception as e:
            print('Error reading votes in line {}'.format(i))
            print('current_district_results: {}\n'.format(self.current_district_results))
            raise e

        # 2010 and prior FEC results don't use winner indicator column
        # self.set_winner(party, candidate_last_name, candidate_first_name) if winner_indicator == 'W' else None

    def print_current_district_votes(self):
        print('{} {}: votes_total={}, votes_rep={}, votes_dem={}, votes_other={}, votes_scattered={}'.format(
            self.current_state,
            self.current_district,
            self.current_district_results['votes_total'],
            self.current_district_results['votes_rep'],
            self.current_district_results['votes_dem'],
            self.current_district_results['votes_other'],
            self.current_district_results['votes_scattered']
        ))

    def modify_votes_for_R_unopposed(self):
        votes_total = self.current_district_results['votes_total']
        self.current_district_results['votes_rep'] = math.floor(0.68 * votes_total)
        self.current_district_results['votes_dem'] = math.floor(0.32 * votes_total)
        self.current_district_results['votes_other'] = 0
        self.current_district_results['votes_scattered'] = 1

    def modify_votes_for_D_unopposed(self):
        votes_total = self.current_district_results['votes_total']
        self.current_district_results['votes_rep'] = math.floor(0.3 * votes_total)
        self.current_district_results['votes_dem'] = math.floor(0.7 * votes_total)
        self.current_district_results['votes_other'] = 0
        self.current_district_results['votes_scattered'] = 1

    def check_for_unhandled_elections(self):
        """Check if a congressional election is unhandled by the efficiency gap theory

        Unhandled election scenarios
            - scenario
                => solution

            - Open/jungle primary
                => use the runoff election results

            - A major party candidate ran unopposed and an election was not held
                => apply the authors' regression formula
                Such an election is usually marked "Unopposed" in the "General Votes" column

            - A major party candidate ran unopposed and an election was held => apply the authors' regression formula

            - Only one major party candidate ran and minor party candidates and/or independents won an insignificant (< 25%) share
                => Treat the election as unopposed

            - Only one major party candidate ran and minor party candidates and/or independents won a significant (>= 25%) share
                => Individual case analysis
        """

        votes_rep = self.current_district_results['votes_rep']
        votes_dem = self.current_district_results['votes_dem']
        votes_total = self.current_district_results['votes_total']

        if votes_dem == 0 or votes_rep == 0:
            # Offer suggestions for modifying results
            if isinstance(self.current_district_results['votes_total'], int):
                if votes_rep == 0 and votes_dem == 0:
                    msg = 'Case analysis needed in {} {}: No R or D candidates'.format(self.current_state, self.current_district)
                    if self.only_check_for_unhandled_elections:
                        print(msg)
                        print()
                    else:
                        raise utils.ElectionResultsError(msg)
                elif isinstance(votes_rep, int) and votes_dem == 0:
                    if round(votes_rep / votes_total, 2) >= 0.75:
                        self.modify_votes_for_R_unopposed()
                        if self.print_modifications:
                            print('R >= 75% in {} {}... votes modified'.format(self.current_state, self.current_district))
                            self.print_current_district_votes()
                            print()
                    else:
                        msg = 'Case analysis needed {} {}: no D candidate and R < 75%'.format(self.current_state, self.current_district)
                        if self.only_check_for_unhandled_elections:
                            print(msg)
                            print()
                        else:
                            raise utils.ElectionResultsError(msg)

                elif isinstance(votes_dem, int) and votes_rep == 0:
                    if round(votes_dem / votes_total, 2) >= 0.75:
                        self.modify_votes_for_D_unopposed()
                        if self.print_modifications:
                            print('D >= 75% in {} {}... votes modified'.format(self.current_state, self.current_district))
                            self.print_current_district_votes()
                            print()
                    else:
                        msg = 'Case analysis needed in {} {}: no R candidate D < 75%'.format(self.current_state, self.current_district)
                        if self.only_check_for_unhandled_elections:
                            print(msg)
                            print()
                        else:
                            raise utils.ElectionResultsError(msg)
            else:
                msg = 'Case analysis needed in {} {}: no votes logged'.format(self.current_state, self.current_district)
                if self.only_check_for_unhandled_elections:
                    print(msg)
                else:
                    raise utils.ElectionResultsError(msg)

    def read_and_process_election_results(self, filepath):
        with open(filepath) as file:
            if filepath.endswith(".csv"):
                return self.process_election_results_csv(csv.reader(file))

    def process_election_results_csv(self, csv_reader_obj):
        """Returns a populated NationalElectionResults object
        """

        """Map of column names to indices in source data

        Notes (based on 2014 FEC results)
            1. ge = General Election
            2. ge_votes_runoff applies to LA only if no candidate won a majority in the first round
            3. ge_votes_combined applies to CT, NY, SC because minor parties coalesce around major party
        """
        column_index = {
            'state': 0,
            'district': 1,
            'incumbent_indicator': 2,
            'first_name': 3,
            'last_name': 4,
            'total_votes_label': 5,
            'party': 6,
            'ge_votes': 7,
            'ge_percent': 8,
            'ge_votes_runoff': 9,
            'ge_votes_runoff_percent': 10,
            'ge_votes_combined': 11,
            'ge_votes_combined_percent': 12,
            'ge_winner_indicator': 13
        }

        for i, row in enumerate(csv_reader_obj):
            if i > 0:
                # column names
                state = row[column_index['state']].strip()
                district = self.to_int_district(row[column_index['district']])
                candidate_last_name = row[column_index['last_name']].strip()
                candidate_first_name = row[column_index['first_name']].strip()
                total_votes_label = row[column_index['total_votes_label']].strip()
                party = row[column_index['party']].strip()
                ge_votes = self.to_int_votes(row[column_index['ge_votes']])
                ge_votes_runoff = self.to_int_votes(row[column_index['ge_votes_runoff']])
                ge_votes_combined = self.to_int_votes(row[column_index['ge_votes_combined']])
                winner_indicator = row[column_index['ge_winner_indicator']].strip()

                # init current_state and current_district
                if i == 1:
                    self.current_state = state
                    self.current_district = district

                if state in states:
                    if not self.only_check_for_unhandled_elections and self.verbose_read:
                        print('{}: \t{} {} \t{} \t{} \t{} \t{}'.format(i, state, district, candidate_first_name, candidate_last_name, party, ge_votes))

                    if self.current_district != district:
                        if self.current_district is not None:
                            if self.only_check_for_unhandled_elections:
                                self.check_for_unhandled_elections()
                            else:
                                self.push_current_district_results()

                            self.reset_current_district_results()

                        self.current_district = district

                    if self.current_state != state:
                        if not self.only_check_for_unhandled_elections:
                            self.push_current_state_results()

                        self.current_state = state
                        self.reset_district_results()

                    # Read row data
                    if isinstance(district, int):
                        self.read_row_data(i, state, district, party, winner_indicator, candidate_last_name, candidate_first_name, ge_votes, ge_votes_runoff, ge_votes_combined, total_votes_label)

        # Push the last state
        if not self.only_check_for_unhandled_elections:
            self.push_current_state_results()

            return NationalElectionResults(
                year=self.year,
                legislative_body_code=self.legislative_body_code,
                state_results=self.state_results
            )
