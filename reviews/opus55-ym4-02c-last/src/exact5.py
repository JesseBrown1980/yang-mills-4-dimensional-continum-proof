#!/usr/bin/env python3
"""Helpers, standard library, integers only, json=0."""
import itertools

def q8():
    # Quaternion units as (sign, axis), axis 0..3 = 1,i,j,k. Elements listed +1,-1,+i,-i,+j,-j,+k,-k.
    els = [(s, a) for a in range(4) for s in (1, -1)]
    idx = {e: n for n, e in enumerate(els)}
    tab = {(0, 0): (1, 0), (0, 1): (1, 1), (0, 2): (1, 2), (0, 3): (1, 3),
           (1, 0): (1, 1), (1, 1): (-1, 0), (1, 2): (1, 3), (1, 3): (-1, 2),
           (2, 0): (1, 2), (2, 1): (-1, 3), (2, 2): (-1, 0), (2, 3): (1, 1),
           (3, 0): (1, 3), (3, 1): (1, 2), (3, 2): (-1, 1), (3, 3): (-1, 0)}
    mul = [[0] * 8 for _ in range(8)]
    for g, (s, a) in enumerate(els):
        for h, (t, b) in enumerate(els):
            u, c = tab[(a, b)]
            mul[g][h] = idx[(s * t * u, c)]
    return mul

def cyclic(n):
    return [[(a + b) % n for b in range(n)] for a in range(n)]

def direct(m1, m2):
    n1, n2 = len(m1), len(m2)
    return [[m1[a // n2][b // n2] * n2 + m2[a % n2][b % n2] for b in range(n1 * n2)] for a in range(n1 * n2)]

def perm_group(gens):
    n = len(gens[0])
    idp = tuple(range(n))
    els = [idp]
    seen = {idp}
    i = 0
    while i < len(els):
        for g in gens:
            h = tuple(g[els[i][k]] for k in range(n))
            if h not in seen:
                seen.add(h)
                els.append(h)
        i += 1
    idx = {e: k for k, e in enumerate(els)}
    return [[idx[tuple(els[a][els[b][k]] for k in range(n))] for b in range(len(els))] for a in range(len(els))]

class Group:
    def __init__(self, mul):
        self.mul = mul
        self.n = len(mul)
        self.one = next(e for e in range(self.n) if all(mul[e][g] == g for g in range(self.n)))
        self.inv = [next(h for h in range(self.n) if mul[g][h] == self.one) for g in range(self.n)]
        cls = [-1] * self.n
        reps = []
        for g in range(self.n):
            if cls[g] < 0:
                k = len(reps)
                reps.append(g)
                for v in range(self.n):
                    cls[mul[mul[v][g]][self.inv[v]]] = k
        self.cls, self.reps = cls, reps
        self.sizes = [sum(1 for g in range(self.n) if cls[g] == k) for k in range(len(reps))]
        self.icls = [cls[self.inv[reps[k]]] for k in range(len(reps))]

def bareiss_inertia(rows):
    """Exact inertia of a symmetric integer matrix by fraction-free elimination with symmetric pivoting. Returns positive, negative, rank."""
    m = [list(r) for r in rows]
    n = len(m)
    prev, pos, neg = 1, 0, 0
    for k in range(n):
        piv = next((i for i in range(k, n) if m[i][i]), None)
        if piv is None:
            pair = next(((i, j) for i in range(k, n) for j in range(i + 1, n) if m[i][j]), None)
            if pair is None:
                return pos, neg, k
            i, j = pair
            for r in range(k, n):
                m[i][r] += m[j][r]
            for r in range(k, n):
                m[r][i] += m[r][j]
            piv = i
        m[k], m[piv] = m[piv], m[k]
        for row in m:
            row[k], row[piv] = row[piv], row[k]
        top = m[k][k]
        if (top > 0) == (prev > 0):
            pos += 1
        else:
            neg += 1
        for i in range(k + 1, n):
            mik = m[i][k]
            ri, rk = m[i], m[k]
            for j in range(i, n):
                v, rest = divmod(ri[j] * top - mik * rk[j], prev)
                assert rest == 0
                ri[j] = v
                m[j][i] = v
        prev = top
    return pos, neg, n

class Lat:
    """Sides (L_1,...,L_k,T), last direction is time. Links are (x, mu). Plaquettes are (y, mu, nu), mu<nu, with the word of section 1 of the lemma."""
    def __init__(self, dims):
        self.dims = tuple(dims)
        self.d = len(dims)
        self.T = dims[-1]
        self.sites = list(itertools.product(*[range(s) for s in dims]))
        self.links = [(x, mu) for x in self.sites for mu in range(self.d)]
        self.plaqs = [(x, mu, nu) for x in self.sites for mu in range(self.d) for nu in range(mu + 1, self.d)]
    def shift(self, x, mu):
        y = list(x)
        y[mu] = (y[mu] + 1) % self.dims[mu]
        return tuple(y)
    def word(self, p):
        y, mu, nu = p
        return (((y, mu), 1), ((self.shift(y, mu), nu), 1), ((self.shift(y, nu), mu), -1), ((y, nu), -1))
