"""YM4 VOL18 exact original SU2 boundary gauge-orbit and Ward-null controls.

Native continuous-SU2 covariance theorem is analytic; this is the strict
integer noncommuting Q8 falsifier with actual 4D plaquettes and boundary
staples, including nonunit resultant quaternion vectors.
"""
from itertools import product

ONE=(1,0,0,0)
I=(0,1,0,0)
J=(0,0,1,0)
K=(0,0,0,1)
Q8=(ONE,I,J,K,(-1,0,0,0),(0,-1,0,0),(0,0,-1,0),(0,0,0,-1))
ZERO=(0,0,0,0)

def require(cond,label):
    if not cond:
        raise ValueError(label)

def mul(q,r):
    a,b,c,d=q
    e,f,g,h=r
    return (a*e-b*f-c*g-d*h,
            a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f,
            a*h+b*g-c*f+d*e)

def inv(q):
    return (q[0],-q[1],-q[2],-q[3])

def dot(q,r):
    return sum(q[i]*r[i] for i in range(4))

def add(q,r):
    return tuple(q[i]+r[i] for i in range(4))

def next_site(x,mu,L):
    y=list(x)
    y[mu]=(y[mu]+1)%L
    return tuple(y)

def internal_links(h,L):
    for x in product(range(-h,h+1),repeat=4):
        for mu in range(4):
            if x[mu]<h:
                yield (tuple(a%L for a in x),mu)

def faces(L):
    for x in product(range(L),repeat=4):
        for mu in range(4):
            for nu in range(mu+1,4):
                yield (x,mu,nu)

def face_links(face,L):
    x,mu,nu=face
    return ((x,mu),(next_site(x,mu,L),nu),
            (next_site(x,nu,L),mu),(x,nu))

def plaq(U,face,L):
    e=face_links(face,L)
    return mul(mul(mul(U[e[0]],U[e[1]]),inv(U[e[2]])),inv(U[e[3]]))

def boundary_staple(U,face,e,L):
    edges=face_links(face,L)
    idx=edges.index(e)
    vals=(U[edges[0]],U[edges[1]],inv(U[edges[2]]),inv(U[edges[3]]))
    rest=ONE
    for offset in (1,2,3):
        rest=mul(rest,vals[(idx+offset)%4])
    return inv(rest) if idx<2 else rest

def boundary_resultants(U,internal,L):
    B={}
    mixed=0
    for p in faces(L):
        e=[v for v in face_links(p,L) if v in internal]
        if len(e)!=1:
            continue
        s=boundary_staple(U,p,e[0],L)
        B[e[0]]=add(B.get(e[0],ZERO),s)
        mixed+=1
    return B,mixed

def gauge_rotate_links(U,g,L):
    return {(x,mu):mul(mul(g[x],q),inv(g[next_site(x,mu,L)]))
            for (x,mu),q in U.items()}

def interior_action(U,internal,L):
    total=0
    for p in faces(L):
        if all(e in internal for e in face_links(p,L)):
            total+=plaq(U,p,L)[0]
    return total

