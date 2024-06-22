# BigPanda API Helpers
Get and Post BigPanda Changes

BigPanda's Change API is a mechanism for pulling aggregated change records from many integrated systems (such as ITSM, DevOps, Configuration Monitoring, etc) for your organization.  That's where the bp_getChanges.py script is useful.  You can use this script to pull data for a specific human-readable timeframe, a specific change source, and even tag key/value pairs with the payload. 

Many times, this data is single-stream and cannot be replicated in other systems.  That's where the bp_postChanges.py script is useful.  You can quite literally take the output from the bp_getChanges.py scripted output file and push it into a lower BigPanda instance for development and testing of the correlation functionality. 

---

## BigPanda GET Changes Script: 

Fetching and Filtering Change Records from BigPanda's Change API

### Description
This script retrieves change records from the BigPanda Change API, filters them based on specified criteria, and saves the results to a JSON file. It converts provided start and end times to epoch timestamps using a specified time zone, handles large datasets through pagination, and allows filtering by source system, search queries, and specific key-value pairs within the payload. The script uses an environment variable for secure handling of the API key and supports flexible input through command-line arguments for various parameters.

---

## BigPanda POST Changes Script: 

Sending Change Records to BigPanda's Change API

### Description
This script reads change data from a JSON file, prepares the data by copying all key-value pairs from the tags dictionary, and posts it to the BigPanda Change API endpoint with additional metadata. It validates timestamps and skips records with invalid data. The script uses environment variables for secure handling of API keys and supports command-line arguments for specifying the input file, identifier prefix, and endpoint URL.

**Be sure to set your environment variables with your necessary APP and USER API KEYS before executing.**

---
Official docs: 

https://docs.bigpanda.io/reference/retrieve-all-changes
https://docs.bigpanda.io/reference/create-or-update-a-change

---

## Usage: `bp_getChanges.py`

```plaintext
usage: 
python3 bp_getChanges.py [-h] [-e END_TIME] [-tz TIME_ZONE] [-o OUTPUT_FILE]
                         [-s SOURCE_SYSTEM] [-q SEARCH_QUERY] [-l LIMIT]
                         [--sort {start_time_frame,end_time_frame}]
                         [--key KEY] [--value VALUE] [--array_key ARRAY_KEY]
                         [--api_key_env API_KEY_ENV]
                         start_time

Fetch and filter change records.

positional arguments:
  start_time            Start time in format YYYY-MM-DDTHH:MM:SS

optional arguments:
  -h, --help            show this help message and exit
  -e END_TIME, --end_time END_TIME
                        End time in format YYYY-MM-DDTHH:MM:SS (default: now)
  -tz TIME_ZONE, --time_zone TIME_ZONE
                        Time zone of the provided date and time (default: UTC)
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output file path (default: bp_getChanges_filtered_changes.json)
  -s SOURCE_SYSTEM, --source_system SOURCE_SYSTEM
                        Filter by source system (e.g., 'servicenow_changes.servicenow_prod')
  -q SEARCH_QUERY, --search_query SEARCH_QUERY
                        Additional search query (e.g., "BigPanda is an AI Ops powerhouse")
  -l LIMIT, --limit LIMIT
                        Maximum number of results per request (default: 100)
  --sort {start_time_frame,end_time_frame}
                        Field to sort results by (default: start_time_frame)
  --key KEY             Key to search within each change payload
  --value VALUE         Value to search for within the specified key
  --array_key ARRAY_KEY
                        Array key to search for value (e.g., 'affectedCIs')
  --api_key_env API_KEY_ENV
                        Environment variable name for the API key (default: 'BIGPANDA_API_KEY')

```

## Usage: `bp_postChanges.py`

