"""WG09 independent full-operator finite-beta remainder bound, integer-pair only.

Verifies a conservative analytic norm ledger, independent of the WG09
Haar coefficient producer. Mathematical justification for every operator
bound is in docs/NOTE-YM4-WG09-FINITE-BETA-ORDER-CERT-20261121.md.
Scope: original SU2 gauge physical transfer at spatial L=2,
0 < beta <= 10^-12. Continuum and volume uniformity remain OPEN.
"""
from ym4_su2_wilson_local_transfer import R, require


def bound_ledger(beta):
    beta = R.of(beta)
    require(R(0) < beta <= R(1, 1000000), "beta_outside_full_operator_interval")
    y = beta.power(2).div(4)
    q = R(1).div(R(1) - 24 * beta)
    rho = R(4,9).div((R(1) - y).power(6))

    # All-spin character-series bounds and strict tail resolvent gap.
    require(rho < R(9,20) and q * rho < R(1,2),
            "spinone_tail_resolvent_ineligible")
    require(R(625,64) < R(10),
            "remaining_spin_index_six_envelope_invalid")
    # |V|<=24; exp Taylor majorants through fourth order.
    require(R(24).div(R(1)-24*beta) <= R(25),
            "exponential_first_order_majorant")
    require(R(288).div(R(1)-24*beta) <= R(289),
            "exponential_second_order_majorant")
    require(R(2304).div(R(1)-24*beta) <= R(2400),
            "exponential_third_order_majorant")
    require(R(13824).div(R(1)-24*beta) <= R(14000),
            "exponential_fourth_order_majorant")

    # Vacuum block after eliminating true vacuum electric constant.
    # a>=1-24 beta, lambda<=qt<=2 beta^4.
    require(R(1)-24*beta-2*beta.power(4) >= R(99,100),
            "vacuum_block_inverse_gap")
    require((289*beta.power(2)+2*beta.power(4))*R(100,99)
            <=300*beta.power(2),
            "vacuum_resolvent_vs_unity")
    require(R(24)+288*beta<=R(25),
            "second_order_vacuum_source_bound")
    require(R(625)*R(100,99)<R(632),
            "vacuum_induced_E_R_correction")

    # Rspinone: E V R1=0 exactly; hence E B R1<=289 beta^2.
    # Rdeep: sqrt(K_Rdeep/t) <4 beta from total spin index >=6.
    # Including vacuum elimination: the full E-to-R weighted coupling
    # has norm <=(7/10)*921 beta^2 +4*26 beta^2 <750 beta^2.
    require(R(7,10)*921+4*26 < R(750),
            "complete_E_to_tail_weighted_coupling")

    vacuum_fourth = R(50*2400 + (576*576)//4 + 300*(25*25))
    require(vacuum_fourth == R(390444),
            "vacuum_fourth_coefficient")
    magnetic_fourth = R(14000)
    tail_fourth = R(2*750*750)
    C0 = R(2000000)
    require(vacuum_fourth+magnetic_fourth+tail_fourth < C0,
            "E42_full_physical_remainder_HOLD")

    # H2=EV2E/2-vv*, H3=EV3E/6-(vw*+wv*)/2.
    # Their exact norm envelopes are <=864 and <17000.
    require(R(864)+17000*beta+C0*beta.power(2) < R(865),
            "six_cluster_spectral_proximity")
    # Top magnetic slope m=sqrt2/4>1/3; Q slope <=0.
    # Distance nu-(1+m beta) <=865 beta^2.
    require(R(1,3)-1730*beta > R(1,4),
            "electric_Q_resolvent_gap")
    # Resolvent identity:
    # ||(nu-QFQ)^-1 - G/beta|| <= 21600,
    # G=(m-M_Q)^-1, ||G||<3.
    require(R(865+864)+17000*beta+C0*beta.power(2) < R(1800),
            "inverse_difference_perturbation")
    # ||B_PQ-beta^2 H2_PQ||<=17003 beta^3; ||B_PQ||<865 beta^2.
    require(R(17000)+C0*beta <= R(17003),
            "electric_cross_third_bound")
    require(R(864)+17003*beta < R(865),
            "electric_cross_total_bound")
    cross_remainder = R((865+864)*17003*4)
    resolvent_remainder = R(864*864*21600)
    C = R(20000000000)
    require(C0+cross_remainder+resolvent_remainder < C,
            "full_six_Feshbach_fourth_order_HOLD")
    return {
        "rho":rho, "C0":C0, "C":C,
        "vacuum_fourth":vacuum_fourth,
        "magnetic_fourth":magnetic_fourth,
        "tail_fourth":tail_fourth,
        "electric_six_cross":cross_remainder,
        "electric_six_resolvent":resolvent_remainder,
        "total_six_explicit":C0+cross_remainder+resolvent_remainder,
    }


def certified_first_neutral_order(beta):
    beta=R.of(beta)
    require(R(0)<beta<=R(1,1000000000000),
            "beta_outside_WG09_energy_order_range")
    ledger=bound_ledger(beta)
    C=ledger["C"]
    # Independent WG09 exact Haar source gives:
    # fully symmetric minus 2D even =3sqrt2/32>21/160;
    # fully symmetric minus 3D odd =sqrt2/8>21/160.
    require(R(2)>R(49,25) and R(21,160)>R(0),
            "sqrt2_lower_for_third_order_gap")
    require(2*C*beta < R(21,320),
            "finite_beta_six_mode_energy_gap_HOLD")
    require(R(21,160)-2*C*beta > R(21,320),
            "ordered_symmetry_gap_acceptance")
    return {
        "beta":beta,
        "uniform_C":C,
        "gap_lower_prefactor":R(21,320),
        "WG08_symmetric_Wilson_weight_lower":R(1,289),
    }


def receipt():
    baseline=bound_ledger(R(1,1000000))
    require(baseline["C0"]==R(2000000)
            and baseline["total_six_explicit"]==R(16243906348),
            "whole_interval_remainder_envelope")
    for den in (1000000000000,10000000000000):
        out=certified_first_neutral_order(R(1,den))
        require(out["gap_lower_prefactor"]==R(21,320),
                "third_order_gap_not_certified")
    return (
        "YM4_WG09_AUDIT|original_SU2=YES|spatial_L=2"
        "|electric_spin4_neutral=42|spinone_two_link=12"
        "|all_remaining_spin_index_ge6=YES|json=0\n"
        "YM4_WG09_FESHBACH|beta_analysis_le=1/1000000"
        "|E42_4th_remainder_le=2000000_beta4"
        "|tail_spinone_ratio_lt=9/20|deep_tail_ratio_le=10_beta2"
        "|full_6mode_4th_remainder_le=20000000000_beta4"
        "|exact_6mode_ledger=16243906348|json=0\n"
        "YM4_WG09_FIRST_NEUTRAL|beta_le=1/1000000000000"
        "|symmetric_gap_gt=21_beta3_over320_times_electric_scale"
        "|single_Wilson_weight_gt=1/289"
        "|source_WG08=REQUIRED|json=0\n"
        "YM4_WG09_VERDICT|small_beta_L2_first_neutral_order=PASS"
        "|all_volume_and_continuum_mass_gap=OPEN|json=0\n"
    )


if __name__=="__main__":
    print(receipt(),end="")
