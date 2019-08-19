import requests, configparser, json, csv
import dateutil.parser
from dateutil.tz import *
from datetime import datetime

# Initialize ConfigParser
config = configparser.ConfigParser()
config.readfp(open('config.txt'))

# Set default variables
API = "https://io.plangrid.com"
auth = (config.get('Default', 'key'), '')

def GetTasks():
    csv_file  = open('plangrid_tasks.csv', 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    csv_writer.writerow([
        'PROJECT',
        'DESCRIPTION',
        'TYPE',
        'DATE_CREATED',
        'ROOT_CAUSE',
        'DIVISION',
        'CAUSED_BY',
        'IDENTIFIED_BY',
        'ESTIMATED_VALUE',
        'MD_NATURAL_KEY'
    ])
    
    Header = {
         'Accept': 'application/vnd.plangrid+json; version=1'
    }

    r = requests.get(API + '/projects', headers = Header, auth = auth)
    projects = json.loads(r.text)

    for project in projects['data']:
        print(project['name'])
        if project['uid'] != '0768258e-bac5-4788-a819-e8d441ae7484':
            issuereq = requests.get(API + '/projects/' + project['uid'] + '/issues?include_annotationless=true', headers = Header, auth = auth)
            issues = json.loads(issuereq.text)
            for issue in issues['data']:
                if not issue['deleted']:
                    types = ''
                    created_by = ''
                    created_by_req = json.loads(requests.get(issue['created_by']['url'], headers = Header, auth = auth).text)
                    if not 'message' in created_by_req:
                        created_by = created_by_req['first_name'] + ' ' + created_by_req['last_name']

                    print('    ' + str(issue['number']) + ' - ' + issue['title'])
                    if issue['issue_list'] != None:
                        issue_types = requests.get(issue['issue_list']['url'], headers = Header, auth = auth)
                        types = json.loads(issue_types.text)['name']
                    else:
                        types = 'General'

                    csv_writer.writerow([
                        project['name'],
                        issue['title'],
                        types,
                        dateutil.parser.parse(issue['created_at']).astimezone(tzlocal()).strftime("%m/%d/%Y %H:%M"),
                        "",
                        "",
                        "",
                        created_by,
                        issue['cost_impact'] if issue['has_cost_impact'] and issue['cost_impact'] else "0",
                        issue['uid']
                    ])
                    print(json.dumps(issue, indent=4, sort_keys=True))
    csv_file.close()

if __name__ == "__main__":
    print("Saving tasks to CSV")
    GetTasks()