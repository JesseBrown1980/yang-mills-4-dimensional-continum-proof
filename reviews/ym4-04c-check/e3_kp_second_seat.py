#!/usr/bin/env python3
"""Independent E3 guard: reuse the PRE-EXISTING second-seat L5 integer
interval library, not the new E3 engine's fixed-point helpers.
Read frozen n49 upper-majorant (NOT the underlying infinite power series).
"""
from pathlib import Path
import sys

SRC=Path(__file__).resolve().parents[1]/"opus55-ym4-04c-g-attack"/"L5-numbers"
assert SRC.joinpath("polylib.py").is_file()
sys.path.insert(0,str(SRC))
import ilib as L
import polylib as P
import g1lib as G

# The pre-existing second-seat code uses a separate 640-bit arithmetic scheme.
assert L.P>=512
ONE=L.ONE
THRESHOLD=L.rat(1,4)

def edges(beta,head):
    A=P.A_of(P.eps6(beta[0],beta[1]),0)
    return A,P.coef_list(P.HEADS[head])

def met(p,q,head,an,ad):
    A,coeff=edges((p,q),head)
    good,_,_=P.met_read(A,coeff,L.rat(an,ad))
    assert good,"E3 independent MET witness failed"
    return "E3_INDEP|head="+head+"|beta="+str(p)+"/"+str(q)+"|read=MET|alpha="+str(an)+"/"+str(ad)+"|json=0"

def notmet(p,q,head,alpha_num,alpha_den):
    A,coefs=edges((p,q),head)
    a=L.rat(alpha_num,alpha_den)
    x=P.x_at_iv(A,a)
    z=P.S_eval(x,coefs,deriv=True)
    assert z.pole_ok and z.lo_finite
    gl=z.lo-a[1]
    dlow=(2*x[0]*z.dlo)//ONE-ONE
    dhi=L.cdiv(2*x[1]*z.dhi,ONE)-ONE
    dd=max(abs(dlow),abs(dhi))
    dist=max(a[1],ONE//4-a[0])
    margin=gl-(dd*dist)//ONE
    assert margin>0,"E3 independent global convex tangent failed"
    return ("E3_INDEP|head="+head+"|beta="+str(p)+"/"+str(q)+
            "|read=NOT_MET|alpha="+str(alpha_num)+"/"+str(alpha_den)+
            "|positive_global_tangent=YES|json=0")

def selfmap():
    lo=L.rat(114846768,1000000000)
    hi=L.rat(114846769,1000000000)
    _,l1=G.lam_iv(lo)
    _,l2=G.lam_iv(hi)
    assert l1[1]<ONE//4<l2[0]
    for head in ("C03","headfree"):
        p,q=2075,100000
        A,c=edges((p,q),head)
        is_lower,_,_=P.notmet_read(A,c,L.rat(114846769,6000000000))
        assert is_lower,"C14 beta .02075 least root must lie beyond critical threshold"
        print("E3_INDEP_C14|head="+head+"|beta=2075/100000|read=NOT_MET|least_root_above_delta_crit=YES|json=0",flush=True)
    # A valid upper-root witness below delta_crit.
    A,c=edges((2074,100000),"C03")
    valid,_,_=P.met_read(A,c,L.rat(73,4000))
    assert valid and 6*73*1000000000<114846768*4000
    print("E3_INDEP_C14|head=C03|beta=2074/100000|read=MET|delta1_lt_delta_crit=YES|json=0",flush=True)
    return "E3_INDEP_CRIT|lambda=ATANH_SERIES_ROUTE|delta_crit=[0.114846768,0.114846769]|PASS|json=0"

def run():
    print("E3_INDEP_START|source=PREEXISTING_SECOND_SEAT_L5|P_bits="+str(L.P)+"|frozen_n49_majorant=YES|json=0",flush=True)
    for p,q,head,an,ad in (
        (1904,100000,"crude",1,20),
        (1,50,"C03",1,160),
        (2075,100000,"C03",39,2000),
        (1,64,"C03",1,4000),
    ):
        print(met(p,q,head,an,ad),flush=True)
    for p,q,head,an,ad in (
        (1905,100000,"crude",53646938852,1000000000000),
        (1,50,"crude",29311030801,1000000000000),
        (2076,100000,"C03",20978393291,1000000000000),
        (2076,100000,"headfree",20978404725,1000000000000),
    ):
        print(notmet(p,q,head,an,ad),flush=True)
    print(selfmap(),flush=True)
    print("E3_INDEP_RESULT|PASS|C05=PASS|C06=PASS|C14=PASS|independent_library=YES|json=0",flush=True)

if __name__=="__main__":
    run()
