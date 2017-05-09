from fixtures.states import states
from fixtures.legislative_body_codes import legislative_body_codes
import math
from warnings import warn

class DistrictElectionResults:
    """Stores election results for a legislative district
    """

    def __init__(self, year, state, legislative_body_code, district, data=None):

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
        if not isinstance(state_abbrev, str):
            raise TypeError("state abbrev has invalid type {}, must be str".format(type(state_abbrev)))

        if len(state_abbrev) > 2:
            raise NameError("Invalid state abbrev: {}, must be 2 letters".format(state_abbrev))

        # states = json.load(states_json)
        return state_abbrev in states.keys()

    def is_valid_legislative_body_code(self, code):
        if not isinstance(code, int):
            raise TypeError("legislative body code has invalid type {}".format(type(code)))

        # bodies = json.load(legislative_body_codes_json)
        return code in legislative_body_codes.keys()

    def calc_wasted_votes(self, votes_rep, votes_dem, votes_total):
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
