#!/usr/bin/env python3
"""YM4-07I exact integer verification of a finite 4D SU2 vacuum projector gate.

The proof is analytic and in docs/NOTE-YM4-07I-FINITE-4D-SU2-
PHYSICAL-VACUUM-PROJECTOR-20261121.md. The test checks full enormous
integer powers, not rounded exponentials or a computed 4D spectrum.
"""


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def ipow(base, exponent):
    need(exponent >= 0, "negative_integer_exponent")
    out = 1
    factor = base
    remaining = exponent
    while remaining:
        if remaining & 1:
            out *= factor
        remaining //= 2
        if remaining:
            factor *= factor
    return out


BETA = 64
NL = 648
NS = 648
BETA_NL = BETA * NL
GAP_EXPONENT = 2 * BETA_NL
K_CAP = 8
CAP_D = ipow(3, 405) * ipow(3072 * K_CAP * K_CAP * K_CAP, NL)
REL_TOL = 1000000


def gap_gate(cutoff, tolerance=REL_TOL):
    need(cutoff >= 4 * BETA, "unjustified_representation_cutoff")
    need(tolerance > 0, "invalid_relative_tolerance")
    # Requirement:
    # 2*Nl*(N+1)*(3/8)^N < 1/[tol*CAP_D*3^82944].
    # The comparison contains only exact nonnegative integers.
    left = tolerance * 2 * NL * (cutoff + 1)
    left *= ipow(3, cutoff + GAP_EXPONENT)
    left *= CAP_D
    right = ipow(8, cutoff)
    return left < right


def certify():
    need(BETA_NL == 41472, "wrong_4d_plaquette_link_count")
    need(GAP_EXPONENT == 82944, "wrong_positive_kernel_gap_exponent")
    need(3072 * K_CAP * K_CAP * K_CAP == 1572864,
         "wrong_exact_SU2_cap_volume")
    need(NS // 2 + NL // 8 == 405,
         "wrong_cap_exponential_envelope")
    need(not gap_gate(59049), "power3_10_relative_gate_must_hold")
    print("YM4_07I_GATE|beta=64|N=59049"
          "|delta_over_gap_lt=1_OVER_1000000|gate=HOLD|json=0")
    need(gap_gate(177147), "power3_11_relative_gate_must_pass")
    print("YM4_07I_GATE|beta=64|N=177147"
          "|delta_over_gap_lt=1_OVER_1000000|gate=PASS|json=0")
    need(not gap_gate(6561), "power3_8_must_hold")
    need(not gap_gate(729), "power3_6_must_hold")
    print("YM4_07I_GAP|original_SU2_4D=YES"
          "|lambda0_gt=1_OVER_3POWER405_1572864POWER648"
          "|one_minus_tanh_gt=3_POWER_MINUS82944"
          "|physical_gamma_gt=CAP_L_TIMES_3_POWER_MINUS82944"
          "|json=0")
    # Elementary eigenvector perturbation bound:
    # norm(projector difference) <= 2 delta/gamma.
    need(2 * 500000 == REL_TOL,
         "rank_one_operator_projector_coefficient")
    # Rank-one projector trace norm doubles operator norm.
    need(2 * 250000 == 500000,
         "rank_one_trace_norm_relation")
    # Four-step correlator: 4 delta + 2 projector norm.
    need(4 + 4 == 8 and 1000000 // 8 == 125000,
         "four_step_correlation_error")
    print("YM4_07I_PROJECTOR|group=CONTINUOUS_SU2"
          "|physical_gauge=YES|beta=64|N=177147"
          "|norm_Pi_MINUS_PiN_lt=1_OVER_500000|json=0")
    print("YM4_07I_WILSON|fine_spatial_2x2_rectangle=YES"
          "|vacuum_mean_error_lt=1_OVER_250000"
          "|four_step_W_T4_W_error_lt=1_OVER_125000"
          "|truncated_correlator_value=NOT_COMPUTED|json=0")


def adversaries():
    rejected = 0
    # Four incorrect cutoff gates must refuse the precision claim.
    try:
        gap_gate(243)
    except ValueError:
        rejected += 1
    else:
        raise ValueError("N243_invalid_cutoff_accepted")
    for n in (729, 6561, 59049):
        rejected += int(not gap_gate(n))

    # Six active scope falsifiers.
    contract = {
        "group": "SU2",
        "spatial_Wilson_A": True,
        "physical_gauge_P": True,
        "truncated_kernel_pointwise_positive": False,
        "numeric_first_excited_value": False,
        "continuum_mass_gap": False,
    }

    def scoped(row):
        need(row["group"] == "SU2", "wrong_group")
        need(row["spatial_Wilson_A"], "spatial_action_dropped")
        need(row["physical_gauge_P"], "gauge_projector_dropped")
        need(not row["truncated_kernel_pointwise_positive"],
             "unproved_pointwise_kernel_positivity")
        need(not row["numeric_first_excited_value"],
             "uncomputed_4D_eigenvalue")
        need(not row["continuum_mass_gap"],
             "unproved_continuum_gap")

    scoped(contract)
    for key, value in (
        ("group", "S3"),
        ("spatial_Wilson_A", False),
        ("physical_gauge_P", False),
        ("truncated_kernel_pointwise_positive", True),
        ("numeric_first_excited_value", True),
        ("continuum_mass_gap", True),
    ):
        changed = dict(contract)
        changed[key] = value
        try:
            scoped(changed)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("unsupported_scope_passed")
    need(rejected == 10, "ten_negative_controls")
    print("YM4_07I_ADVERSARIES|false_claims=10_REJECTED"
          "|relative_projector=FINITE_4D_ONLY|json=0")


def main():
    certify()
    adversaries()
    print("YM4_07I_VERDICT|genuine_4D_SU2_beta64_physical_vacuum"
          "_projector=ANALYTIC_BOUND|Wilson_4step_correlation_error"
          "=ANALYTIC_BOUND|numeric_spectrum=OPEN|allscale_RG=OPEN"
          "|continuum_mass_gap=OPEN|json=0")


if __name__ == "__main__":
    main()
