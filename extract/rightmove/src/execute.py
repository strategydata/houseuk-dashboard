import json
import logging
import sys
from os import environ as env

from api import Rightmove

if __name__=="__main__":
    logging.basicConfig(stream=sys.stdout,level=20)
    # greystone, sheffield
    rm = Rightmove("https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=OUTCODE%5E2250&insId=1&sortType=6")
    logging.info("Getting lastest house records")
    rm.get_results.to_json("rightmove_out.json")
    print(rm.results_count)
    logging.info("Getting "+str(rm.results_count)+" house")
    