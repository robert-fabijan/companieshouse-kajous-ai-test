import functions_framework
import sys
import os
import requests

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
    response = requests.get(url)
    if response.status_code != 200:
        return f'Failed to download file from {url}', 500
    
    # with open("file.zip", "wb") as file:
    #     file.write(response.content)

    print("File downloaded successfully!")
    
    print()

    # # Bucket upload
    GCloudIntegrationObject = GCloudIntegration(project_id = 'companieshouse-test') 
    # secret = GCloudIntegrationObject.get_secret(project_id = 'companieshouse-test', secret_id = "credentials-for-authentication")
    GCloudIntegrationObject.upload_data_to_cloud_from_file(
        secret = os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        bucket_name = 'companieshouse_bucket',
        response = response,
        blob_name = 'raw_files_companieshouse',
        filename = filename
    )
    
    return 'Test'
