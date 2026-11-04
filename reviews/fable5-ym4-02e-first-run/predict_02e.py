# YM4-02e: closed forms only, by characters and by hand-derived 2x2 blocks, with integer pairs. This file holds no lattice, no
# orbit matrix and no cross-ratio search, so it stays separate from the test the rows will be read against. Writes rows. json=0.
import math
import sys


def f(n, d=1):
    assert d != 0
    if d < 0:
        n, d = -n, -d
    g = math.gcd(n, d)
    return n // g, d // g


def add(a, b):
    return f(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def sub(a, b):
    return f(a[0] * b[1] - b[0] * a[1], a[1] * b[1])


def mul(a, b):
    return f(a[0] * b[0], a[1] * b[1])


def div(a, b):
    return f(a[0] * b[1], a[1] * b[0])


def pw(a, k):
    out = (1, 1)
    for _ in range(k):
        out = mul(out, a)
    return out


def show(a):
    return "%d/%d" % a if a[1] != 1 else "%d" % a[0]


ONE = (1, 1)
TWO = (2, 1)
KS = (1, 2, 4, 8)
rows = []


def tau_from_s(s):
    return div(sub(s, ONE), add(s, ONE))


# ---- One link, by characters. kernel(x, y) = sum over irreps of lambda^k chi(x) chi(y).
def z2(q, k):
    rho = div(sub(ONE, q), add(ONE, q))
    x = pw(rho, k)
    return div(add(ONE, x), sub(ONE, x))


def z3(r, k):
    rho = div(sub(ONE, r), add(ONE, mul(TWO, r)))
    x = pw(rho, k)
    return div(add(ONE, mul(TWO, x)), sub(ONE, x))


def q8_sqrt_r(k):
    a, b, c = pw((41, 1), k), pw((15, 1), k), pw((9, 1), k)
    same = add(add(a, mul((3, 1), c)), mul((4, 1), b))
    flip = sub(add(a, mul((3, 1), c)), mul((4, 1), b))
    return div(same, flip)


def t2_sqrt_r(k):
    # In units of 1/384: 121 trivial, 1 twice for the other two characters, 39 and 3 twice on the faithful 2-dim irreps, 9 on the 3-dim.
    even = add(add(pw((121, 1), k), TWO), mul((9, 1), pw((9, 1), k)))
    odd = add(mul((4, 1), pw((39, 1), k)), mul((8, 1), pw((3, 1), k)))
    return div(add(even, odd), sub(even, odd))


for k in KS:
    s = z2((1, 4), k)
    rows.append("YM4_02E_KSTEP|group=Z2|dims=1|weight=q=1/4|k=%d|sqrt_R=%s|tau=%s|json=0" % (k, show(s), show(tau_from_s(s))))
for k in KS:
    s = z3((1, 2), k)
    rows.append("YM4_02E_KSTEP|group=Z3|dims=1|weight=1,1/2,1/2|k=%d|sqrt_R=%s|tau=%s|json=0" % (k, show(s), show(tau_from_s(s))))
for k in KS:
    # S3 in units of 1/36: 19 trivial, 4 standard, 1 sign. Classes e, t, c: standard reads 2, 0, -1; sign reads 1, -1, 1.
    lam0, lam2, lams = pw((19, 1), k), pw((4, 1), k), pw((1, 1), k)
    ee = add(add(lam0, mul((4, 1), lam2)), lams)
    ec = add(sub(lam0, mul(TWO, lam2)), lams)
    cc = add(add(lam0, lam2), lams)
    rows.append("YM4_02E_KSTEP|group=S3|dims=1|weight=1,1/2,1/3|k=%d|R=%s|quadruple=e,c;e,c|json=0" % (k, show(div(mul(ee, cc), mul(ec, ec)))))
for k in KS:
    s = q8_sqrt_r(k)
    rows.append("YM4_02E_KSTEP|group=Q8|dims=1|weight=r=1/2|k=%d|sqrt_R=%s|tau=%s|json=0" % (k, show(s), show(tau_from_s(s))))
for k in KS:
    s = t2_sqrt_r(k)
    rows.append("YM4_02E_KSTEP|group=2T|dims=1|weight=r=1/2|k=%d|sqrt_R=%s|tau=%s|json=0" % (k, show(s), show(tau_from_s(s))))

# ---- Independent links: Z2 with no effective plaquette, n links. tau = ((1+x)^n - (1-x)^n) / ((1+x)^n + (1-x)^n), x = rho^k.
for dims, n in (("1,1", 2), ("1,1,1", 3)):
    for k in KS:
        x = pw((3, 5), k)
        s = pw(div(add(ONE, x), sub(ONE, x)), n)
        rows.append("YM4_02E_PRODUCT|group=Z2|dims=%s|weight=q=1/4|copies=%d|k=%d|sqrt_R=%s|tau=%s|json=0" % (dims, n, k, show(s), show(tau_from_s(s))))

# ---- Z2 on 2x1 at q = 1/2, by hand: T = T_v (two self-loops, A = w(v1 v2)^2) tensor T_W (the holonomy of the two other links).
q = (1, 2)
q2 = mul(q, q)
m11, m12, m22 = add(ONE, q2), mul(TWO, q2), mul(q2, add(ONE, q2))
a = sub(ONE, q2)
rho_w = pw(div(sub(ONE, q), add(ONE, q)), 2)
power = {1: (m11, m12, m22)}
for k in (2, 4, 8):
    p, r, t = power[k // 2]
    power[k] = (add(mul(p, p), mul(r, r)), add(mul(p, r), mul(r, t)), add(mul(r, r), mul(t, t)))
for k in KS:
    e = power[k][0]
    x = pw(a, k)
    sv = div(add(e, x), sub(e, x))
    y = pw(rho_w, k)
    sw = div(add(ONE, y), sub(ONE, y))
    s = mul(sv, sw)
    rows.append("YM4_02E_A_ENTERS|group=Z2|dims=2,1|weight=q=1/2|k=%d|sqrt_R_v=%s|sqrt_R_W=%s|sqrt_R=%s|tau=%s|json=0" % (k, show(sv), show(sw), show(s), show(tau_from_s(s))))
# With A set to 1 inside, the two self-loops are independent: sqrt_R_v = ((1 + x) / (1 - x))^2, x = ((1 - q) / (1 + q))^k.
for k in (2, 4, 8):
    x = pw(div(sub(ONE, q), add(ONE, q)), k)
    sv = pw(div(add(ONE, x), sub(ONE, x)), 2)
    y = pw(rho_w, k)
    sw = div(add(ONE, y), sub(ONE, y))
    rows.append("YM4_02E_NO_A|group=Z2|dims=2,1|weight=q=1/2|k=%d|sqrt_R=%s|json=0" % (k, show(mul(sv, sw))))


# ---- The locality bound: r from epsilon and sigma, rounded up to ppm, with phi(r) <= 1 checked in integers.
def local_r_ppm(eps, sigma):
    c = add(mul(TWO, eps), sigma)
    assert c[0] < c[1]
    # r = ((1 - sigma) - sqrt((1 - sigma)^2 - 4 eps^2)) / (2 eps), the smaller root of eps (x + 1/x) + sigma = 1.
    lo, hi = 0, 1000000
    while hi - lo > 1:
        mid = (lo + hi) // 2
        x = (mid, 1000000)
        phi = add(mul(eps, add(x, div(ONE, x))), sigma)
        if phi[0] <= phi[1]:
            hi = mid
        else:
            lo = mid
    return hi


def neighbours(dims):
    # max over links of the sum over other links of the number of plaquettes shared, from the plaquette lists alone.
    import itertools as it
    sites = list(it.product(*[range(d) for d in dims]))

    def step(s, mu):
        moved = list(s)
        moved[mu] = (moved[mu] + 1) % dims[mu]
        return tuple(moved)

    plaquettes = []
    for s in sites:
        for mu, nu in it.combinations(range(len(dims)), 2):
            plaquettes.append({(s, mu), (step(s, mu), nu), (step(s, nu), mu), (s, nu)})
    best = 0
    for s in sites:
        for mu in range(len(dims)):
            link = (s, mu)
            best = max(best, sum(len(p) - 1 for p in plaquettes if link in p))
    return best


q8r = f(160000 - 130321, 160000 + 130321)
for group, label, eps, spec in (
    ("Z2", "q=4/5", (1, 9), ("1", "1,1", "2,1", "3,1", "4,1", "5,1", "6,1", "2,2", "3,2")),
    ("Z2", "q=7/8", (1, 15), ("1,1,1", "2,1,1", "2,2,1")),
    ("Z3", "1,8/9,8/9", (1, 17), ("1", "2,1", "3,1", "2,2")),
    ("S3", "1,9/10,4/5", (1, 9), ("1", "1,1")),
    ("Q8", "r=19/20", q8r, ("1", "1,1", "1,1,1")),
    ("2T", "r=19/20", q8r, ("1", "1,1")),
):
    for dims in spec:
        count = neighbours(tuple(int(d) for d in dims.split(",")))
        sigma = mul((count, 1), eps)
        c = add(mul(TWO, eps), sigma)
        if c[0] >= c[1]:
            rows.append("YM4_02E_LOCAL_OUTSIDE|group=%s|dims=%s|weight=%s|epsilon=%s|neighbours=%d|c=%s|json=0" % (group, dims, label, show(eps), count, show(c)))
            continue
        rows.append("YM4_02E_LOCAL|group=%s|dims=%s|weight=%s|epsilon=%s|neighbours=%d|sigma=%s|c=%s|r_ppm_ceil=%d|json=0" % (
            group, dims, label, show(eps), count, show(sigma), show(c), local_r_ppm(eps, sigma)))
print("\n".join(rows))

# ---- q(L) for the ring at fixed mu: x q^2 + (x + 1) q - 1 = 0 with x = exp(-mu/L), in 10^-9 fixed point, rounded to 1/1000.
SCALE = 1000000000


def exp_minus(num, den):
    # exp(-num/den) by its series, in integers.
    total, term, n, sign = SCALE, SCALE, 1, -1
    while term:
        term = term * num // (den * n)
        total += sign * term
        sign = -sign
        n += 1
    return total


for mu in (1, 2):
    for L in (2, 3, 4, 5, 6, 7, 8):
        x = exp_minus(mu, L)
        b = x + SCALE
        disc = b * b + 4 * x * SCALE
        root = math.isqrt(disc)
        q_scaled = (root - b) * SCALE // (2 * x)
        q3 = (q_scaled + 500000) // 1000000
        print("YM4_02E_RING|group=Z2|dims=%d,1|mu=%d|x_ppm=%d|weight=q=%d/1000|json=0" % (L, mu, x // 1000, q3))
