#!/usr/bin/env python3
"""Recheck of YM4-02c at c32087a. The scoped clause a_negative_c_2dim_fails_on_odd_L_at_T=2_here, the T>=4 witness beyond w>0, and the second seat's own CONJECTURE.
Standard library, integers only, json=0. Group tables and char-poly inertia are the second seat's earlier helpers, read-only, from attack-4d-02c-20261103/src."""
import itertools, sys
sys.path.insert(0, "C:/tmp/opus55/attack-4d-02c-20261103/src")
from exact import FiniteGroup, q8_table, q8_weight, rat, radd, rmul, rtext, charpoly, inertia_from_charpoly
G = FiniteGroup("Q8")
CHI = q8_table(G)
MUL, INV, CLS = G.mul, G.inv, G.cls
DIM = [1, 1, 1, 1, 2]
SIZE = [1, 1, 2, 2, 2]
HIST = sys.argv[1]

def load(path):
    hist = {}
    with open(path, "r") as f:
        for line in f:
            if line.startswith("HIST|"):
                parts = dict(p.split("=") for p in line.strip().split("|")[1:3])
                key, count = int(parts["key"]), int(parts["count"])
                d = []
                for _ in range(8):
                    d.append(key % 5)
                    key //= 5
                hist[tuple(reversed(d))] = count
    return hist

def gram_L3(hist, w):
    red = {}
    for key, n in hist.items():
        term = n
        for k in key[2:]:
            term *= w[k]
        red[(key[0], key[1])] = red.get((key[0], key[1]), 0) + term
    return [[sum(v * CHI[a][k1] * CHI[b][k0] for (k0, k1), v in red.items()) for b in range(5)] for a in range(5)]

def strip_of(w):
    n = G.n
    return [[sum(w[CLS[MUL[MUL[MUL[a][v]][INV[b]]][INV[v]]]] for v in range(n)) for b in range(n)] for a in range(n)]

def inertia(rows):
    return inertia_from_charpoly(charpoly(rows))

hist = load(HIST)
assert sum(hist.values()) == 8 ** 12
print("ROW|lattice_L3_from_the_literal_8^12_histogram|json=0")
for c in ((8, 3, 3, 3, -1), (8, -1, 3, 3, 2), (1, -2, -2, -2, -1), (2, -2, -2, -2, -1), (1, -1, -1, -1, -1), (-8, -3, -3, -3, -1), (-8, 3, 3, 3, 1)):
    w = q8_weight(G, c) if False else None
    w = [sum(c[r] * CHI[r][k] for r in range(5)) for k in range(5)]
    g3 = gram_L3(hist, w)
    den = 8 ** 12
    t = [rat(c[r] ** 3, DIM[r] ** 3) for r in range(5)]
    s = radd(radd(t[0], t[1]), radd(t[2], t[3]))
    rule_e = rmul(rmul((2, 1), t[4]), s)
    ee = rat(g3[4][4], den)
    i3 = inertia(g3)
    st = strip_of(w)
    one = [[st[a][b] * st[b][a] for a in range(8)] for b in range(8)]
    i1 = inertia(one)
    pairs = list(itertools.product(range(8), repeat=2))
    print("NEGATIVE_C_2DIM|c=%s|w_on_+1,-1,i,j,k=%s|min_w=%d|c_0=%d|c_2dim=%d|(Z/3)x(Z/2)_five_characters_pos=%d|neg=%d|zero=%d|G_EE=%s|rule_2*t_E*(t_0+t_1+t_2+t_3)=%s|(Z/1)x(Z/2)_all_8_pos=%d|neg=%d|zero=%d|Z_over_8^12=%d|json=0" % (
        ",".join(map(str, c)), ",".join(map(str, w)), min(w), c[0], c[4], i3[0], i3[1], i3[2], rtext(ee), rtext(rule_e), i1[0], i1[1], i1[2], g3[0][0]))