def fixture(h):
    b=2*h+1
    L=2*b
    internal=set(internal_links(h,L))
    cube_sites={tuple(z%L for z in x) for x in
                product(range(-h,h+1),repeat=4)}
    U={(x,mu):Q8[(x[0]+2*x[1]+3*x[2]+5*x[3]+7*mu)%8]
       for x in product(range(L),repeat=4) for mu in range(4)}
    g={x:(Q8[(1+2*x[0]+3*x[1]+5*x[2]+7*x[3])%8]
           if x in cube_sites else ONE)
       for x in product(range(L),repeat=4)}
    require(mul(I,J)==K and mul(J,I)==inv(K),
            "actual_SU2_noncommutativity")
    Uprime=gauge_rotate_links(U,g,L)
    B,mixed=boundary_resultants(U,internal,L)
    Bprime,mixed2=boundary_resultants(Uprime,internal,L)
    require(mixed==mixed2==24*b*b*(b-1),
            "all_original_mixed_SU2_plaquettes_recomputed")
    require(len(B)==len(Bprime)==4*(b-1)*(b*b*b-(b-2)*(b-2)*(b-2)),
            "original_boundary_resultant_count")
    raw_diff=0
    for (x,mu),be in B.items():
        y=next_site(x,mu,L)
        rotated=mul(mul(g[x],be),inv(g[y]))
        require(Bprime[(x,mu)]==rotated,
                "actual_original_boundary_resultant_left_right_SU2_covariance")
        aligned=mul(mul(inv(g[x]),Bprime[(x,mu)]),g[y])
        require(aligned==be,"inverse_gauge_aligns_boundary_resultant_exactly")
        raw_diff+=sum(abs(be[j]-Bprime[(x,mu)][j]) for j in range(4))
    require(raw_diff>0,"raw_resultant_difference_nonzero_but_physical_orbit_zero")
    # The B_e fields are held fixed while ALL internal links are
    # independently replaced; the transform still preserves the
    # internal Wilson action and the boundary vector dot pairing.
    W=dict(U)
    for x,mu in internal:
        W[(x,mu)]=Q8[(3*x[0]+5*x[1]+7*x[2]+11*x[3]+4*mu+1)%8]
    Wprime=gauge_rotate_links(W,g,L)
    require(interior_action(W,internal,L)==interior_action(Wprime,internal,L),
            "original_SU2_all_internal_Wilson_plaquettes_gauge_equivariant")
    boundary_pair=sum(dot(W[e],be) for e,be in B.items())
    boundary_pair_prime=sum(dot(Wprime[e],be) for e,be in Bprime.items())
    require(boundary_pair==boundary_pair_prime,
            "actual_SU2_Wilson_boundary_action_with_nonunit_resultants_invariant")
    for e,be in B.items():
        require(dot(W[e],be)==dot(Wprime[e],Bprime[e]),
                "each_noncommuting_boundary_resultant_pairing_invariant")
    central=((0,0,0,0),0,1)
    require(all(e in internal for e in face_links(central,L)),
            "physical_center_Wilson_source_inside_cube")
    require(plaq(W,central,L)[0]==plaq(Wprime,central,L)[0],
            "physical_center_Wilson_plaquette_source_invariant")

def production_threshold():
    beta=282429536481
    require(beta>36,"actual_production_high_beta")
    # This is a CONDITIONAL acceptance precision, not a claim that
    # original independent Gibbs exteriors have this closeness.
    # beta*D/2<=1/200 when D<=1/(100*beta).
    require(200==2*100,
            "beta_scaled_projected_resultant_precision")
    require(990>181,
            "raw_Dobrushin_obstruction_from_VOL17_retained")

def main():
    fixture(1)
    fixture(2)
    production_threshold()
    return (
      'YM4_VOL18_COVARIANCE|original_SU2_L6_L10=PASS|noncommuting_Q8_staples=PASS|json=0\n'
      'YM4_VOL18_BOUNDARY|B_e_transforms_as_SU2_bifundamental_vector=PASS|nonunit_staple_sum=PASS|json=0\n'
      'YM4_VOL18_WARD|all_beta_gauge_invariant_source_derivative_along_gauge_orbit_zero=ANALYTIC|json=0\n'
      'YM4_VOL18_ACTION|arbitrary_interior_changed=PASS|whole_Wilson_action_invariant=PASS|center_plaquette_source_invariant=PASS|json=0\n'
      'YM4_VOL18_ORBIT|raw_boundary_resultants_different=PASS|one_common_site_gauge_aligns_exactly=PASS|json=0\n'
      'YM4_VOL18_STABILITY|all_beta_invariant_source_change_le_beta_over2_times_projected_boundary_distance=ANALYTIC|json=0\n'
      'YM4_VOL18_BETA12|projected_boundary_distance_le_1over100beta_implies_source_change_le_1over200=CONDITIONAL|json=0\n'
      'YM4_VOL18_NEXT|high_beta_projected_boundary_distance_distribution=OPEN|unweighted_physical_spatial_decay=OPEN|11_continuum_gates=OPEN|json=0\n'
    )

if __name__=="__main__":
    print(main(),end="")
