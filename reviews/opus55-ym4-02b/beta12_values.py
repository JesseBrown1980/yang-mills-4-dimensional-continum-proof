# Cross-checks of the beta^12 weights by exact Haar polynomial integration, with no character formula and no finite group.
import ast
import sys

sys.path.insert(0, "C:/tmp/opus55/attack-4d-20261103/ym4-02b")
from haarpoly import expect_words


def plus(x, i):
    y = list(x)
    y[i] += 1
    return tuple(y)


def word(f):
    x, mu, nu = f
    return [((x, mu), 1), ((plus(x, mu), nu), 1), ((plus(x, nu), mu), -1), ((x, nu), -1)]


classes = [ast.literal_eval(line) for line in open("C:/tmp/opus55/attack-4d-20261103/ym4-02b/classes_d4_F12.txt", encoding="utf8")]


def links(f):
    x, mu, nu = f
    return ((x, mu), (plus(x, mu), nu), (plus(x, nu), mu), (x, nu))


def interior(k):
    cover = set()
    for f in k:
        cover.update(links(f))
    out = set()
    for (x, m) in cover:
        for n in range(4):
            if n == m:
                continue
            a, b = (m, n) if m < n else (n, m)
            out.add((x, a, b))
            y = list(x)
            y[n] -= 1
            out.add((tuple(y), a, b))
    return [f for f in out if f not in k and all(l in cover for l in links(f))]


flat = next(k for k in classes if len(k) == 10 and len({d for f in k for d in f[1:]}) == 3)
bent = next(k for k in classes if len(k) == 10 and len({d for f in k for d in f[1:]}) == 4)
for name, k in (("flat", flat), ("bent", bent)):
    inner = interior(k)
    assert len(inner) == 1
    words = [word(f) for f in k] + [word(inner[0]), word(inner[0])]
    v = expect_words(words)
    print("TEN_FACE_PLUS_INNER_SQUARED|shape=%s|E=%d/%d|character_formula=1/524288|ok=%d|json=0" % (name, v[0], v[1], 1 if v == (1, 524288) else 0))
    sys.stdout.flush()
sphere = next(k for k in classes if len(k) == 12 and True and len({d for f in k for d in f[1:]}) == 4 and max(sum(1 for f in k if l in links(f)) for f in k for l in links(f)) == 2)
v = expect_words([word(f) for f in sphere])
print("TWELVE_FACE_SPHERE|E=%d/%d|glue=1/4194304|ok=%d|json=0" % (v[0], v[1], 1 if v == (1, 4194304) else 0))
sys.stdout.flush()
pair = next(k for k in classes if len(k) == 12 and max(sum(1 for f in k if l in links(f)) for f in k for l in links(f)) == 4)
v = expect_words([word(f) for f in pair])
print("TWO_CUBES_SHARING_A_LINK|E=%d/%d|cube_value_squared=1/1048576|ok=%d|json=0" % (v[0], v[1], 1 if v == (1, 1048576) else 0))
sys.stdout.flush()
print("BETA12_VALUES_DONE|json=0")
