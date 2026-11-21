"""YM4-WG04: original SU(2) neutral Wilson rank-42 transfer spectral band.

Exact spatial 2^3 continuous-SU2 Wilson model, all 24 magnetic
plaquettes, 24 spatial temporal-convolution factors and full Gauss law.

An exact Peter-Weyl/spin-network combinatorial classification gives a
42-dimensional neutral four-fundamental electric eigenspace spanned
by 24 spatial plaquette loops plus 18 double-winding-loop products.
For 0<beta<=1/100, full magnetic min-max carries this to a separated
rank-42 spectral *band* of the true neutral physical Wilson transfer.
No interacting Wilson-source overlap within this band is promoted.
"""
from itertools import combinations, product
from ym4_su2_wilson_local_transfer import (
    R, require, character_eigen_interval,
)
from ym4_su2_first_centre_energy_order import (
    original_spatial_links, endpoints, uniform_character_bounds,
    original_first_sector_energy_bounds,
)
from ym4_su2_center_flux_projectors import (
    selected_link, physical_transfer_selection, winding_word,
)
from ym4_4d_wilson_cylinder_moments import plaquette_word, ceil_scaled


def support_mask(edges, lookup):
    mask = 0
    for link in edges:
        require(link in lookup, "link_outside_original_spatial_source")
        bit = 1 << lookup[link]
        require(not (mask & bit), "duplicate_original_spatial_link")
        mask |= bit
    return mask


def spatial_link_lookup():
    links = original_spatial_links()
    require(len(set(links)) == 24, "duplicate_spatial_edge_source")
    return {link: i for i, link in enumerate(links)}


def four_fundamental_supports():
    """All 10626 original four-edge supports; gauge and centre parity.

    An invariant spin-1/2 edge assignment requires even count at each
    vertex. At four edges, each neutral admissible assignment has degree
    0 or 2 at every spatial site, so its invariant intertwiner is
    one-dimensional. Charged degree-four vertices may have higher
    intertwiner multiplicity; we count supports rather than dimensions.
    """
    links = original_spatial_links()
    lookup = spatial_link_lookup()
    all_sites = tuple(product((0, 1), repeat=3))
    degree4 = 0
    valid = []
    neutral = []
    charged = []
    counts = {}
    candidates = 0
    for selected in combinations(links, 4):
        candidates += 1
        degrees = {site: 0 for site in all_sites}
        for link in selected:
            a, b = endpoints(link)
            a3, b3 = a[:3], b[:3]
            degrees[a3] += 1
            degrees[b3] += 1
        if any(d % 2 for d in degrees.values()):
            continue
        charge = tuple(
            -1 if sum(int(selected_link(link, axis))
                      for link in selected) % 2 else 1
            for axis in range(3)
        )
        mask = support_mask(selected, lookup)
        require(mask.bit_count() == 4, "wrong_four_link_support")
        max_degree = max(degrees.values())
        valid.append((mask, charge, max_degree))
        counts[charge] = counts.get(charge, 0) + 1
        if max_degree == 4:
            degree4 += 1
        if charge == (1, 1, 1):
            require(max_degree == 2,
                    "neutral_four_fundamental_nonunique_intertwiner")
            neutral.append(mask)
        else:
            charged.append(mask)
    require(candidates == 10626, "wrong_four_edge_candidate_count")
    require(len(valid) == 162 and len(neutral) == 42
            and len(charged) == 120 and degree4 == 24,
            "frozen_four_fundamental_count_mismatch")
    require(counts.get((1, 1, 1), 0) == 42,
            "wrong_neutral_four_edge_count")
    for charge in ((-1, 1, 1), (1, -1, 1), (1, 1, -1)):
        require(counts.get(charge, 0) == 16,
                "wrong_single_charged_four_edge_count")
    for charge in ((-1, -1, 1), (-1, 1, -1), (1, -1, -1)):
        require(counts.get(charge, 0) == 24,
                "wrong_double_charged_four_edge_count")
    require(counts.get((-1, -1, -1), 0) == 0,
            "unexpected_triply_charged_four_edge_count")
    return {"links": links, "valid": tuple(valid),
            "neutral": tuple(neutral), "charged": tuple(charged),
            "counts": counts, "degree4": degree4}


def check_no_three_link_physical_singlet():
    """Cube multigraph has no 3-edge min-degree-two support.

    A nontrivial SU2 gauge singlet cannot have a degree-one occupied
    vertex regardless of the spin label. A support of three edges
    would need a triangle or three parallel edges, both impossible
    on original L=2 periodic cubic multigraph.
    """
    links = original_spatial_links()
    total = 0
    feasible = 0
    for subset in combinations(links, 3):
        total += 1
        degrees = {}
        for link in subset:
            a, b = endpoints(link)
            a, b = a[:3], b[:3]
            degrees[a] = degrees.get(a, 0) + 1
            degrees[b] = degrees.get(b, 0) + 1
        if all(d >= 2 for d in degrees.values()):
            feasible += 1
    require(total == 2024 and feasible == 0,
            "unexpected_three_edge_Gauss_intertwiner")
    return {"candidates": total, "min_degree_two": feasible}


