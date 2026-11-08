#!/usr/bin/env python3
"""
YM4-03C, the prediction commit: small exact derivation checks for the rows of docs/PREDICTION-YM4-03C.hbp.
Integers and integer numerator/denominator pairs only, the standard library only, json=0. The four-dimensional coefficients are the engine's work,
in a later commit; this file reads the facts the prediction rows rest on.

A. McKay powers. N_m(n) = (A^m)_{0,n} on the McKay graph of SU(2), with n = 2j, is the multiplicity of spin n/2 in (1/2)^m. The coefficient of
   chi_n in exp(beta a), a = chi_1/2 / 2, is c_n = sum_m beta^m N_m(n) / (2^m m!), and t_(n+1) = c_n / ((n + 1) c_0). From these: 2 t_2^4 and
   3 t_3^4 - 2 t_2^8, the two-dimensional blocked coefficients, by a route through N_m alone, read against the decide and attack lanes' Bessel routes.
B. Designs. Class sums of chi_n over 2T and 2I in Z[phi], and E[chi_1/2^m] over each group by closed walks on its McKay graph (affine E6, affine E8),
   against the Catalan numbers of SU(2).
C. Surfaces. For the fine boundary of a coarse plaquette, of a chair and of a 1x2 rectangle, every set F xor boundary(C), with F the flat filling
   and C a 3-chain of at most three cubes in a window of Z^4, by size, with its connection through off links, its edge valences, Euler
   characteristic, orientation, and the positions of each coarse link it touches. The defect-repair walk of tests/test_one_scale_blocking.py,
   restricted to the same window, reads the same boundaries as a second method: every set it reaches lies among the chains, the two hold the same
   disks, and on the chair and the rectangle the same sets connected through off links. The walk adds plaquettes on the lowest odd edge only, so a
   cube joined to the filling along one edge is reached in some orders and missed in others. Two earlier runs stay beside this file:
   FIRST-RUN.hbp compared every set with each edge component on the boundary, and read 40 against 96 at size 10, since the walk reaches 8 of the
   64 sets a cube joins along one line link; SECOND-RUN.hbp compared all sets connected through off links, and read 41 against 49 on the plaquette,
   with the 8 it misses among the 16 a cube joins along one off link.
D. The arithmetic of the prediction rows, on the series of part A.
E. Orbits of coarse shapes under the 384 signed permutations with coarse translations.

Run as python3 -I -B -X utf8 derive_checks.py. Its output is DERIVE-CHECKS.hbp beside it, byte for byte.
"""
import itertools
import sys
from math import comb, factorial, gcd

CHECKS = [0]
FAILED = [0]


def say(text):
    sys.stdout.write(text + "\n")


def check(name, ok, detail=""):
    CHECKS[0] += 1
    if not ok:
        FAILED[0] += 1
        say("FAILED|check=" + name + "|" + detail + "|json=0")


# ---- exact rationals as (numerator, denominator) with denominator > 0

