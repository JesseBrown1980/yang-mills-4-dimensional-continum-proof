from s_lane import *
import sys
def dcrit():
    lo,hi=D('0.04'),D('0.06')
    for _ in range(80):
        m=(lo+hi)/2; c=cfun(m)
        if c is not None and c<1: lo=m
        else: hi=m
    return lo
dc=dcrit(); print('delta_crit=%.12f'%dc)
for d in ('0.049','0.05'): print('c(%s)=%.7f'%(d,cfun(D(d))))
dcm = (dc*10**9).to_integral_value(rounding='ROUND_FLOOR')/D(10**9)
print('delta_crit^- on 1e-9 grid', dcm)
for name,pts in (('crude',[1903,1904,1905]),('free',[2075,2076]),('meas',[2075,2076])):
    for j in pts:
        e=eps6(Fr(j,100000)); a=least_a(e,KAP,HEADS[name])
        print('C0',name,j,'MET' if a is not None else 'NOT_MET', a)
for name,pts in (('crude',[1368,1369,1370]),('free',[1959,1960]),('meas',[1958,1959,1960])):
    for j in pts:
        r=C0(Fr(j,100000),HEADS[name])
        ok = r is not None and r[0]<dcm
        print('IND',name,j,'MET' if ok else 'NOT_MET', None if r is None else '%.9e'%r[0], flush=True)
