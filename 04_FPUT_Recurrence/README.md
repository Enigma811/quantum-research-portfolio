# Fermi–Pasta–Ulam–Tsingou Recurrence, Solitons, and Chaos Onset

## Project summary

This project presents a numerical and theoretical investigation of the Fermi–Pasta–Ulam–Tsingou (FPUT) problem. A fixed-end chain of classical particles coupled by anharmonic nearest-neighbour springs is initialized in a single long-wavelength normal mode, and the subsequent exchange of energy among normal modes is tracked.

The work was completed as a term project at the National Institute of Science Education and Research under the guidance of Dr. Subhasish Basak.

## Research questions

- Can the celebrated FPUT near-recurrence be reproduced with direct numerical integration?
- How does recurrence change with cubic and quartic nonlinearities?
- What is the effect of increasing nonlinearity and system size?
- How does the continuum-limit connection to KdV, modified KdV, and Gardner equations explain the numerical behavior?

## Model

The chain has unit masses, fixed Dirichlet boundaries, and a nearest-neighbour potential containing quadratic, cubic, and quartic terms. The simulations use chain sizes \(N=32\) and \(N=64\), with the initial energy placed in the fundamental normal mode \(k=1\).

The analysis tracks:

- Total chain energy.
- Energy in individual normal modes.
- Real-space displacement profiles.
- Recurrence times and recurrence quality.
- Energy leakage into higher modes.
- The transition from clean recurrence to irregular broadband exchange.

## Numerical method

The equations of motion are integrated using a second-order, time-reversible Störmer–Verlet/leapfrog scheme. Fixed boundary values are reset at every timestep. The code uses time-centred estimates for velocities, total energy, and normal-mode energies.

The principal parameter sets include:

- Linear control: \(\alpha=0, \beta=0\), \(N=32\).
- Cubic FPUT-\(\alpha\) runs with weak, moderate, and strong nonlinearity.
- Quartic FPUT-\(\beta\) runs, including \(\beta=0.6\) and \(\beta=1.1\).
- A mixed strong-nonlinearity run with \(\alpha=0.9\), \(\beta=1.1\), \(N=64\).
- Time horizons up to \(t_{\max}=10^5\) for the strongest cases.

## Main results

- The linear control preserves the initial mode energy, validating the initial condition and diagnostics.
- Weak-to-moderate cubic nonlinearity produces the canonical FPUT behavior: energy leaves mode 1, is transferred primarily to low modes, and returns close to the initial mode.
- At \(\alpha=0.9\) and \(\alpha=1.1\), recurrence becomes less periodic and energy leakage into higher modes becomes increasingly visible.
- Increasing the chain length from \(N=32\) to \(N=64\) produces noisier recurrence traces, consistent with the availability of more modes for energy redistribution.
- Pure quartic runs show cleaner and longer-lived two-mode beating in the studied parameter range.
- At strong mixed cubic and quartic nonlinearity, the system exhibits rapid irregular exchange among modes and approaches the equipartition-like behavior expected at sufficiently long times or stronger coupling.
- Real-space profiles steepen and develop localized, soliton-like features before splitting and recombining.

## Continuum-limit interpretation

The report derives the connection between the discrete lattice and weakly nonlinear continuum equations in two stages: a standard long-wavelength expansion and a derivation specialized to the numerical discretization.

- Cubic-dominated dynamics reduces at leading order to KdV-type behavior.
- Quartic-dominated dynamics leads to a modified KdV-type reduction.
- When both nonlinearities contribute at comparable order, the relevant reduced equation is of Gardner type.
- The soliton-bearing and near-integrable character of these continuum equations explains why energy can return close to its initial mode instead of immediately thermalizing.
- Higher-order lattice corrections, finite size, stronger nonlinearity, and additional resonance channels eventually spoil the idealized integrable picture and promote chaotic mode mixing.

## Repository structure

```text
04_fput_recurrence/
├── README.md
├── src/
│   ├── FPUT_classical.py           # system construction + simulation + energy distribution
├── figures/
├── real_space_simulations/
├── report/
│   └── FPUT_report.pdf
└── environment.yml
```

The filenames are a recommended organization and should be changed to match the actual repository contents.

## Reproducibility checklist

Document:

1. Python version and dependencies.
2. Exact Hamiltonian and sign conventions for \(\alpha\) and \(\beta\).
3. Boundary conditions and initial-mode normalization.
4. Time step, total simulation time, and integrator details.
5. Parameter sets used for each figure.
6. Definitions of total energy and mode energy.
7. Energy-conservation and timestep-convergence checks.
8. Commands or notebooks required to regenerate the main figures and animations.

## Limitations

The study uses a single initial mode and selected parameter sets rather than a systematic scan over initial energy, phase, chain length, and nonlinear coefficients. The simulations also do not establish an asymptotic equipartition plateau in every strong-nonlinearity case. The soliton interpretation is primarily qualitative; quantitative fitting to exact soliton profiles is a possible extension.

## Links

- Code: to be added.
- Full report: to be added.
- Figures and animations: to be added.

## Citation

Please cite the associated project report and the references listed there if you use this code or analysis.
