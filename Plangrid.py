import requests, configparser, os

config = configparser.ConfigParser()
config.readfp(open('config.txt'))

API = "https://io.plangrid.com"
Header = {
    'Authorization': 'Bearer ' + config.get('Default', 'access_token'),
    'Accept': 'application/vnd.plangrid+json; version=1'
}

r = requests.get(API + '/projects', headers = Header)
print(r.text)