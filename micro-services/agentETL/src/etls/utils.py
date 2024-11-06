import logging
import os

# Specify the log directory and file
log_directory = "logs"
log_file = "etl_logs.txt"

os.makedirs(log_directory, exist_ok=True)  # Create the folder if it doesn't exist
log_path = os.path.join(log_directory, log_file)

# Configure logging to write to a specific file in the designated folder
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_path),  # Log messages will be saved to this file
        logging.StreamHandler(),  # Optional: also log to console
    ],
)

logger = logging.getLogger("BaseLogger")
