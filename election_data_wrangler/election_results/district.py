"""Defines a class for representing a legislative district's elections
"""

import math
import election_results.utils as utils
from warnings import warn
from election_results.election_results import ElectionResults

class DistrictElectionResults(ElectionResults):
    """Represents the general election results for a legislative district for
       a given state and election year

    Attributes:
        year (Int) - The election year
        state (String) - Two-letter abbreviation of a US state
        legislative_body_code (Int) - Int that maps to a legislative body.
            See ../fixtures/legislative_body_codes.py
        district (Int) - Legislative district number
        votes_dem (Int) - Number of votes for the Democratic candidate
        votes_rep (Int) - Number of votes for the Republican candidate
        votes_other (Int) - Number of votes for a third-party or independent
        votes_scattered (Int) - Number of votes that were invalid and not applied to
            any candidate
        votes_total (Int) - Number of total votes in the election
        votes_wasted_dem (Int) - Number of votes wasted by the Democratic candidate
        votes_wasted_rep (Int) - Number of votes wasted by the Republican candidate
        votes_wasted_net (Int) - The difference in wasted votes between the
            Democratic and republican candidates
        winner (Dict) - Contains party (three-letter lowercase abbreviation),
            last_name and first_name of the winner
    """

    def __init__(self, year, state, legislative_body_code, district, data=None):
        """Instantiate a DistrictElectionResults object

        Attibutes:
            year (Int) - The election year
            state (String) - Two-letter abbreviation of US state
            legislative_body_code (Int) - Int that maps to a legislative body
            district (Int) - Legislative district number
            data (Dict) - Contains the non-argument properties
        """

        super(__class__, self).__init__(type='d', year=year, state=state,
            legislative_body_code=legislative_body_code, district=district)

        self.votes_dem = None if data is None else (data["votes_dem"] if ("votes_dem" in data and data["votes_dem"] is not None) else 0)
        self.votes_rep = None if data is None else (data["votes_rep"] if ("votes_rep" in data and data["votes_rep"] is not None) else 0)
        self.votes_other = None if data is None else (data["votes_other"] if ("votes_other" in data and data["votes_other"] is not None) else 0)
        self.votes_scattered = None if data is None else (data["votes_scattered"] if ("votes_scattered" in data and data["votes_scattered"] is not None) else 0)
        self.votes_total = None if data is None else data["votes_total"]
        self.votes_wasted_dem = None
        self.votes_wasted_rep = None
        self.votes_wasted_net = None

        self.winner = {
            "party": None if data is None else (data['winner']['party'] if 'winner' in data else None),
            "last_name": None if data is None else (data['winner']['last_name'] if 'winner' in data else None),
            "first_name": None if data is None else (data['winner']['first_name'] if 'winner' in data else None),
        }

        if data is not None:
            self.calc_wasted_votes(self.votes_rep, self.votes_dem, self.votes_total)

    def calc_wasted_votes(self, votes_rep, votes_dem, votes_total):
        """Calculates the wasted votes of Republican and Democratic candidates

           A wasted vote is defined as one for the losing candidate or one for
           the winning candidate in excess of the number needed to win.

           Returns a dict of wasted votes for Rep and Dem candidates
        """
        try:
            if votes_total < votes_rep + votes_dem:
                raise utils.VotesError(votes_dem=self.votes_dem, votes_rep=self.votes_rep,
                    votes_total=self.votes_total, year=self.year, state=self.state,
                    legislative_body_code=self.legislative_body_code, district=self.district)

            votes_winner = max(votes_rep, votes_dem)
            votes_loser = min(votes_rep, votes_dem)
            majority_votes = math.floor(votes_total / 2) + 1

            votes_to_win = votes_winner if votes_winner < majority_votes else majority_votes
            winning_party = "rep" if votes_rep > votes_dem else "dem"
            votes_wasted_winner = votes_winner - votes_to_win

            self.votes_wasted_rep = votes_wasted_winner if winning_party == "rep" else votes_loser
            self.votes_wasted_dem = votes_wasted_winner if winning_party == "dem" else votes_loser
            self.votes_wasted_net = self.votes_wasted_dem - self.votes_wasted_rep

        except Exception as e:
            print('Error calculating wasted votes where votes_total={}, votes_rep={}, votes_dem={} for {} {} {}'.format(
                votes_total,
                votes_rep,
                votes_dem,
                self.state,
                self.district,
                self.year
            ))
            raise e
