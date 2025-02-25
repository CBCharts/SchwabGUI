from PySide6.QtWidgets import QMessageBox
from gui.controllers.CC_page_ctrl import CCPageController  # Command Center Page Controller
from gui.controllers.single_v import SingleVController       # Single-View Controller (page_3)
from gui.controllers.TV_ctrl import TVController               # TV Controller (page_4)
from gui.controllers.OW_ctrl import OWController               # OW Controller (page_5)
from gui.controllers.NG_ctrl import NGController               # NG Controller (page_6)
from gui.controllers.indicator_table_controller import IndicatorTableController  # New Indicator Table Controller
from gui.controllers.notepad import NotepadController


class MainController:
    def __init__(self, main_window):
        """
        main_window: an instance of your QMainWindow (from main_window.py)
        """
        self.main_window = main_window
        self.ui = main_window.ui  # The auto-generated Ui_MainWindow object

        # Initialize the Command Center Page Controller
        print("DEBUG: Initializing CCPageController")
        self.cc_page_controller = CCPageController(self.ui)  # Pass the UI to the page controller

        # Initialize the Single-View Controller for page_3 (SV_page)
        print("DEBUG: Initializing SingleVController")
        self.sv_controller = SingleVController(self.ui)
        
        # Initialize the TV Controller for page_4
        print("DEBUG: Initializing TVController")
        self.tv_controller = TVController(self.ui)

        # Initialize the OW Controller for page_5 (OW page)
        print("DEBUG: Initializing OWController")
        self.ow_controller = OWController(self.ui)

        # Initialize the NG Controller for page_6 (NG page)
        print("DEBUG: Initializing NGController")
        self.ng_controller = NGController(self.ui)

        # Initialize the Indicator Table Controller
        print("DEBUG: Initializing IndicatorTableController")
        self.indicator_table_controller = IndicatorTableController(self.ui)

        # Initialize Notepad Controller
        print("DEBUG: Initializing NotepadController")
        self.notepad_controller = NotepadController(self.ui)


        # Setup main window button connections
        self.setup_connections()

    def setup_connections(self):
        """Connect UI elements to their respective handler functions."""
        self.ui.minimizebutton.clicked.connect(self.minimize_window)
        self.ui.maxbutton.clicked.connect(self.maximize_window)
        self.ui.closebutton.clicked.connect(self.close_window)
        # Additional connections can be added here as needed
        print("DEBUG: MainController setup_connections() complete")

    def minimize_window(self):
        """Minimize the main window."""
        self.main_window.showMinimized()

    def maximize_window(self):
        """Toggle maximize/restore the main window."""
        if self.main_window.isMaximized():
            self.main_window.showNormal()
        else:
            self.main_window.showMaximized()

    def close_window(self):
        """Close the main window."""
        self.main_window.close()
