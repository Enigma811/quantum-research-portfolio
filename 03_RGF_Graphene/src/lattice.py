"""
Honeycomb (graphene) lattice generator + slicing into a block-tridiagonal
tight-binding Hamiltonian, for use with the recursive Green's function (RGF)
method.

Convention (matches Fig. 1 of the project report):
    a1 = a0 * (3/2,  sqrt(3)/2)
    a2 = a0 * (3/2, -sqrt(3)/2)
    A sublattice sits on the Bravais lattice R = n1*a1 + n2*a2
    B sublattice sits at R + delta1,  delta1 = a0*(0, 1)
    a0 = nearest-neighbour (C-C) bond length, set to 1 (energy unit t=1).

Nearest-neighbour bonds are found geometrically (cKDTree), not by hand-coded
index algebra, so the construction is robust for any rotation/orientation of
the ribbon.

A ribbon is produced by carving a rectangular window x in [0, Lx), y in
[0, Ly) out of an (optionally rotated) infinite sheet, then partitioning the
surviving atoms into "slices" by their x-coordinate. Because nearest-neighbour
bonds have length a0=1 and successive slices are separated by less than that,
each slice only ever couples to its immediate left/right neighbour slice --
i.e. the Hamiltonian is exactly block-tridiagonal, which is what the RGF
algorithm needs.
"""

import numpy as np
from scipy.spatial import cKDTree

A0 = 1.0  # bond length, energy unit is the hopping t (set separately)


def _rotation(theta_deg):
    th = np.deg2rad(theta_deg)
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s], [s, c]])


def generate_sheet(n1_range, n2_range, theta_deg=0.0):
    """Generate honeycomb sheet coordinates (A and B sublattices) for a
    range of Bravais indices, optionally rotated by theta_deg (degrees).

    Bond vectors from an A site (matches Fig. 1 of the report: delta1 up,
    delta2 lower-right, delta3 lower-left), all of length a0:
        delta1 = a0*(0, 1)
        delta2 = a0*(sqrt(3)/2, -1/2)
        delta3 = a0*(-sqrt(3)/2, -1/2)
    Primitive (Bravais) vectors are then a1 = delta1-delta2, a2 = delta1-delta3,
    which is what actually gives equal (=a0) bond length for ALL three
    nearest-neighbour bonds (a naive guess of a1,a2 does not, in general)."""
    delta1 = A0 * np.array([0.0, 1.0])
    delta2 = A0 * np.array([np.sqrt(3) / 2, -0.5])
    delta3 = A0 * np.array([-np.sqrt(3) / 2, -0.5])
    a1 = delta1 - delta2
    a2 = delta1 - delta3

    n1, n2 = np.meshgrid(n1_range, n2_range, indexing="ij")
    n1 = n1.ravel()
    n2 = n2.ravel()
    R = n1[:, None] * a1[None, :] + n2[:, None] * a2[None, :]

    posA = R
    posB = R + delta1[None, :]

    pos = np.vstack([posA, posB])
    sub = np.array([0] * len(posA) + [1] * len(posB))  # 0=A, 1=B

    rot = _rotation(theta_deg)
    pos = pos @ rot.T
    return pos, sub


EDGE_THETA = {"zigzag": 0.0, "armchair": 30.0}
EDGE_GROUP = {"zigzag": 1, "armchair": 2}


def find_commensurate_size(Lx_target, Ly_target, edge, search=6):
    """
    A straight rectangular cut through the honeycomb lattice only gives a
    perfectly uniform (translationally invariant) set of slices -- required
    for defining an ideal semi-infinite lead -- for specific commensurate
    (Lx, Ly). This does a small local search around the requested size and
    returns the nearest commensurate (Lx, Ly).
    """
    theta = EDGE_THETA[edge]
    group = EDGE_GROUP[edge]
    best = None
    for dLy in range(0, search):
        for dLx in range(0, search):
            for Ly in {Ly_target + dLy, Ly_target - dLy}:
                for Lx in {Lx_target + dLx, Lx_target - dLx}:
                    if Lx <= 0 or Ly <= 0:
                        continue
                    slices, bonds, pos, sub, slice_of, n_bad = build_ribbon(Lx, Ly, theta_deg=theta)
                    if n_bad or len(slices) < 2:
                        continue
                    sizes = [len(s["pos"]) for s in slices]
                    if group > 1:
                        # widths must repeat with the given group period, AND
                        # the number of raw slices must be a multiple of the
                        # group size so merging leaves no leftover partial group
                        ok = (len(sizes) % group == 0) and all(
                            sizes[i] == sizes[i % group] for i in range(len(sizes)))
                    else:
                        ok = len(set(sizes)) == 1
                    if ok:
                        score = abs(Lx - Lx_target) + abs(Ly - Ly_target)
                        if best is None or score < best[0]:
                            best = (score, Lx, Ly)
        if best is not None:
            break
    if best is None:
        raise RuntimeError("no commensurate ribbon size found in search range")
    return best[1], best[2]


