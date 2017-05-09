from fixtures.states import states
from fixtures.legislative_body_codes import legislative_body_codes
import math
from warnings import warn

class DistrictElectionResults:
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
        votes_voided (Int) - Number of votes that were invalid and not applied to
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
        try:
            if isinstance(year, int):
                self.year = year
            else:
                raise TypeError("Year has invalid type {}".format(type(year)))
        except TypeError as error:
            raise error

        try:
            is_valid_state = self.is_valid_state(state)
            if is_valid_state:
                self.state = state
            else:
                raise NameError("No such state with abbrev {}".format(state))
        except (TypeError, NameError) as error:
            raise error

        try:
            is_valid_legislative_body_code = self.is_valid_legislative_body_code(legislative_body_code)
            if is_valid_legislative_body_code:
                self.legislative_body_code = legislative_body_code
            else:
                raise IndexError("Invalid legislative body code {}".format(legislative_body_code))
        except (IndexError, TypeError) as error:
            raise error

        try:
            if isinstance(district, int):
                self.district = district
            else:
                raise TypeError("district has invalid type {}, must be int".format(type(district)))
        except TypeError as error:
            raise error


        self.votes_dem = None if data is None else data["votes_dem"]
        self.votes_rep = None if data is None else data["votes_rep"]
        self.votes_other = None if data is None else data["votes_other"]
        self.votes_voided = None if data is None else data["votes_voided"]
        self.votes_total = None if data is None else data["votes_total"]

        self.votes_wasted_dem = None if data is None else data["votes_wasted_dem"]
        self.votes_wasted_rep = None if data is None else data["votes_wasted_rep"]
        self.votes_wasted_net = None if data is None else data["votes_wasted_net"]

        self.winner = {
            "party": None if data is None else data["winner_party"],
            "last_name": None if data is None else data["winner_last_name"],
            "first_name": None if data is None else data["winner_first_name"]
        }

    def is_valid_state(self, state_abbrev):
        """Returns true if state_abbrev is a US state abbreviation, else false

           See ../fixtures/states.py
        """
        if not isinstance(state_abbrev, str):
            raise TypeError("state abbrev has invalid type {}, must be str".format(type(state_abbrev)))

        if len(state_abbrev) > 2:
            raise NameError("Invalid state abbrev: {}, must be 2 letters".format(state_abbrev))

        return state_abbrev.upper() in states.keys()

    def is_valid_legislative_body_code(self, code):
        """Returns true if code maps to a legislative body, else false

           See ../fixtures/legislative_body_codes.py
        """
        if not isinstance(code, int):
            raise TypeError("legislative body code has invalid type {}".format(type(code)))

        return str(code) in legislative_body_codes.keys()

    def calc_wasted_votes(self, votes_rep, votes_dem, votes_total):
        """Calculates the wasted votes of Republican and Democratic candidates

           A wasted vote is defined as one for the losing candidate or one for
           the winning candidate in excess of the number needed to win.
        """
        if votes_total > votes_rep + votes_dem:
            votes_total = votes_rep + votes_dem
            warn("Total votes is greater than the sum of votes for Reps and Dems")
        elif votes_total < votes_rep + votes_dem:
            raise ArithmeticError("Total votes is less than the sum of votes for Reps and Dems")

        votes_to_win = math.floor(votes_total / 2) + 1
        winning_party = "rep" if votes_rep > votes_dem else "dem"

        votes_wasted_winner = max(votes_rep, votes_dem) - votes_to_win
        votes_wasted_loser = min(votes_rep, votes_dem)

        votes_wasted_rep = votes_wasted_winner if winning_party == "rep" else votes_wasted_loser
        votes_wasted_dem = votes_wasted_winner if winning_party == "dem" else votes_wasted_loser
        votes_wasted_net = votes_wasted_dem - votes_wasted_rep

        return {
            "rep": votes_wasted_rep,
            "dem": votes_wasted_dem,
            "net": votes_wasted_net
        }
