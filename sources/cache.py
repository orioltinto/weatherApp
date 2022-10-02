from pathlib import Path
import pickle


class Cache:
    def __init__(self):
        self.raw_data = {}
        self.probabilities = {}
        self.figures = {}

    @staticmethod
    def from_file(file_path: Path):
        with file_path.open("rb") as f:
            _cache = pickle.load(f)
        assert isinstance(_cache, Cache)
        return _cache

    def save_cache(self, file_path: Path):
        with file_path.open("wb") as f:
            pickle.dump(self, f)
