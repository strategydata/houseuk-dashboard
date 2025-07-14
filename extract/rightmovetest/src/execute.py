import logging
import sys
from os import environ as env

from amberdata.orchestration_utils import (
    snowflake_engine_factory,
    snowflake_stage_load_copy_remove,
)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=20)
    # greystone, sheffield
    # rm = Rightmove("https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E68508&inside=1&sortType=6")
    # logging.info("Getting latest house records")
    # rm.get_results.to_json("rightmove_out.json")
    # print(rm.results_count)
    # logging.info("Getting "+str(rm.results_count)+" house")
    config_dict = env.copy()
    snowflake_load_database = config_dict["SNOWFLAKE_LOAD_DATABASE"].strip()
    logging.info("Getting " + str(snowflake_load_database) + " value")
    snowflake_engine = snowflake_engine_factory(config_dict, "LOADER")
    logging.info("Getting snowflake engine")
    snowflake_stage_load_copy_remove(
        "rightmove_out.json",
        f"{snowflake_load_database}.rightmove.rightmove_load",
        f"{snowflake_load_database}.rightmove.property",
        snowflake_engine,
    )
