"""YM4-VOL02 exact independent 2-chain parity witness for SU2 L>=3.

The accompanying mathematics proves that every nonempty mod-two
2-cycle on an L>=3 periodic cubical 3-torus has >=6 faces. This
enumeration exercises up to five-face supports on L=2,3,4,5.

No physical volume-uniform spectral estimate is asserted.
"""
from itertools import combinations, product
from collections import Counter


def plaquette_masks(n):
    sites = tuple(product(range(n), repeat=3))
    ix = {(s, d): k for k, (s, d) in enumerate(
        (s, d) for s in sites for d in range(3))}

    def shifted(site, d):
        return tuple((site[k] + int(k == d)) % n for k in range(3))

    out = tuple(sum(1 << ix[e] for e in (
        (s, a), (shifted(s, a), b), (shifted(s, b), a), (s, b)))
        for s in sites for a, b in combinations(range(3), 2))
    assert len(out) == 3 * n * n * n and len(set(out)) == len(out)
    return out


def certify():
    expected = {2: (24, 276, 36), 3: (81, 3240, 0),
                4: (192, 18336, 0), 5: (375, 70125, 0)}
    rows = []
    for n in (2, 3, 4, 5):
        masks = plaquette_masks(n)
        pair = Counter(p ^ q for p in masks for q in masks)
        assert pair[0] == len(masks)

        # For any five-face SU2 product, designate any two factors
        # as initial/final plaquettes; the three remaining insertions
        # have parity support m_i XOR m_j. Count every possibility
        # exactly using a pair-XOR convolution.
        nonzero = 0
        pair_nonunique = 0
        pair_count = 0
        for i, p in enumerate(masks):
            for j in range(i+1, len(masks)):
                q = masks[j]
                pair_count += 1
                alternatives = pair[p ^ q]
                assert alternatives >= 2
                if alternatives > 2:
                    pair_nonunique += 1
                if n >= 3:
                    assert alternatives == 2
                if any(pair[p ^ q ^ r] for r in masks):
                    nonzero += 1
        # Diagonal third-order matrix elements would require any three
        # plaquette factors to form a mod-two closed 2-chain.
        diag_third = sum(pair[r] for r in masks)
        assert (len(masks), pair_count, pair_nonunique) == expected[n]
        assert diag_third == 0 and nonzero == 0
        rows.append(
            "YM4_VOL02_PARITY|spatial_L=" + str(n)
            + "|plaquettes=" + str(len(masks))
            + "|offdiag_pairs=" + str(pair_count)
            + "|nonunique_two_insertions=" + str(pair_nonunique)
            + "|third_order_diagonal_parity=0"
            + "|third_order_offdiagonal_parity=0|json=0"
        )
    rows.append(
        "YM4_VOL02_EXACT|L_ge3_nonempty_cycle_min_faces_ge6"
        "=PROVED_IN_NOTE|PVP=ZERO|PV3P=ZERO|PV2_vac=ZERO"
        "|second_order_band=SCALAR"
        "|first_nonscalar_possible_order=FOURTH"
        "|volume_uniform_mass_gap=OPEN|continuum_mass_gap=OPEN|json=0"
    )
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    print(certify(), end="")
