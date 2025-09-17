from datetime import datetime
from airflow.decorators import dag
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

from airflow_utils import (
    DATA_IMAGE,
)


@dag(
    dag_id="landRegistry_dag",
    schedule_interval="@monthly",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["landRegistry", "extract"],
)
def landRegistry_extract():
    """landRegistry_extract
    langRegistry data extraction DAG.
    """
    landRegistry_extract_task = KubernetesPodOperator(
        task_id="landRegistry_extract_task",
        name="landRegistry-extract-task",
        namespace="airflow",
        image=DATA_IMAGE,
        cmds=["uv run python", "house/extract/landRegistry/landRegistry_extract.py"],
        arguments=["--complete=False"],
        labels={"task": "python"},
        get_logs=True,
        is_delete_operator_pod=True,
    )

    landRegistry_extract_task


dag = landRegistry_extract()
