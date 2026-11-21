#!/usr/bin/env python3
"""Exact integer/rational Wilson spectral-window dual acceptance.

All physics assumptions, valid source moments and energy/state isolation are
separate inputs. This test uses a toy positive spectral measure, NOT SU2 data.
"""

from math import gcd


def need(ok, why):
    if not ok:
        raise ValueError(why)


def R(n, d=1):
    need(d != 0, "zero_denominator")
    if d < 0:
        n, d = -n, -d
    k = gcd(n, d)
    return n // k, d // k


def add(x, y):
    return R(x[0] * y[1] + y[0] * x[1], x[1] * y[1])


def neg(x):
    return R(-x[0], x[1])


def sub(x, y):
    return add(x, neg(y))


def mul(x, y):
    return R(x[0] * y[0], x[1] * y[1])


def div(x, y):
    need(y[0] != 0, "divided_by_zero")
    return R(x[0] * y[1], x[1] * y[0])


def less(x, y):
    return x[0] * y[1] < y[0] * x[1]


def same(x, y):
    return x[0] * y[1] == y[0] * x[1]


def powr(x, n):
    need(n >= 0, "negative_exponent")
    out = R(1)
    for _ in range(n):
        out = mul(out, x)
    return out


def positive_part(x):
    return R(0) if less(x, R(0)) else x


def spectral_window(q, n, C0_upper, Cn_lower,
                    claim_first_eigenstate=False,
                    unique_physical_eigenvalue_in_window=False):
    need(less(R(0), q) and less(q, R(1)),
         "invalid_physical_transfer_threshold")
    need(isinstance(n, int) and n >= 1,
         "invalid_moment_power")
    need(less(R(0), C0_upper), "nonpositive_source_total_weight")
    need(not less(Cn_lower, R(0)), "negative_moment_lower_data")
    need(not less(C0_upper, Cn_lower),
         "inconsistent_positive_contraction_moments")
    if claim_first_eigenstate:
        need(unique_physical_eigenvalue_in_window,
             "first_weight_requires_physical_eigenvalue_isolation")
    qn = powr(q, n)
    dual = div(sub(Cn_lower, mul(qn, C0_upper)), sub(R(1), qn))
    return positive_part(dual)


def check_pointwise_dual(q, n, t):
    need(not less(t, R(0)) and not less(R(1), t),
         "t_outside_positive_spectral_domain")
    p = div(sub(powr(t, n), powr(q, n)),
            sub(R(1), powr(q, n)))
    if not less(q, t):
        need(not less(R(0), p), "minorant_above_zero_below_cutoff")
    else:
        need(not less(R(1), p), "minorant_above_one_in_window")


def fixtures():
    # Independent toy: 1/4 point mass at t=1/2, 3/4 at t=1/4.
    w1, w2 = R(1, 4), R(3, 4)
    t1, t2 = R(1, 2), R(1, 4)
    C0 = add(w1, w2)
    C2 = add(mul(w1, powr(t1, 2)), mul(w2, powr(t2, 2)))
    C4 = add(mul(w1, powr(t1, 4)), mul(w2, powr(t2, 4)))
    need(same(C0, R(1)), "toy_C0")
    need(same(C2, R(7, 64)), "toy_C2")
    need(same(C4, R(19, 1024)), "toy_C4")

    q = R(1, 3)
    n2 = spectral_window(q, 2, C0, C2)
    need(same(n2, R(0)), "second_power_should_hold")
    n4 = spectral_window(q, 4, C0, C4)
    need(same(n4, R(103, 16384)), "fourth_power_exact")
    need(less(R(0), n4) and less(n4, w1),
         "window_weight_conservative")

    epsilon = R(1, 1000)
    n4_interval = spectral_window(
        q, 4, add(C0, epsilon), sub(C4, epsilon))
    need(same(n4_interval, R(53879, 10240000)),
         "fourth_power_certified_interval")
    need(less(R(0), n4_interval), "interval_window_positive")
    n4_high_cutoff = spectral_window(R(1, 2), 4, C0, C4)
    need(same(n4_high_cutoff, R(0)), "threshold_half_HOLD")

    for numerator in range(0, 37):
        check_pointwise_dual(q, 4, R(numerator, 36))
    print("YM4_SW01_FIXTURE|model=TOY_POSITIVE_SPECTRAL_MEASURE"
          "|q=1_OVER_3|n2=HOLD|n4_window_lower=103_OVER_16384"
          "|actual_fixture_window_mass=1_OVER_4|json=0")
    print("YM4_SW01_INTERVAL|q=1_OVER_3|n=4"
          "|C0upper=1_PLUS_1_OVER_1000"
          "|C4lower=19_OVER_1024_MINUS_1_OVER_1000"
          "|window_lower=53879_OVER_10240000|gate=PASS|json=0")
    print("YM4_SW01_HOLD|q=1_OVER_2|n=4"
          "|positive_window_weight=NOT_CERTIFIED|json=0")


def falsifiers():
    bad = 0

    def reject_case(q, n, C0, Cn, first=False, isolated=False):
        nonlocal bad
        try:
            spectral_window(q, n, C0, Cn,
                            claim_first_eigenstate=first,
                            unique_physical_eigenvalue_in_window=isolated)
        except ValueError:
            bad += 1
        else:
            raise ValueError("false_spectral_claim_not_rejected")

    reject_case(R(0), 4, R(1), R(19, 1024))
    reject_case(R(1), 4, R(1), R(19, 1024))
    reject_case(R(1, 3), 0, R(1), R(1))
    reject_case(R(1, 3), 4, R(-1), R(19, 1024))
    reject_case(R(1, 3), 4, R(1), R(2))
    reject_case(R(1, 3), 4, R(1), R(-1))
    reject_case(R(1, 3), 4, R(1), R(19, 1024),
                first=True, isolated=False)
    try:
        check_pointwise_dual(R(1, 3), 4, R(2))
    except ValueError:
        bad += 1
    else:
        raise ValueError("invalid_transfer_spectrum_range_accepted")
    need(bad == 8, "eight_active_falsifiers")
    print("YM4_SW01_ADVERSARIES|false_claims=8_REJECTED"
          "|first_eigenstate_without_isolation=REJECTED|json=0")


def main():
    fixtures()
    falsifiers()
    print("YM4_SW01_VERDICT|positive_measure_dual=ANALYTIC"
          "|exact_rational_test=PASS"
          "|actual_original_SU2_moment=OPEN"
          "|first_physical_Wilson_weight=OPEN"
          "|continuum_mass_gap=OPEN|json=0")


if __name__ == "__main__":
    main()
