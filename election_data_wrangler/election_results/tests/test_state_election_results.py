import unittest
from election_results.election_results import ElectionResults
from election_results.state import StateElectionResults
from election_results.district import DistrictElectionResults

class StateElectionResultsTest(unittest.TestCase):

    def setUp(self):
        self.results = StateElectionResults(year=2014, state='NY', legislative_body_code=0, data=None)

    def tearDown(self):
        del self.results

    def test_inherits_from_ElectionResults(self):
        self.assertIsInstance(self.results, ElectionResults)

    def test_init(self):
        self.assertEqual(self.results.year, '2014')
        self.assertEqual(self.results.state, 'NY')
        self.assertEqual(self.results.legislative_body_code, '0')

        self.assertEqual(self.results.votes_total_dem, None)
        self.assertEqual(self.results.votes_total_rep, None)
        self.assertEqual(self.results.votes_total_other, None)
        self.assertEqual(self.results.votes_total_scattered, None)
        self.assertEqual(self.results.votes_total, None)
        self.assertEqual(self.results.votes_wasted_total_dem, None)
        self.assertEqual(self.results.votes_wasted_total_rep, None)
        self.assertEqual(self.results.votes_wasted_net, None)
        self.assertEqual(self.results.districts_won_dem, [])
        self.assertEqual(self.results.districts_won_rep, [])

    # TODO: extract test cases out of this file into a separate fixtures file/dir
    def test_calculates_the_efficiency_gap(self):
        eff_gap = self.results.calc_eff_gap(votes_total=500, votes_wasted_net=101)
        self.assertEqual(eff_gap, 0.202)

    # TODO: extract test cases out of this file into a separate fixtures file/dir
    def test_summarize_votes(self):
        dist1 = DistrictElectionResults(year=2014, state='NY', legislative_body_code=1, district=1, data={
            'votes_dem': 75,
            'votes_rep': 25,
            'votes_other': 0,
            'votes_scattered': 0,
            'votes_total': 100,
            'votes_wasted_dem': 24,
            'votes_wasted_rep': 25,
            'votes_wasted_net': -1,
            'winner': {
                'party': 'rep',
                'first_name': 'foo',
                'last_name': 'bar'
            }
        })

        dist2 = DistrictElectionResults(year=2014, state='NY', legislative_body_code=1, district=2, data={
            'votes_dem': 60,
            'votes_rep': 40,
            'votes_other': 0,
            'votes_scattered': 0,
            'votes_total': 100,
            'votes_wasted_dem': 9,
            'votes_wasted_rep': 40,
            'votes_wasted_net': -31,
            'winner': {
                'party': 'dem',
                'first_name': 'foo',
                'last_name': 'bar'
            }
        })

        dist3 = DistrictElectionResults(year=2014, state='NY', legislative_body_code=1, district=3, data={
            'votes_dem': 43,
            'votes_rep': 57,
            'votes_other': 0,
            'votes_scattered': 0,
            'votes_total': 100,
            'votes_wasted_dem': 43,
            'votes_wasted_rep': 6,
            'votes_wasted_net': 37,
            'winner': {
                'party': 'rep',
                'first_name': 'foo',
                'last_name': 'bar'
            }
        })

        dist4 = DistrictElectionResults(year=2014, state='NY', legislative_body_code=1, district=4, data={
            'votes_dem': 48,
            'votes_rep': 52,
            'votes_other': 0,
            'votes_scattered': 0,
            'votes_total': 100,
            'votes_wasted_dem': 48,
            'votes_wasted_rep': 1,
            'votes_wasted_net': 47,
            'winner': {
                'party': 'dem',
                'first_name': 'foo',
                'last_name': 'bar'
            }
        })

        dist5 = DistrictElectionResults(year=2014, state='NY', legislative_body_code=1, district=5, data={
            'votes_dem': 49,
            'votes_rep': 51,
            'votes_other': 0,
            'votes_scattered': 0,
            'votes_total': 100,
            'votes_wasted_dem': 49,
            'votes_wasted_rep': 0,
            'votes_wasted_net': 49,
            'winner': {
                'party': 'rep',
                'first_name': 'foo',
                'last_name': 'bar'
            }
        })

        districts_results = [dist1, dist2, dist3, dist4, dist5]

        self.results.summarize_votes(districts_results)

        self.assertEqual(self.results.votes_total_dem, 275)
        self.assertEqual(self.results.votes_total_rep, 225)
        self.assertEqual(self.results.votes_wasted_total_dem, 173)
        self.assertEqual(self.results.votes_wasted_total_rep, 72)
        self.assertEqual(self.results.votes_wasted_net, 101)
        self.assertEqual(self.results.votes_total_other, 0)
        self.assertEqual(self.results.votes_total_scattered, 0)
        self.assertEqual(self.results.votes_total, 500)
        self.assertEqual(self.results.efficiency_gap, 0.202)
        self.assertEqual(len(self.results.districts_won_rep), 3)
        self.assertEqual(len(self.results.districts_won_dem), 2)
