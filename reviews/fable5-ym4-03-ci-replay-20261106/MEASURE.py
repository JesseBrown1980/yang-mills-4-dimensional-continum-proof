# YM4-03 CI replay: every number of MEASURE.hbp from the raw logs in this folder, then each prediction of PREDICTION.hbp read as MET or MISS.
# usage = MEASURE.py FOLDER REPO, FOLDER being reviews/fable5-ym4-03-ci-replay-20261106 and REPO the tree that holds tests/. Python standard
# library, integers only (times in ms, ratios x1000), json=0.
import hashlib
import os
import re
import sys

FOLDER, REPO = sys.argv[1], sys.argv[2]
RAW = os.path.join(FOLDER, "raw")
HOSTED = os.path.join(FOLDER, "hosted", "run-42138789854.log")
with open(os.path.join(REPO, "tests", "ONE_SCALE_BLOCKING_RECEIPT.txt"), "rb") as handle:
    RECEIPT = handle.read()
STDERR_TAGS = ("SECTION|", "REPLAY|", "REPLAY_START|", "REPLAY_DONE|", "REPLAY_REFUSED|", "REPLAY_INDEX|", "REPLAY_NOT_READY|")
OUT = []
READS = {}


def emit(row, tag="MEASURED"):
    OUT.append(row + "|tag=%s|json=0" % tag)


def fields(line):
    return dict(p.partition("=")[::2] for p in line.split("|")[1:])


def read(label, name, mode="rb"):
    with open(os.path.join(RAW, label, name), mode) as handle:
        return handle.read()


def steps(label):
    out = {}
    for line in read(label, "STEPS.hbp").decode("utf-8").split("\n"):
        if line.startswith("STEP|"):
            f = fields(line)
            out[int(f["k"])] = {"rc": int(f["rc"]), "ms": int(f["ms"]), "cpu": int(f["cpu_ms"]), "name": f["name"]}
    return out


def step_of(table, prefix):
    hits = [k for k, s in table.items() if s["name"].startswith(prefix)]
    return hits[0] if len(hits) == 1 else None


def calls(label, k):
    """The read_sabotage calls of a step script: name and named checks, in order."""
    out = []
    for line in read(label, "step-%d.sh" % k).decode("utf-8").split("\n"):
        if line.startswith("read_sabotage "):
            name = line.split(" ", 2)[1]
            out.append((name, re.findall(r"'([^']*)'", line)))
    return out


def echoes(label, k):
    """(name, ms since the previous echo line or the step start, the rest of the line) for each sabotage echo line of a step."""
    out, last = [], 0
    for line in read(label, "step-%d.out" % k).decode("utf-8").split("\n"):
        m = re.match(r"T\+(\d+)\|sabotage=(\S+) exit=(\d+) (.*)$", line)
        if m:
            t = int(m.group(1))
            out.append((m.group(2), t - last, int(m.group(3)), m.group(4)))
            last = t
    return out


def stdout_only(data):
    return "\n".join(line for line in data.decode("utf-8").split("\n") if not line.startswith(STDERR_TAGS)).encode("utf-8")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def mean2(a, b):
    return (a + b) // 2


# ---- The runs on this machine.
A = {label: steps(label) for label in ("A1", "A2")}
B0 = steps("B0")
def split_row(label):
    """chunk and size of a before script, from the SPLIT row its run printed."""
    with open(os.path.join(RAW, label + ".hbp"), encoding="utf-8") as handle:
        row = fields([line for line in handle.read().split("\n") if line.startswith("SPLIT|")][0])
    return int(row["chunk"]), int(row["size"])


B_LABELS = sorted((d for d in os.listdir(RAW) if re.fullmatch(r"B[1-9][0-9]*", d)), key=lambda d: (split_row(d)[0] - 1) * split_row(d)[1])
BC = {label: steps(label) for label in B_LABELS}
info = {}
for label in ("A1", "A2"):
    t = A[label]
    k_main, k_sab, k_ctl, k_unk = step_of(t, "Every row against"), step_of(t, "Each sabotage"), step_of(t, "The replay refuses"), step_of(t, "An unknown")
    cheap = sum(t[k]["ms"] for k in t if k not in (k_main, k_sab, k_ctl, k_unk))
    info[label] = {"main": t[k_main]["ms"], "main_cpu": t[k_main]["cpu"], "sab": t[k_sab]["ms"], "sab_cpu": t[k_sab]["cpu"], "ctl": t[k_ctl]["ms"], "unk": t[k_unk]["ms"], "cheap": cheap, "k_sab": k_sab, "k_ctl": k_ctl}
    emit("RUN|label=%s|steps=%d|rc_zero=%d|cheap_ms=%d|main_ms=%d|main_cpu_ms=%d|sabotage_ms=%d|sabotage_cpu_ms=%d|controls_ms=%d|unknown_ms=%d|total_ms=%d" % (
        label, len(t), sum(1 for s in t.values() if s["rc"] == 0), cheap, t[k_main]["ms"], t[k_main]["cpu"], t[k_sab]["ms"], t[k_sab]["cpu"], t[k_ctl]["ms"], t[k_unk]["ms"], sum(s["ms"] for s in t.values())))
