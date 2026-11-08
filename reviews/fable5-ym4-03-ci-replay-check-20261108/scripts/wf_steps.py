"""Write each run step of a workflow as a bash file, /tmp/ moved into a run folder of this lane.

usage = python3 -I -B -X utf8 wf_steps.py WORKFLOW RUNDIR OUTDIR
OUTDIR/step-K.sh holds the run text of step K with every "/tmp/" replaced by RUNDIR + "/"; OUTDIR/STEPS.hbp names each step with the sha256 of its
original run text and of the written file. A sabotage step is also split: OUTDIR/sab-prelude.sh is its text up to the first read_sabotage call, and
OUTDIR/call-NN-NAME.sh is the prelude with one call line. The workflow is read by wfread.py beside this file. Integers only, json=0.
"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wfread  # noqa: E402


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    workflow, rundir, outdir = sys.argv[1], sys.argv[2].rstrip("/"), sys.argv[3]
    os.makedirs(outdir, exist_ok=True)
    data = wfread.read_workflow(workflow)
    rows = []
    k = 0
    for job_name, steps in data["jobs"]:
        for step in steps:
            if "run" not in step:
                continue
            k += 1
            text = step["run"]
            moved = text.replace("/tmp/", rundir + "/")
            path = os.path.join(outdir, "step-%d.sh" % k)
            with open(path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(moved)
            rows.append("STEP|k=%d|job=%s|name=%s|run_sha256=%s|file_sha256=%s|json=0" % (k, job_name, step["name"].replace("|", "_"), sha(text), sha(moved)))
            lines = moved.split("\n")
            calls = [i for i, line in enumerate(lines) if line.startswith("read_sabotage ")]
            if calls:
                prelude = "\n".join(lines[:calls[0]]) + "\n"
                with open(os.path.join(outdir, "sab-prelude.sh"), "w", encoding="utf-8", newline="\n") as handle:
                    handle.write(prelude)
                for n, i in enumerate(calls):
                    name = lines[i].split()[1]
                    call_path = os.path.join(outdir, "call-%02d-%s.sh" % (n + 1, name))
                    with open(call_path, "w", encoding="utf-8", newline="\n") as handle:
                        handle.write(prelude + lines[i] + "\n")
                    rows.append("CALL|step=%d|n=%d|name=%s|line_sha256=%s|json=0" % (k, n + 1, name, sha(lines[i])))
                tail = [line for line in lines[calls[-1] + 1:] if line.strip()]
                rows.append("SPLIT|step=%d|calls=%d|prelude_lines=%d|after_last_call=%d|json=0" % (k, len(calls), calls[0], len(tail)))
    with open(os.path.join(outdir, "STEPS.hbp"), "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(rows) + "\n")
    print("\n".join(rows))


main()
