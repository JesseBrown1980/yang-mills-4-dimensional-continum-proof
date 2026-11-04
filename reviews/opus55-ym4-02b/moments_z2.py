# Claim 3: E[X^2], E[X^3], E[X^4] on (Z/2Z)^4. Own enumeration of ALL multisets with no symmetry reduction; every integrand evaluated by polynomial Haar integration,
# memoised only on identical integrand after renaming independent link variables. Also tests the script's filter and its symmetry group directly.
import itertools
import math
import sys

sys.path.insert(0, "C:/tmp/opus55/attack-4d-20261103/ym4-02b")
from haarpoly import expect_words, qadd, qmul, red
from grp import build, qmul as gq, table, ZZ

SIDE = 2
D = 4
SITES = list(itertools.product(range(SIDE), repeat=D))


def shift(x, mu):
    y = list(x)
    y[mu] = (y[mu] + 1) % SIDE
    return tuple(y)


# plaquette word, repository convention: U_mu(x) U_nu(x+mu) U_mu(x+nu)^-1 U_nu(x)^-1
PLAQ = []
for x in SITES:
    for mu in range(D):
        for nu in range(mu + 1, D):
            PLAQ.append((x, mu, nu))
WORD = {p: [((p[0], p[1]), 1), ((shift(p[0], p[1]), p[2]), 1), ((shift(p[0], p[2]), p[1]), -1), ((p[0], p[2]), -1)] for p in PLAQ}
LINKS = sorted({l for p in PLAQ for l, _ in WORD[p]})
LID = {l: i for i, l in enumerate(LINKS)}
assert len(PLAQ) == 96 and len(LINKS) == 64
MASK = []
for p in PLAQ:
    m = 0
    ids = [LID[l] for l, _ in WORD[p]]
    assert len(set(ids)) == 4  # four distinct links on side 2
    for i in ids:
        m |= 1 << i
    MASK.append(m)
assert len(set(MASK)) == 96
BYMASK = {m: i for i, m in enumerate(MASK)}

# ---- A. Which multisets have every link covered an even number of times (a necessary condition for a nonzero integral, by U_l -> -U_l on an oddly covered link).
even2 = [(i, i) for i in range(96)]
even3 = []
for i, j in itertools.combinations_with_replacement(range(96), 2):
    want = MASK[i] ^ MASK[j]
    k = BYMASK.get(want)
    if k is not None and k >= j:
        even3.append((i, j, k))
even4 = []
for i, j, k in itertools.combinations_with_replacement(range(96), 3):
    want = MASK[i] ^ MASK[j] ^ MASK[k]
    if want == 0:
        continue  # a single further plaquette has a nonzero mask
    l = BYMASK.get(want)
    if l is not None and l >= k:
        even4.append((i, j, k, l))
# p,p,q,q and p,p,p,p have want == mask of the odd one, so they are caught above when i==j etc.
kinds = {}
for c in even4:
    key = "+".join(map(str, sorted(c.count(i) for i in sorted(set(c)))))
    kinds[key] = kinds.get(key, 0) + 1
print("EVEN_COVER|order2=%d|order3=%d|order4=%d|kinds=%s|json=0" % (len(even2), len(even3), len(even4), ";".join("%s=%d" % kv for kv in sorted(kinds.items()))))

# ---- B. The script's filter, by a separate full scan: no link covered exactly once.
scan = {2: 0, 3: 0, 4: 0}
scan_kinds = {}
for order in (2, 3, 4):
    for c in itertools.combinations_with_replacement(range(96), order):
        once, more = 0, 0
        for i in c:
            more |= once & MASK[i]
            once |= MASK[i]
        if once & ~more:
            continue
        scan[order] += 1
        if order == 4:
            key = "+".join(map(str, sorted(c.count(i) for i in sorted(set(c)))))
            scan_kinds[key] = scan_kinds.get(key, 0) + 1
print("NOT_SINGLY_COVERED|order2=%d|order3=%d|order4=%d|kinds4=%s|json=0" % (scan[2], scan[3], scan[4], ";".join("%s=%d" % kv for kv in sorted(scan_kinds.items()))))

# ---- C. Polynomial Haar value of each even multiset, memoised on the renamed integrand only.
MEMO = {}


def pattern(combo):
    ren = {}
    out = []
    for i in combo:
        w = []
        for l, s in WORD[PLAQ[i]]:
            if l not in ren:
                ren[l] = len(ren)
            w.append((ren[l], s))
        out.append(tuple(w))
    return tuple(out)


