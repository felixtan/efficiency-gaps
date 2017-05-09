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
        self.assertEqual(self.results.year, 2014)
        self.assertEqual(self.results.state, 'NY')
        self.assertEqual(self.results.legislative_body_code, 0)
        self.assertEqual(self.results.district, 1)

        self.assertEqual(self.results.votes_dem, None)
        self.assertEqual(self.results.votes_rep, None)
        self.assertEqual(self.results.votes_other, None)
        self.assertEqual(self.results.votes_voided, None)
        self.assertEqual(self.results.votes_total, None)
        self.assertEqual(self.results.winner['party'], None)
        self.assertEqual(self.results.winner['last_name'], None)
        self.assertEqual(self.results.winner['first_name'], None)

    # TODO: extract test cases out of this file into a separate fixtures file/dir
    def test_calculates_wasted_votes(self):
        wasted_votes = self.results.calc_wasted_votes(votes_rep=25, votes_dem=75, votes_total=100)

        self.assertEqual(wasted_votes['rep'], 25)
        self.assertEqual(wasted_votes['dem'], 24)
        self.assertEqual(wasted_votes['net'], -1)

        wasted_votes = self.results.calc_wasted_votes(votes_rep=57, votes_dem=43, votes_total=100)
        self.assertEqual(wasted_votes['rep'], 6)
        self.assertEqual(wasted_votes['dem'], 43)
        self.assertEqual(wasted_votes['net'], 37)

        wasted_votes = self.results.calc_wasted_votes(votes_rep=26, votes_dem=75, votes_total=101)
        self.assertEqual(wasted_votes['rep'], 26)
        self.assertEqual(wasted_votes['dem'], 24)
        self.assertEqual(wasted_votes['net'], -2)

        wasted_votes = self.results.calc_wasted_votes(votes_rep=58, votes_dem=43, votes_total=101)
        self.assertEqual(wasted_votes['rep'], 7)
        self.assertEqual(wasted_votes['dem'], 43)
        self.assertEqual(wasted_votes['net'], 36)

    # TODO: extract test cases out of this file into a separate fixtures file/dir
    def test_calculates_wasted_votes_raises_exception_if_votes_dont_add_up(self):
        self.assertRaises(utils.VotesError, self.results.calc_wasted_votes, votes_rep=58, votes_dem=43, votes_total=100)
        self.assertRaises(utils.VotesError, self.results.calc_wasted_votes, votes_rep=43, votes_dem=58, votes_total=100)
