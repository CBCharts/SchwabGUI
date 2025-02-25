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
    LOG_DIR / "greek_totals.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# Define the 3 target directories for input CSV files
target_dirs = [
    PROJECT_ROOT / "outputs" / "step_two" / "grok",
    PROJECT_ROOT / "outputs" / "step_two" / "hybrid_one",
    PROJECT_ROOT / "outputs" / "step_two" / "brent_bs"
]

# Centralized output directory for ratio results
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "step_three" / "ratio"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SPX_SPOT_DIFF_FILE = PROJECT_ROOT / "outputs" / "step_one" / "spot_price_differences.xlsx"

# ---------------------------- Load JSON Configurations ---------------------------- #
# Load IV Method configuration
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
    # Allow "All" as a valid option in addition to the others
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

def calculate_greek_totals(df):
    """Calculate total Call and Put exposure for DEX, GEX, CEX and VEX."""
    try:
        greek_totals = []
        for greek in ["DEX", "GEX", "CEX", "VEX"]:
            call_total = df.loc[df["putCall"].str.upper() == "CALL", greek].sum()
            put_total  = df.loc[df["putCall"].str.upper() == "PUT",  greek].sum()
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

def update_ranked_file(processed_file_path, cum_gam, vec_gam):
    """
    Update the corresponding ranked file in project_root/outputs/step_three with
    two new columns: "Gamma Flip (cum)" and "Gamma Flip (vec)" populated with the
    computed gamma flip values.
    
    The ranked file is assumed to have a name of the form:
      {expiration}_{ivmethod}_{results or clean}_ranked.csv
    which is obtained by taking the processed file's stem and appending "_ranked.csv".
    """
    # The ranked files are in the parent folder of OUTPUT_DIR (i.e. project_root/outputs/step_three)
    ranked_dir = OUTPUT_DIR.parent  # project_root/outputs/step_three
    # Form the ranked file name by appending "_ranked" to the processed file's stem
    ranked_stem = processed_file_path.stem + "_ranked"
    ranked_file = ranked_dir / (ranked_stem + ".csv")
    if ranked_file.exists():
        try:
            df_ranked = pd.read_csv(ranked_file)
            df_ranked["Gamma Flip (cum)"] = cum_gam
            df_ranked["Gamma Flip (vec)"] = vec_gam
            df_ranked.to_csv(ranked_file, index=False)
            logger.info(f"Ranked file {ranked_file} updated with gamma flip values.")
        except Exception as e:
            logger.error(f"Error updating ranked file {ranked_file}: {e}")
    else:
        logger.warning(f"Ranked file {ranked_file} not found; skipping update.")

