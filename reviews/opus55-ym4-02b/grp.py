# Own exact construction of Q8, 2T, 2O, 2I as unit quaternions. Integers only.
# A coordinate is (a,b) meaning a + b*w with w^2 = p*w + q, stored DOUBLED (2*x), so every group element has coordinates in Z[w].
import itertools


def ring(p, q):
    def mul(x, y):
        return (x[0] * y[0] + x[1] * y[1] * q, x[0] * y[1] + x[1] * y[0] + x[1] * y[1] * p)
    return mul


ZZ = ring(0, 0)  # b always 0
R2 = ring(0, 2)  # w = sqrt 2
PH = ring(1, 1)  # w = phi


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def neg(x):
    return (-x[0], -x[1])


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def halve(x):
    assert x[0] % 2 == 0 and x[1] % 2 == 0, x
    return (x[0] // 2, x[1] // 2)


def qmul(R, p, q):
    # (doubled p)(doubled q) = 4 p q, so doubled(pq) = product/2.
    a, b, c, d = p
    e, f, g, h = q
    r0 = sub(sub(sub(R(a, e), R(b, f)), R(c, g)), R(d, h))
    r1 = sub(add(add(R(a, f), R(b, e)), R(c, h)), R(d, g))
    r2 = add(add(sub(R(a, g), R(b, h)), R(c, e)), R(d, f))
    r3 = add(sub(add(R(a, h), R(b, g)), R(c, f)), R(d, e))
    return (halve(r0), halve(r1), halve(r2), halve(r3))


def qconj(p):
    return (p[0], neg(p[1]), neg(p[2]), neg(p[3]))


O = (0, 0)


def even_perms_of(tup):
    out = set()
    for perm in itertools.permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if perm[i] > perm[j])
        if inv % 2 == 0:
            out.add(tuple(tup[perm[i]] for i in range(4)))
    return out


def signs_applied(tup):
    idx = [i for i in range(4) if tup[i] != O]
    out = set()
    for s in itertools.product((1, -1), repeat=len(idx)):
        v = list(tup)
        for i, sg in zip(idx, s):
            v[i] = (sg * tup[i][0], sg * tup[i][1])
        out.add(tuple(v))
    return out


def build(name):
    TWO, ONE = (2, 0), (1, 0)
    q8 = set()
    for i in range(4):
        v = [O] * 4
        v[i] = TWO
        q8 |= signs_applied(tuple(v))
    t16 = signs_applied((ONE, ONE, ONE, ONE))
    if name == "Q8":
        return ZZ, sorted(q8)
    if name == "2T":
        return ZZ, sorted(q8 | t16)
    if name == "2O":
        extra = set()
        # all permutations of (+-sqrt2, +-sqrt2, 0, 0) in doubled coordinates, i.e. (+-1,+-1,0,0)/sqrt2
        S2 = (0, 1)
        for i, j in itertools.combinations(range(4), 2):
            v = [O] * 4
            v[i] = S2
            v[j] = S2
            extra |= signs_applied(tuple(v))
        return R2, sorted(q8 | t16 | extra)
    if name == "2I":
        extra = set()
        # even permutations of (+-phi, +-1, +-(phi-1), 0) in doubled coordinates, i.e. (phi, 1, 1/phi, 0)/2
        base = ((0, 1), ONE, (-1, 1), O)
        for perm in even_perms_of(base):
            extra |= signs_applied(perm)
        return PH, sorted(q8 | t16 | extra)
    raise ValueError(name)


def norm_is_one(R, e):
    tot = (0, 0)
    for c in e:
        tot = add(tot, R(c, c))
    return tot == (4, 0)


def table(R, E):
    idx = {e: i for i, e in enumerate(E)}
    mult = [[idx[qmul(R, x, y)] for y in E] for x in E]  # KeyError means not closed
    inv = [idx[qconj(e)] for e in E]
    return mult, inv, idx
