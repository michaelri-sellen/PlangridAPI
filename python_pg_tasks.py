# 
import python_pg_api as api, python_pg_common as common

RootURL = "https://io.plangrid.com"

def GetTasks():
    csv_writer = common.CSV('plangrid_tasks.csv')
    csv_writer.Write([
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
    
    projects = api.APICall(RootURL + '/projects')
    for project in projects['data']:
        print(project['name'])
        if project['uid'] != '0768258e-bac5-4788-a819-e8d441ae7484':
            issues = api.APICall(RootURL + '/projects/' + project['uid'] + '/issues?include_annotationless=true')
            for issue in issues['data']:
                if not issue['deleted']:
                    types = ''
                    created_by = ''
                    created_by_req = api.APICall(issue['created_by']['url'])
                    
                    if not 'message' in created_by_req:
                        created_by = created_by_req['first_name'] + ' ' + created_by_req['last_name']

                    if issue['issue_list'] != None:
                        types = api.APICall(issue['issue_list']['url'])['name']
                    else:
                        types = 'General'

                    print(' |-' + str(issue['number']) + ': ' + issue['title'])
                    csv_writer.Write([
                        project['name'],
                        issue['title'],
                        types,
                        common.ConvertDateTime(issue['created_at']),
                        "",
                        "",
                        "",
                        created_by,
                        issue['cost_impact'] if issue['has_cost_impact'] and issue['cost_impact'] else "0",
                        issue['uid']
                    ])

if __name__ == "__main__":
    print("Saving tasks to CSV")
    GetTasks()