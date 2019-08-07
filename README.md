#LinkedinSearch to csv

Script that scraps linkedin search and builds csv file with results.
Note: does not avoid recaptchas!


#pre-requisites

python 2.7

selenium for python

firefox

selenium firefox driver


#usage

Usage: python main.py email password search_url filename

Example: python main.py "your@email.com" "your_password" "https://www.linkedin.com/search/results/people/?keywords=neurosurgeon&origin=GLOBAL_SEARCH_HEADER" "results.csv"
