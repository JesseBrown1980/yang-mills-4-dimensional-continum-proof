# Scratch checks for the G0 assembly-and-constants attack. Integers and Fractions only.
# Not an engine, not evidence. Floats appear only in display.
import sys
from fractions import Fraction as Fr
from itertools import product, combinations

def say(*a):
    print(*a)
    sys.stdout.flush()

# ---------------- A: pi, E|chi_1/2| = 8/(3 pi), and the 8489/10000 bound ----------------
def atan_partial(y, terms):
    s = Fr(0)
    for k in range(terms):
        s += Fr((-1) ** k) * y ** (2 * k + 1) / (2 * k + 1)
    return s

def pi_bounds(t5, t239):
    # even number of terms: lower bound; odd: upper bound (0 < y < 1, terms decreasing)
    lo = 16 * atan_partial(Fr(1, 5), 2 * t5) - 4 * atan_partial(Fr(1, 239), 2 * t239 - 1)
    hi = 16 * atan_partial(Fr(1, 5), 2 * t5 + 1) - 4 * atan_partial(Fr(1, 239), 2 * t239)
    return lo, hi

lo_a = 16 * (Fr(1, 5) - Fr(1, 375) + Fr(1, 15625) - Fr(1, 546875)) - Fr(4, 239)
say("A G0-a lower bound on pi =", lo_a, " > 333/106:", lo_a > Fr(333, 106))
say("A G0-a 848/999 < 8489/10000:", Fr(848, 999) < Fr(8489, 10000), " 8/(3*333/106) == 848/999:", Fr(8) / (3 * Fr(333, 106)) == Fr(848, 999))
say("A G0-b lower bound 1231847548/392109375 equals G0-a's Machin sum:", lo_a == Fr(1231847548, 392109375))
plo, phi = pi_bounds(6, 2)
say("A pi in [%.12f, %.12f], width %.1e" % (float(plo), float(phi), float(phi - plo)))
e_lo, e_hi = Fr(8) / (3 * phi), Fr(8) / (3 * plo)
say("A 8/(3 pi) in [%.11f, %.11f]" % (float(e_lo), float(e_hi)))
say("A 8/(3 pi) < 0.8488264 (so [0.8488264, 0.8488266] is not an enclosure):", e_hi < Fr(8488264, 10 ** 7))
say("A outward 7-digit enclosure [0.8488263, 0.8488264] valid:", Fr(8488263, 10 ** 7) <= e_lo and e_hi <= Fr(8488264, 10 ** 7))
say("A margin 8489/10000 - 8/(3 pi) in [%.6e, %.6e]" % (float(Fr(8489, 10000) - e_hi), float(Fr(8489, 10000) - e_lo)))
say("A ratio 2*(8489/10000)/(8/(3pi)) in [%.6f, %.6f]" % (float(2 * Fr(8489, 10000) / e_hi), float(2 * Fr(8489, 10000) / e_lo)))

# ---------------- B: geometry at N = 8 and N = 10 ----------------
def build(N):
    D = 4
    sites = list(product(range(N), repeat=D))
    def add(x, mu, s=1):
        y = list(x); y[mu] = (y[mu] + s) % N; return tuple(y)
    def odd(x):
        return frozenset(l for l in range(D) if x[l] % 2)
    links = {}
    for x in sites:
        for mu in range(D):
            links[(x, mu)] = len(links)
    lcls = [None] * len(links)
    for (x, mu), i in links.items():
        lcls[i] = len(odd(x) - {mu})
    plaqs = []
    for x in sites:
        for mu in range(D):
            for nu in range(mu + 1, D):
                ls = (links[(x, mu)], links[(add(x, mu), nu)], links[(add(x, nu), mu)], links[(x, nu)])
                plaqs.append((x, mu, nu, ls))
    inc = [[] for _ in links]
    for pid, (_, _, _, ls) in enumerate(plaqs):
        for l in ls:
            inc[l].append(pid)
    return dict(N=N, sites=sites, add=add, odd=odd, links=links, lcls=lcls, plaqs=plaqs, inc=inc)

