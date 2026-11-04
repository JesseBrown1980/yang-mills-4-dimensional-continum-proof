# Runs a child at below-normal priority on Windows, with stdout to a file in binary mode. Integers only.
import subprocess, sys, time
out = sys.argv[1]
cmd = sys.argv[2:]
t0 = time.perf_counter_ns()
with open(out, "wb") as h:
    r = subprocess.run(cmd, stdout=h, stderr=subprocess.STDOUT, creationflags=0x00004000)
print("exit=%d ms=%d" % (r.returncode, (time.perf_counter_ns() - t0) // 10**6))
