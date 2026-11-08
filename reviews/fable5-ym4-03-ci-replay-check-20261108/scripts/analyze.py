"""Read this lane's runs into result rows: the main step, the index against the lane's, each sabotage read, replay against full run, and timing.

usage = python3 -I -B -X utf8 analyze.py BASE OUT
Integers only: every ratio is kept as x1000 by integer division, json=0.
"""
import hashlib
import os
import sys

BASE, OUT = sys.argv[1], sys.argv[2]
W = os.path.join(BASE, "work")
REPO = os.path.join(BASE, "repo")
LANE_A1 = "/mnt/c/tmp/opus55/ym4d-ci-replay-20261106/repo/reviews/fable5-ym4-03-ci-replay-20261106/raw/A1/ym4-03-cache/REPLAY-INDEX.hbp"
STDERR_HEADS = ("SECTION|", "REPLAY|", "REPLAY_START|", "REPLAY_DONE|", "REPLAY_REFUSED|", "REPLAY_NOT_READY|", "REPLAY_INDEX|")
NAMES = ["reversed_order", "shifted_endpoint", "dropped_inverse", "theta_no_inverse", "wrong_convolution_power", "wrong_first_coefficient",
         "extra_plaquette_factor", "wrong_block_shell", "twist_every_link", "flux_wrong_sign", "overlap_skips_next", "visibility_ignores_omega_error",
         "visibility_error_halved", "visibility_error_inflated", "overlap_one_power"]
ROWS = []


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    with open(path, "rb") as handle:
        return handle.read()


def field(line, key):
    for part in line.split("|"):
        if part.startswith(key + "="):
            return part[len(key) + 1:]
    return None


def stdout_only(data):
    return b"".join(line for line in data.splitlines(keepends=True) if not line.decode("utf-8", "replace").startswith(STDERR_HEADS))


def timed_rows(path):
    out = []
    if os.path.exists(path):
        for line in read(path).decode("utf-8").split("\n"):
            if line.startswith("TIMED|"):
                out.append({k: field(line, k) for k in ("label", "rc", "wall_ms", "cpu_ms", "load_start", "load_end")})
    return out


def emit(row):
    ROWS.append(row)
    print(row)


def main_step():
    receipt = read(os.path.join(REPO, "tests", "ONE_SCALE_BLOCKING_RECEIPT.txt"))
    for label, folder in (("A", "runA"), ("B", "runB")):
        out = read(os.path.join(W, folder, "blocking.out"))
        emit("MAIN_STEP|side=%s|bytes=%d|sha256=%s|equal_to_receipt=%d|receipt_bytes=%d|receipt_sha256=%s|json=0" % (label, len(out), sha(out), int(out == receipt), len(receipt), sha(receipt)))
    err = read(os.path.join(W, "runA", "ym4-03-cache", "REPLAY-INDEX.hbp")).decode("utf-8")
    done = [line for line in err.split("\n") if line.startswith("REPLAY_DONE|")]
    emit("MAIN_STEP_REPLAY_DONE|%s" % (done[0][len("REPLAY_DONE|"):] if done else "missing=1|json=0"))


def index_rows(path):
    rows = []
    for line in read(path).decode("utf-8").split("\n"):
        if not line:
            continue
        rows.append("|".join(part for part in line.split("|") if not part.startswith("ms=") and not part.startswith("path=")))
    return rows


def index_compare():
    mine = index_rows(os.path.join(W, "runA", "ym4-03-cache", "REPLAY-INDEX.hbp"))
    lane = index_rows(LANE_A1)
    differ = [k for k in range(max(len(mine), len(lane))) if k >= len(mine) or k >= len(lane) or mine[k] != lane[k]]
    emit("INDEX_COMPARE|mine_rows=%d|lane_rows=%d|rows_differing_without_ms=%d|first=%s|json=0" % (len(mine), len(lane), len(differ), ",".join(str(k + 1) for k in differ[:5]) or "none"))


def reach_of_index():
    out = {}
    for line in read(os.path.join(W, "runA", "ym4-03-cache", "REPLAY-INDEX.hbp")).decode("utf-8").split("\n"):
        if line.startswith("REPLAY_SECTION|"):
            reach = field(line, "reach")
            out[field(line, "section")] = set() if reach == "none" else set(reach.split(","))
    return out


