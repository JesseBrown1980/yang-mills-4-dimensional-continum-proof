#!/usr/bin/env python3
"""Second seat: Tr(T^N_t P) from a transfer matrix on gauge orbits, written from Theorem 5(c), for lattices the builder's rows did not run, against direct sums from the Rust walker. Also the torus rule on new cases.
Standard library, integers only, json=0."""
import itertools
import re
import subprocess
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("\\", 1)[0])
from exact import FiniteGroup, q8_table, q8_weight, rat, radd, rtext, charpoly, inertia_from_charpoly

BRUTE = sys.argv[1]
Q8 = FiniteGroup("Q8")
T2 = FiniteGroup("2T")
TAB = q8_table(Q8)


def spatial(dims):
    n = len(dims)
    sites = list(itertools.product(*[range(d) for d in dims]))
    pos = {s: i for i, s in enumerate(sites)}
    links = [(s, mu) for s in sites for mu in range(n)]
    lid = {l: i for i, l in enumerate(links)}
    def shift(s, mu):
        y = list(s)
        y[mu] = (y[mu] + 1) % dims[mu]
        return tuple(y)
    ends = [(pos[s], pos[shift(s, mu)]) for (s, mu) in links]
    faces = []
    for s in sites:
        for mu in range(n):
            for nu in range(mu + 1, n):
                faces.append(((lid[(s, mu)], 1), (lid[(shift(s, mu), nu)], 1), (lid[(shift(s, nu), mu)], -1), (lid[(s, nu)], -1)))
    return sites, links, ends, faces


