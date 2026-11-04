// Second seat, PR 13, item 3: a route to the d >= 3 statement with no characters, checked by enumeration.
// Fix a maximum-weight spanning forest of the non-loop links, weight = degree in the monomial. Each remaining non-loop link e closes a cycle whose other
// links f have deg f >= deg e, and each plaquette adds at most 2 per power to deg e + deg f, so deg e <= k. A loop link has degree <= k when no plaquette holds it twice.
// This counts, over ALL multisets of plaquettes through K, the largest free degree. Integers only, Rust 1.81, json=0.
//   usage: forest SIDES K
struct Lat {
    sides: Vec<usize>,
    nsites: usize,
    d: usize,
    faces: Vec<[usize; 4]>,
}

impl Lat {
    fn coords(&self, mut s: usize) -> Vec<usize> {
        let mut x = vec![0; self.d];
        for i in (0..self.d).rev() {
            x[i] = s % self.sides[i];
            s /= self.sides[i];
        }
        x
    }
    fn site_of(&self, x: &[usize]) -> usize {
        let mut s = 0;
        for i in 0..self.d {
            s = s * self.sides[i] + x[i];
        }
        s
    }
    fn shift(&self, s: usize, mu: usize) -> usize {
        let mut x = self.coords(s);
        x[mu] = (x[mu] + 1) % self.sides[mu];
        self.site_of(&x)
    }
    fn new(sides: Vec<usize>) -> Lat {
        let d = sides.len();
        let nsites: usize = sides.iter().product();
        let mut l = Lat { sides, nsites, d, faces: vec![] };
        for s in 0..nsites {
            for mu in 0..d {
                for nu in mu + 1..d {
                    let f = [s * d + mu, l.shift(s, mu) * d + nu, l.shift(s, nu) * d + mu, s * d + nu];
                    l.faces.push(f);
                }
            }
        }
        l
    }
}

struct W<'a> {
    lat: &'a Lat,
    kmax: usize,
    deg: Vec<u16>,
    ends: Vec<(usize, usize)>,
    nonloop: Vec<usize>,
    loops: Vec<usize>,
    multisets: u64,
    co_violate: u64,
    loop_violate: u64,
    worst_co_over: i64,
    worst_loop_over: i64,
    tight: u64,
    k: usize,
    parent: Vec<usize>,
    order: Vec<usize>,
}

impl<'a> W<'a> {
    fn leaf(&mut self) {
        self.multisets += 1;
        let k = self.k as i64;
        // Kruskal on non-loop links, heaviest first.
        for (i, p) in self.parent.iter_mut().enumerate() {
            *p = i;
        }
        self.order.clear();
        self.order.extend_from_slice(&self.nonloop);
        let deg = &self.deg;
        self.order.sort_unstable_by(|a, b| deg[*b].cmp(&deg[*a]));
        let mut top_co = 0i64;
        for idx in 0..self.order.len() {
            let l = self.order[idx];
            let (a, b) = self.ends[l];
            let ra = find(&mut self.parent, a);
            let rb = find(&mut self.parent, b);
            if ra != rb {
                self.parent[ra] = rb;
            } else {
                let dv = self.deg[l] as i64;
                if dv > top_co {
                    top_co = dv;
                }
            }
        }
        if top_co > k {
            self.co_violate += 1;
        }
        if top_co == k {
            self.tight += 1;
        }
        if top_co - k > self.worst_co_over {
            self.worst_co_over = top_co - k;
        }
        let mut top_l = 0i64;
        for &l in &self.loops {
            let dv = self.deg[l] as i64;
            if dv > top_l {
                top_l = dv;
            }
        }
        if top_l > k {
            self.loop_violate += 1;
        }
        if top_l - k > self.worst_loop_over {
            self.worst_loop_over = top_l - k;
        }
    }
    fn go(&mut self, start: usize) {
        if self.k > 0 {
            self.leaf();
        }
        if self.k == self.kmax {
            return;
        }
        for f in start..self.lat.faces.len() {
            let ls = self.lat.faces[f];
            for &l in &ls {
                self.deg[l] += 1;
            }
            self.k += 1;
            self.go(f);
            self.k -= 1;
            for &l in &ls {
                self.deg[l] -= 1;
            }
        }
    }
}

fn find(p: &mut [usize], mut x: usize) -> usize {
    while p[x] != x {
        p[x] = p[p[x]];
        x = p[x];
    }
    x
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let sides: Vec<usize> = args[1].split('x').map(|v| v.parse().unwrap()).collect();
    let kmax: usize = args[2].parse().unwrap();
    let lat = Lat::new(sides);
    let nl = lat.nsites * lat.d;
    let mut ends = vec![(0, 0); nl];
    let mut nonloop = vec![];
    let mut loops = vec![];
    for s in 0..lat.nsites {
        for mu in 0..lat.d {
            let l = s * lat.d + mu;
            let t = lat.shift(s, mu);
            ends[l] = (s, t);
            if s == t {
                loops.push(l);
            } else {
                nonloop.push(l);
            }
        }
    }
    let mut w = W {
        lat: &lat,
        kmax,
        deg: vec![0; nl],
        ends,
        nonloop,
        loops,
        multisets: 0,
        co_violate: 0,
        loop_violate: 0,
        worst_co_over: i64::MIN,
        worst_loop_over: i64::MIN,
        tight: 0,
        k: 0,
        parent: vec![0; lat.nsites],
        order: vec![],
    };
    w.go(0);
    println!(
        "FOREST|sides={}|K={}|N_p={}|multisets={}|co_forest_link_over_k={}|largest_co_forest_minus_k={}|co_forest_equal_k={}|loop_link_over_k={}|largest_loop_minus_k={}|json=0",
        args[1], kmax, lat.faces.len(), w.multisets, w.co_violate, w.worst_co_over, w.tight, w.loop_violate, w.worst_loop_over
    );
}
