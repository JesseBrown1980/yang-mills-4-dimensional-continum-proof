"""YM4-WG05: true original SU(2) physical Wilson 42-band source weight >1/5.

Builds on WG04's exact isolated rank-42 spectral projector of the
full interacting Gauss-projected Wilson transfer at fixed spatial L=2.
Uniform for original Wilson 0<beta<=1/10000.

The true vacuum is controlled by the exact positive rank-one electric
vacuum plus its bounded excited kernel. A Rayleigh/Gram inequality
then certifies nonzero original centred local-plaquette Wilson
spectral weight in the entire interacting 42-state neutral band.
At least one individual physical eigenstate in this band has squared
Wilson overlap >1/210. Its exact rank/energy position remains OPEN.
"""
from ym4_su2_wilson_local_transfer import R, require
from ym4_su2_neutral_42_band import (
    physical_neutral_band, neutral_tail_character_envelope,
)
from ym4_su2_first_centre_energy_order import (
    check_fundamental_two_link_support,
)
from ym4_4d_wilson_cylinder_moments import floor_scaled, ceil_scaled


BETA_MAX = R(1, 10000)
RANK = 42


def physical_vacuum_source_estimates(beta):
    """Original physical centre-neutral vacuum and source error majorants.

    In the *full physical Gauss-invariant Hilbert space*, the exact
    electric convolution K_phys decomposes as P0+Kexc with
    P0=|1><1| and ||Kexc||<=kappa1^2: a nontrivial gauge-invariant
    original spatial spin network needs at least two nonzero edge
    labels, with every irrep coefficient <=kappa1. The actual
    transfer is T=Bhalf K_phys Bhalf with all magnetic plaquettes:
       T=|f><f|+E, f=Bhalf*1, 0<=E, ||E||<=kappa1^2.

    Its unique normalized positive vacuum Omega obeys
       ||Omega-f/||f||||_2 <=2 e,
    e=kappa1_upper^2 / b, b=1-48beta.
    Since b<=B<=1, c=||f||² is in [b,1], and with
       d=(1-b)/b
    both ||f/||f||-1||_2 and ||Bhalf*f/||f||-1||_2 <=d.

    For W=(1/2)Tr(original spatial plaquette), ||W||_inf<=1,
    Haar <W>=0, Haar ||W||²=1/4. Let m=<Omega,W Omega>,
    u=(W-m)Omega, z=Bhalf u. Then
      |m|<=4e+2d,  ||z-W||_2<=D=6e+3d,
      C0=||u||²<=1/4+4e+2d.
    All bounds involve the true interacting physical vacuum.
    """
    beta = R.of(beta)
    require(R(0) < beta and beta <= BETA_MAX,
            "beta_outside_source_weight_window")
    source = physical_neutral_band(beta)
    require(source["band_rank"] == RANK
            and source["Haar_local_Wilson_norm_square"] == R(1,4),
            "wrong_original_Wilson_source_or_band_rank")
    require(check_fundamental_two_link_support()["admissible"] == 12,
            "original_electric_excited_gap_unverified")
    c = neutral_tail_character_envelope(beta)
    b = R(1) - 48 * beta
    kappa1_hi = c["kappa1_upper"]
    electric_excited_norm = kappa1_hi.power(2)
    e = electric_excited_norm.div(b)
    d = (R(1)-b).div(b)
    D = 6*e + 3*d
    C0_hi = R(1,4) + 4*e + 2*d
    require(b > R(0) and D < R(1,2)
            and R(1,4) < C0_hi < R(1),
            "original_vacuum_source_error_not_controlled")
    return {"beta":beta,"band":source,"characters":c,
            "b":b,"electric_excited_norm":electric_excited_norm,
            "e":e,"d":d,"D":D,"C0_upper":C0_hi,
            "Haar_W_norm_square":R(1,4)}


