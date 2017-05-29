"""Defines a class for representing US national legislative election results
"""

from election_results.election_results import ElectionResults
import election_results.utils as utils

class NationalElectionResults(ElectionResults):
    """Represents the summary of national elections for a legislative body

    Attributes:
        year (Int) - The election year
        legislative_body_code (Int) - Int that maps to a legislative body
            see ../fixtures/legislative_body_codes.py

        votes_total_dem (Int) - Sum total votes for Democratic candidates across
            the country
        votes_total_rep (Int) - Sum total votes for Republican candidates across
            the country
        votes_total_other (Int) - Sum total votes for third-party or independent
            candidates across the country
        votes_total_scattered (Int) - Sum total votes counted but not applied to any candidate
        votes_total (Int) - Sum total votes from all state elections
        votes_wasted_total_dem (Int) - Sum total votes wasted in voting for a
            Democratic candidate
        votes_wasted_total_rep (Int) - Sum total votes wasted in voting for a
            Republican candidate
        votes_wasted_net (Int) - Net wasted votes; difference between the Democratic
            and Republican numbers
        state_results (Dict) - Dict of two-letter state abbreviations to StateElectionResults
    """

    def __init__(self, year, legislative_body_code, data=None, state_results=None):
        """Initializes a NationalElectionResults object

           Attibutes:
                year (Int) - The election year
                legislative_body_code (Int) - Int that maps to a legislative body
                data (Dict) - Contains the non-argument properties
        """
        super(__class__, self).__init__(
            type='n', year=year, legislative_body_code=legislative_body_code)

        self.state_results = {}
        self.votes_total_dem = None
        self.votes_total_rep = None
        self.votes_total_other = None
        self.votes_total_scattered = None
        self.votes_total = None
        self.votes_wasted_total_dem = None
        self.votes_wasted_total_rep = None
        self.votes_wasted_net = None

        if state_results is not None:
            self.summarize_votes(state_results)

    def summarize_votes(self, state_results_dict):
        """Collects the results of state legislative elections
        """
        self.votes_total_dem = 0
        self.votes_total_rep = 0
        self.votes_total_other = 0
        self.votes_total_scattered = 0
        self.votes_total = 0
        self.votes_wasted_total_dem = 0
        self.votes_wasted_total_rep = 0
        self.votes_wasted_net = 0
        self.state_results = {}

        def generate_err_msg(state_results):
            return "{} {} body_code {} StateElectionResults does not belong in \
                    {} {} body_code {} NationalElectionResults".format(
                        state_results.year,
                        state_results.state,
                        state_results.legislative_body_code,
                        self.year,
                        self.state,
                        self.legislative_body_code
                    )

        for results in state_results_dict.values():
            if results.year != self.year:
                raise utils.ElectionResultsError(generate_err_msg(results))

            if results.legislative_body_code != self.legislative_body_code:
                raise utils.ElectionResultsError(generate_err_msg(results))

            try:
                self.votes_total_dem += results.votes_total_dem
                self.votes_total_rep += results.votes_total_rep
                self.votes_total_other += results.votes_total_other
                self.votes_total_scattered += results.votes_total_scattered
                self.votes_total += results.votes_total
                self.votes_wasted_total_dem += results.votes_wasted_total_dem
                self.votes_wasted_total_rep += results.votes_wasted_total_rep
                self.votes_wasted_net += results.votes_wasted_net
                self.state_results[results.state] = results
            except Exception as e:
                print('\nError in {} {} {}'.format(results.year, results.state, results.district))
                print('{}\n'.format(results.__dict__))
                raise e
