import requests, configparser, json

# Initialize ConfigParser
config = configparser.ConfigParser()
config.readfp(open('config.txt'))

# Set default variables
auth = (config.get('Default', 'key'), '')
Header = {'Accept': 'application/vnd.plangrid+json; version=1'}

def APICall(URL):
    result = requests.get(URL, headers = Header, auth = auth)
    return json.loads(result.text)