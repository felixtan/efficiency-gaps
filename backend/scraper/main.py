#!/usr/bin/env python

import os
import sys
import scraper.election_results_scraper as scraper

if __name__ == "__main__":
    data_directory = sys.argv[1]

    for root, dirnames, filenames in os.walk(data_directory):
        for filename in filenames:
            print("Inside {}".format(root))
            print("Processing file \"{}\"...".format(filename))

            filepath = root + filename
            scraper.read(filepath)
