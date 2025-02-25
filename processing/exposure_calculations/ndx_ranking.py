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
    LOG_DIR / "ndx_ranking.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# For NDX, input files are in a dedicated folder
INPUT_DIR = PROJECT_ROOT / "outputs" / "step_two" / "NDX"
# For NDX, output ranked files will be saved in a dedicated NDX folder under step_three
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "step_three" / "NDX"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# NDX spot difference file (for multiplier extraction)
NDX_SPOT_DIFF_FILE = PROJECT_ROOT / "outputs" / "step_one" / "ndx_spot_price_differences.xlsx"

# ---------------------------- Load JSON Configurations ---------------------------- #

# Load IV method configuration
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

# Load kClean configuration
KCLEAN_CONFIG_PATH = PROJECT_ROOT / "configs" / "settings" / "kClean_config.json"
try:
    with open(KCLEAN_CONFIG_PATH, "r") as f:
        kclean_config = json.load(f)
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
    # For NDX, only 0DTE, 1DTE, and EoW are valid. If config is "EoM" or an invalid value, default to "All".
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

def extract_nq_multiplier():
    """
    Extracts the NDX-NQ % Diff multiplier from ndx_spot_price_differences.xlsx.
    Converts the Excel value to a decimal fraction.
    """
    try:
        df = pd.read_excel(NDX_SPOT_DIFF_FILE, sheet_name=0)
        required_columns = ["Symbol", "Spot Price"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Expected columns not found in Excel.")
        row = df[df["Symbol"] == "NDX-NQ % Diff"]
        if row.empty:
            raise ValueError("NDX-NQ % Diff row not found in Excel.")
        nq_value = row["Spot Price"].values[0]
        if pd.isna(nq_value):
            raise ValueError("Extracted NQ multiplier is NaN or empty.")
        nq_multiplier = nq_value / 100.0
        logger.info(f"Extracted NQ Multiplier from Excel: {nq_multiplier}")
        return nq_multiplier
    except Exception as e:
        logger.critical(f"Failed to extract NQ multiplier: {e}")
        raise SystemExit("Aborting due to missing NQ multiplier.")

def calculate_theo_nq(strike_price, multiplier):
    """Calculate the theoretical NQ price for a given strike price and multiplier."""
    try:
        theo_price = strike_price + (strike_price * multiplier)
        return round(theo_price * 4) / 4
    except Exception as e:
        logger.error(f"Error calculating Theo NQ for strike price {strike_price}: {e}")
        return None

def rank_exposures(df, exposure_column, top_n=5):
    """Rank exposures (DEX, GEX, VEX, CEX) and return top and lowest rankings."""
    try:
        nq_multiplier = extract_nq_multiplier()
        aggregated = (
            df.groupby("strikePrice")[exposure_column]
            .sum()
            .reset_index()
            .sort_values(by=exposure_column, ascending=False)
        )
        aggregated["Theo NQ"] = aggregated["strikePrice"].apply(lambda x: calculate_theo_nq(x, nq_multiplier))
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
        for col in ["DEX", "GEX", "VEX", "CEX" "strikePrice"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        ranked_data = []
        for greek in ["DEX", "GEX", "VEX", "CEX"]:
            ranked = rank_exposures(df, greek)
            ranked_data.append(ranked)
        final_df = pd.concat(ranked_data, ignore_index=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        final_df["timestamp"] = timestamp
        final_df = final_df[["timestamp", "strikePrice", "Theo NQ", "Rank", "Greek", "Value"]]
        numerical_columns = ["strikePrice", "Theo NQ", "Value"]
        final_df[numerical_columns] = final_df[numerical_columns].round(3)
        output_file_name = file_path.stem + "_ranked.csv"
        output_path = OUTPUT_DIR / output_file_name
        final_df.to_csv(output_path, index=False)
        logger.info(f"Ranked results saved to: {output_path}")
    except ValueError as ve:
        logger.warning(f"Validation error in {file_path}: {ve}")
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")

def rank_all_exposures():
    """Main function to process all CSV files in the NDX input directory for ranking exposures."""
    try:
        logger.info("Starting NDX exposure ranking process.")

        # Gather all CSV files from the NDX input folder
        csv_files = list(INPUT_DIR.glob("*.csv"))
        if not csv_files:
            logger.warning("No CSV files found in the input directory.")
            return

        # kClean filtering: if kClean is not "Yes", skip files with 'clean' in the filename
        if process_clean_data != "Yes":
            original_count = len(csv_files)
            csv_files = [f for f in csv_files if "clean" not in f.stem.lower()]
            logger.info(f"{len(csv_files)} CSV files remain after skipping files with 'clean' in the name because kClean is set to 'No'.")
        else:
            logger.info("kClean is set to 'Yes'; processing all CSV files, including those with 'clean' in the name.")

        # IV method filtering: if selected_iv_method is not "All", filter files by identifier
        if selected_iv_method != "All":
            identifier = iv_method_mapping.get(selected_iv_method)
            if identifier:
                original_count = len(csv_files)
                csv_files = [f for f in csv_files if identifier in f.stem.lower()]
                logger.info(f"Filtered CSV files: {len(csv_files)} of {original_count} match IV method '{selected_iv_method}'.")
            else:
                logger.warning(f"No identifier mapping found for IV method '{selected_iv_method}'. Processing all files.")

        # Filter based on expiration configuration: if expiration_option is not "All", filter by filename starting with expiration token
        if expiration_option != "All":
            original_count = len(csv_files)
            csv_files = [f for f in csv_files if f.stem.lower().startswith(expiration_option.lower())]
            logger.info(f"Filtered CSV files: {len(csv_files)} of {original_count} match expiration option '{expiration_option}'.")
        else:
            logger.info("Expiration option 'All' selected; processing all CSV files regardless of expiration indicator.")

        # Optionally sort files (e.g., prioritizing _results files)
        csv_files.sort(key=lambda f: ("_results" in f.stem, f.stem))

        for file_path in csv_files:
            logger.info(f"Processing file: {file_path}")
            process_file(file_path)

        logger.info("NDX exposure ranking process completed successfully.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    rank_all_exposures()
