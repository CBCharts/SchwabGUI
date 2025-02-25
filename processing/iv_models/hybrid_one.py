import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from loguru import logger
from datetime import datetime, timedelta
from pathlib import Path
from joblib import Parallel, delayed
import calendar
import json  # For configuration loading

# ---------------------------- Configuration ---------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Configure logger
LOG_DIR = PROJECT_ROOT / "logs" / "iv_initial"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "hybrid_one.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

INPUT_FILE = PROJECT_ROOT / "outputs" / "step_one" / "SPX_Option_Chain.xlsx"
# Base output directory – files will be prefixed with their bucket indicator
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "step_two" / "hybrid_one"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SKIPPED_FILE = PROJECT_ROOT / "outputs" / "step_two" / "Skipped_Rows" / "hybrid_one_skipped.csv"

# ---------------------------- Expiration Configuration ---------------------------- #
# Define the path to the configuration file
CONFIG_FILE = PROJECT_ROOT / "configs" / "settings" / "expiration_config.json"
try:
    with open(CONFIG_FILE, "r") as cf:
        config_data = json.load(cf)
        expiration_option = config_data.get("value", "EoM")
        # Allow "All" as a valid option now
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

# ---------------------------- IV and Greek Calculation Functions ---------------------------- #

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
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        delta = norm.cdf(d1) if option_type.upper() == "CALL" else norm.cdf(d1) - 1
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T)
        theta_call = ((-S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
                      - r * K * np.exp(-r * T) * norm.cdf(d2))
        theta_put = ((-S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
                     + r * K * np.exp(-r * T) * norm.cdf(-d2))
        theta = theta_call if option_type.upper() == "CALL" else theta_put
        rho_call = K * T * np.exp(-r * T) * norm.cdf(d2)
        rho_put = -K * T * np.exp(-r * T) * norm.cdf(-d2)
        rho = rho_call if option_type.upper() == "CALL" else rho_put
        vanna = d1 * gamma
        charm = -norm.pdf(d1) * ((2 * r * T - d2 * sigma * np.sqrt(T)) / (2 * T))
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
        logger.error(f"Greek calculation error: {e}")
        return None

def process_row(row, today):
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
        initial_iv = closed_form_iv(S, K, T, r, option_type, market_price)
        refined_iv = refine_iv(S, K, T, r, option_type, market_price, initial_iv)
        greeks = calculate_greeks(S, K, T, r, refined_iv, option_type)
        if greeks is None:
            return None
        row_dict = row.to_dict()
        processed = {
            **row_dict,
            "impliedVolatility": refined_iv,
            **greeks,
            "expirationDate": expiration_date  # ensure it's a date object
        }
        return processed
    except Exception as e:
        logger.error(f"Error processing row: {e}")
        return None

def save_to_csv(df, filename):
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False)
        logger.info(f"Results saved to {filename}")
    except Exception as e:
        logger.error(f"Failed to save to CSV: {e}")

# ---------------------------- Main Processing ---------------------------- #

def hybrid_one_processing():
    try:
        logger.info("Starting Hybrid One processing (full spectrum).")
        df = pd.read_excel(INPUT_FILE)
        today = datetime.now().date()
        results = []
        skipped_rows = []
        # Process every row (do not filter by expiration date here)
        for _, row in df.iterrows():
            processed_row = process_row(row, today)
            if processed_row is None:
                exp_date = row["expirationDate"]
                if isinstance(exp_date, str):
                    exp_date = datetime.strptime(exp_date, "%Y-%m-%d").date()
                if exp_date == today:
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
                # Optionally filter out rows with gamma==0 or openInterest==0
                bucket_df = bucket_df[(bucket_df["gamma"] != 0) & (bucket_df["openInterest"] != 0)]
                if not bucket_df.empty:
                    out_filename = OUTPUT_DIR / f"{bucket_name}_hybrid_one_results.csv"
                    save_to_csv(bucket_df, out_filename)
                else:
                    logger.info(f"No data for bucket {bucket_name}; no CSV created.")
        else:
            selected_bucket = bucket_mapping.get(expiration_option)
            if selected_bucket is not None:
                selected_bucket = selected_bucket[(selected_bucket["gamma"] != 0) & (selected_bucket["openInterest"] != 0)]
                if not selected_bucket.empty:
                    out_filename = OUTPUT_DIR / f"{expiration_option}_hybrid_one_results.csv"
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
        
        logger.info("Processing completed successfully.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# ---------------------------- Main Execution ---------------------------- #

if __name__ == "__main__":
    hybrid_one_processing()
