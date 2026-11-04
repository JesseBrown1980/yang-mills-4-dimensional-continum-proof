import time,sys
t=time.perf_counter_ns()
m=[[(i*j)%97 for j in range(97)] for i in range(97)]
c=[i%97 for i in range(1000)]
x=0
for i in range(2000000):
    x=m[m[x][c[i%1000]]][c[(i+1)%1000]]
print(sys.version.split()[0],x,(time.perf_counter_ns()-t)//10**6,"ms")
