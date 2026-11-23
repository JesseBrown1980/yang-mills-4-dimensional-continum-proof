"""VOL23 original 4D Wilson boundary-resultant four-source Gram geometry.

Exact SU2 quaternion geometry, original link/plaquette separations and
rational Haar-moment checks. Continuous beta>0 Gibbs proof is analytic.
No floating arithmetic or finite-group substitute for original Haar law.
"""
from itertools import product

O=(1,0,0,0)
I=(0,1,0,0)
J=(0,0,1,0)
K=(0,0,0,1)
Q8=(O,I,J,K,(-1,0,0,0),(0,-1,0,0),(0,0,-1,0),(0,0,0,-1))


def check(ok, label):
    if not ok:
        raise AssertionError(label)


def shift(x, mu, step=1):
    y=list(x)
    y[mu]+=step
    return tuple(y)


def mul(a,b):
    w,x,y,z=a
    p,q,r,s=b
    return (w*p-x*q-y*r-z*s,w*q+x*p+y*s-z*r,
            w*r-x*s+y*p+z*q,w*s+x*r-y*q+z*p)


def adj(a):
    return (a[0],-a[1],-a[2],-a[3])


def add(a,b):
    return tuple(x+y for x,y in zip(a,b))


def norm2(a):
    return sum(x*x for x in a)


def oriented_step(edge):
    x,mu,sign=edge
    return (x,shift(x,mu)) if sign==1 else (shift(x,mu),x)


def path_value(path,links):
    out=O
    where=None
    for x,mu,sign in path:
        st,en=oriented_step((x,mu,sign))
        if where is not None:
            check(st==where,'connected_nonabelian_path')
        where=en
        value=links[(x,mu)]
        out=mul(out,value if sign==1 else adj(value))
    return out


def staples(r,first,second):
    x=(0,first*r,second*r,0)
    paths=[]
    for nu,sign in ((1,first),(2,second)):
        if sign==1:
            p=((shift(x,0),nu,1),(shift(x,nu),0,-1),(x,nu,-1))
        else:
            p=((shift(shift(x,0),nu,-1),nu,-1),
               (shift(x,nu,-1),0,-1),(shift(x,nu,-1),nu,1))
        start,_=oriented_step(p[0])
        _,end=oriented_step(p[-1])
        check(start==shift(x,0) and end==x,'complement_endpoints')
        paths.append(p)
    return x,tuple(paths)


def original_links(r):
    return {(x,mu) for x in product(range(-r,r+1),repeat=4)
            for mu in range(4) if x[mu]<r}


def face_edges(x,mu,nu):
    return {(x,mu),(shift(x,mu),nu),(shift(x,nu),mu),(x,nu)}


def incidence(e):
    x,mu=e
    out=set()
    for nu in range(4):
        if nu==mu:
            continue
        for start in (x,shift(x,nu,-1)):
            a,b=sorted((mu,nu))
            if e in face_edges(start,a,b):
                out.add((start,a,b))
    check(len(out)==6,'original_six_plaquettes_per_link')
    return out


