# Float sanity of R12 only (scratch; not an engine, not evidence)
import numpy as np, sys
L=int(sys.argv[1])
k=2*np.pi*np.arange(L)/L
kh=4*np.sin(k/2)**2
K=kh[:,None,None,None]+kh[None,:,None,None]+kh[None,None,:,None]+kh[None,None,None,:]
K[0,0,0,0]=np.inf
G=np.real(np.fft.ifftn(1.0/K))  # (1/N) sum e^{ikx}/khat^2, zero mode removed
def V(n):
    hor=[((j,0),1) for j in range(n)]+[((j,n),-1) for j in range(n)]
    ver=[((n,j),1) for j in range(n)]+[((0,j),-1) for j in range(n)]
    tot=0.0
    for links in (hor,ver):
        for (a,s) in links:
            for (b,t) in links:
                tot+=s*t*G[(a[0]-b[0])%L,(a[1]-b[1])%L,0,0]
    return tot
v1=V(1); print(L, 'V11*4=',4*v1/2, 'r1=',V(2)/v1, 'r2=',V(4)/v1, 'r2/r1=',V(4)/V(2))
