# gcp-discovery
Project to learn about the Google Cloud Plateform development environment for Data Engineering purposes.
The Job build permit to mine data from a movie API based on random keywords.

Author : Anisse Imer

# Deploy
- You need first to setup BigQuery (API, and init the database).
- Then create a service account with the right roles (BigQuery admin preferably).
- Download the credentials json file, add it to your project naming it "client_secret.json".
- Perform then the following commands
## Commands :
```
# Install/setup - GCP
gcloud auth login
gcloud config set project <project_id>
gcloud services enable cloudfunctions.googleapis.com

# Deploy - Cloud function
gcloud functions deploy cinema_data_fetcher \
    --runtime python311 \
    --trigger-http \
    --allow-unauthenticated \
    --memory 512MB \
    --timeout 540s \
    --region europe-west1 \
    --source .
    --entry-point cinema_data_fetcher

# Deploy - Scheduler (every 5 minutes)
gcloud scheduler jobs create http cinema-data-fetcher-job \
    --schedule="*/5 * * * *" \
    --uri=https://europe-west1-striking-talent-462114-d2.cloudfunctions.net/cinema-data-fetcher \
    --http-method=GET \
    --time-zone="Europe/Paris" \
    --location=europe-west1

# Read logs
gcloud functions logs read cinema-data-fetcher --region europe-west1 --limit 50
```

## Sources :
- Oauth2 : https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account
- BigQuery - python : https://medium.com/@akshaybagal/mastering-google-bigquery-with-python-a-comprehensive-guide-to-data-extraction-and-analysis-4e43af30b5c6
- BigQuery - sql : 
    - https://medium.com/data-engineers-notes/bigquery-primary-key-foreign-key-constraints-593d53be380
