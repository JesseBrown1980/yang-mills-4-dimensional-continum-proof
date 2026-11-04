// Recheck of YM4-02c at c32087a, second seat. Separate lattice and group code. Integers only, json=0.
// modes: thm2 GROUP SEED d1 .. dk T [one]   the display of Theorem 2, both sides as integers, complex F, plaquette-dependent weights (or one w)
//        moved                              (Z/2)x(Z/2), Q8, c=8,3,3,3,1: literal 8^8 walk, 17x17 Gram for three reflections
//        signs GROUP d1 d2                  Remark 4.2: every inverse-symmetric sign pattern against homomorphisms, on a slice
//        witness GROUP w.. chi.. d1..dk T   Remark 6.2: literal N_w(chi_rho(W)/W_plus), link reflection
use std::collections::HashMap;
use std::env;

#[derive(Clone)]
struct G {
    n: usize,
    mul: Vec<Vec<u8>>,
    inv: Vec<u8>,
    cls: Vec<u8>,
    ncls: usize,
    one: u8,
}

fn closure<T: Clone + Eq + std::hash::Hash>(gens: &[T], one: T, op: &dyn Fn(&T, &T) -> T) -> G {
    let mut elems = vec![one.clone()];
    let mut index: HashMap<T, usize> = HashMap::new();
    index.insert(one.clone(), 0);
    let mut i = 0;
    while i < elems.len() {
        for g in gens {
            let p = op(&elems[i], g);
            if !index.contains_key(&p) {
                index.insert(p.clone(), elems.len());
                elems.push(p);
            }
        }
        i += 1;
    }
    let n = elems.len();
    let mut mul = vec![vec![0u8; n]; n];
    for a in 0..n {
        for b in 0..n {
            mul[a][b] = index[&op(&elems[a], &elems[b])] as u8;
        }
    }
    finish(mul)
}

fn finish(mul: Vec<Vec<u8>>) -> G {
    let n = mul.len();
    let mut one = 0usize;
    for e in 0..n {
        if (0..n).all(|g| mul[e][g] as usize == g) {
            one = e;
        }
    }
    let mut inv = vec![0u8; n];
    for a in 0..n {
        for b in 0..n {
            if mul[a][b] as usize == one {
                inv[a] = b as u8;
            }
        }
    }
    let mut cls = vec![255u8; n];
    let mut ncls = 0usize;
    for g in 0..n {
        if cls[g] == 255 {
            for h in 0..n {
                let c = mul[mul[h][g] as usize][inv[h] as usize] as usize;
                cls[c] = ncls as u8;
            }
            ncls += 1;
        }
    }
    G { n, mul, inv, cls, ncls, one: one as u8 }
}

fn perm_op(a: &Vec<u8>, b: &Vec<u8>) -> Vec<u8> {
    (0..a.len()).map(|i| a[b[i] as usize]).collect()
}

fn perm_group(k: usize, gens: &[Vec<u8>]) -> G {
    let one: Vec<u8> = (0..k as u8).collect();
    closure(gens, one, &perm_op)
}

fn mat_group(modulus: i32, gens: &[[i32; 4]]) -> G {
    let op = move |a: &[i32; 4], b: &[i32; 4]| -> [i32; 4] {
        [
            (a[0] * b[0] + a[1] * b[2]).rem_euclid(modulus),
            (a[0] * b[1] + a[1] * b[3]).rem_euclid(modulus),
            (a[2] * b[0] + a[3] * b[2]).rem_euclid(modulus),
            (a[2] * b[1] + a[3] * b[3]).rem_euclid(modulus),
        ]
    };
    closure(gens, [1, 0, 0, 1], &op)
}

fn q8() -> G {
    // Signed quaternion units. index = 2*unit + (1 if negative), with unit in 1,i,j,k.
    let table: [[(usize, bool); 4]; 4] = [
        [(0, false), (1, false), (2, false), (3, false)],
        [(1, false), (0, true), (3, false), (2, true)],
        [(2, false), (3, true), (0, true), (1, false)],
        [(3, false), (2, false), (1, true), (0, true)],
    ];
    let mut mul = vec![vec![0u8; 8]; 8];
    for a in 0..8 {
        for b in 0..8 {
            let (ua, sa, ub, sb) = (a / 2, a % 2 == 1, b / 2, b % 2 == 1);
            let (u, s) = table[ua][ub];
            let neg = s ^ sa ^ sb;
            mul[a][b] = (2 * u + if neg { 1 } else { 0 }) as u8;
        }
    }
    finish(mul)
}

