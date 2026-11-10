#!/usr/bin/env python3
"""Independent refuter for YM4-06A: algebra counts, 2-torus brute force, receipt witnesses re-evaluated,
flux gate, Bianchi degree check on searched solutions, exact SU(2). Own code; integers only; no fractions.
usage: refute_aux.py RECEIPT_PATH
"""
import itertools
import sys

import refute_s3 as R

MUL, INV, E_, COST, KIND, PERMS, IDX = R.MUL, R.INV, R.E_, R.COST, R.KIND, R.PERMS, R.IDX


def out(s):
    print(s + "|json=0")


# ------------------------------------------------ algebra
def algebra():
    comm = lambda a, b: MUL[a][b] == MUL[b][a]  # noqa: E731
    pairs = [t for t in itertools.product(range(6), repeat=2) if comm(*t)]
    triples = [t for t in itertools.product(range(6), repeat=3)
               if comm(t[0], t[1]) and comm(t[0], t[2]) and comm(t[1], t[2])]

    def norb(ts):
        return len({min(tuple(MUL[MUL[g][a]][INV[g]] for a in t) for g in range(6)) for t in ts})
    # independent second method: classify by subgroup generated (S3 commuting tuples generate a cyclic/abelian subgroup)
    commutators = sorted({MUL[MUL[MUL[a][b]][INV[a]]][INV[b]] for a in range(6) for b in range(6)})
    out("ALG|chi_std=%s|cost=%s|commuting_pairs=%d|pair_orbits=%d|commuting_triples=%d|triple_orbits=%d|commutator_set_kinds=%s"
        % (",".join(map(str, sorted(set(R.CHI), reverse=True))), ",".join(map(str, sorted(set(COST)))), len(pairs), norb(pairs),
           len(triples), norb(triples), ",".join(KIND[c] for c in commutators)))
    return triples


# ------------------------------------------------ 2-torus brute force
def two_torus(Lx, Ly):
    sites = [(x, y) for x in range(Lx) for y in range(Ly)]
    sid = {s: i for i, s in enumerate(sites)}
    lk = lambda s, mu: 2 * sid[s] + mu  # noqa: E731
    sh = lambda s, mu: tuple((s[i] + (1 if i == mu else 0)) % (Lx, Ly)[i] for i in range(2))  # noqa: E731
    faces = [((lk(s, 0), 1), (lk(sh(s, 0), 1), 1), (lk(sh(s, 1), 0), -1), (lk(s, 1), -1)) for s in sites]
    # comb tree: y-links at x... use x-links on every row y<... : U1(x,y) for y<Ly-1, U0(x,0) for x<Lx-1
    tree = {lk((x, y), 1) for x in range(Lx) for y in range(Ly - 1)} | {lk((x, 0), 0) for x in range(Lx - 1)}
    free = [l for l in range(2 * len(sites)) if l not in tree]
    vals = [E_] * (2 * len(sites))
    flat, minE, mins = [], None, 0
    total = 0
    for assign in itertools.product(range(6), repeat=len(free)):
        total += 1
        for l, v in zip(free, assign):
            vals[l] = v
        en = 0
        for f in faces:
            h = E_
            for l, sg in f:
                h = MUL[h][vals[l] if sg == 1 else INV[vals[l]]]
            en += COST[h]
        if en == 0:
            flat.append(tuple(vals))
        elif minE is None or en < minE:
            minE, mins = en, 1
        elif en == minE:
            mins += 1
    orb = len({min(tuple(MUL[MUL[g][a]][INV[g]] for a in s) for g in range(6)) for s in flat})
    out("TWO_TORUS_REFUTER|lattice=%dx%d|tree_fixed_configurations=%d|flat=%d|flat_orbits=%d|kappa_2D=%d|minimizers=%d"
        % (Lx, Ly, total, len(flat), orb, minE, mins))


