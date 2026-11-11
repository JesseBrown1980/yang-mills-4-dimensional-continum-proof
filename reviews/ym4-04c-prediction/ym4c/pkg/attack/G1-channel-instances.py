# G1 channel attack: the two smallest instances, exactly. Integers and Fractions only.
# Fine lattice (Z/8)^4 at scale k, coarse (Z/4)^4 at scale k+1, b = 2 line map.
from fractions import Fraction as F
import itertools, random

M = 8
D = 4
E = [tuple(1 if i == mu else 0 for i in range(D)) for mu in range(D)]


def add(x, y, s=1):
    return tuple((a + s * b) % M for a, b in zip(x, y))


sites = list(itertools.product(range(M), repeat=D))
links = [(x, mu) for x in sites for mu in range(D)]


def is_line(link):
    x, mu = link
    return all(x[i] % 2 == 0 for i in range(D) if i != mu)


def coarse_of(link):
    """(coarse link, position) for a line link."""
    x, mu = link
    xc = tuple(x[i] // 2 for i in range(D))
    return (xc, mu), x[mu] % 2


line_links = [l for l in links if is_line(l)]
off_links = [l for l in links if not is_line(l)]
print("fine links", len(links), "line", len(line_links), "off", len(off_links))

# midpoint rule: a midpoint meets exactly two line links
def links_at(site):
    out = []
    for mu in range(D):
        out.append((site, mu))
        out.append((add(site, E[mu], -1), mu))
    return out

mid_ok = True
for x in sites:
    odd = [i for i in range(D) if x[i] % 2]
    if len(odd) == 1:
        ll = [l for l in links_at(x) if is_line(l)]
        mid_ok &= (len(ll) == 2 and {coarse_of(l)[0] for l in ll} == {((tuple(x[i] // 2 for i in range(D))), odd[0])})
print("every midpoint meets exactly the two line links of its coarse link:", mid_ok)

# a fine closed loop of line links only is a subdivided coarse loop: line links at a non-coarse, non-midpoint site
bad_sites = 0
for x in sites:
    odd = [i for i in range(D) if x[i] % 2]
    if len(odd) >= 2:
        bad_sites += sum(1 for l in links_at(x) if is_line(l))
print("line links touching a site with >= 2 odd coordinates:", bad_sites)

# ---------- C10: one line-supported object per coarse plaquette ----------
L = M // 2
csites = list(itertools.product(range(L), repeat=D))


def cadd(x, y, s=1):
    return tuple((a + s * b) % L for a, b in zip(x, y))


cplaq = [(x, mu, nu) for x in csites for mu in range(D) for nu in range(mu + 1, D)]


def fine_line_pair(cl):
    (xc, mu) = cl
    x0 = tuple(2 * a for a in xc)
    return [(x0, mu), (add(x0, E[mu]), mu)]


def cboundary(P):
    x, mu, nu = P
    return [(x, mu), (cadd(x, E[mu]), nu), (cadd(x, E[nu]), mu), (x, nu)]


Ys = {}
for P in cplaq:
    Y = []
    for cl in cboundary(P):
        Y += fine_line_pair(cl)
    Ys[P] = frozenset(Y)
mult = {}
for P, Y in Ys.items():
    for l in Y:
        mult[l] = mult.get(l, 0) + 1
print("C10: #Y =", {len(Y) for Y in Ys.values()},
      "| multiplicity on line links:", {mult.get(l, 0) for l in line_links},
      "| on off links:", {mult.get(l, 0) for l in off_links})


def shadow(Y):
    """Y'' = coarse links with both positions in Y."""
    pos = {}
    for l in Y:
        if is_line(l):
            cl, p = coarse_of(l)
            pos.setdefault(cl, set()).add(p)
    return frozenset(cl for cl, s in pos.items() if s == {0, 1})


cmult = {}
for P in cplaq:
    for cl in cboundary(P):
        cmult[cl] = cmult.get(cl, 0) + 1
print("C10: Y'' = boundary for every P'':", all(shadow(Ys[P]) == frozenset(cboundary(P)) for P in cplaq),
      "| 2#Y'' = #Y:", all(2 * len(shadow(Ys[P])) == len(Ys[P]) for P in cplaq),
      "| coarse plaquettes per coarse link:", set(cmult.values()))
k = F(1, 4)
print("C10 ratio: (6 * 2|s| e^{4k}) / (6 * 2|s| e^{8k}) = e^{-4k}; exponents:", 4 * k, "-", 8 * k)

# ---------- exact quaternion holonomies ----------
def qmul(a, b):
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return (a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3,
            a0 * b1 + a1 * b0 + a2 * b3 - a3 * b2,
            a0 * b2 - a1 * b3 + a2 * b0 + a3 * b1,
            a0 * b3 + a1 * b2 - a2 * b1 + a3 * b0)


def qinv(a):
    return (a[0], -a[1], -a[2], -a[3])


def rq(rng):
    """Rational unit quaternion by the Cayley-type map v -> (1 - |v|^2, 2v)/(1 + |v|^2)."""
    v = [F(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(4)]
    n = sum(t * t for t in v)
    return tuple(t / n for t in [v[0] * v[0] - v[1] * v[1] - v[2] * v[2] - v[3] * v[3],
                                  2 * v[0] * v[1], 2 * v[0] * v[2], 2 * v[0] * v[3]]) if n else (F(1), F(0), F(0), F(0))


def unit(q):
    return sum(t * t for t in q) == 1


rng = random.Random(20261109)
ok_hol = True
ok_inv = True
for trial in range(4):
    V = {}
    for x in csites:
        for mu in range(D):
            q = rq(rng)
            assert unit(q)
            V[(x, mu)] = q
    # line gauge: (U0, U1) = (1, V); off links: random rational unit quaternions
    U = {}
    for l in links:
        if is_line(l):
            cl, p = coarse_of(l)
            U[l] = V[cl] if p == 1 else (F(1), F(0), F(0), F(0))
        else:
            U[l] = rq(rng)
    # random fine gauge transformation
    g = {x: rq(rng) for x in sites}
    Ug = {(x, mu): qmul(qmul(g[x], U[(x, mu)]), qinv(g[add(x, E[mu])])) for (x, mu) in links}
    for P in cplaq[:: max(1, len(cplaq) // 6)]:
        x, mu, nu = P
        x0 = tuple(2 * a for a in x)
        # fine 2x2 loop: +mu,+mu,+nu,+nu,-mu,-mu,-nu,-nu
        def hol(UU):
            h = (F(1), F(0), F(0), F(0))
            y = x0
            for d, s in [(mu, 1), (mu, 1), (nu, 1), (nu, 1), (mu, -1), (mu, -1), (nu, -1), (nu, -1)]:
                if s == 1:
                    h = qmul(h, UU[(y, d)])
                    y = add(y, E[d])
                else:
                    y = add(y, E[d], -1)
                    h = qmul(h, qinv(UU[(y, d)]))
            return h
        VP = qmul(qmul(V[(x, mu)], V[(cadd(x, E[mu]), nu)]), qmul(qinv(V[(cadd(x, E[nu]), mu)]), qinv(V[(x, nu)])))
        ok_hol &= (hol(U) == VP)
        # BU of the gauge-transformed configuration, coarse plaquette trace vs fine loop trace
        def BU(UU, cl):
            a, b = fine_line_pair(cl)
            return qmul(UU[a], UU[b])
        VPg = qmul(qmul(BU(Ug, (x, mu)), BU(Ug, (cadd(x, E[mu]), nu))), qmul(qinv(BU(Ug, (cadd(x, E[nu]), mu))), qinv(BU(Ug, (x, nu)))))
        ok_inv &= (hol(Ug)[0] == VPg[0] == VP[0])
print("C10 holonomy: fine 2x2 loop in the line gauge equals V_P'':", ok_hol,
      "| trace unchanged under a rational fine gauge transformation, through BU:", ok_inv)

# ---------- C10b: two 1x2 rectangles sharing the arm ----------
def rects(P):
    x, mu, nu = P
    lo, hi = (mu, nu)  # split along the lower direction mu: bottom and top halves in nu
    x0 = tuple(2 * a for a in x)
    def path(start, steps):
        out = []
        y = start
        for d, s in steps:
            if s == 1:
                out.append((y, d)); y = add(y, E[d])
            else:
                y = add(y, E[d], -1); out.append((y, d))
        return out
    bot = path(x0, [(mu, 1), (mu, 1), (nu, 1), (mu, -1), (mu, -1), (nu, -1)])
    top = path(add(x0, E[nu]), [(mu, 1), (mu, 1), (nu, 1), (mu, -1), (mu, -1), (nu, -1)])
    return frozenset(bot), frozenset(top)

rm = {}
arm_ok = True
sh_ok = True
for P in cplaq:
    b, t = rects(P)
    arm = b & t
    arm_ok &= (len(arm) == 2 and all(not is_line(l) for l in arm) and len(b) == 6 and len(t) == 6
               and sum(is_line(l) for l in b) == 4 and sum(is_line(l) for l in t) == 4)
    sh_ok &= (len(shadow(b)) == 1 and len(shadow(t)) == 1 and shadow(b | t) == frozenset(cboundary(P)))
    for o in (b, t):
        for l in o:
            rm[l] = rm.get(l, 0) + 1
print("C10b: each rectangle 6 links (4 line, 2 arm off links shared):", arm_ok)
print("C10b: Y'' of each rectangle alone is 1 coarse link (no loop); of the pair, the boundary of P'':", sh_ok)
print("C10b: rectangles per line link:", {rm.get(l, 0) for l in line_links},
      "| per off link:", sorted({rm.get(l, 0) for l in off_links}))

# Exact moments of X = chi_b + chi_t over the Haar arm pi (pi uniform on S^3):
# chi_b = 2<A, pi>, chi_t = 2<Bbar, pi>, so X = <c, pi>, c = 2(A + Bbar), E[<c,pi>^{2m}] = |c|^{2m} (2m-1)!!/(2^m (m+1)!).
def dot(a, b):
    return sum(x * y for x, y in zip(a, b))
mom_ok = True
for trial in range(6):
    A, B = rq(rng), rq(rng)
    chi = 2 * qmul(A, B)[0]
    c = tuple(2 * (a + bb) for a, bb in zip(A, qinv(B)))
    c2 = dot(c, c)
    for m in range(1, 7):
        dfact = 1
        for j in range(1, 2 * m, 2):
            dfact *= j
        fact = 1
        for j in range(1, m + 2):
            fact *= j
        mom = c2 ** m * F(dfact, 2 ** m * fact)
        cat = F(1)
        # Cat_m = C(2m, m)/(m+1)
        from math import comb
        cat = F(comb(2 * m, m), m + 1)
        mom_ok &= (mom == cat * (2 + chi) ** m)
print("C10b moments E[X^{2m}] = Cat_m (2 + chi_1/2(V_P''))^m, m = 1..6, 6 rational (A, B):", mom_ok)

# ---------- the slice lower bound ----------
# On the slice where every coarse link other than l is 1, log rho_{k+1} = const + 6 f(chi_1/2(V_l)) for C10, C10b, C10c,
# and every R(Y) with l not in Y is constant there. So sum_{Y ni l} sup|R(Y)| >= (1/2) osc(6 f) = 3 osc(f) for every representation.
slice_ok = True
for trial in range(3):
    lsel = ((0, 0, 0, 0), 0)
    g = rq(rng)
    V = {(x, mu): (F(1), F(0), F(0), F(0)) for x in csites for mu in range(D)}
    V[lsel] = g
    chis = []
    for P in cplaq:
        x, mu, nu = P
        VP = qmul(qmul(V[(x, mu)], V[(cadd(x, E[mu]), nu)]), qmul(qinv(V[(cadd(x, E[nu]), mu)]), qinv(V[(x, nu)])))
        chis.append((lsel in cboundary(P), 2 * VP[0]))
    slice_ok &= (sum(1 for a, _ in chis if a) == 6 and all(ch == 2 * g[0] for a, ch in chis if a) and all(ch == 2 for a, ch in chis if not a))
print("slice: with every coarse link but l at 1, the 6 plaquettes through l read chi(V_l) and the rest read 2:", slice_ok)
