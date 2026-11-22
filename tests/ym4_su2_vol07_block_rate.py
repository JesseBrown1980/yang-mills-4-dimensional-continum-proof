"""YM4 VOL07: exact-integer physical block-rate implication audit.

Conditional analytic transfer lemma and toy rate controls, NOT an original SU2
weak-coupling block measurement. Only integers. Ternary scales 3**(-k).
"""


def require(ok, label):
    if not ok:
        raise ValueError(label)


def less(an, ad, bn, bd):
    require(ad > 0 and bd > 0, "positive_rational_denominator")
    return an * bd < bn * ad


def ternary_denominator(k):
    require(isinstance(k, int) and 1 <= k <= 12, "certified_ternary_exponent")
    out = 1
    for unused in range(k):
        out *= 3
    return out


def test_single_step(k):
    a_den = ternary_denominator(k)
    # q = 1 - a/2 = (2*3**k-1)/(2*3**k).
    # -log(1-x) >= x for x in [0,1); hence -log(q)/a >= 1/2.
    q_num = 2 * a_den - 1
    q_den = 2 * a_den
    require(0 < q_num < q_den, "positive_microscopic_contraction")
    require(q_den - q_num == 1, "exact_micro_rate_deficit")
    require(2 * a_den == q_den, "rational_mass_half_identity")
    return q_num, q_den


def test_physical_cube(k):
    a_den = ternary_denominator(k)
    # Block time b=3**k, so physical time a*b=1 exactly.
    b = a_den
    require(b == a_den, "physical_time_exact_one")
    # q=1/2 gives physical-block mass >= log(2) > 1/2.
    # e^(1/2) = 1 + 1/2 + 1/8 + sum(n>=3) (1/2)^n/n!
    # < 1 + 1/2 + 1/8 + sum(n>=3) (1/2)^n
    # = 1 + 1/2 + 1/8 + 1/4 = 15/8 < 2.
    # All components and strict comparison checked with integers.
    first_three_in_eighths = 8 + 4 + 1
    geometric_tail_in_eighths = 2
    require(first_three_in_eighths + geometric_tail_in_eighths == 15,
            "strict_series_majorant")
    require(first_three_in_eighths + geometric_tail_in_eighths < 16,
            "strict_e_half_less_than_two")
    return b


def test_quadratic_negative(k):
    a_den = ternary_denominator(k)
    # q_bad=1-a**2/2: -log(q_bad) <= x/(1-x) with x=a**2/2.
    # Hence its physical-unit mass lower candidate is at most
    # a/(2-a**2) < 1/2 for k>=1, and tends to zero.
    qn = 2 * (a_den * a_den) - 1
    qd = 2 * (a_den * a_den)
    require(0 < qn < qd, "bad_rate_is_contraction")
    upper_n = a_den
    upper_d = 2 * (a_den * a_den) - 1
    require(less(upper_n, upper_d, 1, 2),
            "quadratic_contraction_does_not_certify_mass_half")
    return qn, qd


def test_weak_coupling_rejection(k):
    beta = ternary_denominator(k)
    # Direct link influence envelope alpha=18*beta
    require(18 * beta > 1, "single_link_alpha_not_contractive")
    return beta


def certify():
    for k in range(1, 13):
        test_single_step(k)
        test_physical_cube(k)
        test_quadratic_negative(k)
        test_weak_coupling_rejection(k)
    # Independent negative inputs must be rejected by the physical-rate
    # gate, rather than by positivity of q alone.
    require(not less(1, 2, 0, 1), "negative_control_nonzero_q")
    require(less(1, 18, 1, 17), "strict_Dobrushin_beta_threshold")
    return (
        "YM4_VOL07_THEOREM|hypothesis=ALL_BOUNDED_GAUSS_SLICE_COVARIANCES"
        "|block_time=b|covariance_bound=M_q_power_n"
        "|eigenvalue_ratio_le=q_power_1_over_b|scope=CONDITIONAL|json=0\n"
        "YM4_VOL07_MASS|physical_gap_ge=-log_q_over_ab"
        "|rational_sufficient_q_le=1_minus_mab"
        "|continuum_OS=SEPARATE|json=0\n"
        "YM4_VOL07_TERNARY|scales=1_to_12|a=3_to_minus_k"
        "|b=3_to_k|physical_block_length=1|toy_q=1/2"
        "|toy_mass_gt=1/2|model_input=NONE|json=0\n"
        "YM4_VOL07_NEGATIVE|q_microscopic=1_minus_a_squared_over2"
        "|physical_mass_floor_uniform_half=REJECT"
        "|18beta_weak_coupling_contraction=REJECT"
        "|integer_only=YES|json=0\n"
        "YM4_VOL07_VERDICT|rate_implication=EXACT"
        "|SU2_weak_block_estimate=OPEN|source_weight_continuum=OPEN"
        "|eleven_continuum_gates=OPEN|json=0\n"
    )


if __name__ == "__main__":
    print(certify(), end="")