# ------------------------------------------------ receipt witnesses
def parse_links(lat, text):
    vals = [E_] * lat.nl
    for item in text.split(";"):
        lhs, rhs = item.split("=")
        mu = int(lhs[1])
        s = tuple(int(c) for c in lhs[lhs.index("(") + 1:lhs.index(")")])
        vals[lat.lk(s, mu)] = IDX[tuple(int(c) for c in rhs)]
    return vals


def nonflat_list(lat, vals):
    res = []
    for f, (s, mu, nu, _) in enumerate(lat.faces):
        h = lat.hol(vals, f)
        if h != E_:
            res.append("P%d%d(%s)=%s" % (mu, nu, "".join(map(str, s)), KIND[h]))
    return res


def witnesses(path):
    rows = open(path, "rb").read().decode("utf-8").splitlines()
    for row in rows:
        kv = dict(p.split("=", 1) for p in row.split("|")[1:] if "=" in p)
        tag = row.split("|")[0]
        if tag not in ("S3_KAPPA_WITNESS", "S3_FOUR_FACE", "S3_TUBE", "FLUX_GATE"):
            continue
        dims = tuple(int(c) for c in kv["lattice"].split("x"))
        lat = R.Lat(dims)
        links = kv["witness"] if tag == "FLUX_GATE" else kv["links"]
        vals = parse_links(lat, links)
        en = lat.energy(vals)
        nf = nonflat_list(lat, vals)
        claimed = kv.get("E", "")
        if tag == "S3_TUBE":
            claimed = kv["E"].split("=")[-1]
        if tag == "FLUX_GATE":
            claimed = "6"
        ok = str(en) == claimed
        extra = ""
        if tag in ("S3_KAPPA_WITNESS", "S3_FOUR_FACE"):
            ok = ok and ";".join(nf) == kv["nonflat_faces"]
        if tag == "S3_TUBE":
            L = int(kv["L"])
            ok = ok and len(nf) == L and all(x.endswith("3-cycle") for x in nf) and en == 3 * L
            extra = "|axis=%s|L=%d" % (kv["axis"], L)
        deg_ok = cube_degree_ok(lat, vals)
        out("WITNESS_REEVAL|row=%s|lattice=%s%s|E_mine=%d|E_claimed=%s|nonflat=%s|no_cube_with_exactly_one_nonflat=%d|agree=%d"
            % (tag, kv["lattice"], extra, en, claimed, ",".join(nf), deg_ok, ok))


def cube_faces(lat):
    res = []
    fid = {(f[0], f[1], f[2]): i for i, f in enumerate(lat.faces)}
    for s in lat.sites:
        fs = [fid[(s, 0, 1)], fid[(s, 0, 2)], fid[(s, 1, 2)],
              fid[(lat.sh(s, 2), 0, 1)], fid[(lat.sh(s, 1), 0, 2)], fid[(lat.sh(s, 0), 1, 2)]]
        res.append(fs)
    return res


def cube_degree_ok(lat, vals):
    nf = {f for f in range(len(lat.faces)) if lat.hol(vals, f) != E_}
    return int(all(len(nf & set(cf)) != 1 for cf in cube_faces(lat)))


