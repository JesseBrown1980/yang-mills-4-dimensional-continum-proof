# Second seat, PR 13: the engine read Haar from 2I. Here the same patterns, in the same walk order, go through the group-free polynomial integration filed as
# reviews/opus55-ym4-02b/haarpoly.py, and each value is compared with the engine's row. Rows flush as they finish, so a stop leaves the finished ones. Integers only, json=0.
#   usage: haar_against_engine.py SIDES T ENGINE_RAW_ROWS
import sys

sys.path.insert(0, "C:/tmp/ym4-02d-wt/reviews/opus55-ym4-02b")
import haarpoly  # noqa: E402

sides = tuple(int(v) for v in sys.argv[1].split("x"))
t = int(sys.argv[2])
rows = [l.strip() for l in open(sys.argv[3], encoding="utf8") if l.startswith("OVER2|")]
d = len(sides)
nsites = 1
for s in sides:
    nsites *= s


def coords(s):
    x = [0] * d
    for i in range(d - 1, -1, -1):
        x[i] = s % sides[i]
        s //= sides[i]
    return x


def site_of(x):
    s = 0
    for i in range(d):
        s = s * sides[i] + x[i]
    return s


def shift(s, mu):
    x = coords(s)
    x[mu] = (x[mu] + 1) % sides[mu]
    return site_of(x)


faces = []
for s in range(nsites):
    for mu in range(d):
        for nu in range(mu + 1, d):
            faces.append((s * d + mu, shift(s, mu) * d + nu, shift(s, nu) * d + mu, s * d + nu))

nl = nsites * d
deg = [0] * nl
seen = {}
order = []
stack = []


def go(start, odd):
    if stack and odd == 0 and max(deg) > t:
        key = []
        ids = {}
        for f in stack:
            for l in faces[f]:
                key.append(ids.setdefault(l, len(ids)))
        key = tuple(key)
        if key not in seen:
            seen[key] = 1
            order.append(list(stack))
    if len(stack) == t:
        return
    if odd > 4 * (t - len(stack)):
        return
    for f in range(start, len(faces)):
        o = odd
        for l in faces[f]:
            deg[l] += 1
            o += 1 if deg[l] % 2 else -1
        stack.append(f)
        go(f, o)
        stack.pop()
        for l in faces[f]:
            deg[l] -= 1


go(0, 0)
assert len(order) == len(rows), (len(order), len(rows))
done = same = 0
for rep, row in zip(order, rows):
    words = []
    ids = {}
    for f in rep:
        ls = faces[f]
        w = [(ls[0], 1), (ls[1], 1), (ls[2], -1), (ls[3], -1)]
        words.append([(ids.setdefault(l, len(ids)), s) for l, s in w])
    v = haarpoly.expect_words(words)
    text = "%d/%d" % (v[0], v[1])
    field = [p for p in row.split("|") if p.startswith("Haar_by_")][0].split("=")[1]
    done += 1
    ok = text == field
    same += 1 if ok else 0
    print("HAARPOLY|sides=%s|k=%d|poly=%s|engine_2I=%s|same=%d|done=%d|of=%d|json=0" % (sys.argv[1], len(rep), text, field, 1 if ok else 0, done, len(rows)))
    sys.stdout.flush()
print("HAARPOLY_DONE|sides=%s|checked=%d|same=%d|json=0" % (sys.argv[1], done, same))
