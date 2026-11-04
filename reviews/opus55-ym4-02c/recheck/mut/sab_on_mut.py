#!/usr/bin/env python3
"""What the sabotages read when a piece of the new row is removed. Each mutant is applied to a private copy and only the named sabotage runs, so each takes seconds. Integers only, json=0."""
import os
import subprocess
import sys

R = r"C:/tmp/opus55/recheck-02c-20261103"
SRC = open(R + "/run/t.py", "rb").read().decode("utf8")
OUT = R + "/mut/out4"
os.makedirs(OUT, exist_ok=True)
CASES = [
    ("moved_guard_removed", "if not (fixed_ok and time_ok and word_ok):", "if False:", "wrong_plane_in_gram"),
    ("moved_guard_removed", "if not (fixed_ok and time_ok and word_ok):", "if False:", "no_inverse_in_gram"),
    ("moved_mirror_ignores_sign_uses_inverse", "mirror = [bad[k] for k in inverse_position] if sign < 0 else bad", "mirror = [bad[k] for k in inverse_position]", "no_inverse_in_gram"),
    ("orientation_once_check_removed", "once = set(forward) == set(backward) and all(v == 1 for v in forward.values()) and all(v == 1 for v in backward.values())", "once = True", "dropped_inverse_fourth_letter"),
    ("orientation_closed_check_removed", "closed += 1 if ends[0][0] == x and all(ends[i][1] == ends[(i + 1) % 4][0] for i in range(4)) else 0", "closed += 1", "dropped_inverse_fourth_letter"),
    ("orientation_conjugate_check_removed", "conjugate = conjugate and holonomy(word, gauged) == qmul(qmul(gauge[p[0]], holonomy(word, field)), qinv(gauge[p[0]]))", "conjugate = True", "dropped_inverse_fourth_letter"),
]
for name, old, new, sab in CASES:
    assert SRC.count(old) == 1
    path = "%s/%s__%s.py" % (OUT, name, sab)
    with open(path, "wb") as f:
        f.write(SRC.replace(old, new).encode("utf8"))
    p = subprocess.run([sys.executable, "-I", "-X", "utf8", path, "sabotage=" + sab], capture_output=True)
    out = p.stdout.replace(b"\r", b"").decode("utf8")
    failed = [ln.split("check=")[1].split("|")[0] for ln in out.splitlines() if ln.startswith("FAILED|")]
    print("SAB_ON_MUT|mutant=%s|sabotage=%s|exit=%d|named_failures=%d|checks=%s|traceback=%d|json=0" % (name, sab, p.returncode, len(failed), ",".join(failed), 1 if b"Traceback" in p.stderr else 0))
