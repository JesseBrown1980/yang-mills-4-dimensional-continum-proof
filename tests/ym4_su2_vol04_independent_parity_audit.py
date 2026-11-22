"""Independent VOL04 clean-room six-face parity-count falsifier.

Uses only original periodic L^3 link incidence, XOR convolution of
ordered two-plaquette insertions, and elementary-cube incidence.
No imports from any WG/VOL producer. Integer-only.

At each pair (i,j), the complete parity-admissible ordered V^4 terms
are 12*N-16 disconnected repeated-face words plus 24 for each cube
whose boundary contains both designated faces. This source counts
all pairs at L=3, four representative pair types at L=4 and L=5.
The SU2 Haar weights are separately derived in the VOL04 proof note.
"""
from collections import Counter
from itertools import combinations, product


def inc(site, axis, n):
    return tuple((site[k] + int(k == axis)) % n for k in range(3))


def reconstruct(n):
    sites = tuple(product(range(n), repeat=3))
    links = {(s, d): i for i, (s, d) in enumerate(
        (s, d) for s in sites for d in range(3))}
    faces = tuple((s, a, b) for s in sites
                  for a, b in combinations(range(3), 2))
    face_index = {v: i for i, v in enumerate(faces)}
    masks = []
    for s, a, b in faces:
        edge_keys = ((s, a), (inc(s, a, n), b),
                     (inc(s, b, n), a), (s, b))
        assert len(set(edge_keys)) == 4
        masks.append(sum(1 << links[e] for e in edge_keys))
    assert len(set(masks)) == 3 * n * n * n
    cubes = Counter()
    for site in sites:
        f = []
        for a, b in combinations(range(3), 2):
            other = 3 - a - b
            f.extend((face_index[site, a, b],
                      face_index[inc(site, other, n), a, b]))
        assert len(set(f)) == 6
        for i, j in combinations(sorted(f), 2):
            cubes[i, j] += 1
    assert all(v == 1 for v in cubes.values())
    return masks, cubes


def four_count(d, pair_xor):
    return sum(weight * pair_xor.get(x ^ d, 0)
               for x, weight in pair_xor.items())


def certify():
    rows = []
    for n in (3, 4, 5):
        masks, cubes = reconstruct(n)
        N = len(masks)
        pair_xor = Counter(p ^ q for p in masks for q in masks)
        assert pair_xor[0] == N
        assert all(v == 2 for k, v in pair_xor.items() if k)
        assert four_count(0, pair_xor) == 3 * N * N - 2 * N
        types = {}
        checked = 0
        for i in range(N):
            for j in range(i + 1, N):
                c = bool(cubes.get((i, j), 0))
                e = (masks[i] & masks[j]).bit_count() == 1
                kind = (c, e)
                if n != 3 and kind in types:
                    continue
                lhs = four_count(masks[i] ^ masks[j], pair_xor)
                rhs = 12 * N - 16 + 24 * int(c)
                assert lhs == rhs, (n, i, j, lhs, rhs)
                types[kind] = (i, j)
                checked += 1
        assert len(types) == 4
        assert checked == (N * (N - 1)) // 2 if n == 3 else checked == 4
        rows.append(
            "YM4_VOL04_AUDIT|L=" + str(n)
            + "|N=" + str(N)
            + "|ordered_four_parity_pair_checks=" + str(checked)
            + "|pair_types=4"
            + "|cube_boundary_extra_words=24"
            + "|disconnected_words=12N-16"
            + "|all_checks=PASS|json=0"
        )
    rows.append(
        "YM4_VOL04_AUDIT_VERDICT|L3_complete_pairs=PASS"
        "|L4_L5_all_four_pair_types=PASS"
        "|local_SU2_Haar_weights=SEPARATE_EXACT_PROOF"
        "|volume_uniform_beta_remainder=OPEN|json=0"
    )
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    print(certify(), end="")