def process_file(file_path):
    """
    Process a single CSV file to:
      1. Validate and convert numeric columns.
      2. Calculate two Gamma Flip values:
           - cum_gam: Using an iterative cumulative GEX approach.
           - vec_gam: Using a vectorized approach (detecting zero crossings via np.diff(np.sign(...))).
      3. Overwrite the input file with new columns "cum_gam" and "cum_vec".
      4. Calculate Greek totals and save them to an output CSV.
      5. Save a separate CSV with cumulative GEX details for diagnostics.
      6. Update the corresponding ranked file with gamma flip values.
    """
    try:
        logger.info(f"Processing file: {file_path}")
        df = pd.read_csv(file_path)

        # Validate required columns
        required_columns = ["putCall", "DEX", "GEX", "CEX", "VEX"]
        validate_columns(df, required_columns)
        for col in ["DEX", "GEX", "CEX", "VEX"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Initialize gamma flip values
        cum_gam = None
        vec_gam = None
        gamma_flip_details = None

        if "strikePrice" in df.columns:
            df["strikePrice"] = pd.to_numeric(df["strikePrice"], errors="coerce")
            # Group by strikePrice and sum GEX, then sort strikes in descending order
            gex_by_strike = df.groupby("strikePrice")["GEX"].sum().sort_index(ascending=False)
            cumulative_gex = gex_by_strike.cumsum()
            
            
            # --- Cumulative (iterative) method ("cum_gam") ---
            prev_strike = None
            prev_cum_gex = None
            for strike, cum_value in cumulative_gex.items():
                if prev_cum_gex is not None:
                    if prev_cum_gex > 0 and cum_value < 0:
                        fraction = prev_cum_gex / (prev_cum_gex - cum_value)
                        cum_gam = prev_strike - fraction * (prev_strike - strike)
                        break
                prev_strike = strike
                prev_cum_gex = cum_value
            logger.info(f"Gamma Flip (cum) value for file {file_path}: {cum_gam}")

            # --- Vectorized method ("vec_gam") ---
            levels = gex_by_strike.index.to_numpy()  # strikes sorted descending
            totalGamma = cumulative_gex.to_numpy()
            # Find indices where sign changes in totalGamma
            zeroCrossIdx = np.where(np.diff(np.sign(totalGamma)))[0]
            if zeroCrossIdx.size > 0:
                i = zeroCrossIdx[0]
                negGamma = totalGamma[i]
                posGamma = totalGamma[i+1]
                negStrike = levels[i]
                posStrike = levels[i+1]
                fraction = negGamma / (negGamma - posGamma)
                vec_gam = negStrike - fraction * (negStrike - posStrike)
            else:
                vec_gam = None
            logger.info(f"Gamma Flip (vec) value for file {file_path}: {vec_gam}")
        else:
            logger.warning("Column 'strikePrice' not found in file; cannot compute Gamma Flip.")
        
        # Amend the input file with the new gamma flip columns (overwrite)
        df["cum_gam"] = cum_gam
        df["cum_vec"] = vec_gam
        df.to_csv(file_path, index=False)
        logger.info(f"Input file amended with Gamma Flip columns: {file_path}")

        # Calculate Greek totals
        greek_totals_df = calculate_greek_totals(df)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        greek_totals_df.insert(0, "timestamp", timestamp)

        # Save Greek totals to output CSV
        output_file_name = file_path.stem + "_greek_totals.csv"
        output_path = OUTPUT_DIR / output_file_name
        greek_totals_df.to_csv(output_path, index=False)
        logger.info(f"Greek totals saved to: {output_path}")

        # --- New Step: Update the corresponding ranked file with gamma flip values ---
        update_ranked_file(file_path, cum_gam, vec_gam)

    except ValueError as ve:
        logger.warning(f"Validation error in {file_path}: {ve}")
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")

def calculate_all_greek_totals():
    """Main function to process all CSV files from the target directories for calculating Greek totals."""
    try:
        logger.info("Starting Greek totals calculation process.")
        csv_files = []
        # Iterate over each target directory
        for directory in target_dirs:
            files = list(directory.glob("*.csv"))
            logger.info(f"Found {len(files)} CSV files in {directory}")
            csv_files.extend(files)

        if not csv_files:
            logger.warning("No CSV files found in the target directories.")
            return

        # --- Dynamic Filtering Based on User Input ---
        # If kClean is set to "No", skip any files with 'clean' in the filename.
        if process_clean_data != "Yes":
            original_count = len(csv_files)
            csv_files = [f for f in csv_files if "clean" not in f.stem.lower()]
            logger.info(f"{len(csv_files)} CSV files remain after skipping 'clean' files (from {original_count}).")
        else:
            logger.info("kClean is set to 'Yes'; processing all files, including those with 'clean' in the name.")

        # If a specific IV method is selected (other than "All"), filter the files accordingly.
        if selected_iv_method != "All":
            identifier = iv_method_mapping.get(selected_iv_method)
            if identifier:
                original_count = len(csv_files)
                csv_files = [f for f in csv_files if identifier in f.stem.lower()]
                logger.info(f"Filtered CSV files: {len(csv_files)} of {original_count} match IV method '{selected_iv_method}'.")
            else:
                logger.warning(f"No identifier mapping found for IV method '{selected_iv_method}'. Processing all files.")
        # --- End Dynamic Filtering ---

        # Filter based on expiration configuration only if not "All"
        if expiration_option != "All":
            original_count = len(csv_files)
            csv_files = [f for f in csv_files if f.stem.lower().startswith(expiration_option.lower())]
            logger.info(f"Filtered CSV files: {len(csv_files)} of {original_count} match expiration option '{expiration_option}'.")
        else:
            logger.info("Expiration option 'All' selected; processing all CSV files regardless of expiration indicator.")

        if not csv_files:
            logger.warning("No CSV files found to process after filtering.")
            return

        # Sort files so that _results.csv is processed before _clean.csv (if both exist)
        csv_files.sort(key=lambda f: ("_results" in f.stem, f.stem))
        for file_path in csv_files:
            logger.info(f"Processing file: {file_path}")
            process_file(file_path)

        logger.info("Greek totals calculation process completed successfully.")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# ---------------------------- Entry Point ---------------------------- #

if __name__ == "__main__":
    calculate_all_greek_totals()
