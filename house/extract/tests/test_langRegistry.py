import pytest
import pandas as pd
import logging

from house.extract.landRegistry.langRegistry import download_and_save_parquet

@pytest.mark.parametrize(
    "complete,expected_url,expected_filename,df_mock",
    [
        pytest.param(
            True,
            "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv",
            "landRegistry_complete.parquet",
            pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]}),
            id="happy_path_complete_true"
        ),
        pytest.param(
            False,
            "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update-new-version.csv",
            "landRegistry_monthly.parquet",
            pd.DataFrame({"col1": [], "col2": []}),
            id="happy_path_complete_false_empty_df"
        ),
        pytest.param(
            True,
            "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv",
            "landRegistry_complete.parquet",
            pd.DataFrame({"col1": [None, None]}),
            id="edge_case_null_values"
        ),
    ]
)
def test_download_and_save_parquet_happy_and_edge(monkeypatch, complete, expected_url, expected_filename, df_mock):
    
    # Arrange
    class DummyDF(pd.DataFrame):
        def to_parquet(self, fname, **kwargs):
            self._to_parquet_called = True
            self._to_parquet_args = (fname, kwargs)
    dummy_df = DummyDF(df_mock)
    read_csv_called = {}
    def mock_read_csv(url, encoding=None):
        read_csv_called['url'] = url
        read_csv_called['encoding'] = encoding
        return dummy_df
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)
    logs = []
    def mock_info(msg):
        logs.append(msg)
    monkeypatch.setattr(logging, "info", mock_info)

    # Act
    download_and_save_parquet(complete)

    # Assert
    assert read_csv_called['url'] == expected_url
    assert read_csv_called['encoding'] == "utf-8"
    assert hasattr(dummy_df, "_to_parquet_called") and dummy_df._to_parquet_called
    assert dummy_df._to_parquet_args[0] == expected_filename
    assert dummy_df._to_parquet_args[1] == {"index": False}
    assert logs[0] == f"Downloading: {expected_url}"
    assert logs[1] == f"Downloaded and saved to {expected_filename}"
