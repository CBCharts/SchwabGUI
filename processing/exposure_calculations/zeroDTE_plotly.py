import os
import json
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import concurrent.futures

# -----------------------------------------------------------------------------
# Input/output directories
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Instead of a single input directory, use the following subdirectories:
INPUT_SUBDIRS = ["grok", "hybrid_one", "brent_bs"]
INPUT_BASE_DIR = PROJECT_ROOT / "outputs" / "step_two"

# Where we want to output the final HTML charts
OUTPUT_DIR_CLEAN = PROJECT_ROOT / "visualization" / "plotly" / "clean"
OUTPUT_DIR_FULL  = PROJECT_ROOT / "visualization" / "plotly" / "full"

# CSVs with per-greek totals + ratio live in "step_three/ratio"
RATIO_DIR = PROJECT_ROOT / "outputs" / "step_three" / "ratio"

# Ensure output directories exist
OUTPUT_DIR_CLEAN.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR_FULL.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Load Strike Range from JSON Config
# -----------------------------------------------------------------------------
STRIKE_CONFIG_PATH = PROJECT_ROOT / "configs" / "settings" / "strikerange_config.json"

def load_strike_range():
    """Reads strike range from strikerange_config.json, defaulting to 700 if missing."""
    try:
        with open(STRIKE_CONFIG_PATH, "r") as f:
            config = json.load(f)
            return int(config.get("value", 700))
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"⚠️ Error reading {STRIKE_CONFIG_PATH}: {e}. Using default strike range 700.")
        return 700

STRIKE_RANGE = load_strike_range()

# -----------------------------------------------------------------------------
# Load IV method configuration
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# Load kClean configuration
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# Load Expiration configuration
# -----------------------------------------------------------------------------
EXPIRATION_CONFIG_PATH = PROJECT_ROOT / "configs" / "settings" / "expiration_config.json"
try:
    with open(EXPIRATION_CONFIG_PATH, "r") as cf:
        exp_config = json.load(cf)
    expiration_option = exp_config.get("value", "EoM")
    # Allow "All" as a valid option in addition to the others
    if expiration_option not in ["0DTE", "1DTE", "EoW", "EoM", "All"]:
        print(f"Invalid expiration option '{expiration_option}' found in config; defaulting to 'EoM'.")
        expiration_option = "EoM"
    print(f"Expiration configuration set to: {expiration_option}")
except Exception as e:
    print(f"Error loading expiration configuration: {e}. Defaulting to 'EoM'.")
    expiration_option = "EoM"

# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------

def group_by_greek(df: pd.DataFrame, greek_name: str) -> pd.DataFrame:
    """
    Groups the dataframe by strikePrice (ignoring putCall), summing the
    'greek_name' column across calls and puts. Returns a DataFrame:
       ['strikePrice', 'exposure'].
    """
    grouped = (
        df.groupby("strikePrice", as_index=False)[greek_name]
          .sum()
          .rename(columns={greek_name: "exposure"})
    )
    return grouped

