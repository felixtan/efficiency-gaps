import unittest
import election_results.utils as utils
from election_results.election_results import ElectionResults as Results

class TestElectionResults(unittest.TestCase):

    def test_raises_exception_if_type_is_district_and_number_is_None(self):
        self.assertRaises(utils.DistrictError, Results, type='d', year=2014, state='NY', legislative_body_code=0)

    def test_raises_exception_if_type_is_state_and_district_is_not_None(self):
        self.assertRaises(utils.USStateError, Results, type='s', year=2014, state='NY', legislative_body_code=0, district=1)

    def test_sets_state_only_if_abbrev_is_valid(self):
        # Invalid
        self.assertRaises(utils.USStateError, Results, state='AB', type='s', year=2014, legislative_body_code=0)
        self.assertRaises(utils.USStateError, Results, state='CE', type='s', year=2014, legislative_body_code=0)
        self.assertRaises(utils.USStateError, Results, state='IO', type='s', year=2014, legislative_body_code=0)
        self.assertRaises(utils.USStateError, Results, state='KA', type='s', year=2014, legislative_body_code=0)
        self.assertRaises(utils.USStateError, Results, state='MN', type='s', year=2014, legislative_body_code=0)
        self.assertRaises(utils.USStateError, Results, state='NB', type='d', year=2014, legislative_body_code=0, district=1)
        self.assertRaises(utils.USStateError, Results, state='NW', type='d', year=2014, legislative_body_code=0, district=1)
        self.assertRaises(utils.USStateError, Results, state='OI', type='d', year=2014, legislative_body_code=0, district=1)
        self.assertRaises(utils.USStateError, Results, state='SA', type='d', year=2014, legislative_body_code=0, district=1)
        self.assertRaises(utils.USStateError, Results, state='TE', type='d', year=2014, legislative_body_code=0, district=1)
        self.assertRaises(utils.USStateError, Results, state='WS', type='d', year=2014, legislative_body_code=0, district=1)

        # Valid
        r = Results(type='d', state='NY', year=2014, legislative_body_code=0, district=1)
        self.assertEqual(r.state, 'NY')

        r = Results(type='d', state='AL', year=2014, legislative_body_code=0, district=1)
        self.assertEqual(r.state, 'AL')

        r = Results(type='s', state='OH', year=2014, legislative_body_code=0)
        self.assertEqual(r.state, 'OH')

        r = Results(type='s', state='KY', year=2014, legislative_body_code=0)
        self.assertEqual(r.state, 'KY')

    def test_sets_year_only_if_valid(self):
        # Invalid
        self.assertRaises(ValueError, Results, year='foo', type='d', state='NY', legislative_body_code=0, district=1)
        self.assertRaises(ValueError, Results, year='bar', type='s', state='NY', legislative_body_code=0)

        # Valid
        r = Results(year=1990, type='d', state='NY', legislative_body_code=0, district=1)
        self.assertEqual(r.state, '1990')

        r = Results(year='2161', type='d', state='NY', legislative_body_code=0, district=1)
        self.assertEqual(r.state, '2161')

    def test_sets_legislative_body_code_only_if_valid(self):
        # Invalid
        self.assertRaises(utils.LegislativeBodyError, Results, legislative_body_code=-1, type='d', year=2000, state='NY', district=1)
        self.assertRaises(utils.LegislativeBodyError, Results, legislative_body_code=3, type='s', year=2010, state='NY')

        # Valid
        r = Results(year=1990, type='d', state='NY', legislative_body_code=0, district=1)
        self.assertEqual(r.legislative_body_code, '0')

        r = Results(year=1990, type='d', state='NY', legislative_body_code='1', district=1)
        self.assertEqual(r.legislative_body_code, '1')

    def test_sets_district_only_if_valid(self):
        # Invalid
        self.assertRaises(utils.DistrictError, Results, district=0, legislative_body_code=-1, type='d', state='NY', year=2000)
        self.assertRaises(utils.DistrictError, Results, district=-1, legislative_body_code=-1, type='d', state='NY', year=2000)

        # Valid
        utils.set_district_if_valid(results=self.results, district='1')
        self.assertEqual(self.results.district, '1')

        utils.set_district_if_valid(results=self.results, district=999)
        self.assertEqual(self.results.district, '999')