def q(n, d=1):
    if d < 0:
        n, d = -n, -d
    g = gcd(n, d) or 1
    return (n // g, d // g)


def qadd(a, b):
    return q(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def qsub(a, b):
    return q(a[0] * b[1] - b[0] * a[1], a[1] * b[1])


def qmul(a, b):
    return q(a[0] * b[0], a[1] * b[1])


def qs(a):
    return str(a[0]) + "/" + str(a[1])


ZERO, ONE = (0, 1), (1, 1)
TOP = 16  # series in beta are kept through beta^TOP


def smul(p, r):
    out = [ZERO] * (TOP + 1)
    for i in range(TOP + 1):
        if p[i][0] == 0:
            continue
        for k in range(TOP + 1 - i):
            if r[k][0]:
                out[i + k] = qadd(out[i + k], qmul(p[i], r[k]))
    return out


def sinv(p):
    out = [ZERO] * (TOP + 1)
    out[0] = q(p[0][1], p[0][0])
    for k in range(1, TOP + 1):
        s = ZERO
        for i in range(1, k + 1):
            s = qadd(s, qmul(p[i], out[k - i]))
        out[k] = qmul(q(-s[0], s[1]), out[0])
    return out


def spow(p, k):
    out = [ONE] + [ZERO] * TOP
    for _ in range(k):
        out = smul(out, p)
    return out


def sscale(c, p):
    return [qmul(c, x) for x in p]


def ssub(p, r):
    return [qsub(x, y) for x, y in zip(p, r)]


def sadd(p, r):
    return [qadd(x, y) for x, y in zip(p, r)]


def sshow(p, top):
    return ",".join("b" + str(k) + ":" + qs(p[k]) for k in range(top + 1) if p[k][0])


# ---- A. McKay powers on SU(2) and the character coefficients of exp(beta a)

def mckay_su2(m_max):
    rows = [[0] * (m_max + 2) for _ in range(m_max + 1)]
    rows[0][0] = 1
    for m in range(m_max):
        for n in range(m + 1):
            v = rows[m][n]
            if v:
                if n >= 1:
                    rows[m + 1][n - 1] += v
                rows[m + 1][n + 1] += v
    return rows


def catalan(k):
    return comb(2 * k, k) // (k + 1)


def part_a():
    N = mckay_su2(TOP)
    cat_ok = all(N[m][0] == (catalan(m // 2) if m % 2 == 0 else 0) for m in range(TOP + 1))
    check("mckay_su2_closed_walks_are_catalan", cat_ok)
    say("YM4_03C_MCKAY_SU2|N_m(0)_m=0..12=" + ",".join(str(N[m][0]) for m in range(13)) + "|N_6(n)_n=0..6=" + ",".join(str(N[6][n]) for n in range(7)) + "|catalan_match=" + str(int(cat_ok)) + "|tag=MEASURED|json=0")
    coeff = {}
    for n in range(4):
        coeff[n] = [q(N[m][n], (1 << m) * factorial(m)) if m >= n else ZERO for m in range(TOP + 1)]
    inv0 = sinv(coeff[0])
    t = {}
    for n in (1, 2, 3):
        t[n + 1] = sscale(q(1, n + 1), smul(coeff[n], inv0))
    s_half = sscale(q(2), spow(t[2], 4))
    s_one = ssub(sscale(q(3), spow(t[3], 4)), sscale(q(2), spow(t[2], 8)))
    say("YM4_03C_T_SERIES|route=McKay_powers|t_2=" + sshow(t[2], 9) + "|t_3=" + sshow(t[3], 8) + "|tag=MEASURED|json=0")
    say("YM4_03C_D2_SERIES|route=McKay_powers|2t2^4=" + sshow(s_half, 12) + "|3t3^4-2t2^8=" + sshow(s_one, 12) + "|tag=MEASURED|json=0")
    # The decide lane's series_check.py and the attack lane's attack_checks.py, Bessel routes, as filed on 2026-11-06.
    filed_half = {4: q(1, 128), 6: q(-1, 768), 8: q(1, 6144), 10: q(-79, 4423680), 12: q(769, 424673280)}
    filed_one = {8: q(-19, 884736), 10: q(7, 884736), 12: q(-373, 212336640)}
    half_ok = all(s_half[k] == filed_half.get(k, ZERO) for k in range(13))
    one_ok = all(s_one[k] == filed_one.get(k, ZERO) for k in range(13))
    check("d2_half_through_b12_equals_the_bessel_lanes", half_ok)
    check("d2_one_through_b12_equals_the_bessel_lanes", one_ok)
    check("t2_leading_terms", t[2][1] == q(1, 4) and t[2][3] == q(-1, 96) and t[2][0] == ZERO and t[2][2] == ZERO)
    check("t3_leading_term", t[3][2] == q(1, 24) and t[3][0] == ZERO and t[3][1] == ZERO)
    say("YM4_03C_D2_MATCH|half_through_b12=" + str(int(half_ok)) + "|one_through_b12=" + str(int(one_ok)) + "|lanes=decide_series_check.py,attack_attack_checks.py|tag=MEASURED|json=0")
    return t, s_half, s_one


# ---- B. 2T and 2I as designs

def zp_mul(a, b):
    return (a[0] * b[0] + a[1] * b[1], a[0] * b[1] + a[1] * b[0] + a[1] * b[1])


def zp_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def zp_sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


# Trace of the fundamental representation, 2 cos(theta), as a + b phi with phi^2 = phi + 1, and the number of elements with that trace.
TRACES_2I = [((2, 0), 1), ((-2, 0), 1), ((0, 0), 30), ((1, 0), 20), ((-1, 0), 20), ((0, 1), 12), ((0, -1), 12), ((-1, 1), 12), ((1, -1), 12)]
TRACES_2T = [((2, 0), 1), ((-2, 0), 1), ((0, 0), 6), ((1, 0), 8), ((-1, 0), 8)]
E8_AFFINE = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)]
E8_DIMS = [1, 2, 3, 4, 5, 6, 4, 2, 3]
E6_AFFINE = [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (5, 6)]
E6_DIMS = [1, 2, 3, 2, 1, 2, 1]


def class_sums(traces, kmax):
    out = []
    for k in range(kmax + 1):
        total = (0, 0)
        for x, size in traces:
            s_prev, s_cur = (0, 0), (1, 0)
            for _ in range(k):
                s_prev, s_cur = s_cur, zp_sub(zp_mul(x, s_cur), s_prev)
            total = zp_add(total, (size * s_cur[0], size * s_cur[1]))
        out.append(total)
    return out


def power_sums(traces, mmax):
    out = []
    for m in range(mmax + 1):
        total = (0, 0)
        for x, size in traces:
            p = (1, 0)
            for _ in range(m):
                p = zp_mul(p, x)
            total = zp_add(total, (size * p[0], size * p[1]))
        out.append(total)
    return out


def closed_walks(edges, nodes, mmax):
    adj = [[] for _ in range(nodes)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    vec = [1] + [0] * (nodes - 1)
    out = [1]
    for _ in range(mmax):
        vec = [sum(vec[b] for b in adj[a]) for a in range(nodes)]
        out.append(vec[0])
    return out


def part_b():
    order_2i = sum(s for _, s in TRACES_2I)
    order_2t = sum(s for _, s in TRACES_2T)
    check("orders_120_and_24", order_2i == 120 and order_2t == 24)
    sums_2i = class_sums(TRACES_2I, 14)
    sums_2t = class_sums(TRACES_2T, 8)
    first_2i = [k for k in range(1, 15) if sums_2i[k] != (0, 0)]
    first_2t = [k for k in range(1, 9) if sums_2t[k] != (0, 0)]
    check("2I_chi_sums_vanish_for_spin_1/2_to_11/2", all(sums_2i[k] == (0, 0) for k in range(1, 12)))
    check("2I_first_nonzero_at_spin_6_equal_120", first_2i[:1] == [12] and sums_2i[12] == (120, 0))
    check("2T_chi_sums_vanish_for_spin_1/2_to_5/2", all(sums_2t[k] == (0, 0) for k in range(1, 6)))
    check("2T_first_nonzero_at_spin_3_equal_24", first_2t[:1] == [6] and sums_2t[6] == (24, 0))
    say("YM4_03C_DESIGN|group=2I|order=" + str(order_2i) + "|sum_chi_spin_k/2_k=0..14=" + ",".join(str(v[0]) + ("" if v[1] == 0 else "+" + str(v[1]) + "phi") for v in sums_2i) + "|design_degree=11|tag=MEASURED|json=0")
    say("YM4_03C_DESIGN|group=2T|order=" + str(order_2t) + "|sum_chi_spin_k/2_k=0..8=" + ",".join(str(v[0]) + ("" if v[1] == 0 else "+" + str(v[1]) + "phi") for v in sums_2t) + "|design_degree=5|tag=MEASURED|json=0")
    dims_ok = True
    for edges, dims in ((E8_AFFINE, E8_DIMS), (E6_AFFINE, E6_DIMS)):
        adj = [[] for _ in dims]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        dims_ok = dims_ok and all(2 * dims[a] == sum(dims[b] for b in adj[a]) for a in range(len(dims)))
    check("mckay_graphs_tensor_with_the_doublet", dims_ok)
    walks_2i = closed_walks(E8_AFFINE, 9, 14)
    walks_2t = closed_walks(E6_AFFINE, 7, 8)
    psum_2i = power_sums(TRACES_2I, 14)
    psum_2t = power_sums(TRACES_2T, 8)
    check("2I_moments_by_classes_equal_closed_walks_on_affine_E8", all(psum_2i[m] == (120 * walks_2i[m], 0) for m in range(15)))
    check("2T_moments_by_classes_equal_closed_walks_on_affine_E6", all(psum_2t[m] == (24 * walks_2t[m], 0) for m in range(9)))
    su2 = [catalan(m // 2) if m % 2 == 0 else 0 for m in range(15)]
    agree_2i = [m for m in range(15) if walks_2i[m] == su2[m]]
    agree_2t = [m for m in range(9) if walks_2t[m] == su2[m]]
    check("2I_moments_equal_SU2_through_m=11_and_differ_at_12", agree_2i[:12] == list(range(12)) and 12 not in agree_2i)
    check("2T_moments_equal_SU2_through_m=5_and_differ_at_6", agree_2t[:6] == list(range(6)) and 6 not in agree_2t)
    say("YM4_03C_MOMENTS|E[chi_1/2^m]_m=0..14|SU2=" + ",".join(str(v) for v in su2) + "|2I=" + ",".join(str(v) for v in walks_2i) + "|2T_m=0..8=" + ",".join(str(v) for v in walks_2t) + "|first_difference_2I_m=12_133_vs_132|first_difference_2T_m=6_6_vs_5|tag=MEASURED|json=0")


# ---- C. Surfaces in a window of Z^4, with b = 2 and coarse sites at even coordinates

DIM = 4
UNIT = [tuple(1 if i == mu else 0 for i in range(DIM)) for mu in range(DIM)]


def vadd(x, y):
    return tuple(a + b for a, b in zip(x, y))


def vsub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def plaq(x, mu, nu):
    return (x, mu, nu) if mu < nu else (x, nu, mu)


def plaq_edges(p):
    x, mu, nu = p
    return ((x, mu), (vadd(x, UNIT[mu]), nu), (vadd(x, UNIT[nu]), mu), (x, nu))


PLAQ_SIGNS = (1, 1, -1, -1)


def plaq_vertices(p):
    x, mu, nu = p
    return (x, vadd(x, UNIT[mu]), vadd(vadd(x, UNIT[mu]), UNIT[nu]), vadd(x, UNIT[nu]))


def cube_faces(c):
    x, dirs = c
    out = []
    for k in dirs:
        i, j = [d for d in dirs if d != k]
        out.append(plaq(x, i, j))
        out.append(plaq(vadd(x, UNIT[k]), i, j))
    return frozenset(out)


def is_line(edge):
    x, mu = edge
    return all(x[l] % 2 == 0 for l in range(DIM) if l != mu)


def coarse_of(edge):
    """A line link's coarse link, as (coarse base site, direction), and its position 0 or 1 along it."""
    x, mu = edge
    base = list(x)
    position = x[mu] % 2
    base[mu] = x[mu] - position
    return (tuple(base), mu), position


def filling(start, mu, nu):
    out = set()
    for s in (0, 1):
        for r in (0, 1):
            out.add(plaq(vadd(vadd(start, tuple(s * u for u in UNIT[mu])), tuple(r * u for u in UNIT[nu])), mu, nu))
    return frozenset(out)


def boundary(H):
    odd = set()
    for p in H:
        for e in plaq_edges(p):
            odd ^= {e}
    return frozenset(odd)


def window_cubes(lo, hi):
    out = []
    for dirs in itertools.combinations(range(DIM), 3):
        ranges = [range(lo[i], hi[i] if i in dirs else hi[i] + 1) for i in range(DIM)]
        for x in itertools.product(*ranges):
            out.append((tuple(x), dirs))
    return out


def chains_up_to_three(F, cubes, budget):
    faces = [cube_faces(c) for c in cubes]
    owners = {}
    for index, fs in enumerate(faces):
        for f in fs:
            owners.setdefault(f, []).append(index)
    found = {}

    def record(H, chain):
        if len(H) <= budget and H not in found:
            found[H] = chain

    record(F, ())
    n = len(cubes)
    for i in range(n):
        Hi = F ^ faces[i]
        record(Hi, (i,))
        for j in range(i + 1, n):
            Hij = Hi ^ faces[j]
            record(Hij, (i, j))
            need = len(Hij) + 6 - budget  # a third cube k reaches the budget only with 2 |Hij & faces[k]| >= need
            if need > 12:
                continue
            counts = {}
            for f in Hij:
                for k in owners.get(f, ()):
                    if k > j:
                        counts[k] = counts.get(k, 0) + 1
            for k, shared in counts.items():
                if 2 * shared >= need:
                    record(Hij ^ faces[k], (i, j, k))
            if need <= 0:
                # every third cube reaches the budget, including those sharing no face with Hij
                for k in range(j + 1, n):
                    if k not in counts:
                        record(Hij ^ faces[k], (i, j, k))
    return found


def classify(H, target):
    """Connection through off links and through any shared edge, edge valences, Euler characteristic, orientation, and the positions touched."""
    plist = sorted(H)
    index = {p: k for k, p in enumerate(plist)}
    by_edge = {}
    for p in plist:
        for e in plaq_edges(p):
            by_edge.setdefault(e, []).append(p)
    parent = list(range(len(plist)))
    parent_e = list(range(len(plist)))

    def find(par, a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    for e, ps in by_edge.items():
        for p in ps[1:]:
            a, b = find(parent_e, index[ps[0]]), find(parent_e, index[p])
            parent_e[a] = b
            if not is_line(e):
                a, b = find(parent, index[ps[0]]), find(parent, index[p])
                parent[a] = b
    off_components = len({find(parent, k) for k in range(len(plist))})
    edge_components = len({find(parent_e, k) for k in range(len(plist))})
    valences = sorted({len(ps) for ps in by_edge.values()})
    manifold = max(len(ps) for ps in by_edge.values()) <= 2
    vertices = set()
    for p in plist:
        vertices.update(plaq_vertices(p))
    euler = len(vertices) - len(by_edge) + len(plist)
    orientable = None
    if manifold:
        sign = {}
        orientable = True
        for start in plist:
            if start in sign:
                continue
            sign[start] = 1
            stack = [start]
            while stack and orientable:
                p = stack.pop()
                for e, s in zip(plaq_edges(p), PLAQ_SIGNS):
                    for r in by_edge[e]:
                        if r == p:
                            continue
                        s_r = PLAQ_SIGNS[plaq_edges(r).index(e)]
                        want = -sign[p] * s * s_r
                        if r not in sign:
                            sign[r] = want
                            stack.append(r)
                        elif sign[r] != want:
                            orientable = False
    positions = {}
    for e in by_edge:
        if is_line(e):
            link, position = coarse_of(e)
            positions.setdefault(link, set()).add(position)
    return {"off_components": off_components, "edge_components": edge_components, "manifold": manifold, "valences": valences,
            "euler": euler, "orientable": orientable, "positions": positions}


def walk_count(target, lo, hi, budget, cap):
    """The defect-repair walk of tests/test_one_scale_blocking.py, count_surfaces, on plaquettes inside the window."""
    def inside(p):
        return all(lo[i] <= v[i] <= hi[i] for v in plaq_vertices(p) for i in range(DIM))

    def plaquettes_at(edge):
        x, mu = edge
        out = []
        for nu in range(DIM):
            if nu == mu:
                continue
            for p in (plaq(x, mu, nu), plaq(vsub(x, UNIT[nu]), mu, nu)):
                if inside(p):
                    out.append(p)
        return out

    counts = set()
    seen = set()
    stack = [(frozenset(), frozenset(target))]
    while stack:
        chosen, odd = stack.pop()
        if chosen in seen:
            continue
        seen.add(chosen)
        if len(seen) > cap:
            return counts, False
        if not odd:
            counts.add(chosen)
            continue
        remaining = budget - len(chosen)
        if remaining <= 0 or len(odd) > 4 * remaining:
            continue
        work = min(odd)
        for option in plaquettes_at(work):
            if option in chosen:
                continue
            moved = set(odd)
            for e in plaq_edges(option):
                moved ^= {e}
            stack.append((chosen | {option}, frozenset(moved)))
    return counts, True


def surface_report(name, F, target, lo, hi, budget, walk_budget, cap):
    cubes = window_cubes(lo, hi)
    found = chains_up_to_three(F, cubes, budget)
    good = {H: chain for H, chain in found.items() if boundary(H) == target}
    check("surfaces_" + name + "_boundary_exact", len(good) == len(found))
    rows = {}
    detail = {}
    connected_sets = set()
    for H, chain in good.items():
        c = classify(H, target)
        key = (len(H), int(c["off_components"] == 1), int(c["manifold"]), c["euler"], c["orientable"])
        rows[key] = rows.get(key, 0) + 1
        if c["off_components"] == 1:
            detail.setdefault(len(H), []).append((chain, c))
            connected_sets.add(H)
    text = ";".join("size=" + str(k[0]) + ",connected=" + str(k[1]) + ",manifold=" + str(k[2]) + ",euler=" + str(k[3]) + ",orientable=" + str(k[4]) + ",count=" + str(v) for k, v in sorted(rows.items(), key=lambda kv: (kv[0][0], -kv[0][1], -kv[0][2], kv[0][3], str(kv[0][4]))))
    say("YM4_03C_SURFACES|shape=" + name + "|window=" + ",".join(str(a) + ".." + str(b) for a, b in zip(lo, hi)) + "|cubes_in_window=" + str(len(cubes)) + "|chains=at_most_3_cubes|budget=" + str(budget) + "|" + text + "|tag=MEASURED|json=0")
    walked, complete = walk_count(target, lo, hi, walk_budget, cap)
    walk_sizes = {}
    for H in walked:
        walk_sizes[len(H)] = walk_sizes.get(len(H), 0) + 1
    inside = all(H in good for H in walked)
    by_class = {}
    for source, sets in (("walk", walked), ("chains", [H for H in connected_sets if len(H) <= walk_budget])):
        for H in sets:
            c = classify(H, target)
            if c["off_components"] == 1:
                key = (len(H), int(c["manifold"]))
                by_class.setdefault(key, {"walk": set(), "chains": set()})[source].add(H)
    disks_same = all(v["walk"] == v["chains"] for k, v in by_class.items() if k[1] == 1)
    all_same = all(v["walk"] == v["chains"] for v in by_class.values())
    text = ";".join("size=" + str(k[0]) + ",manifold=" + str(k[1]) + ",walk=" + str(len(v["walk"])) + ",chains=" + str(len(v["chains"])) + ",same=" + str(int(v["walk"] == v["chains"])) for k, v in sorted(by_class.items()))
    say("YM4_03C_WALK|shape=" + name + "|budget=" + str(walk_budget) + "|complete=" + str(int(complete)) + "|walk_by_size=" + ",".join(str(k) + ":" + str(v) for k, v in sorted(walk_sizes.items())) + "|every_walk_set_among_the_chains=" + str(int(inside)) + "|connected_through_off_links:" + text + "|tag=MEASURED|json=0")
    return rows, detail, (complete and inside and disks_same, all_same)


def part_c():
    o = (0, 0, 0, 0)
    FP = filling(o, 0, 1)
    tP = boundary(FP)
    rowsP, detP, walkP = surface_report("plaquette", FP, tP, (-1, -1, -1, -1), (3, 3, 1, 1), 10, 10, 1500000)
    check("plaquette_one_at_4", rowsP.get((4, 1, 1, 1, True), 0) == 1)
    check("plaquette_16_disks_at_8", rowsP.get((8, 1, 1, 1, True), 0) == 16 and sum(v for k, v in rowsP.items() if k[0] == 8) == 16)
    check("plaquette_16_connected_disks_at_10", rowsP.get((10, 1, 1, 1, True), 0) == 16)
    conn_nonmanifold_10 = sum(v for k, v in rowsP.items() if k[0] == 10 and k[1] == 1 and k[2] == 0)
    check("plaquette_16_connected_edge_sharing_at_10", conn_nonmanifold_10 == 16)
    check("plaquette_none_at_5_6_7_9", all(k[0] in (4, 8, 10) for k in rowsP))
    # The walk adds plaquettes on the lowest odd edge only, so a cube joined along one edge is reached in some orders and missed in others.
    check("plaquette_walk_within_chains_and_the_same_disks", walkP[0])
    # The 16 connected sets at 10 with a valence-4 edge: one cube sharing exactly one off link of the filling, no face.
    edge_cubes = [ch for ch, c in detP.get(10, []) if not c["manifold"]]
    shapes = sorted({len(ch) for ch in edge_cubes})
    check("edge_sharing_sets_are_single_cubes", shapes == [1])
    say("YM4_03C_PLAQUETTE_CLASSES|size_4=F_P|size_8=16_one_cube_on_a_face|size_10_disks=16_two_cubes_on_two_adjacent_faces|size_10_edge_sharing=" + str(conn_nonmanifold_10) + "_one_cube_on_one_off_link|tag=MEASURED|json=0")

    FQ = filling(o, 0, 2)
    F2 = FP | FQ
    tC = boundary(F2)
    rowsC, detC, walkC = surface_report("chair", F2, tC, (-1, -1, -1, -1), (3, 3, 3, 1), 10, 10, 1500000)
    check("chair_size_8_is_the_two_fillings_joined_on_line_links_only", sum(v for k, v in rowsC.items() if k[0] == 8) == 1 and sum(v for k, v in rowsC.items() if k[0] == 8 and k[1] == 1) == 0)
    check("chair_three_connected_disks_at_10", rowsC.get((10, 1, 1, 1, True), 0) == 3 and sum(v for k, v in rowsC.items() if k[0] == 10 and k[1] == 1) == 3)
    check("chair_walk_within_chains_and_the_same_connected_sets", walkC[0] and walkC[1])
    shared = ((0, 0, 0, 0), 0)
    touched = sorted(tuple(sorted(c["positions"].get(shared, set()))) for _, c in detC.get(10, []) if c["manifold"])
    check("chair_disks_touch_the_shared_link_at_one_position_or_none", touched == [(), (0,), (1,)])
    say("YM4_03C_CHAIR_CLASSES|size_8=F_P_and_F_Q_on_line_links_only|size_10=3_disks|shared_link_positions_touched=" + ";".join("(" + ",".join(str(v) for v in t) + ")" for t in touched) + "|tag=MEASURED|json=0")

    FR = filling((0, -2, 0, 0), 0, 1)
    F3 = FP | FR
    tR = boundary(F3)
    rowsR, detR, walkR = surface_report("rectangle", F3, tR, (-1, -3, -1, -1), (3, 3, 1, 1), 14, 14, 1500000)
    conn_R = {k[0]: 0 for k in rowsR}
    for k, v in rowsR.items():
        if k[1] == 1:
            conn_R[k[0]] += v
    check("rectangle_no_connected_set_through_12", all(conn_R.get(s, 0) == 0 for s in range(13)))
    check("rectangle_8_connected_disks_at_14", rowsR.get((14, 1, 1, 1, True), 0) == 8 and conn_R.get(14, 0) == 8)
    check("rectangle_walk_within_chains_and_the_same_connected_sets_through_14", walkR[0] and walkR[1])
    say("YM4_03C_RECTANGLE_CLASSES|connected_by_size=" + ",".join(str(k) + ":" + str(v) for k, v in sorted(conn_R.items())) + "|tag=MEASURED|json=0")


# ---- D. The arithmetic of the rows

def part_d(t, s_half, s_one):
    t2, t3 = t[2], t[3]
    p4 = s_half[6]
    p5_d2 = s_half[8]
    bump = sscale(q(2), spow(t2, 8))
    p5 = qadd(p5_d2, qmul(q(16), bump[8]))
    check("P4_order_6_is_-1/768", p4 == q(-1, 768))
    check("P5_order_8_is_1/1536", p5 == q(1, 1536))
    check("chi1_order_8_is_-19/884736", s_one[8] == q(-19, 884736))
    disk10 = sscale(q(2), spow(t2, 10))
    p6 = qmul(q(3), disk10[10])
    check("P6_chair_is_3/524288", p6 == q(3, 524288))
    p7_14 = qmul(q(8), sscale(q(2), spow(t2, 14))[14])
    check("P7_rectangle_at_14_is_1/16777216", p7_14 == q(1, 16777216))
    tube = qmul(q(12), spow(t2, 8)[8])
    check("P10b_tube_is_3/16384", tube == q(3, 16384))
    # P11, the lane's order-10 conjecture for chi_1/2(V_P) in d = 4, by its parts.
    part_d2 = s_half[10]
    part_bumps = qmul(q(16), bump[10])
    part_dominoes = qmul(q(16), disk10[10])
    face_joint = sscale(q(6), smul(t3, spow(t2, 8)))
    face_cluster = sscale(q(8), spow(t2, 10))
    part_face = qmul(q(16), qsub(face_joint[10], face_cluster[10]))
    total = qadd(qadd(part_d2, part_bumps), qadd(part_dominoes, part_face))
    check("P11_parts", part_bumps == q(-1, 6144) and part_dominoes == q(1, 32768) and part_face == q(-1, 16384))
    check("P11_total_is_-467/2211840", total == q(-467, 2211840))
    p12 = s_one[10]
    check("P12_chi1_order_10_is_7/884736", p12 == q(7, 884736))
    # The same rows in d = 3, where each of the four classes holds 8 (d - 2) = 8 members.
    p5_d3 = qadd(p5_d2, qmul(q(8), bump[8]))
    p11_d3 = qadd(qadd(part_d2, qmul(q(8), bump[10])), qadd(qmul(q(8), disk10[10]), qmul(q(8), qsub(face_joint[10], face_cluster[10]))))
    check("P5_d3_is_5/12288", p5_d3 == q(5, 12288))
    check("P11_d3_is_-1013/8847360", p11_d3 == q(-1013, 8847360))
    say("YM4_03C_D3|P5_d3=" + qs(p5_d3) + "|P11_d3=" + qs(p11_d3) + "|P11_general_d=-79/4423680-19(d-2)/196608|tag=MEASURED_arithmetic|json=0")
    # G2 rows: the partition-function level against the logarithm.
    xi_chi1 = sscale(q(3), spow(t3, 4))[8]
    self_cluster = sscale(q(-2), spow(t2, 8))[8]
    product_pair = qmul(s_half[4], s_half[4])
    check("G2_chi1_partition_level_and_self_cluster", xi_chi1 == q(1, 110592) and self_cluster == q(-1, 32768) and qadd(xi_chi1, self_cluster) == s_one[8])
    check("G2_disjoint_pair_partition_level_2^-14", product_pair == q(1, 16384))
    say("YM4_03C_ROWS|P4=" + qs(p4) + "|P5=" + qs(p5_d2) + "+16*" + qs(bump[8]) + "=" + qs(p5) + "|chi1_b8=" + qs(s_one[8]) + "|P6=3*" + qs(disk10[10]) + "=" + qs(p6) + "|P7_b14=8*" + qs(sscale(q(2), spow(t2, 14))[14]) + "=" + qs(p7_14) + "|P10b=12*" + qs(spow(t2, 8)[8]) + "=" + qs(tube) + "|tag=MEASURED|json=0")
    say("YM4_03C_P11|d2=" + qs(part_d2) + "|bumps_16x=" + qs(part_bumps) + "|dominoes_16x=" + qs(part_dominoes) + "|face_cubes_16x(6t3t2^8-8t2^10)=" + qs(part_face) + "|edge_cubes_16x=0/1|total=" + qs(total) + "|P12_chi1_b10=" + qs(p12) + "|tag=MEASURED_arithmetic_of_a_CONJECTURE|json=0")
    say("YM4_03C_G2|chi1_b8_partition_level=" + qs(xi_chi1) + "|self_cluster=" + qs(self_cluster) + "|chi1_b8_log=" + qs(s_one[8]) + "|disjoint_pair_b8_partition_level=" + qs(product_pair) + "|disjoint_pair_b8_log=0/1|tag=MEASURED|json=0")


# ---- E. Orbits of coarse shapes under the 384 signed permutations with coarse translations

def path_links(start, steps):
    links = []
    x = start
    for mu, s in steps:
        y = vadd(x, tuple(s * u for u in UNIT[mu]))
        links.append(frozenset((x, y)))
        x = y
    assert x == start
    return frozenset(links)


def normalized(links):
    sites = sorted({s for l in links for s in l})
    base = sites[0]
    return frozenset(frozenset(vsub(s, base) for s in l) for l in links)


def part_e():
    group = []
    for perm in itertools.permutations(range(DIM)):
        for signs in itertools.product((1, -1), repeat=DIM):
            group.append((perm, signs))
    check("point_group_order_384", len(group) == 384)

    def act(g, links):
        perm, signs = g
        return frozenset(frozenset(tuple(signs[i] * s[perm[i]] for i in range(DIM)) for s in l) for l in links)

    o = (0, 0, 0, 0)
    shapes = [
        ("coarse_link", frozenset([frozenset((o, UNIT[0]))]), 4),
        ("plaquette", path_links(o, [(0, 1), (1, 1), (0, -1), (1, -1)]), 6),
        ("chair", path_links(o, [(1, 1), (0, 1), (1, -1), (2, 1), (0, -1), (2, -1)]), 48),
        ("rectangle_1x2", path_links(o, [(0, 1), (1, 1), (1, 1), (0, -1), (1, -1), (1, -1)]), 12),
        ("twisted_hexagon", path_links(o, [(0, 1), (1, 1), (2, 1), (0, -1), (1, -1), (2, -1)]), 16),
        ("parallel_pair_distance_1", path_links(o, [(0, 1), (1, 1), (0, -1), (1, -1)]) | path_links(UNIT[2], [(0, 1), (1, 1), (0, -1), (1, -1)]), 12),
    ]
    parts = []
    for name, links, predicted in shapes:
        base = normalized(links)
        stab = sum(1 for g in group if normalized(act(g, links)) == base)
        per_site = 384 // stab
        check("orbit_" + name, per_site == predicted and 384 % stab == 0, "stab=" + str(stab))
        parts.append(name + ":stabilizer=" + str(stab) + ",per_coarse_site=" + str(per_site))
    say("YM4_03C_ORBITS|group=coarse_translations_x_384|" + "|".join(parts) + "|tag=MEASURED|json=0")


def main():
    say("YM4_03C_CHECKS_START|file=reviews/fable5-ym4-03c-prediction/derive_checks.py|rows=docs/PREDICTION-YM4-03C.hbp|integers_only=1|json=0")
    t, s_half, s_one = part_a()
    part_b()
    part_c()
    part_d(t, s_half, s_one)
    part_e()
    say("YM4_03C_CHECKS_DONE|checks=" + str(CHECKS[0]) + "|failed=" + str(FAILED[0]) + "|json=0")
    return 1 if FAILED[0] else 0


if __name__ == "__main__":
    sys.exit(main())
