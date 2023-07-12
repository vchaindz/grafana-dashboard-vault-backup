import os
import requests
import json
import argparse

# Parse arguments from command line
parser = argparse.ArgumentParser(description='Backup Grafana dashboards')
parser.add_argument('--url', required=True, help='Grafana URL')
parser.add_argument('--api_key', required=True, help='Grafana API Key')
parser.add_argument('--vault_api_key', type=str, help='API key for the vault.immudb.io service.')
args = parser.parse_args()

grafana_url = args.url
api_key = args.api_key

# Get API key for the vault.immudb.io service from command line argument or environment variable
vault_api_key = args.vault_api_key or os.getenv('VAULT_IMMUDB_API_KEY', None)
if not vault_api_key:
    raise Exception('No API key provided for the vault.immudb.io service.')

# Define headers for requests
headers = {
    "Authorization": "Bearer " + api_key,
    "Accept": "application/json",
}

# Creating a immudb Vault Session to handle the requests
s = requests.Session()
s.headers.update({"Content-Type": "application/json", "X-API-KEY": vault_api_key})

# Define ledger and collection parameters
ledger = "default" # replace with your ledger
collection = "default" # replace with your collection

# Initialize the collection within the immudb vault
payload = {
    "fields": [{"name": "uid", "type": "STRING"}, {"name": "title", "type": "STRING"}],
    "idFieldName": "_id",
    "indexes": [{"fields": ["uid"], "isUnique": True}]
}
# ignore for now as the endpoint is currently disabled
r = s.put(f"https://vault.immudb.io/ics/api/v1/ledger/{ledger}/collection/{collection}", json=payload)
r.raise_for_status() # If the request failed, this line will raise an exception



# Get all dashboards
r = requests.get(grafana_url + '/api/search', headers=headers)
r.raise_for_status()  # If the request failed, this line will raise an exception

dashboards = r.json()

# Fetch and save each dashboard
for db in dashboards:
    r = requests.get(grafana_url + '/api/dashboards/uid/' + db['uid'], headers=headers)
    r.raise_for_status()

    json_data = r.json()
    # Remove meta data that's not needed for restore
    del json_data['meta']

    # Prepare the data for the immudb Vault service
    record_data = {
        'uid': db['uid'],
        'title': json_data['dashboard']['title'],
        'dashboard': json_data
    }

    # Send the data to the immudb Vault service
    inserted = s.put("https://vault.immudb.io/ics/api/v1/ledger/default/collection/default/document", json=record_data)
    print(db['uid'], json_data['dashboard']['title'])
    print(inserted.status_code)
    assert inserted.status_code == 200
