//! Independent YM4-04C E0 4D b=2 geometry, link incidence and closed n=4 census.
//! Native Rust 1.81; no floating-point numbers, unsafe, JSON or dynamic code.
#![forbid(unsafe_code)]
#![deny(clippy::float_arithmetic, clippy::float_cmp, clippy::cast_precision_loss)]
use std::collections::BTreeSet;

const PAIRS: [(usize,usize);6]=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)];

struct CubicFour {
    n:usize,
    sites:usize,
    spans:[usize;4],
    kinds:Vec<u8>,
    faces:Vec<[usize;4]>,
    off:Vec<Vec<usize>>,
    incident:Vec<Vec<usize>>,
}
impl CubicFour {
    fn new(n:usize)->Self{
        assert!(n>=8 && n%2==0);
        let sites=n*n*n*n;
        let spans=[n*n*n,n*n,n,1];
        let mut kinds=vec![0u8;4*sites];
        for v in 0..sites{
            let mut parity=0u8;
            for (axis,span) in spans.iter().enumerate(){
                if (v/span)%n%2==1 {parity |= 1<<axis;}
            }
            for axis in 0..4 {
                kinds[4*v+axis]=(parity & !(1<<axis)).count_ones() as u8;
            }
        }
        let mut faces=Vec::with_capacity(6*sites);
        let mut off=Vec::with_capacity(6*sites);
        let mut incident=vec![Vec::<usize>::new();4*sites];
        for v in 0..sites{
            for &(a,b) in &PAIRS {
                let edge=[4*v+a,4*Self::advance(v,a,n,&spans)+b,
                          4*Self::advance(v,b,n,&spans)+a,4*v+b];
                let unique:BTreeSet<_>=edge.iter().copied().collect();
                assert_eq!(unique.len(),4);
                let support=edge.iter().copied().filter(|&e|kinds[e]>0).collect::<Vec<_>>();
                let id=faces.len();
                for &e in &edge{incident[e].push(id);}
                faces.push(edge);
                off.push(support);
            }
        }
        Self{n,sites,spans,kinds,faces,off,incident}
    }
    fn advance(v:usize,axis:usize,n:usize,spans:&[usize;4])->usize{
        let stride=spans[axis];
        if (v/stride)%n +1<n{v+stride}else{v-(n-1)*stride}
    }
    fn site(&self,coords:[usize;4])->usize{
        coords.into_iter().fold(0usize,|acc,x|{assert!(x<self.n);acc*self.n+x})
    }
    fn adjacent(&self,f:usize)->BTreeSet<usize>{
        let mut res=BTreeSet::new();
        for &edge in &self.off[f]{
            res.extend(self.incident[edge].iter().copied());
        }
        res.remove(&f);
        res
    }
    fn closed(&self,subset:&[usize])->bool{
        let mut incidence=std::collections::BTreeMap::<usize,usize>::new();
        for &f in subset{
            for &e in &self.off[f]{*incidence.entry(e).or_default()+=1;}
        }
        !incidence.is_empty() && incidence.values().all(|&num|num>=2)
    }
    fn closed4(&self,coords:[usize;4])->(usize,usize){
        let root=4*self.site(coords);
        assert_eq!(self.incident[root].len(),6);
        let mut prev=self.incident[root].iter().map(|&f|vec![f]).collect::<BTreeSet<_>>();
        for size in 2..=4{
            let mut next=BTreeSet::new();
            for set in &prev{
                for &f in set{
                    for nf in self.adjacent(f){
                        if set.binary_search(&nf).is_err(){
                            let mut new=set.clone();
                            new.push(nf);
                            new.sort_unstable();
                            assert_eq!(new.len(),size);
                            next.insert(new);
                        }
                    }
                }
            }
            prev=next;
        }
        (prev.iter().filter(|set|self.closed(set)).count(),prev.len())
    }
    fn verify(&self)->String{
        assert_eq!(self.faces.len(),6*self.sites);
        let counts=(0..4).map(|k|self.kinds.iter().filter(|&&x|x==k).count()).collect::<Vec<_>>();
        assert_eq!(counts,[self.sites/2,3*self.sites/2,3*self.sites/2,self.sites/2]);
        assert!(self.incident.iter().all(|r|r.len()==6));
        let quarters=self.off.iter().filter(|a|a.len()==2).count();
        let full=self.off.iter().filter(|a|a.len()==4).count();
        assert_eq!(quarters*4,6*self.sites);
        assert_eq!(quarters+full,self.faces.len());
        let mut degrees=[0usize;2];
        for f in 0..self.faces.len(){
            let deg=self.adjacent(f).len();
            assert_eq!(deg,5*self.off[f].len());
            match deg{
                10=>degrees[0]+=1,
                20=>degrees[1]+=1,
                _=>panic!("incorrect off-link adjacency degree"),
            }
        }
        assert_eq!(degrees,[quarters,full]);
        let v0=self.site([0,0,0,0]);
        let mid=Self::advance(v0,0,self.n,&self.spans);
        let e0=4*v0;
        let e1=4*mid;
        assert_eq!(self.kinds[e0],0);
        assert_eq!(self.kinds[e1],0);
        let mut w=BTreeSet::new();
        for &f in &self.incident[e0]{w.extend(self.off[f].iter().copied());}
        assert_eq!(w.len(),12);
        assert!(w.iter().all(|&e|self.kinds[e]==1));
        let mut wp=BTreeSet::new();
        for axis in 0..4{
            let stride=self.spans[axis];
            let v=if (mid/stride)%self.n >0 {mid-stride}else{mid+(self.n-1)*stride};
            for e in [4*v+axis,4*mid+axis]{
                if self.kinds[e]>0{wp.insert(e);}
            }
        }
        assert_eq!(wp.len(),6);
        assert!(wp.is_subset(&w));
        let a=self.closed4([0,1,0,0]);
        let b=self.closed4([0,1,1,0]);
        let c=self.closed4([0,1,1,1]);
        assert_eq!((a.0,b.0,c.0),(1,0,0));
        format!("YM4_04C_E0_RUST|N={}|links={}|plaquettes={}|link_classes={},{},{},{}|quarter_faces={quarters}|four_off_faces={full}|degrees=10,20|W=12|Wprime=6|closed_n4=1,0,0|json=0",
          self.n,self.kinds.len(),self.faces.len(),counts[0],counts[1],counts[2],counts[3])
    }
}
fn main(){
    for n in [8,10]{
        println!("{}",CubicFour::new(n).verify());
    }
    println!("YM4_04C_E0_RUST_RESULT|PASS|independent_algorithm=YES|C03_n12=OPEN|json=0");
}
#[cfg(test)]
mod tests{
    use super::*;
    #[test]fn low_lattice(){
        let x=CubicFour::new(8);
        assert_eq!(x.closed4([0,1,0,0]).0,1);
    }
    #[test]fn off_link_incidence(){
        let x=CubicFour::new(8);
        assert_eq!(x.adjacent(0).len(),10);
    }
}