k_main_b, k_unk_b = step_of(B0, "Every row against"), step_of(B0, "An unknown")
b_sab = sum(s["ms"] for c in BC for s in BC[c].values())
b_sab_cpu = sum(s["cpu"] for c in BC for s in BC[c].values())
b_cheap = sum(B0[k]["ms"] for k in B0 if k not in (k_main_b, k_unk_b))
b_rc = sum(1 for s in B0.values() if s["rc"] == 0) + int(all(s["rc"] == 0 for c in BC for s in BC[c].values()))
info["B"] = {"main": B0[k_main_b]["ms"], "main_cpu": B0[k_main_b]["cpu"], "sab": b_sab, "sab_cpu": b_sab_cpu, "unk": B0[k_unk_b]["ms"]}
emit("RUN|label=B|steps=%d|rc_zero=%d|cheap_ms=%d|main_ms=%d|main_cpu_ms=%d|sabotage_ms=%d|sabotage_cpu_ms=%d|sabotage_scripts=%s|unknown_ms=%d|total_ms=%d" % (
    len(B0) + 1, b_rc, b_cheap, B0[k_main_b]["ms"], B0[k_main_b]["cpu"], b_sab, b_sab_cpu, ",".join("%s:%d" % (c, sum(s["ms"] for s in BC[c].values())) for c in B_LABELS), B0[k_unk_b]["ms"], b_cheap + B0[k_main_b]["ms"] + b_sab + B0[k_unk_b]["ms"]))
split_text = ",".join("%s:chunk=%d:size=%d" % ((c,) + split_row(c)) for c in B_LABELS)
if split_text != "B1:chunk=1:size=4,B2:chunk=2:size=4,B3:chunk=3:size=4,B4:chunk=4:size=4":
    emit("DEVIATION|plan=4_scripts_of_4_calls|run=%s|why=other_lanes_raised_the_load_to_6_to_8_and_one_4_call_script_took_over_23_minutes_so_calls_9_to_16_ran_2_at_a_time_to_keep_each_run_under_30_minutes|same_bash_text_and_order=1" % split_text)
main_same = {label: int(read(label, "blocking.out") == RECEIPT) for label in ("A1", "A2", "B0")}
emit("MAIN_STDOUT|receipt_sha256=%s|receipt_bytes=%d|A1_is_receipt=%d|A2_is_receipt=%d|B_is_receipt=%d" % (sha(RECEIPT), len(RECEIPT), main_same["A1"], main_same["A2"], main_same["B0"]))
done_rows = {}
for label in ("A1", "A2"):
    index = read(label, os.path.join("ym4-03-cache", "REPLAY-INDEX.hbp"))
    side = read(label, os.path.join("ym4-03-cache", "REPLAY-INDEX.hbp.sha256")).decode("utf-8").split(" ", 1)[0]
    done = [line for line in index.decode("utf-8").split("\n") if line.startswith("REPLAY_DONE|")][0]
    done_rows[label] = fields(done)
    emit("RECORD|label=%s|index_sha256=%s|sidecar_matches=%d|%s" % (label, sha(index), int(sha(index) == side), done[len("REPLAY_DONE|"):-len("|json=0")]))

# ---- Each sabotage, before and after.
b_calls, b_times, b_where = [], [], []
for c in B_LABELS:
    k = step_of(BC[c], "Each sabotage")
    got = calls(c, k)
    b_calls += got
    b_where += [c] * len(got)
    b_times += echoes(c, k)
a_calls = calls("A1", info["A1"]["k_sab"])
a_times = {label: echoes(label, info[label]["k_sab"]) for label in ("A1", "A2")}
b_first = {}
for (name, dt, rc, _), (cname, named) in zip(b_times, b_calls):
    b_first.setdefault(name, dt)
b_all = {}
for name, dt, rc, _ in b_times:
    b_all.setdefault(name, []).append(dt)
