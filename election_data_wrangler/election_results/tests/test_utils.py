import unittest
import election_results.utils as utils

class TestElectionResultsUtils(unittest.TestCase):

    def test_VotesError_requires_all_arguments(self):
        self.assertRaises(TypeError, utils.VotesError,
            votes_dem=0, votes_rep=0, votes_total=0,
            year=0, state='NY', legislative_body_code=0)

        self.assertRaises(TypeError, utils.VotesError,
            votes_dem=0, votes_rep=0, votes_total=0,
            year=0, state='NY', district=1)

        self.assertRaises(TypeError, utils.VotesError,
            votes_dem=0, votes_rep=0, votes_total=0,
            year=0, legislative_body_code=0, district=1)

        self.assertRaises(TypeError, utils.VotesError,
            votes_dem=0, votes_rep=0, votes_total=0,
            state='NY', legislative_body_code=0, district=1)

        self.assertRaises(TypeError, utils.VotesError,
            votes_dem=0, votes_rep=0,
            year=0, state='NY', legislative_body_code=0, district=1)

        self.assertRaises(TypeError, utils.VotesError,
            votes_dem=0, votes_total=0,
            year=0, state='NY', legislative_body_code=0, district=1)

        self.assertRaises(TypeError, utils.VotesError,
            votes_rep=0, votes_total=0,
            year=0, state='NY', legislative_body_code=0, district=1)

    def test_VotesError_stores_information_about_the_error(self):
        e = utils.VotesError(votes_dem=0, votes_rep=0, votes_total=0,
            year=0, state='NY', legislative_body_code=0, district=1)

        self.assertEqual(e.votes_dem, 0)
        self.assertEqual(e.votes_rep, 0)
        self.assertEqual(e.votes_total, 0)
        self.assertEqual(e.year, 0)
        self.assertEqual(e.state, 'NY')
        self.assertEqual(e.legislative_body_code, 0)
        self.assertEqual(e.district, 1)

    def test_USStateError_stores_information_about_the_error(self):
        e = utils.USStateError(state='NT')
        self.assertEqual(e.state, 'NT')

    def test_LegislativeBodyError_stores_information_about_the_error(self):
        e = utils.LegislativeBodyError(legislative_body_code=3)
        self.assertEqual(e.legislative_body_code, 3)

    def test_DistrictError_stores_information_about_the_error(self):
        e = utils.DistrictError(district=-1)
        self.assertEqual(e.district, -1)
