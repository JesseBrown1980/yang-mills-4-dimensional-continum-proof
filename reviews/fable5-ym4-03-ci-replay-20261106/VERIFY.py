# YM4-03 CI replay: the independent replay of this folder. It reads every byte against SHA256SUMS, INDEX.hbi and SEAL.hbp, the prediction against
# its committed sha256, the main-step outputs against the receipt, then recomputes the headline numbers from the raw logs by its own reading
# (step rows, echo-line times, the hosted log's group lines) and compares each with MEASURE.hbp. PASS needs all of that and every gate row:
# P01, P03, P05, P06, P09, P10, P16, P18, P19, P20 and Q4 read MET. The range rows P11 to P15, P17 and Q1 to Q3 are read and printed, a miss
# kept on file.
# Any changed, missing or unlisted byte exits 1. usage = VERIFY.py FOLDER REPO. Python standard library, integers only, json=0.
import hashlib
import os
import re
import sys

FOLDER, REPO = sys.argv[1], sys.argv[2]
PREDICTION_SHA256 = "1107015f4d5b206b081574d78497d53ebe2405063f6e5b8683256fe6b626ce74"
RECEIPT_SHA256 = "c6fbb64b30500f4f97b4cf3a508397977e6c4773182037ea820f527af8c79b8b"
CHAIN = ("INDEX.hbi", "SHA256SUMS", "SEAL.hbp", "VERIFY.hbp")
GATE_ROWS = ("P01", "P03", "P05", "P06", "P09", "P10", "P16", "P18", "P19", "P20", "Q4")
bad = []


def h(data):
    return hashlib.sha256(data).hexdigest()


def blob(*parts):
    with open(os.path.join(FOLDER, *parts), "rb") as handle:
        return handle.read()


def row(line):
    return dict(p.split("=", 1) for p in line.split("|")[1:] if "=" in p)


def fail(what):
    bad.append(what)
    print("VERIFY_FAIL|what=%s|json=0" % what)


# 1. Every byte.
listed = {}
for line in blob("SHA256SUMS").decode("utf-8").split("\n"):
    if line:
        digest, rel = line.split("  ", 1)
        listed[rel] = digest
present = []
for folder, dirs, files in os.walk(FOLDER):
    for name in files:
        rel = os.path.relpath(os.path.join(folder, name), FOLDER).replace(os.sep, "/")
        if rel not in CHAIN:
            present.append(rel)
for rel in sorted(set(present) | set(listed)):
    if rel not in listed:
        fail("unlisted_%s" % rel)
    elif rel not in present:
        fail("missing_%s" % rel)
    elif h(blob(rel)) != listed[rel]:
        fail("changed_%s" % rel)
index_text = blob("INDEX.hbi").decode("utf-8")
index_rows = [row(line) for line in index_text.split("\n") if line.startswith("FILE|")]
if sorted(r["path"] for r in index_rows) != sorted(listed):
    fail("index_paths")
for r in index_rows:
    if r["path"] in listed and (r["sha256"] != listed[r["path"]] or r["sh"] != r["sha256"][:16] or int(r["bytes"]) != len(blob(r["path"])) or int(r["cr"]) != blob(r["path"]).count(b"\r")):
        fail("index_row_%s" % r["path"])
seal = row(blob("SEAL.hbp").decode("utf-8").strip())
want = h(("SEAL|index_sha256=%s|sha256sums_sha256=%s" % (h(index_text.encode("utf-8")), h(blob("SHA256SUMS")))).encode("utf-8"))
if seal.get("seal") != want or seal.get("index_sha256") != h(index_text.encode("utf-8")) or seal.get("sha256sums_sha256") != h(blob("SHA256SUMS")):
    fail("seal")

# 2. The prediction and the receipt.
if h(blob("PREDICTION.hbp")) != PREDICTION_SHA256:
    fail("prediction_sha256")
with open(os.path.join(REPO, "tests", "ONE_SCALE_BLOCKING_RECEIPT.txt"), "rb") as handle:
    receipt = handle.read()
if h(receipt) != RECEIPT_SHA256:
    fail("receipt_sha256")
for label in ("A1", "A2", "B0"):
    if h(blob("raw", label, "blocking.out")) != RECEIPT_SHA256:
        fail("main_stdout_%s" % label)


# 3. The numbers again, read another way.
def step_rows(label):
    return [row(line) for line in blob("raw", label, "STEPS.hbp").decode("utf-8").split("\n") if line.startswith("STEP|")]


