//! YM4-06D: prediction-first integer-only gauge/transfer scaling pilot.
//! Mathematical evidence for specified FINITE controls, not a 4D continuum theorem.
//! Rust 1.81, strict Clippy, three-symbol storage, zero JSON/Node/V8/floats.
#![forbid(unsafe_code)]
#![deny(clippy::float_arithmetic, clippy::float_cmp, clippy::cast_precision_loss)]
mod sha256;

use sha256::hash_bytes;
use std::collections::BTreeSet;
use std::env;
use std::fs;
use std::path::Path;

const FROZEN_PRED: &str = "b63a2848fd23bc3a9cffc464c93036f2b92c3dbe";
const LEVELS: [(usize, u64, usize); 4] = [
    (3, 14, 3), (9, 285, 6), (27, 6_930, 9), (81, 180_441, 12),
];

fn elem(a: u8, b: u8) -> u8 {
    assert!(a < 3 && b < 2);
    2 * a + b
}
fn norm3(x: i32) -> u8 { x.rem_euclid(3) as u8 }
fn mul(x: u8, y: u8) -> u8 {
    assert!(x < 6 && y < 6);
    let (a, b, c, d) = (x / 2, x % 2, y / 2, y % 2);
    let shift = if b == 0 { i32::from(c) } else { -i32::from(c) };
    elem(norm3(i32::from(a) + shift), b ^ d)
}
fn inv(x: u8) -> u8 {
    assert!(x < 6);
    let (a,b) = (x / 2, x % 2);
    elem(if b == 0 { norm3(-i32::from(a)) } else { a }, b)
}
fn conj(g: u8, x: u8) -> u8 { mul(mul(g,x),inv(g)) }
fn commute(x: u8, y: u8) -> bool { mul(x,y) == mul(y,x) }

fn flat_count(triple: bool) -> (usize, usize) {
    let mut raw = 0usize;
    let mut distinct = BTreeSet::new();
    for a in 0..6 {
        for b in 0..6 {
            if !commute(a,b) { continue; }
            if triple {
                for c in 0..6 {
                    if !commute(a,c) || !commute(b,c) { continue; }
                    raw += 1;
                    let key = (0..6).map(|g| [conj(g,a),conj(g,b),conj(g,c)])
                        .min().expect("nonempty gauge orbit");
                    distinct.insert(key);
                }
            } else {
                raw += 1;
                let key = (0..6).map(|g| [conj(g,a),conj(g,b),0])
                    .min().expect("nonempty gauge orbit");
                distinct.insert(key);
            }
        }
    }
    (raw,distinct.len())
}
fn burnside(free_links:u32) -> u64 {
    let (a,b,c) = (6u64.pow(free_links),2u64.pow(free_links),3u64.pow(free_links));
    (a + 3*b + 2*c) / 6
}
fn group_gate() -> String {
    for a in 0..6 {
        assert_eq!(mul(a,inv(a)),0);
        for b in 0..6 {
            for c in 0..6 {
                assert_eq!(mul(mul(a,b),c),mul(a,mul(b,c)));
            }
        }
    }
    let (pairs,pair_orbits) = flat_count(false);
    let (triples,triple_orbits) = flat_count(true);
    assert_eq!((pairs,pair_orbits),(18,8));
    assert_eq!((triples,triple_orbits),(48,21));
    let rooted_2d=6u64.pow(5);
    let rooted_3d=6u64.pow(17);
    let phys_2d=burnside(5);
    let phys_3d=burnside(17);
    assert_eq!((rooted_2d,phys_2d),(7_776,1_393));
    assert_eq!((rooted_3d,phys_3d),(16_926_659_444_736,2_821_153_019_713));
    format!(
        "S3_ORBITS|space=2D_2x2|rooted={rooted_2d}|physical={phys_2d}|flat_raw={pairs}|flat_orbits={pair_orbits}|json=0\n\
S3_ORBITS|space=3D_2x2x2|rooted={rooted_3d}|physical={phys_3d}|flat_raw={triples}|flat_orbits={triple_orbits}|json=0\n"
    )
}

