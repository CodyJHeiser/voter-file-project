import requests
import json
import csv
import time

# Constants
TIME_BETWEEN_REQUESTS = 0.5  # Time in seconds between each request
LIMIT = 10000  # Number of items to fetch per request
STATE_ABBR = 'WI'  # State abbreviation to filter by
EXPORT_FILE = f'{STATE_ABBR}_output.csv'  # File to export the data to

# URL to send the POST request
url = 'https://votereference-api-staging.idevdesign.net/graphql'

# Payload to send with the POST request
payload = [
    {
        "operationName": "VoterList",
        "variables": {
            "esQuery": {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"archived": {"query": False}}},
                            {"match": {"state_abbr": {"query": STATE_ABBR}}}
                        ],
                        "filter": []
                    }
                },
                "sort": [
                    {"person.data.last_name": "asc"},
                    {"person.data.first_name": "asc"},
                    {"person.data.middle_name": "asc"}
                ]
            },
            "offset": 1000,
            "limit": 1000,
            "orderBy": []
        },
        "query": """
            query VoterList($esQuery: JSONObject!, $offset: Int!, $limit: Int!) {
                results: voterArchivesConnection(
                    first: $limit
                    offset: $offset
                    elasticSearch: $esQuery
                ) {
                    esResult
                    totalCount
                    __typename
                }
            }
        """
    }
]

# Headers to let the server know the type of content being sent
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to send POST request and return the response data
def fetch_data(offset, limit):
    # URL to send the POST request
    url = 'https://votereference-api-staging.idevdesign.net/graphql'

    # Adjust payload with the current offset
    payload[0]['variables']['offset'] = offset
    payload[0]['variables']['limit'] = limit

    # Send the POST request with the specified URL, payload, and headers
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Return the JSON response if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print('Request failed with status code', response.status_code)
        return None

# Your initial offset
offset = 0

# Open CSV file just once outside the loop
with open(EXPORT_FILE, 'w', newline='') as csvfile:
    # Define the field names for the CSV
    fieldnames = ['person_id', 'first_name', 'last_name', 'address', 'phone', 'registration_date', 'registration_status', 'voter_id', 'voting_history']
    
    # Create a CSV writer object
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header to the CSV file
    writer.writeheader()

    while True:  # Keep looping until break
        response_data = fetch_data(offset, LIMIT)  # Fetch new data with current offset

        if response_data:
            # Total count of items; assuming it's present in the response
            total_count = response_data[0]['data']['results']['totalCount']

            # If no items are returned, we've reached the end, so we exit the loop
            if not response_data[0]['data']['results']['esResult']['hits']['hits']:
                break  # No more data to retrieve

            # Process the items just like before
            for item in response_data:
                person_data = item['data']['results']['esResult']['hits']['hits']
                for person in person_data:
                    source = person['_source']
                    person_info = source['person']['data']
                    address_info = person_info['address'][0] if 'address' in person_info and person_info['address'] else {}

                    # Flatten the voting history into a single string
                    voting_history = '; '.join([
                        f"{history['year']}: {history['vote_result']}" 
                        for history in person_info.get('voter_histories', [])
                    ])

                    # Create a dictionary for each row in the CSV
                    row = {
                        'person_id': source['person_id'],
                        'first_name': person_info['first_name'],
                        'last_name': person_info['last_name'],
                        'address': address_info.get('address', ''),
                        'phone': person_info['phone'],
                        'registration_date': address_info.get('registration_date', ''),
                        'registration_status': address_info.get('registration_status', ''),
                        'voter_id': person_info['voter_id'],
                        'voting_history': voting_history
                    }

                    # Write the row to the CSV
                    writer.writerow(row)

                    # Write the row to the CSV
                    writer.writerow(row)

            # Increase the offset by limit for the next iteration
            offset += LIMIT

            # Break out of the loop if we've fetched all items
            if offset >= total_count:
                break
        else:
            break  # Break the loop if the request failed

        # Pause for specified time before the next iteration
        time.sleep(TIME_BETWEEN_REQUESTS)

        print(f'Fetched {offset} of {total_count} items')