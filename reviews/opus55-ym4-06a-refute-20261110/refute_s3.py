#!/usr/bin/env python3
"""Independent refuter for YM4-06A (S3 part). Own code, integers only, no fractions, no float.

Method (different from the PR's support-enumeration solver):
  * comb maximal tree (z-links, then y-links on z=0, then x-links on y=z=0) fixed to e;
  * ONE depth-first branch-and-bound over ALL free links of the whole lattice, static greedy order
    (next link = the one completing most faces), cost of every completed face added, branch cut when
    accumulated cost > BUDGET. No support enumeration, no translation reduction, no Bianchi filter.
  * completeness: every face is completed exactly once (at its last-ordered link) and its exact cost is
    added; costs are >= 0 so the cut is monotone; every free link is branched over all 6 elements
    unless a completed face's cost already exceeds budget. Hence every tree-fixed configuration with
    E <= BUDGET is emitted, and each emitted one is re-evaluated from scratch.
usage: refute_s3.py Lx Ly Lz [budget]
"""
import itertools
import sys

PERMS = list(itertools.permutations(range(3)))
IDX = {p: i for i, p in enumerate(PERMS)}
E_ = IDX[(0, 1, 2)]
MUL = [[IDX[tuple(a[b[i]] for i in range(3))] for b in PERMS] for a in PERMS]
INV = [next(b for b in range(6) if MUL[a][b] == E_) for a in range(6)]


def rep2(p):
    # standard rep on {v : sum v = 0}, basis f1 = e0 - e1, f2 = e1 - e2; integer 2x2 matrix
    def img(vec):  # vec as coefficients on e0,e1,e2 ; permutation acts e_i -> e_p(i)
        out = [0, 0, 0]
        for i in range(3):
            out[p[i]] += vec[i]
        return out
    cols = []
    for f in ([1, -1, 0], [0, 1, -1]):
        w = img(f)
        # w = c1 f1 + c2 f2 : c1 = w0, c2 = w0 + w1
        cols.append((w[0], w[0] + w[1]))
    return cols[0][0] + cols[1][1]  # trace


CHI = [rep2(p) for p in PERMS]
COST = [2 - c for c in CHI]
KIND = ["e" if c == 2 else ("transposition" if c == 0 else "3-cycle") for c in CHI]


class Lat:
    def __init__(self, dims):
        self.dims = dims
        Lx, Ly, Lz = dims
        self.sites = [(x, y, z) for x in range(Lx) for y in range(Ly) for z in range(Lz)]
        self.sid = {s: i for i, s in enumerate(self.sites)}
        self.N = len(self.sites)
        self.faces = []  # (x, mu, nu, [(link, sign)...])
        for s in self.sites:
            for mu, nu in ((0, 1), (0, 2), (1, 2)):
                l1 = self.lk(s, mu)
                l2 = self.lk(self.sh(s, mu), nu)
                l3 = self.lk(self.sh(s, nu), mu)
                l4 = self.lk(s, nu)
                self.faces.append((s, mu, nu, ((l1, 1), (l2, 1), (l3, -1), (l4, -1))))
        self.nl = 3 * self.N
        tree = set()
        for (x, y, z) in self.sites:
            if z < Lz - 1:
                tree.add(self.lk((x, y, z), 2))
            if z == 0 and y < Ly - 1:
                tree.add(self.lk((x, y, z), 1))
            if z == 0 and y == 0 and x < Lx - 1:
                tree.add(self.lk((x, y, z), 0))
        assert len(tree) == self.N - 1
        self.tree = tree

    def sh(self, s, mu, k=1):
        t = list(s)
        t[mu] = (t[mu] + k) % self.dims[mu]
        return tuple(t)

    def lk(self, s, mu):
        return 3 * self.sid[s] + mu

    def hol(self, vals, f):
        h = E_
        for l, sg in self.faces[f][3]:
            g = vals[l]
            h = MUL[h][g if sg == 1 else INV[g]]
        return h

    def energy(self, vals):
        return sum(COST[self.hol(vals, f)] for f in range(len(self.faces)))


def tree_is_spanning(lat):
    parent = list(range(lat.N))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for l in lat.tree:
        s = l // 3
        t = lat.sid[lat.sh(lat.sites[s], l % 3)]
        a, b = find(s), find(t)
        if a == b:
            return False
        parent[a] = b
    return len({find(i) for i in range(lat.N)}) == 1


def order_links(lat):
    face_links = [set(l for l, _ in f[3]) for f in lat.faces]
    assigned = set(lat.tree)
    remaining = [l for l in range(lat.nl) if l not in assigned]
    order = []
    done = [False] * len(lat.faces)
    for f in range(len(lat.faces)):
        if face_links[f] <= assigned:
            done[f] = True  # face made of tree links only
    pre_done = [f for f in range(len(lat.faces)) if done[f]]
    link_faces = {l: [] for l in range(lat.nl)}
    for f, fl in enumerate(face_links):
        for l in fl:
            link_faces[l].append(f)
    completes = []
    while remaining:
        best, bestc, bestp = None, [], -1
        for l in remaining:
            c = [f for f in link_faces[l] if not done[f] and face_links[f] <= assigned | {l}]
            # tie-break: link touching most partially-filled faces
            p = sum(1 for f in link_faces[l] if not done[f] and face_links[f] & assigned)
            key = (len(c), p)
            if best is None or key > (len(bestc), bestp):
                best, bestc, bestp = l, c, p
        order.append(best)
        completes.append(bestc)
        assigned.add(best)
        remaining.remove(best)
        for f in bestc:
            done[f] = True
    return order, completes, pre_done


