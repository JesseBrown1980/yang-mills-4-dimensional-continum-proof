from s_lane import *
from multiprocessing import Pool
def P10(b): return b**4/128-b**6/768+b**8/1536-467*b**10/2211840
def I_n(n,x):
    x=dec(x); s=D(0); t=(x/2)**n/D(__import__('math').factorial(n)); m=0
    while True:
        s+=t; t=t*(x/2)**2/((m+1)*(m+1+n)); m+=1
        if m>5 and t<D(10)**-85*s: return s
def job(q):
    out=[]
    for imax in (128,320):
        r=C0(q,HEADS['meas'],imax,'T')
        b=dec(q); p=P10(b); t2=I_n(2,b)/I_n(1,b); lead=2*t2**4
        out.append('C09 %s imax=%d T/P10=%.5e i=%d contain=%s |P10-2t2^4|/T=%.3e'%(q,imax,r[0]/p,r[2], abs(p-lead)<=r[0], abs(p-lead)/r[0]))
    return out
if __name__=='__main__':
    qs=[Fr(1,4000),Fr(1,2000),Fr(1,1000),Fr(1,700),Fr(1,100)]
    with Pool(4) as P:
        for o in P.map(job,qs):
            print('\n'.join(o),flush=True)
