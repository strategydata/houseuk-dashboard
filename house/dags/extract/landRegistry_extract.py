from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

from airflow_utils import (
    DATA_IMAGE,
    clone_repo_cmd
)


@dag(
    dag_id="example_taskflow_k8s_dag",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["kubernetes", "taskflow"],
)
def taskflow_k8s_dag():
    """
    Example DAG using TaskFlow API + KubernetesPodOperator.
    """

    @task
    def start_message():
        print("Starting TaskFlow DAG with Kubernetes...")

    run_python = KubernetesPodOperator(
        task_id="run_python_in_k8s",
        namespace="airflow",
        image=DATA_IMAGE,
        cmds=["python", "-c"],
        arguments=["print('Hello from KubernetesPodOperator - Python!')"],
        labels={"task": "python"},
        name="python-task",
        get_logs=True,
        is_delete_operator_pod=True,
    )

    @task
    def end_message():
        print("TaskFlow DAG finished!")

    # Dependencies with TaskFlow style
    start = start_message()
    end = end_message()

    start >> run_python >> end


dag = taskflow_k8s_dag()
