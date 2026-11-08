# The coverage map from a replay index: per section, its units by name, the dynamic and static counts, the sabotages that reach it, and which
# sabotages compute it. Integers only, json=0.
import sys

rows = []
with open(sys.argv[1], encoding="utf-8") as handle:
    for line in handle.read().split("\n"):
        if line.startswith("REPLAY_SECTION|"):
            rows.append(dict(p.partition("=")[::2] for p in line.split("|")[1:]))
shared = {}
for r in rows:
    for part in r["units"].split(","):
        shared.setdefault(part.partition(":")[0], []).append(r["section"])
print("COVERAGE_HEAD|sections=%d|units=%d|units_in_two_or_more_sections=%d|json=0" % (len(rows), len(shared), sum(1 for v in shared.values() if len(v) > 1)))
for r in rows:
    names = [p.partition(":")[0] for p in r["units"].split(",")]
    print("COVERAGE|order=%s|section=%s|units=%d|dynamic=%s|static=%s|dynamic_only=%s|reach=%s|record_ms=%s|names=%s|json=0" % (r["order"], r["section"], len(names), r["dynamic"], r["static"], r["dynamic_only"], r["reach"], r["ms"], ",".join(names)))
for name in sorted(shared):
    if len(shared[name]) > 1:
        print("SHARED_HELPER|unit=%s|sections=%d|in=%s|json=0" % (name, len(shared[name]), ",".join(shared[name])))
