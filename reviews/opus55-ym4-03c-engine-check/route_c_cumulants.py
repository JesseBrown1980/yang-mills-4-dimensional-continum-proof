# YM4-03C engine check, route C. Integers and integer pairs only, standard library only, json=0.
#
# Route C reads the coefficients of log rho(V) in a way kept apart from the engine:
#  - cumulants of the plaquette variables a_p = Re Tr U_p / 2 by the moment-cumulant recursion over sub-multisets,
#    with the multinomial 1/prod m_p! written per multiset (no polymers, no t-series, no McKay fold, no cluster expansion);
#  - placed supports in the unbounded lattice Z^d, summed one by one (no classes, no orbits, no stabilizers);
#  - the line gauge (V, 1): position 0 of each coarse line holds V_l and position 1 holds 1 (the engine uses (1, V));
#  - coarse gauge fixed by the comb tree (x', mu) with x'_nu = 0 for nu > mu, so the coarse plaquette P0 = (0; 0,1)
#    reads V_P0 = g^-1 with g = V on the coarse link (e1, 0), and the chair P0, Q0 = (0; 0,2) reads g1 g2^-1;
#  - SU(2) Haar integration of polynomials in the complex coordinates U = [[a, -b*], [b, a*]] by
#    E[a^p a*^q b^r b*^s] = [p = q][r = s] p! r! / (p + r + 1)!, link by link, after gauge fixing at fine sites
#    with two or more odd coordinates (no Weingarten matrix, no character merge);
#  - readout of chi_j(V_P0) by restricting the class function of g to the torus diag(z, 1/z) and reading
#    (z - 1/z) f(z), every other coarse link integrated (spin 0 there); the chair and N1 by inserting the functional and
#    integrating every coarse link.
#  - G2: the family of two disjoint fillings measured as a moment and as a cumulant, and rho/int rho on chi_1(V_P) at
#    beta^8 from this route's own log rho coefficients;
#  - each read set beside the frozen value, and the frozen literal looked up in the first 26 lines of
#    docs/PREDICTION-YM4-03C.hbp; a MISS makes the exit code 1.
# Usage, from the repository root: python3 -I -B -X utf8 route_c_cumulants.py D TOP [OPTION]
# OPTION: lemma_a (read only supports holding both positions of (e1, 0)), gauge_1V (the control gauge, V at position 1),
# or a planted error: plant_no_multinomial, plant_moment_for_cumulant, plant_support_twice, plant_recursion_sign.
import sys
from math import gcd, factorial

# ------------------------------------------------------------------ rationals as integer pairs


def rq(n, d=1):
    if d < 0:
        n, d = -n, -d
    g = gcd(n, d)
    if g > 1:
        n //= g
        d //= g
    return (n, d)


def radd(x, y):
    return rq(x[0] * y[1] + y[0] * x[1], x[1] * y[1])


def rmul(x, y):
    return rq(x[0] * y[0], x[1] * y[1])


def rshow(x):
    if x[1] == 1:
        return str(x[0])
    return str(x[0]) + "/" + str(x[1])


RZ = (0, 1)
R1 = (1, 1)

# ------------------------------------------------------------------ polynomials: dict mono -> int numerator, one denominator
# A monomial is an int with 5 bits per symbol and 4 symbols (a, a*, b, b*) per slot.
SB = 5
SM = (1 << SB) - 1
SLOTB = 4 * SB
SLOTM = (1 << SLOTB) - 1
FACT = [factorial(i) for i in range(64)]


def sym(slot, t):
    return 1 << (SLOTB * slot + SB * t)


