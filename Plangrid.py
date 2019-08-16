import requests, configparser, os, json

# Initialize ConfigParser
config = configparser.ConfigParser()
config.readfp(open('config.txt'))

# Set default variables
API = "https://io.plangrid.com"
auth = (config.get('Default', 'key'), '')

def RunDemo():
    Header = {
         'Accept': 'application/vnd.plangrid+json; version=1'
    }

    r = requests.get(API + '/projects', headers = Header, auth = auth)
    projects = json.loads(r.text)

    for project in projects['data']:
        print(project['name'])
        issuereq = requests.get(API + '/projects/' + project['uid'] + '/issues?include_annotationless=true', headers = Header, auth = auth)
        issues = json.loads(issuereq.text)
        for issue in issues['data']:
            print('    ' + str(issue['number']) + ' - ' + issue['title'])