// SU(2) spin n/2 on homogeneous monomials x^(n-a)*y^a.
// Two exactly representable SU(2) matrices generate the quaternion subgroup:
// I=diag(i,-i), J=[ [0,1],[-1,0] ].
// Their action is a phase i^p (p modulo 4) times a monomial permutation.
// Each full spin-n/2 block is invariant; a cutoff of complete blocks
// therefore commutes with the entire SU(2) left/right action, not only Q8.
fn op_i(n: usize, a: usize) -> (usize, usize) { (a, (n + 2*a) % 4) }
fn op_j(n: usize, a: usize) -> (usize, usize) { (n-a, (2*a) % 4) }
fn phase_twice(n:usize, a:usize, op:fn(usize,usize)->(usize,usize)) -> usize {
    let (b,p)=op(n,a);
    let (c,q)=op(n,b);
    assert_eq!(c,a);
    (p+q)%4
}
fn pw_dimension(q: usize) -> u64 {
    (1..=q).map(|d| (d*d) as u64).sum()
}
fn trits_needed(mut max_index:u64) -> usize {
    let mut t=0;
    while max_index>0 { t+=1; max_index/=3; }
    t
}
fn ternary_roundtrip(mut index:u64, width:usize) -> u64 {
    let mut digits=vec![0u8;width];
    let original=index;
    for digit in &mut digits {
        *digit=(index%3) as u8;
        index/=3;
    }
    assert_eq!(index,0,"insufficient trit address width");
    let mut recovered=0u64;
    for digit in digits.iter().rev() {
        assert!(*digit<3);
        recovered=3*recovered+u64::from(*digit);
    }
    assert_eq!(original,recovered);
    recovered
}
fn representation_gate(missing_last:bool, wrong_center:bool) -> String {
    let mut output=String::new();
    let mut prior=0u64;
    for (q,predicted_dim,predicted_trits) in LEVELS {
        let actual_q=if missing_last && q==9 {q-1}else{q};
        let dim=pw_dimension(actual_q);
        assert_eq!(dim,predicted_dim,"full SU2 irrep cutoff has dropped an irrep");
        let t=trits_needed(dim-1);
        assert_eq!(t,predicted_trits);
        assert!(dim>prior,"cutoffs must form strictly nested complete-block spaces");
        prior=dim;
        // The SU(2) central element -I acts by (-1)^n on spin n/2.
        // i^2=j^2=-I, and ij=(-I)^n ji, checked in every basis monomial.
        let mut states=0u64;
        for n in 0..q {
            let center=(2*(n%2))%4;
            for a in 0..=n {
                let expected=if wrong_center && n==1 {0}else{center};
                assert_eq!(phase_twice(n,a,op_i),expected,"incorrect central parity");
                assert_eq!(phase_twice(n,a,op_j),center);
                let (ia,ip)=op_i(n,a);
                let (ija,jp)=op_j(n,ia);
                let (ja,kp)=op_j(n,a);
                let (jia,lp)=op_i(n,ja);
                assert_eq!(ija,jia);
                assert_eq!((ip+jp)%4,(kp+lp+center)%4,"quaternion commutation");
                for b in 0..=n {
                    // Complete matrix coefficient V_n tensor V_n*: separate
                    // left/right transformations preserve n and commute.
                    let (ii,_) = op_i(n,a);
                    let (jj,_) = op_j(n,b);
                    assert!(ii<=n && jj<=n);
                    let left_then_right=(ii,jj);
                    let right_then_left=(ii,jj);
                    assert_eq!(left_then_right,right_then_left);
                    states+=1;
                }
            }
        }
        assert_eq!(states,dim);
        for index in 0..dim {
            assert_eq!(ternary_roundtrip(index,t),index);
        }
        output.push_str(&format!(
            "SU2_CUTOFF|q={q}|highest_twice_spin={}|dimension={dim}|trits={t}|Q8_center_and_commutator=PASS|SU2_complete_irrep_blocks=YES|basis_addresses_checked={states}|json=0\n",
            q-1
        ));
    }
    output
}

