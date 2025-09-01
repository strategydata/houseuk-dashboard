import os
import pendulum

from airflow.sdk import dag
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

from airflow_utils import (
    DATA_IMAGE,
    clone_and_setup_extraction_cmd,
    gitlab_defaults,
    gitlab_pod_env_vars,
    slack_failed_task,
)

from kube_secrets import (
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_LOAD_DATABASE,
    SNOWFLAKE_LOAD_PASSWORD,
    SNOWFLAKE_LOAD_ROLE,
    SNOWFLAKE_LOAD_USER,
    SNOWFLAKE_LOAD_WAREHOUSE,
)

from dags.kubernetes_helpers import get_affinity, get_toleration

# Load the env vars into a dict and set Secrets
env = os.environ.copy()
pod_env_vars = gitlab_pod_env_vars


@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 5, 10, tz="Europe/London"),
)
def landRegistry_extract():
    """DAG to extract data from the land registry"""
    pass


default_args = {
    "depends_on_past": False,
    "on_failure_callback": slack_failed_task,
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "sla": timedelta(hours=12),
    "sla_miss_callback": slack_failed_task,
    "start_date": datetime(2023, 5, 10),
    "dagrun_timeout": timedelta(hours=6),
}

dag = DAG(
    "landRegistry_extract",
    default_args=default_args,
    schedule_interval="0 */2 * * *",
    concurrency=1,
    catchup=False,
)


landRegistry_extract_cmd = f"""
    {clone_and_setup_extraction_cmd} &&
    python landRegistry/src/execute.py
"""

landRegistry_extract = KubernetesPodOperator(
    **gitlab_defaults,
    image=DATA_IMAGE,
    task_id="landRegistry-extract",
    name="landRegistry-extract",
    secrets=[
        SNOWFLAKE_ACCOUNT,
        SNOWFLAKE_LOAD_DATABASE,
        SNOWFLAKE_LOAD_ROLE,
        SNOWFLAKE_LOAD_USER,
        SNOWFLAKE_LOAD_WAREHOUSE,
        SNOWFLAKE_LOAD_PASSWORD,
    ],
    env_vars=pod_env_vars,
    affinity=get_affinity("extraction"),
    tolerations=get_toleration("extraction"),
    arguments=[landRegistry_extract_cmd],
    do_xcom_push=True,
    dag=dag,
)