def sabotage_reads():
    reach = reach_of_index()
    receipt = read(os.path.join(REPO, "tests", "ONE_SCALE_BLOCKING_RECEIPT.txt"))
    timings = {}
    for lane in ("lane1", "lane2"):
        for row in timed_rows(os.path.join(W, "T", lane + ".hbp")):
            timings.setdefault(row["label"].split("-", 1)[0], []).append(row)
    a_rc = {}
    for row in timings.get("A", []):
        a_rc[row["label"].split("-", 3)[3].rsplit("-", 1)[0]] = int(row["rc"])
    identical = 0
    for name in NAMES:
        path_a = os.path.join(W, "runA", "sab-%s.out" % name)
        path_b = os.path.join(W, "runB", "sab-%s.out" % name)
        if not (os.path.exists(path_a) and os.path.exists(path_b)):
            emit("SABOTAGE_READ|name=%s|missing=1|json=0" % name)
            continue
        a, b = read(path_a), read(path_b)
        text = a.decode("utf-8")
        computed = [field(line, "section") for line in text.split("\n") if line.startswith("REPLAY|") and "|mode=computed|" in line]
        reused = [field(line, "section") for line in text.split("\n") if line.startswith("REPLAY|") and "|mode=reused|" in line]
        wanted = sorted(s for s, r in reach.items() if name in r)
        outside = [s for s in computed if name not in reach.get(s, set())]
        done = [line for line in text.split("\n") if line.startswith("REPLAY_DONE|")]
        same = stdout_only(a) == stdout_only(b)
        identical += int(same)
        emit("SABOTAGE_READ|name=%s|step_rc=%s|computed=%s|reused=%d|index_reach_sections=%s|computed_equals_reach=%d|computed_outside_reach=%d|brackets_certified=%s|brackets_bisected=%s|replay_stdout_bytes=%d|full_stdout_bytes=%d|replay_equals_full=%d|replay_stdout_sha256=%s|full_stdout_sha256=%s|stdout_equals_receipt=%d|json=0" % (
            name, a_rc.get(name, "unknown"), ",".join(computed) or "none", len(reused), ",".join(wanted) or "none", int(sorted(computed) == wanted), len(outside),
            field(done[0], "brackets_certified") if done else "missing", field(done[0], "brackets_bisected") if done else "missing",
            len(stdout_only(a)), len(stdout_only(b)), int(same), sha(stdout_only(a)), sha(stdout_only(b)), int(stdout_only(a) == receipt)))
    emit("SABOTAGE_READ_DONE|names=%d|replay_equals_full=%d|json=0" % (len(NAMES), identical))


def ratio(num, den):
    return num * 1000 // den if den else -1


