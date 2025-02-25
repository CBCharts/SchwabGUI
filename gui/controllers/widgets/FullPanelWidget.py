import os
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget

class FullPanelWidget(QWidget):
    """
    A popup widget for FullPanelWidget.ui
    Provides filtering/setting controls for 'full' data or advanced options.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Build path to FullPanelWidget.ui
        ui_file = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "ui",
            "FullPanelWidget.ui"
        )

        loader = QUiLoader()
        file = QFile(ui_file)
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()

        # Connect signals if needed
        if hasattr(self.ui, "applyButton"):
            self.ui.applyButton.clicked.connect(self.apply_clicked)
        if hasattr(self.ui, "resetButton"):
            self.ui.resetButton.clicked.connect(self.reset_clicked)
        if hasattr(self.ui, "saveButton"):
            self.ui.saveButton.clicked.connect(self.save_clicked)

    def apply_clicked(self):
        print("FullPanelWidget: Apply clicked")

    def reset_clicked(self):
        print("FullPanelWidget: Reset clicked")

    def save_clicked(self):
        print("FullPanelWidget: Save clicked")
