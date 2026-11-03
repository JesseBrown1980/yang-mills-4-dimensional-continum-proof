# Claim 1: explicit groups, closure, class sizes, then every monomial on S^3 through degree t+1 against the exact Haar monomial integral.
import itertools
import math
import sys

sys.path.insert(0, "C:/tmp/opus55/attack-4d-20261103/ym4-02b")
from grp import O, add, build, norm_is_one, table


def dfact(n):  # (2a-1)!! with n=2a-1, (-1)!!=1
    r = 1
    while n > 1:
        r *= n
        n -= 2
    return r


def haar_monomial(e):
    # E[prod x_i^{e_i}] on S^3: 0 if any exponent is odd, else prod (2a_i-1)!! / (2^{|a|} (|a|+1)!)
    if any(x % 2 for x in e):
        return (0, 1)
    A = sum(e) // 2
    num = 1
    for x in e:
        num *= dfact(x - 1)
    den = 2 ** A * math.factorial(A + 1)
    g = math.gcd(num, den)
    return (num // g, den // g)


# Sanity of the closed form, without any group: multinomial sum = 1 and Catalan.
for m in range(0, 8):
    tot_n, tot_d = 0, 1
    for a in itertools.product(range(m + 1), repeat=4):
        if sum(a) != m:
            continue
        mn = math.factorial(m)
        for x in a:
            mn //= math.factorial(x)
        h = haar_monomial(tuple(2 * x for x in a))
        tot_n = tot_n * h[1] + mn * h[0] * tot_d
        tot_d = tot_d * h[1]
    assert tot_n == tot_d, m
for k in range(0, 8):
    h = haar_monomial((2 * k, 0, 0, 0))
    assert 4 ** k * h[0] == h[1] * (math.factorial(2 * k) // (math.factorial(k) * math.factorial(k + 1))), k
print("HAAR_CLOSED_FORM|multinomial_sum_is_one_through_m=7|catalan_through_k=7|ok=1|json=0")

EXPECT = {"Q8": 3, "2T": 5, "2O": 7, "2I": 11}
ORDERS = {"Q8": 8, "2T": 24, "2O": 48, "2I": 120}
for name in ("Q8", "2T", "2O", "2I"):
    R, E = build(name)
    assert len(E) == ORDERS[name], (name, len(E))
    assert all(norm_is_one(R, e) for e in E)
    mult, inv, idx = table(R, E)  # raises KeyError if not closed
    n = len(E)
    one = idx[((2, 0), O, O, O)]
    assert all(mult[one][g] == g == mult[g][one] for g in range(n))
    assert all(mult[g][inv[g]] == one for g in range(n))
    if n <= 48:
        assert all(mult[mult[a][b]][c] == mult[a][mult[b][c]] for a in range(n) for b in range(n) for c in range(n))
    seen, classes = set(), []
    for g in range(n):
        if g in seen:
            continue
        orb = {mult[mult[h][g]][inv[h]] for h in range(n)}
        seen |= orb
        tr = E[g][0]  # doubled real part = Tr U
        o, x = 1, g
        while x != one:
            x = mult[x][g]
            o += 1
        classes.append((len(orb), tr, o))
    classes.sort(key=lambda c: (c[2], c[1]))
    print("CLASSES|group=%s|order=%d|closed=1|associative_checked=%d|n_classes=%d|rows=%s|json=0" % (name, n, 1 if n <= 48 else 0, len(classes), ";".join("size=%d,trace=%d+%dw,elt_order=%d" % (c[0], c[1][0], c[1][1], c[2]) for c in classes)))
    t = EXPECT[name]
    fails_at = {}
    tested = {}
    powcache = [{} for _ in range(n)]

    def pw(g, i, k):
        key = (i, k)
        c = powcache[g].get(key)
        if c is None:
            c = (1, 0)
            for _ in range(k):
                c = R(c, E[g][i])
            powcache[g][key] = c
        return c
    for deg in range(0, t + 2):
        failed = []
        cnt = 0
        for e0 in range(deg + 1):
            for e1 in range(deg + 1 - e0):
                for e2 in range(deg + 1 - e0 - e1):
                    e3 = deg - e0 - e1 - e2
                    e = (e0, e1, e2, e3)
                    S = (0, 0)
                    for g in range(n):
                        v = (1, 0)
                        for i in range(4):
                            v = R(v, pw(g, i, e[i]))
                        S = add(S, v)
                    h = haar_monomial(e)
                    lhs = (S[0] * h[1], S[1] * h[1])
                    rhs = (h[0] * n * 2 ** deg, 0)
                    cnt += 1
                    if lhs != rhs:
                        failed.append((e, S, h))
        tested[deg] = cnt
        fails_at[deg] = failed
    ok_through = all(not fails_at[d] for d in range(0, t + 1))
    fail_next = len(fails_at[t + 1]) > 0
    ex = fails_at[t + 1][:3]
    show = ";".join("e=%s,avg=(%d+%dw)/%d,haar=%d/%d" % ("".join(map(str, x[0])), x[1][0], x[1][1], n * 2 ** (t + 1), x[2][0], x[2][1]) for x in ex)
    print("MONOMIALS|group=%s|t=%d|monomials_through_t=%d|mismatches_through_t=%d|monomials_at_t+1=%d|mismatches_at_t+1=%d|examples=%s|json=0" % (name, t, sum(tested[d] for d in range(0, t + 1)), sum(len(fails_at[d]) for d in range(0, t + 1)), tested[t + 1], len(fails_at[t + 1]), show))
    assert ok_through and fail_next
    tot = (0, 0)
    for g in range(n):
        tot = add(tot, pw(g, 0, t + 1))
    print("TRACE_MOMENT|group=%s|k=%d|E_TrU^k=(%d+%dw)/%d|json=0" % (name, t + 1, tot[0], tot[1], n))
print("DESIGNS_EXPLICIT_DONE|json=0")
