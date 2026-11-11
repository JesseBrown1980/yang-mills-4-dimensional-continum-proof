//! Independent native Rust 1.81 exhaustive YM4-04C E1/C03 rooted polymer census.
//! Frozen C03 counts are checked, not derived from the Python implementation.
//! Exact face ID equality is used after hashing: no symmetry divisions or
//! probabilistic de-duplication. Every closed state is materialized for SHA-256.
#![forbid(unsafe_code)]
#![deny(clippy::float_arithmetic,clippy::float_cmp,clippy::cast_precision_loss)]
#[path="e1_c03_sha256.rs"] mod sha256;
use std::collections::HashSet;
use std::hash::{BuildHasherDefault,Hasher};
use std::fmt::Write;

const PLANES:[(usize,usize);6]=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)];
const PRED:[[usize;9];3]=[
    [1,0,12,0,32,32,304,284,2326],
    [0,0,12,0,12,12,240,244,1640],
    [0,0,12,0,0,0,216,228,1242]
];
struct KeyHasher(u64);
impl Default for KeyHasher{
    fn default()->Self{Self(0xcbf29ce484222325)}
}
impl Hasher for KeyHasher{
    fn finish(&self)->u64{
        let mut x=self.0;
        x^=x>>33;
        x=x.wrapping_mul(0xff51afd7ed558ccd);
        x^=x>>33;
        x=x.wrapping_mul(0xc4ceb9fe1a85ec53);
        x^(x>>33)
    }
    fn write(&mut self,bytes:&[u8]){
        for &b in bytes{
            self.0^=u64::from(b);
            self.0=self.0.wrapping_mul(0x100000001b3);
        }
    }
    fn write_u32(&mut self,value:u32){
        self.0^=u64::from(value);
        self.0=self.0.wrapping_mul(0x100000001b3);
    }
}
type ExactSeen=HashSet<[u32;12],BuildHasherDefault<KeyHasher>>;
struct Geometry{
    side:usize,
    links:usize,
    classes:Vec<u8>,
    off:Vec<Vec<u32>>,
    incidence:Vec<Vec<u32>>,
}
impl Geometry{
    fn new(side:usize)->Self{
        assert!(side==8||side==12);
        let sites=side*side*side*side;
        let strides=[side*side*side,side*side,side,1];
        let links=4*sites;
        let mut classes=vec![0u8;links];
        for site in 0..sites{
            let parity=(0..4).fold(0u8,|acc,axis|{
                acc|(((site/strides[axis])%side%2) as u8)<<axis
            });
            for axis in 0..4{
                classes[4*site+axis]=(parity&!(1u8<<axis)).count_ones() as u8;
            }
        }
        let mut off=Vec::with_capacity(6*sites);
        let mut incidence=vec![Vec::<u32>::new();links];
        let mut full_counts=vec![0u8;links];
        for site in 0..sites{
            for &(a,b) in &PLANES{
                let sa=strides[a];let sb=strides[b];
                let va=if (site/sa)%side+1<side{site+sa}else{site-(side-1)*sa};
                let vb=if (site/sb)%side+1<side{site+sb}else{site-(side-1)*sb};
                let edges=[4*site+a,4*va+b,4*vb+a,4*site+b];
                assert_eq!(edges.iter().collect::<std::collections::BTreeSet<_>>().len(),4);
                let fid=off.len() as u32;
                let mut support=Vec::with_capacity(4);
                for e in edges{
                    full_counts[e]+=1;
                    if classes[e]!=0{
                        incidence[e].push(fid);
                        support.push(e as u32);
                    }
                }
                assert!(support.len()==2||support.len()==4);
                off.push(support);
            }
        }
        assert_eq!(off.len(),6*sites);
        assert!(full_counts.iter().all(|&count|count==6));
        let class_counts=(0..4).map(|k|classes.iter().filter(|&&v|v==k).count()).collect::<Vec<_>>();
        assert_eq!(class_counts,[sites/2,3*sites/2,3*sites/2,sites/2]);
        // Independently rebuild all 4D off-neighbourhoods: 10 or 20.
        for (f,support) in off.iter().enumerate(){
            let mut adjacent=std::collections::BTreeSet::new();
            for &e in support{
                adjacent.extend(incidence[e as usize].iter().copied());
            }
            adjacent.remove(&(f as u32));
            assert_eq!(adjacent.len(),5*support.len());
        }
        Self{side,links,classes,off,incidence}
    }
    fn root(&self,kind:usize)->usize{
        assert!((1..=3).contains(&kind));
        let mut coords=[0usize;4];
        for v in &mut coords[1..=kind]{*v=1;}
        let site=coords.iter().fold(0usize,|acc,&x|acc*self.side+x);
        4*site
    }
}
struct Counter<'a>{
    g:&'a Geometry,
    seen:ExactSeen,
    counts:[usize;13],
    levels:[usize;13],
    closed:Vec<Vec<u32>>,
}
impl<'a> Counter<'a>{
    fn new(g:&'a Geometry)->Self{
        Self{
            g,seen:HashSet::with_hasher(BuildHasherDefault::default()),
            counts:[0;13],levels:[0;13],closed:Vec::new(),
        }
    }
    fn visit(&mut self,state:&mut Vec<u32>){
        let key=std::array::from_fn(|index|{
            state.get(index).copied().unwrap_or(u32::MAX)
        });
        if !self.seen.insert(key){return;}
        let size=state.len();
        self.levels[size]+=1;
        let mut edges=Vec::with_capacity(4*size);
        for &face in state.iter(){
            edges.extend(self.g.off[face as usize].iter().copied());
        }
        edges.sort_unstable();
        let mut unique=Vec::with_capacity(edges.len());
        let mut single=None;
        let mut singles=0usize;
        let mut index=0usize;
        while index<edges.len(){
            let e=edges[index];
            let mut next=index+1;
            while next<edges.len()&&edges[next]==e{next+=1;}
            unique.push(e);
            if next==index+1{
                singles+=1;
                if single.is_none(){single=Some(e);}
            }
            index=next;
        }
        if singles==0{
            self.counts[size]+=1;
            self.closed.push(state.clone());
        }
        if size==12||singles>4*(12-size){return;}
        let candidates:Vec<u32>=if let Some(edge)=single{
            self.g.incidence[edge as usize].clone()
        }else{
            let mut choices=Vec::new();
            for e in unique{
                choices.extend(self.g.incidence[e as usize].iter().copied());
            }
            choices.sort_unstable();
            choices.dedup();
            choices
        };
        for candidate in candidates{
            if let Err(pos)=state.binary_search(&candidate){
                state.insert(pos,candidate);
                self.visit(state);
                state.remove(pos);
            }
        }
    }
    fn run(mut self,kind:usize)->String{
        assert_eq!(self.g.links,4*self.g.side*self.g.side*self.g.side*self.g.side);
        let root=self.g.root(kind);
        assert_eq!(usize::from(self.g.classes[root]),kind);
        let first=self.g.incidence[root].clone();
        assert_eq!(first.len(),6,"all six root faces are required");
        for face in first{
            self.visit(&mut vec![face]);
        }
        assert_eq!(&self.counts[4..=12],&PRED[kind-1]);
        self.closed.sort_unstable();
        let mut lines=String::new();
        for state in &self.closed{
            for (j,face) in state.iter().enumerate(){
                if j>0{lines.push(',');}
                write!(&mut lines,"{face}").expect("face ID serialization");
            }
            lines.push('\n');
        }
        let digest=sha256::hash_bytes(lines.as_bytes());
        let counts=self.counts[4..=12].iter().map(usize::to_string)
            .collect::<Vec<_>>().join(",");
        let levels=self.levels[1..=12].iter().map(usize::to_string)
            .collect::<Vec<_>>().join(",");
        format!("C03_RUST|N={}|class={kind}|counts_n4_to_n12={counts}|states_by_n={levels}|states_exact={}|closed_set_sha256={digest}|degree_off_10_20=YES|root_face_count=6|dedup=EXACT_SORTED_FACE_IDS|status=PASS|json=0",self.g.side,self.seen.len())
    }
}
fn main(){
    let args=std::env::args().collect::<Vec<_>>();
    let mut n=None;
    let mut kind=None;
    for window in args.windows(2){
        match window[0].as_str(){
            "--n"=>n=Some(window[1].parse::<usize>().expect("integer lattice side")),
            "--class"=>kind=Some(window[1].parse::<usize>().expect("integer off class")),
            _=>{},
        }
    }
    let n=n.expect("usage: --n 8|12 --class 1|2|3");
    let kind=kind.expect("missing off-link class");
    println!("YM4_04C_E1_C03_RUST|freeze_sha256=c74e6388295a6309674268dd18deba3728a4eb627a1530c42054182b2fadc404|full_finite_Geometry=YES|prefreeze=CROSS_READ|json=0");
    println!("{}",Counter::new(&Geometry::new(n)).run(kind));
    println!("YM4_04C_E1_C03_RUST_RESULT|PASS|n4_to_n12=EXHAUSTIVELY_RECOMPUTED|source_disjoint_from_Python=YES|r9_runs=0|json=0");
}
#[cfg(test)]
mod tests{
    use super::*;
    #[test]fn full_8_geometry(){
        let g=Geometry::new(8);
        assert_eq!(g.off.len(),24576);
        assert_eq!(g.links,16384);
    }
    #[test]fn exact_root_class(){
        let g=Geometry::new(8);
        for class in 1..=3 {
            assert_eq!(g.classes[g.root(class)],class as u8);
        }
    }
}