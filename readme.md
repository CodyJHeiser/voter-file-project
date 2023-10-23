# Voter Data Fetching Script

This script allows you to retrieve voter data from a specific API and save it into a CSV file. It's designed to handle pagination from the API and will loop through all available data until it has been entirely fetched.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.6 or later.
- You have a working internet connection to access the API endpoint.
- (Optional) You are familiar with GraphQL queries, as the script uses a GraphQL endpoint.

## Installing the Script

To install the script, follow these steps:

1. Clone the repository or download the script to your local machine.
2. (Optional) Create a virtual environment for the project.
3. Install the necessary Python packages using pip:

   ```bash
   pip install requests
   ```

## Using the Script

To use the script, follow these steps:

1. Open the script in your preferred code editor.
2. Modify the `STATE_ABBR` constant at the top of the script to the desired state abbreviation you wish to query.
3. (Optional) Adjust the `LIMIT` constant to change the number of records fetched per request (default is 10000).
4. (Optional) If required, modify the `TIME_BETWEEN_REQUESTS` to change the waiting time between each API request.
5. Save any changes and run the script:

   ```bash
   python path_to_your_script.py
   ```

6. The script will start fetching data and will periodically output the progress in the terminal. Once complete, the data will be saved in a CSV file named `{STATE_ABBR}_output.csv`.

## Troubleshooting

- If you encounter issues with the script, first check the response from the API and ensure the endpoint is functioning correctly and the server is responsive.
- Make sure you are not hitting a rate limit for the API, if the API provider has such limits in place. You may need to adjust the `TIME_BETWEEN_REQUESTS` or contact the API provider to increase your rate limit.
