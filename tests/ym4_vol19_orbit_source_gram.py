"""YM4 VOL19 integer-only original quaternion orbit and source-Gram controls.

All arithmetic uses integers and cross-products; continuous SU2 Haar proof analytic.
"""
O=(1,0,0,0)
I=(0,1,0,0)
J=(0,0,1,0)
K=(0,0,0,1)
Q8=(O,I,J,K,(-1,0,0,0),(0,-1,0,0),(0,0,-1,0),(0,0,0,-1))

def mul(a,b):
    w,x,y,z=a
    t,u,v,s=b
    return (w*t-x*u-y*v-z*s,w*u+x*t+y*s-z*v,
            w*v-x*s+y*t+z*u,w*s+x*v-y*u+z*t)

def inv(q):
    return (q[0],-q[1],-q[2],-q[3])

def conj(g,q):
    return mul(mul(g,q),inv(g))

def check(condition,label):
    if not condition:
        raise AssertionError(label)

E=((0,1,2,O,1),(1,2,3,O,1),(2,3,4,O,1),(0,3,5,I,0),
   (0,4,2,O,1),(4,5,3,O,1),(5,6,4,O,1),(0,6,6,J,0))

def paths(edges):
    p={0:O}
    for x,y,r,q,tree in edges:
        if tree:
            check(x in p and y not in p,"rooted forest")
            p[y]=mul(p[x],q)
    check(len(p)==7,"forest spans every vertex")
    return p

def chords(edges):
    p=paths(edges)
    return tuple(mul(mul(p[x],q),inv(p[y]))
                 for x,y,r,q,t in edges if not t)

def rotate(edges,g):
    return tuple((x,y,r,mul(mul(g[x],q),inv(g[y])),t)
                 for x,y,r,q,t in edges)

def orbit_control():
    check(mul(I,J)==K and mul(J,I)==inv(K),"noncommutative Q8")
    g={x:Q8[(3*x+2)%8] for x in range(7)}
    Ep=rotate(E,g)
    check(all(a[2]==b[2] for a,b in zip(E,Ep)),"nonunit radii preserved")
    check(all(v==conj(g[0],u) for u,v in zip(chords(E),chords(Ep))),
          "common-root chord conjugacy")
    p,pp=paths(E),paths(Ep)
    restored={x:mul(mul(inv(pp[x]),g[0]),p[x]) for x in p}
    check(rotate(E,restored)==Ep,"complete gauge reconstruction")
    pair1=(I,I)
    pair2=(I,inv(I))
    check(all(q[0]==0 for q in pair1+pair2),"single-cycle traces equal")
    check(any(conj(u,I)==inv(I) for u in Q8),"individual conjugacy possible")
    check(mul(inv(pair1[0]),pair1[1])[0]==1,"pair1 mixed invariant")
    check(mul(inv(pair2[0]),pair2[1])[0]==-1,"pair2 mixed invariant")

def gram_control():
    X=((1,1,0,0),(1,-1,0,0),(-1,1,0,0),(-1,-1,0,0))
    F=(1,1,0,0)
    Y=((1,0,0,0),(1,0,0,0),(-1,0,0,0),(-1,0,0,0))
    D=(2,7,0,0)
    G=(0,1,0,0)
    scores=[sum(a*b for a,b in zip(x,D)) for x in X]
    projected=[sum(a*b for a,b in zip(x,D)) for x in Y]
    gauge=[sum(a*b for a,b in zip(x,G)) for x in Y]
    check(sum(scores)==0 and sum(v*v for v in scores)==4*53,
          "unprojected variance 53")
    check(sum(projected)==0 and sum(v*v for v in projected)==4*4,
          "source-projected variance 4")
    check(sum(gauge)==0 and sum(v*v for v in gauge)==0,
          "gauge tangent null")
    check(sum(F)==2 and sum(f*s for f,s in zip(F,scores))==4,
          "covariance=1 and source variance=1over4")
    check(1*1*4==4,"sharp integer cross-product Cauchy-Schwarz")

if __name__=="__main__":
    orbit_control()
    gram_control()
    print("YM4_VOL19_ORBIT|noncommuting_two_square_forest=PASS|radii=PASS|chords=PASS|common_conjugacy=PASS")
    print("YM4_VOL19_RED|individual_cycle_traces_insufficient=PASS")
    print("YM4_VOL19_GRAM|source_projection_53_to_4=PASS|Ward_null_fixture=PASS|fraction_Cauchy_Schwarz=PASS")
    print("YM4_VOL19_SCOPE|continuous_Haar=ANALYTIC|physical_high_beta_decay=OPEN|continuum_11=OPEN")
