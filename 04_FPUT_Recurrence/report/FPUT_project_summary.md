# The Fermi–Pasta–Ulam–Tsingou Problem
## Numerical recurrence, chaos onset, and the continuum-limit connection to KdV

**Author:** Monu Kumar Choubey  
**Institution:** School of Physical Sciences, NISER  
**Project type:** Term project  
**Supervisor/course instructor:** Dr. Subhasish Basak  
**Project period:** January–May 2024

---

## Abstract

The Fermi–Pasta–Ulam–Tsingou problem is a foundational numerical experiment in nonlinear dynamics and statistical mechanics. A chain of particles coupled by weakly anharmonic springs was expected to approach equipartition of energy among its normal modes. Instead, the original simulations displayed a near-recurrence: energy returned close to the initially excited mode after substantial energy exchange.

This project reproduces and analyzes that behavior numerically for fixed-end chains with $N=32$ and $N=64$ particles. The equations of motion contain quadratic, cubic, and quartic nearest-neighbor interactions and are integrated using a second-order, time-reversible Störmer–Verlet/leapfrog scheme. Mode energies, total energy, real-space displacement profiles, and recurrence behavior are tracked as functions of nonlinearity and system size.

The simulations reproduce clean near-recurrence for weak-to-moderate nonlinearity and show systematic degradation as nonlinear coupling, chain length, and the number of active resonance channels increase. A continuum-limit derivation connects the lattice to Korteweg–de Vries (KdV), modified KdV, and Gardner-type equations. Their soliton-bearing and near-integrable dynamics provides the theoretical interpretation of recurrence, while lattice corrections and strong nonlinear mixing explain the onset of irregular, broadband energy exchange.

---

## 1. Background and motivation

In 1955, Fermi, Pasta, Ulam, and Mary Tsingou studied a chain of nonlinear oscillators to test the approach to thermal equilibrium. A generic nonlinear system was expected to redistribute energy among normal modes and approach equipartition. Instead, the initial mode repeatedly regained a large fraction of its energy.

The later connection between the FPUT lattice and the integrable KdV equation provided a conceptual explanation. Long-wavelength excitations can organize into soliton-like structures whose collisions are nearly elastic. The recurrence is therefore associated with near-integrability and coherent nonlinear dynamics rather than a simple failure of statistical mechanics.

---

## 2. Objectives

The project had the following objectives:

1. Reproduce the FPUT near-recurrence numerically.
2. Verify the numerical method through energy conservation and a linear control run.
3. Track how recurrence changes with cubic and quartic nonlinearities.
4. Study the effects of system size and strong nonlinear coupling.
5. Examine real-space displacement profiles for localized, soliton-like structures.
6. Derive the continuum-limit connection to KdV, modified KdV, and Gardner equations.
7. Interpret the transition from clean recurrence to irregular mode mixing.

---

## 3. Lattice model

Consider a chain of $N$ identical particles with unit mass and fixed boundary conditions. Let $y_n(t)$ denote the displacement of particle $n$ from equilibrium. The nearest-neighbor relative displacement is

$$
r_n = y_{n+1}-y_n.
$$

The interaction potential contains harmonic, cubic, and quartic contributions:

$$
V(r) = \frac{1}{2}r^2 + \frac{\alpha}{3}r^3 + \frac{\beta}{4}r^4.
$$

The total Hamiltonian has the schematic form

$$
H = \sum_n \frac{1}{2}\dot y_n^2 + \sum_n V(y_{n+1}-y_n),
$$

with fixed-end boundary conditions enforced throughout the simulation.

The cubic coefficient $\alpha$ controls the asymmetric FPUT-$\alpha$ nonlinearity, while $\beta$ controls the symmetric quartic FPUT-$\beta$ contribution.

---

## 4. Linear normal modes

In the harmonic limit, the fixed-end chain is diagonalized by a discrete sine transform. The normal-mode coordinates are