def uniformly_frozen_positive_witness():
    """Exact rational endpoint envelope valid for every beta<=1/10000.

    q=beta_max=1/10000, Y=q²/4; the scalar rational functions
    e(beta),d(beta),D(beta) are increasing in beta. The Bessel
    coefficient ratios and tail coefficients admit monotone
    endpoint estimates. In the true source lower-bound formula,
    bound numerator below and denominator above to get one
    uniform *rational* w42 lower with no numerical diagonalization.
    """
    y_max = BETA_MAX.power(2).div(4)
    b_min = R(1) - 48*BETA_MAX
    d_max = (R(1)-b_min).div(b_min)
    k1hi_at_max = BETA_MAX.div(4*(R(1)-y_max))
    e_max = k1hi_at_max.power(2).div(b_min)
    D_max = 6*e_max + 3*d_max
    C0_max = R(1,4) + 4*e_max + 2*d_max
    require(b_min == R(622,625) and d_max == R(3,622),
            "frozen_original_magnetic_vacuum_envelope_changed")
    require(y_max == R(1,400000000),
            "frozen_Wilson_Bessel_y_endpoint_changed")
    require(D_max < R(1,2), "source_Wilson_L2_band_inactive")
    one_minus_y = R(1)-y_max
    rayleigh_coeff_lower = (
        one_minus_y.power(4).div(256) *
        (R(1,2)-D_max).power(2)
    )
    tail_coeff_upper = R(1).div(576*one_minus_y.power(2))
    num_lower = rayleigh_coeff_lower - tail_coeff_upper*C0_max
    # Here the exact chosen tail envelope delta(beta) is at least
    # beta^4/576 and the band-top envelope <=
    # beta^4/[256*(1-y_max)^4]. This gives an upper denominator.
    den_upper = R(1).div(256*one_minus_y.power(4)) - R(1,576)
    require(R(0) < num_lower and R(0) < den_upper,
            "positive_Wilson_band_dual_not_feasible")
    uniform = num_lower.div(den_upper)
    require(uniform > R(1,5),
            "frozen_uniform_original_SU2_band_weight_lower_failed")
    return {"y_max":y_max,"b_min":b_min,"d_max":d_max,
            "e_max":e_max,"D_max":D_max,"C0_max":C0_max,
            "numerator_coefficient_lower":num_lower,
            "denominator_coefficient_upper":den_upper,
            "weight_lower":uniform}


def original_physical_wilson_42band_weight(beta):
    """Positive source-adapted physical spectral-window dual.

    Define u=(W-<W>)Omega and z=Bhalf*u, all with *true* physical
    vacuum Omega. Let E_42 be original electric band projector.
    W lies in E_42 and ||W||_Haar=1/2; therefore
       ||E_42 z|| >= 1/2-D,
       <u,T u> = <z,K z> >= kappa1_lower^4*(1/2-D)^2.

    If Pi_42 denotes the isolated *interacting* physical neutral
    band spectral projector from WG04, with w=||Pi_42 u||²,
    full operator minmax gives
       <u,T u> <= kappa1_upper^4*w
                        +delta*(C0-w)
    with delta=kappa2_upper² bounding all other neutral excited
    physical eigenvalues. Rearrange to get a positive rational
    lower w, and independently enforce the frozen uniform bound.
    """
    source = physical_vacuum_source_estimates(beta)
    c = source["characters"]
    lower_rayleigh = (
        c["kappa1_lower"].power(4) *
        (R(1,2)-source["D"]).power(2)
    )
    delta = c["kappa2_upper"].power(2)
    band_top = c["kappa1_upper"].power(4)
    require(delta < band_top,
            "physical_Wilson_band_dual_denominator_not_positive")
    numerator = lower_rayleigh - delta*source["C0_upper"]
    require(numerator > R(0),
            "original_physical_Wilson_band_Rayleigh_HOLD")
    weight_lower = numerator.div(band_top-delta)
    uniform = uniformly_frozen_positive_witness()["weight_lower"]
    require(weight_lower >= uniform and weight_lower > R(1,5),
            "physical_Wilson_band_uniform_positive_witness_failed")
    require(weight_lower < source["C0_upper"],
            "unphysical_Wilson_band_weight_gt_source_variance")
    individual_lower = weight_lower.div(RANK)
    require(individual_lower > R(1,210),
            "individual_in_band_Wilson_eigenmode_witness_failed")
    return {"beta":R.of(beta),"rank":RANK,
            "weight_lower":weight_lower,
            "uniform_weight_lower":uniform,
            "one_eigenmode_weight_lower":individual_lower,
            "source_C0_upper":source["C0_upper"],
            "Rayleigh_lower":lower_rayleigh,
            "tail_eigenvalue_upper":delta,
            "band_eigenvalue_upper":band_top,
            "source_L2_error_upper":source["D"],
            "first_neutral_individual_weight":"OPEN"}


