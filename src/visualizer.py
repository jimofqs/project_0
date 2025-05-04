import pandapower.plotting.plotly as pplotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pandapower as pp
import os

def assign_default_geodata(net):
    if hasattr(net, "bus_geodata") and not net.bus_geodata.empty:
        return
    n = len(net.bus)
    angle = np.linspace(0, 2 * np.pi, n, endpoint=False)
    net.bus_geodata = pd.DataFrame({
        "x": np.cos(angle),
        "y": np.sin(angle)
    }, index=net.bus.index)

def run_power_flow(net):
    pp.runpp(net)

def plot_tech_style(net):
    assign_default_geodata(net)
    run_power_flow(net)

    fig = go.Figure()

    # Plot lines with color by loading
    for _, line in net.line.iterrows():
        from_bus = line.from_bus
        to_bus = line.to_bus
        x0, y0 = net.bus_geodata.loc[from_bus, ['x', 'y']]
        x1, y1 = net.bus_geodata.loc[to_bus, ['x', 'y']]
        loading = net.res_line.loading_percent.at[line.name]

        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1],
            mode="lines",
            line=dict(width=2 + loading / 50, color="cyan" if loading < 80 else "red"),
            hoverinfo="text",
            text=f"Line {line.name}<br>Loading: {loading:.1f}%",
            showlegend=False
        ))

    # Plot buses with color by voltage
    for idx, row in net.bus.iterrows():
        x, y = net.bus_geodata.loc[idx, ['x', 'y']]
        vm_pu = net.res_bus.vm_pu.at[idx]
        name = row.name

        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers+text",
            marker=dict(
                size=12,
                color=vm_pu,
                colorscale='Electric',
                cmin=0.95, cmax=1.05,
                colorbar=dict(title="Voltage (pu)")
            ),
            text=f"Bus {name}<br>V = {vm_pu:.3f} pu",
            textposition="top center",
            hoverinfo="text",
            showlegend=False
        ))

    fig.update_layout(
        title="🚀 Tech-Style Power Grid Visualization",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        hovermode="closest"
    )

    fig.show()

if __name__ == "__main__":
    from grid_builder import load_network_from_json
    net = load_network_from_json("ieee9bus.json")
    plot_tech_style(net)
