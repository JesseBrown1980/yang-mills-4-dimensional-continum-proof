#!/usr/bin/env python3
"""Second seat: from the literal 8^12 histogram (no gauge fixing) on (Z/3)x(Z/2), the link and site Gram matrices, against character gluing, with the PSD test by characteristic polynomial and Descartes' rule.
Key digits, base 5: class W0, class W1, p(0,0), p(1,0), p(2,0), p(0,1), p(1,1), p(2,1). Standard library, integers only, json=0."""
import collections
import itertools
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("\\", 1)[0])
from exact import FiniteGroup, q8_table, q8_weight, charpoly, inertia_from_charpoly, rank_mod, signature_by_rational_ldl, rat, radd, rmul, rtext

G = FiniteGroup("Q8")
CHI = q8_table(G)
DIM = [1, 1, 1, 1, 2]
SIZE = [1, 1, 2, 2, 2]


def load(path):
    hist = {}
    total = 0
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
                total += count
    return hist, total


def char_triple(a, b, c):
    """E[chi_a chi_b chi_c] over Q8, an integer."""
    s = sum(SIZE[k] * CHI[a][k] * CHI[b][k] * CHI[c][k] for k in range(5))
    q, r = divmod(s, 8)
    assert r == 0
    return q


def gluing_gram(c, L):
    """G_ab = sum_(rho, tau) t_rho t_tau E[chi_a chi_rho chi_tau] E[chi_b chi_rho chi_tau], t = (c/d)^L, as reduced pairs."""
    t = [rat(c[r] ** L, DIM[r] ** L) for r in range(5)]
    out = []
    for a in range(5):
        row = []
        for b in range(5):
            s = (0, 1)
            for r in range(5):
                for u in range(5):
                    s = radd(s, rmul(rmul(t[r], t[u]), (char_triple(a, r, u) * char_triple(b, r, u), 1)))
            row.append(s)
        out.append(row)
    return out


def main():
    path = sys.argv[1]
    hist, total = load(path)
    print("HIST_READ|keys=%d|total=%d|is_8^12=%d|json=0" % (len(hist), total, 1 if total == 8 ** 12 else 0))
    den = 8 ** 12
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1)):
        w = q8_weight(CHI, c)
        z = 0
        red = collections.defaultdict(int)
        for key, n in hist.items():
            term = n
            for k in key[2:]:
                term *= w[k]
            z += term
            red[(key[0], key[1])] += term
        link = [[sum(v * CHI[a][k1] * CHI[b][k0] for (k0, k1), v in red.items()) for b in range(5)] for a in range(5)]
        glue = gluing_gram(c, 3)
        agree = all(rat(link[a][b], den) == glue[a][b] for a in range(5) for b in range(5))
        symmetric = all(link[a][b] == link[b][a] for a in range(5) for b in range(5))
        poly = charpoly(link)
        pos, neg, zero = inertia_from_charpoly(poly)
        ldl = signature_by_rational_ldl(link)
        print("LINK_GRAM|c=%s|w=%s|Z=%s|G_FF=%s|agrees_with_gluing=%d|symmetric=%d|charpoly_inertia_pos=%d|neg=%d|zero=%d|ldl_pos=%d|ldl_neg=%d|rank_mod_p=%d|json=0" % (
            ",".join(map(str, c)), ",".join(map(str, w)), rtext(rat(z, den)), rtext(rat(link[4][4], den)), 1 if agree else 0, 1 if symmetric else 0, pos, neg, zero, ldl[0], ldl[1], rank_mod(link, 2305843009213693951)), flush=True)
        print("LINK_GRAM_MATRIX|c=%s|rows=%s|json=0" % (",".join(map(str, c)), ";".join(",".join(rtext(glue[a][b]) for b in range(5)) for a in range(5))))
    # Site reflection: F on the closed half; class point functions of (p(0,0), p(1,0), p(2,0)), mirror reads (p(0,1), p(1,1), p(2,1)); both Wilson lines are fixed.
    for name, w in (("c=8,3,3,3,1", q8_weight(CHI, (8, 3, 3, 3, 1))), ("c=8,3,3,3,-1", q8_weight(CHI, (8, 3, 3, 3, -1))), ("values=3,-2,1,-1,2", [3, -2, 1, -1, 2]), ("values=-1,-1,2,-3,1", [-1, -1, 2, -3, 1])):
        idx = {t: i for i, t in enumerate(itertools.product(range(5), repeat=3))}
        n = len(idx)
        mat = [[0] * n for _ in range(n)]
        for key, cnt in hist.items():
            term = cnt
            for k in key[2:]:
                term *= w[k]
            mat[idx[key[5:8]]][idx[key[2:5]]] += term
        symmetric = all(mat[i][j] == mat[j][i] for i in range(n) for j in range(i))
        pos, neg, ok = signature_by_rational_ldl(mat)
        print("SITE_GRAM_125|weight=%s|symmetric=%d|ldl_pos=%d|ldl_neg=%d|zero_tail_ok=%d|rank_mod_p=%d|json=0" % (name, 1 if symmetric else 0, pos, neg, 1 if ok else 0, rank_mod(mat, 2305843009213693951)), flush=True)
        # The same with W0 and W1 joined to the function: point functions of (W0, W1, p(0,0)), mirror (W0, W1, p(0,1)).
        idx2 = {t: i for i, t in enumerate(itertools.product(range(5), repeat=3))}
        mat2 = [[0] * 125 for _ in range(125)]
        for key, cnt in hist.items():
            term = cnt
            for k in key[2:]:
                term *= w[k]
            mat2[idx2[(key[0], key[1], key[5])]][idx2[(key[0], key[1], key[2])]] += term
        symmetric = all(mat2[i][j] == mat2[j][i] for i in range(125) for j in range(i))
        pos, neg, ok = signature_by_rational_ldl(mat2)
        print("SITE_GRAM_W0W1P|weight=%s|symmetric=%d|ldl_pos=%d|ldl_neg=%d|zero_tail_ok=%d|json=0" % (name, 1 if symmetric else 0, pos, neg, 1 if ok else 0), flush=True)


main()
