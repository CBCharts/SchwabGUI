import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from loguru import logger
from datetime import datetime, timedelta
from pathlib import Path
import calendar
import json

# ---------------------------- Configuration ---------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Configure logger with enhanced settings
LOG_DIR = PROJECT_ROOT / "logs" / "iv_initial"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "ndx_brent_bs.log",
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

SKIPPED_DIR = PROJECT_ROOT / "outputs" / "step_two" / "Skipped_Rows"
SKIPPED_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------- Load Expiration Configuration ---------------------------- #
EXPIRATION_CONFIG_PATH = PROJECT_ROOT / "configs" / "settings" / "expiration_config.json"
try:
    with open(EXPIRATION_CONFIG_PATH, "r") as cf:
        exp_config = json.load(cf)
    expiration_option = exp_config.get("value", "EoM")
    # For NDX scripts, if the config is "EoM", default to "All"
    if expiration_option == "EoM":
        logger.info("Expiration option 'EoM' not valid for NDX; defaulting to 'All'.")
        expiration_option = "All"
    elif expiration_option not in ["0DTE", "1DTE", "EoW", "All"]:
        logger.warning(f"Invalid expiration option '{expiration_option}' found; defaulting to 'All'.")
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
    if last_date.weekday() == 5:
        last_date -= timedelta(days=1)
    elif last_date.weekday() == 6:
        last_date -= timedelta(days=2)
    return last_date

def get_upcoming_friday(today):
    """Return the upcoming Friday (end-of-week) for today's date."""
    days_to_friday = (4 - today.weekday()) % 7
    return today + timedelta(days=days_to_friday)

# ---------------------------- Utility Functions ---------------------------- #

def calculate_greeks(S, K, T, r, sigma, option_type):
    """Calculate Greeks using the Black-Scholes model."""
    try:
        if T <= 0 or sigma <= 0:
            return {"delta": None, "gamma": None, "vega": None, "theta": None,
                    "rho": None, "vanna": None, "charm": None}
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if T < 1e-6:
            gamma = 1e-5
            delta = 1.0 if S > K else 0.0 if option_type == "CALL" else -1.0
        else:
            delta = norm.cdf(d1) if option_type == "CALL" else norm.cdf(d1) - 1
            gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T)
        theta_call = ((-S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
                      - r * K * np.exp(-r * T) * norm.cdf(d2))
        theta_put = ((-S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
                     + r * K * np.exp(-r * T) * norm.cdf(-d2))
        theta = theta_call if option_type == "CALL" else theta_put
        rho_call = K * T * np.exp(-r * T) * norm.cdf(d2)
        rho_put = -K * T * np.exp(-r * T) * norm.cdf(-d2)
        rho = rho_call if option_type == "CALL" else rho_put
        vanna = d2 * S * norm.pdf(d1) / sigma
        charm = (-norm.pdf(d1) * (2 * r * T - d2 * sigma * np.sqrt(T))
                 / (2 * T * sigma * np.sqrt(T)))
        return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta,
                "rho": rho, "vanna": vanna, "charm": charm}
    except Exception as e:
        logger.error(f"Error in Greek calculation: {e}")
        return {"delta": None, "gamma": None, "vega": None, "theta": None,
                "rho": None, "vanna": None, "charm": None}

def calculate_implied_volatility(market_price, S, K, T, r, option_type):
    """Calculates the implied volatility using Brent's method."""
    try:
        if S <= 0 or K <= 0 or T <= 0 or market_price <= 0:
            return None
        lower_bound = 1e-6
        upper_bound = 10
        def black_scholes_price(sigma):
            d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)
            if option_type == "CALL":
                return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
            elif option_type == "PUT":
                return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return brentq(lambda sigma: black_scholes_price(sigma) - market_price, lower_bound, upper_bound, xtol=1e-5)
    except Exception as e:
        logger.error(f"Failed to calculate implied volatility: {e}")
        return None

def save_to_csv(df, filename):
    """Saves the DataFrame to a CSV file."""
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False)
        logger.info(f"Results saved to {filename}")
    except Exception as e:
        logger.error(f"Failed to save to CSV: {e}")

# ---------------------------- Main Processing ---------------------------- #

