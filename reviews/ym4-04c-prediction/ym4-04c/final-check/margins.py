from s_lane import *
def g(a,e,b,head):
    s,_=S_and_dS(e*(2*a+b).exp(),head)
    return None if s is None else s-a
def gmin(e,b,head):
    lo,hi=D(0),D(1)/4
    for _ in range(300):
        m1=lo+(hi-lo)/3; m2=hi-(hi-lo)/3
        g1=g(m1,e,b,head); g2=g(m2,e,b,head)
        if g1 is None: hi=m1; continue
        if g2 is None or g1<=g2: hi=m2
        else: lo=m1
    am=(lo+hi)/2; return am,g(am,e,b,head)
def width(e,b,head,am,gm):
    # least and greatest roots around am
    def root(lo,hi,inc):
        for _ in range(250):
            m=(lo+hi)/2
            v=g(m,e,b,head)
            neg = v is not None and v<=0
            if inc: 
                if neg: hi=m
                else: lo=m
            else:
                if neg: lo=m
                else: hi=m
        return (lo+hi)/2
    a1=root(D(0),am,True); a2=root(am,D(1)/4 if g(D(1)/4,e,b,head) is not None and g(D(1)/4,e,b,head)>0 else am*2,False)
    return a1,a2
for name,j in (('crude',1904),('crude',1905),('free',2075),('free',2076),('meas',2075),('meas',2076)):
    e=eps6(Fr(j,100000)); am,gm=gmin(e,KAP,HEADS[name])
    out='%s %d a_min=%.10f g_min=%.4e'%(name,j,am,gm)
    if gm<=0:
        a1,a2=width(e,KAP,HEADS[name],am,gm); out+=' interval=[%.12f,%.12f] width=%.3e (2^-30=%.3e)'%(a1,a2,a2-a1,D(2)**-30)
    print(out)
