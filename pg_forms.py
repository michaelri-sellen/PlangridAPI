# This script will get all Plangrid forms under all relevant Sellen projects. 
#It will then output those forms (which are actually quality checklists) to a 
#basic CSV file that will be processed by Alteryx for upload to Snowflake.
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
CSV = Common.CSV('plangrid_forms.csv') 
# Write the Header row to the top of the CSV file
CSV.Write([
    'PROJECT_NAME',
    'CHECKLIST_NAME',
    'CHECKLIST_TYPE',
    'CREATED_DATE',
    'STATUS_DATE',
    'OPEN_TASKS',
    'CLOSED_TASKS',
    'STATUS',
    'OVER_DUE',
    'COMPLETE',
    'CLOSED',
    'MD_NATURAL_KEY'
])

# Get a list of all projects from the API
projects = API.Call(Common.RootURL + '/projects')
for project in projects['data']: # Repeat the below code for each project
    # Ignore sample projects
    if not project['uid'] in Common.SampleProjects:
        # Get a list of all forms for this project
        forms = API.Call(Common.RootURL + '/projects/' + project['uid'] + '/field_reports')
        for form in forms['data']: # Repeat the below code for each form
            # Write this form data for this project to the CSV file
            CSV.Write([
                project['name'],                     # PROJECT_NAME
                form['field_report_type']['name'],   # CHECKLIST_NAME
                '',                                  # CHECKLIST_TYPE
                Common.DateTime(form['updated_at']), # CREATED_DATE
                Common.DateTime(form['updated_at']), # STATUS_DATE
                '',                                  # OPEN_TASKS
                '',                                  # CLOSED_TASKS
                form['status'],                      # STATUS
                '',                                  # OVER_DUE
                '',                                  # COMPLETE
                '',                                  # CLOSED
                form['uid']                          # MD_NATURAL_KEY
            ])