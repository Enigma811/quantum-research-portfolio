"""Local density of states (LDOS) map from the RGF diagonal blocks."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from transport import GrapheneRibbon

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)

rib = GrapheneRibbon(Lx=20, Ly=30, edge="armchair", t=1.0)
print("N slices", rib.N, "width", max(rib.widths))

energies = [0.3, 1.0]
fig, axes = plt.subplots(1, len(energies), figsize=(6 * len(energies), 6))
if len(energies) == 1:
    axes = [axes]

for ax, E in zip(axes, energies):
    rho = rib.ldos(E)  # list of per-slice arrays
    xs, ys, vals = [], [], []
    for n, s in enumerate(rib.merged_slices):
        pos = s["pos"]
        xs.extend(pos[:, 0])
        ys.extend(pos[:, 1])
        vals.extend(rho[n])
    sc = ax.scatter(xs, ys, c=vals, cmap="inferno", s=28, edgecolors="none")
    ax.set_aspect("equal")
    ax.set_title(f"LDOS at E = {E:.2f} t")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    plt.colorbar(sc, ax=ax, label=r"$\rho(E)$ (states / t / site)")

plt.tight_layout()
p = os.path.join(OUT, "local_density_of_states.png")
plt.savefig(p, dpi=150)
print("saved", p)
