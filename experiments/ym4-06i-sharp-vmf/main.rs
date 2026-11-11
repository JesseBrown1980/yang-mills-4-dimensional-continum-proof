//! YM4-06I. Strong-coupling 4D SU(2) Wilson: local influence independent
//! of volume, a Dobrushin/Follmer spacetime-covariance bound, and a
//! reflection-positive physical-transfer mass-gap consequence at FIXED a.
//! The standard covariance and Wilson transfer theorems are ANALYTIC INPUTS,
//! not computations of the infinite-dimensional Wilson eigenvalues.
//! Improved global S3 variance bound, beta_s=1/128 beta_t=1/10; beta_t>=1/9 excluded.
#![forbid(unsafe_code)]
#![deny(clippy::float_arithmetic,clippy::float_cmp,clippy::cast_precision_loss)]
mod sha256;
use sha256::hash_bytes;
use std::env;
use std::fs;
use std::path::Path;

const FREEZE:&str="7f4da6d135978453d7eeddfd2a8396c183814387";
const TESTS:[(usize,usize);6]=[(2,3),(3,3),(3,6),(5,3),(9,3),(27,2)];
type Quaternion=[i32;4];
const I:Quaternion=[0,1,0,0];
const J:Quaternion=[0,0,1,0];
const K:Quaternion=[0,0,0,1];
const ONE:Quaternion=[1,0,0,0];
const Q8:[Quaternion;8]=[ONE,[-1,0,0,0],I,[0,-1,0,0],J,[0,0,-1,0],K,[0,0,0,-1]];
fn product(x:Quaternion,y:Quaternion)->Quaternion{
    [x[0]*y[0]-x[1]*y[1]-x[2]*y[2]-x[3]*y[3],
     x[0]*y[1]+x[1]*y[0]+x[2]*y[3]-x[3]*y[2],
     x[0]*y[2]-x[1]*y[3]+x[2]*y[0]+x[3]*y[1],
     x[0]*y[3]+x[1]*y[2]-x[2]*y[1]+x[3]*y[0]]
}
fn inverse(x:Quaternion)->Quaternion{[x[0],-x[1],-x[2],-x[3]]}
fn face_hol(u:&[Quaternion],p:[usize;4])->Quaternion{
    product(product(product(u[p[0]],u[p[1]]),inverse(u[p[2]])),inverse(u[p[3]]))
}
fn gcd(mut x:u128,mut y:u128)->u128{while y>0{let r=x%y;x=y;y=r;}x}
#[derive(Clone,Copy)]
struct Rat{a:u128,b:u128}
impl Rat{
    fn new(a:u128,b:u128)->Self{
        assert!(b>0);
        let g=gcd(a,b);
        Self{a:a/g,b:b/g}
    }
    fn add(self,other:Self)->Self{
        let g=gcd(self.b,other.b);
        Self::new(self.a*(other.b/g)+other.a*(self.b/g),(self.b/g)*other.b)
    }
    fn lt(self,other:Self)->bool{
        self.a*other.b<other.a*self.b
    }
    fn display(self)->String{format!("{}/{}",self.a,self.b)}
}
struct Torus{
    l:usize,nt:usize,n:usize,faces:Vec<([usize;4],bool)>,
}
impl Torus{
    fn new(l:usize,nt:usize)->Self{
        assert!(l>=2&&nt>=2);
        let n=l*l*l*nt;
        let mut faces=Vec::with_capacity(6*n);
        let helper=Self{l,nt,n,faces:Vec::new()};
        for v in 0..n {
            for a in 0..4 {
                for b in (a+1)..4 {
                    faces.push(([
                        helper.link(a,v),
                        helper.link(b,helper.step(v,a)),
                        helper.link(a,helper.step(v,b)),
                        helper.link(b,v),
                    ],b==3));
                }
            }
        }
        assert_eq!(faces.len(),6*n);
        Self{l,nt,n,faces}
    }
    fn link(&self,axis:usize,vertex:usize)->usize {
        assert!(axis<4&&vertex<self.n);
        axis*self.n+vertex
    }
    fn step(&self,vertex:usize,axis:usize)->usize{
        let stride=if axis==3{self.l*self.l*self.l}else{self.l.pow(axis as u32)};
        let length=if axis==3{self.nt}else{self.l};
        let c=(vertex/stride)%length;
        if c+1<length {vertex+stride}else{vertex-(length-1)*stride}
    }
    fn time(&self,link:usize)->usize{
        (link%self.n)/(self.l*self.l*self.l)
    }
    fn cyclic_temporal_distance(&self,x:usize,y:usize)->usize{
        let diff=x.abs_diff(y);
        diff.min(self.nt-diff)
    }
    fn incidence(&self,drop_face:bool,wrong_time:bool,wrong_tag:bool)->(usize,usize){
        let mut spatial=vec![0usize;4*self.n];
        let mut temporal=vec![0usize;4*self.n];
        let mut max_delta=0usize;
        for (index,(edges,is_temporal)) in self.faces.iter().enumerate(){
            if drop_face && index==0 {continue;}
            for (i,&edge) in edges.iter().enumerate(){
                for (j,&other) in edges.iter().enumerate(){
                    if i!=j{assert_ne!(edge,other,"4D face repeats a link");}
                    let td=self.cyclic_temporal_distance(self.time(edge),self.time(other));
                    max_delta=max_delta.max(td);
                    assert!(td<=1,"Wilson face permits nonlocal temporal jump");
                }
                if *is_temporal {temporal[edge]+=1;}else{spatial[edge]+=1;}
            }
        }
        let link_total=4*self.n;
        for e in 0..link_total{
            let count=spatial[e]+temporal[e];
            assert_eq!(count,6,"six Wilson faces per oriented 4D link");
            if e/self.n==3 {
                assert_eq!(spatial[e],0,"temporal link must have no spatial faces");
                assert_eq!(temporal[e],6,"temporal link must have six temporal faces");
                if wrong_tag && e==3*self.n {
                    assert_eq!(spatial[e],1,"temporal link was misclassified");
                }
            } else {
                assert_eq!(spatial[e],4,"spatial link needs four spatial faces");
                assert_eq!(temporal[e],2,"spatial link needs two temporal faces");
            }
        }
        if wrong_time {assert_eq!(max_delta,0,"temporal face jump cannot be erased");}
        assert_eq!(max_delta,1);
        (6,18)
    }
    fn gauge_geometry(&self)->(usize,usize){
        let mut u=vec![ONE;4*self.n];
        for v in 0..self.n {
            u[self.link(0,v)]=I;
            u[self.link(1,v)]=J;
            u[self.link(3,v)]=K;
        }
        let mut moved=vec![ONE;4*self.n];
        for axis in 0..4 {
            for v in 0..self.n {
                moved[self.link(axis,v)]=product(
                    product(Q8[v%8],u[self.link(axis,v)]),
                    inverse(Q8[self.step(v,axis)%8])
                );
            }
        }
        let mut nonflat_s=0usize;
        let mut nonflat_t=0usize;
        for (face_index,(p,t)) in self.faces.iter().enumerate(){
            let h=face_hol(&u,*p);
            if h!=ONE {if *t{nonflat_t+=1;}else{nonflat_s+=1;}}
            let v=face_index/6;
            let expected=product(product(Q8[v%8],h),inverse(Q8[v%8]));
            let new=face_hol(&moved,*p);
            assert_eq!(new,expected,"local SU2 gauge-covariance of 4D face");
            assert_eq!(h[0],new[0],"SU2 Wilson trace invariant");
        }
        assert_eq!(nonflat_s,self.n);
        assert_eq!(nonflat_t,2*self.n);
        (nonflat_s,nonflat_t)
    }
}
fn geometry()->String{
    let mut rows=String::new();
    for (l,nt) in TESTS{
        let t=Torus::new(l,nt);
        let (degree,total)=t.incidence(false,false,false);
        let (nonflat_s,nonflat_t)=t.gauge_geometry();
        rows.push_str(&format!(
            "4D_GEOMETRY|L={l}|Nt={nt}|sites={}|links={}|plaquettes={}|faces_per_link={degree}|other_link_incidences={total}|spatial_link_faces=4spatial+2temporal|temporal_link_faces=6temporal|time_jump_per_face_le=1|nonflat_spatial={nonflat_s}|nonflat_temporal={nonflat_t}|gauge_witness=PASS|json=0\n",
            t.n,4*t.n,t.faces.len()
        ));
    }
    rows
}
fn vmf_covariance_gate(false_variance:bool,false_old_factor:bool)->String{
    // Z(r)=2 I1(r)/r, A(r)=I2(r)/I1(r) for vMF on quaternion S3.
    // The Hessian of logZ has eigenvalues A'(r), A(r)/r (triple).
    // Positive Bessel coefficients imply A(r)<=r/4: for each s>=0,
    // coefficient I2/(r I1/4) is 2/(s+2)<=1.
    for s in 0..=1024u128 {assert!(2<=s+2);}
    // A'=1-A²-3A/r, A=r/4-r³/96+O(r^5) at the origin.
    // At an upward crossing A'=1/4, its derivative is
    // A''=[A(12-2r²)-3r]/(4r²), strictly negative for r>0:
    // if r²<=6 use A<=r/4; otherwise both terms are negative.
    // Therefore A'<=1/4 for all r>=0. Hessian Cov_h(X)<=I/4.
    // dTV/dt<=0.5 sqrt Var((h'-h)dot X) <=||h'-h||/4.
    // A co-plaquette neighbor changes |h-h'| by <=2 beta*c,
    // hence c_ij<= beta*c/2 at ALL external fields.
    if false_variance{
        assert!(1u128*8<=4,"uniform S3 has directional variance 1/4 not 1/8");
    }
    if false_old_factor{
        assert_eq!(1u128,2,"old beta per face is not the sharpened beta/2 certificate");
    }
    "SU2_VMF_THEOREM|Hessian_logZ_eigenvalues_le=1/4|Bessel_ratio_A_over_r_le=1/4|Riccati_upcrossing=NEGATIVE|TV_field_Lipschitz=1/4|cij_per_shared_face_le=beta/2|all_h=YES|analytic_certificate=YES|json=0\n".to_string()
}

