# house-data

This repo contains house data for house buyers in the UK. I've deepened my expertise in Data Engineering, MLOps, and ML Engineering from [Data Talk Club](https://datatalks.club/). This project presents this journey and demonstrates my learning and skills.

this project lies in its comprehensive architecture, designed to predict house prices with precision. It contains:
1. Data Engineering through an asynchronous web scraper and batch ingestion pipelines, enabling efficient data extraction and preprocessing.
2. ML Engineering with a focus on model training and feature engineering
3. MLOps by implementing monitoring practices to ensure the system's reliability and performance over time.

this project has use data source:

## Problem
this is simple project this takes data from the land registry and transforms it in order to visualize the best house

## Dataset and Methods
The chosen dataset for this project:
- this is for house transaction dataset (land registry[https://landregistry.data.gov.uk/app/ppd/]).
- this is crime data from the police [https://data.police.uk/data/archive/]
- This is a sales and rental house dataset from [rightmove](https://www.rightmove.co.uk/).

| Data | Extraction | Raw Format | destination |
| --------- | --------- | ---------- | --------- |
| land Registry | airflow,extract from link | csv | Snowflake |
| crime data | airflow, extract from link | zip and csv | Snowflake |
| rightmove | scrapy | json | Snowflake |

The dataset contains every single public transaction made by house transaction, from transaction info such as prices, house details

## Dashboard

you may access the dashboard with the visualization in this link[http://amberdata.link/house]


## Project details and implementation

This project makes use of Google Cloud Platform, particularly Cloud Storage and BigQuery.

Cloud infrastructure is mostly managed with Terraform, except for Airflow and dbt instances (detailed below in the reproduce the project section)

Data ingestion is carried out by an Airflow DAG. The DAG downloads new data hourly and ingests in to a Cloud Storage bucket which behaves as the Data Lake for the project. The dataset is inJSON format;  the DAG transforms it in order to get rid of any payload objects and parquetizes the data before uploading it. the DAG also creates an external table in BigQuery for querying the parquet files.

The Data Warehouse is defined with DBT

## Reproduce the project
### Prerequisites
The following requirements are needed to reproduce the project :
1. A Google Cloud Platform account
2. The Google Cloud SDK
3. A SSH client
4. AWS account

### EC2

inside ec2, you

## Data Extraction and Processing
