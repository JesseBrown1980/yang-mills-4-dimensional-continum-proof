from fractions import Fraction as Fr
from math import comb, factorial
def c0(x,M=40): return sum((x/2)**(2*m)/(factorial(m)*factorial(m+1)) for m in range(M))
def e6(b):
    b=Fr(b)
    v=sum(comb(6,k)*(-1)**(6-k)*c0(k*b)/c0(b)**k for k in range(7))
    return float(v)**(1/6)
for b in (Fr(1,1000),Fr(1,100),Fr(1,45),Fr(1,40)):
    print(b, e6(b))