fn group(name: &str) -> G {
    match name {
        "Q8" => q8(),
        "Z2" => perm_group(2, &[vec![1, 0]]),
        "Z3" => perm_group(3, &[vec![1, 2, 0]]),
        "Z4" => perm_group(4, &[vec![1, 2, 3, 0]]),
        "S3" => perm_group(3, &[vec![1, 0, 2], vec![1, 2, 0]]),
        "D4" => perm_group(4, &[vec![1, 2, 3, 0], vec![0, 3, 2, 1]]),
        "A4" => perm_group(4, &[vec![1, 2, 0, 3], vec![1, 0, 3, 2]]),
        "S4" => perm_group(4, &[vec![1, 0, 2, 3], vec![1, 2, 3, 0]]),
        "SL23" => mat_group(3, &[[1, 1, 0, 1], [1, 0, 1, 1]]),
        "GL23" => mat_group(3, &[[1, 1, 0, 1], [1, 0, 1, 1], [2, 0, 0, 1]]),
        _ => panic!("group"),
    }
}

struct Lat {
    dims: Vec<usize>,
    nsites: usize,
    nd: usize,
}

impl Lat {
    fn new(dims: Vec<usize>) -> Lat {
        let nsites = dims.iter().product();
        let nd = dims.len();
        Lat { dims, nsites, nd }
    }
    fn coord(&self, s: usize) -> Vec<usize> {
        let mut c = vec![0; self.nd];
        let mut v = s;
        for i in 0..self.nd {
            c[i] = v % self.dims[i];
            v /= self.dims[i];
        }
        c
    }
    fn site(&self, c: &[usize]) -> usize {
        let mut v = 0;
        let mut f = 1;
        for i in 0..self.nd {
            v += c[i] * f;
            f *= self.dims[i];
        }
        v
    }
    fn up(&self, s: usize, mu: usize) -> usize {
        let mut c = self.coord(s);
        c[mu] = (c[mu] + 1) % self.dims[mu];
        self.site(&c)
    }
    fn link(&self, s: usize, mu: usize) -> usize {
        s * self.nd + mu
    }
    fn nlinks(&self) -> usize {
        self.nsites * self.nd
    }
    fn time(&self) -> usize {
        self.nd - 1
    }
    fn t_of(&self, s: usize) -> usize {
        self.coord(s)[self.nd - 1]
    }
    fn word(&self, s: usize, mu: usize, nu: usize) -> [(usize, bool); 4] {
        // U_mu(s) U_nu(s+mu) U_mu(s+nu)^-1 U_nu(s)^-1. true means inverse.
        [
            (self.link(s, mu), false),
            (self.link(self.up(s, mu), nu), false),
            (self.link(self.up(s, nu), mu), true),
            (self.link(s, nu), true),
        ]
    }
    // (theta U)(l) = U(image)^sign with t -> c - t: spatial U_i(x,t) -> U_i(x,c-t); time V(x,t) -> V(x,c-t-1)^-1.
    fn reflect(&self, l: usize, c: i64, no_inverse: bool) -> (usize, bool) {
        let (s, mu) = (l / self.nd, l % self.nd);
        let mut co = self.coord(s);
        let t = co[self.nd - 1] as i64;
        let tt = self.dims[self.nd - 1] as i64;
        if mu != self.time() {
            co[self.nd - 1] = (c - t).rem_euclid(tt) as usize;
            (self.link(self.site(&co), mu), false)
        } else {
            co[self.nd - 1] = (c - t - 1).rem_euclid(tt) as usize;
            (self.link(self.site(&co), mu), !no_inverse)
        }
    }
    fn reflect_plaquette(&self, s: usize, _mu: usize, nu: usize, c: i64) -> usize {
        let mut co = self.coord(s);
        let t = co[self.nd - 1] as i64;
        let tt = self.dims[self.nd - 1] as i64;
        co[self.nd - 1] = if nu == self.time() { (c - t - 1).rem_euclid(tt) } else { (c - t).rem_euclid(tt) } as usize;
        self.site(&co)
    }
}

