# src/grid_builder.py

import pandapower as pp
import pandapower.networks as pn
import pandapower.converter as pc
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def create_ieee9bus():
    """Create IEEE 9-bus system using pandapower's built-in function."""
    net = pn.case9()
    return net


def save_network_to_json(net, filename):
    """Save a pandapower network to a JSON file."""
    path = os.path.join(DATA_DIR, filename)
    pp.to_json(net, path)
    print(f"Network saved to {path}")


def load_network_from_json(filename):
    """Load a pandapower network from a JSON file."""
    path = os.path.join(DATA_DIR, filename)
    net = pp.from_json(path)
    print(f"Network loaded from {path}")
    return net


if __name__ == "__main__":
    # Example usage
    net = create_ieee9bus()
    save_network_to_json(net, "ieee9bus.json")
    
    # Test loading
    loaded_net = load_network_from_json("ieee9bus.json")
