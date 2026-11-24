"""Original 4D SU2 boundary staple sufficient statistic, exact Q8 fixtures."""
from itertools import product
ONE=(1,0,0,0)
I=(0,1,0,0)
J=(0,0,1,0)
K=(0,0,0,1)
Q8=(ONE,I,J,K,(-1,0,0,0),(0,-1,0,0),(0,0,-1,0),(0,0,0,-1))

def require(ok,label):
    if not ok:
        raise ValueError(label)

def mul(u,v):
    a,b,c,d=u
    e,f,g,h=v
    return (a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e)

def inv(u):
    return (u[0],-u[1],-u[2],-u[3])

def dot(u,v):
    return sum(u[j]*v[j] for j in range(4))

def plus(x,mu,L):
    y=list(x)
    y[mu]=(y[mu]+1)%L
    return tuple(y)

def links(h,L):
    for x in product(range(-h,h+1),repeat=4):
        for mu in range(4):
            if x[mu]<h:
                yield tuple(z%L for z in x),mu

def all_plaquettes(L):
    for x in product(range(L),repeat=4):
        for mu in range(4):
            for nu in range(mu+1,4):
                yield (x,mu,nu)

def corners(x,mu,nu,L):
    return ((x,mu),(plus(x,mu,L),nu),(plus(x,nu,L),mu),(x,nu))

def plaquette(U,p,target=None):
    x,mu,nu=p
    edges=corners(x,mu,nu,LIMIT)
    vals=[ONE if e==target else U[e] for e in edges]
    return mul(mul(mul(vals[0],vals[1]),inv(vals[2])),inv(vals[3]))

def staple(U,p,e):
    faces=corners(p[0],p[1],p[2],LIMIT)
    index=faces.index(e)
    values=[U[faces[0]],U[faces[1]],inv(U[faces[2]]),inv(U[faces[3]])]
    rest=ONE
    # Original SU2 halftrace is cyclic: factors AFTER the selected
    # internal factor multiply BEFORE those preceding it.  Merely
    # replacing it by identity fails for noncommuting SU2 staples.
    for offset in (1,2,3):
        rest=mul(rest,values[(index+offset)%4])
    return inv(rest) if index<2 else rest

def sum_boundary(U,internal,plist):
    total=0
    for p in plist:
        e=corners(p[0],p[1],p[2],LIMIT)
        if sum(link in internal for link in e)==1:
            total+=plaquette(U,p)[0]
    return total

def fixture(h):
    global LIMIT
    b=2*h+1
    LIMIT=2*b
    interior=set(links(h,LIMIT))
    cube_sites=set(tuple(z%LIMIT for z in x)
                   for x in product(range(-h,h+1),repeat=4))
    U={(x,mu):Q8[(x[0]+2*x[1]+3*x[2]+5*x[3]+7*mu)%8]
       for x in product(range(LIMIT),repeat=4) for mu in range(4)}
    plist=list(all_plaquettes(LIMIT))
    B={}
    count={}
    total=0
    mixed=0
    for p in plist:
        parts=corners(p[0],p[1],p[2],LIMIT)
        interior_edges=[e for e in parts if e in interior]
        if not interior_edges:
            continue
        if len(interior_edges)==4:
            continue
        require(len(interior_edges)==1,"one_internal_link_per_mixed_plaquette")
        e=interior_edges[0]
        s=staple(U,p,e)
        require(dot(U[e],s)==plaquette(U,p)[0],
                "actual_SU2_mixed_Wilson_plaquette_staple_equality")
        old=B.get(e,(0,0,0,0))
        B[e]=tuple(old[j]+s[j] for j in range(4))
        count[e]=count.get(e,0)+1
        total+=dot(U[e],s)
        mixed+=1
    require(mixed==24*b*b*(b-1),"total_boundary_original_plaquette_staples")
    expected=4*(b-1)*(b*b*b-(b-2)*(b-2)*(b-2))
    require(len(B)==expected,"number_of_boundary_tangent_original_links")
    require(max(count.values())<=3 and min(count.values())>=1,
            "each_original_boundary_link_has_one_two_or_three_staples")
    require(sum(count.values())==mixed,"exact_full_boundary_staple_multiplicity")
    require(total==sum_boundary(U,interior,plist),
            "exact_boundary_action_sum_factorization")
    modified=dict(U)
    for e in interior:
        x,mu=e
        modified[e]=Q8[(x[0]+5*x[1]+7*x[2]+3*x[3]+4*mu+1)%8]
    require(sum(dot(modified[e],v) for e,v in B.items())
            ==sum_boundary(modified,interior,plist),
            "boundary_statistic_independent_of_arbitrary_internal_configuration")
    gauge={x:(ONE if x in cube_sites else Q8[(x[0]+3*x[1]+5*x[2]+7*x[3])%8])
           for x in product(range(LIMIT),repeat=4)}
    transformed={(x,mu):mul(mul(gauge[x],q),inv(gauge[plus(x,mu,LIMIT)]))
                 for (x,mu),q in U.items()}
    require(all(U[e]==transformed[e] for e in interior),
            "external_site_gauge_fixes_internal_links")
    for p in plist:
        parts=corners(p[0],p[1],p[2],LIMIT)
        e=[q for q in parts if q in interior]
        if len(e)==1:
            require(staple(U,p,e[0])==staple(transformed,p,e[0]),
                    "individual_original_boundary_staple_gauge_neutral")
    require(mul(I,J)==K and mul(J,I)==inv(K),"genuine_SU2_noncommuting")

def main():
    for h in (1,2):
        fixture(h)
    return (
        'YM4_VOL15_STAPLE|original_continuous_SU2_boundary_action=ANALYTIC|exact_Q8_L6_L10=PASS|json=0\n'
        'YM4_VOL15_STAT_COUNT|mixed_original_plaquettes=24b2_bminus1|affected_original_links=4_bminus1_times_b3_minus_bminus2cubed|json=0\n'
        'YM4_VOL15_STAT_FORM|boundary_action=sum_internal_link_dot_SU2_boundary_resultant|each_link_staples_le3|json=0\n'
        'YM4_VOL15_STAT_TEST|interior_configuration_changed=PASS|same_boundary_resultants=PASS|json=0\n'
        'YM4_VOL15_STAT_GAUGE|exterior_site_gauge_identity_on_cube_sites|each_staple_unchanged=PASS|json=0\n'
        'YM4_VOL15_STAT_TARGET|interpolated_boundary_resultant_covariance_decay=OPEN|all_Gauss_sector_mass_gap=OPEN|11_continuum_gates=OPEN|json=0\n'
    )

if __name__=='__main__':
    print(main(),end='')
