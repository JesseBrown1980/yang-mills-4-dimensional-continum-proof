#!/usr/bin/env python3
"""One row per file of this recheck, size and sha256, hot path first, json=0. The mutant copies under mut/out regenerate from src/mut_last.py and the blob run/t.py."""
import hashlib, os, sys
root = "C:/tmp/opus55/recheck-02c-20261103/last"
rows = []
for base, dirs, files in os.walk(root):
    rel = os.path.relpath(base, root).replace(os.sep, "/")
    if rel.startswith("mut/out") or rel == "src/__pycache__" or "__pycache__" in rel:
        continue
    for f in sorted(files):
        if f.startswith("LAST_FILES"):
            continue
        p = os.path.join(base, f)
        data = open(p, "rb").read()
        path = f if rel == "." else rel + "/" + f
        rows.append("LAST_FILE|%s|bytes=%d|sha256=%s|json=0" % (path, len(data), hashlib.sha256(data).hexdigest()))
rows.sort()
head = "LAST_FILES|head=b3025496309fa6a8132ed11d2f95c10db7460ff7|files=%d|seat=second_seat|json=0" % len(rows)
text = "\n".join([head] + rows) + "\n"
out = os.path.join(root, "LAST_FILES.hbp")
open(out, "w", encoding="utf8", newline="\n").write(text)
open(out + ".sha256", "w", encoding="utf8", newline="\n").write(hashlib.sha256(text.encode("utf8")).hexdigest() + "\n")
print(head)
