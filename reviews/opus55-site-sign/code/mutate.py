# Mutation harness. Copies the test, applies one exact-string fault, runs a chosen set of sections at below-normal priority, and compares to the unmutated run
# of the same sections. Reads no credentials and edits no repository. Integers only. json=0.
import os, re, subprocess, sys, time

ROOT = "C:/tmp/opus55/site-sign-attack-20261103"
SRC = ROOT + "/repl/tests/test_site_sign_4d.py"
MUT = ROOT + "/mut/tests"
os.makedirs(MUT, exist_ok=True)
os.makedirs(ROOT + "/mut/docs", exist_ok=True)
for name in ("PREDICTION-YM4-02c-SITE-SIGN.hbp", "PREDICTION-YM4-02c.hbp"):
    data = open(ROOT + "/repl/docs/" + name, "rb").read()
    open(ROOT + "/mut/docs/" + name, "wb").write(data)

ORIGINAL = open(SRC, encoding="utf-8", newline="\n").read()
TAIL = "\n\nmain()\n"
assert ORIGINAL.endswith(TAIL)
SELECT = '''

WITNESS_BOUND = 1 << 13
_order = ["groups", "lattices", "exhaustive", "torus_route", "witnesses", "side_one", "second_seat", "zeros", "su2", "summary"]
_sel = os.environ.get("SEL", ",".join(_order)).split(",")
print("SITE_SIGN_TAGS|each_row_below=MEASURED_by_this_script|a_field_reading_DERIVED_or_OPEN_carries_that_tag_in_place|json=0")
for _name in _order:
    if _name in _sel:
        globals()["section_" + _name]()
    if _name == "zeros" and "zeros_light" in _sel:
        q = group("Q8")
        section, section_ok = q8_section(q)
        print("SITE_SIGN_ZEROS_SECTION|group=Q8|projection_to_(Z/2)^2_is_a_homomorphism_with_kernel_the_centre=%d|ok=%d|json=0" % (flag(section_ok), check("projection of Q8", section_ok)))
        section_zeros_control(q, section)
        section_zeros_twist(q)
finish()
'''


def build(mutations, name):
    text = ORIGINAL
    for old, new in mutations:
        count = text.count(old)
        if count != 1:
            raise RuntimeError("mutation %s: old string occurs %d times: %r" % (name, count, old[:80]))
        text = text.replace(old, new)
    text = text[: -len(TAIL)] + SELECT
    path = MUT + "/" + name + ".py"
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return path


def run(path, sel, argv=()):
    env = dict(os.environ)
    env["SEL"] = sel
    t0 = time.perf_counter_ns()
    r = subprocess.run(["python3", "-I", "-X", "utf8", path] + list(argv), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, creationflags=0x00004000, cwd=MUT, timeout=900)
    out = r.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    err = r.stderr.decode("utf-8", "replace").replace("\r\n", "\n")
    return r.returncode, out, err, (time.perf_counter_ns() - t0) // 10 ** 6


BASE_CACHE = {}


def baseline(sel):
    if sel not in BASE_CACHE:
        path = build([], "base_" + re.sub(r"\W+", "_", sel)[:60])
        rc, out, err, ms = run(path, sel)
        BASE_CACHE[sel] = (rc, out, ms)
        print("MUT_BASE|sel=%s|exit=%d|ms=%d|lines=%d|json=0" % (sel, rc, ms, out.count("\n")))
        sys.stdout.flush()
    return BASE_CACHE[sel]


def evaluate(mid, desc, mutations, sel):
    base_rc, base_out, _ = baseline(sel)
    path = build(mutations, mid)
    try:
        rc, out, err, ms = run(path, sel)
    except subprocess.TimeoutExpired:
        print("MUT|id=%s|desc=%s|result=timeout|json=0" % (mid, desc))
        return
    crash = "Traceback" in err
    failed = re.findall(r"^FAILED\|check=([^|]*)\|", out, flags=re.M)
    base_lines = base_out.split("\n")
    lines = out.split("\n")
    changed = sum(1 for a, b in zip(base_lines, lines) if a != b) + abs(len(base_lines) - len(lines))
    if crash:
        verdict = "killed_by_crash"
    elif failed:
        verdict = "killed_by_named_check"
    elif rc != base_rc:
        verdict = "killed_by_exit"
    elif changed:
        verdict = "passes_its_checks_cmp_catches_it"
    else:
        verdict = "SURVIVES_identical_output"
    print("MUT|id=%s|desc=%s|sel=%s|verdict=%s|exit=%d|named_failures=%d|first=%s|rows_changed=%d|ms=%d|json=0" % (mid, desc, sel, verdict, rc, len(failed), failed[0] if failed else "none", changed, ms))
    sys.stdout.flush()
