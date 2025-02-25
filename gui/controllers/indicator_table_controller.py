import os
import csv
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import (
    QMenu, QMessageBox, QInputDialog, QLineEdit, QTableWidgetItem, QAbstractItemView
)
from PySide6.QtGui import QAction

class IndicatorTableController:
    def __init__(self, ui):
        """
        ui: The Ui_MainWindow object containing:
          - toolButton_5 (the Indicator toolbutton)
          - pushButton_44 (Save)
          - pushButton_45 (Clear)
          - pushButton_46 (Save As)
          - indicator_drop_tableWidget (QTableWidget for dropped data)
          - checkBox_3 (Disable PopUp Warning)
        """
        self.ui = ui

        # Set up the Indicator tool button with dropdown options.
        self.setup_indicator_toolbutton()

        # Connect top-level buttons.
        self.ui.pushButton_44.clicked.connect(self.handle_save)
        self.ui.pushButton_45.clicked.connect(self.handle_clear)
        if hasattr(self.ui, "pushButton_46"):
            self.ui.pushButton_46.clicked.connect(self.handle_save_as)

        # Configure the QTableWidget.
        table = self.ui.indicator_drop_tableWidget
        table.setDragEnabled(False)   # Typically, this table is used as a drop target.
        table.setAcceptDrops(True)
        table.setDragDropMode(QAbstractItemView.DropOnly)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self.handle_context_menu)

        # In-memory storage.
        self.current_file_path = ""  # Will be set based on the indicator.
        self.clipboard_rows = []     # For copy/paste functionality.

    # -------------------------------------------------------------------------
    # Indicator toolbutton setup (including new "Greek Exposures")
    # -------------------------------------------------------------------------
    def setup_indicator_toolbutton(self):
        """
        Sets up toolButton_5 with a default label 'Indicator' and
        dropdown options: Premium, TimeStamped, Vol/Oi, Greek Exposures.
        """
        tb = self.ui.toolButton_5
        tb.setText("Indicator")
        menu = QMenu(tb)

        act_premium = QAction("Premium", tb)
        act_timestamped = QAction("TimeStamped", tb)
        act_voloi = QAction("Vol/Oi", tb)
        act_greek = QAction("Greek Exposures", tb)

        act_premium.triggered.connect(lambda: self.set_indicator("Premium"))
        act_timestamped.triggered.connect(lambda: self.set_indicator("TimeStamped"))
        act_voloi.triggered.connect(lambda: self.set_indicator("Vol/Oi"))
        act_greek.triggered.connect(lambda: self.set_indicator("Greek Exposures"))

        menu.addAction(act_premium)
        menu.addAction(act_timestamped)
        menu.addAction(act_voloi)
        menu.addAction(act_greek)

        tb.setMenu(menu)

        # Start with a default indicator.
        self.selected_indicator = "Premium"
        self.set_indicator("Premium")

    def set_indicator(self, indicator_name):
        """
        Update the current indicator, set its header template, and load its associated CSV.
        """
        self.selected_indicator = indicator_name
        self.ui.toolButton_5.setText(indicator_name)
        self.current_file_path = self.default_csv_for_indicator(indicator_name)
        self.load_table_from_csv(self.current_file_path)

    def default_csv_for_indicator(self, indicator_name):
        """
        Return a default CSV filename (in the NT Indicators folder) based on the indicator.
        """
        base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "NT Indicators")
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        mapping = {
            "Premium": "premium_data.csv",
            "TimeStamped": "timestamped_data.csv",
            "Vol/Oi": "vol_oi_data.csv",
            "Greek Exposures": "greek_exposures.csv",
        }
        return os.path.join(base_dir, mapping.get(indicator_name, "unknown_indicator.csv"))

    def get_default_headers(self):
        """
        Return the header row for the currently selected indicator.
        """
        if self.selected_indicator in ["Premium", "TimeStamped"]:
            return ["timestamp", "interval", "call premium", "call vol", "call oi", "call_vol/oi",
                    "strike", "put vol", "put oi", "put_vol/oi", "put premium", "block deltas"]
        elif self.selected_indicator == "Vol/Oi":
            return ["call vol", "call oi", "call_vol/oi", "strike", "put vol", "put oi", "put_vol/oi"]
        elif self.selected_indicator == "Greek Exposures":
            return ["timestamp", "strikePrice", "Theo Price", "Rank", "Greek", "Value"]
        else:
            return []

    # -------------------------------------------------------------------------
    # Save / Load / Clear functions (with header preservation)
    # -------------------------------------------------------------------------
    def handle_save(self):
        """
        Save the current table data (including the fixed header row) to self.current_file_path.
        """
        if not self.current_file_path:
            self.current_file_path = self.default_csv_for_indicator(self.selected_indicator)
        self.save_table_to_csv(self.current_file_path)

    def handle_save_as(self):
        """
        Prompt for a new filename and save to that CSV.
        Then show a warning regarding NinjaTrader filename updates.
        """
        new_name, ok = QInputDialog.getText(
            None,
            "Save As",
            "Enter new filename (e.g. my_custom.csv):",
            QLineEdit.Normal,
            ""
        )
        if ok and new_name.strip():
            self.show_ninjatrader_filename_warning()
            self.current_file_path = os.path.join(
                os.path.dirname(self.default_csv_for_indicator(self.selected_indicator)),
                new_name.strip()
            )
            self.save_table_to_csv(self.current_file_path)

    def handle_clear(self):
        """
        Clear only the data rows (preserve the header row) in the table and overwrite the CSV.
        """
        if not self.confirm_action("This will delete ALL data rows in the CSV. Continue?"):
            return
        table = self.ui.indicator_drop_tableWidget
        # Preserve header row (row 0) and clear all data rows
        table.setRowCount(1)
        headers = self.get_default_headers()
        table.setColumnCount(len(headers))
        for col, header in enumerate(headers):
            item = QTableWidgetItem(header)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            table.setItem(0, col, item)
        self.save_table_to_csv(self.current_file_path)

    def save_table_to_csv(self, filepath):
        """
        Write all rows from the table to a CSV file.
        The header row (row 0) is always written first.
        """
        table = self.ui.indicator_drop_tableWidget
        row_count = table.rowCount()
        col_count = table.columnCount()

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for r in range(row_count):
                row_data = []
                for c in range(col_count):
                    item = table.item(r, c)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)
        # Convert the relative file path to an absolute path.
        simplified_path = os.path.abspath(filepath)
        QMessageBox.information(None, "Saved", f"Table saved to {simplified_path}")


    def load_table_from_csv(self, filepath):
        """
        Load CSV data into the table.
        If the file does not exist, create it with the default header row.
        """
        table = self.ui.indicator_drop_tableWidget
        default_headers = self.get_default_headers()
        if not os.path.exists(filepath):
            # Create the file with header row only.
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(default_headers)
            rows = [default_headers]
        else:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)
            if not rows:
                rows = [default_headers]

        table.clearContents()
        table.setRowCount(len(rows))
        table.setColumnCount(len(default_headers))
        for r, row_data in enumerate(rows):
            for c in range(len(default_headers)):
                # Use existing data if available; otherwise, use header default.
                val = row_data[c] if c < len(row_data) else default_headers[c]
                item = QTableWidgetItem(val)
                # For header row, disable editing.
                if r == 0:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table.setItem(r, c, item)

    def show_ninjatrader_filename_warning(self):
        """
        Popup warning regarding the need to update the NinjaTrader indicator filename.
        Only shown if the Disable PopUp Warning checkbox is unchecked.
        """
        if not self.ui.checkBox_3.isChecked():
            QMessageBox.warning(
                None,
                "NinjaTrader Filename Warning",
                "Remember to manually change the filename in the NinjaTrader indicator!"
            )

    # -------------------------------------------------------------------------
    # Context Menu for the table
    # -------------------------------------------------------------------------
    def handle_context_menu(self, pos: QPoint):
        """
        Display a custom context menu based on whether the user clicked a data row.
        (Row 0 is the header and is protected.)
        """
        table = self.ui.indicator_drop_tableWidget
        menu = QMenu(table)
        # Do not allow context menu on the header row.
        row = table.rowAt(pos.y())
        if row <= 0:
            # Right-click on empty area or header row.
            save_action = QAction("Save", menu)
            save_action.triggered.connect(self.handle_save)
            menu.addAction(save_action)

            save_as_action = QAction("Save As", menu)
            save_as_action.triggered.connect(self.handle_save_as)
            menu.addAction(save_as_action)

            clear_action = QAction("Clear", menu)
            clear_action.triggered.connect(self.handle_clear)
            menu.addAction(clear_action)

            copy_all_action = QAction("Copy All", menu)
            copy_all_action.triggered.connect(self.copy_all)
            menu.addAction(copy_all_action)

            paste_action = QAction("Paste", menu)
            paste_action.triggered.connect(self.paste_rows)
            menu.addAction(paste_action)
        else:
            # Right-click on a data row.
            delete_action = QAction("Delete Row", menu)
            delete_action.triggered.connect(lambda: self.delete_row(row))
            menu.addAction(delete_action)

            save_action = QAction("Save", menu)
            save_action.triggered.connect(self.handle_save)
            menu.addAction(save_action)

            save_as_action = QAction("Save As", menu)
            save_as_action.triggered.connect(self.handle_save_as)
            menu.addAction(save_as_action)

            clear_action = QAction("Clear", menu)
            clear_action.triggered.connect(self.handle_clear)
            menu.addAction(clear_action)

            copy_action = QAction("Copy", menu)
            copy_action.triggered.connect(lambda: self.copy_rows([row]))
            menu.addAction(copy_action)

        menu.exec(table.mapToGlobal(pos))

    def delete_row(self, row_idx):
        """
        Delete a specific data row after confirmation.
        (Row 0 is the header and will not be deleted.)
        """
        if row_idx == 0:
            return
        if not self.confirm_action(f"Delete row {row_idx}?"):
            return
        table = self.ui.indicator_drop_tableWidget
        table.removeRow(row_idx)

    # -------------------------------------------------------------------------
    # Copy and Paste functionality
    # -------------------------------------------------------------------------
    def copy_rows(self, rows):
        """
        Copy the specified rows (excluding header) to a local clipboard.
        """
        table = self.ui.indicator_drop_tableWidget
        self.clipboard_rows = []
        for r in rows:
            if r == 0:
                continue
            row_data = []
            for c in range(table.columnCount()):
                item = table.item(r, c)
                row_data.append(item.text() if item else "")
            self.clipboard_rows.append(row_data)

    def copy_all(self):
        """
        Copy all data rows (excluding header) in the table.
        """
        table = self.ui.indicator_drop_tableWidget
        rows = list(range(1, table.rowCount()))
        self.copy_rows(rows)

    def paste_rows(self):
        """
        Paste rows from the local clipboard to the end of the table.
        """
        if not self.clipboard_rows:
            return
        table = self.ui.indicator_drop_tableWidget
        for row_data in self.clipboard_rows:
            row_idx = table.rowCount()
            table.insertRow(row_idx)
            for col_idx, val in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(val))
        self.save_table_to_csv(self.current_file_path)

    # -------------------------------------------------------------------------
    # Helper function for confirmations
    # -------------------------------------------------------------------------
    def confirm_action(self, message):
        """
        If the Disable PopUp Warning checkbox is checked, skip confirmation.
        Otherwise, show a Yes/No dialog.
        """
        if self.ui.checkBox_3.isChecked():
            return True
        reply = QMessageBox.question(
            None,
            "Confirm",
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return (reply == QMessageBox.Yes)
