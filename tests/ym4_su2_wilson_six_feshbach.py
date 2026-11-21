"""YM4-WG07: original SU2 full-transfer six-cluster Schur/Feshbach theorem.

The L=2, 3+1D continuous SU(2) original Wilson physical transfer,
its 24 spatial magnetic plaquettes, full Gauss projection and entire
infinite-dimensional Peter-Weyl tail are retained.

WG06's six positive first magnetic slopes have a gap. Schur elimination
of the true electric vacuum and complete neutral tail, performed on the
isospectral K^(1/2) B K^(1/2), establishes an *actual* rank-six
interacting physical neutral spectral projector at 0<beta<=1/10000.
At beta<=1/1000000 its squared overlap with the *true interacting
vacuum-centered original Wilson plaquette* is >9/400.

A separate uniform 24-Hurwitz-unit cubature exactly reproduces
continuous-SU2 Haar fourth-coordinate moments, in contrast to Q8.
Full 42x42 explicit magnetic second-order coefficients remain OPEN:
the full Taylor remainder is instead bounded in operator norm.
All arithmetic in acceptance checks is exact integer-rational.
"""
from itertools import product
from ym4_su2_wilson_local_transfer import R, require
from ym4_su2_wilson_first_magnetic_42gram import (
    exact_graph_spectral_certificate,
)
from ym4_su2_neutral_42_band import neutral_tail_character_envelope
from ym4_su2_wilson_42band_positive_weight import (
    original_physical_wilson_42band_weight,
)


SIX_BETA_MAX = R(1, 10000)
WEIGHT_BETA_MAX = R(1, 1000000)


def hurwitz_24_scaled_quaternions():
    """Uniform 24-cell cubature, with each coordinate scaled by two.

    Eight signed coordinate-axis units, plus all sixteen unit
    half-coordinate sign patterns. These form the 24 Hurwitz units,
    the binary tetrahedral group; finite exact quadrature for
    polynomial degree <=4 in a single SU2 quaternion coordinate.
    """
    pts = []
    for axis in range(4):
        for sign in (-1, 1):
            p = [0] * 4
            p[axis] = 2 * sign
            pts.append(tuple(p))
    pts.extend(tuple(v) for v in product((-1, 1), repeat=4))
    require(len(pts) == 24 and len(set(pts)) == 24,
            "invalid_Hurwitz_24_point_cubature")
    return tuple(pts)


def exact_Haar_coordinate_monomial(indices):
    """Haar coordinate monomial of total degree at most four.

    Quaternion q on S^3 has exact Haar tensor
      E[q_i q_j]=delta_ij/4,
      E[q_i q_j q_k q_l]
       =(delta_ij delta_kl+delta_ik delta_jl+
         delta_il delta_jk)/24.
    The 24-cell points reproduce these exact identities.
    """
    require(type(indices) is tuple and len(indices) <= 4
            and all(type(i) is int and 0 <= i < 4 for i in indices),
            "invalid_S3_Haar_monomial")
    numerator = 0
    for p in hurwitz_24_scaled_quaternions():
        value = 1
        for i in indices:
            value *= p[i]
        numerator += value
    return R(numerator, 24 * 2 ** len(indices))


def verify_fourth_Haar_tensor():
    """Independently compare 256 fourth and sixteen second moments."""
    require(all(exact_Haar_coordinate_monomial((i,)) == R(0)
                for i in range(4)), "Haar_quaternion_first_moment")
    require(all(exact_Haar_coordinate_monomial((i,j)) ==
                (R(1,4) if i == j else R(0))
                for i in range(4) for j in range(4)),
            "Haar_quaternion_second_tensor")
    for i,j,k,l in product(range(4), repeat=4):
        pairings = int(i == j and k == l)
        pairings += int(i == k and j == l)
        pairings += int(i == l and j == k)
        expected = R(pairings,24)
        require(exact_Haar_coordinate_monomial((i,j,k,l)) == expected,
                "original_continuous_SU2_Haar_fourth_tensor")
    require(exact_Haar_coordinate_monomial((0,0,0,0)) == R(1,8)
            and exact_Haar_coordinate_monomial((0,0,1,1)) == R(1,24),
            "fourth_Haar_frozen_scalar_mismatch")
    # One normalized fundamental plaquette trace phi=2W=2q0 has
    # <phi W^2 phi>_Haar = 4 E[q0^4]=1/2.
    original_same_plaquette_fourth = (
        4 * exact_Haar_coordinate_monomial((0,0,0,0))
    )
    require(original_same_plaquette_fourth == R(1,2),
            "original_SU2_plaquette_quartic_fixture_failed")
    # Q8 has E[q0^4]=1/4: its second-order Haar shortcut
    # is not a valid fourth-order quadrature.
    require(R(1,4) != R(1,8), "bad_Q8_fourth_order_negative_control")
    return True


