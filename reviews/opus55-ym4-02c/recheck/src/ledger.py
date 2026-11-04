#!/usr/bin/env python3
"""Hot-path rows of this recheck, one per file, with size and sha256, and a sidecar. Integers only, json=0."""
import hashlib
import os

R = r"C:/tmp/opus55/recheck-02c-20261103"
names = []
for sub in ("src", "rust", "mut", "out", "run"):
    for d, _, fs in os.walk(os.path.join(R, sub)):
        rel = os.path.relpath(d, R).replace("\\", "/")
        if rel.startswith("mut/out") or rel.startswith("mut/old"):
            continue
        for f in sorted(fs):
            if f.endswith((".pdb", ".lf")) or f == "__pycache__" or d.endswith("__pycache__"):
                continue
            names.append(rel + "/" + f)
rows = ["RECHECK_HEAD|head=c32087a3f2c54412bb3028f7d0a53b8b63d6133c|branch=ym4-02c-reflection-transfer|seat=second_seat|json=0"]
for n in sorted(names):
    b = open(os.path.join(R, n), "rb").read()
    rows.append("RECHECK_FILE|path=%s|bytes=%d|sha256=%s|json=0" % (n, len(b), hashlib.sha256(b).hexdigest()))
text = "\n".join(rows) + "\n"
path = os.path.join(R, "RECHECK_FILES.hbp")
with open(path, "w", newline="\n") as f:
    f.write(text)
digest = hashlib.sha256(text.encode("utf8")).hexdigest()
with open(path + ".sha256", "w", newline="\n") as f:
    f.write(digest + "\n")
print(len(rows) - 1, digest)
