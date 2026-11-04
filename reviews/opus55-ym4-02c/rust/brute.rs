// Second seat's brute force for YM4-02c. Integers only. Written without reading any walker of the builder's beyond its row names.
// Build: rustc +1.81 -C opt-level=3 --edition=2021 brute.rs
// Modes:
//   brute lat GROUP fix|nofix sum W...  -- DIMS...    sum over the lattice of prod_p w(class of U_p); W lists the integer weight on the classes.
//   brute lat GROUP fix|nofix hist      -- DIMS...    dense histogram over the plaquette classes, written to stdout as HIST rows.
//   brute gram12                                       literal 8^12 pass on (Z/3)x(Z/2) with the Wilson lines W0, W1 and the six plaquettes; HIST rows.
//   brute sitemirror                                   for all 8^9 (A, B, V) on (Z/3)x(Z/2), the classes of the lower plaquettes at X = V^-1 against the upper plaquettes.
use std::thread;

#[derive(Clone)]
struct Group {
    order: usize,
    mult: Vec<u8>,
    inv: Vec<u8>,
    cls: Vec<u8>,
    ncls: usize,
    one: u8,
    elems: Vec<[i32; 4]>,
}

fn qmul2(p: [i32; 4], q: [i32; 4]) -> [i32; 4] {
    // Doubled quaternions: the stored value is 2 * q, so the product of two stored values is divided by 2.
    let r = [
        p[0] * q[0] - p[1] * q[1] - p[2] * q[2] - p[3] * q[3],
        p[0] * q[1] + p[1] * q[0] + p[2] * q[3] - p[3] * q[2],
        p[0] * q[2] - p[1] * q[3] + p[2] * q[0] + p[3] * q[1],
        p[0] * q[3] + p[1] * q[2] - p[2] * q[1] + p[3] * q[0],
    ];
    [r[0] / 2, r[1] / 2, r[2] / 2, r[3] / 2]
}

fn build(name: &str) -> Group {
    let mut elems: Vec<[i32; 4]> = Vec::new();
    for a in 0..4 {
        for s in [2, -2] {
            let mut e = [0; 4];
            e[a] = s;
            elems.push(e);
        }
    }
    if name == "2T" {
        for a in [1, -1] {
            for b in [1, -1] {
                for c in [1, -1] {
                    for d in [1, -1] {
                        elems.push([a, b, c, d]);
                    }
                }
            }
        }
    } else if name != "Q8" {
        panic!("group");
    }
    let order = elems.len();
    let find = |e: [i32; 4]| -> u8 { elems.iter().position(|x| *x == e).unwrap() as u8 };
    let mut mult = vec![0u8; order * order];
    for i in 0..order {
        for j in 0..order {
            mult[i * order + j] = find(qmul2(elems[i], elems[j]));
        }
    }
    let inv: Vec<u8> = (0..order).map(|i| find([elems[i][0], -elems[i][1], -elems[i][2], -elems[i][3]])).collect();
    let one = find([2, 0, 0, 0]);
    let mut cls = vec![255u8; order];
    let mut ncls = 0usize;
    for g in 0..order {
        if cls[g] == 255 {
            for h in 0..order {
                let k = mult[(mult[h * order + g] as usize) * order + inv[h] as usize] as usize;
                cls[k] = ncls as u8;
            }
            ncls += 1;
        }
    }
    Group { order, mult, inv, cls, ncls, one, elems }
}

struct Lat {
    dims: Vec<usize>,
    nsites: usize,
    nlinks: usize,
    words: Vec<[(usize, bool); 4]>,
}

