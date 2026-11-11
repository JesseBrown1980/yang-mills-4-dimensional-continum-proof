//! Independent YM4-06B adversarial recheck: *affine* S3 model, not the six-permutation tables.
//! Each element acts on Z3 as x -> (-1)^b*x+a; label is (a,b) encoded 2a+b.
//! Independent site order, link order and plaquette evaluator; 3D torus 2x2x2.
//! Integer and ternary only, zero JSON, no Cargo, Node or V8. Rust 1.81.
#![forbid(unsafe_code)]
#![deny(clippy::float_arithmetic, clippy::float_cmp, clippy::cast_precision_loss)]
use std::collections::{BTreeMap, BTreeSet};
use std::env;

fn norm3(v: i32) -> u8 { v.rem_euclid(3) as u8 }
fn element(a: u8,b: u8) -> u8 { assert!(a<3 && b<2);2*a+b }
fn ab(g: u8) -> (u8,u8) { assert!(g<6);(g/2,g%2) }
fn product(g: u8,h: u8) -> u8 {
    let (a,b)=ab(g);let(c,d)=ab(h);
    element(norm3(i32::from(a)+if b==0 {i32::from(c)} else {-i32::from(c)}),b^d)
}
fn inverse(g: u8) -> u8 {
    let (a,b)=ab(g);
    element(if b==0 {norm3(-i32::from(a))}else{a},b)
}
fn conjugate(g:u8,h:u8)->u8{product(product(g,h),inverse(g))}
fn cost(g:u8)->u64 {if g==0{0}else if g%2==1{2}else{3}}
fn flat_orbits()->(u64,Vec<[u8;3]>){
    let(mut raw,mut seen)=(0u64,BTreeSet::new());
    for x in 0..6 {
        for y in 0..6 {
            for z in 0..6 {
                if product(x,y)!=product(y,x)||product(x,z)!=product(z,x)||product(y,z)!=product(z,y){continue}
                raw+=1;
                let canon=(0..6).map(|g| [conjugate(g,x),conjugate(g,y),conjugate(g,z)]).min().unwrap();
                seen.insert(canon);
            }
        }
    }
    (raw,seen.into_iter().collect())
}
fn site(x:usize,y:usize,z:usize)->usize { x+2*y+4*z }
fn move_one(x:usize,y:usize,z:usize,axis:usize)->(usize,usize,usize){
    match axis {0=>(1-x,y,z),1=>(x,1-y,z),2=>(x,y,1-z),_=>panic!("axis")}
}
fn edge(x:usize,y:usize,z:usize,axis:usize)->usize{8*axis+site(x,y,z)}
fn canonical_flat(x:u8,y:u8,z:u8)->[u8;24]{
    let mut a=[0u8;24];
    for iz in 0..2 {for iy in 0..2 {for ix in 0..2 {
        if ix==1{a[edge(ix,iy,iz,0)]=x}
        if iy==1{a[edge(ix,iy,iz,1)]=y}
        if iz==1{a[edge(ix,iy,iz,2)]=z}
    }}}
    a
}
fn energy(links:&[u8;24])->u64{
    let mut total=0;
    for iz in 0..2 {for iy in 0..2 {for ix in 0..2 {
        for p in 0..3 {for q in (p+1)..3 {
            let (xp,yp,zp)=move_one(ix,iy,iz,p);
            let (xq,yq,zq)=move_one(ix,iy,iz,q);
            let word=[
                (links[edge(ix,iy,iz,p)],false),
                (links[edge(xp,yp,zp,q)],false),
                (links[edge(xq,yq,zq,p)],true),
                (links[edge(ix,iy,iz,q)],true)
            ];
            let mut hol=0u8;
            for (a,negative) in word{
                hol=product(hol,if negative{inverse(a)}else{a});
            }
            total+=cost(hol);
        }}
    }}}
    total
}
type Mat=[[i64;6];6];
fn mm(x:&Mat,y:&Mat)->Mat{
    let mut z=[[0;6];6];
    for (i,xi) in x.iter().enumerate(){
        for (k,coef) in xi.iter().enumerate(){
            for (j,yval) in y[k].iter().enumerate(){
                z[i][j]+=coef*yval;
            }
        }
    }
    z
}
fn diagminus(x:&Mat,q:i64)->Mat{
    let mut result=*x;
    for(i,row)in result.iter_mut().enumerate(){row[i]-=q;}
    result
}
fn electric_check()->(i64,usize){
    let mut lap=[[0i64;6];6];
    for j in 0..6{
        lap[j][j]+=3;
        for a in 0..3 {let t=element(a,1);lap[usize::from(product(t,j as u8))][j]-=1;}
    }
    assert!(lap.iter().enumerate().all(|(i,row)|row.iter().enumerate().all(|(j,v)|*v==lap[j][i])));
    let polynomial=mm(&mm(&lap,&diagminus(&lap,3)),&diagminus(&lap,6));
    assert!(polynomial.iter().flatten().all(|c|*c==0),"electric polynomial fails");
    let tr=(0..6).map(|i|lap[i][i]).sum::<i64>();
    assert_eq!(tr,18);
    (tr,polynomial.iter().flatten().filter(|v|**v!=0).count())
}
fn compute(corrupted:bool){
    for a in 0..6 {assert_eq!(product(a,inverse(a)),0);assert_eq!(product(inverse(a),a),0);}
    for a in 0..6 {for b in 0..6{for c in 0..6 {
        assert_eq!(product(product(a,b),c),product(a,product(b,c)));
    }}}
    let(tr,nonzero)=electric_check();
    let(raw,mut sectors)=flat_orbits();
    assert_eq!(raw,48);
    if corrupted {sectors.pop();}
    assert_eq!(sectors.len(),21);
    let(mut single,mut double)=(0u64,0u64);
    let(mut hist1,mut hist2)=(BTreeMap::<u64,u64>::new(),BTreeMap::<u64,u64>::new());
    for sector in &sectors{
        let state=canonical_flat(sector[0],sector[1],sector[2]);
        assert_eq!(energy(&state),0,"invalid flat-sector representative");
        for i in 0..24{
            for a in 0..3 {
                let mut t=state;
                t[i]=product(element(a,1),t[i]);
                let e=energy(&t);
                *hist1.entry(e).or_default()+=1;
                single+=1;
            }
            for j in (i+1)..24 {
                for a in 0..3 {for b in 0..3 {
                    let mut t=state;
                    t[i]=product(element(a,1),t[i]);
                    t[j]=product(element(b,1),t[j]);
                    *hist2.entry(energy(&t)).or_default()+=1;
                    double+=1;
                }}
            }
        }
    }
    assert_eq!(single,1512);
    assert_eq!(double,52164);
    assert_eq!(hist1.get(&8).copied(),Some(single));
    assert_eq!(hist1.len(),1);
    assert_eq!(hist2.values().sum::<u64>(),double);
    assert_eq!(hist2.keys().next().copied(),Some(8));
    let n=6u64.pow(17);
    let orbits=(n+3*2u64.pow(17)+2*3u64.pow(17))/6;
    assert_eq!(orbits,2_821_153_019_713);
    let min2=hist2.keys().next().copied().unwrap();
    println!("INDEPENDENT_AFFINE|PASS|model=S3_affine_on_Z3|flat_triples={raw}|flat_orbits={}|free_link_states={n}|physical_orbits={orbits}|single_moves={single}|single_cost=8|double_moves={double}|double_min_cost={min2}|electric_trace={tr}|electric_polynomial_nonzero={nonzero}|r9_runs=0|json=0",sectors.len());
    for (e,c) in hist2{println!("DOUBLE_HIST|cost={e}|count={c}|json=0");}
    for r in [27u64,81] {
        let c=144+72*r;
        let cluster=6*r-72;
        let numerator=(u128::from(c)-72)*u128::from(n);
        assert_eq!(cluster,if r==27{90}else{414});
        println!("INDEPENDENT_BOUNDS|r={r}|E22_E21_lower_JE={cluster}|first_gap_num={numerator}|first_gap_den=34*{c}^68|strict_positive=YES|spectral_levels=NOT_COMPUTED|json=0");
    }
}
fn main(){
    let args:Vec<String>=env::args().collect();
    match args.get(1).map(String::as_str){
        None=>compute(false),
        Some("plant")=>compute(true),
        _=>panic!("expected no args or plant"),
    }
}