def build_ribbon(Lx, Ly, theta_deg=0.0, pad=6, x_tol=1e-3):
    """
    Carve a rectangular ribbon [0,Lx) x [0,Ly) out of an infinite sheet
    rotated by theta_deg, then group atoms into slices along x.

    Returns
    -------
    slices : list of dict, one per slice n, each with
        'pos'   : (n_i,2) array of atom coordinates in this slice
        'sub'   : (n_i,) sublattice index (0=A,1=B)
        'x'     : scalar x-coordinate of this slice (all atoms share it)
    bonds : (n_bonds,2) int array of GLOBAL atom indices (for diagnostics)
    all_pos, all_sub : full atom arrays (for plotting)
    slice_of : (n_atoms,) which slice index each atom belongs to
    """
    # Overshoot the Bravais index range enough to cover the rotated window
    span = max(Lx, Ly) / A0
    n_range = np.arange(-int(span) - pad, int(span) + pad)
    pos, sub = generate_sheet(n_range, n_range, theta_deg=theta_deg)

    keep = (pos[:, 0] >= -1e-6) & (pos[:, 0] < Lx) & (pos[:, 1] >= -1e-6) & (pos[:, 1] < Ly)
    pos = pos[keep]
    sub = sub[keep]

    # group into slices by rounded x-coordinate
    xr = np.round(pos[:, 0] / x_tol) * x_tol
    x_unique = np.unique(xr)
    slice_of = np.searchsorted(x_unique, xr)

    n_slices = len(x_unique)
    order = np.argsort(slice_of, kind="stable")
    pos = pos[order]
    sub = sub[order]
    slice_of = slice_of[order]

    # nearest-neighbour bonds via KDTree (bond length A0, small tolerance)
    tree = cKDTree(pos)
    pairs = tree.query_pairs(r=A0 * 1.01, output_type="ndarray")
    d = np.linalg.norm(pos[pairs[:, 0]] - pos[pairs[:, 1]], axis=1)
    bonds = pairs[d > A0 * 0.9]  # drop accidental same-site / far pairs

    slices = []
    for n in range(n_slices):
        idx = np.where(slice_of == n)[0]
        slices.append({"pos": pos[idx], "sub": sub[idx], "x": x_unique[n], "global_idx": idx})

    # sanity check: verify strictly nearest-neighbour slice coupling only
    bad = np.abs(slice_of[bonds[:, 0]] - slice_of[bonds[:, 1]]) > 1
    n_bad = int(bad.sum())

    return slices, bonds, pos, sub, slice_of, n_bad


def merge_slices(h, u, group_size):
    """
    Merge every `group_size` consecutive raw slices into one super-slice.
    Needed for armchair-edge ribbons, whose raw per-atom-row slicing has a
    period-2 pattern of alternating slice widths (see Fig. 2 of the report);
    grouping two raw slices restores an exactly periodic block-tridiagonal
    chain, which is what a uniform semi-infinite lead requires. Bonds within
    a group become part of the merged on-site block; bonds that cross a
    group boundary remain the inter-slice coupling (this stays exact because
    the raw chain is itself strictly nearest-neighbour block-tridiagonal).
    """
    if group_size == 1:
        return h, u
    n_raw = len(h)
    n_groups = int(np.ceil(n_raw / group_size))
    sizes_raw = [hh.shape[0] for hh in h]

    h_new, u_new = [], []
    offset = 0
    group_bounds = []
    for g in range(n_groups):
        lo = g * group_size
        hi = min(lo + group_size, n_raw)
        group_bounds.append((lo, hi))
        dim = sum(sizes_raw[lo:hi])
        Hg = np.zeros((dim, dim), dtype=complex)
        off = 0
        offs_local = []
        for k in range(lo, hi):
            offs_local.append(off)
            Hg[off:off + sizes_raw[k], off:off + sizes_raw[k]] = h[k]
            off += sizes_raw[k]
        for k in range(lo, hi - 1):
            i0, i1 = offs_local[k - lo], offs_local[k - lo + 1]
            s0, s1 = sizes_raw[k], sizes_raw[k + 1]
            Hg[i0:i0 + s0, i1:i1 + s1] = u[k]
            Hg[i1:i1 + s1, i0:i0 + s0] = u[k].conj().T
        h_new.append(Hg)

    for g in range(n_groups - 1):
        lo, hi = group_bounds[g]
        lo2, hi2 = group_bounds[g + 1]
        dim1 = sum(sizes_raw[lo:hi])
        dim2 = sum(sizes_raw[lo2:hi2])
        Ug = np.zeros((dim1, dim2), dtype=complex)
        # only the last raw slice of group g couples to the first raw slice of group g+1
        last_local_off = sum(sizes_raw[lo:hi - 1])
        Ug[last_local_off:last_local_off + sizes_raw[hi - 1], 0:sizes_raw[lo2]] = u[hi - 1]
        u_new.append(Ug)

    return h_new, u_new


def hamiltonian_blocks(slices, bonds, slice_of, t=1.0, onsite=0.0):
    """
    Build the block-tridiagonal tight-binding Hamiltonian from the sliced
    ribbon: on-site blocks h[n] (n_i x n_i) and inter-slice coupling blocks
    u[n] connecting slice n -> slice n+1 (n_i x n_{i+1}).
    """
    n_slices = len(slices)
    sizes = [len(s["pos"]) for s in slices]

    # local index within each slice, for global atom index
    local_index = np.zeros(len(slice_of), dtype=int)
    for s in slices:
        local_index[s["global_idx"]] = np.arange(len(s["global_idx"]))

    h = [np.full((sz, sz), 0j) for sz in sizes]
    for hn in h:
        hn[:, :] = 0.0
    h = [np.eye(sz, dtype=complex) * onsite for sz in sizes]
    u = [np.zeros((sizes[n], sizes[n + 1]), dtype=complex) for n in range(n_slices - 1)]

    for i, j in bonds:
        ni, nj = slice_of[i], slice_of[j]
        li, lj = local_index[i], local_index[j]
        if ni == nj:
            h[ni][li, lj] = -t
            h[ni][lj, li] = -t
        elif abs(ni - nj) == 1:
            n_lo = min(ni, nj)
            if ni < nj:
                u[n_lo][li, lj] = -t
            else:
                u[n_lo][lj, li] = -t
        else:
            raise RuntimeError("non-nearest-neighbour slice coupling encountered")

    return h, u
