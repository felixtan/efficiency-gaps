class DistrictElectionResults:
    """Stores election results
    """

    def __init__(self, year, state, legislative_body_code, district, data=None):
        self.year = year
        self.state = state
        self.legislative_body = legislative_body_code
        self.district = district

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
