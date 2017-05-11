"""Custom errors for ElectionResults
"""

class ElectionResultsError(Exception):
    """Exception for errors raise by ElectionResults"""
    def __init__(self, msg):
        super(ElectionResultsError, self).__init__(msg)

class VotesError(ElectionResultsError):
    """Exception for errors raised in counting votes in election results
    """

    def __init__(self, votes_dem, votes_rep, votes_total,
        year, state, legislative_body_code, district):

        msg = "Sum of votes for dem(={dem}) and rep(={rep}) is greater than \
            total(={total})".format(dem=votes_dem, rep=votes_rep, total=votes_total)

        super(__class__, self).__init__(msg)

        self.votes_dem = votes_dem
        self.votes_rep = votes_rep
        self.votes_total = votes_total
        self.year = year
        self.state = state
        self.legislative_body_code = legislative_body_code
        self.district = district

class USStateError(ElectionResultsError):
    """Exception for errors raised in validating US states
    """

    def __init__(self, state):
        msg = "There is no such state with the two-letter abbreviation {}".format(state)
        super(__class__, self).__init__(msg)
        self.state = state

class LegislativeBodyError(ElectionResultsError):
    """Exception for errors raised in validating legislative body code
    """

    def __init__(self, legislative_body_code):
        msg = """Invalid legislative body code {}
            Valid options
                0 - US House of Representatives
                1 - State Legislature Upper House
                2 - State Legislature Lower House
        """.format(legislative_body_code)

        super(__class__, self).__init__(msg)
        self.legislative_body_code = legislative_body_code

class DistrictError(ElectionResultsError):
    """Exception for errors raised in validating district numbers
    """

    def __init__(self, district):
        msg = "Invalid district number {}".format(district)
        super(__class__, self).__init__(msg)
        self.district = district
