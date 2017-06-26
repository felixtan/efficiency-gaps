import unittest
import election_results.utils as utils
from election_results.election_results import ElectionResults
from election_results.state import StateElectionResults
from election_results.national import NationalElectionResults

class TestNationalElectionResults(unittest.TestCase):

    def setUp(self):
        self.results = NationalElectionResults(year=2016, legislative_body_code=0)

    def tearDown(self):
        del self.results

    def test_inherits_from_ElectionResults(self):
        self.assertIsInstance(self.results, ElectionResults)

    def test_init(self):
        self.assertEqual(self.results.year, '2016')
        self.assertEqual(self.results.legislative_body_code, '0')

        self.assertEqual(self.results.votes_total_dem, None)
        self.assertEqual(self.results.votes_total_rep, None)
        self.assertEqual(self.results.votes_total_other, None)
        self.assertEqual(self.results.votes_total_scattered, None)
        self.assertEqual(self.results.votes_total, None)
        self.assertEqual(self.results.votes_wasted_total_dem, None)
        self.assertEqual(self.results.votes_wasted_total_rep, None)
        self.assertEqual(self.results.votes_wasted_net, None)
        self.assertEqual(self.results.state_results, {})

    def test_sets_state_to_None(self):
        self.assertEqual(self.results.state, None)

    def test_summarize_states_results(self):
        s1 = StateElectionResults(year='2016', state='AL', legislative_body_code=0, data={
            'votes_total_dem': 100,
            'votes_total_rep': 150,
            'votes_total_other': 20,
            'votes_total_scattered': 15,
            'votes_total': 270,
            'votes_wasted_total_dem': 50,
            'votes_wasted_total_rep': 45,
            'votes_wasted_net': 5
        })

        s2 = StateElectionResults(year='2016', state='AK', legislative_body_code=0, data={
            'votes_total_dem': 80,
            'votes_total_rep': 120,
            'votes_total_other': 10,
            'votes_total_scattered': 10,
            'votes_total': 210,
            'votes_wasted_total_dem': 40,
            'votes_wasted_total_rep': 30,
            'votes_wasted_net': 10
        })

        states = { 'AL': s1, 'AK': s2 }
        self.results.summarize_votes(states)
        self.assertEqual(self.results.votes_total_dem, 180)
        self.assertEqual(self.results.votes_total_rep, 270)
        self.assertEqual(self.results.votes_total_other, 30)
        self.assertEqual(self.results.votes_total_scattered, 25)
        self.assertEqual(self.results.votes_total, 480)
        self.assertEqual(self.results.votes_wasted_total_dem, 90)
        self.assertEqual(self.results.votes_wasted_total_rep, 75)
        self.assertEqual(self.results.votes_wasted_net, 15)
        self.assertEqual(self.results.votes_wasted_net, self.results.votes_wasted_total_dem - self.results.votes_wasted_total_rep)

    def test_raises_exception_if_StateElectionResults_year_does_not_match(self):
        s = StateElectionResults(year='2015', state='AL', legislative_body_code=0, data={
            'votes_total_dem': 0,
            'votes_total_rep': 0,
            'votes_total_other': 0,
            'votes_total_scattered': 0,
            'votes_total': 0,
            'votes_wasted_total_dem': 0,
            'votes_wasted_total_rep': 0,
            'votes_wasted_net': 0
        })
        self.assertRaises(utils.ElectionResultsError, self.results.summarize_votes, {'AL': s})

    def test_raises_exception_if_StateElectionResults_legislative_body_code_does_not_match(self):
        s = StateElectionResults(year='2016', state='AL', legislative_body_code=1, data={
            'votes_total_dem': 0,
            'votes_total_rep': 0,
            'votes_total_other': 0,
            'votes_total_scattered': 0,
            'votes_total': 0,
            'votes_wasted_total_dem': 0,
            'votes_wasted_total_rep': 0,
            'votes_wasted_net': 0
        })
        self.assertRaises(utils.ElectionResultsError, self.results.summarize_votes, {'AL': s})
