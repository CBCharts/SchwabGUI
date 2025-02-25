import pandas as pd
from datetime import datetime, timedelta, date
import json
import calendar
from pathlib import Path
from filelock import FileLock
from loguru import logger

# ---------------------------- Configuration ---------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
INPUT_FILE = PROJECT_ROOT / "outputs" / "step_one" / "SPX_Option_Chain.xlsx"
CONFIG_FILE = PROJECT_ROOT / "configs" / "settings" / "expiration_config.json"

# Define output files
OUTPUT_FILE_0DTE = PROJECT_ROOT / "outputs" / "vol_oi" / "0DTE_vol_oi.csv" 
OUTPUT_FILE_1DTE = PROJECT_ROOT / "outputs" / "vol_oi" / "1DTE_vol_oi.csv"
OUTPUT_FILE_EoW  = PROJECT_ROOT / "outputs" / "vol_oi" / "EoW_vol_oi.csv" 
OUTPUT_FILE_EoM  = PROJECT_ROOT / "outputs" / "vol_oi" / "EoM_vol_oi.csv"

# Configure logger
LOG_DIR = PROJECT_ROOT / "logs" / "vol_oi"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "vol_oi_initial.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# ---------------------------- Utility Functions ---------------------------- #

def load_data(file_path):
    """Load the input Excel file."""
    try:
        data = pd.read_excel(file_path)
        logger.info(f"Successfully loaded data from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        raise

def load_expiration_config(config_file):
    """Load expiration configuration from JSON file."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        # Expecting a JSON such as: {"expiration": "All"} or {"expiration": "0DTE"}
        expiration = config.get("expiration", "All")
        logger.info(f"Expiration config loaded: {expiration}")
        return expiration
    except Exception as e:
        logger.error(f"Error loading expiration config from {config_file}: {e}")
        raise

def extract_spot_price(file_path):
    """Extract the spot price from cell O2."""
    try:
        spot_price = pd.read_excel(file_path, header=None).iloc[1, 14]
        logger.info(f"Spot price extracted: {spot_price}")
        return spot_price
    except Exception as e:
        logger.error(f"Error extracting spot price from {file_path}: {e}")
        raise

def filter_data_by_strike_range(data, spot_price, range_width=500):
    """Filter data to include strikes within the specified range of the spot price."""
    try:
        strike_min = spot_price - range_width
        strike_max = spot_price + range_width
        filtered_data = data[(data['strikePrice'] >= strike_min) & (data['strikePrice'] <= strike_max)]
        logger.info(f"Filtered data to {len(filtered_data)} rows within ±{range_width} range.")
        return filtered_data
    except Exception as e:
        logger.error(f"Error filtering data by strike range: {e}")
        raise

def compute_vol_oi_columns(data):
    """Compute volume and open interest columns for calls and puts."""
    try:
        data['call vol'] = data.apply(lambda row: row['totalVolume'] if row['putCall'] == 'CALL' else 0, axis=1)
        data['call oi'] = data.apply(lambda row: row['openInterest'] if row['putCall'] == 'CALL' else 0, axis=1)
        data['put vol'] = data.apply(lambda row: row['totalVolume'] if row['putCall'] == 'PUT' else 0, axis=1)
        data['put oi'] = data.apply(lambda row: row['openInterest'] if row['putCall'] == 'PUT' else 0, axis=1)
        logger.info("Computed volume and open interest columns.")
        return data
    except Exception as e:
        logger.error(f"Error computing vol/oi columns: {e}")
        raise

def filter_by_date_range(data, start_date, end_date):
    """Filter data by expiration date range (inclusive)."""
    try:
        # Convert expirationDate to a date (if not already)
        data['expirationDate'] = pd.to_datetime(data['expirationDate']).dt.date
        filtered = data[(data['expirationDate'] >= start_date) & (data['expirationDate'] <= end_date)]
        logger.info(f"Filtered data to {len(filtered)} rows between {start_date} and {end_date}.")
        return filtered
    except Exception as e:
        logger.error(f"Error filtering data by date range: {e}")
        raise

def process_bucket_data(data, timestamp, spot_price):
    """Group and aggregate data for a given expiration bucket."""
    try:
        grouped_data = data.groupby(['strikePrice', 'expirationDate']).agg({
            'call vol': 'sum',
            'call oi': 'sum',
            'put vol': 'sum',
            'put oi': 'sum'
        }).reset_index()

        grouped_data['timestamp'] = timestamp
        grouped_data['spotPrice'] = spot_price
        grouped_data.rename(columns={'strikePrice': 'strike'}, inplace=True)

        # Sort data by expirationDate and strike
        grouped_data = grouped_data.sort_values(by=['expirationDate', 'strike'])
        logger.info("Processed and sorted bucket data successfully.")
        return grouped_data
    except Exception as e:
        logger.error(f"Error processing bucket data: {e}")
        raise

def ensure_output_directories(*output_files):
    """Ensure the output directories exist."""
    try:
        for file_path in output_files:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info("Output directories verified/created.")
    except Exception as e:
        logger.error(f"Error ensuring output directories: {e}")
        raise

def save_data_to_csv(data, file_path):
    """Save the processed data to a CSV file with file locking."""
    try:
        lock = FileLock(f"{file_path}.lock")
        with lock:
            data.to_csv(file_path, index=False)
            logger.info(f"Saved data to {file_path}")
    except Exception as e:
        logger.error(f"Error saving data to {file_path}: {e}")
        raise

# ---------------------------- Main Processing ---------------------------- #

def process_vol_oi_data():
    """Main function to process vol/oi data for various expiration buckets."""
    try:
        logger.info("Starting vol/oi data processing...")

        # Load expiration config
        expiration_config = load_expiration_config(CONFIG_FILE)
        if expiration_config == "All":
            buckets_to_process = ["0DTE", "1DTE", "EoW", "EoM"]
        else:
            buckets_to_process = [expiration_config]

        # Load input data and extract the spot price
        data = load_data(INPUT_FILE)
        spot_price = extract_spot_price(INPUT_FILE)

        # Filter data by strike range
        data = filter_data_by_strike_range(data, spot_price, range_width=500)

        # Compute vol/oi columns once for the entire dataset
        data = compute_vol_oi_columns(data)

        # Ensure output directories exist
        ensure_output_directories(OUTPUT_FILE_0DTE, OUTPUT_FILE_1DTE, OUTPUT_FILE_EoW, OUTPUT_FILE_EoM)

        # Define date boundaries
        today_date = datetime.today().date()
        tomorrow_date = today_date + timedelta(days=1)
        end_of_week = today_date + timedelta(days=(6 - today_date.weekday()))
        last_day = calendar.monthrange(today_date.year, today_date.month)[1]
        end_of_month = date(today_date.year, today_date.month, last_day)

        # Get current timestamp for metadata
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Process each bucket according to the expiration config
        if "0DTE" in buckets_to_process:
            bucket_data = filter_by_date_range(data, today_date, today_date)
            processed_data = process_bucket_data(bucket_data, current_timestamp, spot_price)
            save_data_to_csv(processed_data, OUTPUT_FILE_0DTE)

        if "1DTE" in buckets_to_process:
            bucket_data = filter_by_date_range(data, today_date, tomorrow_date)
            processed_data = process_bucket_data(bucket_data, current_timestamp, spot_price)
            save_data_to_csv(processed_data, OUTPUT_FILE_1DTE)

        if "EoW" in buckets_to_process:
            bucket_data = filter_by_date_range(data, today_date, end_of_week)
            processed_data = process_bucket_data(bucket_data, current_timestamp, spot_price)
            save_data_to_csv(processed_data, OUTPUT_FILE_EoW)

        if "EoM" in buckets_to_process:
            bucket_data = filter_by_date_range(data, today_date, end_of_month)
            processed_data = process_bucket_data(bucket_data, current_timestamp, spot_price)
            save_data_to_csv(processed_data, OUTPUT_FILE_EoM)

        logger.info("Files saved successfully for buckets: " + ", ".join(buckets_to_process))
    except Exception as e:
        logger.critical(f"Critical error in processing vol/oi data: {e}")

# ---------------------------- Main Execution ---------------------------- #

if __name__ == "__main__":
    process_vol_oi_data()
