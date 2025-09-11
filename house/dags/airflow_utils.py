import os
env = os.environ.copy()
GIT_BRANCH = env["GIT_BRANCH"]
github_pod_env_vars = {
    "CI_PROJECT_DIR": "/extract",
    "EXECUTION_DATE": "{{ next_execution_date }}",
    "SNOWFLAKE_PREPARATION_SCHEMA": "preparation",
    "SNOWFLAKE_SNAPSHOT_DATABASE": (
        "RAW" if GIT_BRANCH == "main" else f"{GIT_BRANCH.upper()}_RAW"
    ),
    "SNOWFLAKE_LOAD_DATABASE": (
        "RAW" if GIT_BRANCH == "main" else f"{GIT_BRANCH.upper()}_RAW"
    ),
    "SNOWFLAKE_PREP_DATABASE": (
        "PREP" if GIT_BRANCH == "main" else f"{GIT_BRANCH.upper()}_PREP"
    ),
    "SNOWFLAKE_PROD_DATABASE": (
        "PROD" if GIT_BRANCH == "main" else f"{GIT_BRANCH.upper()}_PROD"
    ),
    "DBT_RUNNER": (
        "{{ task_instance_key_str }}__{{ run_id }}__{{ task_instance.try_number }}"
        if GIT_BRANCH == "main"
        else f"{GIT_BRANCH.upper()}"
    ),
    "DBT_EXCLUDE_RESOURCE_TYPES": ("unit_test" if GIT_BRANCH == "master" else ""),    
}
DATA_IMAGE="docker.io/kangqiwang/data_image:0.0.1"
DBT_IMAGE=""

SSH_REPO ="git@github.com:strategydata/houseuk-dashboard.git"
HTTP_REPO = "https://github.com/strategydata/houseuk-dashboard.git"

# git commands
data_test_ssh_key_cmd = """
    export DATA_TEST_BRANCH="main" &&
    export DATA_SIREN_BRANCH="master" &&
    mkdir ~/.ssh/ &&
    touch ~/.ssh/id_rsa && touch ~/.ssh/config &&
    echo "$GIT_DATA_TESTS_PRIVATE_KEY" > ~/.ssh/id_rsa && chmod 0400 ~/.ssh/id_rsa &&
    echo "$GIT_DATA_TESTS_CONFIG" > ~/.ssh/config"""

clone_repo_cmd = f"""
    {data_test_ssh_key_cmd} &&
    if [[ -z "$GIT_COMMIT" ]]; then
        export GIT_COMMIT="HEAD"
    fi
    if [[ -z "$DBT_REPO_BRANCH" ]]; then
        export DBT_REPO_BRANCH="master"
    fi 
    if [[ -z "$GIT_DATA_TESTS_PRIVATE_KEY" ]]; then
        export REPO="{HTTP_REPO}";
        else
        export REPO="{SSH_REPO}";
    fi &&
    echo "git clone -b {GIT_BRANCH} --single-branch --depth 1 $REPO" &&
    git clone -b {GIT_BRANCH} --single-branch --depth 1 $REPO &&
    echo "checking out commit $GIT_COMMIT" &&
    cd extract &&
    git checkout $GIT_COMMIT &&
    cd .."""

# extract command
clone_and_setup_extraction_cmd = f"""
    {clone_repo_cmd} &&
    export PYTHONPATH="$CI_PROJECT_DIR/orchestration/:$PYTHONPATH" &&
    cd extract/extract/
    """
