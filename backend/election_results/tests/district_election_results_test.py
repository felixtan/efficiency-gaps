import unittest
import election_results.district import DistrictElectionResults as Results

class DistrictElectionResultsTest(unittest.TestCase):

    def setUp(self):
        self.results = Results()
