# Attack question (i): does the KP condition close with a(G) = alpha #off, d(G) = theta #G, alpha = t = delta',
# theta = kappa, when #G is read literally as the number of fine links of the objects of G?
# An explicit admissible input on the b = 2 geometry at scale k. Fractions with outward exp enclosures.
from fractions import Fraction as F
from itertools import combinations
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from g1tg_constants import exp_iv, rdn, rup, dprime, fmt

M = 8  # fine side at scale k (any even M >= 8 gives the same local picture)

def link(x, mu):
    return (tuple(c % M for c in x), mu)

def is_line(l):
    x, mu = l
    return all(x[r] % 2 == 0 for r in range(4) if r != mu)

def plaquette(x, mu, nu):
    e = [[1 if i == j else 0 for i in range(4)] for j in range(4)]
    add = lambda a, b: tuple(p + q for p, q in zip(a, b))
    return frozenset([link(x, mu), link(add(x, e[mu]), nu), link(add(x, e[nu]), mu), link(x, nu)])

p0 = plaquette((0, 0, 0, 0), 0, 1)
offs0 = sorted(l for l in p0 if not is_line(l))
eB, eA = offs0  # sorted: ((0,1,0,0),0) then ((1,0,0,0),1)
pA = plaquette((1, 0, 0, 0), 1, 2)   # holds eA = ((1,0,0,0),1)
pB = plaquette((0, 1, 0, 0), 0, 3)   # holds eB = ((0,1,0,0),0)
assert eA in pA and eB in pB, (eA, eB)
assert not (pA & pB) and len(p0 & pA) == 1 and len(p0 & pB) == 1
objs = {'p0': p0, 'pA': pA, 'pB': pB}
for k, o in objs.items():
    print(k, 'links', len(o), 'off', sum(1 for l in o if not is_line(l)), 'line', sum(1 for l in o if is_line(l)))

kappa = F(1, 4)
delta = F(1, 100)
eps = F(1, 10**6)
e1 = exp_iv(1)
r = F(36787, 10**7) - eps            # e*(r + eps) <= delta at eA and eB
assert e1[1] * (r + eps) <= delta
R = {'p0': eps, 'pA': r, 'pB': r}     # constant objects: real, gauge invariant, functions of U|_Y, #Y = 4, loop
# the norm at every link
norm = {}
for k, o in objs.items():
    for l in o:
        norm[l] = norm.get(l, (F(0), F(0)))
        w = exp_iv(kappa * len(o))
        norm[l] = (norm[l][0] + w[0] * R[k], norm[l][1] + w[1] * R[k])
print('max norm over links <=', fmt(max(v[1] for v in norm.values())), ' delta =', delta)
assert max(v[1] for v in norm.values()) <= delta
dp = dprime(delta)
print("2 delta' in [", fmt(2*dp[0]), ",", fmt(2*dp[1]), "]  C_k (2 delta' <= kappa/2):", 2*dp[1] <= kappa/2)

def off(o):
    return {l for l in o if not is_line(l)}

def connected(names):
    names = list(names)
    seen = {names[0]}; stack = [names[0]]
    while stack:
        a = stack.pop()
        for b in names:
            if b not in seen and off(objs[a]) & off(objs[b]):
                seen.add(b); stack.append(b)
    return len(seen) == len(names)

polys = [c for n in (1, 2, 3) for c in combinations(objs, n) if connected(c)]
G = ('p0',)
inc = [P for P in polys if any(off(objs[a]) & off(objs['p0']) for a in P)]
print('polymers incompatible with {p0}:', inc)

def omega(name, kind):
    x = R[name]
    if kind == 'A':     # e^R - 1 with R constant: exact majorant
        v = exp_iv(x); return v[0] - 1, v[1] - 1
    v = exp_iv(x); return rdn(x * v[0]), rup(x * v[1])   # route B's rho-bar = r e^r

def lhs(weight_d, kind):
    lo = F(0); hi = F(0)
    for P in inc:
        plo, phi = F(1), F(1)
        for a in P:
            o = objs[a]
            w = omega(a, kind)
            ex = exp_iv(dp[0] * len(off(o)) + weight_d(o))[0], exp_iv(dp[1] * len(off(o)) + weight_d(o))[1]
            plo *= w[0] * ex[0]; phi *= w[1] * ex[1]
        lo += plo; hi += phi
    return lo, hi

a_G = (2 * dp[0], 2 * dp[1])   # a({p0}) = delta' #off(p0)
lit = lhs(lambda o: kappa * len(o), 'A')
print("literal d = kappa*#fine links: LHS in [", fmt(lit[0]), ",", fmt(lit[1]), "]  a({p0}) in [", fmt(a_G[0]), ",", fmt(a_G[1]), "]  KP fails:", lit[0] > a_G[1])
single = (lambda w, x: (w[0] * x[0], w[1] * x[1]))(omega('pA', 'A'), exp_iv(4 * dp[0] + 1))
print("   the two single terms {pA},{pB} alone give >=", fmt(2 * single[0]), "> a({p0})")
rB = lhs(lambda o: kappa * len(o) / 2, 'B')
print("route B d = (kappa/2)*#fine links: LHS <=", fmt(rB[1]), " KP holds:", rB[1] <= a_G[0])
rA = lhs(lambda o: kappa * sum(1 for l in o if is_line(l)) / 2, 'A')
aA = (dp[0] * 2, dp[1] * 2)
print("route A d = (kappa/2)*#line links: LHS <=", fmt(rA[1]), " KP holds:", rA[1] <= aA[0])
# the other literal reading, #G = number of objects: KP may close, but the weight bound fails
print("reading #G = #objects: C10c's object (8 line links, 2 off) has #Y'' = 4 and d = kappa*1, so e^{kappa #Y''} = e^{4 kappa} > e^{d} = e^{kappa}")
