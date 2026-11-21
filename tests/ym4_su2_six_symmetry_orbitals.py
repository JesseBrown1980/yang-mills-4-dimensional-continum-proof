"""WG09 structural pilot: exact 6-mode orbit algebra, not a spectral-order theorem.

Original L=2 spatial SU(2) electric supports, 48 spatial symmetries,
and WG06 first-magnetic support adjacency are rebuilt with integers only.
The V^2 support counts are necessary center-parity filters, NOT Haar
matrix elements. No finite-beta energy ordering is asserted.
"""
from itertools import combinations, permutations, product


def certify():
    sites = tuple(product((0, 1), repeat=3))
    links = tuple((s, d) for s in sites for d in range(3))
    index = {edge: i for i, edge in enumerate(links)}

    def shifted(site, axis):
        return tuple(site[d] ^ (d == axis) for d in range(3))

    def bitmask(edges):
        assert len(set(edges)) == len(edges)
        return sum(1 << index[e] for e in edges)

    plaquettes = tuple(bitmask((
        (s, a), (shifted(s, a), b),
        (shifted(s, b), a), (s, b)))
        for s in sites for a, b in combinations(range(3), 2))
    doubles = []
    for axis in range(3):
        transverse_axes = tuple(d for d in range(3) if d != axis)
        winds = []
        for t in product((0, 1), repeat=2):
            s = tuple(dict(zip(transverse_axes, t)).get(d, 0)
                      for d in range(3))
            winds.append(bitmask(((s, axis), (shifted(s, axis), axis))))
        doubles.extend(winds[i] | winds[j] for i, j in combinations(range(4), 2))
    masks = plaquettes + tuple(doubles)
    assert len(links) == 24 and len(plaquettes) == 24
    assert len(masks) == len(set(masks)) == 42
    pset = set(plaquettes)
    A = tuple(tuple(int(i != j and (masks[i] ^ masks[j]) in pset)
                    for j in range(42)) for i in range(42))
    assert sum(map(sum, A)) // 2 == 48
    seen, comps = set(), []
    for i in range(42):
        if i in seen:
            continue
        component = [i]
        seen.add(i)
        for v in component:
            for w in range(42):
                if A[v][w] and w not in seen:
                    component.append(w)
                    seen.add(w)
        comps.append(tuple(sorted(component)))
    blocks = tuple(c for c in comps if len(c) == 6)
    assert len(blocks) == 6 and sorted(map(len, comps)) == [1] * 6 + [6] * 6
    byindex = {i: b for b, comp in enumerate(blocks) for i in comp}
    mindex = {m: i for i, m in enumerate(masks)}

    def image(mask, shift, perm):
        result = 0
        for i, (s, axis) in enumerate(links):
            if mask & (1 << i):
                ns = tuple(s[perm[d]] ^ shift[d] for d in range(3))
                result |= 1 << index[(ns, perm.index(axis))]
        return result

    actions = []
    for sh in product((0, 1), repeat=3):
        for perm in permutations(range(3)):
            g = tuple(mindex[image(mask, sh, perm)] for mask in masks)
            assert all(A[i][j] == A[g[i]][g[j]]
                       for i in range(42) for j in range(42))
            actions.append(tuple(byindex[g[blocks[b][0]]] for b in range(6)))
    assert len(actions) == len(set(actions)) == 48
    unseen = {(i, j) for i in range(6) for j in range(6)}
    orbitals = []
    while unseen:
        i, j = min(unseen)
        orbit = {(g[i], g[j]) for g in actions}
        assert orbit <= unseen
        orbitals.append(orbit)
        unseen -= orbit
    assert sorted(map(len, orbitals)) == [6, 6, 24]
    opposite = next(orbit for orbit in orbitals
                    if len(orbit) == 6 and all(i != j for i, j in orbit))
    assert all(sum(1 for i, j in opposite if i == k) == 1 for k in range(6))
    O = tuple(tuple(int((i, j) in opposite) for j in range(6))
              for i in range(6))
    X = tuple(tuple(int(i != j and not O[i][j]) for j in range(6))
              for i in range(6))
    I = tuple(tuple(int(i == j) for j in range(6)) for i in range(6))
    J = tuple((1,) * 6 for _ in range(6))

    def multiply(A, B):
        return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(6))
                           for j in range(6)) for i in range(6))

    a, b, c = 11, 7, 3
    H = tuple(tuple(a * I[i][j] + b * O[i][j] + c * X[i][j]
                    for j in range(6)) for i in range(6))
    Q1 = J  # 6 times rank-one invariant projector
    Q2 = tuple(tuple(3 * (I[i][j] + O[i][j]) - J[i][j]
                     for j in range(6)) for i in range(6))  # 6 P_even
    Q3 = tuple(tuple(I[i][j] - O[i][j] for j in range(6))
               for i in range(6))  # 2 P_odd
    assert sum(Q1[i][i] for i in range(6)) == 6
    assert sum(Q2[i][i] for i in range(6)) == 12
    assert sum(Q3[i][i] for i in range(6)) == 6
    assert multiply(H, Q1) == tuple(tuple((a+b+4*c)*e for e in row) for row in Q1)
    assert multiply(H, Q2) == tuple(tuple((a+b-2*c)*e for e in row) for row in Q2)
    assert multiply(H, Q3) == tuple(tuple((a-b)*e for e in row) for row in Q3)

    # Necessary per-link parity filter for two insertions of V=sum_p W_p.
    # Counts are integer support witnesses; they are not Haar amplitudes.
    candidates = []
    for ia in range(6):
        row = []
        for ib in range(6):
            total = sum(int((masks[i] ^ masks[j]) == (p ^ q))
                        for i in blocks[ia] for j in blocks[ib]
                        for p in plaquettes for q in plaquettes)
            row.append(total)
        candidates.append(row)
    assert all(candidates[i][j] == (200 if i == j else 32)
               for i in range(6) for j in range(6))
    return ("YM4_WG09_STRUCTURE|original_L2_SU2_supports=42|magnetic_edges=48"
            "|six_K4_2=YES|isolates=6\n"
            "YM4_WG09_SYMMETRY|48_affine_spatial_actions=EXACT"
            "|six_block_action=FAITHFUL|pair_orbitals=6,6,24\n"
            "YM4_WG09_ALGEBRA|commutant_basis=I,O,X"
            "|ranks=1,2,3|eigenvalues=a+b+4c,a+b-2c,a-b\n"
            "YM4_WG09_V2_PARITY|ordered_support_candidates_diagonal=200"
            "|offdiagonal=32|Haar_coefficients=OPEN\n"
            "YM4_WG09_VERDICT|symmetry_reduction=PASS"
            "|effective_b_c=OPEN|full_beta3_remainder=OPEN"
            "|first_neutral_energy_order=OPEN\n")


if __name__ == '__main__':
    print(certify(), end='')
