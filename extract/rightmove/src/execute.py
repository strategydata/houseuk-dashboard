import json
import logging
import sys
from os import environ as env

from api import Rightmove

if __name__=="__main__":
    logging.basicConfig(stream=sys.stdout,level=20)
    rm = Rightmove("https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E1195&insId=1")
    print(rm.get_results)
    print(rm.results_count)
    print(rm.average_price)