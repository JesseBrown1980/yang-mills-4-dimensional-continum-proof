# Judge float sanity checks (NOT an engine): small-large-field and coupling-flow headline numbers.
import numpy as np, math
from math import comb
# R03 Phi_0
def phi0(L, beta):
    Ns = L**4; Nf = 3*Ns+1; Np = 6*Ns
    t = 3*Nf/(32*beta*Np)
    th = math.acos(1-t)
    h = (2*th - math.sin(2*th))/(2*math.pi)
    return (-Nf*math.log(h) + 1.5*Nf)/Ns
for L in (4, 8):
    print("R03 Phi0", L, [round(phi0(L, b), 9) for b in (16, 64, 256, 1024, 4096)])
print("R03 const", [phi0(4,b) - 1.5*(3*256+1)/256*math.log(b) for b in (16, 4096)], [phi0(8,b) - 1.5*(3*4096+1)/4096*math.log(b) for b in (16,4096)])
# R11 cubic root
r = min(np.roots([1, -18, 80, -48]).real); print("R11 lambda0*", r)
# R12 r_1, r_2 on torus L via FFT Green's function
def green(L):
    k = 2*np.pi*np.arange(L)/L
    s = 4*np.sin(k/2)**2
    den = s[:,None,None,None]+s[None,:,None,None]+s[None,None,:,None]+s[None,None,None,:]
    den[0,0,0,0] = np.inf
    return np.real(np.fft.ifftn(1/den))
def loopvar(G, R):
    L = G.shape[0]
    # square R x R in plane (0,1), Feynman gauge: sum over parallel link pairs
    links = []
    for i in range(R):
        links.append(((i,0), 0, +1)); links.append(((i,R), 0, -1))
        links.append(((R,i), 1, +1)); links.append(((0,i), 1, -1))
    V = 0.0
    for (x, mu, s) in links:
        for (y, nu, t) in links:
            if mu != nu: continue
            d = ((x[0]-y[0]) % L, (x[1]-y[1]) % L, 0, 0)
            V += s*t*G[d]
    return V
for L in (8, 16):
    G = green(L)
    v1, v2, v4 = loopvar(G, 1), loopvar(G, 2), loopvar(G, 4)
    print("R12 L", L, "V11", v1, "r1", v2/v1, "r2", v4/v1, "r2/r1", v4/v2)
# R13/R12 Q(3/2,y)
def Q32(y): return math.erfc(math.sqrt(y)) + 2*math.sqrt(y/math.pi)*math.exp(-y)
print("Q32(2),Q32(8),Q32(6),Q32(12)", Q32(2), Q32(8), Q32(6), Q32(12))
print("R12 LF probs p^2=2:", Q32(8), Q32(8/2.75), Q32(8/6.5))
# R14
b0 = 11*math.log(2)/(3*math.pi**2); print("b0'", b0, [math.log(2**e/16)/b0 for e in (20,40,80)], 1/256+1/(16*b0))
# CT06
for e in (24, 23):
    beta = 2.0**-e; x = beta*7776/0.25; hw = 2*0.5*x**12/(1-x**2)
    poly = beta**4/64 - beta**6/384
    print("CT06 2^-%d rel half-width" % e, hw/poly)
# CT12 alias A_b and corner r
def khat2(k): return sum(4*math.sin(ki/2)**2 for ki in k)
def A_line(b):
    s = 0.0
    for n1 in range(b):
        for n2 in range(b):
            for n3 in range(b):
                if (n1,n2,n3) == (0,0,0): continue
                s += 1/khat2((2*math.pi*n1/b, 2*math.pi*n2/b, 2*math.pi*n3/b))
    return s/b**2 - (1-1/b**2)/12
def r_corner(b, d=4):
    p = math.pi
    C = 0.0
    for n in np.ndindex(*([b]*(d-1))):
        # nu direction carries p; others perpendicular aliases; mu has n_mu = 0
        k = [(p + 2*math.pi*n[0])/b] + [2*math.pi*ni/b for ni in n[1:]]
        C += 1/khat2(k)
    C *= b**(2-d)
    return (1/khat2([p]))/C
for b in (2, 4, 8):
    print("CT12 b", b, "A", A_line(b), "A/b", A_line(b)/b, "r_corner", r_corner(b), "b r", b*r_corner(b))
print("15/28", 15/28, "25823/98640", 25823/98640, "1367/1920", 1367/1920)
for b in (2,4,8):
    print("CT14 d=3 b", b, "b r", b*r_corner(b, d=3))
