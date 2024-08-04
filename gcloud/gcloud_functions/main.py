import functions_framework
import sys
import os
import requests
from io import BytesIO
from google.cloud import storage

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  

from shared.models.gcloud_integration import GCloudIntegration

@functions_framework.http
def gcloud_download_companieshouse_file(request, context=None) -> None:
    """
    Run a process of downloading a csv file from companieshouse endpoint

    :param request:
    :param context:
    :return pandas.DataFrame: clean dataframe with air pollution data 
    """
    
    # The URL of the file to download
    url = 'https://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2024-08-01.zip'
    
    # Get the filename from the URL
    filename = url.split('/')[-1]

    # Download the file
    # Create a requests session
    session = requests.Session()
    bucket_name = 'raw_files_companieshouse'

    #  Get the file content from the URL
    response = session.get(url, stream=True)
    if response.status_code == 200:
        # Read the content into a BytesIO object
        file_stream = BytesIO(response.content)
        
        # Create a storage client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        
        # Upload the file content from the BytesIO object
        blob.upload_from_file(file_stream, rewind=True)
        
        print(f"File uploaded to {filename} in bucket {bucket_name}.")
    else:
        response.raise_for_status()

    return "True"
