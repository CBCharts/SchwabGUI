import json
import logging
from pathlib import Path

from PySide6.QtCore import Qt, QUrl, QPoint
from PySide6.QtWidgets import QMenu, QToolButton, QMessageBox
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings


class TVController:
    """
    Controller for page_4 (Tri-View) in the stacked widget.
    Manages three QToolButtons (p4_v1_drop, p4_v2_drop, p4_v3_drop)
    and three QWebEngineViews (p4_wev1, p4_wev2, p4_wev3).

    Each QToolButton shows a nested menu with the following structure:
      • Index (SPX or NDX) →
           Expiration (0DTE, 1DTE, EoW [and EoM if SPX]) →
               (A) Volume/Open Interest submenu (with options: Volume, Open Interest, Vol/Oi)
            OR
               (B) Greek Exposure submenu →
                     IV Model submenu (with options: Brent Black Scholes, Grok, Hybrid_one) →
                           Final options: GEX, DEX, VEX, CEX

    For greek exposure, the key is constructed as:
         "{index}|{iv_model}|{expiration}|{final_option}"
    """

    def __init__(self, ui):
        self.ui = ui

        # Determine project root (assumed: project_root/gui/controllers/TV_ctrl.py)
        self.project_root = Path(__file__).resolve().parent.parent.parent

        # Setup logging (logs to project_root/logs/tvpage/tvpage.log)
        log_dir = self.project_root / "logs" / "tvpage"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "tvpage.log"
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(log_file, encoding="utf-8")]
        )
        self.logger = logging.getLogger("TVController")
        self.logger.debug("Initializing TVController for page_4...")

        # JSON file paths
        self.greek_expo_json = self.project_root / "configs" / "htmls" / "greek_expo_paths.json"
        self.vol_oi_json = self.project_root / "configs" / "htmls" / "vol_oi_paths.json"

        # Enable remote URL access for the web views (needed for Plotly CDN)
        for attr in ['p4_wev1', 'p4_wev2', 'p4_wev3']:
            webview = getattr(self.ui, attr, None)
            if webview and isinstance(webview, QWebEngineView):
                settings = webview.settings()
                settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
                self.logger.debug(f"Enabled remote URL access for {attr}.")

        # Create & assign drop menus
        self.setup_drop_menus()

        self.logger.debug("TVController initialization complete.")

        # Connect buttons for toggling left/right frames (if needed)
        self.ui.p4_hideL_button.clicked.connect(self.toggle_left_frame)
        self.ui.p4_hideR_button.clicked.connect(self.toggle_right_frame)

        # New functionality for pushButton_2:
        # By default, frame_31 is hidden and frame_32 is visible.
        self.ui.frame_31.setVisible(False)
        self.ui.frame_32.setVisible(True)
        self.ui.pushButton_2.clicked.connect(self.toggle_frames_pushButton_2)

    def toggle_left_frame(self):
        is_currently_visible = self.ui.p4_Lframe.isVisible()
        self.ui.p4_Lframe.setVisible(not is_currently_visible)

    def toggle_right_frame(self):
        is_currently_visible = self.ui.p4_Rframe.isVisible()
        self.ui.p4_Rframe.setVisible(not is_currently_visible)

    def toggle_frames_pushButton_2(self):
        """
        Toggles frame_31 and frame_32 so that only one is visible at a time.
        If frame_31 is hidden, show it and hide frame_32.
        If frame_31 is visible, hide it and show frame_32.
        """
        if self.ui.frame_31.isVisible():
            self.ui.frame_31.setVisible(False)
            self.ui.frame_32.setVisible(True)
            self.logger.debug("pushButton_2 clicked: Hiding frame_31 and showing frame_32.")
        else:
            self.ui.frame_31.setVisible(True)
            self.ui.frame_32.setVisible(False)
            self.logger.debug("pushButton_2 clicked: Showing frame_31 and hiding frame_32.")

    def setup_drop_menus(self):
        """
        Creates and assigns QMenus to p4_v1_drop, p4_v2_drop, and p4_v3_drop.
        We force the menus to open on button click (using menu.popup(...)).
        """
        button_map = [
            (1, self.ui.p4_v1_drop),
            (2, self.ui.p4_v2_drop),
            (3, self.ui.p4_v3_drop),
        ]

        for view_number, drop_btn in button_map:
            menu = self.create_view_menu(view_number)
            # Set basic styling
            drop_btn.setMenu(menu)
            drop_btn.setPopupMode(QToolButton.InstantPopup)
            drop_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            drop_btn.setText(f"View {view_number}")
            drop_btn.setMinimumSize(120, 30)
            # Connect clicked signal to force the menu popup at the proper position.
            drop_btn.clicked.connect(lambda checked, btn=drop_btn, m=menu, vw=view_number: self.show_menu(btn, m, vw))
            self.logger.debug(f"Assigned menu to p4_v{view_number}_drop with {len(menu.actions())} top-level actions.")

    def show_menu(self, toolbutton: QToolButton, menu: QMenu, view_num: int):
        """
        Pops up the given menu just below the toolbutton.
        """
        self.logger.debug(f"QToolButton 'p4_v{view_num}_drop' pressed.")
        pos = toolbutton.mapToGlobal(toolbutton.rect().bottomLeft())
        menu.popup(pos)

    def create_view_menu(self, view_number: int) -> QMenu:
        """
        Builds the nested menu structure:
          • For each index in ["SPX", "NDX"]:
              • For each expiration:
                   (if index is SPX, expirations = ["0DTE", "1DTE", "EoW", "EoM"];
                    else, ["0DTE", "1DTE", "EoW"])
                   • Add two submenus:
                        – Volume/Open Interest submenu (final options: Volume, Open Interest, Vol/Oi)
                        – Greek Exposure submenu with IV Model intermediary
        """
        top_menu = QMenu()

        # (Optional) add a top-level test action
        test_action = QAction("Test Top-Level Action", top_menu)
        test_action.triggered.connect(lambda: self.logger.debug(f"[View {view_number}] 'Test Top-Level Action' triggered."))
        top_menu.addAction(test_action)

        for index in ["SPX", "NDX"]:
            index_menu = QMenu(index, top_menu)
            self.logger.debug(f"View {view_number}: Creating submenu for index {index}.")
            expirations = ["0DTE", "1DTE", "EoW"]
            if index == "SPX":
                expirations.append("EoM")
            for exp in expirations:
                exp_menu = QMenu(exp, index_menu)
                self.logger.debug(f"View {view_number}: Creating submenu for expiration {exp}.")

                # Volume/Open Interest submenu
                vol_menu = QMenu("Volume/Open Interest", exp_menu)
                vol_menu.aboutToShow.connect(lambda vw=view_number: self.logger.debug(f"View {vw}: Volume/Open Interest submenu about to show."))
                for vol_item in ["Volume", "Open Interest", "Vol/Oi"]:
                    act_vol = QAction(vol_item, vol_menu)
                    act_vol.triggered.connect(lambda checked, idx=index, xp=exp, cat="vol_oi", sub=vol_item, vw=view_number:
                                                self.load_html_for_view(vw, idx, xp, cat, sub))
                    vol_menu.addAction(act_vol)
                exp_menu.addMenu(vol_menu)

                # Greek Exposure submenu with IV Model intermediary
                greek_menu = QMenu("Greek Exposure", exp_menu)
                greek_menu.aboutToShow.connect(lambda vw=view_number: self.logger.debug(f"View {vw}: Greek Exposure submenu about to show."))
                iv_model_sub = QMenu("IV Model", greek_menu)
                iv_model_sub.aboutToShow.connect(lambda vw=view_number: self.logger.debug(f"View {vw}: IV Model submenu about to show."))
                for iv_model in ["Brent Black Scholes", "Grok", "Hybrid_one"]:
                    iv_menu = QMenu(iv_model, iv_model_sub)
                    iv_menu.aboutToShow.connect(lambda im=iv_model, vw=view_number: self.logger.debug(f"View {vw}: IV Model '{im}' submenu about to show."))
                    for g_item in ["GEX", "DEX", "VEX", "CEX"]:
                        act_g = QAction(g_item, iv_menu)
                        act_g.triggered.connect(lambda checked, idx=index, xp=exp, cat="greek", sub=g_item, model=iv_model, vw=view_number:
                                                  self.load_html_for_view(vw, idx, xp, cat, sub, model))
                        iv_menu.addAction(act_g)
                    iv_model_sub.addMenu(iv_menu)
                greek_menu.addMenu(iv_model_sub)
                exp_menu.addMenu(greek_menu)

                index_menu.addMenu(exp_menu)
            top_menu.addMenu(index_menu)

        return top_menu

    def load_html_for_view(self, view_number: int, index: str, expiration: str, category: str, sub_option: str, iv_model: str = None):
        """
        Called when a final action is triggered.
        For vol_oi, key is: "{index}|{expiration}|{sub_option}".
        For greek exposure, key is: "{index}|{iv_model}|{expiration}|{sub_option}".
        Loads the HTML file from JSON and sets it in the appropriate QWebEngineView.
        """
        if category == "vol_oi":
            key = f"{index}|{expiration}|{sub_option}"
            json_path = self.vol_oi_json
            self.logger.debug(f"[View {view_number}] Final selection (vol_oi): {key}")
        else:
            if iv_model is None:
                self.logger.error(f"[View {view_number}] IV Model not provided for greek exposure.")
                return
            key = f"{index}|{iv_model}|{expiration}|{sub_option}"
            json_path = self.greek_expo_json
            self.logger.debug(f"[View {view_number}] Final selection (greek): index={index}, iv_model={iv_model}, expiration={expiration}, sub_option={sub_option}")
            self.logger.debug(f"[View {view_number}] Looking up key: {key} in {json_path}")

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load JSON: {json_path}\n{e}")
            return

        if key not in config or not config[key]:
            QMessageBox.critical(None, "Configuration Error", f"No HTML file path set for selection: {key}")
            return

        rel_path = config[key]
        abs_path = self.project_root / rel_path
        self.logger.debug(f"[View {view_number}] Absolute path resolved as: {abs_path}")

        # Choose the appropriate QWebEngineView based on view_number
        if view_number == 1:
            wev = self.ui.p4_wev1
        elif view_number == 2:
            wev = self.ui.p4_wev2
        elif view_number == 3:
            wev = self.ui.p4_wev3
        else:
            self.logger.error(f"Invalid view_number: {view_number}")
            return

        # Use setUrl to let QWebEngineView load the file and its assets
        wev.setUrl(QUrl.fromLocalFile(str(abs_path)))
        self.logger.debug(f"[View {view_number}] Set URL to {abs_path}")

