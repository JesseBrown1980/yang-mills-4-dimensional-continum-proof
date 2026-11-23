"""VOL13 original 4D noncommutative SU2 frame check in exact quaternion subgroup.

Theorem concerns ALL SU2 via group algebra. This exact-integer Q8 subgroup
fixture independently tests noncommuting plaquette holonomy, tree frames,
root-conjugacy cycle compatibility, and gauge-invariant obstruction.
"""
from collections import deque
from itertools import product

ONE=(1,0,0,0)
NEG=(-1,0,0,0)
I=(0,1,0,0)
J=(0,0,1,0)
K=(0,0,0,1)

def require(x,name):
    if not x:
        raise ValueError(name)

def mul(u,v):
    a,b,c,d=u
    e,f,g,h=v
    return (a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e)
def inv(u):
    return (u[0],-u[1],-u[2],-u[3])
def conj_by(u,v):
    return mul(mul(u,v),inv(u))
def next_site(x,d,L,step=1):
    a=list(x)
    a[d]=(a[d]+step)%L
    return tuple(a)
def all_sites(L):
    return list(product(range(L),repeat=4))
def original_links(L):
    return [(x,d) for x in all_sites(L) for d in range(4)]
def site_gauge(x):
    group=(ONE,I,J,K,NEG,inv(I),inv(J),inv(K))
    return group[(x[0]+2*x[1]+3*x[2]+5*x[3])%8]
def setup(L):
    links=original_links(L)
    base={e:(I if e[1]==0 else J if e[1]==1 else ONE) for e in links}
    frames={x:site_gauge(x) for x in all_sites(L)}
    shifted={e:mul(mul(frames[e[0]],base[e]),inv(frames[next_site(e[0],e[1],L)])) for e in links}
    return base,shifted,frames

def tree_frame(L,A,B,root_frame):
    root=(0,0,0,0)
    frames={root:root_frame}
    walk=deque([root])
    tree_edges=set()
    while walk:
        x=walk.popleft()
        for d in range(4):
            for step in (1,-1):
                y=next_site(x,d,L,step)
                e=(x,d) if step==1 else (y,d)
                if y not in frames:
                    # V_e = g_x U_e (g_y)^-1; for reverse edges
                    # use Ue^-1,Ve^-1 for the path x->y.
                    u=A[e] if step==1 else inv(A[e])
                    v=B[e] if step==1 else inv(B[e])
                    frames[y]=mul(mul(inv(v),frames[x]),u)
                    tree_edges.add(e)
                    walk.append(y)
    require(len(frames)==L**4 and len(tree_edges)==L**4-1,'original_spanning_tree')
    mismatch=set()
    for e,u in A.items():
        x,d=e
        y=next_site(x,d,L)
        expected=mul(mul(frames[x],u),inv(frames[y]))
        if expected!=B[e]:
            mismatch.add(e)
    require(not (tree_edges & mismatch),'all_tree_links_exact_aligned')
    return frames,mismatch,tree_edges

def rooted_tree_transports(L,A,tree_edges):
    root=(0,0,0,0)
    P={root:ONE}
    queue=deque([root])
    while queue:
        x=queue.popleft()
        for d in range(4):
            for step in (1,-1):
                y=next_site(x,d,L,step)
                e=(x,d) if step==1 else (y,d)
                if e not in tree_edges or y in P:
                    continue
                u=A[e] if step==1 else inv(A[e])
                P[y]=mul(P[x],u)
                queue.append(y)
    require(len(P)==L**4,'all_tree_transports')
    return P

def chord_conjugacy(L,A,B,tree,root_frame,frames):
    PA=rooted_tree_transports(L,A,tree)
    PB=rooted_tree_transports(L,B,tree)
    mismatches=set()
    for e in A:
        if e in tree:
            continue
        x,d=e
        y=next_site(x,d,L)
        cycleA=mul(mul(PA[x],A[e]),inv(PA[y]))
        cycleB=mul(mul(PB[x],B[e]),inv(PB[y]))
        root_target=conj_by(root_frame,cycleA)
        x,d=e
        y=next_site(x,d,L)
        site_target=mul(mul(frames[x],A[e]),inv(frames[y]))
        direct_sq=sum((B[e][j]-site_target[j])**2 for j in range(4))
        rooted_sq=sum((cycleB[j]-root_target[j])**2 for j in range(4))
        require(direct_sq==rooted_sq,'bi_invariant_SU2_exact_chord_distance_identity')
        if rooted_sq:
            mismatches.add(e)
    return mismatches

