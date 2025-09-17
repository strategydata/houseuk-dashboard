import requests
import fire
from datetime import date
from dateutil.relativedelta import relativedelta
import zipfile
import os
import io


class CrimeData:
    def __init__(self, timeout=120, output_dir="/data/crime"):
        self.base_url = "https://data.police.uk/data/archive/"

        self.timeout = timeout
        # Global Headers for requests
        self.header = {}
        self.output_dir = output_dir

    def load_all_history(
        self, start: date = date(2013, 12, 1), end: date = date.today()
    ):
        """
        load_all_history Load all history from start to end date, defaults to start date 2013-12-01 to today, because data.police.uk only has data from 2013-12-01
        see https://data.police.uk/data/archive/
        """
        while start < end:
            url = f"{self.base_url}{start.strftime('%Y-%m')}.zip"
            start += relativedelta(years=1, months=11)
            csv_files = self.load_data(url)
            print(csv_files)

    def load_data(self, url: str) -> list[str]:
        content = self.download_zip(url)
        csv_files = self.extract_csv_from_zip(content)
        return csv_files

    def download_zip(self, url: str) -> bytes:
        """
        load_data Load data from url
        """
        r = requests.get(url, headers=self.header, timeout=self.timeout)
        r.raise_for_status()
        return r.content

    def extract_csv_from_zip(self, zip_content: bytes) -> list[str]:
        """extract_csv_from_zip extracts all csv files from a zip file content and returns a list of csv file names

        Args:
            zip_content (bytes): _description_

        Returns:
            list[str]: _description_
        """
        extracted_files = []
        with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
            csv_files = [
                f for f in z.namelist() if f.endswith(".csv") and not f.endswith("/")
            ]
            for f in csv_files:
                normalized_path = f.replace("\\", os.sep).replace("/", os.sep)
                out_path = os.path.join(self.output_dir, normalized_path)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with z.open(f) as src, open(out_path, "wb") as dst:
                    dst.write(src.read())
                extracted_files.append(out_path)
        return extracted_files

    def load_latest_data(self):
        url = f"{self.base_url}latest.zip"
        self.load_data(url)


def main(all: bool = False):
    """main download crime data from data.police.uk and saves it as parquet file"""
    # TODO: implement incremental number of records loaded for monitoring
    # record_counts = {}
    crimeData = CrimeData()
    if not all:
        crimeData.load_latest_data()
    else:
        crimeData.load_all_history()


if __name__ == "__main__":
    fire.Fire(main)
