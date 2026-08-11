"""
Reproduce report-style conductance figures:
  (a) Conductance quantization: T(E) for a clean, uniformly-doped ribbon
      (both edge types) -- the RGF analogue of counting open ballistic modes.
  (b) The "Fig. 3"-style scan: conductance vs contact Fermi energy V_lead,
      for an UNDOPED device (E=0, Dirac point) contacted by leads whose
      on-site energy (doping) is swept. For a short & wide, clean graphene
      sample this is expected to show the pseudo-diffusive minimum
      conductivity sigma_min -> (4/pi)*(4e^2/h) [Tworzydlo et al. 2006,
      ref. 6 in the report] as a roughly flat dip around V_lead=0, rising
      away from it. We show the approach to this limit as the sample is
      made progressively shorter & wider (increasing M/N), analogous to the
      report's comparison across N = 12...200 at fixed M.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from transport import GrapheneRibbon

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------
# (a) Conductance quantization vs Fermi energy, clean ribbon
# ---------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, edge in zip(axes, ["zigzag", "armchair"]):
    rib = GrapheneRibbon(Lx=20, Ly=40, edge=edge, t=1.0)
    Es = np.linspace(-3.0, 3.0, 400)
    t0 = time.time()
    Ts = rib.conductance_scan(Es)
    print(f"{edge}: N={rib.N} slices, width~{max(rib.widths)}, scan time {time.time()-t0:.1f}s")
    ax.plot(Es, Ts, lw=1.2)
    ax.set_xlabel("E / t")
    ax.set_ylabel(r"$T(E)$  (conductance in units of $2e^2/h$)")
    ax.set_title(f"{edge}-edge ribbon (clean, ballistic)\nM$\\approx${max(rib.widths)}, N={rib.N} slices")
plt.tight_layout()
p1 = os.path.join(OUT, "conductance_vs_fermi_energy_clean_ribbon.png")
plt.savefig(p1, dpi=150)
plt.close(fig)
print("saved", p1)

# ---------------------------------------------------------------
# (b) Pseudo-diffusive minimum conductivity vs contact doping V_lead
#     device fixed at the Dirac point (E=0), for several sample lengths
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5.5))
Vs = np.linspace(-2.5, 2.5, 41)
Lx_list = [8, 14, 20]  # increasing length N at fixed width -> approach to the diffusive-like limit is from SHORT samples, so we scan short -> longer
colors = plt.cm.viridis(np.linspace(0.15, 0.85, len(Lx_list)))

for Lx, c in zip(Lx_list, colors):
    sigmas = []
    t0 = time.time()
    for V in Vs:
        rib = GrapheneRibbon(Lx=Lx, Ly=120, edge="armchair", t=1.0,
                              onsite=0.0, lead_onsite_shift=V)
        sigmas.append(rib.transmission(0.0))
    sigmas = np.array(sigmas)
    print(f"Lx={Lx}: N={rib.N} slices, width~{max(rib.widths)}, "
          f"sigma(V=0)={sigmas[len(Vs)//2]:.3f}, scan time {time.time()-t0:.1f}s")
    ax.plot(Vs, sigmas, color=c, marker="o", ms=3, lw=1.2,
             label=f"N={rib.N} slices (M$\\approx${max(rib.widths)})")

ax.axhline(4 / np.pi, color="k", ls="--", lw=1, label=r"$4/\pi$ (universal limit)")
ax.set_xlabel(r"$V_{\rm lead}/t$")
ax.set_ylabel(r"$\sigma\,/\,(4e^2/h)$")
ax.set_title("Undoped (Dirac-point) device, doped contacts\n"
             "approach to the pseudo-diffusive minimum conductivity")
ax.legend()
plt.tight_layout()
p2 = os.path.join(OUT, "conductance_vs_lead_fermi_energy_pseudo_diffusive.png")
plt.savefig(p2, dpi=150)
plt.close(fig)
print("saved", p2)