```plaintext

usage: 
python3 bp_postChanges.py [-h] [-p PREFIX] [-u URL] [--app_key_env APP_KEY_ENV]
                          [--api_key_env API_KEY_ENV]
                          input_file

Post change data from a JSON file to the BigPanda Change API.

positional arguments:
  input_file            Path to the input JSON file with change data

optional arguments:
  -h, --help            show this help message and exit
  -p PREFIX, --prefix PREFIX
                        Prefix for the identifier (default: 'SN-')
  -u URL, --url URL     Endpoint URL to post data (default: https://api.bigpanda.io/data/changes)
  --app_key_env APP_KEY_ENV
                        Environment variable name for the app key (default: 'BP_APP_KEY')
  --api_key_env API_KEY_ENV
                        Environment variable name for the API key (default: 'BIGPANDA_API_KEY')

```

---

Example Output format bp_getChanges.py 

```plaintext

{
    "results": [
        {
            "_id": "6676539e736f9a1d1585e200",
            "identifier": "SN-CHG0030012",
            "created_at": 1719030686,
            "end": 1718123399,
            "maintenance_condition": null,
            "source_system": "servicenow_changes.fg_servicenow_2_9_change",
            "start": 1718119931,
            "status": "Done",
            "summary": "Monthly Windows Server Patching - Las Vegas",
            "tags": {
                "upon_reject": "Cancel all future Tasks",
                "sys_updated_on": "2024-06-11 16:30:03",
                "type": "Normal",
                "test_plan": "Confirm system returns successfully and login",
                "number": "CHG0030012",
                "state": "Closed",
                "sys_created_by": "admin",
                "knowledge": "false",
                "phase": "Requested",
                "impact": "2 - Medium",
                "active": "false",
                "priority": "3 - Moderate",
                "sys_domain_path": "/",
                "production_system": "false",
                "requested_by": "System Administrator",
                "approval_set": "2024-06-11 08:31:52",
                "implementation_plan": "Take server snapshots\r\nCommunicate the execution of the change\r\nExecute the patch \r\nShutdown /r\r\nConfirm the change executed successfully",
                "end_date": "2024-06-11 21:31:24",
                "short_description": "Monthly Windows Server Patching - Las Vegas",
                "work_start": "2024-06-11 15:32:11",
                "outside_maintenance_schedule": "false",
                "sys_class_name": "Change Request",
                "closed_by": "System Administrator",
                "reassignment_count": "0",
                "start_date": "2024-06-11 12:31:15",
                "assigned_to": "Beth Anglin",
                "hierarchical_variables": "variable_pool",
                "sla_due": "UNKNOWN",
                "escalation": "Normal",
                "upon_approval": "Proceed to Next Task",
                "made_sla": "true",
                "backout_plan": "Remove patch\r\nshutdown /r",
                "conflict_status": "Not Run",
                "task_effective_number": "CHG0030012",
                "sys_updated_by": "admin",
                "opened_by": "System Administrator",
                "sys_created_on": "2024-06-11 15:29:48",
                "sys_domain": "global",
                "closed_at": "2024-06-11 16:30:03",
                "business_service": "Active Directory",
                "chg_model": "Normal",
                "opened_at": "2024-06-11 15:26:26",
                "work_end": "2024-06-11 16:29:59",
                "phase_state": "Open",
                "close_code": "Successful",
                "assignment_group": "Software",
                "description": "We will be applying monthly security patches for the following servers: \r\n\r\nlvaddc01.win.initech.global\r\nlvaddc02.win.initech.global\r\nlvwinpssf01.win.initech.global\r\nlvwinpssf03.win.initech.global\r\nlvwinpssf08.win.initech.global",
                "close_notes": "Completed successfully.",
                "sys_id": "8b22416c93be8a10a93e796efaba10bf",
                "cab_required": "false",
                "urgency": "3 - Low",
                "scope": "Medium",
                "justification": "Monthly patches are required for security posture per company policy.",
                "activity_due": "UNKNOWN",
                "approval": "Approved",
                "sys_mod_count": "17",
                "on_hold": "false",
                "unauthorized": "false",
                "risk": "High",
                "category": "Other",
                "risk_impact_analysis": "Some risk associated with the updates."
            },
            "ticket_url": "https://eventual.service-now.com/nav_to.do?uri=change_request.do?sys_id=8b22416c93be8a10a93e796efaba10bf",
            "updated_at": 1719030686,
            "id": "6676539e736f9a1d1585e200"
        },
        {
            "_id": "66763be9736f9a1d1546cab2",
            "identifier": "SNC-CHG0030012",
            "created_at": 1719024617,
            "end": 1718123399,
            "maintenance_condition": null,
            "source_system": "servicenow_changes.fg_servicenow_2_9_change",
            "start": 1718119931,
            "status": "Done",
            "summary": "Monthly Windows Server Patching - Las Vegas",
            "tags": {
                "sys_id": "CHG0030012",
                "type": "3 - Moderate"
            },
            "ticket_url": "https://eventual.service-now.com/nav_to.do?uri=change_request.do?sys_id=8b22416c93be8a10a93e796efaba10bf",
            "updated_at": 1719024617,
            "id": "66763be9736f9a1d1546cab2"
        },
        {
            "_id": "66686d6e736f9a1d15bd2e23",
            "identifier": "CHG0030012",
            "created_at": 1718119790,
            "maintenance_condition": null,
            "source_system": "servicenow_changes.fg_servicenow_2_9_change",
            "start": 1718119931,
            "status": "Done",
            "summary": "Monthly Windows Server Patching - Las Vegas",
            "tags": {
                "upon_reject": "Cancel all future Tasks",
                "sys_updated_on": "2024-06-11 16:30:03",
                "type": "Normal",
                "test_plan": "Confirm system returns successfully and login",
                "number": "CHG0030012",
                "state": "Closed",
                "sys_created_by": "admin",
                "knowledge": "false",
                "phase": "Requested",
                "impact": "2 - Medium",
                "active": "false",
                "priority": "3 - Moderate",
                "sys_domain_path": "/",
                "production_system": "false",
                "requested_by": "System Administrator",
                "approval_set": "2024-06-11 08:31:52",
                "implementation_plan": "Take server snapshots\r\nCommunicate the execution of the change\r\nExecute the patch \r\nShutdown /r\r\nConfirm the change executed successfully",
                "end_date": "2024-06-11 21:31:24",
                "short_description": "Monthly Windows Server Patching - Las Vegas",
                "work_start": "2024-06-11 15:32:11",
                "outside_maintenance_schedule": "false",
                "sys_class_name": "Change Request",
                "closed_by": "System Administrator",
                "reassignment_count": "0",
                "start_date": "2024-06-11 12:31:15",
                "assigned_to": "Beth Anglin",
                "hierarchical_variables": "variable_pool",
                "sla_due": "UNKNOWN",
                "escalation": "Normal",
                "upon_approval": "Proceed to Next Task",
                "made_sla": "true",
                "backout_plan": "Remove patch\r\nshutdown /r",
                "conflict_status": "Not Run",
                "task_effective_number": "CHG0030012",
                "sys_updated_by": "admin",
                "opened_by": "System Administrator",
                "sys_created_on": "2024-06-11 15:29:48",
                "sys_domain": "global",
                "closed_at": "2024-06-11 16:30:03",
                "business_service": "Active Directory",
                "chg_model": "Normal",
                "opened_at": "2024-06-11 15:26:26",
                "work_end": "2024-06-11 16:29:59",
                "phase_state": "Open",
                "close_code": "Successful",
                "assignment_group": "Software",
                "description": "We will be applying monthly security patches for the following servers: \r\n\r\nlvaddc01.win.initech.global\r\nlvaddc02.win.initech.global\r\nlvwinpssf01.win.initech.global\r\nlvwinpssf03.win.initech.global\r\nlvwinpssf08.win.initech.global",
                "close_notes": "Completed successfully.",
                "sys_id": "8b22416c93be8a10a93e796efaba10bf",
                "cab_required": "false",
                "urgency": "3 - Low",
                "scope": "Medium",
                "justification": "Monthly patches are required for security posture per company policy.",
                "activity_due": "UNKNOWN",
                "approval": "Approved",
                "sys_mod_count": "17",
                "on_hold": "false",
                "unauthorized": "false",
                "risk": "High",
                "category": "Other",
                "risk_impact_analysis": "Some risk associated with the updates."
            },
            "ticket_url": "https://eventual.service-now.com/nav_to.do?uri=change_request.do?sys_id=8b22416c93be8a10a93e796efaba10bf",
            "updated_at": 1718123406,
            "end": 1718123399,
            "id": "66686d6e736f9a1d15bd2e23"
        },
        {
            "_id": "6676539e736f9a1d1585f446",
            "identifier": "SN-CHG0030011",
            "created_at": 1719030686,
            "end": 1717647128,
            "maintenance_condition": null,
            "source_system": "servicenow_changes.fg_servicenow_2_9_change",
            "start": 1717614781,
            "status": "In Progress",
            "summary": "Monthly Patch Interval - Houston Datacenter",
            "tags": {
                "upon_reject": "Cancel all future Tasks",
                "sys_updated_on": "2024-06-05 19:13:01",
                "type": "Normal",
                "test_plan": "Login via Active Directory",
                "number": "CHG0030011",
                "state": "Implement",
                "sys_created_by": "admin",
                "knowledge": "false",
                "phase": "Requested",
                "impact": "3 - Low",
                "active": "true",
                "priority": "4 - Low",
                "sys_domain_path": "/",
                "production_system": "false",
                "requested_by": "System Administrator",
                "approval_set": "2024-06-05 12:12:56",
                "implementation_plan": "Take server snapshot\r\nCommunicate execution of change to NOC\r\nApply patches\r\nshutdown /r\r\nUpon loading confirm AD works",
                "end_date": "2024-06-06 04:12:08",
                "short_description": "Monthly Patch Interval - Houston Datacenter",
                "work_start": "2024-06-05 19:13:01",
                "outside_maintenance_schedule": "false",
                "sys_class_name": "Change Request",
                "reassignment_count": "0",
                "start_date": "2024-06-05 17:00:55",
                "hierarchical_variables": "variable_pool",
                "sla_due": "UNKNOWN",
                "escalation": "Normal",
                "upon_approval": "Proceed to Next Task",
                "made_sla": "true",
                "backout_plan": "Remove patches",
                "conflict_status": "Not Run",
                "task_effective_number": "CHG0030011",
                "sys_updated_by": "admin",
                "opened_by": "System Administrator",
                "sys_created_on": "2024-06-05 19:12:17",
                "sys_domain": "global",
                "business_service": "Active Directory",
                "chg_model": "Normal",
                "opened_at": "2024-06-05 18:48:02",
                "phase_state": "Open",
                "assignment_group": "Service Desk",
                "description": "This month we're patching all servers in the Houston Datacenter.  \r\n\r\nIncluding the following Windows Servers:\r\n\r\nhouaddc01.initech.global\r\n\r\nhouaddc03.initech.global\r\n\r\nhoualias1.initech.global\r\n\r\nhoualias2.initech.global",
                "sys_id": "75c6fe2e93aa8210a93e796efaba1098",
                "cab_required": "false",
                "urgency": "3 - Low",
                "scope": "Medium",
                "justification": "Monthly security patches required by company policy",
                "activity_due": "UNKNOWN",
                "approval": "Approved",
                "sys_mod_count": "16",
                "on_hold": "false",
                "unauthorized": "false",
                "risk": "Moderate",
                "category": "Other",
                "risk_impact_analysis": "These will be done sequentially no impact."
            },
            "ticket_url": "https://eventual.service-now.com/nav_to.do?uri=change_request.do?sys_id=75c6fe2e93aa8210a93e796efaba1098",
            "updated_at": 1719030686,
            "id": "6676539e736f9a1d1585f446"
        },
        {
            "_id": "66763be9736f9a1d1546e79d",
            "identifier": "SNC-CHG0030011",
            "created_at": 1719024617,
            "end": 1717647128,
            "maintenance_condition": null,
            "source_system": "servicenow_changes.fg_servicenow_2_9_change",
            "start": 1717614781,
            "status": "In Progress",
            "summary": "Monthly Patch Interval - Houston Datacenter",
            "tags": {
                "sys_id": "CHG0030011",
                "type": "4 - Low"
            },
            "ticket_url": "https://eventual.service-now.com/nav_to.do?uri=change_request.do?sys_id=75c6fe2e93aa8210a93e796efaba1098",
            "updated_at": 1719024617,
            "id": "66763be9736f9a1d1546e79d"
        },
        {
            "_id": "6660b893cd568d0a2efa8ad4",
            "identifier": "CHG0030011",
            "created_at": 1717614739,
            "end": 1717647128,
            "maintenance_condition": null,
            "source_system": "servicenow_changes.fg_servicenow_2_9_change",
            "start": 1717614781,
            "status": "In Progress",
            "summary": "Monthly Patch Interval - Houston Datacenter",
            "tags": {
                "upon_reject": "Cancel all future Tasks",
                "sys_updated_on": "2024-06-05 19:13:01",
                "type": "Normal",
                "test_plan": "Login via Active Directory",
                "number": "CHG0030011",
                "state": "Implement",
                "sys_created_by": "admin",
                "knowledge": "false",
                "phase": "Requested",
                "impact": "3 - Low",
                "active": "true",
                "priority": "4 - Low",
                "sys_domain_path": "/",
                "production_system": "false",
                "requested_by": "System Administrator",
                "approval_set": "2024-06-05 12:12:56",
                "implementation_plan": "Take server snapshot\r\nCommunicate execution of change to NOC\r\nApply patches\r\nshutdown /r\r\nUpon loading confirm AD works",
                "end_date": "2024-06-06 04:12:08",
                "short_description": "Monthly Patch Interval - Houston Datacenter",
                "work_start": "2024-06-05 19:13:01",
                "outside_maintenance_schedule": "false",
                "sys_class_name": "Change Request",
                "reassignment_count": "0",
                "start_date": "2024-06-05 17:00:55",
                "hierarchical_variables": "variable_pool",
                "sla_due": "UNKNOWN",
                "escalation": "Normal",
                "upon_approval": "Proceed to Next Task",
                "made_sla": "true",
                "backout_plan": "Remove patches",
                "conflict_status": "Not Run",
                "task_effective_number": "CHG0030011",
                "sys_updated_by": "admin",
                "opened_by": "System Administrator",
                "sys_created_on": "2024-06-05 19:12:17",
                "sys_domain": "global",
                "business_service": "Active Directory",
                "chg_model": "Normal",
                "opened_at": "2024-06-05 18:48:02",
                "phase_state": "Open",
                "assignment_group": "Service Desk",
                "description": "This month we're patching all servers in the Houston Datacenter.  \r\n\r\nIncluding the following Windows Servers:\r\n\r\nhouaddc01.initech.global\r\n\r\nhouaddc03.initech.global\r\n\r\nhoualias1.initech.global\r\n\r\nhoualias2.initech.global",
                "sys_id": "75c6fe2e93aa8210a93e796efaba1098",
                "cab_required": "false",
                "urgency": "3 - Low",
                "scope": "Medium",
                "justification": "Monthly security patches required by company policy",
                "activity_due": "UNKNOWN",
                "approval": "Approved",
                "sys_mod_count": "16",
                "on_hold": "false",
                "unauthorized": "false",
                "risk": "Moderate",
                "category": "Other",
                "risk_impact_analysis": "These will be done sequentially no impact."
            },
            "ticket_url": "https://eventual.service-now.com/nav_to.do?uri=change_request.do?sys_id=75c6fe2e93aa8210a93e796efaba1098",
            "updated_at": 1717614783,
            "id": "6660b893cd568d0a2efa8ad4"
        }
    ]
}

```
