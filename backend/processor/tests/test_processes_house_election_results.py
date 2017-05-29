import os
import unittest
import config
import election_results.utils as utils
from csv import reader
from processor.house_election_results import HouseElectionsProcessor as processor
from election_results.national import NationalElectionResults
from election_results.state import StateElectionResults
from election_results.district import DistrictElectionResults

class TestHouseElectionsProcessor(unittest.TestCase):

    def setUp(self):
        self.proc = processor()

    def tearDown(self):
        del self.proc

    def test_inits(self):
        self.assertEqual(self.proc.state_results, {})
        self.assertEqual(self.proc.current_state, None)
        self.assertEqual(self.proc.district_results, [])
        self.assertEqual(self.proc.current_district_results, {
            'votes_dem': 0,
            'votes_rep': 0,
            'votes_other': 0,
            'votes_scattered': 0,
            'votes_total': 0,
            'winner': {
                'party': '',
                'last_name': '',
                'first_name': ''
            }
        })
        self.assertEqual(self.proc.current_district, None)
        self.assertEqual(self.proc.legislative_body_code, 0)

    def test_converts_value_to_int_if_numeric(self):
        self.assertEqual(self.proc.to_int('01'), 1)
        self.assertEqual(self.proc.to_int('11'), 11)
        self.assertEqual(self.proc.to_int('123,456'), 123456)
        self.assertEqual(self.proc.to_int('H'), None)
        self.assertEqual(self.proc.to_int(''), None)

    def test_converts_00_districts_to_1(self):
        self.assertEqual(self.proc.to_int_district('00'), 1)
        self.assertEqual(self.proc.to_int_district('01'), 1)
        self.assertEqual(self.proc.to_int_district('11'), 11)
        self.assertEqual(self.proc.to_int_district('123,456'), 123456)
        self.assertEqual(self.proc.to_int_district('H'), None)
        self.assertEqual(self.proc.to_int_district(''), None)

    def test_sets_vote_counts_to_0_if_candidate_ran_unopposed(self):
        self.proc.to_int_votes('Unopposed')
        self.assertEqual(self.proc.current_district_results['votes_dem'], 0)
        self.assertEqual(self.proc.current_district_results['votes_rep'], 0)
        self.assertEqual(self.proc.current_district_results['votes_other'], 0)
        self.assertEqual(self.proc.current_district_results['votes_scattered'], 0)
        self.assertEqual(self.proc.current_district_results['votes_total'], 0)

    # def test_raises_exception_if_vote_value_has_unexpected_str_value(self):
    #     self.assertRaises(utils.ElectionResultsError, self.proc.to_int_votes, 'foo')

    def test_resets_current_district(self):
        self.proc.current_district = 1
        self.proc.current_district_results = {
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
        }

        self.proc.reset_current_district_results()
        self.assertEqual(self.proc.current_district_results, {
            'votes_dem': 0,
            'votes_rep': 0,
            'votes_other': 0,
            'votes_scattered': 0,
            'votes_total': 0,
            'winner': {
                'party': '',
                'last_name': '',
                'first_name': ''
            }
        })

    def test_resets_district_results(self):
        self.proc.districts_results = [
            DistrictElectionResults(year=2014, state='NY', legislative_body_code=0, district=1),
            DistrictElectionResults(year=2014, state='NY', legislative_body_code=0, district=2)
        ]

        self.proc.reset_district_results()
        self.assertEqual(self.proc.district_results, [])

    # def test_resets_state_and_district_results(self):
    #     self.proc.current_state = 'NY'
    #     self.proc.districts_results = [
    #         DistrictElectionResults(year=2014, state='NY', legislative_body_code=0, district=1),
    #         DistrictElectionResults(year=2014, state='NY', legislative_body_code=0, district=2)
    #     ]
    #
    #     self.proc.reset_state_and_district_results()
    #     self.assertEqual(self.proc.current_state, None)
    #     self.assertEqual(self.proc.district_results, [])

    def test_processes_election_results_csv(self):
        test_file = os.path.join(config.PATH_TO_HOUSE_ELECTION_RESULTS_DATA, "2014.csv")

        with open(test_file) as file:
            results = self.proc.process_election_results_csv(reader(file))

            self.assertIsInstance(results, NationalElectionResults)
            self.assertEqual(len(results.state_results.keys()), 50)
            self.assertTrue(results.votes_total_dem is not None)
            self.assertTrue(results.votes_total_rep is not None)
            self.assertTrue(results.votes_total_other is not None)
            self.assertTrue(results.votes_total_scattered is not None)
            self.assertTrue(results.votes_total is not None)
            self.assertTrue(results.votes_wasted_total_dem is not None)
            self.assertTrue(results.votes_wasted_total_rep is not None)
            self.assertTrue(results.votes_wasted_net is not None)

            for state_results in results.state_results.values():
                self.assertIsInstance(state_results, StateElectionResults)
                districts = state_results.districts_won_dem + state_results.districts_won_rep
                self.assertGreaterEqual(len(districts), 1)
                for district_results in districts:
                    self.assertIsInstance(district_results, DistrictElectionResults)
