import pandas as pd
import numpy as np
from pathlib import Path
from loguru import logger
import json

# ---------------------------- Configuration ---------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Configure logger
LOG_DIR = PROJECT_ROOT / "logs" / "exposure_calculations"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "ndx_exposure.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# For NDX, input files are in a dedicated subfolder
INPUT_DIR = PROJECT_ROOT / "outputs" / "step_two" / "NDX"
# We'll write cleaned files back into the same NDX folder
OUTPUT_DIR = INPUT_DIR

# Exposure columns to calculate
EXPOSURE_COLUMNS = ["DEX", "GEX", "VEX", "CEX"]

# ---------------------------- Load IV Method Selection ---------------------------- #
IV_METHOD_CONFIG_PATH = PROJECT_ROOT / "configs" / "settings" / "iv_method_config.json"
try:
    with open(IV_METHOD_CONFIG_PATH, "r") as f:
        iv_method_config = json.load(f)
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

# ---------------------------- Load kClean (Clean Data) Selection ---------------------------- #
KCLEAN_CONFIG_PATH = PROJECT_ROOT / "configs" / "settings" / "kClean_config.json"
try:
    with open(KCLEAN_CONFIG_PATH, "r") as f:
        kclean_config = json.load(f)
    process_clean_data = kclean_config.get("value", "Yes")
    logger.info(f"User clean data selection: {process_clean_data}")
except Exception as e:
    logger.warning(f"Could not load kClean config; defaulting to 'Yes'. Error: {e}")
    process_clean_data = "Yes"

# ---------------------------- Load Expiration Configuration ---------------------------- #
EXPIRATION_CONFIG_PATH = PROJECT_ROOT / "configs" / "settings" / "expiration_config.json"
try:
    with open(EXPIRATION_CONFIG_PATH, "r") as cf:
        exp_config = json.load(cf)
    expiration_option = exp_config.get("value", "EoM")
    # For NDX, valid expirations are only 0DTE, 1DTE, and EoW.
    # If expiration_option is "EoM" or not one of the valid ones, default to "All"
    if expiration_option not in ["0DTE", "1DTE", "EoW", "All"]:
        logger.info(f"Expiration option '{expiration_option}' not valid for NDX; defaulting to 'All'.")
        expiration_option = "All"
    logger.info(f"Expiration configuration set to: {expiration_option}")
except Exception as e:
    logger.error(f"Error loading expiration configuration: {e}. Defaulting to 'All'.")
    expiration_option = "All"

# ---------------------------- Utility Functions ---------------------------- #

def calculate_exposures(df):
    """
    Calculate exposure columns (DEX, GEX, VEX, CEX) based on option rules.
    """
    try:
        required_columns = [
            "delta", "gamma", "vanna", "charm",
            "spotPrice", "openInterest", "putCall", "impliedVolatility"
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logger.warning(f"Missing required columns for exposure calculation: {missing_columns}. Skipping file.")
            return None

        # Calculate DEX (normalized to millions)
        df["DEX"] = df["delta"] * df["openInterest"] * df["spotPrice"]
        df["DEX"] = df["DEX"].apply(lambda x: round(x / 1_000_000, 3))

        # Calculate GEX (normalized to millions)
        df["GEX"] = df["gamma"] * df["openInterest"] * (df["spotPrice"] ** 2) * 100
        df["GEX"] = df["GEX"].apply(lambda x: round(x / 1_000_000, 3))
        df.loc[df["putCall"].str.upper() == "PUT", "GEX"] *= -1

        # Calculate VEX (normalized to millions)
        df["VEX"] = df["vanna"] * df["openInterest"] * df["spotPrice"] * df["impliedVolatility"]
        df["VEX"] = df["VEX"].apply(lambda x: round(x / 1_000_000, 3))

        # Calculate CEX (normalized to millions)
        df["CEX"] = df["charm"] * df["openInterest"] * df["spotPrice"] * 365
        df["CEX"] = df["CEX"].apply(lambda x: round(x / 1_000_000, 3))

        logger.info(f"Calculated exposures: {EXPOSURE_COLUMNS}.")
        return df
    except Exception as e:
        logger.error(f"Error calculating exposures: {e}")
        return None

def process_file(file_path):
    """
    Process a single CSV file to add exposure columns.
    Overwrites the original file with updated exposures.
    """
    try:
        logger.info(f"Processing file: {file_path}")
        df = pd.read_csv(file_path)
        df = calculate_exposures(df)
        if df is None:
            logger.warning(f"Skipping file due to exposure calculation issues: {file_path}")
            return
        df.to_csv(file_path, index=False)
        logger.info(f"Processed file saved: {file_path}")
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")

# ---------------------------- Main Execution ---------------------------- #

def calculate_total_exposure():
    """
    Main function to process all CSV files in the NDX input folder and calculate exposures.
    Filtering is applied based on IV method, kClean setting, and expiration configuration.
    """
    try:
        logger.info("Starting total exposure calculations for NDX.")
        csv_files = list(INPUT_DIR.glob("*.csv"))
        logger.info(f"Found {len(csv_files)} CSV files in {INPUT_DIR}")

        # Filter by IV method (if not "All")
        if selected_iv_method != "All":
            identifier = iv_method_mapping.get(selected_iv_method)
            if identifier:
                original_count = len(csv_files)
                csv_files = [f for f in csv_files if identifier in f.name.lower()]
                logger.info(f"Filtered CSV files: {len(csv_files)} of {original_count} match IV method '{selected_iv_method}'.")
            else:
                logger.warning(f"No identifier mapping found for IV method '{selected_iv_method}'. Processing all files.")

        # Filter by kClean: if set to "No", skip files ending with '_clean.csv'
        if process_clean_data == "No":
            original_count = len(csv_files)
            csv_files = [f for f in csv_files if not f.name.lower().endswith('_clean.csv')]
            logger.info(f"Filtered CSV files: {len(csv_files)} of {original_count} remain after skipping '_clean.csv' files (kClean set to 'No').")

        # Filter based on expiration configuration if not "All"
        if expiration_option != "All":
            original_count = len(csv_files)
            csv_files = [f for f in csv_files if f.name.lower().startswith(expiration_option.lower())]
            logger.info(f"Filtered CSV files: {len(csv_files)} of {original_count} match expiration option '{expiration_option}'.")
        else:
            logger.info("Expiration option 'All' selected; processing all CSV files regardless of expiration indicator.")

        if not csv_files:
            logger.warning("No CSV files found to process after filtering.")
            return

        for file_path in csv_files:
            process_file(file_path)

        logger.info("Total exposure calculations for NDX completed successfully.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    calculate_total_exposure()
