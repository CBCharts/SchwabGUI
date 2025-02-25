import pandas as pd
import numpy as np
import json  # For configuration loading
from scipy.stats import norm
from scipy.optimize import brentq
from loguru import logger
from datetime import datetime, timedelta
from pathlib import Path
import calendar

# ---------------------------- Configuration ---------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Configure logger with enhanced settings
LOG_DIR = PROJECT_ROOT / "logs" / "iv_initial"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "brent_bs.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# Input/Output paths
INPUT_FILE = PROJECT_ROOT / "outputs" / "step_one" / "SPX_Option_Chain.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "step_two" / "brent_bs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SKIPPED_FILE = PROJECT_ROOT / "outputs" / "step_two" / "Skipped_Rows" / "brent_bs_skipped.csv"

# ---------------------------- Expiration Configuration ---------------------------- #
# Define the path to the configuration file (adjust path if needed)
CONFIG_FILE = PROJECT_ROOT / "configs" / "settings" / "expiration_config.json"
try:
    with open(CONFIG_FILE, "r") as cf:
        config_data = json.load(cf)
        expiration_option = config_data.get("value", "EoM")
        # If user mistakenly sets "Full", convert it to "EoM"
        if expiration_option == "Full":
            logger.warning("Configuration value 'Full' is deprecated. Converting to 'EoM'.")
            expiration_option = "EoM"
        # Validate the config value against the allowed options (now allowing 'All')
        if expiration_option not in ["0DTE", "1DTE", "EoW", "EoM", "All"]:
            logger.warning(f"Invalid expiration option '{expiration_option}' found in config; defaulting to 'EoM'.")
            expiration_option = "EoM"
        logger.info(f"Expiration configuration set to: {expiration_option}")
except Exception as e:
    logger.error(f"Error loading expiration configuration: {e}. Defaulting to 'EoM'.")
    expiration_option = "EoM"

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
    friday = today + timedelta(days=days_to_friday)
    return friday

# ---------------------------- Greek and IV Calculation Functions ---------------------------- #

def calculate_greeks(S, K, T, r, sigma, option_type):
    """Calculate Greeks using the Black-Scholes model."""
    try:
        if T <= 0 or sigma <= 0:
            return {
                "delta": None,
                "gamma": None,
                "vega": None,
                "theta": None,
                "rho": None,
                "vanna": None,
                "charm": None,
            }
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        # Near-expiry adjustments
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
        charm = (-norm.pdf(d1)
                 * (2 * r * T - d2 * sigma * np.sqrt(T))
                 / (2 * T * sigma * np.sqrt(T)))
        return {
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
            "vanna": vanna,
            "charm": charm,
        }
    except Exception as e:
        logger.error(f"Error in Greek calculation: {e}")
        return {
            "delta": None,
            "gamma": None,
            "vega": None,
            "theta": None,
            "rho": None,
            "vanna": None,
            "charm": None,
        }

def calculate_implied_volatility(market_price, S, K, T, r, option_type):
    """Calculates the implied volatility using Brent's method."""
    try:
        if S <= 0 or K <= 0 or T <= 0 or market_price <= 0:
            return None
        lower_bound = 1e-6
        upper_bound = 10  # High bound to handle extreme IV scenarios

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

# ---------------------------- Utility Function for Saving CSV ---------------------------- #

def save_to_csv(df, filename):
    """Saves the DataFrame to a CSV file."""
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False)
        logger.info(f"Results saved to {filename}")
    except Exception as e:
        logger.error(f"Failed to save to CSV: {e}")

# ---------------------------- Main Processing ---------------------------- #