def search(lat, budget):
    order, completes, pre_done = order_links(lat)
    vals = [E_] * lat.nl
    assert all(lat.hol(vals, f) == E_ for f in pre_done)
    faces = [f[3] for f in lat.faces]
    n = len(order)
    sols = []
    nodes = 0
    free_branch_positions = sum(1 for c in completes if not c)
    # iterative DFS
    stack_val = [0] * n
    stack_cost = [0] * (n + 1)
    depth = 0
    stack_val[0] = -1
    while depth >= 0:
        if depth == n:
            sols.append(tuple(vals))
            depth -= 1
            continue
        v = stack_val[depth] + 1
        l = order[depth]
        placed = False
        while v < 6:
            vals[l] = v
            c = stack_cost[depth]
            ok = True
            for f in completes[depth]:
                h = E_
                for ll, sg in faces[f]:
                    g = vals[ll]
                    h = MUL[h][g if sg == 1 else INV[g]]
                c += COST[h]
                if c > budget:
                    ok = False
                    break
            if ok:
                stack_val[depth] = v
                stack_cost[depth + 1] = c
                nodes += 1
                depth += 1
                if depth < n:
                    stack_val[depth] = -1
                placed = True
                break
            v += 1
        if not placed:
            vals[l] = E_
            depth -= 1
    return sols, nodes, free_branch_positions


def conj_all(g, vals):
    gi = INV[g]
    return tuple(MUL[MUL[g][a]][gi] for a in vals)


def orbits(sols):
    keys = set()
    for s in sols:
        keys.add(min(conj_all(g, s) for g in range(6)))
    return len(keys)


def support(lat, vals):
    return tuple(sorted(f for f in range(len(lat.faces)) if lat.hol(vals, f) != E_))


def canon_support(lat, sup):
    # lexicographically least translate (by face tuple (site, mu, nu)), the PR's convention
    best = None
    Lx, Ly, Lz = lat.dims
    fkey = {(f[0], f[1], f[2]): i for i, f in enumerate(lat.faces)}
    for t in lat.sites:
        tr = []
        for f in sup:
            s, mu, nu, _ = lat.faces[f]
            s2 = ((s[0] + t[0]) % Lx, (s[1] + t[1]) % Ly, (s[2] + t[2]) % Lz)
            tr.append((s2, mu, nu))
        tr = tuple(sorted(tr))
        if best is None or tr < best:
            best = tr
    return best


def main():
    dims = tuple(int(a) for a in sys.argv[1:4])
    budget = int(sys.argv[4]) if len(sys.argv) > 4 else 7
    lat = Lat(dims)
    assert tree_is_spanning(lat)
    sols, nodes, fb = search(lat, budget)
    tag = "%dx%dx%d" % dims
    # re-evaluate every solution from scratch
    energies = {}
    for s in sols:
        en = lat.energy(s)
        assert en <= budget
        energies.setdefault(en, []).append(s)
    flat = energies.get(0, [])
    nonflat_E = sorted(k for k in energies if k > 0)
    print("S3_SEARCH|lattice=%s|method=global_dfs_all_free_links_comb_tree|free_links=%d|free_branch_positions=%d|budget=%d|nodes=%d|solutions=%d|json=0"
          % (tag, lat.nl - len(lat.tree), fb, budget, nodes, len(sols)))
    print("S3_FLAT|lattice=%s|tree_fixed_flat=%d|gauge_orbits=%d|json=0" % (tag, len(flat), orbits(flat)))
    for en in nonflat_E:
        group = energies[en]
        sups = {}
        for s in group:
            sups.setdefault(support(lat, s), []).append(s)
        canon = {}
        for sp, ss in sups.items():
            canon.setdefault(canon_support(lat, sp), []).append((sp, ss))
        # per canonical support (only the translate that IS the lex-least one): PR-comparable counts
        per_tf = 0
        per_orb = 0
        for c, lst in canon.items():
            for sp, ss in lst:
                key = tuple(sorted((lat.faces[f][0], lat.faces[f][1], lat.faces[f][2]) for f in sp))
                if key == c:
                    per_tf += len(ss)
                    per_orb += orbits(ss)
        kinds = sorted(set(tuple(sorted(KIND[lat.hol(s, f)] for f in support(lat, s))) for s in group))
        print("S3_NONFLAT|lattice=%s|E=%d|tree_fixed_all_translates=%d|gauge_orbits_all_translates=%d|supports=%d|canonical_supports=%d|canonical_tree_fixed=%d|canonical_orbits=%d|face_kinds=%s|json=0"
              % (tag, en, len(group), orbits(group), len(sups), len(canon), per_tf, per_orb,
                 ";".join(",".join(k) for k in kinds)))
        for c in sorted(canon):
            print("S3_SUPPORT|lattice=%s|E=%d|canonical=%s|json=0" % (tag, en, ";".join("P%d%d(%d%d%d)" % (m, n_, *s) for s, m, n_ in c)))
    kappa = nonflat_E[0] if nonflat_E else "GT%d" % budget
    print("S3_KAPPA_REFUTER|lattice=%s|kappa_below_or_eq_budget=%s|json=0" % (tag, kappa))


if __name__ == "__main__":
    main()
