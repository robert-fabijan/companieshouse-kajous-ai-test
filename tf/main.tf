provider "google" {
  credentials = file(var.gcp_svc_key)
  project     = var.gcp_project
  region      = var.gcp_region
}

provider "google-beta" {
  credentials = file(var.gcp_svc_key)
  project     = var.gcp_project
  region      = var.gcp_region
}

resource "null_resource" "deploy_cloud_function" {
  provisioner "local-exec" {
    command = <<EOT
      gcloud functions deploy companieshouse-function \
        --runtime python311 \
        --trigger-http \
        --entry-point gcloud_download_companieshouse_file \
        --source ../gcloud/gcloud_functions
        --project ${var.gcp_project} \
        --region ${var.gcp_region}
    EOT
  }
}

resource "google_bigquery_dataset" "companieshouse_dataset_unified" {
  dataset_id  = "companieshouse_dataset_unified"
  description = "Dataset for data processed from Companies House UK."
  location    = "EU"
}

resource "google_bigquery_table" "companieshouse_data" {
  dataset_id = google_bigquery_dataset.companieshouse_dataset_unified.dataset_id
  table_id   = "companieshouse_data"
  time_partitioning {
    type = "DAY"
  }

  schema = file("${path.module}/../bigquery_schema.json")
}
