import json
import logging
from pathlib import Path

from PySide6.QtCore import Qt, QUrl, QPoint
from PySide6.QtWidgets import QMenu, QToolButton, QMessageBox, QButtonGroup
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from utils.html_lookup import load_html_configurations, get_html_path


class OWController:
    """
    Controller for page_5 (OW Page) in the stacked widget.
    
    Manages UI components on the OW page, which is accessed via the "OW_button"
    in main_window.py. This controller sets up drop-down menus on tool buttons,
    configures QWebEngineViews for remote URL access, and handles push button events.
    
    It groups three sets of checkable push buttons:
      • "Index" (pushButton_19 and pushButton_20) saved to p5_index.json.
      • "Expiration" (pushButton_21 to pushButton_24) saved to p5_expiration.json.
      • "IV Method" (pushButton_25 to pushButton_27) saved to p5_iv.json.
      
    When the user clicks p5_manual_button, the controller reads these JSONs,
    constructs the appropriate lookup keys, and then loads the corresponding
    HTML charts into the 7 QWebEngineViews as follows:
    
      Greek charts (keys with 4 parts):
        - p5_gex_web -> "{index}|{iv_method}|{expiration}|GEX"
        - p5_dex_web -> "{index}|{iv_method}|{expiration}|DEX"
        - p5_cex_web -> "{index}|{iv_method}|{expiration}|CEX"
        - p5_vex_web -> "{index}|{iv_method}|{expiration}|VEX"
        
      Vol/OI charts (keys with 3 parts):
        - p5_Oi_web    -> "{index}|{expiration}|Open Interest"
        - p5_Vol_web   -> "{index}|{expiration}|Volume"
        - p5_VolOi_web -> "{index}|{expiration}|Vol/Oi"
    """

    def __init__(self, ui):
        self.ui = ui

        # Determine project root (assumed: project_root/gui/controllers/OW_ctrl.py)
        self.project_root = Path(__file__).resolve().parent.parent.parent

        # Setup logging (logs to project_root/logs/owpage/owpage.log)
        log_dir = self.project_root / "logs" / "owpage"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "owpage.log"
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(log_file, encoding="utf-8")]
        )
        self.logger = logging.getLogger("OWController")
        self.logger.debug("Initializing OWController for page_5...")

        # Enable remote URL access for the QWebEngineView if a generic one exists.
        # (We also set attributes later on the Greek views individually.)
        if hasattr(self.ui, "ow_wev") and isinstance(self.ui.ow_wev, QWebEngineView):
            settings = self.ui.ow_wev.settings()
            settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
            self.logger.debug("Enabled remote URL access for ow_wev.")

        # Create drop-down menu for the interval toolbutton
        self.setup_interval_toolbutton_menu()

        # Setup exclusive button groups for Index, Expiration, and IV Method
        self.setup_exclusive_button_groups()

        # Connect manual update button to trigger chart update
        if hasattr(self.ui, "p5_manual_button"):
            self.ui.p5_manual_button.clicked.connect(self.on_manual_button_clicked)
            self.logger.debug("Connected p5_manual_button to update charts function.")
        else:
            self.logger.warning("p5_manual_button not found in UI; manual update not connected.")

        # Connect any additional UI components for the OW page (if needed)
        if hasattr(self.ui, "pushButton_ow"):
            self.ui.pushButton_ow.clicked.connect(self.on_push_button_clicked)
            self.logger.debug("Connected pushButton_ow to click handler.")
        else:
            self.logger.warning("pushButton_ow not found in UI; push button action not connected.")

        self.logger.debug("OWController initialization complete.")

    def setup_interval_toolbutton_menu(self):
        """
        Creates and assigns a QMenu to p5_interval_toolbutton.
        Each action triggers on_interval_selected with the chosen interval.
        """
        if hasattr(self.ui, "p5_interval_toolbutton"):
            menu = QMenu(self.ui.p5_interval_toolbutton)
            intervals = [
                "1 minute",
                "3 minutes",
                "5 minutes",
                "10 minutes",
                "15 minutes",
                "30 minutes",
                "1 hour",
            ]
            for interval in intervals:
                action = QAction(interval, menu)
                action.triggered.connect(lambda checked, i=interval: self.on_interval_selected(i))
                menu.addAction(action)
            self.ui.p5_interval_toolbutton.setMenu(menu)
            self.ui.p5_interval_toolbutton.setPopupMode(QToolButton.InstantPopup)
            self.ui.p5_interval_toolbutton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.logger.debug(
                f"Initialized drop-down menu for p5_interval_toolbutton with {len(menu.actions())} options."
            )
        else:
            self.logger.warning("p5_interval_toolbutton not found in UI; drop-down menu not set up.")

    def setup_exclusive_button_groups(self):
        """
        Sets up three exclusive button groups for Index, Expiration, and IV Method.
        When a button is clicked, its value is saved to the corresponding JSON file.
        (Chart updates are triggered manually.)
        """
        from PySide6.QtWidgets import QButtonGroup

        # Create Index group (pushButton_19 and pushButton_20)
        self.index_group = QButtonGroup()
        self.index_group.setExclusive(True)
        if hasattr(self.ui, "pushButton_19"):
            self.ui.pushButton_19.setCheckable(True)
            self.index_group.addButton(self.ui.pushButton_19)
        if hasattr(self.ui, "pushButton_20"):
            self.ui.pushButton_20.setCheckable(True)
            self.index_group.addButton(self.ui.pushButton_20)
        self.index_group.buttonClicked.connect(self.on_index_selected)
        self.logger.debug("Index button group set up.")

        # Create Expiration group (pushButton_21 to pushButton_24)
        self.expiration_group = QButtonGroup()
        self.expiration_group.setExclusive(True)
        if hasattr(self.ui, "pushButton_21"):
            self.ui.pushButton_21.setCheckable(True)
            self.expiration_group.addButton(self.ui.pushButton_21)
        if hasattr(self.ui, "pushButton_22"):
            self.ui.pushButton_22.setCheckable(True)
            self.expiration_group.addButton(self.ui.pushButton_22)
        if hasattr(self.ui, "pushButton_23"):
            self.ui.pushButton_23.setCheckable(True)
            self.expiration_group.addButton(self.ui.pushButton_23)
        if hasattr(self.ui, "pushButton_24"):
            self.ui.pushButton_24.setCheckable(True)
            self.expiration_group.addButton(self.ui.pushButton_24)
        self.expiration_group.buttonClicked.connect(self.on_expiration_selected)
        self.logger.debug("Expiration button group set up.")

        # Create IV Method group (pushButton_25 to pushButton_27)
        self.iv_group = QButtonGroup()
        self.iv_group.setExclusive(True)
        if hasattr(self.ui, "pushButton_25"):
            self.ui.pushButton_25.setCheckable(True)
            self.iv_group.addButton(self.ui.pushButton_25)
        if hasattr(self.ui, "pushButton_26"):
            self.ui.pushButton_26.setCheckable(True)
            self.iv_group.addButton(self.ui.pushButton_26)
        if hasattr(self.ui, "pushButton_27"):
            self.ui.pushButton_27.setCheckable(True)
            self.iv_group.addButton(self.ui.pushButton_27)
        self.iv_group.buttonClicked.connect(self.on_iv_selected)
        self.logger.debug("IV Method button group set up.")

    def on_interval_selected(self, interval):
        """
        Called when the user selects an interval from the p5_interval_toolbutton menu.
        Saves the selected interval to "p5_interval.json" in the ow settings directory.
        """
        self.logger.debug(f"Interval selected on OW page: {interval}")
        self.save_setting("p5_interval.json", interval)

    def on_index_selected(self, button):
        """
        Called when a button in the Index group is clicked.
        Saves the selected Index value to "p5_index.json".
        """
        value = button.text()
        self.logger.debug(f"Index selected: {value}")
        self.save_setting("p5_index.json", value)

    def on_expiration_selected(self, button):
        """
        Called when a button in the Expiration group is clicked.
        Saves the selected Expiration value to "p5_expiration.json".
        """
        value = button.text()
        self.logger.debug(f"Expiration selected: {value}")
        self.save_setting("p5_expiration.json", value)

    def on_iv_selected(self, button):
        """
        Called when a button in the IV Method group is clicked.
        Saves the selected IV Method value to "p5_iv.json".
        """
        value = button.text()
        self.logger.debug(f"IV Method selected: {value}")
        self.save_setting("p5_iv.json", value)

    def on_manual_button_clicked(self):
        """
        Handler for p5_manual_button click.
        Reads the saved settings, constructs the lookup keys, and loads the charts
        into the QWebEngineViews.
        """
        self.logger.debug("Manual update button clicked; updating charts.")
        self.update_charts()

    def update_charts(self):
        """
        Uses the saved settings (Index, Expiration, IV Method) to construct keys
        and look up the correct HTML file paths from the configuration dictionaries.
        Loads the charts into the 7 QWebEngineViews on the OW page.
        
        For the Greek charts, the keys are constructed as:
           "{index}|{iv_method}|{expiration}|{option}"
        where {option} is one of "GEX", "DEX", "CEX", "VEX", and they load into:
           - p5_gex_web, p5_dex_web, p5_cex_web, p5_vex_web respectively.
        
        For the Vol/OI charts, the keys are constructed as:
           "{index}|{expiration}|{option}"
        where {option} is one of "Open Interest", "Volume", "Vol/Oi", and they load into:
           - p5_Oi_web, p5_Vol_web, p5_VolOi_web respectively.
        """
        index = self.load_setting("p5_index.json")
        expiration = self.load_setting("p5_expiration.json")
        iv_method = self.load_setting("p5_iv.json")
        self.logger.debug(f"Loaded settings - Index: {index}, Expiration: {expiration}, IV Method: {iv_method}")
        if not index or not expiration or not iv_method:
            self.logger.error("One or more required settings are missing; cannot update charts.")
            return

        # Load the HTML configurations from the lookup utility
        greek_config, vol_oi_config = load_html_configurations()

        # Update Greek charts
        greek_options = {
            "GEX": "p5_gex_web",
            "DEX": "p5_dex_web",
            "CEX": "p5_cex_web",
            "VEX": "p5_vex_web"
        }
        for option, view_name in greek_options.items():
            key = f"{index}|{iv_method}|{expiration}|{option}"
            self.logger.debug(f"Constructed Greek key for {option}: {key}")
            path = get_html_path(greek_config, key)
            self.logger.debug(f"Returned Greek path for key '{key}': {path}")
            if path and path.strip():
                abs_path = self.project_root / path
                self.logger.debug(f"Absolute path for Greek {option}: {abs_path}")
                if not abs_path.exists():
                    self.logger.error(f"File not found: {abs_path}")
                # Get the QWebEngineView and set necessary attributes for remote content
                if hasattr(self.ui, view_name) and isinstance(getattr(self.ui, view_name), QWebEngineView):
                    qweb = getattr(self.ui, view_name)
                    qweb.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
                    qweb.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
                    # Connect a loadFinished signal to log when loading completes.
                    qweb.loadFinished.connect(lambda ok, vn=view_name: self.logger.debug(f"{vn} finished loading: {ok}"))
                    qweb.setUrl(QUrl.fromLocalFile(str(abs_path)))
                    self.logger.debug(f"Loaded Greek chart '{option}' into {view_name}")
                else:
                    self.logger.warning(f"{view_name} QWebEngineView not found in UI.")
            else:
                self.logger.error(f"No Greek chart path found for key: {key}")

        # Update Vol/OI charts
        vol_options = {
            "Open Interest": "p5_Oi_web",
            "Volume": "p5_Vol_web",
            "Vol/Oi": "p5_VolOi_web"
        }
        for option, view_name in vol_options.items():
            key = f"{index}|{expiration}|{option}"
            self.logger.debug(f"Constructed Vol/OI key for {option}: {key}")
            path = get_html_path(vol_oi_config, key)
            self.logger.debug(f"Returned Vol/OI path for key '{key}': {path}")
            if path and path.strip():
                abs_path = self.project_root / path
                self.logger.debug(f"Absolute path for Vol/OI {option}: {abs_path}")
                if not abs_path.exists():
                    self.logger.error(f"File not found: {abs_path}")
                if hasattr(self.ui, view_name) and isinstance(getattr(self.ui, view_name), QWebEngineView):
                    qweb = getattr(self.ui, view_name)
                    qweb.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
                    qweb.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
                    qweb.loadFinished.connect(lambda ok, vn=view_name: self.logger.debug(f"{vn} finished loading: {ok}"))
                    qweb.setUrl(QUrl.fromLocalFile(str(abs_path)))
                    self.logger.debug(f"Loaded Vol/OI chart '{option}' into {view_name}")
                else:
                    self.logger.warning(f"{view_name} QWebEngineView not found in UI.")
            else:
                self.logger.error(f"No Vol/OI chart path found for key: {key}")

    def on_push_button_clicked(self):
        """
        Handler for the push button click event on the OW page.
        """
        self.logger.debug("pushButton_ow clicked on OW page.")
        QMessageBox.information(self.ui.page_5, "OW Page", "Button clicked on the OW page!")

    def save_setting(self, filename, value):
        """
        Saves the given value to a JSON file in the ow settings directory.
        """
        settings_dir = self.project_root / "configs" / "settings" / "ow"
        settings_dir.mkdir(parents=True, exist_ok=True)
        filepath = settings_dir / filename
        data = {"value": value}
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self.logger.debug(f"Saved setting '{value}' to {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save setting to {filepath}: {e}")

    def load_setting(self, filename):
        """
        Loads the value from the given JSON file in the ow settings directory.
        Returns the value if found, or None otherwise.
        """
        settings_dir = self.project_root / "configs" / "settings" / "ow"
        filepath = settings_dir / filename
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("value")
        except Exception as e:
            self.logger.error(f"Failed to load setting from {filepath}: {e}")
            return None


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

    app = QApplication(sys.argv)
    main_win = QMainWindow()
    # Create a dummy widget with the required attributes:
    test_widget = QWidget()
    layout = QVBoxLayout(test_widget)

    # Dummy p5_interval_toolbutton:
    test_widget.p5_interval_toolbutton = QToolButton()
    # Dummy manual update button:
    test_widget.p5_manual_button = QToolButton()
    test_widget.p5_manual_button.setText("Update Charts")
    # Dummy buttons for Index
    test_widget.pushButton_19 = QToolButton()
    test_widget.pushButton_19.setText("SPX")
    test_widget.pushButton_20 = QToolButton()
    test_widget.pushButton_20.setText("NDX")
    # Dummy buttons for Expiration
    test_widget.pushButton_21 = QToolButton()
    test_widget.pushButton_21.setText("0DTE")
    test_widget.pushButton_22 = QToolButton()
    test_widget.pushButton_22.setText("1DTE")
    test_widget.pushButton_23 = QToolButton()
    test_widget.pushButton_23.setText("EoW")
    test_widget.pushButton_24 = QToolButton()
    test_widget.pushButton_24.setText("EoM")
    # Dummy buttons for IV Method
    test_widget.pushButton_25 = QToolButton()
    test_widget.pushButton_25.setText("Brent Black Scholes")
    test_widget.pushButton_26 = QToolButton()
    test_widget.pushButton_26.setText("Grok")
    test_widget.pushButton_27 = QToolButton()
    test_widget.pushButton_27.setText("Hybrid_one")
    # Dummy QWebEngineViews for charts:
    test_widget.p5_gex_web = QWebEngineView()
    test_widget.p5_dex_web = QWebEngineView()
    test_widget.p5_cex_web = QWebEngineView()
    test_widget.p5_vex_web = QWebEngineView()
    test_widget.p5_Oi_web = QWebEngineView()
    test_widget.p5_Vol_web = QWebEngineView()
    test_widget.p5_VolOi_web = QWebEngineView()
    # Dummy page_5 for parent widget (used in message boxes)
    test_widget.page_5 = test_widget

    # Add widgets to the layout
    layout.addWidget(test_widget.p5_interval_toolbutton)
    layout.addWidget(test_widget.p5_manual_button)
    layout.addWidget(test_widget.pushButton_19)
    layout.addWidget(test_widget.pushButton_20)
    layout.addWidget(test_widget.pushButton_21)
    layout.addWidget(test_widget.pushButton_22)
    layout.addWidget(test_widget.pushButton_23)
    layout.addWidget(test_widget.pushButton_24)
    layout.addWidget(test_widget.pushButton_25)
    layout.addWidget(test_widget.pushButton_26)
    layout.addWidget(test_widget.pushButton_27)
    layout.addWidget(test_widget.p5_gex_web)
    layout.addWidget(test_widget.p5_dex_web)
    layout.addWidget(test_widget.p5_cex_web)
    layout.addWidget(test_widget.p5_vex_web)
    layout.addWidget(test_widget.p5_Oi_web)
    layout.addWidget(test_widget.p5_Vol_web)
    layout.addWidget(test_widget.p5_VolOi_web)

    main_win.setCentralWidget(test_widget)
    ow_ctrl = OWController(test_widget)
    main_win.show()
    sys.exit(app.exec())
