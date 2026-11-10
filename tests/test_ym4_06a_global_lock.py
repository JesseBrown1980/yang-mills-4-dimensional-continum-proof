#!/usr/bin/env python3
"""YM4-06A: global-lock structure in three spatial dimensions. Structure only.

Finite control: S3 Hamiltonian-lattice gauge fields on periodic Lx x Ly x Lz cubic lattices, built from link variables.
Every plaquette holonomy is derived from the links in the repository's convention U_mu(x) U_nu(x+mu) U_mu(x+nu)^-1 U_nu(x)^-1,
every cube's based, transported product of its six faces is checked to be e, and the magnetic cost of a configuration is
E(U) = sum over faces of (2 - chi_std(U_P)), with chi_std the two-dimensional irreducible character of S3.

  * flat sectors: the 48 tree-gauge-fixed flat configurations and their 21 orbits under the residual global conjugation,
    reproduced on every lattice, against the commuting-triple count and an independent Burnside count;
  * kappa_3D = min over nonflat configurations of E, by a complete branch-and-bound (argument in the NOTE, section 3);
  * every cost that is claimed has an explicit periodic link configuration behind it (the reconstruction gate);
  * continuous SU(2) comparison with the repository's exact quaternions (tests/test_exact_su2_4d.py): an explicit family
    of nonflat configurations whose action goes to 0, a continuous family of pairwise non-conjugate flat connections, and
    the 't Hooft twisted sector kept as a separate labeled object.

No spectrum, gap or transfer-matrix eigenvalue of any Hamiltonian is computed here. Issue #6 is untouched.

usage = test_ym4_06a_global_lock.py [sabotage=NAME]   NAME in SABOTAGE_NAMES; each exits 1 on FAILED|check=RED_NAME.
Python standard library, integers only, json=0.
"""
import itertools
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)
import test_exact_su2_4d as su2  # noqa: E402  (the repository's exact SU(2) quaternions, reused)

SABOTAGE_NAMES = ("broken_transport", "noncommuting_triple", "wrong_chi", "dropped_face", "missing_gauge_orbit",
                  "unreconstructible_flux", "twisted_as_periodic")
SABOTAGE = ""
for argument in sys.argv[1:]:
    if not argument.startswith("sabotage=") or argument.split("=", 1)[1] not in SABOTAGE_NAMES:
        print("usage = test_ym4_06a_global_lock.py [sabotage=NAME]")
        sys.exit(2)
    SABOTAGE = argument.split("=", 1)[1]

LATTICES = ((2, 2, 2), (2, 2, 3), (2, 3, 3), (3, 3, 3), (3, 3, 4))
# Full support enumeration (no Bianchi prefilter) on these; the prefiltered run is done on every lattice and must agree.
FULL_ENUMERATION = ((2, 2, 2), (2, 2, 3), (2, 3, 3), (3, 3, 3), (3, 3, 4))
BOUND = 8  # search every nonflat configuration with E < BOUND


def fail(name):
    print("FAILED|check=RED_%s|json=0" % name)
    sys.exit(1)


def check(ok, name):
    if not ok:
        fail(name)


# ---------------------------------------------------------------- S3
class S3:
    def __init__(self):
        perms = list(itertools.permutations(range(3)))
        self.elements = perms
        self.index = {p: i for i, p in enumerate(perms)}
        self.e = self.index[(0, 1, 2)]
        n = len(perms)
        self.n = n
        self.mult = [[self.index[tuple(a[b[i]] for i in range(3))] for b in perms] for a in perms]
        self.inv = [0] * n
        for a in range(n):
            for b in range(n):
                if self.mult[a][b] == self.e:
                    self.inv[a] = b
        fixed = [sum(1 for i in range(3) if p[i] == i) for p in perms]
        self.chi = [f - 1 for f in fixed]  # chi_std = (fixed points) - 1: 2, 0, -1
        if SABOTAGE == "wrong_chi":
            self.chi = [1 if f == 1 else c for f, c in zip(fixed, self.chi)]  # transposition read as 1
        self.sign = [1 if f != 1 else -1 for f in fixed]
        self.cost = [2 - c for c in self.chi]
        self.kind = ["e" if f == 3 else ("transposition" if f == 1 else "3-cycle") for f in fixed]

    def conj(self, g, a):
        return self.mult[self.mult[g][a]][self.inv[g]]

    def comm(self, a, b):
        return self.mult[self.mult[self.mult[a][b]][self.inv[a]]][self.inv[b]]

    def name(self, a):
        return "".join(str(v) for v in self.elements[a])


G = S3()


