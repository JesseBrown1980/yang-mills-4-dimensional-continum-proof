"""The independent replay of this folder: every byte, the prediction, and the headline numbers recomputed from the raw runs by a second reading.

usage = python3 -I -B -X utf8 VERIFY.py FOLDER
1. Every file against SHA256SUMS and INDEX.hbi (bytes, sha256, SH, carriage returns), no file unlisted, and SEAL.hbp recomputed.
2. PREDICTION.hbp against the sha256 it had when committed, before every script and run.
3. Both main-step outputs against the receipt's sha256.
4. Each sabotage: the replay's stdout against the full run's, read here from raw/sab/A and raw/sab/B with the stderr lines taken out by their
   own prefixes, and the sections the replay computed against the reach in the main step's index.
5. The timing sums and ratios from raw/T/lane1.hbp and raw/T/lane2.hbp, against RESULTS.hbp.
6. Every plant row whose expected check is named, refused by that check; and READS.hbp holding a row for every prediction.
Any changed, missing or unlisted byte, or any number that differs, exits 1. Integers only, json=0.
"""
import hashlib
import os
import sys

FOLDER = sys.argv[1]
PREDICTION_SHA256 = "22d4db4de27c2f605c396b92b246936d54e6252463284c1d6e3d4a82fe00edd3"
RECEIPT_SHA256 = "c6fbb64b30500f4f97b4cf3a508397977e6c4773182037ea820f527af8c79b8b"
OUTSIDE = ("INDEX.hbi", "SHA256SUMS", "SEAL.hbp", "VERIFY.hbp")
bad = []
out_rows = []


def h(data):
    return hashlib.sha256(data).hexdigest()


def blob(path):
    with open(os.path.join(FOLDER, path), "rb") as handle:
        return handle.read()


def fields(line):
    return dict(part.split("=", 1) for part in line.split("|")[1:] if "=" in part)


def fail(what):
    bad.append(what)
    out_rows.append("VERIFY_FAIL|what=%s|json=0" % what)


def rows_of(path, tag):
    return [fields(line) for line in blob(path).decode("utf-8").split("\n") if line.startswith(tag + "|")]


# 1. Bytes.
listed = {}
for line in blob("SHA256SUMS").decode("utf-8").split("\n"):
    if line:
        digest, path = line.split("  ", 1)
        listed[path] = digest
on_disk = set()
for top, dirs, names in os.walk(FOLDER):
    for name in names:
        path = os.path.relpath(os.path.join(top, name), FOLDER).replace(os.sep, "/")
        if path not in OUTSIDE[1:] and "__pycache__" not in path and not path.startswith(".git/"):
            on_disk.add(path)
for path in sorted(on_disk - set(listed)):
    fail("unlisted_" + path)
for path, digest in sorted(listed.items()):
    if not os.path.exists(os.path.join(FOLDER, path)):
        fail("missing_" + path)
    elif h(blob(path)) != digest:
        fail("sha256_" + path)
index_rows = rows_of("INDEX.hbi", "FILE")
for row in index_rows:
    data = blob(row["path"]) if os.path.exists(os.path.join(FOLDER, row["path"])) else b""
    if int(row["bytes"]) != len(data) or row["sha256"] != h(data) or row["sh"] != h(data)[:16] or int(row["cr"]) != data.count(b"\r") or data.count(b"\r"):
        fail("index_row_" + row["path"])
if {r["path"] for r in index_rows} | {"INDEX.hbi"} != set(listed):
    fail("index_and_sums_list_different_files")
seal = rows_of("SEAL.hbp", "SEAL")[0]
seal_text = "SEAL|label=%s|files=%d|index_sha256=%s|sha256sums_sha256=%s|json=0" % (seal["label"], len(index_rows), h(blob("INDEX.hbi")), h(blob("SHA256SUMS")))
if blob("SEAL.hbp").decode("utf-8").split("\n")[0] != seal_text or rows_of("SEAL.hbp", "SEAL_HASH")[0]["seal"] != h(seal_text.encode("utf-8")):
    fail("seal")
out_rows.append("VERIFY_BYTES|files=%d|listed=%d|seal=%s|json=0" % (len(index_rows), len(listed), h(seal_text.encode("utf-8"))[:16]))

# 2. The prediction.
if h(blob("PREDICTION.hbp")) != PREDICTION_SHA256:
    fail("prediction_sha256")

# 3. Main step.
for side in ("A", "B"):
    if h(blob("raw/main/%s-blocking.out" % side)) != RECEIPT_SHA256:
        fail("main_step_%s_not_the_receipt" % side)

