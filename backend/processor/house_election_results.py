import csv
import json
import config
import election_results.utils as utils
from fixtures.states import states
from election_results.national import NationalElectionResults
from election_results.state import StateElectionResults
from election_results.district import DistrictElectionResults

class HouseElectionsProcessor:
    def __init__(self, year=2014):
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
        # print('current state={} dist={}\n'.format(self.current_state, self.current_district))

        if self.current_district_results['votes_dem'] == 0 or self.current_district_results['votes_rep'] == 0:
            raise utils.ElectionResultsError('Possible unopposed election in {} {}'.format(self.current_state, self.current_district))

        r = DistrictElectionResults(
            year=self.year,
            state=self.current_state,
            legislative_body_code=self.legislative_body_code,
            district=self.current_district,
            data=self.current_district_results
        )
        print('pushed district: {}\n'.format(r.__dict__))
        self.district_results.append(r)

    def push_current_state_results(self):
        r = StateElectionResults(
            year=self.year,
            state=self.current_state,
            legislative_body_code=self.legislative_body_code,
            district_results=self.district_results
        )

        # print('current state={} dist={}'.format(self.current_state, self.current_district))
        print('pushed state: {}\n'.format(r.__dict__))
        self.state_results[self.current_state] = r

    def set_winner(self, party, candidate_last_name, candidate_first_name):
        self.current_district_results['winner'] = {}
        self.current_district_results['winner']['party'] = party
        self.current_district_results['winner']['last_name'] = candidate_last_name
        self.current_district_results['winner']['first_name'] = candidate_first_name

    def read_votes(self, ge_votes, ge_votes_runoff, ge_votes_combined):
        return ge_votes_combined if ge_votes_combined is not None else (
            ge_votes_runoff if ge_votes_runoff is not None else (
                ge_votes if ge_votes is not None else 0
            )
        )

    def read_row_data(self, i, state, district, party, winner_indicator, candidate_last_name, candidate_first_name, ge_votes, ge_votes_runoff, ge_votes_combined, total_votes_label):
        try:
            votes = self.read_votes(ge_votes, ge_votes_runoff, ge_votes_combined)
            field = None

            if party == 'R':
                field = 'votes_rep'

            elif party == 'D':
                field = 'votes_dem'

            elif party == 'W':
                field = 'votes_scattered'

            elif party != '':
                field = 'votes_other'

            elif party == '' and 'District Votes' in total_votes_label:
                field = 'votes_total'

            if field is not None:
                self.current_district_results[field] += votes

        except Exception as e:
            print('Error reading votes in line {}'.format(i))
            print('current_district_results: {}\n'.format(self.current_district_results))
            raise e

        self.set_winner(party, candidate_last_name, candidate_first_name) if winner_indicator == 'W' else None

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
                    print('{}: \t{} {} \t{} \t{} \t{} \t{}'.format(i, state, district, candidate_first_name, candidate_last_name, party, ge_votes))
                    if self.current_district != district:
                        if self.current_district is not None:
                            self.push_current_district_results()
                            self.reset_current_district_results()

                        self.current_district = district

                    if self.current_state != state:
                        self.push_current_state_results()
                        self.current_state = state
                        self.reset_district_results()

                    # Read row data
                    if isinstance(district, int):
                        self.read_row_data(i, state, district, party, winner_indicator, candidate_last_name, candidate_first_name, ge_votes, ge_votes_runoff, ge_votes_combined, total_votes_label)

        # Push the last state
        self.push_current_state_results()

        return NationalElectionResults(
            year=self.year,
            legislative_body_code=self.legislative_body_code,
            state_results=self.state_results
        )