names = [name for name, _ in a_calls]
identical = 0
per = {}
b_ok = 0
for name, named in b_calls:
    data = read(b_where[b_calls.index((name, named))], "sab-%s.out" % name)
    rc_echo = [rc for n, _, rc, _ in b_times if n == name]
    ok = int(all(r == 1 for r in rc_echo) and all(("FAILED|check=%s|json=0" % x).encode("utf-8") in data for x in named) and b"Traceback" not in data)
    b_ok += ok
for name, named in a_calls:
    outs = {label: read(label, "sab-%s.out" % name) for label in ("A1", "A2")}
    before = read(b_where[[n for n, _ in b_calls].index(name)], "sab-%s.out" % name)
    digests = [sha(stdout_only(before)), sha(stdout_only(outs["A1"])), sha(stdout_only(outs["A2"]))]
    same = int(digests[0] == digests[1] == digests[2])
    identical += same
    row = {}
    for label in ("A1", "A2"):
        text = outs[label].decode("utf-8")
        done = fields([line for line in text.split("\n") if line.startswith("REPLAY_DONE|")][0])
        flux = re.findall(r"section=section_flux\|mode=computed\|why=[a-z_]+\|ms=(\d+)", text)
        row[label] = {
            "rc": [rc for n, _, rc, _ in a_times[label] if n == name][0], "ms": [d for n, d, _, _ in a_times[label] if n == name][0],
            "named": int(all("FAILED|check=%s|json=0" % x in text for x in named)), "traceback": text.count("Traceback"),
            "replay_failed": len(re.findall(r"^FAILED\|check=replay_", text, re.M)), "computed": text.count("|mode=computed|"),
            "computed_reached": text.count("|mode=computed|why=reached_by_%s|" % name), "reused": text.count("|mode=reused|"),
            "certified": int(done["brackets_certified"]), "bisected": int(done["brackets_bisected"]), "flux_ms": int(flux[0]) if flux else -1,
        }
    stamps = dict(re.findall(r"SECTION\|(\w+)\|elapsed_seconds=(\d+)", before.decode("utf-8")))
    before_flux = (int(stamps["done"]) - int(stamps["electric_flux"])) * 1000 if "electric_flux" in stamps and "done" in stamps else -1
    per[name] = {"b": b_first[name], "a": mean2(row["A1"]["ms"], row["A2"]["ms"]), "flux_a": mean2(row["A1"]["flux_ms"], row["A2"]["flux_ms"]), "flux_b": before_flux, "row": row, "same": same,
                 "flux_class": row["A1"]["flux_ms"] > 1000 and row["A2"]["flux_ms"] > 1000}
    r1, r2 = row["A1"], row["A2"]
    emit("SABOTAGE|name=%s|named=%s|before_ms=%s|A1_ms=%d|A2_ms=%d|rc=%d,%d|named_found=%d,%d|traceback=%d,%d|replay_failed=%d,%d|computed=%d,%d|computed_reached=%d,%d|reused=%d,%d|brackets_certified=%d,%d|brackets_bisected=%d,%d|flux_ms_before=%d|flux_ms_after=%d,%d|stdout_sha256=%s,%s,%s|identical=%d" % (
        name, "+".join(named).replace(" ", "_"), ",".join(map(str, b_all[name])), r1["ms"], r2["ms"], r1["rc"], r2["rc"], r1["named"], r2["named"], r1["traceback"], r2["traceback"], r1["replay_failed"], r2["replay_failed"],
        r1["computed"], r2["computed"], r1["computed_reached"], r2["computed_reached"], r1["reused"], r2["reused"], r1["certified"], r2["certified"], r1["bisected"], r2["bisected"], before_flux, r1["flux_ms"], r2["flux_ms"],
        digests[0][:16], digests[1][:16], digests[2][:16], same))
emit("SABOTAGE_DONE|after_names=%d|before_invocations=%d|before_ok=%d|stdout_identical_B_A1_A2=%d" % (len(names), len(b_calls), b_ok, identical))

# ---- The controls and unknown names.
ctl = {}
for label in ("A1", "A2"):
    text = read(label, "step-%d.out" % info[label]["k_ctl"]).decode("utf-8")
    refused = re.findall(r"cache control exit=1 on (\S+)", text)
    reuse_out = read(label, "reuse.out")
    reuse_err = read(label, "reuse.err").decode("utf-8")
    ctl[label] = {"refused": refused, "reuse": int(reuse_out == RECEIPT and b"FAILED|check=covariance_b=2|json=0" not in reuse_out and "|reused=16|computed=0|" in reuse_err), "rc": A[label][info[label]["k_ctl"]]["rc"]}
    emit("CONTROLS|label=%s|step_rc=%d|refused=%s|reuse_reached_receipt_exit0_no_named=%d" % (label, ctl[label]["rc"], ",".join(refused), ctl[label]["reuse"]))
