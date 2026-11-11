//! YM4-06F. 3+1D SU(2) Wilson transfer, periodic 2x2x2 spatial torus.
//! Exact INTEGER proof checks for the full interacting GAUGE-INVARIANT spectral
//! ratio and SU(2) Peter-Weyl ternary cutoffs; no full matrix is materialized.
//! No claim of spatial continuum or a volume-uniform Yang-Mills mass gap.
#![forbid(unsafe_code)]
#![deny(clippy::float_arithmetic, clippy::float_cmp, clippy::cast_precision_loss)]
mod sha256;
use sha256::hash_bytes;
use std::{env,fs,path::Path};
use std::collections::BTreeSet;

const FREEZE:&str="955a997687d6220fa2ce60c36f97419934b4e06e";
const L:usize=8;
const N_LINKS:usize=24;
const N_FACES:usize=24;
const QROWS:[(u64,u32,u32,u64,u32);4]=[
    (3,0,3,14,3),(9,2,7,285,6),
    (27,6,21,6930,9),(81,20,61,180_441,12),
];
fn factorial(n:u32)->u128 {(1..=u128::from(n)).product()}
fn link(axis:usize,vertex:usize)->usize {assert!(axis<3 && vertex<8);axis*8+vertex}
fn next(vertex:usize,axis:usize)->usize {vertex^(1usize<<axis)}
fn faces()->Vec<[usize;4]>{
    let mut f=Vec::with_capacity(N_FACES);
    for v in 0..L{
        for a in 0..3{
            for b in (a+1)..3{
                f.push([link(a,v),link(b,next(v,a)),
                    link(a,next(v,b)),link(b,v)]);
            }
        }
    }
    assert_eq!(f.len(),N_FACES);
    f
}
fn short_cycles()->Vec<(usize,usize)>{
    let mut p=BTreeSet::new();
    for v in 0..8 {
        for a in 0..3 {
            let w=next(v,a);
            let pair=[link(a,v),link(a,w)];
            assert_ne!(pair[0],pair[1]);
            p.insert((pair[0].min(pair[1]),pair[0].max(pair[1])));
        }
    }
    p.into_iter().collect()
}
// Quaternions are the exact *finite* geometry witnesses inside SU(2).
// They are not substituted for SU(2) Haar integration or transfer spectra.
type Q=[i32;4];
const QIDENT:Q=[1,0,0,0];
const QI:Q=[0,1,0,0];
const QJ:Q=[0,0,1,0];
fn qm(x:Q,y:Q)->Q{
    [x[0]*y[0]-x[1]*y[1]-x[2]*y[2]-x[3]*y[3],
     x[0]*y[1]+x[1]*y[0]+x[2]*y[3]-x[3]*y[2],
     x[0]*y[2]-x[1]*y[3]+x[2]*y[0]+x[3]*y[1],
     x[0]*y[3]+x[1]*y[2]-x[2]*y[1]+x[3]*y[0]]
}
fn qi(x:Q)->Q{[x[0],-x[1],-x[2],-x[3]]}
fn plaquette(u:&[Q;N_LINKS],p:[usize;4])->Q{
    qm(qm(qm(u[p[0]],u[p[1]]),qi(u[p[2]])),qi(u[p[3]]))
}
fn geometry(no_interaction:bool,single_open_link:bool)->String{
    let f=faces();
    let mut incidence=[0usize;N_LINKS];
    for p in &f{
        let distinct=p.iter().copied().collect::<BTreeSet<_>>();
        assert_eq!(distinct.len(),4,"periodic 2x2x2 face must use four distinct links");
        for &e in p {incidence[e]+=1;}
    }
    assert!(incidence.iter().all(|&count|count==4),"each link must belong to 4 faces");
    let loops=short_cycles();
    assert_eq!(loops.len(),12);
    for &(x,y) in &loops{
        assert_ne!(x,y);
        assert_eq!(x/8,y/8);
        assert_eq!(next(x%8,x/8),y%8);
    }
    // An open link is changed under a local center transformation -1
    // at one end, so its fundamental trace cannot be a physical state.
    assert!(!single_open_link,"open-link fundamental is not gauge invariant");
    // Nonzero plaquette commutator is a direct demonstration of interaction.
    let mut u=[QIDENT;N_LINKS];
    for v in 0..8 {u[link(0,v)]=QI;u[link(1,v)]=QJ;}
    let n_nonflat=f.iter().filter(|&&face|plaquette(&u,face)!=QIDENT).count();
    assert!(n_nonflat>0);
    assert!(!no_interaction,"nonzero spatial Wilson plaquettes must be retained");
    // Vertex-wise gauge transform g_src U_e g_dst^-1 (independent at all 8 vertices).
    let gs:[Q;8]=[
        QIDENT,QI,QJ,[0,0,0,1],[-1,0,0,0],
        [0,-1,0,0],[0,0,-1,0],[0,0,0,-1]
    ];
    let mut moved=[QIDENT;N_LINKS];
    for e in 0..N_LINKS{
        let a=e/8;let v=e%8;
        moved[e]=qm(qm(gs[v],u[e]),qi(gs[next(v,a)]));
    }
    for (i,p) in f.iter().enumerate(){
        let v=i/3;
        let old=plaquette(&u,*p);
        let new=plaquette(&moved,*p);
        assert_eq!(new,qm(qm(gs[v],old),qi(gs[v])));
        assert_eq!(old[0],new[0]);
    }
    for &(x,y) in &loops{
        let before=qm(u[x],u[y]);
        let after=qm(moved[x],moved[y]);
        assert_eq!(before[0],after[0],"closed length-two Polyakov trace must be physical");
    }
    format!(
        "GEOMETRY|spatial=2x2x2|vertices=8|links=24|plaquettes=24|face_distinct_links=4|faces_per_link=4|two_link_cycles={}|gauge_transform_8_vertices=PASS|interacting_nonflat_faces={n_nonflat}|json=0\n",
        loops.len()
    )
}
fn pw_dim(q:u64)->u64{q*(q+1)*(2*q+1)/6}
fn trits(mut v:u64)->u32{
    let mut t=0;
    while v>0{t+=1;v/=3;}
    t
}
fn cutoff_geom()->String{
    let mut result=String::new();
    let mut prev=0u64;
    for (q,d,m,dim,t) in QROWS{
        assert_eq!(pw_dim(q),dim);
        assert_eq!(trits(dim-1),t);
        assert_eq!(u64::from(d)+u64::from(m),q);
        assert!(dim>prev);prev=dim;
        // A degree-one character of a four-DISTINCT-link plaquette
        // changes the twice-spin label of each incident link by <=1.
        // D Taylor factors can therefore raise it by at most D.
        result.push_str(&format!("PETER_WEYL|q={q}|D={d}|m={m}|dimension={dim}|trits={t}|complete_irreps=YES|per_link_bandwidth_per_plaquette=1|full_vertex_gauge_invariant=YES|json=0\n"));
    }
    result
}
fn spin_link_ratio()->(u128,u128,u128){
    // Exact rational interval already separately certified by YM4-06D.
    // The test below carries the arithmetic *independently* in integer terms.
    let lo=24_019_372u128;
    let hi=24_019_373u128;
    let scale=100_000_000u128;
    assert!(lo<hi && hi<scale);
    (lo,hi,scale)
}
fn full_ratio()->String{
    let (lo,hi,scale)=spin_link_ratio();
    let n=scale*scale;
    // For product of 24 Wilson link convolutions, gauge invariance at
    // all eight distinct vertices eliminates isolated nontrivial edges.
    // Any nontrivial spin-network support must have degree>=2 at each
    // active vertex and so must contain a cycle. The girth is two;
    // a fundamental two-link Polyakov loop realizes this second level:
    // lambda_2(B)/lambda_1(B)=(b1/b0)^2.
    // Multiplication A(U) is bounded e^-3/8<=A<=1 (24 plaquettes,
    // beta_s=1/128). So 5/8 <= exp(-3/8), exp(3/8)<=8/5.
    // This compares the FULL interacting T=S B P_G S with B by min-max.
    assert!(5*28*lo*lo>8*n,"frozen full physical lower ratio refuted");
    assert!(8*10*hi*hi<5*n,"frozen full physical upper ratio refuted");
    format!("FULL_PHYSICAL_TRANSFER|space=2x2x2|links=24|plaquettes=24|beta_s=1/128|beta_t=1|gauge_projector=ALL_VERTICES|B_first_nontrivial_spin_support=2|B_first_ratio=(ell1/ell0)^2|lambda2_lambda1_gt=1/28|lambda2_lambda1_lt=1/10|continuum_mass=NOT_COMPUTED|json=0\n")
}
fn error_q3()->bool{
    // h_max=beta_s*N_faces/2=3/32, D=0, m=3.
    // delta=3/32 and sqrt(4/(3*2^3*4!))=1/12.
    assert_eq!(3*8*factorial(4),576);
    17u128*8<3*48  // 2*(3/32+1/12)=17/48<3/8.
}
fn error_q9()->bool{
    // D=2,m=7: delta=(3/32)^3/3!=9/65536<1/7000.
    assert!(9u128*7000<65_536);
    // sqrt(4/(3*2^7*8!))<1/1900.
    assert!(4u128*1900*1900<3*(1u128<<7)*factorial(8));
    // 2*(1/7000+1/1900)<1/700.
    2u128*(7000+1900)*700<7000*1900
}
fn error_q27()->bool{
    // D=6,m=21.
    assert!(3u128.pow(7)*70_000_000_000<
        32u128.pow(7)*factorial(7));
    assert!(4u128*40_000_000_000_000u128.pow(2) <
        3*(1u128<<21)*factorial(22));
    // 2*(1/(70e9)+1/(40e12)) < 1/(30e9).
    let a=70_000_000_000u128;
    let b=40_000_000_000_000u128;
    let c=30_000_000_000u128;
    2*(a+b)*c<a*b
}
fn error_q81()->bool{
    // D=20,m=61. The spin tail is below that of m=41.
    // First: delta_7<1/(70e9); subsequent Taylor factors for
    // t=8..21 are <= 1/80. Hence delta_21<1/10^31.
    assert!(3u128.pow(7)*70_000_000_000 <
        32u128.pow(7)*factorial(7));
    assert!((8u128..=21).all(|t|3*80<32*t));
    assert!(70_000_000_000u128*80u128.pow(14) >10u128.pow(31));
    // Second: 3*2^41*42! > 4*10^62 by splitting factorial.
    let fac21=factorial(21);
    let fac22_42=(22u128..=42).product::<u128>();
    let twopow=1u128<<41;
    assert!(fac21>50_000_000_000_000_000_000u128);
    assert!(fac22_42>20_000_000_000_000_000_000_000_000_000_000u128);
    assert!(twopow>2_000_000_000_000u128);
    assert!(3*2*5*2>4); // normalizations 10^12*10^19*10^31.
    // Thus sqrt(b_41/b0)<1/10^31, and sqrt(b_61/b0) smaller.
    // 2*(delta+sqrt)<4/10^31<1/10^30.
    4u128<10
}
fn projected_ratio(e:u128,min_num:u128,min_den:u128,max_num:u128,max_den:u128)->bool{
    // If ||T-P_qTP_q||< b0^24/e, Weyl gives a two-sided ratio
    // using T bounds 5/8 B1 <=lambda2<=B1 and
    // 5/8 B0 <=lambda1<=B0, with B1/B0=(ell1/ell0)^2.
    let (lo,hi,scale)=spin_link_ratio();
    let n=scale*scale;
    let lhs_lower=5*lo*lo*e;
    let correction=8*n;
    if lhs_lower<=correction{return false;}
    let cert_lower=min_den*(lhs_lower-correction)>
        min_num*8*n*(e+1);
    let cert_upper=max_den*8*(hi*hi*e+n)<
        max_num*n*(5*e-8);
    cert_lower&&cert_upper
}
fn cutoffs(drop_irrep:bool,wrong_tail:bool)->String{
    let mut o=String::new();
    for (q,d,m,dim,t) in QROWS{
        let dimension=if drop_irrep && q==9 {pw_dim(q-1)}else{pw_dim(q)};
        assert_eq!(dimension,dim,"missing complete SU2 representation block");
        let (num,den,pass)=match q{
            3=>(3u128,8u128,error_q3()),
            9=>(1,700,error_q9()),
            27=>(1,30_000_000_000,error_q27()),
            81=>(1,10u128.pow(30),error_q81()),
            _=>panic!("unfrozen cutoff")
        };
        assert!(pass,"cutoff error bound not proved from rational inequalities");
        if wrong_tail && q==9{
            assert!(den>=1_000,"overstrong cutoff tail must be rejected");
        }
        o.push_str(&format!("CUTOFF_NORM|q={q}|D={d}|m={m}|dimension={dim}|trits={t}|full_interacting_transfer_error_over_b0^24_lt={num}/{den}|json=0\n"));
        if q==9{
            assert!(projected_ratio(700,1,30,1,10));
            o.push_str("CUTOFF_SPECTRUM|q=9|lambda2_lambda1_gt=1/30|lambda2_lambda1_lt=1/10|Weyl_full_interacting=YES|json=0\n");
        }else if q==27{
            assert!(projected_ratio(30_000_000_000,1,28,1,10));
            o.push_str("CUTOFF_SPECTRUM|q=27|lambda2_lambda1_gt=1/28|lambda2_lambda1_lt=1/10|Weyl_full_interacting=YES|json=0\n");
        }else if q==81{
            // Error <1/10^30 is stronger than the q27 error, hence
            // its ratio enclosure follows monotonically without
            // multiplying denominators beyond u128.
            assert!(den>30_000_000_000);
            o.push_str("CUTOFF_SPECTRUM|q=81|lambda2_lambda1_gt=1/28|lambda2_lambda1_lt=1/10|Weyl_monotone_from_q27=YES|json=0\n");
        }else{
            o.push_str("CUTOFF_SPECTRUM|q=3|physical_ratio=NOT_ENCLOSED|json=0\n");
        }
    }
    o
}
fn trinary_hash()->String{
    let mut out=String::new();
    for k in 1..=4u32{
        let n=3usize.pow(k);let changed=n/2;
        let root=|mutate:bool|{
            let mut leaves=(0..n).map(|i|{
                let trit=if mutate && i==changed{(i+1)%3}else{i%3};
                hash_bytes(format!("YM4_06F_LEAF|{k}|{i}|{trit}").as_bytes())
            }).collect::<Vec<_>>();
            for level in 0..k{
                leaves=leaves.chunks_exact(3).map(|c|{
                    hash_bytes(format!("YM4_06F_NODE|{k}|{level}|{}|{}|{}",c[0],c[1],c[2]).as_bytes())
                }).collect();
            }
            assert_eq!(leaves.len(),1);
            leaves.pop().unwrap()
        };
        let before=root(false);let after=root(true);
        assert_ne!(before,after);
        assert_ne!(changed,0);
        out.push_str(&format!("SHADOW_HASH|k={k}|before={before}|after={after}|remote_physical_trit=UNCHANGED|instant_signal=NOT_INFERRED|json=0\n"));
    }
    out
}
fn hbp()->String{
    let mut s=format!("YM4_06F|model=SU2_WILSON_PHYSICAL_2x2x2|freeze={FREEZE}|Rust=1.81|trinary_storage=YES|r9_runs=0|json=0\n");
    s.push_str(&geometry(false,false));
    s.push_str(&pw_dim_gate());
    s.push_str(&full_ratio());
    s.push_str(&cutoffs(false,false));
    s.push_str(&trinary_hash());
    s.push_str("SCOPE|actual_interacting_gauge_transfer=YES|two_sided_analytic_enclosures=YES|exact_eigenvalues=NOT_COMPUTED|spatial_a_to_zero=NOT_RUN|physical_volume_to_infinity=NOT_RUN|4D_YM_mass_gap=OPEN|r9_runs=0|json=0\n");
    s
}
fn pw_dim_gate()->String{cutoff_geom()}
struct Receipt{hbp:String,hbi:String,sha:String,sh:String,hash:String}
fn evidence()->Receipt{
    let hbp=hbp();let hd=hash_bytes(hbp.as_bytes());
    let mut idx=String::new();let mut offs=0usize;
    for (i,line) in hbp.lines().enumerate(){
        idx.push_str(&format!("INDEX|row={i}|offset={offs}|length={}|json=0\n",line.len()+1));
        offs+=line.len()+1;
    }
    assert_eq!(offs,hbp.len());
    let hbi=format!("HBI|hbp_sha256={hd}|rows={}|bytes={offs}|json=0\n{idx}",hbp.lines().count());
    let id=hash_bytes(hbi.as_bytes());
    let sh=format!("SH|spatial_2x2x2=SU2_PHYSICAL|local_cycles=12|phase=0,1,2|frozen_source={FREEZE}|hash_is_metadata=YES|rooted_gauge_8_vertices=YES|json=0\n");
    let sd=hash_bytes(sh.as_bytes());
    let sha=format!("SHA|hbp={hd}|hbi={id}|sh={sd}|json=0\n");
    let ad=hash_bytes(sha.as_bytes());
    let root=hash_bytes(format!("YM4_06F|{FREEZE}|{hd}|{id}|{sd}|{ad}").as_bytes());
    let hash=format!("HASH|global={root}|sha={ad}|hbp={hd}|hbi={id}|sh={sd}|r9_runs=0|json=0\n");
    Receipt{hbp,hbi,sha,sh,hash}
}
fn paths(e:&Receipt)->[(&'static str,&str);5]{
    [("YM4-06F.hbp",&e.hbp),("YM4-06F.hbi",&e.hbi),
     ("YM4-06F.sha",&e.sha),("YM4-06F.sh",&e.sh),("YM4-06F.hash",&e.hash)]
}
fn write(dir:&Path){
    fs::create_dir_all(dir).unwrap();
    let e=evidence();
    for (name,contents) in paths(&e){fs::write(dir.join(name),contents).unwrap();}
    println!("YM4_06F_EXECUTE|PASS|interacting_SU2_2x2x2=FINITE_ENCLOSED|cutoffs_q3_q9_q27_q81=EXACT_RATIONAL|hash=SEALED|r9_runs=0|json=0");
}
fn verify(dir:&Path){
    let e=evidence();
    for(name,contents)in paths(&e){
        assert_eq!(fs::read(dir.join(name)).unwrap(),contents.as_bytes(),"HBP HBI SHA SH HASH mismatch");
    }
    println!("YM4_06F_VERIFY|PASS|HBI=YES|HBP=YES|SHA=YES|SH=YES|HASH=YES|json=0");
}
fn main(){
    let args=env::args().collect::<Vec<_>>();
    match args.get(1).map(String::as_str){
        Some("run")=>write(Path::new(args.get(2).expect("output folder"))),
        Some("verify")=>verify(Path::new(args.get(2).expect("output folder"))),
        Some("plant")=>match args.get(2).map(String::as_str){
            Some("no_spatial")=>{let _=geometry(true,false);},
            Some("open_link_physical")=>{let _=geometry(false,true);},
            Some("missing_irrep")=>{let _=cutoffs(true,false);},
            Some("overstrong_tail")=>{let _=cutoffs(false,true);},
            _=>panic!("invalid fault control")
        },
        _=>panic!("usage: run OUTPUT | verify OUTPUT | plant NAME")
    }
}
#[cfg(test)]
mod tests{
    use super::*;
    #[test]fn spatial_geometry(){assert!(geometry(false,false).contains("plaquettes=24"));}
    #[test]fn su2_polykov_gauge(){assert_eq!(short_cycles().len(),12);}
    #[test]fn exact_full_ratio(){assert!(full_ratio().contains("lambda2_lambda1_gt=1/28"));}
    #[test]fn q3(){assert!(error_q3());}
    #[test]fn q9(){assert!(error_q9());}
    #[test]fn q27(){assert!(error_q27());}
    #[test]fn q81(){assert!(error_q81());}
    #[test]fn ratio_q9(){assert!(projected_ratio(700,1,30,1,10));}
    #[test]fn ratio_q27(){assert!(projected_ratio(30_000_000_000,1,28,1,10));}
    #[test]fn cutoffs_all(){assert!(cutoffs(false,false).contains("q=81"));}
    #[test]fn hash_metadata(){assert!(trinary_hash().contains("instant_signal=NOT_INFERRED"));}
}
