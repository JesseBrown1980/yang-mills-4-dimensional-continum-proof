# Referee spot-check of polymer-norm numbers (Decimal, high precision; not an engine).
from decimal import Decimal as D, getcontext
from fractions import Fraction as F
from math import comb
getcontext().prec = 80

def c0(x, terms=80):
    x = F(x); s = F(0); t = F(1)  # (x/2)^{2m}/(m!(m+1)!)
    for m in range(terms):
        if m == 0: t = F(1)
        else: t = t * (x/2)**2 / (m*(m+1))
        s += t
    return s

def eps6(beta):
    b = F(beta)
    c = c0(b)
    s = sum(comb(6,k)*(-1)**(6-k)*c0(k*b)/c**k for k in range(7))
    v = D(s.numerator)/D(s.denominator)
    return v ** (D(1)/D(6))

def Fc(n): return D(comb(20*n, n))/D(19*n+1)
mu = D(20)**20/D(19)**19
def S(x, nmax=48):
    s = sum(D(6)*Fc(n)*x**n for n in range(4, nmax+1))
    if mu*x >= 1: return None
    return s + D(6)*Fc(nmax+1)*x**(nmax+1)/(1-mu*x)

def C0(beta, ngrid=129):
    e = eps6(beta); best=None
    for i in range(ngrid):
        b = D(1)/4 + D(i)/64
        a = D(0); ok=False
        for it in range(2000):
            x = e*(2*a+b).exp()
            s = S(x)
            if s is None or s > D(1)/4: break
            if abs(s-a) < D(10)**-40: ok=True; a=s; break
            a = s
        if ok and a <= D(1)/4:
            d1 = 12*a*(-4*(b-D(1)/4)).exp()
            if best is None or d1 < best[0]: best=(d1,a,b)
    return best

for beta in [F(1,1000),F(1,100),F(1,64),F(1,50),F(1,45),F(1,40),F(1,10),F(1),F(4)]:
    e = eps6(beta)
    print('eps6', beta, '%.10e'%e, 'mu e^1/4 eps', '%.6f'%(mu*D(0.25).exp()*e))
print('mu', mu)
for beta in [F(1,100), F(1,64), F(1904,100000), F(1905,100000), F(1,50)]:
    print('C0crude', beta, C0(beta))
