import unittest
from entities.state import State

class TestState(unittest.TestCase):

    def test_init(self):
        d = State(abbrev='NY')
        self.assertEqual(d.abbrev, 'NY')
        self.assertEqual(d.name, 'New York')
        self.congressional_election_results = {}

    def test_raises_exception_if_invalid_abbrev(self):
        self.assertRaises(Exception, State, abbrev='NB')
