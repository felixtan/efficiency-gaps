import unittest
from election_results.election_results import ElectionResults
from election_results.district import DistrictElectionResults as Results
import election_results.utils as utils

class DistrictElectionResultsTest(unittest.TestCase):

    def setUp(self):
        self.results = Results(year=2014, state='NY', legislative_body_code=0, district=1)

    def tearDown(self):
        del self.results

    def test_inherits_from_ElectionResults(self):
        self.assertIsInstance(self.results, ElectionResults)

    def test_init(self):
        self.assertEqual(self.results.year, '2014')
        self.assertEqual(self.results.state, 'NY')
        self.assertEqual(self.results.legislative_body_code, '0')
        self.assertEqual(self.results.district, '1')

        self.assertEqual(self.results.votes_dem, None)
        self.assertEqual(self.results.votes_rep, None)
        self.assertEqual(self.results.votes_other, None)
        self.assertEqual(self.results.votes_scattered, None)
        self.assertEqual(self.results.votes_total, None)
        self.assertEqual(self.results.winner['party'], None)
        self.assertEqual(self.results.winner['last_name'], None)
        self.assertEqual(self.results.winner['first_name'], None)

    def test_sets_votes_to_0_if_row_didnt_include_votes_for_a_party(self):
        # Happens in elections where a candidate ran unopposed
        data = {
            'votes_dem': 120,
            'votes_scattered': 10,
            'votes_total': 130
        }

        r = Results(year=2014, state='NY', legislative_body_code=0, district=1, data=data)

        self.assertEqual(r.votes_rep, 0)
        self.assertEqual(r.votes_other, 0)


        data = {
            'votes_rep': 120,
            'votes_scattered': 10,
            'votes_total': 130
        }

        r = Results(year=2014, state='NY', legislative_body_code=0, district=1, data=data)

        self.assertEqual(r.votes_dem, 0)
        self.assertEqual(r.votes_other, 0)

    # TODO: extract test cases out of this file into a separate fixtures file/dir
    def test_calculates_wasted_votes(self):
        wasted_votes = self.results.calc_wasted_votes(votes_rep=25, votes_dem=75, votes_total=100)

        self.assertEqual(self.results.votes_wasted_rep, 25)
        self.assertEqual(self.results.votes_wasted_dem, 24)
        self.assertEqual(self.results.votes_wasted_net, -1)

        wasted_votes = self.results.calc_wasted_votes(votes_rep=57, votes_dem=43, votes_total=100)
        self.assertEqual(self.results.votes_wasted_rep, 6)
        self.assertEqual(self.results.votes_wasted_dem, 43)
        self.assertEqual(self.results.votes_wasted_net, 37)

        wasted_votes = self.results.calc_wasted_votes(votes_rep=26, votes_dem=75, votes_total=101)
        self.assertEqual(self.results.votes_wasted_rep, 26)
        self.assertEqual(self.results.votes_wasted_dem, 24)
        self.assertEqual(self.results.votes_wasted_net, -2)

        wasted_votes = self.results.calc_wasted_votes(votes_rep=58, votes_dem=43, votes_total=101)
        self.assertEqual(self.results.votes_wasted_rep, 7)
        self.assertEqual(self.results.votes_wasted_dem, 43)
        self.assertEqual(self.results.votes_wasted_net, 36)

    def test_calculates_wasted_votes_if_total_votes_less_than_for_rep_plus_dem(self):
        wasted_votes = self.results.calc_wasted_votes(votes_rep=45, votes_dem=43, votes_total=100)
        self.assertEqual(self.results.votes_wasted_rep, 0)
        self.assertEqual(self.results.votes_wasted_dem, 43)
        self.assertEqual(self.results.votes_wasted_net, 43)

    # TODO: extract test cases out of this file into a separate fixtures file/dir
    def test_calculates_wasted_votes_raises_VotesError_if_total_votes_less_than_sum_of_reps_and_dems(self):
        self.assertRaises(utils.VotesError, self.results.calc_wasted_votes, votes_rep=58, votes_dem=43, votes_total=100)
        self.assertRaises(utils.VotesError, self.results.calc_wasted_votes, votes_rep=43, votes_dem=58, votes_total=100)
