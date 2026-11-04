// Second seat, PR 13, item 3: exact sums on the multisets above the plain degree bound, on one-side-1 lattices.
// Own lattice, own multiset walk, own gauge forest, own variable elimination, groups from SL(2,q) with no quaternions.
// The Haar value is read from 2I where every free link has degree at most 11 after gauge fixing, which the plain degree lemma makes exact.
// Integers only, no floating point anywhere. Rust 1.81. json=0.
//   usage: over SIDES T THREADS GROUPFILE_TESTED GROUPFILE_REFERENCE
use std::collections::HashMap;
use std::fs;

#[derive(Clone)]
struct Group {
    name: String,
    n: usize,
    p: i64,
    q: i64,
    mult: Vec<u16>,
    inv: Vec<u16>,
    tr: Vec<(i64, i64)>,
    one: u16,
}

fn load(path: &str) -> Group {
    let text = fs::read_to_string(path).expect("group file");
    let mut it = text.split_whitespace();
    let name = it.next().unwrap().to_string();
    let n: usize = it.next().unwrap().parse().unwrap();
    let p: i64 = it.next().unwrap().parse().unwrap();
    let q: i64 = it.next().unwrap().parse().unwrap();
    let one: u16 = it.next().unwrap().parse().unwrap();
    let mut mult = Vec::with_capacity(n * n);
    for _ in 0..n * n {
        mult.push(it.next().unwrap().parse().unwrap());
    }
    let mut inv = Vec::with_capacity(n);
    for _ in 0..n {
        inv.push(it.next().unwrap().parse().unwrap());
    }
    let mut tr = Vec::with_capacity(n);
    for _ in 0..n {
        let a: i64 = it.next().unwrap().parse().unwrap();
        let b: i64 = it.next().unwrap().parse().unwrap();
        tr.push((a, b));
    }
    Group { name, n, p, q, mult, inv, tr, one }
}

struct Lat {
    sides: Vec<usize>,
    nsites: usize,
    d: usize,
    faces: Vec<[usize; 4]>,
}

impl Lat {
    fn site_of(&self, x: &[usize]) -> usize {
        let mut s = 0;
        for i in 0..self.d {
            s = s * self.sides[i] + x[i];
        }
        s
    }
    fn coords(&self, mut s: usize) -> Vec<usize> {
        let mut x = vec![0; self.d];
        for i in (0..self.d).rev() {
            x[i] = s % self.sides[i];
            s /= self.sides[i];
        }
        x
    }
    fn shift(&self, s: usize, mu: usize) -> usize {
        let mut x = self.coords(s);
        x[mu] = (x[mu] + 1) % self.sides[mu];
        self.site_of(&x)
    }
    fn link(&self, s: usize, mu: usize) -> usize {
        s * self.d + mu
    }
    fn new(sides: Vec<usize>) -> Lat {
        let d = sides.len();
        let nsites: usize = sides.iter().product();
        let mut l = Lat { sides, nsites, d, faces: vec![] };
        for s in 0..nsites {
            for mu in 0..d {
                for nu in mu + 1..d {
                    let f = [l.link(s, mu), l.link(l.shift(s, mu), nu), l.link(l.shift(s, nu), mu), l.link(s, nu)];
                    l.faces.push(f);
                }
            }
        }
        l
    }
}

struct Pattern {
    k: usize,
    top: u8,
    rep: Vec<usize>,
    multisets: u64,
}

struct Walk<'a> {
    lat: &'a Lat,
    t: usize,
    deg: Vec<u8>,
    odd: usize,
    stack: Vec<usize>,
    index: HashMap<Vec<u8>, usize>,
    out: Vec<Pattern>,
}

