# This module contains functions that are used in mutiple other modules

import csv # Required to output to CSV files
import dateutil.parser # Required to read the date in ISO-8601 format
from dateutil.tz import * # Required to shift the time from UTC to local timezone
from datetime import datetime # Required to output the date/time in the expected format

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