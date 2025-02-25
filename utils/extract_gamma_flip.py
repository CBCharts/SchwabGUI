import os
import pandas as pd
from datetime import datetime

# --------------------------
# CONFIGURATION
# --------------------------
# Dynamically get the project root directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Location of this script
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))  # Move one level up

# Input directories and files
INPUT_DIR = os.path.join(PROJECT_ROOT, "outputs", "step_three")  # CSV directory
SPX_OPTION_CHAIN_FILE = os.path.join(PROJECT_ROOT, "outputs", "step_one", "SPX_Option_Chain.xlsx")
SPOT_PRICE_DIFF_FILE = os.path.join(PROJECT_ROOT, "outputs", "step_one", "spot_price_differences.xlsx")

# --------------------------
# DAILY OUTPUT FILE SETUP
# --------------------------
# Create a folder for today's date if it doesn't exist
today_str = datetime.now().strftime("%Y-%m-%d")
daily_folder = os.path.join(PROJECT_ROOT, "outputs", "gammaflip", today_str)
if not os.path.exists(daily_folder):
    os.makedirs(daily_folder)
    print(f"Created daily folder: {daily_folder}")

# Define the daily CSV file paths
daily_files = {
    "brent_bs": os.path.join(daily_folder, "gamma_flip_brent_bs.csv"),
    "hybrid_one": os.path.join(daily_folder, "gamma_flip_hybrid_one.csv"),
    "grok": os.path.join(daily_folder, "gamma_flip_grok.csv"),
}

# --------------------------
# UTILITY FUNCTIONS
# --------------------------
def get_spx_spot_price():
    """Extracts the first non-null SPX spot price from SPX_Option_Chain.xlsx."""
    try:
        df = pd.read_excel(SPX_OPTION_CHAIN_FILE)
        if "spotPrice" not in df.columns:
            print(f"Warning: 'spotPrice' column not found in {SPX_OPTION_CHAIN_FILE}")
            return None
        spot_price = df["spotPrice"].dropna().iloc[0]
        print(f"SPX Spot Price extracted: {spot_price}")
        return spot_price
    except Exception as e:
        print(f"Error reading SPX spot price: {e}")
        return None

def get_spx_es_diff():
    """Extracts the SPX-ES % Diff from spot_price_difference.xlsx."""
    try:
        df = pd.read_excel(SPOT_PRICE_DIFF_FILE)
        row = df[df.iloc[:, 0] == "SPX-ES % Diff"]
        if row.empty:
            print(f"Warning: 'SPX-ES % Diff' not found in {SPOT_PRICE_DIFF_FILE}")
            return None
        spx_es_diff = row.iloc[0, 1]
        print(f"SPX-ES % Diff extracted: {spx_es_diff}")
        return spx_es_diff
    except Exception as e:
        print(f"Error reading SPX-ES % Diff: {e}")
        return None

def extract_gamma_flip_values(csv_path, spx_spot_price, spx_es_diff):
    """
    Extracts the first row's values for 'timestamp', 'Gamma Flip (cum)', and 'Gamma Flip (vec)'.
    If a gamma flip value is out of range (i.e., not within [SPX spot price ± 350]), it is set to None.
    Computes:
        Theo_Cum = GammaFlipCum + (GammaFlipCum * (spx_es_diff/100))
        Theo_Vec = GammaFlipVec + (GammaFlipVec * (spx_es_diff/100))
    Returns a dictionary if at least one gamma flip value is valid.
    """
    try:
        df = pd.read_csv(csv_path)
        required_columns = ["timestamp", "Gamma Flip (cum)", "Gamma Flip (vec)"]
        if not all(col in df.columns for col in required_columns):
            missing = [c for c in required_columns if c not in df.columns]
            print(f"Skipping {csv_path}, missing columns: {missing}")
            return None

        # Extract the first row
        first_row = df.iloc[0]
        gamma_flip_cum = first_row["Gamma Flip (cum)"]
        gamma_flip_vec = first_row["Gamma Flip (vec)"]

        # Define valid bounds (SPX spot price ± 350)
        lower_bound = spx_spot_price - 350
        upper_bound = spx_spot_price + 350

        # Validate gamma flip values; set invalid ones to None
        if not (lower_bound <= gamma_flip_cum <= upper_bound):
            gamma_flip_cum = None
        if not (lower_bound <= gamma_flip_vec <= upper_bound):
            gamma_flip_vec = None

        # Convert SPX-ES % Diff from percentage to decimal
        spx_es_diff_decimal = spx_es_diff / 100

        # Calculate Theo values using the valid gamma flip values
        theo_cum = (gamma_flip_cum + (gamma_flip_cum * spx_es_diff_decimal)) if gamma_flip_cum is not None else None
        theo_vec = (gamma_flip_vec + (gamma_flip_vec * spx_es_diff_decimal)) if gamma_flip_vec is not None else None

        # Keep the row only if at least one gammaflip value is valid
        if gamma_flip_cum is not None or gamma_flip_vec is not None:
            return {
                "timestamp": first_row["timestamp"],
                "csv extract": os.path.basename(csv_path),
                "GammaFlipCum": gamma_flip_cum,
                "GammaFlipVec": gamma_flip_vec,
                "SPX_SpotPrice": spx_spot_price,
                "Theo_Cum": round(theo_cum, 2) if theo_cum is not None else None,
                "Theo_Vec": round(theo_vec, 2) if theo_vec is not None else None
            }
        return None
    except Exception as e:
        print(f"Error processing {csv_path}: {e}")
        return None

# --------------------------
# MAIN EXECUTION
# --------------------------
if __name__ == "__main__":
    # 1. Get SPX Spot Price
    spx_spot_price = get_spx_spot_price()
    if spx_spot_price is None:
        print("No valid SPX spot price found. Exiting.")
        exit(1)

    # 2. Get SPX-ES % Diff
    spx_es_diff = get_spx_es_diff()
    if spx_es_diff is None:
        print("No valid SPX-ES % Diff found. Exiting.")
        exit(1)

    # 3. Process CSVs in step_three
    categorized_results = {
        "brent_bs": [],
        "hybrid_one": [],
        "grok": [],
    }

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".csv"):
            csv_path = os.path.join(INPUT_DIR, filename)
            row_data = extract_gamma_flip_values(csv_path, spx_spot_price, spx_es_diff)
            if row_data:
                if "_brent_bs_" in filename:
                    categorized_results["brent_bs"].append(row_data)
                elif "_hybrid_one_" in filename:
                    categorized_results["hybrid_one"].append(row_data)
                elif "_grok_" in filename:
                    categorized_results["grok"].append(row_data)

    # 4. Append results to the respective daily CSV files
    for category, file_path in daily_files.items():
        if categorized_results[category]:
            df_results = pd.DataFrame(categorized_results[category])
            write_header = not os.path.exists(file_path)
            df_results.to_csv(file_path, mode='a', header=write_header, index=False)
            print(f"Appended {len(df_results)} row(s) to {file_path}")

    print("Script execution completed.")
