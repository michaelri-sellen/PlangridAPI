# This script will get all Tasks/Issues from Plangrid. It will then output those tasks (which are actually deficiency
# logs) to a basic CSV file that will be processed by Alteryx for upload to Snowflake.
#
# A separate module "python_pg_api" is leveraged to perform calls to the Plangrid API
# A separate module "python_pg_common" is leveraged for miscellaneous functions that are shared with other scripts
#
# Note that 'python_pg_api' and 'python_pg_common' are both custom modules written to support this script
# They are both located in the same directory as this script

# Import API and Common python files
import python_pg_api as api, python_pg_common as common

# Set the root URL for the Plangrid API
RootURL = "https://io.plangrid.com"

# This function will retrieve the tasks/issues from Plangrid and output them to the CSV file
def GetTasks():
    csv_writer = common.CSV('plangrid_tasks.csv') # Create a CSV writer object from the Common module
    # Write the Header row to the top of the CSV file
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
    
    projects = api.APICall(RootURL + '/projects') # Get a list of all projects from the API
    for project in projects['data']: # Repeat the below code for each project found
        if project['uid'] != '0768258e-bac5-4788-a819-e8d441ae7484': # Ignore sample project
            # Get a list of all issues from the API for this project
            issues = api.APICall(RootURL + '/projects/' + project['uid'] + '/issues?include_annotationless=true')
            for issue in issues['data']: # Repeat the below code for each issue found
                if not issue['deleted']: # Ignore deleted issues
                    # Set values to empty strings as default
                    cost = '0'
                    types = ''
                    created_by = ''
                    created_by_req = api.APICall(issue['created_by']['url']) # Get created_by user data using FK
                    
                    # Attempt to get the first and last name of the user that created the issue
                    if not 'message' in created_by_req:
                        created_by = created_by_req['first_name'] + ' ' + created_by_req['last_name']

                    # If there is an issue_list FK, use it to grab the name of the issue_list.
                    # This is the equivalent of the Type field in FieldView, and is called List in the Plangrid UI.
                    if issue['issue_list'] != None:
                        types = api.APICall(issue['issue_list']['url'])['name']
                    else:
                        types = 'General'

                    # If there is a cost impact, and that value is not null grab the cost_impact value                    
                    if issue['has_cost_impact'] and issue['cost_impact']:
                        cost = issue['cost_impact']

                    # Write this issue data for this project to the CSV file
                    csv_writer.Write([
                        project['name'],                                # PROJECT
                        issue['title'],                                 # DESCRIPTION
                        types,                                          # TYPE
                        common.ConvertDateTime(issue['created_at']),    # DATE_CREATED
                        "",                                             # ROOT_CAUSE (Not in Plangrid)
                        "",                                             # DIVISION (Not in Plangrid)
                        "",                                             # CAUSED_BY (Not in Plangrid)
                        created_by,                                     # IDENTIFIED_BY
                        cost,                                           # ESTIMATED_VALUE
                        issue['uid']                                    # MD_NATURAL_KEY
                    ])

# Run the GetTasks function on startup of this module
if __name__ == "__main__":
    GetTasks()