fn lattice(dims: &[usize]) -> Lat {
    let n = dims.len();
    let nsites: usize = dims.iter().product();
    let coord = |mut s: usize| -> Vec<usize> {
        let mut x = vec![0; n];
        for i in 0..n {
            x[i] = s % dims[i];
            s /= dims[i];
        }
        x
    };
    let index = |x: &Vec<usize>| -> usize {
        let mut s = 0;
        let mut m = 1;
        for i in 0..n {
            s += x[i] * m;
            m *= dims[i];
        }
        s
    };
    let mut words = Vec::new();
    for s in 0..nsites {
        let x = coord(s);
        for mu in 0..n {
            for nu in mu + 1..n {
                let mut xm = x.clone();
                xm[mu] = (xm[mu] + 1) % dims[mu];
                let mut xn = x.clone();
                xn[nu] = (xn[nu] + 1) % dims[nu];
                words.push([
                    (index(&x) * n + mu, true),
                    (index(&xm) * n + nu, true),
                    (index(&xn) * n + mu, false),
                    (index(&x) * n + nu, false),
                ]);
            }
        }
    }
    Lat { dims: dims.to_vec(), nsites, nlinks: nsites * n, words }
}

fn forest(lat: &Lat) -> Vec<bool> {
    // Scans the links from the highest index down, so the fixed tree differs from a scan upward.
    let n = lat.dims.len();
    let mut parent: Vec<usize> = (0..lat.nsites).collect();
    fn find(p: &mut Vec<usize>, mut v: usize) -> usize {
        while p[v] != v {
            p[v] = p[p[v]];
            v = p[v];
        }
        v
    }
    let shift = |s: usize, mu: usize| -> usize {
        let mut stride = 1;
        for i in 0..mu {
            stride *= lat.dims[i];
        }
        let c = (s / stride) % lat.dims[mu];
        if c + 1 == lat.dims[mu] {
            s - c * stride
        } else {
            s + stride
        }
    };
    let mut fixed = vec![false; lat.nlinks];
    for l in (0..lat.nlinks).rev() {
        let (s, mu) = (l / n, l % n);
        let (a, b) = (find(&mut parent, s), find(&mut parent, shift(s, mu)));
        if a != b {
            parent[a] = b;
            fixed[l] = true;
        }
    }
    fixed
}

struct Plan {
    free: usize,
    due: Vec<Vec<Vec<(usize, bool)>>>, // per depth, the words completed there, each a list of (free slot, forward)
    root_words: usize,
}

fn plan(lat: &Lat, fixed: &[bool]) -> Plan {
    // Links in order of first appearance across the words, so words complete early.
    let mut slot = vec![usize::MAX; lat.nlinks];
    let mut free = 0;
    for w in &lat.words {
        for (l, _) in w.iter() {
            if !fixed[*l] && slot[*l] == usize::MAX {
                slot[*l] = free;
                free += 1;
            }
        }
    }
    let mut due = vec![Vec::new(); free.max(1)];
    let mut root_words = 0;
    for w in &lat.words {
        let v: Vec<(usize, bool)> = w.iter().filter(|(l, _)| !fixed[*l]).map(|(l, f)| (slot[*l], *f)).collect();
        if v.is_empty() {
            root_words += 1;
            continue;
        }
        let d = v.iter().map(|(s, _)| *s).max().unwrap();
        due[d].push(v);
    }
    Plan { free, due, root_words }
}

fn walk_sum(g: &Group, p: &Plan, weight: &[i128], depth: usize, vals: &mut Vec<u8>, inv: &mut Vec<u8>, prod: i128, total: &mut i128) {
    let last = depth + 1 == p.free;
    let n = g.order;
    let here = &p.due[depth];
    for e in 0..n {
        vals[depth] = e as u8;
        inv[depth] = g.inv[e];
        let mut t = prod;
        for w in here {
            let mut h = g.one as usize;
            for (s, f) in w {
                let v = if *f { vals[*s] } else { inv[*s] };
                h = g.mult[h * n + v as usize] as usize;
            }
            t *= weight[g.cls[h] as usize];
        }
        if last {
            *total += t;
        } else if t != 0 {
            walk_sum(g, p, weight, depth + 1, vals, inv, t, total);
        }
    }
}

fn walk_hist(g: &Group, p: &Plan, depth: usize, vals: &mut Vec<u8>, inv: &mut Vec<u8>, key: usize, counts: &mut Vec<u64>) {
    let last = depth + 1 == p.free;
    let n = g.order;
    let base = g.ncls;
    let here = &p.due[depth];
    for e in 0..n {
        vals[depth] = e as u8;
        inv[depth] = g.inv[e];
        let mut k = key;
        for w in here {
            let mut h = g.one as usize;
            for (s, f) in w {
                let v = if *f { vals[*s] } else { inv[*s] };
                h = g.mult[h * n + v as usize] as usize;
            }
            k = k * base + g.cls[h] as usize;
        }
        if last {
            counts[k] += 1;
        } else {
            walk_hist(g, p, depth + 1, vals, inv, k, counts);
        }
    }
}

