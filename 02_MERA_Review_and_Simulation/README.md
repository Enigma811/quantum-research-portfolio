# MERA Review and Simulation for the Transverse-Field Ising Model

## Project summary

This project reviews the Multiscale Entanglement Renormalization Ansatz (MERA), its tensor-network formulation, its causal structure, and its use in studying strongly correlated quantum systems. A Python-based variational MERA simulation was implemented for a one-dimensional transverse-field Ising model with 256 sites.

The work was completed as a term project at the National Institute of Science Education and Research under the guidance of Dr. Anamitra Mukherjee.

## Motivation

Exact diagonalization becomes impractical as the number of degrees of freedom grows because the Hilbert-space dimension increases exponentially. MERA addresses this challenge by organizing entanglement across length scales: disentanglers remove short-range entanglement before isometries coarse-grain the system.

## Topics covered

- Entanglement entropy, area laws, and critical systems.
- Real-space and tree renormalization.
- Disentanglers and isometries.
- Tensor-network states, including MPS, TTN, and MERA.
- Penrose tensor notation and tensor contractions.
- Causal cones and bounded-width evaluation of local observables.
- Ascending and descending superoperators.
- Variational optimization of MERA tensors.
- Finite-range, scale-invariant, two-dimensional, and branching MERA extensions.
- Geometric and quantum-circuit interpretations of MERA.

## Model and implementation

The numerical study considers a critical one-dimensional quantum Ising model with transverse magnetic field and a finite lattice of $256$ sites. The implementation uses a variational optimization procedure in which tensor environments are constructed and the tensors are updated iteratively.

The simulation evaluates:

- Ground-state energy and its convergence with iterations.
- Error relative to exact/reference ground-state energies.
- Conformal scaling dimensions obtained from the MERA superoperator structure.

## Main results

- The variational MERA calculation converges toward the ground-state energy of the finite Ising system.
- The energy error decreases substantially over the optimization iterations, with the report (Choubey, 2024) showing convergence to a tolerance of approximately $10^{-5}$ for the studied setup.
- MERA-derived scaling dimensions show good agreement with the expected critical-Ising values in the reported calculation.
- Increasing bond dimension improves the variational representation and reduces the observed energy error for a fixed number of iterations.
- Disentanglers prevent the accumulation of short-range entanglement and preserve a bounded causal-cone width, which is central to MERA's computational efficiency.

## Repository structure

```text
02_MERA_Review_and_Simulation/
├── README.md
├── src/
|   └── README.md
├── figures/
|   ├── causal_cone.png                    # bounded causal cone of a local operator in 1D MERA tensor network
|   ├── errr_gs_vs_iteration_count.png     # error in grounds state energy for target model vs iteration count
|   └── scaling_dim.png                    # critical ising model's corresponding conformal scaling dimension vs bond dimension k
├── report/
│   └── MERA_report.pdf
└── environment.yml
```


## Reproducibility checklist

Document the following with the final code:

1. Python version and package versions.
2. MERA type, tensor dimensions, bond dimension, and network depth.
3. Tensor index ordering and normalization conventions.
4. Ising Hamiltonian convention and boundary conditions.
5. Tensor initialization procedure.
6. Optimization update rule and convergence criterion.
7. Number of iterations and stopping conditions.
8. Code to reproduce the energy and scaling-dimension plots.

## Limitations

The numerical accuracy depends on bond dimension, network architecture, initialization, finite-size effects, and the variational optimization procedure. The reported results demonstrate the method for the selected finite system; they are not a systematic benchmark across all MERA architectures or bond dimensions.

## Links

- [Code]: code may be made available on request, subject to viewing/sharing permissions
- [Report](report/): the project summary; the full report may be made available on request, subject to viewing/sharing permissions
- [Figures](figures/): a selection out of the set of figures and result plots from the project

## Citation

Please cite the associated term-project report and the references listed therein if you use this material.