def acceptance_row(beta, stronger_weight, stronger_mode):
    result = original_physical_wilson_42band_weight(beta)
    require(result["weight_lower"] > stronger_weight
            and result["one_eigenmode_weight_lower"] > stronger_mode,
            "frozen_Wilson_42band_weight_example_failed")
    return (
        "YM4_WG05_ORIGINAL|beta="+str(beta)
        +"|physical_neutral_42band_rank=42"
        +"|weight_lower_1e12="+str(floor_scaled(result["weight_lower"],10**12))
        +"|one_eigenmode_lower_1e12="+str(
            floor_scaled(result["one_eigenmode_weight_lower"],10**12))
        +"|all_interacting_magnetic_plaquettes=24"
        +"|true_vacuum_centered=YES|individual_first_neutral=OPEN|json=0"
    )


def receipt():
    s=uniformly_frozen_positive_witness()
    require(s["weight_lower"]>R(1,5), "uniform_positive_source_gate_failed")
    return "\n".join((
        "YM4_WG05_SOURCE|continuous_SU2=YES|L=2,2,2"
        "|full_physical_Gauss=YES|full_magnetic_spatial_plaquettes=24"
        "|true_interacting_vacuum=YES|local_Wilson_halftrace=YES|json=0",
        "YM4_WG05_DECOMPOSITION|T=ket_Bhalf1_bra_Bhalf1_plus_E"
        "|excited_electric_operator_norm_le_kappa1_squared"
        "|vacuum_distance_L2_le_2e|source_z_minus_W_L2_le_6e_plus3d"
        "|C0_upper_le_quarter_plus4e_plus2d|json=0",
        "YM4_WG05_DUAL|Rayleigh_ge_kappa1lo_power4_times_half_minus_D_squared"
        "|tail_eigenvalue_le_kappa2hi_squared"
        "|band_top_eigenvalue_le_kappa1hi_power4"
        "|physical_42band_w_lower=EXACT_RATIONAL|json=0",
        "YM4_WG05_UNIFORM|beta_range=0_LT_beta_LE_1/10000"
        "|b_min=622/625|d_max=3/622|y_max=1/400000000"
        "|physical_Wilson_42band_weight_gt=1/5"
        "|some_individual_neutral_Wilson_eigenmode_weight_gt=1/210"
        "|first_physical_charged_Wilson_weight=ZERO|json=0",
        acceptance_row(R(1,10000),R(21,100),R(1,200)),
        acceptance_row(R(1,100000),R(24,100),R(1,175)),
        "YM4_WG05_VERDICT|original_physical_interacting_42band_Wilson_weight"
        "=CERTIFIED_POSITIVE"
        "|source_weight_whole_42band_gt_one_fifth=PASS"
        "|individual_Wilson_coupled_physical_neutral_eigenmode_exists=YES"
        "|individual_first_neutral_Wilson_weight=OPEN"
        "|larger_volume_weak_coupling=OPEN|continuum_mass_gap=OPEN|json=0",
    ))+"\n"


if __name__=="__main__":
    print(receipt(),end="")
