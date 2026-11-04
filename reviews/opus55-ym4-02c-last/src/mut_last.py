#!/usr/bin/env python3
"""Last recheck at b302549. One exact text replacement in a private copy, full run, integers only, json=0. usage = mut_last.py ROOT WORKERS"""
import concurrent.futures, os, subprocess, sys, time
ROOT = sys.argv[1]
WORKERS = int(sys.argv[2])
SRC = open(os.path.join(ROOT, "run", "t.py"), "rb").read().decode("utf8")
RECEIPT = open(os.path.join(ROOT, "run", "receipt.txt"), "rb").read()
OUT = os.path.join(ROOT, "mut", "out")
os.makedirs(OUT, exist_ok=True)
LINKT = 'return (x[:-1] + (self.t(x[-1] + 1),), mu), (1 if SABOTAGE in ("no_inverse_on_time_links", "no_inverse_in_gram") else -1)'
CASES = [
 ("no_inverse_full_run", LINKT, "return (x[:-1] + (self.t(x[-1] + 1),), mu), 1"),
 ("plane_moved_full_run", 'if SABOTAGE in ("wrong_plane", "wrong_plane_in_gram"):', "if True:"),
 ("witness_middle_dropped", "numerator = red(top * middle * 8 * 8, 8 ** 8)", "numerator = red(top * 8 * 8, 8 ** 4)"),
 ("inertia_pair_branch_returns", "            if pair is None:\n                return positive, negative, k\n", "            if True:\n                return positive, negative, k\n"),
 ("w_plus_mirror_no_inverse", "value[time_one] = inv[v] if sign < 0 else v", "value[time_one] = v"),
 ("slice_pairs_inverse_read_as_equal", "inverse_pairs += 1 if second == inv[first] else 0", "inverse_pairs += 1 if second == first else 0"),
 ("slice_pairs_center_dropped", "same_class += 1 if cls[second] in (cls[first], cls[mult[minus][first]]) else 0", "same_class += 1 if cls[second] == cls[first] else 0"),
 ("minus_w_twin_wrong", "c, twin = (-8, -3, -3, -3, -1), (8, 3, 3, 3, 1)\n    weight = q8_weight(c)\n    plaquettes", "c, twin = (-8, -3, -3, -3, -1), (8, 3, 3, 3, -1)\n    weight = q8_weight(c)\n    plaquettes"),
 ("scan_bound_not_counted", "bound_failures += 0 if convolution[0] >= power(w2[0], length) > 0 else 1", "bound_failures += 0"),
]
def one(case):
    name, old, new = case
    assert SRC.count(old) == 1, name
    path = os.path.join(OUT, name + ".py")
    with open(path, "wb") as f:
        f.write(SRC.replace(old, new).encode("utf8"))
    t0 = time.monotonic_ns()
    p = subprocess.run([sys.executable, "-I", "-X", "utf8", path], capture_output=True)
    out = p.stdout.replace(b"\r", b"")
    failed = [ln.split(b"check=")[1].split(b"|")[0].decode() for ln in out.splitlines() if ln.startswith(b"FAILED|")]
    return "MUTATION|name=%s|exit=%d|named_failures=%d|checks=%s|same_as_receipt=%d|traceback=%d|secs=%d|json=0" % (name, p.returncode, len(failed), ";".join(failed), 1 if out == RECEIPT else 0, 1 if b"Traceback" in p.stderr else 0, (time.monotonic_ns() - t0) // 1000000000)
with concurrent.futures.ThreadPoolExecutor(WORKERS) as ex:
    for row in ex.map(one, CASES):
        print(row, flush=True)
