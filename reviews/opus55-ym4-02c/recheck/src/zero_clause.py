#!/usr/bin/env python3
"""Recheck of YM4-02c at c32087a. The clause of Theorem 2, 'at which W_plus(C, .) is not almost everywhere zero', has no control in the test. A plaquette-dependent weight on (Z/1)x(Z/1)x(Z/2), Q8, gives it one.
And the literal 512-function Gram at T=4 for the weights that decide the second seat's CONJECTURE. Standard library, integers only, json=0."""
import itertools
import sys
sys.path.insert(0, "C:/tmp/opus55/attack-4d-02c-20261103/src")
from exact import FiniteGroup, q8_table
G = FiniteGroup("Q8")
CHI = q8_table(G)
MUL, INV, CLS = G.mul, G.inv, G.cls
ELEMENTS = range(8)
ONE = next(g for g in ELEMENTS if all(MUL[g][h] == h for h in ELEMENTS))
MINUS = next(g for g in ELEMENTS if g != ONE and MUL[g][g] == ONE)
CP, CM = CLS[ONE], CLS[MINUS]


def bareiss_inertia(rows):
    m = [list(r) for r in rows]
    n = len(m)
    prev, pos, neg = 1, 0, 0
    for k in range(n):
        piv = next((i for i in range(k, n) if m[i][i]), None)
        if piv is None:
            pair = next(((i, j) for i in range(k, n) for j in range(i + 1, n) if m[i][j]), None)
            if pair is None:
                return pos, neg, k
            i, j = pair
            for r in range(k, n):
                m[i][r] += m[j][r]
            for r in range(k, n):
                m[r][i] += m[r][j]
            piv = i
        m[k], m[piv] = m[piv], m[k]
        for row in m:
            row[k], row[piv] = row[piv], row[k]
        top = m[k][k]
        if (top > 0) == (prev > 0):
            pos += 1
        else:
            neg += 1
        rk = m[k]
        for i in range(k + 1, n):
            ri, mik = m[i], m[i][k]
            for j in range(i, n):
                v, rest = divmod(ri[j] * top - mik * rk[j], prev)
                assert rest == 0
                ri[j] = v
                m[j][i] = v
        prev = top
    return pos, neg, n


def word(*letters):
    h = ONE
    for x in letters:
        h = MUL[h][x]
    return h


def control(w_fixed, w_time, label):
    # C = (a0, b0, a1, b1). Fixed plaquettes: a b a^-1 b^-1 at t = 0 and t = 1. Time-like upper at t = 0: a0 v a1^-1 v^-1 and b0 v b1^-1 v^-1. Lower at t = 1 with V(1) = u: a1 u a0^-1 u^-1 and b1 u b0^-1 u^-1.
    neg_f, neg_f_live, zero_ct, bad_blocks, total = 0, 0, 0, 0, 0
    lowest = None
    for a0, b0, a1, b1 in itertools.product(ELEMENTS, repeat=4):
        total += 1
        f = w_fixed[CLS[word(a0, b0, INV[a0], INV[b0])]] * w_fixed[CLS[word(a1, b1, INV[a1], INV[b1])]]
        up = [w_time[CLS[word(a0, v, INV[a1], INV[v])]] * w_time[CLS[word(b0, v, INV[b1], INV[v])]] for v in ELEMENTS]
        # F(theta U) reads V(1)^-1 = v2, so V(1) = v2^-1 in the lower plaquettes.
        down = [w_time[CLS[word(a1, INV[v2], INV[a0], v2)]] * w_time[CLS[word(b1, INV[v2], INV[b0], v2)]] for v2 in ELEMENTS]
        block = [[f * d * u for u in up] for d in down]
        p, n, _ = bareiss_inertia(block)
        live = any(up)
        if f < 0:
            neg_f += 1
            neg_f_live += 1 if live else 0
        if not live:
            zero_ct += 1
        if n > 0:
            bad_blocks += 1
        value = f * sum(up) * sum(down)
        lowest = value if lowest is None or value < lowest else lowest
    print("W_PLUS_ZERO_CONTROL|label=%s|lattice=(Z/1)x(Z/1)x(Z/2)|group=Q8|C=%d|C_with_f<0=%d|C_with_f<0_and_W_plus_not_identically_zero=%d|C_with_W_plus_identically_zero=%d|Gram_blocks_with_a_negative_eigenvalue=%d|lowest_N(delta_C)_over_8^6=%d|json=0" % (label, total, neg_f, neg_f_live, zero_ct, bad_blocks, lowest))


w_fixed = [0] * 5
w_fixed[CP], w_fixed[CM] = 1, -1
w_time_support = [0] * 5
w_time_support[CP], w_time_support[CM] = 1, 1
control(w_fixed, [1] * 5, "fixed_+1,-1_time_like_1_red")
control(w_fixed, w_time_support, "fixed_+1,-1_time_like_supported_on_+-1")

REP = [next(g for g in ELEMENTS if CLS[g] == k) for k in range(5)]


def t4_literal(c):
    w = [sum(c[r] * CHI[r][k] for r in range(5)) for k in range(5)]

    def plaquette(lower, upper, v):
        return w[CLS[word(lower, v, INV[upper], INV[v])]]
    strip = [[sum(plaquette(a, b, v) for v in ELEMENTS) for b in ELEMENTS] for a in ELEMENTS]
    triples = list(itertools.product(ELEMENTS, repeat=3))
    rows = [[plaquette(a, b, v) * strip[b][b2] * plaquette(b2, a2, INV[v2]) * strip[a2][a] for (a, b, v) in triples] for (a2, b2, v2) in triples]
    p, n, rk = bareiss_inertia(rows)
    print("T4_OPEN_HALF_LITERAL|lattice=(Z/1)x(Z/4)|group=Q8|c=%s|w=%s|family=all_512_point_functions|pos=%d|neg=%d|rank=%d|json=0" % (",".join(map(str, c)), ",".join(map(str, w)), p, n, rk))


for c in ((8, 3, 3, 3, 1), (-8, -3, -3, -3, -1), (-8, -3, -3, -3, 1), (8, -3, 3, 3, 1), (1, -2, -2, -2, -1), (-8, 3, -3, -3, -1)):
    t4_literal(c)