def section_characters():
    # chi_std must be the 2-dim irreducible character: chi(e)=2, <chi,chi>=1, orthogonal to trivial and sign.
    n = G.n
    norm = sum(c * c for c in G.chi)
    triv = sum(G.chi)
    sgn = sum(c * s for c, s in zip(G.chi, G.sign))
    ok = G.chi[G.e] == 2 and norm == n and triv == 0 and sgn == 0
    check(ok, "wrong_chi")
    classes = sorted(set(zip(G.kind, G.chi, G.cost)), key=lambda t: t[2])
    check([c for _, _, c in classes] == [0, 2, 3], "wrong_chi")
    commutators = sorted({G.comm(a, b) for a in range(n) for b in range(n)})
    check(sorted(G.kind[c] for c in commutators) == ["3-cycle", "3-cycle", "e"], "commutator_subgroup")
    print("S3_CHARACTER|chi_std_on_e,transposition,3-cycle=2,0,-1|norm=%d/%d|orthogonal_to_trivial=1|orthogonal_to_sign=1|"
          "face_cost_2-chi=0,2,3|commutator_subgroup=A3={e,3-cycles}|ok=1|json=0" % (norm, n))


# ---------------------------------------------------------------- algebraic flat sectors
def commuting(a, b):
    return G.mult[a][b] == G.mult[b][a]


def commuting_tuples(k):
    out = []
    for t in itertools.product(range(G.n), repeat=k):
        ok = True
        for i in range(k):
            for j in range(i + 1, k):
                if SABOTAGE == "noncommuting_triple" and k == 3 and (i, j) == (0, 2):
                    continue  # the a,c condition dropped
                if not commuting(t[i], t[j]):
                    ok = False
        if ok:
            out.append(t)
    return out


def conj_orbits(tuples):
    seen, orbits = set(), 0
    for t in tuples:
        if t in seen:
            continue
        orbits += 1
        for g in range(G.n):
            seen.add(tuple(G.conj(g, a) for a in t))
    return orbits


def burnside(k):
    # orbits = (1/|G|) sum_g #{commuting k-tuples fixed by conjugation by g}, i.e. commuting k-tuples inside C(g).
    total = 0
    for g in range(G.n):
        cent = [a for a in range(G.n) if commuting(a, g)]
        for t in itertools.product(cent, repeat=k):
            if all(commuting(t[i], t[j]) for i in range(k) for j in range(i + 1, k)):
                total += 1
    check(total % G.n == 0, "burnside")
    return total // G.n


# ---------------------------------------------------------------- lattice
class Lattice:
    def __init__(self, dims, drop_face=False):
        self.dims = dims
        self.d = len(dims)
        self.sites = list(itertools.product(*[range(n) for n in dims]))
        self.sid = {x: i for i, x in enumerate(self.sites)}
        self.V = len(self.sites)
        self.nlinks = self.V * self.d
        self.planes = [(mu, nu) for mu in range(self.d) for nu in range(mu + 1, self.d)]
        self.faces = []      # (x, mu, nu)
        self.fwords = []     # [(link, sign)] x4
        for x in self.sites:
            for mu, nu in self.planes:
                self.faces.append((x, mu, nu))
                self.fwords.append(self.word(x, mu, nu))
        if drop_face:
            self.faces.pop(0)
            self.fwords.pop(0)
        self.fid = {f: i for i, f in enumerate(self.faces)}
        self.nfaces = len(self.faces)
        self.link_faces = [[] for _ in range(self.nlinks)]
        for f, w in enumerate(self.fwords):
            for l, _ in w:
                self.link_faces[l].append(f)
        self.tree = self.spanning_tree()

    def shift(self, x, mu, k=1):
        y = list(x)
        y[mu] = (y[mu] + k) % self.dims[mu]
        return tuple(y)

    def link(self, x, mu):
        return self.sid[x] * self.d + mu

    def word(self, x, mu, nu):
        return [(self.link(x, mu), 1), (self.link(self.shift(x, mu), nu), 1),
                (self.link(self.shift(x, nu), mu), -1), (self.link(x, nu), -1)]

    def spanning_tree(self):
        tree, seen, queue = set(), {self.sites[0]}, [self.sites[0]]
        while queue:
            x = queue.pop(0)
            for mu in range(self.d):
                y = self.shift(x, mu)
                if y not in seen:
                    seen.add(y)
                    tree.add(self.link(x, mu))
                    queue.append(y)
                z = self.shift(x, mu, -1)
                if z not in seen:
                    seen.add(z)
                    tree.add(self.link(z, mu))
                    queue.append(z)
        assert len(tree) == self.V - 1
        return tree

    def translate_face(self, f, t):
        x, mu, nu = self.faces[f]
        y = tuple((x[i] + t[i]) % self.dims[i] for i in range(self.d))
        return self.fid[(y, mu, nu)]


def holonomy(word, vals):
    h = G.e
    for l, s in word:
        v = vals[l]
        h = G.mult[h][v if s > 0 else G.inv[v]]
    return h


def plaquettes(lat, vals):
    return [holonomy(w, vals) for w in lat.fwords]


def energy(lat, vals):
    return sum(G.cost[h] for h in plaquettes(lat, vals))


