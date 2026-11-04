# Reads tests/SITE_SIGN_RECEIPT.txt and the prediction, row by row, with its own exact arithmetic. Shares no code with the test. Integers only. json=0.
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep import Lat

WT = "C:/tmp/ym4-02c-sign-wt"
RECEIPT = [l.rstrip("\n") for l in open(WT + "/tests/SITE_SIGN_RECEIPT.txt", encoding="utf-8", newline="\n")]
PRED = [l.rstrip("\n") for l in open(WT + "/docs/PREDICTION-YM4-02c-SITE-SIGN.hbp", encoding="utf-8", newline="\n")]


def row(tag, **want):
    out = []
    for l in RECEIPT:
        if l.startswith(tag + "|"):
            d = dict(x.split("=", 1) for x in l.split("|")[1:] if "=" in x)
            if all(d.get(k) == v for k, v in want.items()):
                out.append((l, d))
    return out


# ---- Exact rings as tuples (a, b), value (a + b w) / 2, with w^2 = P w + Q. Coordinates of a quaternion are in this form.
class R:
    def __init__(self, P, Q):
        self.P, self.Q = P, Q

    def mul(self, x, y):
        a, b = x
        c, d = y
        # (a + b w)(c + d w) / 4 = (ac + bd Q + (ad + bc + bd P) w) / 4, returned as numerator over 2
        n0 = a * c + b * d * self.Q
        n1 = a * d + b * c + b * d * self.P
        return n0, n1


def qmul(ring, p, q):
    """(p0 + p1 i + p2 j + p3 k)(q0 + q1 i + q2 j + q3 k), written from the Hamilton formula."""
    m = ring.mul
    c = [[m(p[i], q[j]) for j in range(4)] for i in range(4)]

    def comb(terms):
        n0 = sum(s * c[i][j][0] for s, i, j in terms)
        n1 = sum(s * c[i][j][1] for s, i, j in terms)
        assert n0 % 2 == 0 and n1 % 2 == 0, "left the ring"
        return n0 // 2, n1 // 2

    r0 = comb([(1, 0, 0), (-1, 1, 1), (-1, 2, 2), (-1, 3, 3)])
    r1 = comb([(1, 0, 1), (1, 1, 0), (1, 2, 3), (-1, 3, 2)])
    r2 = comb([(1, 0, 2), (-1, 1, 3), (1, 2, 0), (1, 3, 1)])
    r3 = comb([(1, 0, 3), (1, 1, 2), (-1, 2, 1), (1, 3, 0)])
    return (r0, r1, r2, r3)


def qconj(p):
    return (p[0], (-p[1][0], -p[1][1]), (-p[2][0], -p[2][1]), (-p[3][0], -p[3][1]))


def neg(x):
    return (-x[0], -x[1])


Z0, ONE, TWO = (0, 0), (1, 0), (2, 0)


def build_list(name):
    q8 = []
    for axis in range(4):
        for sign in (1, -1):
            q8.append(tuple(((2 * sign, 0) if a == axis else Z0) for a in range(4)))
    hurwitz = [tuple(((s, 0)) for s in signs) for signs in itertools.product((1, -1), repeat=4)]
    if name == "Q8":
        return R(0, 0), q8
    if name == "2T":
        return R(0, 0), q8 + hurwitz
    if name == "2O":
        extra = []
        for a, b in itertools.combinations(range(4), 2):
            for s, t in itertools.product((1, -1), repeat=2):
                v = [Z0] * 4
                v[a] = (0, s)
                v[b] = (0, t)
                extra.append(tuple(v))
        return R(0, 2), q8 + hurwitz + extra
    if name == "2I":
        extra = []
        # even permutations of (0, +-1, +-1/phi, +-phi), doubled: 1 -> 2/2, and (a + b phi)/2 with 1/phi = phi - 1 -> (-1 + phi) -> coordinate (-1, 1) is doubled form of (phi-1)/2?
        # The doubled quaternion is q*2, so (0, 1, 1/phi, phi)/2 unit quaternion has doubled coordinates 0, 1, phi - 1, phi. In tuple form (a, b) means a + b phi.
        for perm in itertools.permutations(range(4)):
            inv = sum(1 for i in range(4) for j in range(i + 1, 4) if perm[i] > perm[j])
            if inv % 2:
                continue
            for s in itertools.product((1, -1), repeat=3):
                values = (Z0, (s[0], 0), (-s[1], s[1]), (0, s[2]))
                extra.append(tuple(values[perm[slot]] for slot in range(4)))
        return R(1, 1), q8 + hurwitz + extra
    raise ValueError(name)


