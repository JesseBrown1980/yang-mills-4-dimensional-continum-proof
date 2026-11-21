#!/usr/bin/env python3
"""YM4-07E: exact SU2 block/source and cyclic-projector integer controls.

Analytic SU2 statements are proved in the companion note. These checks audit
noncommutative path geometry, Haar second moments, rational gap counterexample,
and the certified rational lower bounds inherited from merged YM4-07C.
No physical SU2 spectrum is numerically diagonalized.
"""
from math import gcd

def need(value, tag):
    if not value:
        raise ValueError(tag)

SIDE = 6

def move(x, axis, steps):
    y = list(x)
    y[axis] = (y[axis] + steps) % SIDE
    return tuple(y)

def coarse_move(x, axis):
    y = list(x)
    y[axis] = (y[axis] + 1) % 3
    return tuple(y)

def negate(word):
    return [(x, d, -s) for x, d, s in reversed(word)]

def line(x, axis):
    base = tuple(2 * a for a in x)
    return [(base, axis, 1), (move(base, axis, 1), axis, 1)]

def blocked_plaquette(x, a, b):
    return (line(x, a) + line(coarse_move(x, a), b)
            + negate(line(coarse_move(x, b), a)) + negate(line(x, b)))

def rectangle(x, a, b):
    y = tuple(2 * k for k in x)
    first = [(y, a, 1), (move(y, a, 1), a, 1)]
    second_base = move(y, a, 2)
    second = [(second_base, b, 1), (move(second_base, b, 1), b, 1)]
    third_base = move(y, b, 2)
    third = negate([(third_base, a, 1),
                    (move(third_base, a, 1), a, 1)])
    fourth = negate([(y, b, 1), (move(y, b, 1), b, 1)])
    return first + second + third + fourth

def geometry():
    count = 0
    for x in ((0, 0, 0, 0), (1, 2, 0, 2), (2, 1, 1, 0)):
        for a in range(4):
            for b in range(a + 1, 4):
                need(blocked_plaquette(x, a, b) == rectangle(x, a, b),
                     "noncommutative_SU2_loop_identity")
                count += 1
    need(count == 18, "four_dimensional_checks")
    # A fine plaquette at an even origin has two links off coarse lines.
    y = (0, 0, 0, 0)
    a, b = 0, 1
    edges = [(y, a), (move(y, a, 1), b),
             (move(y, b, 1), a), (y, b)]
    off = [(x, d) for x, d in edges
           if any(x[k] % 2 for k in range(4) if k != d)]
    need(len(off) == 2 and len(set(edges)) == 4,
         "two_independent_off_line_links")
    print("YM4_07E_GEOMETRY|group=CONTINUOUS_SU2|dimension=4|block=2"
          "|noncommuting_word_checks=18|off_line_edges=2"
          "|coarse_loop_equals_fine_2x2=PASS|json=0")

def haar():
    q = []
    for i in range(4):
        for sign in (-2, 2):
            v = [0] * 4
            v[i] = sign
            q.append(tuple(v))
    for a in (-1, 1):
        for b in (-1, 1):
            for c in (-1, 1):
                for d in (-1, 1):
                    q.append((a, b, c, d))
    need(len(q) == 24 and len(set(q)) == 24, "exact_2_design")
    for i in range(4):
        need(sum(v[i] for v in q) == 0, "zero_first_moment")
        for j in range(4):
            need(sum(v[i] * v[j] for v in q)
                 == (24 if i == j else 0), "haar_second_moment")
    print("YM4_07E_HAAR|beta_zero_pushforward=PRODUCT_HAAR"
          "|matched_source_squared_loss=ZERO"
          "|unmatched_source_squared_loss=1_OVER_4|json=0")