def geometry(G):
    N, add, links, lcls, plaqs, inc = G['N'], G['add'], G['links'], G['lcls'], G['plaqs'], G['inc']
    ok6 = all(len(v) == 6 for v in inc)
    offs = set(len([l for l in p[3] if lcls[l] > 0]) for p in plaqs)
    L = N // 2
    W12 = W6 = fill_ok = True
    nfill_per_link = set()
    for xc in product(range(L), repeat=4):
        for mu in range(4):
            x0 = tuple(2 * c for c in xc)
            m = add(x0, mu)
            e0, e1 = links[(x0, mu)], links[(m, mu)]
            through0 = inc[e0]
            W = set(l for p in through0 for l in plaqs[p][3] if lcls[l] > 0)
            if len(W) != 12:
                W12 = False
            # W'(l): the off links with an end at m
            Wp = set()
            for nu in range(4):
                if nu == mu:
                    continue
                Wp.add(links[(m, nu)])
                Wp.add(links[(add(m, nu, -1), nu)])
            if len(Wp) != 6 or not all(lcls[l] > 0 for l in Wp):
                W6 = False
            for p in through0 + inc[e1]:
                if len([l for l in plaqs[p][3] if l in Wp]) != 1:
                    W6 = False
            # fillings through l: the 4 quarters around a center s = m + e_nu or m - e_nu
            fills = []
            for nu in range(4):
                if nu == mu:
                    continue
                for sg in (1, -1):
                    s = add(m, nu, sg)
                    a, b = min(mu, nu), max(mu, nu)
                    F = set()
                    for da, db in product((0, -1), repeat=2):
                        base = add(add(s, a, da), b, db)
                        F.add([i for i in inc[links[(base, a)]] if plaqs[i][0] == base and plaqs[i][1] == a and plaqs[i][2] == b][0])
                    fills.append(F)
            nfill_per_link.add(len(fills))
            for F in fills:
                held = set(l for p in F for l in plaqs[p][3])
                if not (e0 in held and e1 in held):
                    fill_ok = False
                if len(held & W) != 2 or len(held & Wp) != 1:
                    fill_ok = False
    return ok6, offs, W12, W6, fill_ok, nfill_per_link

def coarse_girth_facts(L):
    # no 3-cycles in (Z/L)^4; a 5-cycle (straight winding loop) exists exactly when L = 5
    def nb(x):
        out = []
        for mu in range(4):
            for s in (1, -1):
                y = list(x); y[mu] = (y[mu] + s) % L; out.append(tuple(y))
        return out
    tri = False
    x = (0, 0, 0, 0)
    for y, z in combinations(set(nb(x)), 2):
        if z in nb(y):
            tri = True
    two = len(nb(x)) != len(set(nb(x)))
    odd_cycle = (L % 2 == 1)
    return tri, two, odd_cycle

