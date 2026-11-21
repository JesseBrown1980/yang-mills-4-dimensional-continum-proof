from fractions import Fraction as Fr
import itertools, math
# CT12 A_b at b=2,4 (judge spot check, floats ok here: not an engine)
def A(b):
    vals={0:Fr(0)}
    s=Fr(0)
    # k^2 per coordinate 4 sin^2(pi n/b); b=2,4 rational
    tab={2:{0:Fr(0),1:Fr(4)},4:{0:Fr(0),1:Fr(2),2:Fr(4),3:Fr(2)}}[b]
    for n in itertools.product(range(b),repeat=3):
        if n==(0,0,0): continue
        s+=1/sum(tab[i] for i in n)
    return s/b**2-(1-Fr(1,b*b))/12
print("A1",A(2),"A2",A(4),Fr(1367,1920))
# polymer-norm eps6 check (float, judge only)
from math import comb, factorial
def c0(x,M=60): return sum((x/2)**(2*m)/(factorial(m)*factorial(m+1)) for m in range(M))
def eps6(b): 
    v=sum(comb(6,k)*(-1)**(6-k)*c0(k*b)/c0(b)**k for k in range(7))
    return v**(1/6)
for b in (1/1000,1/100,1/64,1/50,1/45,1/10,1,4):
    print(b,eps6(b))
mu=20**20/19**19
print("mu",mu)
# beta_wall
lo,hi=0.02,0.03
for _ in range(60):
    m=(lo+hi)/2
    if mu*math.exp(0.25)*eps6(m)<1: lo=m
    else: hi=m
print("wall",lo)
# R11 root
import numpy as np
print(np.roots([1,-18,80,-48]))
# Q(3/2,y)
def Q(y): return math.erfc(math.sqrt(y))+2*math.sqrt(y/math.pi)*math.exp(-y)
print(Q(6),Q(12),Q(2),Q(8))
# R12: k=1 prob at r=2.75 p^2=2 -> Q(3/2,4p^2/r)?
print(Q(8/2.75),Q(8/6.5),Q(8))
