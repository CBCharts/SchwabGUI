import pandas as pd
from datetime import datetime
from pathlib import Path
import json

# -------------------------- Configuration -------------------------- #

# Input/output directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RANKING_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "step_three" / "NDX"
HISTORICAL_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "NDX historical"
HISTORICAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------- Load JSON Configurations -------------------------- #

# Load IV method configuration
IV_METHOD_CONFIG_PATH = PROJECT_ROOT / "configs" / "settings" / "iv_method_config.json"
try:
    with open(IV_METHOD_CONFIG_PATH, "r") as f:
        iv_method_config = json.load(f)
    # Expected values: "All", "Hybrid_one", "Brent Black Scholes", or "Grok"
    selected_iv_method = iv_method_config.get("value", "All")
    print(f"Selected IV method: {selected_iv_method}")
except Exception as e:
    print(f"Could not load IV method config; defaulting to 'All': {e}")
    selected_iv_method = "All"

# Mapping from IV method to an identifier substring in the filenames
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
    print(f"User clean data selection: {process_clean_data}")
except Exception as e:
    print(f"Could not load kClean config; defaulting to 'Yes': {e}")
    process_clean_data = "Yes"

# -------------------------- Utility Functions -------------------------- #

def process_new_format(df):
    """
    Process the new file format and ensure compatibility with historical storage.
    """
    try:
        # Ensure required columns exist
        required_columns = ["timestamp", "strikePrice", "Theo NQ", "Rank", "Greek", "Value"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        # Ensure proper data types for sorting
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["strikePrice"] = pd.to_numeric(df["strikePrice"], errors="coerce")
        return df
    except Exception as e:
        print(f"Error processing new format: {e}")
        return None

def append_to_historical_file(new_data, historical_file):
    """
    Append new data to the historical file for the corresponding input file or create it if it doesn't exist.
    """
    try:
        if historical_file.exists():
            # Load existing historical data
            existing_data = pd.read_csv(historical_file)
            # Ensure proper data types for consistency
            existing_data["timestamp"] = pd.to_datetime(existing_data["timestamp"])
            existing_data["strikePrice"] = pd.to_numeric(existing_data["strikePrice"], errors="coerce")
            # Combine the new data with the existing data
            combined_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            # No existing file, use the new data directly
            combined_data = new_data
        # Sort the combined data for NinjaScript compatibility
        combined_data = combined_data.sort_values(by=["timestamp", "strikePrice", "Greek", "Rank"])
        # Save the combined and sorted data back to the file
        combined_data.to_csv(historical_file, index=False)
        print(f"Updated and sorted historical file: {historical_file}")
    except Exception as e:
        print(f"Error appending to historical file: {e}")

# -------------------------- Main Script -------------------------- #

def process_ranked_files():
    """
    Process all ranked files and append them to corresponding historical files.
    """
    try:
        # Create a subfolder for today's date
        today = datetime.now().strftime('%Y%m%d')
        daily_folder = HISTORICAL_OUTPUT_DIR / today
        daily_folder.mkdir(parents=True, exist_ok=True)

        # Get all ranking files
        ranked_files = list(RANKING_OUTPUT_DIR.glob("*.csv"))
        if not ranked_files:
            print("No ranking files found.")
            return

        # --- Dynamic Filtering Based on JSON Configurations ---
        # If kClean is not "Yes", skip any files with 'clean' in the filename.
        if process_clean_data != "Yes":
            original_count = len(ranked_files)
            ranked_files = [f for f in ranked_files if "clean" not in f.stem.lower()]
            print(f"{len(ranked_files)} ranking files remain after skipping files with 'clean' in the name (from {original_count}).")
        else:
            print("kClean is set to 'Yes'; processing all ranking files, including those with 'clean' in the name.")

        # If a specific IV method is selected (other than "All"), filter the files accordingly.
        if selected_iv_method != "All":
            identifier = iv_method_mapping.get(selected_iv_method)
            if identifier:
                original_count = len(ranked_files)
                ranked_files = [f for f in ranked_files if identifier in f.stem.lower()]
                print(f"Filtered ranking files: {len(ranked_files)} of {original_count} match IV method '{selected_iv_method}'.")
            else:
                print(f"No identifier mapping found for IV method '{selected_iv_method}'. Processing all ranking files.")
        # --- End Dynamic Filtering ---

        # Process each ranking file
        for ranking_file in ranked_files:
            print(f"Processing file: {ranking_file}")
            # Load the ranking file
            new_data = pd.read_csv(ranking_file)
            # Process the new data
            new_data = process_new_format(new_data)
            if new_data is None:
                print(f"Skipping file due to processing error: {ranking_file}")
                continue
            # Create a corresponding historical file name
            historical_file = daily_folder / f"{ranking_file.stem}_historical.csv"
            # Append new data to the corresponding historical file
            append_to_historical_file(new_data, historical_file)
    except Exception as e:
        print(f"Error in processing ranked files: {e}")

if __name__ == "__main__":
    process_ranked_files()
