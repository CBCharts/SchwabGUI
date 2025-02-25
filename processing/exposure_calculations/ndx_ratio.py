import pandas as pd
import json
from pathlib import Path
from loguru import logger
from datetime import datetime
import numpy as np

# ---------------------------- Configuration ---------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Configure logger
LOG_DIR = PROJECT_ROOT / "logs" / "greek_totals"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "ndx_greek_totals.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# For NDX, input files are in a dedicated folder
INPUT_DIR = PROJECT_ROOT / "outputs" / "step_two" / "NDX"
# Output ranked files are saved in a dedicated NDX subfolder under step_three/ratio
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "step_three" / "ratio" / "NDX"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
    # For NDX, valid expirations are only "0DTE", "1DTE", and "EoW". If invalid (e.g. "EoM"), default to "All"
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

def calculate_greek_totals(df):
    """Calculate total Call and Put exposure for DEX, GEX, VEX, and CEX."""
    try:
        greek_totals = []
        for greek in ["DEX", "GEX", "VEX", "CEX"]:
            call_total = df.loc[df["putCall"].str.upper() == "CALL", greek].sum()
            put_total  = df.loc[df["putCall"].str.upper() == "PUT", greek].sum()
            call_total_abs = abs(call_total)
            put_total_abs  = abs(put_total)
            ratio = call_total_abs / put_total_abs if put_total_abs != 0 else None
            greek_totals.append({
                "Greek": greek,
                "Call": round(call_total, 3),
                "Put": round(put_total, 3),
                "Ratio": round(ratio, 6) if ratio is not None else None
            })
        return pd.DataFrame(greek_totals)
    except Exception as e:
        logger.error(f"Error calculating Greek totals: {e}")
        return pd.DataFrame()

def process_file(file_path):
    """
    Process a single CSV file to compute total exposures, calculate dual Gamma Flip values
    (cumulative and vectorized), and amend the input file by adding these Gamma Flip columns.
    Then, calculate Greek totals (including CEX) and save the output.
    """
    try:
        logger.info(f"Processing file: {file_path}")
        df = pd.read_csv(file_path)

        # Validate required columns for Greek totals
        required_columns = ["putCall", "DEX", "GEX", "VEX", "CEX"]
        validate_columns(df, required_columns)

        for col in ["DEX", "GEX", "VEX", "CEX"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Calculate dual Gamma Flip values
        gamma_flip_cum = None
        gamma_flip_vec = None
        if "strikePrice" in df.columns:
            df["strikePrice"] = pd.to_numeric(df["strikePrice"], errors="coerce")
            gex_by_strike = df.groupby("strikePrice")["GEX"].sum().sort_index(ascending=False)
            cumulative_gex = gex_by_strike.cumsum()

            prev_strike = None
            prev_cum_gex = None
            for strike, cum_gex in cumulative_gex.items():
                if prev_cum_gex is not None:
                    if prev_cum_gex > 0 and cum_gex < 0:
                        fraction = prev_cum_gex / (prev_cum_gex - cum_gex)
                        gamma_flip_cum = prev_strike - fraction * (prev_strike - strike)
                        break
                prev_strike = strike
                prev_cum_gex = cum_gex

            levels = gex_by_strike.index.to_numpy()
            totalGamma = cumulative_gex.to_numpy()
            zeroCrossIdx = np.where(np.diff(np.sign(totalGamma)))[0]
            if zeroCrossIdx.size > 0:
                i = zeroCrossIdx[0]
                negGamma = totalGamma[i]
                posGamma = totalGamma[i+1]
                negStrike = levels[i]
                posStrike = levels[i+1]
                fraction = negGamma / (negGamma - posGamma)
                gamma_flip_vec = negStrike - fraction * (negStrike - posStrike)
            else:
                gamma_flip_vec = None

            logger.info(f"Gamma Flip (cumulative) for {file_path}: {gamma_flip_cum}")
            logger.info(f"Gamma Flip (vectorized) for {file_path}: {gamma_flip_vec}")
        else:
            logger.warning("Column 'strikePrice' not found; cannot compute Gamma Flip.")
        
        df["Gamma Flip (cum)"] = gamma_flip_cum
        df["Gamma Flip (vec)"] = gamma_flip_vec
        df.to_csv(file_path, index=False)
        logger.info(f"Input file amended with Gamma Flip columns: {file_path}")

        greek_totals_df = calculate_greek_totals(df)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        greek_totals_df.insert(0, "timestamp", timestamp)

        output_file_name = file_path.stem + "_greek_totals.csv"
        output_path = OUTPUT_DIR / output_file_name
        greek_totals_df.to_csv(output_path, index=False)
        logger.info(f"Greek totals saved to: {output_path}")

    except ValueError as ve:
        logger.warning(f"Validation error in {file_path}: {ve}")
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")

def calculate_all_greek_totals():
    """
    Main function to process all CSV files in the NDX input folder for ranking exposures.
    Filtering is applied based on kClean, IV method, and expiration configuration.
    """
    try:
        logger.info("Starting NDX exposure ranking process.")
        csv_files = list(INPUT_DIR.glob("*.csv"))
        if not csv_files:
            logger.warning("No CSV files found in the input directory.")
            return

        if process_clean_data != "Yes":
            original_count = len(csv_files)
            csv_files = [f for f in csv_files if "clean" not in f.stem.lower()]
            logger.info(f"{len(csv_files)} CSV files remain after skipping 'clean' files (from {original_count}).")
        else:
            logger.info("kClean is set to 'Yes'; processing all CSV files, including those with 'clean' in the name.")

        if selected_iv_method != "All":
            identifier = iv_method_mapping.get(selected_iv_method)
            if identifier:
                original_count = len(csv_files)
                csv_files = [f for f in csv_files if identifier in f.stem.lower()]
                logger.info(f"Filtered CSV files: {len(csv_files)} of {original_count} match IV method '{selected_iv_method}'.")
            else:
                logger.warning(f"No identifier mapping found for IV method '{selected_iv_method}'. Processing all files.")

        if expiration_option != "All":
            original_count = len(csv_files)
            csv_files = [f for f in csv_files if f.stem.lower().startswith(expiration_option.lower())]
            logger.info(f"Filtered CSV files: {len(csv_files)} of {original_count} match expiration option '{expiration_option}'.")
        else:
            logger.info("Expiration option 'All' selected; processing all CSV files regardless of expiration indicator.")

        csv_files.sort(key=lambda f: ("_results" in f.stem, f.stem))
        for file_path in csv_files:
            logger.info(f"Processing file: {file_path}")
            process_file(file_path)

        logger.info("NDX exposure ranking process completed successfully.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    calculate_all_greek_totals()