def create_plotly_figure(
    grouped_df: pd.DataFrame,
    spot_price: float,
    title: str,
    greek_name: str,
    cum_gam: float = None,
    cum_vec: float = None,
    call_val: float = None,
    put_val: float = None,
    yaxis_range: list = None
) -> go.Figure:

    """
    Creates a horizontal bar chart (dark theme) showing total (CALL+PUT)
    exposures by strikePrice for one Greek.
    """
    color_map = {"GEX": "green", "VEX": "blue", "DEX": "red", "CEX": "pink"}
    bar_color = color_map.get(greek_name, "gray")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=grouped_df["exposure"],
            y=grouped_df["strikePrice"],
            orientation="h",
            name="Total",
            marker_color=bar_color,
            hovertemplate=f"%{{y}} total {greek_name} = %{{x}}"
        )
    )

    fig.add_hline(y=spot_price, line_dash="dash", line_color="yellow")
    fig.add_trace(
        go.Scatter(
            x=[None], y=[None],
            mode="lines",
            line=dict(dash="dash", color="yellow"),
            name="SPX Spot Price"
        )
    )

    if greek_name == "GEX":
        # Only plot cum_gam if it's within ±500 of the spot price
        if cum_gam is not None and abs(cum_gam - spot_price) <= 500:
            fig.add_hline(y=cum_gam, line_dash="dash", line_color="red")
            fig.add_trace(
                go.Scatter(
                    x=[None], y=[None],
                    mode="lines",
                    line=dict(dash="dash", color="red"),
                    name=f"cum_gam: {cum_gam}"
                )
            )
        # Only plot cum_vec if it's within ±500 of the spot price
        if cum_vec is not None and abs(cum_vec - spot_price) <= 500:
            fig.add_hline(y=cum_vec, line_dash="dash", line_color="red")
            fig.add_trace(
                go.Scatter(
                    x=[None], y=[None],
                    mode="lines",
                    line=dict(dash="dash", color="red"),
                    name=f"cum_vec: {cum_vec}"
                )
            )



    combined_xaxis_title = f"Total {greek_name} Exposure"
    if call_val is not None and put_val is not None:
        combined_xaxis_title += f" | Call: {call_val:.3f} • Put: {put_val:.3f}"

    fig.update_layout(
        template="plotly_dark",
        title=title,
        autosize=True,
        xaxis_title=combined_xaxis_title,
        yaxis_title="Strike Price",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    if yaxis_range:
        fig.update_yaxes(range=yaxis_range)

    return fig

# -----------------------------------------------------------------------------
# Process Single CSV with Dynamic Strike Range
# -----------------------------------------------------------------------------
def process_single_csv(csv_path: Path):
    """
    Reads one CSV from one of the new input folders, then produces DEX/GEX/VEX/CEX horizontal bar charts.
    Only strike prices within the user-defined strike range around the spot price are included.
    """
    df = pd.read_csv(csv_path)
    if df.empty:
        print(f"Skipping empty file: {csv_path.name}")
        return

    file_name = csv_path.name

    # Determine output directory by suffix
    if file_name.endswith("_clean.csv"):
        out_dir = OUTPUT_DIR_CLEAN
    elif file_name.endswith("_results.csv"):
        out_dir = OUTPUT_DIR_FULL
    else:
        print(f"Skipping file (no recognized suffix): {csv_path.name}")
        return

    base_no_ext = file_name.rsplit(".", 1)[0]
    ratio_csv_name = f"{base_no_ext}_greek_totals.csv"
    ratio_csv_path = RATIO_DIR / ratio_csv_name

    ratio_data = {}
    if ratio_csv_path.exists():
        df_ratios = pd.read_csv(ratio_csv_path)
        needed_cols = {"Greek", "Call", "Put", "Ratio"}
        if not df_ratios.empty and needed_cols.issubset(df_ratios.columns):
            for _, row in df_ratios.iterrows():
                greek = str(row["Greek"]).strip()
                call_val = float(row["Call"])
                put_val = float(row["Put"])
                ratio_val = float(row["Ratio"]) if not pd.isna(row["Ratio"]) else None
                ratio_data[greek] = (call_val, put_val, ratio_val)
        else:
            print(f"Missing columns in ratio CSV for {file_name}: {ratio_csv_path}")
    else:
        print(f"No ratio CSV found for {file_name} at {ratio_csv_path}")

    spot_price = df["spotPrice"].iloc[0]
    min_strike = spot_price - STRIKE_RANGE
    max_strike = spot_price + STRIKE_RANGE

    df = df[(df["strikePrice"] >= min_strike) & (df["strikePrice"] <= max_strike)]
    if df.empty:
        print(f"Skipping {csv_path.name}, no strikes in range ±{STRIKE_RANGE}")
        return

    print(f"Processing {csv_path.name} with strike range ±{STRIKE_RANGE}...")

    mod_time = os.path.getmtime(csv_path)
    timestamp_str = datetime.fromtimestamp(mod_time).strftime("%m.%d.%Y %H:%M:%S")

    # Extract expiration from the file name (assumes first token is expiration)
    expiration_from_file = csv_path.stem.split("_")[0]

    cum_gam_value = df["cum_gam"].iloc[0] if "cum_gam" in df.columns else None
    cum_vec_value = df["cum_vec"].iloc[0] if "cum_vec" in df.columns else None


    for greek_name in ["DEX", "GEX", "VEX", "CEX"]:
        grouped_df = group_by_greek(df, greek_name)
        call_val, put_val, ratio_val = (None, None, None)
        if greek_name in ratio_data:
            call_val, put_val, ratio_val = ratio_data[greek_name]
        chart_title = f"SPX {expiration_from_file} {greek_name} {timestamp_str}"
        if ratio_val is not None:
            chart_title += f" (Ratio: {ratio_val:.4f})"

        fig = create_plotly_figure(
        grouped_df,
        spot_price,
        chart_title,
        greek_name,
        cum_gam=cum_gam_value,
        cum_vec=cum_vec_value,
        call_val=call_val,
        put_val=put_val,
        yaxis_range=[min_strike, max_strike]
    )


        html_name = f"{base_no_ext}_{greek_name}.html"
        html_path = out_dir / html_name
        fig.write_html(html_path, include_plotlyjs="cdn", full_html=True, config={"responsive": True})
        print(f"Produced: {html_path}")

# -----------------------------------------------------------------------------
# Main: Dynamic File Filtering and Parallel Processing
# -----------------------------------------------------------------------------
def run_all_visualizations():
    # Gather all CSV files from the three input subdirectories
    csv_files = []
    for subfolder in INPUT_SUBDIRS:
        folder = INPUT_BASE_DIR / subfolder
        if folder.exists():
            folder_files = list(folder.glob("*.csv"))
            print(f"Found {len(folder_files)} CSV files in {folder}")
            csv_files.extend(folder_files)
        else:
            print(f"Warning: Input folder {folder} does not exist.")

    if not csv_files:
        print(f"No CSV files found in the specified input folders.")
        return

    # --- Dynamic Filtering Based on JSON Configurations ---
    # kClean filtering: if kClean != "Yes", skip files with "clean" in the filename
    if process_clean_data != "Yes":
        original_count = len(csv_files)
        csv_files = [f for f in csv_files if "clean" not in f.stem.lower()]
        print(f"{len(csv_files)} CSV files remain after skipping files with 'clean' in the name (from {original_count}).")
    else:
        print("kClean is set to 'Yes'; processing all CSV files, including those with 'clean' in the name.")

    # IV method filtering: if selected_iv_method != "All", filter files by identifier
    if selected_iv_method != "All":
        identifier = iv_method_mapping.get(selected_iv_method)
        if identifier:
            original_count = len(csv_files)
            csv_files = [f for f in csv_files if identifier in f.stem.lower()]
            print(f"Filtered CSV files: {len(csv_files)} of {original_count} match IV method '{selected_iv_method}'.")
        else:
            print(f"No identifier mapping found for IV method '{selected_iv_method}'. Processing all CSV files.")
    # --- End Dynamic Filtering ---

    # Filter based on expiration configuration only if not "All"
    if expiration_option != "All":
        original_count = len(csv_files)
        csv_files = [f for f in csv_files if f.stem.lower().startswith(expiration_option.lower())]
        print(f"Filtered CSV files: {len(csv_files)} of {original_count} match expiration option '{expiration_option}'.")
    else:
        print("Expiration option 'All' selected; processing all CSV files regardless of expiration indicator.")

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_single_csv, csv_file) for csv_file in csv_files]
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    run_all_visualizations()