for N in (8, 10):
    G = build(N)
    ok6, offs, W12, W6, fill_ok, nf = geometry(G)
    tri, two, oddc = coarse_girth_facts(N // 2)
    say("B N=%d: every link in 6 plaquettes %s; off links per plaquette %s; #W(e_0)=12 at every coarse link %s;"
        " #W'(l)=6 and each plaquette through e_0 or e_1 meets W'(l) once %s; 6 fillings through l, each holding e_0, e_1,"
        " 2 links of W(e_0), 1 of W'(l) %s (count %s)" % (N, ok6, sorted(offs), W12, W6, fill_ok, sorted(nf)))
    say("B coarse side L=%d: a 3-cycle exists %s; a double edge exists %s; an odd cycle (L-cycle) exists, so not bipartite: %s"
        % (N // 2, tri, two, oddc))

# ---------------- C: closed-set counts through an off link, n <= NMAX, on N = 8 and N = 10 ----------------
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
assert 4 <= NMAX <= 10
C03_FULL = {1: [1, 0, 12, 0, 32, 32, 304], 2: [0, 0, 12, 0, 12, 12, 240], 3: [0, 0, 12, 0, 0, 0, 216]}
C03 = {c: v[:NMAX - 3] for c, v in C03_FULL.items()}

def closed_sets_through(G, w, nmax):
    lcls, plaqs, inc = G['lcls'], G['plaqs'], G['inc']
    offl = [[l for l in p[3] if lcls[l] > 0] for p in plaqs]
    seen = set()
    found = set()
    stack = [frozenset([p]) for p in inc[w]]
    for s in stack:
        seen.add(s)
    while stack:
        T = stack.pop()
        mult = {}
        for p in T:
            for l in offl[p]:
                mult[l] = mult.get(l, 0) + 1
        openl = sorted(l for l, c in mult.items() if c == 1)
        if not openl:
            found.add(T)
            if len(T) < nmax:
                cand = set(q for l in mult for q in inc[l]) - T
            else:
                cand = ()
        else:
            if len(T) >= nmax or 4 * (nmax - len(T)) < len(openl):
                continue
            cand = [q for q in inc[openl[0]] if q not in T]
        for q in cand:
            U = T | {q}
            if U not in seen:
                seen.add(U)
                stack.append(U)
    return found, len(seen)

def lift_consistent(G, S):
    # BFS lift along off-link adjacency; False if some cycle of the adjacency graph winds
    N, lcls, plaqs, inc = G['N'], G['lcls'], G['plaqs'], G['inc']
    S = list(S)
    Sset = set(S)
    lift = {S[0]: tuple(plaqs[S[0]][0])}
    queue = [S[0]]
    while queue:
        p = queue.pop()
        for l in plaqs[p][3]:
            if lcls[l] == 0:
                continue
            for q in inc[l]:
                if q == p or q not in Sset:
                    continue
                d = []
                for i in range(4):
                    di = (plaqs[q][0][i] - plaqs[p][0][i]) % N
                    if di > N // 2:
                        di -= N
                    d.append(di)
                yq = tuple(lift[p][i] + d[i] for i in range(4))
                if q in lift:
                    if lift[q] != yq:
                        return False
                else:
                    lift[q] = yq
                    queue.append(q)
    return True

def Ypp(G, S):
    # coarse links both of whose positions S holds; returned as (coarse site, mu)
    N, plaqs, lcls, links = G['N'], G['plaqs'], G['lcls'], G['links']
    inv = {i: k for k, i in links.items()}
    held = set(l for p in S for l in plaqs[p][3] if lcls[l] == 0)
    out = set()
    for l in held:
        x, mu = inv[l]
        if x[mu] % 2 == 0:
            m = list(x); m[mu] = (m[mu] + 1) % N; m = tuple(m)
            if G['links'][(m, mu)] in held:
                out.add((tuple(c // 2 for c in x), mu))
    return out

def has_cycle(L, Y):
    # union-find on coarse sites
    par = {}
    def f(a):
        while par.get(a, a) != a:
            a = par[a]
        return a
    for (x, mu) in Y:
        y = list(x); y[mu] = (y[mu] + 1) % L; y = tuple(y)
        a, b = f(x), f(y)
        if a == b:
            return True
        par[a] = b
    return False

for N in (8, 10):
    G = build(N)
    links, lcls, add = G['links'], G['lcls'], G['add']
    seeds = {1: ((1, 1, 0, 0), 0), 2: ((0, 1, 1, 0), 0), 3: ((0, 1, 1, 1), 0)}
    for c, (x, mu) in seeds.items():
        w = links[(x, mu)]
        assert lcls[w] == c
        found, nst = closed_sets_through(G, w, NMAX)
        counts = [sum(1 for S in found if len(S) == n) for n in range(4, NMAX + 1)]
        small = sum(1 for S in found if len(S) < 4)
        wind = sum(1 for S in found if not lift_consistent(G, S))
        yy_ok = True
        loop_sizes = {}
        for S in found:
            Y = Ypp(G, S)
            nline = sum(1 for p in S if any(lcls[l] == 0 for l in G['plaqs'][p][3]))
            if not (len(Y) <= nline <= len(S)):
                yy_ok = False
            if has_cycle(N // 2, Y):
                loop_sizes[len(S)] = loop_sizes.get(len(S), 0) + 1
                if len(Y) < 4:
                    yy_ok = False
        say("C N=%d class %d: states %d; closed sets n=4..%d: %s; C03 says %s; equal: %s; sets below 4: %d;"
            " winding sets: %d; #Y''<=#line plaquettes<=#gamma and loops only with #Y''>=4: %s; sets with a loop in Y'' by size: %s"
            % (N, c, nst, NMAX, counts, C03[c], counts == C03[c], small, wind, yy_ok, sorted(loop_sizes.items())))
