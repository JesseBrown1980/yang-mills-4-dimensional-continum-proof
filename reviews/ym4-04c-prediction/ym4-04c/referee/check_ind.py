src = open('check_headfree.py').read().split("for beta in [F(1,100), F(1,64)")[0]
exec(src)
# delta_crit by bisection on c(d)=1
lo, hi = D('0.049'), D('0.050')
for _ in range(60):
    mid = (lo+hi)/2
    c = c_of(mid)
    if c is not None and c < 1: lo = mid
    else: hi = mid
print('delta_crit ~', '%.8f'%lo)
dcrit = lo
for beta in [F(1958,100000), F(1959,100000), F(1960,100000), F(1961,100000)]:
    r = C0g(beta, Shf)
    print('headfree', beta, '%.6e'%r[0] if r else None, 'admissible(delta1<dcrit)=', bool(r and r[0] < dcrit), ' surrogate(<=49/1000)=', bool(r and r[0] <= D(49)/1000))
for beta in [F(1365,100000), F(1366,100000), F(1367,100000), F(1368,100000), F(1370,100000)]:
    r = C0g(beta, S)
    print('crude', beta, '%.6e'%r[0] if r else None, 'admissible=', bool(r and r[0] < dcrit), ' surrogate=', bool(r and r[0] <= D(49)/1000))
