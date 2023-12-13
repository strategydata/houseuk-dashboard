provider "google" {
    project = "amberdata"
    region  = "eu-west2"
}

terraform {
  backend "gcs" {
    bucket  = "amberdata-data-terraform-state"
    prefix  = "data-ops/state"
  }
}

variable "environment" {
    type = string
}



resource "google_container_cluster" "airflow_cluster" {
  project="amberdata-analysis"
  location = "eu-west2"
  provider = google-beta
  name=var.environment == "production" ? "data-ops": ""
}
