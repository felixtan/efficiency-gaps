import unittest
from election_results.state import StateElectionResults
from election_results.district import DistrictElectionResults

class StateElectionResultsTest(unittest.TestCase):

    def setUp(self):
        self.results = StateElectionResults(year=2014, state='NY', legislative_body_code=0, data=None)

    def tearDown(self):
        del self.results

    def test_init(self):
        self.assertEqual(self.results.year, 2014)
        self.assertEqual(self.results.state, 'NY')
        self.assertEqual(self.results.legislative_body_code, 0)

        self.assertEqual(self.results.votes_total_dem, None)
        self.assertEqual(self.results.votes_total_rep, None)
        self.assertEqual(self.results.votes_total_other, None)
        self.assertEqual(self.results.votes_total_voided, None)
        self.assertEqual(self.results.votes_total, None)
        self.assertEqual(self.results.districts_won_dem, [])
        self.assertEqual(self.results.districts_won_rep, [])
        self.assertEqual(self.results.votes_wasted_total_dem, None)
        self.assertEqual(self.results.votes_wasted_total_rep, None)
        self.assertEqual(self.results.votes_wasted_total, None)

    def test_raises_exception_if_invalid_state(self):
        self.assertRaises(Exception, StateElectionResults, state='AB', year=2014, legislative_body_code=0)
        self.assertRaises(Exception, StateElectionResults, state='BC', year=2014, legislative_body_code=0)
        self.assertRaises(Exception, StateElectionResults, state='YZ', year=2014, legislative_body_code=0)
        self.assertRaises(TypeError, StateElectionResults, state=1, year=2014, legislative_body_code=0)
        self.assertRaises(Exception, StateElectionResults, year=2014, legislative_body_code=0)

    def test_raises_exception_if_invalid_legislative_body_code(self):
        self.assertRaises(Exception, StateElectionResults, legislative_body_code=3, year=2014, state='NY')
        self.assertRaises(Exception, StateElectionResults, year=2014, state='NY')

    # TODO: extract test cases out of this file into a separate fixtures file/dir
    def test_summarize_votes(self):
        dist1 = DistrictElectionResults(year=2014, state='NY', legislative_body_code=1, district=1, data={
            votes_dem: 75,
            votes_rep: 25,
            votes_other: 0,
            votes_voided: 0,
            votes_total: 100,
            votes_wasted_dem: 24,
            votes_wasted_rep: 25,
            votes_wasted_net: -1
        })

        dist2 = DistrictElectionResults(year=2014, state='NY', legislative_body_code=1, district=2, data={
            votes_dem: 60,
            votes_rep: 40,
            votes_other: 0,
            votes_voided: 0,
            votes_total: 100,
            votes_wasted_dem: 9,
            votes_wasted_rep: 40,
            votes_wasted_net: -31
        })

        dist3 = DistrictElectionResults(year=2014, state='NY', legislative_body_code=1, district=3, data={
            votes_dem: 43,
            votes_rep: 57,
            votes_other: 0,
            votes_voided: 0,
            votes_total: 100,
            votes_wasted_dem: 43,
            votes_wasted_rep: 6,
            votes_wasted_net: 37
        })

        dist4 = DistrictElectionResults(year=2014, state='NY', legislative_body_code=1, district=4, data={
            votes_dem: 48,
            votes_rep: 52,
            votes_other: 0,
            votes_voided: 0,
            votes_total: 100,
            votes_wasted_dem: 48,
            votes_wasted_rep: 1,
            votes_wasted_net: 47
        })

        dist5 = DistrictElectionResults(year=2014, state='NY', legislative_body_code=1, district=5, data={
            votes_dem: 49,
            votes_rep: 51,
            votes_other: 0,
            votes_voided: 0,
            votes_total: 100,
            votes_wasted_dem: 49,
            votes_wasted_rep: 0,
            votes_wasted_net: 49
        })

        districts = [dist1, dist2, dist3, dist4, dist5]

        summary = self.results.summarize_votes(districts)

        self.assertEqual(summary.votes_total_dem, 275)
        self.assertEqual(summary.votes_total_rep, 225)
        self.assertEqual(summary.votes_wasted_total_dem, 173)
        self.assertEqual(summary.votes_wasted_total_rep, 72)
        self.assertEqual(summary.votes_wasted_net, 101)
        self.assertEqual(summary.votes_total_other, 0)
        self.assertEqual(summary.votes_total_voided, 0)
        self.assertEqual(summary.votes_total_, 500)

    # TODO: extract test cases out of this file into a separate fixtures file/dir
    def calc_eff_gap(self):
        self.assertEqual(self.calc_eff_gap(votes_total=500, votes_wasted_net=101), 0.202)
