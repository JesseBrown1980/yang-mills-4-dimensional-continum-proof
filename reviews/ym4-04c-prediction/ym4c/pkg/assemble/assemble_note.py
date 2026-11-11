#!/usr/bin/env python3
"""Assembles NOTE-YM4-04C-LOCAL-POLYMER-NORM-20261109.md from note-src/ and the package's own files, so that the
note's ledger, engine plan, derive-checks output, manifest line and pin are copies of their sources. Packaging only."""
import hashlib
import os
import re
A = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(A)
src = lambda n: open(os.path.join(A, "note-src", n), encoding="utf-8").read()
rd = lambda n: open(os.path.join(PKG, n), encoding="utf-8").read()


def insert_after_heading(text, note):
    head, rest = text.split("\n", 1)
    assert head.startswith("## ")
    return head + "\n\n" + note.strip() + "\n" + rest


s3 = insert_after_heading(src("03-G0.md"), src("03-note.md"))
s4 = insert_after_heading(src("04-G1.md"), src("04-note.md"))
body = src("00-02.md").rstrip() + "\n\n" + s3.rstrip() + "\n\n" + s4.rstrip() + "\n\n" + src("05-18.md").rstrip() + "\n"

led = rd("ledger_rows-final.txt").splitlines()
rows = [ln for ln in led if re.match(r"^L\d\d \| ", ln)]
assert len(rows) == 28 and all(ln.count(" | ") == 4 for ln in rows)
table = "\n".join([led[1], "", "| id | statement | status | source | role in this step, and what would promote it |", "|---|---|---|---|---|"]
                  + ["| " + ln + " |" for ln in rows])
plan = rd("engine_plan-final.txt").rstrip()
assert "```" not in plan
dc = rd("DERIVE-CHECKS.hbp").rstrip()
end = dc.splitlines()[-1]
m = re.match(r"YM4_04C_CHECKS_END\|checks=(\d+)\|failed=(\d+)\|", end)
man = os.path.join(PKG, "MANIFEST-ym4c-pkg.sha256")
pred = open(os.path.join(PKG, "PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp"), "rb").read()
lines = pred.split(b"\n")
assert len(lines) == 42 and lines[-1] == b""
pin = hashlib.sha256(b"\n".join(lines[:41]) + b"\n").hexdigest()
subs = {
    "<<LEDGER_TABLE>>": table,
    "<<ENGINE_PLAN>>": "```text\n" + plan + "\n```",
    "<<DC_OUTPUT>>": dc,
    "<<DC_COUNT>>": m.group(1), "<<DC_FAILED>>": m.group(2),
    "<<MAN3_LINES>>": str(sum(1 for _ in open(man))),
    "<<MAN3_SHA>>": hashlib.sha256(open(man, "rb").read()).hexdigest(),
    "<<PIN>>": pin,
}
for k, v in subs.items():
    assert body.count(k) == 1, k
    body = body.replace(k, v)
assert "<<" not in body
out = os.path.join(PKG, "NOTE-YM4-04C-LOCAL-POLYMER-NORM-20261109.md")
open(out, "w", encoding="utf-8").write(body)
print(out, body.count("\n"), "lines; pin", pin)
