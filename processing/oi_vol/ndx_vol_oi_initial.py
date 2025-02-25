import pandas as pd
from datetime import datetime
from pathlib import Path
from filelock import FileLock
from loguru import logger

# ---------------------------- Configuration ---------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
INPUT_FILE = PROJECT_ROOT / "outputs" / "step_one" / "NDX_Option_Chain.xlsx"
OUTPUT_FILE_ZERO = PROJECT_ROOT / "outputs" / "vol_oi" / "NDX" / "vol_oi_zero.csv"
OUTPUT_FILE_FULL = PROJECT_ROOT / "outputs" / "vol_oi" / "NDX" / "vol_oi_full.csv"

# Configure logger
LOG_DIR = PROJECT_ROOT / "logs" / "vol_oi"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "ndx_vol_oi_initial.log",
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


def ensure_output_directories(*output_files):
    """Ensure the output directories exist."""
    try:
        for file_path in output_files:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info("Output directories verified/created.")
    except Exception as e:
        logger.error(f"Error ensuring output directories: {e}")
        raise


def process_full_data(data, timestamp, spot_price):
    """Process the full dataset for all expiration dates, including spot price."""
    try:
        data['call vol'] = data.apply(lambda row: row['totalVolume'] if row['putCall'] == 'CALL' else 0, axis=1)
        data['call oi'] = data.apply(lambda row: row['openInterest'] if row['putCall'] == 'CALL' else 0, axis=1)
        data['put vol'] = data.apply(lambda row: row['totalVolume'] if row['putCall'] == 'PUT' else 0, axis=1)
        data['put oi'] = data.apply(lambda row: row['openInterest'] if row['putCall'] == 'PUT' else 0, axis=1)

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

        logger.info("Processed and sorted full data successfully.")
        return grouped_data
    except Exception as e:
        logger.error(f"Error processing full data: {e}")
        raise


def process_zero_dte_data(data, timestamp, spot_price):
    """Process the dataset for 0DTE options only, including spot price."""
    try:
        today_date = datetime.today().strftime('%Y-%m-%d')
        zero_dte_data = data[data['expirationDate'] == today_date]

        grouped_data = zero_dte_data.groupby(['strikePrice', 'expirationDate']).agg({
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

        logger.info("Processed and sorted zero DTE data successfully.")
        return grouped_data
    except Exception as e:
        logger.error(f"Error processing zero DTE data: {e}")
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
    """Main function to process vol/oi data for full and 0DTE outputs."""
    try:
        logger.info("Starting vol/oi data processing...")

        # Load input data
        data = load_data(INPUT_FILE)

        # Get current timestamp
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Extract spot price and filter data
        spot_price = extract_spot_price(INPUT_FILE)
        data = filter_data_by_strike_range(data, spot_price, range_width=500)

        # Ensure output directories exist
        ensure_output_directories(OUTPUT_FILE_ZERO, OUTPUT_FILE_FULL)

        # Process full data, retaining expiration date and adding spot price
        full_data = process_full_data(data, current_timestamp, spot_price)
        save_data_to_csv(full_data, OUTPUT_FILE_FULL)

        # Process zero DTE data, retaining expiration date and adding spot price
        zero_dte_data = process_zero_dte_data(data, current_timestamp, spot_price)
        save_data_to_csv(zero_dte_data, OUTPUT_FILE_ZERO)

        logger.info(f"Files saved successfully:\nZero DTE: {OUTPUT_FILE_ZERO}\nFull: {OUTPUT_FILE_FULL}")

    except Exception as e:
        logger.critical(f"Critical error in processing vol/oi data: {e}")

# ---------------------------- Main Execution ---------------------------- #

if __name__ == "__main__":
    process_vol_oi_data()