impl<'a> Walk<'a> {
    fn record(&mut self) {
        let top = *self.deg.iter().max().unwrap();
        if (top as usize) <= self.t {
            return;
        }
        let mut ids: HashMap<usize, u8> = HashMap::new();
        let mut key = Vec::with_capacity(self.stack.len() * 4);
        for &f in &self.stack {
            for &l in &self.lat.faces[f] {
                let next = ids.len() as u8;
                let v = *ids.entry(l).or_insert(next);
                key.push(v);
            }
        }
        if let Some(&i) = self.index.get(&key) {
            self.out[i].multisets += 1;
        } else {
            self.index.insert(key, self.out.len());
            self.out.push(Pattern { k: self.stack.len(), top, rep: self.stack.clone(), multisets: 1 });
        }
    }
    fn go(&mut self, start: usize) {
        if !self.stack.is_empty() && self.odd == 0 {
            self.record();
        }
        if self.stack.len() == self.t {
            return;
        }
        let left = self.t - self.stack.len();
        if self.odd > 4 * left {
            return;
        }
        for f in start..self.lat.faces.len() {
            let ls = self.lat.faces[f];
            for &l in &ls {
                self.deg[l] += 1;
                if self.deg[l] % 2 == 1 {
                    self.odd += 1;
                } else {
                    self.odd -= 1;
                }
            }
            self.stack.push(f);
            self.go(f);
            self.stack.pop();
            for &l in &ls {
                self.deg[l] -= 1;
                if self.deg[l] % 2 == 1 {
                    self.odd += 1;
                } else {
                    self.odd -= 1;
                }
            }
        }
    }
}

// A factor: an original word to a power, or a table.
#[derive(Clone)]
enum Kind {
    Word(Vec<(i32, i32)>, usize),
    Table(Vec<(i64, i64)>),
}

#[derive(Clone)]
struct Factor {
    vars: Vec<usize>,
    kind: Kind,
}

struct Ctx {
    n: usize,
    p: i64,
    q: i64,
    mult: Vec<u16>,
    inv: Vec<u16>,
    one: u16,
    powtab: Vec<Vec<(i64, i64)>>, // powtab[m][element]
}

#[inline]
fn rmul(p: i64, q: i64, x: (i64, i64), y: (i64, i64)) -> (i64, i64) {
    (x.0 * y.0 + x.1 * y.1 * q, x.0 * y.1 + x.1 * y.0 + x.1 * y.1 * p)
}

#[inline]
fn eval(c: &Ctx, f: &Factor, vals: &[u16]) -> (i64, i64) {
    match &f.kind {
        Kind::Word(w, m) => {
            let mut h = c.one as usize;
            for &(i, s) in w {
                if i >= 0 {
                    let g = vals[i as usize] as usize;
                    let e = if s > 0 { g } else { c.inv[g] as usize };
                    h = c.mult[h * c.n + e] as usize;
                }
            }
            c.powtab[*m][h]
        }
        Kind::Table(d) => {
            let mut idx = 0usize;
            for &v in &f.vars {
                idx = idx * c.n + vals[v] as usize;
            }
            d[idx]
        }
    }
}

fn ctx_of(g: &Group, kmax: usize) -> Ctx {
    let mut powtab = vec![];
    for m in 0..=kmax {
        let mut row = vec![];
        for e in 0..g.n {
            let mut t = (1i64, 0i64);
            for _ in 0..m {
                t = rmul(g.p, g.q, t, g.tr[e]);
            }
            row.push(t);
        }
        powtab.push(row);
    }
    Ctx { n: g.n, p: g.p, q: g.q, mult: g.mult.clone(), inv: g.inv.clone(), one: g.one, powtab }
}

fn int_pow(b: u128, e: usize) -> u128 {
    let mut r = 1u128;
    for _ in 0..e {
        r *= b;
    }
    r
}

