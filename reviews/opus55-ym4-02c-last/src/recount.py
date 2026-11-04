#!/usr/bin/env python3
"""Independent recounts of the new rows, with no import from the test. Integers only, json=0."""
import itertools, sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *
Q = Group(q8())
M, I, CL = Q.mul, Q.inv, Q.cls
assert Q.sizes == [1, 1, 2, 2, 2]
plus, minus = 0, 1
chi = [[1,1,1,1,1],[1,1,1,-1,-1],[1,1,-1,1,-1],[1,1,-1,-1,1],[2,-2,0,0,0]]
size = [1,1,2,2,2]
dim = [1,1,1,1,2]
def c8(w): return [sum(size[k]*w[k]*chi[r][k] for k in range(5)) for r in range(5)]
# SLICE_PAIRS, from the word of section 1 on (Z/2)x(Z/1): U_1(x) U_2(x+1) U_1(x)^-1 U_2(x)^-1.
inv_pairs = same = sign = equal = 0
for a0, a1, b0, b1 in itertools.product(range(8), repeat=4):
    p0 = M[M[M[a0][b1]][I[a0]]][I[b0]]
    p1 = M[M[M[a1][b0]][I[a1]]][I[b1]]
    inv_pairs += p1 == I[p0]
    equal += p1 == p0
    same += CL[p1] in (CL[p0], CL[M[minus][p0]])
    sign += {p0, p1} == {plus, minus}
print("SLICE_PAIRS_RECOUNT|configurations=4096|second_is_inverse=%d|second_is_equal=%d|same_class_up_to_center=%d|pair_+1,-1=%d|json=0" % (inv_pairs, equal, same, sign))
# W_PLUS, from the words: f and W_plus on (Z/1)x(Z/1)x(Z/2).
for tw in ([1,1,1,1,1], [1,1,0,0,0]):
    fw = [1,-1,0,0,0]
    negf = live = dead = neg_blocks = 0
    lowest = None
    for a0, b0, a1, b1 in itertools.product(range(8), repeat=4):
        s0 = M[M[M[a0][b0]][I[a0]]][I[b0]]
        s1 = M[M[M[a1][b1]][I[a1]]][I[b1]]
        f = fw[CL[s0]] * fw[CL[s1]]
        ups = []
        for v in range(8):
            u = tw[CL[M[M[M[a0][v]][I[a1]]][I[v]]]] * tw[CL[M[M[M[b0][v]][I[b1]]][I[v]]]]
            ups.append(u)
        downs = []
        for v in range(8):
            # Lower plaquettes with the mirror: V(1) = v^-1, between t=1 and t=2=0: U_i(1) V(1) U_i(0)^-1 V(1)^-1.
            v1 = I[v]
            d = tw[CL[M[M[M[a1][v1]][I[a0]]][I[v1]]]] * tw[CL[M[M[M[b1][v1]][I[b0]]][I[v1]]]]
            downs.append(d)
        assert ups == downs
        any_live = any(ups)
        negf += f < 0
        live += f < 0 and any_live
        dead += not any_live
        rows = [[f * d * u for u in ups] for d in downs]
        p, q, r = bareiss_inertia(rows)
        neg_blocks += q > 0
        n = f * sum(ups) * sum(downs)
        lowest = n if lowest is None or n < lowest else lowest
    print("W_PLUS_RECOUNT|time_weight=%s|C_with_f<0=%d|and_W_plus_live=%d|C_with_W_plus_dead=%d|negative_blocks=%d|lowest=%d|json=0" % (",".join(map(str, tw)), negf, live, dead, neg_blocks, lowest))
# Scan, from t_rho directly, with Python ints scaled by 16^L.
cases = neg = weights = 0
for w in itertools.product(range(7), repeat=5):
    c = c8(w)
    if c[4] >= 0:
        continue
    weights += 1
    for L in (1, 3, 5):
        cases += 1
        sum_t = sum(c[a] ** L for a in range(4))
        # G_EE = 2 (c4/16)^L (sum_t / 8^L), so its sign is that of c4^L sum_t.
        neg += (c[4] ** L) * sum_t < 0
print("SCAN_RECOUNT|weights=%d|cases=%d|G_EE_negative=%d|json=0" % (weights, cases, neg))
# Signed scan, w in -6..6, c_0>0, c_2dim<0, L=3.
cases = pos = 0
for w in itertools.product(range(-6, 7), repeat=5):
    c = c8(w)
    if c[0] <= 0 or c[4] >= 0:
        continue
    cases += 1
    sum_t = sum(c[a] ** 3 for a in range(4))
    pos += (c[4] ** 3) * sum_t > 0
print("SCAN_SIGNED_RECOUNT|cases=%d|G_EE_positive=%d|json=0" % (cases, pos))
# Five-character Gram at L=3 from t_rho and the tensor table, scaled to integers. For c=1,-2,-2,-2,-1 and the two earlier weights.
tab = {}
for r in range(5):
    for s in range(5):
        tab[(r, s)] = [sum(size[k]*chi[r][k]*chi[s][k]*chi[m][k] for k in range(5)) // 8 for m in range(5)]
for c in ((8,-1,3,3,2),(8,-1,2,2,1),(1,-2,-2,-2,-1),(-8,-3,-3,-3,-1),(8,3,3,3,-1)):
    # t_rho = (c_rho/d_rho)^3, scale by 8.
    t = [c[r] ** 3 * (8 // dim[r] ** 3) for r in range(5)]
    G = [[sum(t[r] * t[s] * tab[(r, s)][a] * tab[(r, s)][b] for r in range(5) for s in range(5)) for b in range(5)] for a in range(5)]
    p, q, r = bareiss_inertia(G)
    print("CHAR_GRAM_L3|c=%s|positive=%d|negative=%d|rank=%d|G_EE_over_64=%d|G_s1s1_over_64=%d|json=0" % (",".join(map(str, c)), p, q, r, G[4][4], G[1][1]))
# The grid, recounted.
COUNT = [[[0]*5 for _ in range(5)] for _ in range(5)]
for x in range(5):
    for y in range(5):
        for v in range(8):
            COUNT[x][y][CL[M[M[M[Q.reps[x]][v]][I[Q.reps[y]]]][I[v]]]] += 1
cats = {}
for w in itertools.product(range(-3, 4), repeat=5):
    if not any(w):
        continue
    c = c8(w)
    K = [[sum(COUNT[x][y][k]*w[k] for k in range(5)) for y in range(5)] for x in range(5)]
    S = [(x,y) for x in range(5) for y in range(5) if any(COUNT[x][y][k] and w[k] for k in range(5))]
    rows = [[K[p][p2]*K[q][q2] for (p2,q2) in S] for (p,q) in S]
    pp, qq, rr = bareiss_inertia(rows)
    key = ("c0=0" if c[0] == 0 else "c0!=0", "zero" if 0 in w else "nowhere_zero", "opposite" if any(x*c[0] < 0 for x in c) else "none", "PSD" if qq == 0 else "RED")
    cats[key] = cats.get(key, 0) + 1
for key in sorted(cats):
    print("GRID_RECOUNT|%s|count=%d|json=0" % ("|".join(key), cats[key]))
