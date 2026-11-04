#!/usr/bin/env python3
"""Site reflection at T=2, one weight on every plaquette, every spatial side >= 2. w = 1,-1,0,0,0 on +1,-1,i,j,k. Slices (Z/2)x(Z/2) with every plaquette central, walked exactly. Reads the sign of the product over a slice against the V4 holonomies, and tests the condition of Theorem 2 literally on seeded pairs of slices over all 8^4 time links. Integers only, json=0."""
import itertools, random, sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *
Q = Group(q8())
assert Q.sizes == [1, 1, 2, 2, 2]
M, I, CL = Q.mul, Q.inv, Q.cls
W = [1, -1, 0, 0, 0]
# Links of the slice (Z/2)x(Z/2): u[x][y] in direction 1, v[x][y] in direction 2.
sites = list(itertools.product(range(2), repeat=2))
lk = {}
for s in sites:
    lk[(s, 0)] = len(lk)
for s in sites:
    lk[(s, 1)] = len(lk)
def sh(s, mu):
    t = list(s); t[mu] = (t[mu] + 1) % 2; return tuple(t)
plaq = [(lk[(s, 0)], lk[(sh(s, 0), 1)], lk[(sh(s, 1), 0)], lk[(s, 1)]) for s in sites]
def word(c, p):
    a, b, d, e = p
    return M[M[M[c[a]][c[b]]][I[c[d]]]][I[c[e]]]
coset = [0, 0, 1, 1, 2, 2, 3, 3]
# Walk: cosets first. All plaquettes central means the V4 connection is flat. Enumerate V4 connections, keep the flat, then all center lifts.
vmul = [[coset[M[2 * a][2 * b]] for b in range(4)] for a in range(4)]
flat = []
for cc in itertools.product(range(4), repeat=8):
    ok = True
    for (a, b, d, e) in plaq:
        if vmul[vmul[vmul[cc[a]][cc[b]]][cc[d]]][cc[e]] != 0:
            ok = False
            break
    if ok:
        flat.append(cc)
slices = []
signs = {}
for cc in flat:
    h1 = vmul[cc[lk[((0, 0), 0)]]][cc[lk[((1, 0), 0)]]]
    h2 = vmul[cc[lk[((0, 0), 1)]]][cc[lk[((0, 1), 1)]]]
    for lift in itertools.product(range(2), repeat=8):
        c = tuple(2 * cc[i] + lift[i] for i in range(8))
        z = 1
        for p in plaq:
            z *= W[CL[word(c, p)]]
        signs.setdefault((h1, h2), {}).setdefault(z, 0)
        signs[(h1, h2)][z] += 1
        slices.append((c, h1, h2, z))
print("SITE_CENTER_SLICES|slice=(Z/2)x(Z/2)|group=Q8|w=1,-1,0,0,0|flat_V4_connections=%d|slices_with_every_plaquette_central=%d|json=0" % (len(flat), len(slices)))
plus = sum(1 for s in slices if s[3] > 0)
minus = len(slices) - plus
print("SITE_CENTER_SIGN|slices_with_product_+1=%d|slices_with_product_-1=%d|product_is_a_function_of_the_V4_holonomies=%d|json=0" % (plus, minus, 1 if all(len(v) == 1 for v in signs.values()) else 0))
for key in sorted(signs):
    print("SITE_CENTER_HOLONOMY|h1,h2=%d,%d|%s|json=0" % (key[0], key[1], "|".join("product_%+d=%d" % (z, n) for z, n in sorted(signs[key].items()))))
# Literal: seeded pairs of slices; does some V on the four time links keep every time-like plaquette nonzero? 8^4 V.
rnd = random.Random(20261104)
def reaches(c0, c1):
    for V in itertools.product(range(8), repeat=4):
        vd = dict(zip(sites, V))
        ok = True
        for s in sites:
            for mu in (0, 1):
                p1, p2, p3, p4 = c0[lk[(s, mu)]], vd[sh(s, mu)], I[c1[lk[(s, mu)]]], I[vd[s]]
                g = M[M[M[p1][p2]][p3]][p4]
                if W[CL[g]] == 0:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return True
    return False
negf_reach = negf_noreach = posf_reach = posf_noreach = 0
holonomy_agree = 0
for _ in range(600):
    a = rnd.choice(slices)
    b = rnd.choice(slices)
    # Half the draws force the same holonomies, so both outcomes are sampled.
    if _ % 2:
        same = [s for s in rnd.sample(slices, 4000) if (s[1], s[2]) == (a[1], a[2])]
        if same:
            b = rnd.choice(same)
    f = a[3] * b[3]
    r = reaches(a[0], b[0])
    holonomy_agree += 1 if r == ((a[1], a[2]) == (b[1], b[2])) else 0
    if f < 0:
        if r: negf_reach += 1
        else: negf_noreach += 1
    else:
        if r: posf_reach += 1
        else: posf_noreach += 1
print("SITE_CENTER_PAIRS|seeded_pairs=600|f<0_with_W_plus_not_identically_zero=%d|f<0_with_W_plus_identically_zero=%d|f>0_with_W_plus_not_identically_zero=%d|f>0_with_W_plus_identically_zero=%d|reach_equals_same_V4_holonomies=%d|json=0" % (negf_reach, negf_noreach, posf_reach, posf_noreach, holonomy_agree))
