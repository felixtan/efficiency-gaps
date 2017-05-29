"""Defines a class for representing a US state's legislative elections
"""

import math
import election_results.utils as utils
from election_results.election_results import ElectionResults
from election_results.district import DistrictElectionResults

class StateElectionResults(ElectionResults):
    """Represents the summary of elections for a legislative body for a US state

    Attributes:
        state (String) - Two-letter abbreviation of US state
        year (Int) - The election year
        legislative_body_code (Int) - Int that maps to a legislative body
            see ../fixtures/legislative_body_codes.py

        votes_total_dem (Int) - Sum total votes for Democratic candidates across
            the state's districts
        votes_total_rep (Int) - Sum total votes for Republican candidates across
            the state's districts
        votes_total_other (Int) - Sum total votes for third-party or independent
            candidates across the state's districts
        votes_total_scattered (Int) - Sum total votes counted but not applied to any candidate
        votes_total (Int) - Sum total votes from all district election
        votes_wasted_total_dem (Int) - Sum total votes wasted in voting for a
            Democratic candidate
        votes_wasted_total_rep (Int) - Sum total votes wasted in voting for a
            Republican candidate
        votes_wasted_net (Int) - Net wasted votes; difference between the Democratic
            and Republican numbers
        districts_won_dem (List) - List of DistrictElectionResults won by Democrats
        districts_won_rep (List) - List of DistrictElectionResults won by Republicans
    """

    def __init__(self, year, state, legislative_body_code, data=None, district_results=None):
        """Initializes a StateElectionResults object

           Attibutes:
                year (Int) - The election year
                state (String) - Two-letter abbreviation of US state
                legislative_body_code (Int) - Int that maps to a legislative body
                data (Dict) - Contains the non-argument properties
        """
        super(__class__, self).__init__(type='s', year=year, state=state,
            legislative_body_code=legislative_body_code)

        self.districts_won_dem = []
        self.districts_won_rep = []
        self.votes_total_dem = None if data is None else data["votes_total_dem"]
        self.votes_total_rep = None if data is None else data["votes_total_rep"]
        self.votes_total_other = None if data is None else data["votes_total_other"]
        self.votes_total_scattered = None if data is None else data["votes_total_scattered"]
        self.votes_total = None if data is None else data["votes_total"]
        self.votes_wasted_total_dem = None if data is None else data["votes_wasted_total_dem"]
        self.votes_wasted_total_rep = None if data is None else data["votes_wasted_total_rep"]
        self.votes_wasted_net = None if data is None else data["votes_wasted_net"]

        if district_results is not None and len(district_results) > 0:
            self.summarize_votes(district_results)

    def summarize_votes(self, districts_results):
        """Collects the results for a state's district elections
        """
        self.votes_total_dem = 0
        self.votes_total_rep = 0
        self.votes_total_other = 0
        self.votes_total_scattered = 0
        self.votes_total = 0
        self.votes_wasted_total_dem = 0
        self.votes_wasted_total_rep = 0
        self.votes_wasted_net = 0

        for results in districts_results:
            if not isinstance(results, DistrictElectionResults):
                raise utils.ElectionResultsError("Object is not an instance of\
                 DistrictElectionResults: {}".format(district))

            self.votes_total_dem += results.votes_dem
            self.votes_total_rep += results.votes_rep
            self.votes_total_other += results.votes_other
            self.votes_total_scattered += results.votes_scattered
            self.votes_total += results.votes_total
            self.votes_wasted_total_dem += results.votes_wasted_dem
            self.votes_wasted_total_rep += results.votes_wasted_rep
            self.votes_wasted_net += results.votes_wasted_net

            if results.votes_rep > results.votes_dem:
                self.districts_won_rep.append(results)
            elif results.votes_dem > results.votes_rep:
                self.districts_won_dem.append(results)

            self.efficiency_gap = self.calc_eff_gap(
                votes_total=self.votes_total,
                votes_wasted_net=self.votes_wasted_net
            )

    def calc_eff_gap(self, votes_total, votes_wasted_net):
        """Calculates the efficiency gap of the election
        """
        return round(votes_wasted_net / votes_total, 3)
