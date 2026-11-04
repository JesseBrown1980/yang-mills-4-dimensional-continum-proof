# Independent toolkit for attacking NOTE-YM4-02c-SITE-SIGN. Shares no code with tests/test_site_sign_4d.py.
# Integers only. Groups come from permutations, matrices mod p, or direct products, closed by BFS from generators.
import itertools


class FG:
    """A finite group from generators and a multiplication on hashable elements."""

    def __init__(self, name, gens, mul, one):
        self.name = name
        elems = [one]
        seen = {one: 0}
        frontier = [one]
        while frontier:
            nxt = []
            for x in frontier:
                for g in gens:
                    y = mul(x, g)
                    if y not in seen:
                        seen[y] = len(elems)
                        elems.append(y)
                        nxt.append(y)
            frontier = nxt
        self.elems = elems
        self.n = len(elems)
        self.seen = seen
        self.gen_idx = [seen[g] for g in gens]
        self.tab = [[seen[mul(x, y)] for y in elems] for x in elems]
        self.one = 0
        self.inv = [0] * self.n
        for i in range(self.n):
            row = self.tab[i]
            self.inv[i] = row.index(0)
        self._classes()
        self._homs()

    def _classes(self):
        # conjugacy classes by BFS under generator conjugation, then union with inverse
        cl = [-1] * self.n
        classes = []
        for i in range(self.n):
            if cl[i] >= 0:
                continue
            c = len(classes)
            cl[i] = c
            members = [i]
            stack = [i]
            while stack:
                x = stack.pop()
                for g in self.gen_idx:
                    y = self.tab[self.tab[g][x]][self.inv[g]]
                    if cl[y] < 0:
                        cl[y] = c
                        members.append(y)
                        stack.append(y)
            classes.append(sorted(members))
        self.conj_classes = classes
        self.conj_of = cl
        # merge c with class of inverse
        parent = list(range(len(classes)))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        for c, ms in enumerate(classes):
            a, b = find(c), find(cl[self.inv[ms[0]]])
            if a != b:
                parent[a] = b
        roots = {}
        self.mc_of = [0] * self.n
        for i in range(self.n):
            r = find(cl[i])
            if r not in roots:
                roots[r] = len(roots)
            self.mc_of[i] = roots[r]
        self.nmc = len(roots)
        self.mc_size = [0] * self.nmc
        for i in range(self.n):
            self.mc_size[self.mc_of[i]] += 1

    def _homs(self):
        # Homs to Z/2 from generator assignments, each extended along the Cayley graph, verified on every edge.
        homs = set()
        r = len(self.gen_idx)
        for bits in itertools.product((0, 1), repeat=r):
            val = [-1] * self.n
            val[0] = 0
            stack = [0]
            ok = True
            while stack and ok:
                x = stack.pop()
                for gi, b in zip(self.gen_idx, bits):
                    y = self.tab[x][gi]
                    if val[y] < 0:
                        val[y] = val[x] ^ b
                        stack.append(y)
                    elif val[y] != val[x] ^ b:
                        ok = False
                        break
            if ok:
                homs.add(tuple(val))
        self.hom_vals = sorted(homs)
        self.hom_masks = []
        full = (1 << self.nmc) - 1
        for val in self.hom_vals:
            m = 0
            seen = {}
            for i in range(self.n):
                c = self.mc_of[i]
                if c in seen:
                    assert seen[c] == val[i], "a hom separated an inversion-closed class"
                seen[c] = val[i]
                if val[i]:
                    m |= 1 << c
            self.hom_masks.append(m)
        self.full = full
        self.rule = sorted(set(self.hom_masks + [m ^ full for m in self.hom_masks]))


def cyclic(n):
    return FG("Z%d" % n, [1 % n], lambda a, b: (a + b) % n, 0)


def direct(G, H):
    gens = [(g, 0) for g in G.gen_idx] + [(0, h) for h in H.gen_idx]
    return FG("%sx%s" % (G.name, H.name), gens, lambda a, b: (G.tab[a[0]][b[0]], H.tab[a[1]][b[1]]), (0, 0))


