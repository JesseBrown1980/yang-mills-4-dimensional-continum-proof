#!/usr/bin/env python3
"""YM4-04C E1/C03 independent closure-driven n<=12 exhaustive count.
Continuous 4D geometry is NOT assumed: exactly finite periodic 4D incidence.
No symmetry division, floating-point operations, JSON, or ignored partial states.
"""
import argparse
import hashlib

PAIRS=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
PRED={
    1:(1,0,12,0,32,32,304,284,2326),
    2:(0,0,12,0,12,12,240,244,1640),
    3:(0,0,12,0,0,0,216,228,1242),
}
def build(n):
    assert n in (8,12)
    sites=n*n*n*n
    strides=(n*n*n,n*n,n,1)
    classes=bytearray(4*sites)
    for v in range(sites):
        parity=0
        for axis,stride in enumerate(strides):
            if (v//stride)%n%2:parity|=1<<axis
        for axis in range(4):
            classes[4*v+axis]=(parity & ~(1<<axis)).bit_count()
    off=[]
    incidence=[[] for _ in range(4*sites)]
    all_face_counts=bytearray(4*sites)
    for v in range(sites):
        for a,b in PAIRS:
            sa=strides[a]; sb=strides[b]
            va=v+sa if (v//sa)%n+1<n else v-(n-1)*sa
            vb=v+sb if (v//sb)%n+1<n else v-(n-1)*sb
            edges=(4*v+a,4*va+b,4*vb+a,4*v+b)
            assert len(set(edges))==4
            fid=len(off)
            face_off=tuple(e for e in edges if classes[e]!=0)
            assert len(face_off) in (2,4)
            off.append(face_off)
            for e in edges:all_face_counts[e]+=1
            for e in face_off:incidence[e].append(fid)
    assert len(off)==6*sites
    assert all(v==6 for v in all_face_counts)
    assert [classes.count(c) for c in range(4)]==[
        sites//2,3*sites//2,3*sites//2,sites//2]
    # Rebuild the full off-link adjacency from the six incident faces of
    # each off link, checking Lemma 3.1 local degree without pre-supplied edges.
    for f,edges in enumerate(off):
        neighbors=set()
        for e in edges:neighbors.update(incidence[e])
        neighbors.discard(f)
        assert len(neighbors)==5*len(edges)
    return sites,classes,off,incidence

def class_root(n,c):
    coords=[0]+[1]*c+[0]*(3-c)
    v=0
    for value in coords:v=v*n+value
    return 4*v

def count(n,c,sabotage=None):
    sites,classes,off,incidence=build(n)
    root=class_root(n,c)
    assert classes[root]==c
    first=incidence[root][:]
    if sabotage=="missing_root_face":
        first.pop()
    assert len(first)==6,"C03_REJECT: six root plaquettes required"
    seen=set()
    counts=[0]*13
    levels=[0]*13
    closed=[]
    def visit(state):
        if state in seen:return
        seen.add(state)
        size=len(state)
        levels[size]+=1
        degree={}
        for f in state:
            for e in off[f]:degree[e]=degree.get(e,0)+1
        singles=sorted(e for e,value in degree.items() if value==1)
        if not singles:
            counts[size]+=1
            closed.append(state)
        remaining=12-size
        if remaining==0 or len(singles)>4*remaining:
            return
        if singles:
            # Completeness: every closed completion must cover this *one*
            # unmatched link by a new incident plaquette.
            choices=incidence[singles[0]]
        else:
            # Completeness: a proper connected extension of an already
            # closed state must use an off-link adjacent boundary face.
            choices=set()
            for e in degree:choices.update(incidence[e])
            if sabotage=="skip_closed_extensions":
                choices=()
        for f in choices:
            if f not in state:
                visit(tuple(sorted((*state,f))))
    for f in first:visit((f,))
    want=PRED[c]
    if sabotage=="wrong_frozen_n12":
        want=want[:8]+(want[8]+1,)
    got=tuple(counts[4:13])
    assert got==want,"C03_REJECT: refined closed-polymer counts disagree with freeze"
    digest=hashlib.sha256()
    for state in sorted(closed):
        digest.update((",".join(str(f) for f in state)+"\n").encode("ascii"))
    return ("C03|N="+str(n)+"|class="+str(c)
         +"|counts_n4_to_n12="+",".join(str(v) for v in got)
         +"|states_by_n="+",".join(str(v) for v in levels[1:13])
         +"|states_exact="+str(len(seen))
         +"|closed_set_sha256="+digest.hexdigest()
         +"|degree_off_10_20=YES|root_face_count=6"
         +"|dedup=EXACT_SORTED_FACE_IDS|status=PASS|json=0")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--n",type=int,required=True,choices=(8,12))
    parser.add_argument("--class",type=int,required=True,choices=(1,2,3))
    parser.add_argument("--sabotage",choices=(
        "missing_root_face","skip_closed_extensions","wrong_frozen_n12"))
    args=parser.parse_args()
    print("YM4_04C_E1_C03|freeze_sha256=c74e6388295a6309674268dd18deba3728a4eb627a1530c42054182b2fadc404|prefreeze=CROSS_READ|r9_runs=0|json=0",flush=True)
    print(count(args.n,getattr(args,"class"),args.sabotage),flush=True)
    print("YM4_04C_E1_C03_RESULT|PASS|n4_to_n12=EXHAUSTIVELY_RECOMPUTED|no_symmetry_division=YES|r9_runs=0|json=0",flush=True)
if __name__=="__main__":
    main()