def section_geometry(lat):
    # each face has four distinct links; in d=3 each link lies on 2(d-1)=4 faces; there are 3V faces.
    ok = lat.nfaces == lat.V * 3 and all(len(set(l for l, _ in w)) == 4 for w in lat.fwords)
    ok = ok and all(len(fs) == 2 * (lat.d - 1) for fs in lat.link_faces)
    check(ok, "dropped_face")


# ---------------------------------------------------------------- the cube Bianchi identity
# For the cube at x with axes 0,1,2: loops based at x. A far face is carried to x by the link that leaves x towards it.
#   B(x) = F01(x)^-1 . [U0 F12(x+0) U0^-1] . F02(x) . [U2 F01(x+2) U2^-1] . F12(x)^-1 . [U1 F02(x+1) U1^-1]^-1 = e.
def cube_terms(lat, x):
    def tether(mu, f):
        t = [(lat.link(x, mu), 1)]
        if SABOTAGE == "broken_transport" and mu == 2:
            t = []  # the far face xy at x+2 used without carrying it back to x
        return t + f + [(l, -s) for l, s in reversed(t)]
    F = lambda y, mu, nu: lat.word(y, mu, nu)  # noqa: E731
    return [
        (F(x, 0, 1), -1),
        (tether(0, F(lat.shift(x, 0), 1, 2)), 1),
        (F(x, 0, 2), 1),
        (tether(2, F(lat.shift(x, 2), 0, 1)), 1),
        (F(x, 1, 2), -1),
        (tether(1, F(lat.shift(x, 1), 0, 2)), -1),
    ]


def free_reduce(word):
    out = []
    for t in word:
        if out and out[-1][0] == t[0] and out[-1][1] == -t[1]:
            out.pop()
        else:
            out.append(t)
    return out


def cube_word(lat, x):
    w = []
    for loop, s in cube_terms(lat, x):
        w += loop if s > 0 else [(l, -t) for l, t in reversed(loop)]
    return w


def bianchi_holds(lat, vals):
    return all(holonomy(cube_word(lat, x), vals) == G.e for x in lat.sites)


def section_bianchi_identity(lat):
    # The cube word reduces to the empty word in the free group on the links: it is e for every configuration.
    empty = all(not free_reduce(cube_word(lat, x)) for x in lat.sites)
    check(empty, "broken_transport")
    # and evaluated on pseudo-random configurations (an LCG, the same on every Python)
    state = 20261110
    for _ in range(3):
        vals = []
        for _ in range(lat.nlinks):
            state = (state * 6364136223846793005 + 1442695040888963407) % 18446744073709551616
            vals.append((state >> 33) % G.n)
        check(bianchi_holds(lat, vals), "broken_transport")
    return 1


# ---------------------------------------------------------------- the complete solver (maximal-tree gauge)
class Solver:
    """All tree-gauge-fixed link configurations with: every face outside `free` equal to its target (default e);
    every face in `free` non-identity, with total cost of the free faces <= cap. Forced values come from faces with one
    unknown link; every other unknown is branched over all six elements, so the enumeration is complete."""

    def __init__(self, lat, free=(), target=None, cap=None, limit=None):
        self.lat = lat
        self.free = set(free)
        self.target = target or {}
        self.cap = cap
        self.limit = limit
        self.vals = [-1] * lat.nlinks
        self.cnt = [4] * lat.nfaces
        self.cost = 0
        self.solutions = []
        self.nodes = 0
        for l in lat.tree:
            self.vals[l] = G.e
            for f in lat.link_faces[l]:
                self.cnt[f] -= 1

    def tgt(self, f):
        return self.target.get(f, G.e)

    def assign(self, l, g, trail):
        lat = self.lat
        self.vals[l] = g
        trail.append(("v", l))
        stack = [l]
        while stack:
            l = stack.pop()
            for f in lat.link_faces[l]:
                self.cnt[f] -= 1
                trail.append(("c", f))
                c = self.cnt[f]
                if c == 0:
                    h = holonomy(lat.fwords[f], self.vals)
                    if f in self.free:
                        if h == G.e:
                            return False
                        self.cost += G.cost[h]
                        trail.append(("e", G.cost[h]))
                        if self.cap is not None and self.cost > self.cap:
                            return False
                    elif h != self.tgt(f):
                        return False
                elif c == 1 and f not in self.free:
                    # solve A . X^s . B = target for the one unknown link X
                    w = lat.fwords[f]
                    unknown = [i for i, (m, _) in enumerate(w) if self.vals[m] < 0]
                    if len(unknown) != 1:
                        continue  # a forced value not yet propagated; the face is read when its count reaches 0
                    k = unknown[0]
                    A = holonomy(w[:k], self.vals)
                    B = holonomy(w[k + 1:], self.vals)
                    xs = G.mult[G.mult[G.inv[A]][self.tgt(f)]][G.inv[B]]
                    m, s = w[k]
                    x = xs if s > 0 else G.inv[xs]
                    self.vals[m] = x
                    trail.append(("v", m))
                    stack.append(m)
        return True

    def undo(self, trail, mark):
        while len(trail) > mark:
            kind, v = trail.pop()
            if kind == "v":
                self.vals[v] = -1
            elif kind == "c":
                self.cnt[v] += 1
            else:
                self.cost -= v

    def pick(self):
        best, bestc = -1, 99
        for f in range(self.lat.nfaces):
            c = self.cnt[f]
            if 0 < c < bestc and f not in self.free:
                best, bestc = f, c
                if c == 1:
                    break
        if best >= 0:
            for l, _ in self.lat.fwords[best]:
                if self.vals[l] < 0:
                    return l
        for l in range(self.lat.nlinks):
            if self.vals[l] < 0:
                return l
        return -1

    def run(self):
        trail = []
        # tree links may already complete faces: check them through a zero-length start
        for f in range(self.lat.nfaces):
            if self.cnt[f] == 0:
                h = holonomy(self.lat.fwords[f], self.vals)
                if f in self.free:
                    if h == G.e:
                        return self.solutions
                    self.cost += G.cost[h]
                elif h != self.tgt(f):
                    return self.solutions
        self.dfs(trail)
        return self.solutions

    def dfs(self, trail):
        self.nodes += 1
        if self.limit is not None and len(self.solutions) >= self.limit:
            return
        l = self.pick()
        if l < 0:
            self.solutions.append(tuple(self.vals))
            return
        for g in range(G.n):
            mark = len(trail)
            if self.assign(l, g, trail):
                self.dfs(trail)
            self.undo(trail, mark)


