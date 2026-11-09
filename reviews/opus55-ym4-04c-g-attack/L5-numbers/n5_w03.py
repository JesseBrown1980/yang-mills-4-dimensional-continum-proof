# n5_w03.py -- L5-numbers lane: row W03 (d = 2 and d = 3 alias sums), exact in Q(sqrt2) with rationals
# as reduced integer pairs, plus interval reads with ilib for the d = 2 closure. Integer only.
import sys
sys.path.insert(0, '/mnt/c/tmp/opus55/ym4-04c-gattack/work/L5-numbers')
import ilib as L
from ilib import rat, add, sub, mul, div, muli, divi, fmti, inside, dec, cos_iv, pi_iv, ln1p_iv

FAILS = []


def row(name, ok, **kv):
    print('NUM|id=' + name + '|' + '|'.join(k + '=' + str(v) for k, v in kv.items()) + '|ok=' + ('1' if ok else '0') + '|json=0')
    if not ok:
        FAILS.append(name)


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def q(n, d=1):
    if d < 0:
        n, d = -n, -d
    g = gcd(n, d) or 1
    return (n // g, d // g)


def qadd(a, b):
    return q(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def qsub(a, b):
    return q(a[0] * b[1] - b[0] * a[1], a[1] * b[1])


def qmul(a, b):
    return q(a[0] * b[0], a[1] * b[1])


def qdiv(a, b):
    assert b[0] != 0
    return q(a[0] * b[1], a[1] * b[0])


Z = q(0)
ONEQ = q(1)


# Q(sqrt2): (a, b) = a + b sqrt2
def sadd(x, y):
    return (qadd(x[0], y[0]), qadd(x[1], y[1]))


def ssub(x, y):
    return (qsub(x[0], y[0]), qsub(x[1], y[1]))


def smul(x, y):
    return (qadd(qmul(x[0], y[0]), qmul(q(2), qmul(x[1], y[1]))), qadd(qmul(x[0], y[1]), qmul(x[1], y[0])))


def sinv(x):
    nrm = qsub(qmul(x[0], x[0]), qmul(q(2), qmul(x[1], x[1])))
    assert nrm[0] != 0
    return (qdiv(x[0], nrm), qdiv((-x[1][0], x[1][1]), nrm))


def sq(r):
    return (r, Z)


# cos(2 pi n / b) for b in {2, 4, 8} in Q(sqrt2)
H = (Z, q(1, 2))     # sqrt2/2


def cos_2pi_n_over_b(n, b):
    k = (8 // b) * n % 8          # angle = k pi / 4
    table = {0: sq(ONEQ), 1: H, 2: sq(Z), 3: (Z, q(-1, 2)), 4: sq(q(-1)), 5: (Z, q(-1, 2)), 6: sq(Z), 7: H}
    return table[k]


def v_of(n, b):
    """4 sin^2(pi n / b) = 2 - 2 cos(2 pi n / b)"""
    c = cos_2pi_n_over_b(n, b)
    return ssub(sq(q(2)), smul(sq(q(2)), c))


def A_d(b, d):
    """A_b = b^{-2} sum_{n in Z_b^{d-1}, n != 0} 1/khat^2(2 pi n/b) - (1 - b^{-2})/12"""
    tot = sq(Z)
    import itertools
    for nvec in itertools.product(range(b), repeat=d - 1):
        if all(c == 0 for c in nvec):
            continue
        k2 = sq(Z)
        for c in nvec:
            k2 = sadd(k2, v_of(c, b))
        tot = sadd(tot, sinv(k2))
    tot = smul(tot, sq(q(1, b * b)))
    return ssub(tot, sq(qdiv(qsub(ONEQ, q(1, b * b)), q(12))))


A3 = {b: A_d(b, 3) for b in (2, 4, 8)}
row('W03_A_d3', A3[2] == (q(3, 32), Z) and A3[4] == (q(73, 384), Z) and A3[8] == (q(54335, 182784), Z),
    A2=str(A3[2]), A4=str(A3[4]), A8=str(A3[8]))
A8 = rat(*A3[8][0])
row('W03_A8_d3_bracket', inside(A8, '0.2972634366', '0.2972634367'), A8=fmti(A8, 12))
inc1 = qsub(A3[4][0], A3[2][0])
inc2 = qsub(A3[8][0], A3[4][0])
I2 = rat(*inc2)
row('W03_increments', inc1 == q(37, 384) and inc2 == q(6529, 60928) and inside(I2, '0.1071592', '0.1071593') and inside(rat(*inc1), '0.09', '0.12')
    and inside(I2, '0.09', '0.12'), inc1=str(inc1), inc2=str(inc2), inc2_dec=fmti(I2, 9), inc1_dec=fmti(rat(*inc1), 9))
row('W03_draft_bracket_excludes_inc2', not inside(I2, '0.10716', '0.10717'), note='the_draft_bracket_[0.10716,0.10717]_excludes_6529/60928')
A2d = {b: A_d(b, 2) for b in (2, 4, 8)}
row('W03_A_d2_zero', all(A2d[b] == sq(Z) for b in (2, 4, 8)), values=str([A2d[b] for b in (2, 4, 8)]))
A4d = {b: A_d(b, 4) for b in (2, 4)}
row('W01_A_d4_check', A4d[2] == (q(23, 96), Z) and A4d[4] == (q(1367, 1920), Z), A1=str(A4d[2]), A2=str(A4d[4]))


# d = 3 corner at q = pi: C' = b^{-1} sum_{n_nu, n_rho} 1/(4 sin^2((pi + 2 pi n_nu)/(2b)) + v(n_rho));
# the n_nu values pair as (c, -c) with c = cos((2n+1) pi/b): 1/(2+v-2c) + 1/(2+v+2c) = 2(2+v)/((2+v)^2 - 4c^2)
def four_c2_pairs(b):
    if b == 2:
        return [sq(Z)]
    if b == 4:
        return [sq(q(2)), sq(q(2))]
    if b == 8:
        return [(q(2), q(1)), (q(2), q(1)), (q(2), q(-1)), (q(2), q(-1))]


def corner_d3(b):
    tot = sq(Z)
    for nr in range(b):
        v = v_of(nr, b)
        tv = sadd(sq(q(2)), v)
        for fc2 in four_c2_pairs(b):
            tot = sadd(tot, smul(smul(sq(q(2)), tv), sinv(ssub(smul(tv, tv), fc2))))
    Cp = smul(tot, sq(q(1, b)))
    r = sinv(smul(sq(q(4)), Cp))         # r = (1/phat^2)/C', phat^2 = 4 at q = pi
    return smul(sq(q(b)), r)             # b * r


cr = {b: corner_d3(b) for b in (2, 4, 8)}
c8 = cr[8]
S2 = L.sqrt_iv(L.const(2))
c8_iv = add(rat(*c8[0]), mul(rat(c8[1][0], c8[1][1]) if c8[1][0] >= 0 else L.neg(rat(-c8[1][0], c8[1][1])), S2))
row('W03_corner_d3', cr[2] == sq(q(3, 4)) and cr[4] == sq(q(119, 208)) and inside(c8_iv, '0.4581134488', '0.4581134489'),
    b2=str(cr[2]), b4=str(cr[4]), b8=str(c8), b8_dec=fmti(c8_iv, 12))


# d = 3, b = 2 profile r_1 at t = tan(q/2): u^2 = cos^2(q/2) = 1/(1+t^2), phat^2 = 4 t^2/(1+t^2)
def r1_d3(t):
    u2 = qdiv(ONEQ, qadd(ONEQ, qmul(t, t)))
    ph2 = qdiv(qmul(q(4), qmul(t, t)), qadd(ONEQ, qmul(t, t)))
    tot = Z
    for v in (q(0), q(4)):
        tv = qadd(q(2), v)
        tot = qadd(tot, qdiv(qmul(q(2), tv), qsub(qmul(tv, tv), qmul(q(4), u2))))
    Cp = qmul(tot, q(1, 2))
    return qdiv(qdiv(ONEQ, ph2), Cp)


prof = [r1_d3(q(1, 16)), r1_d3(q(1, 8)), r1_d3(q(1, 4)), r1_d3(q(1, 2)), r1_d3(q(1))]
# q = pi: u^2 = 0, phat^2 = 4
tot = Z
for v in (q(0), q(4)):
    tv = qadd(q(2), v)
    tot = qadd(tot, qdiv(qmul(q(2), tv), qmul(tv, tv)))
prof.append(qdiv(q(1, 4), qmul(tot, q(1, 2))))
exp_prof = [q(2057, 4120), q(521, 1048), q(137, 280), q(41, 88), q(17, 40), q(3, 8)]
row('W03_profile_d3_k1', prof == exp_prof, profile=','.join(str(p[0]) + '/' + str(p[1]) for p in prof))

# d = 2 closure: r = 1/b^2 at q in {pi/2, 2pi/3, pi}, b = 2, 4, 8, by interval cosines
PI = pi_iv()
TWO_PI = muli(PI, 2)
okd2 = True
worst = 0
for (qn, qd, ph2) in [(1, 2, 2), (2, 3, 3), (1, 1, 4)]:
    qq = div(muli(PI, qn), L.const(qd))
    for b in (2, 4, 8):
        Cp = (0, 0)
        for n in range(b):
            y = div(add(qq, muli(TWO_PI, n)), L.const(b))
            if y[0] > PI[1]:
                y = sub(y, TWO_PI)
            kv = sub(L.const(2), muli(cos_iv(y), 2))
            Cp = add(Cp, div(L.const(1), kv))
        r = div(div(L.const(1), L.const(ph2)), Cp)
        rb2 = muli(r, b * b)
        if not (rb2[0] <= L.ONE <= rb2[1]):
            okd2 = False
        worst = max(worst, rb2[1] - rb2[0])
row('W03_d2_closure_r_eq_1_over_b2', okd2, max_width_bits=worst.bit_length(), P=L.P)
LN2 = ln1p_iv((L.ONE, L.ONE))
row('W03_ln2_over_2pi_display', inside(div(LN2, TWO_PI), '0.1103', '0.1104'), value=fmti(div(LN2, TWO_PI), 8))
print('NUM_N5_END|fails=' + str(len(FAILS)) + '|' + ','.join(FAILS) + '|json=0')
