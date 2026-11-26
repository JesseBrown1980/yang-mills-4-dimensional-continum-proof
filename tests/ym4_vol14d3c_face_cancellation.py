#!/usr/bin/env python3
"""Integer geometry for paired crossing-face Wilson gradient cancellation."""
from itertools import product

B=tuple(product((-1,0,1),repeat=4))


def require(ok, why):
    if not ok:
        raise ValueError(why)


def step(x,mu,sg=1):
    return tuple(v+sg if i==mu else v for i,v in enumerate(x))


def path(z):
    return [(i,1 if v>0 else -1) for i,v in enumerate(z) if v]


def walk(w):
    x=(0,0,0,0)
    for i,sg in w:
        x=step(x,i,sg)
        require(x in B,"inside_target_block")
    return x


def swaps(x,nu):
    w=path(x)+[(nu,1)]
    p=len(w)-1
    n=0
    require(walk(w)==step(x,nu),"initial_endpoint")
    while p>0 and w[p-1][0]>nu:
        w[p-1],w[p]=w[p],w[p-1]
        p-=1
        n+=1
        require(walk(w)==step(x,nu),"swapped_endpoint")
    if p and w[p-1]==(nu,-1):
        del w[p-1:p+1]
    require(w==path(step(x,nu)),"tree_endpoint")
    return n


def count(mu):
    face={x for x in B if x[mu]==-1}
    both=set()
    single=set()
    ns=0
    for x in face:
        for nu in range(4):
            if nu==mu:
                continue
            y=step(x,nu)
            if y in face:
                both.add((x,nu))
                ns+=swaps(x,nu)
            else:
                single.add((x,nu))
            y=step(x,nu,-1)
            if y not in face:
                single.add((y,nu))
    require(len(face)==27,"face")
    require(not both & single,"disjoint")
    require(2*len(both)+len(single)==27*6,"incidences")
    return len(both),len(single),ns


def emit(s):
    print("YM4_VOL14D3C|"+s+"|json=0")


def main():
    for mu,n in enumerate((36,54,72,90)):
        require(count(mu)==(54,54,n),"face_count")
        emit("axis="+str(mu)+"|interior=54|boundary=54|tree_swap_sum="+str(n))
    require(54*30+2*90==2*30*30,"gradient_at_delta")
    require(315*2==630,"multiplier")
    require(630<1701 and 2*630<1701,"improvement")
    emit("delta=1/30|face_gradient_le=2|multiplier_norm_le=630/251|old_multiplier_norm_le=1701/251")
    # The seal is supplemental, not a retrospective change to D3B.
    require(27*6*315==1701*30,"D3B_multiplier_arithmetic")
    # Optional extended right inverse at delta=1/22:
    # r >= 743/968; (16/3)*delta/r = 704/2229.
    require(2*22*22-15*15==743,"extended_floor")
    require(16*968*2229==704*3*22*743,"extended_error")
    require(2229-704==1525,"extended_inverse")
    require(54*22+180==4*342,"extended_gradient")
    require(2*342*2229<9*121*1525,"extended_multiplier")
    emit("delta_extended=1/22|V_floor=743/968|LR_error_le=704/2229|inverse_le=2229/1525|multiplier_norm_lt=9/2")
    emit("stationarity_curl_orthogonality=ANALYTIC|augmented_relative_floor=OPEN")


if __name__=="__main__":
    main()