$$
Q_k(t) = \sqrt{\frac{2}{N+1}}
\sum_{n=1}^{N} y_n(t)\sin\left(\frac{\pi k n}{N+1}\right),
$$

with mode frequencies

$$
\omega_k^2 = 4\sin^2\left(\frac{\pi k}{2(N+1)}\right)
$$

in the unit-coupling convention.

For the linear chain, each mode evolves independently. An initial excitation in mode $k=1$ therefore remains in that mode, providing a stringent control test for the numerical implementation.

---

## 5. Numerical method

### 5.1 Initial condition

All runs begin with energy concentrated in the fundamental long-wavelength mode $k=1$. The amplitude is scaled with system size so that the initial energy remains comparable between the $N=32$ and $N=64$ simulations.

### 5.2 Störmer–Verlet integration

The second-order Störmer–Verlet/leapfrog method updates the displacement according to

$$
y_n(t+\Delta t) = 2y_n(t)-y_n(t-\Delta t)
+\Delta t^2 F_n[y(t)],
$$

where $F_n$ is the nonlinear force derived from the Hamiltonian. Boundary values are reset to zero after each update.

The method is symplectic and time reversible. It is therefore well suited to long-time Hamiltonian simulations because it typically produces bounded energy fluctuations rather than a secular energy drift.

### 5.3 Diagnostics

At each time step, the code computes:

- Total energy of the chain.
- Discrete normal-mode amplitudes.
- Energy in modes $k=1,2,3,\ldots$.
- Real-space displacement profiles.
- Recurrence patterns and energy leakage.

The time-centred velocity estimate is used to improve the consistency of the energy diagnostic with the leapfrog update.

---

## 6. Parameter sets

The report studies the following representative cases:

| Case | $N$ | $\alpha$ | $\beta$ | Purpose |
|---|---:|---:|---:|---|
| Linear control | 32 | 0 | 0 | Validate mode decoupling and diagnostics |
| Weak cubic | 32 | 0.3 | 0 | Observe clean recurrence |
| Moderate cubic | 32 | 0.5 | 0 | Study stronger energy exchange |
| Strong cubic | 32 | 0.9–1.1 | 0 | Observe recurrence degradation |
| Strong cubic, larger chain | 64 | 1.1 | 0 | Study finite-size effects |
| Pure quartic | 32 | 0 | 0.6 | Study symmetric nonlinearity |
| Strong pure quartic | 32 | 0 | 1.1 | Observe delayed breakdown |
| Mixed strong nonlinearity | 64 | 0.9 | 1.1 | Study broadband mode mixing |

The precise time step, time horizon, and initial amplitude should be recorded in the repository configuration files.

---

## 7. Numerical results

### 7.1 Linear control

For $\alpha=\beta=0$, the energy in mode 1 remains constant and mode 2 remains unexcited. The total energy also remains stable throughout the simulation. This validates both the pure-mode initial condition and the mode-energy diagnostic.
![[alpha0_beta0_total_energy.png]]

![[alpha0_beta0_mode_energy.png]]
Figure 1: *(a) depicts Total Energy and (b) depicts mode energy vs time for $\alpha=0, \beta=0$. The harmonic chain preserves the initial mode excitation and shows no nonlinear energy transfer.*

### 7.2 Weak-to-moderate cubic nonlinearity

For cubic coupling with $\alpha=0.3$ and $\alpha=0.5$, mode 1 loses energy while low-order modes, especially mode 2, gain energy. A substantial fraction of the energy later returns to mode 1, producing the canonical FPUT recurrence.

The recurrence time is of order $10^4$ simulation time units for the reported weak-to-moderate runs and decreases slightly as the cubic coupling is increased from 0.3 to 0.5.

![[alpha0.3_mode_energy.png]]
Figure 2: *Mode energy vs time for $\alpha=0.3, \beta=0$.*
![[alpha0.5_mode_energy.png]]
Figure 3: *Mode energy vs time for $\alpha=0.5, \beta=0$.*

