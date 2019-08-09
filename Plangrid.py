import requests, configparser, os

config = configparser.ConfigParser()
config.readfp(open('config.txt'))

API = "https://io.plangrid.com/"
API_Key = config.get('Default', 'Key')
Headers = {'Accept': 'application/vnd.plangrid+json'}

r = requests.get(API, auth=(API_Key, ''), headers=Headers)
print(r.text)