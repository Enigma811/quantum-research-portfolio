# Recursive Green's Function Method for Graphene

## Project summary

This project reviews the recursive Green's function (RGF) method for calculating electronic transport in mesoscopic systems and applies it to single-layer graphene in the ballistic-conductor regime.

The work was completed as a term project at the National Institute of Science Education and Research under the guidance of Dr. Anamitra Mukherjee.

## Research questions

- How can the Green's function of a large open system be computed recursively by slicing the conductor?
- How are lead self-energies incorporated into the finite device Green's function?
- How can conductance, transmission, spectral functions, and local density of states be extracted?
- How do graphene edge orientation and slicing strategy affect computational efficiency and transport results?

## Formalism

The report develops the transport framework from the Landauer and Landauer–Büttiker viewpoints and introduces:

- Transmission probabilities and conductance quantization.
- Scattering matrices and their relation to Green's functions.
- Retarded and advanced Green's functions.
- Lead self-energies and level-width matrices.
- Fisher–Lee relations for transmission.
- Spectral functions and local density of states.
- Finite-temperature, finite-bias, and coherent/non-coherent transport considerations.

## Recursive method

The conductor is divided into slices, each containing a finite number of sites. The algorithm performs:

1. A left-to-right recursive sweep to construct left-connected Green's functions.
2. A right-to-left sweep to construct right-connected Green's functions.
3. A combination step to obtain the full Green's function of the open device.
4. Extraction of boundary blocks for transmission calculations.
5. Evaluation of diagonal blocks for local density of states calculations.

Semi-infinite leads are incorporated through surface Green's functions and self-energy terms. The report discusses analytic, eigenmode-decomposition, and decimation approaches for obtaining lead Green's functions.

## Graphene model

The application uses a nearest-neighbour tight-binding Hamiltonian for a single graphene layer:

- Honeycomb lattice with two sublattices.
- Nearest-neighbour hopping and optional onsite-potential framework.
- Ballistic, disorder-free transport in the numerical demonstration.
- Armchair and zigzag edge orientations.
- Alternative slicing schemes designed to reduce the number of sites and inter-slice couplings.

## Main results

- The RGF method provides an efficient way to compute transport quantities for larger systems than direct inversion of the full device matrix.
- Efficient slicing reduces the computational burden while retaining the graphene lattice connectivity.
- Conductance is calculated from the Green's-function blocks connecting the left and right contacts.
- Local density of states is calculated from the diagonal blocks of the spectral function.
- For the clean armchair graphene sample studied in the report, the numerical conductance agrees well with the expected behavior for sufficiently large systems; smaller systems show stronger finite-size effects and less well-defined oscillatory structure.
- The method is discussed as extensible to disorder, interactions, finite temperature, and more complicated edge geometries.

## Repository structure

```text
03_recursive_greens_function_graphene/
├── README.md
├── src/
│   ├── hamiltonian.py          # Tight-binding device and lead blocks
│   ├── surface_greens.py      # Surface Green's functions
│   ├── rgf.py                  # Left/right/full recursive sweeps
│   └── observables.py          # Conductance, transmission, and LDOS
├── notebooks/
├── configs/
├── figures/
├── report/
│   └── RGF_graphene_report.pdf
└── environment.yml
```

The filenames are a recommended organization and should be changed to match the actual repository contents.

## Reproducibility checklist

Document:

1. Python version and dependencies.
2. Tight-binding hopping and onsite-energy conventions.
3. Graphene lattice geometry and slicing convention.
4. Lead model and surface-Green's-function method.
5. Broadening parameter and energy grid.
6. Device width, length, edge orientation, and contact configuration.
7. Commands or notebooks required to reproduce conductance and LDOS figures.

## Scope and limitations

The main numerical demonstration uses a clean, ballistic, single-layer graphene model with nearest-neighbour hopping. Disorder, interactions, inelastic effects, and finite-temperature transport are discussed conceptually in the report but are not necessarily implemented in the repository.

## Links

- Code: to be added.
- Full report: to be added.
- Selected conductance and LDOS figures: to be added.

## Citation

Please cite the associated project report and the methodological references listed there if you use this material.
