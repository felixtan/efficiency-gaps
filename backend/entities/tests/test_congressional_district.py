import unittest
from entities.congressional_district import District

class TestCongressionalDistrict(unittest.TestCase):

    def test_init(self):
        d = District(number=1, state='NY', legislative_body_code=0)
        self.assertEqual(d.number, 1)
        self.assertEqual(d.number, 'NY')
        self.assertEqual(d.legislative_body, 'US House')
        self.election_results = {}

    def test_raises_exception_if_invalid_district_number(self):
        self.assertRaises(TypeError, District, number='1', state='NY', legislative_body_code=0)

    def test_raises_exception_if_invalid_state(self):
        self.assertRaises(TypeError, District, state='NB', number=1, legislative_body_code=0)

    def test_raises_exception_if_invalid_legislative_body_code(self):
        self.assertRaises(TypeError, District, legislative_body_code=3, number=1, state='NY')
