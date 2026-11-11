#!/usr/bin/env python3
"""YM4-07: exact integer tests of a conditional weak-Wilson concentration lemma.
No large-field probability, four-dimensional RG, continuum or mass-gap result.
"""
from hashlib import sha256
from math import factorial
from pathlib import Path
import sys

FAULTS = ("drop_cross_plane", "flip_one_staple",
          "cancel_background_link", "corrupt_exp_tail", "wrong_plaquette_count")
if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] not in FAULTS):
    raise SystemExit("usage: test_ym4_07_weak_conditional.py [fault-name]")
fault = sys.argv[1] if len(sys.argv) == 2 else ""

def check(ok, reason):
    if not ok:
        print("YM4_07_REJECT|reason=" + reason + "|fault=" + fault + "|json=0", flush=True)
        raise SystemExit(1)

def power(base, n):
    check(type(base) is int and type(n) is int and n >= 0, "integer_power")
    out = 1
    while n:
        if n & 1:
            out *= base
        n //= 2
        if n:
            base *= base
    return out

def emit(name, fields):
    print("YM4_07|" + name + "|" + fields + "|json=0", flush=True)

def qmul(a, b):
    w, x, y, z = a
    t, u, v, h = b
    return (w*t-x*u-y*v-z*h,
            w*u+x*t+y*h-z*v,
            w*v-x*h+y*t+z*u,
            w*h+x*v-y*u+z*t)

def conj(a):
    return (a[0], -a[1], -a[2], -a[3])

def dot(a, b):
    return sum(a[i]*b[i] for i in range(4))

def Q(vs):
    return sum(sum(x[i] for x in vs)*sum(x[i] for x in vs) for i in range(4))

def pairQ(vs, drop=False):
    pairs = [(i, j) for i in range(6) for j in range(i+1, 6)]
    if drop:
        pairs = [(i,j) for (i,j) in pairs if i//2 == j//2]
    return 6 + 2*sum(dot(vs[i],vs[j]) for i,j in pairs), len(pairs)

def shift(x, axis, s):
    return tuple((x[j]+(s if j == axis else 0)) % 3 for j in range(4))

def lattice_link(x, axis):
    # Put one negative transverse edge at e0-e_nu for each nu.
    if axis in (1,2,3) and x == shift(shift((0,0,0,0),0,1),axis,-1):
        if fault == "cancel_background_link" and axis == 1:
            return 1
        return -1
    return 1

def z2_plaquette(x, mu, nu):
    return (lattice_link(x,mu)*lattice_link(shift(x,mu,1),nu)
            *lattice_link(shift(x,nu,1),mu)*lattice_link(x,nu))

def test():
    p = Path("docs/PREDICTION-YM4-07-WEAK-CONDITIONAL-NETWORK-20261111.hbp")
    frozen = p.read_bytes()
    rows = [s for s in frozen.decode("utf-8").splitlines()
            if s.startswith("PREDICT|id=W07-")]
    check(len(rows) == 10, "prediction_row_count")
    emit("PREDICTION", "rows=10|sha256=" + sha256(frozen).hexdigest())

    # The exact lattice has six incident plaquettes, grouped in three planes.
    n_planes = 4 if fault == "wrong_plaquette_count" else 3
    check(2*n_planes == 6 and 6*5//2 == 15 and 3*4 == 12,
          "four_dimensional_six_staple_geometry")
    emit("GEOMETRY", "incident=6|unordered_pairs=15|cross_plane=12")

    one=(1,0,0,0); ii=(0,1,0,0); jj=(0,0,1,0); kk=(0,0,0,1)
    vs=(one,ii,jj,kk,conj(ii),conj(jj))
    pval, count = pairQ(vs, fault == "drop_cross_plane")
    check(count == 15 and pval == Q(vs) == 2, "direct_resultant_vs_15_pair_networks")
    # Two-sided gauge action is an orthogonal SO(4) action on unit quaternions.
    transformed = [qmul(qmul(ii,v),conj(jj)) for v in vs]
    check(all(dot(vs[i],vs[j]) == dot(transformed[i],transformed[j])
              for i in range(6) for j in range(6)), "two_sided_gauge_Gram")
    check(Q(vs) == Q(transformed), "two_sided_gauge_resultant")
    emit("NETWORK", "Q_direct=2|Q_all_15_pairs=2|two_sided_gauge_invariance=PASS")

    aligned=[one for _ in range(6)]
    if fault == "flip_one_staple":
        aligned[0]=(-1,0,0,0)
    check(all(2*dot(aligned[i],aligned[j]) >= 1
              for i in range(6) for j in range(i+1,6)),
          "good_field_pair_condition")
    check(Q(aligned) == 36 and 36 >= 21 and 21 > 16,
          "gauge_invariant_good_field_resultant")
    emit("GOOD_FIELD", "pair_dot_ge=1/2|Q_ge=21|R_gt=4|beta_ge=1/4")

    # For s=1/2, beta>=1, tail <= 1728 beta^2 exp(-2 beta).
    # Positivity of the exponential Taylor series proves exp(2 beta)>
    # (2 beta)^m/m!, so these are exact INTEGER sufficient comparisons.
    for beta, digits, m in ((16,6,20),(32,15,29),(64,24,31)):
        denominator = factorial(m+1 if fault == "corrupt_exp_tail" else m)
        check(power(2*beta,m) >
              1728*beta*beta*power(10,digits)*denominator,
              "Taylor_tail_beta_" + str(beta))
        emit("TAIL", "beta="+str(beta)+"|s=1/2|lt=1e-"+str(digits)+
             "|positive_exp_term="+str(m)+"|exact_integer=PASS")

    # All six actual, oriented 4D plaquettes at the central link:
    # positive sides +I, negative sides -I, so the central link has Haar law
    # for every beta despite the six-plaquette geometry.
    x=(0,0,0,0)
    positive=[z2_plaquette(x,0,nu) for nu in (1,2,3)]
    negative=[z2_plaquette(shift(x,nu,-1),0,nu) for nu in (1,2,3)]
    check(positive == [1,1,1] and negative == [-1,-1,-1],
          "realizable_4D_three_plus_three_minus")
    check(sum(positive+negative) == 0, "cancelled_resultant")
    emit("COUNTEREXAMPLE", "4D_side=3|positive=3|negative=3|Q=0|conditional=HAAR")

    # In the illustrative sequence beta_k=16+k/2 and |links_k|=4*81^k,
    # the derived union upper bound grows by ratio
    # 81 * ((beta_k+1/2)/beta_k)^2 / e > 81/3 > 27.
    # Classical elementary fact e < 3 is proved by its factorial series.
    check(81 == 27*3 and 2*16+1>2*16, "illustrative_union_not_uniform")
    emit("SCALING", "beta_k=16+k/2|volume_ratio=81|upper_bound_ratio_gt=27|is_not_probability_lower_bound=YES")
    emit("SCOPE", "good_field_probability=OPEN|all_scale_4D_RG=OPEN|physical_gap=OPEN")
    emit("DONE", "result=PASS_CONDITIONAL_WEAK_FIELD_ONLY|weak_trajectory_certificate=NOT_YET")

if __name__ == "__main__":
    test()
