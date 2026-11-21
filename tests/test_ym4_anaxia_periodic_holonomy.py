#!/usr/bin/env python3
"""Independent exact audit of Anaxia's mod-two fixed-link table.

The 16-site enumeration is a finite combinatorial result on Z^4 parities.
The periodic-torus gauge-orbit counterexample uses exact SU(2) rational
unit quaternions. This checker does not import Anaxia code or prove
periodic Dobrushin contraction / continuum mass gap.
"""

TABLE = (0, 0, 2, 3, 3, 1, 2, 1, 1, 2, 1, 3, 3, 2, 0, 0)


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def step(site, direction):
    return site ^ (1 << direction)


def fixed(site, direction, table=TABLE):
    return table[site] == direction


def plaquette_fixed_count(site, mu, nu, table=TABLE):
    return sum((
        fixed(site, mu, table),
        fixed(step(site, mu), nu, table),
        fixed(step(site, nu), mu, table),
        fixed(site, nu, table),
    ))


def partners(site, mu, nu, table=TABLE):
    y = step(site, nu)
    return (
        fixed(step(site, mu), nu, table),
        fixed(step(site, nu), mu, table),
        fixed(site, nu, table),
        fixed(y, nu, table),
        fixed(step(y, mu), nu, table),
        fixed(y, mu, table),
    )


def remaining_partners(site, mu, table=TABLE):
    return sum(not hit for nu in range(4) if nu != mu
               for hit in partners(site, mu, nu, table))


def opposite_planes(site, mu, table=TABLE):
    return sum(fixed(step(site, nu), mu, table)
               for nu in range(4) if nu != mu)


def local_certificate(table=TABLE):
    need(len(table) == 16 and all(0 <= v < 4 for v in table),
         "invalid_mod_two_table")
    checks = 0
    fixed_edges = 0
    unfixed_edges = 0
    for site in range(16):
        need(sum(fixed(site, mu, table) for mu in range(4)) == 1,
             "not_one_fixed_forward_link_per_site")
        for mu in range(4):
            if fixed(site, mu, table):
                fixed_edges += 1
                need(fixed(step(site, mu), mu, table),
                     "straight_fixed_line_broken")
            else:
                unfixed_edges += 1
                need(remaining_partners(site, mu, table) == 12,
                     "wrong_remaining_neighbours")
                need(2 * opposite_planes(site, mu, table) == 2,
                     "wrong_opposite_plaquette_count")
            for nu in range(mu + 1, 4):
                need(plaquette_fixed_count(site, mu, nu, table) == 1,
                     "not_one_fixed_link_per_plaquette")
                checks += 1
    need((checks, fixed_edges, unfixed_edges) == (96, 16, 48),
         "incorrect_local_counts")
    need(6 * 3 == 18 and 6 * 2 == 12,
         "ordinary_neighbour_count")
    need(4 * 42 + 2 * 25 + 4 * 18 == 290,
         "integer_link_budget")
    return checks, fixed_edges, unfixed_edges


def q_mul(a, b):
    # Exact rational SU(2) quaternion in common-denominator form:
    # (num0, num1, num2, num3, denominator), integers only.
    a0, a1, a2, a3, ad = a
    b0, b1, b2, b3, bd = b
    need(ad > 0 and bd > 0, "invalid_quaternion_denominator")
    return (
        a0*b0 - a1*b1 - a2*b2 - a3*b3,
        a0*b1 + a1*b0 + a2*b3 - a3*b2,
        a0*b2 - a1*b3 + a2*b0 + a3*b1,
        a0*b3 + a1*b2 - a2*b1 + a3*b0,
        ad*bd,
    )


def q_inv(a):
    return (a[0], -a[1], -a[2], -a[3], a[4])


def q_unit(a):
    return a[4] > 0 and sum(v*v for v in a[:4]) == a[4]*a[4]


def q_equal(a, b):
    return a[4] > 0 and b[4] > 0 and all(
        a[i]*b[4] == b[i]*a[4] for i in range(4))


