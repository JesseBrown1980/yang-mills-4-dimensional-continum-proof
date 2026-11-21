from decimal import Decimal as D, getcontext
from fractions import Fraction as F
import itertools, math
getcontext().prec = 50
pi = D('3.14159265358979323846264338327950288419716939937510')
def dacos(x):  # Newton on cos
    th = D(math.acos(float(x)))
    for _ in range(60):
        th = th - (cosd(th)-x)/(-sind(th))
    return th
def sind(x):
    s=D(0); t=x; n=1
    while abs(t) > D(10)**-48:
        s+=t; t = -t*x*x/((n+1)*(n+2)); n+=2
    return s
def cosd(x):
    s=D(0); t=D(1); n=0
    while abs(t) > D(10)**-48:
        s+=t; t = -t*x*x/((n+1)*(n+2)); n+=2
    return s
# R03 Phi_0
for L in (4,8):
    Ns=L**4; Nf=3*Ns+1; Np=6*Ns
    out=[]
    for beta in (16,64,256,1024,4096):
        t = D(3*Nf)/(32*beta*Np)
        th = dacos(1-t)
        h = (2*th - sind(2*th))/(2*pi)
        Phi = (-Nf*h.ln() + D(3)/2*Nf)/Ns
        out.append('%.9f'%Phi)
    print('R03 L=%d'%L, out)
# R11 root
lo,hi=D('0.5'),D('0.9')
f=lambda l: l**3-18*l**2+80*l-48
for _ in range(100):
    m=(lo+hi)/2
    if f(lo)*f(m)<=0: hi=m
    else: lo=m
print('R11 root', '%.12f'%lo)
# CT12 line map alias formula, d=4, transverse polarization mu=0, p along nu=1
def khat2(q): return sum(4*math.sin(x/2)**2 for x in q)
def Cprime(p, b, d=4):
    s=0.0
    for n in itertools.product(range(b), repeat=d-1):
        q=[(p[i+1]+2*math.pi*n[i])/b for i in range(d-1)]
        s+=1/khat2(q)
    return s*b**(2-d)
for b in (2,4,8):
    pc=[0,math.pi,0,0]
    r = (1/khat2([math.pi]))/Cprime(pc,b)
    # slope A_b
    A = sum(1/khat2([2*math.pi*n[i]/b for i in range(3)]) for n in itertools.product(range(b),repeat=3) if any(n))/b**2 - (1-1/b**2)/12
    print('CT12 b=%d corner r=%.10f  A=%.10f'%(b,r,A))
print('targets r2=%.10f A2=%.10f'%(25823/98640, 1367/1920))
# R10 rho4 at t=1/16
for t in (F(1,16),F(1,8),F(1,4),F(1,2),F(1),None):
    S = F(1) if t is None else t*t/(1+t*t)
    rho = F(4)/(4+24*S/(S+8)+20*S/(S+24))
    print('R10 rho4', t, rho)
