#!/usr/bin/env python3
"""Second seat's exact helpers for YM4-02c. Standard library, integers only, json=0. Rationals are reduced pairs of ints, written here with their own names."""
import itertools
import math


def rat(n, d=1):
    if d < 0:
        n, d = -n, -d
    g = math.gcd(n, d)
    return (n // g, d // g)


def radd(a, b):
    return rat(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def rsub(a, b):
    return rat(a[0] * b[1] - b[0] * a[1], a[1] * b[1])


def rmul(a, b):
    return rat(a[0] * b[0], a[1] * b[1])


def rtext(a):
    return str(a[0]) if a[1] == 1 else "%d/%d" % a


def charpoly(rows):
    """Faddeev-LeVerrier in exact integers. Returns c with p(x) = x^n + c[1] x^(n-1) + ... + c[n]. Each division by k is exact."""
    n = len(rows)
    c = [1] + [0] * n
    b = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for k in range(1, n + 1):
        ab = [[sum(rows[i][m] * b[m][j] for m in range(n)) for j in range(n)] for i in range(n)]
        tr = sum(ab[i][i] for i in range(n))
        q, r = divmod(-tr, k)
        assert r == 0
        c[k] = q
        b = [[ab[i][j] + (q if i == j else 0) for j in range(n)] for i in range(n)]
    assert all(v == 0 for row in b for v in row), "Cayley-Hamilton closes"
    return c


def inertia_from_charpoly(c):
    """For a real symmetric matrix every root is real, so Descartes' rule counts exactly: positive roots = sign changes of p(x), negative roots = sign changes of p(-x)."""
    n = len(c) - 1
    # c[k] multiplies x^(n-k)
    def changes(seq):
        s = [v for v in seq if v != 0]
        return sum(1 for a, b in zip(s, s[1:]) if (a > 0) != (b > 0))
    pos = changes(c)
    neg = changes([c[k] * (-1) ** (n - k) for k in range(n + 1)])
    zero = n - pos - neg
    return pos, neg, zero


def rank_mod(rows, p):
    m = [[v % p for v in r] for r in rows]
    rank = 0
    ncols = len(m[0]) if m else 0
    for col in range(ncols):
        piv = next((i for i in range(rank, len(m)) if m[i][col]), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        iv = pow(m[rank][col], p - 2, p)
        m[rank] = [v * iv % p for v in m[rank]]
        for i in range(len(m)):
            if i != rank and m[i][col]:
                f = m[i][col]
                m[i] = [(a - f * b) % p for a, b in zip(m[i], m[rank])]
        rank += 1
    return rank


def signature_by_rational_ldl(rows):
    """Symmetric elimination with diagonal pivots only, over pairs of ints with a common denominator kept per row. Returns (positive pivots, negative pivots, zero_tail_ok)."""
    n = len(rows)
    m = [[(v, 1) for v in r] for r in rows]
    pos, neg = 0, 0
    alive = list(range(n))
    while alive:
        pick = next((i for i in alive if m[i][i][0] != 0), None)
        if pick is None:
            ok = all(m[i][j][0] == 0 for i in alive for j in alive)
            return pos, neg, ok
        d = m[pick][pick]
        if d[0] > 0:
            pos += 1
        else:
            neg += 1
        alive.remove(pick)
        for i in alive:
            if m[i][pick][0] == 0:
                continue
            f = rat(m[i][pick][0] * d[1], m[i][pick][1] * d[0])
            for j in alive:
                if m[pick][j][0]:
                    m[i][j] = rsub(m[i][j], rmul(f, m[pick][j]))
    return pos, neg, True


class FiniteGroup:
    """From doubled integer quaternions. The stored value is twice the unit quaternion."""

    def __init__(self, name):
        q8 = []
        for a in range(4):
            for s in (2, -2):
                e = [0, 0, 0, 0]
                e[a] = s
                q8.append(tuple(e))
        self.elems = q8 if name == "Q8" else q8 + [tuple(v) for v in itertools.product((1, -1), repeat=4)]
        self.n = len(self.elems)
        at = {e: i for i, e in enumerate(self.elems)}
        def times(p, q):
            r = (p[0] * q[0] - p[1] * q[1] - p[2] * q[2] - p[3] * q[3],
                 p[0] * q[1] + p[1] * q[0] + p[2] * q[3] - p[3] * q[2],
                 p[0] * q[2] - p[1] * q[3] + p[2] * q[0] + p[3] * q[1],
                 p[0] * q[3] + p[1] * q[2] - p[2] * q[1] + p[3] * q[0])
            return tuple(v // 2 for v in r)
        self.mul = [[at[times(x, y)] for y in self.elems] for x in self.elems]
        self.inv = [at[(e[0], -e[1], -e[2], -e[3])] for e in self.elems]
        self.one = at[(2, 0, 0, 0)]
        self.cls = [-1] * self.n
        self.classes = []
        for g in range(self.n):
            if self.cls[g] < 0:
                orbit = sorted({self.mul[self.mul[h][g]][self.inv[h]] for h in range(self.n)})
                for x in orbit:
                    self.cls[x] = len(self.classes)
                self.classes.append(orbit)


def q8_table(G):
    """Character table over the classes in the order +1, -1, i, j, k as five integer rows: trivial, s_i, s_j, s_k, E. s_a is +1 on the class of a and on +-1, -1 on the other two."""
    assert [G.elems[c[0]] for c in G.classes] == [(2, 0, 0, 0), (-2, 0, 0, 0), (0, 2, 0, 0), (0, 0, 2, 0), (0, 0, 0, 2)]
    return [[1, 1, 1, 1, 1], [1, 1, 1, -1, -1], [1, 1, -1, 1, -1], [1, 1, -1, -1, 1], [2, -2, 0, 0, 0]]


def q8_weight(table, c):
    return [sum(c[r] * table[r][k] for r in range(5)) for k in range(5)]
