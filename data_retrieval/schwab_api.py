import os
import sys
import json
import base64
import urllib.parse
import requests
import webbrowser
from dotenv import load_dotenv
from loguru import logger
from datetime import datetime, timedelta
from pathlib import Path

# -------------------------- Configuration --------------------------

# Explicitly define project root and log location
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs" / "auth"
LOG_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

# Configure logger
logger.add(
    LOG_DIR / "auth.log",
    rotation="1 MB",
    level="INFO",
    backtrace=True,
    diagnose=True
)

# Load environment variables from .env
dotenv_path = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Token and endpoint configurations
TOKEN_FILE = PROJECT_ROOT / "schwab_token" / "token.json"
AUTH_URL = "https://api.schwabapi.com/v1/oauth/authorize"
TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"

# -------------------------- Utility Functions --------------------------

def construct_init_auth_url():
    """
    Generate the initial authorization URL for Schwab API.
    """
    app_key = os.getenv("SCHWAB_APP_KEY")
    redirect_uri = os.getenv("REDIRECT_URI")

    if not app_key or not redirect_uri:
        logger.error("Environment variables not loaded properly. Check '.env' file.")
        raise ValueError("Missing SCHWAB_APP_KEY or REDIRECT_URI in the .env file.")

    params = {
        "client_id": app_key,
        "redirect_uri": redirect_uri,
        "response_type": "code",
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    logger.info(f"Authorization URL: {auth_url}")
    return auth_url


def save_tokens(tokens):
    """
    Save tokens to a JSON file.
    """
    tokens["expires_at"] = (datetime.utcnow() + timedelta(seconds=tokens["expires_in"])).isoformat()
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, "w") as file:
        json.dump(tokens, file, indent=4)
    logger.info(f"Tokens saved to {TOKEN_FILE}")


def load_tokens():
    """
    Load tokens from a JSON file.
    """
    if not TOKEN_FILE.exists():
        logger.warning(f"Token file not found: {TOKEN_FILE}")
        return None
    with open(TOKEN_FILE, "r") as file:
        return json.load(file)


def is_token_expired(tokens):
    """
    Check if the access token is expired.
    """
    expires_at = datetime.fromisoformat(tokens["expires_at"])
    return datetime.utcnow() >= expires_at


def refresh_access_token():
    """
    Refresh the access token using the refresh token.
    """
    tokens = load_tokens()
    if not tokens or "refresh_token" not in tokens:
        logger.error("No refresh token found. Re-authentication required.")
        return None

    app_key = os.getenv("SCHWAB_APP_KEY")
    app_secret = os.getenv("SCHWAB_APP_SECRET")
    refresh_token = tokens["refresh_token"]

    credentials = f"{app_key}:{app_secret}"
    base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Basic {base64_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    try:
        response = requests.post(TOKEN_URL, headers=headers, data=payload)
        response.raise_for_status()
        new_tokens = response.json()

        if "access_token" in new_tokens:
            save_tokens(new_tokens)
            logger.info("Access token refreshed successfully.")
            return new_tokens["access_token"]
        else:
            logger.error("Failed to refresh access token.")
            logger.debug(new_tokens)
            return None
    except Exception as e:
        logger.exception(f"Error refreshing access token: {e}")
        return None


def get_access_token():
    """
    Retrieve the access token, refreshing it if necessary.
    """
    tokens = load_tokens()
    if not tokens or is_token_expired(tokens):
        logger.info("Access token expired or not found. Refreshing...")
        return refresh_access_token()
    return tokens["access_token"]


# -------------------------- Main Execution --------------------------

if __name__ == "__main__":
    try:
        logger.info(f"Looking for .env file at: {dotenv_path}")
        if not dotenv_path.exists():
            logger.error(f".env file not found: {dotenv_path}")
            sys.exit(1)

        # Debug the environment variables
        logger.info(f"SCHWAB_APP_KEY: {os.getenv('SCHWAB_APP_KEY')}")
        logger.info(f"SCHWAB_APP_SECRET: {os.getenv('SCHWAB_APP_SECRET')}")
        logger.info(f"REDIRECT_URI: {os.getenv('REDIRECT_URI')}")

        # Construct the authorization URL
        auth_url = construct_init_auth_url()

        # ✨ Skip opening the browser if a redirect URL was provided via CLI argument
        if len(sys.argv) <= 1:
            logger.info("Opening the browser for Schwab OAuth login...")
            webbrowser.open(auth_url)
        else:
            logger.info("Skipping browser open since redirect URL was provided via CLI.")

        # Determine how to get the redirected URL
        if len(sys.argv) > 1:
            redirected_url = sys.argv[1].strip()
            logger.info(f"Received redirect URL via CLI: {redirected_url}")
        else:
            # Attempt interactive input for manual usage
            try:
                redirected_url = input("Paste the full redirected URL here: ").strip()
            except EOFError:
                logger.error("EOFError: No terminal input available (no CLI arg) -> Exiting.")
                sys.exit(1)

        # Check if the redirect URL contains an authorization code
        if "code=" not in redirected_url:
            logger.error("No authorization code found in the provided URL.")
            sys.exit(1)

        auth_code = redirected_url.split("code=")[1].split("&")[0]
        auth_code = urllib.parse.unquote(auth_code)

        # Exchange the authorization code for access and refresh tokens
        app_key = os.getenv("SCHWAB_APP_KEY")
        app_secret = os.getenv("SCHWAB_APP_SECRET")
        credentials = f"{app_key}:{app_secret}"
        base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        headers = {
            "Authorization": f"Basic {base64_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": os.getenv("REDIRECT_URI"),
        }

        response = requests.post(TOKEN_URL, headers=headers, data=payload)
        response.raise_for_status()
        tokens = response.json()

        # Save the tokens
        save_tokens(tokens)
        logger.info("Authentication complete. Access and refresh tokens saved.")

    except Exception as e:
        logger.exception(f"An error occurred during the OAuth process: {e}")
