# Lane L2-sec3-part2: integer lattice checks on Z^4 (b = 2 parity rules) of note
# Lemma 3.23 (test set), Lemma 3.21 item 4 (#Y'' <= #quarters), Lemma 3.26 / Corollary 3.27
# (readout exclusion: closed connected sets holding all 8 line links of dP, size <= 8) and the 16 bumps.
# Complete closure-driven search; evidence only, the proofs are the derivations.
import itertools, sys

out = []
def say(s):
    out.append(s); print(s)

DIM = 4
def e(l):
    v = [0] * DIM; v[l] = 1; return tuple(v)
def vadd(a, b): return tuple(x + y for x, y in zip(a, b))
def vsub(a, b): return tuple(x - y for x, y in zip(a, b))

def is_line(link):
    x, l = link
    return all(x[r] % 2 == 0 for r in range(DIM) if r != l)

def plaq_links(p):
    x, l, n = p   # l < n
    return [(x, l), (vadd(x, e(l)), n), (vadd(x, e(n)), l), (x, n)]

def off_links(p): return [L for L in plaq_links(p) if not is_line(L)]
def line_links(p): return [L for L in plaq_links(p) if is_line(L)]
def is_quarter(p): return len(line_links(p)) == 2

def plaqs_through(link):
    y, l = link; res = []
    for n in range(DIM):
        if n == l: continue
        a, b = min(l, n), max(l, n)
        res.append((y, a, b))
        res.append((vsub(y, e(n)), a, b))
    return res

def closed(S):
    cnt = {}
    for p in S:
        for L in off_links(p):
            cnt[L] = cnt.get(L, 0) + 1
    return all(c >= 2 for c in cnt.values())

def connected_off(S):
    S = list(S)
    if not S: return False
    idx = {p: i for i, p in enumerate(S)}
    holders = {}
    for p in S:
        for L in off_links(p):
            holders.setdefault(L, []).append(p)
    seen = {S[0]}; st = [S[0]]
    while st:
        u = st.pop()
        for L in off_links(u):
            for v in holders[L]:
                if v not in seen:
                    seen.add(v); st.append(v)
    return len(seen) == len(S)

# ---------------- Lemma 3.23 and Lemma 3.1 item 6 at a coarse link ----------------
ok23 = True
for lam in range(DIM):
    xc = (0, 0, 0, 0)
    e0 = (xc, lam); e1 = (e(lam), lam); m = e(lam)
    P6 = plaqs_through(e0)
    W = set(); Wp = set()
    for p in P6:
        if not is_quarter(p): ok23 = False
        offs = off_links(p)
        at_m = [L for L in offs if L[0] == m or vadd(L[0], e(L[1])) == m]
        if len(at_m) != 1 or len(offs) != 2: ok23 = False
        W |= set(offs); Wp |= set(at_m)
    links_at_m = set()
    for r in range(DIM):
        for L in ((m, r), (vsub(m, e(r)), r)):
            if not is_line(L): links_at_m.add(L)
    if len(W) != 12 or len(Wp) != 6 or Wp != links_at_m: ok23 = False
    P6b = plaqs_through(e1); Wp2 = set()
    for p in P6b:
        for L in off_links(p):
            if L[0] == m or vadd(L[0], e(L[1])) == m: Wp2.add(L)
    if Wp2 != Wp: ok23 = False
say("LEMMA_3.23_GEOMETRY|each_of_6_plaquettes_through_e0_is_a_quarter_with_1_off_link_at_m_and_2_in_W|#W(e0)=12|#W'=6|W'_=_off_links_at_m|same_W'_from_e1|holds=%d|tag=MEASURED" % int(ok23))

# ---------------- dP for the coarse plaquette at the origin, plane {0,1} ----------------
O = (0, 0, 0, 0)
two = lambda l: tuple(2 * c for c in e(l))
s = (1, 1, 0, 0)
FP = [(vsub(vsub(s, e(0)), e(1)), 0, 1), (vsub(s, e(0)), 0, 1), (vsub(s, e(1)), 0, 1), (s, 0, 1)]
FP = [((x), a, b) for (x, a, b) in FP]
dP_line = [(O, 0), (e(0), 0), (two(1), 0), (vadd(two(1), e(0)), 0),
           (O, 1), (e(1), 1), (two(0), 1), (vadd(two(0), e(1)), 1)]
assert all(is_line(L) for L in dP_line)
held_FP = set(L for p in FP for L in line_links(p))
okFP = closed(FP) and connected_off(FP) and held_FP == set(dP_line) and all(is_quarter(p) for p in FP)
say("F_P|4_quarters|closed=%d|connected=%d|holds_exactly_the_8_line_links_of_dP=%d" % (int(closed(FP)), int(connected_off(FP)), int(held_FP == set(dP_line))))

