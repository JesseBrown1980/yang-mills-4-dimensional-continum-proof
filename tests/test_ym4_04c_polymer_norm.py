#!/usr/bin/env python3
"""YM4-04C stage E2g: exact-integer C04 Wilson Haar-sixth-norm pole test.
This is a limited engine stage, NOT the full YM4-04C polymer engine.
No fractions, decimal or floating-point operations. Do not count
COMPUTED pre-freeze C04 as a blind prediction.
"""
import argparse
from math import comb, factorial, gcd

def ipow(base, exponent):
    if exponent < 0:
        raise AssertionError("negative integer exponent")
    value = 1
    for _ in range(exponent):
        value *= base
    return value

def q(n, d=1):
    if d <= 0:
        raise AssertionError("nonpositive denominator")
    g = gcd(n, d)
    return (n // g, d // g)

def add(a, b):
    return q(a[0] * b[1] + b[0] * a[1], a[1] * b[1])

def neg(a):
    return (-a[0], a[1])

def sub(a, b):
    return add(a, neg(b))

def mul(a, b):
    return q(a[0] * b[0], a[1] * b[1])

def div(a, b):
    if b[0] <= 0:
        raise AssertionError("division by nonpositive certificate")
    return q(a[0] * b[1], a[1] * b[0])

def power(a, n):
    if n < 0:
        raise AssertionError("negative exponent")
    return q(ipow(a[0], n), ipow(a[1], n))

def lt(a, b):
    return a[0] * b[1] < b[0] * a[1]

def le(a, b):
    return a[0] * b[1] <= b[0] * a[1]

def c0_bounds(beta):
    """SU2 normalized Haar moment generating function:
    E exp(beta*cos theta) = sum_m (beta*beta/4)^m/(m!*(m+1)!).
    Positive-tail bound by next term and monotone coefficient ratios.
    """
    x = div(mul(beta, beta), q(4))
    term = q(1)
    total = q(0)
    last = 9
    for m in range(last + 1):
        total = add(total, term)
        term = div(mul(term, x), q((m + 1) * (m + 2)))
    ratio_next = div(x, q((last + 2) * (last + 3)))
    if not lt(ratio_next, q(1)):
        raise AssertionError("unbounded positive Wilson series remainder")
    tail_upper = div(term, sub(q(1), ratio_next))
    return (total, add(total, tail_upper))

def e_quarter_bounds():
    """Positive Taylor series and geometric next-ratio remainder."""
    x = q(1, 4)
    term = q(1)
    total = q(0)
    last = 9
    for n in range(last + 1):
        total = add(total, term)
        term = div(mul(term, x), q(n + 1))
    ratio_next = div(x, q(last + 2))
    return total, add(total, div(term, sub(q(1), ratio_next)))

def eps_sixth_power(beta):
    """Exact binomial moment expansion with outward rational enclosures."""
    norm_lo, norm_hi = c0_bounds(beta)
    lo = q(0)
    hi = q(0)
    for j in range(7):
        moment_lo, moment_hi = c0_bounds(mul(q(j), beta))
        if j % 2 == 0:
            lo = add(lo, div(mul(q(comb(6, j)), moment_lo), power(norm_hi, j)))
            hi = add(hi, div(mul(q(comb(6, j)), moment_hi), power(norm_lo, j)))
        else:
            lo = sub(lo, div(mul(q(comb(6, j)), moment_hi), power(norm_lo, j)))
            hi = sub(hi, div(mul(q(comb(6, j)), moment_lo), power(norm_hi, j)))
    if not lt(q(0), lo) or not lt(lo, hi):
        raise AssertionError("not a positive outward L6 norm enclosure")
    return lo, hi

def root_floor(score, digits=9):
    """Floor(10^digits * score^(1/6)) by exact cross-products."""
    scale = ipow(10, digits)
    low, high = 0, 2 * scale
    while high - low > 1:
        mid = (low + high) // 2
        if le(q(ipow(mid, 6), ipow(scale, 6)), score):
            low = mid
        else:
            high = mid
    return low

def scaled_decimal(n, digits=9):
    scale = ipow(10, digits)
    return str(n // scale) + "." + str(n % scale).zfill(digits)

def trial(label, beta, threshold, wall_below=False, sabotage=None):
    lo6, hi6 = eps_sixth_power(beta)
    exp_lo, exp_hi = e_quarter_bounds()
    mu = q(20 ** 20, 19 ** 19)
    if sabotage == "wrong_mu":
        mu = q(19 ** 19, 18 ** 18)
    score_lo = mul(lo6, power(mul(mu, exp_lo), 6))
    score_hi = mul(hi6, power(mul(mu, exp_hi), 6))
    if wall_below:
        if not lt(score_hi, q(1)):
            raise AssertionError("C04_FAIL: frozen wall-lower control is not below 1")
        kind = "NO_POLE_AT_ALPHA_0"
    else:
        if not lt(power(threshold, 6), score_lo):
            raise AssertionError("C04_FAIL: frozen polymer pole guard lower bracket not certified")
        if sabotage == "missing_tail":
            raise AssertionError("C04_FAIL: missing Fuss-Catalan tail and mandatory pole test")
        kind = "NOT_MET_BY_FUSS_CATALAN_POLE"
    lower = root_floor(score_lo)
    upper = root_floor(score_hi) + 1
    return ("YM4_04C_E2G|row=C04|beta=" + str(beta[0]) + "/" + str(beta[1])
            + "|pole_quantity=mu*exp(1/4)*eps6"
            + "|root_bracket=[" + scaled_decimal(lower) + "," + scaled_decimal(upper) + "]"
            + "|read=" + kind
            + "|method=EXACT_HAAR_BESSEL_SERIES_INTERVAL"
            + "|prefreeze=COMPUTED|confirmation_count=0|json=0")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sabotage", choices=["missing_tail", "false_wall", "wrong_mu"])
    args = parser.parse_args()
    rows = [
        ("quarter_beta", q(1, 40), q(11125, 10000), False),
        ("wall_lower", q(2247, 100000), q(1), True),
        ("wall_upper", q(2248, 100000), q(100035, 100000), False),
    ]
    print("YM4_04C_E2G|stage=C04_ONLY|frozen_first_42_lines_sha256=c74e6388295a6309674268dd18deba3728a4eb627a1530c42054182b2fadc404|G_attack_PR46=FILED|engine_only=YES|json=0")
    for name, beta, threshold, below in rows:
        sabotage = None
        if args.sabotage == "missing_tail" and name == "quarter_beta":
            sabotage = "missing_tail"
        if args.sabotage == "wrong_mu" and name == "wall_upper":
            sabotage = "wrong_mu"
        if args.sabotage == "false_wall" and name == "wall_lower":
            below = False
        print(trial(name, beta, threshold, below, sabotage))
    print("YM4_04C_E2G_RESULT|PASS|C04_pole=NOT_MET_at_1/40_and_0.02248|wall_0.02247_below_pole=YES|complete_polymer_engine=NO|weak_coupling=OPEN|r9_runs=0|json=0")

if __name__ == "__main__":
    main()
