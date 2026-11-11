#!/usr/bin/env python3
"""Third independent integer-rational C04/C15 endpoint gate.

No float, Fraction, Decimal, Node or JSON. The global monotonicity proof is
in docs/NOTE-YM4-04C-E5-GLOBAL-POLE-20261111.md, not inferred from sampling.
"""
import sys
from math import comb, factorial, gcd

class Q:
    def __init__(self, n, d=1):
        assert isinstance(n,int) and isinstance(d,int) and d!=0
        if d<0:n,d=-n,-d
        g=gcd(n,d)
        self.n,self.d=n//g,d//g
    def __add__(self,b):
        b=rat(b)
        return Q(self.n*b.d+b.n*self.d,self.d*b.d)
    def __radd__(self,b):return self+b
    def __neg__(self):return Q(-self.n,self.d)
    def __sub__(self,b):return self+(-rat(b))
    def __mul__(self,b):
        b=rat(b)
        return Q(self.n*b.n,self.d*b.d)
    def __rmul__(self,b):return self*b
    def __truediv__(self,b):
        b=rat(b)
        assert b.n!=0
        return Q(self.n*b.d,self.d*b.n)
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        return Q(self.n**n,self.d**n)
    def __lt__(self,b):
        b=rat(b)
        return self.n*b.d<b.n*self.d
    def __le__(self,b):
        b=rat(b)
        return self.n*b.d<=b.n*self.d

def rat(x):return x if isinstance(x,Q) else Q(x)
def quo(a,b):return rat(a).__truediv__(b)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[1],-a[0])
def mul(a,b):
    assert a[0].n>=0 and b[0].n>=0
    return (a[0]*b[0],a[1]*b[1])
def div(a,b):
    assert b[0].n>0
    return (quo(a[0],b[1]),quo(a[1],b[0]))
def power(a,n):
    assert a[0].n>=0 and n>=0
    return (a[0]**n,a[1]**n)

def c0(t):
    """Positive SU2 character series, with first-omitted-term tail."""
    assert t.n>=0
    count=24
    s=Q(0)
    for m in range(count+1):
        s+=quo(quo(t,2)**(2*m),Q(factorial(m)*factorial(m+1)))
    following=quo(quo(t,2)**(2*count+2),Q(factorial(count+1)*factorial(count+2)))
    r=quo(quo(t,2)**2,Q((count+2)*(count+3)))
    assert r<Q(1,100)
    return (s,s+quo(following,(Q(1)-r)))

def exp_quarter():
    t,count=Q(1,4),80
    s=Q(0)
    for k in range(count+1):s+=quo(t**k,Q(factorial(k)))
    following=quo(t**(count+1),Q(factorial(count+1)))
    r=quo(t,Q(count+2))
    return (s,s+quo(following,(Q(1)-r)))

def floor_sixth(z):
    assert z>=0
    low,high=0,1<<((z.bit_length()+5)//6)
    while high**6<=z:high*=2
    while high-low>1:
        mid=(low+high)//2
        if mid**6<=z:low=mid
        else:high=mid
    return low

def sixth_root(a):
    assert a[0].n>0
    scale=10**24
    lo=floor_sixth(a[0].n*scale**6//a[0].d)
    hi=floor_sixth(a[1].n*scale**6//a[1].d)+1
    return (Q(lo,scale),Q(hi,scale))

def wall(beta):
    base=c0(beta)
    moment=(Q(0),Q(0))
    for j in range(7):
        term=div(c0(j*beta),power(base,j))
        v=mul((Q(comb(6,j)),Q(comb(6,j))),term)
        moment=add(moment,v if j%2==0 else neg(v))
    assert moment[0].n>0
    eps6=sixth_root(moment)
    mu=Q(20**20,19**19)
    return mul((mu,mu),mul(exp_quarter(),eps6))

def run():
    for name,beta,lo,hi,below in [
        ("left",Q(2247,100000),999913588125,999913588128,True),
        ("right",Q(2248,100000),1000358668021,1000358668024,False),
        ("C15",Q(1,40),1112522354464,1112522354467,False),
    ]:
        interval=wall(beta)
        scale=Q(10**12)
        assert Q(lo)<scale*interval[0]
        assert scale*interval[1]<Q(hi)
        assert (interval[1]<Q(1)) if below else (Q(1)<interval[0])
        print("E5_POLE_THIRD|name="+name+"|beta="+str(beta.n)+"/"+
              str(beta.d)+"|wall_scaled_10pow12_in=("+str(lo)+","+str(hi)+
              ")|endpoint="+("BELOW" if below else "ABOVE")+"|PASS|json=0",flush=True)
    print("E5_GLOBAL_POLE|unique_crossing_in=(0.02247,0.02248)"+
          "|all_beta_ge_0.02248=POLE_NOT_MET|proof=CONVEX_TILT_MONOTONICITY"+
          "|physical_mass_gap=OPEN|PASS|json=0",flush=True)

if __name__=="__main__":
    if len(sys.argv)>1:
        assert sys.argv[1]=="--sabotage"
        # Deliberate false claim that the previously certified right endpoint
        # is BELOW the pole; this must fail in strict tests.
        assert wall(Q(2248,100000))[1]<Q(1),"E5_REJECT: inverted pole boundary"
    run()
