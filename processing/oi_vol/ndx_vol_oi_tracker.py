import pandas as pd
import os
from datetime import datetime, timedelta
from pathlib import Path
from filelock import FileLock
from loguru import logger

# ---------------------------- Configuration ---------------------------- #

# Define file paths (adjust as needed for your environment)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
INPUT_FILE = PROJECT_ROOT / "outputs" / "vol_oi" / "NDX" / "vol_oi_zero.csv"
CUMULATIVE_FILE = PROJECT_ROOT / "outputs" / "vol_oi" / "NDX" / "cumulative_vol_oi.csv"
OUTPUT_1_MIN = PROJECT_ROOT / "outputs" / "vol_oi" / "NDX" / "tracker" / "vol_oi_1_min.csv"
OUTPUT_15_MIN = PROJECT_ROOT / "outputs" / "vol_oi" / "NDX" / "tracker" / "vol_oi_15_min.csv"
OUTPUT_30_MIN = PROJECT_ROOT / "outputs" / "vol_oi" / "NDX" / "tracker" / "vol_oi_30_min.csv"
OUTPUT_60_MIN = PROJECT_ROOT / "outputs" / "vol_oi" / "NDX" / "tracker" / "vol_oi_60_min.csv"

# Configure logger
LOG_DIR = PROJECT_ROOT / "logs" / "vol_oi"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "ndx_vol_oi_tracker.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# ---------------------------- Utility Functions ---------------------------- #

def clear_old_data(cumulative_file):
    """Clear cumulative data if it's from a previous trading day."""
    try:
        if cumulative_file.exists():
            df = pd.read_csv(cumulative_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            last_date = df['timestamp'].max().date()
            today = datetime.now().date()

            if last_date < today:
                logger.info("Previous day's data detected. Resetting cumulative file.")
                cumulative_file.unlink()  # Delete the file
                return pd.DataFrame()  # Return an empty DataFrame for new data
            else:
                logger.info("Loaded existing cumulative data.")
                return df
        else:
            logger.info("No previous cumulative data found. Starting fresh.")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error clearing old data: {e}")
        raise

def load_new_data(file_path):
    """Load the latest snapshot of vol/oi data with file locking."""
    try:
        lock = FileLock(str(file_path) + ".lock")
        with lock:
            new_data = pd.read_csv(file_path)
        new_data['timestamp'] = pd.to_datetime(new_data['timestamp'])
        logger.info(f"Successfully loaded new data from {file_path}")
        return new_data
    except Exception as e:
        logger.error(f"Error loading new data from {file_path}: {e}")
        raise
    
def calculate_changes(cumulative_data, new_data):
    """Calculate changes in volume and add change columns."""
    try:
        merged_data = pd.merge(new_data, cumulative_data, on='strike', how='left', suffixes=('', '_prev'))
        merged_data['call_vol_chng'] = merged_data['call vol'] - merged_data['call vol_prev'].fillna(0)
        merged_data['put_vol_chng'] = merged_data['put vol'] - merged_data['put vol_prev'].fillna(0)

        # Calculate vol/oi ratios and explicitly convert to numeric
        merged_data['call_vol/oi'] = pd.to_numeric(merged_data['call vol'] / merged_data['call oi'].replace(0, pd.NA), errors='coerce')
        merged_data['put_vol/oi'] = pd.to_numeric(merged_data['put vol'] / merged_data['put oi'].replace(0, pd.NA), errors='coerce')

        logger.info("Successfully calculated changes in volume and open interest.")
        columns_to_keep = ['strike', 'call vol', 'call oi', 'put vol', 'put oi', 'timestamp',
                           'call_vol_chng', 'put_vol_chng', 'call_vol/oi', 'put_vol/oi']
        return merged_data[columns_to_keep]
    except Exception as e:
        logger.error(f"Error calculating volume and OI changes: {e}")
        raise

def rolling_summary(cumulative_data, minutes):
    """Generate rolling summaries for the last `minutes`."""
    try:
        time_cutoff = datetime.now() - timedelta(minutes=minutes)
        rolling_data = cumulative_data[cumulative_data['timestamp'] >= time_cutoff]

        # Find top changes
        top_call_vol = rolling_data.nlargest(5, 'call_vol_chng')
        top_put_vol = rolling_data.nlargest(5, 'put_vol_chng')
        top_vol = pd.concat([top_call_vol, top_put_vol])

        top_call_vol_oi = rolling_data.nlargest(5, 'call_vol/oi')
        top_put_vol_oi = rolling_data.nlargest(5, 'put_vol/oi')
        top_vol_oi = pd.concat([top_call_vol_oi, top_put_vol_oi])

        logger.info(f"Generated rolling summary for the past {minutes} minutes.")
        return top_vol, top_vol_oi
    except Exception as e:
        logger.error(f"Error generating rolling summary for {minutes} minutes: {e}")
        raise

def save_to_csv(df, filename):
    """Save a DataFrame to a CSV file."""
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False)
        logger.info(f"Successfully saved data to {filename}")
    except Exception as e:
        logger.error(f"Failed to save to CSV: {e}")
        raise

# ---------------------------- Main Processing ---------------------------- #

def vol_oi_processing():
    """Main processing function for tracking and summarizing vol/oi changes."""
    try:
        logger.info("Starting vol/oi tracking process.")

        # Load or reset cumulative data if it's from the previous trading day
        cumulative_data = clear_old_data(CUMULATIVE_FILE)

        # Load the latest snapshot
        new_data = load_new_data(INPUT_FILE)

        # If cumulative_data is empty, initialize it
        if cumulative_data.empty:
            logger.info("Initializing cumulative data.")
            cumulative_data = new_data.copy()
            cumulative_data['call_vol_chng'] = 0
            cumulative_data['put_vol_chng'] = 0
            cumulative_data['call_vol/oi'] = pd.to_numeric(cumulative_data['call vol'] / cumulative_data['call oi'].replace(0, pd.NA), errors='coerce')
            cumulative_data['put_vol/oi'] = pd.to_numeric(cumulative_data['put vol'] / cumulative_data['put oi'].replace(0, pd.NA), errors='coerce')
        else:
            # Calculate changes and update cumulative data
            cumulative_data = calculate_changes(cumulative_data, new_data)

        # Save the 1-minute updated data
        save_to_csv(cumulative_data, OUTPUT_1_MIN)

        # Generate rolling summaries
        for interval, output_file in zip([15, 30, 60], [OUTPUT_15_MIN, OUTPUT_30_MIN, OUTPUT_60_MIN]):
            top_vol, top_vol_oi = rolling_summary(cumulative_data, interval)
            summary_data = pd.concat([top_vol, top_vol_oi]).drop_duplicates()
            save_to_csv(summary_data, output_file)

        # Save the cumulative data for persistence
        save_to_csv(cumulative_data, CUMULATIVE_FILE)

        logger.info(f"1-minute update saved to {OUTPUT_1_MIN}")
        logger.info(f"15-minute summary saved to {OUTPUT_15_MIN}")
        logger.info(f"30-minute summary saved to {OUTPUT_30_MIN}")
        logger.info(f"60-minute summary saved to {OUTPUT_60_MIN}")

    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")

# ---------------------------- Main Execution ---------------------------- #

if __name__ == "__main__":
    vol_oi_processing()
