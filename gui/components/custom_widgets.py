from PySide6.QtWidgets import QPushButton

class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("background-color: #333; color: white;")
