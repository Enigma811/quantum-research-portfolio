"""
Semi-infinite lead surface Green's functions (Lopez-Sancho, Lopez-Sancho &
Rubio decimation, J. Phys. F 14, 1205 (1984); 15, 851 (1985)) and lead
self-energies for the RGF method.

Convention: the ribbon's block-tridiagonal Hamiltonian has on-site blocks
h[n] and inter-slice coupling u[n] with H[n, n+1] = u[n]  (so H[n+1, n] =
u[n]^dagger). The leads are modeled as semi-infinite repetitions of the
device's own end unit cells (h_lead = h[0] or h[-1], u_lead = u[0] or u[-2]),
i.e. ideal, reflectionless contacts made of the same material as the ribbon
-- this is the standard "same-material lead" convention used for computing
intrinsic ballistic conductance.
"""

import numpy as np
from numpy.linalg import inv, norm


def surface_gf(z, h00, alpha, beta, tol=1e-12, max_iter=500):
    """
    Decimation algorithm for the surface Green's function of a semi-infinite
    1D chain of identical blocks with on-site h00, and alpha = hopping from
    the surface layer INTO the bulk (i.e. away from where the lead attaches),
    beta = alpha^dagger.

    Returns g00 = surface layer Green's function at energy z (z = E + i*eta).
    """
    dim = h00.shape[0]
    I = np.eye(dim, dtype=complex)
    eps_s = h00.copy()
    eps = h00.copy()
    a = alpha.copy()
    b = beta.copy()
    for _ in range(max_iter):
        g = inv(z * I - eps)
        ag = a @ g
        bg = b @ g
        eps_s = eps_s + ag @ b
        eps = eps + ag @ b + bg @ a
        a_new = ag @ a
        b_new = bg @ b
        a, b = a_new, b_new
        if norm(a) < tol and norm(b) < tol:
            break
    return inv(z * I - eps_s)


def left_self_energy(z, h_lead, u, eta=1e-6, **kwargs):
    """
    Self-energy of a semi-infinite LEFT lead (made of repeated (h_lead, u)
    cells) attached to the first device slice via coupling u
    (H[lead_surface, device_slice0] = u).
    """
    dim = h_lead.shape[0]
    g_L = surface_gf(z, h_lead, alpha=u.conj().T, beta=u, **kwargs)
    return u.conj().T @ g_L @ u


def right_self_energy(z, h_lead, u, eta=1e-6, **kwargs):
    """
    Self-energy of a semi-infinite RIGHT lead attached to the last device
    slice via coupling u (H[device_last, lead_surface] = u).
    """
    g_R = surface_gf(z, h_lead, alpha=u, beta=u.conj().T, **kwargs)
    return u @ g_R @ u.conj().T


def gamma(sigma):
    """Level-width (broadening) matrix Gamma = i(Sigma^R - Sigma^A) = i(Sigma - Sigma^dagger)."""
    return 1j * (sigma - sigma.conj().T)
