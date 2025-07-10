import logging
import json
import pyspark
import sys
from os import environ as env

if __name__=="__main__":
    logging.basicConfig(stream=sys.stdout, level=20)

    record_counts = {}

    bamboo = BambooAPI(subdomain="gitlab")

    config_dict = env.copy()
    snowflake_load_database = config_dict["SNOWFLAKE_LOAD_DATABASE"].strip()

    snowflake_engine = snowflake_engine_factory(config_dict, "LOADER")

    # Company Directory
    logging.info("Getting latest employee directory.")

    employees = bamboo.get_employee_directory()

    record_counts["directory"] = len(employees)

    with open("directory.json", "w") as outfile:
        json.dump(employees, outfile)

    snowflake_stage_load_copy_remove(
        "directory.json",
        f"{snowflake_load_database}.bamboohr.bamboohr_load",
        f"{snowflake_load_database}.bamboohr.directory",
        snowflake_engine,
    )

    # Tabular Data
    tabular_data = dict(
        compensation="compensation",
        jobinfo="jobInfo",
        employmentstatus="employmentStatus",
        custombonus="customBonus",
        customontargetearnings="customOnTargetEarnings",
        customcurrencyconversion="customCurrencyConversion",
    )

    for key, value in tabular_data.items():
        logging.info(f"Querying for {value} tabular data...")
        data = bamboo.get_tabular_data(value)

        record_counts[key] = len(data)

        with open(f"{key}.json", "w") as outfile:
            json.dump(data, outfile)

        snowflake_stage_load_copy_remove(
            f"{key}.json",
            f"{snowflake_load_database}.bamboohr.bamboohr_load",
            f"{snowflake_load_database}.bamboohr.{key}",
            snowflake_engine,
        )

    # Custom Reports
    report_mapping = dict(id_employee_number_mapping="498")

    for key, value in report_mapping.items():
        logging.info(f"Querying for report number {value} into table {key}...")
        data = bamboo.get_report(value)

        with open(f"{key}.json", "w") as outfile:
            json.dump(data, outfile)

        record_counts[key] = len(data["employees"])

        snowflake_stage_load_copy_remove(
            f"{key}.json",
            f"{snowflake_load_database}.bamboohr.bamboohr_load",
            f"{snowflake_load_database}.bamboohr.{key}",
            snowflake_engine,
        )

    # Metadata
    metadata_mapping = dict(meta_fields="fields")

    for key, value in metadata_mapping.items():
        logging.info(f"Getting metadata for fields...")
        data = bamboo.get_metadata(value)

        with open(f"{key}.json", "w") as outfile:
            json.dump(data, outfile)

        record_counts[key] = len(data)

        snowflake_stage_load_copy_remove(
            f"{key}.json",
            f"{snowflake_load_database}.bamboohr.bamboohr_load",
            f"{snowflake_load_database}.bamboohr.{key}",
            snowflake_engine,
        )

    push_to_xcom_file(record_counts)


