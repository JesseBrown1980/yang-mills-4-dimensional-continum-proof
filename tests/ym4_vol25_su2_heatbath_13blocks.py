"""YM4 VOL25: exact 13-feature SU2 Haar blocks and Wilson IBP recurrence.

Integer numerator/denominator operations and 24-point degree-four cubature.
The beta>0 Haar heat-bath block theorem is analytic; kappa=1 fixture is
synthetic rational recursion data, not an evaluated native Bessel ratio.
"""
from itertools import product
from math import gcd


def check(ok, label):
    if not ok:
        raise AssertionError(label)


def q(n,d=1):
    if isinstance(n,tuple):
        check(d==1 and len(n)==2,'pair_input')
        return n
    check(d!=0,'denominator')
    if d<0:
        n,d=-n,-d
    g=gcd(abs(n),d)
    return (n//g,d//g)


def add(a,b):
    return q(a[0]*b[1]+b[0]*a[1],a[1]*b[1])


def sub(a,b):
    return q(a[0]*b[1]-b[0]*a[1],a[1]*b[1])


def mul(a,b):
    return q(a[0]*b[0],a[1]*b[1])


def div(a,b):
    check(b[0]!=0,'divide_by_zero')
    return q(a[0]*b[1],a[1]*b[0])


def fmt(a):
    return str(a[0]) if a[1]==1 else str(a[0])+'/'+str(a[1])


def greater(a,b):
    return a[0]*b[1]>b[0]*a[1]


def inverse2(a):
    check(len(a)==2 and all(len(row)==2 for row in a),'two_by_two')
    det=sub(mul(a[0][0],a[1][1]),mul(a[0][1],a[1][0]))
    check(greater(det,q(0)),'positive_determinant')
    inv=[[div(a[1][1],det),div(q(-1),q(1))],
         [div(q(-1),q(1)),div(a[0][0],det)]]
    inv[0][1]=div(q(-a[0][1][0],a[0][1][1]),det)
    inv[1][0]=div(q(-a[1][0][0],a[1][0][1]),det)
    for i in range(2):
        for j in range(2):
            dot=add(mul(a[i][0],inv[0][j]),mul(a[i][1],inv[1][j]))
            check(dot==q(int(i==j)),'exact_inverse_product')
    return det,inv


def haar_points():
    pts=[]
    for i in range(4):
        for s in (-1,1):
            a=[0]*4
            a[i]=2*s
            pts.append(tuple(a))
    pts.extend(product((-1,1),repeat=4))
    check(len(pts)==24 and all(sum(x*x for x in v)==4 for v in pts),
          'original_SU2_degree_four_cubature')
    return pts


def adapted_features(v):
    t=v[0]
    # Each pair is (integer numerator, exact scale).
    h=[(t,2),(t*t-1,4)]
    for i in (1,2,3):
        h.append((v[i],2))
        h.append((t*v[i],4))
    for i,j in ((1,2),(1,3),(2,3)):
        h.append((v[i]*v[j],4))
    h.append((v[1]*v[1]-v[3]*v[3],4))
    h.append((v[2]*v[2]-v[3]*v[3],4))
    check(len(h)==13,'harmonic_feature_dimension')
    return h


def haar_gram():
    pts=haar_points()
    values=[adapted_features(v) for v in pts]
    for i in range(13):
        check(sum(row[i][0] for row in values)==0,
              'each_Haar_feature_centered')
    gram=[]
    for i in range(13):
        row=[]
        for j in range(13):
            numerator=sum(val[i][0]*val[j][0] for val in values)
            denominator=24*values[0][i][1]*values[0][j][1]
            row.append(q(numerator,denominator))
        gram.append(row)
    expect=[[q(0) for j in range(13)] for i in range(13)]
    expect[0][0]=q(1,4)
    expect[1][1]=q(1,16)
    for i in (2,4,6):
        expect[i][i]=q(1,4)
        expect[i+1][i+1]=q(1,24)
    for i in (8,9,10):
        expect[i][i]=q(1,24)
    expect[11][11]=q(1,6)
    expect[12][12]=q(1,6)
    expect[11][12]=q(1,12)
    expect[12][11]=q(1,12)
    check(gram==expect,'all_169_native_SU2_Haar_entries')
    ds,inv=inverse2([[gram[0][0],gram[0][1]],
                     [gram[1][0],gram[1][1]]])
    check(ds==q(1,64) and inv==[[q(4),q(0)],[q(0),q(16)]],
          'Haar_scalar_inverse')
    for i in (2,4,6):
        d,a=inverse2([[gram[i][i],gram[i][i+1]],
                      [gram[i+1][i],gram[i+1][i+1]]])
        check(d==q(1,96) and a==[[q(4),q(0)],[q(0),q(24)]],
              'Haar_vector_inverse')
    d,a=inverse2([[gram[11][11],gram[11][12]],
                  [gram[12][11],gram[12][12]]])
    check(d==q(1,48) and a==[[q(8),q(-4)],[q(-4),q(8)]],
          'Haar_tensor_difference_inverse')
    return gram


def synthetic_recursion():
    # Clear nonphysical test values: kappa=1, A=6/25, not I2(1)/I1(1).
    kap=q(1)
    m1=q(6,25)
    m2=sub(q(1),div(mul(q(3),m1),kap))
    m3=add(m1,div(sub(q(1),mul(q(4),m2)),kap))
    m4=add(m2,div(sub(mul(q(2),m1),mul(q(5),m3)),kap))
    check((m1,m2,m3,m4)==(q(6,25),q(7,25),q(3,25),q(4,25)),
          'exact_moment_recurrence_fixture')
    for j in (0,1,2):
        moments=(q(1),m1,m2,m3,m4)
        lhs=mul(kap,sub(moments[j],moments[j+2]))
        if j>0:
            lhs=add(lhs,mul(q(j),moments[j-1]))
        lhs=sub(lhs,mul(q(j+3),moments[j+1]))
        check(lhs==q(0),'integration_by_parts_recurrence')
    z=[[sub(m2,mul(m1,m1)),sub(m3,mul(m1,m2))],
       [sub(m3,mul(m1,m2)),sub(m4,mul(m2,m2))]]
    check(z==[[q(139,625),q(33,625)],
              [q(33,625),q(51,625)]],'synthetic_scalar_block')
    dz,_=inverse2(z)
    check(dz==q(48,3125),'synthetic_scalar_determinant')
    v=[[div(sub(q(1),m2),q(3)),div(sub(m1,m3),q(3))],
       [div(sub(m1,m3),q(3)),div(sub(m2,m4),q(3))]]
    check(v==[[q(6,25),q(1,25)],
              [q(1,25),q(1,25)]],'synthetic_vector_block')
    dv,_=inverse2(v)
    check(dv==q(1,125),'synthetic_vector_determinant')
    R4=add(sub(q(1),mul(q(2),m2)),m4)
    check(R4==q(3,5),'synthetic_transverse_fourth')
    off=div(R4,q(15))
    check(off==q(1,25),'synthetic_tensor_3_offdiagonal')
    tcoef=div(mul(q(2),R4),q(15))
    tensor=[[mul(q(2),tcoef),tcoef],
            [tcoef,mul(q(2),tcoef)]]
    dt,it=inverse2(tensor)
    check(dt==q(12,625),'synthetic_tensor_determinant')
    check(it==[[q(25,3),q(-25,6)],[q(-25,6),q(25,3)]],
          'synthetic_tensor_inverse')
    return dz,dv


def main():
    haar_gram()
    print('YM4_VOL25_HAAR|moments=0,1/4,0,1/8|features=13|cross_blocks=0|PASS')
    print('YM4_VOL25_BLOCKS|scalar=2|vector=3x2|tensor=3+2|Haar_inverse=PASS')
    dz,dv=synthetic_recursion()
    print('YM4_VOL25_RECURRENCE|kappa=0_Haar=PASS|kappa=1_synthetic=PASS|not_physical=1')
    print('YM4_VOL25_SYNTHETIC|m1=6/25|m2=7/25|m3=3/25|m4=4/25|det_scalar='+
          fmt(dz)+'|det_vector='+fmt(dv)+'|PASS')
    print('YM4_VOL25_SCOPE|native_SU2_13block=ANALYTIC|centered_source_value=OPEN|continuum_11=OPEN')


if __name__=='__main__':
    main()
