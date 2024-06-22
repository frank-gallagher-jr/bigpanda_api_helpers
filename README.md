# bigpanda_api_helpers
 Get and Post BigPanda Changes 


# GET Script: Fetching and Filtering Change Records
Description
This script retrieves change records from an API, filters them based on specified criteria, and saves the results to a JSON file. It converts provided start and end times to epoch timestamps using a specified time zone, handles large datasets through pagination, and allows filtering by source system, search queries, and specific key-value pairs within the payload. The script uses an environment variable for secure handling of the API key and supports flexible input through command-line arguments for various parameters.

# POST Script: Posting Modified JSON Data
Description
This script reads filtered JSON data from a file, modifies the payload by adding a prefix to the identifier and copying all key-value pairs from the tags dictionary, and posts it to an API endpoint with additional metadata. It validates timestamps and skips records with invalid data. The script uses environment variables for secure handling of API keys and supports command-line arguments for specifying the input file, identifier prefix, and endpoint URL.
