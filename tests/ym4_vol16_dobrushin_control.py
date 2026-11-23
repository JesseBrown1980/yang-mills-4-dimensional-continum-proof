"""YM4 VOL16: exact original 4D SU2 link-graph Dobrushin controls.

All geometry and arithmetic integer-only. The general continuous-Haar
single-link TV derivative and Dobrushin comparison appear in the proof note.
"""
from collections import defaultdict, deque
from itertools import combinations, product

ONE=(1,0,0,0)
NEG=(-1,0,0,0)
I=(0,1,0,0)
J=(0,0,1,0)
K=(0,0,0,1)
Q8=(ONE,I,J,K,NEG,(0,-1,0,0),(0,0,-1,0),(0,0,0,-1))

def require(x,label):
    if not x:
        raise ValueError(label)

def qmul(u,v):
    a,b,c,d=u
    e,f,g,h=v
    return (a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e)

def qinv(q):
    return (q[0],-q[1],-q[2],-q[3])

def plus(x,d):
    y=list(x)
    y[d]+=1
    return tuple(y)

def link_set(h):
    for x in product(range(-h,h+1),repeat=4):
        for d in range(4):
            if x[d]<h:
                yield (x,d)

def plaquette_faces(h):
    for x in product(range(-h,h+1),repeat=4):
        for mu in range(4):
            for nu in range(mu+1,4):
                if x[mu]<h and x[nu]<h:
                    yield ((x,mu),(plus(x,mu),nu),
                           (plus(x,nu),mu),(x,nu))

def qstaple(U,face,index):
    q=[U[face[0]],U[face[1]],qinv(U[face[2]]),qinv(U[face[3]])]
    acc=ONE
    for j in (1,2,3):
        acc=qmul(acc,q[(index+j)%4])
    return qinv(acc) if index<2 else acc

def noncommuting_single_neighbor_fixture(face):
    U={e:Q8[(abs(e[0][0])+2*abs(e[0][1])+3*abs(e[0][2])
               +5*abs(e[0][3])+7*e[1])%8] for e in face}
    require(qmul(I,J)==K and qmul(J,I)==qinv(K),
            "quaternion_noncommuting")
    for eidx in range(4):
        for fidx in range(4):
            if fidx==eidx:
                continue
            old=qstaple(U,face,eidx)
            modified=dict(U)
            modified[face[fidx]]=qmul(NEG,U[face[fidx]])
            changed=qstaple(modified,face,eidx)
            d2=sum((old[j]-changed[j])**2 for j in range(4))
            require(d2==4,"one_neighbor_changes_one_original_staple_by_at_most_2")

def graph_fixture(h):
    b=2*h+1
    links=list(link_set(h))
    index=set(links)
    require(len(index)==4*(b-1)*b*b*b,
            "exact_internal_original_link_count")
    neighbors={e:set() for e in links}
    multiplicity=defaultdict(int)
    face_count=0
    faces=list(plaquette_faces(h))
    for face in faces:
        require(all(e in index for e in face),"original_interior_plaquette_complete")
        face_count+=1
        for e,f in combinations(face,2):
            neighbors[e].add(f)
            neighbors[f].add(e)
            multiplicity[tuple(sorted((e,f)))]+=1
    require(face_count==6*b*b*(b-1)*(b-1),
            "all_six_original_plane_face_count")
    require(max(multiplicity.values())==1,
            "distinct_original_links_share_at_most_one_original_plaquette")
    require(max(len(n) for n in neighbors.values())<=18,
            "original_4d_link_graph_degree_at_most18")
    require(any(len(n)==18 for n in neighbors.values()),
            "original_4d_interior_degree18_control")
    for e,near in neighbors.items():
        for f in near:
            require(sum(abs(e[0][k]-f[0][k]) for k in range(4))<=2,
                    "adjacent_original_links_base_move_at_most2")
    boundary={e for e in links if any(abs(e[0][nu])==h
                                      for nu in range(4) if nu!=e[1])}
    require(len(boundary)==4*(b-1)*(b*b*b-(b-2)*(b-2)*(b-2)),
            "exact_VOL15_boundary_resultant_link_count")
    distance={e:0 for e in boundary}
    queue=deque(boundary)
    while queue:
        e=queue.popleft()
        for f in neighbors[e]:
            if f not in distance:
                distance[f]=distance[e]+1
                queue.append(f)
    require(len(distance)==len(index),
            "whole_original_link_graph_reaches_boundary")
    sources=[e for e in links if e[0]==(0,0,0,0)]
    require(len(sources)==4,"four_center_source_links")
    for e in sources:
        d=distance[e]
        require(2*d>=h,"center_source_graph_buffer_at_least_h_over2")
        require(d>0,"center_source_separated_from_exterior_resultants")
    for face in faces[:6]:
        noncommuting_single_neighbor_fixture(face)
    return min(distance[e] for e in sources)

def acceptance():
    # Beta 1/36, original 4D degree 18, six-plaquette incidence.
    beta_num=1
    beta_den=36
    degree=18
    require(2*degree*beta_num==beta_den,
            "Dobrushin_row_sum_one_half")
    # B_e is sum of at most 3 original unit SU2 exterior staples;
    # beta/2*||Delta B_e||<=3 beta=1/12.
    require(12*3*beta_num==beta_den,"boundary_site_TV_one_twelfth")
    # direct source influence: bmax/(1-alpha)=1/6.
    require(6*3*beta_num*2==beta_den,
            "unweighted_source_response_prefactor_one_sixth")
    # Strong-coupling acceptance fails for production high beta:
    beta_production=282429536481
    require(degree*beta_production>1,
            "production_beta_fails_uniform_single_link_Dobrushin")
    # h=1,2,3 tests are original centered b=3,5,7 cubes.
    for h in (1,2,3):
        d=graph_fixture(h)
        require(2*d>=h,"real_buffer_distance")
        # For center plaquette F=(1+Re W_p)/2, 4 supporting links,
        # bound on expectation difference <=(4/6)*2^-d.
        require(4*3<=6*2**d,"plaquette_source_bound_at_most_one")
    return (
      'YM4_VOL16_GRAPH|original_4d_SU2_centered_b3_b5_b7=PASS|six_original_plaquette_planes=PASS|json=0\n'
      'YM4_VOL16_NEIGHBORS|one_shared_original_plaquette_per_pair=PASS|degree_le18=PASS|noncommuting_Q8_one_staple_change=PASS|json=0\n'
      'YM4_VOL16_DISTANCE|boundary_resultants=4_bminus1_times_b3_minus_bminus2cubed|center_source_graph_distance_ge_ceil_h_over2=PASS|json=0\n'
      'YM4_VOL16_SMALL_BETA|beta_le_1over36|Dobrushin_alpha_le_1over2|one_site_boundary_b_le_1over12|json=0\n'
      'YM4_VOL16_PHYSICAL_BOUND|uniform_exterior_unweighted_response_le_source_links_over6_times_2power_minus_graph_distance=ANALYTIC|json=0\n'
      'YM4_VOL16_INTERPOLATION|boundary_action_B_t_linear|all_t_in_0_1=ANALYTIC|signed_covariance_sum_bound=ANALYTIC|json=0\n'
      'YM4_VOL16_NEGATIVE|production_beta_9power12=OUTSIDE_DOBRUSHIN_RANGE|mass_gap_not_claimed=YES|json=0\n'
      'YM4_VOL16_SCOPE|strong_coupling_calibration=PASS|high_beta_unweighted_decay=OPEN|all_Gauss_sector=OPEN|11_continuum_gates=OPEN|json=0\n'
    )

if __name__=="__main__":
    print(acceptance(),end="")
