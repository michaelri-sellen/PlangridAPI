import requests, configparser, os, json
import Oauth

# Initialize ConfigParser
config = configparser.ConfigParser()
config.readfp(open('config.txt'))

# Set default variables
API = "https://io.plangrid.com"
DemoMode = 'oauth'

def RunDemo():
    r = ''
    if DemoMode == 'oauth':
        if len(config.get('Default', 'access_token')) == 0:
            Oauth.GetTokens()

        Header = {
            'Authorization': 'Bearer ' + config.get('Default', 'access_token'),
            'Accept': 'application/vnd.plangrid+json; version=1'
        }

        r = requests.get(API + '/projects', headers = Header)
    elif DemoMode == 'apikey':
        Header = {
            'Accept': 'application/vnd.plangrid+json; version=1'
        }

        r = requests.get(API + '/projects', headers = Header, auth = (config.get('Default', 'key'), ''))
    
    if r != '':
        j = json.loads(r.text)
        print(json.dumps(j, indent=4, sort_keys=True))        
