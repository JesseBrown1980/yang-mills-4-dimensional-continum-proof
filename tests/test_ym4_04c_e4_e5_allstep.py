#!/usr/bin/env python3
"""YM4-04C E4/E5 exact 256-bit integer interval independent contraction gate.

Frozen algebra: c_fin=max(e^-1,exp(delta+lambda-5/4),
 exp(delta-1/8)*sup_{f>=4}(exp(-(1/4-lambda)*f)-exp(-f/4))).
Use C03 verified count head and E3 verified least-root intervals. No float.
No all-k physical theorem is claimed unless the G0 and G1 hypotheses hold.
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import test_ym4_04c_e3_kp_edges as E

def pos_exp(value):
    assert value[0]>=0
    n=0
    while value[1]>=E.ONE:
        value=E.div(value,E.rat(2))
        n+=1
        assert n<20
    result=E.exp_pos(value)
    for _ in range(n):
        result=E.mul(result,result)
    return result

def es(value):
    if value[0]>=0:return pos_exp(value)
    if value[1]<=0:return E.div(E.rat(1),pos_exp((-value[1],-value[0])))
    lower=E.div(E.rat(1),pos_exp((-value[0],-value[0])))[0]
    upper=pos_exp((value[1],value[1]))[1]
    return(lower,upper)

def less(a,b):
    return a[1]<b[0]
def less_eq(a,b):
    return a[1]<=b[0]
def enclosed(a,lo,hi,den):
    return a[0]*den>lo*E.ONE and a[1]*den<hi*E.ONE
def maximum(*args):
    return(max(a[0] for a in args),max(a[1] for a in args))

def cfin(delta):
    dp=E.mul(delta,pos_exp(delta))
    lam=E.add(dp,E.ln1p(dp))
    assert lam[1]<E.ONE//4,"E4_REJECT: Ck admissibility lambda exceeds kappa"
    base=es(E.rat(-1))
    two=es(E.sub(E.add(delta,lam),E.rat(5,4)))
    pref=es(E.sub(delta,E.rat(1,8)))
    decay=E.sub(E.rat(1,4),lam)
    assert decay[0]>0,"E4_REJECT: no monotone f tail"
    f_values=[]
    lower=upper=0
    cap=1024
    stop=0
    for f in range(4,cap+1):
        r=E.mul(decay,E.rat(f))
        u=es((-r[1],-r[0]))
        v=es(E.rat(-f,4))
        diff=E.sub(u,v)
        dlo=max(0,diff[0])
        dhi=max(0,diff[1])
        f_values.append((f,dlo,dhi))
        if dlo>lower:lower=dlo
        if dhi>upper:upper=dhi
        rfuture=E.mul(decay,E.rat(f+1))
        future=es((-rfuture[1],-rfuture[0]))[1]
        if future<=lower:
            stop=f
            break
    assert stop>0,"E4_REJECT: no certified tail cutoff for f>=4"
    argmax=max(f_values,key=lambda t:t[1])
    unique=all(hi<argmax[1] for f,_,hi in f_values if f!=argmax[0])
    if unique:
        lower=argmax[1]
        upper=argmax[2]
    three=E.mul(pref,(lower,upper))
    q=maximum(base,two,three)
    # All-step admission: because delta_crit<1/8 and lambda<=1/4,
    # E2<=exp(delta-1), E3<=exp(delta-1/8) < 1.
    assert delta[1]<E.ONE//8 and q[1]<E.ONE,"E4_REJECT: contraction not strict"
    return q,lam,argmax[0],unique,stop,(base,two,three)

def row(beta,head,delta_bounds,lam_bounds,delta2_cap,sum_cap,fault=""):
    p,d=beta
    eps=E.eps6(beta)
    lo,hi,den=E.least_root(head,eps)
    delta=(6*lo*E.ONE//den,E.ceil(6*hi*E.ONE,den))
    if fault=="wrong_G0_six" and head=="crude" and beta==(1,100):
        delta=(2*delta[0],2*delta[1])
    assert enclosed(delta,*delta_bounds[0:2],delta_bounds[2]),"E4_REJECT: frozen G0 factor-six delta1"
    q,lam,f,unique,stop,terms=cfin(delta)
    assert enclosed(lam,*lam_bounds[0:2],lam_bounds[2]),"E4_REJECT: frozen lambda read"
    em1=es(E.rat(-1))
    assert q[0]>=em1[0] and q[1]<=em1[1],"E4_REJECT: predicted e^-1 control"
    second=E.mul(delta,q)
    chain=E.div(delta,E.sub(E.rat(1),q))
    assert second[1]*delta2_cap[1]<delta2_cap[0]*E.ONE,"E4_REJECT: delta2 cap"
    assert chain[1]*sum_cap[1]<sum_cap[0]*E.ONE,"E4_REJECT: geometric sum cap"
    return "E4_CHAIN|beta="+str(p)+"/"+str(d)+"|head="+head+"|delta1=["+E.dec(delta[0],E.ONE,13)+","+E.dec(delta[1],E.ONE,13)+"]|cfin=e^-1|f_stop="+str(stop)+"|delta2_le="+E.dec(second[1],E.ONE,13)+"|sum_all_steps_le="+E.dec(chain[1],E.ONE,13)+"|all_k=CONDITIONAL_G1|PASS|json=0",delta

def e4(fault):
    rows=[
      ((1,100),"crude",(55222,55223,10000000),(110902,110903,10000000),(20316,10000000),(8737,1000000)),
      ((1,100),"refined",(47159,47160,10000000000),(94320,94321,10000000000),(17350,10000000000),(7461,1000000000)),
      ((1,64),"crude",(508265,508266,10000000),(1055724,1055725,10000000),(18699,1000000),(8041,100000)),
      ((1,50),"refined",(363235,363236,10000000),(746422,746423,10000000),(13363,1000000),(57463,1000000)),
      ((1,64),"refined",(101738,101739,100000000),(0,250000,1000000),(37428,100000000),(16095,10000000)),
    ]
    deltas={}
    for beta,head,delta_b,lam_b,d2_cap,s_cap in rows:
        # C14 (1/64) has no named lambda enclosure; only C1 strict < 1/4.
        if beta==(1,64) and head=="refined":
            eps=E.eps6(beta)
            lo,hi,den=E.least_root(head,eps)
            delta=(6*lo*E.ONE//den,E.ceil(6*hi*E.ONE,den))
            assert enclosed(delta,*delta_b)
            q,lam,f,unique,stop,parts=cfin(delta)
            assert lam[1]<E.ONE//4 and enclosed(q,3678794,3678795,10000000)
            assert E.mul(delta,q)[1]*d2_cap[1]<d2_cap[0]*E.ONE
            assert E.div(delta,E.sub(E.rat(1),q))[1]*s_cap[1]<s_cap[0]*E.ONE
            print("E4_CHAIN|beta=1/64|head=refined|delta1="+E.dec(delta[1],E.ONE,12)+"|cfin=e^-1|C14_control=PASS|json=0",flush=True)
            continue
        line,delta=row(beta,head,delta_b,lam_b,d2_cap,s_cap,fault)
        print(line,flush=True)
        deltas[(beta,head)]=delta
    ratio=E.div(deltas[((1,100),"crude")],deltas[((1,100),"refined")])
    assert enclosed(ratio,1170,1172,1)
    print("E4_C08|crude_over_refined_delta1_in=(1170,1172)|ratio_certified=PASS|json=0",flush=True)

    # C13 finite test: delta1 at 0.01767 below delta_crit,
    # delta1 at .01768 above it; q numerical may approach 1 but <1.
    for p,status in ((1767,"MET"),(1768,"NOT_MET")):
        eps=E.eps6((p,100000))
        lo,hi,den=E.least_root("crude",eps)
        delta=(6*lo*E.ONE//den,E.ceil(6*hi*E.ONE,den))
        if status=="MET":
            assert delta[1]*E.CRIT_DEN<E.CRIT_LO*E.ONE
            q,lam,_,_,stop,_=cfin(delta)
            assert q[1]<E.ONE
        else:
            assert delta[0]*E.CRIT_DEN>E.CRIT_HI*E.ONE
        print("E4_C13|beta="+str(p)+"/100000|selfmap="+status+"|delta1="+E.dec(delta[1],E.ONE,12)+"|json=0",flush=True)

    for p,head,status in ((2074,"refined","MET"),(2075,"refined","NOT_MET")):
        eps=E.eps6((p,100000))
        lo,hi,den=E.least_root(head,eps)
        delta=(6*lo*E.ONE//den,E.ceil(6*hi*E.ONE,den))
        assert (delta[1]*E.CRIT_DEN<E.CRIT_LO*E.ONE) if status=="MET" else (delta[0]*E.CRIT_DEN>E.CRIT_HI*E.ONE)
        print("E4_C14|beta="+str(p)+"/100000|head="+head+"|selfmap="+status+"|json=0",flush=True)
    for p,q,lo,hi,den,f_expect in (
        (1,10,611173,611174,1000000,9),
        (11,100,811310,811311,1000000,13),
    ):
        rate,lam,f,unique,stop,parts=cfin(E.rat(p,q))
        if fault=="wrong_f_max" and p==1:f+=1
        assert f==f_expect and unique,"E4_REJECT: independent integer-f maximum"
        assert enclosed(rate,lo,hi,den),"E4_REJECT: frozen cfin interval"
        print("E4_CFIN|delta="+str(p)+"/"+str(q)+"|f_max="+str(f)+"|unique=YES|cfin=["+E.dec(rate[0],E.ONE,9)+","+E.dec(rate[1],E.ONE,9)+"]|tail_stop="+str(stop)+"|PASS|json=0",flush=True)
    for value,above in ((78733761,False),(78733762,True)):
        # The frozen endpoint threshold f-sup can be tested with high precision.
        rate,lam,f,unique,stop,parts=cfin(E.rat(value,1000000000))
        baseline=es(E.rat(-1))
        if above:
            assert rate[0]>baseline[1],"E4_REJECT: frozen cfin threshold crossing"
        else:
            assert rate[0]>=baseline[0] and rate[1]<=baseline[1]
        print("E4_CFIN_EDGE|delta="+str(value)+"/1000000000|above_exp_minus1="+("YES" if above else "NO")+"|PASS|json=0",flush=True)

    # C16 20-scale norm and 4D 4^4 oscillation, conditional on G1.
    delta=deltas[((1,100),"crude")]
    q=es(E.rat(-1))
    d20=E.mul(delta,E.power(q,19))
    osc=E.mul(E.rat(512),E.mul(q,d20))
    assert d20[1]*100000000000000<E.ONE*3094,"E4_REJECT: frozen C16 delta20"
    assert osc[1]*1000000000000<E.ONE*5828,"E4_REJECT: frozen C16 oscillation"
    if fault=="delete_iteration":
        d20=delta
        assert d20[1]*100000000000000<E.ONE*3094,"E4_REJECT: omitted 19 contraction steps"
    print("E4_C16|delta20_le="+E.dec(d20[1],E.ONE,15)+"|osc_4power4_le="+E.dec(osc[1],E.ONE,12)+"|PASS|G1_CONDITIONAL|json=0",flush=True)

    # General all-k theorem is a purely algebraic induction given the G1
    # inequality and cfin monotonicity; no finite run alone proves G1.
    assert E.lam(E.rat(1,8))[0]>E.ONE//4
    assert E.CRIT_HI*8<E.CRIT_DEN
    assert E.rat(1,8)[1]<E.rat(1,4)[0]
    print("E4_ALL_K|delta_crit_lt_1/8=EXACT|lambda_monotone=DERIVED|cfin_monotone=DERIVED|cfin_lt_1_for_lambda_le_kappa=DERIVED|delta_k_le_delta1*q^(k-1)=ALGEBRA_CONDITIONAL_G1|weak_coupling_not_proved=YES|json=0",flush=True)

def exact_sixth_root_scaled(value):
    """Arbitrary magnitude: unlike the frozen E3 small-beta helper, this
    bisection first doubles the upper bound until it encloses the root."""
    assert value>=0
    target=value*(E.ONE*E.ONE*E.ONE*E.ONE*E.ONE)
    high=E.ONE
    def sixth(y):
        z=y*y*y
        return z*z
    while sixth(high)<=target:high*=2
    low=0
    while high-low>1:
        mid=(low+high)//2
        if sixth(mid)<=target:low=mid
        else:high=mid
    return low

def eps6_unbounded(beta):
    """Same positive Wilson c0 series but L6 root permitted above one."""
    base=E.c0(beta)
    lo=hi=0
    for j in range(7):
        bj=(j*beta[0],beta[1])
        v=E.div(E.c0(bj),E.power(base,j))
        coef=E.comb(6,j)
        if j%2==0:
            lo+=coef*v[0]
            hi+=coef*v[1]
        else:
            lo-=coef*v[1]
            hi-=coef*v[0]
    assert lo>0 and hi>lo
    return(exact_sixth_root_scaled(lo),exact_sixth_root_scaled(hi)+1)

def c15(epsilon,fault=""):
    # head-independent mandatory pole upper-bound failure at beta>=1/40
    exponent=pos_exp(E.rat(1,4))
    wall=E.mul(E.rat(E.MU_N,E.MU_D),E.mul(exponent,epsilon))
    if fault=="ignore_pole" and epsilon[0]>E.rat(1,100)[0]:
        wall=(0,0)
    return wall

def e5(fault):
    table=[
        ((1,45),9888,9889,10000,False),
        ((1,40),11125,11126,10000,True),
        ((1,18),2473,2474,1000,True),
        ((1,10),44575,44576,10000,True),
        ((1,1),5040,5041,100,True),
        ((4,1),2924,2925,10,True),
    ]
    for beta,low,high,den,pole in table:
        eps=eps6_unbounded(beta)
        wall=c15(eps,fault)
        assert enclosed(wall,low,high,den),"E5_REJECT: frozen C15 wall bracket/pole"
        if pole:
            assert wall[0]>E.ONE,"E5_REJECT: mandatory μ e^(1/4) eps6 pole"
        else:
            assert wall[1]<E.ONE
            zero=E.func("headfree",eps,0,1)
            assert zero is not None and zero[0][0]>0 and zero[1][0]>=0,"E5_REJECT: headfree nmax10 C0 failure at 1/45"
        print("E5_C15|beta="+str(beta[0])+"/"+str(beta[1])+"|wall=["+E.dec(wall[0],E.ONE,6)+","+E.dec(wall[1],E.ONE,6)+"]|pole="+("YES" if pole else "NO")+"|read=NOT_MET|PASS|json=0",flush=True)

    # New analytic all-large-beta impossibility for this KP certificate:
    # beta>=1, SU2 Haar c0(b)=(2/pi) int_0^pi e^(b cos t) sin² t dt.
    # cos t <= 1-2t²/pi²; sin t<=t; pi<4 => 
    # c0(b)<6 e^b b^(-3/2).
    # beta>=1, integrating t in [0,1/sqrt(6beta)] and
    # cos t >=1-t²/2, sin t>=2t/pi,
    # e^(-1/2)>1/2, pi<4 and 6^(3/2)<15 =>
    # c0(6b)>e^(6b)*b^(-3/2)/720.
    # Hence L6(e^(ba)/c0(b))^6=c0(6b)/c0(b)^6
    #   > b^(15/2)/(720*6^6) >= b^6/(720*6^6) > (b/18)^6
    # (as 720<3^6). Reverse triangle gives
    # eps6 > b/18-1 >=1 for b>=36.
    assert 720<3*3*3*3*3*3
    assert 720*6*6*6*6*6*6<18*18*18*18*18*18
    assert 36//18-1>=1
    assert E.MU_N>E.MU_D
    if fault=="false_weak_pass":
        assert 720>3*3*3*3*3*3,"E5_REJECT: false weak-coupling pole acceptance"
    print("E5_WEAK_BARRIER|all_beta_ge_36|c0_beta_upper=6*exp(beta)*beta^(-3/2)|c0_6beta_lower=exp(6beta)*beta^(-3/2)/720|eps6_gt_beta/18-1_ge_1|mu*exp(1/4)*eps6_gt1|frozen_F20_KP_cert=NOT_MET|physical_gap=UNDECIDED|PASS|json=0",flush=True)
    print("E5_WEAK_LIMIT|Wilson_SU2_asymptotic_beta_to_infty=NOT_COVERED|all_finite_heads_with_F20_tail=REJECTED_FOR_BETA_GE_36|theorem_regime=STRONG_COUPLING_ONLY|continuum_mass_gap=OPEN|json=0",flush=True)

def run(fault):
    print("YM4_04C_E4_E5|separate_prediction_commit=70cceac39ef08bdee88a75bca82b9a9867502a97|frozen_original_c74e6388|exact_256bit=YES|json=0",flush=True)
    if fault not in ("ignore_pole","false_weak_pass"):
        e4(fault)
    if fault not in ("wrong_G0_six","wrong_f_max","delete_iteration"):
        e5(fault)
    print("YM4_04C_E4_E5_RESULT|PASS|E4_all_k_algebra=CONDITIONAL_G1|E5_pole=EXACT|G0_G1_formal_acceptance=OPEN|weak_coupling_continuum=OPEN|r9_runs=0|json=0",flush=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--sabotage",choices=("wrong_G0_six","wrong_f_max","delete_iteration","ignore_pole","false_weak_pass"),default="")
    args=parser.parse_args()
    run(args.sabotage)
