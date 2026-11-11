#!/usr/bin/env python3
"""Exact C03 Fuss-Catalan counting gaps from frozen n4..12 coefficients.
Arithmetic is integer-only and all brackets are strict cross-products.
"""
from math import comb

COUNTS={
    1:(1,0,12,0,32,32,304,284,2326),
    2:(0,0,12,0,12,12,240,244,1640),
    3:(0,0,12,0,0,0,216,228,1242),
}
def f20(n):
    assert n>=1
    v=comb(20*n,n)
    assert v%(19*n+1)==0
    return v//(19*n+1)
def run():
    for n,lo,hi in (
        (8,10_900_000_000,11_000_000_000),
        (10,2_310_000_000_000,2_330_000_000_000),
        (12,649_000_000_000_000,650_000_000_000_000),
    ):
        v=max(row[n-4] for row in COUNTS.values())
        gap_num=6*f20(n)
        assert lo*v<gap_num<hi*v
        print("YM4_04C_C03_GAP|n="+str(n)+"|numerator="+str(gap_num)+
              "|denominator="+str(v)+"|lower="+str(lo)+
              "|upper="+str(hi)+"|strict=PASS|json=0")
    a=f20(10);b=f20(8);c=f20(12)
    assert 201684*b < 100*a
    assert 100*a<201685*b
    assert 214177*a < 100*c
    assert 100*c<214178*a
    assert 304*2==32*19
    assert 2326*152==304*1163
    print("YM4_04C_C03_GROWTH|n10_over_n8=19/2|n12_over_n10=1163/152|F20_n10_over_n8_in=(2016.84,2016.85)|F20_n12_over_n10_in=(2141.77,2141.78)|json=0")
    print("YM4_04C_C03_GAP_RESULT|PASS|all_arithmetic=EXACT_INTEGER|refined_C03=REPRODUCTION|weak_coupling=OPEN|r9_runs=0|json=0")
if __name__=="__main__":
    run()
