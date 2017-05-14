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
        votes_total_voided (Int) - Sum total votes counted but not applied to any candidate
        votes_total (Int) - Sum total votes from all state elections
        votes_wasted_total_dem (Int) - Sum total votes wasted in voting for a
            Democratic candidate
        votes_wasted_total_rep (Int) - Sum total votes wasted in voting for a
            Republican candidate
        votes_wasted_net (Int) - Net wasted votes; difference between the Democratic
            and Republican numbers
        state_results (Dict) - Dict of two-letter state abbreviations to StateElectionResults
    """

    def __init__(self, year, legislative_body_code, data=None):
        """Initializes a NationalElectionResults object

           Attibutes:
                year (Int) - The election year
                legislative_body_code (Int) - Int that maps to a legislative body
                data (Dict) - Contains the non-argument properties
        """
        super(__class__, self).__init__(
            type='n', year=year, legislative_body_code=legislative_body_code)

        self.votes_total_dem = None
        self.votes_total_rep = None
        self.votes_total_other = None
        self.votes_total_voided = None
        self.votes_total = None
        self.votes_wasted_total_dem = None
        self.votes_wasted_total_rep = None
        self.votes_wasted_net = None
        self.state_results = {}

    def summarize_votes(self, state_results):
        """Collects the results of state legislative elections
        """
        self.votes_total_dem = 0
        self.votes_total_rep = 0
        self.votes_total_other = 0
        self.votes_total_voided = 0
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

        for results in state_results:
            if results.year != self.year:
                raise utils.ElectionResultsError(generate_err_msg(results))

            if results.legislative_body_code != self.legislative_body_code:
                raise utils.ElectionResultsError(generate_err_msg(results))

            self.votes_total_dem += results.votes_total_dem
            self.votes_total_rep += results.votes_total_rep
            self.votes_total_other += results.votes_total_other
            self.votes_total_voided += results.votes_total_voided
            self.votes_total += results.votes_total
            self.votes_wasted_total_dem += results.votes_wasted_total_dem
            self.votes_wasted_total_rep += results.votes_wasted_total_rep
            self.votes_wasted_net += results.votes_wasted_net
            self.state_results[results.state] = results
