.PHONY: build

SHELL:=/bin/zsh
TEST_FOLDERS_PATH := $(shell eval find . -name "test" -type d)
PATH := $(PATH):$(PWD):$(TEST_FOLDERS_PATH)
GIT_BRANCH = $$(git symbolic-ref --short HEAD)
DOCKER_UP = "export GIT_BRANCH=$(GIT_BRANCH) && docker-compose up"
DOCKER_DOWN = "export GIT_BRANCH=$(GIT_BRANCH) && docker-compose down"
DOCKER_RUN = "export GIT_BRANCH=$(GIT_BRANCH) && docker-compose run"
DBT_DEPS = "cd transform/snowflake-dbt/ && poetry run dbt clean && poetry run dbt deps"

.EXPORT_ALL_VARIABLES:
DATA_TEST_BRANCH=main
DATA_SIREN_BRANCH=master
SNOWFLAKE_SNAPSHOT_DATABASE=SNOWFLAKE
SNOWFLAKE_LOAD_DATABASE=RAW
SNOWFLAKE_PREP_DATABASE=PREP
SNOWFLAKE_STATIC_DATABASE=STATIC
SNOWFLAKE_PREP_SCHEMA=preparation
SNOWFLAKE_PROD_DATABASE=PROD
SNOWFLAKE_TRANSFORM_WAREHOUSE=ANALYST_XS
SALT=pizza
SALT_IP=pie
SALT_NAME=pepperoni
SALT_EMAIL=cheese
SALT_PASSWORD=416C736F4E6F745365637265FFFFFFAB

VENV_NAME?=dbt

.DEFAULT: help

help:
	@echo "\
	-----------------------------------------------------------------------------------------------------------------------"
########################################################################################################################
# Airflow
########################################################################################################################
airflow:
	@if [ "$(GIT_BRANCH)" = "master" ]; then echo "GIT_BRANCH must not be master" && exit 1; fi
	@echo "Attaching to the Webserver container..."
	@"$(DOCKER_DOWN)"
	@"$(DOCKER_UP)" -d airflow_webserver
	@sleep 5
	@docker-compose exec airflow_scheduler gcloud auth activate-service-account --key-file=/root/gcp_service_creds.json --project=gitlab-analysis
	@docker-compose exec airflow_webserver bash

init-airflow:
	@echo "Initializing the Airflow DB..."
	@"$(DOCKER_UP)" -d airflow_db
	@sleep 5
	@"$(DOCKER_RUN)" airflow_scheduler airflow db init
	@"$(DOCKER_RUN)" airflow_scheduler airflow users create --role Admin -u admin -p admin -e datateam@gitlab.com -f admin -l admin
	@"$(DOCKER_RUN)" airflow_scheduler airflow pools set gitlab-ops-pool 2 "Airflow pool for ops database extract"
	@"$(DOCKER_RUN)" airflow_scheduler airflow pools set customers-pool 2 "Airflow pool for customer database full extract"
	@"$(DOCKER_RUN)" airflow_scheduler airflow pools set gitlab-com-pool 8 "Airflow pool for gitlab database incremental extract"
	@"$(DOCKER_RUN)" airflow_scheduler airflow pools set gitlab-com-scd-pool 16 "Airflow pool for gitlab database full extract"
	@"$(DOCKER_DOWN)"

########################################################################################################################
# Utilities
########################################################################################################################
cleanup:
	@echo "Cleaning things up..."
	@"$(DOCKER_DOWN)" -v
	@docker system prune -f

data-image:
	@echo "Attaching to data-image and mounting repo..."
	@"$(DOCKER_RUN)" data_image bash

update-containers:
	@echo "Pulling latest containers for airflow-image, analyst-image, data-image and dbt-image..."
	@docker pull registry.gitlab.com/gitlab-data/data-image/airflow-image:latest
	@docker pull registry.gitlab.com/gitlab-data/analyst-image:latest
	@docker pull registry.gitlab.com/gitlab-data/data-image/data-image:latest
	@docker pull registry.gitlab.com/gitlab-data/dbt-image:latest

########################################################################################################################
# DBT
########################################################################################################################
prepare-dbt:
	python3 -m pip install poetry==1.5.1
	cd transform/snowflake-dbt/ && poetry install
	"$(DBT_DEPS)"

prepare-dbt-fix:
	python3 -m pip install poetry==1.5.1 --break-system-packages
	cd transform/snowflake-dbt/ && poetry install
	"$(DBT_DEPS)"

run-dbt-no-deps:
	cd transform/snowflake-dbt/ && poetry shell;

clone-dbt-select-local-branch:
	cd transform/snowflake-dbt/ && export INPUT=$$(poetry run dbt --quiet ls --models $(DBT_MODELS) --output json --output-keys "database schema name depends_on unique_id alias") && \
	export ENVIRONMENT="LOCAL_BRANCH" && export GIT_BRANCH=$(GIT_BRANCH) && poetry run ../../orchestration/clone_dbt_models_select.py $$INPUT;

clone-dbt-select-local-user:
	cd transform/snowflake-dbt/ && export INPUT=$$(poetry run dbt --quiet ls --models $(DBT_MODELS) --output json --output-keys "database schema name depends_on unique_id alias") && \
	export ENVIRONMENT="LOCAL_USER" && export GIT_BRANCH=$(GIT_BRANCH) && poetry run ../../orchestration/clone_dbt_models_select.py $$INPUT;

clone-dbt-select-local-user-noscript:
	cd transform/snowflake-dbt/ && curl https://dbt.gitlabdata.com/manifest.json -o reference_state/manifest.json && poetry run dbt clone --select $(DBT_MODELS) --state reference_state --full-refresh;

dbt-deps:
	"$(DBT_DEPS)"
	exit

run-dbt:
	"$(DBT_DEPS)"
	cd transform/snowflake-dbt/ && poetry shell;

run-dbt-docs:
	"$(DBT_DEPS)"
	cd transform/snowflake-dbt/ && poetry run dbt docs generate --target docs && poetry run dbt docs serve --port 8081;

clean-dbt:
	cd transform/snowflake-dbt/ && poetry run dbt clean && poetry env remove python3

########################################################################################################################
# Python
########################################################################################################################
prepare-python:
	which uv || python -m pip install uv --break-system-packages
	uv sync

update-dbt-poetry:
	cd transform/snowflake-dbt/ && poetry install
	exit

complexity:
	@echo "Running complexity (Xenon)..."
	@uv run xenon --max-absolute B --max-modules B --max-average C .

vulture:
	@echo "Running vulture..."
	@uv run vulture . --min-confidence 100

pytest:
	@echo "Running pytest..."
	@uv run python -m pytest -vv -x

python_code_quality:  complexity vulture pytest
	@echo "Running python_code_quality..."

pre:
	@echo "Running pre-commit hooks..."
	@uv run pre-commit run --all-files

scrapy:
	@echo "Running scrapy..."
	@uv run scrapy crawl rightmove
