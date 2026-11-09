# reviewer float check of W01/W03 alias formulas (not an engine)
import math, itertools
from fractions import Fraction as Fr
def khat2(k): return sum(4*math.sin(x/2)**2 for x in k)
def Cline(kappa,b,d):
    # polarization mu=0, p = kappa e_1; aliases n_mu=0, n_perp in Z_b^{d-1}
    s=0.0
    for n in itertools.product(range(b),repeat=d-1):
        k=[(kappa+2*math.pi*n[0])/b]+[2*math.pi*m/b for m in n[1:]]
        s+=1/khat2(k)
    return b**(2-d)*s
def r(kappa,b,d): return (1/(4*math.sin(kappa/2)**2))/Cline(kappa,b,d)
def A(b,d):
    s=0.0
    for n in itertools.product(range(b),repeat=d-1):
        if any(n): s+=1/khat2([2*math.pi*m/b for m in n])
    return b**(-2)*s-(1-1/b**2)/12
print('W01 k=1 profile:')
for t,q in [(Fr(1,16),Fr(12689633,12736932)),(Fr(1,8),Fr(813281,825252)),(Fr(1,4),Fr(56033,59172)),(Fr(1,2),Fr(4961,5892)),(Fr(1),Fr(833,1212))]:
    kap=2*math.atan(float(t)); print(t, '%.15f'%r(kap,2,4), '%.15f'%float(q))
print('corner b=2', r(math.pi,2,4), 15/28)
print('corner b=4', r(math.pi,4,4), 25823/98640)
print('corner b=8 %.12f'%r(math.pi,8,4))
for b in (2,4,8): print('A_b',b,'%.12f'%A(b,4), 'A/b %.5f'%(A(b,4)/b), 'b*r %.6f'%(b*r(math.pi,b,4)))
print(23/96,1367/1920)
# small p check of marginality and slope
for b in (2,4):
    kap=1e-3; ph=4*math.sin(kap/2)**2
    print('slope check b',b, (1/r(kap,b,4)-1)/ph)
# W03 d=3
print('W03 d=3 profile:')
for t,q in [(Fr(1,16),Fr(2057,4120)),(Fr(1,8),Fr(521,1048)),(Fr(1,4),Fr(137,280)),(Fr(1,2),Fr(41,88)),(Fr(1),Fr(17,40))]:
    kap=2*math.atan(float(t)); print(t,'%.15f'%r(kap,2,3),'%.15f'%float(q))
print('corner d=3', r(math.pi,2,3), 3/8)
for b in (2,4,8):
    print('d3 b',b,'b*r=%.10f'%(b*r(math.pi,b,3)))
# d=3 slope: normalized rn = r * b^{4-d}? define 1/(r b^{4-d}) = 1 + A phat^2
for b in (2,4,8):
    kap=1e-4; ph=4*math.sin(kap/2)**2
    print('d3 slope b',b,'%.10f'%((1/(r(kap,b,3)*b)-1)/ph))
print(3/32,73/384,73/384-3/32,37/384, math.log(2)/(2*math.pi))
# d=2
for b in (2,4,8):
    for kap in (math.pi/2,2*math.pi/3,math.pi): print('d2',b,kap, r(kap,b,2)*b*b)
