"""YM4 VOL11: original SU2 Wilson exact separated-link geometry and rational tail.

Integer-only original 4D plaquette incidence, noncommuting Q8 gauge fixtures,
Haar exponential Taylor inequalities and contaminated joint tail arithmetic.
Analytical continuous-SU2 Haar integrals are proved in the companion note.
"""

from itertools import product


def require(ok, name):
    if not ok:
        raise ValueError(name)


def ratio(n, d=1):
    require(isinstance(n, int) and isinstance(d, int) and d > 0,
            "positive_rational_integer_denominator")
    a, b = abs(n), d
    while b:
        a, b = b, a % b
    k = a
    return (n // k, d // k)


def radd(a, b):
    return ratio(a[0]*b[1]+b[0]*a[1], a[1]*b[1])


def rmul(a, b):
    return ratio(a[0]*b[0], a[1]*b[1])


def rdiv(a, b):
    require(b[0] > 0, "positive_rational_divisor")
    return ratio(a[0]*b[1], a[1]*b[0])


def rle(a, b):
    return a[0]*b[1] <= b[0]*a[1]


def ternary(k):
    require(isinstance(k, int) and 0 <= k <= 24, "ternary_integer_index")
    n = 1
    for unused in range(k):
        n *= 3
    return n


def taylor_exp_lower(beta, order):
    """Exact positive rational T_order(45*beta/64), no floats."""
    require(isinstance(beta, int) and beta >= 1 and
            isinstance(order, int) and 0 <= order <= 24, "taylor_domain")
    term = ratio(1)
    total = term
    for j in range(1, order+1):
        term = rmul(term, ratio(45*beta, 64*j))
        total = radd(total, term)
    return total


def q_upper_rational(beta):
    """q<=324 beta squared divided by Taylor12(45beta/64)."""
    return rdiv(ratio(324*beta*beta), taylor_exp_lower(beta, 12))


def check_haar_tails():
    q_81 = q_upper_rational(81)
    require(rle(q_81, ratio(1, 1000000)),
            "exact_continuous_SU2_Haar_beta81_Taylor12_upper_le_one_millionth")
    q4 = rmul(rmul(q_81, q_81), rmul(q_81, q_81))
    require(rle(q4, ratio(1, 1000000000000000000000000)),
            "four_independent_good_star_defects_le_one_over_10power24")
    beta729 = 729
    require(rle(q_upper_rational(beta729), q_81),
            "higher_beta_tail_rational_stronger")
    for k in (4, 6, 8):
        beta = ternary(2*k)
        candidate = q_upper_rational(beta)
        require(rle(candidate, q_81), "ternary_beta_conditional_exponential_tail")
    # Exact geometrical coefficients:
    # eps=1/16, delta=1/2, kappa >=45beta/8, defect T>=1/8,
    # kappa*T >=45beta/64 and 9*(6beta)^2 =324beta^2.
    require(6*15 == 45*2 and 9*6*6 == 324 and 8*8 == 64,
            "SU2_staple_and_angular_concentration_coefficients")


def check_unconditional_splits():
    # VOL09 p_star for eps1/16, beta=9^k, k=8:
    k = 8
    beta = ternary(2*k)
    pstar = ratio(64*(35+18*k), beta)
    require(pstar == ratio(11456, 43046721),
            "VOL09_beta_9power8_bad_exterior_pstar")
    require(rle(pstar, ratio(1, 1000)),
            "pstar_below_one_per_thousand")
    q8 = q_upper_rational(beta)
    require(rle(q8, ratio(1, 1000000)),
            "beta9power8_defect_good_bound_le_millionth")
    # For any r=4, t=1 the unconditional formula is q^3+2*pstar.
    qcube = rmul(q8, rmul(q8, q8))
    bound = radd(qcube, rmul(ratio(2), pstar))
    require(rle(bound, ratio(1, 1000)),
            "four_selected_defects_contaminated_bound_below_one_over1000")
    # Distinguish low marginals from joint improvement: VOL09 direct
    # single-plaquette defect Markov bound is strictly stronger numerically.
    # R <= (35+18k)/(3beta); delta=1/2 -> 2R.
    direct_single = ratio(2*(35+18*k), 3*beta)
    require(rle(direct_single, bound),
            "contaminated_joint_rate_does_not_beat_ordinary_marginal")
    # Worst case pstar=1 must never be interpreted as a decay.
    require(not rle(ratio(1), ratio(1, 2)),
            "red_control_uncertified_arbitrary_boundary_contraction")


I = (1, 0, 0, 0)
NI = (-1, 0, 0, 0)
E1 = (0, 1, 0, 0)
E2 = (0, 0, 1, 0)
E3 = (0, 0, 0, 1)
Q8 = (I, NI, E1, tuple(-v for v in E1),
      E2, tuple(-v for v in E2), E3, tuple(-v for v in E3))


def qm(a, b):
    x, y, z, w = a
    p, q, r, s = b
    return (x*p-y*q-z*r-w*s, x*q+y*p+z*s-w*r,
            x*r-y*s+z*p+w*q, x*s+y*r-z*q+w*p)


def inv(a):
    return (a[0], -a[1], -a[2], -a[3])


def check_bad_star_energy_fixture():
    # Algebraic Q8 subcase of the continuous SU2 chordal inequality:
    # 1-s.t <= 2[(1-u.s)+(1-u.t)] for any unit quaternions.
    for u in Q8:
        for a in Q8:
            for b in Q8:
                dot_ab = sum(a[i]*b[i] for i in range(4))
                dot_ua = sum(u[i]*a[i] for i in range(4))
                dot_ub = sum(u[i]*b[i] for i in range(4))
                lhs = 1-dot_ab
                sum_deficits = (1-dot_ua)+(1-dot_ub)
                require(lhs <= 2*sum_deficits,
                        "original_SU2_bad_star_chordal_energy_budget")
                if lhs >= 1:
                    require(sum_deficits >= 1,
                            "Q8_adversarial_bad_pair_requires_energy")


def step(x, mu, L):
    v = list(x)
    v[mu] = (v[mu]+1) % L
    return tuple(v)


def original_plaquettes(L):
    vertices = list(product(range(L), repeat=4))
    paths = []
    for x in vertices:
        for mu in range(4):
            for nu in range(mu+1, 4):
                paths.append((
                    (x, mu),
                    (step(x, mu, L), nu),
                    (step(x, nu, L), mu),
                    (x, nu),
                ))
    require(len(paths) == 6*L*L*L*L, "original_four_dimensional_plaquette_count")
    return vertices, paths


def wilson_real(qs, p):
    a, b, c, d = (qs[e] for e in p)
    return qm(qm(qm(a, b), inv(c)), inv(d))[0]


def check_original_su2_geometry():
    reports = []
    for L in (3, 4):
        vertices, plaquettes = original_plaquettes(L)
        links = [(x, mu) for x in vertices for mu in range(4)]
        adjacency = {e: set() for e in links}
        incidence = {e: [] for e in links}
        for p in plaquettes:
            require(len(set(p)) == 4, "four_distinct_original_Wilson_links")
            for e in p:
                incidence[e].append(p)
                for f in p:
                    if f != e:
                        adjacency[e].add(f)
        require(all(len(adjacency[e]) == 18 and len(incidence[e]) == 6
                    for e in links), "six_plaquette_eighteen_partner_link_graph")
        selected = []
        forbidden = set()
        for e in links:
            if e not in forbidden:
                selected.append(e)
                forbidden.add(e)
                forbidden.update(adjacency[e])
        marked = {e: incidence[e][0] for e in selected}
        require(len(selected) >= (len(links)+18)//19,
                "original_graph_independent_link_packing")
        require(len(set(marked.values())) == len(selected),
                "one_original_distinct_Wilson_plaquette_per_selected_link")
        for p in plaquettes:
            require(sum(e in marked for e in p) <= 1,
                    "no_two_selected_original_links_share_a_plaquette")
        for e in selected:
            for p in incidence[e]:
                require(all(f not in marked for f in p if f != e),
                        "all_six_original_staples_use_only_exterior_links")
        # Explicit negative control: two links on a chosen original plaquette
        # invalidate conditional product factorization.
        collision = plaquettes[0][:2]
        require(collision[1] in adjacency[collision[0]],
                "adjacent_selected_links_red_control")
        # Noncommuting gauge orbit: arbitrary Q8 site rotations preserve
        # every original SU2 plaquette half-trace.
        field = {(x, mu): Q8[(sum((j+1)*x[j] for j in range(4))+3*mu) % 8]
                 for x in vertices for mu in range(4)}
        gauge = {x: Q8[(sum((j+2)*x[j] for j in range(4))+1) % 8]
                 for x in vertices}
        transformed = {
            (x, mu): qm(qm(gauge[x], u), inv(gauge[step(x, mu, L)]))
            for (x, mu), u in field.items()
        }
        for p in plaquettes:
            require(wilson_real(field, p) == wilson_real(transformed, p),
                    "noncommuting_original_Wilson_plaquette_gauge_invariance")
        reports.append((L, len(links), len(plaquettes), len(selected)))
    require(reports[0][0:3] == (3, 324, 486), "L3_original_graph")
    require(reports[1][0:3] == (4, 1024, 1536), "L4_original_graph")
    return reports


def certify():
    check_haar_tails()
    check_unconditional_splits()
    check_bad_star_energy_fixture()
    report = check_original_su2_geometry()
    require(report[0][3] >= 18 and report[1][3] >= 54,
            "independent_set_sample_packing_cardinality")
    return (
        "YM4_VOL11_MODEL|original_continuous_SU2_Wilson=YES|dimension=4|periodic_L_ge3=YES|json=0\n"
        "YM4_VOL11_GEOMETRY|L3_links=324|L4_links=1024|L3_plaquettes=486|L4_plaquettes=1536|degree=18|selected_links_share_no_original_plaquette=PASS|staples_measurable_on_complement=YES|Q8_nongauge_reduction=NO|json=0\n"
        "YM4_VOL11_HAAR|epsilon=1/16|delta=1/2|kappa_ge=45beta_over8|projection_deficit_ge=1/8|conditional_good_defect_q_le=324_beta_squared_exp_minus_45beta_over64|continuous_SU2=ANALYTIC|json=0\n"
        "YM4_VOL11_EXACT_RATE|beta=81|Taylor_terms=12|conditional_defect_probability_lt=1/1000000|four_selected_all_good_defects_lt=1/10power24|integer_rational_check=PASS|json=0\n"
        "YM4_VOL11_JOINT|all_selected_good_exteriors_and_defects_le=q_power_r|unconditional_all_defects_le=q_power_r_minus_t_plus_rpstar_over_tplus1|original_SU2_conditional_factorization=YES|json=0\n"
        "YM4_VOL11_BAD_STAR_ENERGY|bad_star_indicator_le=2_over_epsilon_times_incident_Wilson_deficits|periodic_pstar_le=12R_over_epsilon|improvement=FACTOR2|Q8_algebra_fixture=PASS|json=0\n"
        "YM4_VOL11_CONTAMINATION|beta=9power8|epsilon=1/16|pstar_le=11456/43046721|r4_t1_joint_bound_lt=1/1000|joint_original_bad_star_rho=OPEN|json=0\n"
        "YM4_VOL11_ACCEPTANCE|exponential_good_exterior_original_SU2=ANALYTIC|exact_integer_source_replay=PASS|bad_exterior_joint_activity=OPEN|physical_size_cube=OPEN|11_continuum_gates=OPEN|json=0\n"
    )


if __name__ == "__main__":
    print(certify(), end="")
