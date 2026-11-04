#!/usr/bin/env python3
"""Recheck at c32087a: the second seat's mutants ported to the new script, and new mutants on the second-round rows. Each is one exact text replacement in a private copy. Standard library, integers only, json=0.
usage = mut3.py ROOT WORKERS [names...]"""
import concurrent.futures
import os
import subprocess
import sys
import time

ROOT = sys.argv[1]
WORKERS = int(sys.argv[2])
ONLY = set(sys.argv[3:])
SRC = open(os.path.join(ROOT, "run", "t.py"), "rb").read().decode("utf8")
RECEIPT = open(os.path.join(ROOT, "run", "receipt.txt"), "rb").read()
WORD_RET = "return (((x, mu), 1), ((self.shift(x, mu), nu), 1), ((self.shift(x, nu), mu), third), ((x, nu), fourth))"
LINKT = 'return (x[:-1] + (self.t(x[-1] + 1),), mu), (1 if SABOTAGE in ("no_inverse_on_time_links", "no_inverse_in_gram") else -1)'
IMAGE = "return tuple(mult[mult[g[s]][u]][inv[g[r]]] for u, (s, r) in zip(config, self.ends))"
T4M = "matrix = [[strip[0][a][b] * strip[1][b][b2] * strip[2][b2][a2] * strip[3][a2][a] for (a, b) in pairs] for (a2, b2) in pairs]"
T4F = "reduced[(family(key[3], key[2], key[6]), family(key[0], key[1], key[4]))] += term"
SITEB = "block = [[signed[site_class(1, a, b, inv[v2])] * signed[site_class(0, a, b, v)] for v in elements] for v2 in elements]"
OLD = [
    ("site_plane_shift_t_to_1-t", 'self.c = 0 if kind == "site" else -1', 'self.c = 1 if kind == "site" else -1'),
    ("link_plane_shift_t_to_-3-t", 'self.c = 0 if kind == "site" else -1', 'self.c = 0 if kind == "site" else -3'),
    ("time_link_off_by_one", LINKT, 'return (x[:-1] + (self.t(x[-1]),), mu), (1 if SABOTAGE in ("no_inverse_on_time_links", "no_inverse_in_gram") else -1)'),
    ("time_plaquette_off_by_one", "return (x[:-1] + (self.t(x[-1] + 1),), mu, nu)", "return (x[:-1] + (self.t(x[-1]),), mu, nu)"),
    ("spatial_link_inverted", "return (x[:-1] + (self.t(x[-1]),), mu), 1", "return (x[:-1] + (self.t(x[-1]),), mu), -1"),
    ("no_inverse_full_run", LINKT, "return (x[:-1] + (self.t(x[-1] + 1),), mu), 1"),
    ("plane_moved_full_run", 'if SABOTAGE in ("wrong_plane", "wrong_plane_in_gram"):', "if True:"),
    ("no_inverse_only_part_G", "theta = [(index[R.link(l)[0]], R.link(l)[1]) for l in lat.links]", "theta = [(index[R.link(l)[0]], 1) for l in lat.links]"),
    ("word_nu_up_flipped", WORD_RET, "return (((x, mu), 1), ((self.shift(x, mu), nu), -1), ((self.shift(x, nu), mu), third), ((x, nu), fourth))"),
    ("word_mu_back_shift_wrong", WORD_RET, "return (((x, mu), 1), ((self.shift(x, mu), nu), 1), ((x, mu), third), ((x, nu), fourth))"),
    ("third_letter_full_run", 'third = 1 if SABOTAGE == "dropped_inverse_third_letter" else -1', "third = 1"),
    ("fourth_letter_full_run", 'fourth = 1 if SABOTAGE == "dropped_inverse_fourth_letter" else -1', "fourth = 1"),
    ("half_weight_one_not_half", "half = pmul((1, 2), padd(deficit(shared, a), deficit(shared, b)))", "half = pmul((1, 1), padd(deficit(shared, a), deficit(shared, b)))"),
    ("partition_site_only_t0_fixed", "side = (upper if t < m else lower) if timelike else (shared if t in (0, m) else (upper if t < m else lower))", "side = (upper if t < m else lower) if timelike else (shared if t in (0,) else (upper if t < m else lower))"),
    ("site_gram_left_uses_upper_plaquettes", "ia, ib, ja, jb = slot[pa], slot[pb], slot[R.plaquette(pa)], slot[R.plaquette(pb)]", "ia, ib, ja, jb = slot[pa], slot[pb], slot[pa], slot[pb]"),
    ("link_gram_same_slice_both_sides", "reduced[(key[0], key[1])] += term", "reduced[(key[0], key[0])] += term"),
    ("projector_half_the_gauge_group", "self.gauges = list(itertools.product(range(Q8.order), repeat=len(self.lat.sites)))", "self.gauges = list(itertools.product(range(Q8.order), repeat=len(self.lat.sites)))[::2]"),
    ("projector_left_action_only", IMAGE, "return tuple(mult[g[s]][u] for u, (s, r) in zip(config, self.ends))"),
    ("orbit_weight_dropped", "out[i][j] = total * n_gauge // len(orbit)", "out[i][j] = total"),
    ("kernel_table_no_inverse_equivalent_on_Q8", "return [[weight[Q8.cls[Q8.mult[a][Q8.inv[b]]]] for b in range(8)] for a in range(8)]", "return [[weight[Q8.cls[Q8.mult[a][b]]] for b in range(8)] for a in range(8)]"),
    ("psd_test_always_true", "def psd_exact(rows):\n", 'def psd_exact(rows):\n    return True, len(rows), "none"\n'),
    ("psd_ignores_negative_diagonal", "if min(m[i][i] for i in range(k, n)) < 0:", "if False:"),
    ("dim_of_2dim_char_set_to_1", "Q8_DIM = [1, 1, 1, 1, 2]", "Q8_DIM = [1, 1, 1, 1, 1]"),
    ("fixed_slice_weight_used_once", "term = count * fixed_weight[s0] * fixed_weight[s1]", "term = count * fixed_weight[s0]"),
    ("every_function_blind_check_removed", "blind = blind and kernel[(b, moved)] == kernel[(b, a)]", "blind = True"),
    ("every_function_plane_dropped", "for plane in (0, 1):\n                    subtotal = 0", "for plane in (0,):\n                    subtotal = 0"),
    ("every_site_block_mirror_no_inverse", SITEB, "block = [[signed[site_class(1, a, b, v2)] * signed[site_class(0, a, b, v)] for v in elements] for v2 in elements]"),
    ("su2_gram_formula_n_n_not_n_n1", "a, b = pmul(low[n], low[n + 1]), pmul(high[n], high[n + 1])", "a, b = pmul(low[n], low[n]), pmul(high[n], high[n])"),
    ("su2_leading_constant_wrong_derivation", "leading = series[3]", "leading = pmul((1, 128), (1, 1))"),
    ("su2_doubled_constant_typed", "doubled = pmul((2, 1), cylinder)", "doubled = (1, 128)"),
    ("enclosure_tail_dropped", "    high = padd(high, red(4, power(2, cut + 1) * math.factorial(cut + 2)))\n    e_low", "    e_low"),
    ("collatz_explicit_check_removed", "explicit = all(first[i] == a_values[i] * c0_power * scale for i in range(size))", "explicit = True"),
    ("gauge_covariance_mirror_uses_identity", "gauge2 = {x: gauge[x[:-1] + (R.t(x[-1]),)] for x in lat.sites}", "gauge2 = {x: gauge[x] for x in lat.sites}"),
    ("staggered_flip_phase_wrong", "flipped = {(x, mu): (qneg(field[(x, mu)]) if sum(x[:mu]) % 2 else field[(x, mu)]) for (x, mu) in lat.links}", "flipped = {(x, mu): (qneg(field[(x, mu)]) if sum(x[:mu + 1]) % 2 else field[(x, mu)]) for (x, mu) in lat.links}"),
    ("t4_upper_and_lower_weights_dropped", T4M, "matrix = [[strip[1][b][b2] * strip[3][a2][a] for (a, b) in pairs] for (a2, b2) in pairs]"),
    ("t4_mirror_slices_swapped", T4M, "matrix = [[strip[0][a][b] * strip[1][b][a2] * strip[2][a2][b2] * strip[3][b2][a] for (a, b) in pairs] for (a2, b2) in pairs]"),
    ("gram_t4_mirror_slots_wrong", T4F, "reduced[(family(key[2], key[3], key[6]), family(key[0], key[1], key[4]))] += term"),
    ("gram_t4_upper_plaquette_mirror_wrong", T4F, "reduced[(family(key[3], key[2], key[4]), family(key[0], key[1], key[4]))] += term"),
    ("signed_open_half_time_weight_unused", "            for k in sides:\n                term *= time_weight[k]\n", "            for k in sides:\n                term *= 1\n"),
    ("signed_open_half_mirror_is_identity", "mirrored = tuple(config[i] if s > 0 else inv[config[i]] for i, s in theta)", "mirrored = config"),
    ("family_mirror_table_key_mixed", "hist[(s0, s1, sides, table[down_key], table[up_key])] += 1", "hist[(s0, s1, sides, table[up_key], table[up_key])] += 1"),
    ("every_function_site_family_drops_lower_weight", SITEB, "block = [[signed[site_class(0, a, b, v2)] * signed[site_class(0, a, b, v)] for v in elements] for v2 in elements]"),
    ("bp_form_uses_inverse_table", "form = [[len(small_members[i]) * table[i][j] * len(small_members[j]) for j in range(size)] for i in range(size)]", "form = [[table[i][j] for j in range(size)] for i in range(size)]"),
    ("transfer_trace_drops_area", "a_values, table = transfer_matrix(small, weight, small_reps, small_members)\n        size = len(small_reps)", "a_values, table = transfer_matrix(small, weight, small_reps, small_members)\n        a_values = [1] * len(a_values)\n        size = len(small_reps)"),
    ("torus_rule_extra_d_power", "rule = padd(rule, red(power(c[rho], faces), power(Q8_DIM[rho], faces)))", "rule = padd(rule, red(power(c[rho], faces), power(Q8_DIM[rho], faces - 2)))"),
    ("cylinder_two_sides_same_plaquette", "sides = [lat.word(((k, 0, 0, 3), 0, 3)) for k in range(3)]", "sides = [lat.word(((k, 0, 0, 2), 0, 3)) for k in range(3)]"),
    ("cylinder_scan_mirror_at_t1", "w_down = line(3)", "w_down = line(1)"),
    ("exclusive_link_count_expectation", "distinct = all(len({l for l, _ in lat.word(p)}) == 4 for p in lat.plaquettes)", "distinct = True"),
    ("stagger_flip_counts_expectation_relaxed", "ok = (count == len(lat.plaquettes)) == (L % 2 == 0) and (commute or L % 2 == 1)", "ok = True"),
    ("collatz_vector_not_iterated", "iterations = 24", "iterations = 0"),
]
NEW = [
    ("moved_mirror_ignores_sign_uses_bad", "mirror = [bad[k] for k in inverse_position] if sign < 0 else bad", "mirror = bad"),
    ("moved_mirror_ignores_sign_uses_inverse", "mirror = [bad[k] for k in inverse_position] if sign < 0 else bad", "mirror = [bad[k] for k in inverse_position]"),
    ("moved_family_sign_dropped", "slots = [(1 + 4 * coordinate[v0][0] + coordinate[v1][0], coordinate[v0][1] * coordinate[v1][1]) for (v0, v1) in pairs]", "slots = [(1 + 4 * coordinate[v0][0] + coordinate[v1][0], 1) for (v0, v1) in pairs]"),
    ("moved_target_even_function", "size, target = 17, 1 + 4 * 1 + 0", "size, target = 17, 1 + 4 * 0 + 0"),
    ("moved_up_second_plaquette_dropped", "up = [ta0[v1][b0][v0] * ta1[v0][b1][v1] for (v0, v1) in pairs]", "up = [ta0[v1][b0][v0] for (v0, v1) in pairs]"),
    ("moved_bad_second_plaquette_swapped", "bad = [tb0[x1][a0][x0] * tb1[x0][a1][x1] for (x0, x1) in pairs]", "bad = [tb0[x0][a0][x1] * tb1[x1][a1][x0] for (x0, x1) in pairs]"),
    ("moved_rank_not_read", "check(\"gauge-moved site Gram\", moved and entry == (91, 128) and psd and rank >= 1)", "check(\"gauge-moved site Gram\", moved and entry == (91, 128) and psd)"),
    ("moved_guard_removed", "if not (fixed_ok and time_ok and word_ok):", "if False:"),
    ("moved_family_gauge_invariant", "moved = all(any(family_value(mu, nu, mult[i_element][v0], v1) != family_value(mu, nu, v0, v1) for (v0, v1) in pairs) for mu in range(4) for nu in range(4))", "moved = True"),
    ("sharp_block_prefactor_dropped", "return prefactor, fixed_values, [[prefactor * d * u for u in ups] for d in downs]", "return prefactor, fixed_values, [[d * u for u in ups] for d in downs]"),
    ("sharp_block_down_is_up", "            for p in lower:\n                down *= weight[word_class(Q8, lat.word(p), value)]\n", "            for p in upper:\n                down *= weight[word_class(Q8, lat.word(p), value)]\n"),
    ("sharp_block_mirror_no_inverse", "value[image] = inv[v] if sign < 0 else v", "value[image] = v"),
    ("sharp_every_block_field_true", "every_block_psd = mismatches == 0 and prefactor_negative == 0", "every_block_psd = True"),
    ("sharp_prefactor_count_one_sided", "prefactor_negative = 2 * negative_slices * positive_slices", "prefactor_negative = negative_slices * positive_slices"),
    ("sharp_mismatch_literal_no_inverse", "if cls[mult[mult[mult[a][v1]][inv[b]]][inv[v0]]] != cls[mult[mult[mult[b][inv[v1]]][inv[a]]][v0]]:", "if cls[mult[mult[mult[a][v1]][inv[b]]][inv[v0]]] != cls[mult[mult[mult[b][v1]][inv[a]]][inv[v0]]]:"),
    ("sharp_value_one_transpose", "value = a_values[i] * a_values[j] * table[i][j] * table[j][i]\n                pair = sizes[i] * sizes[j]", "value = a_values[i] * a_values[j] * table[i][j] * table[i][j]\n                pair = sizes[i] * sizes[j]"),
    ("sharp_value_area_one_slice", "value = a_values[i] * a_values[j] * table[i][j] * table[j][i]\n                pair = sizes[i] * sizes[j]", "value = a_values[i] * table[i][j] * table[j][i]\n                pair = sizes[i] * sizes[j]"),
    ("character_test_always_true", "return all(sign[group.mult[g][h]] * base == sign[g] * sign[h] for g in range(group.order) for h in range(group.order))", "return True"),
    ("character_negative_first_plaquette", "            for k in key:\n                term *= weight[k]\n            negative += count if term < 0 else 0", "            for k in key[:1]:\n                term *= weight[k]\n            negative += count if term < 0 else 0"),
    ("single_w_area_dropped", "value = a_values[i] * a_values[j] * table[i][j] * table[j][i]\n                    total += value * sizes[i] * sizes[j]", "value = table[i][j] * table[j][i]\n                    total += value * sizes[i] * sizes[j]"),
    ("negative_coefficient_T4_second_slice", "four = inertia_exact([[strip[a][b] * strip[b][b2] * strip[b2][a2] * strip[a2][a] for (a, b) in pairs] for (a2, b2) in pairs])", "four = inertia_exact([[strip[a][a2] * strip[b][b2] for (a, b) in pairs] for (a2, b2) in pairs])"),
    ("inertia_sign_logic_positive_only", "if (top > 0) == (prev > 0):\n            positive += 1", "if top > 0:\n            positive += 1"),
    ("inertia_pair_branch_returns", "            if pair is None:\n                return positive, negative, k\n", "            if True:\n                return positive, negative, k\n"),
    ("witness_rule_drops_c0", "rule = pmul(red(c[rho], Q8_DIM[rho]), (c[0], 1))", "rule = pmul(red(c[rho], Q8_DIM[rho]), (1, 1))"),
    ("witness_middle_dropped", "numerator = red(top * middle * 8 * 8, 8 ** 8)", "numerator = red(top * 8 * 8, 8 ** 4)"),
    ("open_half_no_inverse_equivalent_on_Q8", "matrix = [[plaquette(a, b, v) * strip[b][b2] * plaquette(b2, a2, inv[v2]) * strip[a2][a] for (a, b, v) in triples] for (a2, b2, v2) in triples]", "matrix = [[plaquette(a, b, v) * strip[b][b2] * plaquette(b2, a2, v2) * strip[a2][a] for (a, b, v) in triples] for (a2, b2, v2) in triples]"),
    ("open_half_second_plaquette_is_first", "matrix = [[plaquette(a, b, v) * strip[b][b2] * plaquette(b2, a2, inv[v2]) * strip[a2][a] for (a, b, v) in triples] for (a2, b2, v2) in triples]", "matrix = [[plaquette(a, b, v) * strip[b][b2] * strip[b2][a2] * strip[a2][a] for (a, b, v) in triples] for (a2, b2, v2) in triples]"),
    ("two_t_control_mirror_no_inverse", "h = [asymmetric[cls[mult[mult[mult[b][inv[v]]][inv[a]]][v]]] for v in elements]", "h = [asymmetric[cls[mult[mult[mult[b][v]][inv[a]]][inv[v]]]] for v in elements]"),
    ("two_t_link_one_plane", "matrix = [[strip[a][b] * strip[b][a] for a in elements] for b in elements]\n        positive, negative, rank = inertia_exact(matrix)\n        total = sum(sum(row) for row in matrix)\n        rule = (0, 1)\n        for rho in range(7):", "matrix = [[strip[a][b] for a in elements] for b in elements]\n        positive, negative, rank = inertia_exact(matrix)\n        total = sum(sum(row) for row in matrix)\n        rule = (0, 1)\n        for rho in range(7):"),
    ("four_d_area_dropped", "left = [sizes[i] * a_values[i] for i in range(size)]", "left = [sizes[i] for i in range(size)]"),
    ("four_d_trace3_two_steps", "trace3 = red(sum(square[i][j] * m[j][i] for i in range(size) for j in range(size)), power(scale, 3))", "trace3 = red(sum(square[i][i] for i in range(size)), power(scale, 2))"),
    ("l_n_route_positive_check_removed", "positive = positive and value[0] > 0", "positive = True"),
    ("l_n_route_parity_check_removed", "odd_power = odd_power and value[0] == 0", "odd_power = True"),
    ("orientation_conjugate_wrong_site", "conjugate = conjugate and holonomy(word, gauged) == qmul(qmul(gauge[p[0]], holonomy(word, field)), qinv(gauge[p[0]]))", "conjugate = conjugate and holonomy(word, gauged) == qmul(qmul(gauge[lat.shift(p[0], p[1])], holonomy(word, field)), qinv(gauge[lat.shift(p[0], p[1])]))"),
    ("orientation_once_check_removed", "once = set(forward) == set(backward) and all(v == 1 for v in forward.values()) and all(v == 1 for v in backward.values())", "once = True"),
]