### 7.3 Breakdown of clean recurrence

At $\alpha=0.9$, the mode-2 energy displays multiple excursions with unequal amplitudes, indicating leakage into higher modes. At $\alpha=1.1$, recurrence-like behavior persists but becomes irregular in amplitude and spacing.
![[alpha0.9_mode_energy.png]]
Figure 4: *Degrading recurrence in mode energy for $\alpha=0.9$*
![[alpha1.1_mode_energy_run1.png]]
Figure 5: *Degrading recurrence in mode energy for $\alpha=1.1$*
### 7.4 System-size dependence

Repeating the strong cubic run for $N=64$ produces a qualitatively similar decay-and-recurrence pattern but with greater high-frequency structure. The larger chain provides more modes into which energy can leak, making a return to a simple two-mode state less likely.
![[alpha1.1_N64_mode_energy.png]]
Figure 6: *Degrading recurrence in mode energy for $\alpha=1.1, N=64$*

### 7.5 Pure quartic nonlinearity

The pure quartic model shows cleaner and larger-amplitude energy exchange in the studied parameter regime. For $\beta=0.6$, mode 1 and mode 2 exhibit nearly sinusoidal beating over multiple cycles. At $\beta=1.1$, the clean recurrence persists for several periods before gradually developing irregular broadband exchange.
![[beta0.6_mode_energy.png]]
Figure 7: *Pure quartic recurrence in mode energy at $\beta=0.6$*
![[beta1.1_mode_energy.png]]
Figure 8: *Delayed recurrence breakdown at $\beta=1.1$*

### 7.6 Mixed nonlinearities and approach to equipartition

For the mixed case $\alpha=0.9$, $\beta=1.1$, and $N=64$, mode 1 decays rapidly and only a partial rebound occurs. The subsequent dynamics shows irregular exchange among multiple modes with no clear large-scale recurrence during the simulated time interval.

This is the closest reported case to the equipartition-like behavior originally expected from the FPUT experiment.
![[alpha0.9_beta1.1_N64_mode_energy.png]]
Figure 9: *Strong mixed-nonlinearity mode-energy evolution at $\alpha=0.9$, $\beta=1.1$, and $N=64$*

---

## 8. Real-space dynamics

The initial displacement is a smooth, long-wavelength sinusoidal profile. Under anharmonic evolution, the profile steepens and develops localized, soliton-like structures. These structures split, propagate, reflect from the fixed boundaries, and recombine.

The real-space dynamics provides an intuitive complement to the mode-energy plots: recurrence of mode energy corresponds to the reassembly of localized structures into a configuration resembling the initial profile.
![[im α = 1.1, β = 0, N = 32.gif]]
*Evolution of the displacement field showing nonlinear steepening, localization, propagation, reflection, and partial reassembly for $\alpha=0.9, \beta=0, N=32$.*

---

## 9. Continuum-limit connection

### 9.1 Long-wavelength expansion

Let the lattice displacement be represented by a smooth field $u(x,t)$, with $y_n(t)\approx u(nh,t)$. Expanding neighboring displacements in powers of the lattice spacing $h$ produces a weakly dispersive, weakly nonlinear continuum equation.

The linear lattice contribution generates a wave equation with higher-order dispersive corrections. The cubic and quartic lattice nonlinearities produce nonlinear gradient terms.

### 9.2 KdV reduction

For cubic-dominated dynamics, a unidirectional multiple-scales reduction produces a KdV-type equation of the form

$$
u_t + c_1 u u_x + c_2 u_{xxx}=0,
$$

with coefficients determined by the scaling and the microscopic model.

The KdV equation is integrable and has soliton solutions. These solitons preserve their shape and speed under collisions up to phase shifts, providing the theoretical basis for near-recurrence.

### 9.3 Modified KdV reduction

For the pure quartic case, the cubic contribution vanishes and the leading nonlinear term changes. The corresponding unidirectional reduction is of modified KdV type:

