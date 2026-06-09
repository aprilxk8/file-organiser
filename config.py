#map file extensions to categories

import json

def load_file_types():
    with open("config.json", "r") as f:
        return json.load(f)