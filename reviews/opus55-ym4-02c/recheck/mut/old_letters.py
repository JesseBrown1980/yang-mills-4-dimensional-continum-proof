#!/usr/bin/env python3
"""The builder's statement about commit 1618199: the third-letter mutant fails the six REFLECTION rows, the fourth-letter mutant leaves them unchanged and crashes at GRAM_LINK. Run on the blob at 1618199. Integers only, json=0."""
import os
import subprocess
import sys

ROOT = r"C:/tmp/opus55/attack-4d-02c-20261103"
OUT = r"C:/tmp/opus55/recheck-02c-20261103/mut/old"
os.makedirs(OUT, exist_ok=True)
SRC = open(os.path.join(ROOT, "run", "t.py"), "rb").read().decode("utf8")
RECEIPT = open(os.path.join(ROOT, "run", "receipt.txt"), "rb").read()
WORD = "return (((x, mu), 1), ((self.shift(x, mu), nu), 1), ((self.shift(x, nu), mu), -1), ((x, nu), -1))"
assert SRC.count(WORD) == 1
for name, new in (("third_letter", "return (((x, mu), 1), ((self.shift(x, mu), nu), 1), ((self.shift(x, nu), mu), 1), ((x, nu), -1))"),
                  ("fourth_letter", "return (((x, mu), 1), ((self.shift(x, mu), nu), 1), ((self.shift(x, nu), mu), -1), ((x, nu), 1))")):
    path = os.path.join(OUT, name + ".py")
    with open(path, "wb") as f:
        f.write(SRC.replace(WORD, new).encode("utf8"))
    p = subprocess.run([sys.executable, "-I", "-X", "utf8", path], capture_output=True)
    out = p.stdout.replace(b"\r", b"").decode("utf8")
    failed = [ln.split("check=")[1].split("|")[0] for ln in out.splitlines() if ln.startswith("FAILED|")]
    rows = out.splitlines()
    base = RECEIPT.decode("utf8").splitlines()
    changed = [b.split("|")[0] for a, b in zip(rows, base) if a != b]
    err = p.stderr.decode("utf8", "replace").strip().splitlines()
    print("OLD_MUTANT|name=%s|exit=%d|rows_printed=%d|of=%d|named_failures=%d|checks=%s|changed_rows=%s|last_row=%s|stderr_last=%s|json=0" % (
        name, p.returncode, len(rows), len(base), len(failed), ",".join(failed), ",".join(changed), rows[-1].split("|")[0] if rows else "", err[-1][:100] if err else ""))
