"""High-level wrappers tying lattice + leads + RGF together."""

import numpy as np
from lattice import build_ribbon, hamiltonian_blocks, merge_slices, EDGE_THETA, find_commensurate_size
from leads import left_self_energy, right_self_energy, gamma
from rgf import transmission, full_diagonal_blocks

CONDUCTANCE_QUANTUM = 1.0  # we report G in units of (2e^2/h) per spin-summed mode; see run scripts


class GrapheneRibbon:
    def __init__(self, Lx, Ly, edge="armchair", t=1.0, onsite=0.0, eta=1e-5,
                 lead_onsite_shift=0.0):
        """
        Lx, Ly : ribbon length / width (in units of the C-C bond length)
        edge   : 'armchair' or 'zigzag' (edge geometry, see lattice.py)
        t      : nearest-neighbour hopping magnitude (energy unit)
        onsite : uniform on-site energy in the DEVICE region (doping/gate)
        eta    : small imaginary broadening added to E for the retarded GF
        lead_onsite_shift : extra on-site energy added ONLY in the leads,
            relative to the device (models heavily-doped / metallic contacts,
            as used for the "clean armchair sample" conductance scan in the
            report, where V_lead sets the contact Fermi level).
        """
        theta = EDGE_THETA[edge]
        Lx, Ly = find_commensurate_size(Lx, Ly, edge)
        self.Lx, self.Ly = Lx, Ly
        self.slices, self.bonds, self.pos, self.sub, self.slice_of, n_bad = build_ribbon(
            Lx, Ly, theta_deg=theta)
        if n_bad:
            raise RuntimeError(f"{n_bad} non-nearest-neighbour slice couplings; refine slicing")
        self.h, self.u = hamiltonian_blocks(self.slices, self.bonds, self.slice_of, t=t, onsite=onsite)
        group_size = 1 if edge == "zigzag" else 2
        self.h, self.u = merge_slices(self.h, self.u, group_size)
        self._group_size = group_size

        # positions/subs for each MERGED slice (same grouping/order used in
        # merge_slices), needed for plotting LDOS etc. against real space
        n_raw = len(self.slices)
        n_groups = int(np.ceil(n_raw / group_size))
        self.merged_slices = []
        for g in range(n_groups):
            lo, hi = g * group_size, min(g * group_size + group_size, n_raw)
            pos = np.concatenate([self.slices[k]["pos"] for k in range(lo, hi)], axis=0)
            sub = np.concatenate([self.slices[k]["sub"] for k in range(lo, hi)], axis=0)
            self.merged_slices.append({"pos": pos, "sub": sub})
        self.N = len(self.h)
        self.t = t
        self.eta = eta
        self.edge = edge
        self.widths = [hh.shape[0] for hh in self.h]

        # ideal leads = semi-infinite repeats of the ribbon's own end cells,
        # with an optional uniform onsite shift (contact/gate potential)
        self.h_lead_L = self.h[0] + lead_onsite_shift * np.eye(self.widths[0])
        self.u_lead_L = self.u[0]
        self.h_lead_R = self.h[-1] + lead_onsite_shift * np.eye(self.widths[-1])
        self.u_lead_R = self.u[-2]

    def _self_energies(self, E):
        z = E + 1j * self.eta
        sL = left_self_energy(z, self.h_lead_L, self.u_lead_L, eta=self.eta)
        sR = right_self_energy(z, self.h_lead_R, self.u_lead_R, eta=self.eta)
        return z, sL, sR

    def transmission(self, E):
        z, sL, sR = self._self_energies(E)
        gL, gR = gamma(sL), gamma(sR)
        T, _ = transmission(z, self.h, self.u, sL, sR, gL, gR)
        return T

    def conductance_scan(self, energies):
        """G(E) in units of 2e^2/h (spin included as a factor 2 -> so this
        returns T(E); multiply by 2 for the spin-degenerate 2e^2/h unit, or
        by 4 for the 4e^2/h unit used in the report's Fig. 3)."""
        return np.array([self.transmission(E) for E in energies])

    def ldos(self, E):
        z, sL, sR = self._self_energies(E)
        G_diag = full_diagonal_blocks(z, self.h, self.u, sL, sR)
        rho = [-np.diag(G).imag / np.pi for G in G_diag]
        return rho  # list of per-slice arrays

    def slice_positions(self):
        return np.array([s["x"] for s in self.slices])