def preduce(p):
    d, den = p
    if not d:
        return ({}, 1)
    g = den
    for c in d.values():
        g = gcd(g, c)
        if g == 1:
            break
    if g > 1:
        d = {m: c // g for m, c in d.items()}
        den //= g
    return (d, den)


def pmul(p, q):
    a, da = p
    b, db = q
    out = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = m1 + m2
            out[m] = out.get(m, 0) + c1 * c2
    out = {m: c for m, c in out.items() if c != 0}
    return preduce((out, da * db))


def padd(p, q):
    a, da = p
    b, db = q
    out = {}
    for m, c in a.items():
        out[m] = out.get(m, 0) + c * db
    for m, c in b.items():
        out[m] = out.get(m, 0) + c * da
    out = {m: c for m, c in out.items() if c != 0}
    return preduce((out, da * db))


def pscale(p, r):
    d, den = p
    return preduce(({m: c * r[0] for m, c in d.items() if c * r[0] != 0}, den * r[1]))


def pconst(r):
    if r[0] == 0:
        return ({}, 1)
    return ({0: r[0]}, r[1])


def slots_of(p):
    s = set()
    for m in p[0]:
        k = 0
        while m:
            if m & SLOTM:
                s.add(k)
            m >>= SLOTB
            k += 1
    return s


def slot_exps(m, s):
    f = (m >> (SLOTB * s)) & SLOTM
    return (f & SM, (f >> SB) & SM, (f >> (2 * SB)) & SM, (f >> (3 * SB)) & SM)


def pintegrate(p, s):
    # Haar over the slot s: E[a^p a*^q b^r b*^s] = [p=q][r=s] p! r!/(p+r+1)!
    d, den = p
    clear = ~(SLOTM << (SLOTB * s))
    surv = []
    kmax = 0
    for m, c in d.items():
        ea, eab, eb, ebb = slot_exps(m, s)
        if ea != eab or eb != ebb:
            continue
        surv.append((m & clear, c, ea, eb))
        kmax = max(kmax, ea + eb + 1)
    if not surv:
        return ({}, 1)
    big = FACT[kmax]
    out = {}
    for m, c, ea, eb in surv:
        w = FACT[ea] * FACT[eb] * (big // FACT[ea + eb + 1])
        out[m] = out.get(m, 0) + c * w
    out = {m: c for m, c in out.items() if c != 0}
    return preduce((out, den * big))


def pmul_integrate(p, q, s):
    # (p q) integrated over slot s, multiplying only the pairs whose slot-s exponents can close
    a, da = p
    b, db = q
    ga = {}
    for m, c in a.items():
        ga.setdefault(slot_exps(m, s), []).append((m, c))
    gb = {}
    for m, c in b.items():
        gb.setdefault(slot_exps(m, s), []).append((m, c))
    clear = ~(SLOTM << (SLOTB * s))
    acc = {}
    kmax = 0
    pairs = []
    for ka, la in ga.items():
        for kb, lb in gb.items():
            ea = ka[0] + kb[0]
            eab = ka[1] + kb[1]
            eb = ka[2] + kb[2]
            ebb = ka[3] + kb[3]
            if ea != eab or eb != ebb:
                continue
            pairs.append((la, lb, ea, eb))
            kmax = max(kmax, ea + eb + 1)
    if not pairs:
        return ({}, 1)
    big = FACT[kmax]
    for la, lb, ea, eb in pairs:
        w = FACT[ea] * FACT[eb] * (big // FACT[ea + eb + 1])
        for m1, c1 in la:
            for m2, c2 in lb:
                m = (m1 + m2) & clear
                acc[m] = acc.get(m, 0) + c1 * c2 * w
    acc = {m: c for m, c in acc.items() if c != 0}
    return preduce((acc, da * db * big))


def eliminate(factors, int_slots):
    # factors: list of polys; integrate every slot in int_slots, min-degree order
    facs = [(f, slots_of(f)) for f in factors]
    todo = set(int_slots)
    while todo:
        best = None
        for s in sorted(todo):
            inv = [i for i, (_, ss) in enumerate(facs) if s in ss]
            u = set()
            for i in inv:
                u |= facs[i][1]
            key = (len(u), len(inv), s)
            if best is None or key < best[0]:
                best = (key, s, inv)
        _, s, inv = best
        todo.discard(s)
        if not inv:
            continue
        group = [facs[i][0] for i in inv]
        facs = [facs[i] for i in range(len(facs)) if i not in inv]
        group.sort(key=lambda f: len(f[0]))
        acc = group[0]
        for f in group[1:-1]:
            acc = pmul(acc, f)
        if len(group) >= 2:
            acc = pmul_integrate(acc, group[-1], s)
        else:
            acc = pintegrate(acc, s)
        if not acc[0]:
            return ({}, 1)
        facs.append((acc, slots_of(acc)))
    res = pconst(R1)
    for f, _ in facs:
        res = pmul(res, f)
    return res


# 2x2 matrices of polys
PONE = ({0: 1}, 1)
PZERO = ({}, 1)


def mat_link(slot, inverse):
    a = ({sym(slot, 0): 1}, 1)
    ab = ({sym(slot, 1): 1}, 1)
    b = ({sym(slot, 2): 1}, 1)
    bb = ({sym(slot, 3): 1}, 1)
    nb = ({sym(slot, 2): -1}, 1)
    nbb = ({sym(slot, 3): -1}, 1)
    if not inverse:
        return [[a, nbb], [b, ab]]
    return [[ab, bb], [nb, a]]


MID = [[PONE, PZERO], [PZERO, PONE]]


def mat_mul(x, y):
    return [[padd(pmul(x[i][0], y[0][j]), pmul(x[i][1], y[1][j])) for j in range(2)] for i in range(2)]


def mat_tr(x):
    return padd(x[0][0], x[1][1])


# ------------------------------------------------------------------ the lattice in plain fine coordinates of Z^d

D = int(sys.argv[1]) if len(sys.argv) > 1 else 4
TOP = int(sys.argv[2]) if len(sys.argv) > 2 else 10
OPTION = sys.argv[3] if len(sys.argv) > 3 else ""
LEMMA_A = OPTION == "lemma_a"
# the position of each coarse line that holds V: 0 in the gauge (V, 1), 1 in the control gauge (1, V)
VPOS = 1 if OPTION == "gauge_1V" else 0
PLANTS = ("plant_no_multinomial", "plant_moment_for_cumulant", "plant_support_twice", "plant_recursion_sign")
if OPTION not in ("", "lemma_a", "gauge_1V") + PLANTS:
    raise SystemExit("unknown option")


def e(mu):
    return tuple(1 if i == mu else 0 for i in range(D))


def vadd(x, y):
    return tuple(x[i] + y[i] for i in range(D))


def vsub(x, y):
    return tuple(x[i] - y[i] for i in range(D))


def plaq_links(p):
    x, mu, nu = p
    return [((x, mu), 1), ((vadd(x, e(mu)), nu), 1), ((vadd(x, e(nu)), mu), -1), ((x, nu), -1)]


def is_line(l):
    x, mu = l
    return all(x[i] % 2 == 0 for i in range(D) if i != mu)


def line_info(l):
    x, mu = l
    pos = x[mu] % 2
    base = tuple((x[i] - (pos if i == mu else 0)) // 2 for i in range(D))
    return (base, mu), pos


OFFC = {}


def off_links(p):
    r = OFFC.get(p)
    if r is None:
        r = tuple(l for l, _ in plaq_links(p) if not is_line(l))
        OFFC[p] = r
    return r


def link_plaqs(l):
    x, mu = l
    out = []
    for nu in range(D):
        if nu == mu:
            continue
        if mu < nu:
            out.append((x, mu, nu))
            out.append((vsub(x, e(nu)), mu, nu))
        else:
            out.append((x, nu, mu))
            out.append((vsub(x, e(nu)), nu, mu))
    return out


def in_tree(ck):
    base, mu = ck
    return all(base[i] == 0 for i in range(mu + 1, D))


ZERO = tuple(0 for _ in range(D))
G1 = (e(1), 0)  # coarse link (e1, e0), off the comb tree: g
G2 = (e(2), 0)  # coarse link (e2, e0): g2, for the chair
CSLOT = {G1: 0, G2: 1}


def cslot(ck):
    s = CSLOT.get(ck)
    if s is None:
        s = len(CSLOT)
        CSLOT[ck] = s
    return s


OFF_BASE = 600  # local off-link slots start here; coarse slots stay below

# ------------------------------------------------------------------ supports: closed, connected through off links, holding a seed


def n_odd(x):
    return sum(1 for i in range(D) if x[i] % 2 != 0)


def search(seeds, maxsize):
    seen = set()
    closed = set()
    stack = [frozenset([s]) for s in seeds]
    while stack:
        t = stack.pop()
        if t in seen:
            continue
        seen.add(t)
        cnt = {}
        for p in t:
            for l in off_links(p):
                cnt[l] = cnt.get(l, 0) + 1
        dang = [l for l, c in cnt.items() if c == 1]
        if not dang:
            closed.add(t)
            if len(t) < maxsize:
                for l in cnt:
                    for q in link_plaqs(l):
                        if q not in t:
                            stack.append(t | {q})
            continue
        if len(t) >= maxsize:
            continue
        if 4 * (maxsize - len(t)) < len(dang):
            continue
        l0 = min(dang)
        for q in link_plaqs(l0):
            if q not in t:
                stack.append(t | {q})
    return closed, len(seen)


def extent(s):
    pts = []
    for p in s:
        x, mu, nu = p
        pts.append(x)
        pts.append(vadd(vadd(x, e(mu)), e(nu)))
    return max(max(q[i] for q in pts) - min(q[i] for q in pts) for i in range(D))


# ------------------------------------------------------------------ one core: E_V[prod a_p^k_p] over its off links, a poly in coarse slots

CORE_POLY = {}
INTEG_STATS = {"cores": 0, "slots": 0}


def core_poly(core):
    # core: tuple of (plaq, mult), closed and connected through off links
    r = CORE_POLY.get(core)
    if r is not None:
        return r
    mult = dict(core)
    plaqs = [p for p, _ in core]
    offs = []
    for p in plaqs:
        for l in off_links(p):
            if l not in offs:
                offs.append(l)
    weight = {l: sum(m for p, m in core if l in off_links(p)) for l in offs}
    # gauge fixing at fine sites with >= 2 odd coordinates (they touch no line link)
    ends = {}
    for l in offs:
        x, mu = l
        y = vadd(x, e(mu))
        ends.setdefault(x, []).append(l)
        ends.setdefault(y, []).append(l)
    visited = set(v for v in ends if n_odd(v) < 2)
    fixed = set()
    free_left = set(v for v in ends if n_odd(v) >= 2)
    while free_left:
        cand = None
        for v in sorted(free_left):
            for l in ends[v]:
                x, mu = l
                y = vadd(x, e(mu))
                other = y if x == v else x
                if other in visited:
                    key = (-weight[l], v, l)
                    if cand is None or key < cand[0]:
                        cand = (key, v, l)
        if cand is None:
            v = min(free_left)
            visited.add(v)
            free_left.discard(v)
            continue
        _, v, l = cand
        fixed.add(l)
        visited.add(v)
        free_left.discard(v)
    lslot = {}
    for l in offs:
        if l not in fixed:
            lslot[l] = OFF_BASE + len(lslot)
    facs = []
    for p in plaqs:
        m = None
        for l, sg in plaq_links(p):
            if is_line(l):
                ck, pos = line_info(l)
                if pos != VPOS or in_tree(ck):
                    mm = MID
                else:
                    mm = mat_link(cslot(ck), sg < 0)
            elif l in fixed:
                mm = MID
            else:
                mm = mat_link(lslot[l], sg < 0)
            m = mm if m is None else mat_mul(m, mm)
        a = pscale(mat_tr(m), (1, 2))
        k = mult[p]
        f = a
        for _ in range(k - 1):
            f = pmul(f, a)
        facs.append(f)
    res = eliminate(facs, list(lslot.values()))
    INTEG_STATS["cores"] += 1
    INTEG_STATS["slots"] += len(lslot)
    CORE_POLY[core] = res
    return res


# ------------------------------------------------------------------ the Haar moments of one plaquette with a free off link


def haar_moment(k):
    a = pscale(padd(({sym(OFF_BASE, 0): 1}, 1), ({sym(OFF_BASE, 1): 1}, 1)), (1, 2))
    f = pconst(R1)
    for _ in range(k):
        f = pmul(f, a)
    r = pintegrate(f, OFF_BASE)
    if not r[0]:
        return RZ
    return rq(r[0].get(0, 0), r[1])


HAAR = [haar_moment(k) for k in range(TOP + 1)]

# ------------------------------------------------------------------ formal moments and cumulants

CORE_ID = {}
CORES = []


def core_id(core):
    i = CORE_ID.get(core)
    if i is None:
        i = len(CORES)
        CORE_ID[core] = i
        CORES.append(core)
    return i


MU = {}


def mu(k):
    # k: tuple of (plaq, mult) sorted, mult >= 1. Returns {} or {cores_tuple: rational}
    r = MU.get(k)
    if r is not None:
        return r
    cur = dict(k)
    coef = R1
    while True:
        cnt = {}
        for p in cur:
            for l in off_links(p):
                cnt[l] = cnt.get(l, 0) + 1
        hit = None
        for p in sorted(cur):
            if any(cnt[l] == 1 for l in off_links(p)):
                hit = p
                break
        if hit is None:
            break
        h = HAAR[cur[hit]]
        if h[0] == 0:
            MU[k] = {}
            return MU[k]
        coef = rmul(coef, h)
        del cur[hit]
    # components through off links
    left = set(cur)
    comps = []
    while left:
        p0 = min(left)
        comp = {p0}
        stack = [p0]
        left.discard(p0)
        while stack:
            p = stack.pop()
            for l in off_links(p):
                for q in link_plaqs(l):
                    if q in left:
                        left.discard(q)
                        comp.add(q)
                        stack.append(q)
        comps.append(tuple(sorted((p, cur[p]) for p in comp)))
    ids = tuple(sorted(core_id(c) for c in comps))
    MU[k] = {ids: coef}
    return MU[k]


def fadd(x, y):
    out = dict(x)
    for k, v in y.items():
        w = radd(out.get(k, RZ), v)
        if w[0] == 0:
            out.pop(k, None)
        else:
            out[k] = w
    return out


def fmul(x, y, c=R1):
    out = {}
    for k1, v1 in x.items():
        for k2, v2 in y.items():
            k = tuple(sorted(k1 + k2))
            w = radd(out.get(k, RZ), rmul(rmul(v1, v2), c))
            if w[0] == 0:
                out.pop(k, None)
            else:
                out[k] = w
    return out


def fneg(x):
    return {k: (-v[0], v[1]) for k, v in x.items()}


def binom(n, k):
    if k < 0 or k > n:
        return 0
    return FACT[n] // (FACT[k] * FACT[n - k])


KAPPA = {}


def submultisets(m):
    items = list(m)
    out = [()]
    for p, c in items:
        nxt = []
        for t in out:
            for j in range(c + 1):
                nxt.append(t + (((p, j),) if j else ()))
        out = nxt
    return out


def kappa(m):
    r = KAPPA.get(m)
    if r is not None:
        return r
    x = m[0][0]
    md = dict(m)
    res = dict(mu(m))
    for k in submultisets(m):
        kd = dict(k)
        if kd.get(x, 0) == 0 or k == m:
            continue
        rest = tuple((p, md[p] - kd.get(p, 0)) for p in sorted(md) if md[p] - kd.get(p, 0) > 0)
        mr = mu(rest)
        if not mr:
            continue
        c = 1
        for p in md:
            if p == x:
                c *= binom(md[p] - 1, kd[p] - 1)
            else:
                c *= binom(md[p], kd.get(p, 0))
        kk = kappa(k)
        if not kk:
            continue
        if OPTION == "plant_recursion_sign":
            res = fadd(res, fmul(kk, mr, (c, 1)))
        else:
            res = fadd(res, fneg(fmul(kk, mr, (c, 1))))
    KAPPA[m] = res
    return res


# ------------------------------------------------------------------ readouts

PROJ_P0 = {}
PROJ_CHAIR = {}


def product_poly(ids):
    f = pconst(R1)
    for i in ids:
        f = pmul(f, core_poly(CORES[i]))
    return f


def proj_p0(ids):
    # characters chi_j(g), j = n/2, of the product integrated over every coarse slot but g's
    r = PROJ_P0.get(ids)
    if r is not None:
        return r
    f = product_poly(ids)
    others = [s for s in slots_of(f) if s != 0]
    f = eliminate([f], others)
    lau = {}
    for m, c in f[0].items():
        ea, eab, eb, ebb = slot_exps(m, 0)
        if (m >> SLOTB) != 0:
            raise SystemExit("stray coarse slot after integration")
        if eb or ebb:
            continue
        lau[ea - eab] = lau.get(ea - eab, 0) + c
    for n in list(lau):
        if lau.get(n, 0) != lau.get(-n, 0):
            raise SystemExit("not a class function of g")
    out = {}
    hi = max([abs(n) for n in lau] + [0])
    for n in range(0, hi + 1):
        # [z^(n+1)] of (z - 1/z) f(z) is the coefficient of chi_(n/2)
        c = lau.get(n, 0) - lau.get(n + 2, 0)
        if c != 0:
            out[n] = rq(c, f[1])
    PROJ_P0[ids] = out
    return out


def chair_funcs():
    # V_P0 and V_Q0 as words in the coarse links, the comb tree at 1; chair = x' -> +nu -> +mu -> -nu -> +lambda -> -mu -> -lambda
    def cval(ck, inverse):
        if in_tree(ck):
            return MID
        return mat_link(cslot(ck), inverse)

    mu_, nu_, la_ = 0, 1, 2
    o = ZERO
    steps = [
        ((o, nu_), False),
        ((e(nu_), mu_), False),
        ((e(mu_), nu_), True),
        ((e(mu_), la_), False),
        ((e(la_), mu_), True),
        ((o, la_), True),
    ]
    m = MID
    for ck, inv in steps:
        m = mat_mul(m, cval(ck, inv))
    chair = mat_tr(m)
    p = MID
    for ck, inv in [((o, mu_), False), ((e(mu_), nu_), False), ((e(nu_), mu_), True), ((o, nu_), True)]:
        p = mat_mul(p, cval(ck, inv))
    q = MID
    for ck, inv in [((o, mu_), False), ((e(mu_), la_), False), ((e(la_), mu_), True), ((o, la_), True)]:
        q = mat_mul(q, cval(ck, inv))
    n1 = padd(pmul(mat_tr(p), mat_tr(q)), pscale(chair, (-1, 2)))
    return chair, n1, mat_tr(p), mat_tr(q)


CHAIR_F, N1_F, TRP_F, TRQ_F = chair_funcs()


def full_int(f):
    g = eliminate([f], list(slots_of(f)))
    if not g[0]:
        return RZ
    return rq(g[0].get(0, 0), g[1])


def proj_chair(ids):
    r = PROJ_CHAIR.get(ids)
    if r is not None:
        return r
    f = product_poly(ids)
    out = (full_int(pmul(f, CHAIR_F)), rmul(full_int(pmul(f, N1_F)), (4, 3)))
    PROJ_CHAIR[ids] = out
    return out


# ------------------------------------------------------------------ multiplicity vectors on a support


def mult_vectors(s, top):
    s = sorted(s)
    out = []
    links = {}
    for i, p in enumerate(s):
        for l in off_links(p):
            links.setdefault(l, []).append(i)
    lists = list(links.values())

    def rec(i, left, cur):
        if i == len(s):
            for ix in lists:
                if sum(cur[j] for j in ix) % 2 != 0:
                    return
            out.append(tuple(zip(s, cur)))
            return
        for extra in range(left + 1):
            rec(i + 1, left - extra, cur + [1 + extra])

    if len(s) <= top:
        rec(0, top - len(s), [])
    return out


def mfact(m):
    r = 1
    for _, c in m:
        r *= FACT[c]
    return r


# ------------------------------------------------------------------ the disjoint pair, for G2


def filling(base):
    x = tuple(2 * c for c in base)
    out = []
    for i in (0, 1):
        for j in (0, 1):
            out.append((vadd(vadd(x, tuple(i * v for v in e(0))), tuple(j * v for v in e(1))), 0, 1))
    return out


def coarse_loop(base):
    # chi_1/2 of the coarse plaquette (base; 0, 1), the comb tree at 1
    o = base
    steps = [((o, 0), False), ((vadd(o, e(0)), 1), False), ((vadd(o, e(1)), 0), True), ((o, 1), True)]
    mm = MID
    for ck, inv in steps:
        mm = mat_mul(mm, MID if in_tree(ck) else mat_link(cslot(ck), inv))
    return mat_tr(mm)


def g2_pair():
    far = tuple(1 if i == D - 1 else 0 for i in range(D))
    m = tuple(sorted((p, 1) for p in filling(ZERO) + filling(far)))
    fpair = pmul(coarse_loop(ZERO), coarse_loop(far))
    proj = RZ
    for ids, cf in mu(m).items():
        proj = radd(proj, rmul(cf, full_int(pmul(product_poly(ids), fpair))))
    return proj, len(kappa(m))


# ------------------------------------------------------------------ frozen rows: the first 26 lines of the prediction


def frozen_rows(path):
    rows = {}
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().split("\n")[:26]
    except OSError:
        return rows
    for line in lines:
        for part in line.split("|"):
            if part.startswith("id="):
                rows[part[3:]] = line
    return rows


# ------------------------------------------------------------------ run


def main():
    def say(s):
        sys.stdout.write(s + "\n")
        sys.stdout.flush()

    say("ROUTE_C|d=%d|top=beta^%d|option=%s|lemma_a_filter=%d|gauge=%s|coarse_tree=comb|integrator=complex_coordinate_moments|json=0"
        % (D, TOP, OPTION or "none", 1 if LEMMA_A else 0, "(1,V)" if VPOS else "(V,1)"))
    ctrl = []
    for m in (2, 4, 6, 12):
        h = HAAR[m] if m <= TOP else haar_moment(m)
        ctrl.append("%d:%s" % (m, rshow(rmul(h, (1 << m, 1)))))
    say("ROUTE_C_HAAR|E[chi_1/2^m]_SU2=" + ",".join(ctrl) + "|json=0")
    ex = tuple(VPOS * v for v in e(0))
    gline = (vadd(vadd(e(1), e(1)), ex), 0)  # the line link of the coarse link (e1, 0) that holds g
    gother = (vadd(vadd(e(1), e(1)), tuple((1 - VPOS) * v for v in e(0))), 0)
    g2line = (vadd(vadd(e(2), e(2)), ex), 0)
    seeds = link_plaqs(gline)
    closed, states = search(seeds, TOP)
    by_size = {}
    for s in closed:
        by_size[len(s)] = by_size.get(len(s), 0) + 1
    maxext = max(extent(s) for s in closed)
    say("ROUTE_C_SUPPORTS|seeds=plaquettes_at_the_V_position_of_(e1,0)=%d|max_size=%d|search_states=%d|closed_placed=%d|by_size=%s|max_fine_extent=%d|json=0"
        % (len(seeds), TOP, states, len(closed), ",".join("%d:%d" % (k, by_size[k]) for k in sorted(by_size)), maxext))
    p0 = {}
    chair = {}
    n1 = {}
    nsup = 0
    nm = 0
    odd_nonzero = 0
    parts = {}
    order_list = sorted(closed, key=lambda t: (len(t), sorted(t)))
    if OPTION == "plant_support_twice":
        # the first support of 8 plaquettes holding both positions of (e1, 0), read twice
        first8 = [s for s in order_list if len(s) == 8 and any(l == gother for p in s for l, _ in plaq_links(p))][:1]
        order_list = order_list + first8
    for s in order_list:
        holds_other = any(l == gother for p in s for l, _ in plaq_links(p))
        if LEMMA_A and not holds_other:
            continue
        holds_g2 = any(l == g2line for p in s for l, _ in plaq_links(p))
        nsup += 1
        for m in mult_vectors(s, TOP):
            nm += 1
            order = sum(c for _, c in m)
            kk = mu(m) if OPTION == "plant_moment_for_cumulant" else kappa(m)
            if not kk:
                continue
            den = 1 if OPTION == "plant_no_multinomial" else mfact(m)
            for ids, cf in kk.items():
                w = rmul(cf, (1, den))
                for n, v in proj_p0(ids).items():
                    if n == 0:
                        continue
                    t = rmul(w, v)
                    if t[0] != 0:
                        key = (order, n)
                        p0[key] = radd(p0.get(key, RZ), t)
                        if order % 2 == 1:
                            odd_nonzero += 1
                        if n == 1 and order >= 8:
                            pk = (order, len(s), "".join(str(c) for _, c in m if c > 1) or "1")
                            parts[pk] = radd(parts.get(pk, RZ), t)
                if holds_g2:
                    cc, nn = proj_chair(ids)
                    if cc[0] != 0:
                        chair[order] = radd(chair.get(order, RZ), rmul(w, cc))
                    if nn[0] != 0:
                        n1[order] = radd(n1.get(order, RZ), rmul(w, nn))
    say("ROUTE_C_WORK|supports_read=%d|multiplicity_vectors=%d|core_integrals=%d|integrated_off_links=%d|odd_order_nonzero_terms=%d|json=0"
        % (nsup, nm, INTEG_STATS["cores"], INTEG_STATS["slots"], odd_nonzero))
    for order in range(1, TOP + 1):
        cells = []
        for n in range(1, 2 * TOP + 2):
            v = p0.get((order, n), RZ)
            if v[0] != 0:
                cells.append("chi_%s:%s" % (("%d/2" % n) if n % 2 else str(n // 2), rshow(v)))
        say("ROUTE_C_P0|d=%d|beta^%d|%s|json=0" % (D, order, ",".join(cells) if cells else "none"))
    for order in range(1, TOP + 1):
        say("ROUTE_C_CHAIR|d=%d|beta^%d|chair=%s|N1=%s|json=0" % (D, order, rshow(chair.get(order, RZ)), rshow(n1.get(order, RZ))))
    for pk in sorted(parts):
        say("ROUTE_C_PART|d=%d|beta^%d|support_size=%d|multiplicities_above_1=%s|chi_1/2(V_P0)=%s|json=0" % (D, pk[0], pk[1], pk[2], rshow(parts[pk])))
    g = p0.get
    reads = []
    if TOP >= 8:
        pair, pair_terms = g2_pair()
        c4 = g((4, 1), RZ)
        rho_one = radd(g((8, 2), RZ), rmul(rmul(c4, c4), (1, 2)))
        say("ROUTE_C_G2|d=%d|family_of_two_disjoint_fillings_moment_on_chi_1/2(V_P0)chi_1/2(V_P1)=%s|its_cumulant_terms=%d|rho_over_int_rho_b8_chi_1(V_P)=c8_chi_1+c4^2/2=%s|self_cluster_on_chi_1=-c4^2/2=%s|json=0"
            % (D, rshow(pair), pair_terms, rshow(rho_one), rshow(rmul(rmul(c4, c4), (-1, 2)))))
        reads.append(("G2", "rho_b8_disjoint_pair_by_integration", rshow(pair), "1/16384", "2^-14"))
        reads.append(("G2", "log_rho_b8_disjoint_pair_cumulant_terms", str(pair_terms), "0", ""))
        reads.append(("G2", "rho_b8_chi_1(V_P)", rshow(rho_one), "1/110592", "1/110592"))
        reads.append(("G2", "self_cluster_b8_chi_1", rshow(rmul(rmul(c4, c4), (-1, 2))), "-1/32768", "-1/32768"))
    low = [k for k in p0 if k[0] < 4]
    reads.append(("P2", "any_chi_j(V_P0)_b1..b3", "0" if not low else "nonzero", "0", ""))
    odd = [k for k in p0 if k[0] % 2 == 1] + [k for k in chair if k % 2 == 1] + [k for k in n1 if k % 2 == 1]
    reads.append(("P3", "odd_orders_through_b%d" % TOP, "0" if not odd else "nonzero", "0", ""))
    reads.append(("P1", "b4_chi_1/2(V_P)", rshow(g((4, 1), RZ)), "1/128", "1/128"))
    if TOP >= 6:
        reads.append(("P4", "b6_chi_1/2(V_P)", rshow(g((6, 1), RZ)), "-1/768", "-1/768"))
        other6 = [k for k in p0 if k[0] == 6 and k[1] != 1] + [k for k in chair if k == 6] + [k for k in n1 if k == 6]
        reads.append(("P4", "b6_other_functionals_read", "none" if not other6 else "some", "none", ""))
    if TOP >= 8:
        v8 = "1/1536" if D == 4 else "5/12288"
        reads.append(("P5", "b8_chi_1/2(V_P)", rshow(g((8, 1), RZ)), v8, v8))
        reads.append(("P5", "b8_chi_1(V_P)", rshow(g((8, 2), RZ)), "-19/884736", "-19/884736"))
        other8 = [k for k in p0 if k[0] == 8 and k[1] > 2] + [k for k in chair if k == 8] + [k for k in n1 if k == 8]
        reads.append(("P5", "b8_other_functionals_read", "none" if not other8 else "some", "none", ""))
    below = [k for k in chair if k < 10]
    reads.append(("P6", "chair_below_b10", "0" if not below else "nonzero", "0", ""))
    if TOP >= 10:
        v10 = "-467/2211840" if D == 4 else "-1013/8847360"
        reads.append(("P6", "b10_chi_1/2(V_chair)", rshow(chair.get(10, RZ)), "3/524288", "3/524288"))
        reads.append(("P11", "b10_chi_1/2(V_P)", rshow(g((10, 1), RZ)), v10, v10))
        reads.append(("P12", "b10_chi_1(V_P)", rshow(g((10, 2), RZ)), "7/884736", "7/884736"))
    hi = [k for k in p0 if k[1] >= 3]
    reads.append(("P13", "spin_3/2_and_above_on_V_P_through_b%d" % TOP, "0" if not hi else "nonzero", "0", ""))
    reads.append(("P13", "N1_through_b%d" % TOP, "0" if not n1 else "nonzero", "0", ""))
    reads.append(("P10a", "max_fine_extent_below_the_fine_side_6", "fit" if maxext < 6 else "wraps", "fit", ""))
    rows = frozen_rows("docs/PREDICTION-YM4-03C.hbp")
    met = 0
    miss = 0
    for row, item, read, frozen, literal in reads:
        text = rows.get(row)
        if text is None:
            in_row = "CANNOT_SEE"
        elif literal == "":
            in_row = "1"
        else:
            in_row = "1" if literal in text else "0"
        ok = read == frozen and in_row == "1"
        met += 1 if ok else 0
        miss += 0 if ok else 1
        say("ROUTE_C_READ|d=%d|row=%s|item=%s|read=%s|frozen=%s|literal_in_frozen_row=%s|result=%s|json=0" % (D, row, item, read, frozen, in_row, "MET" if ok else "MISS"))
    say("ROUTE_C_DONE|d=%d|reads=%d|met=%d|miss=%d|json=0" % (D, met + miss, met, miss))
    return 1 if miss else 0


sys.exit(main())
