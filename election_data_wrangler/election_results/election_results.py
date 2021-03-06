"""Defines an abstract class for representing US legislative elections
"""

import abc
import election_results.utils as utils
from fixtures.states import states
from fixtures.legislative_body_codes import legislative_body_codes

class ElectionResults(abc.ABC):
    """Abstract class to be implemented by DistrictElectionResults and StateElectionResults

    Attributes:
        type (String) - Indicates whether it's for state or district
            'd' or 'district' for district
            's' or 'state' for state
        year (Int/String) - Election year
        state (String) - Two-letter US state abbreviation
        legislative_body_code (Int/String) - Number that maps to a legislative body
            See ../fixtures/legislative_body_codes.py
        district (Int/String) - Legislative district number
    """

    def __init__(self, type, year, legislative_body_code, state=None, district=None):
        """Initializes an ElectionResults object. Validates year, state,
            district and legislative_body_code.
        """

        if (type is None or
            (type != 'd' and
            type != 'district' and
            type != 's' and
            type != 'state' and
            type != 'n' and
            type != 'national')):
            raise utils.ElectionResultsError('Invalid type {}'.format(type))

        try:
            int(year)
            self.year = str(year)
        except ValueError as e:
            raise ValueError("Invalid year {}".format(year))

        try:
            if type == 'n' or type == 'national':
                self.state = None
            elif isinstance(state, str) and len(state) == 2 and state in states.keys():
                self.state = state
            else:
                raise utils.USStateError(state)
        except utils.USStateError as e:
            raise e

        try:
            code = str(legislative_body_code)
            if code in legislative_body_codes.keys():
                self.legislative_body_code = code
            else:
                raise utils.LegislativeBodyError(legislative_body_code)
        except utils.LegislativeBodyError as e:
            raise e

        try:
            if (type == 'd' or type == 'district') and district is not None and int(district) > 0:
                self.district = str(district)
            elif (type == 's' or type == 'state'):
                self.district = None
            elif (type == 'n' or type == 'national'):
                self.district = None
                self.state = None
            else:
                raise utils.DistrictError(district)
        except (utils.DistrictError, ValueError) as e:
            raise e
