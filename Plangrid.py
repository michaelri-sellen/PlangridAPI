import requests, configparser, os, json

config = configparser.ConfigParser()
config.readfp(open('config.txt'))

API = "https://io.plangrid.com"
Header = {
    'Authorization': 'Bearer ' + config.get('Default', 'access_token'),
    'Accept': 'application/vnd.plangrid+json; version=1'
}

r = requests.get(API + '/projects', headers = Header)
j = json.loads(r.text)
print(json.dumps(j, indent=4, sort_keys=True))