def orbit_key(vals):
    return min(tuple(G.conj(g, v) for v in vals) for g in range(G.n))


def gauge_orbits(sols):
    if SABOTAGE == "missing_gauge_orbit":
        return len(set(sols))
    return len({orbit_key(s) for s in sols})


def winding(lat, vals, mu):
    # holonomy along the straight line from the origin in direction mu
    h, x = G.e, lat.sites[0]
    for _ in range(lat.dims[mu]):
        h = G.mult[h][vals[lat.link(x, mu)]]
        x = lat.shift(x, mu)
    return h


def corner_config(lat, hol):
    # U_mu(x) = hol[mu] on the links with x_mu = L_mu - 1, e elsewhere. Flat iff the hol[mu] commute pairwise.
    vals = [G.e] * lat.nlinks
    for x in lat.sites:
        for mu in range(lat.d):
            if x[mu] == lat.dims[mu] - 1:
                vals[lat.link(x, mu)] = hol[mu]
    return vals


def section_flat(lat, triples, orbits_alg):
    sols = Solver(lat).run()
    for s in sols:
        check(all(h == G.e for h in plaquettes(lat, s)), "flat_solver")
        check(bianchi_holds(lat, s), "broken_transport")
    wind = sorted(tuple(winding(lat, s, mu) for mu in range(3)) for s in sols)
    # every algebraically counted triple must be realized as a flat periodic link configuration
    for t in triples:
        check(all(h == G.e for h in plaquettes(lat, corner_config(lat, t))), "noncommuting_triple")
    check(len(sols) == len(triples) and wind == sorted(triples), "noncommuting_triple")
    orb = gauge_orbits(sols)
    check(orb == orbits_alg, "missing_gauge_orbit")
    return len(sols), orb


# ---------------------------------------------------------------- explicit excitations from links
def four_face(lat):
    vals = [G.e] * lat.nlinks
    vals[lat.link(lat.sites[0], 0)] = G.index[(1, 0, 2)]
    return vals


def tube(lat, rho, a, b):
    # winding tube along rho: in every slice x_rho = t, holonomies a, b along the two transverse axes (corner links).
    mu, nu = [m for m in range(3) if m != rho]
    hol = [G.e] * 3
    hol[mu], hol[nu] = a, b
    return corner_config(lat, hol)


def report_config(lat, vals):
    rows = []
    for x in lat.sites:
        for mu in range(lat.d):
            v = vals[lat.link(x, mu)]
            if v != G.e:
                rows.append("U%d(%s)=%s" % (mu, "".join(str(c) for c in x), G.name(v)))
    return ";".join(rows)


def faces_text(lat, vals):
    ps = plaquettes(lat, vals)
    out = []
    for f, h in enumerate(ps):
        if h != G.e:
            x, mu, nu = lat.faces[f]
            out.append("P%d%d(%s)=%s" % (mu, nu, "".join(str(c) for c in x), G.kind[h]))
    return ";".join(out)


def local_bianchi_of_flux(lat, flux):
    # A flux arrangement alone (face -> element) checked against the cube identity with every transport set to e.
    for x in lat.sites:
        h = G.e
        for loop, s in cube_terms(lat, x):
            # the face of each term is the 4-letter core; its flux value with trivial transport
            core = loop[1:5] if len(loop) == 6 else loop
            f = [i for i, w in enumerate(lat.fwords) if w == core][0]
            v = flux.get(f, G.e)
            h = G.mult[h][v if s > 0 else G.inv[v]]
        if h != G.e:
            return False
    return True


