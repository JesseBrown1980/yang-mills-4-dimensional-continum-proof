"""YM4-WG02: exact 8-sector SU(2) centre charge of original 4D Wilson.

Three global spatial Z2 centre transformations of the original periodic
2x2x2x10 continuous SU(2) Wilson link field. The full Wilson action,
physical local Gauss projector, and magnetic/temporal transfer commute
with each centre transformation. A *contractible* local spatial Wilson
plaquette is centre-neutral; hence its vacuum-connected source has
exact zero overlap with all seven charged spectral sectors.

Projector identities are verified in exact integer group algebra.
The relative spectral ordering of the neutral and charged sectors is
a separate physical first-eigenstate isolation obligation.
"""
from itertools import product
from ym4_su2_wilson_local_transfer import require, R
from ym4_4d_wilson_cylinder_moments import (
    sites, positive_links, plaquettes, plaquette_word, translate, geometry,
)

CHARGES = tuple(product((-1, 1), repeat=3))
GROUP = tuple(product((0, 1), repeat=3))
ORIGIN = (0, 0, 0, 0)


def selected_link(link, axis):
    require(type(axis) is int and 0 <= axis < 3, "invalid_centre_direction")
    site, direction = link
    require(len(site) == 4 and type(direction) is int
            and 0 <= direction < 4, "invalid_spatial_link_key")
    return direction == axis and site[axis] == 0


def flip_count(word, axis):
    require(type(word) is tuple, "invalid_loop_word")
    return sum(int(selected_link((site, mu), axis))
               for site, mu, sign in word)


def flip_parity(word, axis):
    return -1 if flip_count(word, axis) % 2 else 1


def word_charge(word):
    return tuple(flip_parity(word, d) for d in range(3))


def winding_word(axis, base=ORIGIN):
    """Two original spatial links wrapping once around periodic direction."""
    require(type(axis) is int and 0 <= axis < 3,
            "invalid_winding_direction")
    require(len(base) == 4 and all(type(v) is int for v in base),
            "invalid_winding_base")
    first = (base, axis, 1)
    second = (translate(base, axis), axis, 1)
    require(translate(translate(base, axis), axis) == base,
            "winding_loop_not_closed")
    return (first, second)


def character(charge, group_element):
    require(charge in CHARGES and group_element in GROUP,
            "invalid_centre_character")
    sign = 1
    for e, s in zip(charge, group_element):
        if s:
            sign *= e
    return sign


def xor3(a, b):
    require(a in GROUP and b in GROUP, "invalid_centre_group_element")
    return tuple((x + y) % 2 for x, y in zip(a, b))


def projector_numerator(charge, group_element):
    """8*P_e = sum_s chi_e(s) Z_s in real centre group algebra."""
    return character(charge, group_element)


def check_projector_group_algebra():
    """P_e P_f=delta_ef P_e, sum_e P_e=I; all integer checks."""
    require(len(CHARGES) == 8 and len(GROUP) == 8,
            "wrong_eight_sector_count")
    for charge in CHARGES:
        for other in CHARGES:
            for u in GROUP:
                convolution = sum(
                    character(charge, s) *
                    character(other, xor3(u, s)) for s in GROUP
                )
                expected = (8 * character(charge, u)
                            if charge == other else 0)
                require(convolution == expected,
                        "centre_projector_multiplication_failed")
    for u in GROUP:
        total = sum(character(e, u) for e in CHARGES)
        expected = 8 if u == (0, 0, 0) else 0
        require(total == expected,
                "centre_projector_completeness_failed")
    for charge in CHARGES:
        for other in CHARGES:
            # P_e applied to eigencharacter charge f = delta(e,f).
            eigenvalue_numerator = sum(
                character(charge, s) * character(other, s)
                for s in GROUP
            )
            require(eigenvalue_numerator ==
                    (8 if charge == other else 0),
                    "centre_projector_eigencharacter_failed")
    return True


def original_full_action_centre_checks(plaquette_candidates=None):
    """All 480 original 4D plaquettes have even centre-cut incidence."""
    pls, masks = geometry(plaquette_candidates)
    links = positive_links()
    require(len(links) == 320 and len(pls) == 480
            and len(masks) == 480, "original_4D_source_mismatch")
    results = []
    for axis in range(3):
        number_flipped = sum(int(selected_link(l, axis)) for l in links)
        require(number_flipped == 40, "centre_cut_link_count_wrong")
        n0, n2, odd = 0, 0, 0
        for _, _, _, word in pls:
            n = flip_count(word, axis)
            if n == 0:
                n0 += 1
            elif n == 2:
                n2 += 1
            else:
                odd += 1
        require((n0, n2, odd) == (360, 120, 0),
                "centre_cut_plaquette_invariance_failed")
        results.append((number_flipped, n0, n2, odd))
    return tuple(results)


