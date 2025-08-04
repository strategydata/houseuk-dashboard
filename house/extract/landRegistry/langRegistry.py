
import logging
import pandas as pd
import fire


def download_and_save_parquet(complete: bool):
    """
    The function `download_and_save_parquet` downloads a CSV file from a specified URL and saves it as a
    Parquet file based on a boolean parameter.
    
    :param complete: The `complete` parameter is a boolean flag that determines whether to download the
    complete dataset or the monthly update dataset from the specified URLs. If `complete` is `True`, the
    function will download the complete dataset from the first URL and save it as
    "landRegistry_complete.parquet". If `complete
    :type complete: bool
    """
    filename= ""
    url=""
    if complete:
        url = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv"
        filename = "landRegistry_complete.parquet"
    else:
        url = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update-new-version.csv"
        filename = "landRegistry_monthly.parquet"
    logging.info(f"Downloading: {url}")
    df = pd.read_csv(url, encoding="utf-8")
    df.to_parquet(filename, index=False)
    logging.info(f"Downloaded and saved to {filename}")

if __name__ == "__main__":
    fire.Fire(download_and_save_parquet)
    
    