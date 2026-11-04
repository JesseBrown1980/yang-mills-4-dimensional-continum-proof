#!/usr/bin/env python3
"""Second seat: part G, the T = 4 entry, Tr(AB) and Collatz-Wielandt from separate code. Standard library, integers only, json=0."""
import itertools
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("\\", 1)[0])
from exact import FiniteGroup, q8_table, q8_weight, rat, rtext

G = FiniteGroup("Q8")
TAB = q8_table(G)
MUL, INV, CLS = G.mul, G.inv, G.cls
PLUS, MINUS = 0, 1  # class indices of +1 and -1


def comm(a, b):
    return CLS[MUL[MUL[MUL[a][b]][INV[a]]][INV[b]]]


def part_g():
    pairs = list(itertools.product(range(8), repeat=2))
    tally = [0, 0]
    for a, b in pairs:
        k = comm(a, b)
        assert k in (PLUS, MINUS)
        tally[k] += 1
    print("COMMUTATOR_SEPARATE|plus=%d|minus=%d|json=0" % (tally[0], tally[1]))
    for wp, wm in ((1, -1), (3, 1)):
        w = {PLUS: wp, MINUS: wm}
        num, z = 0, 0
        for a0, b0 in pairs:
            for a1, b1 in pairs:
                s0, s1 = comm(a0, b0), comm(a1, b1)
                term = w[s0] * w[s1]
                z += term
                if s0 == MINUS and s1 == PLUS:
                    num += term
        # Time-like weight 1: the two time links integrate to 1.
        print("SIGNED_SITE_SEPARATE|w(+1)=%d|w(-1)=%d|numerator=%s|Z=%s|json=0" % (wp, wm, rtext(rat(num, 8 ** 4)), rtext(rat(z, 8 ** 4))))


def part_t4():
    e = TAB[4]
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1)):
        w = q8_weight(TAB, c)
        strip = [[sum(w[CLS[MUL[MUL[MUL[a][v]][INV[b]]][INV[v]]]] for v in range(8)) for b in range(8)] for a in range(8)]
        # U(0), U(1), U(2), U(3) over 8^4, V's integrated by the strips, then divide by 8^8.
        total = 0
        for u0, u1, u2, u3 in itertools.product(range(8), repeat=4):
            total += strip[u0][u1] * strip[u1][u2] * strip[u2][u3] * strip[u3][u0] * e[CLS[u0]] * e[CLS[u3]]
        print("GRAM_T4_SEPARATE|c=%s|G_FF=%s|json=0" % (",".join(map(str, c)), rtext(rat(total, 8 ** 8))))


def part_cw():
    # Spatial (Z/2)x(Z/1): links U0(0), U0(1), U1(0), U1(1); sites 0, 1.
    w = q8_weight(TAB, (8, 3, 3, 3, 1))
    ends = [(0, 1), (1, 0), (0, 0), (1, 1)]
    confs = list(itertools.product(range(8), repeat=4))
    gauges = list(itertools.product(range(8), repeat=2))
    seen = {}
    reps, orbits = [], []
    for u in confs:
        if u in seen:
            continue
        o = sorted({tuple(MUL[MUL[g[s]][x]][INV[g[r]]] for x, (s, r) in zip(u, ends)) for g in gauges})
        for v in o:
            seen[v] = len(reps)
        reps.append(u)
        orbits.append(o)
    def area(u):
        p0 = CLS[MUL[MUL[MUL[u[0]][u[3]]][INV[u[0]]]][INV[u[2]]]]
        p1 = CLS[MUL[MUL[MUL[u[1]][u[2]]][INV[u[1]]]][INV[u[3]]]]
        return w[p0] * w[p1]
    table = [[w[CLS[MUL[a][INV[b]]]] for b in range(8)] for a in range(8)]
    n = len(reps)
    A = [area(r) for r in reps]
    M = []
    for i, r in enumerate(reps):
        rows = [table[x] for x in r]
        row = []
        for o in orbits:
            tot = 0
            for other in o:
                t = 1
                for k in range(4):
                    t *= rows[k][other[k]]
                tot += t
            row.append(A[i] * tot * 64)
        M.append(row)
    scale = 64 * 4096
    first = [sum(row) for row in M]
    print("CW_SEPARATE|orbits=%d|f=1_low=%s|f=1_high=%s|json=0" % (n, rtext(rat(min(first), scale)), rtext(rat(max(first), scale))))
    # Tr(AB): the diagonal of A B with no projector. B(U, U) = w(1)^4.
    trab = sum(area(u) * w[0] ** 4 for u in confs)
    print("NO_PROJECTOR_SEPARATE|Tr_AB=%s|json=0" % rtext(rat(trab, 4096)))
    v = [1] * n
    for step in range(1, 121):
        p = [sum(a * b for a, b in zip(row, v)) for row in M]
        if step in (24, 120):
            # Bound by min and max of p/v, over scale, in units of 10^-6.
            lo = min(rat(x * 10 ** 6, y * scale) for x, y in zip(p, v))
            hi = max(rat(x * 10 ** 6, y * scale) for x, y in zip(p, v))
            print("CW_POWER|steps=%d|lambda_0_times_10^6_floor_low=%d|ceil_high=%d|json=0" % (step, min(x * 10 ** 6 // (y * scale) for x, y in zip(p, v)), max(-((-x * 10 ** 6) // (y * scale)) for x, y in zip(p, v))))
        top = max(p)
        v = [max(1, x * 2 ** 80 // top) for x in p]


part_g()
part_t4()
part_cw()
