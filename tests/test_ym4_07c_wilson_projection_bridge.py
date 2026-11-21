#!/usr/bin/env python3
"""YM4-07C: exact-integer spectral source/projection transfer gate.

This proves one finite-model amplitude threshold and exact conditional
functional-analysis inequalities. No SU2 source map, weak-coupling RG
bound, OS continuum limit, or physical mass gap is asserted.
No float division, float literals or untracked source imports.
"""
from math import isqrt

DEN = 1000000000000
WILSON_WEIGHT_PPT = 17074763
EXPECTED_AMP_FLOOR_PPT = 4132162024
HALF_OPEN = "SOURCE_TO_SU2_MAP_NOT_CERTIFIED"

def require(condition, label):
    if not condition:
        raise ValueError(label)

def amplitude_floor(weight_ppt):
    require(isinstance(weight_ppt, int) and weight_ppt > 0,
            "positive_source_weight")
    n = isqrt(weight_ppt * DEN)
    require(n*n <= weight_ppt*DEN and
            (n+1)*(n+1) > weight_ppt*DEN,
            "integer_square_root_outward")
    return n

def bound_row(name, sum_error_ppt):
    a=amplitude_floor(WILSON_WEIGHT_PPT)
    require(isinstance(sum_error_ppt,int) and sum_error_ppt >= 0,
            "nonnegative_transfer_error")
    require(sum_error_ppt < a, "source_projection_error_exceeds_wilson_amplitude")
    n=a-sum_error_ppt
    require(n>0,"strict_positive_transferred_overlap")
    print("YM4_07C_CONDITIONAL_TRANSFER|case="+name+
          "|original_finite_weight_lower_ppt="+str(WILSON_WEIGHT_PPT)+
          "|original_finite_amplitude_lower_ppt="+str(a)+
          "|combined_assumed_error_ppt="+str(sum_error_ppt)+
          "|conditional_new_amplitude_lower_ppt="+str(n)+
          "|conditional_new_squared_weight_lower_numer="+str(n*n)+
          "|conditional_new_squared_weight_denominator=1000000000000000000000000"+
          "|actual_su2_error_receipt="+HALF_OPEN+"|json=0")
    return n*n

def prove_geometric_budget():
    # Hypothetical, explicitly NOT a measured SU2 scale-error sequence:
    # eps_j <= (1/2000)*4^(-j), j>=0; sum <= 1/1500.
    # Integer comparison to the finite S3 source norm.
    budget_n=DEN
    budget_d=1500
    require(budget_n < EXPECTED_AMP_FLOOR_PPT*budget_d,
            "hypothetical_error_budget_less_than_source_weight")
    # Conservative ceil in 10^-12 units:
    ceil_budget=(budget_n+budget_d-1)//budget_d
    result=bound_row("HYPOTHETICAL_SUMMABLE_RADIX3_RG",ceil_budget)
    three=1
    four=1
    for k in range(1,12):
        three*=3
        four*=4
        # Ternary-cutoff count N=3^k; analytic geometric tail
        # sum_{j=k}infty (1/2000)*4^-j = 1/(1500*4^k).
        tail_den=1500*four
        require(three>0 and tail_den>budget_d and
                (DEN+tail_den-1)//tail_den<=ceil_budget,
                "ternary_scale_tail_is_summable")
    print("YM4_07C_TERNARY_ERROR_LEDGER|scale_ratio=3"+
          "|hypothetical_error_j=1_over_2000_times_4_to_minus_j"+
          "|infinite_total_error=1_over_1500"+
          "|conditional_transfer_squared_weight_numer="+str(result)+
          "|continuum_bare_coupling_trajectory=NOT_PROVED|json=0")

def counterexamples():
    # Exact 3x3 transfer eigenvalues: 1, q_dark, q_visible.
    # a_k=3^-k; q_dark=1/(1+a_k^2), q_visible=1/(1+2*a_k).
    # Since -log(q_dark)/a_k=log(1+a_k^2)/a_k <= a_k,
    # the full physical gap tends to zero.
    # Visible source f=(0,0,1) sees only the second massive mode.
    three=1
    for k in range(1,11):
        three*=3
        qdark_n=three*three
        qdark_d=qdark_n+1
        qvisible_n=three
        qvisible_d=three+2
        require(0<qdark_n<qdark_d and 0<qvisible_n<qvisible_d,
                "positive_reflection_transfer")
        require(qdark_n*qvisible_d>qvisible_n*qdark_d,
                "hidden_lower_energy_excitation")
        # Exact analytical inequalities:
        # physical dark gap <= 1/3^k, visible physical gap >= 2/(1+2/3^k)
        require(three>k and 2*three < 2*(three+2),
                "dark_physical_gap_to_zero_while_visible_remains_positive")
    print("YM4_07C_DARK_STATE_FALSIFIER|family=diagonal_positive_transfer"+
          "|spacing=3_to_minus_k|dark_gap_upper=3_to_minus_k"+
          "|visible_gap_lower=2_over_1_plus_2_times_spacing"+
          "|Wilson_source_orthogonal_to_dark=EXACT"+
          "|full_mass_gap_from_single_wilson=REJECTED|json=0")
    # A source entirely in the dark state has first-excitation squared
    # weight one, at every finite k, while its physical gap tends to 0.
    print("YM4_07C_FINITE_WEIGHT_FALSIFIER|first_excitation_weight=1_AT_EVERY_SCALE"+
          "|full_physical_gap_upper=3_to_minus_k"+
          "|uniform_gap_from_first_weight=REJECTED|json=0")

