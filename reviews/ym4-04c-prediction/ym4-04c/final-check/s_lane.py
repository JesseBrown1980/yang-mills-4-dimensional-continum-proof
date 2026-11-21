# Final-check reviewer scratch (Decimal, not an engine). Independent route: Newton from a=0 for the least KP root.
from decimal import Decimal as D, getcontext
from fractions import Fraction as Fr
from math import comb
import sys
getcontext().prec = 90
KAP = D(1)/4
def dec(q): return D(q.numerator)/D(q.denominator) if isinstance(q,Fr) else D(q)
def c0(x):
    x=dec(x); h=(x/2)**2; t=D(1); s=D(0); m=0
    while True:
        s+=t; t=t*h/((m+1)*(m+2)); m+=1
        if m>6 and t < D(10)**-85*s: return s
def eps6(beta):
    b=dec(beta); cb=c0(b)
    v=sum(comb(6,k)*(-1)**(6-k)*c0(k*b)/cb**k for k in range(7))
    return v**(D(1)/6)
def F20(n): return comb(20*n,n)//(19*n+1)
MU=D(20)**20/D(19)**19
F6={n:6*D(F20(n)) for n in range(1,60)}
HEADS={'crude':{}, 'free':{n:0 for n in range(4,11)}, 'meas':{4:1,5:0,6:12,7:0,8:32,9:32,10:304}}
def S_and_dS(x, head):
    # returns S(x), x S'(x)
    if MU*x>=1: return None,None
    s=D(0); xs=D(0)
    for n in range(4,49):
        c = D(head[n]) if n in head else F6[n]
        t=c*x**n; s+=t; xs+=n*t
    q=1-MU*x; T=F6[49]*x**49/q
    s+=T; xs+= T*(49 + MU*x/q)
    return s,xs
def least_a(e,b,head):
    # g(a)=S(e*exp(2a+b))-a ; g'(a)=2 x S'(x) - 1 ; Newton from 0
    a=D(0)
    for it in range(200):
        x=e*(2*a+b).exp()
        s,xs=S_and_dS(x,head)
        if s is None: return None
        g=s-a; gp=2*xs-1
        if g<=D(10)**-70: return a
        if gp>=0: return None
        an=a-g/gp
        if an>D(1)/4: return None
        if abs(an-a)<D(10)**-60: return an
        a=an
    return a
def C0(beta,head,imax=320,mode='delta'):
    e=eps6(beta); best=None
    for i in range(imax+1):
        b=KAP+D(i)/64
        a=least_a(e,b,head)
        if a is None: continue
        v = 12*a*(-4*(b-KAP)).exp() if mode=='delta' else D('0.8489')*12*a*(-8*b).exp()
        if best is None or v<best[0]: best=(v,a,i)
        if mode=='delta' and i>40: break
    return best
def cfun(d):
    dp=d*d.exp()
    if 2*dp>KAP/2: return None
    r=2*dp; m=max((-(KAP/2-r)*n).exp()-(-KAP*n/2).exp() for n in range(4,400))
    return d.exp()*((-4*KAP).exp()+m)
if __name__=='__main__':
    w=sys.argv[1]
    if w=='eps':
        for q in [Fr(1,1000),Fr(1,100),Fr(1,64),Fr(1,50),Fr(1,45),Fr(1,40),Fr(1,10),Fr(1),Fr(4)]:
            e=eps6(q); print(q, '%.12e'%e, 'eps/beta=%.8f'%(e/dec(q)))
        print('limit', '%.8f'%(D(5)**(D(1)/6)/2))
        print('mu', MU)
    elif w=='wall':
        for f,lab in ((D(KAP).exp()*MU,'wall(1/4)'),(MU,'kappa0')):
            lo,hi=D('0.01'),D('0.04')
            for _ in range(60):
                m=(lo+hi)/2
                if f*eps6(m)>=1: hi=m
                else: lo=m
            print(lab,'%.8f'%lo)
        for q in [Fr(1,45),Fr(1,40),Fr(1,18),Fr(1,10),Fr(1),Fr(4)]:
            print(q,'mu e^1/4 eps=%.6f'%(MU*KAP.exp()*eps6(q)))
        pi=D('3.14159265358979323846264338327950288419716939937510582097494459')
        print('one-loop', '%.10f'%(D(11)/(3*pi*pi)*D(2).ln()))
    elif w=='pts':
        for name in sys.argv[2].split(','):
            for q in [Fr(x) for x in sys.argv[3].split(',')]:
                r=C0(q,HEADS[name])
                if r is None: print(name,q,'C0 NOT_MET'); continue
                c=cfun(r[0])
                print(name,q,'delta1=%.8e a=%.8e i=%d'%(r[0],r[1],r[2]),"2d'=%.6f"%(2*r[0]*r[0].exp()),'c=',None if c is None else '%.7f'%c, flush=True)