class QG:
    def __init__(self, name):
        self.name = name
        self.ring, self.elems = build_list(name)
        self.n = len(self.elems)
        self.idx = {e: i for i, e in enumerate(self.elems)}
        assert len(self.idx) == self.n
        self.tab = [[self.idx[qmul(self.ring, x, y)] for y in self.elems] for x in self.elems]
        self.one = self.idx[(TWO, Z0, Z0, Z0)]
        self.inv = [self.idx[qconj(e)] for e in self.elems]
        assert all(self.tab[g][self.inv[g]] == self.one for g in range(self.n))
        # merged classes by union-find across every conjugation and inversion
        parent = list(range(self.n))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        for g in range(self.n):
            for h in range(self.n):
                a, b = find(g), find(self.tab[self.tab[h][g]][self.inv[h]])
                if a != b:
                    parent[a] = b
            a, b = find(g), find(self.inv[g])
            if a != b:
                parent[a] = b
        roots = {}
        self.mc = [0] * self.n
        for g in range(self.n):
            r = find(g)
            roots.setdefault(r, len(roots))
            self.mc[g] = roots[r]
        self.nmc = len(roots)
        # sign patterns that are homomorphisms, against the table
        self.homs = []
        for mask in range(1 << self.nmc):
            b = [(mask >> self.mc[g]) & 1 for g in range(self.n)]
            ok = True
            for x in range(self.n):
                rx = self.tab[x]
                bx = b[x]
                for y in range(self.n):
                    if b[rx[y]] != bx ^ b[y]:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                self.homs.append(mask)
        full = (1 << self.nmc) - 1
        self.rule = set(self.homs) | {m ^ full for m in self.homs}


def holo(G, cfg, word):
    h = G.one
    for l, e in word:
        v = cfg[l]
        h = G.tab[h][v if e > 0 else G.inv[v]]
    return h


GROUPS = {n: QG(n) for n in ("Q8", "2T", "2O", "2I")}
fails = 0


def report(name, ok, extra=""):
    global fails
    fails += 0 if ok else 1
    print("IND_RECEIPT_CHECK|%s|ok=%d%s|json=0" % (name, 1 if ok else 0, ("|" + extra) if extra else ""))


# ---- PATTERNS rows, read from the receipt against my tables and against the prediction rows.
for name, G in GROUPS.items():
    (l, d), = row("SITE_SIGN_PATTERNS", group=name)
    ok = int(d["inversion_closed_classes"]) == G.nmc and int(d["patterns"]) == 1 << G.nmc and int(d["homomorphisms_to_{+1,-1}"]) == len(G.homs) and int(d["constant_patterns"]) == len(G.rule)
    pr = "YM4_02C_SITE_SIGN_PATTERNS|group=%s|order=%d|inversion_closed_classes=%d|patterns=%d|homomorphisms_to_{+1,-1}=%d|constant_patterns=%d|json=0" % (name, G.n, G.nmc, 1 << G.nmc, len(G.homs), len(G.rule))
    report("PATTERNS_%s" % name, ok and pr in PRED, "classes=%d|homs=%d|rule=%d|prediction_row_exact=%d" % (G.nmc, len(G.homs), len(G.rule), 1 if pr in PRED else 0))


# ---- WITNESS rows, every one, read by my arithmetic on the indices the receipt prints.
def dims_from(name):
    if name == "(Z/2)^3":
        return (2, 2, 2)
    return tuple(int(p[3:-1]) for p in name.split("x"))


