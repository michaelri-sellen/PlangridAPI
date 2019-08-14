import requests, configparser, os, json

config = configparser.ConfigParser()
config.readfp(open('config.txt'))

API = "https://io.plangrid.com"
OauthURL = "/oauth/authorize"
TokenURL = "/oauth/token"
API_Key = config.get('Default', 'Key')
Client_ID = config.get('Default', 'ClientID')
Client_Secret = config.get('Default', 'ClientSecret')
#Authorization_Code = config.get('Default', 'AuthCode')
RequestAccessTokenHeader = {'Content-Type': 'application/x-www-form-urlencoded'}
print("Navigate to the following URL, sign in to Plangrid, and give permission to access your account. Once permission has been granted, please paste the code below")
print(API + OauthURL + '?response_type=code&client_id=' + Client_ID + '&state=1&scope=write:projects')
print("Code:")
Authorization_Code = input()

r = requests.post(API + TokenURL, headers = RequestAccessTokenHeader, data = {
     'client_id': Client_ID,
     'client_secret': Client_Secret,
     'grant_type': 'authorization_code',
     'code': Authorization_Code,
})
print(r.text)
j = json.loads(r.text)
config['Default']['access_token'] = j['access_token']
config['Default']['refresh_token'] = j['refresh_token']

with open('config.txt', 'w') as configfile:
    config.write(configfile)