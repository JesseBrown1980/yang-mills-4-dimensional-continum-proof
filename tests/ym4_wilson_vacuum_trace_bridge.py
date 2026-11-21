"""YM4-WV01: exact rational transfer-trace to physical vacuum source bounds.

Original 4D Wilson SU(2), 2x2x2 spatial lattice, periodic time T=10.
Builds on the full 480-plaquette WC01 finite-periodic certificate and the
positive gauge-projected finite-lattice transfer operator of YM4-02c/02d.
All arithmetic is integer-rational. No spectral eigenvalue estimation.
"""
from ym4_su2_wilson_local_transfer import R, require
from ym4_4d_wilson_cylinder_moments import (
    bounded_connected, source_haar_data, floor_scaled, ceil_scaled,
)

SPATIAL_SITES = 8
SPATIAL_LINKS = 24
SPATIAL_PLAQUETTES = 24
TIME_CIRCUMFERENCE = 10


def match_original_source(spatial_links=24, spatial_plaquettes=24,
                          temporal_circumference=10):
    """Fail closed on original 3-spatial-dimensional gauge source."""
    h = source_haar_data()
    require(h["sites"] == SPATIAL_SITES * TIME_CIRCUMFERENCE
            and h["links"] == (SPATIAL_LINKS + SPATIAL_SITES)
            * TIME_CIRCUMFERENCE
            and h["plaquettes"] == (2 * SPATIAL_PLAQUETTES)
            * TIME_CIRCUMFERENCE
            and h["spatial"] == SPATIAL_PLAQUETTES * TIME_CIRCUMFERENCE
            and h["timelike"] == SPATIAL_LINKS * TIME_CIRCUMFERENCE,
            "original_Wilson_spatial_temporal_source_mismatch")
    require(type(spatial_links) is int and spatial_links == SPATIAL_LINKS,
            "wrong_physical_spatial_link_count")
    require(type(spatial_plaquettes) is int
            and spatial_plaquettes == SPATIAL_PLAQUETTES,
            "wrong_magnetic_plaquette_count")
    require(type(temporal_circumference) is int
            and temporal_circumference == TIME_CIRCUMFERENCE,
            "wrong_periodic_trace_circumference")
    return True


def single_link_hilbert_schmidt_bound(beta):
    """Tr(K_one^2) <= 1 + y/(1-y)^3, y=beta^2/4.

    K_one is normalized SU(2) Wilson Haar convolution. On L2(SU2)
    character r has eigenvalue lambda_r=I_(r+1)/I_1 and multiplicity
    (r+1)^2. J_(r+1)<=exp(y)/(r+1)! and J_1>=1; with
    exp(y)<=1/(1-y), the sum r>=1 has the stated rational bound.
    """
    beta = R.of(beta)
    require(beta > R(0), "invalid_Wilson_beta")
    y = beta.power(2).div(4)
    require(y < R(1), "character_HS_envelope_requires_y_lt_1")
    one_minus = R(1) - y
    return R(1) + y.div(one_minus.power(3))


def physical_transfer_trace_data(beta, spatial_links=24,
                                 spatial_plaquettes=24):
    """Physical trace ratio and eigenratio bound, fixed spatial L=2.

    T = B^(1/2) P K_24 P B^(1/2) where P is spatial Gauss average,
    K_24 tensor normalized Wilson temporal Haar convolution, B the
    product of all 24 spatial Wilson plaquette weights.

    T is positive selfadjoint trace-class (YM4-02c).
    Lambda0 >= 1-2 beta N_sp by Rayleigh test B^(-1/2)*1.
    Other lambda_j/Lambda0 <= tanh(beta N_links) <= beta N_links
    (YM4-02d). The HS norm contracts under P and B^(1/2)<=1,
    so Tr T^2 <= [Tr K_one^2]^24.
    """
    match_original_source(spatial_links, spatial_plaquettes)
    beta = R.of(beta)
    one_link = single_link_hilbert_schmidt_bound(beta)
    rayleigh = R(1) - 2 * spatial_plaquettes * beta
    q = spatial_links * beta
    require(rayleigh > R(0) and q < R(1),
            "physical_trace_bound_outside_beta_range")
    trK2 = one_link.power(spatial_links)
    M = trK2.div(rayleigh.power(2))
    E = M - R(1)
    require(E > R(0), "nonvacuum_HS_envelope_failure")
    return {"beta": beta, "one_link_HS": one_link,
            "full_unprojected_HS": trK2,
            "vacuum_lambda0_lower": rayleigh,
            "nonvacuum_eigenratio_upper": q,
            "normalized_physical_trace2_upper": M,
            "excited_normalized_trace2_upper": E}


def excited_trace_power_bound(trace_data, k):
    """Sum_j>=1 (lambda_j/lambda0)^k <= E q^(k-2), k>=2."""
    require(type(k) is int and k >= 2, "trace_power_requires_at_least_two")
    return (trace_data["excited_normalized_trace2_upper"]
            * trace_data["nonvacuum_eigenratio_upper"].power(k - 2))