class Transfer:
    def __init__(self, G, dims):
        self.G = G
        self.sites, self.links, self.ends, self.faces = spatial(dims)
        self.nl, self.ns = len(self.links), len(self.sites)
        self.ngauge = G.n ** self.ns
        self.nconf = G.n ** self.nl
        seen = set()
        self.reps = []
        self.orbits = []
        mul, inv = G.mul, G.inv
        gauges = list(itertools.product(range(G.n), repeat=self.ns))
        self.gauges = gauges
        for conf in itertools.product(range(G.n), repeat=self.nl):
            if conf in seen:
                continue
            orb = {tuple(mul[mul[g[s]][u]][inv[g[r]]] for u, (s, r) in zip(conf, self.ends)) for g in gauges}
            seen |= orb
            self.reps.append(conf)
            self.orbits.append(sorted(orb))

    def area(self, conf, w):
        G = self.G
        v = 1
        for f in self.faces:
            h = G.one
            for l, s in f:
                h = G.mul[h][conf[l] if s > 0 else G.inv[conf[l]]]
            v *= w[G.cls[h]]
        return v

    def bp_row(self, rep, w):
        """Sum over each orbit of prod_l w(rep_l other_l^-1), times |gauge|/|orbit|: the integer value of sum_g B(rep, other^g)."""
        G = self.G
        table = [[w[G.cls[G.mul[a][G.inv[b]]]] for b in range(G.n)] for a in range(G.n)]
        rows = [table[u] for u in rep]
        out = []
        for orb in self.orbits:
            tot = 0
            for other in orb:
                t = 1
                for i, r in enumerate(rows):
                    t *= r[other[i]]
                tot += t
            out.append(tot * self.ngauge // len(orb))
        return out

    def matrices(self, w):
        A = [self.area(r, w) for r in self.reps]
        BP = [self.bp_row(r, w) for r in self.reps]
        n = len(self.reps)
        o = [len(x) for x in self.orbits]
        M = [[A[i] * BP[i][j] * o[j] for j in range(n)] for i in range(n)]
        scale = self.ngauge * self.nconf
        return A, BP, o, M, scale

    def trace_power(self, M, scale, k):
        n = len(M)
        P = [row[:] for row in M]
        for _ in range(k - 1):
            P = [[sum(P[i][m] * M[m][j] for m in range(n)) for j in range(n)] for i in range(n)]
        return rat(sum(P[i][i] for i in range(n)), scale ** k)

    def trace_one_diagonal(self, w):
        """Tr(ABP) from the orbit representatives, diagonal only."""
        G = self.G
        total = 0
        table = [[w[G.cls[G.mul[a][G.inv[b]]]] for b in range(G.n)] for a in range(G.n)]
        for rep, orb in zip(self.reps, self.orbits):
            rows = [table[u] for u in rep]
            tot = 0
            for other in orb:
                t = 1
                for i, r in enumerate(rows):
                    t *= r[other[i]]
                tot += t
            total += self.area(rep, w) * tot * self.ngauge // len(orb) * len(orb)
        return rat(total, self.ngauge * self.nconf)


def direct(group, dims, w, fix=True):
    args = [BRUTE, "lat", group, "fix" if fix else "nofix", "sum"] + [str(v) for v in w] + ["--"] + [str(d) for d in dims]
    out = subprocess.run(args, capture_output=True, text=True).stdout
    m = re.search(r"numerator=(-?\d+)\|denominator=(\d+)\^(\d+)", out)
    return rat(int(m.group(1)), int(m.group(2)) ** int(m.group(3)))


def part_transfer():
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1), (5, -2, 3, 1, 2)):
        w = q8_weight(TAB, c)
        for sd, steps in (((2, 1), (2,)), ((1, 1), (1, 2, 3)), ((1, 1, 1), (1, 2, 3)), ((1,), (2, 3, 4, 5))):
            tr = Transfer(Q8, sd)
            A, BP, o, M, scale = tr.matrices(w)
            sym = all(BP[i][j] == BP[j][i] for i in range(len(BP)) for j in range(len(BP)))
            for k in steps:
                val = tr.trace_power(M, scale, k)
                dims = list(sd) + [k]
                d = direct("Q8", dims, w, True)
                extra = ""
                if dims == [1, 1, 1, 2]:
                    d2 = direct("Q8", dims, w, False)
                    extra = "|direct_no_gauge_fixing=%s" % rtext(d2)
                print("TRANSFER_NEW|group=Q8|c=%s|w=%s|spatial=%s|N_t=%d|orbits=%d|Tr_T^N_P=%s|direct=%s%s|equal=%d|BP_symmetric=%d|json=0" % (
                    ",".join(map(str, c)), ",".join(map(str, w)), "x".join(map(str, sd)), k, len(tr.reps), rtext(val), rtext(d), extra, 1 if val == d else 0, 1 if sym else 0), flush=True)
        # Spatial (Z/3)x(Z/1) with one step, and (Z/2)x(Z/1)x(Z/1) with one step, diagonal only.
        for sd in ((3, 1), (2, 1, 1)):
            tr = Transfer(Q8, sd)
            val = tr.trace_one_diagonal(w)
            d = direct("Q8", list(sd) + [1], w, True)
            print("TRANSFER_NEW|group=Q8|c=%s|spatial=%s|N_t=1|orbits=%d|Tr_T_P=%s|direct=%s|equal=%d|json=0" % (
                ",".join(map(str, c)), "x".join(map(str, sd)), len(tr.reps), rtext(val), rtext(d), 1 if val == d else 0), flush=True)
    # 2T with a real weight, classes in the walker's order.
    w = t2_real_weight((7, 2, 2, 4, 3, 1, 1))
    for sd, steps in (((1,), (2, 3, 4)), ((1, 1), (1, 2))):
        tr = Transfer(T2, sd)
        A, BP, o, M, scale = tr.matrices(w)
        for k in steps:
            val = tr.trace_power(M, scale, k)
            d = direct("2T", list(sd) + [k], w, True)
            print("TRANSFER_NEW|group=2T|w=%s|spatial=%s|N_t=%d|orbits=%d|Tr_T^N_P=%s|direct=%s|equal=%d|json=0" % (
                ",".join(map(str, w)), "x".join(map(str, sd)), k, len(tr.reps), rtext(val), rtext(d), 1 if val == d else 0), flush=True)