def canonical_neutral_basis_supports():
    """Exactly 24 plaquette loops + 18 pairs of winding loops.

    Each is a product of fundamental Wilson characters on a support
    where each spatial vertex has 0 or 2 spin-half endpoints. The
    corresponding normalized gauge spin network has Haar norm 1.
    """
    lookup = spatial_link_lookup()
    plaquette = []
    for x, y, z in product((0, 1), repeat=3):
        site = (x, y, z, 0)
        for a in range(3):
            for b in range(a + 1, 3):
                word = plaquette_word(site, a, b)
                mask = support_mask(
                    [(base, mu) for base, mu, sign in word], lookup
                )
                plaquette.append(mask)
    require(len(plaquette) == 24 and len(set(plaquette)) == 24,
            "original_spatial_plaquette_support_count_wrong")
    doubled = []
    for axis in range(3):
        loop_masks = []
        for transverse in product((0, 1), repeat=2):
            coord = [0, 0, 0, 0]
            other = [a for a in range(3) if a != axis]
            for a, bit in zip(other, transverse):
                coord[a] = bit
            loop = winding_word(axis, tuple(coord))
            mask = support_mask(
                [(base, mu) for base, mu, sign in loop], lookup
            )
            require(mask.bit_count() == 2,
                    "nonminimal_original_winding_word")
            loop_masks.append(mask)
        require(len(loop_masks) == 4 and len(set(loop_masks)) == 4,
                "wrong_parallel_original_winding_count")
        for first, second in combinations(loop_masks, 2):
            require(first & second == 0, "winding_pair_link_overlap")
            doubled.append(first | second)
    require(len(doubled) == 18 and len(set(doubled)) == 18
            and not (set(plaquette) & set(doubled)),
            "neutral_double_winding_basis_collision")
    neutral = set(four_fundamental_supports()["neutral"])
    require(set(plaquette) | set(doubled) == neutral,
            "neutral_42_support_basis_incomplete")
    original = plaquette_word((0, 0, 0, 0), 0, 1)
    original_mask = support_mask(
        [(base, mu) for base, mu, sign in original], lookup
    )
    require(original_mask in set(plaquette),
            "original_local_Wilson_not_in_neutral_electric_band")
    return {"plaquettes": tuple(plaquette), "double_winding": tuple(doubled),
            "neutral": tuple(sorted(neutral)), "source_mask": original_mask,
            "rank": 42, "source_Haar_norm_square": R(1, 4)}


def neutral_tail_character_envelope(beta):
    """Exact physical neutral K spectrum after 42 four-fundamental modes.

    On the original graph:
    - no nonvacuum gauge-invariant 1/3 occupied-edge supports;
    - two occupied edges must be parallel, same spin, and for
      neutral charge the common spin is even >=2;
    - four occupied fundamentals have 42 neutral gauge singlets;
    - four with one higher spin: product <= kappa2*kappa1^3;
    - >=5 occupied edges: product <= kappa1^5.
    With kappa2<=kappa1^2 and kappa1^5<=kappa2_up^2
    throughout beta<=1/100, the entire neutral complement is
    bounded by beta^4/[576*(1-y)^2], not a finite-spin truncation.
    """
    beta = R.of(beta)
    uniform_character_bounds(beta)
    require(check_no_three_link_physical_singlet()["min_degree_two"] == 0,
            "three_edge_neutral_excitation_found")
    y = beta.power(2).div(4)
    om = R(1) - y
    k1_lower = (beta * om).div(4)
    k1_upper = beta.div(4 * om)
    k2_upper = beta.power(2).div(24 * om)
    require(k2_upper < k1_lower.power(2),
            "nonfundamental_representation_too_large")
    require(k1_upper < R(1) and k2_upper < k1_lower,
            "nonfundamental_representation_order_wrong")
    require(k1_upper.power(5) < k2_upper.power(2),
            "five_edge_electric_tail_too_large")
    tail = k2_upper.power(2)
    require(tail < beta.power(4).div(550),
            "frozen_neutral_electric_tail_threshold_failed")
    return {"beta": beta, "y": y, "kappa1_lower": k1_lower,
            "kappa1_upper": k1_upper, "kappa2_upper": k2_upper,
            "electric_neutral_band_lower": k1_lower.power(4),
            "electric_neutral_tail_upper": tail}


