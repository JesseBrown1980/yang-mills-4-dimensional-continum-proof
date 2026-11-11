#!/usr/bin/env python3
"""YM4-03: exact finite SU(2) gauge-block identities and Wilson character tail.

Rational unit quaternions test continuous-SU(2) group identities on a
noncommuting subset. Q8 is a separate exact finite-group negative-control
family, not a replacement for Haar integration on SU(2). Continuous SU(2)
Haar/character claims are proved in docs/NOTE-YM4-03-GPT6-ONE-SCALE.md, and the
certified Wilson tail is re-evaluated with rational integer pairs here.

Run: python3 tests/test_one_scale_block_gpt6.py [sabotage=NAME]
A named sabotage must produce a failing control and exit 2. json=0.
"""
import itertools
import math
import sys

SABOTAGES = ("swap_order", "wrong_endpoint", "drop_inverse_loop", "wrong_convolution")
args = sys.argv[1:]
if len(args) > 1 or (args and (not args[0].startswith("sabotage=") or args[0][9:] not in SABOTAGES)):
    raise SystemExit(2)
SABOTAGE = args[0][9:] if args else ""


def power(base, exponent):
    if exponent < 0:
        raise ValueError("non-negative power required")
    out = 1
    for _ in range(exponent):
        out *= base
    return out


def rat(a, b=1):
    if b == 0:
        raise ZeroDivisionError("denominator")
    if b < 0:
        a, b = -a, -b
    g = math.gcd(a, b)
    return a // g, b // g


