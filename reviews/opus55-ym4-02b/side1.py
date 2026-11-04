# Claim 2 attack: the corollary says "on any finite lattice". On a periodic lattice with a side of length 1 a plaquette holds the same link twice,
# so a_p has degree 2 in that link. Exact sums over explicit groups; 2T is exact for per-link degree <= 5, 2O for <= 7, 2I for <= 11, all three confirmed by designs_explicit.py.
import math
import sys

sys.path.insert(0, "C:/tmp/opus55/attack-4d-20261103/ym4-02b")
from grp import O, build, table


def red(n, d):
    g = math.gcd(n, d) or 1
    if d < 0:
        n, d = -n, -d
    return n // g, d // g


def setup(name):
    R, E = build(name)
    mult, inv, idx = table(R, E)
    n = len(E)
    # doubled real part of [g,h] = g h g^-1 h^-1, this is Tr of the commutator. In all four groups the commutator lies in a subgroup whose traces we keep as ring pairs.
    comm = [[E[mult[mult[mult[g][h]][inv[g]]][inv[h]]][0] for h in range(n)] for g in range(n)]
    return R, E, n, comm


# --- d=2, side 1: one plaquette, a = (1/2) Tr [U,V]. E_G[a^k].
print("D2_L1|plaquette_word=U V U^-1 V^-1|degree_in_each_link=2|json=0")
for name in ("Q8", "2T", "2O", "2I"):
    R, E, n, comm = setup(name)
    row = []
    for k in range(1, 7):
        tot = (0, 0)
        for g in range(n):
            for h in range(n):
                v = (1, 0)
                for _ in range(k):
                    v = R(v, comm[g][h])
                tot = (tot[0] + v[0], tot[1] + v[1])
        assert tot[1] == 0
        row.append("E_a^%d=%d/%d" % ((k,) + red(tot[0], n * n * 2 ** k)))
    print("D2_L1|group=%s|%s|json=0" % (name, "|".join(row)))
# closed form with no group: chi^k = sum over spins of (Clebsch-Gordan multiplicity) chi_j, and E[chi_j([U,V])] = 1/d_j.
mult = {1: 1}  # dimension d -> multiplicity in (C^2)^{tensor k}
row = []
for k in range(1, 7):
    nxt = {}
    for d, m in mult.items():
        nxt[d + 1] = nxt.get(d + 1, 0) + m
        if d > 1:
            nxt[d - 1] = nxt.get(d - 1, 0) + m
    mult = nxt
    num, den = 0, 1
    for d, m in mult.items():
        num = num * d + m * den
        den = den * d
    row.append("E_a^%d=%d/%d" % ((k,) + red(num, den * 2 ** k)))
print("D2_L1|method=closed_form_characters|%s|json=0" % "|".join(row))

# --- d=4, side 1: four links, six commutator plaquettes, X = sum a_mu_nu. E_G[X^k] for k <= 3.
for name in ("Q8", "2T", "2O"):
    R, E, n, comm = setup(name)
    # every commutator trace is an ordinary integer here: Q8, 2T commutators lie in Q8; 2O commutators lie in 2T.
    tr = [[comm[g][h][0] for h in range(n)] for g in range(n)]
    assert all(comm[g][h][1] == 0 for g in range(n) for h in range(n))
    s = [0, 0, 0, 0]
    for a in range(n):
        ta = tr[a]
        for b in range(n):
            ab = ta[b]
            tb = tr[b]
            for c in range(n):
                abc = ab + ta[c] + tb[c]
                tc = tr[c]
                for d in range(n):
                    x = abc + ta[d] + tb[d] + tc[d]  # this is 2X
                    s[0] += 1
                    s[1] += x
                    s[2] += x * x
                    s[3] += x * x * x
    row = ["E_X^%d=%d/%d" % ((k,) + red(s[k], s[0] * 2 ** k)) for k in (1, 2, 3)]
    print("D4_L1|group=%s|%s|json=0" % (name, "|".join(row)))
print("SIDE1_DONE|json=0")
