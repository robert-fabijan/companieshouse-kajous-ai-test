

# Set up Cloud Function for air-pollution API data extraction
resource "google_cloudfunctions_function" "companieshouse-download-file" {
  name                  = "companieshouse-function"
  description           = "Function to download file from Companies House UK"
  runtime               = "python311"
  available_memory_mb   = 256
  source_repository {
    url = "https://source.developers.google.com/projects/${var.gcp_project}/repos/${var.repository_name}/moveable-aliases/${var.branch_name}/paths/${var.source_directory}"
  }
  trigger_http          = true
  entry_point           = "gcloud_download_companieshouse_file"
}


# Create BigQuery dataset
resource "google_bigquery_dataset" "companieshouse_dataset_unified" {
    dataset_id = "companieshouse_dataset_unified"
    description = "Dataset for data processed from OpenWeather API."
    location = "EU"
}

# Create BigQuery table
resource "google_bigquery_table" "companieshouse_data" {
  dataset_id = google_bigquery_dataset.companieshouse_dataset_unified.dataset_id
  table_id = "companieshouse_data"
  time_partitioning {
    type = "DAY"
  }

  schema = file("${path.module}/../bigquery_schema.json")
    
}