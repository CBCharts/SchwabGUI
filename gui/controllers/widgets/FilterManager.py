from PySide6.QtCore import QObject, Signal
from gui.controllers.widgets.ZeroPanelWidget import ZeroPanelWidget
from gui.controllers.widgets.FullPanelWidget import FullPanelWidget
from gui.controllers.widgets.MCPriWidget import MCPriWidget

class FilterManager(QObject):
    # This signal will emit the consolidated filter data
    filtersUpdated = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.zeroPanel = ZeroPanelWidget()
        self.fullPanel = FullPanelWidget()
        self.mcPriPanel = MCPriWidget()

        # Only connect if the widget has an applyFilter signal
        if hasattr(self.zeroPanel, "applyFilter"):
            self.zeroPanel.applyFilter.connect(self.updateFilters)
        if hasattr(self.fullPanel, "applyFilter"):
            self.fullPanel.applyFilter.connect(self.updateFilters)
        if hasattr(self.mcPriPanel, "applyFilter"):
            self.mcPriPanel.applyFilter.connect(self.updateFilters)

    def updateFilters(self, new_filter_data: dict):
        """
        This slot is called whenever any filter widget applies its settings.
        You can merge settings from multiple widgets if desired.
        For now, we simply forward the new filter data.
        """
        self.filtersUpdated.emit(new_filter_data)
