import logging
import os
from datetime import datetime,timedelta

from airflow import DAG


env = os.environ.copy()

dag = DAG(
    "rightmove_extract"
)