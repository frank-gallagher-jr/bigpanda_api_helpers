
#####################################################################################################################################
#    ____  _       ____                  __                              
#   / __ )(_)___ _/ __ \____ _____  ____/ /___ _                         
#  / __  / / __ `/ /_/ / __ `/ __ \/ __  / __ `/                         
# / /_/ / / /_/ / ____/ /_/ / / / / /_/ / /_/ /                          
#/_____/_/\__, /_/    \__,_/_/ /_/\__,_/\__,_/                           
#    ____/____/  ___________   ________  _____    _   ___________________
#   / __ \/ __ \/ ___/_  __/  / ____/ / / /   |  / | / / ____/ ____/ ___/
#  / /_/ / / / /\__ \ / /    / /   / /_/ / /| | /  |/ / / __/ __/  \__ \ 
# / ____/ /_/ /___/ // /    / /___/ __  / ___ |/ /|  / /_/ / /___ ___/ / 
#/_/    \____//____//_/     \____/_/ /_/_/  |_/_/ |_/\____/_____//____/  
#                                                                        
######################################################################################################################################
#   Frank Gallagher, Jr. | 2024 | BigPanda 
######################################################################################################################################
#  Use at your own risk.  Presented without warranty.  Use your best judgement! 
######################################################################################################################################
#  PRE-REQUISITE - SET ENVIRONMENT VARIABLE WITH USER API KEY
#####################################################################################################################################

import json
import requests
import argparse
import os
from datetime import datetime

# Function to validate and correct Unix timestamps
def validate_timestamp(timestamp):
    if timestamp is None:
        print(f"Invalid timestamp: None value provided.")
        return None
    try:
        # Ensure the timestamp is an integer and within a reasonable range
        timestamp = int(timestamp)
        if 0 < timestamp < 4102444800:  # Reasonable range up to the year 2100
            return timestamp
        else:
            raise ValueError("Timestamp is out of valid range.")
    except ValueError as e:
        print(f"Invalid timestamp: {timestamp}. Error: {e}")
        return None

# Function to modify the payload with a prefix for the identifier
def modify_payload(record, identifier_prefix):
    start_timestamp = validate_timestamp(record.get("start"))
    end_timestamp = validate_timestamp(record.get("end"))

    if start_timestamp is None or end_timestamp is None:
        return None

    modified_payload = {
        "identifier": f"{identifier_prefix}{record['identifier']}",
        "status": record.get("status", "Unknown"),
        "summary": record.get("summary", "No summary provided"),
        "start": start_timestamp,
        "end": end_timestamp,
        "tags": record.get("tags", {}),  # Copy entire tags dictionary
        "ticket_url": record.get("ticket_url"),
        "metadata": {
            "metadata_id": "RSA-FG",
            "change_source": "bp_postChanges.py"
        }
    }
    return modified_payload

# Read JSON data from file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# POST modified data to the endpoint
def post_data(url, payload, headers):
    response = requests.post(url, json=payload, headers=headers)
    return response

# Main function
def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Push change data in JSON format to BigPanda Changes API.")
    parser.add_argument("input_file", help="Path to the input JSON file with change data - Consult https://docs.bigpanda.io for the required format.")
    parser.add_argument("-p", "--prefix", default="", help="Prefix for the change identifier (default: none) - Useful if you want to avoid collisions with overlapping record IDs.  Example: SN-CHG1234567 vs CHG-1234567 with the prefix set as 'SN-'.")
    parser.add_argument("-u", "--url", default="https://api.bigpanda.io/data/changes", help="Endpoint URL to post data, default should work.  Provided in case a new version of the API becomes available.")
    parser.add_argument("--app_key_env", default="BP_APP_KEY", help="Environment variable name for the Changes app key (default: 'BP_APP_KEY')")
    parser.add_argument("--api_key_env", default="BIGPANDA_API_KEY", help="Environment variable name for the User API key (default: 'BIGPANDA_API_KEY')")

    args = parser.parse_args()

    # Get API keys from environment variables specified by the user
    app_key = os.getenv(args.app_key_env)
    api_key = os.getenv(args.api_key_env)

    if not app_key or not api_key:
        print(f"Error: API keys are not set in environment variables.")
        print(f"EXPORT {args.app_key_env} and {args.api_key_env} environment variables - or - use the command line switches to specify different environment variables.")
        return

    # Set headers for the POST request
    headers = {
        "accept": "application/json",
        "x-bp-app-key": app_key,  # Integration App Key
        "Authorization": f"Bearer {api_key}",  # API Key
        "content-type": "application/json"
    }

    # Read data from the specified JSON file
    data = read_json_file(args.input_file)

    # Check if 'results' exists in data
    if "results" not in data:
        print("No results found in the JSON file.")
        return

    # Iterate through each record and modify the payload
    for record in data["results"]:
        modified_payload = modify_payload(record, args.prefix)
        
        if modified_payload:
            # Post modified payload to the endpoint
            response = post_data(args.url, modified_payload, headers)
            print(f"Response for identifier {record['identifier']}: {response.status_code}")
            print(response.text)
        else:
            print(f"Skipping record with identifier {record['identifier']} due to invalid timestamp.")

if __name__ == "__main__":
    main()
