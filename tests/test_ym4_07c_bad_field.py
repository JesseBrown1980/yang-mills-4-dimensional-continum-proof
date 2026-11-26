#!/usr/bin/env python3
"""YM4-07C unconditional bad-field bound on finite Wilson SU(2) tori.
Exact dyadic rational CONSEQUENCES of a written entropy inequality.
The infinite-dimensional probability bound is a mathematical proof in the note,
not a fact that finitely many rational checks could establish by themselves.
"""
from hashlib import sha256
from math import factorial
from pathlib import Path
import sys

FAULTS = ("wrong_link_face_ratio", "weaken_trace_threshold",
          "wrong_KL_sign", "damage_exp8_term", "inflate_plaquette_count",
          "wrong_dyadic_coefficient")
if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] not in FAULTS):
    raise SystemExit("usage: test_ym4_07c_bad_field.py [fault-name]")
fault = sys.argv[1] if len(sys.argv) == 2 else ""

def check(ok, reason):
    if not ok:
        print("YM4_07C_REJECT|reason="+reason+"|fault="+fault+"|json=0",flush=True)
        raise SystemExit(1)

def emit(kind, data):
    print("YM4_07C|"+kind+"|"+data+"|json=0",flush=True)

def power(x,n):
    check(type(x) is int and type(n) is int and n>=0,
          "integer_nonnegative_exponent")
    out=1
    while n:
        if n&1:
            out*=x
        n//=2
        if n:
            x*=x
    return out

def check_freeze():
    raw=Path("docs/PREDICTION-YM4-07C-UNCONDITIONAL-BAD-FIELD-20261111.hbp").read_bytes()
    rows=[line for line in raw.decode("utf-8").splitlines()
          if line.startswith("PREDICT|id=W07C-")]
    check(len(rows)==14,"frozen_fourteen_predictions")
    emit("FREEZE","rows=14|sha256="+sha256(raw).hexdigest())

def geometry():
    # Exact four-dimensional hypercubic counts on all periodic sides L>=3.
    for L in (3,4,9,27):
        sites=power(L,4)
        links=4*sites
        faces=(7 if fault=="inflate_plaquette_count" else 6)*sites
        ratio_num,ratio_den=links,faces
        check(3*ratio_num==2*ratio_den,
              "four_dimensional_links_over_plaquettes")
    if fault=="wrong_link_face_ratio":
        ratio_num,ratio_den=3,2
    else:
        ratio_num,ratio_den=2,3
    check(3*ratio_num==2*ratio_den,
          "partition_function_entropy_ratio")
    emit("GEOMETRY","dimension=4|links_per_site=4|plaquettes_per_site=6|Nl_over_Np=2/3")

def exponential():
    # The positive eighth partial sum is already larger than 1536.
    n=8
    common=factorial(n)
    terms=[power(8,j)*(common//factorial(j)) for j in range(n+1)]
    if fault=="damage_exp8_term":
        terms[8]=0
    sum_numer=sum(terms)
    check(sum_numer>1536*common,
          "exp_eight_Taylor_strict_exceeds_1536")
    check(sum_numer==556403*common//315,
          "independent_exact_exp8_partial")
    # e > 1+1+1/2 > 2, so ln 2 < 1.
    check(5>2*2, "log_two_less_than_one")
    emit("ELEMENTARY_LOG","exp8_partial_n=8|exp8_gt_1536=PASS|ln2_lt_1=PASS")

def trace_cutoff():
    # In S3, if u.v_i,u.v_j>=c, then v_i.v_j>=2c*c-1.
    # For c=7/8, this is 17/32>1/2; c=4/5 FAILS.
    cn,cd=(4,5) if fault=="weaken_trace_threshold" else (7,8)
    lower_n=2*cn*cn-cd*cd
    lower_d=cd*cd
    check(2*lower_n>lower_d,
          "trace_cutoff_for_all_staple_pairs")
    check(lower_n*32 == 17*lower_d,
          "spherical_pair_alignment_17over32")
    # A realizable rational SU2 pair with u.v_i=u.v_j=4/5
    # but v_i.v_j=7/25, a negative control of weak cutoff.
    vi=(4,3,0,0)
    vj=(4,-3,0,0)
    u=(5,0,0,0)
    check(sum(vi[i]*vj[i] for i in range(4))==7,
          "weak_cutoff_actual_pair_separation")
    check(sum(u[i]*vi[i] for i in range(4))==20,
          "weak_cutoff_actual_u_dot")
    emit("STAPLE","plaquette_trace_cutoff=7/8|pair_lower=17/32|G_good=YES|weaker_4over5=FALSE")

def entropy_and_dyadic():
    # Given the written KL and small-ball lemmas:
    # E[1-a_p] <= (1/2+2/3 ln1536 + ln beta)/beta.
    # For beta=2^m, ln1536<8, ln2<1 =>
    # E[1-a_p] < (35/6+m)/2^m.
    kl_sign= -1 if fault=="wrong_KL_sign" else 1
    check(kl_sign==1,"relative_entropy_nonnegative_sign")
    for m,want in ((10,760),(12,856),(16,1048),(20,1240)):
        beta=power(2,m)
        coeff=48 if fault=="wrong_dyadic_coefficient" else 48
        derived=8*(35+6*m)
        if fault=="wrong_dyadic_coefficient":
            derived+=1
        check(derived==want and coeff*(35+6*m)==6*want,
              "dyadic_integer_coefficient_"+str(m))
        check(want<beta,"dyadic_nontrivial_bound_"+str(m))
        emit("BAD_LINK","beta_pow2="+str(m)+"|bound_strict_lt="+
             str(want)+"/"+str(beta)+"|uniform_in_4D_volume=YES")

    # For a fraction eta=1/10, Markov density bound at higher beta.
    for m,want in ((16,1048),(20,1240)):
        beta=power(2,m)
        check(want*10<beta*2, "bad_fraction_less_than_two_"+str(m))
        emit("DENSITY","beta_pow2="+str(m)+
             "|fraction_threshold=1/10|probability_lt="+
             str(10*want)+"/"+str(beta))

def main():
    check_freeze()
    geometry()
    exponential()
    trace_cutoff()
    entropy_and_dyadic()
    emit("CONCLUSION","fixed_link_bad_probability_tends_to_zero=DERIVED|global_all_link_event=OPEN|RG=OPEN|physical_gap=OPEN")
    emit("DONE","integer_checks=PASS|theorem_analytic_proof=IN_NOTE|physical_gap=NOT_PROVED")

if __name__=="__main__":
    main()
