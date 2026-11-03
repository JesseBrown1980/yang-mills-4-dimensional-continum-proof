# The 12-face spheres through the script's own expectation with Q8 (every link covered twice, so degree 2 <= 3). Fresh code path relative to my word-gluing evaluator.
import ast,itertools,math,sys
src=open("C:/tmp/opus55/attack-4d-20261103/replay/test_subgroup_designs_4d.py",encoding="utf8").read()
ns={"itertools":itertools,"math":math,"SABOTAGE":"","FAILS":[],"sys":sys}
a=src.index("# ---- Exact rationals as reduced integer pairs."); b=src.index("# ---- 1. Design strength")
exec(compile(src[a:b],"r","exec"),ns)
ns["check"]=lambda name,ok:None
a=src.index("# ---- 2. Group tables"); b=src.index("# ---- 4. Moments of X")
exec(compile(src[a:b].replace('print("GROUP_TABLE','("GROUP_TABLE'),"g","exec"),ns)
Lattice,expectation,Q8,text=ns["Lattice"],ns["expectation"],ns["Q8"],ns["text"]
lat=Lattice(4,0)
classes=[ast.literal_eval(l) for l in open("classes_d4_F12.txt",encoding="utf8")]
def links(f):
    return {l for l,_ in lat.plaquette(*f)}
spheres=[k for k in classes if len(k)==12 and max(sum(1 for f in k if l in links(f)) for f in k for l in links(f))==2]
print("SPHERES|count=%d|json=0"%len(spheres))
vals={}
for k in spheres:
    v=expectation(lat,[lat.plaquette(*f) for f in k],Q8)
    vals[v]=vals.get(v,0)+1
    sys.stdout.flush()
print("SPHERES_Q8_VALUES|%s|expected=1/4194304|json=0"%";".join("%s x%d"%(text(a),b) for a,b in vals.items()))