# ------------------------------------------------ flux gate (local check with trivial transport + realization)
def flux_gate():
    lat = R.Lat((2, 2, 2))
    fid = {(f[0], f[1], f[2]): i for i, f in enumerate(lat.faces)}
    stack = [fid[((0, 0, 0), 0, 1)], fid[((0, 0, 1), 0, 1)]]
    t01 = IDX[(1, 0, 2)]
    c3 = IDX[(1, 2, 0)]

    def local_ok(flux):
        # trivial transport: each cube, product F01(x)^-1 F12(x+0) F02(x) F01(x+2) F12(x)^-1 F02(x+1)^-1
        for s in lat.sites:
            seq = [(fid[(s, 0, 1)], -1), (fid[(lat.sh(s, 0), 1, 2)], 1), (fid[(s, 0, 2)], 1),
                   (fid[(lat.sh(s, 2), 0, 1)], 1), (fid[(s, 1, 2)], -1), (fid[(lat.sh(s, 1), 0, 2)], -1)]
            h = E_
            for f, sg in seq:
                v = flux.get(f, E_)
                h = MUL[h][v if sg == 1 else INV[v]]
            if h != E_:
                return 0
        return 1
    # realization: complete DFS over the whole lattice with budget 7 (from refute_s3) lists every config with E <= 7;
    # an exact transposition stack would have E = 4 and so must appear if it exists.
    sols, nodes, _ = R.search(lat, 7)
    target_t = [s for s in sols if all(lat.hol(s, f) == t01 for f in stack)
                and all(lat.hol(s, f) == E_ for f in range(len(lat.faces)) if f not in stack)]
    any_transposition = [s for s in sols if any(KIND[lat.hol(s, f)] == "transposition" for f in range(len(lat.faces)))]
    target_c = [s for s in sols if all(lat.hol(s, f) == c3 for f in stack)
                and all(lat.hol(s, f) == E_ for f in range(len(lat.faces)) if f not in stack)]
    deg = all(cube_degree_ok(lat, s) for s in sols)
    out("FLUX_GATE_REFUTER|lattice=2x2x2|stack=P01(000),P01(001)|transposition_local_trivial_transport=%d|transposition_realizations=%d|any_config_E<=7_with_a_transposition_face=%d|3cycle_120_local=%d|3cycle_120_realizations=%d|all_E<=7_solutions_no_cube_with_one_nonflat=%d"
        % (local_ok({f: t01 for f in stack}), len(target_t), len(any_transposition), local_ok({f: c3 for f in stack}), len(target_c), deg))


