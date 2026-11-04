# Exact rational unit quaternions as integer tuples (a, b, c, d, den), never reduced by anything but gcd. Integers only. json=0.
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep import Lat, RNG


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def red(q):
    g = q[4]
    for v in q[:4]:
        g = gcd(g, v)
    return tuple(v // g for v in q)


def mul(p, q):
    a, b, c, d, m = p
    e, f, g, h, n = q
    return red((a * e - b * f - c * g - d * h, a * f + b * e + c * h - d * g, a * g - b * h + c * e + d * f, a * h + b * g - c * f + d * e, m * n))


def inv(p):
    return (p[0], -p[1], -p[2], -p[3], p[4])


ONE = (1, 0, 0, 0, 1)
I = (0, 1, 0, 0, 1)
J = (0, 0, 1, 0, 1)
K = (0, 0, 0, 1, 1)
MINUS = (-1, 0, 0, 0, 1)


def is_unit(q):
    return q[0] ** 2 + q[1] ** 2 + q[2] ** 2 + q[3] ** 2 == q[4] ** 2


def small_unit(rng, bound, scale):
    """Stereographic: t = (t1, t2, t3) / scale, q = ((1 - |t|^2) + 2 t) / (1 + |t|^2), a rational unit quaternion near 1 when t is small."""
    t = [rng.below(2 * bound + 1) - bound for _ in range(3)]
    s2 = scale * scale
    n2 = t[0] * t[0] + t[1] * t[1] + t[2] * t[2]
    q = (s2 - n2, 2 * scale * t[0], 2 * scale * t[1], 2 * scale * t[2], s2 + n2)
    q = red(q)
    assert is_unit(q)
    return q


def word_value(cfg, word):
    h = ONE
    for l, e in word:
        h = mul(h, cfg[l] if e > 0 else inv(cfg[l]))
    return h


# delta = 8/25 < 1/3. In the norm of H, |U - sigma|^2 = 2 - 2 sigma Re U. Strictly inside means (2 - 2 sigma a/den) < delta^2.
DN, DD = 8, 25


def in_ball(u, sigma):
    a, den = u[0], u[4]
    # 2 - 2 sigma a/den < DN^2/DD^2  <=>  (2 den - 2 sigma a) DD^2 < DN^2 den   with den > 0
    return (2 * den - 2 * sigma * a) * DD * DD < DN * DN * den


def sigma_of(u):
    if in_ball(u, 1):
        return 1
    if in_ball(u, -1):
        return -1
    return 0


def twist(lat):
    cfg = []
    for x, mu in lat.links:
        if mu == 0 and x[0] == 0:
            cfg.append(I)
        elif mu == 1 and x[1] == 0:
            cfg.append(J)
        else:
            cfg.append(ONE)
    return cfg


# ---- 1. The note's twist, read with real quaternions rather than Q8 indices.
for dims in ((2, 2, 2), (2, 2, 3), (2, 2, 4), (2, 3, 3), (3, 3, 3), (2, 2), (3, 3), (3, 2), (2, 2, 5)):
    lat = Lat(*dims)
    cfg = twist(lat)
    values = [word_value(cfg, w) for w in lat.words]
    minus = sum(1 for v in values if v == MINUS)
    plus = sum(1 for v in values if v == ONE)
    where = sorted(set(p[1:] and (p[1], p[2]) for p, v in zip(lat.plaq, values) if v == MINUS))
    third = lat.dims[2] if lat.k > 2 else 1
    print("IND_SU2_TWIST|lattice=%s|plaquettes=%d|at_+1=%d|at_-1=%d|each_-1_in_plane=%s|expected_-1=L3=%d|S=%+d|json=0" % ("x".join(map(str, dims)), len(values), plus, minus, where, third, -1 if minus % 2 else 1))


# ---- 2. A neighbourhood of the twist: each link moved by a small rational unit quaternion. Every plaquette stays in the support, signs stay, S stays. Cubes read exactly.
def cube_faces(lat, x):
    """Words of the six faces at x as (index in lat.plaq), read with the cube identity below."""
    index = {p: i for i, p in enumerate(lat.plaq)}
    return [index[(x, 0, 1)], index[(lat.step(x, 2), 0, 1)], index[(x, 0, 2)], index[(lat.step(x, 1), 0, 2)], index[(x, 1, 2)], index[(lat.step(x, 0), 1, 2)]]


for dims, seed in (((2, 2, 2), 11), ((2, 2, 3), 12), ((2, 2, 4), 13), ((2, 2), 14), ((3, 3), 15)):
    lat = Lat(*dims)
    rng = RNG(seed)
    base = twist(lat)
    runs = 200
    all_support = all_even_cube = 0
    S_values = set()
    negs = {}
    for _ in range(runs):
        cfg = [mul(u, small_unit(rng, 3, 100)) for u in base]
        values = [word_value(cfg, w) for w in lat.words]
        sig = [sigma_of(v) for v in values]
        if all(sig):
            all_support += 1
            S_values.add(-1 if sum(1 for s in sig if s < 0) % 2 else 1)
            negs[sum(1 for s in sig if s < 0)] = negs.get(sum(1 for s in sig if s < 0), 0) + 1
            if lat.k == 3:
                ok = True
                for x in lat.sites:
                    p = 1
                    for f in cube_faces(lat, x):
                        p *= sig[f]
                    ok = ok and p == 1
                all_even_cube += 1 if ok else 0
    print("IND_SU2_NEIGHBOURHOOD|lattice=%s|delta=%d/%d|runs=%d|all_plaquettes_in_the_support=%d|S_values=%s|negative_counts=%s|runs_with_every_cube_even=%d|json=0" % ("x".join(map(str, dims)), DN, DD, runs, all_support, sorted(S_values), sorted(negs.items()), all_even_cube))
    sys.stdout.flush()


# ---- 3. The cube identity with real quaternions, using the order found by the free reduction: x0, z1^-1, y0^-1, x1^-1, z0, y1.
def cube_product(rng):
    edges = {}
    verts = list(itertools.product((0, 1), repeat=3))
    for v in verts:
        for a in range(3):
            if v[a] == 0:
                edges[(v, a)] = mul(small_unit(rng, 40, 41), small_unit(rng, 40, 41))

    def walk(start, axes):
        cur = start
        out = ONE
        for a in axes:
            w = list(cur)
            w[a] ^= 1
            nxt = tuple(w)
            out = mul(out, edges[(cur, a)]) if cur[a] == 0 else mul(out, inv(edges[(nxt, a)]))
            cur = nxt
        return out, cur

    def lasso(conn, loop, inverted):
        c, corner = walk((0, 0, 0), conn)
        l, end = walk(corner, loop)
        assert end == corner
        if inverted:
            l = inv(l)
        return mul(mul(c, l), inv(c))

    faces = {"x0": ((), (1, 2, 1, 2)), "x1": ((0,), (1, 2, 1, 2)), "y0": ((), (0, 2, 0, 2)), "y1": ((1,), (0, 2, 0, 2)), "z0": ((), (0, 1, 0, 1)), "z1": ((2,), (0, 1, 0, 1))}
    total = ONE
    for name, sign in zip(("x0", "z1", "y0", "x1", "z0", "y1"), (0, 1, 1, 1, 0, 0)):
        conn, loop = faces[name]
        total = mul(total, lasso(conn, loop, sign))
    return total


rng = RNG(77)
hits = sum(1 for _ in range(50) if cube_product(rng) == ONE)
print("IND_SU2_CUBE|random_exact_rational_cubes=50|ordered_product_equal_to_1=%d|json=0" % hits)


# ---- 4. a_p on the side-1 slices: both signs of S exist on SU(2), where Q8 keeps one sign.
def real_sign(q):
    return (q[0] > 0) - (q[0] < 0)


found = {}
for dims, seed in (((2, 1), 501), ((1, 1), 502), ((2, 1, 1), 503), ((1, 1, 1), 504), ((2, 1, 2), 505)):
    lat = Lat(*dims)
    rng = RNG(seed)
    pal = [(1, 2, 2, 0, 3), (2, 1, 0, 2, 3), (2, 0, 1, -2, 3), (1, -2, 2, 0, 3), (2, 1, 2, 0, 3), (1, 1, 1, 1, 2), (1, -1, 1, -1, 2), (3, 4, 0, 0, 5), (0, 3, 0, 4, 5), (5, 12, 0, 0, 13), (0, 5, 12, 0, 13), I, J, K]
    wit = {}
    draws = 0
    while len(wit) < 2 and draws < 20000:
        draws += 1
        idx = [rng.below(len(pal)) for _ in lat.links]
        cfg = [pal[i] for i in idx]
        sg = 1
        for w in lat.words:
            sg *= real_sign(word_value(cfg, w))
            if sg == 0:
                break
        if sg:
            wit.setdefault(sg, idx)
    print("IND_SU2_SIDE_ONE|lattice=%s|weight=a_p|draws=%d|both_signs_of_S=%d|plus=%s|minus=%s|json=0" % ("x".join(map(str, dims)), draws, 1 if len(wit) == 2 else 0, ".".join(map(str, wit.get(1, []))), ".".join(map(str, wit.get(-1, [])))))
print("IND_SU2_DONE|json=0")
