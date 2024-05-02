# Create a service account
#!/bin/bash

# Print out environment variables
echo "Running the script with following variables:"
echo "SA_NAME: $SA_NAME"
echo "PROJECT_ID: $PROJECT_ID"
echo "ORGANIZATION_ID: $ORGANIZATION_ID"

gcloud iam service-accounts create $SA_NAME --project=$PROJECT_ID

# Add IAM policy binding to the organization
gcloud organizations add-iam-policy-binding $ORGANIZATION_ID \
  --member="serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/viewer"

# # Create a key for the service account
gcloud iam service-accounts keys create ${SA_NAME}.json --iam-account ${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

# # Activate the service account
gcloud auth activate-service-account --key-file=${SA_NAME}.json
