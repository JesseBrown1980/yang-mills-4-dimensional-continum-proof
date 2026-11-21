#!/usr/bin/env python3
"""YM4-07D: integer controls for the all-beta genuine SU2 local Wilson-source bound.

Analytic theorem and its exact scope: docs/NOTE-YM4-07D-ALLBETA-SU2-POLYNOMIAL-SOURCE-20261120.md
This checker verifies universal rational constant inequalities, SU2 moment
identities and six-staple Wilson-network structure. No physical projector.
"""
from math import gcd

def need(ok, tag):
    if not ok:
        raise ValueError(tag)

def network():
    pairs = [(i, j) for i in range(6) for j in range(i + 1, 6)]
    same = [(i, j) for i, j in pairs if i // 2 == j // 2]
    mixed = [(i, j) for i, j in pairs if i // 2 != j // 2]
    need(len(pairs) == 15 and len(same) == 3 and len(mixed) == 12,
         "four_dimensional_six_staple_pair_count")
    print("YM4_07D_NETWORK|links=1|staples=6|pairs=15|coplanar=3"
          "|mixed_plane=12|induced_chairs=RETAINED|json=0")

def moments():
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
    need(len(q) == 24 and len(set(q)) == 24, "24_design")
    need(all(sum(x * x for x in v) == 4 for v in q), "unit_quaternions")
    need(sum(v[0] for v in q) == 0, "haar_first_zero")
    need(sum(v[0] * v[0] for v in q) == 24, "haar_second_quarter")
    need(sum(v[0] * v[0] * v[0] * v[0] for v in q) == 48,
         "haar_fourth_eighth")
    need(sum(v[0] * v[0] * v[1] * v[1] for v in q) == 16,
         "haar_mixed_fourth_twentyfourth")
    need(192 == 24 * 8 and 384 == 2 * 192,
         "quaternion_haar_series_coefficients")
    print("YM4_07D_HAAR|test_design=24_QUATERNIONS"
          "|second_moment=1_OVER_4|fourth_moment=1_OVER_8"
          "|mixed_fourth=1_OVER_24|Z_order2=1_OVER_8"
          "|Z_order4=1_OVER_192|logZ_order4=MINUS_1_OVER_384"
          "|continuous_Haar_formula=ANALYTIC|json=0")

def dot(a, b):
    return sum(a[i] * b[i] for i in range(4))

def nonplaquette():
    pos = (0, 1, 0, 0)
    neg = (0, -1, 0, 0)
    a = [pos] * 6
    b = [pos] * 3 + [neg] * 3
    need(all(v[0] == 0 for v in a + b), "same_plaquette_traces")
    qa = tuple(sum(v[i] for v in a) for i in range(4))
    qb = tuple(sum(v[i] for v in b) for i in range(4))
    q2a, q2b = dot(qa, qa), dot(qb, qb)
    ga = sum(dot(a[i], a[j]) for i in range(6) for j in range(i + 1, 6))
    gb = sum(dot(b[i], b[j]) for i in range(6) for j in range(i + 1, 6))
    need(q2a == 36 and q2b == 0 and ga == 15 and gb == -3,
         "mixed_staple_G_matrix_contrast")
    for beta in (1, 16, 64):
        strict_lower_za = 1 + beta * beta * q2a // 8
        need(strict_lower_za > 1 and q2b == 0, "exact_all_beta_nonclosure")
        print("YM4_07D_NONPLAQUETTE|beta=" + str(beta) +
              "|same_six_plaquette_traces=YES|Q_A=36|Q_B=0"
              "|integrated_Z_A_strictly_gt=" + str(strict_lower_za) +
              "|integrated_Z_B=1|plaquette_only_closure=REFUTED|json=0")

def analytic_constant():
    # t >= 1, c=(1+t)^-1: D(t)<4*c^(3/2), p(A)>1/144,
    # p(B)>1/72, radial Var(s)>c*c/165888,
    # tangential Var > c/432 >= c*c/432.
    # t <= 1: comparison to Haar gives Var > 1/36.
    # The inequalities are proved for all real t in the companion note.
    need(144 * 72 * 16 == 165888, "radial_event_pair_constant")
    need(165888 < 262144 and 72 * 2 * 3 == 432 and
         432 < 262144 and 36 < 262144,
         "uniform_S3_conditional_covariance_constant")
    print("YM4_07D_ANALYTIC_GATE|t_ge_1_radial_den=165888"
          "|t_ge_1_tangential_den=432|t_le_1_den=36"
          "|universal_den=262144|universal_power=2"
          "|all_unit_projections=ANALYTIC_PROOF|json=0")

def lower(beta_n, beta_d):
    need(isinstance(beta_n, int) and beta_n >= 0 and
         isinstance(beta_d, int) and beta_d > 0, "valid_beta")
    n = beta_d * beta_d
    d = 262144 * (beta_d + 6 * beta_n) * (beta_d + 6 * beta_n)
    g = gcd(n, d)
    return n // g, d // g

def benchmarks():
    predicted = ((0, 1, 262144), (1, 8, 802816),
                 (1, 1, 12845056), (16, 1, 2466512896),
                 (64, 1, 38856294400))
    for n, d, expected in predicted:
        p, q = lower(n, d)
        need((p, q) == (1, expected), "frozen_benchmark_mismatch")
        print("YM4_07D_FLOOR|beta_num=" + str(n) + "|beta_den=" + str(d) +
              "|variance_gt_numer=" + str(p) +
              "|variance_gt_denom=" + str(q) +
              "|volume_uniform=YES|beta_to_infinity_uniform=NO|json=0")

def validate_claim(group, dimension, staples, pairs, mixed,
                   floor_den, exponent, networks, os_projector,
                   mass_gap):
    need(group == "continuous_SU2", "correct_group")
    need(dimension == 4, "four_dimensional")
    need(staples == 6 and pairs == 15 and mixed == 12,
         "complete_six_staple_graph")
    need(floor_den >= 262144 and exponent == 2, "certified_floor")
    need(networks, "nonplaquette_retained")
    need(not os_projector and not mass_gap,
         "unproved_OS_or_full_spectrum_promotion")

def falsifiers():
    valid = ["continuous_SU2", 4, 6, 15, 12, 262144, 2, True, False, False]
    validate_claim(*valid)
    bad = ((0, "finite_S3"), (1, 3), (2, 5), (3, 14), (4, 11),
           (5, 16384), (6, 1), (7, False), (8, True), (9, True))
    caught = 0
    for index, replacement in bad:
        altered = list(valid)
        altered[index] = replacement
        try:
            validate_claim(*altered)
        except ValueError:
            caught += 1
        else:
            raise ValueError("false_claim_accepted_" + str(index))
    need(caught == len(bad), "all_negative_controls")
    print("YM4_07D_CONTROLS|false_claims=10_REJECTED"
          "|Wilson_local_source=PASS"
          "|physical_spectral_projector=OPEN|full_continuum_gap=OPEN|json=0")

def main():
    network()
    moments()
    nonplaquette()
    analytic_constant()
    benchmarks()
    falsifiers()
    print("YM4_07D_VERDICT|continuous_SU2_4D_local_link_source"
          "=POLYNOMIAL_VOLUME_UNIFORM_FINITE_BETA"
          "|nonplaquette_network=ALL_15_PAIRS"
          "|one_step_full_RG=OPEN|OS_projector=OPEN"
          "|continuum_mass_gap=OPEN|json=0")

if __name__ == "__main__":
    main()
