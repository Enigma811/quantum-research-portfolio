# Multipartite Entanglement in a 1D Heisenberg Model

## Project summary

This project investigates multipartite entanglement in the isotropic one-dimensional Heisenberg antiferromagnetic spin-1/2 model using quantum Fisher information (QFI). It combines analytical calculations for \(N=2\) with exact diagonalization for finite chains of \(N=3\)–\(12\), studying the dependence of entanglement on temperature, magnetic field, and system size.

This work was completed as an M.Sc. thesis at the National Institute of Science Education and Research under the guidance of Dr. Anamitra Mukherjee.

> The linked document is a concise thesis presentation/summary. The complete thesis is substantially longer and is available on request where appropriate.

## Research questions

- How can QFI be used to detect and quantify multipartite entanglement in mixed thermal states?
- How does the entanglement signature scale with temperature and system size?
- How does an external magnetic field affect entanglement depth?
- How experimentally accessible are QFI-based entanglement criteria for strongly correlated systems?

## Model and methods

- Isotropic 1D Heisenberg antiferromagnetic spin-1/2 model.
- Analytical treatment of the two-spin case.
- Exact diagonalization for finite chains with \(N=3\)–\(12\).
- Thermal density matrices and energy eigenstate decompositions.
- Quantum Fisher information and QFI-density-based multipartite-entanglement criteria.
- Entanglement witnesses, separability bounds, correlation functions, and susceptibility connections.
- Parameter sweeps over temperature \(T\), magnetic field \(B\), and system size \(N\).
- Extension to multiparameter estimation in an anisotropic/isotropic XY setting.

## Main results

- QFI detects entanglement over a finite thermal window that shrinks with increasing system size.
- The QFI density decreases as temperature increases because thermal population of higher-spin sectors weakens the entanglement signature.
- Increasing magnetic field suppresses the QFI-based entanglement signal in the parameter regime studied.
- The crossover temperature associated with a given entanglement depth decreases as \(N\) increases.
- The analysis supports QFI as a thermodynamically accessible and experimentally relevant tool for entanglement detection in strongly correlated systems.
- The XY-model extension illustrates how multiparameter QFI can support simultaneous estimation and phase-diagnostic analysis.

## Repository structure

```text
01_multipartite_entanglement_qfi/
├── README.md
├── src/
│   ├── model.py                 # Hamiltonians and operators
│   ├── diagonalization.py       # Finite-size eigensystems
│   ├── thermal_states.py        # Thermal density matrices
│   └── qfi.py                   # QFI and witness calculations
├── notebooks/
│   ├── qfi_temperature.ipynb
│   ├── qfi_field.ipynb
│   └── finite_size_scaling.ipynb
├── figures/
├── data/
├── report/
│   └── thesis_presentation.pdf
└── environment.yml
```

The filenames above are a recommended organization and should be changed to match the actual repository contents.

## Reproducibility checklist

Before publication, document:

1. Python version and package versions.
2. Hamiltonian convention, coupling normalization, and units.
3. Basis ordering and spin-operator conventions.
4. Exact-diagonalization settings and numerical precision.
5. Temperature and magnetic-field grids.
6. QFI convention and normalization used for entanglement depth.
7. Commands or notebooks required to reproduce each main figure.

## Limitations

Exact diagonalization is limited to small chains because the Hilbert-space dimension grows exponentially with system size. The reported conclusions therefore concern finite systems and the parameter ranges studied; they should not be interpreted as a direct thermodynamic-limit result.

## Links

- [Code]: code available on request, subject to viewing/sharing permissions.
- [Report](report/): thesis presentation; full thesis available on request, subject to viewing/sharing permissions.
- [Figures](figures/): a selection out of the set of result plots obtained during the project
- [Simulations](animations/): animation of QFI density for the target model for various system sizes under varying magnetic field B. 

## Citation

Please cite the associated M.Sc. thesis once the final bibliographic information and repository DOI, if any, have been added.
