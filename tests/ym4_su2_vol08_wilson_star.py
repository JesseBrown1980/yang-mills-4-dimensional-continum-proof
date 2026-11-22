"""VOL08: exact original 4D continuous SU2 Wilson link-star boundary audit.

Finite Q8 tests check gauge covariance and exact rational arithmetic.
Analytic continuous SU2 Haar/gamma argument is in the companion proof note.
"""
from fractions import Fraction
from itertools import product

I = (1, 0, 0, 0)
NI = (-1, 0, 0, 0)
E1 = (0, 1, 0, 0)
E2 = (0, 0, 1, 0)
E3 = (0, 0, 0, 1)
Q8 = (I, NI, E1, tuple(-v for v in E1),
      E2, tuple(-v for v in E2), E3, tuple(-v for v in E3))


def require(ok, label):
    if not ok:
        raise ValueError(label)


def qm(a, b):
    x, y, z, w = a
    p, q, r, s = b
    return (x*p-y*q-z*r-w*s, x*q+y*p+z*s-w*r,
            x*r-y*s+z*p+w*q, x*s+y*r-z*q+w*p)


def inv(a):
    return (a[0], -a[1], -a[2], -a[3])


def dot(a, b):
    return sum(a[j]*b[j] for j in range(4))


def step(x, mu, sign, L):
    v = list(x)
    v[mu] = (v[mu] + sign) % L
    return tuple(v)


def path_value(links, path):
    v = I
    for x, mu, sense in path:
        u = links[x, mu]
        v = qm(v, u if sense == 1 else inv(u))
    return v


def staple_paths(x, mu, L):
    result = []
    for nu in range(4):
        if nu == mu:
            continue
        xm = step(x, nu, -1, L)
        result.append((
            ((step(x, mu, 1, L), nu, 1),
             (step(x, nu, 1, L), mu, -1), (x, nu, -1)),
            ((step(xm, mu, 1, L), nu, -1),
             (xm, mu, -1), (xm, nu, 1)),
        ))
    return [p for pair in result for p in pair]


def preferred(links, x, mu, L):
    return [inv(path_value(links, p)) for p in staple_paths(x, mu, L)]


def fixtures(L):
    vertices = list(product(range(L), repeat=4))
    links = {(x, mu): Q8[(sum((j+1)*x[j] for j in range(4)) + 3*mu) % 8]
             for x in vertices for mu in range(4)}
    gauge = {x: Q8[(sum((j+2)*x[j] for j in range(4)) + 1) % 8]
             for x in vertices}
    changed = {(x, mu): qm(qm(gauge[x], u),
                           inv(gauge[step(x, mu, 1, L)]))
               for (x, mu), u in links.items()}
    return links, gauge, changed


def check_gauge_covariance():
    for L in (3, 4):
        links, gauge, changed = fixtures(L)
        vertices = list(product(range(L), repeat=4))
        count = 0
        for x in vertices:
            for mu in range(4):
                paths = staple_paths(x, mu, L)
                require(len(paths) == 6 and all(len(p) == 3 for p in paths),
                        "six_triple_staples")
                require(len({(site, axis) for p in paths
                             for site, axis, direction in p}) == 18,
                        "original_distinct_4d_link_partners")
                ss = preferred(links, x, mu, L)
                ts = preferred(changed, x, mu, L)
                require(len(ss) == len(ts) == 6, "six_staples")
                for i in range(6):
                    expected = qm(qm(gauge[x], ss[i]),
                                  inv(gauge[step(x, mu, 1, L)]))
                    require(ts[i] == expected,
                            "SU2_bifundamental_staple_covariance")
                    require(dot(links[x, mu], ss[i]) ==
                            dot(changed[x, mu], ts[i]),
                            "closed_plaquette_Wilson_gauge_invariance")
                    for j in range(i):
                        require(dot(ss[i], ss[j]) == dot(ts[i], ts[j]),
                                "six_link_closed_Wilson_pair_gauge_invariance")
                count += 1
        require(count == 4 * L * L * L * L, "all_original_links_checked")
    return "L3_324_AND_L4_1024_LINKS"


