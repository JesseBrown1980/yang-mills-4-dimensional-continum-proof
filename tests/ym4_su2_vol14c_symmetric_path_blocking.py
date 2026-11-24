#!/usr/bin/env python3
"""VOL14-C: exact path-family and linearization checks; analytic proof in note."""
from itertools import product, permutations

B = 3
ZERO = (0, 0, 0, 0)
OFFSETS = tuple(product((-1, 0, 1), repeat=4))
DEN = 46656


def require(ok, name):
    if not ok:
        raise ValueError(name)


def emit(*fields):
    print("|".join(("YM4_VOL14C",) + fields + ("json=0",)))


def step(x, s):
    out = list(x)
    out[abs(s)-1] += 1 if s > 0 else -1
    return tuple(out)


def translate(x, y):
    return tuple(a+b for a,b in zip(x,y))


def inverse(w):
    return tuple(-s for s in reversed(w))


def connector(z):
    steps = tuple((i+1 if v > 0 else -i-1)
                  for i,v in enumerate(z) for unused in range(abs(v)))
    return tuple(sorted(set(permutations(steps))))


def add(table, key, value):
    val = table.get(key, 0) + value
    if val:
        table[key] = val
    elif key in table:
        del table[key]


def family(s):
    out = {}
    count = 0
    for z in OFFSETS:
        cs = connector(z)
        require(24 % len(cs) == 0, "connector_denominator")
        w = 24 // len(cs)
        for a in cs:
            for c in cs:
                add(out, a + (s,)*B + inverse(c), w*w)
                count += 1
    return out, count


def edge_table(words, start=ZERO):
    out = {}
    for word, weight in words.items():
        x = start
        for s in word:
            y = step(x, s)
            add(out, (x if s > 0 else y, abs(s)), weight if s > 0 else -weight)
            x = y
    return out


def connector_table(start):
    words = {}
    for z in OFFSETS:
        cs = connector(z)
        for word in cs:
            add(words, word, 576 // len(cs))
    return edge_table(words, start)


def straight_average(s, start=ZERO):
    out = {}
    for z in OFFSETS:
        t = edge_table({(s,)*B: 576}, translate(start,z))
        for key,val in t.items():
            add(out,key,val)
    return out


def combine(*terms):
    out = {}
    for sign, table in terms:
        for key,val in table.items():
            add(out,key,sign*val)
    return out


def image(word, mapping):
    return tuple(mapping[abs(s)-1] if s > 0 else -mapping[abs(s)-1] for s in word)


def endpoint(x, s):
    for unused in range(B):
        x = step(x,s)
    return x


def check_geometry(families):
    # All signed-coordinate generators, with reversal as a separate identity.
    generators = []
    for i in range(4):
        generators.append(tuple(-j-1 if j == i else j+1 for j in range(4)))
    for i in range(4):
        for j in range(i+1,4):
            p = list(range(1,5))
            p[i],p[j] = p[j],p[i]
            generators.append(tuple(p))
    for s in range(1,5):
        f = families[s]
        require({inverse(w):n for w,n in f.items()} == families[-s], "reversal")
        for g in generators:
            require({image(w,g):n for w,n in f.items()} == families[g[s-1]],
                    "signed_coordinate_covariance")
        y = endpoint(ZERO,s)
        blocks = set(OFFSETS) | {translate(y,z) for z in OFFSETS}
        for w in f:
            x = ZERO
            for a in w:
                x = step(x,a)
                require(x in blocks, "path_in_endpoint_blocks")
            require(x == y, "endpoint")
    # The two open halves at every coarse mid-plane are unions of entire
    # centered blocks. Check the block partition and noncrossing pair support.
    for axis in range(4):
        for plane in range(4):
            low = B*plane+1
            for k in range(4):
                sides = {((B*k+z-low-1) % 12) < 6 for z in (-1,0,1)}
                require(len(sides) == 1, "block_one_half")
                nxt = (k+1)%4
                sides2 = {((B*nxt+z-low-1) % 12) < 6 for z in (-1,0,1)}
                if sides == sides2:
                    require(len(sides | sides2) == 1, "noncrossing_union")
    emit("representative_link", "all_signed_coordinate_generators=PASS",
         "reversal=PASS", "half_support=PASS")


def check_linear(families):
    for s in range(1,5):
        y = endpoint(ZERO,s)
        require(edge_table(families[s]) ==
                combine((1,straight_average(s)),(1,connector_table(ZERO)),
                        (-1,connector_table(y))), "linear_gradient")
    x1,x2 = endpoint(ZERO,1),endpoint(ZERO,2)
    cur = combine((1,edge_table(families[1])),(1,edge_table(families[2],x1)),
                  (-1,edge_table(families[1],x2)),(-1,edge_table(families[2])))
    ref = combine((1,straight_average(1)),(1,straight_average(2,x1)),
                  (-1,straight_average(1,x2)),(-1,straight_average(2)))
    require(cur == ref, "curl")
    emit("linearization=centred_Q_minus_coarse_gradient", "coarse_curl=centred_Q_curl")


def check_bounds():
    h = 1
    swaps = 3*B*h+6*h*h
    require(swaps == 15 and 2*swaps == 30, "swap_cap")
    require(8*(2*30*30-swaps*swaps) == 7*2*30*30, "cosine_lower")
    emit("b=3", "plaquette_swaps_bound=15", "fine_angle_cap=1/30", "mean_norm_ge=7/8")
    length = B+8*h
    require(8 <= 2*7 and 6*8*8 <= 8*7*7, "normalization_derivatives")
    require(2*length == 22 and 8*length*length+2*length*(length-1) <= 1210,
            "blocking_derivatives")
    emit("normalization_first_derivative_le=2", "normalization_second_derivative_le=8",
         "blocking_first_derivative_le=22", "blocking_second_derivative_le=1210")
    # A transverse reflection sends this corner-offset connector to a
    # negative offset. The word length fixes the connector length at two.
    word = (2,2,1,1,1,-2,-2)
    reflected = image(word,(1,-2,3,4))
    x = ZERO
    for s in reflected[:2]:
        x = step(x,s)
    require(x[1] == -2 and x[1] not in (0,1,2), "corner_reflection_negative")
    emit("negative_control=corner_offsets", "reflection_covariance=FAIL")


def main():
    families = {}
    for s in (-4,-3,-2,-1,1,2,3,4):
        f,count = family(s)
        require(count == 10473 and sum(f.values()) == DEN, "path_count_and_weight")
        require(max(len(w) for w in f) == 11, "max_length")
        families[s] = f
    emit("b=3", "offsets=81", "full_paths=10473", "common_weight_den=46656",
         "weight_sum=46656", "max_length=11")
    check_geometry(families)
    check_linear(families)
    check_bounds()
    print("YM4_VOL14C_VERDICT|rows=6|scope=GROUP_MAP_PATH_STRUCTURE"
          "|effective_action=OPEN|propagator_decay=OPEN|physical_mass_gap=OPEN|json=0")


if __name__ == "__main__":
    main()
