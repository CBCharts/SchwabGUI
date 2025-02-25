# single_v.py

import os
import json
import logging
from pathlib import Path
from PySide6.QtWidgets import QMenu, QToolButton, QMessageBox
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtWebEngineCore import QWebEngineSettings

class SingleVController:
    """
    Controller for the Single-View page.
    Manages drop menus for Index, IV Model, Expiration, Chart, Vol/OI, and auto-refresh interval.
    Saves user selections to JSON config files.
    Auto-refresh uses a QTimer so that the refresh process runs concurrently with the main GUI.
    Logging is directed to project_root/logs/svpage/svpage.log.
    """

    def __init__(self, ui):
        self.ui = ui
        self.last_page_type = None  # "greek_expo" or "vol_oi"

        # Setup project root and settings directory (project_root/configs/settings/sv)
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.settings_dir = self.project_root / "configs" / "settings" / "sv"
        self.settings_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging: Log file will be at project_root/logs/svpage/svpage.log
        log_dir = self.project_root / "logs" / "svpage"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "svpage.log"
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(log_file, encoding="utf-8"),
                      logging.StreamHandler()]  # Remove StreamHandler() to hide terminal output
        )
        self.logger = logging.getLogger("SingleVController")
        # Uncomment the next line to disable console output completely:
        # self.logger.handlers = [logging.FileHandler(log_file, encoding="utf-8")]

        self.logger.debug("Initializing SingleVController...")

        self.logger.debug(f"Settings directory is {self.settings_dir}")

        # Enable local file and remote URL access in the QWebEngineView (p3_wev)
        self.ui.p3_wev.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        self.ui.p3_wev.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.logger.debug("Enabled local file and remote URL access for p3_wev")

        # Setup drop menus (Index, IV Model, Expiration, Chart, Vol/OI, Interval)
        self.setup_drop_menus()

        # Connect auto-refresh interval field (lineEdit_5) to update_auto_refresh_interval
        self.ui.lineEdit_5.textChanged.connect(self.update_auto_refresh_interval)

        # Connect buttons to load HTML into p3_wev
        self.ui.pushButton_3.clicked.connect(self.load_greek_expo_html)
        self.ui.pushButton_4.clicked.connect(self.load_vol_oi_html)

        # Connect manual refresh button
        self.ui.p3_refresh_button.clicked.connect(self.manual_refresh)

        # Create a QTimer for auto-refresh; its timeout calls auto_refresh_slot
        self.refresh_timer = QTimer(self.ui.p3_wev)
        self.refresh_timer.timeout.connect(self.auto_refresh_slot)

        # Connect auto-refresh start/stop buttons
        self.ui.p3_startRe_button.clicked.connect(self.start_auto_refresh)
        self.ui.p3_endRe_button.clicked.connect(self.stop_auto_refresh)

        self.logger.debug("SingleVController initialization complete.")

    def setup_drop_menus(self):
        # Index Menu
        index_menu = self.create_index_menu()
        self.ui.toolButton_index_p3.setMenu(index_menu)
        self.ui.toolButton_index_p3.setPopupMode(QToolButton.InstantPopup)
        self.ui.toolButton_index_p3.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.logger.debug(f"Assigned index menu with {len(index_menu.actions())} items.")

        # IV Model Menu
        iv_menu = self.create_iv_model_menu()
        self.ui.toolButton_2.setMenu(iv_menu)
        self.ui.toolButton_2.setPopupMode(QToolButton.InstantPopup)
        self.ui.toolButton_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.logger.debug(f"Assigned IV model menu with {len(iv_menu.actions())} items.")

        # Expiration Menu
        exp_menu = self.create_expiration_menu()
        self.ui.toolButton_3.setMenu(exp_menu)
        self.ui.toolButton_3.setPopupMode(QToolButton.InstantPopup)
        self.ui.toolButton_3.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.logger.debug(f"Assigned expiration menu with {len(exp_menu.actions())} items.")

        # Chart Menu
        chart_menu = self.create_chart_menu()
        self.ui.toolButton_4.setMenu(chart_menu)
        self.ui.toolButton_4.setPopupMode(QToolButton.InstantPopup)
        self.ui.toolButton_4.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.logger.debug(f"Assigned chart menu with {len(chart_menu.actions())} items.")

        # Vol/OI Menu
        vol_oi_menu = self.create_vol_oi_menu()
        self.ui.toolButton_10.setMenu(vol_oi_menu)
        self.ui.toolButton_10.setPopupMode(QToolButton.InstantPopup)
        self.ui.toolButton_10.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.logger.debug(f"Assigned vol/oi menu with {len(vol_oi_menu.actions())} items.")

        # Interval Menu
        p3Interval_menu = self.create_p3Interval_menu()
        self.ui.p3_interval_drop.setMenu(p3Interval_menu)
        self.ui.p3_interval_drop.setPopupMode(QToolButton.InstantPopup)
        self.ui.p3_interval_drop.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.logger.debug(f"Assigned Single View Page Interval menu with {len(p3Interval_menu.actions())} items.")

    ### Dropdown Menu Creation Methods

    def create_index_menu(self):
        menu = QMenu(self.ui.toolButton_index_p3)
        for item in ["SPX", "NDX"]:
            action = QAction(item, menu)
            action.triggered.connect(lambda checked, i=item: self.set_index(i))
            menu.addAction(action)
        self.logger.debug(f"Index menu created with {len(menu.actions())} items.")
        return menu

    def set_index(self, selection):
        self.ui.lineEdit_index_p3.setText(selection)
        self.logger.debug(f"Index set to {selection}")
        self.save_json_setting("index_config.json", selection)
        new_exp_menu = self.create_expiration_menu()
        self.ui.toolButton_3.setMenu(new_exp_menu)
        self.logger.debug(f"Expiration menu refreshed with {len(new_exp_menu.actions())} items.")

    def create_iv_model_menu(self):
        menu = QMenu(self.ui.toolButton_2)
        for item in ["Brent Black Scholes", "Grok", "Hybrid_one"]:
            action = QAction(item, menu)
            action.triggered.connect(lambda checked, i=item: self.set_iv_model(i))
            menu.addAction(action)
        self.logger.debug(f"IV model menu created with {len(menu.actions())} items.")
        return menu

    def set_iv_model(self, selection):
        self.ui.lineEdit_2.setText(selection)
        self.logger.debug(f"IV Model set to {selection}")
        self.save_json_setting("iv_model_config.json", selection)

    def create_expiration_menu(self):
        menu = QMenu(self.ui.toolButton_3)
        expirations = ["0DTE", "1DTE", "EoW", "EoM"]
        for item in expirations:
            action = QAction(item, menu)
            action.triggered.connect(lambda checked, i=item: self.set_expiration_range(i))
            menu.addAction(action)
        self.logger.debug(f"Expiration menu created with {len(menu.actions())} items.")
        return menu

    def set_expiration_range(self, selection):
        self.ui.lineEdit_3.setText(selection)
        self.logger.debug(f"Expiration Range set to {selection}")
        self.save_json_setting("expiration_config.json", selection)

    def create_chart_menu(self):
        menu = QMenu(self.ui.toolButton_4)
        for item in ["GEX", "DEX", "VEX", "CEX"]:
            action = QAction(item, menu)
            action.triggered.connect(lambda checked, i=item: self.set_chart(i))
            menu.addAction(action)
        self.logger.debug(f"Chart menu created with {len(menu.actions())} items.")
        return menu

    def set_chart(self, selection):
        self.ui.lineEdit_4.setText(selection)
        self.logger.debug(f"Chart set to {selection}")
        self.save_json_setting("chart_config.json", selection)

    def create_vol_oi_menu(self):
        menu = QMenu(self.ui.toolButton_10)
        for item in ["Volume", "Open Interest", "Vol/Oi"]:
            action = QAction(item, menu)
            action.triggered.connect(lambda checked, i=item: self.set_vol_oi(i))
            menu.addAction(action)
        self.logger.debug(f"Vol/OI menu created with {len(menu.actions())} items.")
        return menu

    def set_vol_oi(self, selection):
        self.ui.lineEdit_10.setText(selection)
        self.logger.debug(f"Vol/OI set to {selection}")
        self.save_json_setting("vol_oi_config.json", selection)

    def create_p3Interval_menu(self):
        menu = QMenu(self.ui.p3_interval_drop)
        for item in ["1 minute", "5 minutes", "15 minutes", "30 minutes", "60 minutes"]:
            action = QAction(item, menu)
            action.triggered.connect(lambda checked, i=item: self.set_p3Interval(i))
            menu.addAction(action)
        self.logger.debug(f"Single_V Interval menu created with {len(menu.actions())} items.")
        return menu

    def set_p3Interval(self, selection):
        self.ui.lineEdit_5.setText(selection)
        self.logger.debug(f"Interval set to {selection}")
        self.save_json_setting("p3Interval_config.json", selection)

    ### Utility Methods

    def update_auto_refresh_interval(self, text):
        self.logger.debug(f"Auto-refresh interval set to {text} seconds")

    def save_json_setting(self, filename: str, user_value: str):
        filepath = self.settings_dir / filename
        data = {"value": user_value}
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self.logger.debug(f"Saved {user_value} to {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save {filename}: {e}")

    def load_json(self, filename: str) -> dict:
        filepath = self.project_root / "configs" / "htmls" / filename
        self.logger.debug(f"Attempting to load JSON file from {filepath}")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.logger.debug(f"Loaded JSON keys: {list(data.keys())[:5]}{' ...' if len(data.keys())>5 else ''}")
            return data
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load {filename}: {e}", QMessageBox.Ok)
            return {}

    ### HTML Loading Methods

    def load_greek_expo_html(self):
        """Loads HTML into p3_wev using greek_expo_paths.json (requires Index, IV Model, Expiration, Chart)."""
        index = self.ui.lineEdit_index_p3.text().strip()
        iv_model = self.ui.lineEdit_2.text().strip()
        expiration = self.ui.lineEdit_3.text().strip()
        chart = self.ui.lineEdit_4.text().strip()

        missing = []
        if not index:
            missing.append("Index")
        if not iv_model:
            missing.append("IV Model")
        if not expiration:
            missing.append("Expiration")
        if not chart:
            missing.append("Chart")
        if missing:
            QMessageBox.warning(None, "Missing Selection",
                                f"Please set the following dropmenu(s): {', '.join(missing)}",
                                QMessageBox.Ok)
            return

        key = f"{index}|{iv_model}|{expiration}|{chart}"
        self.logger.debug(f"Looking up key: {key}")

        config = self.load_json("greek_expo_paths.json")
        self.logger.debug(f"Available keys (first 10): {list(config.keys())[:10]}")
        if key not in config or not config[key]:
            QMessageBox.critical(None, "Configuration Error",
                                 f"No HTML file path set for selection: {key}",
                                 QMessageBox.Ok)
            return

        rel_path = config[key]
        self.logger.debug(f"Relative path from JSON: {rel_path}")
        abs_path = self.project_root / rel_path
        self.logger.debug(f"Absolute path resolved as: {abs_path}")

        short_err_msg = f"No file was found for {index} {iv_model} {expiration} {chart}"
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        except FileNotFoundError:
            QMessageBox.critical(None, "File Not Found", short_err_msg, QMessageBox.Ok)
            return
        except OSError:
            QMessageBox.critical(None, "Error", short_err_msg, QMessageBox.Ok)
            return

        if index == "NDX":
            base_folder = self.project_root / "visualization" / "NDX" / "plotly" / "full"
        else:
            base_folder = self.project_root / "visualization" / "plotly" / "full"
        base_url = QUrl.fromLocalFile(str(base_folder))
        self.logger.debug(f"Base URL set to: {base_url.toString()}")

        self.ui.p3_wev.setHtml(html_content, baseUrl=base_url)
        self.logger.debug(f"Loaded Greek Expo HTML from {abs_path} with base URL {base_url.toString()}")
        self.last_page_type = "greek_expo"

    def load_vol_oi_html(self):
        """Loads HTML into p3_wev using vol_oi_paths.json (requires Index, Expiration, Vol/OI)."""
        index = self.ui.lineEdit_index_p3.text().strip()
        expiration = self.ui.lineEdit_3.text().strip()
        vol_oi = self.ui.lineEdit_10.text().strip()

        missing = []
        if not index:
            missing.append("Index")
        if not expiration:
            missing.append("Expiration")
        if not vol_oi:
            missing.append("Vol/OI")
        if missing:
            QMessageBox.warning(None, "Missing Selection",
                                f"Please set the following dropmenu(s): {', '.join(missing)}",
                                QMessageBox.Ok)
            return

        key = f"{index}|{expiration}|{vol_oi}"
        self.logger.debug(f"Looking up key: {key}")
        config = self.load_json("vol_oi_paths.json")
        if key not in config or not config[key]:
            QMessageBox.critical(None, "Configuration Error",
                                 f"No HTML file path set for selection: {key}",
                                 QMessageBox.Ok)
            return

        rel_path = config[key]
        abs_path = self.project_root / rel_path
        self.ui.p3_wev.setUrl(QUrl.fromLocalFile(str(abs_path)))
        self.logger.debug(f"Loaded Vol/OI HTML from {abs_path}")
        self.last_page_type = "vol_oi"

    ### Auto-Refresh Methods

    def start_auto_refresh(self):
        """Starts auto-refresh using the interval specified in lineEdit_5."""
        interval_str = self.ui.lineEdit_5.text().strip()
        if not interval_str:
            QMessageBox.warning(None, "No Interval", "Please select an interval first.", QMessageBox.Ok)
            return

        interval_map = {
            "1 minute": 60_000,
            "5 minutes": 300_000,
            "15 minutes": 900_000,
            "30 minutes": 1_800_000,
            "60 minutes": 3_600_000
        }
        if interval_str not in interval_map:
            QMessageBox.warning(None, "Invalid Interval", f"Unrecognized interval: {interval_str}", QMessageBox.Ok)
            return

        interval_ms = interval_map[interval_str]
        self.logger.debug(f"Starting auto-refresh timer for {interval_str} ({interval_ms} ms)")
        self.refresh_timer.start(interval_ms)

    def stop_auto_refresh(self):
        """Stops the auto-refresh timer."""
        if self.refresh_timer.isActive():
            self.refresh_timer.stop()
            self.logger.debug("Auto-refresh timer stopped.")
        else:
            self.logger.debug("Auto-refresh timer was not running.")

    def auto_refresh_slot(self):
        """
        Called by the QTimer to auto-refresh the current HTML in p3_wev.
        Uses self.last_page_type to determine which function to call.
        """
        if self.last_page_type == "greek_expo":
            self.logger.debug("Auto-refresh: reloading Greek Expo HTML")
            self.load_greek_expo_html()
        elif self.last_page_type == "vol_oi":
            self.logger.debug("Auto-refresh: reloading Vol/OI HTML")
            self.load_vol_oi_html()
        else:
            self.logger.debug("Auto-refresh: No valid page type set, so not reloading.")

    def manual_refresh(self):
        """
        Manually refreshes the currently loaded HTML in p3_wev without resetting the auto-refresh timer.
        """
        if self.last_page_type == "greek_expo":
            self.logger.debug("Manual refresh: reloading Greek Expo HTML")
            self.load_greek_expo_html()
        elif self.last_page_type == "vol_oi":
            self.logger.debug("Manual refresh: reloading Vol/OI HTML")
            self.load_vol_oi_html()
        else:
            self.logger.debug("Manual refresh: No valid page type set.")
