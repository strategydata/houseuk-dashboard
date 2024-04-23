import logging
import os
from datetime import datetime,timedelta

from airflow import DAG
# from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator


env = os.environ.copy()


rightmove_extract_cmd =f"""
    
"""

# dag = DAG(
#     "rightmove_extract"
# )




# rightmove_extract = KubernetesPodOperator(
    
# )