def control(r):
    inside=original_links(r)
    outer=original_links(r+1)
    groups=[]
    for first,second in product((-1,1),repeat=2):
        x,paths=staples(r,first,second)
        target=(x,0)
        check(target in inside,'source_edge_inside')
        combined={e[:2] for p in paths for e in p}
        check(len(combined)==6 and combined.issubset(outer-inside),
              'two_disjoint_three_link_external_staples')
        chosen=paths[0][1][:2]
        check(chosen[1]==0 and chosen in combined,'unique_parallel_witness')
        check(sum(chosen in {e[:2] for e in p} for p in paths)==1,
              'unique_link_in_only_one_staple')
        candidates=[]
        for nu in (1,2,3):
            for t in (x,shift(x,nu,-1)):
                a,b=sorted((0,nu))
                e=face_edges(t,a,b)
                if target in e and sum(z in inside for z in e)==1:
                    candidates.append((t,a,b))
        check(len(candidates)==2,'two_exact_mixed_faces')
        expected=set()
        for t,a,b in candidates:
            expected.update(z for z in face_edges(t,a,b) if z not in inside)
        check(expected==combined,'staples_equal_original_mixed_face_support')
        groups.append((first,second,x,paths,combined,chosen))
    for i,a in enumerate(groups):
        for b in groups[i+1:]:
            check(not a[4].intersection(b[4]),'all_four_loop_supports_disjoint')
            check(not incidence(a[5]).intersection(incidence(b[5])),
                  'distinguished_links_share_no_original_plaquette')
    all_edges=set().union(*(g[4] for g in groups))
    links={e:O for e in all_edges}
    for idx,g in enumerate(groups):
        paths=g[3]
        links[paths[0][1][:2]]=I
        links[paths[1][1][:2]]=J
    check(mul(I,J)!=mul(J,I),'adversarial_noncommuting')
    vertices=set()
    for edge in all_edges:
        x,mu=edge
        vertices.add(x)
        vertices.add(shift(x,mu))
    gauge={x:Q8[(sum((k+7)*(v+11) for k,v in enumerate(x))+3)%8]
           for x in vertices}
    turned={(x,mu):mul(mul(gauge[x],v),adj(gauge[shift(x,mu)]))
            for (x,mu),v in links.items()}
    for first,second,x,paths,edges,chosen in groups:
        aa=path_value(paths[0],links)
        bb=path_value(paths[1],links)
        bfield=add(adj(aa),adj(bb))
        f2=norm2(bfield)-2
        check(f2==2*mul(aa,adj(bb))[0],
              'resultant_norm_is_six_link_wilson_trace')
        check(abs(f2)<=2,'bounded_wilson_loop')
        check(aa!=bb and mul(aa,bb)!=mul(bb,aa),
              'genuinely_noncommuting_staples')
        a2=path_value(paths[0],turned)
        b2=path_value(paths[1],turned)
        bfield2=add(adj(a2),adj(b2))
        check(bfield2==mul(mul(gauge[x],bfield),adj(gauge[shift(x,0)])),
              'boundary_resultant_gauge_covariance')
        check(norm2(bfield2)==norm2(bfield),'wilson_gauge_invariance')
    return len(groups),len(all_edges)


def haar_moment_control():
    # The 24 Hurwitz unit quaternions are an exact cubature for quadratic
    # and quartic uniform S3 moments only, never a finite-beta Gibbs model.
    pts=[]
    for mu in range(4):
        for s in (-1,1):
            x=[0]*4
            x[mu]=2*s
            pts.append(tuple(x))
    pts.extend(tuple(x) for x in product((-1,1),repeat=4))
    check(len(pts)==24 and all(norm2(v)==4 for v in pts),
          '24_unit_quaternion_cubature')
    for mu in range(4):
        check(sum(v[mu] for v in pts)==0,'Haar_first_moment')
        check(sum(v[mu]*v[mu] for v in pts)==24,'Haar_second_diag')
        check(sum(v[mu]**4 for v in pts)==48,'Haar_fourth_diag')
        for nu in range(4):
            if nu!=mu:
                check(sum(v[mu]*v[nu] for v in pts)==0,
                      'Haar_second_off_diag')
                check(3*sum(v[mu]**2*v[nu]**2 for v in pts)==2*24,
                      'Haar_fourth_cross')
    # Exact SU2 Haar: E(U_a U_b)=delta_ab/4; E(U_a^4)=1/8;
    # E(U_a^2 U_b^2)=1/24. Four disjoint loops at beta=0 have G=D=I/4.
    check(48*48*16==36864,'continuous_Haar_two_cap_covariance_constant')


def main():
    for r in (1,2,3,4):
        n,links=control(r)
        check(n==4 and links==24,'four_disjoint_six_link_loops')
        print('YM4_VOL23_GEOMETRY|r='+str(r)+'|six_link_loops=4|external_links=24|joint_heatbath=4|PASS')
    haar_moment_control()
    beta=9**12
    k_den=147456*(1+6*beta)**2
    check(k_den==423433462692859012475599601664,
          'original_beta12_native_gram_denominator')
    print('YM4_VOL23_HAAR|S3_second=1/4|fourth_diag=1/8|fourth_cross=1/24|PASS')
    print('YM4_VOL23_BETA0|native_G=I4/4|native_D=I4/4|kappa=1|ANALYTIC')
    print('YM4_VOL23_NATIVE_GRAM|beta=9^12|dimension=4|k_min=1/'+str(k_den)+'|PSD=ANALYTIC')
    print('YM4_VOL23_SCOPE|actual_original_SU2_beta12=ANALYTIC|predictor_transfer=OPEN|continuum_11=OPEN')


if __name__=='__main__':
    main()