total_rows = 0
for l, d in row("SITE_SIGN_WITNESS"):
    total_rows += 1
    G = GROUPS[d["group"]]
    dims = dims_from(d["lattice"])
    lat = Lat(*dims)
    # my lattice lists links in the same site order and direction order as the test's documented link order
    configs = [[int(v) for v in w.split(".")] for w in d["witnesses"].split(";")]
    assert all(len(c) == len(lat.links) for c in configs)
    # the classes per plaquette
    parities = []
    for c in configs:
        p = 0
        for w in lat.words:
            p ^= 1 << G.mc[holo(G, c, w)]
        parities.append(p)
    both_all = True
    const_all = True
    F = len(lat.words)
    for mask in range(1 << G.nmc):
        vals = {bin(mask & p).count("1") & 1 for p in parities}
        if mask in G.rule:
            eps_minus = (mask >> G.mc[G.one]) & 1
            want = 1 if eps_minus and F % 2 else 0
            const_all = const_all and vals == {want}
        else:
            both_all = both_all and len(vals) == 2
    basis = {}
    rank = 0
    for p in parities[1:]:
        v = p ^ parities[0]
        while v:
            b = v.bit_length() - 1
            if b in basis:
                v ^= basis[b]
            else:
                basis[b] = v
                rank += 1
                break
    ok = both_all and const_all and rank == int(d["affine_dimension"]) and int(d["off_the_rule"]) == (1 << G.nmc) - len(G.rule) and int(d["off_rule_showing_both_values_of_S"]) == (1 << G.nmc) - len(G.rule)
    report("WITNESS_%s_%s" % (d["group"], d["lattice"]), ok, "plaquettes=%d|witnesses=%d|rank=%d|rule_patterns_constant_on_them=%d|off_rule_both_values=%d" % (F, len(configs), rank, 1 if const_all else 0, 1 if both_all else 0))
print("IND_WITNESS_ROWS|read=%d|json=0" % total_rows)


# ---- SU(2) rows: my own integer reduction of the printed palette indices and the printed g value.
PALETTE = None
(l, d), = row("SITE_SIGN_SU2_PALETTE")
PALETTE = []
for piece in d["palette"].split(";"):
    nums, den = piece.split("/")
    a, b, c, e = [int(x) for x in nums.split(",")]
    PALETTE.append((a, b, c, e, int(den)))
    assert a * a + b * b + c * c + e * e == int(den) ** 2


def qint(p, q):
    a, b, c, d, m = p
    e, f, g, h, n = q
    return (a * e - b * f - c * g - d * h, a * f + b * e + c * h - d * g, a * g - b * h + c * e + d * f, a * h + b * g - c * f + d * e, m * n)


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


for l, d in row("SITE_SIGN_SU2"):
    dims = dims_from(d["lattice"])
    lat = Lat(*dims)
    for key in ("g_+1", "g_-1"):
        value = d[key]
        pieces = {p.split("=", 1)[0]: p.split("=", 1)[1] for p in [key + "=" + value.split(":")[0]] + value.split(":")[1:]}
        top, bottom = [int(x) for x in pieces[key].split("/")]
        indices = [int(x) for x in pieces["palette_indices"].split(".")]
        prod_n, prod_d, negs = 1, 1, 0
        for w in lat.words:
            q = (1, 0, 0, 0, 1)
            for link, e in w:
                a, b, c, dd, n = PALETTE[indices[link]]
                if e < 0:
                    b, c, dd = -b, -c, -dd
                q = qint(q, (a, b, c, dd, n))
            prod_n *= q[0]
            prod_d *= q[4]
            negs += 1 if q[0] < 0 else 0
        g = gcd(prod_n, prod_d)
        rn, rd = prod_n // g, prod_d // g
        ok = rn == top and rd == bottom and negs == int(pieces["negative_a_p"]) and (rn > 0) == (key == "g_+1")
        report("SU2_%s_%s" % (d["lattice"], key), ok, "g=%d/%d|negative_a_p=%d" % (rn, rd, negs))


# ---- The prediction rows, row by row, against fields of the receipt.
def has(tag, field):
    return any(l.startswith(tag + "|") and (("|" + field + "|") in l or l.endswith("|" + field)) for l in RECEIPT)


