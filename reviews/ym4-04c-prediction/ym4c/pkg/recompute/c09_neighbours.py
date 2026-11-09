# Scratch read (not an engine, not evidence): relative gaps of T between the minimizing theta index and its
# neighbours at the C09 couplings, against the engine's dyadic alpha resolution 2^-48. Reuses the definitions of
# final_s_lane.py by exec of its source up to its section list. Fractions only; floats only in display.
from fractions import Fraction as Q
src = open('final_s_lane.py').read().split("SECTIONS = sys.argv")[0]
ns = {'__file__': 'final_s_lane.py'}
exec(src, ns)
alpha_root, ex, fmt, K = ns['alpha_root'], ns['ex'], ns['fmt'], ns['K']
lines = []
for beta, i0 in [(Q(1, 4000), 194), (Q(1, 2000), 150), (Q(1, 1000), 105), (Q(1, 700), 83), (Q(1, 600), 73), (Q(1, 4000), 128)]:
    T = {}
    for i in (i0 - 1, i0, i0 + 1):
        th = K + Q(i, 64)
        a_lo, a_up, ok = alpha_root(beta, 'C03', theta=th)
        T[i] = (a_lo * ex(-8 * th)[0], a_up * ex(-8 * th)[1], a_lo)
    gap = min(T[i][0] for i in T if i != i0) / T[i0][1] - 1
    dy = Q(1, 2 ** 48) / T[i0][2]
    s = 'beta=%s i*=%d: alpha_-(i*)=%s; min relative gap to a neighbour %s; 2^-48/alpha_- = %s' % (beta, i0, fmt(T[i0][2], 6), fmt(gap, 4), fmt(dy, 3))
    lines.append(s); print(s, flush=True)
open('c09_neighbours.out', 'w').write('\n'.join(lines) + '\n')