def value(combo):
    key = pattern(combo)
    v = MEMO.get(key)
    if v is None:
        v = expect_words([list(w) for w in key])
        MEMO[key] = v
    return v


def multinom(combo):
    n = math.factorial(len(combo))
    for i in set(combo):
        n //= math.factorial(combo.count(i))
    return n


def total(multisets):
    t = (0, 1)
    parts = {}
    for c in multisets:
        v = value(c)
        key = "+".join(map(str, sorted(c.count(i) for i in sorted(set(c)))))
        term = qmul((multinom(c), 1), v)
        t = qadd(t, term)
        parts[key] = qadd(parts.get(key, (0, 1)), term)
    return t, parts


m2, p2 = total(even2)
print("E_X2=%d/%d|parts=%s|patterns=%d" % (m2[0], m2[1], p2, len(MEMO)))
m3, p3 = total(even3)
print("E_X3=%d/%d|parts=%s" % (m3[0], m3[1], p3))
m4, p4 = total(even4)
print("E_X4=%d/%d|parts=%s|patterns=%d" % (m4[0], m4[1], p4, len(MEMO)))
k4 = qadd(m4, qmul((-3, 1), qmul(m2, m2)))
print("KAPPA4=%d/%d|json=0" % k4)

# Every value by kind, so a mixed-value kind would show up.
vals = {}
for c in even4:
    key = "+".join(map(str, sorted(c.count(i) for i in sorted(set(c)))))
    vals.setdefault(key, {})
    v = value(c)
    vals[key][v] = vals[key].get(v, 0) + 1
print("VALUES_BY_KIND|%s|json=0" % ";".join("%s:%s" % (k, ",".join("%d/%d x%d" % (a[0], a[1], b) for a, b in sorted(v.items()))) for k, v in sorted(vals.items())))
# Which sets are the 1+1+1+1 ones.
tori = [c for c in even4 if len(set(c)) == 4]
geom = {}
for c in tori:
    planes = {PLAQ[i][1:] for i in c}
    transverse = set()
    for i in c:
        x, mu, nu = PLAQ[i]
        transverse.add(tuple(x[d] for d in range(D) if d not in (mu, nu)))
    k = (len(planes), len(transverse))
    geom[k] = geom.get(k, 0) + 1
print("FOUR_FACE_SETS|count=%d|by(planes,transverse_positions)=%s|expected_count=6*2^2=%d|json=0" % (len(tori), geom, 6 * 4))
# Odd-cover integrals that the filter keeps at order 3 really vanish, by polynomial integration.
print("P3_VALUE=%s|json=0" % (value((0, 0, 0)),))

# ---- D. Does each symmetry the script uses preserve the integrand? Direct test on 2T link assignments: a_{image p}(U') = a_p(U), where U'(image l) = U(l).
R, E = build("2T")
mult, inv, idx = table(R, E)
trace = [e[0] for e in E]


def trace_of(word, assign):
    h = idx[((2, 0), (0, 0), (0, 0), (0, 0))]
    for l, s in word:
        g = assign[l]
        h = mult[h][g if s > 0 else inv[g]]
    return trace[h]


# integer-only deterministic generator
state = 1234567891011
def nxt(n):
    global state
    state = (state * 6364136223846793005 + 1442695040888963407) % (1 << 64)
    return (state >> 20) % n


bad_pointwise, checked, swapped = 0, 0, 0
for perm in itertools.permutations(range(D)):
    for tr in itertools.product(range(SIDE), repeat=D):
        def lmap(l):
            x, mu = l
            y = [0] * D
            for i in range(D):
                y[perm[i]] = (x[i] + tr[perm[i]]) % SIDE
            return (tuple(y), perm[mu])
        assert len({lmap(l) for l in LINKS}) == 64
        for _ in range(2):
            U = {l: nxt(24) for l in LINKS}
            Up = {lmap(l): U[l] for l in LINKS}
            for p in PLAQ:
                x, mu, nu = p
                y = [0] * D
                for i in range(D):
                    y[perm[i]] = (x[i] + tr[perm[i]]) % SIDE
                m, n = sorted((perm[mu], perm[nu]))
                image = (tuple(y), m, n)
                checked += 1
                if perm[mu] > perm[nu]:
                    swapped += 1
                if trace_of(WORD[p], U) != trace_of(WORD[image], Up):
                    bad_pointwise += 1
print("SYMMETRY_POINTWISE|symmetries=%d|plaquette_checks=%d|orientation_swapped_checks=%d|mismatches=%d|json=0" % (24 * 16, checked, swapped, bad_pointwise))
print("MOMENTS_Z2_DONE|json=0")
