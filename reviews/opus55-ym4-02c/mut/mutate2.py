#!/usr/bin/env python3
"""Second seat's second round of mutations: hypotheses of the theorems, mirrors, the two planes, and the half weights inside Gram rows. Standard library, integers only, json=0."""
import subprocess, sys, os, time

ROOT = sys.argv[1]
SRC = open(os.path.join(ROOT, "run", "t.py"), "rb").read().decode("utf8")
RECEIPT = open(os.path.join(ROOT, "run", "receipt.txt"), "rb").read()
M = [
    ("t4_upper_and_lower_weights_dropped", "matrix = [[strip[0][a][b] * strip[1][b][b2] * strip[2][b2][a2] * strip[3][a2][a] for (a, b) in pairs] for (a2, b2) in pairs]", "matrix = [[strip[1][b][b2] * strip[3][a2][a] for (a, b) in pairs] for (a2, b2) in pairs]"),
    ("t4_mirror_slices_swapped", "matrix = [[strip[0][a][b] * strip[1][b][b2] * strip[2][b2][a2] * strip[3][a2][a] for (a, b) in pairs] for (a2, b2) in pairs]", "matrix = [[strip[0][a][b] * strip[1][b][a2] * strip[2][a2][b2] * strip[3][b2][a] for (a, b) in pairs] for (a2, b2) in pairs]"),
    ("gram_t4_mirror_slots_wrong", "reduced[(family(key[3], key[2], key[6]), family(key[0], key[1], key[4]))] += term", "reduced[(family(key[2], key[3], key[6]), family(key[0], key[1], key[4]))] += term"),
    ("gram_t4_upper_plaquette_mirror_wrong", "reduced[(family(key[3], key[2], key[6]), family(key[0], key[1], key[4]))] += term", "reduced[(family(key[3], key[2], key[4]), family(key[0], key[1], key[4]))] += term"),
    ("site_gram_weight_dropped", "        term = count\n        for k in key[2:]:\n            term *= weight[k]\n        reduced[(site_family(", "        term = count\n        reduced[(site_family("),
    ("signed_open_half_time_weight_unused", "            for k in sides:\n                term *= time_weight[k]\n", "            for k in sides:\n                term *= 1\n"),
    ("signed_open_half_mirror_is_identity", "mirrored = tuple(config[i] if s > 0 else inv[config[i]] for i, s in theta)", "mirrored = config"),
    ("family_mirror_table_key_mixed", "hist[(s0, s1, sides, table[down_key], table[up_key])] += 1", "hist[(s0, s1, sides, table[up_key], table[up_key])] += 1"),
    ("every_function_site_family_drops_lower_weight", "block = [[signed[site_class(1, a, b, inv[v2])] * signed[site_class(0, a, b, v)] for v in elements] for v2 in elements]", "block = [[signed[site_class(0, a, b, v2)] * signed[site_class(0, a, b, v)] for v in elements] for v2 in elements]"),
    ("bp_form_uses_inverse_table", "form = [[len(small_members[i]) * table[i][j] * len(small_members[j]) for j in range(size)] for i in range(size)]", "form = [[table[i][j] for j in range(size)] for i in range(size)]"),
    ("transfer_trace_drops_area", "a_values, table = transfer_matrix(small, weight, small_reps, small_members)\n        size = len(small_reps)", "a_values, table = transfer_matrix(small, weight, small_reps, small_members)\n        a_values = [1] * len(a_values)\n        size = len(small_reps)"),
    ("torus_rule_extra_d_power", "rule = padd(rule, red(c[rho] ** faces, Q8_DIM[rho] ** faces))", "rule = padd(rule, red(c[rho] ** faces, Q8_DIM[rho] ** (faces - 2)))"),
    ("cylinder_two_sides_same_plaquette", "sides = [lat.word(((k, 0, 0, 3), 0, 3)) for k in range(3)]", "sides = [lat.word(((k, 0, 0, 2), 0, 3)) for k in range(3)]"),
    ("cylinder_scan_mirror_at_t1", "w_down = line(3)", "w_down = line(1)"),
    ("exclusive_link_count_expectation", 'distinct = all(len({l for l, _ in lat.word(p)}) == 4 for p in lat.plaquettes)', 'distinct = True'),
    ("stagger_flip_counts_expectation_relaxed", "ok = (count == len(lat.plaquettes)) == (L % 2 == 0) and (commute or L % 2 == 1)", "ok = True"),
    ("quadrature_2I_class_sizes_wrong", '"2I": ("Z[phi]", PHI_RING, [(1, (2, 0)), (1, (-2, 0)), (30, (0, 0)), (20, (1, 0)), (20, (-1, 0)), (12, (0, 1)), (12, (1, -1)), (12, (-1, 1)), (12, (0, -1))], 11)', '"2I": ("Z[phi]", PHI_RING, [(1, (2, 0)), (1, (-2, 0)), (30, (0, 0)), (20, (1, 0)), (20, (-1, 0)), (12, (0, 1)), (12, (1, -1)), (12, (-1, 1)), (12, (1, 0))], 11)'),
    ("collatz_vector_not_iterated", "iterations = 24", "iterations = 0"),
]
only = set(sys.argv[2:])
outdir = os.path.join(ROOT, "mut", "out2")
os.makedirs(outdir, exist_ok=True)
for name, old, new in M:
    if only and name not in only:
        continue
    found = SRC.count(old)
    if found < 1:
        print("MUTATION|name=%s|applied=0|found=%d|json=0" % (name, found), flush=True)
        continue
    path = os.path.join(outdir, name + ".py")
    with open(path, "wb") as f:
        f.write(SRC.replace(old, new).encode("utf8"))
    t0 = time.time_ns()
    p = subprocess.run([sys.executable, "-I", "-X", "utf8", path], capture_output=True, timeout=1500)
    secs = (time.time_ns() - t0) // 10 ** 9
    out = p.stdout.replace(b"\r", b"")
    failed = [ln.split(b"check=")[1].split(b"|")[0].decode() for ln in out.splitlines() if ln.startswith(b"FAILED|")]
    tb = b"Traceback" in p.stderr
    last = p.stderr.strip().splitlines()[-1].decode("utf8", "replace")[:80] if tb else ""
    same = out == RECEIPT
    a, b = out.splitlines(), RECEIPT.splitlines()
    ndiff = sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))
    verdict = "SURVIVES_ALL" if p.returncode == 0 and same else ("SURVIVES_CHECKS_CMP_CATCHES" if p.returncode == 0 else ("CAUGHT_CRASH" if tb else "CAUGHT_NAMED"))
    print("MUTATION|name=%s|verdict=%s|exit=%d|named_failures=%d|first=%s|rows_differ=%d|crash=%s|secs=%d|json=0" % (name, verdict, p.returncode, len(failed), ",".join(failed[:3]), ndiff, last, secs), flush=True)
