"""VOL05: exact independent strong-coupling Wilson-channel spectral ledger.

Uses original 4D continuous-SU2 Wilson link geometry, the already accepted
YM4-04B application of a named Dobrushin comparison theorem, and standard
positive Wilson transfer spectral representation. The mathematical proof is
in NOTE-YM4-VOL05-WILSON-SPECTRAL-SUPPORT-20261122.md.

This program checks only exact integer rational instances and 4D geometry;
it does not numerically verify the external comparison theorem or formally
prove OS/transfer positivity. Only Wilson-visible spectrum is covered.
"""
from collections import defaultdict, deque
from itertools import combinations, product


def check(ok, name):
    if not ok:
        raise ValueError(name)


def shifted(site, axis, side):
    z = list(site)
    z[axis] = (z[axis] + 1) % side[axis]
    return tuple(z)


def lattice_4d(spatial, temporal):
    side = (temporal, spatial, spatial, spatial)
    vertices = tuple(product(*(range(s) for s in side)))
    edges = tuple((v, d) for v in vertices for d in range(4))
    adjacency = {e: defaultdict(int) for e in edges}
    inc = {e: 0 for e in edges}
    for site in vertices:
        for a, b in combinations(range(4), 2):
            p = ((site, a), (shifted(site, a, side), b),
                 (shifted(site, b, side), a), (site, b))
            check(len(set(p)) == 4, "plaquette_repeated_original_link")
            for e in p:
                inc[e] += 1
                for other in p:
                    if other != e:
                        adjacency[e][other] += 1
    check(all(v == 6 for v in inc.values()),
          "four_dimensional_six_plaquette_incidence")
    check(all(sum(row.values()) == 18 for row in adjacency.values()),
          "four_dimensional_eighteen_neighbor_multiplicity")
    return adjacency, side


def square_at_time(t):
    s = (t, 0, 0, 0)
    return (
        (s, 1), ((t, 1, 0, 0), 2),
        ((t, 0, 1, 0), 1), (s, 2)
    )


def graph_distance(adjacency, first, second):
    target = set(second)
    frontier = deque((e, 0) for e in first)
    seen = set(first)
    while frontier:
        edge, d = frontier.popleft()
        if edge in target:
            return d
        for adjacent in adjacency[edge]:
            if adjacent not in seen:
                seen.add(adjacent)
                frontier.append((adjacent, d + 1))
    raise ValueError("temporal_plaquette_graph_disconnected")


def ipow(n, exponent):
    out = 1
    for unused in range(exponent):
        out *= n
    return out


def less(num1, den1, num2, den2):
    check(den1 > 0 and den2 > 0, "positive_rational_denominator")
    return num1 * den2 < num2 * den1


def covariance_bound(beta_n, beta_d, separation):
    # Alpha=18beta, F/G local normalized spatial plaquette support=4;
    # named Dobrushin comparison gives 4 alpha^r/(1-alpha).
    check(beta_n > 0 and 18 * beta_n < beta_d,
          "strong_coupling_dobrushin_gate")
    an, ad = 18 * beta_n, beta_d
    return (4 * ipow(an, separation) * ad,
            ipow(ad, separation) * (ad - an))


def uniform_wilson_ledger(beta_n, beta_d):
    check(18 * beta_n < beta_d,
          "d_obr_gate_rejects_large_beta")
    # Conditional single-link log potential is within +/-6beta;
    # density relative to Haar >= exp(-12beta) >= 1-12beta.
    var_num, var_den = beta_d - 12 * beta_n, 4 * beta_d
    check(var_num > 0, "positive_lower_Wilson_variance")
    check(18 * beta_n > 0, "spectral_support_ratio_positive")
    return (18 * beta_n, beta_d, var_num, var_den)


def certify():
    adjacency, side = lattice_4d(3, 7)
    check(side == (7, 3, 3, 3), "genuine_3p1_geometry")
    check(graph_distance(adjacency, square_at_time(0),
                         square_at_time(3)) == 3,
          "exact_spatial_Wilson_time_separation")
    a_n, a_d, v_n, v_d = uniform_wilson_ledger(1, 1000)
    check(a_n * 500 == 9 * a_d,
          "alpha_9_over_500")
    check(v_n * 1000 == 247 * v_d,
          "uniform_variance_247_over_1000")
    bound3 = covariance_bound(1, 1000, 3)
    bound9 = covariance_bound(1, 1000, 9)
    check(less(bound3[0], bound3[1], 1, 10000),
          "third_time_step_connected_covariance")
    check(less(bound9[0], bound9[1], 1, 100000000000000),
          "ninth_time_step_connected_covariance")
    rejected = False
    try:
        uniform_wilson_ledger(1, 10)
    except ValueError:
        rejected = True
    check(rejected, "high_beta_negative_control")

    # Synthetic contradiction: a positive spectral atom with ratio
    # 1/10 > alpha=9/500 and weight 1/4 violates the all-n covariance
    # upper envelope already at n=3. For all n this follows by powers.
    c_num, c_den = covariance_bound(1, 1000, 3)
    check(less(c_num, c_den, 1, 4000),
          "positive_transfer_spectral_support_falsifier")
    return (
        "YM4_VOL05_GEOMETRY|original_4D_SU2=YES"
        "|spatial_L=3|temporal_T=7|each_link_plaquettes=6"
        "|neighbor_multiplicity=18|temporal_distance_3=EXACT|json=0\n"
        "YM4_VOL05_SPECTRAL|beta=1/1000|alpha=9/500"
        "|Wilson_visible_transfer_ratio_le=9/500"
        "|local_centered_Wilson_total_weight_ge=247/1000"
        "|scope=ALL_FINITE_SPATIAL_L|json=0\n"
        "YM4_VOL05_INPUTS|Dobrushin_comparison=YM4_04B_NAMED_THEOREM"
        "|transfer_positive=STANDARD_SU2_WILSON_HAAR"
        "|numerical_Lean_proof=NOT_CLAIMED|json=0\n"
        "YM4_VOL05_SCOPE|Wilson_spectral_support_gap=STRONG_COUPLING"
        "|first_full_physical_state=NOT_IDENTIFIED"
        "|weak_coupling_beta_to_infty=OPEN"
        "|continuum_mass_gap=OPEN|json=0\n"
    )


if __name__ == "__main__":
    print(certify(), end="")