# ------------------------------------------------ exact rationals and quaternions (integer pairs)
def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def Q(n, d=1):
    if d < 0:
        n, d = -n, -d
    g = gcd(n, d) or 1
    return (n // g, d // g)


def qa(x, y):
    return Q(x[0] * y[1] + y[0] * x[1], x[1] * y[1])


def qs(x, y):
    return Q(x[0] * y[1] - y[0] * x[1], x[1] * y[1])


def qm(x, y):
    return Q(x[0] * y[0], x[1] * y[1])


def qd(x, y):
    return Q(x[0] * y[1], x[1] * y[0])


ZERO, ONE = (0, 1), (1, 1)


def hm(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    a = qs(qs(qs(qm(a1, a2), qm(b1, b2)), qm(c1, c2)), qm(d1, d2))
    b = qs(qa(qa(qm(a1, b2), qm(b1, a2)), qm(c1, d2)), qm(d1, c2))
    c = qa(qa(qs(qm(a1, c2), qm(b1, d2)), qm(c1, a2)), qm(d1, b2))
    d = qa(qs(qa(qm(a1, d2), qm(b1, c2)), qm(c1, b2)), qm(d1, a2))
    return (a, b, c, d)


def hnorm(p):
    s = ZERO
    for x in p:
        s = qa(s, qm(x, x))
    return s


def hinv(p):
    n = hnorm(p)
    return (qd(p[0], n),) + tuple(qd(Q(-x[0], x[1]), n) for x in p[1:])


H1 = (ONE, ZERO, ZERO, ZERO)
HM1 = ((-1, 1), ZERO, ZERO, ZERO)
HI = (ZERO, ONE, ZERO, ZERO)
HJ = (ZERO, ZERO, ONE, ZERO)


def rot(n, axis):
    d = n * n + 1
    q = [ZERO, ZERO, ZERO, ZERO]
    q[0] = Q(n * n - 1, d)
    q[axis] = Q(2 * n, d)
    return tuple(q)


def hcomm(a, b):
    return hm(hm(hm(a, b), hinv(a)), hinv(b))


class QLat:
    def __init__(self, dims):
        self.dims = dims
        self.d = len(dims)
        self.sites = list(itertools.product(*[range(n) for n in dims]))
        self.sid = {s: i for i, s in enumerate(self.sites)}
        self.planes = [(m, n) for m in range(self.d) for n in range(m + 1, self.d)]

    def sh(self, s, mu):
        t = list(s)
        t[mu] = (t[mu] + 1) % self.dims[mu]
        return tuple(t)

    def lk(self, s, mu):
        return self.d * self.sid[s] + mu

    def plaqs(self, U):
        res = []
        for s in self.sites:
            for mu, nu in self.planes:
                p = hm(hm(hm(U[self.lk(s, mu)], U[self.lk(self.sh(s, mu), nu)]), hinv(U[self.lk(self.sh(s, nu), mu)])),
                       hinv(U[self.lk(s, nu)]))
                res.append(((s, mu, nu), p))
        return res


def cost_sum(plist, weight_full_trace=True):
    # weight_full_trace: sum (2 - Tr) with Tr = 2*Re ; else sum (1 - Re) (Wilson, beta = 1)
    s = ZERO
    for _, p in plist:
        s = qa(s, qs((2, 1), qm((2, 1), p[0])) if weight_full_trace else qs(ONE, p[0]))
    return s


def fr(x):
    return "%d/%d" % x


def su2():
    # (a) one link on 3x3x3
    lat = QLat((3, 3, 3))
    rows = []
    ok = True
    for n in (2, 3, 10, 100, 1000, 10 ** 6):
        U = [H1] * (len(lat.sites) * 3)
        U[0] = rot(n, 1)
        ps = lat.plaqs(U)
        moved = sum(1 for _, p in ps if p != H1)
        E = cost_sum(ps)
        ok = ok and moved == 4 and E == Q(16, n * n + 1) and hnorm(U[0]) == ONE
        rows.append("%d:%s" % (n, fr(E)))
    out("SU2_SMALL_ACTION_REFUTER|lattice=3x3x3|moved_faces=4|E_by_n=%s|equals_16/(n^2+1)=%d" % (",".join(rows), ok))
    # (b) 2^4 Wilson, beta=1, plus a rational gauge transform
    l4 = QLat((2, 2, 2, 2))
    gq = [Q(1, 5), Q(2, 5), Q(2, 5), Q(4, 5)]
    g1 = tuple(gq)
    g2 = (Q(3, 5), Q(4, 5), ZERO, ZERO)
    rows, ok = [], True
    for n in (2, 10, 1000):
        U = [H1] * (len(l4.sites) * 4)
        U[0] = rot(n, 1)
        S = cost_sum(l4.plaqs(U), weight_full_trace=False)
        G = [g1 if sum(s) % 2 == 0 else g2 for s in l4.sites]
        Ut = list(U)
        for s in l4.sites:
            for mu in range(4):
                Ut[l4.lk(s, mu)] = hm(hm(G[l4.sid[s]], U[l4.lk(s, mu)]), hinv(G[l4.sid[l4.sh(s, mu)]]))
        St = cost_sum(l4.plaqs(Ut), weight_full_trace=False)
        ok = ok and S == Q(12, n * n + 1) and St == S
        rows.append("%d:%s" % (n, fr(S)))
    out("SU2_4D_REFUTER|lattice=2^4|S_W_beta1_by_n=%s|equals_12/(n^2+1)=%d|gauge_invariant=%d" % (",".join(rows), ok, ok))
    # (c) winding flux: corner holonomies a_n (x), b_n (y), all slices z
    rows, prev, ok = [], None, True
    for n in (2, 10, 1000):
        a, b = rot(n, 1), rot(n, 2)
        U = [H1] * (len(lat.sites) * 3)
        for s in lat.sites:
            if s[0] == 2:
                U[lat.lk(s, 0)] = a
            if s[1] == 2:
                U[lat.lk(s, 1)] = b
        ps = lat.plaqs(U)
        moved = [p for _, p in ps if p != H1]
        E = cost_sum(ps)
        c = hcomm(a, b)
        ok = ok and len(moved) == 3 and c != H1 and all(m[0] == c[0] for m in moved)
        if prev is not None:
            ok = ok and E[0] * prev[1] < prev[0] * E[1]
        prev = E
        rows.append("%d:%s" % (n, fr(E)))
    out("SU2_WINDING_REFUTER|lattice=3x3x3|faces_per_slice=1|E_by_n=%s|decreasing_and_nonflat=%d" % (",".join(rows), ok))
    # (d) six flat triples in one U(1)
    pts = [((3, 5), (4, 5)), ((4, 5), (3, 5)), ((15, 17), (8, 17)), ((12, 13), (5, 13)), ((24, 25), (7, 25)), ((60, 61), (11, 61))]
    hts, ok = [], True
    for c, s in pts:
        a = (Q(*c), Q(*s), ZERO, ZERO)
        ok = ok and hnorm(a) == ONE
        tri = (a, hm(a, a), H1)
        U = [H1] * (len(lat.sites) * 3)
        for x in lat.sites:
            for mu in range(3):
                if x[mu] == 2:
                    U[lat.lk(x, mu)] = tri[mu]
        ok = ok and all(p == H1 for _, p in lat.plaqs(U))
        hts.append(Q(*c))
    out("SU2_FLAT_REFUTER|triples=6|all_plaquettes_exactly_1=%d|half_traces=%s|distinct=%d" % (ok, ",".join(fr(h) for h in hts), len(set(hts)) == 6))
    # (e) twisted
    ij, ji = hm(HI, HJ), hm(HJ, HI)
    anti = ij == tuple(Q(-x[0], x[1]) for x in ji)
    cij = hcomm(HI, HJ)
    # centralizer of {i, j} in H: q = a + b i + c j + d k ; [q,i]=0 forces c=d=0, [q,j]=0 forces b=d=0 (checked on basis)
    basis = [H1, HI, HJ, (ZERO, ZERO, ZERO, ONE)]
    cent = [k for k, q in enumerate(basis) if hm(q, HI) == hm(HI, q) and hm(q, HJ) == hm(HJ, q)]
    rows = []
    for cc in (H1, HM1):
        tri = (HI, HJ, cc)
        U = [H1] * (len(lat.sites) * 3)
        for x in lat.sites:
            for mu in range(3):
                if x[mu] == 2:
                    U[lat.lk(x, mu)] = tri[mu]
        ps = lat.plaqs(U)
        E = cost_sum(ps)
        bad = [(f, p) for f, p in ps if p != H1]
        twisted_flat = all(p == HM1 and f[1:] == (0, 1) for f, p in bad) and len(bad) == 3
        rows.append("c=%s:E_periodic=%s:twisted_flat=%d" % ("+1" if cc == H1 else "-1", fr(E), twisted_flat))
    out("SU2_TWISTED_REFUTER|ij=-ji=%d|[i,j]=-1=%d|centralizer_basis_dims=%s|%s" % (anti, cij == HM1, ",".join(map(str, cent)), "|".join(rows)))


def main():
    algebra()
    two_torus(2, 2)
    two_torus(2, 3)
    witnesses(sys.argv[1])
    flux_gate()
    for dims in ((2, 2, 2), (2, 3, 3), (3, 3, 3)):
        lat = R.Lat(dims)
        sols, _, _ = R.search(lat, 8)
        out("BIANCHI_DEGREE|lattice=%dx%dx%d|solutions_E<=8=%d|all_no_cube_with_exactly_one_nonflat=%d"
            % (dims + (len(sols), all(cube_degree_ok(lat, s) for s in sols))))
    su2()


if __name__ == "__main__":
    main()
