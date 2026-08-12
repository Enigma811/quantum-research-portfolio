# Multipartite Entanglement in a 1D Heisenberg Model

## Project summary

This project investigates multipartite entanglement in the isotropic one-dimensional Heisenberg antiferromagnetic spin-1/2 model using quantum Fisher information (QFI). It combines analytical calculations for $N=2$ with exact diagonalization for finite chains of $N=3-12$, studying the dependence of entanglement on temperature, magnetic field, and system size.

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
- Exact diagonalization for finite chains with $N=3-12$.
- Thermal density matrices and energy eigenstate decompositions.
- Quantum Fisher information and QFI-density-based multipartite-entanglement criteria.
- Entanglement witnesses, separability bounds, correlation functions, and susceptibility connections.
- Parameter sweeps over temperature $T$, magnetic field $B$, and system size $N$.

## Main results

- QFI detects entanglement over a finite thermal window that shrinks with increasing system size.
- The QFI density decreases as temperature increases because thermal population of higher-spin sectors weakens the entanglement signature.
- Increasing magnetic field suppresses the QFI-based entanglement signal in the parameter regime studied.
- The crossover temperature associated with a given entanglement depth decreases with increasing system size.
- The analysis supports QFI as a thermodynamically accessible and experimentally relevant tool for entanglement detection in strongly correlated systems.

## Repository structure

```text
01_Multipartite_Entanglement_QFI/
├── README.md
├── animations/
|   └── qfi_field_sweep.gif
├── figures/
│   ├── f_Q vs T (var N, B= 0.0).png            # qfi density vs T for varying system sizes with B = 0
|   ├── Line_T(m_by_N)_vs_N.png                 # crossover temp. T_m/N vs system size for thermal window of entanglement depth
|   ├── spin_sector_heatmap_N=9_B=0.png         # spin-resolved contributions to qfi density
│   └── var N B=0.1.png                         # qfi density vs T for varying N, B: field induced suppression
├── report/
│   └── thesis_presentation.pdf
└── environment.yml
```

## Reproducibility checklist

1. Chosen programming language version and dependencies/relevant package versions.
2. Model and parameter conventions (exact Hamiltonian, appropriate spin representation and boundary conditions/effects).
3. State preparation and thermal ensemble.
4. **Choice of generator / observable for QFI**.
5. QFI definition and evaluation scheme.
6. Spectral broadening and finite-resolution effects, if any.
7. System-size and scaling choices.
8. Figure-generation scripts and post-processing


## Limitations

Exact diagonalization is limited to small chains because the Hilbert-space dimension grows exponentially with system size. The reported conclusions therefore concern finite systems (equilibrium thermal states, static QFI witness for a fixed choice of generator) and the parameter ranges studied (where numerical results are reliable; some known failure modes: loss of accuracy at very low $T$ or large $N$ due to finite-size or numerical issues); they should not be interpreted as a direct thermodynamic-limit result. Dynamics, disorder and real time entanglement tracking are some direct extensions, along with possible execution of the complete computation/analysis on a QPU integrated workflow.

## Links

- [Code]: code may be made available on request, subject to viewing/sharing permissions
- [Report](report/): thesis presentation slides; full thesis may be made available on request, subject to viewing/sharing permissions
- [Figures](figures/): a selection out of the set of figures and result plots from the project
- [Animations](animations/): animation of QFI density for the target model for various system sizes under varying magnetic field B 

## Citation

Please cite the associated M.Sc. thesis once the final bibliographic information and repository DOI, if any, have been added.
