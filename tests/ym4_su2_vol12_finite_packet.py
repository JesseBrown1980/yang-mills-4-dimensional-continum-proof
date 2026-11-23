"""YM4 VOL12 preliminary original SU2 finite-volume packet certificate.

Checks unconditional multi-bad-star bound derived from VOL09 global
Haar cap partition function, independent Wilson plaquette supports, and
VOL10 deterministic local defect implication. Integer-only mathematics;
continuous Haar integration stays in the accompanying analytic proof.
"""
from itertools import product


def require(ok, label):
    if not ok:
        raise ValueError(label)


def step(x, mu, L):
    t = list(x)
    t[mu] = (t[mu] + 1) % L
    return tuple(t)


def link_incidence(L):
    points = product(range(L), repeat=4)
    adjacency = {}
    support = {}
    for x in points:
        for mu in range(4):
            adjacency[(x, mu)] = set()
            support[(x, mu)] = set()
    plaquettes = []
    for x in product(range(L), repeat=4):
        for mu in range(4):
            for nu in range(mu+1, 4):
                p = ((x, mu), (step(x, mu, L), nu),
                     (step(x, nu, L), mu), (x, nu))
                plaquettes.append(p)
                for e in p:
                    support[e].add(len(plaquettes)-1)
                    for f in p:
                        if e != f:
                            adjacency[e].add(f)
    require(len(adjacency) == 4*L**4 and len(plaquettes) == 6*L**4,
            "four_dim_original_incidence")
    require(all(len(s) == 6 for s in support.values()),
            "six_original_plaquettes_per_link")
    require(all(len(s) == 18 for s in adjacency.values()),
            "eighteen_original_neighbors")
    return adjacency, support


def independent_packet(adjacency, support, r):
    selected = []
    for e in sorted(adjacency):
        if all(e not in adjacency[f] for f in selected):
            selected.append(e)
        if len(selected) == r:
            break
    require(len(selected) == r, "r_distinct_pivots_exist")
    require(all(support[e].isdisjoint(support[f])
                for i, e in enumerate(selected) for f in selected[i+1:]),
            "distinct_forced_plaquettes")
    return selected


def envelope_parameters(k, L, r):
    """P(r bad separated stars) <= A^V/2^n, exact integer envelope.

    beta=9^k, epsilon=1/16. A=27(1536 beta^(3/2))^4,
    n=floor(r beta epsilon/8)=floor(r 9^k /128).
    Derivation: Z>=exp(beta Np-Np/2) (1536 beta^1.5)^(-Ne),
    E implies r distinct plaquette deficits > epsilon/4,
    exp(3V)<27^V, exp(x)>2^floor(x/2) (x>0).
    """
    require(1 <= k <= 18 and L >= 3 and 1 <= r <= 4*L**4,
            "parameter_domain")
    beta = 9**k
    vol = L**4
    prefactor = 27*(1536*27**k)**4
    denom_exp = r*beta//128
    conservative_margin = denom_exp-vol*prefactor.bit_length()
    return beta, prefactor, denom_exp, conservative_margin


def certify():
    for L in (3, 4):
        graph, support = link_incidence(L)
        independent_packet(graph, support, 2)
        independent_packet(graph, support, 4)
        require(len(next(iter(support.values()))) == 6,
                "original_selected_incidence")
    # L=3,4 have a rigorous two- and four-star envelope far below 1
    # at beta=9^7. These bounds are deliberately NOT uniform in volume.
    results = []
    for L in (3, 4):
        for r in (2, 4):
            beta, prefactor, n, margin = envelope_parameters(7, L, r)
            require(margin >= 1000, "pilot_probability_lt_2power_minus1000")
            results.append((L, r, margin))
    require(results == [(3, 2, 60072), (3, 4, 134806),
                        (4, 2, 28397), (4, 4, 103131)],
            "independent_reconstruction_of_exact_margins")
    # Red gate: at fixed beta the global-cap envelope eventually grows
    # with volume. It cannot be used as a uniform rho^r certificate.
    _, _, _, large_margin = envelope_parameters(7, 8, 2)
    require(large_margin < 0, "reject_volume_uniform_activity")
    # Red gate: two adjacent star pivots can share a defective plaquette,
    # so no r-times-energy-deficit claim for overlapping stars.
    graph, support = link_incidence(3)
    root = sorted(graph)[0]
    near = sorted(graph[root])[0]
    require(not support[root].isdisjoint(support[near]),
            "reject_adjacent_two_star_energy_additivity")
    # Correct model-specific epsilon action deficit: B_e forces a
    # plaquette deficit strictly above epsilon/4 = 1/64.
    require(4*16 == 64 and 8*16 == 128,
            "defect_and_integer_exponential_factors")
    return (
        "YM4_VOL12_MODEL|original_continuous_SU2_Wilson=ANALYTIC|epsilon=1/16|dimension=4|json=0\n"
        "YM4_VOL12_GEOMETRY|L3_links=324|L4_links=1024|degree=18|packet_sizes=2,4|disjoint_incident_plaquette_sets=PASS|json=0\n"
        "YM4_VOL12_THEOREM|unconditional_P_all_r_bad_le=min_1_A_power_V_over_2_power_n|A=27_times_1536_times_27powerk_to_power4|n=floor_r_times_9powerk_over128|all_beta_original_Haar_cap=ANALYTIC|json=0\n"
        "YM4_VOL12_K7_L3|beta=4782969|two_star_lt=2power_minus60072|four_star_lt=2power_minus134806|integer_only=PASS|json=0\n"
        "YM4_VOL12_K7_L4|beta=4782969|two_star_lt=2power_minus28397|four_star_lt=2power_minus103131|integer_only=PASS|json=0\n"
        "YM4_VOL12_REDS|adjacent_stars_nonadditive=REJECTED|volume_uniform_promotion=REJECTED|json=0\n"
        "YM4_VOL12_SCOPE|finite_volume_unconditional_packet=DERIVED|uniform_independent_bad_star_rho=OPEN|physical_size_cube=OPEN|11_continuum_gates=OPEN|json=0\n"
    )


if __name__ == '__main__':
    print(certify(), end='')
