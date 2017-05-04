import unittest
from election_results.district import DistrictElectionResults as Results

class DistrictElectionResultsTest(unittest.TestCase):

    def setUp(self):
        self.results = Results(year=2014, state='NY', legislative_body_code=0, district=1)

    def tearDown(self):
        del self.results

    def test_init(self):
        self.assertEqual(self.results.year, 2014)
        self.assertEqual(self.results.state, 'NY')
        self.assertEqual(self.results.legislative_body, "US House")
        self.assertEqual(self.results.district, 1)

        self.assertEqual(self.results.votes_dem, None)
        self.assertEqual(self.results.votes_rep, None)
        self.assertEqual(self.results.votes_other, None)
        self.assertEqual(self.results.votes_voided, None)
        self.assertEqual(self.results.votes_total, None)
        self.assertEqual(self.results.winner.party, None)
        self.assertEqual(self.results.winner.last_name, None)
        self.assertEqual(self.results.winner.first_name, None)

    def test_raises_exception_if_invalid_state(self):
        self.assertRaises(Exception, Results, state='AB', year=2014, legislative_body_code=0, district=1)
        self.assertRaises(Exception, Results, state='BC', year=2014, legislative_body_code=0, district=1)
        self.assertRaises(Exception, Results, state='YZ', year=2014, legislative_body_code=0, district=1)
        self.assertRaises(Exception, Results, state=1, year=2014, legislative_body_code=0, district=1)
        self.assertRaises(Exception, Results, year=2014, legislative_body_code=0, district=1)

    def test_raises_exception_if_invalid_legislative_body_code(self):
        self.assertRaises(Exception, Results, legislative_body_code=3, year=2014, state='NY', district=1)
        self.assertRaises(Exception, Results, year=2014, state='NY', district=1)

    def test_raises_exception_if_invalid_district(self):
        self.assertRaises(Exception, Results, district='1', year=2014, state='NY', legislative_body_code=0)
        self.assertRaises(Exception, Results, year=2014, state='NY', legislative_body_code=0)

    # TODO: extract test cases out of this file into a separate fixtures file/dir
    def test_calculates_wasted_votes(self):
        wasted_votes = self.results.calc_wasted_votes(votes_rep=25, votes_dem=75, votes_total=100)
        self.assertEquals(wasted_votes.rep, 25)
        self.assertEquals(wasted_votes.dem, 24)
        self.assertEquals(wasted_votes.net, -1)

        wasted_votes = self.results.calc_wasted_votes(votes_rep=57, votes_dem=43, votes_total=100)
        self.assertEquals(wasted_votes.rep, 6)
        self.assertEquals(wasted_votes.dem, 43)
        self.assertEquals(wasted_votes.net, 37)

        wasted_votes = self.results.calc_wasted_votes(votes_rep=26, votes_dem=75, votes_total=101)
        self.assertEquals(wasted_votes.rep, 26)
        self.assertEquals(wasted_votes.dem, 24)
        self.assertEquals(wasted_votes.net, -2)

        wasted_votes = self.results.calc_wasted_votes(votes_rep=58, votes_dem=43, votes_total=101)
        self.assertEquals(wasted_votes.rep, 7)
        self.assertEquals(wasted_votes.dem, 43)
        self.assertEquals(wasted_votes.net, 36)

    # TODO: extract test cases out of this file into a separate fixtures file/dir
    def test_calculates_wasted_votes_raises_exception_if_votes_dont_add_up(self):
        self.assertRaises(Exception, self.results.calc_wasted_votes, votes_rep=58, votes_dem=43, votes_total=100)
        self.assertRaises(Exception, self.results.calc_wasted_votes, votes_rep=43, votes_dem=58, votes_total=100)