def spatial_source_selection():
    """Physical local Wilson source commutes with all three Z_i."""
    source = plaquette_word(ORIGIN, 0, 1)
    require(word_charge(source) == (1, 1, 1),
            "local_Wilson_source_not_centre_neutral")
    charges = []
    for axis in range(3):
        word = winding_word(axis)
        e = word_charge(word)
        expected = tuple(-1 if axis == i else 1 for i in range(3))
        require(e == expected, "incorrect_spatial_winding_charge")
        charges.append(e)
    # Gauge-invariant products of winding traces produce all eight
    # electric-centre sectors (and are not identically zero at U=I).
    all_e = set()
    for chosen in GROUP:
        q = [1, 1, 1]
        for axis in range(3):
            if chosen[axis]:
                for i in range(3):
                    q[i] *= charges[axis][i]
        all_e.add(tuple(q))
    require(all_e == set(CHARGES), "missing_electric_flux_sector_witness")
    return source, tuple(charges)


def physical_transfer_selection():
    """Analytic operator commutation proof with exact geometric premises.

    Z_i multiplies spatial links at x_i=0 by centre -I simultaneously on
    all time slices. Each spatial magnetic plaquette has two or zero
    such links; every timelike Wilson plaquette also has two or zero.
    Local gauge transformations commute with central multiplication.
    The normalized Wilson link-convolution kernel is invariant under
    multiplying both spatial arguments by the same centre sign.
    Therefore B^(1/2), P_G, K_24 and T_phys commute with Z_i.
    A unique positive physical vacuum is centre-invariant. The
    original centered local Wilson source remains neutral.
    """
    checks = original_full_action_centre_checks()
    source, charges = spatial_source_selection()
    require(check_projector_group_algebra(),
            "centre_projector_algebra_failure")
    require(all(word_charge(plaquette_word((x,y,z,0),mu,nu)) ==
                (1, 1, 1)
                for x,y,z in product((0,1), repeat=3)
                for mu in range(3) for nu in range(mu+1,3)),
            "spatial_magnetic_multiplier_not_centre_invariant")
    require(all(n0+n2 == 480 and odd == 0
                for flipped,n0,n2,odd in checks),
            "timelike_Wilson_centre_invariance_failure")
    require(word_charge(source) == (1, 1, 1),
            "centred_Wilson_source_wrong_sector")
    return {"sectors": 8, "checks": checks, "winding": charges,
            "source_charge": (1,1,1),
            "charged_Wilson_overlap_exact_zero": True,
            "first_excited_sector_order": "OPEN"}


def receipt():
    s = physical_transfer_selection()
    require(s["winding"] == ((-1,1,1),(1,-1,1),(1,1,-1)),
            "frozen_centre_winding_charge_mismatch")
    return "\n".join((
        "YM4_WG02_SOURCE|continuous_SU2=YES|full_4D_Wilson=YES"
        "|L=2,2,2|T=10|sites=80|links=320|plaquettes=480"
        "|physical_Gauss=PROJECTED|json=0",
        "YM4_WG02_CENTRE|Z2_cubed=YES|commuting_involutions=3"
        "|sector_projectors=8|each_spatial_slice_cut_links=4"
        "|all_times_cut_links_each_axis=40"
        "|each_axis_plaquettes_0_cuts=360|2_cuts=120|odd=0|json=0",
        "YM4_WG02_PROJECTORS|one_eighth_Walsh_group_algebra=EXACT"
        "|P_e_P_f_delta=PASS|sum_P_e_identity=PASS"
        "|eight_nonzero_winding_witness_sectors=YES|json=0",
        "YM4_WG02_WILSON|contractible_source_charge=+++"
        "|winding0=-++|winding1=+-+|winding2=++-"
        "|vacuum_centre_neutral=YES|json=0",
        "YM4_WG02_PHYSICAL_SELECTION|full_magnetic_B=COMMUTES"
        "|temporal_K24=COMMUTES|Gauss_P=COMMUTES"
        "|all_charged_sectors_local_Wilson_overlap=EXACT_ZERO|json=0",
        "YM4_WG02_VERDICT|centre_sector_projectors=EXACT"
        "|first_charged_eigenstate_weight=ZERO_IF_FIRST_CHARGED"
        "|first_eigenstate_sector_order=OPEN"
        "|neutral_first_excitation_isolation=OPEN"
        "|continuum_gap=OPEN|json=0",
    )) + "\n"


if __name__ == "__main__":
    print(receipt(),end="")