struct Lcg(u64);

impl Lcg {
    fn below(&mut self, n: i64) -> i64 {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        ((self.0 >> 33) as i64) % n
    }
}

fn sym_weight(g: &G, r: &mut Lcg, range: i64) -> Vec<i64> {
    let mut w = vec![0i64; g.ncls];
    for x in w.iter_mut() {
        *x = r.below(2 * range + 1) - range;
    }
    for x in 0..g.n {
        let (a, b) = (g.cls[x] as usize, g.cls[g.inv[x] as usize] as usize);
        if a < b {
            w[b] = w[a];
        }
    }
    w
}

fn eval(g: &G, word: &[(usize, bool); 4], u: &[u8]) -> usize {
    let mut h = g.one as usize;
    for &(l, inv) in word.iter() {
        let x = if inv { g.inv[u[l] as usize] } else { u[l] } as usize;
        h = g.mul[h][x] as usize;
    }
    g.cls[h] as usize
}

type Plaq = ([(usize, bool); 4], Vec<i64>);

fn thm2(args: &[String]) {
    let g = group(&args[0]);
    let seed: u64 = args[1].parse().unwrap();
    let mut dims: Vec<usize> = vec![];
    let mut one_w = false;
    for a in &args[2..] {
        if a == "one" {
            one_w = true;
        } else {
            dims.push(a.parse().unwrap());
        }
    }
    let lat = Lat::new(dims.clone());
    let tt = *dims.last().unwrap();
    assert!(tt % 2 == 0);
    let m = tt / 2;
    let time = lat.time();
    let nl = lat.nlinks();
    let mut r = Lcg(seed.wrapping_mul(2862933555777941757).wrapping_add(3037000493));
    // Plaquettes, classified from the planes.
    let mut fixed: Vec<Plaq> = vec![];
    let mut upper: Vec<Plaq> = vec![];
    let mut lower: Vec<Plaq> = vec![];
    let mut weights: HashMap<(usize, usize, usize), Vec<i64>> = HashMap::new();
    let shared = sym_weight(&g, &mut r, 3);
    for s in 0..lat.nsites {
        for mu in 0..lat.nd {
            for nu in (mu + 1)..lat.nd {
                let t = lat.t_of(s);
                let w = lat.word(s, mu, nu);
                let key = (s, mu, nu);
                let image = (lat.reflect_plaquette(s, mu, nu, 0), mu, nu);
                let ww = if one_w {
                    shared.clone()
                } else if let Some(x) = weights.get(&image) {
                    x.clone()
                } else {
                    sym_weight(&g, &mut r, 3)
                };
                weights.insert(key, ww.clone());
                if nu == time {
                    if t < m {
                        upper.push((w, ww));
                    } else {
                        lower.push((w, ww));
                    }
                } else if t == 0 || t == m {
                    fixed.push((w, ww));
                } else if t < m {
                    upper.push((w, ww));
                } else {
                    lower.push((w, ww));
                }
            }
        }
    }
    // Closed half: spatial links with 0<=t<=m, time links with base 0<=t<=m-1. C: spatial at t=0,m. A: the rest of the closed half.
    let mut c_links = vec![];
    let mut a_links = vec![];
    for l in 0..nl {
        let (s, mu) = (l / lat.nd, l % lat.nd);
        let t = lat.t_of(s);
        if mu != time {
            if t == 0 || t == m {
                c_links.push(l);
            } else if t < m {
                a_links.push(l);
            }
        } else if t < m {
            a_links.push(l);
        }
    }
    let ch: Vec<usize> = c_links.iter().chain(a_links.iter()).cloned().collect();
    let size = g.n.pow(ch.len() as u32);
    let mut f_re = vec![0i8; size];
    let mut f_im = vec![0i8; size];
    for i in 0..size {
        f_re[i] = (r.below(5) - 2) as i8;
        f_im[i] = (r.below(5) - 2) as i8;
    }
    // Left side, a literal walk over all links.
    let theta: Vec<(usize, bool)> = (0..nl).map(|l| lat.reflect(l, 0, false)).collect();
    let all_plaq: Vec<&Plaq> = fixed.iter().chain(upper.iter()).chain(lower.iter()).collect();
    let mut u = vec![0u8; nl];
    let mut lhs_re: i128 = 0;
    let mut lhs_im: i128 = 0;
    let n = g.n;
    let total: u128 = (n as u128).pow(nl as u32);
    let mut count: u128 = 0;
    loop {
        let mut prod: i64 = 1;
        for p in all_plaq.iter() {
            prod *= p.1[eval(&g, &p.0, &u)];
            if prod == 0 {
                break;
            }
        }
        if prod != 0 {
            let (mut i1, mut i2) = (0usize, 0usize);
            let mut fac = 1usize;
            for &l in ch.iter() {
                i1 += (u[l] as usize) * fac;
                let (img, s) = theta[l];
                let v = if s { g.inv[u[img] as usize] } else { u[img] } as usize;
                i2 += v * fac;
                fac *= n;
            }
            // conj(F(theta U)) F(U)
            let (ar, ai, br, bi) = (f_re[i2] as i64, f_im[i2] as i64, f_re[i1] as i64, f_im[i1] as i64);
            lhs_re += ((ar * br + ai * bi) * prod) as i128;
            lhs_im += ((ar * bi - ai * br) * prod) as i128;
        }
        count += 1;
        let mut k = 0;
        loop {
            if k == nl {
                break;
            }
            u[k] += 1;
            if (u[k] as usize) < n {
                break;
            }
            u[k] = 0;
            k += 1;
        }
        if k == nl {
            break;
        }
    }
    assert!(count == total);
    // Right side: sum_C f(C) |sum_A F W_plus|^2.
    let mut rhs: i128 = 0;
    let mut neg_f: u128 = 0;
    let mut ncs: u128 = 0;
    let mut v = vec![0u8; nl];
    let (nc, na) = (c_links.len(), a_links.len());
    let size_a = n.pow(na as u32);
    let size_c = n.pow(nc as u32);
    for ic in 0..size_c {
        let mut x = ic;
        for &l in c_links.iter() {
            v[l] = (x % n) as u8;
            x /= n;
        }
        let mut f: i64 = 1;
        for p in fixed.iter() {
            f *= p.1[eval(&g, &p.0, &v)];
        }
        ncs += 1;
        if f < 0 {
            neg_f += 1;
        }
        let (mut gr, mut gi): (i128, i128) = (0, 0);
        for ia in 0..size_a {
            let mut y = ia;
            for &l in a_links.iter() {
                v[l] = (y % n) as u8;
                y /= n;
            }
            let mut w: i64 = 1;
            for p in upper.iter() {
                w *= p.1[eval(&g, &p.0, &v)];
                if w == 0 {
                    break;
                }
            }
            if w != 0 {
                let idx = ic + ia * size_c;
                gr += (f_re[idx] as i64 * w) as i128;
                gi += (f_im[idx] as i64 * w) as i128;
            }
        }
        rhs += (f as i128) * (gr * gr + gi * gi);
    }
    println!(
        "THM2|group={}|order={}|dims={:?}|seed={}|one_w={}|links={}|fixed={}|upper={}|lower={}|C_links={}|A_links={}|LHS_re={}|LHS_im={}|RHS={}|equal={}|C_with_f<0={}|of={}|json=0",
        args[0], n, dims, seed, one_w as u8, nl, fixed.len(), upper.len(), lower.len(), nc, na, lhs_re, lhs_im, rhs,
        ((lhs_re == rhs) && (lhs_im == 0)) as u8, neg_f, ncs
    );
}