fn cmd_lat(args: &[String]) {
    let g = build(&args[0]);
    let use_fix = args[1] == "fix";
    let mode = args[2].as_str();
    let sep = args.iter().position(|a| a == "--").unwrap();
    let dims: Vec<usize> = args[sep + 1..].iter().map(|a| a.parse().unwrap()).collect();
    let lat = lattice(&dims);
    let fixed = if use_fix { forest(&lat) } else { vec![false; lat.nlinks] };
    let p = plan(&lat, &fixed);
    println!(
        "LATTICE|dims={:?}|sites={}|links={}|plaquettes={}|fixed={}|free={}|group_order={}|classes={}|json=0",
        dims, lat.nsites, lat.nlinks, lat.words.len(), fixed.iter().filter(|x| **x).count(), p.free, g.order, g.ncls
    );
    for (i, e) in g.elems.iter().enumerate() {
        if g.cls.iter().position(|c| *c == g.cls[i]).unwrap() == i {
            println!("CLASS|index={}|rep_doubled={:?}|size={}|json=0", g.cls[i], e, g.cls.iter().filter(|c| **c == g.cls[i]).count());
        }
    }
    let threads: usize = 8;
    if mode == "sum" {
        let weight: Vec<i128> = args[3..sep].iter().map(|a| a.parse().unwrap()).collect();
        assert_eq!(weight.len(), g.ncls);
        let root: i128 = weight[g.cls[g.one as usize] as usize].pow(p.root_words as u32);
        let shared_g = g.clone();
        let mut handles = Vec::new();
        for t in 0..threads {
            let gg = shared_g.clone();
            let ww = weight.clone();
            let pp = Plan { free: p.free, due: p.due.clone(), root_words: p.root_words };
            handles.push(thread::spawn(move || {
                let mut total: i128 = 0;
                let mut vals = vec![0u8; pp.free];
                let mut inv = vec![0u8; pp.free];
                let here = &pp.due[0];
                for e in (t..gg.order).step_by(threads) {
                    vals[0] = e as u8;
                    inv[0] = gg.inv[e];
                    let mut prod = root;
                    for w in here {
                        let mut h = gg.one as usize;
                        for (s, f) in w {
                            let v = if *f { vals[*s] } else { inv[*s] };
                            h = gg.mult[h * gg.order + v as usize] as usize;
                        }
                        prod *= ww[gg.cls[h] as usize];
                    }
                    if pp.free == 1 {
                        total += prod;
                    } else if prod != 0 {
                        walk_sum(&gg, &pp, &ww, 1, &mut vals, &mut inv, prod, &mut total);
                    }
                }
                total
            }));
        }
        let mut total: i128 = 0;
        for h in handles {
            total += h.join().unwrap();
        }
        println!("SUM|weight={:?}|numerator={}|denominator={}^{}|json=0", weight, total, g.order, p.free);
    } else {
        let size = g.ncls.pow((lat.words.len() - p.root_words) as u32);
        let mut handles = Vec::new();
        for t in 0..threads {
            let gg = g.clone();
            let pp = Plan { free: p.free, due: p.due.clone(), root_words: p.root_words };
            handles.push(thread::spawn(move || {
                let mut counts = vec![0u64; size];
                let mut vals = vec![0u8; pp.free];
                let mut inv = vec![0u8; pp.free];
                let here = &pp.due[0];
                let base = gg.ncls;
                for e in (t..gg.order).step_by(threads) {
                    vals[0] = e as u8;
                    inv[0] = gg.inv[e];
                    let mut k = 0usize;
                    for w in here {
                        let mut h = gg.one as usize;
                        for (s, f) in w {
                            let v = if *f { vals[*s] } else { inv[*s] };
                            h = gg.mult[h * gg.order + v as usize] as usize;
                        }
                        k = k * base + gg.cls[h] as usize;
                    }
                    if pp.free == 1 {
                        counts[k] += 1;
                    } else {
                        walk_hist(&gg, &pp, 1, &mut vals, &mut inv, k, &mut counts);
                    }
                }
                counts
            }));
        }
        let mut merged = vec![0u64; size];
        for h in handles {
            let c = h.join().unwrap();
            for i in 0..size {
                merged[i] += c[i];
            }
        }
        let mut total = 0u64;
        for (k, c) in merged.iter().enumerate() {
            if *c != 0 {
                println!("HIST|key={}|count={}|json=0", k, c);
                total += *c;
            }
        }
        println!("HIST_DONE|root_words={}|words={}|total={}|json=0", p.root_words, lat.words.len(), total);
    }
}

