import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from loguru import logger
from datetime import datetime, timedelta
from pathlib import Path
from joblib import Parallel, delayed
import json

# ---------------------------- Configuration ---------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Configure logger
LOG_DIR = PROJECT_ROOT / "logs" / "iv_initial"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "ndx_hybrid_one.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# Input/Output paths
INPUT_FILE = PROJECT_ROOT / "outputs" / "step_one" / "NDX_Option_Chain.xlsx"
OUTPUT_FILE_DIR = PROJECT_ROOT / "outputs" / "step_two" / "NDX"
OUTPUT_FILE_DIR.mkdir(parents=True, exist_ok=True)
SKIPPED_FILE_DIR = PROJECT_ROOT / "outputs" / "step_two" / "Skipped_Rows"
SKIPPED_FILE_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------- Load Expiration Configuration ---------------------------- #
EXPIRATION_CONFIG_PATH = PROJECT_ROOT / "configs" / "settings" / "expiration_config.json"
try:
    with open(EXPIRATION_CONFIG_PATH, "r") as cf:
        exp_config = json.load(cf)
    expiration_option = exp_config.get("value", "EoM")
    # For NDX, only 0DTE, 1DTE, and EoW are valid; if config is "EoM" (or any invalid value), default to "All"
    if expiration_option == "EoM" or expiration_option not in ["0DTE", "1DTE", "EoW", "All"]:
        logger.info("Expiration option for NDX must be 0DTE, 1DTE, or EoW; defaulting to 'All'.")
        expiration_option = "All"
    logger.info(f"Expiration configuration set to: {expiration_option}")
except Exception as e:
    logger.error(f"Error loading expiration configuration: {e}. Defaulting to 'All'.")
    expiration_option = "All"

# ---------------------------- Helper Functions for Date Filtering ---------------------------- #

def get_upcoming_friday(today):
    """Return the upcoming Friday (end-of-week) for today's date."""
    days_to_friday = (4 - today.weekday()) % 7
    return today + timedelta(days=days_to_friday)

# ---------------------------- Utility Functions ---------------------------- #

def closed_form_iv(S, K, T, r, option_type, observed_price):
    try:
        if observed_price <= 0 or S <= 0 or K <= 0 or T <= 0:
            return np.nan
        intrinsic_value = max(0, S - K) if option_type.upper() == "CALL" else max(0, K - S)
        if observed_price <= intrinsic_value:
            return 0.0
        moneyness = np.log(S / K)
        volatility_estimate = (observed_price / S) * np.sqrt(2 * np.pi / T)
        adjustment = ((moneyness if option_type.upper() == "CALL" else -moneyness) / volatility_estimate) + (r * np.sqrt(T) / volatility_estimate)
        return max(volatility_estimate * (1 + adjustment), 0.0)
    except Exception as e:
        logger.error(f"Closed-form IV error: {e}")
        return np.nan

def refine_iv(S, K, T, r, option_type, observed_price, initial_iv):
    def objective(sigma):
        return black_scholes_price(S, K, T, r, sigma, option_type) - observed_price
    lower_bound = max(1e-6, initial_iv * 0.5)
    upper_bound = min(5.0, max(1.0, initial_iv * 1.5))
    try:
        refined_iv = brentq(objective, lower_bound, upper_bound, xtol=1e-8)
        return refined_iv
    except Exception as e:
        logger.error(f"Refinement error: {e}")
        return initial_iv

def black_scholes_price(S, K, T, r, sigma, option_type):
    if any(param <= 0 for param in [S, K, T, sigma]):
        return np.nan
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type.upper() == "CALL":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type.upper() == "PUT":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return np.nan

def calculate_greeks(S, K, T, r, sigma, option_type):
    try:
        if any(param <= 0 for param in [S, K, T, sigma]):
            return None
        d1_val = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2_val = d1_val - sigma * np.sqrt(T)
        delta = norm.cdf(d1_val) if option_type.upper() == "CALL" else norm.cdf(d1_val) - 1
        gamma = norm.pdf(d1_val) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1_val) * np.sqrt(T)
        theta_call = ((-S * norm.pdf(d1_val) * sigma) / (2 * np.sqrt(T))
                      - r * K * np.exp(-r * T) * norm.cdf(d2_val))
        theta_put = ((-S * norm.pdf(d1_val) * sigma) / (2 * np.sqrt(T))
                     + r * K * np.exp(-r * T) * norm.cdf(-d2_val))
        theta = theta_call if option_type.upper() == "CALL" else theta_put
        rho_call = K * T * np.exp(-r * T) * norm.cdf(d2_val)
        rho_put = -K * T * np.exp(-r * T) * norm.cdf(-d2_val)
        rho = rho_call if option_type.upper() == "CALL" else rho_put
        vanna = d2_val * S * norm.pdf(d1_val) / sigma
        charm = (-norm.pdf(d1_val) * (2 * r * T - d2_val * sigma * np.sqrt(T))
                 / (2 * T * sigma * np.sqrt(T)))
        return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta,
                "rho": rho, "vanna": vanna, "charm": charm}
    except Exception as e:
        logger.error(f"Error in Greek calculation: {e}")
        return None

def save_to_csv(df, filename):
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False)
        logger.info(f"Results saved to {filename}")
    except Exception as e:
        logger.error(f"Failed to save to CSV: {e}")

