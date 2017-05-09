import unittest
from entities.state import State

class TestState(unittest.TestCase):

    def test_init(self):
        s = State(abbrev='NY')
        self.assertEqual(s.abbrev, 'NY')
        self.assertEqual(s.name, 'New York')
        self.congressional_election_results = {}
