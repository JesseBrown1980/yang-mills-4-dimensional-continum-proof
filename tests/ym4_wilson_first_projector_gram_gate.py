"""YM4-WG01: original Wilson physical even-Krylov Gram and rank-one gate.

This exact-integer module improves the full original SU(2) 4D physical-vacuum
Wilson C2/C4 upper enclosures by using the proved YM4-02d spectral cap.
It does not identify the first physical excited state. Two independently
verified compact positive spectra show that exact C0/C2/C4 and trace data
cannot determine the first-state Wilson weight.

Only integer pairs from the repository's exact rational class are used.
"""
from ym4_su2_wilson_local_transfer import R, require
from ym4_wilson_vacuum_trace_bridge import vacuum_wilson_intervals
from ym4_4d_wilson_cylinder_moments import ceil_scaled


def moment_power(values, masses, n):
    require(type(n) is int and n >= 0, "invalid_moment_order")
    require(len(values) == len(masses) and len(values) > 0,
            "invalid_spectral_measure_shape")
    require(all(R.of(t) >= R(0) and R.of(t) < R(1) for t in values),
            "invalid_excited_spectrum")
    require(all(R.of(w) >= R(0) for w in masses),
            "negative_spectral_weight")
    return sum((R.of(w) * R.of(t).power(n)
                for t, w in zip(values, masses)), R(0))


def q_for_beta(beta):
    beta = R.of(beta)
    require(beta == R(1, 10000) or beta == R(1, 100000),
            "beta_not_in_frozen_original_source")
    return 24 * beta


def sharpen_physical_source(beta):
    """Take original WV01 C0 upper; enforce positive-transfer spectral cap.

    For physical u=(W-<W>)Omega and R=Tphys/Lambda0, the spectral
    measure is supported on (0,q], with q=24beta at this fixed lattice.
    Therefore 0<C2<=q^2 C0 and 0<C4<=q^4 C0, and
    0<=C0*C4-C2^2. This is a physical full-gauge source certificate.
    """
    q = q_for_beta(beta)
    v = vacuum_wilson_intervals(beta)
    require(v["vacuum_C0_lower"] > R(0)
            and v["vacuum_C0_upper"] > v["vacuum_C0_lower"],
            "nonpositive_original_Wilson_source")
    require(v["trace"]["nonvacuum_eigenratio_upper"] == q,
            "physical_spectral_cap_mismatch")
    old2, old4 = v["vacuum_C2_upper"], v["vacuum_C4_upper"]
    new2 = q.power(2) * v["vacuum_C0_upper"]
    new4 = q.power(4) * v["vacuum_C0_upper"]
    require(new2 < old2 and new4 < old4,
            "spectral_Gram_bound_not_an_improvement")
    return {
        "beta": R.of(beta), "q": q,
        "C0_lower": v["vacuum_C0_lower"],
        "C0_upper": v["vacuum_C0_upper"],
        "C2_lower": R(0), "C2_upper": new2,
        "C4_lower": R(0), "C4_upper": new4,
        "old_C2_upper": old2, "old_C4_upper": old4,
        "strict_C2_positive": True, "strict_C4_positive": True,
        "Gram_even_determinant_nonnegative": True,
    }


