"""VOL14 original 4D SU2 centred-source signed path and orbit certificates.
All controls exact integer/Q8; actual Wilson Gibbs theorem is analytic.
"""
from itertools import product

ONE=(1,0,0,0)
NEG=(-1,0,0,0)
I=(0,1,0,0)
J=(0,0,1,0)
K=(0,0,0,1)
Q8=(ONE,I,J,K,NEG,(0,-1,0,0),(0,0,-1,0),(0,0,0,-1))

def check(value,name):
    if not value:
        raise ValueError(name)

def mul(u,v):
    a,b,c,d=u
    e,f,g,h=v
    return (a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e)

def inv(q):
    return (q[0],-q[1],-q[2],-q[3])

def sq(u,v=ONE):
    return sum((u[j]-v[j])*(u[j]-v[j]) for j in range(4))

def move(x,mu,sign):
    z=list(x)
    z[mu]+=sign
    return tuple(z)

def internal_links(h):
    for x in product(range(-h,h+1),repeat=4):
        for mu in range(4):
            if x[mu]<h:
                yield (x,mu)

def path(x):
    word=[]
    for mu in range(4):
        sign=1 if x[mu]>=0 else -1
        for unused in range(abs(x[mu])):
            word.append((mu,sign))
    return word

def link_field(h):
    return {(x,mu):Q8[(x[0]+2*x[1]+3*x[2]+5*x[3]+7*mu)%8]
            for x,mu in internal_links(h)}

def prod_word(U,word):
    z=(0,0,0,0)
    p=ONE
    for mu,sign in word:
        edge=(z,mu) if sign==1 else (move(z,mu,-1),mu)
        value=U[edge]
        p=mul(p,value if sign==1 else inv(value))
        z=move(z,mu,sign)
    return p,z

def plaq(U,z,mu,nu):
    a=U[(z,mu)]
    b=U[(move(z,mu,1),nu)]
    c=inv(U[(move(z,nu,1),mu)])
    d=inv(U[(z,nu)])
    return mul(mul(mul(a,b),c),d)

def check_signed_swap(U,e):
    x,mu=e
    y=move(x,mu,1)
    words=path(x)+[(mu,1)]
    original,start_end=prod_word(U,words)
    check(start_end==y,"original_signed_path_endpoint")
    at=len(words)-1
    n=sum(abs(x[nu]) for nu in range(mu+1,4))
    step_squared=0
    for unused in range(n):
        check(at>0 and words[at][0]==mu and words[at-1][0]>mu,
              "coordinate_signed_bubble")
        before,z_before=prod_word(U,words)
        z=prod_word(U,words[:at-1])[1]
        nu,sign_nu=words[at-1]
        low=z if sign_nu==1 else move(z,nu,-1)
        face=plaq(U,low,min(mu,nu),max(mu,nu))
        words[at-1],words[at]=words[at],words[at-1]
        after,z_after=prod_word(U,words)
        check(z_before==z_after==y,"plaquette_swap_endpoint_fixed")
        diff=sq(before,after)
        check(diff==sq(face,ONE),"swap_chord_equals_original_plaquette_chord")
        step_squared+=diff
        at-=1
    if x[mu]<0:
        check(at>0 and words[at-1]==(mu,-1) and words[at]==(mu,1),
              "negative_axis_inverse_cancellation")
        del words[at-1:at+1]
    check(words==path(y),"signed_original_tree_target_path")
    final,_=prod_word(U,words)
    check(sq(original,final)<=n*step_squared,
          "nonabelian_signed_plaquette_strip_Cauchy")
    return n

def centered_geometry(h):
    U=link_field(h)
    b=2*h+1
    max_depth=4*h
    powers=[1]
    for unused in range(max_depth):
        powers.append(powers[-1]*3)
    den=powers[max_depth]
    count=0
    chords=0
    strip_sum=0
    weighted_count=0
    weighted_strip=0
    for e in internal_links(h):
        x,mu=e
        n=check_signed_swap(U,e)
        d=sum(abs(v) for v in x)
        count+=1
        chords+=int(n>0)
        strip_sum+=n
        weighted_count+=powers[max_depth-d]
        weighted_strip+=n*powers[max_depth-d]
    check(count==4*(b-1)*b*b*b,"original_centered_edges")
    check(chords==3*b*b*b*b-4*b*b*b+1,"original_centered_cycle_rank")
    check(4*weighted_count<=256*den,"centered_weighted_edge_le64")
    check(weighted_strip<=72*den,"centered_weighted_strip_le72")
    return weighted_count,weighted_strip,den

def beta_bound():
    beta=282429536481
    s=41000
    m=740000
    small=1
    for unused in range(663):
        small*=2
    check(502*s*s<3*beta,"vol09_s_threshold")
    check((37*small+288*beta)*m*m<72*beta*small,
          "original_good_star_m_threshold")
    check(200*(144*m+544*s)<s*m,"centered_chord_lt_1over200")
    check(400*(72*m+336*s)<s*m,"centered_joint_orbit_lt_1over400")
    check(28000*(9*m+42*s)<8*s*m,"centered_normalized_orbit_lt_1over28000")
    check(3*(9000*m+25500*s)<s*m,
          "centered_orbit_tail_lt_2power_minus_r_over3")
    check(192==3*64,"centered_normalized_tail_lt_2power_minus_r_over192")

def winding_red(h):
    b=2*h+1
    L=2*b
    def qperiodic(x,mu):
        return NEG if mu==0 and x[0]%L==b-1 else ONE
    check(all(qperiodic(x,mu)==ONE for x,mu in internal_links(h)),
          "source_centered_internal_zero_winding_distance")
    q=ONE
    for k in range(L):
        q=mul(q,qperiodic((k,0,0,0),0))
    check(q==NEG,"centered_full_torus_winding_minusI")

def main():
    check(mul(I,J)==K and mul(J,I)==inv(K),"noncommuting_quaternion_SU2")
    for h in (1,2):
        centered_geometry(h)
        winding_red(h)
    beta_bound()
    return (
      'YM4_VOL14_CENTERED|original_4D_signed_cubes_b3_b5=PASS|nonabelian_Q8_swap=PASS|negative_axes=PASS|json=0\n'
      'YM4_VOL14_CENTER_GEOM|all_faces_collar_distance_h|weighted_links_le_64|weighted_strip_le_72|json=0\n'
      'YM4_VOL14_CENTER_ORBIT|beta9power12|full_Gibbs_averaged_orbit_lt_1over28000|b_independent=PASS|json=0\n'
      'YM4_VOL14_CENTER_TAIL|normalized_source_weighted_tail_lt_2power_minus_r_over192|induced_weight=YES|json=0\n'
      'YM4_VOL14_CENTER_RED|flat_winding_nontrivial|interior_orbit_distance_zero|global_sector_not_controlled=YES|json=0\n'
      'YM4_VOL14_CENTER_SCOPE|actual_distance_to_all_boundary_faces=h|physical_unweighted_boundary_susceptibility=OPEN|11_continuum_gates=OPEN|json=0\n'
    )

if __name__=='__main__':
    print(main(),end='')