fn cmd_gram12() {
    // (Z/3)x(Z/2) with no gauge fixing. A[x] = U(x,0), B[x] = U(x,1), V[x] = time link from t=0 to t=1, X[x] = time link from t=1 to t=0.
    // Upper plaquette p(x,0) = A[x] V[x+1] B[x]^-1 V[x]^-1. Lower plaquette p(x,1) = B[x] X[x+1] A[x]^-1 X[x]^-1.
    // Key digits: class W0, class W1, then p(0,0), p(1,0), p(2,0), p(0,1), p(1,1), p(2,1).
    let g = build("Q8");
    let mut handles = Vec::new();
    for a0 in 0..8usize {
        let gg = g.clone();
        handles.push(thread::spawn(move || {
            let m = |x: usize, y: usize| -> usize { gg.mult[x * 8 + y] as usize };
            let i = |x: usize| -> usize { gg.inv[x] as usize };
            let c = |x: usize| -> usize { gg.cls[x] as usize };
            let mut counts = vec![0u64; 390625];
            for a1 in 0..8usize {
                for a2 in 0..8usize {
                    let w0 = m(m(a0, a1), a2);
                    for b0 in 0..8usize {
                        for b1 in 0..8usize {
                            for b2 in 0..8usize {
                                let w1 = m(m(b0, b1), b2);
                                let k0 = c(w0) * 5 + c(w1);
                                for v0 in 0..8usize {
                                    for v1 in 0..8usize {
                                        let p00 = c(m(m(m(a0, v1), i(b0)), i(v0)));
                                        for v2 in 0..8usize {
                                            let p10 = c(m(m(m(a1, v2), i(b1)), i(v1)));
                                            let p20 = c(m(m(m(a2, v0), i(b2)), i(v2)));
                                            let k1 = ((k0 * 5 + p00) * 5 + p10) * 5 + p20;
                                            for x0 in 0..8usize {
                                                for x1 in 0..8usize {
                                                    let p01 = c(m(m(m(b0, x1), i(a0)), i(x0)));
                                                    let k2 = k1 * 5 + p01;
                                                    for x2 in 0..8usize {
                                                        let p11 = c(m(m(m(b1, x2), i(a1)), i(x1)));
                                                        let p21 = c(m(m(m(b2, x0), i(a2)), i(x2)));
                                                        counts[(k2 * 5 + p11) * 5 + p21] += 1;
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            counts
        }));
    }
    let mut merged = vec![0u64; 390625];
    for h in handles {
        let c = h.join().unwrap();
        for k in 0..390625 {
            merged[k] += c[k];
        }
    }
    let mut total = 0u64;
    for (k, c) in merged.iter().enumerate() {
        if *c != 0 {
            println!("HIST|key={}|count={}|json=0", k, c);
            total += *c;
        }
    }
    println!("HIST_DONE|total={}|json=0", total);
}

fn cmd_sitemirror() {
    // Site reflection on (Z/3)x(Z/2): F(theta U) reads X[x]^-1 where F(U) reads V[x]. For every (A, B, V), the classes of p(x,1) at X = V^-1 must equal the classes of p(x,0) at V.
    let g = build("Q8");
    let m = |x: usize, y: usize| -> usize { g.mult[x * 8 + y] as usize };
    let i = |x: usize| -> usize { g.inv[x] as usize };
    let c = |x: usize| -> usize { g.cls[x] as usize };
    let mut bad = 0u64;
    let mut total = 0u64;
    for code in 0..(1usize << 27) {
        let d = |n: usize| -> usize { (code >> (3 * n)) & 7 };
        let (a, b, v) = ([d(0), d(1), d(2)], [d(3), d(4), d(5)], [d(6), d(7), d(8)]);
        let x = [i(v[0]), i(v[1]), i(v[2])];
        for s in 0..3 {
            let t = (s + 1) % 3;
            let up = c(m(m(m(a[s], v[t]), i(b[s])), i(v[s])));
            let down = c(m(m(m(b[s], x[t]), i(a[s])), i(x[s])));
            if up != down {
                bad += 1;
            }
        }
        total += 1;
    }
    println!("SITE_MIRROR|assignments={}|mismatches={}|json=0", total, bad);
}

fn cmd_site_c(args: &[String]) {
    // (Z/2)x(Z/1)x(Z/2), site reflection, F = delta_C with C = (C0, C1) the spatial links of the two fixed slices, over all 8^8 C and all time links.
    // N(delta_C) over 8^12 = f(C0) f(C1) g_up(C) g_down(C), each factor from the plaquette words.
    let g = build("Q8");
    let w: Vec<i128> = args.iter().map(|a| a.parse().unwrap()).collect();
    assert_eq!(w.len(), 5);
    let m = |x: usize, y: usize| -> usize { g.mult[x * 8 + y] as usize };
    let i = |x: usize| -> usize { g.inv[x] as usize };
    let c = |x: usize| -> usize { g.cls[x] as usize };
    let dec = |n: usize| -> [usize; 4] { [n & 7, (n >> 3) & 7, (n >> 6) & 7, (n >> 9) & 7] };
    let mut f = vec![0i128; 4096];
    let mut fixed_negative_evaluations = 0u64;
    for n in 0..4096usize {
        let d = dec(n); // U0(0), U0(1), U1(0), U1(1)
        let p0 = c(m(m(m(d[0], d[3]), i(d[0])), i(d[2])));
        let p1 = c(m(m(m(d[1], d[2]), i(d[1])), i(d[3])));
        if w[p0] < 0 { fixed_negative_evaluations += 1; }
        if w[p1] < 0 { fixed_negative_evaluations += 1; }
        f[n] = w[p0] * w[p1];
    }
    let slices_negative = f.iter().filter(|v| **v < 0).count();
    let mut z: i128 = 0;
    let mut lowest: i128 = i128::MAX;
    let mut negatives: u64 = 0;
    let mut mirror_bad: u64 = 0;
    for n0 in 0..4096usize {
        let a = dec(n0);
        for n1 in 0..4096usize {
            let b = dec(n1);
            let mut up: i128 = 0;
            let mut down: i128 = 0;
            for v0 in 0..8usize {
                for v1 in 0..8usize {
                    // Base t=0: U0(x,0) V(x+1) U0(x,1)^-1 V(x)^-1 and U1(x,0) V(x) U1(x,1)^-1 V(x)^-1.
                    let u = w[c(m(m(m(a[0], v1), i(b[0])), i(v0)))] * w[c(m(m(m(a[1], v0), i(b[1])), i(v1)))]
                        * w[c(m(m(m(a[2], v0), i(b[2])), i(v0)))] * w[c(m(m(m(a[3], v1), i(b[3])), i(v1)))];
                    up += u;
                    // Base t=1: U0(x,1) X(x+1) U0(x,0)^-1 X(x)^-1 and U1(x,1) X(x) U1(x,0)^-1 X(x)^-1.
                    let d = w[c(m(m(m(b[0], v1), i(a[0])), i(v0)))] * w[c(m(m(m(b[1], v0), i(a[1])), i(v1)))]
                        * w[c(m(m(m(b[2], v0), i(a[2])), i(v0)))] * w[c(m(m(m(b[3], v1), i(a[3])), i(v1)))];
                    down += d;
                }
            }
            if up != down { mirror_bad += 1; }
            let n = f[n0] * f[n1] * up * down;
            z += n;
            if n < lowest { lowest = n; }
            if n < 0 { negatives += 1; }
        }
    }
    println!("SITE_C|lattice=(Z/2)x(Z/1)x(Z/2)|w={:?}|C=8^8|fixed_plaquette_evaluations_with_w<0={}|slice_products_negative={}|N(delta_C)_lowest_numerator={}|C_with_negative_N={}|up_equals_down_failures={}|Z_numerator={}|denominator=8^12|json=0", w, fixed_negative_evaluations, slices_negative, lowest, negatives, mirror_bad, z);
}

fn cmd_site_blocks(args: &[String]) {
    // (Z/2)x(Z/1)x(Z/2), site reflection, every point function of the closed half: (C0, C1, v0, v1), 8^10 of them.
    // N(delta_(C,v'), delta_(C,v)) = f(C0) f(C1) h_C(v') u_C(v), where u_C(v) is the product over the upper plaquettes and h_C(v') the product over the lower plaquettes at X = v'^-1.
    // Each block is PSD of rank at most one exactly when h_C = u_C and f(C0) f(C1) >= 0. Entries with C != C' vanish because theta fixes C.
    let g = build("Q8");
    let w: Vec<i128> = args.iter().map(|a| a.parse().unwrap()).collect();
    let mut handles = Vec::new();
    for t in 0..8usize {
        let gg = g.clone();
        let ww = w.clone();
        handles.push(thread::spawn(move || {
            let m = |x: usize, y: usize| -> usize { gg.mult[x * 8 + y] as usize };
            let i = |x: usize| -> usize { gg.inv[x] as usize };
            let c = |x: usize| -> usize { gg.cls[x] as usize };
            let dec = |n: usize| -> [usize; 4] { [n & 7, (n >> 3) & 7, (n >> 6) & 7, (n >> 9) & 7] };
            let f = |d: [usize; 4]| -> i128 {
                ww[c(m(m(m(d[0], d[3]), i(d[0])), i(d[2])))] * ww[c(m(m(m(d[1], d[2]), i(d[1])), i(d[3])))]
            };
            let mut mismatches = 0u64;
            let mut negative_prefactor = 0u64;
            let mut points = 0u64;
            for n0 in (t * 512)..((t + 1) * 512) {
                let a = dec(n0);
                let fa = f(a);
                for n1 in 0..4096usize {
                    let b = dec(n1);
                    if fa * f(b) < 0 { negative_prefactor += 1; }
                    for v0 in 0..8usize {
                        for v1 in 0..8usize {
                            let u = ww[c(m(m(m(a[0], v1), i(b[0])), i(v0)))] * ww[c(m(m(m(a[1], v0), i(b[1])), i(v1)))]
                                * ww[c(m(m(m(a[2], v0), i(b[2])), i(v0)))] * ww[c(m(m(m(a[3], v1), i(b[3])), i(v1)))];
                            let (x0, x1) = (i(v0), i(v1));
                            let d = ww[c(m(m(m(b[0], x1), i(a[0])), i(x0)))] * ww[c(m(m(m(b[1], x0), i(a[1])), i(x1)))]
                                * ww[c(m(m(m(b[2], x0), i(a[2])), i(x0)))] * ww[c(m(m(m(b[3], x1), i(a[3])), i(x1)))];
                            if u != d { mismatches += 1; }
                            points += 1;
                        }
                    }
                }
            }
            (mismatches, negative_prefactor, points)
        }));
    }
    let (mut a, mut b, mut c) = (0u64, 0u64, 0u64);
    for h in handles {
        let r = h.join().unwrap();
        a += r.0;
        b += r.1;
        c += r.2;
    }
    println!("SITE_BLOCKS|lattice=(Z/2)x(Z/1)x(Z/2)|w={:?}|point_functions_of_the_closed_half={}|mirror_mismatches={}|C_pairs_with_negative_prefactor={}|json=0", w, c, a, b);
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match args[0].as_str() {
        "lat" => cmd_lat(&args[1..]),
        "gram12" => cmd_gram12(),
        "sitemirror" => cmd_sitemirror(),
        "sitec" => cmd_site_c(&args[1..]),
        "siteblocks" => cmd_site_blocks(&args[1..]),
        _ => panic!("mode"),
    }
}
