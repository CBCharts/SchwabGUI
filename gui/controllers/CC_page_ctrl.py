import os
import json
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from PySide6.QtWidgets import (
    QWidget, QMessageBox, QToolButton, QMenu
)
from PySide6.QtGui import QAction
from functools import partial

class CCPageController(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

        # Define paths
        self.project_root = Path(__file__).resolve().parent.parent.parent  # Moves up to 'project' folder
        self.env_path = self.project_root / ".env"
        self.schwab_api_path = self.project_root / "data_retrieval" / "schwab_api.py"

        # Wrapper script paths
        self.wrapper_script = self.project_root / "wrapper.py"
        self.ndx_wrapper_script = self.project_root / "ndx_wrapper.py"

        # We will store each drop menu’s JSON file in:  PROJECT_ROOT / "configs" / "settings"
        self.settings_dir = self.project_root / "configs" / "settings"
        self.settings_dir.mkdir(parents=True, exist_ok=True)

        # Config file paths
        self.interval_config = self.settings_dir / "interval_config.json"
        self.index_config = self.settings_dir / "index_config.json"
        self.expiration_config = self.settings_dir / "strikerange_config.json"
        self.iv_method_config = self.settings_dir / "iv_method_config.json"
        self.kclean_config = self.settings_dir / "kClean_config.json"

        # Load .env
        load_dotenv(self.env_path)

        # Process reference for Schwab API script
        self.process = None
        # Process reference for the continuously running wrapper script
        self.wrapper_process = None

        # Setup dropdown menus
        self.setup_interval_menu()
        self.setup_index_menu()
        self.setup_expiration_menu()
        self.setup_iv_menu()
        self.setup_clean_menu()
        self.setup_clearHist_menu()

        # Connect Schwab API buttons
        self.ui.p2_auth_button.clicked.connect(self.authenticate_schwab)
        self.ui.p2_getToken_button.clicked.connect(self.submit_redirect_url)
        # Connect the Start and End buttons to their functionality
        self.ui.p2_startWrap_button.clicked.connect(self.start_wrapper)
        self.ui.p2_endWrap_button.clicked.connect(self.end_wrapper)

    # ---------------------- MENUS: REFRESH DATA INTERVALS ---------------------- #
    def setup_interval_menu(self):
        """
        p2_interval_toolbutton / p2_interval_lineedit
        Options: 1 minute, 3 minutes, 5 minutes, 15 minutes, 30 minutes, 60 minutes
        """
        menu = QMenu(self.ui.p2_interval_toolbutton)
        intervals = ["1 minute", "3 minutes", "5 minutes", "15 minutes", "30 minutes", "60 minutes"]
        for interval_text in intervals:
            action = QAction(interval_text, menu)
            action.triggered.connect(lambda checked, val=interval_text: self.set_interval(val))
            menu.addAction(action)

        self.ui.p2_interval_toolbutton.setMenu(menu)
        self.ui.p2_interval_toolbutton.setPopupMode(QToolButton.MenuButtonPopup)

    def set_interval(self, val: str):
        """Update lineedit & save immediately to interval_config.json"""
        self.ui.p2_interval_lineedit.setText(val)
        self.save_json_setting("interval_config.json", val)

    # ---------------------- MENUS: INDEX ---------------------- #
    def setup_index_menu(self):
        """
        p2_index_toolbutton / p2_index_lineedit
        Options: SPX, NDX, Both
        """
        menu = QMenu(self.ui.p2_index_toolbutton)
        indexes = ["SPX", "NDX", "Both"]  # <-- Added "Both"
        for idx_text in indexes:
            action = QAction(idx_text, menu)
            action.triggered.connect(lambda checked, val=idx_text: self.set_index(val))
            menu.addAction(action)

        self.ui.p2_index_toolbutton.setMenu(menu)
        self.ui.p2_index_toolbutton.setPopupMode(QToolButton.MenuButtonPopup)

    def set_index(self, val: str):
        """Update lineedit & save to index_config.json"""
        self.ui.p2_index_lineedit.setText(val)
        self.save_json_setting("index_config.json", val)

    # ---------------------- MENUS: EXPIRATION RANGE ---------------------- #
    def setup_expiration_menu(self):
        """
        p2_exp_toolbutton / p2_exp_lineedit
        Options: 350, 700, 500, 1050, 1400
        """
        menu = QMenu(self.ui.p2_exp_toolbutton)
        expirations = ["350", "500", "700", "1050", "1400"]
        for exp_text in expirations:
            action = QAction(exp_text, menu)
            action.triggered.connect(lambda checked, val=exp_text: self.set_expiration(val))
            menu.addAction(action)

        self.ui.p2_exp_toolbutton.setMenu(menu)
        self.ui.p2_exp_toolbutton.setPopupMode(QToolButton.MenuButtonPopup)

    def set_expiration(self, val: str):
        """Update lineedit & save to expiration_config.json"""
        self.ui.p2_exp_lineedit.setText(val)
        self.save_json_setting("strikerange_config.json", val)

    # ---------------------- MENUS: IV Method ---------------------- #
    def setup_iv_menu(self):
        """
        IV Method -> p2_iv_toolbutton / p2_iv_lineedit
        Options: All, Hybrid_one, Brent Black Scholes, Grok
        """
        menu = QMenu(self.ui.p2_iv_toolbutton)
        iv_methods = ["All", "Hybrid_one", "Brent Black Scholes", "Grok"]
        for method_text in iv_methods:
            action = QAction(method_text, menu)
            action.triggered.connect(lambda checked, val=method_text: self.set_iv_method(val))
            menu.addAction(action)

        self.ui.p2_iv_toolbutton.setMenu(menu)
        self.ui.p2_iv_toolbutton.setPopupMode(QToolButton.MenuButtonPopup)

    def set_iv_method(self, val: str):
        """
        Update lineedit & save to iv_method_config.json
        """
        self.ui.p2_iv_lineedit.setText(val)
        self.save_json_setting("iv_method_config.json", val)

    # ---------------------- MENUS: Clean Keep ---------------------- #
    def setup_clean_menu(self):
        """
        Clean Keep -> p2_kClean_toolbutton / p2_kClean_lineedit
        Options: Yes, No
        """
        menu = QMenu(self.ui.p2_kClean_toolbutton)
        clean_keeps = ["Yes", "No"]
        for clean_text in clean_keeps:
            action = QAction(clean_text, menu)
            action.triggered.connect(lambda checked, val=clean_text: self.set_clean_keep(val))
            menu.addAction(action)

        self.ui.p2_kClean_toolbutton.setMenu(menu)
        self.ui.p2_kClean_toolbutton.setPopupMode(QToolButton.MenuButtonPopup)

    def set_clean_keep(self, val: str):
        """
        Update lineedit & save to kClean_config.json
        """
        self.ui.p2_kClean_lineedit.setText(val)
        self.save_json_setting("kClean_config.json", val)

    ## ---------------------- MENUS: Clear Hist ---------------------- #
    def setup_clearHist_menu(self):
        """
        Setup the dropdown menu for the clear history tool button.
        """
        menu = QMenu(self.ui.clearHist_toolbutton)
        clear_hist_options = ["Keep 2 Days", "Keep 1 Week", "Keep 1 Month"]

        for cHist_text in clear_hist_options:
            action = QAction(cHist_text, menu)
            action.triggered.connect(partial(self.confirm_clear_hist, cHist_text))
            menu.addAction(action)

        self.ui.clearHist_toolbutton.setMenu(menu)
        self.ui.clearHist_toolbutton.setPopupMode(QToolButton.InstantPopup)

    def confirm_clear_hist(self, val: str):
        """
        Show a confirmation popup before executing the cleanup script.
        """
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Confirm Clear History")
        msg_box.setText(f"Are you sure you want to set history retention to '{val}'?\n\nThis action cannot be undone.")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.set_clear_hist(val)  # Update the UI setting
            self.run_clear_hist_script(val)  # Run cleanup script

    def run_clear_hist_script(self, retention_option: str):
        """
        Executes clear_hist.py with the user-selected retention option.
        """
        script_path = self.project_root / "utils" / "clear_hist.py"

        try:
            subprocess.run(["python", str(script_path), retention_option], check=True)
            QMessageBox.information(self, "Success", "Old historical CSV files cleared successfully.")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to clear historical CSV files:\n{e}")

    def set_clear_hist(self, val: str):
        """
        Update the setting and save to cHist_config.json.
        """
        self.save_json_setting("cHist_config.json", val)

    # ---------------------- SAVE INDIVIDUAL JSON ---------------------- #
    def save_json_setting(self, filename: str, user_value: str):
        """
        Save a single setting to PROJECT_ROOT/configs/settings/<filename>.
        The JSON structure is:
          { "value": "...user_value..." }
        """
        filepath = self.settings_dir / filename
        data = {"value": user_value}

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"DEBUG: Saved {user_value} to {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save {filename}: {e}")

    # ------------------- SCHWAB API AUTH FLOW ------------------- #
    def authenticate_schwab(self):
        """Retrieve user input, save credentials to .env, and run Schwab API authentication."""
        app_key = self.ui.lineEdit_AppKey.text().strip()
        secret_key = self.ui.lineEdit_SecretKey.text().strip()
        redirect_uri = self.ui.lineEdit_Uri.text().strip()

        if not app_key or not secret_key or not redirect_uri:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields before authenticating.")
            return

        # Save credentials to .env
        try:
            with open(self.env_path, "w", encoding="utf-8") as env_file:
                env_file.write(f"SCHWAB_APP_KEY={app_key}\n")
                env_file.write(f"SCHWAB_APP_SECRET={secret_key}\n")
                env_file.write(f"REDIRECT_URI={redirect_uri}\n")
            print(f"DEBUG: Credentials saved to {self.env_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save credentials: {e}")
            return

        # Ensure Schwab API script exists
        if not self.schwab_api_path.exists():
            QMessageBox.critical(self, "Authentication Failed", 
                                 f"Error: Schwab API script not found at:\n{self.schwab_api_path}")
            return

        # Launch schwab_api.py
        try:
            self.process = subprocess.Popen(
                ["python", str(self.schwab_api_path)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True
            )
            QMessageBox.information(self, "Authentication Initiated", 
                                    "Browser will open. Complete login and paste the redirect URL.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to run Schwab API script: {e}")
            print(f"DEBUG: General error running schwab_api.py: {e}")

    def submit_redirect_url(self):
        """Simulate user pasting redirect URL for schwab_api.py."""
        redirect_url = self.ui.lineEdit_RedirectUrl.text().strip()
        if not redirect_url:
            QMessageBox.warning(self, "Input Error", "Please paste the redirected URL before proceeding.")
            return

        # Ensure script exists
        if not self.schwab_api_path.exists():
            QMessageBox.critical(self, "Error", f"Schwab API script not found at:\n{self.schwab_api_path}")
            return

        try:
            # Pass the redirect URL as an argument
            result = subprocess.run(
                ["python", str(self.schwab_api_path), redirect_url],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                QMessageBox.information(self, "Success", "Token retrieval successful.")
            else:
                QMessageBox.critical(self, "Error", f"Authentication Failed: {result.stderr}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send redirect URL: {e}")

    # ---------------------- START WRAPPER SCRIPT ---------------------- #
    def start_wrapper(self):
        """
        Validate that all required drop menus/line edits are populated and start the appropriate
        wrapper script (wrapper.py for SPX, ndx_wrapper.py for NDX, or both sequentially).
        """
        # Validate required fields
        required_fields = {
            "Interval": self.ui.p2_interval_lineedit.text().strip(),
            "Index": self.ui.p2_index_lineedit.text().strip(),
            "Expiration": self.ui.p2_exp_lineedit.text().strip(),
            "IV Method": self.ui.p2_iv_lineedit.text().strip(),
            "Clean Keep": self.ui.p2_kClean_lineedit.text().strip()
        }

        missing = [key for key, value in required_fields.items() if not value]
        if missing:
            QMessageBox.warning(self, "Missing Configuration", 
                                f"Please populate the following fields: {', '.join(missing)}")
            return

        index_value = self.ui.p2_index_lineedit.text().strip().upper()

        if index_value == "SPX":
            # Ensure wrapper.py exists
            if not self.wrapper_script.exists():
                QMessageBox.critical(self, "Error", f"Wrapper script not found at:\n{self.wrapper_script}")
                return
            try:
                self.wrapper_process = subprocess.Popen(["python", str(self.wrapper_script)])
                QMessageBox.information(self, "Wrapper Started", f"Started {self.wrapper_script.name} successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to start wrapper script:\n{e}")
                return

        elif index_value == "NDX":
            # Ensure ndx_wrapper.py exists
            if not self.ndx_wrapper_script.exists():
                QMessageBox.critical(self, "Error", f"Wrapper script not found at:\n{self.ndx_wrapper_script}")
                return
            try:
                self.wrapper_process = subprocess.Popen(["python", str(self.ndx_wrapper_script)])
                QMessageBox.information(self, "Wrapper Started", f"Started {self.ndx_wrapper_script.name} successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to start wrapper script:\n{e}")
                return

        elif index_value == "BOTH":
            # Ensure both scripts exist
            if not self.wrapper_script.exists() or not self.ndx_wrapper_script.exists():
                QMessageBox.critical(self, "Error", "One or both wrapper scripts were not found.")
                return
            try:
                # Start SPX first...
                self.wrapper_process_spx = subprocess.Popen(["python", str(self.wrapper_script)])
                # ...then start NDX
                self.wrapper_process_ndx = subprocess.Popen(["python", str(self.ndx_wrapper_script)])
                QMessageBox.information(self, "Wrapper Started", 
                                        f"Started both {self.wrapper_script.name} and {self.ndx_wrapper_script.name} successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to start wrapper scripts:\n{e}")
                return

        else:
            QMessageBox.critical(self, "Error", "Invalid index selection.")
            return

    # ---------------------- END WRAPPER SCRIPT ---------------------- #
    def end_wrapper(self):
        """
        Terminates the running wrapper process(es) if they exist.
        If multiple processes (for BOTH) are running, all will be terminated.
        """
        terminated = False

        # Terminate the single process case (SPX or NDX)
        if hasattr(self, 'wrapper_process') and self.wrapper_process is not None and self.wrapper_process.poll() is None:
            try:
                self.wrapper_process.terminate()
                self.wrapper_process = None
                terminated = True
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to terminate wrapper:\n{e}")
                return

        # Terminate the BOTH case processes if they exist
        if hasattr(self, 'wrapper_process_spx') and self.wrapper_process_spx is not None and self.wrapper_process_spx.poll() is None:
            try:
                self.wrapper_process_spx.terminate()
                self.wrapper_process_spx = None
                terminated = True
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to terminate SPX wrapper:\n{e}")
                return

        if hasattr(self, 'wrapper_process_ndx') and self.wrapper_process_ndx is not None and self.wrapper_process_ndx.poll() is None:
            try:
                self.wrapper_process_ndx.terminate()
                self.wrapper_process_ndx = None
                terminated = True
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to terminate NDX wrapper:\n{e}")
                return

        if terminated:
            QMessageBox.information(self, "Terminating Wrapper", "Terminating Wrapper(s)")
        else:
            QMessageBox.warning(self, "Error 420", "There is currently no Wrapper running")