# ---------------------------- Process Row Function ---------------------------- #
def process_row(row):
    try:
        # Convert expirationDate to date
        expiration_date = row["expirationDate"]
        if isinstance(expiration_date, str):
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()
        row_dict = row.to_dict()
        S = row.get("spotPrice")
        K = row.get("strikePrice")
        T = row.get("T")
        r = row.get("SOFR")
        option_type = row.get("putCall")
        market_price = row.get("mid") or row.get("mark") or row.get("last")
        if any(param is None or param <= 0 for param in [S, K, T, r, market_price]) or not option_type:
            return None
        initial_iv = closed_form_iv(S, K, T, r, option_type, market_price)
        refined_iv = refine_iv(S, K, T, r, option_type, market_price, initial_iv)
        greeks = calculate_greeks(S, K, T, r, refined_iv, option_type)
        if greeks is None:
            return None
        row_dict.update({"impliedVolatility": refined_iv})
        row_dict.update(greeks)
        return row_dict
    except Exception as e:
        logger.error(f"Error processing row: {e}")
        return None

# ---------------------------- Main Processing ---------------------------- #

def ndx_hybrid_one_adjusted_processing():
    """
    Processes NDX option chain using the Hybrid One method with expiration bucketing.
    For NDX, only three buckets are valid: 0DTE, 1DTE, and EoW.
    If expiration_config.json specifies an invalid bucket (e.g. "EoM"), default to processing all buckets.
    """
    try:
        logger.info("Starting adjusted NDX Hybrid One processing.")
        df = pd.read_excel(INPUT_FILE)
        today = datetime.now().date()
        df["expirationDate"] = pd.to_datetime(df["expirationDate"]).dt.date

        # Create buckets for NDX: 0DTE, 1DTE, and EoW
        df_0dte = df[df["expirationDate"] == today]
        df_1dte = df[(df["expirationDate"] >= today) & (df["expirationDate"] <= today + timedelta(days=1))]
        upcoming_friday = get_upcoming_friday(today)
        df_eow = df[(df["expirationDate"] >= today) & (df["expirationDate"] <= upcoming_friday)]

        bucket_mapping = {
            "0DTE": df_0dte,
            "1DTE": df_1dte,
            "EoW": df_eow
        }

        output_files = []
        skipped_files = []

        # For NDX, if expiration_option is not one of the three valid keys, default to "All"
        if expiration_option not in bucket_mapping:
            logger.info(f"Expiration option '{expiration_option}' not valid for NDX; defaulting to 'All'.")
            expiration_use = "All"
        else:
            expiration_use = expiration_option

        if expiration_use == "All":
            for bucket, bucket_df in bucket_mapping.items():
                # Exclude rows with zero openInterest
                bucket_df = bucket_df[bucket_df["openInterest"] != 0].copy()
                results = []
                skipped_rows = []
                for _, row in bucket_df.iterrows():
                    processed = process_row(row)
                    if processed is None:
                        skipped_rows.append(row.to_dict())
                    else:
                        results.append(processed)
                if results:
                    df_results = pd.DataFrame(results)
                    df_results = df_results[df_results["gamma"] != 0]
                    out_file = OUTPUT_FILE = OUTPUT_FILE_DIR / f"{bucket}_ndx_hybrid_one_results.csv"
                    save_to_csv(df_results, out_file)
                    output_files.append(out_file)
                else:
                    logger.info(f"No valid results for bucket {bucket}; no file created.")
                if skipped_rows:
                    skip_file = SKIPPED_FILE_DIR / f"{bucket}_ndx_hybrid_one_skipped.csv"
                    save_to_csv(pd.DataFrame(skipped_rows), skip_file)
                    skipped_files.append(skip_file)
                else:
                    logger.info(f"No skipped rows to save for bucket {bucket}.")
        else:
            selected_bucket = bucket_mapping.get(expiration_use)
            if selected_bucket is None:
                logger.error(f"Invalid expiration bucket: {expiration_use}")
                return
            selected_bucket = selected_bucket[selected_bucket["openInterest"] != 0]
            results = []
            skipped_rows = []
            for _, row in selected_bucket.iterrows():
                processed = process_row(row)
                if processed is None:
                    skipped_rows.append(row.to_dict())
                else:
                    results.append(processed)
            if results:
                df_results = pd.DataFrame(results)
                df_results = df_results[df_results["gamma"] != 0]
                out_file = OUTPUT_FILE = OUTPUT_FILE_DIR / f"{expiration_use}_ndx_hybrid_one_results.csv"
                save_to_csv(df_results, out_file)
                output_files.append(out_file)
            else:
                logger.warning(f"No valid results for bucket {expiration_use}; no file created.")
            if skipped_rows:
                skip_file = SKIPPED_FILE_DIR / f"{expiration_use}_ndx_hybrid_one_skipped.csv"
                save_to_csv(pd.DataFrame(skipped_rows), skip_file)
                skipped_files.append(skip_file)
            else:
                logger.info("No skipped rows to save.")

        logger.info("NDX Hybrid One processing completed successfully.")
    except Exception as e:
        logger.error(f"Unexpected error during processing: {e}")

if __name__ == "__main__":
    ndx_hybrid_one_adjusted_processing()
