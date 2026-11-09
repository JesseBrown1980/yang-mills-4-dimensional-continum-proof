from s_lane import *
from fractions import Fraction as Fr
E=D(1).exp()
PI=D('3.14159265358979323846264338327950288419716939937510582097494459')
from math import comb
def cat(m): return comb(2*m,m)//(m+1)
def proj_cP(s):
    # chi coefficient of log c0(2 s sqrt(2+chi)) : expand f(u)=log c0(2s sqrt(u)) as power series in u=2+chi, project u^j onto chi.
    # c0(2s sqrt u) = sum_m (s^2 u)^m/(m!(m+1)!) ; log series in w=s^2 u
    N=30
    c=[D(1)/(D(__import__('math').factorial(m))*D(__import__('math').factorial(m+1))) for m in range(N)]
    # log(1+X) series coefficients in w
    L=[D(0)]*N
    # compute log of power series c (c[0]=1)
    for n in range(1,N):
        L[n]=c[n]-sum((D(k)*L[k]*c[n-k] for k in range(1,n)),D(0))/n
    # <chi,(2+chi)^j> under Haar: chi=2cos t; E[chi^m]=Cat(m/2) for even m
    def Echi(m): return D(cat(m//2)) if m%2==0 else D(0)
    tot=D(0)
    for j in range(1,N):
        # (2+chi)^j = sum_i C(j,i) 2^{j-i} chi^i ; <chi, .> = sum C(j,i)2^{j-i}E[chi^{i+1}]
        pj=sum(comb(j,i)*D(2)**(j-i)*Echi(i+1) for i in range(j+1))
        tot+=L[j]*s**(2*j)*pj
    return tot
for s in (D(1)/2000, D(1)/4096):
    din=12*s*D('1.5').exp()
    dp=din*din.exp()
    cc=cfun(din)
    dout=3*E*c0(4*s).ln()
    cP=proj_cP(s)
    low=E*abs(cP)/(D(8)/(3*PI))
    low2=E*abs(cP)/D('0.8489')
    print('s=%s din=%.8f 2dp=%.7f c=%.6f dout=%.6e ratio=%.6e cP=%.8e s2/2=%.8e lower=%.5e lower(8489)=%.5e low/(c din)=%.4e'%(s,din,2*dp,cc,dout,dout/din,cP,s*s/2,low,low2,low/(cc*din)))