def adversarial_spectral_pair(beta):
    """Exact same even Wilson moments, distinct first-excitation weights.

    Two separate positive spectral measures on the *same* four
    nonvacuum eigenvalue ratios t=(3q/4,q/2,q/3,q/4).

    A has no first-excited-state Wilson overlap.
    B has first weight 21/4000. Each has C0=1/4, and exactly
    the same C2,C4; both satisfy original WV01 interval enclosures.
    Thus the original reported moments cannot isolate w_first.
    """
    q = q_for_beta(beta)
    values = (R(3, 4) * q, R(1, 2) * q,
              R(1, 3) * q, R(1, 4) * q)
    a = (R(0), R(1, 12), R(1, 12), R(1, 12))
    b = (R(21, 4000), R(1, 12) - R(182, 4000),
         R(1, 12) + R(486, 4000), R(1, 12) - R(325, 4000))
    require(all(w >= R(0) for w in a + b), "negative_falsifier_weight")
    moments_a = tuple(moment_power(values, a, n) for n in (0, 2, 4))
    moments_b = tuple(moment_power(values, b, n) for n in (0, 2, 4))
    require(moments_a == moments_b and moments_a[0] == R(1, 4),
            "counterexample_distinct_moments")
    require(a[0] == R(0) and b[0] == R(21, 4000),
            "first_state_counterexample_failed")
    original = vacuum_wilson_intervals(beta)
    require(original["vacuum_C0_lower"] <= moments_a[0]
            and moments_a[0] <= original["vacuum_C0_upper"],
            "counterexample_outside_original_C0_interval")
    require(moments_a[2] <= original["vacuum_C4_upper"]
            and moments_a[1] <= original["vacuum_C2_upper"],
            "counterexample_outside_original_C2_C4_interval")
    sharpened = sharpen_physical_source(beta)
    require(moments_a[1] <= sharpened["C2_upper"]
            and moments_a[2] <= sharpened["C4_upper"],
            "counterexample_outside_sharpened_interval")
    physical_trace = original["trace"]
    excited_trace2 = sum((t.power(2) for t in values), R(0))
    require(excited_trace2 <
            physical_trace["excited_normalized_trace2_upper"],
            "counterexample_outside_physical_trace_envelope")
    return {"values": values, "weights_no_first": a,
            "weights_with_first": b, "even_moments": moments_a,
            "first_weight_no": a[0], "first_weight_yes": b[0],
            "trace2": excited_trace2}


def isolated_first_weight_dual(c0_upper, c2_lower,
                               first_upper, remainder_upper):
    """CONDITIONAL algebraic first-eigenspace projector witness.

    Assumptions to prove independently: one rank-one eigenprojection
    at first_upper or below; all other nonvacuum eigenratios
    <= remainder_upper < first_upper; physical source moments
    have C2 >= c2_lower and C0 <= c0_upper.

    Since C2 <= first_upper^2*w1 + remainder_upper^2*(C0-w1),
    w1 >= max(0, (C2_lower - remainder_upper^2*C0_upper) /
                  (first_upper^2 - remainder_upper^2)).
    Without a certified rank-one spectral-isolation object, this is
    only a conditional algebraic helper, not an original YM4 PASS.
    """
    a = R.of(c0_upper)
    b = R.of(c2_lower)
    top = R.of(first_upper)
    rest = R.of(remainder_upper)
    require(a > R(0) and b >= R(0), "invalid_physical_source_intervals")
    require(R(0) <= rest and rest < top and top < R(1),
            "unordered_spectral_isolation")
    numer = b - rest.power(2) * a
    denom = top.power(2) - rest.power(2)
    if numer <= R(0):
        return R(0)
    bound = numer.div(denom)
    require(bound <= a, "infeasible_isolated_first_data")
    return bound


def independently_checked_isolation_fixture(beta):
    """Exact diagonal, rank-one fixture tests the conditional polynomial.

    Top eigenratio=3q/4, second eigenratio=q/4, two source
    weights=1/8 each. Explicit rest upper=q/2 gives the
    conservative rank-one first weight lower bound 1/20.
    """
    q = q_for_beta(beta)
    values = (R(3, 4) * q, R(1, 4) * q)
    weights = (R(1, 8), R(1, 8))
    require(values[0] > values[1] and len(values) == 2,
            "fixture_rank_one_not_isolated")
    c0 = moment_power(values, weights, 0)
    c2 = moment_power(values, weights, 2)
    lower = isolated_first_weight_dual(c0, c2, values[0],
                                       R(1, 2) * q)
    require(lower == R(1, 20) and lower < weights[0],
            "fixture_first_weight_lower_mismatch")
    return {"C0": c0, "C2": c2, "lower": lower}