// Variable elimination. Returns None past the budget.
fn contract(c: &Ctx, mut factors: Vec<Factor>, nvars: usize, threads: usize, budget: u128) -> Option<(i128, i128)> {
    let mut remaining: Vec<usize> = (0..nvars).collect();
    while !remaining.is_empty() {
        let mut best: Option<(usize, usize)> = None;
        for &v in &remaining {
            let mut u: Vec<usize> = vec![];
            for f in &factors {
                if f.vars.contains(&v) {
                    for &x in &f.vars {
                        if x != v && !u.contains(&x) {
                            u.push(x);
                        }
                    }
                }
            }
            if best.is_none() || u.len() < best.unwrap().0 {
                best = Some((u.len(), v));
            }
        }
        let (_, v) = best.unwrap();
        remaining.retain(|&x| x != v);
        let mut using = vec![];
        let mut rest = vec![];
        for f in factors.into_iter() {
            if f.vars.contains(&v) {
                using.push(f);
            } else {
                rest.push(f);
            }
        }
        let mut u: Vec<usize> = vec![];
        for f in &using {
            for &x in &f.vars {
                if x != v && !u.contains(&x) {
                    u.push(x);
                }
            }
        }
        u.sort_unstable();
        let size_u = int_pow(c.n as u128, u.len());
        if size_u * c.n as u128 > budget {
            return None;
        }
        let size = size_u as usize;
        let mut data = vec![(0i64, 0i64); size];
        let chunk = size.div_ceil(threads).max(1);
        let using_ref = &using;
        let u_ref = &u;
        std::thread::scope(|sc| {
            for (ci, part) in data.chunks_mut(chunk).enumerate() {
                sc.spawn(move || {
                    let mut vals = vec![0u16; nvars];
                    for (j, slot) in part.iter_mut().enumerate() {
                        let mut idx = ci * chunk + j;
                        for &x in u_ref.iter().rev() {
                            vals[x] = (idx % c.n) as u16;
                            idx /= c.n;
                        }
                        let mut s = (0i64, 0i64);
                        for g in 0..c.n {
                            vals[v] = g as u16;
                            let mut t = (1i64, 0i64);
                            for f in using_ref.iter() {
                                t = rmul(c.p, c.q, t, eval(c, f, &vals));
                                if t == (0, 0) {
                                    break;
                                }
                            }
                            s.0 += t.0;
                            s.1 += t.1;
                        }
                        *slot = s;
                    }
                });
            }
        });
        rest.push(Factor { vars: u, kind: Kind::Table(data) });
        factors = rest;
    }
    let mut r = (1i128, 0i128);
    let vals = vec![0u16; nvars];
    for f in &factors {
        let v = eval(c, f, &vals);
        let (a, b) = (r.0, r.1);
        r = (a * v.0 as i128 + b * v.1 as i128 * c.q as i128, a * v.1 as i128 + b * v.0 as i128 + b * v.1 as i128 * c.p as i128);
    }
    Some(r)
}

fn gcd(a: i128, b: i128) -> i128 {
    let (mut a, mut b) = (a.abs(), b.abs());
    while b != 0 {
        let t = a % b;
        a = b;
        b = t;
    }
    a
}

