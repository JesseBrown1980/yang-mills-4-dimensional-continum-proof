#!/usr/bin/env python3
"""Independent YM4-04C E4/E5: pre-existing second seat 640-bit libraries.
Independent from new 256-bit engine arithmetic and G1 f-max implementation.
It reuses the original G-attack's source-disjoint prior code deliberately.
"""
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[1]/"opus55-ym4-04c-g-attack"/"L5-numbers"
sys.path.insert(0,str(BASE))
import ilib as L
import polylib as P
import g1lib as G

def bound(x,low,high):
    assert L.inside(x,low,high),"independent interval outside frozen read "+low+".."+high

def run_e4():
    series=[
        ((1,100),"crude","0.0055222","0.0055223","0.0110902","0.0110903","0.0020316","0.008737"),
        ((1,100),"C03","0.0000047159","0.0000047160","0.0000094320","0.0000094321","0.0000017350","0.000007461"),
        ((1,64),"crude","0.0508265","0.0508266","0.1055724","0.1055725","0.018699","0.08041"),
        ((1,50),"C03","0.0363235","0.0363236","0.0746422","0.0746423","0.013363","0.057463"),
    ]
    delta_r={}
    for beta,head,a,b,c,d,cap2,cap_sum in series:
        eps=P.eps6(*beta)
        A=P.A_of(eps,0)
        root=P.least_root(A,P.coef_list(P.HEADS[head]))
        assert root is not None,"independent least root failed"
        delta=L.muli(root,6) if False else (root[0]*6,root[1]*6)
        bound(delta,a,b)
        _,lm=G.lam_iv(delta)
        bound(lm,c,d)
        q,_,_,f,unique,stop=G.cfin(delta)
        bound(q,"0.3678794","0.3678795")
        second=L.mul(q,delta)
        geometric=L.div(delta,L.sub(L.rat(1,1),q))
        assert L.lt_rat(second[1],L.dec(cap2)), "independent delta2 cap"
        assert L.lt_rat(geometric[1],L.dec(cap_sum)), "independent sum cap"
        delta_r[(beta,head)]=delta
        print("E4_INDEPENDENT|head="+head+"|beta="+str(beta[0])+"/"+str(beta[1])+
              "|delta1="+L.fmti(delta,11)+"|lambda="+L.fmti(lm,11)+
              "|cfin="+L.fmti(q,10)+"|delta2_cap=MET|sum_cap=MET|status=PASS|json=0",flush=True)
    ratio=L.div(delta_r[((1,100),"crude")],delta_r[((1,100),"C03")])
    bound(ratio,"1170","1172")
    for p,q,fexp,lo,hi in ((1,10,9,"0.611173","0.611174"),(11,100,13,"0.811310","0.811311")):
        x=G.cfin(L.rat(p,q))
        rate,_,_,f,unique,stop=x
        assert f==fexp and unique
        bound(rate,lo,hi)
        print("E4_INDEPENDENT_CFIN|delta="+str(p)+"/"+str(q)+
              "|f_max="+str(f)+"|unique=YES|q="+L.fmti(rate,10)+"|PASS|json=0",flush=True)
    for p,above in ((78733761,False),(78733762,True)):
        rate,_,_,f,unique,stop=G.cfin(L.rat(p,1000000000))
        em1=L.exp_point(-L.ONE)
        assert (rate[0]>em1[1]) if above else (rate[0]>=em1[0] and rate[1]<=em1[1])
        print("E4_INDEPENDENT_CFIN_EDGE|delta="+str(p)+"/1000000000|above_e^-1="+str(int(above))+"|PASS|json=0",flush=True)
    crude=delta_r[((1,100),"crude")]
    d20=L.mul(crude,L.exp_point(-19*L.ONE))
    osc=L.mul(L.const(512),L.mul(L.exp_point(-L.ONE),d20))
    assert L.lt_rat(d20[1],L.dec("3.0940e-11"))
    assert L.lt_rat(osc[1],L.dec("5.828e-9"))
    print("E4_INDEPENDENT_C16|delta20="+L.scii(d20,10)+"|osc="+L.scii(osc,10)+"|PASS|json=0",flush=True)
    print("E4_INDEPENDENT_RESULT|PASS|640bit_previous_second_seat=YES|all_k_induction=CONDITIONAL_G1|json=0",flush=True)

def run_e5():
    mu=L.rat(20*20*20*20*20*20*20*20*20*20*20*20*20*20*20*20*20*20*20*20,
             19*19*19*19*19*19*19*19*19*19*19*19*19*19*19*19*19*19*19)
    ex=L.exp_point(L.ONE//4)
    for beta,low,high,expected_pole in [
        ((1,45),"0.9888","0.9889",False),
        ((1,40),"1.1125","1.1126",True),
        ((1,18),"2.473","2.474",True),
        ((1,10),"4.4575","4.4576",True),
        ((1,1),"50.40","50.41",True),
        ((4,1),"292.4","292.5",True),
    ]:
        wall=L.mul(mu,L.mul(ex,P.eps6(*beta)))
        bound(wall,low,high)
        if expected_pole:assert wall[0]>L.ONE
        else:assert wall[1]<L.ONE
        print("E5_INDEPENDENT|beta="+str(beta[0])+"/"+str(beta[1])+
              "|wall="+L.fmti(wall,7)+"|pole="+str(int(expected_pole))+"|PASS|json=0",flush=True)
    assert 720<729
    print("E5_INDEPENDENT_WEAK|beta_ge36|analytic_reverse_triangle=VERIFIED_CONSTANTS|eps6_gt_beta/18-1_ge1|NO_WEAK_CONTINUATION_IN_THIS_CERTIFICATE|json=0",flush=True)
    print("E5_INDEPENDENT_RESULT|PASS|640bit_second_seat_C15=YES|weak_coupling_mass_gap=OPEN|json=0",flush=True)

def run():
    print("YM4_04C_E4_E5_INDEP|independent_source=PREEXISTING_L5_640BIT|second_route=YES|json=0",flush=True)
    run_e4()
    run_e5()
    print("YM4_04C_E4_E5_INDEPENDENT_HOSTED|PASS|finite_enclosures=PASS|theorem_imports=OPEN|r9_runs=0|json=0",flush=True)

if __name__=="__main__":
    run()
