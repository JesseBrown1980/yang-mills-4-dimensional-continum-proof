"""VOL03 continuous SU2 exact six-face cube Haar plus conditional cell-tree.

Only the local cube Haar integrals are physical. The cell-tree inputs
are abstract numerical test fixtures, awaiting independently certified
SU2 fourth-order physical Schur block bounds. Integer-only.
"""
from collections import defaultdict
from itertools import combinations, product

Q = {}
for i in range(4):
    for j in range(4):
        if i == 0:
            Q[i, j] = (1, j)
        elif j == 0:
            Q[i, j] = (1, i)
        elif i == j:
            Q[i, j] = (-1, 0)
        elif (i, j) in ((1, 2), (2, 3), (3, 1)):
            Q[i, j] = (1, 6 - i - j)
        else:
            Q[i, j] = (-1, 6 - i - j)


def shift(s, axis, n):
    return tuple((s[d] + int(d == axis)) % n for d in range(3))


def plaquette(s, a, b, n):
    return ((s, a, 1), (shift(s, a, n), b, 1),
            (shift(s, b, n), a, -1), (s, b, -1))


def cube_faces(s, n):
    lo = tuple(plaquette(s, a, b, n)
               for a, b in combinations(range(3), 2))
    hi = tuple(plaquette(shift(s, k, n), a, b, n)
               for a, b, k in ((0, 1, 2), (0, 2, 1), (1, 2, 0)))
    return lo + hi


def trace_tensor(face):
    labels = tuple((s, d) for s, d, orient in face)
    signs = tuple(orient for s, d, orient in face)
    out = {}
    for keys in product(range(4), repeat=4):
        state = 0
        sign = 1
        for key, orient in zip(keys, signs):
            update, state = Q[state, key]
            sign *= update
            if orient < 0 and key:
                sign = -sign
        if state == 0:
            out[keys] = 2 * sign
    return labels, out


def contract(tensors):
    while len(tensors) > 1:
        choices = []
        for i in range(len(tensors)):
            for j in range(i + 1, len(tensors)):
                a, ad = tensors[i]
                b, bd = tensors[j]
                common = set(a) & set(b)
                choices.append(((len(set(a) | set(b)) - len(common),
                                 -len(common), len(ad) * len(bd)), i, j))
        _, i, j = min(choices)
        a, da = tensors[i]
        b, db = tensors[j]
        common = tuple(v for v in a if v in b)
        ia = {v: k for k, v in enumerate(a)}
        ib = {v: k for k, v in enumerate(b)}
        ak = tuple((v, k) for k, v in enumerate(a) if v not in common)
        bk = tuple((v, k) for k, v in enumerate(b) if v not in common)
        buckets = defaultdict(list)
        for keys, value in db.items():
            buckets[tuple(keys[ib[v]] for v in common)].append((keys, value))
        out = defaultdict(int)
        for ka, va in da.items():
            for kb, vb in buckets.get(tuple(ka[ia[v]] for v in common), ()):
                key = tuple(ka[k] for v, k in ak) + tuple(kb[k] for v, k in bk)
                out[key] += va * vb
        remaining = tuple(v for v, k in ak) + tuple(v for v, k in bk)
        for k in sorted((i, j), reverse=True):
            tensors.pop(k)
        tensors.append((remaining, {k: v for k, v in out.items() if v}))
    labels, result = tensors[0]
    assert not labels
    return result.get((), 0)


def cube_integral(n):
    faces = cube_faces((0, 0, 0), n)
    appearances = defaultdict(list)
    for face_no, face in enumerate(faces):
        for s, d, orient in face:
            appearances[s, d].append(face_no)
    assert len(faces) == 6 and len(appearances) == 12
    assert all(len(v) == 2 for v in appearances.values())
    numerator = contract([trace_tensor(face) for face in faces])
    denominator = 1
    for unused in appearances:
        denominator *= 4
    assert numerator == 1048576
    assert denominator == 16777216
    assert numerator * 16 == denominator
    # Four inserted W=chi/2 contribute 1/16; ordering 4! cancels 1/4!.
    assert numerator * 256 == denominator * 16
    return numerator, denominator


def parent_lower(children, cross_norm):
    assert len(children) == 2 and cross_norm >= 0
    return min(children) - cross_norm


def conditional_assembly_fixture():
    # Exact abstract two-block eigenvalue theorem:
    # lambda_min([[A,B],[B*,D]])>=min(g_A,g_D)-||B||.
    # Demo values have not been measured from the SU2 physical operator.
    leaves = (12, 12, 12, 12, 12, 12, 12, 12)
    middle = tuple(parent_lower(leaves[i:i + 2], 1)
                   for i in range(0, 8, 2))
    upper = tuple(parent_lower(middle[i:i + 2], 2)
                  for i in range(0, 4, 2))
    top = parent_lower(upper, 4)
    assert middle == (11, 11, 11, 11)
    assert upper == (9, 9) and top == 5
    assert parent_lower((2, 2), 3) == -1
    return top


def certify():
    assert cube_integral(3) == cube_integral(4)
    assert conditional_assembly_fixture() == 5
    return (
        "YM4_VOL03_HAAR|group=continuous_SU2|spatial_L=3_4"
        "|cube_faces=6|unique_links=12|integral_six_trace=1/16"
        "|raw_W_fourth_cube_contribution=1/256|integer_only=YES|json=0\n"
        "YM4_VOL03_TREE|two_block_lower=min_children-minus_cross_norm"
        "|test_levels=8_4_2_1|test_floor=5"
        "|negative_control=REJECT_NONPOSITIVE|SU2_input=NOT_CERTIFIED|json=0\n"
        "YM4_VOL03_EXTERNAL|navier_lean_comparator=PINNED_REFERENCE"
        "|numerical_certificate=UNAVAILABLE"
        "|source_link_math_import=NONE|json=0\n"
        "YM4_VOL03_VERDICT|local_cube_Haar=EXACT"
        "|global_fourth_Feshbach=OPEN|volume_uniform_gap=OPEN"
        "|continuum_mass_gap=OPEN|json=0\n"
    )


if __name__ == "__main__":
    print(certify(), end="")