def ndx_brent_bs_adjusted_processing():
    """Processes NDX option rows using Brent and Black-Scholes, with 3 expiration buckets (0DTE, 1DTE, EoW)."""
    try:
        logger.info("Starting adjusted NDX Brent + Black-Scholes processing.")
        df = pd.read_excel(INPUT_FILE)
        today = datetime.now().date()

        # Convert expirationDate column to date objects
        df["expirationDate"] = pd.to_datetime(df["expirationDate"]).dt.date

        # Create buckets for NDX (only 0DTE, 1DTE, EoW)
        df_0dte = df[df["expirationDate"] == today]
        df_1dte = df[(df["expirationDate"] >= today) & (df["expirationDate"] <= today + timedelta(days=1))]
        upcoming_friday = get_upcoming_friday(today)
        df_eow = df[(df["expirationDate"] >= today) & (df["expirationDate"] <= upcoming_friday)]
        
        # Note: EoM is not applicable for NDX; if config is not "All", it must be one of the 3 valid buckets.
        bucket_mapping = {
            "0DTE": df_0dte,
            "1DTE": df_1dte,
            "EoW": df_eow
        }

        output_files = []
        skipped_files = []

        # For NDX, if expiration_option is not one of the valid keys ("0DTE", "1DTE", "EoW"), default to "All"
        if expiration_option not in bucket_mapping:
            logger.info(f"Expiration option '{expiration_option}' not valid for NDX; defaulting to 'All'.")
            expiration_option_use = "All"
        else:
            expiration_option_use = expiration_option

        if expiration_option_use == "All":
            for bucket, bucket_df in bucket_mapping.items():
                bucket_df = bucket_df.copy()
                results = []
                skipped_rows = []
                for _, row in bucket_df.iterrows():
                    try:
                        S = row["spotPrice"]
                        K = row["strikePrice"]
                        T = row["T"]
                        r = row["SOFR"]
                        option_type = row["putCall"]
                        market_price = row.get("last", None)
                        if pd.isnull([S, K, T, r, market_price]).any():
                            row_dict = dict(row)
                            row_dict["skip_reason"] = "Missing or invalid inputs"
                            skipped_rows.append(row_dict)
                            continue
                        iv = calculate_implied_volatility(market_price, S, K, T, r, option_type)
                        if iv is None:
                            row_dict = dict(row)
                            row_dict["skip_reason"] = "Failed IV calculation"
                            skipped_rows.append(row_dict)
                            continue
                        greeks = calculate_greeks(S, K, T, r, iv, option_type)
                        greeks["impliedVolatility"] = iv
                        results.append({**row, **greeks})
                    except Exception as e:
                        logger.error(f"Row processing failed: {e}")
                        row_dict = dict(row)
                        row_dict["skip_reason"] = f"Exception: {e}"
                        skipped_rows.append(row_dict)
                if results:
                    df_results = pd.DataFrame(results)
                    df_results = df_results[df_results["gamma"] != 0]
                    out_file = NDX_OUTPUT_DIR / f"{bucket}_ndx_brent_bs_results.csv"
                    save_to_csv(df_results, out_file)
                    output_files.append(out_file)
                else:
                    logger.info(f"No valid results for bucket {bucket}; no file created.")
                if skipped_rows:
                    skip_file = SKIPPED_DIR / f"{bucket}_ndx_brent_bs_skipped.csv"
                    save_to_csv(pd.DataFrame(skipped_rows), skip_file)
                    skipped_files.append(skip_file)
        else:
            selected_bucket = bucket_mapping.get(expiration_option_use)
            if selected_bucket is None:
                logger.error(f"Invalid expiration bucket: {expiration_option_use}")
                return
            results = []
            skipped_rows = []
            for _, row in selected_bucket.iterrows():
                try:
                    S = row["spotPrice"]
                    K = row["strikePrice"]
                    T = row["T"]
                    r = row["SOFR"]
                    option_type = row["putCall"]
                    market_price = row.get("last", None)
                    if pd.isnull([S, K, T, r, market_price]).any():
                        row_dict = dict(row)
                        row_dict["skip_reason"] = "Missing or invalid inputs"
                        skipped_rows.append(row_dict)
                        continue
                    iv = calculate_implied_volatility(market_price, S, K, T, r, option_type)
                    if iv is None:
                        row_dict = dict(row)
                        row_dict["skip_reason"] = "Failed IV calculation"
                        skipped_rows.append(row_dict)
                        continue
                    greeks = calculate_greeks(S, K, T, r, iv, option_type)
                    greeks["impliedVolatility"] = iv
                    results.append({**row, **greeks})
                except Exception as e:
                    logger.error(f"Row processing failed: {e}")
                    row_dict = dict(row)
                    row_dict["skip_reason"] = f"Exception: {e}"
                    skipped_rows.append(row_dict)
            if results:
                df_results = pd.DataFrame(results)
                df_results = df_results[df_results["gamma"] != 0]
                out_file = NDX_OUTPUT_DIR / f"{expiration_option_use}_ndx_brent_bs_results.csv"
                save_to_csv(df_results, out_file)
                output_files.append(out_file)
            else:
                logger.warning(f"No valid results for bucket {expiration_option_use}; no file created.")
            if skipped_rows:
                skip_file = SKIPPED_DIR / f"{expiration_option_use}_ndx_brent_bs_skipped.csv"
                save_to_csv(pd.DataFrame(skipped_rows), skip_file)
                skipped_files.append(skip_file)
            else:
                logger.info("No skipped rows to save.")

        logger.info("NDX Brent BS processing completed successfully.")
    except Exception as e:
        logger.error(f"Processing failed: {e}")

if __name__ == "__main__":
    ndx_brent_bs_adjusted_processing()
