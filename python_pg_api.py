# This module will perform API calls to the Plangrid API using the API key from
# the config.txt file and format the response as JSON

import requests # Required to make the API call
import configparser # Required to load the API key from config.txt
import json # Required to format API responses as JSON

# Initialize ConfigParser and open config.txt
config = configparser.ConfigParser()
config.readfp(open('config.txt'))

# Set authentication to the API key and Header to the default headers
auth = (config.get('Default', 'key'), '')
Header = {'Accept': 'application/vnd.plangrid+json; version=1'}

# Perform an API call to the provided URL and return the response as JSON
def APICall(URL):
    result = requests.get(URL, headers = Header, auth = auth)
    return json.loads(result.text)