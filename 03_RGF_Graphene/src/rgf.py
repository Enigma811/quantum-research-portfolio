"""
Recursive Green's function (RGF) algorithm for a block-tridiagonal
conductor Hamiltonian (h[0..N-1], u[0..N-2]) contacted by a left and a
right lead self-energy.

Implements:
  - forward (left-connected) sweep g^L_{n,n}
  - backward (right-connected) sweep g^R_{n,n}
  - transmission via the boundary Green's function G_{N-1,0}
  - full diagonal blocks G_{n,n} (for the local density of states) by
    combining the left- and right-connected quantities at each slice,
    exactly as described in the report (Sec. 4.4).
"""

import numpy as np
from numpy.linalg import inv


def forward_sweep(z, h, u, sigma_L):
    """Left-connected recursion. Returns list g_L[n], n=0..N-1 (no Sigma_R
    included anywhere)."""
    N = len(h)
    g_L = [None] * N
    g_L[0] = inv(z * np.eye(h[0].shape[0]) - h[0] - sigma_L)
    for n in range(1, N):
        prev = u[n - 1].conj().T @ g_L[n - 1] @ u[n - 1]
        g_L[n] = inv(z * np.eye(h[n].shape[0]) - h[n] - prev)
    return g_L


def backward_sweep(z, h, u, sigma_R):
    """Right-connected recursion. Returns list g_R[n], n=0..N-1 (no Sigma_L
    included anywhere)."""
    N = len(h)
    g_R = [None] * N
    g_R[N - 1] = inv(z * np.eye(h[-1].shape[0]) - h[-1] - sigma_R)
    for n in range(N - 2, -1, -1):
        nxt = u[n] @ g_R[n + 1] @ u[n].conj().T
        g_R[n] = inv(z * np.eye(h[n].shape[0]) - h[n] - nxt)
    return g_R


def transmission(z, h, u, sigma_L, sigma_R, gamma_L, gamma_R):
    """
    Transmission T(E) = Tr[Gamma_L G^r_{N-1,0} Gamma_R G^a_{0,N-1}]
    obtained from a single forward sweep, tracking the boundary block
    G_{n,0} alongside g^L_{n,n} (standard RGF transmission recursion).
    """
    N = len(h)
    g_L = [None] * N
    G_col0 = [None] * N  # G_{n,0}, partial (no Sigma_R yet)

    g_L[0] = inv(z * np.eye(h[0].shape[0]) - h[0] - sigma_L)
    G_col0[0] = g_L[0]
    for n in range(1, N):
        prev = u[n - 1].conj().T @ g_L[n - 1] @ u[n - 1]
        g_L[n] = inv(z * np.eye(h[n].shape[0]) - h[n] - prev)
        G_col0[n] = g_L[n] @ u[n - 1].conj().T @ G_col0[n - 1]

    # include the right lead self-energy at the last slice (Dyson equation)
    gL_last_inv = inv(g_L[-1])
    G_last_full = inv(gL_last_inv - sigma_R)
    G_col0_full = G_last_full @ gL_last_inv @ G_col0[-1]  # G_{N-1,0}

    T = np.trace(gamma_L @ G_col0_full.conj().T @ gamma_R @ G_col0_full).real
    return T, G_col0_full


def full_diagonal_blocks(z, h, u, sigma_L, sigma_R):
    """
    Full retarded Green's function diagonal blocks G_{n,n} for every slice,
    combining left- and right-connected quantities (used for LDOS).
    """
    N = len(h)
    g_L = forward_sweep(z, h, u, sigma_L)
    g_R = backward_sweep(z, h, u, sigma_R)

    G_diag = [None] * N
    G_diag[0] = inv(inv(g_L[0]) - u[0] @ g_R[1] @ u[0].conj().T) if N > 1 else inv(inv(g_L[0]) - sigma_R)
    for n in range(1, N - 1):
        coupR = u[n] @ g_R[n + 1] @ u[n].conj().T
        G_diag[n] = inv(inv(g_L[n]) - coupR)
    if N > 1:
        G_diag[N - 1] = inv(inv(g_L[N - 1]) - sigma_R)
    return G_diag


def ldos_from_diag(G_diag):
    """rho_n(E) per-site local density of states, rho = -Im(diag(G))/pi."""
    return [-np.diag(G).imag / np.pi for G in G_diag]
