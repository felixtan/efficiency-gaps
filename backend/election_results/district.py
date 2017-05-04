class DistrictElectionResults:
    """Stores election results
    """

    def __init__(self, year, state, political_body, district_num, data):
        self.year = year
        self.state = state
        self.political_body = political_body
        self.district_num = district_num

        self.votes_for_dem = data["votes_for_dem"]
        self.votes_for_rep = data["votes_for_rep"]
        self.votes_for_other = data["votes_for_other"]
        self.votes_scattered = data["votes_scattered"]

        self.winner = {
            party: data["winner_party"],
            last_name: data["winner_last_name"],
            first_name: data["winner_first_name"]
        }

        # For calculating efficiency gap
        self.votes_total_not_void = data["votes_total_not_void"]
        self.votes_wasted_winner = data["votes_wasted_winner"]
        self.votes_wasted_loser = data["votes_wasted_loser"]
        self.votes_wasted_net = data["votes_wasted_net"]
