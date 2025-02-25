import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.optimize import newton
from loguru import logger
from datetime import datetime, timedelta
from pathlib import Path
from joblib import Parallel, delayed
import calendar
import json

# ---------------------------- Configuration ---------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Configure logger
LOG_DIR = PROJECT_ROOT / "logs" / "iv_initial"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "ndx_grok.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# Input/Output paths
INPUT_FILE = PROJECT_ROOT / "outputs" / "step_one" / "NDX_Option_Chain.xlsx"
# For NDX outputs, store results in a dedicated subfolder under "NDX"
NDX_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "step_two" / "NDX"
NDX_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SKIPPED_FILE_DIR = PROJECT_ROOT / "outputs" / "step_two" / "Skipped_Rows"
SKIPPED_FILE_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------- Load Expiration Configuration ---------------------------- #
EXPIRATION_CONFIG_PATH = PROJECT_ROOT / "configs" / "settings" / "expiration_config.json"
try:
    with open(EXPIRATION_CONFIG_PATH, "r") as cf:
        exp_config = json.load(cf)
    expiration_option = exp_config.get("value", "EoM")
    # For NDX, only 0DTE, 1DTE, EoW are allowed. If "EoM" is chosen, default to "All".
    if expiration_option == "EoM" or expiration_option not in ["0DTE", "1DTE", "EoW", "All"]:
        logger.info("Expiration option 'EoM' not valid for NDX; defaulting to 'All'.")
        expiration_option = "All"
    logger.info(f"Expiration configuration set to: {expiration_option}")
except Exception as e:
    logger.error(f"Error loading expiration configuration: {e}. Defaulting to 'All'.")
    expiration_option = "All"

# ---------------------------- Helper Functions for Date Filtering ---------------------------- #

def get_last_trading_day(year, month):
    """Calculate the last trading day of a given month."""
    last_day = calendar.monthrange(year, month)[1]
    last_date = datetime(year, month, last_day).date()
    if last_date.weekday() == 5:  # Saturday
        last_date -= timedelta(days=1)
    elif last_date.weekday() == 6:  # Sunday
        last_date -= timedelta(days=2)
    return last_date

def get_upcoming_friday(today):
    """Return the upcoming Friday (end-of-week) for today's date."""
    days_to_friday = (4 - today.weekday()) % 7
    return today + timedelta(days=days_to_friday)

# ---------------------------- Utility Functions ---------------------------- #

def d1(S, K, T, r, sigma):
    if sigma <= 0 or T <= 0:
        return np.nan
    capped_sigma = min(sigma, 10)
    return (np.log(S / K) + (r + 0.5 * capped_sigma ** 2) * T) / (capped_sigma * np.sqrt(T))

def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

def black_scholes(S, K, T, r, sigma, option_type):
    d1_val = d1(S, K, T, r, sigma)
    d2_val = d2(S, K, T, r, sigma)
    if option_type.upper() == "CALL":
        return S * norm.cdf(d1_val) - K * np.exp(-r * T) * norm.cdf(d2_val)
    elif option_type.upper() == "PUT":
        return K * np.exp(-r * T) * norm.cdf(-d2_val) - S * norm.cdf(-d1_val)
    return np.nan

def implied_volatility(price, S, K, T, r, option_type):
    def vega(S, K, T, r, sigma):
        return S * norm.pdf(d1(S, K, T, r, sigma)) * np.sqrt(T)
    sigma_initial = 0.5
    max_sigma = 10
    try:
        sigma_est = newton(
            lambda x: black_scholes(S, K, T, r, x, option_type) - price,
            sigma_initial,
            fprime=lambda x: vega(S, K, T, r, x),
            tol=1e-6,
            maxiter=100
        )
        if sigma_est > max_sigma or sigma_est <= 0:
            logger.warning(f"Implied volatility capped or invalid for price: {price}, S: {S}, K: {K}")
            sigma_est = np.nan
    except (RuntimeError, OverflowError, ZeroDivisionError) as e:
        logger.warning(f"Newton's method failed for price: {price}, S: {S}, K: {K}, error: {e}")
        sigma_est = np.nan
    return sigma_est

