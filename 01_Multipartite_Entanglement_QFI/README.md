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

1. **Model and parameter conventions**  
   - Exact Hamiltonian (sign of $J$, definition of the exchange term, longitudinal field term, and any anisotropies).  
   - Spin representation (spin-$1/2$ operators, normalization of $S_i^\alpha$).  
   - Boundary conditions (open vs periodic chain), lattice size $N$, and unit conventions (e.g. $\hbar = k_B = 1$, energies measured in units of $J$).

2. **State preparation and thermal ensemble**  
   - Construction of the thermal state $\rho(T) = e^{-\beta H}/Z$ (full exact diagonalization vs symmetry-resolved blocks).  
   - Temperature grid used for all plots (range, spacing, and any special points such as benchmark temperatures).  
   - Treatment of degeneracies and numerical tolerances in the spectrum.

3. **Choice of generator / observable for QFI**  
   - Local operator used (e.g. $O^i = S_i^z$) and corresponding collective generator $\hat{O} = \sum_i O^i$.  
   - Eigenvalue range $[h_{\min}, h_{\max}]$ for the chosen generator and the associated normalization of the entanglement-depth thresholds $f_Q > m(h_{\max}-h_{\min})^2$.[web:22]  

4. **QFI definition and evaluation scheme**  
   - Definition of QFI adopted (e.g. symmetric logarithmic derivative form vs thermal-susceptibility integral).[web:21]  
   - If using the susceptibility route, specify the dynamical susceptibility $\chi''(q,\omega)$ used (momentum sector, spin component) and how it is built from eigenvalues/eigenvectors.[web:22]  
   - Numerical quadrature method, frequency range, and resolution for evaluating the QFI integral.

5. **Spectral broadening and finite-resolution effects**  
   - Replacement of $\delta(\omega - \Delta E)$ by a broadened lineshape (e.g. Lorentzian/Gaussian), including the width parameter $\eta$ and any $\omega$-dependent cutoffs.  
   - Checks performed to ensure that QFI and entanglement-depth claims are stable under reasonable variations of $\eta$, frequency resolution, and integration bounds.

6. **Benchmarks and sanity checks**  
   - Closed-form analytical benchmark(s) used (e.g. $N = 2$, $B = 0$ QFI vs $T$) and how the numerical workflow reproduces them within quoted tolerances.[web:23]  
   - Independent entanglement check(s) used for validation (e.g. PPT criterion / negativity for small $N$), and agreement with the QFI-based witness in the benchmark regime.

7. **System-size and scaling choices**  
   - List of chain lengths $N$ simulated for each figure and whether only even/odd sizes were considered.  
   - Criteria for choosing $N$ relative to correlation length $\xi(T)$ in “finite-size scaling” plots (e.g. what is treated as “finite-size–dominated” vs “saturated” regime).[web:17]  
   - Any finite-size extrapolations (functional form, fit range, and reported uncertainties).

8. **Figure-generation scripts and post-processing**  
   - Script names and entry points that produce each main figure (e.g. QFI vs $T$ at fixed $N$, QFI vs $N$ at fixed $T$), including command-line arguments or configuration files.  
   - Plotting conventions (log/linear axes, normalization by $N$, reference lines at entanglement-depth thresholds, color/marker mapping to different $N$ or parameter sets).

9. **Software environment and dependencies**  
   - Programming language and version, and key numerical libraries (e.g. linear algebra, sparse diagonalization, quadrature, plotting).  
   - Any specialized quantum-many-body or quantum toolbox packages used (e.g. for spin chains or operator construction), with exact versions.  
   - Instructions or environment file (e.g. `environment.yml` or `requirements.txt`) needed to recreate the environment.

10. **Scope and limitations of the implementation**  
    - Regime covered (equilibrium thermal states, static QFI witness for a fixed choice of generator) and what is *not* implemented (e.g. dynamics, disorder, other witnesses such as concurrence/tangles, higher-spin chains).[web:22][web:23]  
    - Parameter ranges where numerical results are reliable, and known failure modes (e.g. loss of accuracy at very low $T$ or large $N$ due to finite-size or numerical issues).


## Limitations

Exact diagonalization is limited to small chains because the Hilbert-space dimension grows exponentially with system size. The reported conclusions therefore concern finite systems (equilibrium thermal states, static QFI witness for a fixed choice of generator) and the parameter ranges studied (where numerical results are reliable; some known failure modes: loss of accuracy at very low $T$ or large $N$ due to finite-size or numerical issues); they should not be interpreted as a direct thermodynamic-limit result. Dynamics and disorder are some direct extensions, along with possible execution of the complete computation/analysis on a QPU integrated workflow.

## Links

- [Code]: code may be made available on request, subject to viewing/sharing permissions
- [Report](report/): thesis presentation slides; full thesis may be made available on request, subject to viewing/sharing permissions
- [Figures](figures/): a selection out of the set of figures and result plots from the project
- [Animations](animations/): animation of QFI density for the target model for various system sizes under varying magnetic field B 

## Citation

Please cite the associated M.Sc. thesis once the final bibliographic information and repository DOI, if any, have been added.