def pcomp(a, b):
    # (a*b)(i) = a(b(i))
    return tuple(a[b[i]] for i in range(len(a)))


def perm_group(name, gens):
    return FG(name, gens, pcomp, tuple(range(len(gens[0]))))


def mat_group(name, gens, p):
    def mul(a, b):
        return ((a[0] * b[0] + a[1] * b[2]) % p, (a[0] * b[1] + a[1] * b[3]) % p, (a[2] * b[0] + a[3] * b[2]) % p, (a[2] * b[1] + a[3] * b[3]) % p)

    return FG(name, gens, mul, (1, 0, 0, 1))


def S(n):
    a = tuple(list(range(1, n)) + [0])
    b = tuple([1, 0] + list(range(2, n)))
    return perm_group("S%d" % n, [a, b])


def A4():
    return perm_group("A4", [(1, 2, 0, 3), (1, 0, 3, 2)])


def A5():
    return perm_group("A5", [(1, 2, 3, 4, 0), (1, 2, 0, 3, 4)])


def D(n):
    # dihedral of order 2n acting on n points
    r = tuple((i + 1) % n for i in range(n))
    s = tuple((-i) % n for i in range(n))
    return perm_group("D%d" % n, [r, s])


def F21():
    # Z7 semidirect Z3, classes that inversion swaps
    r = tuple((i + 1) % 7 for i in range(7))
    t = tuple((2 * i) % 7 for i in range(7))
    return perm_group("F21", [r, t])


def F20():
    r = tuple((i + 1) % 5 for i in range(5))
    t = tuple((2 * i) % 5 for i in range(5))
    return perm_group("F20", [r, t])


def Q8_mat():
    # Q8 inside SL(2,3)
    i = (0, 2, 1, 0)
    j = (1, 1, 1, 2)
    return mat_group("Q8", [i, j], 3)


def SL23():
    return mat_group("SL23_2T", [(1, 1, 0, 1), (1, 0, 1, 1)], 3)


def SL25():
    return mat_group("SL25_2I", [(1, 1, 0, 1), (1, 0, 1, 1)], 5)


def GL23():
    return mat_group("GL23", [(1, 1, 0, 1), (1, 0, 1, 1), (2, 0, 0, 1)], 3)


def Dic3():
    # Z3 semidirect Z4 inside S3 x Z4 via (r,0),(s,1)
    s3 = S(3)
    z4 = cyclic(4)
    r = next(i for i in range(6) if i and s3.tab[s3.tab[i][i]][i] == 0)
    s = next(i for i in range(6) if i and s3.tab[i][i] == 0)
    return FG("Dic3", [(r, 0), (s, 1)], lambda a, b: (s3.tab[a[0]][b[0]], z4.tab[a[1]][b[1]]), (0, 0))


def TwoO():
    """The binary octahedral group as a subgroup of SL(2,7): order 48, class sizes 1,1,6,6,6,8,8,12."""
    p = 7
    els = []
    for a, b, c, d in itertools.product(range(p), repeat=4):
        if (a * d - b * c) % p == 1:
            els.append((a, b, c, d))

    def mul(x, y):
        return ((x[0] * y[0] + x[1] * y[2]) % p, (x[0] * y[1] + x[1] * y[3]) % p, (x[2] * y[0] + x[3] * y[2]) % p, (x[2] * y[1] + x[3] * y[3]) % p)

    one = (1, 0, 0, 1)

    def order(x):
        k, y = 1, x
        while y != one:
            y = mul(y, x)
            k += 1
        return k

    eights = [x for x in els if order(x) == 8]
    threes = [x for x in els if order(x) == 3]
    for a in eights:
        for b in threes:
            seen = {one}
            frontier = [one]
            big = False
            while frontier and not big:
                nxt = []
                for x in frontier:
                    for g in (a, b):
                        y = mul(x, g)
                        if y not in seen:
                            seen.add(y)
                            nxt.append(y)
                frontier = nxt
                if len(seen) > 48:
                    big = True
            if not big and len(seen) == 48:
                G = FG("2O_in_SL27", [a, b], mul, one)
                assert sorted(len(c) for c in G.conj_classes) == [1, 1, 6, 6, 6, 8, 8, 12]
                return G
    raise RuntimeError("no 2O found")


