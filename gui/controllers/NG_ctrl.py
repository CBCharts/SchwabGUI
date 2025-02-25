import csv
import logging
import json
from pathlib import Path

# Instead of connecting directly to ZeroPanelWidget, we import FilterManager.
from gui.controllers.widgets.FilterManager import FilterManager
from gui.controllers.widgets.FullPanelWidget import FullPanelWidget
from gui.controllers.widgets.MCPriWidget import MCPriWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QMessageBox, QAbstractItemView
)

class NGController:
    def __init__(self, ui):
        self.ui = ui
        self.setup_logging()

        # Load CSV paths
        self.csv_paths = {}
        self.load_csv_paths()

        self.current_index = None

        # Instantiate FilterManager and connect signals
        self.filterManager = FilterManager()
        self.filterManager.filtersUpdated.connect(self.onFiltersUpdated)
        self.connect_signals()
        self.logger.debug("NGController initialized with all signals connected.")

        # Configure source tables for copy-only drag actions.
        self.configure_tables_for_copy()

    def configure_tables_for_copy(self):
        """
        For each source QTableWidget in this page, enable dragging with a default drop action of Copy.
        This prevents the original rows from being removed or hidden when pasted elsewhere.
        """
        # List of the table widget names (as strings) to be configured.
        table_names = [
            "tableWidget_9",
            "tableWidget_13",
            "tableWidget_4",
            "tableWidget_6",
            "tableWidget_8",
            "tableWidget_7",
            "tableWidget_12",
            "tableWidget_10",
            "tableWidget_11"
        ]
        for name in table_names:
            if hasattr(self.ui, name):
                table = getattr(self.ui, name)
                # Enable dragging from the table.
                table.setDragEnabled(True)
                # Set the drag-drop mode to DragOnly so that this table is only a source.
                table.setDragDropMode(QAbstractItemView.DragOnly)
                # Force the drop action to be a copy.
                table.setDefaultDropAction(Qt.CopyAction)
                # Ensure that dropping does not overwrite existing data.
                table.setDragDropOverwriteMode(False)
                self.logger.debug(f"Configured {name} for copy-only drag actions.")
            else:
                self.logger.debug(f"Table widget '{name}' not found in UI; skipping configuration.")
    

    def setup_logging(self):
        self.project_root = Path(__file__).resolve().parent.parent.parent
        log_dir = self.project_root / "logs" / "NG"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "ng_page.log"
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(log_file, encoding="utf-8")]
        )
        self.logger = logging.getLogger("NGController")
        self.logger.debug("Logging is set up for NGController (ng_page.log).")

    def load_csv_paths(self):
        csv_db_path = self.project_root / "configs" / "excel" / "csv_paths.json"
        if csv_db_path.exists():
            try:
                with open(csv_db_path, "r", encoding="utf-8") as f:
                    self.csv_paths = json.load(f)
                self.logger.debug(f"Loaded CSV paths from {csv_db_path}")
            except Exception as e:
                self.logger.error(f"Error loading CSV paths: {e}")
        else:
            self.logger.warning(f"CSV paths file not found at {csv_db_path}.")

    def connect_signals(self):
        if hasattr(self.ui, "pushButton_38") and hasattr(self.ui, "frame_52"):
            self.ui.pushButton_38.clicked.connect(self.toggle_frame_52)
            self.logger.debug("Connected pushButton_38 to toggle_frame_52.")
        if hasattr(self.ui, "pushButton_35") and hasattr(self.ui, "frame_54"):
            self.ui.pushButton_35.clicked.connect(self.toggle_frame_54)
            self.logger.debug("Connected pushButton_35 to toggle_frame_54.")
        if hasattr(self.ui, "pushButton_33") and hasattr(self.ui, "frame_55"):
            self.ui.pushButton_33.clicked.connect(self.toggle_frame_55)
            self.logger.debug("Connected pushButton_33 to toggle_frame_55.")
        if hasattr(self.ui, "pushButton_40") and hasattr(self.ui, "frame_53"):
            self.ui.pushButton_40.clicked.connect(self.toggle_frame_53)
            self.logger.debug("Connected pushButton_40 to toggle_frame_53.")
        if hasattr(self.ui, "pushButton_42") and hasattr(self.ui, "frame_43"):
            self.ui.pushButton_42.clicked.connect(self.toggle_frame_43)
            self.logger.debug("Connected pushButton_42 to toggle_frame_43.")
        if hasattr(self.ui, "pushButton_37"):
            self.ui.pushButton_37.clicked.connect(self.show_filter_panel)
        if hasattr(self.ui, "pushButton_30"):
            self.ui.pushButton_30.clicked.connect(self.show_MCPri_panel)
        if hasattr(self.ui, "pushButton_34"):
            self.ui.pushButton_34.clicked.connect(self.show_full_panel)

        if hasattr(self.ui, "pushButton_41") and hasattr(self.ui, "p6_Lframe"):
            self.ui.pushButton_41.clicked.connect(self.toggle_p6_Lframe)
            self.logger.debug("Connected pushButton_41 to toggle_p6_Lframe.")
        if hasattr(self.ui, "pushButton_43") and hasattr(self.ui, "p6_Rframe"):
            self.ui.pushButton_43.clicked.connect(self.toggle_p6_Rframe)
            self.logger.debug("Connected pushButton_43 to toggle_p6_Rframe.")

        if hasattr(self.ui, "pushButton_28"):
            self.ui.pushButton_28.setCheckable(True)
            self.ui.pushButton_28.clicked.connect(self.handle_pushButton_28)
            self.logger.debug("Connected pushButton_28 to handle_pushButton_28 (SPX).")
        if hasattr(self.ui, "pushButton_31"):
            self.ui.pushButton_31.setCheckable(True)
            self.ui.pushButton_31.clicked.connect(self.handle_pushButton_31)
            self.logger.debug("Connected pushButton_31 to handle_pushButton_31 (NDX).")

        if hasattr(self.ui, "p6_manual_button"):
            self.ui.p6_manual_button.clicked.connect(self.handle_manual_load_button)
            self.logger.debug("Connected p6_manual_button to handle_manual_load_button.")

    def show_filter_panel(self):
        # Show the ZeroPanelWidget from the filter manager.
        self.filterManager.zeroPanel.show()

    def onFiltersUpdated(self, filter_data: dict):
        self.logger.debug(f"onFiltersUpdated called with: {filter_data}")
        self.apply_filters_to_table(self.ui.tableWidget_6, filter_data)
        user_opt_type = filter_data.get("option_type", "All")
        if user_opt_type == "Calls":
            self.ui.tableWidget_6.setColumnHidden(4, True)
            self.ui.tableWidget_6.setColumnHidden(5, True)
            self.ui.tableWidget_6.setColumnHidden(6, True)
            self.ui.tableWidget_6.setColumnHidden(0, False)
            self.ui.tableWidget_6.setColumnHidden(1, False)
            self.ui.tableWidget_6.setColumnHidden(2, False)
        elif user_opt_type == "Puts":
            self.ui.tableWidget_6.setColumnHidden(0, True)
            self.ui.tableWidget_6.setColumnHidden(1, True)
            self.ui.tableWidget_6.setColumnHidden(2, True)
            self.ui.tableWidget_6.setColumnHidden(4, False)
            self.ui.tableWidget_6.setColumnHidden(5, False)
            self.ui.tableWidget_6.setColumnHidden(6, False)
        else:
            for col in [0,1,2,4,5,6]:
                self.ui.tableWidget_6.setColumnHidden(col, False)

    def apply_filters_to_table(self, table_widget, filter_data: dict):
        row_count = table_widget.rowCount()
        for row in range(row_count):
            hide_row = False
            try:
                vol_min = float(filter_data.get("volume_min", "0") or "0")
                vol_max = float(filter_data.get("volume_max", "99999999") or "99999999")
            except ValueError:
                vol_min, vol_max = 0, 99999999
            call_vol_item = table_widget.item(row, 0)
            if call_vol_item:
                try:
                    call_vol = float(call_vol_item.text())
                    if call_vol < vol_min or call_vol > vol_max:
                        hide_row = True
                except ValueError:
                    pass
            try:
                strike_min = float(filter_data.get("strike_min", "0") or "0")
                strike_max = float(filter_data.get("strike_max", "99999999") or "99999999")
            except ValueError:
                strike_min, strike_max = 0, 99999999
            strike_item = table_widget.item(row, 3)
            if strike_item:
                try:
                    strike_val = float(strike_item.text())
                    if strike_val < strike_min or strike_val > strike_max:
                        hide_row = True
                except ValueError:
                    pass
            table_widget.setRowHidden(row, hide_row)

    def show_full_panel(self):
        self.full_panel = FullPanelWidget()
        self.full_panel.show()

    def show_MCPri_panel(self):
        self.MCPri_panel = MCPriWidget()
        self.MCPri_panel.show()

    def toggle_frame_52(self):
        self.logger.debug("pushButton_38 clicked (NGController).")
        visible = self.ui.frame_52.isVisible()
        self.ui.frame_52.setVisible(not visible)
        self.logger.debug(f"toggle_frame_52: frame_52 visibility set to {not visible}")

    def toggle_frame_54(self):
        self.logger.debug("pushButton_35 clicked (NGController).")
        visible = self.ui.frame_54.isVisible()
        self.ui.frame_54.setVisible(not visible)
        self.logger.debug(f"toggle_frame_54: frame_54 visibility set to {not visible}")

    def toggle_frame_55(self):
        self.logger.debug("pushButton_33 clicked (NGController).")
        visible = self.ui.frame_55.isVisible()
        self.ui.frame_55.setVisible(not visible)
        self.logger.debug(f"toggle_frame_55: frame_55 visibility set to {not visible}")

    def toggle_frame_53(self):
        self.logger.debug("pushButton_40 clicked (NGController).")
        visible = self.ui.frame_53.isVisible()
        self.ui.frame_53.setVisible(not visible)
        self.logger.debug(f"toggle_frame_53: frame_53 visibility set to {not visible}")

    def toggle_frame_43(self):
        self.logger.debug("pushButton_42 clicked (NGController).")
        visible = self.ui.frame_43.isVisible()
        self.ui.frame_43.setVisible(not visible)
        self.logger.debug(f"toggle_frame_43: frame_43 visibility set to {not visible}")

    def toggle_p6_Lframe(self):
        self.logger.debug("pushButton_41 clicked (NGController) -> toggling p6_Lframe.")
        visible = self.ui.p6_Lframe.isVisible()
        self.ui.p6_Lframe.setVisible(not visible)
        self.logger.debug(f"toggle_p6_Lframe: p6_Lframe visibility set to {not visible}")

    def toggle_p6_Rframe(self):
        self.logger.debug("pushButton_43 clicked (NGController) -> toggling p6_Rframe.")
        visible = self.ui.p6_Rframe.isVisible()
        self.ui.p6_Rframe.setVisible(not visible)
        self.logger.debug(f"toggle_p6_Rframe: p6_Rframe visibility set to {not visible}")

    def handle_pushButton_28(self):
        self.logger.debug("pushButton_28 clicked (NGController).")
        if self.ui.pushButton_28.isChecked():
            if hasattr(self.ui, "pushButton_31"):
                self.ui.pushButton_31.setChecked(False)
                self.logger.debug("pushButton_31 unchecked due to pushButton_28 selection.")
            self.current_index = "SPX"
            self.logger.debug("pushButton_28 set current_index to 'SPX'.")
        else:
            if hasattr(self.ui, "pushButton_31") and not self.ui.pushButton_31.isChecked():
                self.current_index = None
                self.logger.debug("pushButton_28 unchecked and pushButton_31 not checked; current_index reset.")

    def handle_pushButton_31(self):
        self.logger.debug("pushButton_31 clicked (NGController).")
        if self.ui.pushButton_31.isChecked():
            if hasattr(self.ui, "pushButton_28"):
                self.ui.pushButton_28.setChecked(False)
                self.logger.debug("pushButton_28 unchecked due to pushButton_31 selection.")
            self.current_index = "NDX"
            self.logger.debug("pushButton_31 set current_index to 'NDX'.")
        else:
            if hasattr(self.ui, "pushButton_28") and not self.ui.pushButton_28.isChecked():
                self.current_index = None
                self.logger.debug("pushButton_31 unchecked and pushButton_28 not checked; current_index reset.")

    def handle_manual_load_button(self):
        self.logger.debug("p6_manual_button clicked (NGController).")
        if not self.current_index:
            self.logger.debug("Manual load aborted: No index selected.")
            QMessageBox.warning(None, "Index Not Selected", "Please Choose 'SPX or NDX'")
            return

        time_segment = "0DTE"
        table_map = {
            "tableWidget_6":  "Chain",
            "tableWidget_9":  "Greeks",
            "tableWidget_4":  "Greek Ratios",
            "tableWidget_13": "Greek Ranked"
        }
        columns_to_extract = {
            "Chain": [
                "call vol",
                "call oi",
                "call_vol/oi",
                "strike",
                "put vol",
                "put oi",
                "put_vol/oi"
            ],
            "Greeks": [
                "strikePrice",
                "expirationDate",
                "putCall",
                "delta",
                "gamma",
                "vanna",
                "charm",
                "DEX",
                "GEX",
                "VEX",
                "CEX",
                "Gamma Flip"
            ],
            "Greek Ratios": [
                "timestamp",
                "Greek",
                "Call",
                "Put",
                "Ratio"
            ],
            "Greek Ranked": [
                "timestamp",
                "strikePrice",
                "Theo ES",
                "Rank",
                "Greek",
                "Value"
            ]
        }
        for widget_name, final_segment in table_map.items():
            if hasattr(self.ui, widget_name):
                table_widget = getattr(self.ui, widget_name)
                csv_key = f"{self.current_index}|{time_segment}|{final_segment}"
                csv_path = self.csv_paths.get(csv_key, "")
                self.logger.debug(
                    f"Manual load: For widget '{widget_name}', using key '{csv_key}' → CSV path '{csv_path}'."
                )
                if not csv_path:
                    self.logger.warning(
                        f"No CSV path for key {csv_key}. Skipping table '{widget_name}'."
                    )
                    continue

                wanted_cols = columns_to_extract.get(final_segment, None)
                self.load_csv_into_table(table_widget, csv_path, wanted_cols)
            else:
                self.logger.warning(f"Widget '{widget_name}' not found in UI. Skipping.")

    def load_csv_into_table(self, table_widget: QTableWidget, csv_file_path: str, columns=None):
        self.logger.debug(f"Attempting to load CSV from '{csv_file_path}' into table widget.")
        csv_file = Path(self.project_root / csv_file_path)
        if not csv_file.exists():
            self.logger.error(f"CSV file not found: {csv_file}")
            QMessageBox.critical(None, "File Error", f"CSV file not found:\n{csv_file}")
            return

        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                all_rows = list(reader)

            if not all_rows:
                self.logger.warning(f"CSV file {csv_file} is empty.")
                return

            header_row = all_rows[0]
            data_rows = all_rows[1:]
            if not columns:
                final_headers = header_row
                final_data = data_rows
            else:
                col_indices = []
                for col_name in columns:
                    if col_name in header_row:
                        col_indices.append(header_row.index(col_name))
                    else:
                        self.logger.warning(
                            f"Column '{col_name}' not found in CSV {csv_file_path}. Will insert blank data."
                        )
                        col_indices.append(None)
                final_headers = [c for c in columns if c in header_row]
                final_data = []
                for row in data_rows:
                    filtered_row = []
                    for idx in col_indices:
                        if idx is not None and idx < len(row):
                            formatted_value = self.format_cell_value(row[idx])
                            filtered_row.append(formatted_value)
                        else:
                            filtered_row.append("")
                    final_data.append(filtered_row)

            table_widget.clear()
            table_widget.setRowCount(len(final_data))
            table_widget.setColumnCount(len(final_headers))
            table_widget.setHorizontalHeaderLabels(final_headers)
            for r, row_data in enumerate(final_data):
                for c, cell_value in enumerate(row_data):
                    table_widget.setItem(r, c, QTableWidgetItem(cell_value))
            self.logger.debug(
                f"Loaded CSV data from '{csv_file}' into table widget with columns {final_headers}."
            )
        except Exception as e:
            self.logger.error(f"Error loading CSV file {csv_file}: {e}")
            QMessageBox.critical(None, "Error", f"Error loading CSV file {csv_file}:\n{e}")

    def format_cell_value(self, raw_value: str) -> str:
        try:
            num = float(raw_value)
            formatted = f"{num:.3f}"
            return formatted
        except ValueError:
            return raw_value