# coarse shadow Y''(gamma): coarse links both of whose positions are held
def coarse_shadow(S):
    held = set(L for p in S for L in line_links(p))
    Y = set()
    for (x, l) in held:
        if x[l] % 2 == 0:   # position 0: base 2x'
            if (vadd(x, e(l)), l) in held:
                Y.add((tuple(c // 2 for c in x), l))
    return Y

# ---------------- complete closure-driven search ----------------
MAXN = 8
need = set(dP_line)
found = set()
visited = set()
def search(S):
    key = frozenset(S)
    if key in visited: return
    visited.add(key)
    cnt = {}
    for p in S:
        for L in off_links(p):
            cnt[L] = cnt.get(L, 0) + 1
    openl = sorted(L for L, c in cnt.items() if c == 1)
    held = set(L for p in S for L in line_links(p))
    unheld = need - held
    rem = MAXN - len(S)
    if len(openl) > 4 * rem: return
    if len(unheld) > 2 * rem: return
    if not openl:
        if not unheld and connected_off(S):
            found.add(key)
        if rem == 0: return
        # closed: may add any off-link neighbour
        nb = set()
        for p in S:
            for L in off_links(p):
                for p2 in plaqs_through(L):
                    if p2 not in key: nb.add(p2)
        for p2 in sorted(nb):
            search(S + [p2])
        return
    if rem == 0: return
    L = openl[0]
    for p2 in plaqs_through(L):
        if p2 not in key:
            search(S + [p2])

L0 = dP_line[0]
for p0 in plaqs_through(L0):
    search([p0])

by_size = {}
for g in found:
    by_size.setdefault(len(g), []).append(g)
sizes = {n: len(by_size.get(n, [])) for n in range(4, MAXN + 1)}
only_FP_below_8 = (sizes[4] == 1 and frozenset(FP) in found and sizes[5] == 0 and sizes[6] == 0 and sizes[7] == 0)
say("LEMMA_3.26_SEARCH|Z^4|closed_connected_sets_holding_all_8_line_links_of_dP|size_counts=%s|only_F_P_below_8=%d|states_visited=%d|tag=MEASURED" % (",".join("n%d:%d" % (n, sizes[n]) for n in sorted(sizes)), int(only_FP_below_8), len(visited)))

# the 16 bumps F_P (+) dC
def cube_faces(base, dirs):
    a, b, c = dirs
    faces = []
    for (u, v, w) in ((a, b, c), (a, c, b), (b, c, a)):
        lo, hi = min(u, v), max(u, v)
        faces.append((base, lo, hi))
        faces.append((vadd(base, e(w)), lo, hi))
    return faces
bumps = set()
for qd in FP:
    x, a, b = qd
    for r in (2, 3):
        for sgn in (0, 1):
            base = x if sgn == 0 else vsub(x, e(r))
            faces = cube_faces(base, (a, b, r))
            assert qd in faces
            bump = frozenset(set(FP) ^ set(faces))
            bumps.add(bump)
bumps_ok = len(bumps) == 16 and all(len(bb) == 8 and bb in found for bb in bumps)
three_q = all(len(set(bb) & set(FP)) == 3 for bb in bumps)
say("COROLLARY_3.27_BUMPS|16_distinct=%d|each_8_plaquettes_closed_connected_holding_dP=%d|each_keeps_3_quarters_of_F_P=%d|size8_found_total=%d|tag=MEASURED" % (int(len(bumps) == 16), int(bumps_ok), int(three_q), sizes[8]))

# Lemma 3.21 item 4 on every polymer found, and Y'' contains dP
ok21 = True; cP = set([(O, 0), (O, 1), (e(0), 1), (e(1), 0)])
for g in found:
    nq = sum(1 for p in g if is_quarter(p))
    Y = coarse_shadow(g)
    if not (len(Y) <= nq <= len(g)): ok21 = False
    if not cP <= Y: ok21 = False
say("LEMMA_3.21_ITEM4|#Y''(gamma)<=#quarters<=#gamma_and_dP_in_Y''_on_all_%d_found_polymers=%d|Y''(F_P)=dP=%d|tag=MEASURED" % (len(found), int(ok21), int(coarse_shadow(FP) == cP)))

allok = ok23 and okFP and only_FP_below_8 and bumps_ok and three_q and ok21
say("SUMMARY|readout_geometry_all_pass=%d|json=0" % int(allok))
open("/mnt/c/tmp/opus55/ym4-04c-gattack/work/L2-sec3-part2/readout_geometry.out", "w").write("\n".join(out) + "\n")
sys.exit(0 if allok else 1)
