# FPUT recurrence — classical chain simulation

Python implementation of the Fermi–Pasta–Ulam–Tsingou (FPUT) problem for fixed-end chains with quadratic, cubic, and quartic nearest-neighbour interactions, using a Störmer–Verlet/leapfrog integrator and normal-mode diagnostics as in the associated project report.

## Structure

```
src/
  FPUT_classical.py               : lattice construction, time integration, mode/energy diagnostics, animations + summary plots
```

- All production runs (linear control, cubic FPUT-α, quartic FPUT-β, and mixed α–β cases) are driven by `FPUT_classical.py` with parameter blocks edited directly in the script.


## Model and conventions

- **Lattice**: $1-D$ chain with $N$ unit-mass particles and fixed Dirichlet boundaries; the simulated sizes are $N=32$ and $N=64$.
- **Interactions**: nearest-neighbour potential with harmonic, cubic, and quartic contributions,
  $V(r) = \tfrac{1}{2} r^2 + \alpha \tfrac{1}{3} r^3 + \beta \tfrac{1}{4} r^4 $
  in the report’s convention (code uses the same schematic α/β control, with exact prefactors documented there).
- **Boundary conditions**: end sites are pinned to zero displacement after every timestep update (`x[0] = x[-1] = 0`), enforcing fixed ends throughout the simulation.
- **Initial condition**: energy is concentrated in the fundamental long-wavelength normal mode $k = 1$; amplitudes are scaled with $N$ to keep the initial energy comparable across $N = 32$ and $N = 64$.
- **Nonlinearity parameters**: representative runs include
  - linear control with $\alpha = 0, \beta = 0$,
  - weak and moderate cubic nonlinearity around $\alpha \approx 0.3$–$0.5$,
  - strong cubic runs with $\alpha \approx 0.9$–$1.1$,
  - pure quartic runs with $\beta = 0.6, 1.1$,
  - a mixed strong-nonlinearity case with $\alpha = 0.9, \beta = 1.1, N = 64$.
- **Time horizon and step**: long runs up to $t_{\max} \sim 10^5$ in simulation units are performed with a fixed timestep `dt` (e.g. `dt = 0.4`), chosen to balance energy conservation with computational cost.

## Numerical method

- **Integrator**: second-order, time-reversible Störmer–Verlet/leapfrog scheme for the lattice equations of motion; the update in the report is $y_n(t+\Delta t) = 2 y_n(t) - y_n(t-\Delta t) + \Delta t^2 F_n[y(t)],$
  and the code implements the same central-difference structure for the positions.
- **Time-reversibility and symplecticity**: the method is symplectic and time-reversible, which yields bounded energy fluctuations over long runs and suppresses secular energy drift in the Hamiltonian dynamics regime considered.
- **Diagnostics in code**:
  - total energy of the chain via a time-centred velocity estimate and nearest-neighbour potential energy,
  - per-mode energies for $k = 1, 2, 3, \dots$ using a discrete sine transform consistent with fixed-end boundary conditions,
  - real-space displacement profiles $x_n(t)$,
  - simple recurrence and leakage indicators via mode-energy time series.

## Validation performed

- **Linear control run** ($\alpha = 0, \beta = 0$, $N = 32$): mode 1 energy remains essentially constant, mode 2 stays unexcited, and total energy is stable over the full time horizon, validating the initial-condition construction and mode-energy diagnostic.
- **Energy conservation**: total-energy traces show bounded oscillations without systematic drift for the reported timesteps, consistent with the use of a symplectic leapfrog integrator at appropriately small `dt`.
- **Physics sanity checks**:
  - weak-to-moderate cubic nonlinearity produces the canonical FPUT near-recurrence—energy leaves mode 1, populates low-order modes (especially mode 2), and returns close to the initial mode;
  - strong cubic coupling and increased chain length ($N = 64$) lead to noisier recurrence traces and enhanced leakage into higher modes;
  - pure quartic runs show extended two-mode beating before eventual degradation at stronger $\beta$.

## Scaling with system size and runtime

- Computational cost scales linearly with particle number $N$ and with the number of timesteps in the simulation, since each update step applies local finite-difference operations to the full chain and updates a fixed number of mode-energy diagnostics.
- Long recurrence studies ($t_{\max} \sim 10^5$) therefore require careful choice of `dt` and output sampling to keep runtimes manageable while preserving the relevant nonlinear dynamics.

## What’s NOT implemented here

- Systematic parameter scans over initial energy, phase, chain length, and nonlinear coefficients are not automated in this script; runs are configured manually via the parameter block.
- Asymptotic equipartition plateaus at very long times and very strong nonlinearity are not established for every case; the focus is on the transition from clean near-recurrence to irregular broadband mode mixing in a representative parameter set.
- Quantitative fitting of lattice profiles to exact continuum KdV / modified KdV / Gardner soliton solutions is not part of the code; the connection to these integrable equations is derived and discussed in the report rather than implemented numerically here.
