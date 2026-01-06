import time
import json
import os


class BookmarkManager:
    def __init__(self, output_base_name="recording"):
        self.start_time = time.time()
        self.bookmarks = []

        self.file_path = f"{output_base_name}_bookmarks.json"

    def add(self, note=""):
        t = time.time() - self.start_time
        self.bookmarks.append({
            "time_seconds": round(t, 2),
            "note": note
        })

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.bookmarks, f, indent=4)