class Lat:
    """Periodic lattice with explicit path-traced plaquettes. word = [(link, +1 or -1)]*4, in the order walked from x."""

    def __init__(self, *dims):
        self.dims = dims
        self.k = len(dims)
        self.sites = list(itertools.product(*[range(d) for d in dims]))
        self.lid = {}
        self.links = []
        for x in self.sites:
            for mu in range(self.k):
                self.lid[(x, mu)] = len(self.links)
                self.links.append((x, mu))
        self.plaq = []
        self.words = []
        for x in self.sites:
            for mu in range(self.k):
                for nu in range(mu + 1, self.k):
                    self.plaq.append((x, mu, nu))
                    y = self.step(x, mu)
                    z = self.step(y, nu)
                    t = self.step(x, nu)
                    assert self.step(t, mu) == z
                    self.words.append(((self.lid[(x, mu)], 1), (self.lid[(y, nu)], 1), (self.lid[(t, mu)], -1), (self.lid[(x, nu)], -1)))

    def step(self, x, mu, d=1):
        y = list(x)
        y[mu] = (y[mu] + d) % self.dims[mu]
        return tuple(y)

    def tree(self):
        # BFS tree over sites using forward links, one link per non-origin site
        seen = {self.sites[0]}
        q = [self.sites[0]]
        tr = []
        while q:
            n = []
            for x in q:
                for mu in range(self.k):
                    y = self.step(x, mu)
                    if y not in seen:
                        seen.add(y)
                        tr.append(self.lid[(x, mu)])
                        n.append(y)
            q = n
        return tr


def hol(G, cfg, word):
    t, inv = G.tab, G.inv
    h = 0
    for l, e in word:
        v = cfg[l]
        h = t[h][v if e > 0 else inv[v]]
    return h


def parity_vec(G, lat, cfg):
    p = 0
    for w in lat.words:
        p ^= 1 << G.mc_of[hol(G, cfg, w)]
    return p


class RNG:
    def __init__(self, seed):
        self.s = (seed * 2654435761 + 88172645463325252) & ((1 << 64) - 1) or 1

    def below(self, n):
        # xorshift, integers only
        s = self.s
        s ^= (s << 13) & ((1 << 64) - 1)
        s ^= s >> 7
        s ^= (s << 17) & ((1 << 64) - 1)
        self.s = s
        return (s >> 11) % n


def rank_f2(vectors):
    basis = {}
    for v in vectors:
        while v:
            b = v.bit_length() - 1
            if b in basis:
                v ^= basis[b]
            else:
                basis[b] = v
                break
    return len(basis)


def popcount(x):
    return bin(x).count("1")


def constant_masks(nmc, parity_set):
    ps = list(parity_set)
    out = []
    for m in range(1 << nmc):
        vals = {popcount(m & p) & 1 for p in ps}
        if len(vals) == 1:
            out.append(m)
    return out


def exhaustive_parities(G, lat):
    """All parity vectors over the gauge-fixed set. Returns (dict parity -> count, number of free links)."""
    tr = set(lat.tree())
    free = [i for i in range(len(lat.links)) if i not in tr]
    cfg = [0] * len(lat.links)
    out = {}
    for vals in itertools.product(range(G.n), repeat=len(free)):
        for f, v in zip(free, vals):
            cfg[f] = v
        p = parity_vec(G, lat, cfg)
        out[p] = out.get(p, 0) + 1
    return out, len(free)


def sampled_parities(G, lat, target_rank, seed, max_draws):
    rng = RNG(seed)
    seen = set()
    base = None
    diffs = []
    rank = 0
    draws = 0
    while draws < max_draws and (rank < target_rank or draws < 512):
        draws += 1
        cfg = [rng.below(G.n) for _ in lat.links]
        p = parity_vec(G, lat, cfg)
        if p in seen:
            continue
        seen.add(p)
        if base is None:
            base = p
        else:
            diffs.append(p ^ base)
            if len(diffs) < 256 or rank < target_rank:
                rank = rank_f2(diffs)
    return seen, rank, draws
