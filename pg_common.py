# This module contains functions that are used in mutiple other modules

import csv # Required to output to CSV files
import dateutil.parser # Required to read the date in ISO-8601 format
from dateutil.tz import * # Required to shift the time from UTC to local timezone
from datetime import datetime # Required to output the date/time in the expected format

# Set the root URL for the Plangrid API
RootURL = "https://io.plangrid.com"

# A collection of sample or test projects that should be ignored
SampleProjects = [
    '0768258e-bac5-4788-a819-e8d441ae7484',
    'e239ce91-78c2-438a-97a6-9b2e83717ba2',
    'c3fc0b62-90ed-41cb-a063-d5adaad9056a',
    'd88ec57b-2896-4f75-bbdb-cb750c189dad'
]

# Takes a date string in ISO-8601 format, parses it as a python datetime object, shifts
#the timezone from UTC to the local timezone of the computer running this script, and 
#formats the time as MM/DD/YYYY H:M
def DateTime(sourcetime):
    return dateutil.parser.parse(sourcetime).astimezone(tzlocal()).strftime("%m/%d/%Y %H:%M")

# Manages safe writing to a CSV file
class CSV:
    def __init__(self, filename):
        self.outfile = open(filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    def Write(self, output):
        self.writer.writerow(output)

    def __del__(self):
        self.outfile.close()