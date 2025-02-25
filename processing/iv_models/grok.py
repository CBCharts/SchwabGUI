import pandas as pd
import numpy as np
import json  # For configuration loading
from scipy.stats import norm
from scipy.optimize import newton
from loguru import logger
from datetime import datetime, timedelta
from pathlib import Path
import calendar
from joblib import Parallel, delayed

# ---------------------------- Configuration ---------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Configure logger
LOG_DIR = PROJECT_ROOT / "logs" / "iv_initial"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "grok.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

INPUT_FILE = PROJECT_ROOT / "outputs" / "step_one" / "SPX_Option_Chain.xlsx"
# Base output directory – files will be prefixed with their bucket indicator
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "step_two" / "grok"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SKIPPED_FILE = PROJECT_ROOT / "outputs" / "step_two" / "Skipped_Rows" / "grok_skipped.csv"

# ---------------------------- Expiration Configuration ---------------------------- #
# Define the path to the configuration file
CONFIG_FILE = PROJECT_ROOT / "configs" / "settings" / "expiration_config.json"
try:
    with open(CONFIG_FILE, "r") as cf:
        config_data = json.load(cf)
        expiration_option = config_data.get("value", "EoM")
        # Allow "All" as a valid option
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

# ---------------------------- Grok Calculation Functions ---------------------------- #

def d1(S, K, T, r, sigma):
    """Calculate d1 for Black-Scholes."""
    if sigma <= 0 or T <= 0:
        return np.nan
    capped_sigma = min(sigma, 10)  # Cap sigma to prevent extreme values
    return (np.log(S / K) + (r + 0.5 * capped_sigma ** 2) * T) / (capped_sigma * np.sqrt(T))

def d2(S, K, T, r, sigma):
    """Calculate d2 for Black-Scholes."""
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

def black_scholes(S, K, T, r, sigma, option_type):
    """Calculate Black-Scholes price."""
    d1_val = d1(S, K, T, r, sigma)
    d2_val = d2(S, K, T, r, sigma)
    if option_type.upper() == "CALL":
        return S * norm.cdf(d1_val) - K * np.exp(-r * T) * norm.cdf(d2_val)
    elif option_type.upper() == "PUT":
        return K * np.exp(-r * T) * norm.cdf(-d2_val) - S * norm.cdf(-d1_val)
    return np.nan

def implied_volatility(price, S, K, T, r, option_type):
    """
    Calculate implied volatility using Newton's method with fallback and error handling.
    """
    def vega(S, K, T, r, sigma):
        return S * norm.pdf(d1(S, K, T, r, sigma)) * np.sqrt(T)
    sigma_initial = 0.5  # Initial guess
    max_sigma = 10  # Cap sigma to prevent overflow
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
    """Calculate Greeks: delta, gamma, vega, theta, rho, vanna, charm."""
    try:
        if sigma <= 0 or S <= 0 or K <= 0 or T <= 0:
            return None

        d1_val = d1(S, K, T, r, sigma)
        d2_val = d2(S, K, T, r, sigma)

        # Delta
        delta = norm.cdf(d1_val) if option_type.upper() == "CALL" else norm.cdf(d1_val) - 1

        # Gamma
        gamma = norm.pdf(d1_val) / (S * sigma * np.sqrt(T))

        # Vega
        vega = S * norm.pdf(d1_val) * np.sqrt(T)

        # Theta
        theta_call = (
            (-S * norm.pdf(d1_val) * sigma) / (2 * np.sqrt(T))
            - r * K * np.exp(-r * T) * norm.cdf(d2_val)
        )
        theta_put = (
            (-S * norm.pdf(d1_val) * sigma) / (2 * np.sqrt(T))
            + r * K * np.exp(-r * T) * norm.cdf(-d2_val)
        )
        theta = theta_call if option_type.upper() == "CALL" else theta_put

        # Rho
        rho_call = K * T * np.exp(-r * T) * norm.cdf(d2_val)
        rho_put = -K * T * np.exp(-r * T) * norm.cdf(-d2_val)
        rho = rho_call if option_type.upper() == "CALL" else rho_put

        # Optimized Vanna
        vanna = d1_val * gamma

        # Optimized Charm
        charm = -norm.pdf(d1_val) * ((2 * r * T - d2_val * sigma * np.sqrt(T)) / (2 * T))

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

def process_row(row, today):
    """Process one row to calculate IV and Greeks."""
    try:
        expiration_date = row["expirationDate"]
        if isinstance(expiration_date, str):
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()
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
        return {**row.to_dict(), "impliedVolatility": iv, **greeks, "expirationDate": expiration_date}
    except Exception as e:
        logger.error(f"Error processing row: {e}")
        return None

def save_to_csv(df, filename):
    """Utility function to save DataFrame to CSV."""
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False)
        logger.info(f"Results saved to {filename}")
    except Exception as e:
        logger.error(f"Failed to save to CSV: {e}")

# ---------------------------- Main Processing ---------------------------- #

def grok_processing():
    """
    Main function to:
      1) Read the full input file.
      2) Process all rows for IV and Greeks.
      3) Create bucketed datasets for:
         - 0DTE: Expiring today.
         - 1DTE: Expiring today or tomorrow.
         - EoW: Expiring from today through the upcoming Friday.
         - EoM: Expiring from today through the last trading day of the month.
      4) Save only the bucket indicated by the configuration.
    """
    try:
        logger.info("Starting Grok processing (full spectrum).")
        df = pd.read_excel(INPUT_FILE)
        today = datetime.now().date()
        results = []
        skipped_rows = []

        # Process every row in the input file
        for _, row in df.iterrows():
            processed_row = process_row(row, today)
            if processed_row is None:
                skipped_rows.append(row.to_dict())
            else:
                results.append(processed_row)

        df_results = pd.DataFrame(results)
        if df_results.empty:
            logger.warning("No valid rows to save after processing.")
            return

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
        
        # Modified processing: if "All" is selected, process every bucket
        if expiration_option == "All":
            for bucket_name, bucket_df in bucket_mapping.items():
                # Optionally filter out rows with gamma == 0
                bucket_df = bucket_df[bucket_df["gamma"] != 0]
                if not bucket_df.empty:
                    out_filename = OUTPUT_DIR / f"{bucket_name}_grok_results.csv"
                    save_to_csv(bucket_df, out_filename)
                else:
                    logger.info(f"No data for bucket {bucket_name}; no CSV created.")
        else:
            selected_bucket = bucket_mapping.get(expiration_option)
            if selected_bucket is not None:
                selected_bucket = selected_bucket[selected_bucket["gamma"] != 0]
                if not selected_bucket.empty:
                    out_filename = OUTPUT_DIR / f"{expiration_option}_grok_results.csv"
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

        logger.info("Grok processing completed successfully.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# ---------------------------- Main Execution ---------------------------- #

if __name__ == "__main__":
    grok_processing()