def step_ms(label, start):
    return [int(r["ms"]) for r in step_rows(label) if r["name"].startswith(start)]


def invocations(label):
    """ms per echoed sabotage, read from the T+ stamps of every step output of a run, in order."""
    out = []
    for name in sorted(os.listdir(os.path.join(FOLDER, "raw", label))):
        if not re.fullmatch(r"step-\d+\.out", name):
            continue
        last = 0
        for line in blob("raw", label, name).decode("utf-8").split("\n"):
            m = re.match(r"T\+(\d+)\|sabotage=([a-z_]+) exit=1 ", line)
            if m:
                out.append((m.group(2), int(m.group(1)) - last))
                last = int(m.group(1))
    return out


B_DIRS = [d for d in os.listdir(os.path.join(FOLDER, "raw")) if re.fullmatch(r"B[1-9][0-9]*", d)]


def first_call(label):
    split = row([line for line in blob("raw", label + ".hbp").decode("utf-8").split("\n") if line.startswith("SPLIT|")][0])
    return (int(split["chunk"]) - 1) * int(split["size"])


B_DIRS.sort(key=first_call)
before = sum(sum(step_ms(c, "Each sabotage")) for c in B_DIRS)
after = (step_ms("A1", "Each sabotage")[0] + step_ms("A2", "Each sabotage")[0]) // 2
main_before = step_ms("B0", "Every row against")[0]
main_after = (step_ms("A1", "Every row against")[0] + step_ms("A2", "Every row against")[0]) // 2
b_inv, b_dir = [], []
for c in B_DIRS:
    got = invocations(c)
    b_inv += got
    b_dir += [c] * len(got)
b_first = {}
for name, ms in b_inv:
    b_first.setdefault(name, ms)
a_inv = {label: dict(invocations(label)) for label in ("A1", "A2")}
log = blob("hosted", "run-42138789854.log").decode("utf-8", "replace").split("\n")


def t_of(line):
    m = re.search(r"T(\d\d):(\d\d):(\d\d)\.(\d+)Z", line)
    return (int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))) * 10000000 + int(m.group(4)[:7].ljust(7, "0"))


