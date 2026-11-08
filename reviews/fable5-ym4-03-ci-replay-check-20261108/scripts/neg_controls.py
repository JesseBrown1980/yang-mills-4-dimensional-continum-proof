"""Line by line: every line of the bf58ab2 workflow's run steps, and where it stands in the branch's workflow.

usage = python3 -I -B -X utf8 neg_controls.py MAIN_WORKFLOW BRANCH_WORKFLOW OUT
Each run line of the main workflow, stripped of leading spaces, is SAME when the branch holds the identical line in the step of the same name, MOVED
when the branch holds it in another step, and REWRITTEN otherwise. Each read_sabotage call of the main workflow is matched with the branch call of
the same sabotage name and the named check is looked for in the branch call's arguments. Every trigger path of main is looked for in the branch.
The workflows are read by wfread.py beside this file.
Integers only, json=0.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wfread  # noqa: E402


def steps_of(path):
    data = wfread.read_workflow(path)
    out = []
    for _, steps in data["jobs"]:
        for step in steps:
            if "run" in step:
                out.append((step["name"], [line.strip() for line in step["run"].split("\n") if line.strip()]))
    return data, out


def calls(lines):
    out = []
    for line in lines:
        if line.startswith("read_sabotage "):
            words = line.split()[:2] + re.findall("'([^']*)'", line)
            out.append((words[1], words[2:]))
    return out


def main():
    main_data, main_steps = steps_of(sys.argv[1])
    branch_data, branch_steps = steps_of(sys.argv[2])
    rows = []
    by_name = {name: lines for name, lines in branch_steps}
    every_branch = {line for _, lines in branch_steps for line in lines}
    counts = {"SAME": 0, "MOVED": 0, "REWRITTEN": 0}
    for k, (name, lines) in enumerate(main_steps, 1):
        own = by_name.get(name, [])
        for n, line in enumerate(lines, 1):
            status = "SAME" if line in own else ("MOVED" if line in every_branch else "REWRITTEN")
            counts[status] += 1
            rows.append("LINE|step=%d|n=%d|status=%s|step_name_in_branch=%d|text=%s|json=0" % (k, n, status, int(name in by_name), line.replace("|", "\\x7c")))
    main_calls = [c for _, lines in main_steps for c in calls(lines)]
    branch_calls = [c for _, lines in branch_steps for c in calls(lines)]
    branch_named = {}
    for sabotage, named in branch_calls:
        branch_named.setdefault(sabotage, set()).update(named)
    kept = 0
    for sabotage, named in main_calls:
        ok = all(item in branch_named.get(sabotage, set()) for item in named)
        kept += int(ok)
        rows.append("CALL|sabotage=%s|named=%s|in_branch=%d|json=0" % (sabotage, ";".join(named), int(ok)))
    main_on = main_data["on"]
    branch_on = branch_data["on"]
    for event in ("push", "pull_request"):
        main_paths = main_on[event].get("paths", [])
        branch_paths = branch_on[event].get("paths", [])
        missing = [p for p in main_paths if p not in branch_paths]
        added = [p for p in branch_paths if p not in main_paths]
        rows.append("TRIGGER|event=%s|main_paths=%d|branch_paths=%d|missing=%s|added=%s|main_branches=%s|branch_branches=%s|json=0" % (
            event, len(main_paths), len(branch_paths), ",".join(missing) or "none", ",".join(added) or "none",
            ",".join(main_on[event].get("branches", [])) or "any", ",".join(branch_on[event].get("branches", [])) or "any"))
    rows.append("NEG_CONTROLS_DONE|main_lines=%d|same=%d|moved=%d|rewritten=%d|main_calls=%d|calls_kept=%d|branch_calls=%d|json=0" % (
        sum(counts.values()), counts["SAME"], counts["MOVED"], counts["REWRITTEN"], len(main_calls), kept, len(branch_calls)))
    with open(sys.argv[3], "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(rows) + "\n")
    print("\n".join(rows))


main()
