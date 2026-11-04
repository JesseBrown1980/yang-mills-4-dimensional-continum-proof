#!/usr/bin/env python3
"""Second seat: extra exact controls. Standard library, integers only, json=0.
1. T = 2, L odd, a negative coefficient: is the Gram always red? From the literal 8^12 histogram and from gluing.
2. T = 2 and T = 4, every point function, (Z/1), same weights.
3. 2T: the hypothesis w(g^-1) = w(g), and Theorem 4 on a group with complex characters."""
import itertools
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("\\", 1)[0])
from exact import FiniteGroup, q8_table, q8_weight, rat, rtext, charpoly, inertia_from_charpoly, rank_mod

G = FiniteGroup("Q8")
TAB = q8_table(G)
MUL, INV, CLS = G.mul, G.inv, G.cls
PRIME = 2305843009213693951


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


def link_gram_L3(hist, w):
    red = {}
    for key, n in hist.items():
        term = n
        for k in key[2:]:
            term *= w[k]
        red[(key[0], key[1])] = red.get((key[0], key[1]), 0) + term
    return [[sum(v * TAB[a][k1] * TAB[b][k0] for (k0, k1), v in red.items()) for b in range(5)] for a in range(5)]


def kernel_T2_side1(w):
    # (Z/1)x(Z/2): N(delta_b, delta_a) = (sum_v w(b v a^-1 v^-1)) (sum_v' w(a v' b^-1 v'^-1)).
    n = G.n
    mat = []
    for b in range(n):
        row = []
        for a in range(n):
            p1 = sum(w[CLS[MUL[MUL[MUL[b][v]][INV[a]]][INV[v]]]] for v in range(n))
            p0 = sum(w[CLS[MUL[MUL[MUL[a][v]][INV[b]]][INV[v]]]] for v in range(n))
            row.append(p1 * p0)
        mat.append(row)
    return mat


def kernel_T4_side1(w):
    # (Z/1)x(Z/4), the 64 point functions of (U(0), U(1)).
    n = G.n
    strip = [[sum(w[CLS[MUL[MUL[MUL[a][v]][INV[b]]][INV[v]]]] for v in range(n)) for b in range(n)] for a in range(n)]
    pairs = list(itertools.product(range(n), repeat=2))
    return [[strip[a][b] * strip[b][b2] * strip[b2][a2] * strip[a2][a] for (a, b) in pairs] for (a2, b2) in pairs]


def bareiss(rows):
    m = [list(r) for r in rows]
    n = len(m)
    prev, sign_prev, pos, neg = 1, 1, 0, 0
    for k in range(n):
        piv = next((i for i in range(k, n) if m[i][i] != 0), None)
        if piv is None:
            return pos, neg, all(m[i][j] == 0 for i in range(k, n) for j in range(k, n))
        m[k], m[piv] = m[piv], m[k]
        for row in m:
            row[k], row[piv] = row[piv], row[k]
        top = m[k][k]
        s = 1 if top > 0 else -1
        if s == sign_prev:
            pos += 1
        else:
            neg += 1
        sign_prev = s
        rk = m[k]
        for i in range(k + 1, n):
            ri, mik = m[i], m[i][k]
            for j in range(k + 1, n):
                q, r = divmod(ri[j] * top - mik * rk[j], prev)
                assert r == 0
                ri[j] = q
        prev = top
    return pos, neg, True


def part1(path):
    hist = load(path)
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1), (8, -1, 3, 3, 2), (8, -1, 2, 2, 1), (8, -3, 3, 3, 1), (20, -1, 6, 6, 2)):
        w = q8_weight(TAB, c)
        mat = link_gram_L3(hist, w)
        p, n, z = inertia_from_charpoly(charpoly(mat))
        t2 = kernel_T2_side1(w)
        p1, n1, ok1 = bareiss(t2)
        t4 = kernel_T4_side1(w)
        p4, n4, ok4 = bareiss(t4)
        print("NEGATIVE_COEFFICIENT|c=%s|w=%s|(Z/3)x(Z/2)_five_characters_pos=%d|neg=%d|zero=%d|(Z/1)x(Z/2)_all_8_pos=%d|neg=%d|(Z/1)x(Z/4)_all_64_pos=%d|neg=%d|json=0" % (",".join(map(str, c)), ",".join(map(str, w)), p, n, z, p1, n1, p4, n4), flush=True)


