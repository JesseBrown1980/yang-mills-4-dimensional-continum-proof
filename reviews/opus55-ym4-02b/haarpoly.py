# Exact Haar integration by polynomial expansion in quaternion coordinates, with no finite group and no gauge fixing.
# a_p = Re(q1 q2 conj(q3) conj(q4)), each q a unit quaternion with 4 coordinates. Link-by-link Fubini with the closed-form S^3 monomial integral.
# Integers only. Coefficients are reduced integer pairs.
import math

BASIS = {}
# quaternion basis multiplication: (i,j) -> (sign, k), e0=1, e1=i, e2=j, e3=k
_T = [[(1, 0), (1, 1), (1, 2), (1, 3)],
      [(1, 1), (-1, 0), (1, 3), (-1, 2)],
      [(1, 2), (-1, 3), (-1, 0), (1, 1)],
      [(1, 3), (1, 2), (-1, 1), (-1, 0)]]


def red(n, d):
    if d < 0:
        n, d = -n, -d
    g = math.gcd(n, d) or 1
    return n // g, d // g


def qadd(a, b):
    return red(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def qmul(a, b):
    return red(a[0] * b[0], a[1] * b[1])


def dfact(n):
    r = 1
    while n > 1:
        r *= n
        n -= 2
    return r


_HAAR = {}


def haar_monomial(e):
    h = _HAAR.get(e)
    if h is None:
        if any(x % 2 for x in e):
            h = (0, 1)
        else:
            A = sum(e) // 2
            num = 1
            for x in e:
                num *= dfact(x - 1)
            h = red(num, 2 ** A * math.factorial(A + 1))
        _HAAR[e] = h
    return h


def word_poly(word):
    """Polynomial of the REAL PART of the product of a word [(link, sign), ...], as a dict: tuple of ((link,coord), ...) sorted -> integer coefficient."""
    # state: basis index -> dict monomial(tuple sorted) -> coefficient
    state = {0: {(): 1}}
    for link, s in word:
        new = {}
        for k, terms in state.items():
            for i in range(4):
                conj_sign = 1 if (s > 0 or i == 0) else -1
                sg, k2 = _T[k][i]
                bucket = new.setdefault(k2, {})
                for m, c in terms.items():
                    m2 = tuple(sorted(m + ((link, i),)))
                    bucket[m2] = bucket.get(m2, 0) + c * sg * conj_sign
        state = new
    return {m: c for m, c in state.get(0, {}).items() if c}


def to_exp(poly):
    """dict: frozenset-like canonical tuple ((link, (e0,e1,e2,e3)), ...) -> rational pair."""
    out = {}
    for m, c in poly.items():
        ex = {}
        for link, i in m:
            e = ex.setdefault(link, [0, 0, 0, 0])
            e[i] += 1
        key = tuple(sorted((l, tuple(e)) for l, e in ex.items()))
        out[key] = (c, 1) if key not in out else qadd(out[key], (c, 1))
    return {k: v for k, v in out.items() if v[0]}


def pmul(a, b):
    out = {}
    for ma, ca in a.items():
        da = dict(ma)
        for mb, cb in b.items():
            d = dict(da)
            for l, e in mb:
                f = d.get(l)
                d[l] = e if f is None else (f[0] + e[0], f[1] + e[1], f[2] + e[2], f[3] + e[3])
            key = tuple(sorted(d.items()))
            c = qmul(ca, cb)
            old = out.get(key)
            out[key] = c if old is None else qadd(old, c)
    return {k: v for k, v in out.items() if v[0]}


def integrate_link(poly, link):
    out = {}
    for m, c in poly.items():
        rest = []
        h = (1, 1)
        for l, e in m:
            if l == link:
                h = haar_monomial(e)
            else:
                rest.append((l, e))
        if h[0] == 0:
            continue
        key = tuple(rest)
        v = qmul(c, h)
        old = out.get(key)
        out[key] = v if old is None else qadd(old, v)
    return {k: v for k, v in out.items() if v[0]}


def links_of(poly):
    s = set()
    for m in poly:
        for l, _ in m:
            s.add(l)
    return s


def expect_words(words):
    """E[prod over words of Re(word)] exactly, by elimination: integrate any link private to one factor, else multiply the pair sharing the most links."""
    factors = [to_exp(word_poly(w)) for w in words]
    linksets = [set(l for l, _ in w) for w in words]
    const = (1, 1)
    while True:
        # integrate private links
        changed = True
        while changed:
            changed = False
            count = {}
            for ls in linksets:
                for l in ls:
                    count[l] = count.get(l, 0) + 1
            for i in range(len(factors)):
                priv = [l for l in linksets[i] if count[l] == 1]
                for l in priv:
                    factors[i] = integrate_link(factors[i], l)
                    linksets[i].discard(l)
                    changed = True
        # drop constants
        keep_f, keep_l = [], []
        for f, ls in zip(factors, linksets):
            if not ls:
                v = f.get((), (0, 1))
                const = qmul(const, v)
            else:
                keep_f.append(f)
                keep_l.append(ls)
        factors, linksets = keep_f, keep_l
        if const[0] == 0:
            return (0, 1)
        if not factors:
            return const
        best, bi, bj = None, 0, 1
        for i in range(len(factors)):
            for j in range(i + 1, len(factors)):
                shared = len(linksets[i] & linksets[j])
                if shared == 0:
                    continue
                score = (-shared, len(factors[i]) * len(factors[j]))
                if best is None or score < best:
                    best, bi, bj = score, i, j
        f = pmul(factors[bi], factors[bj])
        ls = linksets[bi] | linksets[bj]
        factors = [factors[k] for k in range(len(factors)) if k not in (bi, bj)] + [f]
        linksets = [linksets[k] for k in range(len(linksets)) if k not in (bi, bj)] + [ls]
