# Faults inside the two long loops of section_zeros_central, read against the ZEROS rows of the receipt. Below-normal priority, three at a time. json=0.
import os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutate

ROOT = mutate.ROOT
RECEIPT = open(ROOT + "/repl/tests/SITE_SIGN_RECEIPT.txt", encoding="utf-8", newline="\n").read().split("\n")
BASE_ROWS = [l for l in RECEIPT if l.startswith("SITE_SIGN_ZEROS")]

HEAVY = [
    ("h1_lifts_all_zero", "route 1 reads the zero lift of each field", [("lifts = [[4 * stream.below(2) for _ in range(width)] for _ in range(4093)]", "lifts = [[0 for _ in range(width)] for _ in range(4093)]")]),
    ("h2_face_bit_swapped", "route 1 records each negative face at its neighbour's bit", [("                    negative |= 1 << position\n", "                    negative |= 1 << (position ^ 1)\n")]),
    ("h3_gray_no_flip", "route 2 flips nothing", [("                config[flip] = m[minus][config[flip]]\n", "                config[flip] = m[one][config[flip]]\n")]),
    ("h4_cycles_short", "cycle count one bit short", [("cycles = 1 << len(f2_kernel(cubes, len(faces)))", "cycles = 1 << (len(f2_kernel(cubes, len(faces))) - 1)")]),
    ("h5_tree_ignored", "route 2 fields taken as any eight flat cochains, tree left free", [("fixed_fields = [u for u in span if (u & tree_mask) == 0]", "fixed_fields = span[:8]")]),
    ("h6_negative_s_constant", "route 2 counts odd S as zero", [("gauge_negative += negative.bit_count() & 1", "gauge_negative += 0")]),
    ("h7_face_order_cube", "cube masks read a shifted face", [("            mask |= 1 << index[(lat.shift(x, rho), mu, nu)]\n", "            mask |= 1 << index[(x, mu, nu)]\n")]),
    ("h8_patterns_formula", "patterns per field formula off", [("patterns_per_field, patterns_each_field_ok, every_pattern = 1 << (width - dimension), True, set()", "patterns_per_field, patterns_each_field_ok, every_pattern = 1 << (width - dimension - 1), True, set()")]),
    ("h9_section_lift_ignored", "route 1 section ignores the lift bit, so flips are never read", [("config = [section[a + b + c] for a, b, c in zip(u_row, v_row, lifts[read % 4093])]", "config = [section[a + b] for a, b, c in zip(u_row, v_row, lifts[read % 4093])]")]),
]


def one(item):
    mid, desc, muts = item
    path = mutate.build(muts, mid)
    env = dict(os.environ)
    env["SEL"] = "zeros"
    t0 = time.perf_counter_ns()
    try:
        r = subprocess.run(["python3", "-I", "-X", "utf8", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, creationflags=0x00004000, cwd=mutate.MUT, timeout=2400)
    except subprocess.TimeoutExpired:
        print("MUTH|id=%s|desc=%s|verdict=timeout|json=0" % (mid, desc))
        sys.stdout.flush()
        return
    out = r.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    err = r.stderr.decode("utf-8", "replace")
    rows = [l for l in out.split("\n") if l.startswith("SITE_SIGN_ZEROS")]
    failed = re.findall(r"^FAILED\|check=([^|]*)\|", out, flags=re.M)
    changed = sum(1 for a, b in zip(BASE_ROWS, rows) if a != b) + abs(len(BASE_ROWS) - len(rows))
    verdict = "killed_by_crash" if "Traceback" in err else "killed_by_named_check" if failed else "killed_by_exit" if r.returncode else "passes_its_checks_cmp_catches_it" if changed else "SURVIVES_identical_output"
    print("MUTH|id=%s|desc=%s|verdict=%s|exit=%d|named_failures=%d|first=%s|zero_rows_changed=%d|ms=%d|json=0" % (mid, desc, verdict, r.returncode, len(failed), failed[0] if failed else "none", changed, (time.perf_counter_ns() - t0) // 10 ** 6))
    sys.stdout.flush()


only = set(sys.argv[1:])
items = [h for h in HEAVY if not only or h[0] in only]
with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(one, items))
print("MUTH_DONE|json=0")