fn moved() {
    // (Z/2)x(Z/2). Literal walk over 8^8 assignments for each reflection, every F read through the same evaluation of (theta U).
    let g = q8();
    let lat = Lat::new(vec![2, 2]);
    let c = [8i64, 3, 3, 3, 1];
    let mut w_cls = vec![0i64; g.ncls];
    for x in 0..8usize {
        let unit = x / 2;
        let neg = x % 2 == 1;
        let chi_e: i64 = if unit == 0 {
            if neg {
                -2
            } else {
                2
            }
        } else {
            0
        };
        let s = |a: usize| -> i64 {
            if unit == 0 || unit == a {
                1
            } else {
                -1
            }
        };
        w_cls[g.cls[x] as usize] = c[0] + c[1] * s(1) + c[2] * s(2) + c[3] * s(3) + c[4] * chi_e;
    }
    let mut plaq = vec![];
    for s in 0..lat.nsites {
        plaq.push(lat.word(s, 0, 1));
    }
    let nl = lat.nlinks();
    let v00 = lat.link(lat.site(&[0, 0]), 1);
    let v10 = lat.link(lat.site(&[1, 0]), 1);
    let coord = |x: usize| -> (usize, i64) { (x / 2, if x % 2 == 1 { -1 } else { 1 }) };
    let slot = |a: usize, b: usize| -> (usize, i64) {
        let (ma, sa) = coord(a);
        let (mb, sb) = coord(b);
        (1 + 4 * ma + mb, sa * sb)
    };
    for (label, refl_c, no_inv) in [("site_correct", 0i64, false), ("site_inverse_dropped", 0i64, true), ("wrong_plane_c=-1", -1i64, false)] {
        let theta: Vec<(usize, bool)> = (0..nl).map(|l| lat.reflect(l, refl_c, no_inv)).collect();
        let mut gram = vec![vec![0i128; 17]; 17];
        let mut u = vec![0u8; nl];
        loop {
            let mut prod: i64 = 1;
            for p in plaq.iter() {
                prod *= w_cls[eval(&g, p, &u)];
            }
            let (a, b) = (u[v00] as usize, u[v10] as usize);
            let m0 = {
                let (img, s) = theta[v00];
                if s {
                    g.inv[u[img] as usize]
                } else {
                    u[img]
                }
            } as usize;
            let m1 = {
                let (img, s) = theta[v10];
                if s {
                    g.inv[u[img] as usize]
                } else {
                    u[img]
                }
            } as usize;
            let (sb, fb) = slot(a, b);
            let (sa, fa) = slot(m0, m1);
            let p = prod as i128;
            gram[0][0] += p;
            gram[sa][0] += fa as i128 * p;
            gram[0][sb] += fb as i128 * p;
            gram[sa][sb] += (fa * fb) as i128 * p;
            let mut k = 0;
            loop {
                if k == nl {
                    break;
                }
                u[k] += 1;
                if u[k] < 8 {
                    break;
                }
                u[k] = 0;
                k += 1;
            }
            if k == nl {
                break;
            }
        }
        println!("MOVED|reflection={}|denominator=8^8|json=0", label);
        for row in gram.iter() {
            println!("ROW|{}", row.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(","));
        }
    }
}

