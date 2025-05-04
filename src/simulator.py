# src/simulator.py
import os
import pandapower as pp
import pandapower.networks as pn


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_network_from_json(filename):
    """Load a pandapower network from a JSON file."""
    path = os.path.join(DATA_DIR, filename)
    net = pp.from_json(path)
    print(f"Network loaded from {path}")
    return net


def run_power_flow(net):
    """Run a power flow calculation on the given network."""
    pp.runpp(net)
    print("Power flow calculation completed.")
    return net


def display_results(net):
    """Display key results after power flow."""
    print("\n=== Bus Voltages ===")
    print(net.res_bus[["vm_pu", "va_degree"]])

    print("\n=== Line Loadings ===")
    print(net.res_line[["loading_percent"]])


if __name__ == "__main__":
    # Example usage
    net = load_network_from_json("ieee9bus.json")
    net = run_power_flow(net)
    display_results(net)
