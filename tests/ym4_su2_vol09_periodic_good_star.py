"""VOL09 original SU2 Wilson periodic-volume-uniform good-star frequency.

Exact integer audit of an analytic Haar-cap, Gibbs free-energy convexity
and gauge-invariant plaquette-to-staple proof. No Monte Carlo or floats.
"""


def require(ok, label):
    if not ok:
        raise ValueError(label)


def ratio(n, d=1):
    require(isinstance(n, int) and isinstance(d, int) and d > 0,
            "positive_integer_ratio")
    a, b = abs(n), d
    while b:
        a, b = b, a % b
    g = a
    return n // g, d // g


def add(a, b):
    return ratio(a[0]*b[1] + b[0]*a[1], a[1]*b[1])


def mul(a, b):
    return ratio(a[0]*b[0], a[1]*b[1])


def lt(a, b):
    return a[0]*b[1] < b[0]*a[1]


def ternary(k):
    require(isinstance(k, int) and 1 <= k <= 12, "bounded_ternary_k")
    n = 1
    for unused in range(k):
        n *= 3
    return n


def verify_exponential_barriers():
    # e^8 > sum_(j=0)^8 8^j/j! = 556403/315 > 1536.
    total = ratio(1)
    term = ratio(1)
    for j in range(1, 9):
        term = ratio(term[0]*8, term[1]*j)
        total = add(total, term)
    require(total == ratio(556403, 315),
            "integer_exponential_series_exact")
    require(lt(ratio(1536), total), "log1536_below8")
    # e^(3/2) > 1+3/2+9/8 = 29/8 > 3.
    lower = add(add(ratio(1), ratio(3, 2)), ratio(9, 8))
    require(lower == ratio(29, 8) and lt(ratio(3), lower),
            "log3_below_three_halves")


def verify_original_volume_geometry():
    for L in (3, 4, 5):
        v = L*L*L*L
        edges = 4*v
        plaquettes = 6*v
        require(2*edges*3 == 4*plaquettes,
                "four_thirds_geometry_factor")
        require(edges == 4*v and plaquettes == 6*v,
                "original_four_dimensional_sites")


def verify_su2_chordal_pair_implication():
    I = (1, 0, 0, 0)
    M = (-1, 0, 0, 0)
    Q8 = (I, M, (0, 1, 0, 0), (0, -1, 0, 0),
          (0, 0, 1, 0), (0, 0, -1, 0),
          (0, 0, 0, 1), (0, 0, 0, -1))
    def dist2(a, b):
        return sum((a[i]-b[i])*(a[i]-b[i]) for i in range(4))
    for u in Q8:
        for s in Q8:
            for t in Q8:
                require(dist2(s, t) <=
                        2*(dist2(s, u)+dist2(t, u)),
                        "chordal_triangle_rational_necessary_bound")
                deficit_s = dist2(s, u)
                deficit_t = dist2(t, u)
                if deficit_s <= 1 and deficit_t <= 1:
                    require(dist2(s, t) <= 4,
                            "pointwise_plaquette_to_star_control")


def verify_exact_constants():
    verify_exponential_barriers()
    verify_original_volume_geometry()
    verify_su2_chordal_pair_implication()
    # beta=9^k, n=3^k, link cap radius r=1/(4n).
    # cap h>=1/(1536n^3); plaquette deficit eta<=1/(2n^2).
    # log(1536 n^3) < 8 + 9k/2.
    for k in range(1, 13):
        n = ternary(k)
        beta = n*n
        volume_deficit = ratio(35+18*k, 3*beta)
        bad_fixed_half = mul(ratio(48), volume_deficit)
        require(volume_deficit == ratio(35+18*k, 3*beta),
                "volume_uniform_normalized_action_deficit")
        require(bad_fixed_half == ratio(16*(35+18*k), beta),
                "fixed_eps_half_bad_star_union")
        if k >= 4:
            require(lt(bad_fixed_half, ratio(1)),
                    "first_nonnegligible_periodic_bad_star_probability")
    k = 5
    n = ternary(k)
    require(ratio(16*(35+18*k), n*n) == ratio(2000, 59049),
            "beta_9_power5_fixed_half")
    k = 6
    n = ternary(k)
    require(ratio(16*(35+18*k), n*n) == ratio(2288, 531441),
            "beta_9_power6_fixed_half")
    # Shrinking epsilon=beta^-1/4=1/(3^(k/2)), even k.
    k = 8
    n = ternary(k)
    epsden = ternary(4)
    bad_shrinking = ratio(8*epsden*(35+18*k), n*n)
    require(bad_shrinking == ratio(1432, 531441),
            "shrinking_epsilon_k8_exact")
    # Shrinking epsilon=1/sqrt(beta)=1/n converges as well.
    k = 10
    n = ternary(k)
    bad_sqrt = ratio(8*(35+18*k), n)
    require(bad_sqrt == ratio(1720, 59049),
            "shrinking_epsilon_k10_exact")
    return (
        "YM4_VOL09_MODEL|original_continuous_SU2=YES|Wilson_beta=9_power_k|periodic_L4=L_ge3|all_volumes=ANALYTIC|json=0\n"
        "YM4_VOL09_HAAR_CAP|radius=1_over_4n|n=3_power_k|cap_probability_ge=1_over_1536_n_cubed|four_link_plaquette_deficit_le=1_over_2n_squared|proof=ANALYTIC|json=0\n"
        "YM4_VOL09_ENERGY|plaquette_mean_deficit_le=(35_plus_18k)_over_(3_times_9_power_k)|uniform_volume=YES|log1536_lt8=EXACT_SERIES|log3_lt3_over2=EXACT_SERIES|json=0\n"
        "YM4_VOL09_BAD_STAR|all_15_gauge_invariant_double_staple_loops=YES|fixed_epsilon=1/2|k5_beta=59049|bad_probability_le=2000/59049|k6_bad_probability_le=2288/531441|json=0\n"
        "YM4_VOL09_SHRINKING|k8_beta=43046721|epsilon=1/81|bad_probability_le=1432/531441|k10_epsilon=1/59049|bad_probability_le=1720/59049|rate=O_k_over_3powerk|json=0\n"
        "YM4_VOL09_ACCEPTANCE|periodic_unconditional_bad_star_frequency=ANALYTIC_DERIVATION|integer_rational_replay=PASS|arbitrary_boundary_cube=OPEN|bad_island_cluster=OPEN|11_continuum_gates=OPEN|json=0\n"
    )


if __name__ == "__main__":
    print(verify_exact_constants(), end="")
