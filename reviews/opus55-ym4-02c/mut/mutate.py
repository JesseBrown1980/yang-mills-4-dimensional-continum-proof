#!/usr/bin/env python3
"""Second seat's mutation harness for tests/test_reflection_transfer_4d.py. Standard library, integers only, json=0.
Each mutation is one exact text replacement in a private copy of the builder's script. A mutant survives when the
script exits 0 and its rows equal the receipt, or exits 0 with different rows that only the cmp step would catch."""
import subprocess, sys, os, time

ROOT = sys.argv[1]
SRC = open(os.path.join(ROOT, "run", "t.py"), "rb").read().decode("utf8")
RECEIPT = open(os.path.join(ROOT, "run", "receipt.txt"), "rb").read()
WORD = "return (((x, mu), 1), ((self.shift(x, mu), nu), 1), ((self.shift(x, nu), mu), -1), ((x, nu), -1))"
LINKT = 'return (x[:-1] + (self.t(x[-1] + 1),), mu), (1 if SABOTAGE == "no_inverse_on_time_links" else -1)'
IMAGE = "return tuple(mult[mult[g[s]][u]][inv[g[r]]] for u, (s, r) in zip(config, self.ends))"
M = [
    ("site_plane_shift_t_to_1-t", 'self.c = 0 if kind == "site" else -1', 'self.c = 1 if kind == "site" else -1'),
    ("link_plane_shift_t_to_-3-t", 'self.c = 0 if kind == "site" else -1', 'self.c = 0 if kind == "site" else -3'),
    ("time_link_off_by_one", LINKT, 'return (x[:-1] + (self.t(x[-1]),), mu), (1 if SABOTAGE == "no_inverse_on_time_links" else -1)'),
    ("time_plaquette_off_by_one", "return (x[:-1] + (self.t(x[-1] + 1),), mu, nu)", "return (x[:-1] + (self.t(x[-1]),), mu, nu)"),
    ("spatial_link_inverted", "return (x[:-1] + (self.t(x[-1]),), mu), 1", "return (x[:-1] + (self.t(x[-1]),), mu), -1"),
    ("no_inverse_full_run", LINKT, "return (x[:-1] + (self.t(x[-1] + 1),), mu), 1"),
    ("no_inverse_only_part_G", "theta = [(index[R.link(l)[0]], R.link(l)[1]) for l in lat.links]", "theta = [(index[R.link(l)[0]], 1) for l in lat.links]"),
    ("word_nu_up_flipped", WORD, "return (((x, mu), 1), ((self.shift(x, mu), nu), -1), ((self.shift(x, nu), mu), -1), ((x, nu), -1))"),
    ("word_mu_back_shift_wrong", WORD, "return (((x, mu), 1), ((self.shift(x, mu), nu), 1), ((x, mu), -1), ((x, nu), -1))"),
    ("half_weight_one_not_half", "half = pmul((1, 2), padd(deficit(shared, a), deficit(shared, b)))", "half = pmul((1, 1), padd(deficit(shared, a), deficit(shared, b)))"),
    ("partition_site_only_t0_fixed", "side = (upper if t < m else lower) if timelike else (shared if t in (0, m) else (upper if t < m else lower))", "side = (upper if t < m else lower) if timelike else (shared if t in (0,) else (upper if t < m else lower))"),
    ("partition_link_plane_moved", "side = (shared if t in (m - 1, lat.T - 1) else (upper if t < m else lower)) if timelike else (upper if t < m else lower)", "side = (shared if t in (m - 1, 0) else (upper if t < m else lower)) if timelike else (upper if t < m else lower)"),
    ("site_gram_left_uses_upper_plaquettes", "ia, ib, ja, jb = slot[pa], slot[pb], slot[R.plaquette(pa)], slot[R.plaquette(pb)]", "ia, ib, ja, jb = slot[pa], slot[pb], slot[pa], slot[pb]"),
    ("site_gram_swap_slices_on_left", "reduced[(site_family(key[0], key[1], key[ja], key[jb]), site_family(key[0], key[1], key[ia], key[ib]))] += term", "reduced[(site_family(key[1], key[0], key[ja], key[jb]), site_family(key[0], key[1], key[ia], key[ib]))] += term"),
    ("link_gram_same_slice_both_sides", "reduced[(key[0], key[1])] += term", "reduced[(key[0], key[0])] += term"),
    ("link_gram_transposed_is_equivalent", "return [[sum(v * Q8_CHI[a][w1] * Q8_CHI[b][w0] for (w0, w1), v in reduced.items()) for b in range(5)] for a in range(5)]", "return [[sum(v * Q8_CHI[b][w1] * Q8_CHI[a][w0] for (w0, w1), v in reduced.items()) for b in range(5)] for a in range(5)]"),
    ("projector_half_the_gauge_group", "self.gauges = list(itertools.product(range(Q8.order), repeat=len(self.lat.sites)))", "self.gauges = list(itertools.product(range(Q8.order), repeat=len(self.lat.sites)))[::2]"),
    ("projector_left_action_only", IMAGE, "return tuple(mult[g[s]][u] for u, (s, r) in zip(config, self.ends))"),
    ("projector_g_inverse_is_equivalent", IMAGE, "return tuple(mult[mult[inv[g[s]]][u]][g[r]] for u, (s, r) in zip(config, self.ends))"),
    ("orbit_weight_dropped", "out[i][j] = total * n_gauge // len(orbit)", "out[i][j] = total"),
    ("kernel_table_no_inverse_equivalent_on_Q8", "return [[weight[Q8.cls[Q8.mult[a][Q8.inv[b]]]] for b in range(8)] for a in range(8)]", "return [[weight[Q8.cls[Q8.mult[a][b]]] for b in range(8)] for a in range(8)]"),
    ("trace_of_ABP_kernel_no_inverse", "hist[(faces, tuple(cls[mult[config[ell]][inv[moved[ell]]]] for ell in links))] += 1", "hist[(faces, tuple(cls[mult[config[ell]][moved[ell]]] for ell in links))] += 1"),
    ("psd_test_always_true", "def psd_exact(rows):\n", 'def psd_exact(rows):\n    return True, len(rows), "none"\n'),
    ("psd_ignores_negative_diagonal", "if min(m[i][i] for i in range(k, n)) < 0:", "if False:"),
    ("dim_of_2dim_char_set_to_1", "Q8_DIM = [1, 1, 1, 1, 2]", "Q8_DIM = [1, 1, 1, 1, 1]"),
    ("fixed_slice_weight_used_once", "term = count * fixed_weight[s0] * fixed_weight[s1]", "term = count * fixed_weight[s0]"),
    ("every_function_blind_check_removed", "blind = blind and kernel[(b, moved)] == kernel[(b, a)]", "blind = True"),
    ("every_function_plane_dropped", "for plane in (0, 1):\n                    subtotal = 0", "for plane in (0,):\n                    subtotal = 0"),
    ("every_site_block_mirror_no_inverse", "block = [[signed[site_class(1, a, b, inv[v2])] * signed[site_class(0, a, b, v)] for v in elements] for v2 in elements]", "block = [[signed[site_class(1, a, b, v2)] * signed[site_class(0, a, b, v)] for v in elements] for v2 in elements]"),
    ("su2_gram_formula_n_n_not_n_n1", "a, b = pmul(low[n], low[n + 1]), pmul(high[n], high[n + 1])", "a, b = pmul(low[n], low[n]), pmul(high[n], high[n])"),
    ("su2_gram_minus_side_power_formula", "a = pmul(at_minus[n], at_minus[n + 1])", "a = pmul(at_minus[n], at_minus[n])"),
    ("su2_leading_constant_wrong_derivation", "leading = pmul((1, 2), red(1, 4 ** 3))", "leading = pmul((1, 128), (1, 1))"),
    ("enclosure_tail_dropped", "high = padd(high, red(4, 2 ** (cut + 1) * math.factorial(cut + 2)))", "high = high"),
    ("collatz_explicit_check_removed", "explicit = all(first[i] == a_values[i] * c0_power * scale for i in range(size))", "explicit = True"),
    ("gauge_covariance_mirror_uses_identity", "gauge2 = {x: gauge[x[:-1] + (R.t(x[-1]),)] for x in lat.sites}", "gauge2 = {x: gauge[x] for x in lat.sites}"),
    ("staggered_flip_phase_wrong", "flipped = {(x, mu): (qneg(field[(x, mu)]) if sum(x[:mu]) % 2 else field[(x, mu)]) for (x, mu) in lat.links}", "flipped = {(x, mu): (qneg(field[(x, mu)]) if sum(x[:mu + 1]) % 2 else field[(x, mu)]) for (x, mu) in lat.links}"),
]
only = set(sys.argv[2:])
outdir = os.path.join(ROOT, "mut", "out")
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
    p = subprocess.run([sys.executable, "-I", "-X", "utf8", path], capture_output=True, timeout=500)
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