def part3():
    T = FiniteGroup("2T")
    n = T.n
    mul, inv, cls = T.mul, T.inv, T.cls
    classes = T.classes
    inverse_class = [cls[inv[c[0]]] for c in classes]
    print("2T_CLASSES|sizes=%s|inverse_class=%s|traces=%s|json=0" % ([len(c) for c in classes], inverse_class, [T.elems[c[0]][0] for c in classes]), flush=True)
    # A real class function with w(g^-1) != w(g), positive everywhere.
    w = [9, 7, 5, 8, 2, 3, 6]
    print("2T_WEIGHT|w=%s|inverse_symmetric=%d|json=0" % (w, 1 if all(w[i] == w[inverse_class[i]] for i in range(7)) else 0), flush=True)
    # Site reflection on (Z/1)x(Z/2): F on the closed half, F(theta U) reads V^-1 of the lower link.
    worst, broken = None, 0
    for a in range(n):
        for b in range(n):
            f = [w[cls[mul[mul[mul[a][v]][inv[b]]][inv[v]]]] for v in range(n)]
            h = [w[cls[mul[mul[mul[b][inv[v]]][inv[a]]][v]]] for v in range(n)]
            if f != h:
                broken += 1
                for i in range(n):
                    for j in range(i):
                        al, ga = h[j] + f[j], -(h[i] + f[i])
                        v = (al * h[i] + ga * h[j]) * (al * f[i] + ga * f[j])
                        if worst is None or v < worst:
                            worst = v
    print("2T_ASYMMETRIC_WEIGHT|lattice=(Z/1)x(Z/2)|fixed_links=%d|blocks_not_symmetric=%d|most_negative_form_value=%s|json=0" % (n * n, broken, worst), flush=True)
    # Theorem 4 on 2T, real weight with non-negative coefficients on complex characters: (Z/1)x(Z/2), all 24 point functions.
    for name, c in (("c=7,2,2,4,3,1,1", (7, 2, 2, 4, 3, 1, 1)), ("c=7,-2,-2,4,3,1,1", (7, -2, -2, 4, 3, 1, 1)), ("c=7,2,2,4,-1,1,1", (7, 2, 2, 4, -1, 1, 1))):
        tab = t2_rows(T)
        ww = []
        for k in range(7):
            s0 = sum(c[r] * tab[r][k][0] for r in range(7))
            s1 = sum(c[r] * tab[r][k][1] for r in range(7))
            assert s1 == 0
            ww.append(s0)
        mat = []
        for b in range(n):
            row = []
            for a in range(n):
                p1 = sum(ww[cls[mul[mul[mul[b][v]][inv[a]]][inv[v]]]] for v in range(n))
                p0 = sum(ww[cls[mul[mul[mul[a][v]][inv[b]]][inv[v]]]] for v in range(n))
                row.append(p1 * p0)
            mat.append(row)
        p, q, ok = bareiss(mat)
        print("2T_LINK_T2|%s|w=%s|pointwise_positive=%d|pos=%d|neg=%d|zero_tail_ok=%d|json=0" % (name, ww, 1 if min(ww) > 0 else 0, p, q, 1 if ok else 0), flush=True)


def t2_rows(G2):
    e = G2.elems.index((1, 1, 1, 1))
    e2 = G2.mul[e][e]
    q8 = {i for i, v in enumerate(G2.elems) if sorted(abs(u) for u in v) == [0, 0, 0, 2]}
    coset = []
    for g in range(G2.n):
        if g in q8:
            coset.append(0)
        elif G2.mul[G2.inv[e]][g] in q8:
            coset.append(1)
        else:
            coset.append(2)
    W = [(1, 0), (0, 1), (-1, -1)]
    rows = []
    for shape in range(7):
        row = []
        for orbit in G2.classes:
            g = orbit[0]
            tau = G2.elems[g][0]
            lam = W[coset[g]]
            lam2 = W[(2 * coset[g]) % 3]
            row.append({0: (1, 0), 1: lam, 2: lam2, 3: (tau * tau - 1, 0), 4: (tau, 0), 5: (tau * lam[0], tau * lam[1]), 6: (tau * lam2[0], tau * lam2[1])}[shape])
        rows.append(row)
    return rows


if sys.argv[1] == "neg":
    part1(sys.argv[2])
if sys.argv[1] == "2t":
    part3()
