import functions_framework
import json
import os
import requests
from google.cloud import storage
from google.oauth2 import service_account


@functions_framework.http
def gcloud_download_companieshouse_file(request, context=None) -> str:
    """
    Download a CSV file from Companies House endpoint and upload it to a Google Cloud Storage bucket.

    :param request:
    :param context:
    :return: Confirmation string indicating successful upload.
    """
    # The URL of the file to download
    url = 'https://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2024-08-01.zip'
    
    # Get the filename from the URL
    filename = url.split('/')[-1]
    bucket_name = 'raw_files_companieshouse'

    # Load credentials from JSON
    credentials = service_account.Credentials.from_service_account_info(json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS']))
    

    # Start a session and download the file
    with requests.Session() as session:
        with session.get(url, stream=True) as response:
            response.raise_for_status()  # Check for HTTP errors

            # Stream the file directly into GCS without saving locally
            storage_client = storage.Client(credentials=credentials)
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(filename)
            
            # Stream directly from the response to GCS
            blob.upload_from_file(response.raw, content_type='application/zip', rewind=True)
            print(f"File uploaded to {filename} in bucket {bucket_name}.")

    return "File successfully uploaded."

