variable "project" {
  description = "project id"
  type = string
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  type = string
}

variable "storage_class" {
    description = "storage class type for the bucket"
    type = string
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
}
