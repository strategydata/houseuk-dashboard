import logging
import os
import sys
import json
from snowflake.sqlalchemy import URL as snowflake_URL
from sqlalchemy import text,create_engine
from sqlalchemy.engine.base import Engine
from typing import List, Tuple, Any,Dict
from pathlib import Path
def snowflake_engine_factory(
    args: Dict[str, str],
    role: str,
    schema: str = "",
    load_warehouse: str = "SNOWFLAKE_LOAD_WAREHOUSE",
) -> Engine:
    """
    Create a database engine from a dictionary of database info.
    """

    # Figure out which vars to grab
    role_dict = {
        "SYSADMIN": {
            "USER": "SNOWFLAKE_USER",
            "PASSWORD": "SNOWFLAKE_PASSWORD",
            "ACCOUNT": "SNOWFLAKE_ACCOUNT",
            "DATABASE": "SNOWFLAKE_LOAD_DATABASE",
            "WAREHOUSE": load_warehouse,
            "ROLE": "SYSADMIN",
        },
        "ANALYTICS_LOADER": {
            "USER": "SNOWFLAKE_LOAD_USER",
            "PASSWORD": "SNOWFLAKE_LOAD_PASSWORD",
            "ACCOUNT": "SNOWFLAKE_ACCOUNT",
            "DATABASE": "SNOWFLAKE_PROD_DATABASE",
            "WAREHOUSE": load_warehouse,
            "ROLE": "LOADER",
        },
        "LOADER": {
            "USER": "SNOWFLAKE_LOAD_USER",
            "PASSWORD": "SNOWFLAKE_LOAD_PASSWORD",
            "ACCOUNT": "SNOWFLAKE_ACCOUNT",
            "DATABASE": "SNOWFLAKE_LOAD_DATABASE",
            "WAREHOUSE": load_warehouse,
            "ROLE": "LOADER",
        },
        "DATA_SCIENCE_LOADER": {
            "USER": "SNOWFLAKE_DATA_SCIENCE_LOAD_USER",
            "PASSWORD": "SNOWFLAKE_DATA_SCIENCE_LOAD_PASSWORD",
            "ACCOUNT": "SNOWFLAKE_ACCOUNT",
            "DATABASE": "SNOWFLAKE_PROD_DATABASE",
            "WAREHOUSE": load_warehouse,
            "ROLE": "DATA_SCIENCE_LOADER",
        },
        "CI_USER": {
            "USER": "SNOWFLAKE_USER",  ## this is the CI User
            "PASSWORD": "SNOWFLAKE_PASSWORD",
            "ACCOUNT": "SNOWFLAKE_ACCOUNT",
            "DATABASE": "SNOWFLAKE_PROD_DATABASE",
            "WAREHOUSE": "SNOWFLAKE_TRANSFORM_WAREHOUSE",
            "ROLE": "TRANSFORMER",
        },
        "SALES_ANALYTICS": {
            "USER": "SNOWFLAKE_LOAD_USER",
            "PASSWORD": "SNOWFLAKE_LOAD_PASSWORD",
            "ACCOUNT": "SNOWFLAKE_ACCOUNT",
            "DATABASE": "SNOWFLAKE_LOAD_DATABASE",
            "WAREHOUSE": load_warehouse,
            "ROLE": "SALES_ANALYTICS",
        },
    }

    vars_dict = role_dict[role]

    conn_string = snowflake_URL(
        user=args[vars_dict["USER"]],
        password=args[vars_dict["PASSWORD"]],
        account=args[vars_dict["ACCOUNT"]],
        database=args[vars_dict["DATABASE"]],
        warehouse=args[vars_dict["WAREHOUSE"]],
        role=vars_dict["ROLE"],  # Don't need to do a lookup on this one
        schema=schema,
    )

    return create_engine(
        conn_string, connect_args={"sslcompression": 0, "autocommit": True}
    )