fn find(p: &mut Vec<usize>, x: usize) -> usize {
    let mut v = x;
    while p[v] != v {
        p[v] = p[p[v]];
        v = p[v];
    }
    v
}

fn signs(args: &[String]) {
    let g = group(&args[0]);
    let dims: Vec<usize> = args[1..].iter().map(|x| x.parse().unwrap()).collect();
    let lat = Lat::new(dims.clone());
    let nl = lat.nlinks();
    let mut plaq = vec![];
    for s in 0..lat.nsites {
        for mu in 0..lat.nd {
            for nu in (mu + 1)..lat.nd {
                plaq.push(lat.word(s, mu, nu));
            }
        }
    }
    // A spanning tree set to the identity: plaquette classes are gauge invariant.
    let mut parent: Vec<usize> = (0..lat.nsites).collect();
    let mut free = vec![];
    for l in 0..nl {
        let (s, mu) = (l / lat.nd, l % lat.nd);
        let (a, b) = (find(&mut parent, s), find(&mut parent, lat.up(s, mu)));
        if a != b {
            parent[a] = b;
        } else {
            free.push(l);
        }
    }
    let mut u = vec![g.one; nl];
    let n = g.n;
    let ncl = g.ncls;
    let mut hist: HashMap<u64, u64> = HashMap::new();
    let mut idx = vec![0usize; free.len()];
    for &l in free.iter() {
        u[l] = 0;
    }
    loop {
        let mut key: u64 = 0;
        for p in plaq.iter() {
            key = key * ncl as u64 + eval(&g, p, &u) as u64;
        }
        *hist.entry(key).or_insert(0) += 1;
        let mut k = 0;
        loop {
            if k == free.len() {
                break;
            }
            idx[k] += 1;
            if idx[k] < n {
                u[free[k]] = idx[k] as u8;
                break;
            }
            idx[k] = 0;
            u[free[k]] = 0;
            k += 1;
        }
        if k == free.len() {
            break;
        }
    }
    let mut inv_cls = vec![0usize; ncl];
    for x in 0..n {
        inv_cls[g.cls[x] as usize] = g.cls[g.inv[x] as usize] as usize;
    }
    let (mut patterns, mut homs, mut agree, mut disagree) = (0u64, 0u64, 0u64, 0u64);
    for mask in 0u64..(1u64 << ncl) {
        let s: Vec<i64> = (0..ncl).map(|k| if mask >> k & 1 == 1 { -1 } else { 1 }).collect();
        if (0..ncl).any(|k| s[k] != s[inv_cls[k]]) {
            continue;
        }
        patterns += 1;
        let base = s[g.cls[g.one as usize] as usize];
        let mut is_hom = true;
        for a in 0..n {
            for b in 0..n {
                if s[g.cls[g.mul[a][b] as usize] as usize] * base != s[g.cls[a] as usize] * s[g.cls[b] as usize] {
                    is_hom = false;
                }
            }
        }
        if is_hom {
            homs += 1;
        }
        let (mut neg, mut pos) = (0u64, 0u64);
        for (&key, &count) in hist.iter() {
            let mut k = key;
            let mut prod = 1i64;
            for _ in 0..plaq.len() {
                prod *= s[(k % ncl as u64) as usize];
                k /= ncl as u64;
            }
            if prod < 0 {
                neg += count;
            } else {
                pos += count;
            }
        }
        let one_signed = neg == 0 || pos == 0;
        if one_signed == is_hom {
            agree += 1;
        } else {
            disagree += 1;
            println!("DISAGREE|group={}|dims={:?}|sign_on_classes={:?}|is_hom={}|neg={}|pos={}|json=0", args[0], dims, s, is_hom as u8, neg, pos);
        }
    }
    println!(
        "SIGNS|group={}|order={}|classes={}|dims={:?}|free_links={}|plaquettes={}|inverse_symmetric_patterns={}|plus_or_minus_homomorphisms={}|one_signed_iff_homomorphism_agree={}|disagree={}|json=0",
        args[0], n, ncl, dims, free.len(), plaq.len(), patterns, homs, agree, disagree
    );
}

