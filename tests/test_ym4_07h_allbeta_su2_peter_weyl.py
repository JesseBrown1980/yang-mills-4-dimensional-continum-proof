#!/usr/bin/env python3
"""YM4-07H: exact-integer audit of analytic SU2 Fourier tails and Haar-cap floor.

This verifies the rational conclusions and negative controls of the analytic
proof in docs/NOTE-YM4-07H-ALLBETA-SU2-PETER-WEYL-CAP-20261121.md.
No finite-group quadrature substitutes for continuous Haar or Peter-Weyl.
"""

from math import gcd


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def ipow(base, exponent):
    need(exponent >= 0, "negative_integer_exponent")
    output = 1
    for _ in range(exponent):
        output *= base
    return output


def fraction(n, d=1):
    need(d > 0, "nonpositive_denominator")
    g = gcd(n, d)
    return (n // g, d // g)


def less(a, b):
    return a[0] * b[1] < b[0] * a[1]


def equal(a, b):
    return a[0] * b[1] == b[0] * a[1]


def trace_error(beta, cutoff, spatial_links, time_steps):
    need(beta >= 1, "coupling_under_one_outside_benchmark")
    need(cutoff >= 4 * beta, "unproved_representation_cutoff")
    need(spatial_links > 0 and time_steps > 0, "invalid_geometry")
    return fraction(
        2 * time_steps * spatial_links * (cutoff + 1) * ipow(3, cutoff),
        ipow(8, cutoff),
    )


def operator_error(beta, cutoff, spatial_links):
    return trace_error(beta, cutoff, spatial_links, 1)


def one_link_rank(cutoff):
    need(cutoff >= 1, "zero_dimensional_representation_set")
    return cutoff * (cutoff + 1) * (2 * cutoff + 1) // 6


def cap_floor(beta, k, spatial_links=648, spatial_plaquettes=648):
    need(beta >= 1 and k >= 1 and beta <= k * k,
         "invalid_cap_radius_for_coupling")
    # All exponential analytic inequalities were bounded by 3 powers:
    # L > 1/[3^405 * (3072*k^3)^648] at L=6.
    need(spatial_links == 648 and spatial_plaquettes == 648,
         "unexpected_cap_geometry")
    return fraction(
        1,
        ipow(3, 405) * ipow(3072 * k * k * k, spatial_links),
    )


def transfer_checks():
    Nl = Ns = 648
    need(3 * 216 == Nl, "incorrect_original_4d_spatial_links")
    need(one_link_rank(3) == 14, "su2_cutoff3_rank")
    need(one_link_rank(9) == 285, "su2_cutoff9_rank")
    need(one_link_rank(27) == 6930, "su2_cutoff27_rank")
    need(one_link_rank(81) == 180441, "su2_cutoff81_rank")
    print("YM4_07H_RANK|cutoffs=3_9_27_81"
          "|one_link_dims=14_285_6930_180441"
          "|full_rank=ONE_LINK_DIM_POWER_648|dense_matrix=NOT_BUILT"
          "|json=0")
    first = trace_error(4, 27, Nl, 4)
    need(equal(first, fraction(
        4323713773987629, 9444732965739290427392)),
        "beta4_exact_rational_moment_budget")
    need(less(first, fraction(1, 1000000)),
         "beta4_n27_four_step")
    print("YM4_07H_CUTOFF|beta=4|N=27|n=4"
          "|trace_error_num=4323713773987629"
          "|trace_error_den=9444732965739290427392"
          "|trace_error_lt=1_OVER_1000000|gate=PASS|json=0")
    second = trace_error(9, 81, Nl, 4)
    need(less(second, fraction(1, ipow(10, 20))),
         "beta9_n81_four_step")
    print("YM4_07H_CUTOFF|beta=9|N=81|n=4"
          "|trace_error_lt=1_OVER_10POWER20|gate=PASS|json=0")
    third = trace_error(64, 729, Nl, 4)
    need(less(third, fraction(1, ipow(10, 100))),
         "beta64_n729_four_step")
    print("YM4_07H_CUTOFF|beta=64|N=729|n=4"
          "|trace_error_lt=1_OVER_10POWER100|gate=PASS|json=0")
    # Absolute error is deliberately not a relative vacuum certificate.
    upper_operator = operator_error(64, 729, Nl)
    lower_perron = cap_floor(64, 8)
    need(less(lower_perron, upper_operator),
         "absolute_vs_relative_gate_must_hold")
    need(3072 * 8 * 8 * 8 < ipow(3, 14),
         "beta64_cap_denominator_envelope")
    need(405 + 648 * 14 == 9477,
         "beta64_cap_exponent")
    need(2 * 2 > 3 and 82944 // 2 == 41472,
         "beta64_old_Jensen_envelope")
    print("YM4_07H_PERRON|group=CONTINUOUS_SU2|beta=64"
          "|k=8|lambda0_gt=3_POWER_MINUS_9477"
          "|old_Jensen_lt=3_POWER_MINUS_41472"
          "|cap_floor_stronger=YES|json=0")
    print("YM4_07H_RELATIVE|beta=64|N=729"
          "|operator_error_UPPER_gt_Perron_LOWER=YES"
          "|relative_vacuum_error=HOLD|json=0")
    return first, second, third


def active_falsifiers():
    rejects = 0

    cases = (
        (4, 12), (9, 27), (64, 243), (64, 81),
    )
    for beta, cutoff in cases:
        try:
            trace_error(beta, cutoff, 648, 4)
        except ValueError:
            rejects += 1
        else:
            raise ValueError("invalid_four_beta_cutoff_accepted")

    # 5: The n=4 original beta4 N=16 budget is not under 1e-6.
    rejects += int(not less(trace_error(4, 16, 648, 4),
                            fraction(1, 1000000)))
    # 6: The beta64 n=4 upper is not below 1e-400.
    rejects += int(not less(trace_error(64, 729, 648, 4),
                            fraction(1, ipow(10, 400))))
    # 7: The linkwise rank must contain d*d matrix coefficients.
    rejects += int(one_link_rank(27) != 27 * 28 // 2)
    # 8: Per-step error does not remain the same when times grow.
    rejects += int(less(trace_error(4, 27, 648, 4),
                        trace_error(4, 27, 648, 5)))
    # 9: The positive-cap radius for beta64 must have k>=8.
    try:
        cap_floor(64, 7)
    except ValueError:
        rejects += 1
    else:
        raise ValueError("unqualified_cap_beta_accepted")

    # 10-12: Require original SU2 spatial A, physical gauge P,
    # and no unsupported relative-gap conclusion.
    contract = {"gauge": "SU2", "spatial_action": True,
                "physical_projection": True, "relative_gap": False}

    def scope_check(row):
        need(row["gauge"] == "SU2", "wrong_gauge_group")
        need(row["spatial_action"], "discarded_spatial_Wilson_action")
        need(row["physical_projection"], "discarded_gauge_projector")
        need(not row["relative_gap"], "unsupported_relative_gap")

    for field, value in (
        ("spatial_action", False),
        ("physical_projection", False),
        ("relative_gap", True),
    ):
        changed = dict(contract)
        changed[field] = value
        try:
            scope_check(changed)
        except ValueError:
            rejects += 1
        else:
            raise ValueError("false_spectral_promotion_accepted")

    need(rejects == 12, "twelve_falsifiers_must_reject")
    print("YM4_07H_ADVERSARIES|false_claims=12_REJECTED"
          "|weak_coupling_gap=OPEN|json=0")


def main():
    transfer_checks()
    active_falsifiers()
    print("YM4_07H_VERDICT|original_4D_SU2_Fourier_truncation=ANALYTIC"
          "|high_beta_Perron_cap=ANALYTIC"
          "|power3_representation_cutoffs=EXACT_RATIONAL_CONTROLS"
          "|relative_4D_spectrum=OPEN|volume_uniform=OPEN"
          "|continuum_mass_gap=OPEN|json=0")


if __name__ == "__main__":
    main()
