"""Run workflow step files with wall time and child CPU time, both integers.

usage = python3 -I -B -X utf8 run_timed.py one LABEL CWD SCRIPT ROWFILE LOGDIR
        python3 -I -B -X utf8 run_timed.py pairs ROWFILE LOGDIR A_CWD A_CALLS B_CWD B_CALLS FIRST NAME...
one runs bash --noprofile --norc -eo pipefail SCRIPT in CWD, as GitHub runs a run step, and appends a TIMED row. pairs runs, for each NAME in turn,
the bf58ab2 calls of that name (B_CALLS/call-NN-NAME.sh, one or more) and the branch call (A_CALLS/call-NN-NAME.sh) back to back; the order is
B then A for the first name when FIRST=B, and it alternates name by name. Wall time from perf_counter_ns, CPU from cutime+cstime of
/proc/self/stat in clock ticks, the load average kept as its text. Integers only, json=0.
"""
import os
import subprocess
import sys
import time

TICK = os.sysconf("SC_CLK_TCK")


def child_ticks():
    with open("/proc/self/stat", encoding="utf-8") as handle:
        text = handle.read()
    rest = text[text.rindex(")") + 2:].split()
    return int(rest[13]) + int(rest[14])


def load_text():
    with open("/proc/loadavg", encoding="utf-8") as handle:
        return handle.read().split()[0]


def one(label, cwd, script, rowfile, logdir):
    os.makedirs(logdir, exist_ok=True)
    load0 = load_text()
    c0 = child_ticks()
    t0 = time.perf_counter_ns()
    with open(os.path.join(logdir, label + ".out"), "wb") as out, open(os.path.join(logdir, label + ".err"), "wb") as err:
        rc = subprocess.call(["bash", "--noprofile", "--norc", "-eo", "pipefail", script], cwd=cwd, stdout=out, stderr=err)
    t1 = time.perf_counter_ns()
    c1 = child_ticks()
    row = "TIMED|label=%s|rc=%d|wall_ms=%d|cpu_ms=%d|load_start=%s|load_end=%s|script=%s|cwd=%s|start_ns=%d|json=0" % (
        label, rc, (t1 - t0) // 1000000, (c1 - c0) * 1000 // TICK, load0, load_text(), script, cwd, t0)
    with open(rowfile, "a", encoding="utf-8", newline="\n") as handle:
        handle.write(row + "\n")
    print(row, flush=True)
    return rc


def calls_of(folder, name):
    out = []
    for entry in sorted(os.listdir(folder)):
        if entry.startswith("call-") and entry.endswith(".sh") and entry[len("call-NN-"):-3] == name:
            out.append(os.path.join(folder, entry))
    return out


def pairs(rowfile, logdir, a_cwd, a_calls, b_cwd, b_calls, first, names):
    for k, name in enumerate(names):
        b_first = (first == "B") == (k % 2 == 0)
        a_list, b_list = calls_of(a_calls, name), calls_of(b_calls, name)
        if len(a_list) != 1 or not b_list:
            print("PAIR_REFUSED|name=%s|a=%d|b=%d|json=0" % (name, len(a_list), len(b_list)), flush=True)
            sys.exit(1)
        plan = ([("B", p) for p in b_list] + [("A", a_list[0])]) if b_first else ([("A", a_list[0])] + [("B", p) for p in b_list])
        for side, path in plan:
            label = "%s-%s-%s" % (side, os.path.basename(path)[:-3], "first" if (side == "B") == b_first else "second")
            one(label, a_cwd if side == "A" else b_cwd, path, rowfile, logdir)


def main():
    if sys.argv[1] == "one":
        sys.exit(one(*sys.argv[2:7]))
    if sys.argv[1] == "pairs":
        pairs(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9:])
        return
    sys.exit(2)


main()
