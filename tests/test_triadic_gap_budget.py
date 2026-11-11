#!/usr/bin/env python3
"""Exact rational PR34 counterfamily audit of triadic first-gap budget.
The infinite telescoping and logarithmic inequalities are proved in the note.
This checker proves rational finite-K identities, not physical Yang-Mills gaps.
"""
from hashlib import sha256
from math import gcd
from pathlib import Path
import sys

BAD = ("wrong_refinement", "ignore_dark", "substitute_defect",
       "assert_strict_budget")
if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] not in BAD):
    raise SystemExit("usage: test_triadic_gap_budget.py [fault-name]")
fault=sys.argv[1] if len(sys.argv)==2 else ""

def check(ok, name):
    if not ok:
        print("GAP_BUDGET_REJECT|check="+name+"|fault="+fault+"|json=0",flush=True)
        raise SystemExit(1)

def emit(kind,fields):
    print("GAP_BUDGET|"+kind+"|"+fields+"|json=0",flush=True)

def ipow(base, exponent):
    check(type(base) is int and type(exponent) is int and exponent>=0,
          "nonnegative_integer_exponent")
    result=1
    while exponent:
        if exponent & 1:
            result*=base
        exponent//=2
        if exponent:
            base*=base
    return result

def rat(n,d=1):
    check(type(n) is int and type(d) is int and d!=0,"integer_rational")
    if d<0:
        n=-n
        d=-d
    g=gcd(n,d)
    return n//g,d//g

def mul(a,b):
    return rat(a[0]*b[0],a[1]*b[1])

def quot(a,b):
    check(b[0]!=0,"nonzero_quotient")
    return rat(a[0]*b[1],a[1]*b[0])

def sub(a,b):
    return rat(a[0]*b[1]-b[0]*a[1],a[1]*b[1])

def power(a,n):
    return rat(ipow(a[0],n),ipow(a[1],n))

def lt(a,b):
    return a[0]*b[1] < b[0]*a[1]

def eq(a,b):
    return a[0]*b[1] == b[0]*a[1]

def qb(k):
    p=ipow(3,2*k)
    return rat(p,p+1)

def qa(k):
    p=ipow(3,k)
    return rat(p,p+1)

def main():
    frozen=Path("docs/PREDICTION-YM4-TRIADIC-GAP-BUDGET-20261111.hbp").read_bytes()
    rows=[line for line in frozen.decode("utf-8").splitlines()
          if line.startswith("PREDICT|id=GB")]
    check(len(rows)==11,"prediction_rows")
    emit("FREEZE","rows=11|sha256="+sha256(frozen).hexdigest())

    qzero=qb(0)
    check(eq(qzero,rat(1,2)),"starting_gap_ln2")
    product=rat(1)
    for k in range(1,7):
        a_prev=rat(1,ipow(3,k-1))
        a_now=rat(1,ipow(3,k))
        if fault=="wrong_refinement":
            a_now=rat(1,ipow(2,k))
        check(eq(a_prev,mul(rat(3),a_now)),"exact_refinement")
        qprev=qb(k-1)
        qnow=qb(k)
        coarse_defect=sub(power(qnow,3),qprev)
        if fault=="substitute_defect":
            coarse_defect=sub(qnow,qprev)
        check(eq(coarse_defect,sub(power(qnow,3),qprev)),
              "one_step_actual_transfer_power")
        check(lt(rat(0),coarse_defect),"family_b_positive_coarse_defect")
        check(lt(coarse_defect,rat(6,ipow(3,2*k))),
              "family_b_raw_defect_six_a_squared")

        ratio=quot(power(qnow,3),qprev)
        check(lt(rat(1),ratio),"family_b_positive_minimum_epsilon")
        product=mul(product,power(ratio,ipow(3,k-1)))
        telescoped=quot(power(qnow,ipow(3,k)),qzero)
        check(eq(product,telescoped),"full_first_gap_log_budget_product")
        # e^(cumulative weighted epsilon) = q_k^(3^k) / q_0.
        # Since 3^k log(1+3^(-2k)) -> 0, infinite sum = log(1/q_0).
        visible=qa(k)
        dark=qnow
        first=visible if fault=="ignore_dark" else dark
        check(eq(first,dark) and lt(visible,first),
              "three_level_dark_mode_is_true_first_gap")
        check(lt(power(visible,3),qa(k-1)),
              "family_a_epsilon_zero")

        emit("EXACT_LEVEL","k="+str(k)+"|three_to_one=PASS"+
             "|family_b_raw_D_le_6a2=PASS"+
             "|minimum_log_error_positive=YES"+
             "|telescoping_product=PASS|true_dark_mode=PASS")

    # Positive control: the stable family is not falsely rejected.
    check(lt(rat(0),qa(0)) and lt(qa(0),rat(1)),
          "family_a_positive_gap")
    emit("CONTROL","family_A_weighted_epsilon=0|physical_gap_lower=ln2"+
         "|family_B_weighted_sum_equals_m0|strict_budget=FAIL")
    if fault=="assert_strict_budget":
        check(False,"false_strict_budget_claim")
    emit("SCOPE","exact_rational_levels=6|analytic_infinite_limit=IN_NOTE"+
         "|physical_SU2_spectral_theorem=OPEN|r9_launch=UNTOUCHED")
    emit("DONE","result=PASS_COUNTERFAMILY_REJECTED|json=0")

if __name__=="__main__":
    main()