$$
u_t + c_3 u^2u_x + c_2 u_{xxx}=0.
$$

The different nonlinearity helps explain why the pure quartic simulations show cleaner and longer-lived recurrence in the parameter ranges studied.

### 9.4 Gardner-type mixed case

When cubic and quartic terms contribute simultaneously at comparable order, the reduced equation contains both KdV and modified-KdV nonlinearities and takes Gardner-type form:

$$
u_t + c_1 u u_x + c_3 u^2u_x + c_2 u_{xxx}=0.
$$

The continuum equation can retain integrable structure under idealized assumptions, but the finite discrete lattice includes higher-order corrections and additional resonance channels. These effects promote chaotic mixing at stronger coupling and larger system size.

---

## 10. Interpretation of recurrence and chaos onset

The numerical results support the following physical picture:

1. A long-wavelength initial mode excites a small number of nearby modes.
2. Weak nonlinearity organizes the energy exchange coherently.
3. Soliton-like structures form in real space.
4. Near-elastic soliton interactions lead to a return close to the initial configuration.
5. Stronger nonlinearity, larger system size, longer times, and additional nonlinear channels increase mode mixing.
6. Discreteness and higher-order corrections break the idealized integrable behavior.
7. The dynamics becomes irregular and increasingly compatible with equipartition-like energy distribution.

The recurrence is therefore not a simple absence of energy transfer. It is a structured redistribution followed by coherent reassembly.

---

## 11. Numerical validation and limitations

### Validation checks

- Linear-chain mode decoupling.
- Bounded total-energy fluctuations.
- Timestep sensitivity and convergence.
- Consistency of the discrete sine transform.
- Reproducibility of the reported parameter sets.

### Limitations

- The study uses a single initial mode and selected initial amplitudes.
- The parameter space of $\alpha$, $\beta$, $N$, and initial energy is not exhaustively scanned.
- The longest simulations do not establish an asymptotic equipartition plateau for every strong case.
- Multiple initial phases and ensembles are not systematically averaged.
- The soliton interpretation is primarily qualitative; a quantitative fit to exact soliton profiles remains a possible extension.

---
## 12. Conclusion

The project numerically reproduces the FPUT near-recurrence for weak-to-moderate nonlinearities and documents its systematic degradation as nonlinearity and system size increase. Pure quartic dynamics exhibits cleaner recurrence in the studied regime, while mixed strong nonlinearities produce rapid, irregular, broadband energy exchange.

The continuum-limit analysis connects the discrete chain to KdV, modified KdV, and Gardner-type equations. The soliton-bearing and near-integrable character of these equations explains the coherent recurrence, while finite-lattice corrections and multiple nonlinear resonance channels explain the onset of chaotic mode mixing.

The work combines nonlinear dynamics, Hamiltonian simulation, numerical integration, normal-mode analysis, continuum asymptotics, and scientific visualization.

---
## References

- Fermi, E., Pasta, J., Ulam, S., & Tsingou, M. (1955). *Studies of Nonlinear Problems I*. Los Alamos Report LA-1940.

- Zabusky, N. J., & Kruskal, M. D. (1965). Interaction of “Solitons” in a Collisionless Plasma and the Recurrence of Initial States. *Physical Review Letters, 15*, 240.

- Dauxois, T. (2008). Fermi, Pasta, Ulam, and a mysterious lady. *Physics Today, 61*, 55.

- Toda, M. (1967). Vibration of a Chain with Nonlinear Interaction. *Journal of the Physical Society of Japan, 22*, 431.

- Berman, G. P., & Izrailev, F. M. (2005). The Fermi–Pasta–Ulam problem: Fifty years of progress. *Chaos, 15*, 015104.

- Drazin, P. G., & Johnson, R. S. (1989). *Solitons: An Introduction*. Cambridge University Press.

- Ford, J. (1992). The Fermi–Pasta–Ulam problem: paradox turns discovery. *Physics Reports, 213*, 271.
