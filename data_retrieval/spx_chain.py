import requests
import pandas as pd
from schwab_api import get_access_token
from loguru import logger
from datetime import datetime, timedelta
import calendar
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pytz import timezone, utc

# ---------------------------- Configuration ---------------------------- #

# Configure logger with enhanced settings
LOG_DIR = Path(__file__).resolve().parent.parent / "logs" / "spx_chain"
LOG_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
logger.add(
    LOG_DIR / "SPX_Chain.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# API configuration
API_BASE_URL = "https://api.schwabapi.com/marketdata/v1"
CHAINS_ENDPOINT = f"{API_BASE_URL}/chains"

# Symbol and output file location
SYMBOL = "$SPX"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "step_one" / "SPX_Option_Chain.xlsx"

# Retry configuration for API requests
RETRY_STRATEGY = Retry(
    total=5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"],
    backoff_factor=1
)
ADAPTER = HTTPAdapter(max_retries=RETRY_STRATEGY)
SESSION = requests.Session()
SESSION.mount("https://", ADAPTER)
SESSION.mount("http://", ADAPTER)

# Placeholders for dividend_yield and SOFR
DIVIDEND_YIELD = 0.01
SOFR = 0.0428

# ---------------------------- Utility Functions ---------------------------- #

def get_last_trading_day(year, month):
    """Calculates the last trading day of the specified month."""
    last_day = calendar.monthrange(year, month)[1]
    last_date = datetime(year, month, last_day)
    if last_date.weekday() == 5:  # Saturday
        return last_date - timedelta(days=1)
    elif last_date.weekday() == 6:  # Sunday
        return last_date - timedelta(days=2)
    return last_date

from pytz import timezone, utc

def calculate_t(expiration_date):
    """Calculates the time to expiration (T) in years using Arizona and Eastern timezones."""
    try:
        # Combine expiration date with the hardcoded expiration time (2:15 PM Arizona time)
        expiration_datetime = datetime.strptime(expiration_date, "%Y-%m-%d")
        expiration_time = datetime.strptime("14:15", "%H:%M").time()  # 2:15 PM
        expiration_combined = datetime.combine(expiration_datetime, expiration_time)

        # Convert Arizona time to Eastern Time
        arizona = timezone("US/Arizona")
        eastern = timezone("US/Eastern")
        expiration_az = arizona.localize(expiration_combined)
        expiration_et = expiration_az.astimezone(eastern)

        # Make current time timezone-aware in Arizona
        now = arizona.localize(datetime.now()).astimezone(eastern)

        # Calculate T in years (using trading days approximation)
        seconds_in_trading_year = 252 * 24 * 60 * 60
        T = max((expiration_et - now).total_seconds() / seconds_in_trading_year, 0)
        return T
    except Exception as e:
        logger.error(f"Failed to calculate T for expiration date {expiration_date}: {e}")
        return 0

def save_to_excel(data, filename):
    """Saves the flattened options data to an Excel file."""
    try:
        if not data or len(data) == 0:
            logger.warning("No data to save. Skipping Excel file creation.")
            return

        # Ensure the directory exists
        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        full_path = Path(filename).resolve()
        logger.info(f"Saving {len(data)} rows to {full_path}.")
        df = pd.DataFrame(data)
        df.to_excel(full_path, index=False)
        logger.info(f"Data successfully saved to {full_path}.")
    except Exception as e:
        logger.error(f"Failed to save data to Excel: {e}")

# ---------------------------- Main Data Fetching Logic ---------------------------- #

def fetch_spx_option_chain():
    """Fetches SPX options chain data and saves to an Excel file."""
    try:
        logger.info("Starting SPX option chain retrieval.")

        # Prepare API request
        access_token = get_access_token()
        if not access_token:
            logger.error("Access token not available.")
            return

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }

        today = datetime.today()
        last_trading_day = get_last_trading_day(today.year, today.month)

        params = {
            "symbol": SYMBOL,
            "contractType": "ALL",
            "fromDate": today.strftime("%Y-%m-%d"),
            "toDate": last_trading_day.strftime("%Y-%m-%d"),
        }

        logger.debug(f"Requesting SPX option chain with params: {params}")
        logger.debug(f"Request headers: {headers}")

        response = SESSION.get(CHAINS_ENDPOINT, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        logger.debug(f"Response status code: {response.status_code}")
        data = response.json()

        # Process and save data
        options_data = flatten_options_data(data)
        save_to_excel(options_data, OUTPUT_FILE)

    except requests.exceptions.RequestException as e:
        logger.error(f"RequestException occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# ---------------------------- Data Flattening ---------------------------- #

def flatten_options_data(data):
    """Flattens the nested options chain data."""
    logger.info("Flattening options data.")
    flat_data = []

    for option_type in ["callExpDateMap", "putExpDateMap"]:
        if option_type in data:
            for exp_date, strikes in data[option_type].items():
                for strike, options in strikes.items():
                    for option in options:
                        flat_option = {
                            "description": option.get("description"),
                            "last": option.get("last"),
                            "mark": option.get("mark"),
                            "openInterest": option.get("openInterest"),
                            "totalVolume": option.get("totalVolume"),
                            "bid": option.get("bid"),
                            "ask": option.get("ask"),
                            "mid": (option.get("bid", 0) + option.get("ask", 0)) / 2,
                            "expirationDate": exp_date.split(":")[0],
                            "strikePrice": float(strike),
                            "putCall": option.get("putCall"),
                            "dividend_yield": DIVIDEND_YIELD,
                            "SOFR": SOFR,
                            "T": calculate_t(exp_date.split(":")[0]),
                        }
                        flat_data.append(flat_option)

    logger.info(f"Flattened {len(flat_data)} options records.")
    return flat_data

# ---------------------------- Main Execution ---------------------------- #

if __name__ == "__main__":
    fetch_spx_option_chain()
