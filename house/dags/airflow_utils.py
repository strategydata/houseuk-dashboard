"""this file contains common operator/functions to be used across multiple DAGs"""

import os
import pathlib
from datetime import date, timedelta


if os.environ["IN_CLOUD"] == "False":
    REPO_BASE_PATH = f"{os.environ['AIRFLOW_HOME']}/houseuk-dashboard"
else:
    REPO_BASE_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/repo"

SSH_REPO = "git@github.com:strategydata/houseuk-dashboard.git"
HTTP_REPO = "https://github.com/strategydata/houseuk-dashboard.git"

# Docker images for different pipeline stages
PYTHON_IMAGE = "python:3.11-slim"
DATA_PROCESSING_IMAGE = "pandas/pandas:latest"
JUPYTER_IMAGE = "jupyter/scipy-notebook:latest"
DBT_IMAGE = "ghcr.io/dbt-labs/dbt-core:1.9.10"

# Project paths
AIRFLOW_NOTEBOOKS_PATH = f"{REPO_BASE_PATH}/notebooks"


def get_ml_notebooks(frequency: str) -> dict:
    """get_ml_notebooks Get ML notebooks
    for different execution frequencies
    Args:
        frequency (str): _description_

    Returns:
        dict: _description_
    """
    notebooks = []
    fileNames = []
    path = pathlib.Path(f"{AIRFLOW_NOTEBOOKS_PATH}/{frequency}/")
    for file in path.rglob("*.ipynb"):
        relative_path = file.relative_to(AIRFLOW_NOTEBOOKS_PATH)
        notebooks.append(relative_path.as_posix())
        expanded_name = (
            str(relative_path.parent).replace("/", "_") + "_" + relative_path.stem
        )
        fileNames.append(expanded_name)
    return dict(zip(notebooks, fileNames, strict=False))


# Data ingestion pipeline DAGs
data_ingestion_dags = [
    "rightmove_data_extraction",
    "land_register_data_extraction",
    "crime_data_extraction",
    "property_features_extraction",
    "postcode_data_extraction",
]

# Data processing pipeline DAGs
data_processing_dags = [
    "data_cleaning_rightmove",
    "data_cleaning_land_register",
    "data_cleaning_crime_data",
    "feature_engineering",
    "data_validation",
    "data_quality_checks",
]

# ML pipeline DAGs
ml_pipeline_dags = [
    "property_price_prediction_training",
    "property_value_estimation_training",
    "market_trend_analysis",
    "area_classification_training",
    "model_validation_testing",
    "model_deployment",
]

# Analytics and reporting DAGs
analytics_pipeline_dags = [
    "property_analytics_daily",
    "property_analytics_weekly",
    "property_analytics_monthly",
    "market_reports_generation",
    "model_performance_monitoring",
]


def split_date_parts(day: date, partition: str) -> dict:
    """split_date_parts split data into components
    for partitioning

    Args:
        day (date): _description_
        partition (str): _description_

    Returns:
        dict: _description_
    """
    if partition == "month":
        split_dict = {
            "year": day.strftime("%Y"),
            "month": day.strftime("%m"),
            "part": day.strftime("%Y_%m"),
        }
    elif partition == "week":
        week_start = day - timedelta(days=day.weekday())
        split_dict = {
            "year": week_start.strftime("%Y"),
            "week": week_start.strftime("%U"),
            "part": week_start.strftime("%Y_W%U"),
        }
    elif partition == "day":
        split_dict = {
            "year": day.strftime("%Y"),
            "month": day.strftime("%m"),
            "day": day.strftime("%d"),
            "part": day.strftime("%Y_%m_%d"),
        }

    return split_dict


def partitions(from_date: date, to_date: date, partition: str) -> list[dict]:
    """partitions _summary_

    Args:
        from_date (date): _description_
        to_date (date): _description_
        partition (str): _description_

    Returns:
        list[dict]: _description_
    """
    delta = to_date - from_date
    all_parts = [
        split_date_parts((from_date + timedelta(days=i)), partition)
        for i in range(delta.days + 1)
    ]

    seen = set()
    parts = []
    # loops through every day and pulls out unique set of date parts
    for p in all_parts:
        if p["part"] not in seen:
            seen.add(p["part"])
            parts.append({k: v for k, v in p.items()})
    return parts


# GitLab default settings for all DAGs
gitlab_defaults = dict(
    get_logs=True,
    image_pull_policy="Always",
    in_cluster=not os.environ["IN_CLUSTER"] == "False",
    is_delete_operator_pod=True,
    namespace=os.environ["NAMESPACE"],
    cmds=["/bin/bash", "-c"],
)

# GitLab default environment variables for worker pods
env = os.environ.copy()
GIT_BRANCH = env["GIT_BRANCH"]
gitlab_pod_env_vars = {
    "CI_PROJECT_DIR": "/analytics",
    "EXECUTION_DATE": "{{ next_execution_date }}",
    "SNOWFLAKE_PREPARATION_SCHEMA": "preparation",
    "SNOWFLAKE_SNAPSHOT_DATABASE": "RAW"
    if GIT_BRANCH == "master"
    else f"{GIT_BRANCH.upper()}_RAW",
    "SNOWFLAKE_LOAD_DATABASE": "RAW"
    if GIT_BRANCH == "master"
    else f"{GIT_BRANCH.upper()}_RAW",
    "SNOWFLAKE_PREP_DATABASE": "PREP"
    if GIT_BRANCH == "master"
    else f"{GIT_BRANCH.upper()}_PREP",
    "SNOWFLAKE_PROD_DATABASE": "PROD"
    if GIT_BRANCH == "master"
    else f"{GIT_BRANCH.upper()}_PROD",
}
