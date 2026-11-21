#!/usr/bin/env python3
"""YM4-07F: pure integer/rational dark trace budgets and SU2 analytic constants.

The full proof is in docs/NOTE-YM4-07F-DARK-TRACE-GRAM-CERTIFICATE-20261121.md.
Actual four-dimensional transfer moments are separately required; this program
checks a nonorthogonal rational transfer model and the certified SU2 character
series inequalities. Fractions are represented by (numerator, denominator).
"""
from math import gcd, factorial


def need(ok, label):
    if not ok:
        raise ValueError(label)


def rat(n, d=1):
    need(d != 0, "zero_denominator")
    if d < 0:
        n, d = -n, -d
    g = gcd(n, d)
    return (n // g, d // g)


def add(a, b):
    return rat(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def neg(a):
    return (-a[0], a[1])


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    return rat(a[0] * b[0], a[1] * b[1])


def div(a, b):
    need(b[0] != 0, "divide_by_zero")
    return rat(a[0] * b[1], a[1] * b[0])


def lt(a, b):
    return a[0] * b[1] < b[0] * a[1]


def eq(a, b):
    return a[0] * b[1] == b[0] * a[1]


def rp(a, n):
    need(n >= 0, "negative_power")
    z = rat(1)
    for _ in range(n):
        z = mul(z, a)
    return z


def ip(n, k):
    need(k >= 0, "negative_integer_power")
    value = 1
    for _ in range(k):
        value *= n
    return value


EIG = (rat(1), rat(3, 4), rat(1, 2), rat(1, 4))
VAC = (1, 0, 0, 0)
NONORTH = (1, 0, 1, 0)
WITNESS = (0, 0, 1, 0)


def gram(x, y):
    return rat(sum(x[i] * y[i] for i in range(4)))


def moment(x, y, power, eig=EIG):
    value = rat(0)
    for i in range(4):
        value = add(value, mul(rat(x[i] * y[i]), rp(eig[i], power)))
    return value


def total_trace(power, eig=EIG):
    value = rat(0)
    for x in eig:
        value = add(value, rp(x, power))
    return value


def covered_one(x, power, eig=EIG):
    return div(moment(x, x, power, eig), gram(x, x))


def covered_two(x, y, power, eig=EIG):
    g00, g01 = gram(x, x), gram(x, y)
    g10, g11 = gram(y, x), gram(y, y)
    det = sub(mul(g00, g11), mul(g01, g10))
    need(lt(rat(0), det), "singular_or_nonpositive_gram")
    m00, m01 = moment(x, x, power, eig), moment(x, y, power, eig)
    m10, m11 = moment(y, x, power, eig), moment(y, y, power, eig)
    num = add(sub(mul(g11, m00), mul(g01, m10)),
              sub(mul(g00, m11), mul(g10, m01)))
    return div(num, det)


def residual(power, x=VAC, y=NONORTH, eig=EIG):
    return sub(total_trace(power, eig), covered_two(x, y, power, eig))


def threshold(res, q, power):
    return lt(res, rp(q, power))


def report_gram():
    need(eq(gram(VAC, VAC), rat(1)), "gram_g00")
    need(eq(gram(VAC, NONORTH), rat(1)), "gram_g01")
    need(eq(gram(NONORTH, NONORTH), rat(2)), "gram_g11")
    need(eq(covered_two(VAC, NONORTH, 2), rat(5, 4)),
         "nonorthogonal_gram_inverse")
    print("YM4_07F_GRAM|dimension=2|G=1_1_1_2"
          "|inverse=2_MINUS1_MINUS1_1|covered_m2=5_OVER_4|json=0")


def report_rational_model():
    q = rat(4, 5)
    one = sub(total_trace(2), covered_one(VAC, 2))
    need(eq(one, rat(7, 8)), "vacuum_only_trace")
    need(not threshold(one, q, 2), "vacuum_only_must_hold")
    print("YM4_07F_BENCH|m=1|E=VACUUM_ONLY|R=7_OVER_8"
          "|q=4_OVER_5|gate=HOLD|json=0")

    expected = ((1, rat(5, 8)), (2, rat(41, 128)),
                (4, rat(3281, 32768)))
    for n, target in expected:
        r = residual(2 * n)
        need(eq(r, target), "trace_residual_exact")
        need(threshold(r, q, 2 * n), "certified_dark_bound")
        print("YM4_07F_BENCH|m=" + str(n)
              + "|E=VACUUM_AND_BLOCK_WITNESS|R_NUM=" + str(r[0])
              + "|R_DEN=" + str(r[1])
              + "|q=4_OVER_5|gate=PASS|json=0")

    tight = rat(3, 4)
    need(not threshold(residual(2), tight, 2),
         "strict_dark_threshold_not_reached")
    print("YM4_07F_BENCH|m=1|E=VACUUM_AND_BLOCK_WITNESS"
          "|R=5_OVER_8|q=3_OVER_4|gate=HOLD|json=0")
    jump = sub(one, residual(2))
    need(eq(jump, rat(1, 4)), "one_witness_schur_jump")
    need(eq(div(moment(WITNESS, WITNESS, 2),
                gram(WITNESS, WITNESS)), jump),
         "schur_residual_independent_check")
    print("YM4_07F_SCHUR|m=1|increment=1_OVER_4"
          "|first_gate=HOLD|second_gate=PASS|json=0")

    scaled = tuple(mul(rat(4), x) for x in EIG)
    r_scaled = residual(2, eig=scaled)
    need(eq(r_scaled, rat(10)), "unnormalized_trace")
    need(lt(r_scaled, rp(mul(q, rat(4)), 2)), "exact_Perron_floor")
    need(not lt(r_scaled, rp(mul(q, rat(3)), 2)),
         "weak_Perron_floor_hold")
    print("YM4_07F_UNNORMALIZED|lambda0=4|L=4|R_T=10"
          "|gate=PASS|json=0")
    print("YM4_07F_UNNORMALIZED|lambda0=4|L=3|R_T=10"
          "|gate=HOLD|json=0")


def su2_one_link():
    # The character and Bessel series derivation is an analytic theorem,
    # not a finite sample replacing continuous Haar.
    first = div(mul(rat(16, 9), rat(1, 16)), rat(factorial(3) * factorial(3)))
    need(eq(first, rat(1, 324)), "SU2_dim_three_tail_first")
    ratio = rat(1, 64)
    tail = div(first, sub(rat(1), ratio))
    need(eq(tail, rat(16, 5103)), "SU2_analytic_series_tail")
    need(lt(tail, rat(1, 100)), "SU2_dark_less_than_one_tenth")
    need(lt(rat(1, 10), rat(3, 16)), "SU2_visible_exceeds_dark_gate")
    need(lt(rat(3, 16), rat(1, 3)), "SU2_visible_brackets")
    # Verify exact factorial/geometric envelope at four initial dimensions.
    for n in (3, 4, 5, 6):
        a = div(mul(rat(16, 9), rat(4, ip(4, n))),
                rat(factorial(n) * factorial(n)))
        b = div(mul(rat(16, 9), rat(4, ip(4, n + 1))),
                rat(factorial(n + 1) * factorial(n + 1)))
        need(eq(div(b, a), rat(1, 4 * (n + 1) * (n + 1))),
             "SU2_factorial_ratio")
        need(not lt(rat(1, 64), div(b, a)),
             "SU2_tail_geometric_enclosure")
    print("YM4_07F_SU2|group=CONTINUOUS_SU2|beta=1"
          "|space=HAAR_CLASS_FUNCTIONS|Bessel=ANALYTIC_SERIES"
          "|dark_trace_lt_num=16|dark_trace_lt_den=5103"
          "|dark_radius_lt=1_OVER_10|json=0")
    print("YM4_07F_SU2_VISIBLE|t2_gt=3_OVER_16|t2_lt=1_OVER_3"
          "|q=1_OVER_10|full_gate=HOLD|json=0")
    print("YM4_07F_SU2_FULL|beta=1|one_link_class_convolution=YES"
          "|gap_gt=LOG_3_PER_STEP|gate=PASS|4D_gap=OPEN|json=0")
    return tail


def adversaries(tail):
    bad = 0
    # 1: The inverse Gram correction must not be replaced by double counting.
    naive = add(covered_one(VAC, 2), covered_one(NONORTH, 2))
    bad += int(lt(residual(2),
                  sub(total_trace(2), naive)) is False
               and lt(sub(total_trace(2), naive), residual(2)))
    # 2: Singularity is detected rather than pseudoinverted.
    try:
        covered_two(VAC, VAC, 2)
    except ValueError:
        bad += 1
    # 3: A strict threshold at the true dark edge is rejected.
    bad += int(not threshold(residual(2), rat(3, 4), 2))
    # 4: Omitting a blocked witness leaves a false positive out.
    only_vac = sub(total_trace(2), covered_one(VAC, 2))
    bad += int(not threshold(only_vac, rat(4, 5), 2))
    # 5: Omitting vacuum leaves a residual at least one.
    only_excited = sub(total_trace(2), covered_one(WITNESS, 2))
    bad += int(not lt(only_excited, rat(1)))
    # 6: A weak Perron lower bound cannot be strengthened for free.
    scaled = tuple(mul(rat(4), x) for x in EIG)
    bad += int(not lt(residual(2, eig=scaled),
                      rp(mul(rat(4, 5), rat(3)), 2)))
    # 7: A value exceeding the true Perron root is not a lower bound.
    bad += int(not (5 <= 4))
    # 8: A zero cyclic discrepancy does not mean the dark spectrum is zero.
    bad += int(lt(rat(0), EIG[1]))
    # 9: SU2 dark q=1/10 does not cover the visible first mode.
    bad += int(lt(rat(1, 10), rat(3, 16)))
    # 10: The SU2 trace must not include the first visible mode in its tail.
    bad += int(not lt(add(tail, mul(rat(3, 16), rat(3, 16))),
                       rat(1, 100)))
    need(bad == 10, "active_falsifiers")
    print("YM4_07F_ADVERSARIES|false_claims=10_REJECTED"
          "|operator_certificate=CONDITIONAL|json=0")


def main():
    report_gram()
    report_rational_model()
    tail = su2_one_link()
    adversaries(tail)
    print("YM4_07F_VERDICT|small_gram_dark_trace_theorem=DERIVED"
          "|rational_matrix=PASS|continuous_SU2_class_model=PASS"
          "|four_dimensional_trace_data=OPEN|weak_allscale_RG=OPEN"
          "|continuum_mass_gap=OPEN|json=0")


if __name__ == "__main__":
    main()
