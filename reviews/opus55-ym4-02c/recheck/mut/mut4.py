#!/usr/bin/env python3
"""Recheck at c32087a: does finding 9's new route react? One text replacement each, full run, integers only, json=0."""
import os
import subprocess
import sys

R = r"C:/tmp/opus55/recheck-02c-20261103"
SRC = open(R + "/run/t.py", "rb").read().decode("utf8")
RECEIPT = open(R + "/run/receipt.txt", "rb").read()
OUT = R + "/mut/out5"
os.makedirs(OUT, exist_ok=True)
CASES = [
    ("series_half_dropped", "total = [padd(x, pmul((1, 2), y)) for x, y in zip(total, cube)]", "total = [padd(x, y) for x, y in zip(total, cube)]"),
    ("series_second_factor_wrong_index", "two = [l_coefficient(n + 1, (m - n - 1) // 2) if m >= n + 1 and (m - n - 1) % 2 == 0 else (0, 1) for m in range(degree + 1)]", "two = [l_coefficient(n, (m - n) // 2) if m >= n and (m - n) % 2 == 0 else (0, 1) for m in range(degree + 1)]"),
    ("s3_moment_wrong_denominator", "moment = pmul(moment, red(2 * i + 1, 2 * i + 4))\n    return moment", "moment = pmul(moment, red(2 * i + 1, 2 * i + 3))\n    return moment"),
    ("l_coefficient_wrong_factorial", "return red(1, power(2, 2 * k + n) * math.factorial(k) * math.factorial(k + n + 1))", "return red(1, power(2, 2 * k + n) * math.factorial(k) * math.factorial(k + n))"),
]
for name, old, new in CASES:
    assert SRC.count(old) == 1, name
    path = "%s/%s.py" % (OUT, name)
    with open(path, "wb") as f:
        f.write(SRC.replace(old, new).encode("utf8"))
    p = subprocess.run([sys.executable, "-I", "-X", "utf8", path], capture_output=True)
    out = p.stdout.replace(b"\r", b"")
    failed = [ln.split(b"check=")[1].split(b"|")[0].decode() for ln in out.splitlines() if ln.startswith(b"FAILED|")]
    print("MUTATION|name=%s|exit=%d|named_failures=%d|checks=%s|same_as_receipt=%d|traceback=%d|json=0" % (name, p.returncode, len(failed), ",".join(failed)[:300], 1 if out == RECEIPT else 0, 1 if b"Traceback" in p.stderr else 0), flush=True)
