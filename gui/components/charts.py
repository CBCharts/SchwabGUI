from pathlib import Path

# Base directory for HTML files
HTML_BASE_PATH = Path(__file__).parent / "html_files"

# Categorized storage of HTML files by Index (SPX, NDX) -> Expiration -> Metric
HTML_FILES = {
    "SPX": {
        "0DTE": {
            "GEX": HTML_BASE_PATH / "spx_0dte_gex.html",
            "DEX": HTML_BASE_PATH / "spx_0dte_dex.html",
            "VEX": HTML_BASE_PATH / "spx_0dte_vex.html",
            "CEX": HTML_BASE_PATH / "spx_0dte_cex.html",
            "Volume": HTML_BASE_PATH / "spx_0dte_volume.html",
            "Open Interest": HTML_BASE_PATH / "spx_0dte_oi.html",
            "Vol/Open Interest": HTML_BASE_PATH / "spx_0dte_vol_oi.html",
        },
        "1DTE": {
            "GEX": HTML_BASE_PATH / "spx_1dte_gex.html",
            "DEX": HTML_BASE_PATH / "spx_1dte_dex.html",
            "VEX": HTML_BASE_PATH / "spx_1dte_vex.html",
            "CEX": HTML_BASE_PATH / "spx_1dte_cex.html",
            "Volume": HTML_BASE_PATH / "spx_1dte_volume.html",
            "Open Interest": HTML_BASE_PATH / "spx_1dte_oi.html",
            "Vol/Open Interest": HTML_BASE_PATH / "spx_1dte_vol_oi.html",
        },
        "EoW": {
            "GEX": HTML_BASE_PATH / "spx_eow_gex.html",
            "DEX": HTML_BASE_PATH / "spx_eow_dex.html",
            "VEX": HTML_BASE_PATH / "spx_eow_vex.html",
            "CEX": HTML_BASE_PATH / "spx_eow_cex.html",
            "Volume": HTML_BASE_PATH / "spx_eow_volume.html",
            "Open Interest": HTML_BASE_PATH / "spx_eow_oi.html",
            "Vol/Open Interest": HTML_BASE_PATH / "spx_eow_vol_oi.html",
        },
        "EoM": {
            "GEX": HTML_BASE_PATH / "spx_eom_gex.html",
            "DEX": HTML_BASE_PATH / "spx_eom_dex.html",
            "VEX": HTML_BASE_PATH / "spx_eom_vex.html",
            "CEX": HTML_BASE_PATH / "spx_eom_cex.html",
            "Volume": HTML_BASE_PATH / "spx_eom_volume.html",
            "Open Interest": HTML_BASE_PATH / "spx_eom_oi.html",
            "Vol/Open Interest": HTML_BASE_PATH / "spx_eom_vol_oi.html",
        },
    },
    "NDX": {
        "0DTE": {
            "GEX": HTML_BASE_PATH / "ndx_0dte_gex.html",
            "DEX": HTML_BASE_PATH / "ndx_0dte_dex.html",
            "VEX": HTML_BASE_PATH / "ndx_0dte_vex.html",
            "CEX": HTML_BASE_PATH / "ndx_0dte_cex.html",
            "Volume": HTML_BASE_PATH / "ndx_0dte_volume.html",
            "Open Interest": HTML_BASE_PATH / "ndx_0dte_oi.html",
            "Vol/Open Interest": HTML_BASE_PATH / "ndx_0dte_vol_oi.html",
        },
        "1DTE": {
            "GEX": HTML_BASE_PATH / "ndx_1dte_gex.html",
            "DEX": HTML_BASE_PATH / "ndx_1dte_dex.html",
            "VEX": HTML_BASE_PATH / "ndx_1dte_vex.html",
            "CEX": HTML_BASE_PATH / "ndx_1dte_cex.html",
            "Volume": HTML_BASE_PATH / "ndx_1dte_volume.html",
            "Open Interest": HTML_BASE_PATH / "ndx_1dte_oi.html",
            "Vol/Open Interest": HTML_BASE_PATH / "ndx_1dte_vol_oi.html",
        },
        "EoW": {
            "GEX": HTML_BASE_PATH / "ndx_eow_gex.html",
            "DEX": HTML_BASE_PATH / "ndx_eow_dex.html",
            "VEX": HTML_BASE_PATH / "ndx_eow_vex.html",
            "CEX": HTML_BASE_PATH / "ndx_eow_cex.html",
            "Volume": HTML_BASE_PATH / "ndx_eow_volume.html",
            "Open Interest": HTML_BASE_PATH / "ndx_eow_oi.html",
            "Vol/Open Interest": HTML_BASE_PATH / "ndx_eow_vol_oi.html",
        },
        # ✅ **No EoM for NDX**
    }
}

# Function to retrieve HTML file path
def get_html_path(index, expiration, metric):
    """Retrieve the path of an HTML file based on index (SPX/NDX), expiration type, and metric."""
    try:
        return str(HTML_FILES[index][expiration][metric])
    except KeyError:
        print(f"ERROR: No HTML file found for {index} -> {expiration} -> {metric}")
        return None
