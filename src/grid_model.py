import json
import sqlite3
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx

# === Classes ===
class Bus:
    def __init__(self, bus_id, bus_type, V=None, angle=None):
        self.id = bus_id
        self.type = bus_type
        self.V = V
        self.angle = angle

class Generator:
    def __init__(self, bus, Pg):
        self.bus = bus
        self.Pg = Pg

class Load:
    def __init__(self, bus, Pd, Qd):
        self.bus = bus
        self.Pd = Pd
        self.Qd = Qd

class Branch:
    def __init__(self, from_bus, to_bus, R, X, B):
        self.from_bus = from_bus
        self.to_bus = to_bus
        self.R = R
        self.X = X
        self.B = B

# === Load JSON ===
def load_grid_model(json_path: str):
    with open(json_path, 'r') as f:
        return json.load(f)

# === Save to SQLite ===
def save_to_sqlite(data, db_path: str):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create tables
    c.execute("DROP TABLE IF EXISTS buses")
    c.execute("DROP TABLE IF EXISTS generators")
    c.execute("DROP TABLE IF EXISTS loads")
    c.execute("DROP TABLE IF EXISTS branches")

    c.execute("""CREATE TABLE buses (id INTEGER, type TEXT, V REAL, angle REAL)""")
    c.execute("""CREATE TABLE generators (bus INTEGER, Pg REAL)""")
    c.execute("""CREATE TABLE loads (bus INTEGER, Pd REAL, Qd REAL)""")
    c.execute("""CREATE TABLE branches (from_bus INTEGER, to_bus INTEGER, R REAL, X REAL, B REAL)""")

    # Insert data
    for b in data["buses"]:
        c.execute("INSERT INTO buses VALUES (?, ?, ?, ?)", 
                  (b["id"], b["type"], b.get("V"), b.get("angle")))

    for g in data["generators"]:
        c.execute("INSERT INTO generators VALUES (?, ?)", 
                  (g["bus"], g["Pg"]))

    for l in data["loads"]:
        c.execute("INSERT INTO loads VALUES (?, ?, ?)", 
                  (l["bus"], l["Pd"], l["Qd"]))

    for br in data["branches"]:
        c.execute("INSERT INTO branches VALUES (?, ?, ?, ?, ?)", 
                  (br["from"], br["to"], br["R"], br["X"], br["B"]))

    conn.commit()
    conn.close()

# === Plot Grid Topology ===
def plot_topology(branches):
    G = nx.Graph()
    for br in branches:
        G.add_edge(br["from"], br["to"])
    
    pos = nx.spring_layout(G, seed=42)  # 用 spring layout 畫圖
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=10, font_weight='bold')
    plt.title("IEEE 9-Bus Grid Topology")
    plt.show()

# === Main ===
if __name__ == "__main__":
    base = Path(__file__).parent.parent
    json_path = base / "data" / "ieee9bus.json"
    db_path = base / "database" / "ieee9bus.db"

    data = load_grid_model(str(json_path))
    print("✅ Grid model loaded!")

    save_to_sqlite(data, str(db_path))
    print("✅ Data saved to SQLite!")

    plot_topology(data["branches"])