# For testing TVController independently:
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

    app = QApplication(sys.argv)
    main_win = QMainWindow()
    # Create a dummy widget with the required attributes:
    test_widget = QWidget()
    layout = QVBoxLayout(test_widget)
    # Dummy QToolButtons:
    test_widget.p4_v1_drop = QToolButton()
    test_widget.p4_v2_drop = QToolButton()
    test_widget.p4_v3_drop = QToolButton()
    # Dummy QWebEngineViews:
    test_widget.p4_wev1 = QWebEngineView()
    test_widget.p4_wev2 = QWebEngineView()
    test_widget.p4_wev3 = QWebEngineView()
    # Dummy toggle buttons and frames for additional functionality:
    test_widget.p4_hideL_button = QToolButton()
    test_widget.p4_hideL_button.setText("Toggle Left Frame")
    test_widget.p4_hideR_button = QToolButton()
    test_widget.p4_hideR_button.setText("Toggle Right Frame")
    test_widget.pushButton_2 = QToolButton()
    test_widget.pushButton_2.setText("Toggle frame_31/frame_32")
    # Dummy frames for left/right toggling:
    test_widget.p4_Lframe = QWidget()
    test_widget.p4_Lframe.setStyleSheet("background-color: lightblue")
    test_widget.p4_Rframe = QWidget()
    test_widget.p4_Rframe.setStyleSheet("background-color: lightgreen")
    # Dummy frames for pushButton_2 toggling:
    test_widget.frame_31 = QWidget()
    test_widget.frame_31.setStyleSheet("background-color: pink")
    test_widget.frame_32 = QWidget()
    test_widget.frame_32.setStyleSheet("background-color: orange")
    # Add widgets to the layout
    layout.addWidget(test_widget.p4_v1_drop)
    layout.addWidget(test_widget.p4_v2_drop)
    layout.addWidget(test_widget.p4_v3_drop)
    layout.addWidget(test_widget.p4_wev1)
    layout.addWidget(test_widget.p4_wev2)
    layout.addWidget(test_widget.p4_wev3)
    layout.addWidget(test_widget.p4_hideL_button)
    layout.addWidget(test_widget.p4_hideR_button)
    layout.addWidget(test_widget.pushButton_2)
    layout.addWidget(test_widget.p4_Lframe)
    layout.addWidget(test_widget.p4_Rframe)
    layout.addWidget(test_widget.frame_31)
    layout.addWidget(test_widget.frame_32)
    main_win.setCentralWidget(test_widget)
    tv_ctrl = TVController(test_widget)
    main_win.show()
    sys.exit(app.exec())
