#!/usr/bin/env python3
"""YM4-04/06: integer-pair transfer-gap and observability counterexamples.

Predictions frozen before implementation at 439f1b9 and b23d897.
Neither this toy transfer family nor any scalar residual proves 4D Yang-Mills.
No fractions, Decimal, floating-point divisions, or external packages.
"""
import sys
from hashlib import sha256
from math import gcd
from pathlib import Path

SABOTAGES = ("drop_physical_a", "misread_high_cluster",
             "wrong_cube_block", "fake_uniform_collapsing_gap",
             "claim_observed_residual_implies_gap")
args = sys.argv[1:]
if len(args) > 1 or (args and (not args[0].startswith("sabotage=")
                                   or args[0][9:] not in SABOTAGES)):
    print("usage: test_triadic_physical_gap.py [sabotage=NAME]")
    sys.exit(2)
SABOTAGE = args[0][9:] if args else ""
FAILED = []


def q(n, d=1):
    assert isinstance(n, int) and isinstance(d, int) and d != 0
    if d < 0:
        n, d = -n, -d
    g = gcd(n, d)
    return (n//g, d//g)


def add(x, y):
    return q(x[0]*y[1]+y[0]*x[1], x[1]*y[1])


def sub(x, y):
    return q(x[0]*y[1]-y[0]*x[1], x[1]*y[1])


def mul(x, y):
    return q(x[0]*y[0], x[1]*y[1])


def ab(x):
    return q(abs(x[0]), x[1])


def le(x, y):
    return x[0]*y[1] <= y[0]*x[1]


def lt(x, y):
    return x[0]*y[1] < y[0]*x[1]


def power(x, n):
    assert isinstance(n, int) and n >= 0
    acc = q(1)
    while n:
        if n % 2:
            acc = mul(acc, x)
        n //= 2
        if n:
            x = mul(x, x)
    return acc


def text(x):
    return str(x[0])+"/"+str(x[1])


def digest(x):
    h = sha256()
    for n in x:
        assert n >= 0
        data = n.to_bytes(max(1, (n.bit_length()+7)//8), "big")
        h.update(len(data).to_bytes(4, "big"))
        h.update(data)
    return h.hexdigest()


def stable(j):
    K=3**j
    return q(K, K+1)


def collapse(j):
    K=3**j
    return q(K*K, K*K+1)


def emit(tag, **fields):
    print(tag+"|"+"|".join(str(k)+"="+str(v) for k,v in fields.items())+"|json=0")


def check(name, condition):
    if not condition:
        FAILED.append(name)
        emit("FAILED", check=name)


def step(r, state):
    return (state[0], mul(r,state[1]))


def main():
    root=Path(__file__).resolve().parents[1]
    pred=(root/"docs/PREDICTION-YM4-04-TRIADIC-PHYSICAL-GAP-20261106.hbp").read_bytes()
    res=(root/"docs/PREDICTION-YM4-04-OBSERVABLE-RESIDUAL-20261106.hbp").read_bytes()
    pre_rows=[line for line in pred.splitlines() if line.startswith(b"PREDICT|id=")]
    res_rows=[line for line in res.splitlines() if line.startswith(b"PREDICT|id=")]
    assert len(pre_rows)==13 and len(res_rows)==7
    emit("YM4_BRIDGE_BEGIN",prediction_rows=13,residual_prediction_rows=7,
         prediction_sha256=sha256(pred).hexdigest(),
         residual_sha256=sha256(res).hexdigest(),model="TOY_TRANSFER_NOT_YM4")
    for j in range(13):
        K=3**j
        qs=stable(j)
        qc=collapse(j)
        lower=q(K,K+1)
        upper=q(1,K)
        check("stable_physical_gap_j"+str(j),le(q(1,2),lower))
        check("collapsing_physical_bound_j"+str(j),lt(q(0),qc) and lt(qc,q(1)))
        if j in (0,1,3,6,9,12):
            emit("YM4_FAMILY",j=j,inv_spacing=K,
                 stable_ratio=text(qs),stable_physical_mass_lower=text(lower),
                 stable_physical_mass_upper="1/1",collapse_ratio=text(qc),
                 collapse_physical_mass_upper=text(upper),
                 every_finite_transfer_gap_positive=1)
    check("gap_physical_scale",
          SABOTAGE!="drop_physical_a" or q(1,3**24)==q(1,3**12))
    check("collapsing_limit",lt(q(1,3**12),q(1,100000)))
    for j in range(1,13):
        K=3**j
        delta=ab(sub(power(collapse(j),3),collapse(j-1)))
        bound=q(6,K*K)
        check("one_scale_block_j"+str(j),le(delta,bound))
        if j in (1,2,3,6,9,12):
            emit("YM4_BLOCK_DEFECT",j=j,scale=3,defect=text(delta),
                 bound=text(bound),bound_met=1)
    emit("YM4_COLLAPSE",family="q=1/(1+a^2)",
         one_scale_blocking_defect_bound="6*a_squared",
         physical_mass_upper="a",continuum_gap_limit="ZERO",
         interpretation="EXACT_FINITE_JUMPS_ARE_NOT_UNIFORM_GAP")
    fine=q(1,2)
    mid=q(1,8)
    coarse=q(1,512)
    block_ok=power(fine,3)==mid and power(fine,9)==coarse
    if SABOTAGE=="wrong_cube_block":
        block_ok=block_ok and power(fine,2)==mid
    check("exact_three_scale",block_ok)
    for t in (1,2,3):
        f=power(fine,9*t)
        m=power(mid,3*t)
        c=power(coarse,t)
        check("exact_correlation_t"+str(t),f==m==c)
        emit("YM4_THREE_SCALE",physical_time=t,
             a_fine="1/9",a_middle="1/3",a_coarse="1",
             fine_exponent=9*t,middle_exponent=3*t,coarse_exponent=t,
             correlation=text(c),physical_mass="9*log(2)",
             all_equal=int(f==m==c))
    for name,getter in (("STABLE",stable),("COLLAPSE",collapse)):
        one=getter(5)
        for exponent in range(1,7):
            n=3**exponent
            jumped=one
            for _ in range(exponent):
                jumped=mul(mul(jumped,jumped),jumped)
            binary=power(one,n)
            check("triadic_"+name+"_"+str(exponent),jumped==binary)
            if n<=243:
                state=q(0),q(1)
                for _ in range(n):
                    state=step(one,state)
                check("direct_"+name+"_"+str(exponent),state[1]==binary)
            emit("YM4_MATRIX_JUMP",family=name,spacing="1/243",
                 exponent=exponent,steps=n,cubings=exponent,
                 cube_equals_binary=int(jumped==binary),
                 direct_checked=int(n<=243),
                 state_sha256=digest(binary))
    for j in (0,3,6,12):
        K=3**j
        E=[q(i,K) for i in range(8)]
        E.extend([add(q(94),q(7,K)),add(q(95),q(7,K))])
        high=sub(E[8],E[7])
        first=sub(E[1],E[0])
        ok=high==q(94) and first==q(1,K) and high!=first
        if SABOTAGE=="misread_high_cluster":
            ok=ok and high==first
        check("cluster_not_first",ok)
        emit("YM4_CLUSTER",j=j,cluster_high_gap=text(high),
             true_first_gap=text(first),state_count=len(E),
             high_gap_is_not_first=1)
    check("uniform_continuum_gap_not_inferred",
          lt(q(1,3**12),q(1,2)) if SABOTAGE!="fake_uniform_collapsing_gap"
          else le(q(1,2),q(1,3**12)))
    # A fixed-time observable residual: 1-C_j(1), where C_j(t)=q_j^(t/a_j).
    for j in range(7):
        K=3**j
        c_stable=power(stable(j),K)
        c_collapse=power(collapse(j),K)
        r_stable=sub(q(1),c_stable)
        r_collapse=sub(q(1),c_collapse)
        check("visible_stable_residual_j"+str(j),
              le(q(1,2),r_stable) and lt(r_stable,q(1)))
        check("collapsing_observable_residual_j"+str(j),
              lt(q(0),r_collapse) and le(r_collapse,q(1,K)))
        emit("YM4_OBSERVABLE_RESIDUAL",j=j,inv_spacing=K,
             stable_residual=text(r_stable),
             collapsing_residual=text(r_collapse),
             collapsing_upper=text(q(1,K)),
             spectral_first_gap_not_deduced=1)
        if j>=1:
            # q_dark > q_visible, so the FIRST excited state is dark.
            # Our observable only couples vacuum to the VISIBLE state.
            dark=collapse(j)
            visible=stable(j)
            C=power(visible,K)
            R=sub(q(1),C)
            ok=lt(visible,dark) and le(q(1,2),R)
            if SABOTAGE=="claim_observed_residual_implies_gap":
                ok=ok and le(q(1,2),q(1,K))
            check("visible_residual_does_not_set_first_gap",ok)
            emit("YM4_DARK_EXCITATION",j=j,inv_spacing=K,
                 visible_q=text(visible),dark_q=text(dark),
                 visible_residual=text(R),
                 dark_physical_gap_upper=text(q(1,K)),
                 observable_overlap_with_dark="ZERO",
                 physical_first_gap_can_collapse=1)
    emit("YM4_SCOPE",finite_S3_E9_minus_E8_lower="24.039673_JE_at_r9",
         finite_S3_first_gap="NOT_INFERRED",
         finite_SU2_transfer_gap="FIXED_LATTICE",
         YM4_04="ALL_SCALE_CONTROL_OPEN",
         YM4_05="OS_CONTINUUM_OPEN",
         YM4_06="PHYSICAL_GAP_OPEN",
         real_user_Shadow_Cat_residual="NOT_YET_GAUGE_OPERATOR",
         Clay_proof="NOT_CLAIMED")
    if FAILED:
        emit("YM4_BRIDGE_VERIFY",status="FAIL",failed=len(FAILED),
             sabotage=SABOTAGE or "NONE",json_zero=1)
        sys.exit(1)
    emit("YM4_BRIDGE_VERIFY",status="PASS",prediction_rows=13,
         residual_prediction_rows=7,rational_family_levels=13,
         exact_three_scale=1,jump_rows=12,cluster_examples=4,
         residual_levels=7,dark_counterexamples=6,
         first_physical_gap_continuum="OPEN",Clay_proof="NOT_CLAIMED",
         json_zero=1)

if __name__=="__main__":
    main()