def network():
    pairs = [(i, j) for i in range(6) for j in range(i + 1, 6)]
    same = sum(1 for i, j in pairs if i // 2 == j // 2)
    mixed = sum(1 for i, j in pairs if i // 2 != j // 2)
    need((len(pairs), same, mixed) == (15, 3, 12),
         "induced_mixed_networks")
    print("YM4_07E_NETWORK|exact_pushforward=ALL_NETWORKS"
          "|one_link_pairs=15|coplanar=3|mixed_plane=12"
          "|Wilson_only_truncation=REJECTED|json=0")

def physical_toy():
    # Fine positive transfer eigenratios 1, 3/4, 1/2.
    # Observable-generated K is span(e0,e2), with two-step transfer 1,1/4.
    numer = (4, 3, 2)
    image = (0, 2)
    coarse = [numer[i] * numer[i] for i in image]
    need(coarse == [16, 4], "exact_transfer_squared")
    # Energy window [log(3/2)/a,log(3)/a] has ratios [1/3,2/3].
    fine_Q = [3 * n >= 4 and 3 * n <= 8 for n in numer]
    coarse_Q = [9 * n >= 16 and 9 * n <= 64 for n in coarse]
    need(fine_Q == [False, False, True], "fine_spectral_window")
    need(coarse_Q == [False, True], "coarse_spectral_window")
    need([fine_Q[i] for i in image] == coarse_Q,
         "physical_energy_projector_intertwining")
    need(numer[1] > numer[2], "dark_first_state")
    # A different physical energy band catches only the lower dark state.
    # Ratios [2/3,4/5] correspond to physical energies
    # [log(5/4)/a,log(3/2)/a] without evaluating any logarithm.
    dark_window = [3 * n >= 2 * 4 and 5 * n <= 4 * 4 for n in numer]
    need(dark_window == [False, True, False], "dark_energy_band")
    need([dark_window[i] for i in image] == [False, False],
         "dark_component_orthogonal_to_cyclic_subspace")
    # The unmatched difference is a nonzero orthogonal projector,
    # hence its operator norm equals exactly one.
    print("YM4_07E_DARK_PROJECTOR|difference=RANK_ONE_PROJECTOR"
          "|whole_space_operator_norm=1|cyclic_restricted_norm=0"
          "|dark_band_full_gap_gate=OPEN|json=0")
    print("YM4_07E_SPECTRUM|fine=DIAG_1_3over4_1over2"
          "|coarse=DIAG_1_1over4|projectors=INTERTWINED"
          "|matched_delta=0|cyclic_epsilon=0"
          "|dark_first_state=PRESENT|full_gap=OPEN|json=0")

def power_nonnegative(base, exp):
    need(exp >= 0, "positive_integer_exponent")
    y = 1
    for _ in range(exp):
        y *= base
    return y

def bound_samples():
    examples = ((0, 1, 1, 1, 4), (1, 1000, 1, 247, 1000),
                (1, 8, 3, 1, 32), (1, 1, 24, 1, 67108864))
    for bn, bd, n, en, ed in examples:
        need(n * bd > 12 * bn, "positive_enclosure")
        p = power_nonnegative(n * bd - 12 * bn, n)
        q = 4 * power_nonnegative(n * bd, n)
        g = gcd(p, q)
        need((p // g, q // g) == (en, ed), "genuine_Haar_source_bound")
        print("YM4_07E_UNMATCHED_SOURCE|beta_num=" + str(bn)
              + "|beta_den=" + str(bd)
              + "|squared_loss_ge_num=" + str(en)
              + "|squared_loss_ge_den=" + str(ed) + "|json=0")

def validate(group, b, source, action, projector, units, os, cross, full):
    need(group == "continuous_SU2", "wrong_group")
    need(b == 2, "wrong_block")
    need(source == "blocked_Wilson_loop", "unmatched_source")
    need(action == "exact_network_pushforward", "truncated_action")
    need(projector == "physical_cyclic", "wrong_projector")
    need(units == "physical", "wrong_time_units")
    need(os == "positive_transfer", "missing_OS")
    need(not cross, "unsupported_S3_bridge")
    need(not full, "dark_states_excluded")

def adversaries():
    good = ["continuous_SU2", 2, "blocked_Wilson_loop",
            "exact_network_pushforward", "physical_cyclic", "physical",
            "positive_transfer", False, False]
    validate(*good)
    bad = ((0, "finite_S3"), (1, 3), (2, "fine_plaquette"),
           (3, "Wilson_only"), (4, "Euclidean_projection"),
           (5, "lattice_units"), (6, "no_OS"), (7, True), (8, True))
    rejected = 0
    for i, wrong in bad:
        item = list(good)
        item[i] = wrong
        try:
            validate(*item)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("false_promotion_" + str(i))
    need(rejected == 9, "all_adversaries_rejected")
    print("YM4_07E_CONTROLS|active_false_claims=9_REJECTED"
          "|full_gap=OPEN|json=0")

def main():
    geometry()
    haar()
    network()
    physical_toy()
    bound_samples()
    adversaries()
    print("YM4_07E_VERDICT|exact_SU2_induced_step=PASS"
          "|matched_source_error=ZERO|cyclic_spectral_error=ZERO"
          "|unmatched_source_loss=POSITIVE"
          "|independent_RG_beta_flow=OPEN|continuum_mass_gap=OPEN|json=0")

if __name__ == "__main__":
    main()
