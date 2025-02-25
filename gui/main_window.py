from PySide6.QtWidgets import QMainWindow, QApplication
from gui.ui.lite_ui import Ui_MainWindow
from gui.controllers.main_controller import MainController
import gui.resources.resources_rc



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("DEBUG: In MainWindow.__init__()")

        # Instantiate and set up the generated UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        print("DEBUG: Creating MainController")
        self.controller = MainController(self)

        # Mapping buttons to their respective stacked widget page indices
        button_page_map = {
            "CC_button": 0,
            "SV_button": 1,
            "TV_button": 2,
            "OW_button": 3,
            "pushButton": 4,  # NG_button was renamed to pushButton
            "DOC_button": 5
        }

        # Loop through and connect buttons dynamically
        for button_name, page_index in button_page_map.items():
            button = getattr(self.ui, button_name, None)
            if button:
                button.clicked.connect(self.create_page_switcher(page_index))
            else:
                print(f"WARNING: {button_name} not found in UI file. Skipping...")

        # ✅ FIX: Connect collapse_leftframe_button to toggle_left_frame
        if hasattr(self.ui, "collapse_leftframe_button"):
            self.ui.collapse_leftframe_button.clicked.connect(self.toggle_left_frame)
        else:
            print("WARNING: collapse_leftframe_button not found in UI file.")

        print("DEBUG: Done with MainWindow.__init__()")

    def create_page_switcher(self, index):
        """Returns a function to switch the stacked widget page dynamically."""
        def switch_page():
            print(f"DEBUG: Switching to page {index}")
            self.ui.stackedWidget.setCurrentIndex(index)
        return switch_page

    def toggle_left_frame(self):
        """Hide/Show the left frame with a single button click."""
        if hasattr(self.ui, "LeftMain"):
            visible = self.ui.LeftMain.isVisible()
            self.ui.LeftMain.setVisible(not visible)
            print(f"DEBUG: LeftMain visibility set to {not visible}")
        else:
            print("WARNING: LeftMain frame not found in UI file.")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()  # FIXED: Changed from MainApp() to MainWindow()
    window.show()
    app.exec()
