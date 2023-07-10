# Grafana Dashboard Backup

This script allows you to back up all Grafana dashboards by sending their data to the immudb Vault service. The dashboards are fetched from a Grafana instance and then each dashboard's data is sent to the immudb Vault service.

## Prerequisites

- Python 3
- `requests` library in Python
- Access to a Grafana instance and its API Key
- Access to an immudb Vault service and its API Key

## Usage

```bash
python backup_grafana_dashboards.py --url <grafana_url> --api_key <grafana_api_key> --vault_api_key <immudb_vault_api_key>
```

Replace `<grafana_url>` with the URL of your Grafana instance, `<grafana_api_key>` with your Grafana API Key, and `<immudb_vault_api_key>` with your immudb Vault API Key.

If the immudb Vault API Key is not provided as a command line argument, the script will attempt to read it from the `VAULT_IMMUDB_API_KEY` environment variable.

## Description

The script performs the following steps:

1. It first initializes a collection in the immudb Vault service with appropriate field definitions and indexes.
2. It then fetches all dashboards from the Grafana instance.
3. For each dashboard, it sends a request to fetch the detailed dashboard data.
4. It prepares a record for each dashboard with the 'uid', 'title' and the entire dashboard data.
5. Each record is then sent to the immudb Vault service.

The script will print the 'uid' and 'title' of each dashboard that it processes. If any request fails, the script will raise an exception and stop.

## Notes

- The script uses the `requests` library to send HTTP requests. Make sure to install this library using pip: `pip install requests`
- The Grafana API Key needs to have sufficient permissions to read all dashboards.
- The immudb Vault service needs to accept the API Key and allow the operations that the script performs.
- The ledger and collection used in the script should be replaced with the actual ledger and collection names for your immudb Vault service.
- The script does not handle all possible error situations, so it might need adjustments based on your specific use case and environment.

