
import json
from pathlib import Path


class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.config_path = Path(config_path)
        self.data = self._load()

    def _load(self):
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def all(self):
        return self.data
