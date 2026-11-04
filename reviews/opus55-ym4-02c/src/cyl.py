#!/usr/bin/env python3
"""Second seat: E[a_W a_thetaW prod a_side] on SU(2) itself, by index contraction with the degree-2 Haar integrals, and the closed form from character gluing.
Each link occurs exactly twice. For (U, U^-1): int U_ab (U^-1)_cd = (1/2) delta_ad delta_bc. For (U, U): int U_ab U_cd = (1/2) eps_ac eps_bd. Standard library, integers only, json=0."""
import itertools
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("\\", 1)[0])
from exact import rat, rtext

EPS = {(0, 0): 0, (1, 1): 0, (0, 1): 1, (1, 0): -1}


def expectation(words):
    """words: list of traces, each a list of (link, sign). Returns E[prod (1/2) Tr word] as a reduced pair, or (0,1) when some link has degree other than 2."""
    occ = {}
    for w_i, w in enumerate(words):
        for p_i, (l, s) in enumerate(w):
            occ.setdefault(l, []).append((w_i, p_i, s))
    for l, v in occ.items():
        if len(v) != 2:
            return None
    # One index variable per position: letter p of word w runs from index I[w][p] to index I[w][p+1].
    offset = []
    n = 0
    for w in words:
        offset.append(n)
        n += len(w)
    total = 0
    pairs = list(occ.values())
    for bits in itertools.product((0, 1), repeat=n):
        val = 1
        for (w1, p1, s1), (w2, p2, s2) in pairs:
            a = bits[offset[w1] + p1]
            b = bits[offset[w1] + (p1 + 1) % len(words[w1])]
            c = bits[offset[w2] + p2]
            d = bits[offset[w2] + (p2 + 1) % len(words[w2])]
            if s1 != s2:
                # Write the forward letter first.
                if s1 < 0:
                    a, b, c, d = c, d, a, b
                val *= 1 if (a == d and b == c) else 0
            elif s1 > 0:
                val *= EPS[(a, c)] * EPS[(b, d)]
            else:
                # (U^-1)_ab (U^-1)_cd has the same value as eps_ac eps_bd / 2, since U^-1 is Haar distributed.
                val *= EPS[(a, c)] * EPS[(b, d)]
            if val == 0:
                break
        total += val
    return rat(total, 2 ** (len(pairs) + len(words)))


def strip(L):
    """W on links A_x, its mirror W' on links B_x, and the side plaquettes in the repository's word: B_x V_(x+1) A_x^-1 V_x^-1."""
    a = lambda x: ("A", x % L)
    b = lambda x: ("B", x % L)
    v = lambda x: ("V", x % L)
    w = [(a(x), 1) for x in range(L)]
    wp = [(b(x), 1) for x in range(L)]
    sides = [[(b(x), 1), (v(x + 1), 1), (a(x), -1), (v(x), -1)] for x in range(L)]
    return [w, wp] + sides


def main():
    assert expectation([[("U", 1)], [("U", 1)]]) == (1, 4), "E[(Tr U)^2]/4 = 1/4"
    assert expectation([[("U", 1), ("V", 1), ("U", -1), ("V", -1)]]) == (1, 4), "E a on a commutator = 1/4"
    for L in (1, 2, 3):
        got = expectation(strip(L))
        want = rat(1, 4 ** (L + 1))
        print("CYLINDER_SU2_CONTRACTION|L=%d|index_variables=%d|E=%s|closed_form_4^-(L+1)=%s|equal=%d|json=0" % (L, sum(len(w) for w in strip(L)), rtext(got), rtext(want), 1 if got == want else 0), flush=True)
    # Character gluing: integrate the three V, each gives 1/2 on the spin-1/2 sector: E[chi_1(W') chi_1(W) (1/2)^L chi_1(W') chi_1(W)] (1/2)^(L+2) = (1/2)^L E[chi_1^2]^2 (1/2)^(L+2).
    for L in (1, 2, 3, 5, 7):
        print("CYLINDER_GLUING|L=%d|value=%s|json=0" % (L, rtext(rat(1, 2 ** L * 2 ** (L + 2)))))


main()
