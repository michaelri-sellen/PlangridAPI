import csv, dateutil.parser
from dateutil.tz import *
from datetime import datetime

def ConvertDateTime(sourcetime):
    return dateutil.parser.parse(sourcetime).astimezone(tzlocal()).strftime("%m/%d/%Y %H:%M")

class CSV:
    def __init__(self, filename):
        self.outfile = open(filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    def Write(self, output):
        self.writer.writerow(output)

    def __del__(self):
        self.outfile.close()