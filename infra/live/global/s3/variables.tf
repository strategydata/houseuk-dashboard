variable "project" {
  description = "project id"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "europe-west2"
  type = string
}

variable "storage_class" {
    description = "storage class type for the bucket"
    default = "STANDARD"
}

