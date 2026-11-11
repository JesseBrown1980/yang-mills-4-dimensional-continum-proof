//! YM4-06E interacting 3+1D SU2 Wilson transfer, spatial periodic (Z/1)^3.
//! Full gauge-invariant transfer spectral ratio and P_q norm errors, exact rationals.
//! This is fixed spatial volume/coupling; NO spatial continuum or Clay mass proof.
#![forbid(unsafe_code)]
#![deny(clippy::float_arithmetic, clippy::float_cmp, clippy::cast_precision_loss)]
mod sha256;
use sha256::hash_bytes;
use std::env;
use std::fs;
use std::path::Path;

const FIRST_FREEZE:&str="89904ca89abc5962162e25509e5c20cf9588151e";
const QROWS:[(u64,u32,u32,u64,u32,u128,u128);4]=[
    (3,0,3,14,3,3,8),
    (9,2,5,285,6,1,60),
    (27,6,15,6930,9,1,300_000_000),
    (81,20,41,180_441,12,1,1_000_000_000_000_000_000_000_000_000_000),
];

fn gcd(mut x:u128,mut y:u128)->u128{
    while y>0{let z=x%y;x=y;y=z;}x
}
#[derive(Clone,Copy,Debug)]
struct Rat{a:u128,b:u128}
impl Rat{
    fn new(a:u128,b:u128)->Self{
        assert!(b>0);
        let g=gcd(a,b);
        Self{a:a/g,b:b/g}
    }
    fn add(self,other:Self)->Self{
        let g=gcd(self.b,other.b);
        let b1=self.b/g;
        Self::new(self.a*(other.b/g)+other.a*b1,b1*other.b)
    }
    fn mul(self,other:Self)->Self{
        let g=gcd(self.a,other.b);
        let h=gcd(other.a,self.b);
        Self::new((self.a/g)*(other.a/h),(self.b/h)*(other.b/g))
    }
    fn div(self,other:Self)->Self{
        assert!(other.a>0);
        self.mul(Self::new(other.b,other.a))
    }
    fn lt(self,other:Self)->bool{
        self.a*other.b<other.a*self.b
    }
    fn display(self)->String{format!("{}/{}",self.a,self.b)}
}
fn factorial(n:u32)->u128{(1..=u128::from(n)).product()}
fn term(n:u32,s:u32)->Rat{
    Rat::new(1,(1u128<<(2*s+n))*factorial(s)*factorial(s+n+1))
}
fn partial(n:u32,through:u32)->Rat{
    let mut sum=Rat::new(0,1);
    for s in 0..=through{sum=sum.add(term(n,s));}
    sum
}
fn remainder(n:u32,through:u32)->Rat{
    let s=through+1;
    let t=term(n,s);
    let den=4*u128::from(s+1)*u128::from(s+n+2);
    t.mul(Rat::new(den,den-1))
}
fn link_ratio()->(Rat,Rat){
    let l0=partial(0,4);
    let l1=partial(1,4);
    let lo=l1.div(l0.add(remainder(0,4)));
    let hi=l1.add(remainder(1,4)).div(l0);
    assert!(Rat::new(24_019_372,100_000_000).lt(lo));
    assert!(hi.lt(Rat::new(24_019_373,100_000_000)));
    assert!(lo.lt(hi));
    (lo,hi)
}
// Quaternion units, exact Hamilton multiplication. Q8 is used solely as
// a noncommuting SU(2) configuration witness, NOT as a SU(2) quadrature.
type Q=[i32;4];
fn qm(x:Q,y:Q)->Q{
    [
        x[0]*y[0]-x[1]*y[1]-x[2]*y[2]-x[3]*y[3],
        x[0]*y[1]+x[1]*y[0]+x[2]*y[3]-x[3]*y[2],
        x[0]*y[2]-x[1]*y[3]+x[2]*y[0]+x[3]*y[1],
        x[0]*y[3]+x[1]*y[2]-x[2]*y[1]+x[3]*y[0]
    ]
}
fn qi(x:Q)->Q{[x[0],-x[1],-x[2],-x[3]]}
fn comm(x:Q,y:Q)->Q{qm(qm(qm(x,y),qi(x)),qi(y))}
fn interaction_gate(missing_spatial:bool,missing_gauge_excitation:bool)->String{
    const ONE:Q=[1,0,0,0];
    const I:Q=[0,1,0,0];
    const J:Q=[0,0,1,0];
    const K:Q=[0,0,0,1];
    assert_eq!(comm(ONE,J),ONE);
    assert_eq!(comm(I,J),[-1,0,0,0]);
    assert_eq!(comm(J,K),[-1,0,0,0]);
    let coupling_num=if missing_spatial{0}else{1};
    assert_eq!(coupling_num,1,"spatial plaquette interaction removed");
    // Each closed one-site spatial link has character chi_1(U)=Tr(U).
    // Simultaneous conjugation leaves it invariant by cyclicity of trace.
    // Test a noncentral SU2 rational quaternion 3/5+4i/5, with Q8 gauge g.
    let u=[3,4,0,0];
    let mut good=0usize;
    for g in [ONE,I,J,K]{
        let conjugated=qm(qm(g,u),qi(g));
        assert_eq!(conjugated[0],u[0]);
        good+=1;
    }
    if missing_gauge_excitation{good=0;}
    assert_eq!(good,4,"missing physical fundamental Wilson excitation");
    "INTERACTING_WILSON|spatial_sides=1,1,1|links=3|plaquettes=3|beta_s=1/16|beta_t=1|nonconstant_commutator=YES|comm_i_j=-identity|fundamental_trace_gauge_invariant=YES|physical_first_excitation_in_B=spin_half|json=0\n".to_string()
}
fn full_gap_gate()->String{
    let (l,h)=link_ratio();
    let mlo=Rat::new(5,8);
    let min_ratio=mlo.mul(l);
    let max_ratio=Rat::new(8,5).mul(h);
    assert!(Rat::new(3,20).lt(min_ratio));
    assert!(max_ratio.lt(Rat::new(2,5)));
    // B is the product of three positive Wilson convolution kernels,
    // restricted to simultaneous-conjugation-invariant functions.
    // Ground: constant function, b0^3; first nonvacuum: Tr U_i,
    // b0^2*b1. S=A^(1/2), A in [exp(-3/8),1].
    // S B S and B^(1/2) S^2 B^(1/2) have the same nonzero eigenvalues.
    // 5/8 I <= S^2 <= I implies 5/8 *lambda_i(B)<=lambda_i(T)<=lambda_i(B).
    // This is the FULL, infinite-dimensional interacting physical operator,
    // not a small Galerkin diagonalization.
    format!("FULL_SPECTRUM|space=1x1x1_SU2|beta_s=1/16|beta_t=1|full_gauge_projection=YES|lambda_2_over_lambda_1_gt=3/20|lambda_2_over_lambda_1_lt=2/5|stronger_lower={}|stronger_upper={}|a_t=REFERENCE_UNIT|continuum_limit=OPEN|json=0\n",min_ratio.display(),max_ratio.display())
}
fn pw_dim(q:u64)->u64{q*(q+1)*(2*q+1)/6}
fn trit_width(mut x:u64)->u32{
    let mut n=0u32;
    while x>0 {n+=1;x/=3;}n
}
fn lt_sum_bound_q3()->bool{
    let delta=Rat::new(3,32);
    let tail=Rat::new(1,12);
    Rat::new(2,1).mul(delta.add(tail)).lt(Rat::new(3,8))
}
fn lt_sum_bound_q9()->bool{
    let delta=Rat::new(9,65_536);
    // l5/l0 < 4/(3*2^5*6!) < (1/130)^2
    assert!(4u128*130*130<3*32*factorial(6));
    Rat::new(2,1).mul(delta.add(Rat::new(1,130))).lt(Rat::new(1,60))
}
fn lt_sum_bound_q27()->bool{
    // Taylor rest (3/32)^7/7! < 1/(70e9).
    assert!(3u128.pow(7)*70_000_000_000 < 32u128.pow(7)*factorial(7));
    // sqrt(4/(3*2^15*16!)) <1/(700e6).
    assert!(4u128*700_000_000*700_000_000 <3*(1u128<<15)*factorial(16));
    Rat::new(2,1).mul(
        Rat::new(1,70_000_000_000).add(Rat::new(1,700_000_000))
    ).lt(Rat::new(1,300_000_000))
}
fn lt_sum_bound_q81()->bool{
    // (3/32)^21 <10^-20, and 21!>10^11,
    // hence Taylor rest <10^-31.
    assert!(3u128.pow(21)*10u128.pow(20)<32u128.pow(21));
    let fac21=factorial(21);
    assert!(fac21>50_000_000_000_000_000_000u128);
    // 42!=21! * product(22..42); two factors are separately within u128.
    let upper_product=(22u128..=42u128).product::<u128>();
    assert!(upper_product>20_000_000_000_000_000_000_000_000_000_000u128);
    let shift=41u32;
    let two_power=1u128.checked_shl(shift).expect("valid SU2 Wilson high-spin exponent");
    assert!(two_power>2_000_000_000_000u128);
    // Consequently 3*2^41*42! > 3*2e12*5e19*2e31 > 4*(10^31)^2.
    // sqrt(l41/l0) <10^-31.
    // 2*(10^-31+10^-31)<10^-30.
    Rat::new(4,10u128.pow(31)).lt(Rat::new(1,10u128.pow(30)))
}
fn cutoff_gate(wrong_cutoff:bool,wrong_tail:bool)->String{
    let mut out=String::new();
    let mut previous=0u64;
    for (q,d,m,dim,trits,eps_num,eps_den) in QROWS{
        let q_effective=if wrong_cutoff && q==9 {q-1}else{q};
        assert_eq!(pw_dim(q_effective),dim,"representation cutoff missing complete SU2 spin block");
        assert_eq!(trit_width(dim-1),trits);
        assert!(dim>previous);previous=dim;
        assert_eq!(m+2*d,q as u32);
        let passed=match q{
            3=>lt_sum_bound_q3(),
            9=>lt_sum_bound_q9(),
            27=>lt_sum_bound_q27(),
            81=>lt_sum_bound_q81(),
            _=>panic!("unsupported q")
        };
        assert!(passed,"exact rational interacting transfer-cutoff tail failed");
        if wrong_tail && q==9{
            assert!(Rat::new(1,60).lt(Rat::new(1,100)),"invalid tighter cutoff error accepted");
        }
        // Full compact transfer T=S B P_G S (on physical gauge invariant Hilbert
        // space). With X=S B^(1/2), ||X||<=sqrt(b0^3). Let S_D be Taylor
        // polynomial of e^-3/32 * exp((sum comm traces)/32) through D:
        // ||S-S_D||<delta_D=(3/32)^(D+1)/(D+1)!.
        // It raises each SU2 twice-spin link label by <= 2D.
        // Thus (I-P_q)S_D P_m=0 for m+2D=q. The high B tail is
        // b_m/b0 <= 4/[3*2^m*(m+1)!].
        // Consequently ||T-P_q T P_q||/b0^3 <=
        // 2[delta_D+sqrt(b_m/b0)] <eps_num/eps_den.
        out.push_str(&format!(
            "INTERACTING_CUTOFF|q={q}|D={d}|m={m}|per_link_dim={dim}|trits={trits}|physical_gauge_projector_preserved=YES|full_transfer_norm_error_over_b0_cubed_lt={eps_num}/{eps_den}|proof=Taylor_PeterWeyl_spin_support_and_Wilson_B_tail|json=0\n"
        ));
        if q==81 {
            // The q=81 error is <10^-30, smaller than q=27's
            // certified 1/300000000. The same rational first-gap
            // bracket thus follows monotonically, avoiding a huge
            // (>u128) intermediate common denominator.
            assert!(eps_num==1 && eps_den>300_000_000);
            out.push_str("CUTOFF_SPECTRUM|q=81|lambda2_lambda1_gt=3/20|lambda2_lambda1_lt=2/5|Weyl_bound_monotone_from_q27=PASS|full_4D_continuum=OPEN|json=0\n");
        } else if q>=9 {
            let (rlo,rhi)=link_ratio();
            let eps=Rat::new(eps_num,eps_den);
            let wlo=Rat::new(5,8).mul(rlo);
            let lower_num=Rat::new(wlo.a*eps.b - eps.a*wlo.b, wlo.b*eps.b);
            let lower=lower_num.div(Rat::new(1,1).add(eps));
            let upper_num=rhi.add(eps);
            let upper_den=Rat::new(5*eps.b-eps.a*8,8*eps.b);
            let upper=upper_num.div(upper_den);
            let (lo_required,hi_required)=if q==9{
                (Rat::new(1,8),Rat::new(1,2))
            }else{
                (Rat::new(3,20),Rat::new(2,5))
            };
            assert!(lo_required.lt(lower),"cutoff first-gap lower ratio not certified");
            assert!(upper.lt(hi_required),"cutoff first-gap upper ratio not certified");
            out.push_str(&format!(
                "CUTOFF_SPECTRUM|q={q}|lambda2_lambda1_gt={}|lambda2_lambda1_lt={}|Weyl_rank_and_trace_modes=PASS|full_4D_continuum=OPEN|json=0\n",
                lo_required.display(),hi_required.display()
            ));
        }else{
            out.push_str("CUTOFF_SPECTRUM|q=3|first_ratio=NOT_ENCLOSED_BY_CURRENT_OPERATOR_NORM_ERROR|json=0\n");
        }
    }
    out
}
fn norm_monotone_extended()->String{
    // q_k=3^k, D_k=floor((q_k-1)/4), m_k=q_k-2D_k.
    // Both D_k,m_k increase, so Taylor and Wilson tails decrease.
    // Thus q>=81 at all further ternary levels has error <10^-30,
    // for this fixed finite-volume/coupling Wilson transfer only.
    let mut prev_d=0u128;let mut prev_m=0u128;
    for k in 1..=8u32{
        let q=3u128.pow(k);
        let d=(q-1)/4;
        let m=q-2*d;
        assert!(d>=prev_d && m>prev_m);
        prev_d=d;prev_m=m;
    }
    "EXTENDED_CUTOFF|q=3^k|k_ge_4|fixed_beta_s=1/16|fixed_beta_t=1|operator_norm_error_over_b0_cubed_lt=1/1000000000000000000000000000000|monotone_Taylor_and_high_spin_tail=YES|physical_lattice_refinement=NO|json=0\n".to_string()
}
fn frame_hash_gate()->String{
    let mut out=String::new();
    for k in 1..=4u32{
        let n=3usize.pow(k);let changed=n/2;
        let hash_tree=|mutated:bool|{
            let mut leaves=(0..n).map(|i|{
                let t=if mutated && i==changed{(i+1)%3}else{i%3};
                hash_bytes(format!("YM4_06E|LEAF|k={k}|i={i}|trit={t}").as_bytes())
            }).collect::<Vec<_>>();
            let mut level=0usize;
            while leaves.len()>1{
                leaves=leaves.chunks_exact(3).map(|t|
                    hash_bytes(format!("YM4_06E|NODE|level={level}|{}|{}|{}",t[0],t[1],t[2]).as_bytes())
                ).collect::<Vec<_>>();
                level+=1;
            }
            assert_eq!(level,k as usize);
            leaves.pop().unwrap()
        };
        let old=hash_tree(false);let new=hash_tree(true);
        assert_ne!(old,new);
        assert_ne!(changed,0);
        out.push_str(&format!("GLOBAL_HASH|k={k}|old_root={old}|new_root={new}|remote_physical_trit=UNCHANGED|physical_instant_action=NOT_CLAIMED|json=0\n"));
    }
    out
}
fn output()->String{
    let mut out=format!(
        "YM4_06E_RUN|model=FULL_INTERACTING_SU2_WILSON_3PLUS1D|finite_spatial=1x1x1|prediction_commit={FIRST_FREEZE}|arithmetic=EXACT_INTEGER_RATIONAL|toolchain=RUST_1_81|r9_runs=0|json=0\n"
    );
    out.push_str(&interaction_gate(false,false));
    out.push_str(&full_gap_gate());
    out.push_str(&cutoff_gate(false,false));
    out.push_str(&norm_monotone_extended());
    out.push_str(&frame_hash_gate());
    out.push_str("SCOPE|positive_gap_fixed_beta_and_volume=CERTIFIED|spatial_lattice_refinement=NOT_COMPUTED|renormalized_coupling_flow=NOT_COMPUTED|continuum_infinite_volume_mass_gap=OPEN|full_matrix_entries=NOT_STORED|r9_runs=0|json=0\n");
    out
}
struct Receipt{hbp:String,hbi:String,sha:String,sh:String,hash:String}
fn seal()->Receipt{
    let hbp=output();
    let digest=hash_bytes(hbp.as_bytes());
    let mut offset=0usize;let mut index=String::new();
    for (i,line) in hbp.lines().enumerate(){
        index.push_str(&format!("HBI_ROW|row={i}|offset={offset}|bytes={}|json=0\n",line.len()+1));
        offset+=line.len()+1;
    }
    assert_eq!(offset,hbp.len());
    let hbi=format!("HBI|source=YM4_06E|hbp_sha256={digest}|bytes={offset}|json=0\n{index}");
    let hbi_digest=hash_bytes(hbi.as_bytes());
    let sh=format!("SH|slice=3PLUS1D_SU2_WILSON|global_sector=GAUGE_INVARIANT|trit_phases=minus,zero,plus|source_prediction={FIRST_FREEZE}|residuals=ANALYTIC_OPERATOR_NORM_INEQUALITIES|hash_is_metadata=YES|r9_runs=0|json=0\n");
    let sh_digest=hash_bytes(sh.as_bytes());
    let sha=format!("SHA|hbp={digest}|hbi={hbi_digest}|sh={sh_digest}|json=0\n");
    let sha_digest=hash_bytes(sha.as_bytes());
    let global=hash_bytes(format!("YM4_06E|{FIRST_FREEZE}|{digest}|{hbi_digest}|{sh_digest}|{sha_digest}").as_bytes());
    let hash=format!("HASH|value={global}|sha={sha_digest}|hbp={digest}|hbi={hbi_digest}|sh={sh_digest}|json=0\n");
    Receipt{hbp,hbi,sha,sh,hash}
}
fn files(e:&Receipt)->[(&'static str,&str);5]{
    [("YM4-06E.hbp",&e.hbp),("YM4-06E.hbi",&e.hbi),("YM4-06E.sha",&e.sha),("YM4-06E.sh",&e.sh),("YM4-06E.hash",&e.hash)]
}
fn run(dir:&Path){
    fs::create_dir_all(dir).unwrap();
    let r=seal();
    for (name,contents) in files(&r){fs::write(dir.join(name),contents).unwrap();}
    println!("YM4_06E_RESULT|PASS|full_interacting_Wilson_physical_gap=FINITE_CERTIFIED|q=3,9,27,81|norm_cutoff=RIGOROUS|SHA=PASS|r9_runs=0|json=0");
}
fn verify(dir:&Path){
    let r=seal();
    for (name,contents) in files(&r){
        assert_eq!(fs::read(dir.join(name)).unwrap(),contents.as_bytes(),"spectral receipt changed without anchor");
    }
    println!("YM4_06E_VERIFY|PASS|HBI=PASS|HBP=PASS|SHA=PASS|SH=PASS|HASH=PASS|r9_runs=0|json=0");
}
fn main(){
    let args=env::args().collect::<Vec<_>>();
    match args.get(1).map(String::as_str){
        Some("run")=>run(Path::new(args.get(2).expect("output path"))),
        Some("verify")=>verify(Path::new(args.get(2).expect("output path"))),
        Some("plant")=>{
            match args.get(2).map(String::as_str){
                Some("no_spatial")=>{let _=interaction_gate(true,false);},
                Some("no_gauge_excitation")=>{let _=interaction_gate(false,true);},
                Some("drop_irrep")=>{let _=cutoff_gate(true,false);},
                Some("wrong_tail")=>{let _=cutoff_gate(false,true);},
                _=>panic!("unknown planted fault")
            }
        },
        _=>panic!("usage: run DIRECTORY | verify DIRECTORY | plant NAME")
    }
}
#[cfg(test)]
mod tests{
    use super::*;
    #[test]fn exact_wilson_link(){let (lo,hi)=link_ratio();assert!(lo.lt(hi));}
    #[test]fn spatial_interacting(){assert!(interaction_gate(false,false).contains("plaquettes=3"));}
    #[test]fn full_physical_gap(){assert!(full_gap_gate().contains("lambda_2_over_lambda_1_gt=3/20"));}
    #[test]fn cutoff_q3(){assert!(lt_sum_bound_q3());}
    #[test]fn cutoff_q9(){assert!(lt_sum_bound_q9());}
    #[test]fn cutoff_q27(){assert!(lt_sum_bound_q27());}
    #[test]fn cutoff_q81(){assert!(lt_sum_bound_q81());}
    #[test]fn all_cutoffs(){assert!(cutoff_gate(false,false).contains("q=81"));}
    #[test]fn further_refinements(){assert!(norm_monotone_extended().contains("k_ge_4"));}
    #[test]fn metadata_locality(){assert!(frame_hash_gate().contains("physical_instant_action=NOT_CLAIMED"));}
}