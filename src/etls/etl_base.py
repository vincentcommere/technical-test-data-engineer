import requests
import pandas as pd
from typing import Optional
from src.etls.utils import logger
# from utils import logger


class BaseETL:
    """
    BaseETL class to perform basic ETL operations such as extracting data from a specified endpoint
    and performing health checks on both the endpoint and SQL database connections.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        endpoint: Optional[str] = None,
        load_path: Optional[str] = None

    ) -> None:
        """
        Initializes the BaseETL with host, port, and endpoint.

        Args:
            host (Optional[str]): The host URL for the ETL process.
            port (Optional[int]): The port to connect to.
            endpoint (Optional[str]): The specific endpoint path.

        Raises:
            ValueError: If host, port, or endpoint is not provided.
        """
        if host is None or port is None or endpoint is None:
            raise ValueError("host, port, and endpoint must all be provided.")

        self.host = host
        self.port = port
        self.endpoint = endpoint
        self.load_path = load_path
        
        self.url = f"{self.host}:{self.port}{self.endpoint}"
        self.logger = logger

    def __call__(self) -> None:
        """
        Executes the ETL process by performing health checks, extracting data,
        transforming it, and then loading the transformed data.
        """
        self.health_check()
        df = self.extract()
        transformed_df = self.transform(df)
        self.load(transformed_df, )

    def _extract_health_check(self) -> bool:
        """
        Performs a health check on the endpoint to determine if it is reachable.

        Returns:
            bool: True if the endpoint is reachable, False otherwise.
        """
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                logger.info("Health check successful: Endpoint is reachable.")
                return True
            else:
                logger.warning(
                    f"Health check failed: Received status code {response.status_code}"
                )
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Health check error: {e}")
            return False

    def _load_health_check(self) -> bool:
        """
        Placeholder for checking SQL database connectivity.

        Returns:
            bool: True if the SQL database is reachable, False otherwise.
        """
        return True
    
    def _check_schema(self, df) -> pd.DataFrame:
        """
        Placeholder for checking Data Source Schema Stability.
        """
        return df

    def _check_nan(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Placeholder for checking Data Source Quality.
        """
        return df

    def health_check(self) -> bool:
        """
        Performs health checks for both the endpoint and the SQL database.

        Returns:
            bool: True if both health checks are successful, False otherwise.
        """
        try:
            endpoint_check = self._extract_health_check()
            database_check = self._load_health_check()
            return endpoint_check and database_check
        except Exception as e:
            logger.warning(f"Health check aborted due to an error: {e}")
            return False

    def extract(self) -> pd.DataFrame:
        """
        Extracts data from the specified endpoint and returns it as a DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the extracted data. Returns an empty DataFrame if extraction fails.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)
            logger.info("Data extraction successful")
            
            df = self._check_schema(df)
            df = self._check_nan(df)
            
            logger.info("Data source Stability Check successful")

            return df

        except requests.exceptions.RequestException as e:
            logger.error(f"Error during extraction: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error

    def load(self, df: pd.DataFrame) -> None:
        """
        Loads the transformed data to its final destination by saving it to a CSV file.
        This method also checks for an empty DataFrame and for duplicates before saving.

        Args:
            df (pd.DataFrame): The transformed DataFrame to be loaded.
            file_path (str): The path to save the CSV file. Defaults to "./output.csv".

        Raises:
            ValueError: If the DataFrame is empty or contains duplicate rows.
        """
        # Check if the DataFrame is empty
        if df.empty:
            self.logger.warning("DataFrame is empty. No data to load.")
            raise ValueError("Cannot load an empty DataFrame.")
        
        # Check for duplicate rows
        if df.duplicated().any():
            self.logger.warning("DataFrame contains duplicate rows.")
            raise ValueError("Cannot load DataFrame with duplicate rows.")
        
        # Save to CSV
        df.to_csv(self.load_path, index=False)
        self.logger.info(f"Data successfully saved to {self.load_path}")