def brent_bs_adjusted_processing():
    """Processes the full input file and creates expiration bucket outputs based on configuration."""
    try:
        logger.info("Starting adjusted Brent + Black-Scholes processing (full spectrum).")
        df = pd.read_excel(INPUT_FILE)
        today = datetime.now().date()
        results = []
        skipped_rows = []

        # Process every row in the input file
        for _, row in df.iterrows():
            try:
                S = row["spotPrice"]
                K = row["strikePrice"]
                T = row["T"]
                r = row["SOFR"]
                option_type = row["putCall"]
                market_price = row.get("last", None)
                # Check for missing or invalid inputs
                if pd.isnull([S, K, T, r, market_price]).any():
                    msg = "Skipped due to missing or invalid inputs."
                    logger.warning(msg)
                    skipped_row = dict(row)
                    skipped_row["skip_reason"] = msg
                    skipped_rows.append(skipped_row)
                    continue

                iv = calculate_implied_volatility(market_price, S, K, T, r, option_type)
                if iv is None:
                    msg = "Skipped due to failed IV calculation."
                    logger.warning(msg)
                    skipped_row = dict(row)
                    skipped_row["skip_reason"] = msg
                    skipped_rows.append(skipped_row)
                    continue

                greeks = calculate_greeks(S, K, T, r, iv, option_type)
                greeks["impliedVolatility"] = iv
                # Convert expirationDate to a date object
                exp_date = pd.to_datetime(row["expirationDate"]).date()
                processed = {**row, **greeks, "expirationDate": exp_date}
                results.append(processed)
            except Exception as e:
                logger.error(f"Row processing failed: {e}")
                skipped_row = dict(row)
                skipped_row["skip_reason"] = f"Exception: {e}"
                skipped_rows.append(skipped_row)

        if not results:
            logger.warning("No valid results to save after processing.")
            return

        df_results = pd.DataFrame(results)

        # Create bucketed datasets based on expiration date ranges:
        df_0dte = df_results[df_results["expirationDate"] == today]
        df_1dte = df_results[(df_results["expirationDate"] >= today) & 
                             (df_results["expirationDate"] <= (today + timedelta(days=1)))]
        upcoming_friday = get_upcoming_friday(today)
        df_eow = df_results[(df_results["expirationDate"] >= today) & 
                            (df_results["expirationDate"] <= upcoming_friday)]
        last_day = get_last_trading_day(today.year, today.month)
        df_eom = df_results[(df_results["expirationDate"] >= today) & 
                            (df_results["expirationDate"] <= last_day)]

        # Map configuration option to the corresponding bucket
        bucket_mapping = {
            "0DTE": df_0dte,
            "1DTE": df_1dte,
            "EoW": df_eow,
            "EoM": df_eom
        }

        # Modified processing: if 'All' is selected, process every bucket
        if expiration_option == "All":
            for bucket_name, bucket_df in bucket_mapping.items():
                # Optionally filter out rows with gamma == 0
                bucket_df = bucket_df[bucket_df["gamma"] != 0]
                if not bucket_df.empty:
                    out_filename = OUTPUT_DIR / f"{bucket_name}_brent_bs_results.csv"
                    save_to_csv(bucket_df, out_filename)
                else:
                    logger.info(f"No data for bucket {bucket_name}; no CSV created.")
        else:
            selected_bucket = bucket_mapping.get(expiration_option)
            if selected_bucket is not None:
                # Optionally filter out rows with gamma == 0
                selected_bucket = selected_bucket[selected_bucket["gamma"] != 0]
                if not selected_bucket.empty:
                    out_filename = OUTPUT_DIR / f"{expiration_option}_brent_bs_results.csv"
                    save_to_csv(selected_bucket, out_filename)
                else:
                    logger.info(f"No data for bucket {expiration_option}; no CSV created.")
            else:
                logger.error(f"Invalid expiration option '{expiration_option}'; no bucket processed.")

        if skipped_rows:
            df_skipped = pd.DataFrame(skipped_rows)
            save_to_csv(df_skipped, SKIPPED_FILE)
        else:
            logger.info("No skipped rows to save.")

        logger.info("Brent BS processing completed successfully.")
    except Exception as e:
        logger.error(f"Processing failed: {e}")

# ---------------------------- Main Execution ---------------------------- #

if __name__ == "__main__":
    brent_bs_adjusted_processing()
