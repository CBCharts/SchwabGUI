import json

class DataController:
    def __init__(self, data_path):
        self.data_path = data_path

    def load_data(self):
        """Load data from JSON."""
        with open(self.data_path, "r") as f:
            return json.load(f)
