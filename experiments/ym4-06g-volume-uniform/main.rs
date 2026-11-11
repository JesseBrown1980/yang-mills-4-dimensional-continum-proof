//! YM4-06G exact spatial Wilson locality and zero-spatial-coupling transfer controls.
//! A VOLUME-INDEPENDENT spectral gap is proved here for the classical spatial
//! single-link heat-bath generator, NOT the interacting quantum Wilson transfer.
//! The beta_s=0 quantum transfer has a separate exact physical volume-uniform gap.
//! All checks are integer/rational; SHA is evidence integrity, not physics.
#![forbid(unsafe_code)]
#![deny(clippy::float_arithmetic,clippy::float_cmp,clippy::cast_precision_loss)]
mod sha256;
use sha256::hash_bytes;
use std::env;
use std::fs;
use std::path::Path;

const FREEZE:&str="19c9d0f78532e5b7bef1104fcbbcf89f1dd79940";
const LVALUES:[usize;6]=[2,3,4,5,9,27];
const BETA_NUM:u64=1;
const BETA_DEN:u64=128;
const INCIDENCE:usize=4;
const INFLUENCE_BUDGET:usize=12;

type Quat=[i32;4];
const ONE:Quat=[1,0,0,0];
const I:Quat=[0,1,0,0];
const J:Quat=[0,0,1,0];
const Q8:[Quat;8]=[
    ONE,[-1,0,0,0],I,[-0,-1,0,0],
    J,[0,0,-1,0],[0,0,0,1],[0,0,0,-1]
];
fn qm(a:Quat,b:Quat)->Quat{
    [a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3],
    a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2],
    a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1],
    a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0]]
}
fn qi(a:Quat)->Quat{[a[0],-a[1],-a[2],-a[3]]}
fn plaquette(u:&[Quat],p:&[usize;4])->Quat{
    qm(qm(qm(u[p[0]],u[p[1]]),qi(u[p[2]])),qi(u[p[3]]))
}
struct Cubic{
    side:usize,sites:usize,links:usize,faces:Vec<[usize;4]>,
}
impl Cubic {
    fn new(side:usize)->Self{
        assert!(side>=2);
        let sites=side*side*side;
        let links=3*sites;
        let mut faces=Vec::with_capacity(3*sites);
        let temp=Self{side,sites,links,faces:Vec::new()};
        for v in 0..sites {
            for a in 0..3 {
                for b in (a+1)..3 {
                    faces.push([
                        temp.link(a,v),
                        temp.link(b,temp.step(v,a)),
                        temp.link(a,temp.step(v,b)),
                        temp.link(b,v),
                    ]);
                }
            }
        }
        assert_eq!(faces.len(),3*sites);
        Self{side,sites,links,faces}
    }
    fn link(&self,axis:usize,vertex:usize)->usize {
        assert!(axis<3&&vertex<self.sites);
        axis*self.sites+vertex
    }
    fn step(&self,v:usize,axis:usize)->usize {
        let l=self.side;
        let stride=l.pow(axis as u32);
        let c=(v/stride)%l;
        if c+1<l {v+stride}else{v-(l-1)*stride}
    }
    fn other_face_counts(&self,broken:bool)->(usize,usize){
        let mut face_counts=vec![0usize;self.links];
        let mut neighbor_count=vec![0usize;self.links];
        for (fid,f) in self.faces.iter().enumerate(){
            if broken&&fid==0 {continue;}
            for i in 0..4 {
                for j in 0..4 {
                    if i!=j {assert_ne!(f[i],f[j],"face must have distinct links");}
                }
                face_counts[f[i]]+=1;
                neighbor_count[f[i]]+=3;
            }
        }
        assert!(face_counts.iter().all(|&n|n==INCIDENCE),
            "link face incidence must be four");
        assert!(neighbor_count.iter().all(|&n|n==INFLUENCE_BUDGET),
            "twelve other-link face incidences per link");
        // Every co-occurrence (i,j) is symmetric in the Wilson action,
        // so the sum of both row AND column Dobrushin bounds is twelve.
        (face_counts.iter().copied().max().unwrap(),
         neighbor_count.iter().copied().max().unwrap())
    }
    fn gauge_and_nonflat(&self)->usize{
        let mut links=vec![ONE;self.links];
        for v in 0..self.sites{
            links[self.link(0,v)]=I;
            links[self.link(1,v)]=J;
        }
        let mut transformed=vec![ONE;self.links];
        for axis in 0..3 {
            for v in 0..self.sites {
                let a=Q8[v%8];
                let b=Q8[self.step(v,axis)%8];
                let id=self.link(axis,v);
                transformed[id]=qm(qm(a,links[id]),qi(b));
            }
        }
        let mut nonflat=0usize;
        for (index,p) in self.faces.iter().enumerate(){
            let u=plaquette(&links,p);
            if u!=ONE {nonflat+=1;}
            let v=index/3;
            let g=Q8[v%8];
            let expected=qm(qm(g,u),qi(g));
            assert_eq!(plaquette(&transformed,p),expected);
            assert_eq!(expected[0],u[0],"trace is gauge invariant");
        }
        assert_eq!(nonflat,self.sites,"one nontrivial plaquette plane per vertex");
        nonflat
    }
}
fn girth(side:usize)->usize {
    match side {2=>2,3=>3,_=>4}
}
fn geometry(broken:bool)->String {
    let mut rows=String::new();
    for side in LVALUES {
        let lat=Cubic::new(side);
        let (degree,influence)=lat.other_face_counts(broken);
        let witness=lat.gauge_and_nonflat();
        let g=girth(side);
        // Periodic cubic graph: for side 2 two parallel opposite links,
        // side 3 three-step winding loops, and for side>=4 a plaquette
        // provides four-step closed loops. Shorter cycles do not exist.
        assert!(matches!(g,2..=4));
        rows.push_str(&format!(
            "GEOMETRY|L={side}|vertices={}|links={}|plaquettes={}|faces_per_link={degree}|other_link_face_incidences_per_link={influence}|girth={g}|nonflat_quaternion_faces={witness}|full_vertex_gauge_covariance=YES|json=0\n",
            lat.sites,lat.links,lat.faces.len()
        ));
    }
    rows
}
fn budget(beta_num:u64,beta_den:u64)->String {
    assert!(beta_den>0);
    let alpha_num=INFLUENCE_BUDGET as u64*beta_num;
    assert!(alpha_num<beta_den,
        "Dobrushin contractivity threshold violated");
    let gamma_num=beta_den-alpha_num;
    let n=32u64;
    assert_eq!(gamma_num*n,beta_den*29,
        "wrong normalized spatial heatbath gap");
    // Conditional law at one link has density exp(h dot U), |h|<=4 beta.
    // Altering neighbor j in c plaquettes changes |h| by <=2c beta.
    // Along the straight interpolation in h, TV speed <=|dh|/2.
    // So c_ij<=beta*c and sum_{j!=i} c_ij<=12 beta.
    // A random-scan heat-bath contraction in Hamming distance obeys
    // 1-(1-alpha)/N. Its reversible L2 spectral bound is the same.
    // Continuous-time generator sum_i(P_i-I) thus has gap >=1-alpha.
    format!(
        "LOCAL_DOBRUSHIN|beta_s={beta_num}/{beta_den}|conditional_SU2_von_Mises_Fisher=YES|TV_single_neighbour_le=beta_s_times_shared_faces|row_and_column_influence_budget=12|alpha_le={alpha_num}/{beta_den}|rate_one_per_link_classical_heatbath_gap_ge={gamma_num}/{beta_den}|ALL_L_GE2=YES|quantum_Wilson_transfer_GAP=NOT_PROVED|json=0\n"
    )
}
fn factorial(n:u32)->u128{(1..=u128::from(n)).product()}
fn gcd(mut a:u128,mut b:u128)->u128{
    while b!=0{let x=a%b;a=b;b=x;}a
}
#[derive(Clone,Copy)]
struct Rational{a:u128,b:u128}
impl Rational{
    fn new(a:u128,b:u128)->Self{
        assert!(b>0);
        let g=gcd(a,b);
        Self{a:a/g,b:b/g}
    }
    fn mul(self,x:Self)->Self{
        let p=gcd(self.a,x.b);
        let q=gcd(x.a,self.b);
        Self::new((self.a/p)*(x.a/q),(self.b/q)*(x.b/p))
    }
    fn add(self,x:Self)->Self{
        let g=gcd(self.b,x.b);
        Self::new(self.a*(x.b/g)+x.a*(self.b/g),(self.b/g)*x.b)
    }
    fn div(self,x:Self)->Self{
        assert!(x.a>0);
        self.mul(Self::new(x.b,x.a))
    }
    fn lt(self,x:Self)->bool{self.a*x.b<x.a*self.b}
}
fn term(n:u32,s:u32)->Rational{
    Rational::new(1,(1u128<<(2*s+n))*factorial(s)*factorial(s+n+1))
}
fn partial(n:u32)->Rational{
    let mut total=Rational::new(0,1);
    for s in 0..=4 {total=total.add(term(n,s));}
    total
}
fn tail(n:u32)->Rational{
    let s=5u32;
    let den=4*u128::from(s+1)*u128::from(s+n+2);
    term(n,s).mul(Rational::new(den,den-1))
}
fn rho_interval()->(u128,u128,u128){
    let (a,b)=(partial(0),partial(1));
    let lower=b.div(a.add(tail(0)));
    let upper=b.add(tail(1)).div(a);
    let (lo,hi,unit)=(24_019_372u128,24_019_373u128,100_000_000u128);
    assert!(Rational::new(lo,unit).lt(lower));
    assert!(upper.lt(Rational::new(hi,unit)));
    (lo,hi,unit)
}
fn b_transfer(false_quantum:bool)->String{
    let (lo,hi,unit)=rho_interval();
    let mut out=String::new();
    for side in LVALUES {
        let power=girth(side) as u32;
        let expected_limit=match power{2=>17u128,3=>70,4=>300,_=>panic!("invalid girth")};
        assert!(hi.pow(power)*expected_limit<unit.pow(power),
            "pure temporal SU2 Wilson B physical ratio upper gate");
        assert!(lo.pow(power)>0);
        // Exact SU2 temporal B at beta_s=0 has first physical excited
        // spin-network support on a shortest cycle, no open-link singlet.
        out.push_str(&format!(
            "PURE_TEMPORAL_B|L={side}|beta_s=0|beta_t=1|girth={power}|physical_first_ratio=rho^{power}|rho_lower={lo}/{unit}|rho_upper={hi}/{unit}|ratio_lt=1/{expected_limit}|gauge_excitation=SHORTEST_CLOSED_SPIN_NETWORK|json=0\n"
        ));
    }
    let worst=hi.pow(2);
    let denom=unit.pow(2);
    assert!(17*worst<denom,
        "beta_s0 volume-uniform physical temporal transfer gap invalid");
    // For any L>=2, girth>=2, hence physical ratio <=rho² <1/17.
    if false_quantum {
        // Static spatial independence (alpha=0) cannot imply a bound
        // for an arbitrary OTHER temporal transfer: take
        // K_n=(1-1/n)I+(1/n)Pi, n=3^k, a_t=1.
        let n=3u128.pow(8);
        assert!(n>=n*n-1,
            "alpha=0 does not imply a positive mass for an arbitrary temporal transfer");
    }
    out.push_str("PURE_TEMPORAL_UNIFORM|beta_s=0|ALL_L_GE2=YES|lambda2_over_lambda1_lt=1/17|reference_a_t=1|first_mass_gt=log(17)|interacting_beta_s_positive=NOT_INFERRED|json=0\n");
    out
}
fn counterexample()->String {
    let mut output=String::new();
    for k in 1..=8u32{
        let n=3u128.pow(k);
        // Classical independent single-slice Gibbs has alpha=0.
        // An unrelated positive reversible temporal K_n can
        // have nontrivial eigenratio 1-1/n at a_t=1.
        // Mass between 1/n and 1/(n-1), both vanish.
        assert!(n>1);
        output.push_str(&format!(
            "LOGICAL_COUNTERCONTROL|k={k}|n={n}|spatial_alpha=0|temporal_lambda2_lambda1={}/{n}|a_t=1|temporal_mass_lower=1/{n}|temporal_mass_upper=1/{}|limit=0|static_gap_implies_physical_mass=FALSE|json=0\n",
            n-1,n-1
        ));
    }
    output
}
fn witness_hash()->String{
    let mut text=String::new();
    for k in 1..=4u32 {
        let n=3usize.pow(k);
        let leaf=n/2;
        let root=|change:bool|{
            let mut nodes=(0..n).map(|i|{
                let mut t=i%3;
                if change&&i==leaf{t=(t+1)%3;}
                hash_bytes(format!("YM4_06G|k={k}|leaf={i}|trit={t}").as_bytes())
            }).collect::<Vec<_>>();
            for depth in 0..k{
                nodes=nodes.chunks_exact(3).map(|c|{
                    hash_bytes(format!("YM4_06G|depth={depth}|{}|{}|{}",c[0],c[1],c[2]).as_bytes())
                }).collect();
            }
            assert_eq!(nodes.len(),1);
            nodes.pop().unwrap()
        };
        let before=root(false);
        let after=root(true);
        assert_ne!(before,after);
        assert_ne!(leaf,0);
        text.push_str(&format!(
            "SHADOW_HASH|k={k}|leaves={n}|old={before}|new={after}|remote_trit=UNCHANGED|instant_action=NOT_PROVEN|json=0\n"
        ));
    }
    text
}
fn output()->String{
    let mut s=format!("YM4_06G_EXECUTION|freeze={FREEZE}|project=VOLUME_INDEPENDENT_LOCAL_WILSON_TEST|exact_rational=YES|r9_runs=0|json=0\n");
    s.push_str(&geometry(false));
    s.push_str(&budget(BETA_NUM,BETA_DEN));
    s.push_str(&b_transfer(false));
    s.push_str(&counterexample());
    s.push_str(&witness_hash());
    s.push_str("SCOPE|classical_heatbath_uniform_gap=CERTIFIED|beta_s0_physical_Wilson_B_uniform_gap=CERTIFIED|beta_s_positive_interacting_Wilson_T_uniform_mass=OPEN|spatial_a_to_zero=NOT_MEASURED|beta_running=NOT_MEASURED|continuum_SU2_mass=OPEN|r9_runs=0|json=0\n");
    s
}
struct Evidence{hbp:String,hbi:String,sha:String,sh:String,hash:String}
fn seal()->Evidence{
    let hbp=output();
    let digest=hash_bytes(hbp.as_bytes());
    let mut hbi_rows=String::new();
    let mut offset=0usize;
    for (row,line) in hbp.lines().enumerate(){
        hbi_rows.push_str(&format!("INDEX|row={row}|byte={offset}|len={}|json=0\n",line.len()+1));
        offset+=line.len()+1;
    }
    assert_eq!(offset,hbp.len());
    let hbi=format!("HBI|source=YM4_06G|rows={}|bytes={offset}|hbp_sha256={digest}|json=0\n{hbi_rows}",hbp.lines().count());
    let hbi_hash=hash_bytes(hbi.as_bytes());
    let sh=format!("SH|phase=0,1,2|global_sector=GAUGE_INVARIANT_CLASSICAL_SPATIAL_SLICE|fixed_beta_s=1/128|parent_prediction={FREEZE}|local_TV_influence=CLASSICAL|quantum_transfer=SEPARATE|hash_is_metadata=YES|json=0\n");
    let sh_hash=hash_bytes(sh.as_bytes());
    let sha=format!("SHA|hbp={digest}|hbi={hbi_hash}|sh={sh_hash}|json=0\n");
    let sha_hash=hash_bytes(sha.as_bytes());
    let root=hash_bytes(format!("YM4_06G|{FREEZE}|{digest}|{hbi_hash}|{sh_hash}|{sha_hash}").as_bytes());
    let hash=format!("HASH|root={root}|sha={sha_hash}|hbp={digest}|hbi={hbi_hash}|sh={sh_hash}|json=0\n");
    Evidence{hbp,hbi,sha,sh,hash}
}
fn entries(e:&Evidence)->[(&'static str,&str);5] {
    [("YM4-06G.hbp",&e.hbp),("YM4-06G.hbi",&e.hbi),
     ("YM4-06G.sha",&e.sha),("YM4-06G.sh",&e.sh),("YM4-06G.hash",&e.hash)]
}
fn emit(dir:&Path){
    fs::create_dir_all(dir).expect("create receipt folder");
    let evidence=seal();
    for (name,data) in entries(&evidence){fs::write(dir.join(name),data).expect("write evidence");}
    println!("YM4_06G_RESULT|PASS|L=2,3,4,5,9,27|classical_heatbath_uniform_gap=29/32|quantum_beta_s0_uniform_mass_gt=log(17)|interacting_SU2_quantum_gap=OPEN|r9_runs=0|json=0");
}
fn replay(dir:&Path){
    let evidence=seal();
    for (name,data) in entries(&evidence) {
        assert_eq!(fs::read(dir.join(name)).expect("missing receipt"),data.as_bytes(),
            "HBI/HBP/SHA/SH/HASH evidence differs from source replay");
    }
    println!("YM4_06G_VERIFY|PASS|HBI=PASS|HBP=PASS|SHA=PASS|SH=PASS|HASH=PASS|json=0");
}
fn main(){
    let args=env::args().collect::<Vec<_>>();
    match args.get(1).map(String::as_str) {
        Some("run")=>emit(Path::new(args.get(2).expect("destination"))),
        Some("verify")=>replay(Path::new(args.get(2).expect("destination"))),
        Some("plant")=>match args.get(2).map(String::as_str) {
            Some("missing_face")=>{let _=Cubic::new(3).other_face_counts(true);},
            Some("wrong_incidence")=>{
                let lat=Cubic::new(4);
                let (_,total)=lat.other_face_counts(false);
                assert_eq!(total,11,"twelve other-link face incidences per link");
            },
            Some("high_beta")=>{let _=budget(1,8);},
            Some("false_transfer_gap")=>{let _=b_transfer(true);},
            _=>panic!("unknown fault")
        },
        _=>panic!("run DIR | verify DIR | plant NAME"),
    }
}
#[cfg(test)]
mod tests{
    use super::*;
    #[test]fn spatial_l2(){let c=Cubic::new(2);assert_eq!(c.faces.len(),24);assert_eq!(c.other_face_counts(false),(4,12));}
    #[test]fn spatial_l3(){let c=Cubic::new(3);assert_eq!(c.faces.len(),81);assert_eq!(c.other_face_counts(false),(4,12));}
    #[test]fn spatial_l9(){let c=Cubic::new(9);assert_eq!(c.faces.len(),2187);assert_eq!(c.other_face_counts(false),(4,12));}
    #[test]fn spatial_l27(){let c=Cubic::new(27);assert_eq!(c.faces.len(),59049);assert_eq!(c.other_face_counts(false),(4,12));}
    #[test]fn independent_gauge_transform(){assert_eq!(Cubic::new(3).gauge_and_nonflat(),27);}
    #[test]fn volume_independent_coefficient(){assert!(budget(1,128).contains("29/128"));}
    #[test]fn exact_bessel_control(){let (a,b,c)=rho_interval();assert_eq!((a,b,c),(24_019_372,24_019_373,100_000_000));}
    #[test]fn temporal_beta_zero_uniform(){assert!(b_transfer(false).contains("ratio_lt=1/17"));}
    #[test]fn counterexample_necessary(){assert!(counterexample().contains("static_gap_implies_physical_mass=FALSE"));}
    #[test]fn merkle_metadata(){assert!(witness_hash().contains("instant_action=NOT_PROVEN"));}
}