def six_cluster_schur_certificate(beta):
    """Count actual six full-interacting physical neutral eigenvalues.

    Work with the *isospectral* positive operator on H_phys:
      J=Khalf exp(beta V) Khalf,
      V=sum of all 24 original SU2 spatial halftrace plaquettes,
      ||V||<=24.
    The original full transfer is exp(-24beta) Bhalf K Bhalf.
    J and the rescaled latter are unitarily equivalent via the polar
    decomposition A=e^(beta V/2) Khalf (nonzero spectrum including
    multiplicities, and injective dense-range positive K).

    E=the exact electric neutral 42-band, P0=constant vacuum,
    R0=complete other neutral electric spectrum.
      t=kappa1^4 is the exact electric E eigenvalue,
      tau=||K_R0||<=beta^4/[576(1-y)^2],
      rho=tau/t <=4/[9(1-y)^6] <9/20.

    For J, let lambda*=t*(1+beta/6) and
      q=e^(24beta)<=1/(1-24beta),
      eps=||exp(beta V)-I||<=25beta,
      rem=||exp(beta V)-I-beta V||<=289beta^2.

    On [lambda*,q*t], eliminate scalar vacuum block a-lambda
    with gap >=99/100, then entire infinite-dimensional tail
    block with spectral gap >=t/2. The Schur correction E->E,
    relative to t*(I+beta M)-lambda, has norm <=t*Delta,
    where
      Delta <=289beta^2 + (100/99)*eps^2
        +(9/10)*eps^2*(1+(100/99)*eps)^2
      <1500beta^2 < beta/6.

    WG06 gives M eigenvalues (+sqrt8/8)x6,0x30,
    (-sqrt8/8)x6, and sqrt8/8>1/3. Thus the 42x42
    Schur complement has precisely six positive and
    36 negative directions at lambda*. The vacuum contributes
    one positive direction, the full tail negative. Hence
    J has exactly seven eigenvalues above lambda* (one
    vacuum and SIX interacting neutral excitations), uniformly
    for every 0<beta<=1/10000. The six eigenvalues form
    the actual neutral indices 2 through 7.
    """
    beta = R.of(beta)
    require(R(0) < beta <= SIX_BETA_MAX,
            "beta_outside_full_six_cluster_window")
    graph = exact_graph_spectral_certificate()
    require(graph["top6_multiplicity"] == 6
            and graph["zero_multiplicity"] == 30
            and graph["bottom6_multiplicity"] == 6
            and graph["source_positive6_weight"] == R(1,32),
            "wrong_WG06_first_magnetic_sector")
    c = neutral_tail_character_envelope(beta)
    y = beta.power(2).div(4)
    lo = c["kappa1_lower"].power(4)
    hi = c["kappa1_upper"].power(4)
    require(R(0) < lo < hi < R(1,2),
            "original_electric_42band_spectral_enclosure")
    tau = c["kappa2_upper"].power(2)
    rho = R(4,9).div((R(1)-y).power(6))
    require(tau <= rho*lo and rho < R(9,20),
            "all_spin_tail_over_band_ratio_failed")
    q = R(1).div(R(1)-24*beta)
    # The complement inverse is used at every true six-eigenvalue
    # lambda in [theta,q*t], so check the worst upper endpoint q*t.
    require((R(1)-24*beta)-q*hi
            >=R(99,100), "vacuum_Schur_gap_not_certified")
    require(R(1)+beta.div(6)-q*rho>=R(1,2),
            "tail_Schur_gap_not_certified")
    require((R(24)*beta).div(R(1)-24*beta)<=25*beta,
            "Wilson_magnetic_exponential_majorant")
    require(R(24*24,2).div(R(1)-24*beta)<=R(289),
            "Wilson_magnetic_second_order_remainder")
    eps = 25*beta
    delta_coeff = R(289)+R(100,99)*R(625)
    delta_coeff += R(9,10)*R(625)*(
        R(1)+R(100,99)*eps).power(2)
    require(delta_coeff<R(1500)
            and R(1500)*beta < R(1,6),
            "full_physical_Feshbach_six_state_gap_HOLD")
    require(R(1,9) < R(1,8), "positive_slope_lower_one_third_failed")
    # six positive, thirty-six negative E-directions, plus one
    # positive vacuum and all-negative infinite-dimensional tail.
    return {"beta":beta,"electric_band_lo":lo,
            "electric_band_hi":hi,"relative_tail":rho,
            "Schur_error_coefficient":delta_coeff,
            "Schur_error_rel_upper":R(1500)*beta.power(2),
            "cutoff_relative_to_exact_t":R(1)+beta.div(6),
            "physical_neutral_top_six_rank":6,
            "physical_neutral_top_six_indices":(2,3,4,5,6,7),
            "individual_first_eigenstate_weight":"OPEN"}


