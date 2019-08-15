import requests, configparser, os, json

# Initialize ConfigParser
config = configparser.ConfigParser()
config.readfp(open('config.txt'))

# Load data from config.txt
Client_ID = config.get('Default', 'ClientID')
Client_Secret = config.get('Default', 'ClientSecret')

# Set default variables
API = "https://io.plangrid.com"
RequestAccessTokenHeader = {'Content-Type': 'application/x-www-form-urlencoded'}

# Request that the user authorize this application and provide the authorization code
def GetTokens():
    print("Navigate to the following URL, sign in to Plangrid, and give permission to access your account. Once permission has been granted, please paste the code below")
    print(API + '/oauth/authorize' + '?response_type=code&client_id=' + Client_ID + '&state=1&scope=write:projects')
    print("Code:")
    Authorization_Code = input()

    # Use the provided authorization code to obtain the access token and refresh token
    if len(Authorization_Code) > 0:
        r = requests.post(API + '/oauth/token', headers = RequestAccessTokenHeader, data = {
            'client_id': Client_ID,
            'client_secret': Client_Secret,
            'grant_type': 'authorization_code',
            'code': Authorization_Code,
        })
        j = json.loads(r.text)

        # If the key 'error' is found in the json, show the error message. Otherwise load the tokens into the config file
        if 'error' in j:
            print("An error has occurred: " + j['error'])
        else:
            config['Default']['access_token'] = j['access_token']
            config['Default']['refresh_token'] = j['refresh_token']
            with open('config.txt', 'w') as configfile:
                config.write(configfile)
            print("Oauth token saved successfully")
    else:
        print("No code provided")

# Use collected token to run demonstration
def RunDemo():
    Header = {
        'Authorization': 'Bearer ' + config.get('Default', 'access_token'),
        'Accept': 'application/vnd.plangrid+json; version=1'
    }

    r = requests.get(API + '/projects', headers = Header)
    j = json.loads(r.text)
    print(json.dumps(j, indent=4, sort_keys=True))

# If the token has not been obtained, get it. Run the demo using the token.
if len(config.get('Default', 'access_token')) == 0:
    GetTokens()
RunDemo()