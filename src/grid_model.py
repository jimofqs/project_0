import json
from pathlib import Path

def load_grid_model(json_path: str):
    with open(json_path, 'r') as f:
        grid_data = json.load(f)
    return grid_data

if __name__ == "__main__":
    path = Path(__file__).parent.parent / "data" / "ieee9bus.json"
    model = load_grid_model(str(path))
    print("Grid Model Loaded:")
    print(json.dumps(model, indent=2))
