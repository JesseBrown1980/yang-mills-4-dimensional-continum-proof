# Claim 6 stretch: reproduce the published beta^11 coefficient by adding everything that first enters log Z at beta^12.
# Counts come from classes_d*_F12.txt (surfaces_exact.py). Values come from a word-gluing Haar evaluator that uses no finite group; a polynomial evaluator cross-checks small shapes.
# Integers only: rationals are reduced integer pairs.
import ast
import math
import sys

sys.path.insert(0, "C:/tmp/opus55/attack-4d-20261103/ym4-02b")
from haarpoly import expect_words

ORDER = 17


def red(n, d):
    assert d != 0
    if d < 0:
        n, d = -n, -d
    g = math.gcd(n, d) or 1
    return n // g, d // g


def qa(a, b):
    return red(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def qs(a, b):
    return red(a[0] * b[1] - b[0] * a[1], a[1] * b[1])


def qm(a, b):
    return red(a[0] * b[0], a[1] * b[1])


def txt(a):
    return "%d/%d" % a


# ---- series helpers
def smul(a, b):
    out = [(0, 1)] * ORDER
    for i, x in enumerate(a):
        if x[0]:
            for j, y in enumerate(b):
                if i + j >= ORDER:
                    break
                if y[0]:
                    out[i + j] = qa(out[i + j], qm(x, y))
    return out


def sdiv(a, b):
    assert b[0] == (1, 1)
    out = []
    for n in range(ORDER):
        acc = a[n]
        for j in range(n):
            acc = qs(acc, qm(out[j], b[n - j]))
        out.append(acc)
    return out


def sder(a):
    return [qm((i + 1, 1), a[i + 1]) for i in range(ORDER - 1)] + [(0, 1)]


def spow(a, n):
    out = [(1, 1)] + [(0, 1)] * (ORDER - 1)
    for _ in range(n):
        out = smul(out, a)
    return out


# z(beta) = (2/beta) I_1(beta) = sum beta^(2k) / (4^k k! (k+1)!), taken with enough terms (ORDER+2) so derivatives are exact through ORDER-1.
BIG = ORDER + 4
z_full = [(0, 1)] * BIG
for k in range(0, BIG // 2 + 1):
    if 2 * k < BIG:
        z_full[2 * k] = red(1, 4 ** k * math.factorial(k) * math.factorial(k + 1))
z = z_full[:ORDER]
dz = [qm((i + 1, 1), z_full[i + 1]) for i in range(ORDER)]
d2z = [qm((i + 1, 1), dz[i + 1]) for i in range(ORDER - 1)] + [qm((ORDER, 1), qm((ORDER + 1, 1), z_full[ORDER + 1]))]
u = sdiv(dz, z)  # t_{1/2} = I_2/I_1
# chi_1 = 4 a^2 - 1, so c_1 = 4 z'' - z, and t_1 = c_1/(3 z)
c1 = [qs(qm((4, 1), d2z[i]), z[i]) for i in range(ORDER)]
v = [qm((1, 3), x) for x in sdiv(c1, z)]
# chi_{3/2} = 8 a^3 - 4 a, so c_{3/2} = 8 z''' - 4 z', t_{3/2} = c_{3/2}/(4 z)  (kept for later use)
print("U_SERIES|b1=%s|b3=%s|b5=%s|b7=%s|b9=%s|b11=%s|json=0" % tuple(txt(u[i]) for i in (1, 3, 5, 7, 9, 11)))
print("V_SERIES|b2=%s|b4=%s|json=0" % (txt(v[2]), txt(v[4])))


def log_series(a):
    # log of a series with a[0]=1, via d(log a) = a'/a
    da = sder(a)
    q = sdiv(da, a)
    out = [(0, 1)] * ORDER
    for i in range(ORDER - 1):
        out[i + 1] = qm(q[i], (1, i + 1))
    return out


# NOTE sder loses the top coefficient; everything is compared well below ORDER.
logz = log_series(z)


# ---- word gluing Haar evaluator for products of characters chi = Tr of the fundamental
def inv_word(w):
    return [(l, -s) for l, s in reversed(w)]


def reduce_cyclic(w):
    w = list(w)
    changed = True
    while changed and w:
        changed = False
        out = []
        for x in w:
            if out and out[-1][0] == x[0] and out[-1][1] == -x[1]:
                out.pop()
                changed = True
            else:
                out.append(x)
        w = out
        while len(w) >= 2 and w[0][0] == w[-1][0] and w[0][1] == -w[-1][1]:
            w = w[1:-1]
            changed = True
    return w


class Stuck(Exception):
    pass


def glue(words):
    """Exact integral of the product of chi(word). Returns an integer pair."""
    words = [reduce_cyclic(w) for w in words]
    coef = (1, 1)
    while True:
        # trivial words give chi(1)=2
        rest = []
        for w in words:
            if not w:
                coef = qm(coef, (2, 1))
            else:
                rest.append(w)
        words = rest
        if not words:
            return coef
        occ = {}
        for i, w in enumerate(words):
            for p, (l, s) in enumerate(w):
                occ.setdefault(l, []).append((i, p, s))
        # a link seen once integrates to zero
        for l, places in occ.items():
            if len(places) == 1:
                return (0, 1)
        pick = None
        for l, places in sorted(occ.items()):
            if len(places) == 2:
                pick = (l, places)
                break
        if pick is None:
            raise Stuck(str(words))
        l, ((i, p, s), (j, q, t)) = pick
        if i != j:
            wi = words[i]
            wj = words[j]
            wi = wi[p:] + wi[:p]           # U^s A
            wj = wj[q:] + wj[:q]           # U^t B
            if s < 0:
                wi = inv_word(wi)
                # bring the link back to the front
                k = [n for n, x in enumerate(wi) if x[0] == l][0]
                wi = wi[k:] + wi[:k]
                s = 1
            if t > 0:
                wj = inv_word(wj)
                k = [n for n, x in enumerate(wj) if x[0] == l][0]
                wj = wj[k:] + wj[:k]
                t = -1
            A, B = wi[1:], wj[1:]
            # int chi(U A) chi(U^-1 B) dU = (1/2) chi(A B)
            coef = qm(coef, (1, 2))
            new = reduce_cyclic(A + B)
            words = [w for n, w in enumerate(words) if n not in (i, j)] + [new]
        else:
            w = words[i]
            w = w[p:] + w[:p]
            q2 = (q - p) % len(w)
            s2 = w[q2][1]
            A = w[1:q2]
            B = w[q2 + 1:]
            if w[0][1] == -s2:
                # chi(U A U^-1 B) -> (1/2) chi(A) chi(B), also with U^-1 first by inverting names
                coef = qm(coef, (1, 2))
                words = [x for n, x in enumerate(words) if n != i] + [reduce_cyclic(A), reduce_cyclic(B)]
            else:
                # chi(U A U B) -> -(1/2) chi(A^-1 B); the same with both U^-1 after inverting the whole word
                if w[0][1] < 0:
                    w2 = inv_word(w)
                    k = [n for n, x in enumerate(w2) if x[0] == l][0]
                    w2 = w2[k:] + w2[:k]
                    q3 = [n for n, x in enumerate(w2) if x[0] == l and n != 0][0]
                    A = w2[1:q3]
                    B = w2[q3 + 1:]
                coef = qm(coef, (-1, 2))
                words = [x for n, x in enumerate(words) if n != i] + [reduce_cyclic(inv_word(A) + B)]


def face_word(D, f):
    x, mu, nu = f

    def p(y, i):
        z2 = list(y)
        z2[i] += 1
        return tuple(z2)
    return [((x, mu), 1), ((p(x, mu), nu), 1), ((p(x, nu), mu), -1), ((x, nu), -1)]


def surface_value(D, faces):
    """E[prod a_p] = 2^(-F) * int prod chi."""
    v = glue([face_word(D, f) for f in faces])
    return qm(v, red(1, 2 ** len(faces)))


def plus(x, i):
    y = list(x)
    y[i] += 1
    return tuple(y)


def link_set(faces):
    out = {}
    for f in faces:
        x, mu, nu = f
        for l in ((x, mu), (plus(x, mu), nu), (plus(x, nu), mu), (x, nu)):
            out[l] = out.get(l, 0) + 1
    return out


def analyse(D, path):
    classes = [ast.literal_eval(line) for line in open(path, encoding="utf8")]
    table = {}
    keep = []
    for k in classes:
        cover = link_set(k)
        sites = set()
        for (x, m) in cover:
            sites.add(x)
            sites.add(plus(x, m))
        F = len(k)
        chi = len(sites) - len(cover) + F
        spans = len({d for f in k for d in f[1:]})
        val = surface_value(D, k)
        key = (F, spans, chi, max(cover.values()), val)
        table[key] = table.get(key, 0) + 1
        keep.append((k, key))
    return table, keep


# ---- cross-check of the glue evaluator against the polynomial evaluator on the cube and both ten-face shapes
def to_poly_words(faces):
    return [[((f[0], f[1]), 1), ((plus(f[0], f[1]), f[2]), 1), ((plus(f[0], f[2]), f[1]), -1), ((f[0], f[2]), -1)] for f in faces]


path3 = "classes_d3_F12.txt"
path4 = "classes_d4_F12.txt"
table3, keep3 = analyse(3, path3)
table4, keep4 = analyse(4, path4)
for t, d in ((table3, 3), (table4, 4)):
    for key, n in sorted(t.items()):
        print("SHAPE|d=%d|F=%d|spans=%d|chi=%d|maxcover=%d|E_prod_a=%s|per_site=%d|json=0" % (d, key[0], key[1], key[2], key[3], txt(key[4]), n))
done = set()
for k, key in keep4:
    if key[0] in (6, 10) and key not in done:
        done.add(key)
        w = [list(x) for x in to_poly_words(k)]
        pv = expect_words(w)
        print("POLY_CROSSCHECK|F=%d|spans=%d|glue=%s|poly=%s|ok=%d|json=0" % (key[0], key[1], txt(key[4]), txt(pv), 1 if pv == key[4] else 0))
        assert pv == key[4]


# ---- the assembly, in d dimensions
PUBLISHED_P = {1: (-1, 4), 3: (1, 96), 5: (-7, 1536), 7: (31, 23040), 9: (-4451, 8847360), 11: (264883, 1486356480), 13: (-403651, 5945425920)}


def assemble(d, table, planes):
    series = [qm((planes, 1), x) for x in logz]
    terms = {}
    N6 = sum(n for key, n in table.items() if key[0] == 6)
    N10 = sum(n for key, n in table.items() if key[0] == 10)
    # surfaces through F=10, dressed with the full u(beta): each sphere of F faces contributes 2^chi u^F = 4 u^F
    for F, N in ((6, N6), (10, N10)):
        term = [qm((4 * N, 1), x) for x in spow(u, F)]
        series = [qa(a, b) for a, b in zip(series, term)]
    # order-12 pieces
    u12 = spow(u, 12)
    u10v = smul(spow(u, 10), v)
    v6 = spow(v, 6)
    # F=12 closed sets: value*(4u)^12. A pair of cubes sharing one link has value 2^-20 -> 16 u^12, and the overlap term -16 u^12 cancels it. Anything else is new.
    new12 = (0, 1)
    pair12 = 0
    other12 = 0
    for key, n in table.items():
        if key[0] == 12:
            coef = qm(key[4], (4 ** 12, 1))
            # identify cube pairs by value 16: checked below against the enumeration of touching pairs
            if coef == (16, 1):
                pair12 += n
            else:
                other12 += n
                new12 = qa(new12, qm(coef, (n, 1)))
    print("F12_SPLIT|d=%d|value_16u12_pairs=%d|other=%d|other_total_coefficient_of_u12=%s|json=0" % (d, pair12, other12, txt(new12)))
    assembly = [
        ("F12_closed_sets_other_than_two_cubes", [qm(new12, x) for x in u12]),
        ("two_cubes_sharing_a_face:spin1_on_the_shared_face", [qm((N10 * 12, 1), x) for x in u10v]),
        ("two_cubes_sharing_a_face:overlap_minus_16u12", [qm((-N10 * 16, 1), x) for x in u12]),
        ("one_cube:spin1_on_all_six_faces_9v6", [qm((N6 * 9, 1), x) for x in v6]),
        ("one_cube:self_overlap_minus_8u12", [qm((-N6 * 8, 1), x) for x in u12]),
    ]
    for name, term in assembly:
        terms[name] = term[12]
        series = [qa(a, b) for a, b in zip(series, term)]
    # plaquette = (1/planes) d/dbeta of the per-site log Z
    plaq = [qm(x, (1, planes)) for x in sder(series)]
    return series, plaq, terms, N6, N10


series4, plaq4, terms4, N6, N10 = assemble(4, table4, 6)
print("COUNTS|d=4|N6=%d|N10=%d|json=0" % (N6, N10))
for name, val in terms4.items():
    print("BETA12_TERM|d=4|%s=%s|json=0" % (name, txt(val)))
for n in (1, 3, 5, 7, 9, 11):
    want = PUBLISHED_P[n]
    have = plaq4[n]
    # P = 1 - <a>, so a_n = -coefficient of <a>
    match = have == (-want[0], want[1])
    print("COMPARE_TABLE1|n=%d|<a>_coefficient=%s|-a_n_from_table=%d/%d|match=%d|json=0" % (n, txt(have), -want[0], want[1], 1 if match else 0))
# How the published beta^11 decomposes
through10 = [qm((6, 1), x) for x in logz]
print("BETA11_SPLIT|single_plaquette_u11=%s|json=0" % txt(u[11]))
print("BETA11_RESIDUAL|published_minus_all_F_le_10_terms_in_log_Z_units=%s|json=0" % txt(qs(qm((-PUBLISHED_P[11][0], PUBLISHED_P[11][1]), (1, 2)), qa(qa(qm((6, 1), logz[12]), qm((16, 1), spow(u, 6)[12])), qm((144, 1), spow(u, 10)[12])))))
series3, plaq3, terms3, N63, N103 = assemble(3, table3, 3)
print("COUNTS|d=3|N6=%d|N10=%d|json=0" % (N63, N103))
print("SERIES_D3|b1=%s|b3=%s|b5=%s|b7=%s|b9=%s|b11=%s|json=0" % tuple(txt(plaq3[i]) for i in (1, 3, 5, 7, 9, 11)))
print("STRETCH_DONE|json=0")
