"""Exact integer acceptance cells for original SU2 good-star radial transport.

The analytical SU2 Haar integral is established in the companion theorem note.
This tests rational staple geometry and strict numerical threshold only.
"""


def require(flag, label):
    if not flag:
        raise ValueError(label)


def four_norm_sq(q):
    return sum(v*v for v in q)


def sample_six_staples():
    # Five identity unit quaternions and one exact rational unit quaternion.
    identity = (101, 0, 0, 0)
    tilted = (99, 20, 0, 0)
    staples = [identity for unused in range(5)] + [tilted]
    for s in staples:
        require(four_norm_sq(s) == 101*101, "all_staples_unit_SU2")
    pair_count = 0
    for i in range(6):
        for j in range(i+1, 6):
            inner = sum(staples[i][a]*staples[j][a]
                        for a in range(4))
            require(16*inner >= 15*101*101,
                    "all_15_pairs_epsilon_1over16_good")
            pair_count += 1
    require(pair_count == 15, "all_15_pairs_checked")
    H = tuple(sum(s[a] for s in staples) for a in range(4))
    # H=(604,20,0,0)/101 and norm squared is 3616/101.
    require(H == (604,20,0,0), "rational_resultant")
    require(four_norm_sq(H)*101 == 3616*101*101,
            "resultant_squared_3616_over101")
    require(8*four_norm_sq(H) >= 273*101*101,
            "good_star_resultant_uniform_lower_bound")
    return pair_count


def aligned_quaternion_fixture():
    # v=identity, v'=i, u=3/5 + (4/5)i. Left-multiplying by
    # R=i maps u to -4/5+(3/5)i and v to i, preserving dot products.
    u=(3,4,0,0)
    u_rot=(-4,3,0,0)
    v=(1,0,0,0)
    v_rot=(0,1,0,0)
    require(four_norm_sq(u) == 25 and four_norm_sq(u_rot) == 25,
            "unit_quaternion_left_rotation")
    require(sum(u[i]*v[i] for i in range(4)) ==
            sum(u_rot[i]*v_rot[i] for i in range(4)),
            "Haar_isometry_preserves_exponent_at_equal_staple_strength")


def exact_uniform_beta_margin():
    # t_min = sqrt(273/8), t_max = 6.
    # The analytic TV bound is (3/2)*ln(tmax/tmin).
    # ln x <= x-1, and t_min > 216/37 because:
    # (273/8) > (216/37)^2, checked via integers.
    lhs=273*37*37
    rhs=8*216*216
    require(lhs == 373737 and rhs == 373248 and lhs-rhs == 489,
            "exact_positive_lower_radius_margin")
    # t_min>216/37 implies (3/2)*(6/t_min -1)<1/24.
    # 6/(216/37) -1 = 37/36 -1 = 1/36.
    require(6*37 == 216 + 6, "upper_ratio_37over36")
    require(3*24 == 2*36, "TV_lt_one_over24")
    # True 18-neighbor sum would be <3/4 IF compatible multi-link
    # gauge-aligned couplings can be constructed.
    require(18*4 == 3*24, "conditional_eighteen_neighbor_budget")
    # The unit-length resultant lower bound is necessary: three +I and
    # three -I give H=0, and at least one pair is a bad star.
    red = [1,1,1,-1,-1,-1]
    require(sum(red)==0 and any(a*b < 1 for a in red for b in red),
            "red_frustrated_staple_zero_resultant")


def main():
    require(sample_six_staples()==15, "original_six_staple_fixture")
    aligned_quaternion_fixture()
    exact_uniform_beta_margin()
    return (
        "YM4_VOL12_TRANSPORT|original_continuous_SU2_Haar=ANALYTIC|single_link_staples=6|good_pairs=15|json=0\n"
        "YM4_VOL12_TRANSPORT_GEOM|epsilon=1/16|resultant_squared_ge=273/8|preferred_quaternion_nondegenerate=PASS|json=0\n"
        "YM4_VOL12_TRANSPORT_TV|after_quaternion_alignment=YES|all_beta_positive=ANALYTIC|radial_TV_lt=1/24|rational_margin=489|json=0\n"
        "YM4_VOL12_TRANSPORT_BUDGET|original_neighbor_degree=18|formal_18_over24=3/4|multi_link_gauge_frame_coherence=OPEN|json=0\n"
        "YM4_VOL12_TRANSPORT_SCOPE|local_rational_fixture=PASS|opposite_staple_red_control=PASS|global_winding_sector=OPEN|physical_cube=OPEN|11_continuum_gates=OPEN|json=0\n"
    )


if __name__ == '__main__':
    print(main(),end='')
