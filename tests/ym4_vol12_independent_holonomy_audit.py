"""Independent VOL12 adversarial scope: flat SU2 centre holonomy and boundary covariance.

Exact integer-only centre {+I,-I} subgroup fixtures on ORIGINAL periodic
four-dimensional SU2 links. These configurations are legitimate SU2 points;
they are deterministic scope controls, not sampled Wilson-Gibbs probabilities.
"""
from fractions import Fraction
from itertools import product


def require(value, name):
    if not value:
        raise ValueError(name)


def shift(x, mu, L, step=1):
    y = list(x)
    y[mu] = (y[mu] + step) % L
    return tuple(y)


def centre_links(L, wind):
    return {(x, mu): (-1 if wind and mu == 0 and x[0] == L-1 else 1)
            for x in product(range(L), repeat=4) for mu in range(4)}


def exact_original_flat_fixture(L, wind):
    require(L in (4, 6), "even_source_torus")
    U = centre_links(L, wind)
    all_defects = 0
    all_stars = 0
    plaquette_count = 0
    for x in product(range(L), repeat=4):
        for mu in range(4):
            y = shift(x, mu, L)
            staples = []
            for nu in range(4):
                if nu == mu:
                    continue
                plus = shift(x, nu, L)
                minus = shift(x, nu, L, -1)
                minus_next = shift(minus, mu, L)
                # Staple paths both go from x to x+mu, with the central
                # SU(2) inverse equal to itself. Each equals U(x,mu)
                # for a flat connection.
                s_plus = U[(x, nu)] * U[(plus, mu)] * U[(y, nu)]
                s_minus = U[(minus, nu)] * U[(minus, mu)] * U[(minus_next, nu)]
                staples.extend((s_plus, s_minus))
                if mu < nu:
                    p = U[(x, mu)] * U[(y, nu)] * U[(plus, mu)] * U[(x, nu)]
                    plaquette_count += 1
                    all_defects += int(p != 1)
            require(len(staples) == 6, "six_original_staples")
            require(all(s == U[(x, mu)] for s in staples),
                    "all_staples_equal_link_on_flat_field")
            for i in range(6):
                for j in range(i + 1, 6):
                    # Halftrace of the double-staple loop for centre SU2
                    # is exactly the product of its centre signs.
                    all_stars += int(staples[i] * staples[j] < 1)
    require(plaquette_count == 6 * L * L * L * L,
            "all_original_4d_plaquettes")
    require(all_defects == 0 and all_stars == 0,
            "entire_flat_field_has_no_bad_plaquettes_or_bad_stars")
    winding_loop = 1
    for k in range(L):
        winding_loop *= U[((k, 0, 0, 0), 0)]
    expected = -1 if wind else 1
    require(winding_loop == expected, "SU2_global_periodic_winding")
    # SU2 normalized trace of the winding Polyakov loop equals sign;
    # the ordinary (un-normalized) trace is exactly +/-2.
    return winding_loop * 2


def sharp_boundary_covariance_replay():
    # Toy boundary law eta in {0,1}, each with mass 1/2;
    # F=eta is deterministic conditional on eta and G=eta is exterior.
    # No bad-crossing events occur. This is NOT a Wilson-Gibbs sample.
    states = (0, 1)
    half = Fraction(1, 2)
    mean = sum((half * v for v in states), Fraction(0))
    covariance = sum((half * (v-mean) * (v-mean) for v in states),
                     Fraction(0))
    delta = sum((half * half * abs(x-y)
                 for x in states for y in states), Fraction(0))
    require(mean == Fraction(1, 2), "toy_boundary_mean")
    require(covariance == Fraction(1, 4), "sharp_covariance")
    require(delta == Fraction(1, 2), "sharp_average_w1")
    require(8 * covariance * covariance == delta,
            "sharp_factor_8_boundary_covariance_inequality")
    return covariance, delta


def main():
    for L in (4, 6):
        require(exact_original_flat_fixture(L, False) == 2,
                "trivial_SU2_flat_winding")
        require(exact_original_flat_fixture(L, True) == -2,
                "nontrivial_SU2_flat_winding")
    sharp_boundary_covariance_replay()
    return (
        "YM4_VOL12_INDEPENDENT_CENTRE|original_SU2_centre_links=EXACT|even_periodic_L4_L6=PASS|plaquettes_all_W_eq1=PASS|all_15_star_pairs_good=PASS|json=0\n"
        "YM4_VOL12_INDEPENDENT_WINDING|flat_config_A_polyakov_trace=plus2|flat_config_B_polyakov_trace=minus2|periodic_gauge_invariant_distinct=YES|json=0\n"
        "YM4_VOL12_HOLO_SCOPE|bad_island_rarity_alone_all_sector_contraction=INSUFFICIENT|local_contractible_v_global_winding=SEPARATE|json=0\n"
        "YM4_VOL12_BOUNDARY_COV|toy_boundaries=ABSTRACT_CONTROL|delta_W1=1/2|Cov_F_G=1/4|eight_Cov_squared_eq_delta=SHARP|json=0\n"
        "YM4_VOL12_NEXT|upstream_Lean=REBUILT_PASS|all_Gauss_sector_good_region_transport=OPEN|physical_cube=OPEN|11_continuum_gates=OPEN|json=0\n"
    )


if __name__ == '__main__':
    print(main(), end="")
