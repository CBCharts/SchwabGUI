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
    LOG_DIR / "exposure.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# Target directories containing IV method results (CSV files)
target_dirs = [
    PROJECT_ROOT / "outputs" / "step_two" / "grok",
    PROJECT_ROOT / "outputs" / "step_two" / "hybrid_one",
    PROJECT_ROOT / "outputs" / "step_two" / "brent_bs"
]

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
    # Allow "All" as a valid option
    if expiration_option not in ["0DTE", "1DTE", "EoW", "EoM", "All"]:
        logger.warning(f"Invalid expiration option '{expiration_option}' found in config; defaulting to 'EoM'.")
        expiration_option = "EoM"
    logger.info(f"Expiration configuration set to: {expiration_option}")
except Exception as e:
    logger.error(f"Error loading expiration configuration: {e}. Defaulting to 'EoM'.")
    expiration_option = "EoM"

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
        # Adjust GEX for puts
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
    Process all CSV files in the target directories to calculate exposure columns.
    Only files matching the selected expiration option are processed.
    """
    try:
        logger.info("Starting total exposure calculations.")
        all_files = []
        for d in target_dirs:
            files = list(d.glob("*.csv"))
            logger.info(f"Found {len(files)} CSV files in {d}")
            all_files.extend(files)

        # Filter based on IV method selection if needed
        if selected_iv_method != "All":
            identifier = iv_method_mapping.get(selected_iv_method)
            if identifier:
                original_count = len(all_files)
                all_files = [f for f in all_files if identifier in f.name.lower()]
                logger.info(f"Filtered CSV files: {len(all_files)} of {original_count} match IV method '{selected_iv_method}'.")
            else:
                logger.warning(f"No identifier mapping found for IV method '{selected_iv_method}'. Processing all files.")

        # Filter based on kClean selection if applicable
        if process_clean_data == "No":
            original_count = len(all_files)
            all_files = [f for f in all_files if not f.name.lower().endswith('_clean.csv')]
            logger.info(f"Filtered CSV files: {len(all_files)} of {original_count} remain after skipping '_clean.csv' files (kClean set to 'No').")

        # Filter based on expiration configuration only if not "All"
        if expiration_option != "All":
            original_count = len(all_files)
            all_files = [f for f in all_files if f.name.lower().startswith(expiration_option.lower())]
            logger.info(f"Filtered CSV files: {len(all_files)} of {original_count} match expiration option '{expiration_option}'.")
        else:
            logger.info("Expiration option 'All' selected; processing all files regardless of expiration indicator.")

        if not all_files:
            logger.warning("No CSV files found to process after filtering.")
            return

        for file_path in all_files:
            process_file(file_path)

        logger.info("Total exposure calculations completed successfully.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    calculate_total_exposure()
