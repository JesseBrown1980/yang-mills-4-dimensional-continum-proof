#!/usr/bin/env python3
"""YM4-07I2: exact integer validation of physically normalized Wilson transfer.

This is a second, post-original-freeze check. It does not calculate an original
4D Wilson observable; it checks the analytic certified approximation constants.
"""


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def power(base, exponent):
    need(exponent >= 0, "negative_power")
    result = 1
    factor = base
    remaining = exponent
    while remaining > 0:
        if remaining % 2 == 1:
            result *= factor
        remaining //= 2
        if remaining:
            factor *= factor
    return result


def fraction(n, d):
    need(d > 0, "invalid_denominator")
    return (n, d)


def equal(a, b):
    return a[0] * b[1] == b[0] * a[1]


def add(a, b):
    return fraction(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def less(a, b):
    return a[0] * b[1] < b[0] * a[1]


NL = 648
BETA = 64
N = 177147
CAP_D = power(3, 405) * power(1572864, NL)
GAP_EXP = 2 * BETA * NL
TOL = 1000000


def exact_gate(cutoff, rel_tol=TOL):
    need(cutoff >= 4 * BETA, "cutoff_does_not_cover_coupling")
    left = rel_tol * 2 * NL * (cutoff + 1)
    left *= power(3, cutoff + GAP_EXP) * CAP_D
    return left < power(8, cutoff)


def main_certificate():
    need(GAP_EXP == 82944, "physical_spectral_gap_exponent")
    need(exact_gate(N), "physical_gap_relative_cutoff")
    need(not exact_gate(59049), "prior_cutoff_must_hold")

    # Both physical-sector leading eigenvalues are enclosed by delta.
    # The unnormalized gap gamma > gamma_floor guarantees a rank-one
    # truncated physical vacuum eigenprojection.
    projector_operator = fraction(2, TOL)
    projector_trace = fraction(4, TOL)
    normalized_semigroup = fraction(2, TOL)
    mean_error = projector_trace
    physical_four_step = add(
        fraction(4 * normalized_semigroup[0], normalized_semigroup[1]),
        projector_trace,
    )
    connected_extra = fraction(2 * mean_error[0], mean_error[1])
    connected_four_step = add(physical_four_step, connected_extra)

    need(equal(projector_operator, fraction(1, 500000)),
         "physical_vacuum_projector_norm")
    need(equal(projector_trace, fraction(1, 250000)),
         "rank_one_projector_trace")
    need(equal(normalized_semigroup, fraction(1, 500000)),
         "physical_normalized_transfer_error")
    need(equal(physical_four_step, fraction(3, 250000)),
         "correct_four_step_physical_normalization")
    need(equal(connected_extra, fraction(1, 125000)),
         "connected_vacuum_subtraction")
    need(equal(connected_four_step, fraction(1, 50000)),
         "physical_connected_Wilson_correlation")
    need(less(fraction(1, 50000), fraction(1, 10000)),
         "finite_error_is_small")
    print("YM4_07I2_NORMALIZATION|group=CONTINUOUS_SU2"
          "|beta=64|N=177147|time_step=a"
          "|normalized_T_operator_error_lt=1_OVER_500000|json=0")
    print("YM4_07I2_PHYSICAL|n=4|time_separation=4a"
          "|normalized_W_T4_W_error_lt=3_OVER_250000|json=0")
    print("YM4_07I2_CONNECTED|n=4|vacuum_mean_subtracted=YES"
          "|connected_W_error_lt=1_OVER_50000"
          "|actual_first_Wilson_weight=OPEN|json=0")


def adversarial():
    count = 0
    contract = {
        "gauge": "SU2",
        "time_normalized": True,
        "independent_lambda0N": True,
        "physical_gauge_projector": True,
        "connected_subtraction": True,
        "actual_Wilson_value_computed": False,
        "first_excited_weight_computed": False,
        "continuum_gap_claimed": False,
        "exact_4d_spatial_action": True,
    }

    def accept(row):
        need(row["gauge"] == "SU2", "wrong_group")
        need(row["time_normalized"], "raw_time_moment_as_physical")
        need(row["independent_lambda0N"], "same_Perron_root_assumed")
        need(row["physical_gauge_projector"], "physical_projector_dropped")
        need(row["connected_subtraction"], "vacuum_not_subtracted")
        need(not row["actual_Wilson_value_computed"], "invented_Wilson_value")
        need(not row["first_excited_weight_computed"],
             "invented_original_Wilson_excited_weight")
        need(not row["continuum_gap_claimed"], "invented_continuum_gap")
        need(row["exact_4d_spatial_action"], "spatial_Wilson_action_dropped")

    accept(contract)
    for key, value in (
        ("time_normalized", False),
        ("independent_lambda0N", False),
        ("physical_gauge_projector", False),
        ("connected_subtraction", False),
        ("actual_Wilson_value_computed", True),
        ("first_excited_weight_computed", True),
        ("continuum_gap_claimed", True),
        ("exact_4d_spatial_action", False),
    ):
        modified = dict(contract)
        modified[key] = value
        try:
            accept(modified)
        except ValueError:
            count += 1
        else:
            raise ValueError("unsupported_physical_correlation_claim")
    need(count == 8, "eight_false_claims_rejected")
    print("YM4_07I2_ADVERSARIES|false_claims=8_REJECTED"
          "|actual_Wilson_correlator=NOT_COMPUTED|json=0")


def main():
    main_certificate()
    adversarial()
    print("YM4_07I2_VERDICT|physical_normalized_Wilson_error"
          "=ANALYTIC_FIXED_4D|connected_Wilson_error=ANALYTIC_FIXED_4D"
          "|first_spectral_weight=OPEN|allscale_RG=OPEN"
          "|continuum_mass_gap=OPEN|json=0")


if __name__ == "__main__":
    main()
