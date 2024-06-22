
#####################################################################################################################################
#  ____  _       _____                _                                      
# |  _ \(_)     |  __ \              | |                                     
# | |_) |_  __ _| |__) |_ _ _ __   __| | __ _                                
# |  _ <| |/ _` |  ___/ _` | '_ \ / _` |/ _` |                               
# | |_) | | (_| | |  | (_| | | | | (_| | (_| |                               
# |____/|_|\__, |_|   \__,_|_| |_|\__,_|\__,_|                               
#           __/ |                                                            
#   _____ _|___/ _______    _____ _    _          _   _  _____ ______  _____ 
#  / ____|  ____|__   __|  / ____| |  | |   /\   | \ | |/ ____|  ____|/ ____|
# | |  __| |__     | |    | |    | |__| |  /  \  |  \| | |  __| |__  | (___  
# | | |_ |  __|    | |    | |    |  __  | / /\ \ | . ` | | |_ |  __|  \___ \ 
# | |__| | |____   | |    | |____| |  | |/ ____ \| |\  | |__| | |____ ____) |
#  \_____|______|  |_|     \_____|_|  |_/_/    \_\_| \_|\_____|______|_____/
#
#####################################################################################################################################
#   Frank Gallagher, Jr. | 2024 | BigPanda 
#####################################################################################################################################
#  Use at your own risk.  Presented without warranty.  Use your best judgement! 
#####################################################################################################################################
#  PRE-REQUISITE - SET ENVIRONMENT VARIABLE WITH USER API KEY
#####################################################################################################################################


import requests
import json
import argparse
import logging
import calendar
import time
import pytz
from datetime import datetime
import os
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to convert date-time to epoch with specified time zone
def to_epoch(date_str, time_zone):
    try:
        # Parse the date string
        naive_datetime = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

        # Localize the datetime to the specified time zone
        local_tz = pytz.timezone(time_zone)
        local_datetime = local_tz.localize(naive_datetime)

        # Convert to UTC
        utc_datetime = local_datetime.astimezone(pytz.utc)

        # Convert to epoch time
        return calendar.timegm(utc_datetime.timetuple())
    except ValueError as e:
        logging.error(f"Error parsing date or time zone: {e}. Use format YYYY-MM-DDTHH:MM:SS and a valid time zone.")
        raise

# Function to fetch changes with pagination and rate limiting
def fetch_changes(api_url, headers, params):
    changes = []
    while True:
        logging.info(f"Requesting changes with params: {params}")
        response = requests.get(api_url, headers=headers, params=params)
        logging.info(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json().get("results", [])
            changes.extend(data)
            logging.info(f"Fetched {len(data)} records, total so far: {len(changes)}")

            link_header = response.headers.get('Link')
            if not link_header or 'rel="next"' not in link_header:
                break
            cursor = link_header.split('cursor=')[1].split('>')[0]
            params['cursor'] = cursor

            # Implement a delay to avoid rate limiting
            time.sleep(1)  # Adjust the sleep time as needed
        else:
            logging.error(f"Failed to retrieve changes. Status code: {response.status_code}")
            logging.error(f"Response: {response.text}")
            break
    return changes

# Function to search within nested dictionaries and arrays
def search_in_payload(payload, key, value, array_key=None):
    if array_key:
        # Search for value in the specified array key
        if array_key in payload:
            return value in payload[array_key]
    else:
        # Search for key-value pair in the dictionary
        for k, v in payload.items():
            if k == key and str(v).lower() == str(value).lower():
                return True
            # Check nested dictionary
            if isinstance(v, dict):
                if search_in_payload(v, key, value):
                    return True
            # Check arrays
            if isinstance(v, list):
                if value in [str(item).lower() for item in v]:
                    return True
    return False

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Fetch and filter change records.")
parser.add_argument("start_time", help="Start time in format YYYY-MM-DDTHH:MM:SS")
parser.add_argument("-e", "--end_time", default=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                    help="End time in format YYYY-MM-DDTHH:MM:SS (default: now)")
parser.add_argument("-tz", "--time_zone", default="UTC", 
                    help="Time zone of the provided date and time (default: UTC) - Accepts formats like 'America/Chicago', as well as 'Etc/GMT+2', and 'EST' style aliases")
parser.add_argument("-o", "--output_file", default="bp_getChanges_filtered_changes.json",
                    help="Output file path (default: bp_getChanges_filtered_changes.json)")
parser.add_argument("-s", "--source_system", help="Filter by source system id (e.g., 'servicenow_change.servicenow_dev12345')")
parser.add_argument("-q", "--search_query", help='Additional search query - Query only works for status, identifier, and summary fields (e.g., "CHG123456")')
parser.add_argument("-l", "--limit", type=int, default=100,
                    help="Maximum number of results per request (default: 100)")
parser.add_argument("--sort", choices=["start_time_frame", "end_time_frame"], default="start_time_frame",
                    help="Field to sort results by (default: start_time_frame)")
parser.add_argument("--key", help="Tag Key to search within each change payload")
parser.add_argument("--value", help="Tag Value to search for within the specified key")
parser.add_argument("--array_key", help="Array key to search for value (e.g., 'affectedCIs')")
parser.add_argument("--api_key_env", default="BIGPANDA_API_KEY", help="Environment variable name for the User API key (default: 'BIGPANDA_API_KEY')")

args = parser.parse_args()

# Correct usage to get environment variable
USER_API_KEY = os.getenv(args.api_key_env)

# Make sure we have an API Key
if not USER_API_KEY:
    print("ERROR: API key is missing.")
    print(f"Please set the environment variable {args.api_key_env} using the export command.")
    sys.exit(1)

# Convert times to epoch
try:
    start_epoch = to_epoch(args.start_time, args.time_zone)
    end_epoch = to_epoch(args.end_time, args.time_zone)
except ValueError as e:
    logging.error(f"Invalid date or time zone: {e}")
    sys.exit(1)

# Constants
API_URL = "https://api.bigpanda.io/resources/v2.0/changes"

# Define headers
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {USER_API_KEY}"
}

# Define query parameters
params = {
    "start_time_frame": start_epoch,
    "end_time_frame": end_epoch,
    "include": "change",
    "limit": args.limit,
    "sort": args.sort
}

# Add search query if specified
if args.search_query:
    params["search"] = args.search_query

# Fetch changes with pagination
change_records = fetch_changes(API_URL, headers, params)

# Filter change records by source_system if specified
if args.source_system:
    change_records = [
        record for record in change_records
        if args.source_system.lower() in record.get("source_system", "").lower()
    ]

# Further filter by key-value pair or value in array if specified
if args.key and args.value:
    filtered_changes = [
        record for record in change_records
        if search_in_payload(record, args.key, args.value, args.array_key)
    ]
else:
    filtered_changes = change_records

# Log the total number of filtered changes
logging.info(f"Total filtered changes: {len(filtered_changes)}")

# Save filtered changes to a JSON file
try:
    with open(args.output_file, 'w') as file:
        json.dump({"results": filtered_changes}, file, indent=4)
    logging.info(f"Filtered changes saved to {args.output_file}")
except IOError as e:
    logging.error(f"Failed to save changes to file: {e}")