echo_lines = [k for k, line in enumerate(log) if re.search(r"Z sabotage=[a-z_]+ exit=1 ", line)]
group_lines = [k for k, line in enumerate(log) if "##[group]Run " in line]
start = t_of(log[max(k for k in group_lines if k < echo_lines[0])])
end = t_of(log[min(k for k in group_lines if k > echo_lines[-1])])
hosted_step = (end - start) // 10000
hosted_first, prev = {}, start
for k in echo_lines:
    name = re.search(r"Z sabotage=([a-z_]+) exit=1 ", log[k]).group(1)
    hosted_first.setdefault(name, (t_of(log[k]) - prev) // 10000)
    prev = t_of(log[k])
h1 = hosted_step * after // before
h2 = sum(hosted_first[n] * ((a_inv["A1"][n] + a_inv["A2"][n]) // 2) // b_first[n] for n in a_inv["A1"])
p_t = {}
for line in blob("raw", "P", "P.hbp").decode("utf-8").split("\n"):
    if line.startswith("TIMED|"):
        r = row(line)
        p_t.setdefault((r["label"].split("_", 1)[0], r["label"].split("_", 1)[1].rsplit("_", 1)[0]), []).append(int(r["wall_ms"]))
a_mean = {n: (a_inv["A1"][n] + a_inv["A2"][n]) // 2 for n in a_inv["A1"]}


def corr(n):
    pb, pa = sum(p_t[("before", n)]) // len(p_t[("before", n)]), sum(p_t[("after", n)]) // len(p_t[("after", n)])
    return pa * b_first[n], pb * a_mean[n]


flux_names = set()
for n in a_inv["A1"]:
    took = [int(x) for label in ("A1", "A2") for x in re.findall(r"section=section_flux\|mode=computed\|why=\w+\|ms=(\d+)", blob("raw", label, "sab-%s.out" % n).decode("utf-8"))]
    if len(took) == 2 and min(took) > 1000:
        flux_names.add(n)
cf, cd = corr("overlap_one_power"), corr("wrong_first_coefficient")
co = (cf[0] * cd[1] + cd[0] * cf[1], 2 * cf[1] * cd[1])
h4 = 0
for n in a_inv["A1"]:
    c = cf if n in flux_names else (cd if n == "wrong_first_coefficient" else co)
    h4 += hosted_first[n] * a_mean[n] * c[0] // (b_first[n] * c[1])
p_c = {}
for line in blob("raw", "P", "P.hbp").decode("utf-8").split(chr(10)):
    if line.startswith("TIMED|"):
        r = row(line)
        p_c.setdefault((r["label"].split("_", 1)[0], r["label"].split("_", 1)[1].rsplit("_", 1)[0]), []).append(int(r["cpu_ms"]))


def corr_cpu(n):
    pb, pa = sum(p_c[("before", n)]) // len(p_c[("before", n)]), sum(p_c[("after", n)]) // len(p_c[("after", n)])
    return pa * b_first[n], pb * a_mean[n]


kf, kd = corr_cpu("overlap_one_power"), corr_cpu("wrong_first_coefficient")
ko = (kf[0] * kd[1] + kd[0] * kf[1], 2 * kf[1] * kd[1])
h4c = 0
for n in a_inv["A1"]:
    c = kf if n in flux_names else (kd if n == "wrong_first_coefficient" else ko)
    h4c += hosted_first[n] * a_mean[n] * c[0] // (b_first[n] * c[1])
mine = {"sabotage_x1000": before * 1000 // after, "main_x1000": main_after * 1000 // main_before, "H1_after_ms": h1, "H1_x1000": hosted_step * 1000 // h1, "H2_after_ms": h2, "H2_x1000": hosted_step * 1000 // h2, "hosted_step_ms": hosted_step, "H4_after_ms": h4, "H4C_after_ms": h4c}
measure = blob("MEASURE.hbp").decode("utf-8").split("\n")


def measured(head, key, where=None):
    for line in measure:
        if line.startswith(head + "|") and (where is None or where in line):
            return int(row(line)[key])
    return None


theirs = {"sabotage_x1000": measured("LOCAL_RATIO", "sabotage_x1000"), "main_x1000": measured("LOCAL_RATIO", "main_after_over_before_x1000"),
          "H1_after_ms": measured("PROJECTION", "hosted_after_ms", "|id=H1|"), "H1_x1000": measured("PROJECTION", "ratio_x1000", "|id=H1|"),
          "H2_after_ms": measured("PROJECTION", "hosted_after_ms", "|id=H2|"), "H2_x1000": measured("PROJECTION", "ratio_x1000", "|id=H2|"), "hosted_step_ms": measured("HOSTED", "sabotage_step_ms"), "H4_after_ms": measured("PROJECTION", "hosted_after_ms", "|id=H4|"), "H4C_after_ms": measured("PROJECTION", "hosted_after_ms", "|id=H4C|")}
for key in sorted(mine):
    same = int(mine[key] == theirs[key])
    print("VERIFY_NUMBER|name=%s|replayed=%d|measure_hbp=%s|same=%d|json=0" % (key, mine[key], theirs[key], same))
    if not same:
        fail("number_%s" % key)
identical = 0
strip = ("SECTION|", "REPLAY")
for name in a_inv["A1"]:
    texts = [blob("raw", b_dir[[n for n, _ in b_inv].index(name)], "sab-%s.out" % name)] + [blob("raw", label, "sab-%s.out" % name) for label in ("A1", "A2")]
    kept = [b"\n".join(x for x in t.split(b"\n") if not x.startswith(tuple(s.encode("utf-8") for s in strip))) for t in texts]
    identical += int(kept[0] == kept[1] == kept[2])
print("VERIFY_NUMBER|name=stdout_identical|replayed=%d|measure_hbp=%s|same=%d|json=0" % (identical, measured("SABOTAGE_DONE", "stdout_identical_B_A1_A2"), int(identical == measured("SABOTAGE_DONE", "stdout_identical_B_A1_A2"))))
if identical != measured("SABOTAGE_DONE", "stdout_identical_B_A1_A2"):
    fail("number_stdout_identical")

# 4. The gate rows.
results = {}
for line in measure:
    if line.startswith("READ|"):
        r = row(line)
        results[r["id"]] = r["result"]
for pid in GATE_ROWS:
    if results.get(pid) != "MET":
        fail("gate_row_%s" % pid)
ranges = ",".join("%s:%s" % (pid, results.get(pid, "absent")) for pid in ("P11", "P12", "P13", "P14", "P15", "P17", "Q1", "Q2", "Q3"))
print("VERIFY_DONE|files=%d|failures=%d|ranges=%s|result=%s|json=0" % (len(listed), len(bad), ranges, "PASS" if not bad else "FAIL"))
sys.exit(1 if bad else 0)