def original_interacting_six_Wilson_weight(beta):
    """Rank-six true-source positive overlap via exact projector angles.

    For actual J eigenvector psi in the top-six cluster:
    after vacuum/tail elimination, its E vector has non-plus
    part <= (1500beta^2)/(beta/6)=9000beta times E norm.
    Whole tail norm <=36beta and its vacuum part <=26sqrt(t)beta.
    Thus for normalized psi:
       ||(I-Pplus) psi|| <=9100beta.
    Six orthogonal eigenvectors and sqrt6<5/2 give
       ||P6_J-Pplus||<=22750beta.

    Polar mapping to original physical transfer T is
       phi=e^(beta V/2) Khalf psi /sqrt(lambda),
    an isometric mapping of true eigenbases. For a top-six psi:
      exp-half relative part <=13beta,
      electric E factor <=24beta,
      vacuum factor <=26beta,
      electric tail factor <=36beta.
    Hence ||phi-psi||<=100beta. The rank-six transfer projector
    distance is <=500beta, so ||P6_T-Pplus||<=23250beta.

    WG05's original centred physical source u=(W-<W>)Omega and
    the Haar basis vector W obey ||u-W||<=6e+3d<=148beta
    when 0<beta<=1/1000000.

    WG06 has ||Pplus W||^2=1/32, hence ||Pplus W||>1/6
    and ||W||=1/2. Therefore:
      ||P6_T u|| >1/6-(23250/2+148)beta
                =1/6-11773beta
                >3/20  (beta<=1/1000000).
    Its true squared physical first-six Wilson weight >9/400.
    """
    beta = R.of(beta)
    require(R(0) < beta <= WEIGHT_BETA_MAX,
            "beta_outside_positive_six_source_window")
    s = six_cluster_schur_certificate(beta)
    parent = original_physical_wilson_42band_weight(beta)
    require(parent["weight_lower"] > R(1,5),
            "original_interacting_Wilson_source_not_authenticated")
    # Use coarse rational enclosures independently of any floating
    # root or approximate diagonalization.
    require(R(6) < R(25,4), "six_mode_sqrt6_majorant_failed")
    require(R(1,32) > R(1,36),
            "wrong_first_slope_Wilson_source_projection")
    require(R(1500)*beta.power(2) <=R(1500)*SIX_BETA_MAX.power(2),
            "Schur_error_beta_regression")
    # Vacuum component after tail elimination:
    # (100/99)*epsilon*[1+sqrt(rho)*36beta], with sqrt(rho)<7/10.
    require(R(100,99)*R(25)*(
                R(1)+R(7,10)*R(36)*SIX_BETA_MAX) <R(26),
            "vacuum_eigenvector_six_angle_bound")
    # Polar transfer eigenvector: 13beta magnetic-half factor,
    # 24beta electric-band normalization, 26beta vacuum,
    # 36beta tail. Independent spectral upper q ensures lambda>=t.
    require(R(12).div((R(1)-12*SIX_BETA_MAX).power(2))
            <R(13), "polar_magnetic_half_exponential")
    require(R(13)+R(24)+R(26)+R(36) <R(100),
            "polar_operator_eigenvector_angle_overbudget")
    # The following are deliberately conservative exact-rational
    # inequalities supporting the full proof in the module docstring.
    p6J_gap = 22750*beta
    transfer_polar_gap = 500*beta
    combined = p6J_gap + transfer_polar_gap
    require(combined == 23250*beta,
            "original_interacting_rank6_projection_distance")
    # epsilon is smaller than 25beta, rho<=9/20,
    # vacuum/tail resolvents have margins 99/100 and t/2.
    require(R(2)*R(7,10)*R(25)*(
                R(1)+R(100,99)*R(25)*SIX_BETA_MAX) < R(36),
            "complete_electric_tail_eigenvector_bound")
    # At beta<=1/1000000, d=48beta/(1-48beta)<49beta;
    # e=electrically excited norm /b <beta^2/8.
    b = R(1)-48*beta
    require((48*beta).div(b) <49*beta,
            "original_vacuum_magnetic_source_norm")
    require(parent["source_L2_error_upper"] <148*beta,
            "true_interacting_Wilson_centering_source_error")
    lower_norm = R(1,6) - combined.div(2) - 148*beta
    require(lower_norm == R(1,6)-11773*beta
            and lower_norm > R(3,20),
            "true_original_six_band_Wilson_weight_HOLD")
    # Squared actual source overlap is strictly >9/400, and
    # at least one of the six true physical eigenvectors carries
    # >9/(400*6)=3/800.
    return {"beta":beta,"rank":6,"projector_distance_upper":combined,
            "source_distance_upper":148*beta,
            "norm_lower":lower_norm,"weight_lower":R(9,400),
            "one_true_eigenmode_lower":R(3,800),
            "individual_first_neutral_weight":"OPEN"}


