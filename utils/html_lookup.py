# html_lookup.py

import json
from pathlib import Path

def load_json_file(filepath: Path) -> dict:
    """
    Loads a JSON file and returns its contents as a dictionary.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load {filepath}: {e}")
        return {}

def load_html_configurations():
    """
    Loads the Greek expo and vol/oi configuration dictionaries from:
      project_root/configs/htmls/
    Returns a tuple: (greek_expo_config, vol_oi_config)
    """
    # Assuming this script is placed in a subdirectory of the project root.
    base_dir = Path(__file__).resolve().parent.parent / "configs" / "htmls"
    greek_expo_path = base_dir / "greek_expo_paths.json"
    vol_oi_path = base_dir / "vol_oi_paths.json"

    greek_expo = load_json_file(greek_expo_path)
    vol_oi = load_json_file(vol_oi_path)

    return greek_expo, vol_oi

def get_html_path(config: dict, key: str) -> str:
    """
    Given a configuration dictionary and a key, returns the corresponding HTML file path.
    If the key is not found, returns None.
    """
    return config.get(key, None)

# Example usage:
if __name__ == "__main__":
    greek_expo_config, vol_oi_config = load_html_configurations()
    
    # Example key lookups:
    key1 = "SPX|Brent Black Scholes|0DTE|GEX"
    key2 = "SPX|0DTE|Volume"
    
    path1 = get_html_path(greek_expo_config, key1)
    path2 = get_html_path(vol_oi_config, key2)
    
    print("Lookup from Greek Expo Config:")
    print(f"{key1} -> {path1}")
    print("\nLookup from Vol/OI Config:")
    print(f"{key2} -> {path2}")
