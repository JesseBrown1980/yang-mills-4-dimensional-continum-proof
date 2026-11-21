# Scratch reads (not an engine, not evidence): delta_1 brackets at the final edge points, and the C19
# delta_crit_surrogate edge (delta_1 <= 49/1000) for the factors 12 and 6. Reuses the functions of
# G1-repair-checks.py by exec of its source up to its section 1 and its section 7 helpers.
from fractions import Fraction as Q
src = open('G1-repair-checks.py').read()
head = src.split('# ---------- 1. the two scalar edges')[0]
ns = {}
exec(head, ns)
i = src.index('F = lambda n: comb(20 * n, n)')
j = src.index('DCF = (')
exec(src[i:j], ns)
up, down, ex, fmt, S_and_dS, eps6, read, find_edge = (ns[k] for k in ('up', 'down', 'ex', 'fmt', 'S_and_dS', 'eps6', 'read', 'find_edge'))
lines = []
def P(s):
    lines.append(s); print(s, flush=True)


def alpha_bracket(beta, h, iters=3000):
    el, eh = eps6(beta)
    th = Q(1, 4)
    a = Q(0)
    for _ in range(iters):
        x = down(el * ex(2 * a + th)[0])
        r = S_and_dS(x, h)
        if r is None or r[0] > Q(1, 4):
            return None
        a_new = down(r[0])
        if a_new <= a:
            break
        a = a_new
    a_up = up(a * (1 + Q(1, 10 ** 10)))
    r = S_and_dS(up(eh * ex(2 * a_up + th)[1]), h)
    ok = r is not None and up(r[0]) <= a_up
    return a, a_up, ok


for beta, h in [(Q(1595, 10 ** 5), 'crude'), (Q(1596, 10 ** 5), 'crude'), (Q(2040, 10 ** 5), 'C03'), (Q(2041, 10 ** 5), 'C03'),
                (Q(2040, 10 ** 5), 'headfree'), (Q(2041, 10 ** 5), 'headfree'), (Q(1767, 10 ** 5), 'crude'), (Q(1768, 10 ** 5), 'crude'),
                (Q(2074, 10 ** 5), 'C03'), (Q(2075, 10 ** 5), 'C03')]:
    r = alpha_bracket(beta, h)
    if r is None:
        P('E beta=%s %s: lower iterate leaves the domain' % (fmt(beta, 6), h))
        continue
    a, au, ok = r
    P('E beta=%s %s: alpha_- in [%s, %s] (upper certified %s); 12alpha in [%s, %s]; 6alpha in [%s, %s]' % (
        fmt(beta, 6), h, fmt(a, 10), fmt(au, 10), ok, fmt(12 * a, 9), fmt(12 * au, 9), fmt(6 * a, 9), fmt(6 * au, 9)))

T = Q(49, 1000)
for fac, st in [(12, 1365), (6, 1552)]:
    i_, a_, b_ = find_edge('crude', fac, T, T, st)
    P('S surrogate delta_1 <= 49/1000, factor %d, crude: MET at %s (certified %s), NOT_MET at %s (certified %s)' % (
        fac, fmt(Q(i_, 10 ** 5), 6), a_[0], fmt(Q(i_ + 1, 10 ** 5), 6), b_[1]))
open(__file__.replace('.py', '.out'), 'w').write('\n'.join(lines) + '\n')
