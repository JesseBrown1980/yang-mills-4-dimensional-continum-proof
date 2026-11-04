# Why the fixed-slice product stays non-negative on the (Z/2)x(Z/1) slice with Q8. Tests GPT-6's "pairs with inverse holonomies". Integers only, json=0.
# Q8 elements as (sign, axis): axis 0 is the scalar, 1,2,3 are i,j,k. Class index: 0 is +1, 1 is -1, 2 is +-i, 3 is +-j, 4 is +-k.
from itertools import product

ELEMENTS = [(s, a) for a in range(4) for s in (1, -1)]
CROSS = {(1, 2): (1, 3), (2, 3): (1, 1), (3, 1): (1, 2), (2, 1): (-1, 3), (3, 2): (-1, 1), (1, 3): (-1, 2)}


def mul(x, y):
    sx, ax = x
    sy, ay = y
    if ax == 0:
        return (sx * sy, ay)
    if ay == 0:
        return (sx * sy, ax)
    if ax == ay:
        return (-sx * sy, 0)
    s, a = CROSS[(ax, ay)]
    return (sx * sy * s, a)


def inv(x):
    s, a = x
    return (s, 0) if a == 0 else (-s, a)


def cls(x):
    s, a = x
    return (0 if s == 1 else 1) if a == 0 else a + 1


ONE = (1, 0)
assert all(mul(x, inv(x)) == ONE for x in ELEMENTS)
assert all(mul(mul(x, y), z) == mul(x, mul(y, z)) for x, y, z in product(ELEMENTS, repeat=3))


def word(*letters):
    out = ONE
    for g in letters:
        out = mul(out, g)
    return out


# The two plaquettes of the slice (Z/2)x(Z/1). x0,x1 run along the side of 2, a,b along the side of 1 at the two sites.
total = inverse_pairs = same_class = central_pair = polyakov_trivial = polyakov_trivial_inverse = 0
split_central = 0
hist = {}
for x0, x1, a, b in product(ELEMENTS, repeat=4):
    p0 = word(x0, b, inv(x0), inv(a))
    p1 = word(x1, a, inv(x1), inv(b))
    total += 1
    inverse_pairs += 1 if p1 == inv(p0) else 0
    same_class += 1 if cls(p0) == cls(p1) else 0
    central = cls(p0) < 2 and cls(p1) < 2
    central_pair += 1 if central else 0
    split_central += 1 if central and cls(p0) != cls(p1) else 0
    assert central or cls(p0) == cls(p1)
    hist[(cls(p0), cls(p1))] = hist.get((cls(p0), cls(p1)), 0) + 1
    if word(x0, x1) == ONE:
        polyakov_trivial += 1
        polyakov_trivial_inverse += 1 if p1 == inv(p0) else 0
print("SLICE|lattice=(Z/2)x(Z/1)|configs=%d|p1_is_inverse_of_p0=%d|same_class=%d|both_central=%d|central_with_different_sign=%d|json=0" % (total, inverse_pairs, same_class, central_pair, split_central))
print("SLICE_HOLONOMY_TRIVIAL|configs=%d|p1_is_inverse_of_p0=%d|json=0" % (polyakov_trivial, polyakov_trivial_inverse))
print("SLICE_CLASS_PAIRS|%s|json=0" % "|".join("%d,%d=%d" % (k[0], k[1], hist[k]) for k in sorted(hist)))
for w in ((3, 2, 1, -1, -2), (1, 1, 1, -1, -1), (3, 2, 1, -1, 2), (1, -1, 1, 1, 1)):
    negative = sum(hist[k] for k in hist if w[k[0]] * w[k[1]] < 0)
    single = sum(hist[k] for k in hist if w[k[0]] < 0)
    print("SLICE_WEIGHT|w=%s|slice_product_negative=%d|plaquette_negative_at_p0=%d|json=0" % (",".join(str(v) for v in w), negative, single))
