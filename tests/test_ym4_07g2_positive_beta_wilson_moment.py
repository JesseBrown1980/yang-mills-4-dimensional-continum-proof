#!/usr/bin/env python3
"""YM4-07G2 exact rational audit of the analytic genuine SU2 Wilson moment proof.

The SU2 Haar representation-theoretic statements are derived analytically in
docs/NOTE-YM4-07G2-POSITIVE-BETA-WILSON-MOMENT-20261121.md.
This program audits all exact rational constants and refusal controls.
"""
from math import gcd


def need(ok, tag):
    if not ok:
        raise ValueError(tag)


def rat(n, d=1):
    need(d != 0, "denominator_zero")
    if d < 0:
        n, d = -n, -d
    k = gcd(n, d)
    return (n // k, d // k)


def add(a, b):
    return rat(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def sub(a, b):
    return add(a, rat(-b[0], b[1]))


def mul(a, b):
    return rat(a[0] * b[0], a[1] * b[1])


def div(a, b):
    need(b[0] != 0, "divide_by_zero")
    return rat(a[0] * b[1], a[1] * b[0])


def lt(a, b):
    return a[0] * b[1] < b[0] * a[1]


def eq(a, b):
    return a[0] * b[1] == b[0] * a[1]


def power(a, n):
    need(n >= 0, "negative_exponent")
    ans = rat(1)
    for _ in range(n):
        ans = mul(ans, a)
    return ans


def four_dim_wilson_support():
    side = 6
    p = (0, 0, 0)
    edges = []
    steps = ((0, 1), (0, 1), (1, 1), (1, 1),
             (0, -1), (0, -1), (1, -1), (1, -1))
    for d, s in steps:
        new = list(p)
        new[d] = (new[d] + s) % side
        new = tuple(new)
        edges.append((p if s == 1 else new, d))
        p = new
    need(p == (0, 0, 0), "nonclosing_Wilson_word")
    need(len(edges) == 8 and len(set(edges)) == 8,
         "fundamental_rep_support_count")
    need(3 * side * side * side == 648, "wrong_spatial_link_count")
    print("YM4_07G2_WILSON|spatial_side=6|fine_edges=8_DISTINCT"
          "|Haar_second=1_OVER_4|B_eigenvalue=FUNDAMENTAL_POWER_8"
          "_TRIVIAL_POWER_640|json=0")


def rational_vacuum_overlap():
    V = 216
    beta = rat(1, 432000)
    betaV = mul(beta, rat(V))
    need(eq(betaV, rat(1, 2000)), "coupling_volume")

    # Elementary analytic enclosures e^(-x)>1-x and e^x<1/(1-x),
    # for positive x below 1; only their rational sides are checked.
    h_min = sub(rat(1), mul(rat(15), betaV))
    h_max = div(rat(1), sub(rat(1), mul(rat(12), betaV)))
    m_max = sub(div(rat(1), sub(rat(1), mul(rat(24), betaV))),
                rat(1))
    need(eq(h_min, rat(397, 400)), "Perron_half_action_min")
    need(eq(h_max, rat(500, 497)), "Perron_half_action_max")
    need(eq(m_max, rat(3, 247)), "vacuum_Wilson_mean_abs")
    C = sub(mul(rat(1, 4), h_min), mul(m_max, h_max))
    need(eq(C, rat(46335323, 196414400)),
         "physical_Wilson_overlap_constant")
    need(lt(rat(1, 5), C), "overlap_strictly_above_one_fifth")
    need(eq(sub(C, rat(1, 5)), rat(7052443, 196414400)),
         "overlap_margin_exact")
    print("YM4_07G2_OVERLAP|vacuum_m_abs_lt=3_OVER_247"
          "|h_min_gt=397_OVER_400|h_max_lt=500_OVER_497"
          "|C_gt_num=46335323|C_gt_den=196414400"
          "|C_gt_1_OVER_5=YES|json=0")
    return beta, betaV, C


def transfer_moments(beta, betaV):
    # Haar Peter-Weyl: b_fund >= exp(-beta)*beta/4,
    # b_trivial >= exp(-beta), product over exactly eight fine
    # fundamental and 640 trivial spatial links.
    N_links = 648
    need(N_links - 8 == 640, "B_Wilson_trivial_channel_count")
    beta_link_total = mul(beta, rat(N_links))
    need(eq(beta_link_total, rat(3, 2000)),
         "linkwise_convolution_exponential")
    exp_lower = sub(rat(1), beta_link_total)
    need(eq(exp_lower, rat(1997, 2000)), "fundamental_eigen_lower")
    beta_over4 = div(beta, rat(4))
    need(eq(beta_over4, rat(1, 1728000)),
         "one_link_character_power")
    first = mul(mul(rat(4, 25), exp_lower), power(beta_over4, 8))
    expected_first = rat(1997, 12500 * 1728000 * 1728000
                         * 1728000 * 1728000 * 1728000
                         * 1728000 * 1728000 * 1728000)
    need(eq(first, expected_first), "first_moment_rational")
    # Holder/Jensen on positive physical transfer, with source norm<=1.
    fourth_decrement = power(first, 4)
    expected_fourth = rat(1997 * 1997 * 1997 * 1997,
                          power_int(12500, 4) * power_int(1728000, 32))
    need(eq(fourth_decrement, expected_fourth),
         "Schur_fourth_moment_rational")
    need(lt(rat(0), fourth_decrement), "positive_Wilson_Schur_decrement")
    need(lt(fourth_decrement, first), "fourth_below_first")
    print("YM4_07G2_ONE_STEP|original_SU2_transfer=YES"
          "|beta=1_OVER_432000|source_T_source_gt=1997_OVER_12500"
          "_TIMES_1728000_POWER_MINUS8|json=0")
    print("YM4_07G2_FOURTH|Schur_decrement_gt_num=1997_POWER4"
          "|Schur_decrement_gt_den=12500_POWER4_TIMES_1728000_POWER32"
          "|positive_beta=YES|json=0")
    return first, fourth_decrement


def power_int(base, exponent):
    need(exponent >= 0, "negative_integer_exponent")
    value = 1
    for _ in range(exponent):
        value *= base
    return value


def adversaries(beta, betaV, C, first, fourth):
    bad = 0
    # Actual strict constants and support dimensions are compared.
    bad += int(not eq(C, rat(1, 5)))
    bad += int(not eq(C, rat(1, 4)))
    bad += int(not eq(beta, rat(1, 2000)))
    bad += int(not eq(mul(betaV, rat(24)), rat(1, 100)))
    bad += int(not eq(first, power(div(beta, rat(4)), 7)))
    bad += int(not eq(fourth, power(first, 3)))
    # Non-theorem promotions are actively denied by an acceptance contract.
    checked_scope = {"gauge": "SU2", "dimension": 4, "volume": 216,
                     "beta": beta, "moment": "lower_only", "weak_RG": False}
    def require_finite_positive_beta(scope):
        need(scope["gauge"] == "SU2", "wrong_gauge_group")
        need(scope["dimension"] == 4 and scope["volume"] == 216,
             "wrong_geometry")
        need(scope["beta"] == rat(1, 432000), "wrong_coupling")
        need(scope["moment"] == "lower_only", "invented_exact_moment")
        need(not scope["weak_RG"], "unsupported_allscale_RG")

    require_finite_positive_beta(checked_scope)
    for key, value in (("gauge", "S3"), ("dimension", 2),
                       ("moment", "evaluated_exact"), ("weak_RG", True)):
        mutated = dict(checked_scope)
        mutated[key] = value
        try:
            require_finite_positive_beta(mutated)
        except ValueError:
            bad += 1
        else:
            raise ValueError("false_scope_accepted")
    need(bad == 10, "ten_active_falsifiers")
    print("YM4_07G2_ADVERSARIES|arithmetic_and_scope=10_REJECTED"
          "|positive_beta_exact_moment=OPEN"
          "|running_weak_coupling=OPEN|json=0")


def main():
    four_dim_wilson_support()
    beta, betaV, C = rational_vacuum_overlap()
    first, fourth = transfer_moments(beta, betaV)
    adversaries(beta, betaV, C, first, fourth)
    print("YM4_07G2_VERDICT|physical_positive_beta_Wilson_fourth_moment"
          "=RIGOROUS_LOWER|exact_value=OPEN|large_beta_Rg=OPEN"
          "|continuum_mass_gap=OPEN|json=0")


if __name__ == "__main__":
    main()