fn witness(args: &[String]) {
    // witness GROUP w.. chi.. d1..dk T   w and chi are listed in the class order printed by the classes mode.
    let g = group(&args[0]);
    let ncl = g.ncls;
    let w: Vec<i64> = args[1..1 + ncl].iter().map(|x| x.parse().unwrap()).collect();
    let chi: Vec<i64> = args[1 + ncl..1 + 2 * ncl].iter().map(|x| x.parse().unwrap()).collect();
    let dims: Vec<usize> = args[1 + 2 * ncl..].iter().map(|x| x.parse().unwrap()).collect();
    let lat = Lat::new(dims.clone());
    let tt = *dims.last().unwrap();
    let m = tt / 2;
    let time = lat.time();
    let nl = lat.nlinks();
    // Link reflection c=-1. Upper: spatial 0<=t<=m-1, time-like 0<=t<=m-2. Lower: mirror. Crossing: time-like at t=m-1 and t=T-1.
    let (mut upper, mut lower, mut crossing) = (vec![], vec![], vec![]);
    for s in 0..lat.nsites {
        for mu in 0..lat.nd {
            for nu in (mu + 1)..lat.nd {
                let t = lat.t_of(s);
                let word = lat.word(s, mu, nu);
                if nu == time {
                    if t == m - 1 || t == tt - 1 {
                        crossing.push(word);
                    } else if t < m {
                        upper.push(word);
                    } else {
                        lower.push(word);
                    }
                } else if t < m {
                    upper.push(word);
                } else {
                    lower.push(word);
                }
            }
        }
    }
    // W: the line of length L = dims[0] in direction 0 at t=0, the other coordinates 0.
    let mut line = vec![];
    let mut s0 = 0usize;
    for _ in 0..dims[0] {
        line.push(lat.link(s0, 0));
        s0 = lat.up(s0, 0);
    }
    let theta: Vec<(usize, bool)> = (0..nl).map(|l| lat.reflect(l, -1, false)).collect();
    let mut lcm: i128 = 1;
    for &x in w.iter() {
        let a = x.abs() as i128;
        assert!(a > 0);
        let (mut p, mut q) = (lcm, a);
        while q != 0 {
            let r = p % q;
            p = q;
            q = r;
        }
        lcm = lcm / p * a;
    }
    let d: i128 = lcm.pow(upper.len() as u32);
    let n = g.n;
    let mut u = vec![0u8; nl];
    let mut mu_field = vec![0u8; nl];
    let (mut total, mut z): (i128, i128) = (0, 0);
    loop {
        let (mut wu, mut wl, mut wc): (i128, i128, i128) = (1, 1, 1);
        for p in upper.iter() {
            wu *= w[eval(&g, p, &u)] as i128;
        }
        for p in lower.iter() {
            wl *= w[eval(&g, p, &u)] as i128;
        }
        for p in crossing.iter() {
            wc *= w[eval(&g, p, &u)] as i128;
        }
        let prod_all = wu * wl * wc;
        z += prod_all;
        // F(U) = chi(W(U)) / W_plus(U), and F(theta U) is F read on the mirrored field, a separate evaluation of the same words.
        for l in 0..nl {
            let (img, s) = theta[l];
            mu_field[l] = if s { g.inv[u[img] as usize] } else { u[img] };
        }
        let mut wm: i128 = 1;
        for p in upper.iter() {
            wm *= w[eval(&g, p, &mu_field)] as i128;
        }
        let (mut h1, mut h2) = (g.one as usize, g.one as usize);
        for &l in line.iter() {
            h1 = g.mul[h1][u[l] as usize] as usize;
            h2 = g.mul[h2][mu_field[l] as usize] as usize;
        }
        let f1 = chi[g.cls[h1] as usize] as i128 * d / wu;
        let f2 = chi[g.cls[h2] as usize] as i128 * d / wm;
        total += f1 * f2 * prod_all;
        let mut k = 0;
        loop {
            if k == nl {
                break;
            }
            u[k] += 1;
            if (u[k] as usize) < n {
                break;
            }
            u[k] = 0;
            k += 1;
        }
        if k == nl {
            break;
        }
    }
    println!(
        "WITNESS|group={}|dims={:?}|w={:?}|chi={:?}|links={}|upper={}|lower={}|crossing={}|L={}|scaled_numerator={}|scale_D={}|Z_numerator={}|json=0",
        args[0], dims, w, chi, nl, upper.len(), lower.len(), crossing.len(), dims[0], total, d, z
    );
}

fn classes(args: &[String]) {
    let g = group(&args[0]);
    println!(
        "CLASSES|group={}|order={}|classes={}|sizes={:?}|cls={:?}|one={}|json=0",
        args[0], g.n, g.ncls, (0..g.ncls).map(|k| g.cls.iter().filter(|&&c| c as usize == k).count()).collect::<Vec<_>>(), g.cls, g.one
    );
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    match args[0].as_str() {
        "thm2" => thm2(&args[1..]),
        "moved" => moved(),
        "signs" => signs(&args[1..]),
        "witness" => witness(&args[1..]),
        "classes" => classes(&args[1..]),
        _ => panic!("mode"),
    }
}
