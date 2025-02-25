import sys
from pathlib import Path
import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR
from loguru import logger
from schwab_api import get_access_token

# -------------------------- Configuration --------------------------

# Configure logger with enhanced settings
LOG_DIR = Path(__file__).resolve().parent.parent / "logs" / "spot_prices"
LOG_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
logger.add(
    LOG_DIR / "spot_price.log",
    rotation="1 MB",
    level="INFO",
    backtrace=True,
    diagnose=True
)

# Project root and configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STEP_ONE_FOLDER = PROJECT_ROOT / "outputs" / "step_one"
OPTION_CHAIN_FILE = STEP_ONE_FOLDER / "SPX_Option_Chain.xlsx"
OUTPUT_FILE = STEP_ONE_FOLDER / "spot_price_differences.xlsx"

# -------------------------- Utility Functions --------------------------

def get_nearest_es_contract():
    """
    Determines the nearest ES contract symbol based on the current date and the roll period.
    Returns the Schwab API ticker for the nearest ES futures contract.
    """
    month_codes = {3: 'H', 6: 'M', 9: 'U', 12: 'Z'}
    today = datetime.now()
    months_sorted = sorted(month_codes.keys())

    for i, month in enumerate(months_sorted):
        third_friday = datetime(today.year, month, 1) + relativedelta(weekday=FR(3))
        roll_date = third_friday - relativedelta(days=8)

        if today < roll_date:
            contract = f"/ES{month_codes[month]}{str(today.year)[-2:]}"
            logger.info(f"Using current ES contract: {contract}")
            return contract
        elif roll_date <= today < third_friday:
            if i + 1 < len(months_sorted):
                next_month = months_sorted[i + 1]
                next_year = today.year
            else:
                next_month = 3
                next_year = today.year + 1

            contract = f"/ES{month_codes[next_month]}{str(next_year)[-2:]}"
            logger.info(f"Rolling to next ES contract: {contract}")
            return contract

    contract = f"/ESH{str(today.year + 1)[-2:]}"
    logger.info(f"Defaulting to next year's March ES contract: {contract}")
    return contract

def get_spot_price(schwab_symbol):
    """
    Retrieves the spot price for a given symbol using the Schwab API.
    """
    try:
        access_token = get_access_token()
        if not access_token:
            logger.error("Unable to retrieve access token.")
            return None

        url = "https://api.schwabapi.com/marketdata/v1/quotes"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"symbols": schwab_symbol}

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        spot_price = data.get(schwab_symbol, {}).get("quote", {}).get("lastPrice")
        if spot_price is not None:
            logger.info(f"Retrieved spot price for {schwab_symbol}: {spot_price}")
            return float(spot_price)
        else:
            logger.error(f"Spot price not found for {schwab_symbol}.")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching spot price for {schwab_symbol}: {e}")
        return None

# -------------------------- Main Logic --------------------------

def calculate_spot_price_differences():
    """
    Retrieves SPX, SPY, and ES spot prices, calculates differences,
    updates the SPX option chain with the SPX spot price,
    and saves results to a new Excel file in the step_one folder.
    """
    # Ensure step_one folder exists
    STEP_ONE_FOLDER.mkdir(parents=True, exist_ok=True)

    # Load the SPX option chain
    try:
        option_chain = pd.read_excel(OPTION_CHAIN_FILE)
        logger.info(f"Loaded option chain data from {OPTION_CHAIN_FILE}.")
    except Exception as e:
        logger.error(f"Failed to load SPX option chain file: {e}")
        return

    # Retrieve SPX, SPY, and ES spot prices
    spx_spot_price = get_spot_price("$SPX")
    spy_spot_price = get_spot_price("SPY")
    es_contract = get_nearest_es_contract()
    es_spot_price = get_spot_price(es_contract)

    if None in (spx_spot_price, spy_spot_price, es_spot_price):
        logger.error("Failed to retrieve all required spot prices. Exiting.")
        return

    # Calculate differences
    spx_spy_diff = spy_spot_price - spx_spot_price
    spx_es_diff = es_spot_price - spx_spot_price
    spx_spy_pct_diff = (spx_spy_diff / spx_spot_price) * 100
    spx_es_pct_diff = (spx_es_diff / spx_spot_price) * 100

    # Log results
    logger.info(f"SPX Spot Price: {spx_spot_price}")
    logger.info(f"SPY Spot Price: {spy_spot_price}")
    logger.info(f"ES Spot Price ({es_contract}): {es_spot_price}")
    logger.info(f"SPX-SPY Difference: {spx_spy_diff} ({spx_spy_pct_diff:.2f}%)")
    logger.info(f"SPX-ES Difference: {spx_es_diff} ({spx_es_pct_diff:.2f}%)")

    # Update SPX Option Chain with SPX Spot Price
    option_chain["spotPrice"] = spx_spot_price
    try:
        option_chain.to_excel(OPTION_CHAIN_FILE, index=False)
        logger.info(f"Updated SPX option chain saved to {OPTION_CHAIN_FILE}.")
    except Exception as e:
        logger.error(f"Failed to update SPX option chain file: {e}")

    # Save spot prices and differences to a new Excel file
    data = {
        "Symbol": ["SPX", "SPY", "/ES", "SPX-SPY Diff", "SPX-SPY % Diff", "SPX-ES Diff", "SPX-ES % Diff"],
        "Spot Price": [spx_spot_price, spy_spot_price, es_spot_price, spx_spy_diff, spx_spy_pct_diff, spx_es_diff, spx_es_pct_diff],
    }
    df = pd.DataFrame(data)

    try:
        df.to_excel(OUTPUT_FILE, index=False)
        logger.info(f"Spot prices and differences saved to {OUTPUT_FILE}.")
    except Exception as e:
        logger.error(f"Failed to save spot prices to {OUTPUT_FILE}: {e}")

# -------------------------- Main Execution --------------------------

if __name__ == "__main__":
    calculate_spot_price_differences()
