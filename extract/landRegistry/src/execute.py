import logging
import pyspark
import sys
from os import environ as env

if __name__=="__main__":
    logging.basicConfig(stream=sys.stdout,level=20)
    config_dict = env.copy()
    df= spark.read.format("csv").load("http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv")
    
    