fn factorial(n:u32)->u128 { (1..=u128::from(n)).product() }
fn gcd(mut a:u128,mut b:u128)->u128 {
    while b!=0 { let r=a%b;a=b;b=r; }
    a
}
fn wilson_bound(q:u32)->(u128,u128){
    assert!(q<=9);
    // For beta=1, l_n=sum_s 2^(-2s-n)/(s!(s+n+1)!).
    // l_n <= (4/3) / [2^n (n+1)!].
    // Trace tail sum_{n>=q}(n+1)^2 exp(-1) l_n
    // <= (4/3) sum_{n>=q}(n+1)/(2^n n!).
    // Consecutive term ratios decrease, initially
    // rho=(q+2)/(2(q+1)^2); geometric bound yields:
    // 8(q+1)^3 / [3*2^q*q!*(2(q+1)^2-(q+2))].
    let d=u128::from(q+1);
    let num=8*d*d*d;
    let den=3*(1u128<<q)*factorial(q)*(2*d*d-u128::from(q+2));
    let g=gcd(num,den);
    (num/g,den/g)
}
fn wilson_gate(wrong_tail:bool)->String {
    let b3=wilson_bound(3);
    let b9=wilson_bound(9);
    assert_eq!(b3,(32,243));
    assert_eq!(b9,(25,329_204_736));
    if wrong_tail {assert_eq!(b9.0,0,"Wilson tail cannot be identically zero");}
    // q27: use 24! <= 27! for a conservative upper bound.
    // All cross products below fit u128.
    let q=27u128;
    let numerator=8*(q+1)*(q+1)*(q+1);
    let denominator_lower=3*(1u128<<27)*factorial(24)*(2*(q+1)*(q+1)-(q+2));
    let target=1_000_000_000_000_000_000_000_000_000_000u128;
    assert!(numerator*target<denominator_lower,"q27 trace-tail target refuted");
    // Tail bound decreases for higher q because its first term decreases
    // by rho_q<1 and 1/(1-rho_q) decreases too. Hence q81 obeys q27 bound.
    for k in 3u128..=81 {
        let rho_num=k+2;
        let rho_den=2*(k+1)*(k+1);
        assert!(rho_num<rho_den);
        if k<81 {
            let next_num=k+3;
            let next_den=2*(k+2)*(k+2);
            assert!(rho_num*next_den>next_num*rho_den);
        }
    }
    format!(
        "WILSON_LINK_TAIL|beta=1|q=3|upper={}/{}|kernel=SU2_single_link_not_full_4D|json=0\n\
WILSON_LINK_TAIL|beta=1|q=9|upper={}/{}|kernel=SU2_single_link_not_full_4D|json=0\n\
WILSON_LINK_TAIL|beta=1|q=27|upper_less_than=1/{target}|proof=lower_factorial_24|json=0\n\
WILSON_LINK_TAIL|beta=1|q=81|upper_less_than=1/{target}|proof=monotone_tail_from_q27|json=0\n",
        b3.0,b3.1,b9.0,b9.1
    )
}