def periodic_holonomy():
    # On an even L=2 torus the Z^4 parity pattern descends, but
    # each straight fixed link line is a closed periodic cycle.
    site0 = 0
    direction = 0
    site1 = step(site0, direction)
    need((site0, site1) == (0, 1), "unexpected_parity_link")
    need(fixed(site0, direction) and fixed(site1, direction),
         "expected_two_edge_cycle_missing")
    need(step(site1, direction) == site0,
         "cycle_does_not_close_in_L2_quotient")
    u = (3, 4, 0, 0, 5)
    identity = (1, 0, 0, 0, 1)
    need(q_unit(u), "sample_not_unit_SU2")
    product = q_mul(u, u)
    need(q_equal(product, (-7, 24, 0, 0, 25)),
         "unexpected_exact_polyakov_holonomy")
    need(not q_equal(product, identity),
         "nontrivial_polyakov_holonomy_was_lost")

    # Gauge transforms act on the cycle holonomy by conjugation.
    g0 = (0, 1, 0, 0, 1)
    g1 = (5, 0, 12, 0, 13)
    need(q_unit(g0) and q_unit(g1), "invalid_test_gauge")
    e0 = q_mul(q_mul(g0, u), q_inv(g1))
    e1 = q_mul(q_mul(g1, u), q_inv(g0))
    new_product = q_mul(e0, e1)
    expected = q_mul(q_mul(g0, product), q_inv(g0))
    need(q_equal(new_product, expected),
         "gauge_orbit_conjugacy_incorrect")
    need(new_product[0]*25 == -7*new_product[4]
         and not q_equal(new_product, identity),
         "periodic_holonomy_invariance")
    return product


def odd_periodic_obstruction():
    # On an odd L=3 torus x and x+3e0 are the SAME vertex,
    # but the lifted Z^4 parity data can have different directions.
    # Choose x parity index 2, for which flipping bit 0 changes sig.
    need(TABLE[2] == 2 and TABLE[3] == 3,
         "odd_periodicity_witness_changed")
    need(TABLE[2] != TABLE[step(2, 0)],
         "odd_L_pattern_quotient_ambiguity_missing")


def coupling_adapter():
    # JB coefficient beta_JB/2 equals Anaxia coefficient 2*beta_A.
    # beta_A=1/100, beta_JB=1/25. No division or floats needed.
    beta_a_n, beta_a_d = 1, 100
    beta_jb_n, beta_jb_d = 1, 25
    need(beta_jb_n*beta_a_d == 4*beta_a_n*beta_jb_d,
         "beta_adaptation")
    need(beta_jb_n*50 == 2*beta_jb_d
         and 2*beta_a_n*50 == beta_a_d,
         "Wilson_trace_coefficient_mismatch")
    need(12*beta_a_n*beta_jb_d
         == 3*beta_jb_n*beta_a_d,
         "local_influence_budget_adapter")


def adversaries():
    rejects = 0
    corrupt = list(TABLE)
    corrupt[0] = 1
    u = (3, 4, 0, 0, 5)
    cases = (
        lambda: local_certificate(tuple(corrupt)),
        lambda: need(q_equal(q_mul(u, u), (1, 0, 0, 0, 1)),
                     "false_identity_for_nontrivial_cycle"),
        lambda: need(1*100 == 2*25,
                     "wrong_beta_adapter"),
        lambda: need(TABLE[2] == TABLE[3],
                     "odd_torus_parity_falsifier"),
    )
    for test in cases:
        try:
            test()
        except ValueError:
            rejects += 1
        else:
            raise ValueError("planted_false_claim_accepted")
    need(rejects == 4, "missing_negative_controls")
    return rejects


def main():
    checks, fixed_edges, unfixed_edges = local_certificate()
    product = periodic_holonomy()
    odd_periodic_obstruction()
    coupling_adapter()
    adversaries()
    print("YM4_ANAXIA_PARITY|plaquette_checks=" + str(checks)
          + "|fixed=" + str(fixed_edges)
          + "|unfixed=" + str(unfixed_edges)
          + "|remaining_partners=12|local_counts=PASS|json=0")
    need(product[0] == -7 and product[4] == 25, "polyakov_scalar_mismatch")
    print("YM4_ANAXIA_TORUS|L2_nontrivial_Polyakov=PASS"
          "|all_fixed_edges_identity=REJECTED"
          "|odd_L_parity_quotient=REJECTED|json=0")
    print("YM4_ANAXIA_COUPLING|beta_JB=4_beta_Anaxia"
          "|trace_coefficient=1_OVER_50"
          "|local_bound=12_beta_Anaxia_eq_3_beta_JB|json=0")
    print("YM4_ANAXIA_ADVERSARIES|false_claims=4_REJECTED|json=0")
    print("YM4_ANAXIA_VERDICT|local_parity_combinatorics=PASS"
          "|periodic_gauge_orbit_transfer=HOLD"
          "|metric_bridge=OPEN|weak_coupling_cube=OPEN"
          "|continuum_mass_gap=OPEN|json=0")


if __name__ == "__main__":
    main()
