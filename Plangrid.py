import requests, configparser, os

config = configparser.ConfigParser()
config.readfp(open('config.txt'))

API = "https://io.plangrid.com"
OauthURL = "/oath/authorize"
TokenURL = "/oath/token"
API_Key = config.get('Default', 'Key')
Client_ID = config.get('Default', 'ClientID')
Client_Secret = config.get('Default', 'ClientSecret')
Headers = {'Accept': 'application/vnd.plangrid+json; version=1'}

r = requests.get(API + OauthURL + '?response_type=code&client_id=' + Client_ID + '&state=1&scope=write:projects')
print(r.text)