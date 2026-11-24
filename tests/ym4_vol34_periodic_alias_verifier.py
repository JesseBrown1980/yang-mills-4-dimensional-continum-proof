"""VOL34: exact original 4D spherical pair overlap under periodic aliases.

Integer geometry only. Corrects radius-two overlap before comparing
finite-volume SU2 Wilson radial covariance data.
"""

def check(ok,name):
    if not ok:
        raise AssertionError(name)

def shell(r,L):
    out=set()
    for a in range(-r,r+1):
        for b in range(-r,r+1):
            for c in range(-r,r+1):
                for d in range(-r,r+1):
                    if a*a+b*b+c*c+d*d==r*r:
                        out.add((a%L,b%L,c%L,d%L))
    return out

def pair_hist(A,B,L):
    hist={}
    for a in A:
        for b in B:
            h=tuple((b[i]-a[i])%L for i in range(4))
            hist[h]=hist.get(h,0)+1
    return hist

def main():
    expected={
       (6,1,2):(8,1,33),(6,1,3):(8,0,33),
       (6,2,2):(24,9,129),(6,2,3):(24,0,129),
       (8,1,2):(8,1,33),(8,1,3):(8,0,33),
       (8,2,2):(24,8,165),(8,2,3):(24,0,165),
       (10,1,2):(8,1,33),(10,1,3):(8,0,33),
       (10,2,2):(24,8,169),(10,2,3):(24,0,169)
    }
    for L in (6,8,10):
        for r in (1,2):
            a=shell(r,L)
            for d in (2,3):
                b={(x[0],x[1],(x[2]+d)%L,x[3]) for x in a}
                hist=pair_hist(a,b,L)
                n,j,bins=expected[(L,r,d)]
                check(len(a)==len(b)==n,'original_lattice_shell_cardinality')
                check(len(a&b)==hist.get((0,0,0,0),0)==j,'exact_periodic_shared_count')
                check(len(hist)==bins,'exact_periodic_pair_histogram_bins')
                check(sum(hist.values())==n*n,'exact_all_ordered_pair_count')
                print('YM4_VOL34_ALIAS|L='+str(L)+'|R='+str(r)+'|d='+str(d)+
                      '|N='+str(n)+'|J='+str(j)+'|bins='+str(bins)+'|PASS')
    core={(a,b,1,c) for a in (-1,1) for b in (-1,1) for c in (-1,1)}
    check(len(core)==8,'exact_8_unwrapped_four_sphere_shared_sites')
    for L in (6,8,10):
        A=shell(2,L)
        B={(x[0],x[1],(x[2]+2)%L,x[3]) for x in A}
        overlap=A&B
        wrapped={tuple(v%L for v in x) for x in core}
        extra=overlap-wrapped
        if L==6:
            check(extra=={(0,0,4,0)},'L6_one_extra_periodic_alias')
        else:
            check(not extra,'L8_L10_no_extra_alias')
    print('YM4_VOL34_ALIAS_DIFFERENCE|R=2|d=2|L6_J=9|L8_J=8|extra_L6_site=0,0,4,0|PASS')
    print('YM4_VOL34_SCOPE|integer_periodic_geometry=PASS|L8_beta2_screening=PROVISIONAL|production_L128=OPEN|continuum_11=OPEN')

if __name__=='__main__':
    main()