def thermal_to_vacuum_connected_error(trace_data, t, circumference=10):
    """|C_T(t)-C_vac(t)| <= delta_(T-t)+5 delta_T.

    If R=T_op/lambda0, the normalized periodic trace has partition
    denominator 1+delta_T; W=halfTr(space plaquette) has norm<=1.
    |periodic raw pair-vacuum raw pair|<=delta_(T-t)+delta_T.
    |periodic mean-vacuum mean|<=2delta_T; squares differ by <=4delta_T.
    """
    require(type(circumference) is int and
            circumference == TIME_CIRCUMFERENCE,
            "wrong_periodic_trace_circumference")
    require(type(t) is int and 0 <= t <= circumference - 2,
            "insufficient_time_for_trace_tail")
    return (excited_trace_power_bound(trace_data, circumference - t)
            + 5 * excited_trace_power_bound(trace_data, circumference))


def vacuum_wilson_intervals(beta):
    """Original physical fixed-lattice vacuum connected C0,C2,C4.

    The positive transfer operator supplies C_vac(t)>=0 as a spectral
    measure on the non-vacuum Hilbert space. Upper bounds use WC01's
    authentic full-action periodic source plus an explicit trace tail.
    """
    original = bounded_connected(beta)
    d = physical_transfer_trace_data(beta)
    errors = {t: thermal_to_vacuum_connected_error(d, t)
              for t in (0, 2, 4)}
    lower0 = original["C0lo"] - errors[0]
    upper0 = original["C0hi"] + errors[0]
    upper2 = original["Ct_abs"] + errors[2]
    upper4 = original["Ct_abs"] + errors[4]
    require(lower0 > R(0) and upper2 > R(0) and upper4 > R(0),
            "vacuum_source_intervals_invalid")
    return {"beta": R.of(beta), "trace": d, "errors": errors,
            "vacuum_C0_lower": lower0, "vacuum_C0_upper": upper0,
            "vacuum_C2_lower": R(0), "vacuum_C2_upper": upper2,
            "vacuum_C4_lower": R(0), "vacuum_C4_upper": upper4}


def acceptance_row(beta, excited_limit, err0_limit, err4_limit,
                   c0_limit, time_limit):
    v = vacuum_wilson_intervals(beta)
    d = v["trace"]
    require(d["excited_normalized_trace2_upper"] < excited_limit,
            "frozen_physical_Hilbert_Schmidt_failure")
    require(v["errors"][0] < err0_limit
            and v["errors"][4] < err4_limit,
            "frozen_trace_to_vacuum_error_failure")
    require(v["vacuum_C0_lower"] > R(1, 4) - c0_limit
            and v["vacuum_C0_upper"] < R(1, 4) + c0_limit,
            "frozen_vacuum_Wilson_C0_failure")
    require(v["vacuum_C2_upper"] < time_limit
            and v["vacuum_C4_upper"] < time_limit,
            "frozen_vacuum_Wilson_C2_C4_failure")
    scale = 1000000000000
    return (
        "YM4_4D_WILSON_VACUUM|spatial=2,2,2|time_trace=10"
        "|beta=" + str(beta) + "|spatial_links=24|magnetic_plaquettes=24"
        "|vac_C0_lower_1e12=" + str(floor_scaled(v["vacuum_C0_lower"],scale))
        + "|vac_C0_upper_1e12=" + str(ceil_scaled(v["vacuum_C0_upper"],scale))
        + "|vac_C2_lower=0|vac_C2_upper_1e12="
        + str(ceil_scaled(v["vacuum_C2_upper"],scale))
        + "|vac_C4_lower=0|vac_C4_upper_1e12="
        + str(ceil_scaled(v["vacuum_C4_upper"],scale))
        + "|err_t0_upper_1e12=" + str(ceil_scaled(v["errors"][0],scale))
        + "|err_t4_upper_1e12=" + str(ceil_scaled(v["errors"][4],scale))
        + "|trace2_bound=EXACT_RATIONAL"
        + "|physical_Gauss=PROJECTED|positive_Wilson_transfer=YES"
        + "|full_spatial_magnetic_action=INCLUDED"
        + "|first_Wilson_state_weight=OPEN"
        + "|continuum_uniform_mass_gap=OPEN|json=0"
    )


def receipt():
    match_original_source()
    return "\n".join((
        "YM4_WV01_SOURCE|original_SU2_Wilson=YES|spatial_sites=8"
        "|spatial_links=24|spatial_plaquettes=24|T=10"
        "|Gauss_projector=P|transfer=Bhalf_P_K24_P_Bhalf|json=0",
        "YM4_WV01_TRACE|lambda0_lower=1_minus_48beta"
        "|eigenratio_upper=24beta|TrK2_upper=(1+y/(1-y)^3)^24"
        "|y=beta2/4|delta_k_upper=(M-1)*(24beta)^(k-2)"
        "|connected_trace_error=delta_Tminus_t_plus5delta_T|json=0",
        acceptance_row(R(1, 10000), R(1, 100),
                       R(1, 100000000000000000000),
                       R(1, 1000000000000),
                       R(1, 10000), R(1, 50000)),
        acceptance_row(R(1, 100000), R(1, 1000),
                       R(1, 100000000000000000000000000000),
                       R(1, 100000000000000000),
                       R(1, 10000000), R(1, 50000000)),
        "YM4_WV01_VERDICT|original_4D_fixed_lattice_vacuum_Wilson"
        "_C0_C2_C4=EXACT_RATIONAL_INTERVALS"
        "|thermal_to_vacuum_control=PASS"
        "|positive_physical_Wilson_spectral_measure=YES"
        "|first_excited_Wilson_overlap=OPEN"
        "|weak_coupling_uniformity=OPEN|continuum_gap=OPEN|json=0",
    )) + "\n"


if __name__ == "__main__":
    print(receipt(), end="")
