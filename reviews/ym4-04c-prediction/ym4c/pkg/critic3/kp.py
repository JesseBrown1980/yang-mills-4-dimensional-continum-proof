import sys
sys.path.insert(0, ".")
from spot import *
TH = Fr(1, 4)
DCm, DCp = Fr(114846768, 10**9), Fr(114846769, 10**9)
def d1(beta, head):
    eps = eps6_iv(beta); r = root_bracket(eps, TH, coef(HEADS[head]))
    return None if r is None else (6*r[0], 6*r[1])
part = sys.argv[1]
if part == "chains":
    for name, beta, head, lo, hi in [("C07", Fr(1,100), "crude", "0.0055222", "0.0055223"),
                                     ("C08", Fr(1,100), "C03", "4.7159e-6", "4.7160e-6"),
                                     ("C08hf", Fr(1,100), "headfree", "4.6861e-6", "4.6862e-6"),
                                     ("C11", Fr(1,64), "crude", "0.0508265", "0.0508266"),
                                     ("C14@1/64", Fr(1,64), "C03", "1.01738e-3", "1.01739e-3"),
                                     ("C12", Fr(1,50), "C03", "0.0363235", "0.0363236"),
                                     ("C12hf", Fr(1,50), "headfree", "0.0363229", "0.0363230")]:
        d = d1(beta, head)
        show(f"{name} delta_1", d, Fr(lo), Fr(hi))
        l = (lam_iv(d[0])[0], lam_iv(d[1])[1])
        print(f"      lambda in [{float(l[0]):.10g}, {float(l[1]):.10g}]")
        e1 = exp_iv(-1)
        print(f"      delta_2 <= {float(U(e1[1]*d[1])):.8g}; sum <= {float(U(d[1]/(1-e1[1]))):.8g}")
    eps = eps6_iv(Fr(1,50)); print("C12 crude C_0 NOT_MET proof at 1/50:", not_met_c0(eps, TH, coef(HEADS["crude"])))
elif part == "edges":
    for name, b_met, b_not, head in [("C13 crude", Fr(1767,10**5), Fr(1768,10**5), "crude"),
                                     ("C14 C03", Fr(2074,10**5), Fr(2075,10**5), "C03"),
                                     ("C14 headfree", Fr(2074,10**5), Fr(2075,10**5), "headfree")]:
        c = coef(HEADS[head])
        e = eps6_iv(b_met); okm = met(e, DCm/6, TH, c)
        e2 = eps6_iv(b_not); gl, gph = g_lo_gp_hi(e2, DCp/6, TH, c)
        okn = gl is not None and gl > 0 and gph < 0
        print(f"{name}: MET at {float(b_met)} (S+ <= delta_crit^-/6): {okm}; NOT_MET at {float(b_not)} (g^->0, g'^+<0 at delta_crit^+/6): {okn}")
        print(f"     delta_1 at {float(b_met)}: {[float(v) for v in d1(b_met, head)]}; at {float(b_not)}: {[float(v) for v in d1(b_not, head)]}")
    for name, bm, bn, head in [("C05 crude C_0", Fr(1904,10**5), Fr(1905,10**5), "crude"),
                               ("C06 C03 C_0", Fr(2075,10**5), Fr(2076,10**5), "C03"),
                               ("C06 headfree C_0", Fr(2075,10**5), Fr(2076,10**5), "headfree")]:
        c = coef(HEADS[head])
        r = root_bracket(eps6_iv(bm), TH, c)
        nm = not_met_c0(eps6_iv(bn), TH, c)
        print(f"{name}: MET at {float(bm)}: {r is not None}; NOT_MET proof at {float(bn)}: {nm}")
elif part == "surrogate":
    c = coef(HEADS["crude"])
    for j in (1552, 1553, 1761, 1762, 1767):
        b = Fr(j, 10**5); d = d1(b, "crude"); print(j, [float(v) for v in d], "<=0.049:", d[1] <= Fr(49,1000), ">0.049:", d[0] > Fr(49,1000))
