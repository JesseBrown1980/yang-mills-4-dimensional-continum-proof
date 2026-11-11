#!/usr/bin/env python3
"""YM4-04C E0 4D b=2 coarse-line/off-link geometry and exact n=4 closed counts.
The first 42 HBP prediction rows are immutable. This computes E0 only.
No floats, fractions, decimal, true division, non-integer exponent or JSON.
"""
import argparse
from math import comb

PAIRS=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))

class Lattice:
    def __init__(self,n):
        assert n>=8 and n%2==0
        self.n=n
        self.sites=n*n*n*n
        self.strides=(n*n*n,n*n,n,1)
        self.links=4*self.sites
        self.link_class=bytearray(self.links)
        for s in range(self.sites):
            oddmask=0
            for axis in range(4):
                if (s//self.strides[axis])%n%2:
                    oddmask|=1<<axis
            for axis in range(4):
                self.link_class[4*s+axis]=(oddmask & ~(1<<axis)).bit_count()
        self.link_to_faces=[[] for _ in range(self.links)]
        self.face_edges=[]
        self.face_off=[]
        for s in range(self.sites):
            for u,v in PAIRS:
                ps=(4*s+u,4*self.step(s,u)+v,4*self.step(s,v)+u,4*s+v)
                assert len(set(ps))==4
                self.face_edges.append(ps)
                off=tuple(e for e in ps if self.link_class[e]>0)
                self.face_off.append(off)
                fid=len(self.face_edges)-1
                for e in ps:
                    self.link_to_faces[e].append(fid)
        assert len(self.face_edges)==6*self.sites

    def step(self,s,axis):
        span=self.strides[axis]
        val=(s//span)%self.n
        return s+span if val+1<self.n else s-(self.n-1)*span

    def site(self, coords):
        s=0
        for coord in coords:
            assert 0<=coord<self.n
            s=s*self.n+coord
        return s

    def neighbors(self,p):
        adjacent=set()
        for e in self.face_off[p]:
            adjacent.update(self.link_to_faces[e])
        adjacent.discard(p)
        return adjacent

    def closed_set(self,ids):
        degrees={}
        for p in ids:
            for e in self.face_off[p]:
                degrees[e]=degrees.get(e,0)+1
        return bool(degrees) and all(x>=2 for x in degrees.values())

    def closed_four(self,coords):
        w=4*self.site(coords)
        initial={frozenset((p,)) for p in self.link_to_faces[w]}
        assert len(initial)==6
        previous=initial
        for size in (2,3,4):
            augmented=set()
            for subset in previous:
                for p in subset:
                    for nbr in self.neighbors(p):
                        if nbr not in subset:
                            augmented.add(subset | frozenset((nbr,)))
            previous=augmented
            assert all(len(k)==size for k in previous)
        candidates=[p for p in previous if self.closed_set(p)]
        return len(candidates),len(previous)

def run_one(n,sabotage=None):
    g=Lattice(n)
    classes=[g.link_class.count(k) for k in range(4)]
    qcount=sum(len(off)==2 for off in g.face_off)
    fourcount=sum(len(off)==4 for off in g.face_off)
    assert qcount+fourcount==6*g.sites
    assert qcount*4==6*g.sites,"incorrect fine quarter count"
    assert classes==[g.sites//2,3*g.sites//2,3*g.sites//2,g.sites//2]
    assert all(len(fs)==6 for fs in g.link_to_faces)
    assert all(len(off) in (2,4) for off in g.face_off)
    degree_counts={10:0,20:0}
    for p,off in enumerate(g.face_off):
        degree=len(g.neighbors(p))
        expected=5*len(off)
        if sabotage=="degree_19" and n==8 and expected==20:
            expected=19
        assert degree==expected,"E0_FAIL: off-link adjacency degree differs from 5 times its support"
        degree_counts[degree]+=1
    assert degree_counts[10]==qcount and degree_counts[20]==fourcount

    zero=g.site((0,0,0,0))
    e0=4*zero
    e1=4*g.step(zero,0)
    assert g.link_class[e0]==0 and g.link_class[e1]==0
    faces0=g.link_to_faces[e0]
    faces1=g.link_to_faces[e1]
    assert all(len(g.face_off[p])==2 for p in faces0+faces1)
    W0={e for p in faces0 for e in g.face_off[p]}
    assert len(W0)==12 and all(g.link_class[e]==1 for e in W0)
    middle=g.step(zero,0)
    incoming={4*g.step(middle,axis)+axis for axis in ()} # explicitly empty
    for axis in range(4):
        behind=middle
        span=g.strides[axis]
        c=(middle//span)%n
        behind=middle-span if c else middle+(n-1)*span
        incoming.add(4*behind+axis)
    Wprime={e for e in incoming.union({4*middle+axis for axis in range(4)}) if g.link_class[e]>0}
    assert len(Wprime)==6 and Wprime.issubset(W0)
    assert all(g.link_class[e]==1 for e in Wprime)
    assert sabotage!="quarter_wrong","E0_FAIL: planted quarter-count corruption"
    c4={}
    candidate_sizes={}
    for kind,coords in (("class1",(0,1,0,0)),("class2",(0,1,1,0)),("class3",(0,1,1,1))):
        want={"class1":1,"class2":0,"class3":0}[kind]
        got,examined=g.closed_four(coords)
        if sabotage=="closed_class2" and kind=="class2":
            want=1
        assert got==want,"E0_FAIL: closed four-polymer count for "+kind
        c4[kind]=got
        candidate_sizes[kind]=examined
    return ("YM4_04C_E0|N="+str(n)
        +"|sites="+str(g.sites)
        +"|links="+str(g.links)
        +"|plaquettes="+str(len(g.face_edges))
        +"|line_links="+str(classes[0])
        +"|off_classes="+",".join(str(z) for z in classes[1:])
        +"|quarter_faces="+str(qcount)
        +"|four_off_faces="+str(fourcount)
        +"|adjacency_degrees=10,20"
        +"|line_W=12|middle_Wprime=6"
        +"|closed_n4_class1,2,3="+",".join(str(c4[z]) for z in ("class1","class2","class3"))
        +"|n4_candidate_count="+",".join(str(candidate_sizes[z]) for z in ("class1","class2","class3"))
        +"|source=RECALCULATED|prefreeze=CROSS_READ|json=0")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--sabotage",choices=["degree_19","quarter_wrong","closed_class2"])
    args=parser.parse_args()
    print("YM4_04C_E0_START|frozen_sha256=c74e6388295a6309674268dd18deba3728a4eb627a1530c42054182b2fadc404|source=INDEPENDENT_IMPLEMENTATION|whole_engine=NO|json=0")
    for n in (8,10):
        print(run_one(n,args.sabotage))
    print("YM4_04C_E0_RESULT|PASS|lattices=8,10|geometry=EXHAUSTIVE|n4_closed=EXHAUSTIVE|n6_to_n12=NOT_DONE|C03_n12=OPEN|r9_runs=0|json=0")

if __name__=="__main__":
    main()
