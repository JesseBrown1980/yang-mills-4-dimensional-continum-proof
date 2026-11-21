from fractions import Fraction as Fr
import sys, time
sys.path.insert(0, "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4-04c/polymer-norm")
from window2 import best_delta, CRUDE, FREE
t=time.time()
for beta in (Fr(1,100), Fr(1904,100000), Fr(1905,100000), Fr(1,64), Fr(1,50)):
    r = best_delta(beta, CRUDE)
    print("crude", beta, None if r is None else (float(r[0]), float(r[1]), r[2]), round(time.time()-t,1), flush=True)
for beta in (Fr(1,50), Fr(2075,100000), Fr(2076,100000)):
    r = best_delta(beta, FREE)
    print("free", beta, None if r is None else (float(r[0]), float(r[1]), r[2]), round(time.time()-t,1), flush=True)
