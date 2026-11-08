# YM4-03C engine check: every YM4_03C_READ row of the engine's receipt against the frozen prediction rows.
# The engine writes each frozen value as a literal in its own source; this reads each literal back in the text of its
# frozen row (the first 26 lines of docs/PREDICTION-YM4-03C.hbp) and each frozen_tag against that row's tag.
# Usage, from the repository root:
#   python3 -I -B -X utf8 reviews/opus55-ym4-03c-engine-check/frozen_literals.py docs/PREDICTION-YM4-03C.hbp reviews/fable5-ym4-03c-engine/RECEIPT-YM4-03C.hbp
# Integers only, json=0.
import sys

# the same value written another way in the frozen row
ALIASES = {
    "1/16384": ["1/16384", "2^-14"],
    "-1/128": ["-1/128", "-(1/128)"],
    "-3/524288": ["-3/524288", "-(3/524288)"],
    "plaq_half": ["chi_1/2(V_P)"],
    "plaq_one": ["chi_1(V_P)"],
    "chair": ["chair"],
}
GENERIC = ("0", "none", "fit")


def fields(line):
    out = {}
    for part in line.split("|")[1:]:
        if "=" in part:
            k, v = part.split("=", 1)
            out[k] = v
    return out


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        pred = f.read().split("\n")[:26]
    rows = {}
    for line in pred:
        if line.startswith("YM4_03C_ROW|") or line.startswith("YM4_03C_GATE|"):
            rows[fields(line)["id"]] = line
    with open(sys.argv[2], encoding="utf-8") as f:
        rec = f.read().split("\n")
    reads = 0
    found = 0
    tags_equal = 0
    by_row = {}
    clause_tags = []
    for line in rec:
        if not line.startswith("YM4_03C_READ|"):
            continue
        f = fields(line)
        reads += 1
        rid, item, fr, tag = f["row"], f["item"], f["frozen"], f["frozen_tag"]
        text = rows.get(rid, "")
        ok = True
        for v in fr.split(","):
            if v in GENERIC:
                continue
            forms = ALIASES.get(v, [v])
            if not any(x in text for x in forms):
                ok = False
        found += 1 if ok else 0
        if not ok:
            sys.stdout.write("FROZEN_LITERAL_ABSENT|row=%s|item=%s|frozen=%s|json=0\n" % (rid, item, fr))
        if "|tag=CONJECTURE" in text:
            rowtag = "CONJECTURE"
        elif "|tag=DERIVED" in text:
            rowtag = "DERIVED"
        else:
            rowtag = "gate_row"
        if tag == rowtag or rowtag == "gate_row":
            tags_equal += 1
        else:
            sys.stdout.write("FROZEN_TAG_DIFFERS|row=%s|item=%s|engine=%s|frozen_row=%s|json=0\n" % (rid, item, tag, rowtag))
        key = (rid, tag, rowtag)
        by_row[key] = by_row.get(key, 0) + 1
        if rid == "P13" and ("plaq_threehalf" in item or "_rect_" in item):
            clause_tags.append(item + ":" + tag)
    for k in sorted(by_row):
        sys.stdout.write("FROZEN_TAGS|row=%s|engine_tag=%s|frozen_row_tag=%s|reads=%d|json=0\n" % (k[0], k[1], k[2], by_row[k]))
    p13 = rows.get("P13", "")
    if "spin>=3/2_clause_and_the_rectangle_DERIVED" in p13:
        sys.stdout.write("FROZEN_P13_CLAUSES|frozen_row=the_spin>=3/2_clause_and_the_rectangle_DERIVED|engine_reads=%s|the_rectangle_also_read_under_P7=DERIVED|json=0\n" % ",".join(clause_tags))
    sys.stdout.write("FROZEN_LITERALS|reads=%d|values_found_in_their_frozen_row=%d|tags_equal_to_the_row_tag=%d|json=0\n" % (reads, found, tags_equal))
    return 0 if found == reads and tags_equal == reads else 1


sys.exit(main())