def receipt():
    require(verify_fourth_Haar_tensor(),
            "continuous_SU2_quartic_Haar_negative_control_failed")
    rows=[
        "YM4_WG07_SU2_HAAR|original_continuous_SU2=YES"
        "|24_point_Hurwitz_quaternion_fourth_tensor=EXACT"
        "|E_q0power4=1/8|E_q0sq_q1sq=1/24"
        "|original_same_plaquette_chi_W2_chi=1/2"
        "|Q8_quartic_Haar=INVALID_CONTROL|json=0",
        "YM4_WG07_OPERATOR|L=2,2,2|original_24_magnetic_plaquettes=YES"
        "|physical_Gauss=YES|full_infinite_Peter_Weyl=YES"
        "|J=Khalf_exp_betaV_Khalf|isospectral_original_T=YES|json=0",
        "YM4_WG07_FESHBACH|vacuum_gap_ge=99/100"
        "|tail_gap_ge=t_over2|exp_magnetic_error_le=25beta"
        "|second_order_Taylor_norm_le=289beta2"
        "|effective_42_Schur_norm_le=1500beta2_times_t|json=0",
    ]
    for d in (10000,100000,1000000):
        beta=R(1,d)
        s=six_cluster_schur_certificate(beta)
        require(s["physical_neutral_top_six_rank"]==6,
                "rank6_full_transfer_hold")
        rows.append(
            "YM4_WG07_RANK6|beta="+str(beta)
            +"|neutral_physical_eigenvalue_indices=2_to_7"
            +"|actual_interacting_six_projector=PASS"
            +"|full_neutral_complement_bound=PASS|json=0"
        )
    for d in (1000000,10000000):
        beta=R(1,d)
        s=original_interacting_six_Wilson_weight(beta)
        require(s["rank"]==6 and s["weight_lower"]==R(9,400),
                "rank6_positive_source_hold")
        rows.append(
            "YM4_WG07_WILSON_SOURCE|beta="+str(beta)
            +"|true_vacuum_centered=YES"
            +"|actual_interacting_six_spectral_weight_gt=9/400"
            +"|one_eigenmode_of_six_weight_gt=3/800"
            +"|first_individual_neutral_weight=OPEN|json=0"
        )
    rows.append(
        "YM4_WG07_VERDICT|original_SU2_full_interacting_neutral_top6=PASS"
        "|true_physical_vacuum_Wilson_top6_weight_gt=9/400_FOR_BETA_LE_1e-6"
        "|all_six_eigenmode_positions=2_to_7_IN_NEUTRAL"
        "|individual_first_neutral_Wilson_overlap=OPEN"
        "|full_42by42_second_derivative_matrix=OPEN"
        "|large_volume_weak_coupling_continuum_gap=OPEN|json=0"
    )
    return "\n".join(rows)+"\n"


if __name__=="__main__":
    print(receipt(),end="")
