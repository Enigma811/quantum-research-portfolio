# RGF for Graphene — conductance and LDOS code

Python implementation of the recursive Green's-function (RGF) method for
ballistic quantum transport, applied to single-layer graphene nanoribbons,
following the structure of the project report (Choubey, NISER, 2024).

## Structure

```
src/
  lattice.py               : honeycomb lattice generator, ribbon slicing, block-tridiagonal H
  leads.py                 : Sancho-Rubio decimation, lead self-energies, Gamma matrices
  rgf.py                   : forward/backward RGF sweeps, transmission, LDOS diagonal blocks
  transport.py             : GrapheneRibbon: high-level class tying everything together
  run_lattice_figures.py   : Fig 1/2-style lattice + slicing plot
  run_conductance.py       : Fig 3-style conductance plots
  run_ldos.py              : LDOS map
  README.md
```

## Method summary / conventions

- **Lattice**: honeycomb, nearest-neighbour hopping `t`, bond vectors
  `delta1=(0,1)`, `delta2=(sqrt(3)/2,-1/2)`, `delta3=(-sqrt(3)/2,-1/2)`.
- **Ribbons**: a rectangular window is cut from an (optionally rotated)
  infinite sheet, then partitioned into slices by x-coordinate.
  `theta=0` gives **zigzag edges**; `theta=30 deg` gives **armchair edges**.
  Because bonds only connect neighbouring slices, the Hamiltonian is exactly
  block-tridiagonal.
  Armchair ribbons have a natural 2-slice period (alternating slice widths),
  so raw slices are merged pairwise (`merge_slices`) before use — the "efficient slicing" scheme from the report.
- **Leads**: semi-infinite, ideal contacts made of the ribbon's own end
  unit cell (same hopping/geometry as the device, with an optional uniform
  on-site shift `lead_onsite_shift` to model doped/gated contacts). Surface
  Green's functions via Sancho-Rubio decimation; self-energies
  $\Sigma_L = u^\dagger g_L u$, $\Sigma_R = u g_R u^\dagger$.
- **RGF**: forward (left-connected) and backward (right-connected) sweeps;
  transmission from the boundary block $G_{N-1,0}$ (Fisher-Lee/Caroli
  formula); full diagonal blocks for LDOS
  by combining left+right sweeps at each slice.

## Validation performed

Both the transmission and the LDOS diagonal blocks were checked against a
brute-force calculation (building the full open-system Hamiltonian,
including both lead self-energies, as one dense matrix and inverting it
directly) on small test ribbons — **agreement to $~1e-16$** (machine
precision), confirming the recursive formulas are implemented correctly.
Additional physics sanity checks:
- A clean $1D$ chain gives $T=1$ inside the band, $0$ outside.
- Clean graphene ribbons show the expected van Hove conductance peaks at
  $E = \pm t$ and particle-hole symmetry.
- Zigzag ribbons show the well-known single conducting edge-state mode
  pinned near the Dirac point.
- An undoped, short-and-wide sample with doped contacts approaches the
  universal pseudo-diffusive minimum conductivity $4/\pi$ (Tworzydlo et al.
  2006, ref. [6] in the report) as the width/length ratio grows — this is
  exactly the effect shown in the top panel of the report's Fig. 3.

## Scaling of parameters $(M, N)$

RGF cost scales as $O(N * M^3)$ for dense per-slice blocks of width `M`
(each slice requires one `M x M` matrix inversion).

## What's NOT produced

- Exact lead-contact model, disorder, interactions, finite temperature,
next-nearest-neighbour hopping — noted in the report as discussed
conceptually but not necessarily implemented in the project/code.