def snowflake_stage_load_copy_remove(
    file: str,
    stage: str,
    table_path: str,
    engine: Engine,
    type: str = "json",
    on_error: str = "abort_statement",
    file_format_options: str = "",
    col_names: str = "",
):
    """
    Uploads a file to a Snowflake stage, copies its contents into a target table, and removes the staged file.
    This function performs the following steps:
    1. Removes any existing file with the same name from the specified Snowflake stage.
    2. Uploads (PUT) the local file to the Snowflake stage, with optional auto-compression.
    3. Executes a COPY INTO command to load the staged file into the specified table.
    4. Removes the staged file after loading.
    Args:
        file (str): Path to the local file to upload.
        stage (str): Name of the Snowflake stage to use.
        table_path (str): Fully qualified path of the target table in Snowflake.
        engine (Engine): SQLAlchemy engine connected to Snowflake.
        type (str, optional): File format type (e.g., "json", "csv","Avro","ORC","Parquet","XML","TSV"). Defaults to "json".
        on_error (str, optional): Error handling strategy for COPY INTO (e.g., "abort_statement"). Defaults to "abort_statement".
        file_format_options (str, optional): For semi-structured file formats (JSON, Avro, etc.), the only supported character set is UTF-8, 
                                            for delimited files, the default character set is UTF-8. you can find support file format options https://docs.snowflake.com/en/user-guide/intro-summary-loading
        col_names (str, optional): Column names or mapping for COPY INTO. Defaults to "".
    Raises:
        Any exceptions raised during query execution are propagated.
    Note:
        The function logs each step and query for debugging purposes.
    
    """

    file_name = os.path.basename(file)
    if file_name.endswith(".gz"):
        full_stage_file_path = f"{stage}/{file_name}"
    else:
        full_stage_file_path = f"{stage}/{file_name}.gz"
    remove_query = f"remove @{full_stage_file_path};"
    put_query = f"put 'file://{file}' @{stage} auto_compress=true;"

    col_names = _validate_and_format_snowflake_col_names(col_names, type)

    if type == "json":
        copy_query = f"""copy into {table_path} {col_names}
                         from @{full_stage_file_path}
                         file_format=(type='{type}'),
                         on_error='{on_error}';
                         """

    else:
        copy_query = f"""copy into {table_path} {col_names}
                         from @{full_stage_file_path}
                         file_format=(type='{type}' {file_format_options}),
                         on_error='{on_error}';
                        """

    logging.basicConfig(stream=sys.stdout, level=20)

    logging.info("Preview of queries to be run:")
    logging.info(f"\nremove_query: {remove_query}")
    logging.info(f"\nput_query: {put_query}")
    logging.info(f"\ncopy_query: {copy_query}")

    try:
        conn = engine.connect()
        steps = [
            ("Removing leftover files from stage", remove_query),
            (f"Putting {file} to Snowflake stage", put_query),
            (f"Copying to table {table_path}", copy_query),
            (f"Removing {file} from stage", remove_query),
        ]

        for step_description, query in steps:
            logging.info(f"{step_description} ...")
            query_executor(engine, query, dispose_engine=False, connection=conn)
            logging.info(f"Successfully completed: {step_description}")

    finally:
        conn.close()
        engine.dispose()

def query_executor(
    engine: Engine,
    query: str,
    dispose_engine: bool = True,
    connection=None,
    *args,
    **kwargs,
) -> List[Tuple[Any]]:
    """
    Execute SQL queries safely with proper connection management.

    Executes a SQL query using either an existing connection or creates a new one.
    Handles connection cleanup and optional engine disposal.

    Args:
    engine: SQLAlchemy engine instance
    query: SQL query string to execute
    dispose_engine: Whether to dispose engine after execution (default: True)
    connection: Existing SQLAlchemy connection to reuse (default: None)
    Will keep connection alive, if originally passed in.

    Returns:
    List[Tuple[Any]]: Results from the query execution

    Example:
    # New connection
    results = query_executor(engine, "SELECT * FROM table")

    # Reuse existing connection
    with engine.connect() as conn:
        results1 = query_executor(engine, query1, connection=conn)
        results2 = query_executor(engine, query2, connection=conn)
    """
    should_close_connection = connection is None
    try:
        if should_close_connection:
            connection = engine.connect()
        results = execute_query_str(connection, query, *args, **kwargs).fetchall()
        return results
    finally:
        if should_close_connection:
            connection.close()
        if dispose_engine:
            engine.dispose()


def _validate_and_format_snowflake_col_names(col_names: str, type: str):
    # for json files, default to jsontext column
    if type.lower() == "json" and col_names == "":
        return "(jsontext)"

    # if user passes in col_names, it must include '(' and ')'
    if col_names and ("(" not in col_names or ")" not in col_names):
        raise ValueError(
            "col_names arg needs to include '(' and ')' characters, i.e `(first_name, last_name)`."
        )
    return col_names

def execute_query_str(connection, query_str: str, *args, **kwargs) -> List[Tuple[Any]]:
    """
    Execute either a raw SQL query string or SQLAlchemy construct.
    For raw SQL strings, wraps with SQLAlchemy's text() function.
    For SQLAlchemy constructs (like DropTable), passes them directly.

    Args:
        connection: SQLAlchemy connection
        query_str: Either a raw SQL string or SQLAlchemy construct (like DropTable)

    Example:
        execute_query_str(conn, "SELECT * FROM my_table")
        execute_query_str(conn, DropTable(my_table))
    """
    if isinstance(query_str, str):
        return connection.execute(text(query_str), *args, **kwargs)
    return connection.execute(query_str, *args, **kwargs)

def push_to_xcom_file(xcom_json: Dict[Any, Any]) -> None:
    """
    Writes the json passed in as a parameter to the file path required by KubernetesPodOperator to make the json an xcom in Airflow.
    Overwrites any data already there.
    This is primarily used to push metrics to prometheus right now.
    """

    xcom_file_name = "/airflow/xcom/return.json"
    Path("/airflow/xcom/").mkdir(parents=True, exist_ok=True)
    with open(xcom_file_name, "w") as xcom_file:
        json.dump(xcom_json, xcom_file)

