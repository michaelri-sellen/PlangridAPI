# This script will get all Tasks/Issues from Plangrid. It will then output 
#those tasks (which are actually deficiency logs) to a basic CSV file that will
#be processed by Alteryx for upload to Snowflake.
#
# A separate module "pg_api" is leveraged to perform calls to the 
#Plangrid API
#
# A separate module "pg_common" is leveraged for miscellaneous 
#functions that are shared with other scripts
#
# Note that 'pg_api' and 'pg_common' are both custom modules 
#written to support this script. They are both located in the same directory as
#this script

# Import API and Common python files
import pg_api as API, pg_common as Common

# Create a CSV writer object from the Common module
CSV = Common.CSV('plangrid_tasks.csv') 
# Write the Header row to the top of the CSV file
CSV.Write([
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

# Get a list of all projects from the API
projects = API.Call(Common.RootURL + '/projects')
for project in projects['data']: # Repeat the below code for each project
    # Ignore sample projects
    if not project['uid'] in Common.SampleProjects:
        # Get a list of all issues for this project
        issues = API.Call(Common.RootURL + '/projects/' + project['uid'] + '/issues?include_annotationless=true')
        for issue in issues['data']: # Repeat the below code for each issue
            if not issue['deleted']: # Ignore deleted issues
                # Set default values
                cost = '0'
                issue_type = 'General'
                created_by = ''
                # Get created_by user data using Foreign Key
                created_by_FK = API.Call(issue['created_by']['url'])
                
                # Attempt to get the first and last name of the user that
                #created the issue
                if not 'message' in created_by_FK:
                    created_by = created_by_FK['first_name'] + ' ' + created_by_FK['last_name']
                
                # If there is an issue_list FK, use it to grab the name of the
                #issue_list. This is the equivalent of the Type field in 
                #FieldView, and is called List in the Plangrid UI.
                if issue['issue_list'] != None:
                    issue_type = API.Call(issue['issue_list']['url'])['name']

                # If there is a cost impact, and that value is not null grab 
                #the cost_impact value
                if issue['has_cost_impact'] and issue['cost_impact']:
                    cost = issue['cost_impact']

                # Write this issue data for this project to the CSV file
                CSV.Write([
                    project['name'],                     # PROJECT
                    issue['title'],                      # DESCRIPTION
                    issue_type,                          # TYPE
                    Common.DateTime(issue['created_at']),# DATE_CREATED
                    '',                                  # ROOT_CAUSE (Not in Plangrid)
                    '',                                  # DIVISION (Not in Plangrid)
                    '',                                  # CAUSED_BY (Not in Plangrid)
                    created_by,                          # IDENTIFIED_BY
                    cost,                                # ESTIMATED_VALUE
                    issue['uid']                         # MD_NATURAL_KEY
                ])