def reconstruct(lat, flux):
    return Solver(lat, target=flux, limit=1).run()


# ---------------------------------------------------------------- kappa by complete search
def bianchi_admissible(lat, support, cube_faces):
    # Necessary (proved from the cube identity, NOTE section 3): no cube holds exactly one non-identity face.
    sset = set(support)
    return all(len(sset & cf) != 1 for cf in cube_faces)


def kappa_search(lat, prefilter):
    cube_faces = []
    for x in lat.sites:
        fs = set()
        for loop, _ in cube_terms(lat, x):
            core = loop[1:5] if len(loop) == 6 else loop
            fs.add([i for i, w in enumerate(lat.fwords) if w == core][0])
        cube_faces.append(fs)
    translations = lat.sites
    supports_tried = 0
    found = []  # (E, solution)
    nodes = 0
    for k in (1, 2, 3):
        for first in range(3):  # a canonical support holds a face at the origin site
            for rest in itertools.combinations(range(first + 1, lat.nfaces), k - 1):
                sup = (first,) + rest
                canon = min(tuple(sorted(lat.translate_face(f, t) for f in sup)) for t in translations)
                if canon != sup:
                    continue
                if prefilter and not bianchi_admissible(lat, sup, cube_faces):
                    continue
                supports_tried += 1
                sv = Solver(lat, free=sup, cap=BOUND - 1)
                for s in sv.run():
                    found.append((energy(lat, s), sup, s))
                nodes += sv.nodes
    return supports_tried, nodes, found


def section_kappa(lat):
    four = four_face(lat)
    e4 = energy(lat, four)
    check(e4 == 8 and bianchi_holds(lat, four), "four_face")
    rows = []
    results = {}
    for prefilter in ((False, True) if lat.dims in FULL_ENUMERATION else (True,)):
        tried, nodes, found = kappa_search(lat, prefilter)
        for E, sup, s in found:
            check(bianchi_holds(lat, s), "broken_transport")
            check(energy(lat, s) == E and E < BOUND, "kappa_search")
        results[prefilter] = (tried, nodes, found)
    if len(results) == 2:
        a = sorted((E, s) for E, _, s in results[False][2])
        b = sorted((E, s) for E, _, s in results[True][2])
        check(a == b, "prefilter_agreement")
    tried, nodes, found = results[True]
    below = [E for E, _, _ in found]
    kappa = min(below) if below else 8
    minimizers = [s for E, _, s in found if E == kappa] if below else []
    # Every nonflat solution with E < 8 was searched; kappa is attained by an explicit configuration from links.
    if below:
        witness = minimizers[0]
    else:
        witness = four
    check(energy(lat, witness) == kappa and any(h != G.e for h in plaquettes(lat, witness)), "kappa_witness")
    orbits = gauge_orbits(minimizers) if minimizers else 0
    conj = min(8, 3 * min(lat.dims))
    rows.append((tried, nodes, kappa, len(minimizers), orbits, conj, witness, results))
    return rows[0]


# ---------------------------------------------------------------- SU(2) comparison (repository quaternions)
Q = su2.quat
QONE = su2.ONE
QI, QJ, QK = Q(0, 1, 0, 0), Q(0, 0, 1, 0), Q(0, 0, 0, 1)
QMINUS = Q(-1, 0, 0, 0)


def rot(n, axis):
    # exact unit quaternion on the rational circle: ((n^2-1) + 2n e_axis) / (n^2+1), half trace -> 1 as n grows
    c = [n * n - 1, 0, 0, 0]
    c[axis] = 2 * n
    return Q(c[0], c[1], c[2], c[3], n * n + 1)


def qcomm(a, b):
    return su2.multiply(su2.multiply(su2.multiply(a, b), su2.inverse(a)), su2.inverse(b))


def q_plaquettes(lat, vals):
    out = []
    for w in lat.fwords:
        h = QONE
        for l, s in w:
            h = su2.multiply(h, vals[l] if s > 0 else su2.inverse(vals[l]))
        out.append(h)
    return out


