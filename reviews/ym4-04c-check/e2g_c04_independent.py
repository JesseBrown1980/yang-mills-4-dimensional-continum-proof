#!/usr/bin/env python3
"""Independent YM4-04C C04 check, via even SU2 Haar moments/Catalan numbers.
No code is shared with the E2g engine. This is a PARTIAL independent check,
not the full planned YM4-04C Rust checker. All arithmetic uses integer pairs.
"""
from math import comb, factorial, gcd

def ipow(base, exponent):
    if exponent < 0:
        raise AssertionError("negative integer exponent")
    value = 1
    for _ in range(exponent):
        value *= base
    return value

def r(a, b=1):
    assert b>0
    k=gcd(a,b)
    return (a//k,b//k)

def plus(x,y):return r(x[0]*y[1]+y[0]*x[1],x[1]*y[1])
def minus(x,y):return plus(x,(-y[0],y[1]))
def times(x,y):return r(x[0]*y[0],x[1]*y[1])
def ratio(x,y):
    assert y[0]>0
    return r(x[0]*y[1],x[1]*y[0])
def pp(x,n):return r(ipow(x[0],n),ipow(x[1],n))
def less(x,y):return x[0]*y[1]<y[0]*x[1]

def haar_exp_by_even_moments(beta):
    """Integrate Taylor exp(beta a) against SU2 Haar:
    E[a^(2m)]=Catalan(m)/4^m, E[a^(2m+1)]=0.
    This differs from the engine's positive Bessel-term recurrence.
    """
    b2=times(beta,beta)
    total=r(0)
    for m in range(12):
        cat=comb(2*m,m)//(m+1)
        term=r(cat*ipow(b2[0],m),ipow(b2[1],m)*ipow(4,m)*factorial(2*m))
        total=plus(total,term)
    m=12
    cat=comb(2*m,m)//(m+1)
    omitted=r(cat*ipow(b2[0],m),ipow(b2[1],m)*ipow(4,m)*factorial(2*m))
    # Every term after m=0 has ratio beta^2/[4(m+1)(m+2)] <= beta^2/8.
    future=ratio(b2,r(8))
    assert less(future,r(1))
    return total,plus(total,ratio(omitted,minus(r(1),future)))

def exp_quarter_via_integral_series():
    total=r(0)
    for k in range(12):
        total=plus(total,r(1,ipow(4,k)*factorial(k)))
    omitted=r(1,4**12*factorial(12))
    # Future adjacent ratios <=1/(4*13).
    return total,plus(total,ratio(omitted,minus(r(1),r(1,52))))

def sixth_moment(beta):
    normalized_lower,normalized_upper=haar_exp_by_even_moments(beta)
    lower=r(0);upper=r(0)
    for j in range(7):
        lo,hi=haar_exp_by_even_moments(times(r(j),beta))
        c=r(comb(6,j))
        if j%2==0:
            lower=plus(lower,ratio(times(c,lo),pp(normalized_upper,j)))
            upper=plus(upper,ratio(times(c,hi),pp(normalized_lower,j)))
        else:
            lower=minus(lower,ratio(times(c,hi),pp(normalized_lower,j)))
            upper=minus(upper,ratio(times(c,lo),pp(normalized_upper,j)))
    assert less(r(0),lower) and less(lower,upper)
    return lower,upper

def main():
    mu=r(20**20,19**19)
    elo,ehi=exp_quarter_via_integral_series()
    for name,beta,threshold,below in [
        ("quarter_beta",r(1,40),r(11125,10000),False),
        ("wall_lower",r(2247,100000),r(1),True),
        ("wall_upper",r(2248,100000),r(100035,100000),False)
    ]:
        elo6,ehi6=sixth_moment(beta)
        low=times(elo6,pp(times(mu,elo),6))
        hi=times(ehi6,pp(times(mu,ehi),6))
        passed=less(hi,r(1)) if below else less(pp(threshold,6),low)
        assert passed,"independent Haar moment C04 bracket failed at "+name
        print("YM4_04C_E2G_INDEPENDENT|row=C04|point="+name+
              "|route=HAAR_EVEN_MOMENTS_CATALAN|status=PASS"+
              "|frozen_prefreeze=COMPUTED|json=0")
    print("YM4_04C_E2G_INDEPENDENT_RESULT|PASS|three_C04_checks=3|shared_code=NO|full_04C_Rust_checker=NOT_RUN|json=0")

if __name__=="__main__":
    main()
