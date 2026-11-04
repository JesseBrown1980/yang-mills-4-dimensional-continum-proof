# Exact rational unit quaternions as integer tuples (a, b, c, d, den). Integers only.
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


def word_value(cfg, word):
    h = ONE
    for l, e in word:
        h = mul(h, cfg[l] if e > 0 else inv(cfg[l]))
    return h


def random_unit(rng, bound=7):
    """Stereographic from a random rational point: q = (s^2 - |t|^2 + 2 s t) / (s^2 + |t|^2). Spreads over the whole sphere, with an exact rational value."""
    while True:
        s = 1 + rng.below(bound)
        t = [rng.below(2 * bound + 1) - bound for _ in range(3)]
        n2 = t[0] * t[0] + t[1] * t[1] + t[2] * t[2]
        den = s * s + n2
        if den:
            q = red((s * s - n2, 2 * s * t[0], 2 * s * t[1], 2 * s * t[2], den))
            assert q[0] ** 2 + q[1] ** 2 + q[2] ** 2 + q[3] ** 2 == q[4] ** 2
            return q