def original_first_projector_gate(beta):
    """Original first state: HOLD pending a certified physical projector.

    The original WV01 C2 numerical lower is zero, and the global
    YM4-02d bound q does not isolate lambda1 from all other states.
    """
    s = sharpen_physical_source(beta)
    q = s["q"]
    hypothetical = isolated_first_weight_dual(
        s["C0_upper"], s["C2_lower"], q, q.div(2))
    require(hypothetical == R(0),
            "original_projector_gate_promoted_without_evidence")
    return ("HOLD", hypothetical)


def acceptance_row(beta, predicted_q, max_C2_scaled_1e18,
                   max_C4_scaled_1e24):
    s = sharpen_physical_source(beta)
    require(s["q"] == predicted_q, "frozen_q_mismatch")
    c2_scaled = ceil_scaled(s["C2_upper"], 10 ** 18)
    c4_scaled = ceil_scaled(s["C4_upper"], 10 ** 24)
    require(c2_scaled == max_C2_scaled_1e18
            and c4_scaled == max_C4_scaled_1e24,
            "frozen_sharpened_Wilson_interval_mismatch")
    ce = adversarial_spectral_pair(beta)
    require(ce["first_weight_no"] == R(0)
            and ce["first_weight_yes"] == R(21, 4000),
            "first_weight_ambiguity_not_reproduced")
    require(independently_checked_isolation_fixture(beta)["lower"]
            == R(1, 20), "conditional_dual_fixture_failed")
    state, low = original_first_projector_gate(beta)
    require(state == "HOLD" and low == R(0),
            "uncertified_first_state_promotion_rejected")
    return ("YM4_WG01_ORIGINAL_SOURCE|beta=" + str(beta)
            + "|q=" + str(s["q"])
            + "|C0_lower_1e12=" + str(ceil_scaled(s["C0_lower"], 10 ** 12)-1)
            + "|C0_upper_1e12=" + str(ceil_scaled(s["C0_upper"], 10 ** 12))
            + "|C2_upper_1e18=" + str(c2_scaled)
            + "|C4_upper_1e24=" + str(c4_scaled)
            + "|even_Gram_PSD=PASS"
            + "|strict_C2_C4_positive=ANALYTIC"
            + "|first_eigenprojector=HOLD|json=0")


def receipt():
    return "\n".join((
        "YM4_WG01_SOURCE|continuous_SU2=YES|L=2,2,2"
        "|physical_Gauss=PROJECTED|original_Wilson_source=YES"
        "|vacuum_moments=WV01|spectral_cap=YM4_02D|json=0",
        "YM4_WG01_THEOREM|C2_le_q2_C0|C4_le_q2_C2"
        "|C4_le_q4_C0|Gram_det_C0C4_minus_C2sq_ge0"
        "|R_injective=YES|C2_C4_strictly_positive=YES|json=0",
        acceptance_row(R(1, 10000), R(3, 1250),
                       1440139406101, 8295202979139),
        acceptance_row(R(1, 100000), R(3, 12500),
                       14400001334, 829440077),
        "YM4_WG01_COUNTEREXAMPLE|same_C0_C2_C4=PASS"
        "|first_weight_fixture_A=0|first_weight_fixture_B=21/4000"
        "|trace2_envelope=PASS|same_top_spectral_eigenratio=PASS|json=0",
        "YM4_WG01_CONDITIONAL|verified_fixture_isolated_rank1"
        "_first_weight_lower=1/20|original_first_eigenprojector=HOLD"
        "|nonzero_original_first_weight=UNPROVEN|json=0",
        "YM4_WG01_VERDICT|original_physical_C2_C4_upper=SHARPENED"
        "|original_Wilson_visible_excitation_exists=YES"
        "|first_excited_Wilson_weight=HOLD"
        "|continuum_uniform_mass_gap=OPEN|json=0",
    )) + "\n"


if __name__ == "__main__":
    print(receipt(), end="")
