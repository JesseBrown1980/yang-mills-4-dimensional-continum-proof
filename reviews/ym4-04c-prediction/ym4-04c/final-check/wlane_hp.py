from decimal import Decimal as D, getcontext
import itertools
getcontext().prec=50
PI=D('3.14159265358979323846264338327950288419716939937510582')
def sin(x):
    s=D(0); t=x; k=1
    while abs(t)>D(10)**-48:
        s+=t; t=-t*x*x/((k+1)*(k+2)); k+=2
    return s
def s2(x): return 4*sin(x/2)**2
def A(b,d):
    s=D(0)
    for n in itertools.product(range(b),repeat=d-1):
        if any(n): s+=1/sum(s2(2*PI*m/b) for m in n)
    return s/b**2-(1-D(1)/b**2)/12
def corner(b,d):
    s=D(0)
    for n in itertools.product(range(b),repeat=d-1):
        k=[(PI+2*PI*n[0])/b]+[2*PI*m/b for m in n[1:]]
        s+=1/sum(s2(x) for x in k)
    C=D(b)**(2-d)*s
    return (D(1)/4)/C
for d in (3,4):
    for b in (2,4,8):
        print('d',d,'b',b,'A=%.14f'%A(b,d),'r_corner=%.14f'%corner(b,d),'b^{k}r(norm)=%.14f'%(corner(b,d)*b**(4-d)*b if d==3 else corner(b,d)*b))
a2,a4,a8=A(2,3),A(4,3),A(8,3)
print('d3 increments', a4-a2, a8-a4, D(37)/384)
