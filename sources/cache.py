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
            c = pickle.load(f)
        assert isinstance(c, Cache)
        return c

    def save_cache(self, file_path: Path):
        with file_path.open("wb") as f:
            pickle.dump(self, f)