# 4. Each sabotage, read again.
HEADS = ("SECTION|", "REPLAY|", "REPLAY_START|", "REPLAY_DONE|", "REPLAY_REFUSED|", "REPLAY_NOT_READY|", "REPLAY_INDEX|")


def stdout_part(data):
    return b"".join(line for line in data.splitlines(keepends=True) if not any(line.startswith(head.encode("utf-8")) for head in HEADS))


reach = {}
for row in rows_of("raw/main/A-REPLAY-INDEX.hbp", "REPLAY_SECTION"):
    reach[row["section"]] = set() if row["reach"] == "none" else set(row["reach"].split(","))
results = {}
for line in blob("RESULTS.hbp").decode("utf-8").split("\n"):
    if line.startswith("SABOTAGE_READ|"):
        results[fields(line)["name"]] = fields(line)
same_count = 0
names = sorted(name[len("sab-"):-len(".out")] for name in os.listdir(os.path.join(FOLDER, "raw", "sab", "A")))
for name in names:
    a, b = blob("raw/sab/A/sab-%s.out" % name), blob("raw/sab/B/sab-%s.out" % name)
    same = stdout_part(a) == stdout_part(b)
    same_count += int(same)
    computed = sorted(fields(line)["section"] for line in a.decode("utf-8").split("\n") if line.startswith("REPLAY|") and "|mode=computed|" in line)
    wanted = sorted(s for s, r in reach.items() if name in r)
    if name not in results or int(results[name]["replay_equals_full"]) != int(same) or int(results[name]["computed_equals_reach"]) != int(computed == wanted):
        fail("sabotage_read_" + name)
done = [fields(line) for line in blob("RESULTS.hbp").decode("utf-8").split("\n") if line.startswith("SABOTAGE_READ_DONE|")]
if not done or int(done[0]["replay_equals_full"]) != same_count:
    fail("sabotage_read_done")
out_rows.append("VERIFY_SABOTAGES|names=%d|replay_equals_full=%d|json=0" % (len(names), same_count))

# 5. Timing.
sums = {"A": [0, 0, 0], "B": [0, 0, 0]}
for lane in ("lane1", "lane2"):
    for row in rows_of("raw/T/%s.hbp" % lane, "TIMED"):
        side = row["label"][0]
        sums[side][0] += int(row["wall_ms"])
        sums[side][1] += int(row["cpu_ms"])
        sums[side][2] += 1
        if row["rc"] != "0":
            fail("timed_rc_" + row["label"])
step = [fields(line) for line in blob("RESULTS.hbp").decode("utf-8").split("\n") if line.startswith("SABOTAGE_STEP|")][0]
recomputed = {"before_wall_ms": sums["B"][0], "after_wall_ms": sums["A"][0], "before_cpu_ms": sums["B"][1], "after_cpu_ms": sums["A"][1],
              "wall_x1000": sums["B"][0] * 1000 // sums["A"][0], "cpu_x1000": sums["B"][1] * 1000 // sums["A"][1], "before_calls": sums["B"][2], "after_calls": sums["A"][2]}
for key, value in sorted(recomputed.items()):
    if int(step[key]) != value:
        fail("timing_" + key)
    out_rows.append("VERIFY_NUMBER|name=%s|replayed=%d|results_hbp=%s|same=%d|json=0" % (key, value, step[key], int(int(step[key]) == value)))

# 6. Plants and reads.
plants = rows_of("raw/plants/PLANTS.hbp", "PLANT")
named = [p for p in plants if p["expected"] != "none"]
for p in named:
    if p["refused_as_expected"] != "1":
        fail("plant_" + p["id"])
reads = rows_of("READS.hbp", "READ")
ids = {r["id"] for r in reads}
for line in blob("PREDICTION.hbp").decode("utf-8").split("\n"):
    if line.startswith("P|"):
        if fields(line)["id"] not in ids:
            fail("no_read_for_" + fields(line)["id"])
met = sum(1 for r in reads if r["result"] == "MET")
miss = [r["id"] for r in reads if r["result"] == "MISS"]
observed = [r["id"] for r in reads if r["result"] == "OBSERVED"]
out_rows.append("VERIFY_PLANTS|rows=%d|with_a_named_check=%d|refused_by_it=%d|json=0" % (len(plants), len(named), sum(1 for p in named if p["refused_as_expected"] == "1")))
out_rows.append("VERIFY_DONE|files=%d|failures=%d|reads_met=%d|reads_miss=%s|reads_observed=%s|result=%s|json=0" % (
    len(index_rows), len(bad), met, ",".join(miss) or "none", ",".join(observed) or "none", "PASS" if not bad else "FAIL"))
print("\n".join(out_rows))
sys.exit(1 if bad else 0)
