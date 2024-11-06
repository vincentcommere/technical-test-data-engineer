import pandas as pd

from src.etls.etl_base import BaseETL
# from etl_base import BaseETL


class TracksETL(BaseETL):
    """
    TracksETL class that extends BaseETL to perform ETL operations on track data.
    """

    def __init__(
        self,
        host: str = "http://127.0.0.1",
        port: int = 8000,
        endpoint: str = "/tracks",
        load_path = '../../data/tracks.csv'
    ) -> None:
        """
        Initializes the TracksETL instance with default or provided values.

        Args:
            host (str): The host URL for the ETL process.
            port (int): The port to connect to.
            endpoint (str): The specific endpoint path.
        """
        super().__init__(host=host, port=port, endpoint=endpoint, load_path=load_path)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the extracted data by expanding nested JSON structures.

        Args:
            df (pd.DataFrame): The DataFrame containing the extracted data.

        Returns:
            pd.DataFrame: The transformed DataFrame with expanded JSON data.
        """
        expanded_df = pd.json_normalize(df["items"])
        # Define the column mapping dictionary
        column_mapping = {"id": "track_id"}

        # Rename columns using the rename() method
        expanded_df.rename(columns=column_mapping, inplace=True)

        self.logger.info("Transformation complete")
        self.logger.debug(expanded_df.head())  # Log the first few rows to verify
        return expanded_df


if __name__ == "__main__":
    
    from datetime import datetime
    # Generate a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Create filename with timestamp
    load_path = f"/app/data/tracks-{timestamp}.csv"
    tetl = TracksETL(host='http://fastapi_service', load_path = load_path)
    tetl()
