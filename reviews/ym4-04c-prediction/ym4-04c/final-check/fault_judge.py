from s_lane import *
def jv(e,b,head,steps=400,tol=D(10)**-40):
    a=D(0)
    for _ in range(steps):
        s,_=S_and_dS(e*(2*a+b).exp(),head)
        if s is None or s>D(1)/4: return None
        if s<=a*(1+tol): return a
        a=s
    return None
for j in (1899,1900,1901,1902,1903,1904):
    e=eps6(Fr(j,100000)); print(j, 'MET' if jv(e,KAP,{}) is not None else 'NOT_MET')
