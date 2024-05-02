import os

from google.cloud import bigquery
from google.cloud.resourcemanager import ProjectsClient
from google.oauth2 import service_account
from googleapiclient import discovery

# Define the global variable for the service account JSON file path
SA_NAME = os.getenv('SA_NAME')
ORGANIZATION_ID = os.getenv('ORGANIZATION_ID')
SERVICE_ACCOUNT_JSON = f'{SA_NAME}.json'


def get_all_datasets(organization_id):
    # Load the credentials
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_JSON,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    # Build the service usage client
    service = discovery.build('serviceusage', 'v1', credentials=credentials)
    service_name = 'bigquery.googleapis.com'
    bigquery_client = bigquery.Client.from_service_account_json(
        SERVICE_ACCOUNT_JSON)

    # Get all projects
    projects = ProjectsClient.from_service_account_json(
        SERVICE_ACCOUNT_JSON).search_projects()
    print(f"Checking projects for {organization_id}: ",
          [p.project_id for p in projects])
    print()

    # Initialize an empty dictionary
    project_datasets_tables = {}
    for project in projects:
        # Check if BigQuery API is enabled
        request = service.services().get(
            name=f'projects/{project.project_id}/services/{service_name}')
        response = request.execute()
        if response['state'] == 'ENABLED':
            # Initialize an empty list for each project
            project_datasets_tables[project.project_id] = {}

            # List all datasets in the project
            for dataset in bigquery_client.list_datasets(project.project_id):
                # Initialize an empty dictionary for each dataset
                project_datasets_tables[project.project_id][
                    dataset.dataset_id] = {}
                # List all tables in the dataset
                for table in bigquery_client.list_tables(dataset):
                    # Get the table details
                    table_details = bigquery_client.get_table(table)
                    # Add the table and its size to the dictionary
                    project_datasets_tables[project.project_id][
                        dataset.dataset_id][
                            table.table_id] = table_details.num_bytes

    return project_datasets_tables


if __name__ == '__main__':
    # Replace with your organization ID
    organization_id = f'organizations/{ORGANIZATION_ID}'

    datasets = get_all_datasets(organization_id)

    for project, datasets in datasets.items():
        print('Project: {}'.format(project))
        for dataset, tables in datasets.items():
            print('\___\tDataset: {}'.format(dataset))
            for i, (table, size) in enumerate(tables.items(), start=1):
                # size in bytes as per [docs](https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.Table#google_cloud_bigquery_table_Table_num_bytes)
                print('\t\_______\tTable {}: {}, Size: {} bytes'.format(
                    i, table, size))
        print()