def physical_neutral_band(beta):
    """Separated original interacting physical neutral rank-42 band.

    Tphys=Bhalf P K P Bhalf, with 24 original magnetic plaquettes;
    B between exp(-48beta) >=1-48beta and 1.
    In neutral charge sector, K has vacuum eigen 1 and exactly
    42 excited eigenvalues kappa1^4, with all remaining eigenvalues
    bounded by tail. The positive compact min-max principle for
    Khalf B Khalf gives the same ordered bounds for physical Tphys.
    """
    source = canonical_neutral_basis_supports()
    require(source["rank"] == 42, "wrong_neutral_electric_band_rank")
    require(physical_transfer_selection()["source_charge"] == (1, 1, 1),
            "full_SU2_Gauss_centre_source_mismatch")
    original_first_sector_energy_bounds(beta)
    c = neutral_tail_character_envelope(beta)
    beta = c["beta"]
    b_min = R(1) - 48 * beta
    require(b_min >= R(13, 25) and b_min > R(1, 2),
            "magnetic_full_Wilson_floor_failed")
    band = b_min * c["electric_neutral_band_lower"]
    tail = c["electric_neutral_tail_upper"]
    lower = beta.power(4).div(500)
    upper_tail = beta.power(4).div(550)
    require(band > lower and tail < upper_tail,
            "original_physical_neutral_band_not_separated")
    require(lower > upper_tail and lower - upper_tail ==
            beta.power(4).div(5500),
            "frozen_physical_neutral_band_gap_mismatch")
    require(c["kappa1_upper"].power(4) < R(1, 2),
            "neutral_band_mixes_with_unique_vacuum")
    return {
        "beta": beta, "band_rank": 42, "source_mask": source["source_mask"],
        "electric_plaquette_rank": 24, "electric_double_winding_rank": 18,
        "Haar_local_Wilson_norm_square": source["source_Haar_norm_square"],
        "magnetic_floor": b_min, "neutral_vacuum_lower": b_min,
        "band_lower": band, "tail_upper": tail,
        "frozen_band_lower": lower, "frozen_tail_upper": upper_tail,
        "physical_interacting_band_projector_rank": 42,
        "neutral_band_source_weight_status": "OPEN",
    }


def receipt():
    geometry = four_fundamental_supports()
    basis = canonical_neutral_basis_supports()
    require(geometry["degree4"] == 24, "wrong_four_valent_intertwiner_count")
    rows = [
        "YM4_WG04_SOURCE|continuous_SU2=YES|original_physical_Gauss=YES"
        "|spatial_L=2|original_magnetic_plaquettes=24"
        "|original_temporal_Wilson_links=24|json=0",
        "YM4_WG04_GRAPH|total_four_link_subsets=10626"
        "|four_fundamental_gauge_even_supports=162|neutral=42|charged=120"
        "|single_charge_each=16|double_charge_each=24"
        "|three_charge=0|degree4_charged_supports=24|json=0",
        "YM4_WG04_BASIS|elementary_spatial_plaquettes=24"
        "|same_axis_double_winding_products=18"
        "|neutral_electric_Wilson_band_rank=42"
        "|original_local_Wilson_Haar_norm2=1/4"
        "|local_Wilson_electric_eigenvalue=kappa1_power4|json=0",
        "YM4_WG04_ANALYTIC|beta_range=0_LT_beta_LE_1/100"
        "|all_spins_r_ge2_bounded=YES|no_three_link_gauge_singlets=YES"
        "|neutral_K_tail_le=beta4_over576_one_minus_y_squared"
        "|physical_B_min_ge_one_minus_48beta|json=0",
    ]
    for d in (100, 10000, 100000):
        beta = R(1, d)
        physical = physical_neutral_band(beta)
        require(physical["band_rank"] == 42
                and physical["neutral_band_source_weight_status"] == "OPEN",
                "invalid_original_Wilson_band_promotion")
        rows.append(
            "YM4_WG04_PHYSICAL|beta=" + str(beta)
            + "|42_eigenvalues_band_gt=1/" + str(500 * d ** 4)
            + "|45th_neutral_eigenvalue_lt=1/" + str(550 * d ** 4)
            + "|42_dimensional_neutral_projector=EXACT_BY_MINMAX"
            + "|band_to_tail_ratio_gt=11/10"
            + "|physical_band_Wilson_overlap=OPEN|json=0"
        )
    rows.append(
        "YM4_WG04_VERDICT|original_SU2_42_neutral_electric_band=PASS"
        "|physical_interacting_neutral_42_band_isolated=PASS"
        "|first_Wilson_visible_individual_weight=OPEN"
        "|source_Feshbach_residual_needed=YES"
        "|volume_uniform_weak_coupling=OPEN|continuum_mass_gap=OPEN|json=0"
    )
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    print(receipt(), end="")
