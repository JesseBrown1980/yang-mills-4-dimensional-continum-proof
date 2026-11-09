# Lane L2-sec3-part2: the constant Proposition 3.28 takes from note Lemma 3.2 item 5 (integers only).
from qint import q, add, sub, mul, lt, le, dec
lo5 = add(sub(q(1, 5), q(1, 375)), sub(q(1, 15625), q(1, 546875)))   # arctan(1/5) >= this (alternating series)
pi_lo = sub(mul(q(16), lo5), mul(q(4), q(1, 239)))                    # arctan(1/239) <= 1/239
def gmul(a, b):  # Gaussian integers as integer pairs (re, im)
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])
g = (1, 0)
for _ in range(4):
    g = gmul(g, (5, 1))
g = gmul(g, (239, -1))
print("MACHIN|(5+i)^4(239-i)=%d+%di|equals_114244(1+i):%d" % (g[0], g[1], int(g == (114244, 114244))))
print("PI_LO|16*lo(arctan1/5)-4/239=%d/%d|equals_1231847548/392109375:%d|>333/106:%d" % (pi_lo[0], pi_lo[1], int(pi_lo == q(1231847548, 392109375)), int(lt(q(333, 106), pi_lo))))
# 8/(3 pi) < 8/(3*333/106) = 848/999 < 8489/10000
print("E_CHI|848/999<8489/10000:%d|8/(3*pi_lo)=%s<=8489/10000:%d|tag=MEASURED" % (int(lt(q(848, 999), q(8489, 10000))), dec(q(8 * pi_lo[1], 3 * pi_lo[0]), 9, "ceil"), int(le(q(8 * pi_lo[1], 3 * pi_lo[0]), q(8489, 10000)))))
