#!/bin/bash


set -u



URL="http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv"

# update the data on the 20th working day of each month
URL_MONTHLY="http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update-new-version.csv"

if  [ "$1" = "all" ];
then
    echo "download all data"
    URL="http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv"
    LOCAL_PREFIX="data/raw/all"
    LOCAL_PATH="${LOCAL_PREFIX}/complete.csv"
else
    echo "download monthly data"
    URL="http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update-new-version.csv"
    LOCAL_PREFIX="data/raw/monthly"
    LOCAL_PATH="${LOCAL_PREFIX}/monthly.csv"
fi
echo "downloading &{URL_TOTAL}"
mkdir -p ${LOCAL_PREFIX}
wget ${URL} -O ${LOCAL_PATH}