def run(item):
    name, old, new = item
    found = SRC.count(old)
    if found < 1:
        return "MUTATION|name=%s|applied=0|found=%d|json=0" % (name, found)
    outdir = os.path.join(ROOT, "mut", "out3")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, name + ".py")
    with open(path, "wb") as f:
        f.write(SRC.replace(old, new).encode("utf8"))
    t0 = time.time_ns()
    try:
        p = subprocess.run([sys.executable, "-I", "-X", "utf8", path], capture_output=True, timeout=3000)
    except subprocess.TimeoutExpired:
        return "MUTATION|name=%s|verdict=NOT_MEASURED|reason=BUDGET_3000_s|json=0" % name
    secs = (time.time_ns() - t0) // 10 ** 9
    out = p.stdout.replace(b"\r", b"")
    failed = [ln.split(b"check=")[1].split(b"|")[0].decode() for ln in out.splitlines() if ln.startswith(b"FAILED|")]
    tb = b"Traceback" in p.stderr
    last = p.stderr.strip().splitlines()[-1].decode("utf8", "replace")[:80] if tb else ""
    same = out == RECEIPT
    a, b = out.splitlines(), RECEIPT.splitlines()
    ndiff = sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))
    verdict = "SURVIVES_ALL" if p.returncode == 0 and same else ("SURVIVES_CHECKS_CMP_CATCHES" if p.returncode == 0 else ("CAUGHT_CRASH" if tb else "CAUGHT_NAMED"))
    return "MUTATION|name=%s|verdict=%s|exit=%d|named_failures=%d|checks=%s|rows_differ=%d|crash=%s|secs=%d|json=0" % (name, verdict, p.returncode, len(failed), ",".join(failed), ndiff, last, secs)


items = [m for m in OLD + NEW if not ONLY or m[0] in ONLY]
with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
    for line in pool.map(run, items):
        print(line, flush=True)
