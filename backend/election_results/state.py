from fixtures.states import states
from fixtures.legislative_body_codes import legislative_body_codes
import math

class StateElectionResults:
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
        votes_total_voided (Int) - Sum total votes counted but not applied to any candidate
        votes_total (Int) - Sum total votes for a candidate, not voided
        districts_won_dem (List) - List of DistrictElectionResults won by Democrats
        districts_won_rep (List) - List of DistrictElectionResults won by Republicans
        votes_wasted_total_dem (Int) - Sum total votes wasted in voting for a
            Democratic candidate
        votes_wasted_total_rep (Int) - Sum total votes wasted in voting for a
            Republican candidate
        votes_wasted_net (Int) - Net wasted votes; difference between the Democratic
            and Republican numbers
    """

    def __init__(self, year, state, legislative_body_code, data=None):
        """Initializes a StateElectionResults object

           Attibutes:
                year (Int) - The election year
                state (String) - Two-letter abbreviation of US state
                legislative_body_code (Int) - Int that maps to a legislative body
                data (Dict) - Contains the non-argument properties
        """
        pass
