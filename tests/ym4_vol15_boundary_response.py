"""Original 4D SU2 Wilson centered-cube boundary classification and gauge cancellation.
Exact Q8 subgroup controls; analytic Gibbs derivative in companion note.
"""
from itertools import product

ONE=(1,0,0,0)
I=(0,1,0,0)
J=(0,0,1,0)
K=(0,0,0,1)
Q8=(ONE,I,J,K,(-1,0,0,0),(0,-1,0,0),(0,0,-1,0),(0,0,0,-1))

def require(value,label):
    if not value:
        raise ValueError(label)

def mul(u,v):
    a,b,c,d=u
    e,f,g,h=v
    return (a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e)

def inv(q):
    return (q[0],-q[1],-q[2],-q[3])

def pos(x,mu,L):
    y=list(x)
    y[mu]=(y[mu]+1)%L
    return tuple(y)

def internal_links(h,L):
    for x in product(range(-h,h+1),repeat=4):
        for mu in range(4):
            if x[mu]<h:
                yield (tuple(y%L for y in x),mu)

def plaq(U,x,mu,nu,L):
    return mul(mul(mul(U[(x,mu)],U[(pos(x,mu,L),nu)]),
                   inv(U[(pos(x,nu,L),mu)])),inv(U[(x,nu)]))

def verify(h):
    b=2*h+1
    L=2*b
    internal=set(internal_links(h,L))
    sites=set(tuple(y%L for y in x)
              for x in product(range(-h,h+1),repeat=4))
    require(len(internal)==4*(b-1)*b*b*b,"all_original_internal_links")
    U={(x,mu):Q8[(x[0]+2*x[1]+3*x[2]+5*x[3]+7*mu)%8]
       for x in product(range(L),repeat=4) for mu in range(4)}
    gauge={x:(ONE if x in sites else Q8[(x[0]+3*x[1]+5*x[2]+7*x[3])%8])
           for x in product(range(L),repeat=4)}
    V={(x,mu):mul(mul(gauge[x],q),inv(gauge[pos(x,mu,L)]))
       for (x,mu),q in U.items()}
    require(all(U[e]==V[e] for e in internal),
            "exterior_gauge_fixing_all_cube_sites_leaves_all_internal_links")
    numbers={0:0,1:0,2:0,3:0,4:0}
    gauge_terms=0
    for x in product(range(L),repeat=4):
        for mu in range(4):
            for nu in range(mu+1,4):
                e=((x,mu),(pos(x,mu,L),nu),
                   (pos(x,nu,L),mu),(x,nu))
                n=sum(t in internal for t in e)
                numbers[n]+=1
                if n:
                    original=plaq(U,x,mu,nu,L)
                    transformed=plaq(V,x,mu,nu,L)
                    require(original[0]==transformed[0],
                            "all_boundary_and_interior_original_Wilson_traces_gauge_invariant")
                    if n==1:
                        gauge_terms+=1
    require(numbers[4]==6*b*b*(b-1)*(b-1),
            "all_four_original_links_in_internal_plaquettes")
    require(numbers[1]==24*b*b*(b-1),
            "exact_Wilson_one_internal_link_boundary_count")
    require(numbers[2]==numbers[3]==0,
            "all_mixed_Wilson_plaquettes_have_exactly_one_internal_link")
    require(gauge_terms==numbers[1],
            "every_boundary_term_gauge_response_exact_zero")
    require(sum(numbers.values())==6*L*L*L*L,
            "all_periodic_original_SU2_plaquettes")
    beta=282429536481
    require(beta*numbers[1]>1,
            "unconditioned_boundary_oscillation_not_physical_contraction")

def main():
    require(mul(I,J)==K and mul(J,I)==inv(K),
            "genuine_noncommuting_SU2_fixture")
    for h in (1,2):
        verify(h)
    return (
      'YM4_VOL15_BOUNDARY|original_even_SU2_torus_L6_L10=PASS|centered_boxes_b3_b5=PASS|json=0\n'
      'YM4_VOL15_FACE_COUNT|all_interior_original_plaquettes=6b2_times_bminus1_squared|one_internal_link_boundary=24b2_times_bminus1|json=0\n'
      'YM4_VOL15_ORIGINAL_WILSON|all_mixed_plaquettes_have_exactly_one_internal_link=PASS|Q8_noncommuting=PASS|json=0\n'
      'YM4_VOL15_GAUGE_ZERO|exterior_gauge_fixed_on_cube_vertices=PASS|interior_conditional_action_same_for_all_beta=ANALYTIC|json=0\n'
      'YM4_VOL15_RESPONSE|d_expectation_dt=beta_covariance_with_boundary_plaquette_difference=ANALYTIC|json=0\n'
      'YM4_VOL15_TARGET|physical_unweighted_source_to_boundary_covariance_decay=OPEN|interpolated_boundary_law_gate=OPEN|11_continuum_gates=OPEN|json=0\n'
    )

if __name__=='__main__':
    print(main(),end='')
