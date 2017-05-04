import csv
import pickle
import json

from backend.election_results.district import DistrictElectionResults

def to_int(x):
    try:
        return int(x.replace(",", ""))
    except ValueError:
        return None

# class ElectionResultsScraper:
def read(filepath):
    with open(filepath) as csvfile:
        if filepath.endswith(".csv") and "FEC" in filepath:
            file = csv.reader(csvfile)
            for rownum, rowdata in enumerate(file):
                if rownum == 0:
                    print(rowdata)
                else:
                    # column names
                    state_abbrev = rowdata[1]
                    state = rowdata[2]
                    district = to_int(rowdata[3])
                    fec_id = rowdata[4]
                    is_incumbent = rowdata[5] != ""
                    candidate_last_name = rowdata[6]
                    candidate_first_name = rowdata[7]
                    candidate_full_name = rowdata[8]        # ex. Doe, John
                    total_votes_label = rowdata[9]

                    if "District Votes" in total_votes_label:
                        total_votes = ge_votes

                    party_abbrev = rowdata[10]
                    ge_votes = to_int(rowdata[15])
                    combined_ge_party_totals = to_int(rowdata[19])

                    if party_abbrev == "D" and ge_votes is not None:
                        votes_for_dem = combined_ge_party_totals if combined_ge_party_totals is not None else ge_votes

                    if party_abbrev == "R" and ge_votes is not None:
                        votes_for_rep = combined_ge_party_totals if combined_ge_party_totals is not None else ge_votes

                    if party_abbrev != "D" and party_abbrev != "R" and ge_votes is not None:
                        votes_for_other = combined_ge_party_totals if combined_ge_party_totals is not None else ge_votes

                    def party_votes(party_abbrev):
                        if party_abbrev == "D":
                            return votes_for_dem
                        elif party_abbrev == "R":
                            return votes_for_rep
                        else:
                            return votes_for_other

                    if ge_votes is not None:
                        print("{}, {}, {}".format(rownum, party_abbrev, party_votes(party_abbrev)))

                    data = {

                    }
