from datetime import datetime
from airflow.decorators import dag
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

from airflow_utils import (
    DATA_IMAGE,
)


@dag(
    dag_id="crime_dag",
    schedule_interval="@monthly",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["crime", "extract"],
)
def crime_extract():
    """crime_extract
    crime data extraction DAG.
    """
    crime_extract_task = KubernetesPodOperator(
        task_id="crime_extract_task",
        name="crime-extract-task",
        namespace="airflow",
        image=DATA_IMAGE,
        cmds=["uv run python", "house/extract/crime/crime.py"],
        arguments=["--all=False"],
        labels={"task": "python"},
        get_logs=True,
        is_delete_operator_pod=True,
    )

    crime_extract_task


dag = crime_extract()