fn reduced(n: i128, d: i128) -> String {
    let g = gcd(n, d).max(1);
    format!("{}/{}", n / g, d / g)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let sides: Vec<usize> = args[1].split('x').map(|v| v.parse().unwrap()).collect();
    let t: usize = args[2].parse().unwrap();
    let threads: usize = args[3].parse().unwrap();
    let tested = load(&args[4]);
    let refg = load(&args[5]);
    let ref_t: usize = args[6].parse().unwrap();
    let budget: u128 = args[7].parse().unwrap();
    let lat = Lat::new(sides.clone());
    let nlinks = lat.nsites * lat.d;
    let mut w = Walk { lat: &lat, t, deg: vec![0; nlinks], odd: 0, stack: vec![], index: HashMap::new(), out: vec![] };
    w.go(0);
    let patterns = std::mem::take(&mut w.out);
    let total_ms: u64 = patterns.iter().map(|p| p.multisets).sum();
    println!("OVER_WALK|sides={}|t={}|N_p={}|multisets_above_bound={}|patterns={}|json=0", args[1], t, lat.faces.len(), total_ms, patterns.len());
    let cg = ctx_of(&tested, t + 1);
    let cr = ctx_of(&refg, t + 1);
    let mut differ = 0;
    let mut not_measured = 0;
    let mut proxy_bad = 0;
    for pat in &patterns {
        // gauge forest over the links this pattern uses
        let mut links: Vec<usize> = pat.rep.iter().flat_map(|&f| lat.faces[f].iter().copied()).collect();
        links.sort_unstable();
        links.dedup();
        let mut parent: Vec<usize> = (0..lat.nsites).collect();
        fn find(p: &mut Vec<usize>, mut x: usize) -> usize {
            while p[x] != x {
                p[x] = p[p[x]];
                x = p[x];
            }
            x
        }
        let mut fixed = vec![false; nlinks];
        for &l in &links {
            let s = l / lat.d;
            let mu = l % lat.d;
            let a = find(&mut parent, s);
            let b = find(&mut parent, lat.shift(s, mu));
            if a != b {
                parent[a] = b;
                fixed[l] = true;
            }
        }
        let mut idx = vec![-1i32; nlinks];
        let mut nfree = 0usize;
        for &l in &links {
            if !fixed[l] {
                idx[l] = nfree as i32;
                nfree += 1;
            }
        }
        // collapse repeated faces to powers
        let mut factors: Vec<Factor> = vec![];
        let mut seen: Vec<(usize, usize)> = vec![];
        for &f in &pat.rep {
            if let Some(e) = seen.iter_mut().find(|e| e.0 == f) {
                e.1 += 1;
            } else {
                seen.push((f, 1));
            }
        }
        let mut free_deg = vec![0usize; nfree];
        for &(f, m) in &seen {
            let ls = lat.faces[f];
            let word = vec![(idx[ls[0]], 1), (idx[ls[1]], 1), (idx[ls[2]], -1), (idx[ls[3]], -1)];
            let mut vars: Vec<usize> = vec![];
            for &(i, _) in &word {
                if i >= 0 {
                    free_deg[i as usize] += m;
                    if !vars.contains(&(i as usize)) {
                        vars.push(i as usize);
                    }
                }
            }
            vars.sort_unstable();
            factors.push(Factor { vars, kind: Kind::Word(word, m) });
        }
        let top_free = free_deg.iter().copied().max().unwrap_or(0);
        if top_free > ref_t {
            proxy_bad += 1;
            println!("OVER_PROXY_NOT_EXACT|sides={}|k={}|top_free_degree={}|json=0", args[1], pat.k, top_free);
            not_measured += 1;
            continue;
        }
        let vg = contract(&cg, factors.clone(), nfree, threads, budget);
        let vr = contract(&cr, factors, nfree, threads, budget);
        match (vg, vr) {
            (Some(g), Some(r)) => {
                let dg = int_pow(tested.n as u128, nfree) as i128 * (1i128 << pat.k);
                let dr = int_pow(refg.n as u128, nfree) as i128 * (1i128 << pat.k);
                let same = g.1 == 0 && r.1 == 0 && g.0 * int_pow(refg.n as u128, nfree) as i128 == r.0 * int_pow(tested.n as u128, nfree) as i128;
                if !same {
                    differ += 1;
                }
                println!(
                    "OVER2|sides={}|group={}|t={}|k={}|top_degree={}|top_free_degree={}|free={}|multisets={}|G={}|G_surd={}|Haar_by_{}={}|same={}|json=0",
                    args[1], tested.name, t, pat.k, pat.top, top_free, nfree, pat.multisets, reduced(g.0, dg), g.1, refg.name, reduced(r.0, dr), same as i32
                );
            }
            _ => {
                not_measured += 1;
                println!("OVER2_NOT_MEASURED|sides={}|k={}|free={}|reason=BUDGET|json=0", args[1], pat.k, nfree);
            }
        }
    }
    println!(
        "OVER2_CELL|sides={}|group={}|t={}|multisets={}|patterns={}|differ={}|not_measured={}|proxy_not_exact={}|json=0",
        args[1], tested.name, t, total_ms, patterns.len(), differ, not_measured, proxy_bad
    );
}
