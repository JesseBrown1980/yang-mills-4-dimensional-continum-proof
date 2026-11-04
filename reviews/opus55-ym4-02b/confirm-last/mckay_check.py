# An independent path to the 1xL rows with no group elements and no quaternions: McKay graphs and Schur orthogonality only.
# On 1xL, E_G[prod a_i^k_i] = sum over irreps r of prod (W_ki(r) / 2^ki) / d_r^L, where W_k(r) counts walks of length k from the trivial node to r.
# SU(2) is the same sum on the half-line 1-2-3-... Compared with every filed 1x1, 1x2 and 1x3 row. Integers only, json=0.
import math
import re

RC = "C:/tmp/opus55/confirm-4d-20261104/ym4-02b-last/head/reviews/opus55-ym4-02b/recheck/"
T = {"Q8": 3, "2T": 5, "2O": 7, "2I": 11}


def red(n, d):
    g = math.gcd(n, d) or 1
    return n // g, d // g


def add(x, y):
    return red(x[0] * y[1] + y[0] * x[1], x[1] * y[1])


GRAPHS = {
    "Q8": ({"1": 1, "a": 1, "b": 1, "c": 1, "V": 2}, [("1", "V"), ("a", "V"), ("b", "V"), ("c", "V")], 8),
    "2T": ({"1": 1, "1p": 1, "1q": 1, "2": 2, "2p": 2, "2q": 2, "3": 3}, [("1", "2"), ("2", "3"), ("3", "2p"), ("2p", "1p"), ("3", "2q"), ("2q", "1q")], 24),
    "2O": ({"1": 1, "2": 2, "3": 3, "4": 4, "3p": 3, "2p": 2, "1p": 1, "2b": 2}, [("1", "2"), ("2", "3"), ("3", "4"), ("4", "3p"), ("3p", "2p"), ("2p", "1p"), ("4", "2b")], 48),
    "2I": ({"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "4p": 4, "2p": 2, "3p": 3}, [("1", "2"), ("2", "3"), ("3", "4"), ("4", "5"), ("5", "6"), ("6", "4p"), ("4p", "2p"), ("6", "3p")], 120),
}
N = 40
GRAPHS["Haar"] = ({str(i): i for i in range(1, N + 1)}, [(str(i), str(i + 1)) for i in range(1, N)], 0)

for name, (d, edges, order) in GRAPHS.items():
    nb = {v: [] for v in d}
    for a, b in edges:
        nb[a].append(b)
        nb[b].append(a)
    if order:
        assert sum(x * x for x in d.values()) == order
        assert all(sum(d[u] for u in nb[v]) == 2 * d[v] for v in d), name
    GRAPHS[name] = (d, nb, order)

KMAX = 14


def walks(name):
    d, nb, _ = GRAPHS[name]
    w = {v: 0 for v in d}
    w["1"] = 1
    out = [dict(w)]
    for _ in range(KMAX):
        w = {v: sum(w[u] for u in nb[v]) for v in d}
        out.append(dict(w))
    return out


WALK = {g: walks(g) for g in GRAPHS}
for g in T:
    t = T[g]
    # the trace moment table in the PR body, by closed walks
    closed = WALK[g][t + 1]["1"]
    haar = WALK["Haar"][t + 1]["1"]
    print("TRACE_MOMENT|group=%s|t=%d|E_trace_power=%d|Haar=%d|lower_equal=%d|json=0" % (g, t, closed, haar, 1 if all(WALK[g][k]["1"] == WALK["Haar"][k]["1"] for k in range(0, t + 1)) else 0))


def compositions(k, parts):
    if parts == 1:
        yield (k,)
        return
    for i in range(k + 1):
        for rest in compositions(k - i, parts - 1):
            yield (i,) + rest


def moment(name, L, k):
    d, _, _ = GRAPHS[name]
    wk = WALK[name]
    total = (0, 1)
    for comp in compositions(k, L):
        mult = math.factorial(k)
        for c in comp:
            mult //= math.factorial(c)
        for v, dim in d.items():
            p = mult
            for c in comp:
                p *= wk[c][v]
                if p == 0:
                    break
            if p:
                total = add(total, (p, dim ** L))
    return red(total[0], total[1] * 2 ** k)


# compare every filed row on 1x1, 1x2, 1x3
checked = 0
wrong = 0


def compare(sides, g, k, v, src):
    global checked, wrong
    L = int(sides.split("x")[1])
    a, b = v.split("/")
    got = moment(g, L, k)
    checked += 1
    if got != red(int(a), int(b)):
        wrong += 1
        print("DIFF|sides=%s|group=%s|k=%d|filed=%s|closed=%d/%d|src=%s|json=0" % (sides, g, k, v, got[0], got[1], src))


for name in ("mixed_a", "mixed_1x3"):
    for line in open(RC + name + ".out", encoding="utf8"):
        if line.startswith("MIXED|"):
            sides = re.search(r"sides=([0-9x]+)", line).group(1)
            g = re.search(r"group=(\w+)", line).group(1)
            for k, v in re.findall(r"E_X(\d+)=(-?\d+/\d+)", line):
                compare(sides, g, int(k), v, name)
for name in ("multiset_1x2", "multiset_b", "haar_1x3_k7", "haar_1x2_k7"):
    for line in open(RC + name + ".out", encoding="utf8"):
        if line.startswith("MOMENT|"):
            sides = re.search(r"sides=([0-9x]+)", line).group(1)
            if sides not in ("1x1", "1x2", "1x3"):
                continue
            k = int(re.search(r"\|k=(\d+)", line).group(1))
            for g, v in re.findall(r"\|(Q8|2T|2O|2I|Haar)=(-?\d+/\d+)", line):
                compare(sides, g, k, v, name)
for line in open(RC + "CONFIRM-YM4-02b.hbp", encoding="utf8"):
    m = re.match(r"MOMENT\|sides=(1x1|1x2|1x3)\|", line)
    if m:
        k = int(re.search(r"\|k=(\d+)", line).group(1))
        for g, v in re.findall(r"\|(Q8|2T|2O|2I|Haar)=(-?\d+/\d+)", line):
            compare(m.group(1), g, k, v, "confirm")
print("FILED_ROWS_AGAINST_CLOSED_FORM|checked=%d|wrong=%d|json=0" % (checked, wrong))

# the cells the rows did not reach
for L in (1, 2, 3, 4, 5, 6):
    for g in T:
        t = T[g]
        first = 0
        for k in range(1, KMAX + 1):
            if moment(g, L, k) != moment("Haar", L, k):
                first = k
                break
        target = t // 2 if L == 1 else t
        e = moment(g, L, first) if first else (0, 1)
        h = moment("Haar", L, first) if first else (0, 1)
        print("CLOSED_CELL|sides=1x%d|group=%s|t=%d|agrees_through_k=%d|first_diff_k=%d|E_G=%d/%d|Haar=%d/%d|expected_through=%d|as_expected=%d|json=0" % (L, g, t, first - 1 if first else KMAX, first, e[0], e[1], h[0], h[1], target, 1 if (first - 1) == target else 0))
print("MCKAY_DONE|json=0")
