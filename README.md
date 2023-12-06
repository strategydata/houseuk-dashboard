# house-data

this repo contains house data for house buyers in uk

## Index

## Problem
this is simple project thich takes data from the land registry and transforms it in order to visualize the best house 

## Dataset
The chosen dataset for this project land registry[https://landregistry.data.gov.uk/app/ppd/]. The dataset contains every single public transaction made by house transaction, from transaction info such as prices, house details

## Dashboard

you may access the dashboard with the visualization in this link[http://amberdata.link/house]


## Project details and implementation

This projet makes use of Google Cloud Platform, particularly Cloud Storage and BigQuery.

Cloud infrastructure is mostly managed with Terraform, except for Airflow and dbt instances (detailed below in the reproduce the project section)

Data ingestion is carried out by an Airflow DAG. The DAG downloads new data hourly and ingests in to a Cloud Storage bucket which behaves as the Data Lake for the project. The dataset is inJSON format;  the DAG transforms it in order to get rid of any payload objects and parquetizes the data before uploading it. the DAG also creates an external table in BigQuery for querying the parquet files.

The Data Warehouse is defined with DBT

## Reproduce the project
### Prerequisites
The following requirements are needed to reproduce the project :
1. A Google Cloud Platform account
2. The Google Cloud SDK
3. A SSH client


