#!/usr/bin/env python3
"""VOL13: exact geometry and integer bounds; analytic steps are in the note."""
from itertools import product


def require(ok, name):
    if not ok:
        raise ValueError(name)


def power(a, n):
    require(isinstance(n, int) and 0 <= n <= 10000, "bounded_power")
    out = 1
    for unused in range(n):
        out *= a
    return out


def move(x, mu, n, L):
    y = list(x)
    y[mu] = (y[mu] + n) % L
    return tuple(y)


def reflect(x, mu, k, L):
    y = list(x)
    y[mu] = (2 * k - y[mu]) % L
    return tuple(y)


def emit(*fields):
    print("|".join(("YM4_VOL13",) + fields + ("json=0",)))


def check_graph(L):
    nbr = {}
    for x in product(range(L), repeat=4):
        for mu in range(4):
            for nu in range(mu + 1, 4):
                edges = {(x, mu), (x, nu), (move(x, mu, 1, L), nu),
                         (move(x, nu, 1, L), mu)}
                for e in edges:
                    nbr.setdefault(e, set()).update(edges - {e})
    for (x, mu), adj in nbr.items():
        require(len(adj) == 18, "degree")
        for y, nu in adj:
            for u, v in zip(x, y):
                require(min((u-v) % L, (v-u) % L) <= 1, "anchor_step")
    emit("row=01", "link_anchor_step_linf_le=1", "degree=18")


def halo(i, b, M):
    return {(i*b+j) % (b*M) for j in range(-b, 2*b)}


def conflicts(b, M):
    count = 0
    for i in range(M):
        for j in range(i+1, M):
            if i % 3 == j % 3 and halo(i,b,M) & halo(j,b,M):
                count += 1
    return count


def check_colors():
    for b in (3, 9):
        for M in (6, 12, 18):
            require(conflicts(b, M) == 0, "same_color_overlap")
    require(len(set(product(range(3), repeat=4))) == 81, "color_count")
    emit("row=02", "coarse_period_multiple3=YES", "colors=81",
         "same_color_halos_disjoint=YES")
    require(conflicts(3, 8) > 0, "wrap_negative_control")
    emit("row=03", "coarse_period_not_multiple3", "wrap_color_conflict=YES")


def check_bounds():
    require(6*1536*power(3,16) < power(2,59049//1024-18), "VOL12_input")
    expected = (51,128,372,1117,3364)
    for i, b in enumerate((3,9,27,81,243)):
        count = 4*power(b,4)*18*power(17,b-1)
        exponent = 18*(b+1)-count.bit_length()
        require(exponent == expected[i], "crossing_exponent")
        require(count < power(2,18*(b+1)-exponent), "strict_bound")
        emit("row=0"+str(i+4), "b="+str(b), "crossing_q_lt_2_pow_minus="+str(exponent))
    require(expected[3] >= 81*13, "coarse_activity")
    require(power(3,4)-1 == 80 and 4*80 == 320 and 320 < power(2,9), "coarse_count")
    for m in range(1,101):
        require(expected[3]*((m+80)//81) >= 13*m, "color_tail")
        require(power(320,m-1) <= power(2,9*(m-1)), "animal_tail")
    emit("row=09", "b=81", "coarse_activity_lt_2_pow_minus=13",
         "coarse_degree=80", "animal_base=320", "tail_le=2_pow_minus_4m_minus9")


def path(x, mu, b, L):
    return tuple((move(x,mu,j,L),mu,1) for j in range(b))


def inverse(word):
    return tuple((x,mu,-s) for x,mu,s in reversed(word))


def reflect_word(word, nu, k, L):
    out = []
    for x, mu, s in word:
        require(s == 1, "positive_input")
        if mu == nu:
            out.append((reflect(move(x,mu,1,L),nu,k,L),mu,-1))
        else:
            out.append((reflect(x,nu,k,L),mu,1))
    return tuple(out)


def reduce_word(word):
    out = []
    for symbol, sign in word:
        if out and out[-1] == (symbol,-sign):
            out.pop()
        else:
            out.append((symbol,sign))
    return tuple(out)


def check_blocking(b, M):
    L = b*M
    for x in product(range(0,L,b), repeat=4):
        for mu in range(4):
            w = path(x,mu,b,L)
            gauged = []
            for a, axis, sign in w:
                gauged.extend(((("g",a),1), (("u",a,axis),1),
                               (("g",move(a,axis,1,L)),-1)))
            expected = ((("g",x),1),) + tuple((("u",a,axis),sign)
                        for a,axis,sign in w) + ((("g",move(x,mu,b,L)),-1),)
            require(reduce_word(gauged) == expected, "gauge_covariance")
            for nu in range(4):
                for k in range(0,L,b):
                    y = reflect(x,nu,k,L)
                    target = (inverse(path(move(y,mu,-b,L),mu,b,L))
                              if mu == nu else path(y,mu,b,L))
                    require(reflect_word(w,nu,k,L) == target, "reflection_covariance")
                    vertices = [move(x,mu,j,L) for j in range(b+1)]
                    for sign in (-1,1):
                        in_half = lambda a: (sign*(a[nu]-k)) % L <= L//2
                        if in_half(vertices[0]) and in_half(vertices[-1]):
                            require(all(in_half(a) for a in vertices), "half_support")
    emit("row=10", "straight_blocking", "reflection_covariance=PASS",
         "gauge_covariance=PASS", "half_support=PASS")
    zero = (0,0,0,0)
    require(reflect(zero,0,1,L)[0] % b != 0, "unaligned_plane_negative")
    w = reflect_word(path(zero,0,b,L),0,0,L)
    mutant = tuple((a,mu,1) for a,mu,s in w)
    require(mutant != w, "missing_inverse_negative")
    emit("row=11", "mutant_unaligned_plane", "coarse_site_map=FAIL",
         "mutant_no_inverse=FAIL")


def main():
    check_graph(4)
    check_colors()
    check_bounds()
    check_blocking(3,6)
    print("YM4_VOL13_VERDICT|rows=11|periodic_equilibrium=YES|blocked_action_control=OPEN|continuum_mass_gap=OPEN|json=0")


if __name__ == "__main__":
    main()