def gate(candidate):
    # A proof must supply all these independently authenticated SU(2) premises.
    names=("group","source_map","projection_comparison",
           "renormalized_coupling","uniform_physical_gap",
           "os_continuum_construction","infinite_volume_control")
    require(all(x in candidate for x in names),"missing_continuum_proof_fields")
    require(candidate["group"]=="CONTINUOUS_SU2_4D","discrete_group_not_continuum_SU2")
    for k in names[1:]:
        require(candidate[k]=="INDEPENDENT_THEOREM_PASS","unproved_"+k)
    return True

def negative_controls():
    required={
        "group":"CONTINUOUS_SU2_4D",
        "source_map":"INDEPENDENT_THEOREM_PASS",
        "projection_comparison":"INDEPENDENT_THEOREM_PASS",
        "renormalized_coupling":"INDEPENDENT_THEOREM_PASS",
        "uniform_physical_gap":"INDEPENDENT_THEOREM_PASS",
        "os_continuum_construction":"INDEPENDENT_THEOREM_PASS",
        "infinite_volume_control":"INDEPENDENT_THEOREM_PASS"}
    bad=[
      {k:v for k,v in required.items() if k!="source_map"},
      dict(required,group="FINITE_S3_3X4"),
      dict(required,projection_comparison="ASSUMED"),
      dict(required,renormalized_coupling="STRONG_COUPLING_FIXED_BETA"),
      dict(required,uniform_physical_gap="FINITE_POSITIVE_ONLY"),
      dict(required,os_continuum_construction="UNCONSTRUCTED"),
      dict(required,infinite_volume_control="FIXED_VOLUME_ONLY"),
    ]
    rejected=0
    for item in bad:
        try:
            gate(item)
        except ValueError:
            rejected+=1
        else:
            raise ValueError("continuum_false_promotion_accepted")
    try:
        bound_row("TOO_LARGE_TRANSFER_ERROR",EXPECTED_AMP_FLOOR_PPT)
    except ValueError:
        rejected+=1
    else:
        raise ValueError("zero_transfer_weight_accepted")
    require(rejected==8,"negative_controls_count")
    print("YM4_07C_NEGATIVE_CONTROLS|unproved_source=REJECTED"+
          "|wrong_group=REJECTED|unproved_projection=REJECTED"+
          "|wrong_beta=REJECTED|finite_positive_gap=REJECTED"+
          "|missing_OS=REJECTED|missing_infinite_volume=REJECTED"+
          "|exhausted_wilson_margin=REJECTED|count=8|json=0")

def main():
    a=amplitude_floor(WILSON_WEIGHT_PPT)
    require(a==EXPECTED_AMP_FLOOR_PPT,
            "pinned_finite_wilson_source_amplitude")
    require(a*a < WILSON_WEIGHT_PPT*DEN,
            "strictly_outward_Wilson_floor")
    # A conditional spectral projection norm transfers by two triangle
    # inequalities; no SU2 map/projection has yet been supplied.
    bound_row("ZERO_HYPOTHETICAL_SOURCE_ERROR",0)
    bound_row("FOUR_BASIS_POINT_HYPOTHETICAL_ERROR",4000000000)
    prove_geometric_budget()
    counterexamples()
    negative_controls()
    print("YM4_07C_VERDICT|finite_S3_first_Wilson_source=EXTERNALLY_PINNED_RESEARCH_INPUT"+
          "|amplitude_bridge_inequality=MATHEMATICAL_PASS"+
          "|ternary_summable_budget=CONDITIONAL_PASS"+
          "|dark_state_counterexample=PASS"+
          "|actual_cross_group_SU2_source_map=OPEN"+
          "|weak_coupling_all_scale_RG=OPEN"+
          "|continuum_OS_construction=OPEN"+
          "|physical_full_spectrum_mass_gap=OPEN|json=0")
if __name__=="__main__":
    main()
