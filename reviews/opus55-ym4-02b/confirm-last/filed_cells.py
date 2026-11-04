# Reads the rows filed at 1c02d5a only, cell by cell, plus an independent closed form for side 1 in d = 2, and compares each stated group list. Integers only, json=0.
import re
import math
import sys

L = "C:/tmp/opus55/confirm-4d-20261104/ym4-02b-last/"
H = L + "head/"
RC = H + "reviews/opus55-ym4-02b/recheck/"
T = {"Q8": 3, "2T": 5, "2O": 7, "2I": 11}


def red(n, d):
    g = math.gcd(n, d) or 1
    return n // g, d // g


def parse(v):
    a, b = v.split("/")
    return red(int(a), int(b))


val = {}
source = {}


def put(sides, g, k, v, src):
    v = parse(v)
    key = (sides, g)
    d = val.setdefault(key, {})
    if k in d and d[k] != v:
        print("CONFLICT|sides=%s|group=%s|k=%d|a=%s|b=%s|src=%s|json=0" % (sides, g, k, d[k], v, src))
        sys.exit(1)
    d[k] = v
    source.setdefault(key, set()).add(src)


for name in ("mixed_a", "mixed_1x3"):
    for line in open(RC + name + ".out", encoding="utf8"):
        if line.startswith("MIXED|"):
            sides = re.search(r"sides=([0-9x]+)", line).group(1)
            g = re.search(r"group=(\w+)", line).group(1)
            for k, v in re.findall(r"E_X(\d+)=(-?\d+/\d+)", line):
                put(sides, g, int(k), v, name)
for name in ("multiset_1x2", "multiset_b", "multiset_e", "multiset_d4", "haar_1x3_k7", "haar_1x2_k7"):
    for line in open(RC + name + ".out", encoding="utf8"):
        if line.startswith("MOMENT|"):
            sides = re.search(r"sides=([0-9x]+)", line).group(1)
            k = int(re.search(r"\|k=(\d+)", line).group(1))
            for g, v in re.findall(r"\|(Q8|2T|2O|2I|Haar)=(-?\d+/\d+)", line):
                put(sides, g, k, v, name)

# 1x1 Haar: the filed CONFIRM carries the row, and a closed form gives it independently.
# a = cos^2 th + s sin^2 th, s uniform on [-1, 1], th Haar on SU(2), since V' runs over the conjugacy class of V.


def dfact(n):
    r = 1
    while n > 1:
        r *= n
        n -= 2
    return r


def e_cos_sin(a, b):
    # E[cos^(2a) sin^(2b)] for the density (2/pi) sin^2
    return red(2 * dfact(2 * a - 1) * dfact(2 * b + 1), 2 ** (a + b + 1) * math.factorial(a + b + 1))


def add(x, y):
    return red(x[0] * y[1] + y[0] * x[1], x[1] * y[1])


def closed_1x1(k):
    s = (0, 1)
    for j in range(0, k + 1, 2):
        c = e_cos_sin(k - j, j)
        s = add(s, red(math.comb(k, j) * c[0], (j + 1) * c[1]))
    return s


confirm_haar = {}
for line in open(RC + "CONFIRM-YM4-02b.hbp", encoding="utf8"):
    m = re.match(r"MOMENT\|sides=1x1\|N_p=1\|k=(\d+)\|kept=\d+\|patterns=\d+\|Q8=(\S+?)\|2T=(\S+?)\|Haar=(\S+?)\|json=0", line)
    if m:
        k = int(m.group(1))
        confirm_haar[k] = parse(m.group(4))
        put("1x1", "Q8", k, m.group(2), "confirm")
        put("1x1", "2T", k, m.group(3), "confirm")
ok = 1
for k in range(1, 9):
    c = closed_1x1(k)
    same = confirm_haar.get(k) == c if k in confirm_haar else None
    print("CLOSED_FORM_1x1|k=%d|value=%d/%d|filed_haar=%s|same=%s|json=0" % (k, c[0], c[1], confirm_haar.get(k), same))
    if same is False:
        ok = 0
    val.setdefault(("1x1", "Haar"), {})[k] = c
print("CLOSED_FORM_1x1_DONE|ok=%d|json=0" % ok)


def reach(sides, g):
    row = val.get((sides, g))
    haar = val.get((sides, "Haar"), {})
    if not row:
        return None
    common = sorted(k for k in row if k in haar)
    agree = 0
    first = 0
    for k in common:
        if row[k] == haar[k]:
            if first == 0 and k == agree + 1:
                agree = k
        elif first == 0:
            first = k
    return agree, first, max(common) if common else 0, sorted(source.get((sides, g), []))


