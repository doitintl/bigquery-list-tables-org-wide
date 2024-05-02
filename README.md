# Set-up

To use the script, you need to define certain environment variables that are specific to your Google Cloud setup. These variables include:

- SA_NAME - The name of the service account.
- PROJECT_ID - The ID of your Google Cloud project.
- ORGANIZATION_ID - The ID of your Google Cloud organization.

Edit the .env file to include your specific configurations. 

Before running the script, you need to apply the environment variables set in your .env file. You can do this by sourcing the .env file in your terminal session: `source .env`. 

Then you can run `./sa-setup.sh`. On a high level, the script: 
- Creates a service account in the specified GCP project with the name specified by the `SA_NAME` environment variable.
- It adds an IAM policy binding to the GCP organization giving the previously created service account the `roles/viewer` role within the organization.
- Then a key is created for the service account and saved as a JSON file with the name `${SA_NAME}.json`. 
- Finally, the script activates the service account such that it can be used by our Python script.

Finally, you can run the Python script which will print out the projects being checked under your organisation as well as a list of the datasets per project using `python list_bq_datasets_tables.py`.