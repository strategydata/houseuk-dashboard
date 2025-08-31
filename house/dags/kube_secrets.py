"""This file contains k8s secrets used in all DAGs"""

from airflow.providers.cncf.kubernetes.secret import Secret


# Postgres
PG_PORT = Secret("env", "PG_PORT", "airflow", "PG_PORT")


# dbt
GIT_DATA_TESTS_PRIVATE_KEY = Secret(
    "env",
    "GIT_DATA_TESTS_PRIVATE_KEY",
    "airflow",
    "GIT_DATA_TESTS_PRIVATE_KEY",
)
GIT_DATA_TESTS_CONFIG = Secret(
    "env",
    "GIT_DATA_TESTS_CONFIG",
    "airflow",
    "GIT_DATA_TESTS_CONFIG",
)

# Grafana
GRAFANA_HOST = Secret("env", "GRAPHITE_HOST", "airflow", "GRAPHITE_HOST")
GRAFANA_PASSWORD = Secret("env", "GRAPHITE_PASSWORD", "airflow", "GRAPHITE_PASSWORD")
GRAFANA_USERNAME = Secret("env", "GRAPHITE_USERNAME", "airflow", "GRAPHITE_USERNAME")

# Snowflake Generic
SNOWFLAKE_ACCOUNT = Secret("env", "SNOWFLAKE_ACCOUNT", "airflow", "SNOWFLAKE_ACCOUNT")
SNOWFLAKE_PASSWORD = Secret(
    "env",
    "SNOWFLAKE_PASSWORD",
    "airflow",
    "SNOWFLAKE_PASSWORD",
)

# Snowflake Load
SNOWFLAKE_LOAD_DATABASE = Secret(
    "env",
    "SNOWFLAKE_LOAD_DATABASE",
    "airflow",
    "SNOWFLAKE_LOAD_DATABASE",
)
SNOWFLAKE_LOAD_ROLE = Secret(
    "env",
    "SNOWFLAKE_LOAD_ROLE",
    "airflow",
    "SNOWFLAKE_LOAD_ROLE",
)
SNOWFLAKE_LOAD_PASSWORD = Secret(
    "env",
    "SNOWFLAKE_LOAD_PASSWORD",
    "airflow",
    "SNOWFLAKE_LOAD_PASSWORD",
)
SNOWFLAKE_LOAD_USER = Secret(
    "env",
    "SNOWFLAKE_LOAD_USER",
    "airflow",
    "SNOWFLAKE_LOAD_USER",
)
SNOWFLAKE_LOAD_WAREHOUSE = Secret(
    "env",
    "SNOWFLAKE_LOAD_WAREHOUSE",
    "airflow",
    "SNOWFLAKE_LOAD_WAREHOUSE",
)

SNOWFLAKE_LOAD_WAREHOUSE_MEDIUM = Secret(
    "env",
    "SNOWFLAKE_LOAD_WAREHOUSE_MEDIUM",
    "airflow",
    "SNOWFLAKE_LOAD_WAREHOUSE_MEDIUM",
)

# Snowflake Static
SNOWFLAKE_STATIC_DATABASE = Secret(
    "env",
    "SNOWFLAKE_STATIC_DATABASE",
    "airflow",
    "SNOWFLAKE_STATIC_DATABASE",
)
# Snowflake Transform
SNOWFLAKE_TRANSFORM_ROLE = Secret(
    "env",
    "SNOWFLAKE_TRANSFORM_ROLE",
    "airflow",
    "SNOWFLAKE_TRANSFORM_ROLE",
)
SNOWFLAKE_TRANSFORM_SCHEMA = Secret(
    "env",
    "SNOWFLAKE_TRANSFORM_SCHEMA",
    "airflow",
    "SNOWFLAKE_TRANSFORM_SCHEMA",
)
SNOWFLAKE_TRANSFORM_USER = Secret(
    "env",
    "SNOWFLAKE_TRANSFORM_USER",
    "airflow",
    "SNOWFLAKE_TRANSFORM_USER",
)
SNOWFLAKE_TRANSFORM_WAREHOUSE = Secret(
    "env",
    "SNOWFLAKE_TRANSFORM_WAREHOUSE",
    "airflow",
    "SNOWFLAKE_TRANSFORM_WAREHOUSE",
)
SNOWFLAKE_PREP_WAREHOUSE = Secret(
    "env",
    "SNOWFLAKE_PREP_WAREHOUSE",
    "airflow",
    "SNOWFLAKE_PREP_WAREHOUSE",
)
SNOWFLAKE_PROD_WAREHOUSE = Secret(
    "env",
    "SNOWFLAKE_PROD_WAREHOUSE",
    "airflow",
    "SNOWFLAKE_PROD_WAREHOUSE",
)
SNOWFLAKE_USER = Secret("env", "SNOWFLAKE_USER", "airflow", "SNOWFLAKE_USER")

# Data Science Load Role
SNOWFLAKE_DATA_SCIENCE_LOAD_ROLE = Secret(
    "env",
    "SNOWFLAKE_DATA_SCIENCE_LOAD_ROLE",
    "airflow",
    "SNOWFLAKE_DATA_SCIENCE_LOAD_ROLE",
)
SNOWFLAKE_SALES_ANALYTICS_LOAD_ROLE = Secret(
    "env",
    "SNOWFLAKE_SALES_ANALYTICS_LOAD_ROLE",
    "airflow",
    "SNOWFLAKE_SALES_ANALYTICS_LOAD_ROLE",
)

# Writing to GSheets from Jupyter notebooks
GSHEETS_SERVICE_ACCOUNT_CREDENTIALS = Secret(
    "env",
    "GSHEETS_SERVICE_ACCOUNT_CREDENTIALS",
    "airflow",
    "GSHEETS_SERVICE_ACCOUNT_CREDENTIALS",
)
