import pytest
from unittest.mock import patch, MagicMock
from src.etls.etl_tracks import TracksETL
import pandas as pd

ETL = TracksETL
endpoint = "/tracks"

def test_base_etl_initialization() -> None:
    """
    Test the initialization of the ETL instance.
    Ensures that the host, port, endpoint, and URL are set as expected.
    Also checks that missing parameters raise a ValueError.

    Raises:
        ValueError: If host, port, or endpoint are not provided.
    """
    # Check successful initialization
    etl = ETL(host="http://127.0.0.1", port=8000, endpoint=endpoint)
    assert etl.host == "http://127.0.0.1"
    assert etl.port == 8000
    assert etl.endpoint == endpoint
    assert etl.url == "http://127.0.0.1:8000/tracks"

    # Check ValueError for missing parameters
    with pytest.raises(ValueError):
        ETL(host=None, port=8000, endpoint=endpoint)


@patch("requests.get")
def test_extract_non_empty(mock_get: MagicMock) -> None:
    """
    Test the `extract` method to ensure it returns a non-empty DataFrame
    when the endpoint provides valid JSON data.

    Args:
        mock_get (MagicMock): A mock of the requests.get method to simulate
                              HTTP responses with predefined JSON data.
    """
    # Mock a successful response with JSON data
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: [
            {"id": "value1", "items": "value2"},
            {"id": "value3", "items": "value4"},
        ]
    )

    # Instantiate ETL
    etl = ETL(host="http://127.0.0.1", port=8000, endpoint=endpoint)

    # Run the extract method
    df: pd.DataFrame = etl.extract()
    # Assertions to check that the DataFrame is not empty
    assert not df.empty, "The extracted DataFrame should not be empty"
    assert list(df.columns) == ["id", "items"], "DataFrame should have the correct columns"
    assert len(df) == 2, "DataFrame should have 2 rows"
    assert df.iloc[0]["id"] == "value1", "First row, 'id' should match expected value"