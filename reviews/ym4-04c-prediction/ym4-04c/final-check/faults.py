from s_lane import *
def S_cut(x,head,ncut,tail):
    s=D(0)
    for n in range(4,ncut+1):
        c=D(head[n]) if n in head else F6[n]; s+=c*x**n
    if tail:
        if MU*x>=1: return None
        s+=F6[ncut+1]*x**(ncut+1)/(1-MU*x)
    return s
def fp_iter(e,b,head,infl,steps=400):
    a=D(0)
    for _ in range(steps):
        x=e*(2*a+b).exp(); s,_=S_and_dS(x,head)
        if s is None or s>D(1)/4: return None
        if s<=a: return a
        a=s*infl
    return None
for j in (1900,1901,1902,1903,1904):
    e=eps6(Fr(j,100000))
    print('iter400 infl=1.0001', j, fp_iter(e,KAP,{},D('1.0001')) is not None, ' infl=1', fp_iter(e,KAP,{},D(1)) is not None)
# missing tail at 1/40: cut at 10 vs cut at 48, crude head
e=eps6(Fr(1,40))
for ncut in (10,48):
    a=D(0); ok=False
    # search a in grid
    best=None
    for k in range(1,2501):
        a=D(k)/10000
        s=S_cut(e*(2*a+KAP).exp(),{},ncut,False)
        if s is not None and s<=a: ok=True; best=a; break
    print('missing_tail 1/40 cut',ncut,'MET' if ok else 'NOT_MET', best)
print('---')
for hname in ('meas','free','crude'):
    for ncut in (10,48):
        ok=False; best=None
        for k in range(1,2501):
            a=D(k)/10000
            s=S_cut(e*(2*a+KAP).exp(),HEADS[hname],ncut,False)
            if s is not None and s<=a: ok=True; best=a; break
        print('missing_tail 1/40',hname,'cut',ncut,'MET' if ok else 'NOT_MET', best)
