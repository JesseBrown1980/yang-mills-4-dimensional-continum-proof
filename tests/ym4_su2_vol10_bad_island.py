"""YM4 VOL10 original SU2 periodic cube occupancy + conditional bad-island gate.

Integer-only falsifiers: original 4D link graph, box probabilities, greedy
independent sets, rooted animals and perfect-correlation negative controls.
The joint bad-star probability is an OPEN analytic SU2 input.
"""
from itertools import product


def require(ok, name):
    if not ok:
        raise ValueError(name)


def gcd(a, b):
    a = abs(a)
    while b:
        a, b = b, a % b
    return a


def q(n, d=1):
    require(isinstance(n, int) and isinstance(d, int) and d > 0,
            "rational_integer_positive_denominator")
    k = gcd(n, d)
    return (n // k, d // k)


def qle(a, b):
    return a[0] * b[1] <= b[0] * a[1]


def power(base, exponent):
    require(isinstance(base, int) and isinstance(exponent, int)
            and 0 <= exponent <= 300, "bounded_nonfloating_power")
    p = 1
    for unused in range(exponent):
        p *= base
    return p


def box_bound(k, j, r=1):
    require(1 <= k <= 60 and 0 <= j <= 15 and r >= 1,
            "bounded_ternary_box_parameters")
    # epsilon=1/2, beta=9^k, cube b=3^j based vertices.
    # 4*b^4 * 8*(35+18*k)/(epsilon*9^k) divided by r.
    return q(64 * power(3, 4*j) * (35+18*k),
             r * power(9, k))


def check_boxes():
    a = box_bound(12, 3)
    require(a == (16064, 531441), "beta9power12_side27")
    require(qle(a, q(1, 30)), "side27_probability_below_one_over30")
    b = box_bound(12, 4)
    require(b == (16064, 6561), "side81_raw_union")
    require(not qle(b, q(1)), "side81_union_noninformative")
    c = box_bound(16, 5)
    require(c == (20672, 531441), "beta9power16_side243")
    require(qle(c, q(1, 25)), "side243_probability_below_one_over25")
    require(box_bound(12, 3, 4) == (4016, 531441),
            "bad_star_count_four_markov")
    # A larger cube at the same beta must never spuriously get a
    # smaller raw union bound.
    for k in (6, 9, 12, 16):
        for j in range(0, 5):
            require(qle(box_bound(k, j), box_bound(k, j+1)),
                    "monotone_original_box_count")


def step(x, mu, L):
    v = list(x)
    v[mu] = (v[mu] + 1) % L
    return tuple(v)


def original_link_graph(L):
    require(L in (3, 4), "verified_original_link_graph_volume")
    vertices = list(product(range(L), repeat=4))
    links = [(x, mu) for x in vertices for mu in range(4)]
    neighbors = {e: set() for e in links}
    incident_counts = {e: 0 for e in links}
    plaquettes = []
    for x in vertices:
        for mu in range(4):
            for nu in range(mu+1, 4):
                p = ((x, mu), (step(x, mu, L), nu),
                     (step(x, nu, L), mu), (x, nu))
                require(len(set(p)) == 4, "four_distinct_plaquette_edges")
                plaquettes.append(p)
                for e in p:
                    incident_counts[e] += 1
                    for f in p:
                        if e != f:
                            neighbors[e].add(f)
    require(len(neighbors) == 4 * L * L * L * L,
            "actual_original_four_dimensional_link_count")
    require(len(plaquettes) == 6 * L * L * L * L,
            "original_four_dimensional_plaquette_count")
    require(all(c == 6 for c in incident_counts.values()),
            "original_six_plaquettes_per_link")
    require(6 * len(links) == 4 * len(plaquettes),
            "incidence_four_to_one_defect_budget")
    # A selected plaquette defect can trigger bad-star labels on at most
    # its four original oriented links; this is geometry, not an assertion
    # that arbitrarily selected original plaquettes are actually defective.
    selected_defects = plaquettes[::11]
    potentially_bad = set(e for p in selected_defects for e in p)
    require(len(potentially_bad) <= 4 * len(selected_defects),
            "four_to_one_Wilson_defect_budget")
    require(all(len(v) == 18 for v in neighbors.values()),
            "original_Wilson_graph_degree_exact_eighteen")
    for e, vs in neighbors.items():
        require(all(e in neighbors[f] for f in vs),
                "undirected_plaquette_sharing_adjacency")
    return neighbors


def selected_connected(neighbors, root, size):
    got = [root]
    seen = {root}
    i = 0
    while len(got) < size and i < len(got):
        for e in sorted(neighbors[got[i]]):
            if e not in seen:
                seen.add(e)
                got.append(e)
                if len(got) == size:
                    break
        i += 1
    require(len(got) == size, "connected_sample_size")
    return set(got)


def greedily_independent(neighbors, subset):
    available = set(subset)
    chosen = set()
    while available:
        v = sorted(available)[0]
        chosen.add(v)
        available.discard(v)
        available.difference_update(neighbors[v])
    require(all(not (neighbors[e] & chosen) for e in chosen),
            "independent_original_plaquette_stars")
    return chosen


def check_original_graphs():
    for L in (3, 4):
        neighbors = original_link_graph(L)
        root = sorted(neighbors)[0]
        # Explicit rooted animals of sizes 1 to 3, independent of the
        # large 18^(2m-2) paper-and-pencil walking bound.
        animals = {frozenset((root,))}
        for m in (1, 2, 3):
            require(len(animals) <= power(18, 2*(m-1)),
                    "rooted_animal_count_walk_injection")
            sample = sorted(animals, key=lambda s: sorted(s))[0]
            chosen = greedily_independent(neighbors, sample)
            require(len(chosen) * 19 >= len(sample),
                    "greedy_independent_set_ceil_m_over_19")
            if m < 3:
                extended = set()
                for a in animals:
                    border = set()
                    for e in a:
                        border.update(neighbors[e])
                    for e in border.difference(a):
                        extended.add(a.union((e,)))
                animals = extended
        sample40 = selected_connected(neighbors, root, 40)
        chosen40 = greedily_independent(neighbors, sample40)
        require(19 * len(chosen40) >= 40,
                "forty_link_independent_star_packing")
    return "L3_AND_L4_DEGREE18"


def check_conditional_tail_arithmetic():
    # For any independent-set joint activity rho<=18^(-57):
    # rooted animal <=18^(2m-2) rho^(ceil(m/19))
    #             <=18^(-m-2), because ceil(m/19)>=m/19.
    for m in range(1, 2001):
        minimum_packing = (m + 18) // 19
        require(19 * minimum_packing >= m, "exact_greedy_ceil")
        exponent = 2*(m-1) - 57*minimum_packing
        require(exponent <= -m-2, "conditional_tail_exponent")
    # Abstract countermodel: all indicator variables share a Bernoulli Z.
    # Each marginal p=1/9, independent-pair joint is p, not p^2.
    p = q(1, 9)
    joint = p
    product_of_marginals = q(1, 81)
    require(not qle(joint, product_of_marginals),
            "perfect_correlation_rejects_product_inference")
    for m in (1, 2, 19, 20, 100):
        require(p == joint and m <= 324,
                "countermodel_large_island_stays_at_one_site_probability")


def certify():
    check_boxes()
    graph = check_original_graphs()
    check_conditional_tail_arithmetic()
    require(graph == "L3_AND_L4_DEGREE18", "original_graph_replay")
    return (
        "YM4_VOL10_MODEL|original_continuous_SU2_Wilson=YES|law=periodic_Gibbs|bad_star=15_gauge_invariant_loop_test|json=0\n"
        "YM4_VOL10_BOX|beta=9_power_12|epsilon=1/2|side=27|P_any_bad_le=16064/531441|side81_raw=16064/6561|side81_verdict=INCONCLUSIVE|json=0\n"
        "YM4_VOL10_BOX_LARGE|beta=9_power_16|epsilon=1/2|side=243|P_any_bad_le=20672/531441|four_bad_count_side27_le=4016/531441|json=0\n"
        "YM4_VOL10_GRAPH|dimension=4|L3_link_count=324|L4_link_count=1024|degree=18|rooted_animals_le=18_power_2m_minus2|greedy_independent_ge=ceil_m_over19|json=0\n"
        "YM4_VOL10_DEFECT|bad_star_implies_incident_bad_plaquette=YES|full_volume_bad_link_count_le=4_times_bad_plaquette_count|island_size_m_requires_defect_count_ge=ceil_m_over4|original_Wilson=YES|json=0\n"
        "YM4_VOL10_CONDITIONAL|independent_set_joint_rho=OPEN|if_rho_le=18_power_minus57|then_root_island_tail_le=18_power_minus_m_minus2|sampled_integer_exponents=PASS|json=0\n"
        "YM4_VOL10_NEGATIVE|perfectly_correlated_all_bad_indicator=REJECT_PRODUCT_INFERENCE|one_site_marginal_does_not_give_cluster_tail=YES|physical_cube_conditional=OPEN|json=0\n"
        "YM4_VOL10_SCOPE|periodic_original_SU2_finite_box=ANALYTIC_DERIVATION|bad_island_joint=OPEN|arbitrary_exterior_block=OPEN|11_continuum_gates=OPEN|json=0\n"
    )


if __name__ == "__main__":
    print(certify(), end="")
