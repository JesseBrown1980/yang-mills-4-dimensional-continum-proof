"""Design-lane derivation check (integers/Fractions): Hessians of the three beta^10 functionals on abelian coarse plane waves.

Coarse lattice (Z/L)^4, L = 4. Abelian field x_mu(x') = cos(p.x') delta_{mu,0} with p in {0, pi}^4 so cos = +-1 exactly.
For a loop C with flux phi_C (sum of oriented x's): -d^2/de^2 chi_1/2(exp(i e phi sigma_3/2)) = phi^2/2, chi_1 gives 2 phi^2.
beta'_q(p) = 4 H / sum_P phi_P^2, H = c_h sum_P phi_P^2/2 + c_1 sum_P 2 phi_P^2 + c_ch sum_chairs phi_ch^2/2.
Prints kappa(p) = sum_ch phi_ch^2 / sum_P phi_P^2 - 16, so beta'_q(p) - beta'_q(axis) = 2 c_ch kappa(p).
"""
from fractions import Fraction as F
import itertools

d, L = 4, 4
sites = list(itertools.product(range(L), repeat=d))


def add(x, mu, s=1):
    y = list(x)
    y[mu] = (y[mu] + s) % L
    return tuple(y)


def field(p, pol):
    A = {}
    for x in sites:
        ph = sum(p[i] * x[i] for i in range(d)) % 2  # p entries 0 or 1 (units of pi)
        for mu in range(d):
            A[(x, mu)] = (1 if ph == 0 else -1) if mu == pol else 0
    return A


def step(A, x, mu, sign):
    # flux contribution of moving from x along sign*e_mu; returns (new site, value)
    if sign > 0:
        return add(x, mu), A[(x, mu)]
    y = add(x, mu, -1)
    return y, -A[(y, mu)]


def loop_flux(A, x, moves):
    tot = 0
    for mu, s in moves:
        x, v = step(A, x, mu, s)
        tot += v
    return tot, x


def plaquettes_flux2(A):
    tot = 0
    for x in sites:
        for mu in range(d):
            for nu in range(mu + 1, d):
                f, end = loop_flux(A, x, [(mu, 1), (nu, 1), (mu, -1), (nu, -1)])
                assert end == x
                tot += f * f
    return tot


def chairs_flux2(A):
    tot = 0
    count = 0
    for x in sites:
        for mu in range(d):
            sides = [(nu, s) for nu in range(d) if nu != mu for s in (1, -1)]
            for (nu, s), (la, t) in itertools.combinations(sides, 2):
                if nu == la:
                    continue
                # x -> x+s nu -> x+s nu+mu -> x+mu -> x+mu+t la -> x+t la -> x
                f, end = loop_flux(A, x, [(nu, s), (mu, 1), (nu, -s), (la, t), (mu, -1), (la, -t)])
                assert end == x
                tot += f * f
                count += 1
    return tot, count


for p in [(0, 1, 0, 0), (0, 1, 1, 0), (0, 1, 1, 1), (1, 1, 0, 0), (1, 1, 1, 0), (1, 1, 1, 1)]:
    A = field(p, 0)
    sp = plaquettes_flux2(A)
    sc, n = chairs_flux2(A)
    if sp == 0:
        print("p=%s: no plaquette flux (pure gauge/longitudinal)" % (p,))
        continue
    kappa = F(sc, sp) - 16
    print("p=pi*%s pol=0: chairs/site=%d sum_P phi^2=%d sum_ch phi^2=%d kappa=%s" % (p, n // len(sites), sp, sc, kappa))
c_ch = F(3, 524288)
print("2 c_ch =", 2 * c_ch)
