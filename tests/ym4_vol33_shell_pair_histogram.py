"""YM4 VOL33 exact integer spherical pair-histogram two-point contraction.

Only discrete geometry and universal convolution algebra are certified.
Continuous SU2 beta2 field readings are separate floating MC pilots.
"""

def verify(ok,label):
    if not ok:
        raise AssertionError(label)

def sphere(radius):
    return [(a,b,c,d) for a in range(-radius,radius+1)
            for b in range(-radius,radius+1)
            for c in range(-radius,radius+1)
            for d in range(-radius,radius+1)
            if a*a+b*b+c*c+d*d==radius*radius]

def make_pair_weights(L,radius,separation):
    base=sphere(radius)
    center={tuple(q%L for q in x) for x in base}
    outer={tuple((q+(separation if axis==2 else 0))%L
                 for axis,q in enumerate(x)) for x in base}
    verify(len(center)==len(outer)==len(base),'embedded_torus_shells')
    hist={}
    for x in center:
        for y in outer:
            h=tuple((y[i]-x[i])%L for i in range(4))
            hist[h]=hist.get(h,0)+1
    n=len(base)
    j=len(center&outer)
    verify(sum(hist.values())==n*n,'pair_normalization')
    verify(hist.get((0,0,0,0),0)==j,'zero_displacement_shared')
    return center,outer,hist,n,j

def sites(L):
    for a in range(L):
        for b in range(L):
            for c in range(L):
                for d in range(L):
                    yield (a,b,c,d)

def translate(x,h,L):
    return tuple((x[i]+h[i])%L for i in range(4))

def test_integer_contraction(L,A,B,hist,case):
    coords=list(sites(L))
    if case==0:
        field={x:(3*x[0]+5*x[1]+7*x[2]+11*x[3])%19-9 for x in coords}
    else:
        field={x:((x[0]+2*x[1]+3*x[2]+4*x[3])**2+5*x[0]*x[2])%37-18
               for x in coords}
    total=len(coords)
    p_sum=sum(field.values())
    K_num={h:sum(field[x]*field[translate(x,h,L)] for x in coords)
           for h in hist}
    direct=sum(sum(field[translate(t,x,L)] for x in A)*
               sum(field[translate(t,y,L)] for y in B)
               for t in coords)
    reconstructed=sum(count*K_num[h] for h,count in hist.items())
    verify(direct==reconstructed,'independent_shell_K_contraction')
    n=len(A)
    centered_direct=total*direct-n*n*p_sum*p_sum
    centered={h:total*K_num[h]-p_sum*p_sum for h in hist}
    contracted=sum(count*centered[h] for h,count in hist.items())
    verify(centered_direct==contracted,'exact_connected_centering')
    common=hist.get((0,0,0,0),0)*centered.get((0,0,0,0),0)
    offdiag=sum(count*centered[h] for h,count in hist.items()
                if h!=(0,0,0,0))
    verify(common+offdiag==contracted,'exact_common_offdiag_split')

def main():
    L=6
    print('YM4_VOL33_MODEL|L=6|original_4D_integer_site_geometry=PASS|continuous_SU2_measurement=SEPARATE_PILOT')
    for radius in (1,2):
        for sep in (2,3):
            A,B,H,n,j=make_pair_weights(L,radius,sep)
            verify(len(H)>0 and H.get((0,0,0,0),0)==j,'hist_correct')
            for case in (0,1):
                test_integer_contraction(L,A,B,H,case)
            print('YM4_VOL33_GEOMETRY|r='+str(radius)+'|d='+str(sep)+
                  '|N='+str(n)+'|J='+str(j)+'|pair_sum='+str(n*n)+
                  '|hist_bins='+str(len(H))+'|PASS')
            print('YM4_VOL33_CONTRACTION|r='+str(radius)+'|d='+str(sep)+
                  '|independent_integer_fields=2|raw=EXACT|connected=EXACT|diag_plus_offdiag=EXACT|PASS')
    print('YM4_VOL33_HAAR|beta=0|K0_Re=1/4|Knonzero_Re=0|mean_Re=0|ANALYTIC')
    print('YM4_VOL33_SCOPE|math_contraction=PASS|beta2_mc=PROVISIONAL|beta9pow12_shell=OPEN|continuum_11=OPEN')

if __name__=='__main__':
    main()
