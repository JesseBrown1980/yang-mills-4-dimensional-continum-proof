#!/usr/bin/env python3
"""Integer arithmetic, quaternion jets and coarse-lift geometry for D3D."""
from itertools import product, combinations


def require(ok, name):
    if not ok:
        raise ValueError(name)


def add(*vs):
    return tuple(sum(xs) for xs in zip(*vs))


def scale(v, n):
    return tuple(n*x for x in v)


def mul(a,b):
    w,x,y,z=a
    t,i,j,k=b
    return (w*t-x*i-y*j-z*k,w*i+x*t+y*k-z*j,
            w*j-x*k+y*t+z*i,w*k+x*j-y*i+z*t)


def conj(a):
    return (a[0],-a[1],-a[2],-a[3])


def det(a):
    x,y,z=a
    return (x[0]*(y[1]*z[2]-y[2]*z[1])
            -x[1]*(y[0]*z[2]-y[2]*z[0])
            +x[2]*(y[0]*z[1]-y[1]*z[0]))


def solve_num(a,b):
    return tuple(det(tuple(tuple(b[i] if j==k else a[i][j]
                    for j in range(3)) for i in range(3))) for k in range(3))


def mv(a,b):
    return tuple(sum(x*y for x,y in zip(row,b)) for row in a)


def emit(s):
    print("YM4_VOL14D3D|"+s+"|json=0")


def calibration():
    beta=9**7
    require(beta==4782969,"beta")
    require(6*1536*3**22<2**49 and 1536**4*27*3**84<2**181,"prefactors")
    for d,m in ((36,700),(58,1700)):
        require((12*d*d-1)*4*m>24*d**4,"strict_angle")
    require(beta//(64*700)==106 and beta//(16*700)==427,"exponents36")
    require(106-49==57 and 427-181==246 and 972<1024,"local36")
    emit("beta=4782969|delta=1/36|epsilon=1/700|rho_star_lt=2^-57|rho_D_lt=2^-246|local_defect_lt=2^-236")
    require(65*10>27*24,"e_lower_series")
    require(beta//(64*1700)==43 and beta//(16*1700)==175,"exponents58")
    require(2**49*18**3*10**43<27**43,"star58")
    require(2**(181+69)*10**175<27**175,"plaquette58")
    emit("beta=4782969|delta=1/58|epsilon=1/1700|rho_star_lt=18^-3|rho_D_lt=2^-69|local_defect_lt=2^-59")
    require(7*45-8*8==251,"sigma30")
    emit("delta=1/30|M_min_sv_ge=251/360|M_inverse_le=360/251")
    require(2*12*12-25==263,"floor36")
    require(3*263-4*32==661,"sigma36")
    require(54*36+180==59*36,"face36")
    require(789*59*7932==15517*661*36,"lambda36")
    require(4*864*180<661*1000,"nearby_feasible_angle")
    emit("delta=1/36|V_floor=263/288|M_min_sv_ge=661/864|LR_inverse_le=789/661|multiplier_norm_le=15517/7932")


def fixture():
    s=(9999,200,0,0)
    require(mul(s,conj(s))==(10001**2,0,0,0),"unit_suffix")
    # Two synthetic quaternion path jets, with common denominator 2*10001^2.
    data=((s,(0,1,2,-1),(0,0,1,2)),
          (conj(s),(0,-2,1,1),(0,1,-1,0)))
    cols=[[],[],[]]
    for j in range(4):
        e=tuple(int(i==j) for i in range(4))
        jets=[]
        for q,a,b in data:
            v=mul(mul(conj(q),e),q)
            jets.append((v,add(mul(a,v),mul(v,b)),
                         add(mul(mul(a,a),v),scale(mul(mul(a,v),b),2),
                             mul(v,mul(b,b)))))
        for k in range(3):
            cols[k].append(add(jets[0][k],jets[1][k]))
    aa=[tuple(tuple(c[j][i] for j in range(1,4)) for i in range(1,4))
        for c in cols]
    bb=[c[0][1:] for c in cols]
    a=aa[0]
    require(bb[0]==(0,0,0),"base_constraint")
    require(a==((200040002,0,0),(0,199880002,0),(0,0,199880002)),"fixture_matrix")
    # Exact projective finite inversion for a noncentral target direction.
    target=(1,2,3,4)
    pre=(199880002,2*199880002,3*200040002,4*200040002)
    require(tuple(sum(cols[0][j][i]*pre[j] for j in range(4)) for i in range(4))
            ==scale(target,200040002*199880002),"finite_projective_inverse")
    d=det(a)
    require(d>0,"invertible")
    p=solve_num(a,scale(bb[1],-1))
    mixed=mv(aa[1],p)
    p2=solve_num(a,add(scale(bb[2],-d),scale(mixed,-2)))
    require(add(mv(a,p),scale(bb[1],d))==(0,0,0),"first_jet")
    require(add(mv(a,p2),scale(bb[2],d*d),scale(mixed,2*d))==(0,0,0),"second_jet")
    require(add(mv(a,p2),scale(bb[2],d*d))!=(0,0,0),"mixed_omission")
    z=(0,1,2,3)
    c=(0,)+p
    c2=(0,)+p2
    x=add(scale(z,d),c)
    bracket=scale(add(mul(z,c),scale(mul(c,z),-1)),d)
    lhs=add(scale(mul(z,z),d*d),scale(mul(z,c),2*d),c2,mul(c,c))
    require(lhs==add(mul(x,x),c2,bracket),"BCH_second_jet")
    require(lhs!=add(mul(x,x),c2),"commutator_omission")
    emit("noncommuting_fixture|constraint_first_jet=PASS|constraint_second_jet=PASS|BCH_second_jet=PASS|mixed_term_omission=REJECTED|commutator_omission=REJECTED")


def coarse_lift():
    counts=[]
    for m,n in combinations(range(4),2):
        counts.append(sum(x[m]==1 and x[n]==1
                          for x in product((-1,0,1),repeat=4)))
    require(counts==[9]*6 and sum(counts)==54,"coarse_plaquette_copies")
    emit("coarse_lift|plaquette_types=486|nontrivial=54|copies_per_coarse_plaquette=9")


def main():
    calibration()
    fixture()
    coarse_lift()
    emit("uniform_minimizer_angle_transfer=OPEN|augmented_relative_floor=OPEN")


if __name__=="__main__":
    main()