def check_boundary_realizability():
    L = 3
    x = (0, 0, 0, 0)
    mu = 0
    links = {(site, axis): I for site in product(range(L), repeat=4)
             for axis in range(4)}
    aligned = preferred(links, x, mu, L)
    require(all(s == I for s in aligned), "all_aligned_original_Wilson_star")
    bad = dict(links)
    for nu in (1, 2, 3):
        v = step(x, nu, -1, L)
        bad[(step(v, mu, 1, L), nu)] = NI
    baseline = dict(links)
    for nu in (1, 2):
        v = step(x, nu, -1, L)
        baseline[(step(v, mu, 1, L), nu)] = NI
    near_star = preferred(baseline, x, mu, L)
    require(near_star == [I, NI, I, NI, I, I],
            "single_neighbor_baseline_four_plus_two_minus")
    require(tuple(sum(s[j] for s in near_star) for j in range(4)) ==
            (2, 0, 0, 0), "two_staple_resultant")
    require(sum(baseline[e] != bad[e] for e in baseline) == 1,
            "one_original_external_link_change")
    frustration = preferred(bad, x, mu, L)
    require(frustration == [I, NI, I, NI, I, NI],
            "realizable_three_plus_three_staples")
    require(tuple(sum(s[j] for s in frustration) for j in range(4)) ==
            (0, 0, 0, 0), "exact_Haar_conditional_frustrated_link")
    require(frustration[0] == aligned[0] == I,
            "gauge_invariant_test_plaquette_has_same_boundary_path")
    eps = Fraction(1, 81)
    require(any(Fraction(dot(frustration[i], frustration[j])) < (1-eps)
                for i in range(6) for j in range(i)),
            "bad_star_detected_by_physical_six_loops")
    require(dot(Q8[4], frustration[0]) == 0,
            "original_SU2_quaternion_test")
    for u in Q8:
        for s in Q8:
            require(dot(u, s) == dot(qm(NI, u), qm(NI, s)),
                    "reject_raw_link_center_flip_as_physical_observable")
    return "THREE_LOWER_STAPLES_CENTER_FLIPPED"


def ternary(k):
    require(isinstance(k, int) and 1 <= k <= 6,
            "bounded_integer_ternary_index")
    n = 1
    for unused in range(k):
        n *= 3
    return n


def rational_controls():
    beta = 81
    eps = Fraction(1, 81)
    delta = Fraction(1, 3)
    error = eps + Fraction(1, 4*beta) / (1-eps)
    prob_bad = error / delta
    require(error == Fraction(401, 25920),
            "gauge_invariant_good_sector_mean_error")
    require(prob_bad == Fraction(401, 8640),
            "good_star_plaq_bad_probability")
    require(6*prob_bad == Fraction(401, 1440),
            "six_plaquette_star_union")
    controls = []
    for k in range(1, 7):
        n = ternary(k)
        beta = n*n
        delta = Fraction(1, n)
        tv_floor = 1-delta-Fraction(1, 4*beta)/delta
        require(tv_floor == Fraction(4*n-5, 4*n),
                "Haar_TV_integer_threshold")
        require(0 < tv_floor < 1, "gauge_invariant_TV_strictly_positive")
        single_neighbor_floor = 1-delta-Fraction(3, 4*beta)/delta
        require(single_neighbor_floor == Fraction(4*n-7, 4*n),
                "single_external_link_Wilson_TV_bound")
        require(single_neighbor_floor < tv_floor,
                "same_Wilson_plaquette_comparison_consistency")
        controls.append((k, tv_floor.numerator, tv_floor.denominator,
                         single_neighbor_floor.numerator,
                         single_neighbor_floor.denominator))
    require(controls[1] == (2, 31, 36, 29, 36),
            "beta81_two_boundary_TV_bounds")
    require(controls[2] == (3, 103, 108, 101, 108),
            "beta729_two_boundary_TV_bounds")
    return controls


def certify():
    geometry = check_gauge_covariance()
    boundary = check_boundary_realizability()
    ctl = rational_controls()
    require(geometry == "L3_324_AND_L4_1024_LINKS", "stencil_replay")
    require(boundary == "THREE_LOWER_STAPLES_CENTER_FLIPPED",
            "nonflat_boundary_replay")
    require(len(ctl) == 6, "ternary_count")
    return (
        "YM4_VOL08_MODEL|gauge=continuous_SU2|action=exp_beta_halftrace_plaquettes|dimension=4|site_conditionals=original_Haar|json=0\n"
        "YM4_VOL08_GEOMETRY|L3_linkstars=324|L4_linkstars=1024|staples_per_link=6|links_per_staple=3|distinct_partners=18|Q8_subgroup_gauge_covariance=PASS|json=0\n"
        "YM4_VOL08_GOOD|gauge_invariant_test=all_15_pairwise_six_link_Wilson_traces|epsilon=1/81|beta=81|delta=1/3|mean_deficit_le=401/25920|conditional_bad_plaquette_probability_le=401/8640|six_plaquette_union_le=401/1440|json=0\n"
        "YM4_VOL08_FRUSTRATION|original_L3_Wilson_boundary=REALIZED|three_plus_three_staples=PASS|conditional_distribution=HAAR|same_gauge_invariant_plaquette_test=YES|json=0\n"
        "YM4_VOL08_TV|beta=81|delta=1/9|aligned_vs_frustrated_TV_ge=31/36|single_external_link_change_TV_ge=29/36|beta729_single_external_TV_ge=101/108|limit_beta_tends_infinity=ONE|json=0\n"
        "YM4_VOL08_ACCEPTANCE|SU2_local_star_exact_analytic=PROOF_DEPENDENCY|integer_stencil_and_rational=PASS|single_link_uniform_weak_mixing=REJECT|physical_cube_bound=OPEN|bad_block_global_weight=OPEN|11_continuum_gates=OPEN|json=0\n"
    )


if __name__ == "__main__":
    print(certify(), end="")
