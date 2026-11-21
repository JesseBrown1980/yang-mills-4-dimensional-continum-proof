import importlib.util, sys
spec = importlib.util.spec_from_file_location('cp', 'check_polymer.py')
src = open('check_polymer.py').read().split("for beta in [F(1,1000)")[0]
exec(src)
def Shf(x, n0=11, nmax=48):
    if mu*x >= 1: return None
    s = sum(D(6)*Fc(n)*x**n for n in range(n0, nmax+1))
    return s + D(6)*Fc(nmax+1)*x**(nmax+1)/(1-mu*x)
def Smodel(x):  # head: N(4)=1, N(6)=12, N(8)=200, N(10)=5000 (a small-count model), tail 6F from 11
    base = Shf(x)
    if base is None: return None
    return base + x**4 + 12*x**6 + 200*x**8 + 5000*x**10
def C0g(beta, Sf, ngrid=129):
    e = eps6(beta); best=None
    for i in range(ngrid):
        b = D(1)/4 + D(i)/64
        a = D(0); ok=False
        for it in range(3000):
            s = Sf(e*(2*a+b).exp())
            if s is None or s > D(1)/4: break
            if abs(s-a) < D(10)**-40: ok=True; a=s; break
            a = s
        if ok and a <= D(1)/4:
            d1 = 12*a*(-4*(b-D(1)/4)).exp()
            if best is None or d1 < best[0]: best=(d1,a,b)
    return best
def c_of(d):
    dp = d*d.exp(); k=D(1)/4
    if 2*dp > k/2: return None
    m = max((-(k/2-2*dp)*n).exp() - (-k*n/2).exp() for n in range(4, 400))
    return d.exp()*((-4*k).exp() + m)
for beta in [F(1,100), F(1,64), F(1,50), F(2075,100000), F(2076,100000), F(1958,100000), F(1959,100000)]:
    r = C0g(beta, Shf); rm = C0g(beta, Smodel)
    print(beta, 'headfree', None if r is None else ('%.6e'%r[0], 'c=%s'%(None if c_of(r[0]) is None else '%.5f'%c_of(r[0])), 'b=%s'%r[2]),
          'model', None if rm is None else ('%.6e'%rm[0],))
