import subprocess
import time
import sys
import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
from pathlib import Path

# ---------------------------- Configure Logger ---------------------------- #
PROJECT_ROOT = Path(__file__).resolve().parent
LOG_DIR = PROJECT_ROOT / "logs" / "wrapper"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.add(
    LOG_DIR / "wrapper_log.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# ---------------------------- Config Paths ---------------------------- #
CONFIG_DIR = PROJECT_ROOT / "configs" / "settings"
INTERVAL_CONFIG = CONFIG_DIR / "interval_config.json"
KCLEAN_CONFIG = CONFIG_DIR / "kClean_config.json"
IV_METHOD_CONFIG = CONFIG_DIR / "iv_method_config.json"

# ---------------------------- Script Paths ---------------------------- #
sequential_scripts_before_iv = [
    "data_retrieval/spx_chain.py",
    "data_retrieval/spot_prices.py",
]

iv_model_scripts_all = {
    "Brent Black Scholes": "processing/iv_models/brent_bs.py",
    "Grok": "processing/iv_models/grok.py",
    "Hybrid_one": "processing/iv_models/hybrid_one.py",
}

clean_script = "processing/exposure_calculations/clean.py"  # 🔹 This may be skipped

sequential_scripts_after_iv = [
    "processing/exposure_calculations/abso_expo.py",
    clean_script,
    "processing/exposure_calculations/ranking.py",
    "processing/exposure_calculations/ratio.py",
    "processing/exposure_calculations/historical_rankings.py",
    "processing/exposure_calculations/zeroDTE_plotly.py",
    "utils/extract_gamma_flip.py"
]


# ---------------------------- Load User Settings ---------------------------- #
def load_json_setting(file_path, default_value):
    """Loads a JSON setting file and returns the stored value or a default."""
    try:
        with open(file_path, "r") as f:
            config = json.load(f)
            return config.get("value", default_value)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning(f"⚠️ Failed to load {file_path}. Using default: {default_value}")
        return default_value

# Load settings
interval_seconds = {
    "1 minute": 60,
    "3 minutes": 180,
    "5 minutes": 300,
    "15 minutes": 900,
    "30 minutes": 1800,
    "60 minutes": 3600
}.get(load_json_setting(INTERVAL_CONFIG, "60 minutes"), 60)  # Default to 60 seconds

run_clean = load_json_setting(KCLEAN_CONFIG, "Yes") == "Yes"  # Convert to Boolean
iv_method_selected = load_json_setting(IV_METHOD_CONFIG, "All")  # IV Model selection

# ---------------------------- Helper Functions ---------------------------- #
def run_script(script_path):
    """Run a script and wait for it to complete."""
    logger.info(f"Running {script_path}...")
    try:
        subprocess.run([sys.executable, script_path], check=True)
        logger.info(f"✅ Successfully executed {script_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error running {script_path}: {e}")
    except Exception as e:
        logger.error(f"⚠️ Unexpected error while running {script_path}: {e}")

def run_sequential_scripts(scripts_list):
    """Run a list of scripts sequentially."""
    for script in scripts_list:
        script_full_path = os.path.join(os.getcwd(), script)
        run_script(script_full_path)
        time.sleep(0.1)  # Sleep for 100ms between scripts to reduce CPU load

def run_vol_oi_scripts():
    """Run vol_oi_initial.py first, then vol_oi_tracker.py, and finally vol_oi_zero_visual.py."""
    vol_oi_initial_path = os.path.join(os.getcwd(), "processing/oi_vol/vol_oi_initial.py")
    vol_oi_tracker_path = os.path.join(os.getcwd(), "processing/oi_vol/vol_oi_tracker.py")
    vol_oi_visual_path = os.path.join(os.getcwd(), "processing/oi_vol/vol_oi_zero_visual.py")
    vol_oi_tryouts_path = os.path.join(os.getcwd(), "processing/oi_vol/tryouts.py")

    logger.info("Starting vol_oi scripts sequence...")

    # Run vol_oi_initial.py and wait for completion
    run_script(vol_oi_initial_path)
    time.sleep(0.1)

    # Run vol_oi_tracker.py and wait for completion
    run_script(vol_oi_tracker_path)
    time.sleep(0.1)

    # Run vol_oi_zero_visual.py after vol_oi_tracker completes
    run_script(vol_oi_visual_path)
    time.sleep(0.1)

    # run tryouts.py after vol_oi_visual.py completes
    run_script(vol_oi_tryouts_path)
    time.sleep(0.1)

    logger.info("Completed vol_oi scripts sequence.")

def run_iv_models_parallel():
    """Run IV model scripts in parallel, starting vol_oi_zero_visual.py only after vol_oi_initial and vol_oi_tracker complete."""
    logger.info(f"Starting IV model scripts in parallel - Selected: {iv_method_selected}")

    # Run vol_oi scripts sequentially first
    run_vol_oi_scripts()

    selected_scripts = []
    if iv_method_selected == "All":
        selected_scripts = list(iv_model_scripts_all.values())  # Run all IV models
    elif iv_method_selected in iv_model_scripts_all:
        selected_scripts.append(iv_model_scripts_all[iv_method_selected])  # Run only the selected IV model

    with ThreadPoolExecutor(max_workers=len(selected_scripts)) as executor:
        futures = [executor.submit(run_script, os.path.join(os.getcwd(), script)) for script in selected_scripts]
        for future in as_completed(futures):
            future.result()

    logger.info("✅ Completed IV model scripts execution.")

# ---------------------------- Main Execution Loop ---------------------------- #
def main():
    while True:
        logger.info("🚀 Starting new execution cycle...")

        # Run initial sequential scripts
        run_sequential_scripts(sequential_scripts_before_iv)
        
        # Run IV models in parallel with vol_oi scripts
        run_iv_models_parallel()
        
        # Run post-IV scripts, optionally skipping clean.py
        scripts_after_iv = sequential_scripts_after_iv.copy()
        if not run_clean:
            scripts_after_iv.remove(clean_script)
            logger.info("⏭️ Skipping clean.py as per user selection.")

        run_sequential_scripts(scripts_after_iv)
        
        logger.info(f"⏳ All scripts executed. Sleeping for {interval_seconds} seconds...")
        time.sleep(interval_seconds)  # Sleep based on user-selected interval

if __name__ == "__main__":
    main()
