import sys
sys.path.insert(0,'/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4-04c/polymer-norm')
from fractions import Fraction as Fr
import window2 as w
for j in (1901,1902,1903,1904):
    eps=w.up(w.eps6_upper(Fr(j,100000)))
    a=w.least_a(eps,w.KAPPA,{})
    print(j, 'MET' if a is not None else 'NOT_MET', None if a is None else float(a), flush=True)
