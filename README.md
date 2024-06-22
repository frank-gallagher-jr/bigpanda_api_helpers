# BigPanda API Helpers
Get and Post BigPanda Changes

---

## GET Script: Fetching and Filtering Change Records

### Description
This script retrieves change records from the BigPanda Change API, filters them based on specified criteria, and saves the results to a JSON file. It converts provided start and end times to epoch timestamps using a specified time zone, handles large datasets through pagination, and allows filtering by source system, search queries, and specific key-value pairs within the payload. The script uses an environment variable for secure handling of the API key and supports flexible input through command-line arguments for various parameters.

---

## POST Script: Posting Modified JSON Data

### Description
This script reads change data from a JSON file, prepares the data by copying all key-value pairs from the tags dictionary, and posts it to the BigPanda Change API endpoint with additional metadata. It validates timestamps and skips records with invalid data. The script uses environment variables for secure handling of API keys and supports command-line arguments for specifying the input file, identifier prefix, and endpoint URL.

**Be sure to set your environment variables before running.**

---

## Usage: `bp_getChanges.py`

```plaintext
usage: 
python3 get_script.py [-h] [-e END_TIME] [-tz TIME_ZONE] [-o OUTPUT_FILE]
                     [-s SOURCE_SYSTEM] [-q SEARCH_QUERY] [-l LIMIT]
                     [--sort {start_time_frame,end_time_frame}] [--key KEY]
                     [--value VALUE] [--array_key ARRAY_KEY]
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
                        Output file path (default: filtered_changes.json)
  -s SOURCE_SYSTEM, --source_system SOURCE_SYSTEM
                        Filter by source system (e.g., 'servicenow')
  -q SEARCH_QUERY, --search_query SEARCH_QUERY
                        Additional search query (e.g., "ChatGPT Is a cool and helpful entity")
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


usage: post_script.py [-h] [-p PREFIX] [-u URL] [--app_key_env APP_KEY_ENV]
                      [--api_key_env API_KEY_ENV]
                      input_file

Post modified JSON data to an endpoint.

positional arguments:
  input_file            Path to the input JSON file with filtered data

optional arguments:
  -h, --help            show this help message and exit
  -p PREFIX, --prefix PREFIX
                        Prefix for the identifier (default: 'SN-')
  -u URL, --url URL     Endpoint URL to post data (default: https://api.bigpanda.io/data/changes)
  --app_key_env APP_KEY_ENV
                        Environment variable name for the app key (default: 'BP_APP_KEY')
  --api_key_env API_KEY_ENV
                        Environment variable name for the API key (default: 'BIGPANDA_API_KEY')
