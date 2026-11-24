"""VOL34 exact-integer evidence-accounting witness for rounded MC chain means.

Checks finite reported chain mean arithmetic only: not a rigorous SU2 proof,
not a source of statistical confidence guarantees, not a validation of sampling.
The original physical model is continuous SU2; exploratory measurements are
produced externally with numerical Monte Carlo.
"""

PATH='docs/certificate-atlas/YM4-VOL34-FIXED-POINT-CHAINS-20261124.csv'
EXPECTED={'Heatbath_L6_beta0':6,'Heatbath_L6_beta2':8,
          'Metropolis_L6_beta0':6,'Metropolis_L6_beta2':8,
          'MetropolisSphere_L6_beta0':6,'MetropolisSphere_L6_beta2':8}

def check(ok,name):
    if not ok:
        raise AssertionError(name)

def group_measurements(rows,column):
    a=[row[column] for row in rows]
    n=len(a)
    check(n>1,'independent_chains_required')
    total=sum(a)
    varnum=n*sum(v*v for v in a)-total*total
    check(varnum>=0,'chain_mean_variance_nonnegative')
    return n,total,varnum

def higher_than_sigma(A,B,key,sigma):
    a,ta,va=group_measurements(A,key)
    b,tb,vb=group_measurements(B,key)
    difference=b*ta-a*tb
    numerator=difference*difference*(a-1)*(b-1)
    vtotal=va*b*b*(b-1)+vb*a*a*(a-1)
    return numerator>sigma*sigma*vtotal

def close_within_sigma(A,B,key,sigma):
    return not higher_than_sigma(A,B,key,sigma)

def near_zero(rows,key,sigma):
    n,total,varnum=group_measurements(rows,key)
    return total*total*(n-1)<sigma*sigma*varnum

def main():
    with open(PATH,encoding='utf-8') as source:
        content=source.read().strip().splitlines()
    check(content[0]=='group,seed,K0_x1e12,Ktime1_x1e12,r1d2_offdiag_x1e12,r1d3_offdiag_x1e12,r2d2_offdiag_x1e12,r2d3_offdiag_x1e12','exact_input_schema')
    grouped={k:[] for k in EXPECTED}
    for line in content[1:]:
        cells=line.split(',')
        check(len(cells)==8,'fixed_point_columns')
        tag=cells[0]
        check(tag in grouped,'known_method_coupling_group')
        row=tuple(int(x) for x in cells[1:])
        check(row[1]>0,'true_observable_self_variance_positive')
        grouped[tag].append(row)
    check(sum(len(v) for v in grouped.values())==42,'exact_42_independent_chain_summaries')
    for key,n in EXPECTED.items():
        observed=grouped[key]
        check(len(observed)==n,'grouped_chain_count')
        check(len(set(v[0] for v in observed))==n,'unique_chain_seed')
    print('YM4_VOL34_INPUT|methods=2|couplings=0,2|groups=6|chain_summaries=42|scale=10pow12|PASS')
    hb=grouped['Heatbath_L6_beta2']
    metro=grouped['Metropolis_L6_beta2']
    check(close_within_sigma(hb,metro,2,2),'independent_two_engines_C1_within_two_SE')
    check(higher_than_sigma(hb,grouped['Heatbath_L6_beta0'],2,4),'heatbath_nonzero_beta_C1_above_Haar')
    check(higher_than_sigma(metro,grouped['Metropolis_L6_beta0'],2,4),'metropolis_nonzero_beta_C1_above_Haar')
    print('YM4_VOL34_TWO_ENGINES|L=6|beta=2|Ktime1_agreement_within_2_SE=PASS|both_above_Haar_by_4_SE=PASS')
    check(near_zero(grouped['Metropolis_L6_beta0'],2,2),'Haar_independent_Metropolis_C1_zero')
    check(near_zero(grouped['Heatbath_L6_beta0'],2,2),'Haar_independent_heatbath_C1_zero')
    print('YM4_VOL34_HAAR|beta=0|Ktime1_zero_within_2_SE_both_methods=PASS')
    sphere0=grouped['MetropolisSphere_L6_beta0']
    sphere2=grouped['MetropolisSphere_L6_beta2']
    for pos,name,shared,threshold in ((3,'r1d2',1,2),(4,'r1d3',0,4),
                                      (5,'r2d2',9,2),(6,'r2d3',0,6)):
        yes=higher_than_sigma(sphere2,sphere0,pos,threshold)
        if shared==0:
            check(yes,'nonoverlap_beta2_vs_Haar_radial_signal')
            print('YM4_VOL34_RADIAL|case='+name+'|shared_J=0|beta2_minus_Haar_exceeds_'+str(threshold)+'_combined_SE=PASS')
        else:
            check(not yes,'overlap_radial_contrast_inconclusive')
            print('YM4_VOL34_RADIAL|case='+name+'|shared_J='+str(shared)+'|beta2_minus_Haar_within_'+str(threshold)+'_combined_SE=HOLD')
    print('YM4_VOL34_SCOPE|machine_check=ROUNDED_STATISTICAL_ARITHMETIC_ONLY|physical_measurements=EXPLORATORY|L128_beta9pow12=OPEN|continuum_11=OPEN')

if __name__=='__main__':
    main()