def radd(a, b):
    return rat(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def rneg(a):
    return -a[0], a[1]


def rsub(a, b):
    return radd(a, rneg(b))


def rmul(a, b):
    return rat(a[0] * b[0], a[1] * b[1])


def rdiv(a, b):
    return rat(a[0] * b[1], a[1] * b[0])


def rpower(a, exponent):
    if exponent < 0:
        raise ValueError("non-negative rational power required")
    out = rat(1)
    for _ in range(exponent):
        out = rmul(out, a)
    return out


def rlt(a, b):
    return a[0] * b[1] < b[0] * a[1]


def rle(a, b):
    return a[0] * b[1] <= b[0] * a[1]


def rstr(a):
    return str(a[0]) if a[1] == 1 else str(a[0]) + "/" + str(a[1])


# ---- SU(2) as rational unit quaternions (a,b,c,d)/denominator.
def unit(a, b, c, d, den):
    if den <= 0 or a*a + b*b + c*c + d*d != den*den:
        raise ValueError("quaternion outside unit 3-sphere")
    g = math.gcd(math.gcd(math.gcd(math.gcd(abs(a), abs(b)), abs(c)), abs(d)), den)
    return a // g, b // g, c // g, d // g, den // g


def qmul(x, y):
    a, b, c, d, e = x
    f, g, h, k, l = y
    return unit(a*f - b*g - c*h - d*k,
                a*g + b*f + c*k - d*h,
                a*h - b*k + c*f + d*g,
                a*k + b*h - c*g + d*f, e*l)


def qinv(x):
    a, b, c, d, e = x
    return a, -b, -c, -d, e


def qprod(*xs):
    v = ID
    for x in xs:
        v = qmul(v, x)
    return v


ID = unit(1, 0, 0, 0, 1)
QI = unit(3, 4, 0, 0, 5)
QJ = unit(5, 0, 12, 0, 13)
QK = unit(7, 0, 0, 24, 25)
GENERATORS = [ID, QI, QJ, QK, qmul(QI, QJ), qmul(QJ, QK), qmul(QK, QI), qinv(QI)]


def step(x, mu, length=4):
    v = list(x)
    v[mu] = (v[mu] + 1) % length
    return tuple(v)


def step2(x, mu):
    return step(step(x, mu), mu)


def block(field, sites):
    return {(x, mu): qmul(field[(x, mu)], field[(step(x, mu), mu)])
            for x in sites for mu in range(4)}


def block_bad_order(field, sites):
    return {(x, mu): qmul(field[(step(x, mu), mu)], field[(x, mu)])
            for x in sites for mu in range(4)}


def plaquette(field, x, mu, nu):
    return qprod(field[(x, mu)], field[(step2(x, mu), nu)],
                 qinv(field[(step2(x, nu), mu)]), qinv(field[(x, nu)]))


def fine_rectangle(field, x, mu, nu, bad=False):
    right = step2(x, mu)
    up = step2(x, nu)
    vals = [field[(x, mu)], field[(step(x, mu), mu)],
            field[(right, nu)], field[(step(right, nu), nu)],
            qinv(field[(step(up, mu), mu)]), qinv(field[(up, mu)]),
            qinv(field[(step(x, nu), nu)]), qinv(field[(x, nu)])]
    if bad:
        vals[4] = qinv(vals[4])
    return qprod(*vals)


def su2_lattice_check():
    sites = list(itertools.product(range(4), repeat=4))
    coarse = list(itertools.product((0, 2), repeat=4))
    u = {(x, mu): GENERATORS[(sum((i+1)*(v+1) for i, v in enumerate(x)) + 3*mu + x[mu]) % len(GENERATORS)]
         for x in sites for mu in range(4)}
    g = {x: GENERATORS[(sum((i+2)*(v+1) for i, v in enumerate(x)) + 3*x[0]) % len(GENERATORS)]
         for x in sites}
    transformed = {(x, mu): qprod(g[x], u[(x, mu)], qinv(g[step(x, mu)]))
                   for x in sites for mu in range(4)}
    B = block(u, coarse)
    Bprime = block(transformed, coarse) if SABOTAGE != "swap_order" else block_bad_order(transformed, coarse)
    if SABOTAGE == "swap_order":
        B = block_bad_order(u, coarse)
    endpoint_good = 0
    for x in coarse:
        for mu in range(4):
            endpoint = step2(x, mu) if SABOTAGE != "wrong_endpoint" else step(x, mu)
            wanted = qprod(g[x], B[(x, mu)], qinv(g[endpoint]))
            endpoint_good += int(Bprime[(x, mu)] == wanted)
    loops_good = 0
    gauge_trace_good = 0
    for x in coarse:
        for mu in range(4):
            for nu in range(mu + 1, 4):
                f = fine_rectangle(u, x, mu, nu, bad=SABOTAGE == "drop_inverse_loop")
                v = plaquette(B, x, mu, nu)
                loops_good += int(f == v)
                vp = plaquette(Bprime, x, mu, nu)
                gauge_trace_good += int(vp[0] * v[4] == v[0] * vp[4])
    if SABOTAGE in ("swap_order", "wrong_endpoint", "drop_inverse_loop"):
        if endpoint_good == 64 and loops_good == 96 and gauge_trace_good == 96:
            raise SystemExit("CONTROL_SURVIVED")
        print("YM4_03_SABOTAGE|name=" + SABOTAGE + "|result=REJECTED|json=0")
        raise SystemExit(2)
    if not (endpoint_good == 64 and loops_good == 96 and gauge_trace_good == 96):
        raise SystemExit("SU2_COVARIANCE_OR_LOOP_FAIL")
    if qmul(QI, QJ) == qmul(QJ, QI):
        raise SystemExit("NONCOMMUTATIVE_CONTROL_MISSING")
    return endpoint_good, loops_good, gauge_trace_good


# ---- Q8 finite-group arithmetic. This checks noncommuting identities only.
Q8 = [(s if j == 0 else 0, s if j == 1 else 0, s if j == 2 else 0, s if j == 3 else 0)
      for j in range(4) for s in (1, -1)]
INDEX = {v: i for i, v in enumerate(Q8)}


def q8mul(a, b):
    x = Q8[a]
    y = Q8[b]
    aa, ab, ac, ad = x
    ba, bb, bc, bd = y
    value = (aa*ba-ab*bb-ac*bc-ad*bd,
             aa*bb+ab*ba+ac*bd-ad*bc,
             aa*bc-ab*bd+ac*ba+ad*bb,
             aa*bd+ab*bc-ac*bb+ad*ba)
    return INDEX[value]


def q8inv(i):
    a,b,c,d = Q8[i]
    return INDEX[(a,-b,-c,-d)]


def q8conv(f, g):
    out = []
    for v in range(8):
        total = rat(0)
        for x in range(8):
            term = rmul(f[x], g[q8mul(q8inv(x), v)])
            total = radd(total, term)
        out.append(rdiv(total, rat(8)))
    return out


def q8_checks():
    # Exactly 8 choices for each of two links and three gauge vertices.
    cases = 0
    for u, v, ga, gm, gb in itertools.product(range(8), repeat=5):
        left = q8mul(q8mul(q8mul(ga, u), q8inv(gm)), q8mul(q8mul(gm, v), q8inv(gb)))
        right = q8mul(q8mul(ga, q8mul(u, v)), q8inv(gb))
        if left != right:
            raise SystemExit("Q8_NONCOMMUTING_GAUGE_FAIL")
        cases += 1
    # χ is the character of the defining two-dimensional SU(2) irrep,
    # restricted to Q8 (also irreducible there). t = 1/4.
    t = rat(1, 4)
    chi = [2*e[0] for e in Q8]
    weights = [radd(rat(1), rmul(t, rat(v))) for v in chi]
    f = weights
    for _ in range(3):
        f = q8conv(f, weights)
    if SABOTAGE == "wrong_convolution":
        expected = [radd(rat(1), rmul(rat(1, 4096), rat(v))) for v in chi]
    else:
        expected = [radd(rat(1), rmul(rat(1, 2048), rat(v))) for v in chi]
    if SABOTAGE == "wrong_convolution":
        if f == expected:
            raise SystemExit("CONVOLUTION_MUTANT_SURVIVED")
        print("YM4_03_SABOTAGE|name=wrong_convolution|result=REJECTED|json=0")
        raise SystemExit(2)
    if f != expected or rdiv(radd(rat(0), sum_rat(f)),rat(8)) != rat(1):
        raise SystemExit("Q8_FOURFOLD_CONVOLUTION_FAIL")
    return cases, f


def sum_rat(a):
    out = rat(0)
    for v in a:
        out = radd(out,v)
    return out


# ---- Continuous SU(2) Wilson tile: exact character and Bessel-series tails.
def fn_interval(n, K):
    # f_n(q)=sum_{k>=0} q^(n+2k)/(k! (n+k+1)!), q=beta/2.
    q = rat(1, 2)
    partial = rat(0)
    for k in range(K + 1):
        term = rdiv(rpower(q, n + 2*k), rat(math.factorial(k)*math.factorial(n+k+1)))
        partial = radd(partial, term)
    omitted = rdiv(rpower(q, n + 2*K + 2), rat(math.factorial(K+1)*math.factorial(n+K+2)))
    ratio = rdiv(rmul(q,q), rat((K+2)*(n+K+3)))
    bound = rdiv(omitted, rsub(rat(1), ratio))
    return partial, radd(partial, bound)


def su2_character_tail():
    f0low, f0high = fn_interval(0, 8)
    if not rlt(f0low, f0high):
        raise SystemExit("SERIES_INTERVAL_UNORDERED")
    density_lower_from_series = rat(1)
    for n in (1,2):
        fnlow, fnhigh = fn_interval(n, 8)
        blow = rdiv(fnlow, f0high)
        bhigh = rdiv(fnhigh, f0low)
        if not rlt(blow, bhigh):
            raise SystemExit("CHARACTER_RATIO_INTERVAL_FAIL")
        density_lower_from_series = rsub(density_lower_from_series, rmul(rat((n+1)*(n+1)),rpower(bhigh, 4)))
    q = rat(1,2)
    n = 3
    first = rdiv(rmul(rmul(rpower(rat(4,3),4),rat((n+1)*(n+1))),rpower(q,4*n)),rat(power(math.factorial(n+1),4)))
    ratio = rdiv(rpower(q,4),rat((n+1)*(n+1)*(n+2)*(n+2)))
    err = rdiv(first,rsub(rat(1),ratio))
    lower = rsub(rsub(rat(1),rat(4,81)),rat(1,11664))
    action_err = rdiv(err,rsub(lower,err))
    if err != rat(25,671741424) or lower != rat(11087,11664) or action_err != rat(25,638511392):
        raise SystemExit("REGISTERED_EXACT_RATIONAL_FORMULA_FAIL")
    if not (rlt(err,rat(1,25_000_000)) and rlt(rat(19,20),lower) and
            rlt(rat(19,20),density_lower_from_series) and
            rlt(action_err,rat(1,20_000_000))):
        raise SystemExit("WILSON_TAIL_CERTIFICATE_FAIL")
    if rmul(rat(2),rpower(rat(1,4),4)) != rat(1,128):
        raise SystemExit("SU2_FUNDAMENTAL_LEADING_COEFFICIENT_FAIL")
    return err, lower, action_err


def main():
    gauged, loops, traces = su2_lattice_check()
    count, f = q8_checks()
    err, lower, action_err = su2_character_tail()
    print("YM4_03_GAUGE|fine_sites=256|fine_links=1024|coarse_sites=16|coarse_links=64|fine_to_coarse_covariant=" + str(gauged) + "|SU2_noncommuting=1|json=0")
    print("YM4_03_LOOP|coarse_plaquettes=" + str(loops) + "|fine_boundaries_equal=" + str(loops) + "|trace_invariant=" + str(traces) + "|json=0")
    print("YM4_03_Q8|gauge_assignments=" + str(count) + "|fourfold_identity=" + rstr(f[0]) + "|minus_identity=" + rstr(f[1]) + "|others_one=" + str(sum(1 for x in f[2:] if x == rat(1))) + "|json=0")
    print("YM4_03_WILSON|beta_range=0_to_1|chars=0,1,2|density_error_upper=" + rstr(err) + "|truncated_density_lower=" + rstr(lower) + "|effective_action_error_upper=" + rstr(action_err) + "|json=0")
    print("YM4_03_DONE|result=PASS|json=0")


if __name__ == "__main__":
    main()
