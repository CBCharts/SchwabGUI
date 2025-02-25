import os
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget

class MCPriWidget(QWidget):
    """
    A popup widget for MCPriWidget.ui
    Provides filtering/setting controls for multi-criteria priority, etc.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Build path to MCPriWidget.ui
        ui_file = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "ui",
            "MCPriWidget.ui"
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

        # Example: a "priority" group or radio buttons might exist
        # if hasattr(self.ui, "priorityGroup"):
        #     # connect signals, etc.

    def apply_clicked(self):
        print("MCPriWidget: Apply clicked")

    def reset_clicked(self):
        print("MCPriWidget: Reset clicked")
