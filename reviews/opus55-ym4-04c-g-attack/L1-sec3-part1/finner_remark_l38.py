#!/usr/bin/env python3
# Lane L1-sec3-part1: the remark after note Lemma 3.8 (exponent 6 is attained): three unit 3-cubes through a class-1
# link w, each of the 6 plaquettes at w a face of exactly one, give a polymer of 18 plaquettes in which w lies in 6.
# Integer arithmetic only.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from poly_enum import build

N = 8
G = build(N)
plaqs = G["plaqs"]; idx = {p: i for i, p in enumerate(plaqs)}
add = G["add"]; lid = G["lid"]
x = (0, 1, 0, 0); lam = 0          # w = (x, 0), O_perp = {1}: class 1
w = lid(x, lam)
def cube_faces(base, dirs):
    a, b, c = dirs
    faces = []
    for (u, v, t) in ((a, b, c), (a, c, b), (b, c, a)):
        l, n = min(u, v), max(u, v)
        faces.append((base, l, n))
        faces.append((add(base, t), l, n))
    return faces
def shift(base, d, s):
    return add(base, d, s) if s < 0 else base
# cube A: directions {0,1,2}, on the + side of 1 and 2 ; B: {0,2,3}, - side of 2, + side of 3 ; C: {0,3,1}, - side of 3 and 1
A = cube_faces(x, (0, 1, 2))
B = cube_faces(add(x, 2, -1), (0, 2, 3))
C = cube_faces(add(add(x, 3, -1), 1, -1), (0, 3, 1))
S = [idx[(b, l, n)] for (b, l, n) in A + B + C]
distinct = len(set(S)) == 18
cnt = {}
for p in S:
    for e in G["poff"][p]:
        cnt[e] = cnt.get(e, 0) + 1
closed = all(c >= 2 for c in cnt.values())
seen = {S[0]}; st = [S[0]]
while st:
    u = st.pop()
    for v in G["nbrs"][u]:
        if v in S and v not in seen:
            seen.add(v); st.append(v)
inc_w = sum(1 for p in S if w in G["plinks"][p])
maxinc = max(cnt.values())
print("FINNER_REMARK|N=%d|w_class=%d|plaquettes=%d|distinct=%d|closed=%d|connected=%d|w_incidence=%d|max_offlink_incidence=%d|tag=MEASURED|json=0" % (
    N, G["lclass"][w], len(S), int(distinct), int(closed), int(len(seen) == 18), inc_w, maxinc))
