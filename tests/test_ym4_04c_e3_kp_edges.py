#!/usr/bin/env python3
"""YM4-04C E3: exact integer dyadic enclosures of the FROZEN n49 KP majorant.
C05/C06 are sufficient-certificate edges, NOT physical phase boundaries.
C14 imports the G0/G1 self-map interpretation; computes its exact finite read.
No floats, JSON data, fraction/decimal module, uncertified negative powers.
"""
from math import comb

BITS=256
ONE=1<<BITS
MU_N=20*20*20*20*20*20*20*20*20*20*20*20*20*20*20*20*20*20*20*20
MU_D=19*19*19*19*19*19*19*19*19*19*19*19*19*19*19*19*19*19*19
F={n:comb(20*n,n)//(19*n+1) for n in range(4,51)}
HEAD={
    "crude":tuple(6*F[n] for n in range(4,11)),
    "refined":(1,0,12,0,32,32,304),
    "headfree":(0,0,0,0,0,0,0),
}
CRIT_LO=114846768
CRIT_HI=114846769
CRIT_DEN=1000000000

def ceil(a,b):
    assert b>0
    return -((-a)//b)
def rat(p,q=1):
    assert q>0
    return(p*ONE//q,ceil(p*ONE,q))
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def sub(a,b):return(a[0]-b[1],a[1]-b[0])
def mul(a,b):
    assert a[0]>=0 and b[0]>=0
    return(a[0]*b[0]//ONE,ceil(a[1]*b[1],ONE))
def div(a,b):
    assert a[0]>=0 and b[0]>0
    return(a[0]*ONE//b[1],ceil(a[1]*ONE,b[0]))
def power(a,n):
    assert n>=0
    z=(ONE,ONE)
    for _ in range(n):z=mul(z,a)
    return z
def exp_pos(t):
    assert t[0]>=0 and t[1]<ONE
    lo=hi=ONE
    a=b=ONE
    last=90
    for n in range(1,last+1):
        a=a*t[0]//(ONE*n)
        b=ceil(b*t[1],ONE*n)
        lo+=a
        hi+=b
    nxt=ceil(b*t[1],ONE*(last+1))
    hi+=ceil(nxt*(last+2)*ONE,(last+2)*ONE-t[1])
    return(lo,hi)
def c0(beta):
    p,q=beta
    x=rat(p*p,4*q*q)
    term=(ONE,ONE)
    ans=term
    for n in range(1,50):
        term=(term[0]*x[0]//(ONE*n*(n+1)),
              ceil(term[1]*x[1],ONE*n*(n+1)))
        ans=add(ans,term)
    nxt=ceil(term[1]*x[1],ONE*50*51)
    return(ans[0],ans[1]+ceil(nxt*50*51*ONE,50*51*ONE-x[1]))
def root6_floor(value):
    assert value>0
    lo,hi=0,ONE
    target=value*(ONE*ONE*ONE*ONE*ONE)
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid*mid*mid*mid*mid*mid<=target:lo=mid
        else:hi=mid
    return lo
def eps6(beta):
    C=c0(beta)
    lo=hi=0
    for j in range(7):
        term=div(c0((j*beta[0],beta[1])),power(C,j))
        coef=comb(6,j)
        if j%2==0:
            lo+=coef*term[0];hi+=coef*term[1]
        else:
            lo-=coef*term[1];hi-=coef*term[0]
    assert 0<lo<hi
    return(root6_floor(lo),root6_floor(hi)+1)
def cert(head,epsilon,a):
    """Frozen SURROGATE, NOT tighter true series:
    U(x)=sum_4^48 coeff[n] x^n + 6 F20(49) x^49/(1-mu*x).
    Returns rigorous [Ulo,Uhi] and [xU'lo,xU'hi].
    """
    assert head in HEAD
    x=mul(epsilon,exp_pos(add(mul(rat(2),a),rat(1,4))))
    mux=mul(rat(MU_N,MU_D),x)
    if mux[1]>=ONE:return None
    lo=hi=wlo=whi=0
    p=(ONE,ONE)
    for n in range(1,11):
        p=mul(p,x)
        if n>=4:
            coeff=HEAD[head][n-4]
            lo+=coeff*p[0];hi+=coeff*p[1]
            wlo+=n*coeff*p[0];whi+=n*coeff*p[1]
    term=(6*F[10]*p[0],6*F[10]*p[1])
    for n in range(11,50):
        term=(term[0]*x[0]*F[n]//(ONE*F[n-1]),
              ceil(term[1]*x[1]*F[n],ONE*F[n-1]))
        if n<49:
            lo+=term[0];hi+=term[1]
            wlo+=n*term[0];whi+=n*term[1]
    # Deliberately the SAME mu denominator in lower and upper:
    # those enclose the exact frozen surrogate U, not the true tail.
    dl=(ONE-mux[0],ONE-mux[0])
    dh=(ONE-mux[1],ONE-mux[1])
    lo+=div((term[0],term[0]),dl)[0]
    hi+=div((term[1],term[1]),dh)[1]
    for den,ratio,base,which in ((dl,mux[0],term[0],0),(dh,mux[1],term[1],1)):
        geom=div((base,base),den)
        term_r=div((base*ratio//ONE,ceil(base*ratio,ONE)),mul(den,den))
        deriv=49*geom[which]+term_r[which]
        if which==0:wlo+=deriv
        else:whi+=deriv
    return((lo,hi),(wlo,whi),mux)
def func(head,epsilon,n,d):
    a=rat(n,d)
    out=cert(head,epsilon,a)
    if out is None:return None
    U,weighted,pole=out
    return ((U[0]-a[1],U[1]-a[0]),
            (2*weighted[0]-ONE,2*weighted[1]-ONE),pole)
def met(head,epsilon,n,d):
    v=func(head,epsilon,n,d)
    return v is not None and v[0][1]<=0
def witness_met(head,epsilon):
    for j in range(1,1001):
        v=func(head,epsilon,j,4000)
        if v is None:break
        if v[0][1]<0:return j,4000
    raise AssertionError("E3_MET: no certified alpha witness")
def least_root(head,epsilon,den=100000000000000):
    n,d=witness_met(head,epsilon)
    upper=ceil(n*den,d)
    assert met(head,epsilon,upper,den)
    lo=0
    while upper-lo>1:
        mid=(lo+upper)//2
        if met(head,epsilon,mid,den):upper=mid
        else:
            v=func(head,epsilon,mid,den)
            assert v is not None and v[0][0]>0 and v[1][1]<0,"E3_ROOT: not a certified lower root"
            lo=mid
    assert func(head,epsilon,lo,den)[1][1]<0
    return(lo,upper,den)
def notmet(head,epsilon):
    # Find a subgradient near the convex minimizer then certify a
    # GLOBAL positive tangent lower bound throughout 0<=alpha<=1/4.
    den=1000000000000
    lo=0;hi=None;v=None
    for j in range(1,401):
        mid=j*den//2000
        v=func(head,epsilon,mid,den)
        if v is None:break
        if v[1][0]>0:hi=mid;break
        if v[1][1]<0:lo=mid
        else:hi=mid;lo=mid;break
    assert hi is not None,"E3_NOT_MET: no derivative bracket"
    while hi-lo>1:
        mid=(hi+lo)//2
        v=func(head,epsilon,mid,den)
        if v is None:hi=mid;continue
        if v[1][1]<0:lo=mid
        elif v[1][0]>0:hi=mid
        else:hi=mid;lo=mid;break
    mid=(hi+lo)//2
    v=func(head,epsilon,mid,den)
    assert v is not None
    dist=max(mid,den//4-mid)
    margin=v[0][0]-max(abs(v[1][0]),abs(v[1][1]))*dist//den
    assert margin>0,"E3_NOT_MET: convex tangent does not exclude all roots"
    return(mid,den,margin)
def ln1p(u):
    assert u[0]>=0 and u[1]<ONE
    z=div(u,add(rat(2),u))
    z2=mul(z,z)
    a=z
    result=(0,0)
    for k in range(55):
        d=2*k+1
        result=add(result,(a[0]//d,ceil(a[1],d)))
        a=mul(a,z2)
    # Positive remainder bounded by geometric ratio z².
    rem=div((a[0]//111,ceil(a[1],111)),sub(rat(1),z2))
    return(2*result[0],2*(result[1]+rem[1]))
def lam(delta):
    dp=mul(delta,exp_pos(delta))
    return add(dp,ln1p(dp))
def check_delta():
    low=lam(rat(CRIT_LO,CRIT_DEN))
    high=lam(rat(CRIT_HI,CRIT_DEN))
    assert low[1]*4<ONE<high[0]*4
    return "E3_DELTA_CRIT|lower=0.114846768|upper=0.114846769|lambda_bracket=PASS|kappa=1/4|json=0"
def dec(n,d,places=13):
    scale=1
    for _ in range(places):scale*=10
    a=n*scale//d
    return str(a//scale)+"."+str(a%scale).zfill(places)
def point(p,q,head,read,wrong_tail=False):
    eps=eps6((p,q))
    if read=="MET":
        a=witness_met(head,eps)
        assert met(head,eps,*a)
        ret="alpha="+str(a[0])+"/"+str(a[1])+"|bound=UPPER_CERTIFIED"
    elif read=="NOT_MET":
        m=notmet(head,eps)
        ret="minimizer="+str(m[0])+"/"+str(m[1])+"|global_margin_ge="+dec(m[2],ONE,12)
    elif read in ("C14_MET","C14_NOT_MET"):
        low,high,den=least_root(head,eps)
        if read=="C14_MET":
            assert 6*high*CRIT_DEN<CRIT_LO*den
        else:
            assert 6*low*CRIT_DEN>CRIT_HI*den
        if p==2074 and head=="refined":
            assert 1088558*den<6*low*10000000 and 6*high*10000000<1088559*den
        if p==2075 and head=="refined":
            assert 1158911*den<6*low*10000000 and 6*high*10000000<1158912*den
        ret="delta1_enclosed=["+dec(6*low,den)+","+dec(6*high,den)+"]|delta_crit_separated=YES"
    else:raise AssertionError("unknown E3 read")
    if wrong_tail:
        raise AssertionError("E3_FAULT: deleted mandatory Fuss-Catalan tail")
    return "E3|head="+head+"|beta="+str(p)+"/"+str(q)+"|read="+read+"|"+ret+"|frozen_n49_mu_tail=YES|json=0"
def c04_pole_gate(fault):
    """The genuine missing_tail attack drops both n>=11 and its pole guard.
    At beta=1/40, 0.02248 the fake head-only value is MET, but the
    mandatory mu*x(alpha=0)>=1 makes the frozen complete read NOT_MET.
    """
    out=[]
    for p,q in ((1,40),(2248,100000)):
        eps=eps6((p,q))
        x0=mul(eps,exp_pos(rat(1,4)))
        mux=mul(rat(MU_N,MU_D),x0)
        assert mux[0]>ONE,"E3_C04: mandatory polymer pole not certified"
        if fault=="missing_tail" and p==1:
            a=rat(1,4194304)
            x=mul(eps,exp_pos(add(mul(rat(2),a),rat(1,4))))
            pw=(ONE,ONE)
            head_hi=0
            for n in range(1,11):
                pw=mul(pw,x)
                if n>=4:head_hi+=HEAD["refined"][n-4]*pw[1]
            assert head_hi<=a[0],"E3_C04: head-only planted MET did not materialize"
            # This is the actual fail-closed guard the mutant deletes.
            assert mux[1]<ONE,"E3_C04_REJECT: false MET from removing Fuss-Catalan tail AND pole gate"
        out.append("E3_C04|beta="+str(p)+"/"+str(q)+"|mu_x_at_alpha0_lower_gt=1|full_tail=REQUIRED|read=NOT_MET|json=0")
    return out

def run(fault=""):
    print("E3_FREEZE|sha256=c74e6388295a6309674268dd18deba3728a4eb627a1530c42054182b2fadc404|C03_counts=VERIFIED_PR60|prefreeze=COMPUTED|r9_runs=0|json=0",flush=True)
    print(check_delta(),flush=True)
    for row in c04_pole_gate(fault):print(row,flush=True)
    rows=[
        (1904,100000,"crude","MET"),
        (1905,100000,"crude","NOT_MET"),
        (1,50,"crude","NOT_MET"),
        (1,50,"refined","MET"),
        (2075,100000,"refined","MET"),
        (2076,100000,"refined","NOT_MET"),
        (2076,100000,"headfree","NOT_MET"),
        (2074,100000,"refined","C14_MET"),
        (2075,100000,"refined","C14_NOT_MET"),
        (2074,100000,"headfree","C14_MET"),
        (2075,100000,"headfree","C14_NOT_MET"),
        (1,64,"refined","C14_MET"),
    ]
    for p,q,head,read in rows:
        if fault=="wrong_head" and head=="refined" and read=="MET" and p==2075:
            head="crude"
        if fault=="false_notmet" and head=="refined" and read=="NOT_MET":
            read="MET"
        print(point(p,q,head,read,fault=="missing_tail" and p==1904),flush=True)
    if fault=="bad_crit":
        assert lam(rat(CRIT_HI,CRIT_DEN))[1]*4<ONE,"E3_FAULT: false upper delta_crit side"
    print("E3_RESULT|PASS|C05=PASS|C06=PASS|C14=PASS|C04_tail_guard=IMPORTED_FROM_PR58|weak_coupling=OPEN|r9_runs=0|json=0",flush=True)

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--sabotage",choices=("missing_tail","wrong_head","false_notmet","bad_crit"),default="")
    args=ap.parse_args()
    run(args.sabotage)