unk = {label: A[label][step_of(A[label], "An unknown")]["rc"] for label in ("A1", "A2")}
emit("UNKNOWN|A1_step_rc=%d|A2_step_rc=%d|B_step_rc=%d|names_per_step=3,3,1" % (unk["A1"], unk["A2"], B0[k_unk_b]["rc"]))

# ---- Ratios on this machine.
a_sab = mean2(info["A1"]["sab"], info["A2"]["sab"])
a_sab_cpu = mean2(info["A1"]["sab_cpu"], info["A2"]["sab_cpu"])
a_main = mean2(info["A1"]["main"], info["A2"]["main"])
a_ctl = mean2(info["A1"]["ctl"], info["A2"]["ctl"])
a_unk = mean2(info["A1"]["unk"], info["A2"]["unk"])
local_sab = b_sab * 1000 // a_sab
local_main = a_main * 1000 // info["B"]["main"]
emit("LOCAL_RATIO|sabotage_before_ms=%d|sabotage_after_mean_ms=%d|sabotage_x1000=%d|sabotage_cpu_x1000=%d|main_after_mean_ms=%d|main_before_ms=%d|main_after_over_before_x1000=%d|A1_x1000=%d|A2_x1000=%d" % (
    b_sab, a_sab, local_sab, b_sab_cpu * 1000 // a_sab_cpu, a_main, info["B"]["main"], local_main, b_sab * 1000 // info["A1"]["sab"], b_sab * 1000 // info["A2"]["sab"]))


# ---- The hosted run 42138789854.
def ticks_of(line):
    m = re.search(r"T(\d\d):(\d\d):(\d\d)\.(\d{7})Z", line)
    return None if not m else ((int(m.group(1)) * 60 + int(m.group(2))) * 60 + int(m.group(3))) * 10000000 + int(m.group(4))


with open(HOSTED, "rb") as handle:
    hosted_bytes = handle.read()
log = hosted_bytes.decode("utf-8", "replace").split("\n")
groups = [(k, ticks_of(line)) for k, line in enumerate(log) if "##[group]Run " in line]


def group_containing(text):
    for j, (k, t) in enumerate(groups):
        end = groups[j + 1][0] if j + 1 < len(groups) else len(log)
        if any(text in line for line in log[k:end]):
            return t, groups[j + 1][1] if j + 1 < len(groups) else None, k
    return None, None, None


sab_start, sab_end, sab_line = group_containing("read_sabotage() {")
main_start, main_end, _ = group_containing("tests/test_one_scale_blocking.py > /tmp/blocking.out")
first = [ticks_of(line) for line in log if ticks_of(line) is not None]
hosted_step = (sab_end - sab_start) // 10000
hosted_main = (main_end - main_start) // 10000
hosted_job = (first[-1] - first[0]) // 10000
hosted_k, prev = {}, sab_start
hosted_list = []
for line in log[sab_line:]:
    m = re.search(r"Z sabotage=(\S+) exit=1 ", line)
    if m:
        t = ticks_of(line)
        hosted_list.append((m.group(1), (t - prev) // 10000))
        hosted_k.setdefault(m.group(1), (t - prev) // 10000)
        prev = t
stamps = {}
for line in log:
    m = re.search(r"Z SECTION\|(\w+)\|elapsed_seconds=(\d+)", line)
    if m:
        stamps[m.group(1)] = int(m.group(2)) * 1000
emit("HOSTED|run=42138789854|log_sha256=%s|log_bytes=%d|job_ms=%d|main_step_ms=%d|sabotage_step_ms=%d|invocations=%d|invocation_sum_ms=%d|stamp_done_ms=%d|stamp_electric_flux_ms=%d|pushforward_ms=%d|first_dependence_ms=%d" % (
    sha(hosted_bytes), len(hosted_bytes), hosted_job, hosted_main, hosted_step, len(hosted_list), sum(dt for _, dt in hosted_list), stamps["done"], stamps["electric_flux"],
    stamps["two_dimensions"] - stamps["integral_identity"], stamps["certified_truncation"] - stamps["first_dependence"]))
for name, dt in hosted_list:
    emit("HOSTED_INVOCATION|name=%s|ms=%d" % (name, dt))
h1_after = hosted_step * a_sab // b_sab
h1_ratio = hosted_step * 1000 // h1_after
emit("PROJECTION|id=H1|hosted_before_ms=%d|hosted_after_ms=%d|ratio_x1000=%d" % (hosted_step, h1_after, h1_ratio), "DERIVED")
h2_after = 0
for name in names:
    part = hosted_k[name] * per[name]["a"] // per[name]["b"]
    h2_after += part
    emit("PROJECTION_PART|id=H2|name=%s|hosted_before_ms=%d|local_before_ms=%d|local_after_mean_ms=%d|hosted_after_ms=%d" % (name, hosted_k[name], per[name]["b"], per[name]["a"], part), "DERIVED")
h2_ratio = hosted_step * 1000 // h2_after
emit("PROJECTION|id=H2|hosted_before_ms=%d|hosted_after_ms=%d|ratio_x1000=%d" % (hosted_step, h2_after, h2_ratio), "DERIVED")
scale_n, scale_d = 166000, info["B"]["main"]
s0 = (per["shifted_endpoint"]["a"] + per["dropped_inverse"]["a"] + per["theta_no_inverse"]["a"]) * scale_n // (3 * scale_d)
h3_after = 0
for name in names:
    if per[name]["flux_class"]:
        part, how = s0 + (hosted_k[name] - 91000) * per[name]["flux_a"] // per[name]["flux_b"], "s0+hosted_flux_times_local_after_flux_over_local_before_flux"
    elif name == "wrong_first_coefficient":
        part, how = s0 + 35000, "s0+first_dependence_35000"
    elif name == "extra_plaquette_factor":
        part, how = s0 + 17000, "s0+pushforward_17000"
    else:
        part, how = per[name]["a"] * scale_n // scale_d, "local_after_times_166000_over_local_before_main"
    h3_after += part
    emit("PROJECTION_PART|id=H3|name=%s|hosted_after_ms=%d|from=%s" % (name, part, how), "DERIVED")
h3_ratio = hosted_step * 1000 // h3_after
emit("PROJECTION|id=H3|s0_ms=%d|hosted_before_ms=%d|hosted_after_ms=%d|ratio_x1000=%d" % (s0, hosted_step, h3_after, h3_ratio), "DERIVED")
job_after = 7000 + 166000 * local_main // 1000 + h1_after + (a_ctl + a_unk) * scale_n // scale_d
job_ratio = hosted_job * 1000 // job_after
emit("PROJECTION|id=JOB|hosted_job_before_ms=%d|hosted_job_after_ms=%d|ratio_x1000=%d|main_after_ms=%d|sabotage_after_ms=%d|controls_and_unknown_after_ms=%d" % (
    hosted_job, job_after, job_ratio, 166000 * local_main // 1000, h1_after, (a_ctl + a_unk) * scale_n // scale_d), "DERIVED")
emit("CLAIM|source=attack_lane_a_b_d|hosted_after_ms=293000|ratio_x1000=%d|H1_x1000=%d|H2_x1000=%d|H3_x1000=%d|H1_and_H2_at_least_8700=%d" % (2557 * 1000 // 293, h1_ratio, h2_ratio, h3_ratio, int(h1_ratio >= 8700 and h2_ratio >= 8700)), "DERIVED")

# ---- P: load-matched pairs, B A A B, and the projection H4 they correct.
p_rows = [fields(line) for line in read("P", "P.hbp").decode("utf-8").split("\n") if line.startswith("TIMED|")]
paired = {}
q4 = True
for name in ("overlap_one_power", "wrong_first_coefficient"):
    named = [x for n, x in a_calls if n == name][0]
    b = [r for r in p_rows if r["label"].startswith("before_%s_" % name)]
    a = [r for r in p_rows if r["label"].startswith("after_%s_" % name)]
    pb, pa = sum(int(r["wall_ms"]) for r in b) // len(b), sum(int(r["wall_ms"]) for r in a) // len(a)
    pbc, pac = sum(int(r["cpu_ms"]) for r in b) // len(b), sum(int(r["cpu_ms"]) for r in a) // len(a)
    outs_b = [read("P", "before-%s-%s.out" % (name, r["label"].rsplit("_", 1)[1])) for r in b]
    outs_a = [read("P", "after-%s-%s.out" % (name, r["label"].rsplit("_", 1)[1])) for r in a]
    ok = all(r["rc"] == "1" for r in b + a) and all(all(("FAILED|check=%s|json=0" % x).encode("utf-8") in o for x in named) for o in outs_a) and all(o == outs_b[0] for o in outs_b + outs_a)
    q4 = q4 and ok
    paired[name] = (pb, pa)
    emit("PAIRED|name=%s|before_ms=%s|after_ms=%s|before_cpu_ms=%s|after_cpu_ms=%s|loads=%s|ratio_x1000=%d|cpu_ratio_x1000=%d|sandwich_before_ms=%d|sandwich_after_mean_ms=%d|sandwich_ratio_x1000=%d|correction_x1000=%d|rc_named_stdout_equal=%d" % (
        name, ",".join(r["wall_ms"] for r in b), ",".join(r["wall_ms"] for r in a), ",".join(r["cpu_ms"] for r in b), ",".join(r["cpu_ms"] for r in a), ",".join(r["load"] for r in p_rows if name in r["label"]),
        pb * 1000 // pa, pbc * 1000 // pac, per[name]["b"], per[name]["a"], per[name]["b"] * 1000 // per[name]["a"], pa * per[name]["b"] * 1000 // (pb * per[name]["a"]), int(ok)))
fb, fa = paired["overlap_one_power"]
db, da = paired["wrong_first_coefficient"]
cf = (fa * per["overlap_one_power"]["b"], fb * per["overlap_one_power"]["a"])
cd = (da * per["wrong_first_coefficient"]["b"], db * per["wrong_first_coefficient"]["a"])
co = (cf[0] * cd[1] + cd[0] * cf[1], 2 * cf[1] * cd[1])
h4_after = 0
for name in names:
    c, how = (cf, "c_flux") if per[name]["flux_class"] else ((cd, "c_first_dependence") if name == "wrong_first_coefficient" else (co, "c_other"))
    part = hosted_k[name] * per[name]["a"] * c[0] // (per[name]["b"] * c[1])
    h4_after += part
    emit("PROJECTION_PART|id=H4|name=%s|hosted_after_ms=%d|correction=%s|correction_x1000=%d" % (name, part, how, c[0] * 1000 // c[1]), "DERIVED")
h4_ratio = hosted_step * 1000 // h4_after
cpu_pairs = {}
for name in ("overlap_one_power", "wrong_first_coefficient"):
    b = [int(r["cpu_ms"]) for r in p_rows if r["label"].startswith("before_%s_" % name)]
    a = [int(r["cpu_ms"]) for r in p_rows if r["label"].startswith("after_%s_" % name)]
    cpu_pairs[name] = (sum(b) // len(b), sum(a) // len(a))
gb, ga = cpu_pairs["overlap_one_power"]
eb, ea = cpu_pairs["wrong_first_coefficient"]
kf = (ga * per["overlap_one_power"]["b"], gb * per["overlap_one_power"]["a"])
kd = (ea * per["wrong_first_coefficient"]["b"], eb * per["wrong_first_coefficient"]["a"])
ko = (kf[0] * kd[1] + kd[0] * kf[1], 2 * kf[1] * kd[1])
h4c_after = 0
for name in names:
    c = kf if per[name]["flux_class"] else (kd if name == "wrong_first_coefficient" else ko)
    h4c_after += hosted_k[name] * per[name]["a"] * c[0] // (per[name]["b"] * c[1])
h4c_ratio = hosted_step * 1000 // h4c_after
emit("PROJECTION|id=H4C|added_after_the_plan=1|hosted_before_ms=%d|hosted_after_ms=%d|ratio_x1000=%d|pair_cpu_ms=overlap_one_power:%d,%d;wrong_first_coefficient:%d,%d|c_flux_x1000=%d|c_first_dependence_x1000=%d|c_other_x1000=%d" % (
    hosted_step, h4c_after, h4c_ratio, gb, ga, eb, ea, kf[0] * 1000 // kf[1], kd[0] * 1000 // kd[1], ko[0] * 1000 // ko[1]), "DERIVED")
for label in ("A1", "A2"):
    after_cpu = info[label]["sab_cpu"]
    emit("PROJECTION|id=H1C_%s|added_after_the_plan=1|local_before_cpu_ms=%d|local_after_cpu_ms=%d|local_cpu_x1000=%d|hosted_before_ms=%d|hosted_after_ms=%d|ratio_x1000=%d" % (
        label, b_sab_cpu, after_cpu, b_sab_cpu * 1000 // after_cpu, hosted_step, hosted_step * after_cpu // b_sab_cpu, b_sab_cpu * 1000 // after_cpu), "DERIVED")
emit("PROJECTION|id=H1C_MEAN|added_after_the_plan=1|local_before_cpu_ms=%d|local_after_cpu_ms=%d|hosted_after_ms=%d|ratio_x1000=%d" % (b_sab_cpu, a_sab_cpu, hosted_step * a_sab_cpu // b_sab_cpu, b_sab_cpu * 1000 // a_sab_cpu), "DERIVED")
emit("FLUX_CLASS|names=%s|count=%d|from=after_runs_section_flux_computed_over_1000_ms|note=every_before_run_computes_the_flux_section_so_the_before_reading_holds_for_%d_names" % (",".join(n for n in names if per[n]["flux_class"]), sum(1 for n in names if per[n]["flux_class"]), sum(1 for n in names if per[n]["flux_b"] > 1000)))
emit("PROJECTION|id=H4|hosted_before_ms=%d|hosted_after_ms=%d|ratio_x1000=%d|c_flux_x1000=%d|c_first_dependence_x1000=%d|c_other_x1000=%d" % (hosted_step, h4_after, h4_ratio, cf[0] * 1000 // cf[1], cd[0] * 1000 // cd[1], co[0] * 1000 // co[1]), "DERIVED")

# ---- X1: record with every seed moved up by one.
x1 = fields([line for line in read("X1", "X1.hbp").decode("utf-8").split("\n") if line.startswith("X1|")][0])
x1_same = int(read("X1", "record.out") == RECEIPT)
x1_done = fields([line for line in read("X1", "ym4-03-cache/REPLAY-INDEX.hbp").decode("utf-8").split("\n") if line.startswith("REPLAY_DONE|")][0])
emit("X1|rc=%s|ms=%s|stdout_is_receipt=%d|seeded=%s|bisected=%s|brackets=%s|seed_file_rows_moved=%s" % (x1["rc"], x1["ms"], x1_same, x1_done["seeded"], x1_done["bisected"], x1_done["brackets"], x1["moved"]))

# ---- Gates and carriage returns.
gates = open(os.path.join(FOLDER, "GATES.hbp"), encoding="utf-8").read().split("\n")
gate_steps = [fields(line) for line in gates if line.startswith("STEP|")]
gate_ok = int(all(g["rc"] == "0" for g in gate_steps) and len(gate_steps) == 9 and any("NO_FLOAT_BASE_SCAN|rc=0|" in line for line in gates)
              and any("NO_FLOAT_BASE_SELFTEST|rc=0|" in line for line in gates) and any("NO_FLOAT_LIST|" in line and "|changed=none|" in line for line in gates) and any(line.startswith("rustc 1.81.0 ") for line in gates))
crs = {}
for rel in ("tests/one_scale_replay.py", "tests/test_one_scale_blocking.py", "tests/ONE_SCALE_BLOCKING_BRACKETS.hbp", ".github/workflows/one-scale-blocking.yml"):
    with open(os.path.join(REPO, rel), "rb") as handle:
        crs[rel] = handle.read().count(b"\r")
for folder, dirs, files in os.walk(FOLDER):
    dirs.sort()
    for name in sorted(files):
        if name in ("MEASURE.hbp", "VERIFY.hbp", "INDEX.hbi", "SHA256SUMS", "SEAL.hbp"):
            continue
        with open(os.path.join(folder, name), "rb") as handle:
            crs[os.path.relpath(os.path.join(folder, name), FOLDER)] = handle.read().count(b"\r")
emit("GATES|steps=%d|all_ok=%d|carriage_returns=%d|files_read_for_cr=%d" % (len(gate_steps), gate_ok, sum(crs.values()), len(crs)))

# ---- The predictions, read.
pred = {}
for line in open(os.path.join(FOLDER, "PREDICTION.hbp"), encoding="utf-8").read().split("\n"):
    if line.startswith("P|"):
        f = fields(line)
        pred[f["id"]] = f


def in_range(pid, value):
    p = pred[pid]
    return int(p["low"]) <= value <= int(p["high"])


a1, a2 = done_rows["A1"], done_rows["A2"]
names_other = [n for n in names if n != "reversed_order"]
flux_full = ("overlap_skips_next", "visibility_ignores_omega_error", "visibility_error_halved", "visibility_error_inflated", "overlap_one_power")
reads = [
    ("P01", main_same["A1"] and main_same["A2"], "A1=%d,A2=%d" % (main_same["A1"], main_same["A2"])),
    ("P02", all(d["sections"] == "16" and d["brackets"] == "44" and d["seeded"] == "44" and d["bisected"] == "0" and d["crosschecked"] == "26" for d in (a1, a2)), "A1=%s,A2=%s" % ("/".join(a1[k] for k in ("sections", "brackets", "seeded", "bisected", "crosschecked")), "/".join(a2[k] for k in ("sections", "brackets", "seeded", "bisected", "crosschecked")))),
    ("P03", main_same["B0"], "B=%d" % main_same["B0"]),
    ("P04", len(A["A1"]) == 7 and len(A["A2"]) == 7 and all(s["rc"] == 0 for t in A.values() for s in t.values()) and b_rc == 6, "A1=%d,A2=%d,B=%d_with_B_scripts_%d" % (sum(1 for s in A["A1"].values() if s["rc"] == 0), sum(1 for s in A["A2"].values() if s["rc"] == 0), b_rc, len(B_LABELS))),
    ("P05", len(names) == 15 and all(per[n]["row"][l]["rc"] == 1 and per[n]["row"][l]["named"] == 1 and per[n]["row"][l]["traceback"] == 0 and per[n]["row"][l]["replay_failed"] == 0 for n in names for l in ("A1", "A2")) and len(b_calls) == 16 and b_ok == 16, "A_names=%d,B_invocations_ok=%d" % (len(names), b_ok)),
    ("P06", identical == 15, "identical=%d" % identical),
    ("P07", all(per["reversed_order"]["row"][l]["computed"] == 3 and per["reversed_order"]["row"][l]["reused"] == 13 for l in ("A1", "A2")) and all(per[n]["row"][l]["computed"] == 1 and per[n]["row"][l]["reused"] == 15 for n in names_other for l in ("A1", "A2")) and all(per[n]["row"][l]["computed"] == per[n]["row"][l]["computed_reached"] for n in names for l in ("A1", "A2")), "see_SABOTAGE_rows"),
    ("P08", all((per["flux_wrong_sign"]["row"][l]["certified"], per["flux_wrong_sign"]["row"][l]["bisected"]) == (40, 4) for l in ("A1", "A2")) and all((per[n]["row"][l]["certified"], per[n]["row"][l]["bisected"]) == (44, 0) for n in flux_full for l in ("A1", "A2")) and all((per["twist_every_link"]["row"][l]["certified"], per["twist_every_link"]["row"][l]["bisected"]) == (0, 0) for l in ("A1", "A2")), "see_SABOTAGE_rows"),
    ("P09", all(ctl[l]["rc"] == 0 and len(ctl[l]["refused"]) == 4 and ctl[l]["reuse"] == 1 for l in ("A1", "A2")), "A1=%d+%d,A2=%d+%d" % (len(ctl["A1"]["refused"]), ctl["A1"]["reuse"], len(ctl["A2"]["refused"]), ctl["A2"]["reuse"])),
    ("P10", unk["A1"] == 0 and unk["A2"] == 0, "A1_step_rc=%d,A2_step_rc=%d" % (unk["A1"], unk["A2"])),
    ("P11", in_range("P11", local_sab), "x1000=%d" % local_sab),
    ("P12", in_range("P12", local_main), "x1000=%d" % local_main),
    ("P13", in_range("P13", h1_after), "ms=%d" % h1_after),
    ("P14", in_range("P14", h2_ratio), "x1000=%d" % h2_ratio),
    ("P15", in_range("P15", h3_ratio), "x1000=%d" % h3_ratio),
    ("P16", h1_ratio >= 8700 and h2_ratio >= 8700, "H1=%d,H2=%d" % (h1_ratio, h2_ratio)),
    ("P17", in_range("P17", job_ratio), "x1000=%d" % job_ratio),
    ("P18", x1_same == 1 and x1_done["seeded"] == "0" and x1_done["bisected"] == "44", "stdout_is_receipt=%d,seeded=%s,bisected=%s" % (x1_same, x1_done["seeded"], x1_done["bisected"])),
    ("P19", gate_ok == 1, "all_ok=%d" % gate_ok),
    ("P20", sum(crs.values()) == 0, "carriage_returns=%d" % sum(crs.values())),
]
pred_p = {}
for line in open(os.path.join(FOLDER, "PREDICTION-P.hbp"), encoding="utf-8").read().split("\n"):
    if line.startswith("P|"):
        f = fields(line)
        pred_p[f["id"]] = f


def in_p(pid, value):
    return int(pred_p[pid]["low"]) <= value <= int(pred_p[pid]["high"])


reads += [
    ("Q1", in_p("Q1", fb * 1000 // fa), "x1000=%d" % (fb * 1000 // fa)),
    ("Q2", in_p("Q2", db * 1000 // da), "x1000=%d" % (db * 1000 // da)),
    ("Q3", in_p("Q3", h4_ratio), "x1000=%d" % h4_ratio),
    ("Q4", q4, "all=%d" % int(q4)),
]
met = 0
for pid, ok, value in reads:
    met += int(bool(ok))
    emit("READ|id=%s|measured=%s|result=%s" % (pid, value, "MET" if ok else "MISS"))
emit("READ_DONE|predictions=%d|met=%d|missed=%d" % (len(reads), met, len(reads) - met))
sys.stdout.write("\n".join(OUT) + "\n")
