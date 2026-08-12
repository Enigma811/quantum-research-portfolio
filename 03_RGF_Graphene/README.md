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

The report (Choubey, 2024) develops the transport framework from the Landauer and Landauer–Büttiker viewpoints and introduces:

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

Semi-infinite leads are incorporated through surface Green's functions and self-energy terms. The report (Choubey, 2024) discusses analytic, eigenmode-decomposition, and decimation approaches for obtaining lead Green's functions.

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
- Local density of states can be calculated from the diagonal blocks of the spectral function.
- For the clean armchair graphene sample studied in the report (Choubey, 2024), the numerical conductance agrees well with the expected behavior for sufficiently large systems; smaller systems show stronger finite-size effects and less well-defined oscillatory structure.
- The method is discussed as extensible to disorder, interactions, finite temperature, and more complicated edge geometries.

## Repository structure

```text
03_RGF_Graphene/
├── README.md
├── src/
│   ├── README.md
|   ├── lattice.py                 # Generates honeycomb graphene lattices and block-tridiagonal RGF Hamiltonians
|   ├── leads.py                   # Computes semi-infinite lead surface Green's functions and self-energies
|   ├── rgf.py                     # Implements the recursive Green's function algorithm for transmission and LDOS
|   ├── transport.py               # High-level graphene transport wrapper combining lattice, leads, and RGF methods
|   ├── run_lattice_figures.py     # Generates graphene lattice and RGF slicing visualizations for armchair and zigzag ribbons
|   ├── run_conductance.py         # Generates conductance quantization and pseudo-diffusive conductivity figures
|   └── run_ldos.py                # Computes and plots local density of states maps from RGF Green's functions 
├── figures/
│   ├── README.md
│   ├── honeycomb_graphene_lattice.png                # graphene lattice structure
|   ├── armchair_slice_scheme.png                     # slicing scheme for armchair edge
|   ├── zigzag_slice_scheme.png                       # slicing scheme for zigzag edge
|   ├── conductance_vs_fermi_energy_(M=360,N=70).png  # conductance vs contact fermi energy
│   ├── conductance_vs_fermi_energy_(M=120,varN).png  # conductance vs contact fermi energy
│   └── local_density_of_states.png                   # spatial LDOS map
├── report/
│   └── RGF_project_summary.pdf
└── environment.yml
```


## Reproducibility checklist

Document:

1. Chosen programming language version and dependencies/relevant package versions.
2. Tight-binding hopping and onsite-energy conventions.
3. Graphene lattice geometry and slicing convention.
4. Lead model and surface-Green's-function method.
5. Broadening parameter and energy grid.
6. Device width, length, edge orientation, and contact configuration.
7. Code to setup RGF and compute conductance and LDOS for Graphene.

## Scope and limitations

The main numerical demonstration uses a clean, ballistic, single-layer graphene model with nearest-neighbour hopping. Disorder, interactions, inelastic effects, and finite-temperature transport are discussed conceptually in the report (Choubey, 2024) but are not necessarily implemented in the repository.

## Links

- [Code](src/): code to set up the scheme and compute relevant quantities for graphene with specified (in the the project) set of configurations and parameters
- [Report](report/): the project summary; the full report may be made available on request, subject to viewing/sharing permissions
- [Figures](figures/): a selection out of the set of figures and result plots from the project

## Citation

Please cite the associated project report and the references listed therein if you use this material/code.