checks = [
    ("ALREADY_SEEN class pairs", has("SITE_SIGN_SIDE_ONE_PAIRS", "class_pairs_on_+1,+1;+1,-1;-1,+1;-1,-1;i,i;j,j;k,k=320,192,192,320,1024,1024,1024")),
    ("ALREADY_SEEN five cases", bool(row("SITE_SIGN_FIVE_CASES", lattice="(Z/2)x(Z/2)"))),
    ("RULE exhaustive Q8", has("SITE_SIGN_EXHAUSTIVE", "constant_patterns=8") and has("SITE_SIGN_EXHAUSTIVE", "equal_to_plus_or_minus_homomorphisms=1") and has("SITE_SIGN_EXHAUSTIVE", "configurations_read=32768")),
    ("SIDE_ONE (Z/2)x(Z/1) configurations", has("SITE_SIGN_SIDE_ONE_PAIRS", "configurations=4096")),
    ("SIDE_ONE constant 16 of 32", has("SITE_SIGN_SIDE_ONE", "constant_patterns=16_of_32")),
    ("SIDE_ONE w 3,2,1,-1,2 constant", has("SITE_SIGN_SIDE_ONE", "w_3,2,1,-1,2=constant_1")),
    ("SIDE_ONE w 1,-1,1,1,1 negative 384", "w_1,-1,1,1,1=negative_product_384:negative_at_first_plaquette_512" in " ".join(l.split("|")[-3] if False else l for l in RECEIPT if l.startswith("SITE_SIGN_SIDE_ONE_WEIGHTS"))),
    ("SIDE_ONE corner configurations 64", has("SITE_SIGN_SIDE_ONE_CORNER", "configurations=64")),
    ("SIDE_ONE corner constant 16 of 32", has("SITE_SIGN_SIDE_ONE_CORNER", "constant_patterns=16_of_32")),
    ("SIDE_ONE corner literal 24 of 64 on all 16", has("SITE_SIGN_SIDE_ONE", "value_met_on_all_16_patterns=1")),
    ("MISS row present beside it", any(l.startswith("YM4_02C_SITE_SIGN_MISS|") for l in RECEIPT)),
    ("MISS row present in the prediction file", any(l.startswith("YM4_02C_SITE_SIGN_MISS|") for l in PRED)),
    ("ZEROS negative_S 0", has("SITE_SIGN_ZEROS_CENTRAL", "negative_S=0") and has("SITE_SIGN_ZEROS_GAUGE_FIXED", "negative_S=0")),
    ("ZEROS twist row", has("SITE_SIGN_ZEROS_TWIST", "lattice=(Z/2)^3:S=+1:negative_plaquettes=2") and has("SITE_SIGN_ZEROS_TWIST", "lattice=(Z/2)x(Z/2)x(Z/3):S=-1:negative_plaquettes=3") and has("SITE_SIGN_ZEROS_TWIST", "lattice=(Z/2)x(Z/2):S=-1:negative_plaquettes=1")),
    ("SU2 row both lattices", len(row("SITE_SIGN_SU2")) == 2),
    ("LIMITS runtime", has("SITE_SIGN_LIMITS", "runtime_within_600_seconds=1")),
    ("LIMITS stdlib", has("SITE_SIGN_LIMITS", "all_in_the_standard_library=1")),
    ("LIMITS integers_only read in the receipt", any("integers_only" in l for l in RECEIPT)),
    ("LIMITS gate read in the receipt", any("no_float_gate" in l for l in RECEIPT)),
    ("TEETH sabotage rows read in the receipt", any("sabotage" in l for l in RECEIPT)),
    ("DONE failed=0", "SITE_SIGN_DONE|failed=0|json=0" in RECEIPT),
]
for name, ok in checks:
    print("IND_PREDICTION_ROW|%s|found=%d|json=0" % (name.replace(" ", "_"), 1 if ok else 0))
print("IND_RECEIPT_DONE|failures_in_group_witness_su2_reads=%d|json=0" % fails)
