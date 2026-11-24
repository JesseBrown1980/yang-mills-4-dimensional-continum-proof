"""VOL35 integer-only finite-volume spherical source / reported-data audit.

The numerical chain input is rounded exploratory data, not a Gibbs measure
certificate. The exact lattice geometry and integer arithmetic are proven.
"""
SOURCE='docs/certificate-atlas/YM4-VOL35-FIXED-POINT-CHAINS-20261124.csv'
HEADER='L,beta,seed,configs,mean_x1e12,K0_x1e12,Ktime1_x1e12,Ktime2_x1e12,Ktime3_x1e12,Kspatial1_x1e12,r1d2_off_x1e12,r1d3_off_x1e12,r2d2_off_x1e12,r2d3_off_x1e12,time1_late_minus_early_x1e12'

def check(ok,key):
    if not ok:
        raise AssertionError(key)

def moment(group,column):
    vals=[v[column] for v in group]
    n=len(vals)
    check(n>=2,'independent_seeds')
    s=sum(vals)
    varnum=n*sum(v*v for v in vals)-s*s
    check(varnum>=0,'variance_numerator_positive')
    return n,s,varnum

def comparison(a,b,col,threshold):
    na,sa,va=moment(a,col)
    nb,sb,vb=moment(b,col)
    d=sa*nb-sb*na
    lhs=d*d*(na-1)*(nb-1)
    rhs=threshold*threshold*(va*nb*nb*(nb-1)+vb*na*na*(na-1))
    return lhs>rhs

def near_zero(a,col,threshold):
    n,s,v=moment(a,col)
    return s*s*(n-1)<threshold*threshold*v

def sphere(radius):
    pts=set()
    for a in range(-radius,radius+1):
        for b in range(-radius,radius+1):
            for c in range(-radius,radius+1):
                for d in range(-radius,radius+1):
                    if a*a+b*b+c*c+d*d==radius*radius:
                        pts.add((a,b,c,d))
    return pts

def histogram(L,r,d):
    a=sphere(r)
    A={tuple(p%L for p in site) for site in a}
    B={tuple((p+(d if axis==2 else 0))%L for axis,p in enumerate(site))
       for site in a}
    H={}
    for x in A:
        for y in B:
            z=tuple((y[i]-x[i])%L for i in range(4))
            H[z]=H.get(z,0)+1
    check(len(A)==len(a)==len(B),'injective_embedded_spheres')
    check(sum(H.values())==len(a)*len(a),'ordered_sphere_pairs')
    check(H.get((0,0,0,0),0)==len(A&B),'diagonal_overlap_identity')
    return len(a),len(A&B),len(H)

def main():
    with open(SOURCE,encoding='utf-8') as f:
        lines=f.read().splitlines()
    check(lines[0]==HEADER,'fixed_point_schema')
    groups={(L,b):[] for L in (8,10) for b in (0,2)}
    seeds=set()
    for line in lines[1:]:
        cells=line.split(',')
        check(len(cells)==15,'exact_fixedpoint_row_width')
        row=tuple(int(x) for x in cells)
        L,b,seed,n=row[:4]
        check((L,b) in groups,'fixed_volume_and_beta')
        check((L,b,seed) not in seeds,'unique_chain_seed')
        seeds.add((L,b,seed))
        check(n==(350 if L==8 and b==2 else 220 if L==10 and b==2 else 500),
              'complete_seed_sample_count')
        check(row[5]>0,'positive_Wilson_self_covariance')
        groups[L,b].append(row)
    check(len(lines)==27,'exact_twenty_six_chains')
    for L in (8,10):
        check(len(groups[L,0])==6,'Haar_seeds_per_volume')
        check(len(groups[L,2])==(8 if L==8 else 6),'interacting_seeds_per_volume')
    check(sum(row[3] for group in groups.values() for row in group)==10120,
          'ten_thousand_one_hundred_twenty_complete_frames')
    print('YM4_VOL35_INPUT|L8_beta2=8x350|L10_beta2=6x220|Haar=12x500|chains=26|total_configs=10120|scale=10pow12|PASS')
    for L in (8,10):
        for r,d,expected in ((1,2,(8,1,33)),(1,3,(8,0,33)),
                             (2,2,(24,8,165 if L==8 else 169)),
                             (2,3,(24,0,165 if L==8 else 169))):
            observed=histogram(L,r,d)
            check(observed==expected,'original_4D_periodic_histogram')
            print('YM4_VOL35_GEOMETRY|L='+str(L)+'|r='+str(r)+'|d='+str(d)+
                  '|N='+str(observed[0])+'|shared='+str(observed[1])+ '|bins='+str(observed[2])+'|PASS')
    for L in (8,10):
        H=groups[L,0]
        I=groups[L,2]
        check(near_zero(H,6,3),'zero_Haar_nearest_time_consistent')
        check(comparison(I,H,6,5),'interacting_C1_different_from_Haar')
        check(comparison(I,H,11,3),'nonoverlap_R1_d3_beta2_vs_Haar')
        check(comparison(I,H,13,5),'nonoverlap_R2_d3_beta2_vs_Haar')
        check(not comparison(I,H,12,2),'overlap_R2_d2_unresolved')
        print('YM4_VOL35_INDEPENDENT|L='+str(L)+'|Haar_C1_within_3SE=PASS|beta2_C1_above_Haar_5SE=PASS|r1d3_J0_above_Haar_3SE=PASS|r2d3_J0_above_Haar_5SE=PASS|r2d2=HOLD')
    check(not comparison(groups[8,2],groups[10,2],6,2),
          'nearest_time_C1_volume_agreement')
    check(comparison(groups[8,2],groups[10,2],13,3),
          'r2d3_finite_volume_effect')
    check(not comparison(groups[8,2],groups[10,2],11,2),
          'r1d3_volume_difference_unresolved')
    print('YM4_VOL35_VOLUME|C1_L8_vs_L10_within_2SE=PASS|r2d3_difference_gt_3SE=PASS|r1d3_difference_within_2SE=HOLD')
    print('YM4_VOL35_SCOPE|geometry=EXACT|reported_chain_arithmetic=EXACT|simulation=EXPLORATORY|production_beta9pow12=OPEN|upper_mass_decay=OPEN|continuum_11=OPEN')

if __name__=='__main__':
    main()