def plaq(L,U,x,mu,nu):
    a=U[(x,mu)]
    b=U[(next_site(x,mu,L),nu)]
    c=inv(U[(next_site(x,nu,L),mu)])
    d=inv(U[(x,nu)])
    return mul(mul(mul(a,b),c),d)

def loop(L,U,d):
    x=(0,0,0,0)
    q=ONE
    for unused in range(L):
        q=mul(q,U[(x,d)])
        x=next_site(x,d,L)
    return q

def main():
    require(mul(I,J)==K and mul(J,I)==inv(K),'noncommuting_quaternion_group')
    for L in (4,6):
        A,B,site=setup(L)
        require(plaq(L,A,(0,0,0,0),0,1)==NEG,'genuine_nonabelian_curvature')
        root_frame=site[(0,0,0,0)]
        frames,bad,tree=tree_frame(L,A,B,root_frame)
        require(not bad and all(frames[x]==site[x] for x in frames),
                'nonabelian_true_site_gauge_reconstructed')
        require(not chord_conjugacy(L,A,B,tree,root_frame,frames),
                'all_rooted_chord_holonomies_conjugate')
        require(len(tree)==L**4-1 and 4*L**4-len(tree)==3*L**4+1,
                'exact_cycle_rank')
        # Flat Z2 cut alters winding but preserves EVERY original
        # plaquette holonomy, and is not gauge conjugate (central trace).
        Bw={}
        for e,v in B.items():
            x,d=e
            Bw[e]=mul(NEG,v) if d==0 and x[0]==L-1 else v
        for x in all_sites(L):
            for mu in range(4):
                for nu in range(mu+1,4):
                    require(plaq(L,B,x,mu,nu)==plaq(L,Bw,x,mu,nu),
                            'winding_twist_preserves_all_plaquettes')
        require(loop(L,Bw,0)==mul(NEG,loop(L,B,0)),
                'nontrivial_gauge_invariant_polyakov_trace_flip')
        frames_w,missing_w,tree_w=tree_frame(L,A,Bw,root_frame)
        require(missing_w and chord_conjugacy(L,A,Bw,tree_w,root_frame,frames_w)==missing_w,
                'rooted_chord_test_detects_winding')
        # Local isolated central edge flip changes elementary plaquette
        # curvature in the original 4D SU2 field.
        Bl=dict(B)
        e=((0,0,0,0),0)
        Bl[e]=mul(NEG,Bl[e])
        require(plaq(L,B,(0,0,0,0),0,1)!=plaq(L,Bl,(0,0,0,0),0,1),
                'local_plaquette_trace_red')
        frames_l,missing_l,tree_l=tree_frame(L,A,Bl,root_frame)
        require(missing_l and chord_conjugacy(L,A,Bl,tree_l,root_frame,frames_l)==missing_l,
                'rooted_chord_test_detects_plaquette')
    return (
        'YM4_VOL13_NONABELIAN|original_SU2_quaternions=EXACT_Q8_SUBGROUP|L4_L6=PASS|i_j_noncommute=PASS|json=0\n'
        'YM4_VOL13_TREE|vertex_frame_from_path=PASS|tree_edges=Lpower4minus1|chords=3Lpower4plus1|json=0\n'
        'YM4_VOL13_CHORD|relative_frame_exists_iff_root_conjugated_chord_holonomies_match=ANALYTIC|positive_control=PASS|json=0\n'
        'YM4_VOL13_NEGATIVES|local_SU2_plaquette_mismatch=REJECTED|flat_central_winding_mismatch=REJECTED|json=0\n'
        'YM4_VOL13_BOUND|unit_quaternion_chord_distance_equals_rooted_cycle_distance=ANALYTIC|radial_TV_lt_1over24=IMPORTED_VOL12|json=0\n'
        'YM4_VOL13_SCOPE|continuous_SU2_tree_theorem=ANALYTIC|nonabelian_exact_Q8_fixture=PASS|quantitative_good_chord_residual=OPEN|delta_good=OPEN|11_continuum_gates=OPEN|json=0\n'
    )

if __name__=="__main__":
    print(main(),end="")
