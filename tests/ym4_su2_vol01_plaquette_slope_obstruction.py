"""YM4-VOL01: exact integer geometry test for the first L>2 transfer bridge.

For a periodic n^3 spatial SU2 lattice, n=2,3,4,5:
- every elementary plaquette occupies four distinct oriented positive links;
- for n>=3 distinct plaquettes share at most one link;
- thus <plaquette_i,V,plaquette_j> has no parity-supported term
  inside the four-fundamental plaquette span, so compressed first
  magnetic slope is the ZERO matrix, unlike the six K4,2 blocks at L=2.

This is an exact local support obstruction, not a volume-uniform
physical spectral-gap theorem. Integer-only; source independent of WG09.
"""
from itertools import combinations, product


def shifted(site, axis, n):
    return tuple((site[k] + int(k == axis)) % n for k in range(3))


def spatial_plaquettes(n):
    sites = tuple(product(range(n), repeat=3))
    links = tuple((s, d) for s in sites for d in range(3))
    ix = {link: k for k, link in enumerate(links)}
    out = []
    for s in sites:
        for a, b in combinations(range(3), 2):
            edges = ((s, a), (shifted(s, a, n), b),
                     (shifted(s, b, n), a), (s, b))
            assert len(set(edges)) == 4
            out.append(sum(1 << ix[edge] for edge in edges))
    assert len(out) == 3 * n ** 3
    assert len(set(out)) == len(out)
    return out


def run():
    expected = {
        2: (24, 156, 96, 24),
        3: (81, 2754, 486, 0),
        4: (192, 17184, 1152, 0),
        5: (375, 67875, 2250, 0),
    }
    rows = []
    for n in (2, 3, 4, 5):
        masks = spatial_plaquettes(n)
        support = set(masks)
        overlaps = [0] * 5
        magnetic_nonzero_candidates = 0
        for i, m in enumerate(masks):
            for other in masks[i + 1:]:
                common = (m & other).bit_count()
                overlaps[common] += 1
                if (m ^ other) in support:
                    magnetic_nonzero_candidates += 1
        assert (len(masks), overlaps[0], overlaps[1], overlaps[2]) == expected[n]
        assert overlaps[3] == overlaps[4] == 0
        assert magnetic_nonzero_candidates == 0
        # For n>=3 the lack of two-link loops is another physical
        # distinction from L=2's double-winding 4-fundamental basis.
        if n >= 3:
            assert overlaps[2] == 0
        rows.append(
            "YM4_VOL01_GEOMETRY|spatial_L=" + str(n)
            + "|spatial_plaquettes=" + str(len(masks))
            + "|plaquette_pairs_share2=" + str(overlaps[2])
            + "|first_order_P_to_P_parity_candidates=0|json=0"
        )
    rows.append(
        "YM4_VOL01_OBSTRUCTION|L2_six_K4_2_requires_double_windings=YES"
        "|L_ge3_plaquette_band_first_variation=ZERO"
        "|second_order_local_cluster_input=NEXT"
        "|volume_uniform_SU2_gap=OPEN|json=0"
    )
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    print(run(), end="")
