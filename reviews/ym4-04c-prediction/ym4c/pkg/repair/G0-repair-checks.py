# G0 repair scratch checks. Integers and Fractions only, outward dyadic rounding.
# Not an engine and not evidence. Floats appear only in display (fmt).
# Shares no code with G0-a-*.py, G0-b-checks.py or the attack scripts.
import sys
from fractions import Fraction as Q
from math import comb, factorial

B = 288  # bits kept after each outward rounding


def up(x, b=B):
    x = Q(x)
    if x == 0:
        return x
    n, d = x.numerator, x.denominator
    s = max(0, b - (n.bit_length() - d.bit_length()))
    return Q(-((-n << s) // d), 1 << s)


def down(x, b=B):
    x = Q(x)
    if x == 0:
        return x
    n, d = x.numerator, x.denominator
    s = max(0, b - (n.bit_length() - d.bit_length()))
    return Q((n << s) // d, 1 << s)


def fmt(x, k=12):
    return format(x.numerator / x.denominator, '.%dg' % k)


def exp_enc(y, M=60):
    """[lo, hi] with lo <= e^y <= hi, for rational y (range reduction by halving)."""
    y = Q(y)
    if y < 0:
        lo, hi = exp_enc(-y, M)
        return down(1 / hi), up(1 / lo)
    if y > Q(1, 2):
        lo, hi = exp_enc(y / 2, M)
        return down(lo * lo), up(hi * hi)
    s, t = Q(0), Q(1)
    for m in range(M + 1):
        s += t
        t = t * y / (m + 1)
    # remainder: t * sum_j (y/(M+2))^j <= t / (1 - y/(M+2))
    rem = t / (1 - y / (M + 2))
    return down(s), up(s + rem)


def c0_enc(x, M=40):
    """[lo, hi] for c_0(x) = sum_m (x/2)^{2m}/(m!(m+1)!), x >= 0 rational."""
    x = Q(x)
    q = (x / 2) ** 2
    s, t = Q(0), Q(1)
    for m in range(M + 1):
        s += t
        t = t * q / ((m + 1) * (m + 2))
    rem = t / (1 - q / ((M + 2) * (M + 3)))
    return s, s + rem


def eps6_enc(beta):
    """[lo, hi] for eps_6(beta) = (sum_k C(6,k)(-1)^{6-k} c0(k beta)/c0(beta)^k)^{1/6}."""
    c1lo, c1hi = c0_enc(beta)
    lo, hi = Q(0), Q(0)
    for k in range(7):
        ck_lo, ck_hi = c0_enc(k * beta)
        r_lo, r_hi = ck_lo / c1hi ** k, ck_hi / c1lo ** k
        sgn = (-1) ** (6 - k) * comb(6, k)
        if sgn > 0:
            lo += sgn * r_lo
            hi += sgn * r_hi
        else:
            lo += sgn * r_hi
            hi += sgn * r_lo
    assert 0 < lo <= hi
    return root6_down(lo), root6_up(hi)


def iroot(n, k):
    """floor(n^{1/k}) for integer n >= 0."""
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + k - 1) // k)
    while True:
        y = ((k - 1) * x + n // x ** (k - 1)) // k
        if y >= x:
            break
        x = y
    while x ** k > n:
        x -= 1
    while (x + 1) ** k <= n:
        x += 1
    return x


def root6_down(r, bits=200):
    n = (r.numerator << (6 * bits)) // r.denominator
    return Q(iroot(n, 6), 1 << bits)


def root6_up(r, bits=200):
    n = -((-r.numerator << (6 * bits)) // r.denominator)
    z = iroot(n, 6)
    if z ** 6 < n:
        z += 1
    return Q(z, 1 << bits)


F = lambda n: comb(20 * n, n) // (19 * n + 1)
MU = Q(20 ** 20, 19 ** 19)
HEADS = {
    'crude': {n: 6 * F(n) for n in range(4, 11)},
    'C03': dict(zip(range(4, 11), [1, 0, 12, 0, 32, 32, 304])),
    'headfree': {n: 0 for n in range(4, 11)},
}


def S_exact(x, head):
    """The frozen closed form S(x); None if mu*x >= 1."""
    if MU * x >= 1:
        return None
    s = Q(0)
    p = x ** 4
    for n in range(4, 49):
        s += (head[n] if n <= 10 else 6 * F(n)) * p
        p *= x
    s += 6 * F(49) * p / (1 - MU * x)  # p = x^49 here
    return s


def S_up(x, head):
    s = S_exact(up(x), head)
    return None if s is None else up(s)


def S_down(x, head):
    s = S_exact(down(x), head)
    return None if s is None else down(s)


def alpha_bracket(eps, head, theta=Q(1, 4), iters=60):
    """Lower iterate from 0 and an upper certificate; None if the lower iterate leaves the domain."""
    elo, ehi = eps
    a = Q(0)
    for _ in range(iters):
        xlo = down(elo * exp_enc(2 * a + theta)[0])
        s = S_down(xlo, head)
        if s is None or s > Q(1, 4):
            return None
        a = s
    a_lo = a
    a_up = up(a_lo * (1 + Q(1, 10 ** 12)) + Q(1, 2 ** 200))
    xhi = up(ehi * exp_enc(2 * a_up + theta)[1])
    s = S_up(xhi, head)
    ok = s is not None and s <= a_up
    return a_lo, a_up, ok


out = []


def P(*a):
    line = ' '.join(str(t) for t in a)
    out.append(line)
    print(line, flush=True)


# A. Fuss-Catalan, mu, ratios
frozenF = [20540, 784245, 31763004, 1340246340, 58281448940, 2593593086150,
           117544525178080, 5406686759963586, 251754316822792420]
P('A F_20(4..12) equal frozen:', [F(n) for n in range(4, 13)] == frozenF)
P('A mu in [53.00068,53.00069]:', 5300068 * 19 ** 19 <= 100000 * 20 ** 20 <= 5300069 * 19 ** 19)
ok = True
prev = None
for n in range(0, 401):
    r = Q(F(n + 1), F(n))
    prod = 20 * Q(1)
    for j in range(1, 20):
        prod *= Q(20 * n + j, 19 * n + j + 1)
    ok &= (r == prod) and (r < MU) and (prev is None or r > prev)
    prev = r
P('A product formula, strict increase, below mu, n=0..400:', ok)
P('A F(n+2)/F(n), n=4..10:', [fmt(Q(F(n + 2), F(n)), 7) for n in range(4, 11)])
P('A F(n+2)/F(n) > 2000 exactly from n =', min(n for n in range(1, 40) if Q(F(n + 2), F(n)) > 2000))

# B. pi, Machin, E|chi|
z = (5 + 1j) ** 4 * (239 - 1j)
P('B (5+i)^4 (239-i) =', z, '(real part = imaginary part, so Machin holds)')
at5_lo = Q(1, 5) - Q(1, 3 * 5 ** 3) + Q(1, 5 * 5 ** 5) - Q(1, 7 * 5 ** 7)
pi_lo = 16 * at5_lo - 4 * Q(1, 239)
P('B pi_lo =', pi_lo, '>', Q(333, 106), ':', pi_lo > Q(333, 106))
def atan_enc(y, K=24):
    s = Q(0)
    for k in range(K):
        s += (-1) ** k * y ** (2 * k + 1) / (2 * k + 1)
    return s, s + y ** (2 * K + 1) / (2 * K + 1)  # K even: partial sum ends negative, so it is a lower bound
a5 = atan_enc(Q(1, 5)); a239 = atan_enc(Q(1, 239))
pi_lo2, pi_hi = 16 * a5[0] - 4 * a239[1], 16 * a5[1] - 4 * a239[0]
assert pi_lo2 >= pi_lo
P('B pi in [', fmt(pi_lo2, 15), ',', fmt(pi_hi, 15), '], width', fmt(pi_hi - pi_lo2, 3))
e_lo, e_hi = 8 / (3 * pi_hi), 8 / (3 * pi_lo2)
P('B 8/(3pi) in [', fmt(down(e_lo), 12), ',', fmt(up(e_hi), 12), ']; outward 7-digit: [0.8488263,0.8488264]:',
  Q(8488263, 10 ** 7) <= e_lo and e_hi <= Q(8488264, 10 ** 7))
P('B 848/999 < 8489/10000:', Q(848, 999) < Q(8489, 10000), '; 8/(3pi) < 8489/10000:', e_hi < Q(8489, 10000))
P('B margin 8489/10000 - 8/(3pi) >=', fmt(Q(8489, 10000) - e_hi, 6))

# C. eps_6 and the certificate at theta = 1/4
FROZEN_EPS = {Q(1, 100): (Q(6538419, 10 ** 9), Q(6538420, 10 ** 9)),
              Q(1, 64): (Q(10216544, 10 ** 9), Q(10216545, 10 ** 9)),
              Q(1, 50): (Q(13077541, 10 ** 9), Q(13077542, 10 ** 9))}
EPS = {}
for beta, (flo, fhi) in FROZEN_EPS.items():
    e = eps6_enc(beta)
    EPS[beta] = e
    P('C eps6(%s) in [%s, %s]; inside C02 bracket: %s' % (beta, fmt(e[0], 13), fmt(e[1], 13), flo <= e[0] and e[1] <= fhi))

res = {}
for beta in [Q(1, 100), Q(1, 64), Q(1, 50)]:
    for name in ['crude', 'C03', 'headfree']:
        r = alpha_bracket(EPS[beta], HEADS[name])
        if r is None:
            P('C beta=%s %s: lower iterate leaves the domain or passes 1/4 (no certificate)' % (beta, name))
            continue
        a_lo, a_up, ok = r
        res[(beta, name)] = (a_lo, a_up)
        d6lo, d6hi = 6 * a_lo, 6 * a_up
        dp_hi = up(2 * d6hi * exp_enc(d6hi)[1])
        dp_lo = down(2 * d6lo * exp_enc(d6lo)[0])
        P('C beta=%s %s: certified %s; alpha_- in [%s, %s]; 12alpha in [%s, %s]; 6alpha in [%s, %s]; 2delta\'(6) in [%s, %s]' % (
            beta, name, ok, fmt(a_lo), fmt(a_up), fmt(12 * a_lo), fmt(12 * a_up), fmt(d6lo), fmt(d6hi), fmt(dp_lo), fmt(dp_hi)))

# D. Edges with the factor 6 (G1 as drafted: admissible iff C_0 MET and 6 alpha_- < delta_crit^-)
DC_LO, DC_HI = Q(496174, 10 ** 7), Q(496175, 10 ** 7)   # C13 bracket of delta_crit


def edge_read(beta, head, factor, thr_met, thr_not):
    e = eps6_enc(beta)
    r = alpha_bracket(e, head)
    if r is None:
        return 'C_0 lower iterate leaves domain: NOT_MET'
    a_lo, a_up, ok = r
    met = ok and factor * a_up < thr_met
    notmet = factor * a_lo >= thr_not
    return 'MET certified=%s (%d*alpha<=%s), NOT_MET certified=%s (%d*alpha_->=%s)' % (
        met, factor, fmt(factor * a_up, 10), notmet, factor, fmt(factor * a_lo, 10))


for name, pair in [('crude', (Q(1556, 10 ** 5), Q(1557, 10 ** 5))),
                   ('C03', (Q(2029, 10 ** 5), Q(2030, 10 ** 5))),
                   ('headfree', (Q(2029, 10 ** 5), Q(2030, 10 ** 5)))]:
    for beta in pair:
        P('D factor 6 %s at %s: %s' % (name, fmt(beta, 6), edge_read(beta, HEADS[name], 6, DC_LO, DC_HI)))
for beta in [Q(1552, 10 ** 5), Q(1553, 10 ** 5)]:
    P('D surrogate delta_1<=49/1000, factor 6, crude at %s: %s' % (
        fmt(beta, 6), edge_read(beta, HEADS['crude'], 6, Q(49, 1000) + Q(1, 10 ** 30), Q(49, 1000) + Q(1, 10 ** 30))))
if len(sys.argv) > 1:
    for name, pair in [('crude', (Q(1369, 10 ** 5), Q(1370, 10 ** 5))), ('C03', (Q(1959, 10 ** 5), Q(1960, 10 ** 5)))]:
        for beta in pair:
            P('D factor 12 %s at %s: %s' % (name, fmt(beta, 6), edge_read(beta, HEADS[name], 12, DC_LO, DC_HI)))

# F. C08 and C09 spot reads with the proved prefactor 6 (P_10 is the MEASURED YM4-03C series)
def P10(b):
    return b ** 4 / 128 - b ** 6 / 768 + b ** 8 / 1536 - 467 * b ** 10 / 2211840
elo, ehi = exp_enc(1)
b = Q(1, 100)
a_lo, a_up = res[(b, 'C03')]
w_lo, w_hi = 12 * elo * P10(b), 12 * ehi * P10(b)
P('F C08: 12e*P_10(1/100) in [%s, %s]; 6alpha_-(C03)/(12e P_10) in [%s, %s]; crude/C03 ratio in [%s, %s]' % (
    fmt(w_lo, 8), fmt(w_hi, 8), fmt(6 * a_lo / w_hi, 8), fmt(6 * a_up / w_lo, 8),
    fmt(res[(b, 'crude')][0] / a_up, 8), fmt(res[(b, 'crude')][1] / a_lo, 8)))
for bb, i in [(Q(1, 4000), 194), (Q(1, 2000), 150), (Q(1, 1000), 105), (Q(1, 700), 83), (Q(1, 600), 73), (Q(1, 100), 0)]:
    th = Q(1, 4) + Q(i, 64)
    e = eps6_enc(bb)
    r = alpha_bracket(e, HEADS['C03'], theta=th)
    a_lo, a_up, ok = r
    t_lo = Q(8489, 10000) * 6 * a_lo * exp_enc(-8 * th)[0]
    t_hi = Q(8489, 10000) * 6 * a_up * exp_enc(-8 * th)[1]
    P('F C09 at beta=%s, i=%d: certified %s; T6/P_10 in [%s, %s]; T12/P_10 in [%s, %s]' % (
        bb, i, ok, fmt(t_lo / P10(bb), 6), fmt(t_hi / P10(bb), 6), fmt(2 * t_lo / P10(bb), 6), fmt(2 * t_hi / P10(bb), 6)))

# E. Monotonicity of eps_6 on a few grid points (a check of the lemma, not its proof)
pts = [Q(k, 10 ** 5) for k in (1000, 1500, 1556, 1557, 1904, 2029, 2030, 2075, 2247)]
encs = [eps6_enc(b) for b in pts]
P('E eps6 increasing on the sample grid:', all(encs[i][1] < encs[i + 1][0] for i in range(len(encs) - 1)))

with open(__file__.replace('.py', '.out'), 'w') as f:
    f.write('\n'.join(out) + '\n')
