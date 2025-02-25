import os
import json
import logging

from PySide6.QtCore import QFile, Qt, Signal
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QWidget, QInputDialog, QLineEdit, QMessageBox
)

# Each step of prem_slider represents 10,000 real units.
PREM_SCALE = 10_000  


class ZeroPanelWidget(QWidget):
    """
    This widget is loaded from ZeroPanelWidget.ui.
    It gathers filter settings (volume, OI, premium, strike, lastPrice, option type),
    ties lineEdits to sliders (with a special scaling for premium),
    and emits signals for apply/reset/save.
    """

    # Emitted when the user clicks "Apply," carrying the chosen filter data.
    applyFilter = Signal(dict)
    # Emitted when the user clicks "Save," to store a preset.
    savePreset = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_logging()
        self.logger.debug("ZeroPanelWidget __init__() started.")

        # 1) Load the UI from projectroot/gui/ui/ZeroPanelWidget.ui
        loader = QUiLoader()
        ui_file_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..",  # up two levels => projectroot/gui
            "ui",
            "ZeroPanelWidget.ui"
        )
        self.logger.debug(f"Loading UI from: {ui_file_path}")
        file = QFile(ui_file_path)
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()
        self.logger.debug("UI file loaded successfully.")

        # 2) Set explicit slider ranges.
        if hasattr(self.ui, "vol_slider"):
            self.logger.debug("Setting vol_slider range to 0..400000")
            self.ui.vol_slider.setRange(0, 400000)
        if hasattr(self.ui, "oi_slider"):
            self.logger.debug("Setting oi_slider range to 0..400000")
            self.ui.oi_slider.setRange(0, 400000)
        if hasattr(self.ui, "prem_slider"):
            # Use scaled approach: internal range 0..1,000,000, each step = 10,000
            self.logger.debug(f"Setting prem_slider range to 0..1,000,000 (scaled by {PREM_SCALE})")
            self.ui.prem_slider.setRange(0, 1_000_000)
        if hasattr(self.ui, "strikePrice_slider"):
            self.logger.debug("Setting strikePrice_slider range to 0..50000")
            self.ui.strikePrice_slider.setRange(0, 50_000)
        if hasattr(self.ui, "lastPrice_slider"):
            self.logger.debug("Setting lastPrice_slider range to 0..50000")
            self.ui.lastPrice_slider.setRange(0, 50_000)

        # 3) Connect push buttons.
        if hasattr(self.ui, "apply_button"):
            self.ui.apply_button.clicked.connect(self.on_apply_clicked)
            self.logger.debug("Found apply_button => on_apply_clicked connected.")
        if hasattr(self.ui, "reset_button"):
            self.ui.reset_button.clicked.connect(self.on_reset_clicked)
            self.logger.debug("Found reset_button => on_reset_clicked connected.")
        if hasattr(self.ui, "save_button"):
            self.ui.save_button.clicked.connect(self.on_save_clicked)
            self.logger.debug("Found save_button => on_save_clicked connected.")

        # 4) Option Type combo.
        if hasattr(self.ui, "optionType_combo"):
            self.logger.debug("Found optionType_combo in .ui.")

        # 5) Tie sliders to lineEdits.
        self.setup_slider_lineEdit_pair(
            slider=self.ui.vol_slider,
            lineEdit_min=self.ui.vol_lineEdit_min,
            lineEdit_max=self.ui.vol_lineEdit_max
        )
        self.setup_slider_lineEdit_pair(
            slider=self.ui.oi_slider,
            lineEdit_min=self.ui.oi_lineEdit_min,
            lineEdit_max=self.ui.oi_lineEdit_max
        )
        # For prem_slider, use our specialized scaled pairing.
        if hasattr(self.ui, "prem_slider"):
            self.setup_prem_slider_pair(
                slider=self.ui.prem_slider,
                lineEdit_min=self.ui.prem_lineEdit_min,
                lineEdit_max=self.ui.prem_lineEdit_max
            )
        self.setup_slider_lineEdit_pair(
            slider=self.ui.strikePrice_slider,
            lineEdit_min=self.ui.strikePrice_lineEdit_min,
            lineEdit_max=self.ui.strikePrice_lineEdit_max
        )
        self.setup_slider_lineEdit_pair(
            slider=self.ui.lastPrice_slider,
            lineEdit_min=self.ui.lastPrice_lineEdit_min,
            lineEdit_max=self.ui.lastPrice_lineEdit_max
        )

        # 6) Build path for presets JSON at projectroot/configs/settings/filterwidgets.
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        self.presets_file_path = os.path.join(
            project_root,
            "configs", "settings", "filterwidgets",
            "zero_panel_presets.json"
        )
        self.logger.debug(f"Presets file path => {self.presets_file_path}")

        # 7) Load existing presets.
        self.loaded_presets = self.load_presets_from_json()
        self.logger.debug(f"loaded_presets => {self.loaded_presets}")

        # 8) Populate preset_combo with the loaded presets, offset by +1 (index 0 is the label "Preset").
        if hasattr(self.ui, "preset_combo"):
            count_before = self.ui.preset_combo.count()
            self.logger.debug(f"preset_combo initially has {count_before} items. (Should have 1: 'Preset')")
            for p in self.loaded_presets:
                insert_index = self.ui.preset_combo.count()
                self.ui.preset_combo.insertItem(insert_index, p["name"])
            self.ui.preset_combo.currentIndexChanged.connect(self.on_preset_combo_changed)
            self.logger.debug("preset_combo => on_preset_combo_changed connected.")
        else:
            self.logger.debug("No preset_combo found in .ui.")

        self.logger.debug("ZeroPanelWidget __init__ complete.")


    def setup_logging(self):
        """
        Set up logging to projectroot/logs/zero_panel_widget/zero_panel_widget.log.
        """
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        log_dir = os.path.join(project_root, "logs", "zero_panel_widget")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "zero_panel_widget.log")
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(log_file, encoding="utf-8")]
        )
        self.logger = logging.getLogger("ZeroPanelWidgetLogger")
        self.logger.debug(f"Logging set up => {log_file}")


    def setup_slider_lineEdit_pair(self, slider, lineEdit_min, lineEdit_max):
        """
        Standard integer QSlider pairing: the min lineEdit drives the slider’s value,
        and the max lineEdit sets the slider’s maximum.
        """
        if not slider or not lineEdit_min or not lineEdit_max:
            self.logger.debug("setup_slider_lineEdit_pair => missing widget(s), skipping.")
            return

        self.logger.debug(f"Linking {slider.objectName()} with {lineEdit_min.objectName()} / {lineEdit_max.objectName()}")

        def min_edited():
            try:
                val = float(lineEdit_min.text())
                slider.setValue(int(val))
                self.logger.debug(f"{lineEdit_min.objectName()} => {slider.objectName()}.setValue({val})")
            except ValueError:
                self.logger.warning(f"Invalid float in {lineEdit_min.objectName()} => '{lineEdit_min.text()}'")

        def max_edited():
            try:
                val = float(lineEdit_max.text())
                slider.setMaximum(int(val))
                self.logger.debug(f"{lineEdit_max.objectName()} => {slider.objectName()}.setMaximum({val})")
            except ValueError:
                self.logger.warning(f"Invalid float in {lineEdit_max.objectName()} => '{lineEdit_max.text()}'")

        lineEdit_min.editingFinished.connect(min_edited)
        lineEdit_max.editingFinished.connect(max_edited)

        def slider_changed(value):
            lineEdit_min.setText(str(value))
            self.logger.debug(f"{slider.objectName()} => {lineEdit_min.objectName()}.setText({value})")

        slider.valueChanged.connect(slider_changed)


    def setup_prem_slider_pair(self, slider, lineEdit_min, lineEdit_max):
        """
        Specialized pairing for prem_slider using scaling:
        Internal slider range: 0 to 1,000,000.
        Each step represents PREM_SCALE (10,000) real units.
        """
        if not slider or not lineEdit_min or not lineEdit_max:
            self.logger.debug("setup_prem_slider_pair => missing widget(s), skipping.")
            return

        self.logger.debug(f"Linking prem_slider with {lineEdit_min.objectName()} / {lineEdit_max.objectName()} (scaled)")

        def min_edited():
            try:
                real_val = float(lineEdit_min.text())  # Real value, e.g. 5000000000
                scaled_val = int(real_val // PREM_SCALE)
                slider.setValue(scaled_val)
                self.logger.debug(f"{lineEdit_min.objectName()} => prem_slider.setValue({scaled_val}) from {real_val}")
            except ValueError:
                self.logger.warning(f"Invalid float in {lineEdit_min.objectName()} => '{lineEdit_min.text()}'")

        def max_edited():
            try:
                real_val = float(lineEdit_max.text())
                scaled_max = int(real_val // PREM_SCALE)
                slider.setMaximum(scaled_max)
                self.logger.debug(f"{lineEdit_max.objectName()} => prem_slider.setMaximum({scaled_max}) from {real_val}")
            except ValueError:
                self.logger.warning(f"Invalid float in {lineEdit_max.objectName()} => '{lineEdit_max.text()}'")

        lineEdit_min.editingFinished.connect(min_edited)
        lineEdit_max.editingFinished.connect(max_edited)

        def slider_changed(value):
            real_val = value * PREM_SCALE
            lineEdit_min.setText(str(real_val))
            self.logger.debug(f"prem_slider => {lineEdit_min.objectName()}.setText({real_val}) (scaled)")

        slider.valueChanged.connect(slider_changed)


    # --------------------------
    # APPLY / RESET / SAVE
    # --------------------------
    def on_apply_clicked(self):
        self.logger.debug("on_apply_clicked called.")
        filter_data = {}

        filter_data["volume_min"] = self.ui.vol_lineEdit_min.text() if hasattr(self.ui, "vol_lineEdit_min") else ""
        filter_data["volume_max"] = self.ui.vol_lineEdit_max.text() if hasattr(self.ui, "vol_lineEdit_max") else ""

        filter_data["oi_min"] = self.ui.oi_lineEdit_min.text() if hasattr(self.ui, "oi_lineEdit_min") else ""
        filter_data["oi_max"] = self.ui.oi_lineEdit_max.text() if hasattr(self.ui, "oi_lineEdit_max") else ""

        filter_data["premium_min"] = self.ui.prem_lineEdit_min.text() if hasattr(self.ui, "prem_lineEdit_min") else ""
        filter_data["premium_max"] = self.ui.prem_lineEdit_max.text() if hasattr(self.ui, "prem_lineEdit_max") else ""

        filter_data["strike_min"] = self.ui.strikePrice_lineEdit_min.text() if hasattr(self.ui, "strikePrice_lineEdit_min") else ""
        filter_data["strike_max"] = self.ui.strikePrice_lineEdit_max.text() if hasattr(self.ui, "strikePrice_lineEdit_max") else ""

        filter_data["lastPrice_min"] = self.ui.lastPrice_lineEdit_min.text() if hasattr(self.ui, "lastPrice_lineEdit_min") else ""
        filter_data["lastPrice_max"] = self.ui.lastPrice_lineEdit_max.text() if hasattr(self.ui, "lastPrice_lineEdit_max") else ""

        if hasattr(self.ui, "optionType_combo"):
            filter_data["option_type"] = self.ui.optionType_combo.currentText()
        else:
            filter_data["option_type"] = "All"

        self.logger.debug(f"on_apply_clicked => filter_data: {filter_data}")
        self.applyFilter.emit(filter_data)


    def on_reset_clicked(self):
        self.logger.debug("on_reset_clicked => clearing line edits & resetting sliders.")
        for widget_name in [
            "vol_lineEdit_min", "vol_lineEdit_max",
            "oi_lineEdit_min", "oi_lineEdit_max",
            "prem_lineEdit_min", "prem_lineEdit_max",
            "strikePrice_lineEdit_min", "strikePrice_lineEdit_max",
            "lastPrice_lineEdit_min", "lastPrice_lineEdit_max"
        ]:
            if hasattr(self.ui, widget_name):
                getattr(self.ui, widget_name).clear()

        # Reset slider values to 0 (keeping the maximums as set above)
        if hasattr(self.ui, "vol_slider"):
            self.ui.vol_slider.setValue(0)
        if hasattr(self.ui, "oi_slider"):
            self.ui.oi_slider.setValue(0)
        if hasattr(self.ui, "prem_slider"):
            self.ui.prem_slider.setValue(0)
        if hasattr(self.ui, "strikePrice_slider"):
            self.ui.strikePrice_slider.setValue(0)
        if hasattr(self.ui, "lastPrice_slider"):
            self.ui.lastPrice_slider.setValue(0)

        if hasattr(self.ui, "optionType_combo"):
            idx = self.ui.optionType_combo.findText("All")
            if idx >= 0:
                self.ui.optionType_combo.setCurrentIndex(idx)


    def on_save_clicked(self):
        """
        Prompt user for a preset name, apply the filters to the table,
        and either overwrite or create a new preset in JSON + combo.
        """
        self.logger.debug("on_save_clicked => user wants to save a preset AND apply filters.")
        
        # 1) Gather filter data
        filter_data = self.collect_filter_data()
        self.logger.debug(f"Current filter_data => {filter_data}")

        # 2) Apply the filter data immediately (like the 'Apply' button)
        self.logger.debug("Applying filter data to the table (like 'Apply' button).")
        self.applyFilter.emit(filter_data)

        # 3) Ask for a preset name
        name, ok = QInputDialog.getText(self, "Save Preset", "Enter Preset Name:",
                                        QLineEdit.Normal, "")
        if not ok or not name.strip():
            self.logger.debug("User canceled or blank preset name. Done.")
            return

        chosen_name = name.strip()
        self.logger.debug(f"User entered preset name: {chosen_name}")

        # 4) Check for an existing preset (case-insensitive)
        existing_index = next((i for i, p in enumerate(self.loaded_presets)
                                if p["name"].lower() == chosen_name.lower()), None)

        if existing_index is not None:
            # Confirm overwrite
            overwrite = QMessageBox.question(
                self,
                "Overwrite Existing Preset?",
                f"A preset named '{chosen_name}' already exists.\nDo you want to overwrite it?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if overwrite == QMessageBox.No:
                self.logger.debug("User canceled overwrite. Aborting save.")
                return
            else:
                self.logger.debug(f"Overwriting existing preset: {chosen_name}")
                self.loaded_presets[existing_index]["data"] = filter_data
                self.save_presets_to_json(self.loaded_presets)
                self.rebuild_preset_combo()
                # Since combo index is offset by 1 (index 0 is the label),
                # the preset is at index existing_index + 1.
                combo_index = existing_index + 1
                self.ui.preset_combo.setCurrentIndex(combo_index)
                return

        # Otherwise, create a new preset.
        new_preset = {"name": chosen_name, "data": filter_data}
        self.logger.debug(f"new_preset => {new_preset}")

        self.loaded_presets.append(new_preset)
        self.save_presets_to_json(self.loaded_presets)

        if hasattr(self.ui, "preset_combo"):
            # Insert after the label (index 0)
            insert_index = self.ui.preset_combo.count()
            self.logger.debug(f"Adding new preset => {chosen_name} at index={insert_index}")
            self.ui.preset_combo.insertItem(insert_index, chosen_name)
            self.ui.preset_combo.setCurrentIndex(insert_index)


    def rebuild_preset_combo(self):
        # Clear all items except the first ("Preset" label)
        while self.ui.preset_combo.count() > 1:
            self.ui.preset_combo.removeItem(self.ui.preset_combo.count() - 1)
        # Re-add each loaded preset
        for p in self.loaded_presets:
            idx = self.ui.preset_combo.count()
            self.ui.preset_combo.insertItem(idx, p["name"])


    def on_preset_combo_changed(self, index):
        self.logger.debug(f"on_preset_combo_changed => index={index}")
        if index == 0:
            self.logger.debug("User clicked 'Preset' label => ignoring.")
            return

        # Offset because index 0 is the label.
        offset = index - 1
        if offset < 0 or offset >= len(self.loaded_presets):
            self.logger.debug(f"Offset {offset} out of range for loaded_presets.")
            return

        chosen_preset = self.loaded_presets[offset]
        self.logger.debug(f"Chosen preset => {chosen_preset}")
        self.load_filter_data(chosen_preset["data"])


    def collect_filter_data(self):
        self.logger.debug("collect_filter_data called.")
        data = {}
        if hasattr(self.ui, "vol_lineEdit_min"):
            data["volume_min"] = self.ui.vol_lineEdit_min.text()
        if hasattr(self.ui, "vol_lineEdit_max"):
            data["volume_max"] = self.ui.vol_lineEdit_max.text()

        if hasattr(self.ui, "oi_lineEdit_min"):
            data["oi_min"] = self.ui.oi_lineEdit_min.text()
        if hasattr(self.ui, "oi_lineEdit_max"):
            data["oi_max"] = self.ui.oi_lineEdit_max.text()

        if hasattr(self.ui, "prem_lineEdit_min"):
            data["premium_min"] = self.ui.prem_lineEdit_min.text()
        if hasattr(self.ui, "prem_lineEdit_max"):
            data["premium_max"] = self.ui.prem_lineEdit_max.text()

        if hasattr(self.ui, "strikePrice_lineEdit_min"):
            data["strike_min"] = self.ui.strikePrice_lineEdit_min.text()
        if hasattr(self.ui, "strikePrice_lineEdit_max"):
            data["strike_max"] = self.ui.strikePrice_lineEdit_max.text()

        if hasattr(self.ui, "lastPrice_lineEdit_min"):
            data["lastPrice_min"] = self.ui.lastPrice_lineEdit_min.text()
        if hasattr(self.ui, "lastPrice_lineEdit_max"):
            data["lastPrice_max"] = self.ui.lastPrice_lineEdit_max.text()

        if hasattr(self.ui, "optionType_combo"):
            data["option_type"] = self.ui.optionType_combo.currentText()
        else:
            data["option_type"] = "All"

        self.logger.debug(f"collect_filter_data => {data}")
        return data


    def load_filter_data(self, filter_data: dict):
        self.logger.debug(f"load_filter_data => {filter_data}")
        if hasattr(self.ui, "vol_lineEdit_min") and "volume_min" in filter_data:
            self.ui.vol_lineEdit_min.setText(filter_data["volume_min"])
        if hasattr(self.ui, "vol_lineEdit_max") and "volume_max" in filter_data:
            self.ui.vol_lineEdit_max.setText(filter_data["volume_max"])

        if hasattr(self.ui, "oi_lineEdit_min") and "oi_min" in filter_data:
            self.ui.oi_lineEdit_min.setText(filter_data["oi_min"])
        if hasattr(self.ui, "oi_lineEdit_max") and "oi_max" in filter_data:
            self.ui.oi_lineEdit_max.setText(filter_data["oi_max"])

        if hasattr(self.ui, "prem_lineEdit_min") and "premium_min" in filter_data:
            self.ui.prem_lineEdit_min.setText(filter_data["premium_min"])
        if hasattr(self.ui, "prem_lineEdit_max") and "premium_max" in filter_data:
            self.ui.prem_lineEdit_max.setText(filter_data["premium_max"])

        if hasattr(self.ui, "strikePrice_lineEdit_min") and "strike_min" in filter_data:
            self.ui.strikePrice_lineEdit_min.setText(filter_data["strike_min"])
        if hasattr(self.ui, "strikePrice_lineEdit_max") and "strike_max" in filter_data:
            self.ui.strikePrice_lineEdit_max.setText(filter_data["strike_max"])

        if hasattr(self.ui, "lastPrice_lineEdit_min") and "lastPrice_min" in filter_data:
            self.ui.lastPrice_lineEdit_min.setText(filter_data["lastPrice_min"])
        if hasattr(self.ui, "lastPrice_lineEdit_max") and "lastPrice_max" in filter_data:
            self.ui.lastPrice_lineEdit_max.setText(filter_data["lastPrice_max"])

        if hasattr(self.ui, "optionType_combo") and "option_type" in filter_data:
            idx = self.ui.optionType_combo.findText(filter_data["option_type"])
            if idx >= 0:
                self.ui.optionType_combo.setCurrentIndex(idx)
        self.logger.debug("load_filter_data => done.")


    def load_presets_from_json(self):
        self.logger.debug(f"load_presets_from_json => {self.presets_file_path}")
        dir_name = os.path.dirname(self.presets_file_path)
        if not os.path.exists(dir_name):
            self.logger.debug(f"Presets directory not found => {dir_name}")
            return []

        if not os.path.exists(self.presets_file_path):
            self.logger.debug("No presets file found => returning empty.")
            return []

        try:
            with open(self.presets_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("presets", [])
        except Exception as e:
            self.logger.warning(f"Could not load presets JSON: {e}")
            return []


    def save_presets_to_json(self, presets_list):
        self.logger.debug(f"save_presets_to_json => {presets_list}")
        data = {"presets": presets_list}
        dir_name = os.path.dirname(self.presets_file_path)
        os.makedirs(dir_name, exist_ok=True)  # ensure path exists
        try:
            with open(self.presets_file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self.logger.debug(f"Presets saved to {self.presets_file_path}.")
        except Exception as e:
            self.logger.error(f"Could not save presets to JSON: {e}")
