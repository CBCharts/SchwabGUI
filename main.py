import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    print("DEBUG: Starting main.py")
    app = QApplication(sys.argv)

    print("DEBUG: Creating MainWindow")
    window = MainWindow()
    window.show()

    print("DEBUG: Starting event loop")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
