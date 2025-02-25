import pandas as pd
import json
from pathlib import Path
from loguru import logger
from datetime import datetime

# ---------------------------- Configuration ---------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Configure logger
LOG_DIR = PROJECT_ROOT / "logs" / "ranking"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "ranking.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# Define the 6 target directories for input CSV files
target_dirs = [
    PROJECT_ROOT / "outputs" / "step_two" / "grok",
    PROJECT_ROOT / "outputs" / "step_two" / "hybrid_one",
    PROJECT_ROOT / "outputs" / "step_two" / "brent_bs",
]

# Centralized output directory for ranked results
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "step_three"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SPX_SPOT_DIFF_FILE = PROJECT_ROOT / "outputs" / "step_one" / "spot_price_differences.xlsx"

# ---------------------------- Load IV Method Configuration ---------------------------- #

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

# Mapping from IV method to an identifier substring in the filenames
iv_method_mapping = {
    "Brent Black Scholes": "brent_bs",
    "Grok": "grok",
    "Hybrid_one": "hybrid_one"
}

# ---------------------------- Load kClean Configuration ---------------------------- #

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

def validate_columns(df, required_columns):
    """Check if required columns are present in the DataFrame."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

def extract_es_multiplier():
    """
    Extracts the SPX-ES % Diff multiplier from spot_price_differences.xlsx.
    Aborts execution if the value cannot be retrieved.
    """
    try:
        df = pd.read_excel(SPX_SPOT_DIFF_FILE, sheet_name=0)
        # Debug: Print first few rows to verify structure
        print("Extracted DataFrame from Excel:")
        print(df.head(10))
        required_columns = ["Symbol", "Spot Price"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Expected columns not found. Verify Excel format.")
        row = df[df["Symbol"] == "SPX-ES % Diff"]
        if row.empty:
            raise ValueError("SPX-ES % Diff row not found in Excel.")
        es_value = row["Spot Price"].values[0]
        if pd.isna(es_value):
            raise ValueError("Extracted ES multiplier is NaN or empty.")
        es_multiplier = es_value / 100.0
        logger.info(f"Extracted ES Multiplier from Excel: {es_multiplier}")
        print(f"Extracted ES Multiplier: {es_multiplier}")
        return es_multiplier
    except Exception as e:
        logger.critical(f"Failed to extract ES multiplier from {SPX_SPOT_DIFF_FILE}: {e}")
        raise SystemExit("Aborting script due to missing ES multiplier.")

def calculate_theo_es(strike_price, multiplier):
    """Calculate the theoretical ES price for a given strike price and multiplier."""
    try:
        theo_price = strike_price + (strike_price * multiplier)
        return round(theo_price * 4) / 4  # Round to nearest 0.25
    except Exception as e:
        logger.error(f"Error calculating Theo ES for strike price {strike_price}: {e}")
        return None

def rank_exposures(df, exposure_column, top_n=5):
    """Rank exposures (DEX, GEX, VEX, CEX) and return top and lowest rankings."""
    try:
        es_multiplier = extract_es_multiplier()  # Get dynamic multiplier
        aggregated = (
            df.groupby("strikePrice")[exposure_column]
            .sum()
            .reset_index()
            .sort_values(by=exposure_column, ascending=False)
        )
        aggregated["Theo ES"] = aggregated["strikePrice"].apply(lambda x: calculate_theo_es(x, es_multiplier))
        top_levels = aggregated.head(top_n).copy()
        bottom_levels = aggregated.tail(top_n).copy()
        top_levels["Rank"] = [f"Call {exposure_column} {i + 1}" for i in range(len(top_levels))]
        bottom_levels["Rank"] = [f"Put {exposure_column} {top_n - i}" for i in range(len(bottom_levels))]
        top_levels["Greek"] = exposure_column
        bottom_levels["Greek"] = exposure_column
        top_levels["Value"] = top_levels[exposure_column]
        bottom_levels["Value"] = bottom_levels[exposure_column]
        ranked_levels = pd.concat([top_levels, bottom_levels], axis=0).reset_index(drop=True)
        logger.info(f"Top {top_n} and lowest {top_n} rankings for {exposure_column} identified.")
        return ranked_levels
    except Exception as e:
        logger.error(f"Failed to rank exposures for {exposure_column}: {e}")
        return pd.DataFrame()

def process_file(file_path):
    """Process a single CSV file to rank exposures and save outputs."""
    try:
        logger.info(f"Processing file: {file_path}")
        df = pd.read_csv(file_path)
        required_columns = ["strikePrice", "DEX", "GEX", "VEX", "CEX", "putCall"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns in {file_path}")
        for col in ["DEX", "GEX", "VEX", "CEX", "strikePrice"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        ranked_data = []
        for greek in ["DEX", "GEX", "VEX", "CEX"]:
            ranked = rank_exposures(df, greek)
            ranked_data.append(ranked)
        final_df = pd.concat(ranked_data, ignore_index=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        final_df["timestamp"] = timestamp
        final_df = final_df[["timestamp", "strikePrice", "Theo ES", "Rank", "Greek", "Value"]]
        numerical_columns = ["strikePrice", "Theo ES", "Value"]
        final_df[numerical_columns] = final_df[numerical_columns].round(3)
        output_file_name = file_path.stem + "_ranked.csv"
        output_path = OUTPUT_DIR / output_file_name
        final_df.to_csv(output_path, index=False)
        logger.info(f"Ranked results saved to: {output_path}")
    except ValueError as ve:
        logger.warning(f"Validation error in {file_path}: {ve}")
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")

# ---------------------------- Main Processing ---------------------------- #

def rank_all_exposures():
    """Main function to process all CSV files from target directories for ranking exposures."""
    try:
        logger.info("Starting exposure ranking process.")
        all_csv_files = []
        for directory in target_dirs:
            files = list(directory.glob("*.csv"))
            logger.info(f"Found {len(files)} CSV files in {directory}")
            all_csv_files.extend(files)

        if process_clean_data != "Yes":
            original_count = len(all_csv_files)
            all_csv_files = [f for f in all_csv_files if "clean" not in f.stem.lower()]
            logger.info(f"{len(all_csv_files)} CSV files remain after skipping files with 'clean' in the name (kClean set to 'No').")
        else:
            logger.info("kClean is set to 'Yes'; processing all files, including those with 'clean' in the name.")

        if selected_iv_method != "All":
            identifier = iv_method_mapping.get(selected_iv_method)
            if identifier:
                original_count = len(all_csv_files)
                all_csv_files = [f for f in all_csv_files if identifier in f.stem.lower()]
                logger.info(f"Filtered CSV files: {len(all_csv_files)} of {original_count} match IV method '{selected_iv_method}'.")
            else:
                logger.warning(f"No identifier mapping found for IV method '{selected_iv_method}'. Processing all files.")

        # Filter based on expiration configuration only if not "All"
        if expiration_option != "All":
            original_count = len(all_csv_files)
            all_csv_files = [f for f in all_csv_files if f.stem.lower().startswith(expiration_option.lower())]
            logger.info(f"Filtered CSV files: {len(all_csv_files)} of {original_count} match expiration option '{expiration_option}'.")
        else:
            logger.info("Expiration option 'All' selected; processing all CSV files regardless of expiration indicator.")

        if not all_csv_files:
            logger.warning("No CSV files found to process after filtering.")
            return

        # Optionally sort files; here we use a sort key that prioritizes files containing '_results' in their stem
        all_csv_files.sort(key=lambda f: ("_results" in f.stem, f.stem))
        for file_path in all_csv_files:
            logger.info(f"Processing file: {file_path}")
            process_file(file_path)
        logger.info("Exposure ranking process completed successfully.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# ---------------------------- Entry Point ---------------------------- #

if __name__ == "__main__":
    rank_all_exposures()
