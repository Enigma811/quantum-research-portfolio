"""Reproduce Figs. 1-2 style plots: honeycomb lattice + slicing scheme for
armchair and zigzag edge orientations."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from lattice import build_ribbon, EDGE_THETA

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(13, 6))
for ax, edge in zip(axes, ["zigzag", "armchair"]):
    theta = EDGE_THETA[edge]
    slices, bonds, pos, sub, slice_of, n_bad = build_ribbon(Lx=16, Ly=12, theta_deg=theta)
    cmap = plt.cm.tab20(np.linspace(0, 1, 20))
    for n in range(len(slices)):
        c = cmap[n % 20]
        idx = slices[n]["global_idx"]
        ax.scatter(pos[idx, 0], pos[idx, 1], color=c, s=25, zorder=3,
                   edgecolors="k", linewidths=0.3)
    for i, j in bonds:
        ax.plot([pos[i, 0], pos[j, 0]], [pos[i, 1], pos[j, 1]], color="gray", lw=0.6, zorder=1)
    ax.set_title(f"{edge}-edge ribbon\n({len(slices)} RGF slices, bad couplings = {n_bad})")
    ax.set_aspect("equal")
    ax.set_xlabel("x"); ax.set_ylabel("y")

plt.tight_layout()
outpath = os.path.join(OUT, "honeycomb_graphene_lattice_and_slicing.png")
plt.savefig(outpath, dpi=150)
print("saved", outpath)