def t2_tables():
    G = T2
    e = G.elems.index((1, 1, 1, 1))
    e2 = G.mul[e][e]
    q8 = {i for i, v in enumerate(G.elems) if sorted(abs(u) for u in v) == [0, 0, 0, 2]}
    coset = []
    for g in range(G.n):
        if g in q8:
            coset.append(0)
        elif G.mul[G.inv[e]][g] in q8:
            coset.append(1)
        else:
            assert G.mul[G.inv[e2]][g] in q8
            coset.append(2)
    W = [(1, 0), (0, 1), (-1, -1)]  # 1, w, w^2 as a + b w
    def wm(x, y):
        # w^2 = -1 - w
        return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0] - x[1] * y[1])
    rows = []
    for shape in range(7):
        row = []
        for orbit in G.classes:
            g = orbit[0]
            tau = G.elems[g][0]
            lam = W[coset[g]]
            lam2 = W[(2 * coset[g]) % 3]
            row.append({0: (1, 0), 1: lam, 2: lam2, 3: (tau * tau - 1, 0), 4: (tau, 0), 5: (tau * lam[0], tau * lam[1]), 6: (tau * lam2[0], tau * lam2[1])}[shape])
        rows.append(row)
    return rows, wm


def t2_real_weight(c):
    rows, wm = t2_tables()
    out = []
    for k in range(7):
        s = (0, 0)
        for r in range(7):
            s = (s[0] + c[r] * rows[r][k][0], s[1] + c[r] * rows[r][k][1])
        assert s[1] == 0
        out.append(s[0])
    return out


def part_torus():
    dims_q8 = [(1, 2), (1, 3), (1, 5), (5, 1), (2, 3), (3, 3), (4, 2), (2, 4), (5, 2), (1, 1)]
    for c in ((8, 3, 3, 3, 1), (8, 3, 3, 3, -1), (5, -2, 3, 1, 2), (1, 1, -2, 3, -4)):
        w = q8_weight(TAB, c)
        dim = [1, 1, 1, 1, 2]
        for L, T in dims_q8:
            F = L * T
            rule = (0, 1)
            for r in range(5):
                rule = radd(rule, rat(c[r] ** F, dim[r] ** F))
            d = direct("Q8", [L, T], w, True)
            print("TORUS_NEW|group=Q8|c=%s|w=%s|L=%d|T=%d|F=%d|direct=%s|rule=%s|equal=%d|json=0" % (",".join(map(str, c)), ",".join(map(str, w)), L, T, F, rtext(d), rtext(rule), 1 if d == rule else 0), flush=True)
    # 2T, complex weight, from a histogram. Base 7 digits, one per plaquette.
    rows, wm = t2_tables()
    dimt = [1, 1, 1, 3, 2, 2, 2]
    for L, T in ((1, 4), (1, 5), (2, 2), (3, 1), (3, 2), (2, 3)):
        out = subprocess.run([BRUTE, "lat", "2T", "fix", "hist", "--", str(L), str(T)], capture_output=True, text=True).stdout
        hist = {}
        for line in out.splitlines():
            if line.startswith("HIST|"):
                m = re.match(r"HIST\|key=(\d+)\|count=(\d+)", line)
                hist[int(m.group(1))] = int(m.group(2))
        F = L * T
        free = int(re.search(r"free=(\d+)", out).group(1))
        for c in ((7, 2, 1, 4, 3, 1, 2), (3, -5, 1, 2, -4, 6, 1)):
            weight = []
            for k in range(7):
                s = (0, 0)
                for r in range(7):
                    s = (s[0] + c[r] * rows[r][k][0], s[1] + c[r] * rows[r][k][1])
                weight.append(s)
            total = (0, 0)
            for key, cnt in hist.items():
                t = (cnt, 0)
                k = key
                for _ in range(F):
                    t = wm(t, weight[k % 7])
                    k //= 7
                total = (total[0] + t[0], total[1] + t[1])
            rule = (0, 1)
            for r in range(7):
                rule = radd(rule, rat(c[r] ** F, dimt[r] ** F))
            direct_val = rat(total[0], 24 ** free)
            print("TORUS_NEW|group=2T|c=%s|L=%d|T=%d|F=%d|assignments=24^%d|imaginary=%d|direct=%s|rule=%s|equal=%d|json=0" % (",".join(map(str, c)), L, T, F, free, total[1], rtext(direct_val), rtext(rule), 1 if direct_val == rule and total[1] == 0 else 0), flush=True)


if "torus" in sys.argv:
    part_torus()
if "transfer" in sys.argv:
    part_transfer()