def calculate_greeks(S, K, T, r, sigma, option_type):
    try:
        if sigma <= 0 or S <= 0 or K <= 0 or T <= 0:
            return None
        d1_val = d1(S, K, T, r, sigma)
        d2_val = d2(S, K, T, r, sigma)
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

# ---------------------------- Modified Process Row ---------------------------- #
# Remove the strict "expirationDate == today" check so that rows from each bucket pass
def process_row(row):
    try:
        # Convert expirationDate to date
        expiration_date = row["expirationDate"]
        if isinstance(expiration_date, str):
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()
        row_dict = row.to_dict()
        # Process other values
        S = row.get("spotPrice")
        K = row.get("strikePrice")
        T = row.get("T")
        r = row.get("SOFR")
        option_type = row.get("putCall")
        market_price = row.get("mid") or row.get("mark") or row.get("last")
        if any(param is None or param <= 0 for param in [S, K, T, r, market_price]) or not option_type:
            return None
        iv = implied_volatility(market_price, S, K, T, r, option_type)
        if np.isnan(iv):
            return None
        greeks = calculate_greeks(S, K, T, r, iv, option_type)
        if greeks is None:
            return None
        row_dict.update({"impliedVolatility": iv})
        row_dict.update(greeks)
        return row_dict
    except Exception as e:
        logger.error(f"Error processing row: {e}")
        return None

# ---------------------------- Main Processing ---------------------------- #

def ndx_grok_adjusted_processing():
    """Processes NDX option chain using Grok method with 3 expiration buckets (0DTE, 1DTE, EoW)."""
    try:
        logger.info("Starting adjusted NDX Grok processing.")
        df = pd.read_excel(INPUT_FILE)
        today = datetime.now().date()
        df["expirationDate"] = pd.to_datetime(df["expirationDate"]).dt.date

        # Create NDX expiration buckets (only 0DTE, 1DTE, and EoW)
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

        # For NDX, if expiration_option is not one of the valid keys, default to "All"
        if expiration_option not in bucket_mapping:
            logger.info(f"Expiration option '{expiration_option}' not valid for NDX; defaulting to 'All'.")
            expiration_option_use = "All"
        else:
            expiration_option_use = expiration_option

        if expiration_option_use == "All":
            for bucket, bucket_df in bucket_mapping.items():
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
                    out_file = NDX_OUTPUT_DIR / f"{bucket}_ndx_grok_results.csv"
                    save_to_csv(df_results, out_file)
                    output_files.append(out_file)
                else:
                    logger.info(f"No valid results for bucket {bucket}; no file created.")
                if skipped_rows:
                    skip_file = SKIPPED_FILE_DIR / f"{bucket}_ndx_grok_skipped.csv"
                    save_to_csv(pd.DataFrame(skipped_rows), skip_file)
                    skipped_files.append(skip_file)
                else:
                    logger.info(f"No skipped rows to save for bucket {bucket}.")
        else:
            selected_bucket = bucket_mapping.get(expiration_option_use)
            if selected_bucket is None:
                logger.error(f"Invalid expiration bucket: {expiration_option_use}")
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
                out_file = NDX_OUTPUT_DIR / f"{expiration_option_use}_ndx_grok_results.csv"
                save_to_csv(df_results, out_file)
                output_files.append(out_file)
            else:
                logger.warning(f"No valid results for bucket {expiration_option_use}; no file created.")
            if skipped_rows:
                skip_file = SKIPPED_FILE_DIR / f"{expiration_option_use}_ndx_grok_skipped.csv"
                save_to_csv(pd.DataFrame(skipped_rows), skip_file)
                skipped_files.append(skip_file)
            else:
                logger.info("No skipped rows to save.")

        logger.info("NDX Grok processing completed successfully.")
    except Exception as e:
        logger.error(f"Unexpected error during processing: {e}")

if __name__ == "__main__":
    ndx_grok_adjusted_processing()
