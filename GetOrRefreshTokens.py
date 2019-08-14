import requests, configparser, os, json

config = configparser.ConfigParser()
config.readfp(open('config.txt'))

API = "https://io.plangrid.com"

Client_ID = config.get('Default', 'ClientID')
Client_Secret = config.get('Default', 'ClientSecret')
RequestAccessTokenHeader = {'Content-Type': 'application/x-www-form-urlencoded'}

print("Navigate to the following URL, sign in to Plangrid, and give permission to access your account. Once permission has been granted, please paste the code below")
print(API + '/oauth/authorize' + '?response_type=code&client_id=' + Client_ID + '&state=1&scope=write:projects')
print("Code:")
Authorization_Code = input()

r = requests.post(API + '/oauth/token', headers = RequestAccessTokenHeader, data = {
     'client_id': Client_ID,
     'client_secret': Client_Secret,
     'grant_type': 'authorization_code',
     'code': Authorization_Code,
})
j = json.loads(r.text)

if 'error' in j:
    print("An error has occurred: " + j['error'])
else:
    config['Default']['access_token'] = j['access_token']
    config['Default']['refresh_token'] = j['refresh_token']
    with open('config.txt', 'w') as configfile:
        config.write(configfile)
    print("Oauth token saved successfully")