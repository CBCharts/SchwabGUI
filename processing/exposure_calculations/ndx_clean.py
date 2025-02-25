import pandas as pd
import json
from pathlib import Path
from loguru import logger

# ---------------------------- Configuration ---------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Configure logger
LOG_DIR = PROJECT_ROOT / "logs" / "data_cleaning"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "ndx_data_cleaning.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# Directories for NDX data cleaning
INPUT_DIR = PROJECT_ROOT / "outputs" / "step_two" / "NDX"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "step_two" / "NDX"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------- Load JSON Configurations ---------------------------- #

# Load IV method configuration
IV_METHOD_CONFIG_PATH = PROJECT_ROOT / "configs" / "settings" / "iv_method_config.json"
try:
    with open(IV_METHOD_CONFIG_PATH, "r") as f:
        iv_method_config = json.load(f)
    # Expected values: "All", "Hybrid_one", "Brent Black Scholes", or "Grok"
    selected_iv_method = iv_method_config.get("value", "All")
    logger.info(f"Selected IV method: {selected_iv_method}")
except Exception as e:
    logger.warning(f"Could not load IV method config; defaulting to 'All'. Error: {e}")
    selected_iv_method = "All"

iv_method_mapping = {
    "Brent Black Scholes": "brent_bs",
    "Grok": "grok",
    "Hybrid_one": "hybrid_one"
}

# Load kClean configuration
KCLEAN_CONFIG_PATH = PROJECT_ROOT / "configs" / "settings" / "kClean_config.json"
try:
    with open(KCLEAN_CONFIG_PATH, "r") as f:
        kclean_config = json.load(f)
    # Expected values: "Yes" or "No"
    process_clean_data = kclean_config.get("value", "Yes")
    logger.info(f"User clean data selection: {process_clean_data}")
except Exception as e:
    logger.warning(f"Could not load kClean config; defaulting to 'Yes'. Error: {e}")
    process_clean_data = "Yes"

# Load Expiration configuration
EXPIRATION_CONFIG_PATH = PROJECT_ROOT / "configs" / "settings" / "expiration_config.json"
try:
    with open(EXPIRATION_CONFIG_PATH, "r") as cf:
        exp_config = json.load(cf)
    expiration_option = exp_config.get("value", "EoM")
    # For NDX, only "0DTE", "1DTE", and "EoW" are valid. If expiration_option is "EoM" or any invalid value, default to "All".
    if expiration_option not in ["0DTE", "1DTE", "EoW", "All"]:
        logger.info(f"Expiration option '{expiration_option}' not valid for NDX; defaulting to 'All'.")
        expiration_option = "All"
    logger.info(f"Expiration configuration set to: {expiration_option}")
except Exception as e:
    logger.error(f"Error loading expiration configuration: {e}. Defaulting to 'All'.")
    expiration_option = "All"

# ---------------------------- Utility Functions ---------------------------- #

def validate_columns(df, required_columns):
    """Check if required columns are present in the DataFrame."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

def filter_matching_strikes(df):
    """
    Retains only rows where each strikePrice has both a CALL and a PUT entry.
    """
    try:
        grouped = df.groupby("strikePrice")["putCall"].nunique()
        valid_strikes = grouped[grouped == 2].index
        filtered_df = df[df["strikePrice"].isin(valid_strikes)]
        logger.info(f"Filtered {len(df) - len(filtered_df)} rows. Retaining {len(filtered_df)} valid entries.")
        return filtered_df
    except Exception as e:
        logger.error(f"Error filtering strike prices: {e}")
        return df

def process_file(file_path):
    """Process a single CSV file and create a cleaned version."""
    try:
        logger.info(f"Processing file: {file_path}")
        df = pd.read_csv(file_path)
        required_columns = ["strikePrice", "putCall"]
        validate_columns(df, required_columns)
        cleaned_df = filter_matching_strikes(df)
        # Create a cleaned filename by replacing "_results" with "_clean"
        output_file_name = file_path.stem.replace("_results", "_clean") + ".csv"
        output_path = OUTPUT_DIR / output_file_name
        cleaned_df.to_csv(output_path, index=False)
        logger.info(f"Cleaned data saved to: {output_path}")
    except ValueError as ve:
        logger.warning(f"Validation error in {file_path}: {ve}")
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")

# ---------------------------- Main Processing ---------------------------- #

def clean_all_csv_files():
    """Main function to process all CSV files and clean the data for NDX."""
    try:
        if process_clean_data != "Yes":
            logger.info("Data cleaning is disabled in kClean config. Skipping cleaning process.")
            return

        logger.info("Starting NDX data cleaning process.")

        # Get all CSV files ending with '_results.csv' from the NDX input folder
        csv_files = list(INPUT_DIR.glob("*_results.csv"))
        logger.info(f"Found {len(csv_files)} CSV files in {INPUT_DIR}")

        # Filter based on IV method if not "All"
        if selected_iv_method != "All":
            identifier = iv_method_mapping.get(selected_iv_method)
            if identifier:
                original_count = len(csv_files)
                csv_files = [f for f in csv_files if identifier in f.name.lower()]
                logger.info(f"Filtered CSV files: {len(csv_files)} of {original_count} match IV method '{selected_iv_method}'.")
            else:
                logger.warning(f"No identifier mapping found for IV method '{selected_iv_method}'. Processing all files.")

        # Filter based on kClean selection: if kClean is "No", skip files ending in '_clean.csv'
        if process_clean_data == "No":
            original_count = len(csv_files)
            csv_files = [f for f in csv_files if not f.name.lower().endswith('_clean.csv')]
            logger.info(f"Filtered CSV files: {len(csv_files)} of {original_count} remain after skipping '_clean.csv' files (kClean set to 'No').")

        # Filter based on expiration configuration (if not "All")
        if expiration_option != "All":
            original_count = len(csv_files)
            csv_files = [f for f in csv_files if f.name.lower().startswith(expiration_option.lower())]
            logger.info(f"Filtered CSV files: {len(csv_files)} of {original_count} match expiration option '{expiration_option}'.")
        else:
            logger.info("Expiration option 'All' selected; processing all CSV files regardless of expiration indicator.")

        if not csv_files:
            logger.warning("No valid CSV files found in the input directory after filtering.")
            return

        for file_path in csv_files:
            process_file(file_path)

        logger.info("NDX data cleaning process completed successfully.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    clean_all_csv_files()