measured_one = {}
measured_both = {}
ONE = ["1x2", "1x3", "1x4", "1x2x2", "1x2x2x2"]
BOTH = ["1x1", "1x1x2", "1x1x2x2"]
for s in ONE + BOTH:
    for g in T:
        r = reach(s, g)
        if r is None:
            print("FILED_CELL|sides=%s|group=%s|rows=0|json=0" % (s, g))
            continue
        target = T[g] if s in ONE else T[g] // 2
        held = 1 if r[0] >= target else 0
        exact_edge = "" if s in ONE else "|runs_exactly_through_target=%d" % (1 if (r[0] == target and r[1] == target + 1) else 0)
        print("FILED_CELL|sides=%s|group=%s|t=%d|target=%d|agrees_through_k=%d|first_diff_k=%d|haar_read_through_k=%d|held=%d%s|src=%s|json=0" % (s, g, T[g], target, r[0], r[1], r[2], held, exact_edge, ",".join(r[3]), ))
        if held:
            (measured_one if s in ONE else measured_both).setdefault(s, []).append(g)

GROUPS = "Q8|2T|2O|2I"
lemma = open(H + "docs/LEMMA-0003-SUBGROUP-DESIGNS.md", encoding="utf8").read()
pred = open(H + "docs/PREDICTION-YM4-02b.hbp", encoding="utf8").read()
body = open(L + "out/pr_body.md", encoding="utf8").read()
stated = {}
stated["lemma_one"] = {"1x2": ["Q8", "2T", "2O"], "1x3": ["Q8", "2T"], "1x2x2": ["Q8"], "1x2x2x2": ["Q8"]} if "Agreement was measured through β^t on 1×2 (Q8, 2T, 2O), on 1×3 (Q8, 2T), and for Q8 on 1×2×2 and 1×2×2×2." in lemma else None
stated["lemma_both"] = {"1x1": ["Q8", "2T", "2O", "2I"], "1x1x2": ["Q8", "2T"], "1x1x2x2": ["Q8"]} if "with side 1 in every direction (d = 2, all four groups; Q8 reads E[a²] = 1 against SU(2)'s 1/3) and on 1×1×2 (Q8, 2T) and 1×1×2×2 (Q8)." in lemma else None
stated["pr_body_one"] = {"1x2": ["Q8", "2T", "2O"], "1x3": ["Q8", "2T"], "1x2x2": ["Q8"], "1x2x2x2": ["Q8"]} if "agreement was measured through t for Q8, 2T and 2O on 1×2, for Q8 and 2T on 1×3, and for Q8 on 1×2×2 and 1×2×2×2" in body else None
m = re.search(r"corrected=1x2:Q8,2T,2O;1x3:Q8,2T;1x2x2:Q8;1x2x2x2:Q8\|found_by=second_seat_confirm_at_f4d0946\|rows_changed=0", pred)
stated["prediction_row"] = {"1x2": ["Q8", "2T", "2O"], "1x3": ["Q8", "2T"], "1x2x2": ["Q8"], "1x2x2x2": ["Q8"]} if m else None
for name, st in stated.items():
    if st is None:
        print("LIST|where=%s|sentence_found=0|json=0" % name)
        continue
    meas = measured_both if "both" in name else measured_one
    bad = []
    extra = []
    for s, gs in st.items():
        for g in gs:
            if g not in meas.get(s, []):
                bad.append("%s:%s" % (s, g))
        for g in meas.get(s, []):
            if g not in gs:
                extra.append("%s:%s" % (s, g))
    print("LIST|where=%s|sentence_found=1|cells_stated=%d|stated_but_not_held=%s|held_but_not_stated=%s|json=0" % (name, sum(len(v) for v in st.values()), ",".join(bad) or "none", ",".join(extra) or "none"))

# M_{2k} of 2I against Catalan, exact, integer only, from the traces as (rational, golden) parts.
def lucas_even(n):
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a


rows = []
for k in range(1, 201):
    num = 2 * 4 ** k + 40 + 24 * lucas_even(2 * k)
    assert num % 120 == 0
    M = num // 120
    C = math.comb(2 * k, k) // (k + 1)
    rows.append((k, M, C))
print("M2K|k=1..5|M=%s|C=%s|equal=%d|json=0" % (",".join(str(r[1]) for r in rows[:5]), ",".join(str(r[2]) for r in rows[:5]), 1 if all(r[1] == r[2] for r in rows[:5]) else 0))
print("M2K|k=6..200|all_exceed=%d|first=%d_vs_%d|json=0" % (1 if all(r[1] > r[2] for r in rows[5:]) else 0, rows[5][1], rows[5][2]))
print("FILED_CELLS_DONE|json=0")