def timing():
    rows = []
    for lane in ("lane1", "lane2"):
        rows += timed_rows(os.path.join(W, "T", lane + ".hbp"))
    sums = {"A": [0, 0, 0], "B": [0, 0, 0]}
    per = {}
    for row in rows:
        side = row["label"][0]
        name = row["label"].split("-", 3)[3].rsplit("-", 1)[0]
        sums[side][0] += int(row["wall_ms"])
        sums[side][1] += int(row["cpu_ms"])
        sums[side][2] += 1
        entry = per.setdefault(name, {"A": [0, 0], "B": [0, 0]})
        entry[side][0] += int(row["wall_ms"])
        entry[side][1] += int(row["cpu_ms"])
    for name in NAMES:
        if name in per:
            e = per[name]
            emit("PAIR|name=%s|before_wall_ms=%d|after_wall_ms=%d|wall_x1000=%d|before_cpu_ms=%d|after_cpu_ms=%d|cpu_x1000=%d|json=0" % (
                name, e["B"][0], e["A"][0], ratio(e["B"][0], e["A"][0]), e["B"][1], e["A"][1], ratio(e["B"][1], e["A"][1])))
    emit("SABOTAGE_STEP|before_calls=%d|after_calls=%d|before_wall_ms=%d|after_wall_ms=%d|wall_x1000=%d|before_cpu_ms=%d|after_cpu_ms=%d|cpu_x1000=%d|json=0" % (
        sums["B"][2], sums["A"][2], sums["B"][0], sums["A"][0], ratio(sums["B"][0], sums["A"][0]), sums["B"][1], sums["A"][1], ratio(sums["B"][1], sums["A"][1])))
    hosted_before = HOSTED_MS
    emit("HOSTED_PROJECTION|hosted_before_ms=%d|after_by_cpu_ms=%d|after_by_wall_ms=%d|claimed_after_ms=293000|claimed_x1000=%d|json=0" % (
        hosted_before, hosted_before * sums["A"][1] // sums["B"][1] if sums["B"][1] else -1, hosted_before * sums["A"][0] // sums["B"][0] if sums["B"][0] else -1, ratio(hosted_before, 293000)))
    main = {r["label"]: r for r in timed_rows(os.path.join(W, "T", "phase1-main.hbp"))}
    if "A-step-4" in main and "B-step-4" in main:
        a, b = main["A-step-4"], main["B-step-4"]
        emit("MAIN_STEP_TIME|record_wall_ms=%s|plain_wall_ms=%s|wall_x1000=%d|record_cpu_ms=%s|plain_cpu_ms=%s|cpu_x1000=%d|json=0" % (
            a["wall_ms"], b["wall_ms"], ratio(int(a["wall_ms"]), int(b["wall_ms"])), a["cpu_ms"], b["cpu_ms"], ratio(int(a["cpu_ms"]), int(b["cpu_ms"]))))
        others_a = sum(int(r["cpu_ms"]) for r in timed_rows(os.path.join(W, "T", "phase1.hbp")) + timed_rows(os.path.join(W, "T", "phase2-tail.hbp")) if r["label"].startswith("A-") and r["rc"] == "0")
        others_b = sum(int(r["cpu_ms"]) for r in timed_rows(os.path.join(W, "T", "phase1.hbp")) + timed_rows(os.path.join(W, "T", "phase2-tail.hbp")) if (r["label"].startswith("B-step-1") or r["label"].startswith("B-step-2") or r["label"] == "B-step-3-clone" or r["label"] == "B-step-6") and r["rc"] == "0")
        job_a = others_a + int(a["cpu_ms"]) + sums["A"][1]
        job_b = others_b + int(b["cpu_ms"]) + sums["B"][1]
        emit("JOB_CPU|before_ms=%d|after_ms=%d|x1000=%d|other_steps_before_ms=%d|other_steps_after_ms=%d|json=0" % (job_b, job_a, ratio(job_b, job_a), others_b, others_a))
        # DERIVED: the hosted job with its main step scaled by record over plain CPU, its sabotage step by after over before CPU, and the branch's
        # added control steps scaled by the hosted main step over the local plain main step.
        hosted_job, hosted_main = HOSTED["job_ms"], HOSTED["main_ms"]
        added_a = sum(int(r["cpu_ms"]) for r in timed_rows(os.path.join(W, "T", "phase2-tail.hbp")) if r["label"] in ("A-step-6", "A-step-7"))
        added_b = sum(int(r["cpu_ms"]) for r in timed_rows(os.path.join(W, "T", "phase2-tail.hbp")) if r["label"] == "B-step-6")
        rest = hosted_job - hosted_before - hosted_main
        main_after = hosted_main * int(a["cpu_ms"]) // int(b["cpu_ms"])
        sab_after = hosted_before * sums["A"][1] // sums["B"][1]
        controls = (added_a - added_b) * hosted_main // int(b["cpu_ms"])
        job_after = rest + main_after + sab_after + controls
        emit("HOSTED_JOB_PROJECTION|hosted_job_ms=%d|rest_ms=%d|main_after_ms=%d|sabotage_after_ms=%d|added_controls_ms=%d|job_after_ms=%d|x1000=%d|json=0" % (
            hosted_job, rest, main_after, sab_after, controls, job_after, ratio(hosted_job, job_after)))


def stamp_100ns(text):
    """2026-11-06T00:45:32.4517526Z as an integer count of 100 ns within the day; the run stays inside one day."""
    clock = text.split("T", 1)[1].rstrip("Z")
    hms, frac = clock.split(".")
    h, m, s = (int(x) for x in hms.split(":"))
    return ((h * 60 + m) * 60 + s) * 10000000 + int((frac + "0000000")[:7])


def hosted():
    path = os.path.join(REPO, "reviews", "fable5-ym4-03-ci-replay-20261106", "hosted", "run-42138789854.log")
    lines = read(path).decode("utf-8").split("\n")
    groups = [(k, stamp_100ns(line.split("\t")[2].split(" ", 1)[0])) for k, line in enumerate(lines) if "##[group]Run " in line]
    for n, (k, t) in enumerate(groups):
        block = "\n".join(lines[k:groups[n + 1][0]]) if n + 1 < len(groups) else ""
        if "read_sabotage()" in block and n + 1 < len(groups):
            ms = (groups[n + 1][1] - t) // 10000
            emit("HOSTED_STEP|log_sha256=%s|sabotage_step_ms=%d|echo_lines=%d|json=0" % (sha(read(path)), ms, block.count("exit=1 ")))
            return ms
        if "tests/test_one_scale_blocking.py > /tmp/blocking.out" in block and n + 1 < len(groups):
            HOSTED["main_ms"] = (groups[n + 1][1] - t) // 10000
            emit("HOSTED_MAIN_STEP|main_step_ms=%d|json=0" % HOSTED["main_ms"])
    return -1


def hosted_job():
    path = os.path.join(REPO, "reviews", "fable5-ym4-03-ci-replay-20261106", "hosted", "run-42138789854.log")
    lines = [line for line in read(path).decode("utf-8").split("\n") if line.count("\t") >= 2]
    first = stamp_100ns(lines[0].split("\t")[2].lstrip("﻿").split(" ", 1)[0])
    last = stamp_100ns(lines[-1].split("\t")[2].lstrip("﻿").split(" ", 1)[0])
    HOSTED["job_ms"] = (last - first) // 10000
    emit("HOSTED_JOB|job_ms=%d|json=0" % HOSTED["job_ms"])


def proposed():
    """The proposal's workflow, run in its clone: each step's exit code, its main step against the receipt, the index against the branch's
    without ms and paths, each sabotage's stdout against the branch replay's, and the line its new control must print."""
    steps = timed_rows(os.path.join(W, "T", "proposed.hbp"))
    if not steps:
        return
    receipt = read(os.path.join(REPO, "tests", "ONE_SCALE_BLOCKING_RECEIPT.txt"))

    def bare(path):
        return [line for line in (("|".join(p for p in line.split("|") if not p.startswith("ms=") and not p.startswith("path="))) for line in read(path).decode("utf-8").split("\n")) if line]

    same = 0
    for name in NAMES:
        own = "sab-%s-rerun.out" % name if name == "reversed_order" else "sab-%s.out" % name
        same += int(stdout_only(read(os.path.join(W, "runP", own))) == stdout_only(read(os.path.join(W, "runA", "sab-%s.out" % name))))
    control = read(os.path.join(W, "logs", "P-step-5.out")).decode("utf-8")
    emit("PROPOSED_RUN|steps=%s|main_equals_receipt=%d|index_equals_branch=%d|sabotage_stdout_equal_to_branch=%d_of_15|control_refused=%d|reversed_order_read_from_its_rerun=1|json=0" % (
        ",".join("%s:%s" % (r["label"], r["rc"]) for r in steps), int(read(os.path.join(W, "runP", "blocking.out")) == receipt),
        int(bare(os.path.join(W, "runP", "ym4-03-cache", "REPLAY-INDEX.hbp")) == bare(os.path.join(W, "runA", "ym4-03-cache", "REPLAY-INDEX.hbp"))),
        same, int("sabotage=reversed_order reused section_loops, which the index says it reaches" in control)))


HOSTED = {}
main_step()
HOSTED_MS = hosted()
hosted_job()
index_compare()
sabotage_reads()
timing()
proposed()
with open(OUT, "w", encoding="utf-8", newline="\n") as handle:
    handle.write("\n".join(ROWS) + "\n")
