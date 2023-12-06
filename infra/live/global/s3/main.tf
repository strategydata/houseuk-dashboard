terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
    project = var.project
    region=var.region
}

resource "google_storage_bucket" "amberdata-house-uk" {
  name = "amberdata_house_uk"
  location = var.region

  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }

    condition {
      age=30
    }
  }

  force_destroy = true
}


resource "google_bigquery_dataset" "amberdata-dataset" {
  dataset_id = var.BQ_DATASET
  project = var.project
  location = var.region
}



# provider "aws" {
#   region     = "eu-west-2"
# }

# resource "aws_s3_bucket" "terraform_state" {
#   bucket        = var.amberdata_bucket
#   force_destroy = true
# }

# resource "aws_s3_bucket_versioning" "enabled" {
#   bucket = aws_s3_bucket.terraform_state.id
#   versioning_configuration {
#     status = "Enabled"
#   }
# }

# resource "aws_s3_bucket_public_access_block" "public_access" {
#   bucket                  = aws_s3_bucket.terraform_state.id
#   block_public_acls       = true
#   block_public_policy     = true
#   ignore_public_acls      = true
#   restrict_public_buckets = true
# }

# resource "aws_dynamodb_table" "terraform_locks" {
#   name         = var.amberdata_table
#   billing_mode = "PAY_PER_REQUEST"
#   hash_key     = "LockID"
#   attribute {
#     name = "LockID"
#     type = "S"
#   }
# }