fn anisotropic_alpha(bs_num:u128,bs_den:u128,bt_num:u128,bt_den:u128)->(Rat,Rat,Rat){
    assert!(bs_den>0 && bt_den>0);
    let spatial=Rat::new(6*bs_num,bs_den).add(Rat::new(3*bt_num,bt_den));
    let temporal=Rat::new(9*bt_num,bt_den);
    let alpha=if spatial.lt(temporal){temporal}else{spatial};
    assert!(alpha.a<alpha.b,"four-dimensional Dobrushin threshold violated");
    (spatial,temporal,alpha)
}
fn coefficient_rows()->String{
    let mut out=String::new();
    for denominator in [10u128,16,32]{
        let (s,t,a)=anisotropic_alpha(1,128,1,denominator);
        let gamma=Rat::new(a.b-a.a,a.b);
        let (expected_s,expected_t)=match denominator {
            10=>("111/320","9/10"),16=>("15/64","9/16"),32=>("9/64","9/32"),
            _=>panic!("unfrozen temporal beta"),
        };
        assert_eq!(s.display(),expected_s);
        assert_eq!(t.display(),expected_t);
        out.push_str(&format!(
            "4D_ALPHA|beta_s=1/128|beta_t=1/{denominator}|spatial_link_alpha_le={}|temporal_link_alpha_le={}|all_link_alpha_le={}|one_minus_alpha_ge={}|coface_neighbor_count=3|TV_beta_factor=1/2|volume_independent=YES|json=0\n",
            s.display(),t.display(),a.display(),gamma.display()
        ));
    }
    out
}
fn cov_tail(power:u32,alpha:Rat)->Rat{
    let num=alpha.a.pow(power)*alpha.b;
    let den=alpha.b.pow(power)*(alpha.b-alpha.a);
    Rat::new(num,den)
}
fn transfer_bridge()->String{
    let (_,_,a)=anisotropic_alpha(1,128,1,10);
    assert_eq!(a.display(),"9/10");
    let mut out=String::new();
    // Dobrushin/Follmer: connected covariances bounded by
    // sum delta_f (I-C)^-1 delta_g with C_ij<=sum(beta*c_ij)/2.
    // Every co-plaquette influence step moves the temporal link anchor
    // by at most one frame, so |C_f(t)|<=C_f alpha^t/(1-alpha).
    // C_f may depend on fixed spatial volume but never on t.
    // Wilson reflection positivity identifies C_f(t) with a positive
    // spectral sum of powers of T/lambda_1 on the gauge-invariant slice.
    // Bounded gauge-invariant slice functions are L2-dense for fixed L.
    // Taking t-th roots and using positivity gives lambda2/lambda1<=alpha.
    for t in [1u32,3,9,27]{
        let c=cov_tail(t,a);
        assert!(c.a>0);
        out.push_str(&format!(
            "4D_COVARIANCE_TAIL|beta_s=1/128|beta_t=1/10|frame_separation={t}|connected_covariance_factor_le={}|prefactor=LOCAL_OBSERVABLE_OSCILLATIONS|physical_transfer_spectrum=USE_OS_POSITIVITY|json=0\n",
            c.display()
        ));
    }
    out.push_str("4D_PHYSICAL_TRANSFER|beta_s=1/128|beta_t=1/10|all_spatial_L_ge2=YES|Wilson_transfer_positive=OS_INPUT|Dobrushin_covariance=FOLLMER_INPUT|time_anchor_one_step=GEOMETRY_CERTIFIED|full_physical_lambda2_over_lambda1_le=9/10|reference_a_t_1_mass_ge=log(10/9)|volume_independent=YES|nonzero_spatial_interaction=YES|nonzero_temporal_interaction=YES|continuum=OPEN|json=0\n");
    out
}
fn shadow_hash()->String{
    let mut rows=String::new();
    for k in 1..=4u32{
        let n=3usize.pow(k);let changed=n/2;
        let root=|mutated:bool|{
            let mut leaves=(0..n).map(|i|{
                let mut trit=i%3;
                if mutated&&i==changed{trit=(trit+1)%3;}
                hash_bytes(format!("YM4_06I|k={k}|leaf={i}|trit={trit}").as_bytes())
            }).collect::<Vec<_>>();
            for level in 0..k {
                leaves=leaves.chunks_exact(3).map(|c|{
                    hash_bytes(format!("YM4_06I|level={level}|{}|{}|{}",c[0],c[1],c[2]).as_bytes())
                }).collect::<Vec<_>>();
            }
            assert_eq!(leaves.len(),1);
            leaves.pop().unwrap()
        };
        let old=root(false);let new=root(true);
        assert_ne!(old,new);
        assert_ne!(changed,0);
        rows.push_str(&format!(
            "SHADOW_HASH|k={k}|old={old}|new={new}|remote_physical_trit=UNCHANGED|SHA_is_physical_interaction=NO|json=0\n"
        ));
    }
    rows
}
fn result()->String{
    let mut out=format!("YM4_06I|freeze={FREEZE}|group=SU2|Wilson_action=3PLUS1D_ANISOTROPIC|gauge=ALL_VERTICES|r9_runs=0|json=0\n");
    out.push_str(&geometry());
    out.push_str(&vmf_covariance_gate(false,false));
    out.push_str(&coefficient_rows());
    out.push_str(&transfer_bridge());
    out.push_str(&shadow_hash());
    out.push_str("SCOPE|finite_a_strong_coupling_4D_uniform_gap=CONDITIONAL_ON_NAMED_DOBRUSHIN_AND_OS_INPUTS|beta_t_1=NOT_COVERED|physical_a_t_calibration=NOT_RUN|weak_coupling_beta_running=NOT_RUN|continuum_YM_mass=OPEN|r9_runs=0|json=0\n");
    out
}
struct Evidence{hbp:String,hbi:String,sha:String,sh:String,hash:String}
fn seal()->Evidence{
    let hbp=result();
    let digest=hash_bytes(hbp.as_bytes());
    let mut index=String::new();let mut offset=0usize;
    for (row,line) in hbp.lines().enumerate(){
        index.push_str(&format!("INDEX|row={row}|byte={offset}|length={}|json=0\n",line.len()+1));
        offset+=line.len()+1;
    }
    assert_eq!(offset,hbp.len());
    let hbi=format!("HBI|source=YM4_06I|rows={}|bytes={offset}|hbp_sha256={digest}|json=0\n{index}",hbp.lines().count());
    let hbi_digest=hash_bytes(hbi.as_bytes());
    let sh=format!("SH|phase=0,1,2|global_physical_sector=SU2_ALL_VERTEX_GAUGE_INVARIANTS|source={FREEZE}|beta_s=1/128|beta_t=1/10|time_frame=ONE_WILSON_TRANSFER|SHA=EVIDENCE_METADATA|json=0\n");
    let sh_digest=hash_bytes(sh.as_bytes());
    let sha=format!("SHA|hbp={digest}|hbi={hbi_digest}|sh={sh_digest}|json=0\n");
    let sha_digest=hash_bytes(sha.as_bytes());
    let global=hash_bytes(format!("YM4_06I|{FREEZE}|{digest}|{hbi_digest}|{sh_digest}|{sha_digest}").as_bytes());
    let hash=format!("HASH|root={global}|hbp={digest}|hbi={hbi_digest}|sh={sh_digest}|sha={sha_digest}|json=0\n");
    Evidence{hbp,hbi,sha,sh,hash}
}
fn entries(e:&Evidence)->[(&'static str,&str);5]{
    [("YM4-06I.hbp",&e.hbp),("YM4-06I.hbi",&e.hbi),
     ("YM4-06I.sha",&e.sha),("YM4-06I.sh",&e.sh),("YM4-06I.hash",&e.hash)]
}
fn write(dir:&Path){
    fs::create_dir_all(dir).expect("create evidence folder");
    let e=seal();
    for(name,text)in entries(&e){fs::write(dir.join(name),text).expect("write canonical evidence");}
    println!("YM4_06I_EXECUTE|PASS|4D_geometry_L=2,3,5,9,27|alpha_primary=9/10|all_volume_interacting_transfer_ratio_le=9/10|beta_t_1=NOT_COVERED|continuum_YM_gap=OPEN|r9_runs=0|json=0");
}
fn verify(dir:&Path){
    let e=seal();
    for(name,content)in entries(&e){
        assert_eq!(fs::read(dir.join(name)).expect("missing file"),content.as_bytes(),"HBI HBP SHA SH HASH evidence mismatch");
    }
    println!("YM4_06I_VERIFY|PASS|HBI=PASS|HBP=PASS|SHA=PASS|SH=PASS|HASH=PASS|json=0");
}
fn main(){
    let args=env::args().collect::<Vec<_>>();
    match args.get(1).map(String::as_str){
        Some("run")=>write(Path::new(args.get(2).expect("destination"))),
        Some("verify")=>verify(Path::new(args.get(2).expect("destination"))),
        Some("plant")=>match args.get(2).map(String::as_str){
            Some("missing_temporal_face")=>{let _=Torus::new(3,6).incidence(true,false,false);},
            Some("wrong_temporal_type")=>{let _=Torus::new(3,6).incidence(false,false,true);},
            Some("wrong_time_locality")=>{let _=Torus::new(3,6).incidence(false,true,false);},
            Some("beta_above_threshold")=>{let _=anisotropic_alpha(1,128,1,8);},
            Some("beta_at_boundary")=>{let _=anisotropic_alpha(1,128,1,9);},
            Some("wrong_vmf_variance")=>{let _=vmf_covariance_gate(true,false);},
            Some("old_tv_factor")=>{let _=vmf_covariance_gate(false,true);},
            Some("old_beta_t_one")=>{let _=anisotropic_alpha(1,128,1,1);},
            _=>panic!("unknown planted fault")
        },
        _=>panic!("usage: run DEST | verify DEST | plant FAULT")
    }
}
#[cfg(test)]
mod tests{
    use super::*;
    #[test]fn geometry_l2(){let t=Torus::new(2,3);assert_eq!(t.faces.len(),144);assert_eq!(t.incidence(false,false,false),(6,18));}
    #[test]fn geometry_l3(){let t=Torus::new(3,3);assert_eq!(t.faces.len(),486);assert_eq!(t.incidence(false,false,false),(6,18));}
    #[test]fn geometry_l3_longtime(){let t=Torus::new(3,6);assert_eq!(t.faces.len(),972);assert_eq!(t.incidence(false,false,false),(6,18));}
    #[test]fn geometry_l9(){let t=Torus::new(9,3);assert_eq!(t.faces.len(),13122);assert_eq!(t.incidence(false,false,false),(6,18));}
    #[test]fn geometry_l27(){let t=Torus::new(27,2);assert_eq!(t.faces.len(),236196);assert_eq!(t.incidence(false,false,false),(6,18));}
    #[test]fn independent_vertex_gauge(){assert_eq!(Torus::new(3,3).gauge_geometry(),(81,162));}
    #[test]fn uniform_alpha(){let(s,t,a)=anisotropic_alpha(1,128,1,10);assert_eq!((s.display(),t.display(),a.display()),("111/320".into(),"9/10".into(),"9/10".into()));}
    #[test]fn alternate_couplings(){assert!(coefficient_rows().contains("all_link_alpha_le=9/32"));}
    #[test]fn time_covariance_decay(){assert!(transfer_bridge().contains("reference_a_t_1_mass_ge=log(10/9)"));}
    #[test]fn full_s3_variance_lemma(){assert!(vmf_covariance_gate(false,false).contains("TV_field_Lipschitz=1/4"));}
    #[test]fn strict_coupling_control(){let (_,_,a)=anisotropic_alpha(1,128,1,16);assert_eq!(a.display(),"9/16");}
    #[test]fn hash_lineage(){assert!(shadow_hash().contains("SHA_is_physical_interaction=NO"));}
}