def rr(n, d):
    g = math.gcd(n, d)
    return (n // g, d // g)


def rsub(a, b):
    n, d = a[0] * b[1] - b[0] * a[1], a[1] * b[1]
    g = math.gcd(n, d)
    return (n // g, d // g)


def radd(a, b):
    n, d = a[0] * b[1] + b[0] * a[1], a[1] * b[1]
    g = math.gcd(n, d)
    return (n // g, d // g)


def q_cost(ps, twist=None):
    # sum over faces of (2 - Tr U_P) = sum 2(1 - half trace), as a reduced integer pair; twist multiplies U_P by z_P
    total = (0, 1)
    for f, p in enumerate(ps):
        if twist and f in twist:
            p = su2.multiply(p, QMINUS)
        h = su2.half_trace(p)
        total = radd(total, rsub((2, 1), (2 * h[0], h[1])))
    return total


def q_corner(lat, hol):
    vals = [QONE] * lat.nlinks
    for x in lat.sites:
        for mu in range(lat.d):
            if x[mu] == lat.dims[mu] - 1:
                vals[lat.link(x, mu)] = hol[mu]
    return vals


def kernel_of_commutator(a):
    # the real-linear map c -> a c - c a on the basis 1, i, j, k; returns the basis vectors it kills
    basis = [Q(1, 0, 0, 0), QI, QJ, QK]
    killed = []
    for k, e in enumerate(basis):
        d = [x - y for x, y in zip(su2.multiply(a, e)[:4], su2.multiply(e, a)[:4])]
        if d == [0, 0, 0, 0]:
            killed.append(k)
    return killed


def section_su2():
    lat = Lattice((3, 3, 3))
    rows = []
    # (1) local small-action family: one link rot(n), all others 1. Four faces move; E_n = 16/(n^2+1) -> 0.
    fam = []
    for n in (2, 3, 10, 100, 1000, 10 ** 6):
        vals = [QONE] * lat.nlinks
        vals[lat.link(lat.sites[0], 0)] = rot(n, 1)
        ps = q_plaquettes(lat, vals)
        moved = sum(1 for p in ps if p != QONE)
        E = q_cost(ps)
        check(moved == 4 and E == rr(16, n * n + 1) and su2.is_unit(rot(n, 1)), "su2_small_action")
        fam.append("%d:%d/%d" % (n, E[0], E[1]))
    rows.append("SU2_SMALL_ACTION|lattice=3x3x3|family=one_link_U=((n^2-1)+2n*i)/(n^2+1)|nonflat_faces=4|"
                "E_n=sum(2-Tr_U_P)=16/(n^2+1)|E_by_n=%s|inf_above_flat=0|positive_lock_cost=NOT_APPLICABLE|json=0" % ",".join(fam))
    # same on the repository's 2^4 lattice with its own plaquettes, Wilson action and gauge transform
    wil = []
    for n in (2, 10, 1000):
        U = {(x, mu): su2.ONE for x in su2.SITES for mu in range(su2.D)}
        U[(su2.SITES[0], 0)] = rot(n, 1)
        P = su2.all_plaquettes(U)
        S = su2.wilson_action(P, beta=(1, 1))
        Ug, g = su2.links_and_gauge(n)
        Pt = su2.all_plaquettes(su2.gauge_transform(U, g))
        check(S == rr(12, n * n + 1) and su2.wilson_action(Pt, beta=(1, 1)) == S and su2.covariance_holds(P, Pt, g), "su2_small_action")
        wil.append("%d:%d/%d" % (n, S[0], S[1]))
    rows.append("SU2_SMALL_ACTION_4D_REPO|lattice=2^4|code=tests/test_exact_su2_4d.py|S_W(beta=1)=12/(n^2+1)|S_by_n=%s|"
                "gauge_invariant_under_its_gauge_transform=1|json=0" % ",".join(wil))
    # (2) small winding flux: corner holonomies a_n=rot(n,i), b_n=rot(n,j); one face per slice with U=[a_n,b_n].
    tub = []
    for n in (2, 10, 1000):
        a, b = rot(n, 1), rot(n, 2)
        c = qcomm(a, b)
        check(c != QONE, "su2_winding")
        vals = q_corner(lat, [a, b, QONE])
        ps = q_plaquettes(lat, vals)
        moved = [p for p in ps if p != QONE]
        E = q_cost(ps)
        check(len(moved) == 3 and all(p == c for p in moved), "su2_winding")
        tub.append("%d:%d/%d" % (n, E[0], E[1]))
    rows.append("SU2_WINDING_FLUX|lattice=3x3x3|holonomies=a_n=((n^2-1)+2n*i)/(n^2+1),b_n=((n^2-1)+2n*j)/(n^2+1)|"
                "faces_per_slice=1|slices=3|face_holonomy=[a_n,b_n]|E_by_n=%s|winding_cost_lower_bound=0|json=0" % ",".join(tub))
    # (3) continuous flat family in one maximal torus: pairwise non-conjugate (distinct half traces), all faces exactly 1
    flats = []
    for n in (2, 3, 4, 5, 7, 11):
        hol = [rot(n, 1), rot(n + 1, 1), rot(n + 2, 1)]
        ps = q_plaquettes(lat, q_corner(lat, hol))
        check(all(p == QONE for p in ps), "su2_flat_family")
        flats.append(su2.half_trace(hol[0]))
    check(len(set(flats)) == len(flats), "su2_flat_family")
    rows.append("SU2_FLAT_FAMILY|lattice=3x3x3|triples_in_one_U(1)=6|all_plaquettes_exactly_1=1|pairwise_nonconjugate_by_half_trace=1|"
                "half_traces=%s|flat_set=continuous_family_not_a_finite_set|json=0" % ",".join("%d/%d" % h for h in flats))
    # (4) the 't Hooft twisted sector, a separate labeled object: (a,b,c)=(i,j,+-1), ab=-ba.
    check(su2.multiply(QI, QJ) == su2.multiply(QMINUS, su2.multiply(QJ, QI)) and qcomm(QI, QJ) == QMINUS, "twisted")
    cent = sorted(set(kernel_of_commutator(QI)) & set(kernel_of_commutator(QJ)))
    check(cent == [0], "twisted")
    twisted = []
    for c in (QONE, QMINUS):
        vals = q_corner(lat, [QI, QJ, c])
        ps = q_plaquettes(lat, vals)
        tw = {f for f, p in enumerate(ps) if p == QMINUS}
        # twisted-flat: every U_P z_P = 1 with z_P = -1 on the twist faces (one 01-face per slice)
        ok = len(tw) == 3 and all(lat.faces[f][1:] == (0, 1) for f in tw) and q_cost(ps, twist=tw) == (0, 1)
        check(ok, "twisted")
        untw = q_cost(ps)
        twisted.append((vals, ps, untw))
    rows.append("SU2_TWISTED_SECTOR|label=TWISTED_n01=1|lattice=3x3x3|holonomies=(i,j,c)_c=+1,-1|ij=-ji=1|[i,j]=-1|"
                "centralizer_of_{i,j}=R*1_so_c=+1,-1|twisted_flat=2|as_untwisted_periodic_E=%d/%d|counted_as_periodic_flat=0|"
                "kept_separate=1|json=0" % twisted[0][2])
    # the periodic flat list: ordinary periodic configurations only. A twisted configuration must fail the periodic flatness.
    periodic = [q_corner(lat, [rot(2, 1), rot(3, 1), rot(4, 1)])]
    if SABOTAGE == "twisted_as_periodic":
        periodic.append(twisted[0][0])
    for vals in periodic:
        check(all(p == QONE for p in q_plaquettes(lat, vals)), "twisted_as_periodic")
    return rows


# ---------------------------------------------------------------- 2D control (brute force, all configurations)
def section_2d():
    out = []
    for dims in ((2, 2), (2, 3)):
        lat = Lattice(dims)
        free = [l for l in range(lat.nlinks) if l not in lat.tree]
        vals = [G.e] * lat.nlinks
        flat, best, nbest, total = [], 99, 0, 0
        for t in itertools.product(range(G.n), repeat=len(free)):
            for l, g in zip(free, t):
                vals[l] = g
            total += 1
            E = energy(lat, vals)
            if E == 0:
                flat.append(tuple(vals))
            elif E < best:
                best, nbest = E, 1
            elif E == best:
                nbest += 1
        dfs = Solver(lat).run()
        check(sorted(dfs) == sorted(flat), "flat_solver")
        orb = gauge_orbits(flat)
        check(orb == 8, "missing_gauge_orbit")
        check(len(flat) == 18 and best == 3, "two_torus")
        # the support solver on the nonflat side: one free face, cost cap 3, summed over every face, against brute force
        by_support = sum(len(Solver(lat, free=(f,), cap=3).run()) for f in range(lat.nfaces))
        check(by_support == nbest, "kappa_search")
        out.append("TWO_TORUS|lattice=%dx%d|tree_fixed_configurations=%d|flat=%d|flat_orbits=%d|kappa_2D=%d|minimizers=%d|"
                   "solver_flat_set_equal_to_brute_force=1|support_solver_minimizers=%d|equal=1|json=0"
                   % (dims[0], dims[1], total, len(flat), orb, best, nbest, by_support))
    return out


# ---------------------------------------------------------------- main
def main():
    if not __debug__:
        raise SystemExit("assertions are off: run without -O")
    print("YM4_06A_BEGIN|scope=STRUCTURE_ONLY|group_finite=S3|group_continuous=SU2|spatial_dimension=3|arithmetic=EXACT_INTEGER|"
          "spectrum_computed=0|gap_computed=0|issue_6=SEPARATE|json=0")
    section_characters()
    pairs, triples = commuting_tuples(2), commuting_tuples(3)
    o2, o3 = conj_orbits(pairs), conj_orbits(triples)
    b2, b3 = burnside(2), burnside(3)
    check(len(triples) == 48 and len(pairs) == 18, "noncommuting_triple")
    check(o3 == b3 == 21 and o2 == b2 == 8, "missing_gauge_orbit")
    print("S3_FLAT_ALGEBRA|commuting_pairs=%d|pair_orbits=%d|burnside_pairs=%d|commuting_triples=%d|triple_orbits=%d|burnside_triples=%d|json=0"
          % (len(pairs), o2, b2, len(triples), o3, b3))
    for row in section_2d():
        print(row)
    for dims in LATTICES:
        lat = Lattice(dims, drop_face=(SABOTAGE == "dropped_face" and dims == LATTICES[0]))
        section_geometry(lat)
        section_bianchi_identity(lat)
        nflat, orb = section_flat(lat, triples, b3)
        print("S3_FLAT_LATTICE|lattice=%dx%dx%d|links=%d|tree_links=%d|faces=%d|cubes=%d|cube_word_free_reduces_to_empty=%d|"
              "tree_fixed_flat_configurations=%d|windings_equal_commuting_triples=1|gauge_orbits=%d|json=0"
              % (dims + (lat.nlinks, len(lat.tree), lat.nfaces, lat.V, lat.V, nflat, orb)))
        tried, nodes, kappa, nmin, orbits, conj, witness, results = section_kappa(lat)
        full = results.get(False)
        full_text = "supports_without_prefilter=%d|solver_nodes_without_prefilter=%d|solutions_below_8_equal=1" % (full[0], full[1]) if full else "supports_without_prefilter=NOT_RUN"
        print("S3_KAPPA|lattice=%dx%dx%d|searched=every_nonflat_configuration_with_E<8|supports_bianchi_admissible=%d|%s|"
              "kappa_3D=%d|minimizers_tree_fixed=%d|minimizer_gauge_orbits=%d|conjecture_min(8,3*L_min)=%d|agree=%d|json=0"
              % (dims + (tried, full_text, kappa, nmin, orbits, conj, 1 if kappa == conj else 0)))
        print("S3_KAPPA_WITNESS|lattice=%dx%dx%d|E=%d|links=%s|nonflat_faces=%s|bianchi_every_cube=1|json=0"
              % (dims + (energy(lat, witness), report_config(lat, witness), faces_text(lat, witness))))
        e8 = four_face(lat)
        print("S3_FOUR_FACE|lattice=%dx%dx%d|links=%s|E=%d|nonflat_faces=%s|json=0"
              % (dims + (report_config(lat, e8), energy(lat, e8), faces_text(lat, e8))))
        for rho in range(3):
            tv = tube(lat, rho, G.index[(1, 0, 2)], G.index[(0, 2, 1)])
            Et = energy(lat, tv)
            ps = plaquettes(lat, tv)
            nf = [h for h in ps if h != G.e]
            check(Et == 3 * dims[rho] and len(nf) == dims[rho] and all(G.kind[h] == "3-cycle" for h in nf) and bianchi_holds(lat, tv), "tube")
            print("S3_TUBE|lattice=%dx%dx%d|axis=%d|L=%d|holonomies=a=(01),b=(12)|links=%s|nonflat_faces=%d_3-cycles|E=3L=%d|json=0"
                  % (dims + (rho, dims[rho], report_config(lat, tv), len(nf), Et)))
    # the flux-arrangement gate on the smallest lattice: a Bianchi-consistent arrangement without periodic links
    lat = Lattice((2, 2, 2))
    sw = G.index[(1, 0, 2)]
    zface = [lat.fid[((0, 0, z), 0, 1)] for z in range(2)]
    flux_t = {f: sw for f in zface}
    loc = local_bianchi_of_flux(lat, flux_t)
    rec = reconstruct(lat, flux_t)
    check(loc and not rec, "flux_gate")
    c3 = G.comm(G.index[(1, 0, 2)], G.index[(0, 2, 1)])
    rec3 = reconstruct(lat, {f: c3 for f in zface})
    check(rec3 and local_bianchi_of_flux(lat, {f: c3 for f in zface}), "flux_gate")
    print("FLUX_GATE|lattice=2x2x2|arrangement=two_stacked_01_faces_along_axis2|transposition_flux_local_bianchi=PASS|"
          "transposition_flux_periodic_links=0|status=NOT_REALIZABLE_finding|3-cycle_flux_local_bianchi=PASS|3-cycle_flux_periodic_links=FOUND|"
          "witness=%s|json=0" % report_config(lat, rec3[0]))
    claims = [("four_face", four_face(lat)), ("tube_3cycle", rec3[0])]
    if SABOTAGE == "unreconstructible_flux":
        claims.append(("tube_transposition", None))  # a cost claimed from the flux pattern alone
    for name, vals in claims:
        if vals is None:
            vals_list = reconstruct(lat, flux_t)
            check(bool(vals_list), "unreconstructible_flux")
            vals = vals_list[0]
        check(bianchi_holds(lat, vals), "unreconstructible_flux")
    for row in section_su2():
        print(row)
    print("YM4_06A_LIMITS|kappa_formula=MEASURED_on_listed_lattices_only|all_L_statement=CONJECTURE_with_written_argument_in_NOTE|"
          "S3_sectors_identified_with_SU2=0|SU2_positive_lock_cost=NOT_APPLICABLE|continuum_gap=NOT_CLAIMED|issue_6=OPEN|json=0")
    print("YM4_06A_DONE|status=PASS_STRUCTURE_ONLY|failed=0|json=0")


if __name__ == "__main__":
    main()