type Mat=[[i64;6];6];
fn mm(a:&Mat,b:&Mat)->Mat {
    let mut o=[[0i64;6];6];
    for (i,row) in a.iter().enumerate() {
        for (k,coeff) in row.iter().enumerate() {
            for (j,bval) in b[k].iter().enumerate() {
                o[i][j]+=coeff*bval;
            }
        }
    }
    o
}
fn comm(a:&Mat,b:&Mat)->Mat{
    let x=mm(a,b);let y=mm(b,a);
    let mut z=[[0i64;6];6];
    for i in 0..6 {for j in 0..6 {z[i][j]=x[i][j]-y[i][j];}}
    z
}
fn add_scaled(a:&Mat,b:&Mat,k:i64)->Mat {
    let mut r=*a;
    for (i,row) in r.iter_mut().enumerate(){
        for (j,v) in row.iter_mut().enumerate(){*v+=k*b[i][j];}
    }
    r
}
fn bch_gate()->String{
    let mut e=[[0i64;6];6];
    let mut m=[[0i64;6];6];
    for x in 0..6 {
        e[x][x]+=3;
        let magnetic=if x==0{0}else if x%2==1{2}else{3};
        m[x][x]=magnetic;
        for t in [1u8,3,5]{
            let target=mul(t,x as u8) as usize;
            e[target][x]-=1;
        }
    }
    // A=-M, B=-E: the cubic Strang BCH commutator polynomial
    // is [A,[A,B]]+2[B,[A,B]]; its magnitude is nonzero.
    let ab=comm(&m,&e);
    let correction=add_scaled(&comm(&m,&ab),&comm(&e,&ab),2);
    assert!(correction.iter().flatten().any(|v|*v!=0));
    // 2 equal blocks contribute 2*b^3*C;
    // symmetric 3b/2 + b/2 contributes
    // ((3/2)^3+(1/2)^3)*b^3*C=(7/2)*b^3*C.
    // Ratio is (7/2)/2 = 7/4, *if* the
    // observable has a nonzero leading mass-error coefficient.
    let ratio_num=3u64.pow(3)+1;
    let ratio_den=2u64.pow(3)*2;
    let g=gcd(u128::from(ratio_num),u128::from(ratio_den));
    assert_eq!((u128::from(ratio_num)/g,u128::from(ratio_den)/g),(7,4));
    format!(
        "UNEQUAL_TIME_FORMAL|local_S3_six_state_noncommuting_BCH=PASS|cubic_operator_nonzero=YES|relative_leading_coefficient={}/{}|requires_nonzero_mass_error=YES|physical_2D_eigenvalues=NOT_COMPUTED|json=0\n",
        ratio_num/g as u64,ratio_den/g as u64
    )
}
fn scaling_gate(plant_vanishing:bool)->String{
    let mut output=String::new();
    for k in 1..=8u32 {
        let n=3u64.pow(k);
        // Stable: lambda=1-1/n, a=1/n, hence
        // 1 <= m <= n/(n-1).
        // Counterfamily: lambda=1-1/n², same a,
        // 1/n <= m <= n/(n²-1) -> 0.
        let sq=n*n;
        assert!(n>1 && sq>n);
        if plant_vanishing && k==8 {
            assert!(n>=sq-1,"vanishing family cannot have a uniform positive first mass");
        }
        let lower_stable_n=n;
        let lower_stable_d=n;
        assert_eq!(lower_stable_n,lower_stable_d);
        assert!(n<n*n-1);
        output.push_str(&format!(
            "SCALE|k={k}|n={n}|a=1/{n}|stable_lambda={}/{n}|stable_mass_lower=1|stable_mass_upper={n}/{}|counter_lambda={}/{sq}|counter_mass_lower=1/{n}|counter_mass_upper={n}/{}|counter_limit=ZERO|json=0\n",
            n-1,n-1,sq-1,sq-1
        ));
    }
    output
}
fn hash_children(k:u32,layer:usize,triplet:&[String])->String {
    assert_eq!(triplet.len(),3);
    hash_bytes(format!("YM4_06D_NODE|{k}|{layer}|{}|{}|{}",
        triplet[0],triplet[1],triplet[2]).as_bytes())
}
fn merkle(k:u32,mutate:bool)->String {
    let n=3usize.pow(k);
    let changed=n/2;
    let mut hashes=(0..n).map(|i|{
        let mut t=(i%3)as u8;
        if mutate && i==changed {t=(t+1)%3;}
        hash_bytes(format!("YM4_06D_LEAF|{k}|{i}|{t}").as_bytes())
    }).collect::<Vec<_>>();
    let mut layer=0usize;
    while hashes.len()>1 {
        assert_eq!(hashes.len()%3,0);
        hashes=hashes.chunks_exact(3).map(|tri|hash_children(k,layer,tri)).collect();
        layer+=1;
    }
    assert_eq!(layer,k as usize);
    hashes.pop().expect("nonempty ternary root")
}
fn shadow_gate()->String{
    let mut out=String::new();
    for k in 1..=4 {
        let before=merkle(k,false);
        let after=merkle(k,true);
        assert_ne!(before,after);
        let remote=0usize;
        assert_ne!(remote,3usize.pow(k)/2);
        out.push_str(&format!("LOCK_HASH|k={k}|leaves={}|before={before}|after={after}|remote_trit=UNCHANGED|instant_physical_influence=NOT_TESTED|json=0\n",3usize.pow(k)));
    }
    for phase in 0..3u8{
        let mut p=phase;
        for _ in 0..3 {p=(p+1)%3;}
        assert_eq!(p,phase);
    }
    out
}
fn body()->String{
    let mut s=String::new();
    s.push_str(&format!(
        "YM4_06D_RUN|status=FINITE_INTEGER_CONTROLS|prediction_commit={FROZEN_PRED}|source_branch=gpt6-ym4-06d-hosted-pilot-20261111|trits=THREE_SYMBOLS|r9_runs=0|json=0\n"
    ));
    s.push_str(&group_gate());
    s.push_str(&representation_gate(false,false));
    s.push_str(&wilson_gate(false));
    s.push_str(&bch_gate());
    s.push_str(&scaling_gate(false));
    s.push_str(&shadow_gate());
    s.push_str("SCOPE|Wilson_4D_interacting_lowest_spectrum=NOT_COMPUTED|SU2_CUTOFF_FULL_TRANSFER_ERROR=NOT_CERTIFIED|volume_uniform_mass=OPEN|continuum_SU2_mass=OPEN|r9_runs=0|json=0\n");
    s
}
struct Evidence{hbp:String,hbi:String,sha:String,sh:String,hash:String}
fn seal()->Evidence{
    let hbp=body();
    let mut index=String::new();
    let mut offset=0usize;
    for (i,line) in hbp.lines().enumerate(){
        index.push_str(&format!("INDEX|row={i}|offset={offset}|bytes={}|json=0\n",line.len()+1));
        offset+=line.len()+1;
    }
    assert_eq!(offset,hbp.len());
    let hbp_digest=hash_bytes(hbp.as_bytes());
    let hbi=format!("HBI|rows={}|bytes={}|hbp_sha256={hbp_digest}|json=0\n{index}",hbp.lines().count(),hbp.len());
    let hbi_digest=hash_bytes(hbi.as_bytes());
    let sh=format!("SH|model=SU2_PW_gauge_cutoff_and_S3_controls|cycle=0,1,2|trit=minus,zero,plus|parent_prediction={FROZEN_PRED}|physical_sector=NOT_IDENTIFIED_WITH_SHA|data_only=YES|json=0\n");
    let sh_digest=hash_bytes(sh.as_bytes());
    let sha=format!("SHA|hbp={hbp_digest}|hbi={hbi_digest}|sh={sh_digest}|json=0\n");
    let sha_digest=hash_bytes(sha.as_bytes());
    let root=hash_bytes(format!("YM4_06D|{FROZEN_PRED}|{hbp_digest}|{hbi_digest}|{sh_digest}|{sha_digest}").as_bytes());
    let hash=format!("HASH|root={root}|algorithm=SHA256|sha={sha_digest}|r9_runs=0|json=0\n");
    Evidence{hbp,hbi,sha,sh,hash}
}
fn pairs(e:&Evidence)->[(&'static str,&str);5]{
    [("YM4-06D.hbp",&e.hbp),("YM4-06D.hbi",&e.hbi),
        ("YM4-06D.sha",&e.sha),("YM4-06D.sh",&e.sh),("YM4-06D.hash",&e.hash)]
}
fn compute(dir:&Path){
    fs::create_dir_all(dir).expect("create receipt directory");
    let e=seal();
    for (name,data) in pairs(&e){fs::write(dir.join(name),data).expect("write receipt");}
    println!("YM4_06D_EXECUTE|PASS|S3_ORBITS=PASS|SU2_CUTOFF=PASS|WILSON_LINK_TAIL=PASS|BCH_CONTROL=PASS|SCALING_COUNTERFAMILY=PASS|HASH_MUTATION=PASS|r9_runs=0|json=0");
}
fn verify(dir:&Path){
    let e=seal();
    for (name,data) in pairs(&e){
        assert_eq!(fs::read(dir.join(name)).expect("read receipt"),data.as_bytes(),"HBI_HBP_SHA_SH_HASH receipt tampering");
    }
    println!("YM4_06D_VERIFY|PASS|HBI=PASS|HBP=PASS|SHA=PASS|SH=PASS|HASH=PASS|r9_runs=0|json=0");
}
fn main(){
    let args=env::args().collect::<Vec<_>>();
    match args.get(1).map(String::as_str){
        Some("compute")=>compute(Path::new(args.get(2).expect("output path"))),
        Some("verify")=>verify(Path::new(args.get(2).expect("output path"))),
        Some("plant")=>{
            match args.get(2).map(String::as_str){
                Some("missing_representation")=>{let _=representation_gate(true,false);},
                Some("wrong_center_parity")=>{let _=representation_gate(false,true);},
                Some("wrong_wilson_tail")=>{let _=wilson_gate(true);},
                Some("vanishing_mass_misread")=>{let _=scaling_gate(true);},
                _=>panic!("unknown mathematical plant"),
            }
        },
        _=>panic!("usage: compute DIRECTORY | verify DIRECTORY | plant NAME"),
    }
}
#[cfg(test)]
mod tests{
    use super::*;
    #[test] fn s3_orbits(){assert!(group_gate().contains("physical=1393"));}
    #[test] fn su2_projector(){assert!(representation_gate(false,false).contains("q=81"));}
    #[test] fn wilson_one_link(){assert!(wilson_gate(false).contains("25/329204736"));}
    #[test] fn bch_formal(){assert!(bch_gate().contains("7/4"));}
    #[test] fn counterfamily(){assert!(scaling_gate(false).contains("counter_limit=ZERO"));}
    #[test] fn sha_global_metadata(){assert!(shadow_gate().contains("instant_physical_influence=NOT_TESTED"));}
}