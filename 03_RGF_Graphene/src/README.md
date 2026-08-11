# RGF for Graphene — reproduction code

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
```

## Method summary / conventions

- **Lattice**: honeycomb, nearest-neighbour hopping `t`, bond vectors
  `delta1=(0,1)`, `delta2=(sqrt(3)/2,-1/2)`, `delta3=(-sqrt(3)/2,-1/2)`
  (matches Fig. 1 of the report — B1 top, B2/B3 lower-right/left).
- **Ribbons**: a rectangular window is cut from an (optionally rotated)
  infinite sheet, then partitioned into slices by x-coordinate.
  `theta=0` gives **zigzag edges**; `theta=30 deg` gives **armchair edges**
  (verified visually — see [armchair_slice](figures/armchair_slice.png)).
  Because bonds only connect neighbouring slices, the Hamiltonian is exactly
  block-tridiagonal — no manual index bookkeeping needed.
  Armchair ribbons have a natural 2-slice period (alternating slice widths),
  so raw slices are merged pairwise (`merge_slices`) before use — this is
  the same "efficient slicing" idea shown in Fig. 2 of the report.
  `find_commensurate_size` auto-snaps a requested (Lx, Ly) to the nearest
  size giving a perfectly uniform (periodic) ribbon, since leads must be
  made of an exactly repeating unit cell.
- **Leads**: semi-infinite, ideal contacts made of the ribbon's own end
  unit cell (same hopping/geometry as the device, with an optional uniform
  on-site shift `lead_onsite_shift` to model doped/gated contacts). Surface
  Green's functions via Sancho-Rubio decimation; self-energies
  `Sigma_L = u^dagger g_L u`, `Sigma_R = u g_R u^dagger`.
- **RGF**: forward (left-connected) and backward (right-connected) sweeps;
  transmission from the boundary block `G_{N-1,0}` (Fisher-Lee/Caroli
  formula `T = Tr[Gamma_L G^r Gamma_R G^a]`); full diagonal blocks for LDOS
  by combining left+right sweeps at each slice (Sec. 4.4 of the report).

## Validation performed

Both the transmission and the LDOS diagonal blocks were checked against a
brute-force calculation (building the full open-system Hamiltonian,
including both lead self-energies, as one dense matrix and inverting it
directly) on small test ribbons — **agreement to ~1e-16** (machine
precision), confirming the recursive formulas are implemented correctly.
Additional physics sanity checks:
- A clean 1D chain gives T=1 inside the band, 0 outside.
- Clean graphene ribbons show the expected van Hove conductance peaks at
  E = ±t and particle-hole symmetry.
- Zigzag ribbons show the well-known single conducting edge-state mode
  pinned near the Dirac point.
- An undoped, short-and-wide sample with doped contacts approaches the
  universal pseudo-diffusive minimum conductivity `4/pi` (Tworzydlo et al.
  2006, ref. [6] in the report) as the width/length ratio grows — this is
  exactly the effect shown in the top panel of the report's Fig. 3.

## Reproducing the figures

```bash
conda env create -f environment.yml
conda activate rgf-graphene
python src/run_lattice_figures.py     # lattice + slicing (Figs. 1-2 style)
python src/run_conductance.py         # conductance plots (Fig. 3 style)
python src/run_ldos.py                # LDOS map
```

## Scaling up to your report's parameters (M=360, N=70)

The demo scripts use modest ribbon sizes (M ~ 25-140 atoms, N ~ 6-24
slices) so the full set of figures runs in well under a minute on a laptop.
RGF cost scales as `O(N * M^3)` for dense per-slice blocks of width `M`
(each slice requires one `M x M` matrix inversion), so `M=360` is roughly
`(360/140)^3 ≈ 17x` more expensive per energy point than the widest demo
here, and `N=70` is a longer sweep — reproducing the exact report figure
should still be very feasible (each energy point on the order of a second
or so), just increase `Lx`, `Ly` in `run_conductance.py` accordingly and
expect the sweep to take longer. Both `theta=0/30` edge conventions were
verified by eye — if your own code's "armchair"/"zigzag" labeling turns
out to be swapped relative to this one, just swap the `edge=` argument.

## What's NOT reproduced

- Exact figure sizes/parameters from your original report (M=360, N=70,
  and the specific square-lattice-contact comparison) — these require
  your exact lead-contact model, which wasn't in the material provided.
- Disorder, interactions, finite temperature, next-nearest-neighbour
  hopping — noted in the report as discussed conceptually but not
  necessarily implemented in the original repository either.
