//! YM4-03C, stage 2: the engine for the blocked SU(2) action at b = 2 through beta^10.
//!
//! Integers and exact rationals only: i128 numerator/denominator pairs with checked arithmetic,
//! promoted on overflow to the big integers written in this file. Standard library only, one
//! file, built alone by rustc 1.81, as the repository's compiled gate builds every Rust file.
//!
//! The method, as docs/NOTE-YM4-03C-BLOCKED-ACTION.md section 9 plans it, in the polymer form of
//! its section 6: supports connected through off links with every off link in at least two of
//! their plaquettes (Lemma B), grown from the plaquettes at position 0 of one coarse link and
//! keyed by canonical forms under coarse translations x the signed permutations; spins on each
//! support with the per-plaquette multinomial folded into t-series by McKay powers; exact SU(2)
//! Haar integration link by link through the Weingarten matrix of the epsilon-matching basis;
//! readout by coarse Haar projection with a Parseval residual; clusters of incompatible
//! polymers. The Z2 control runs on the same supports before any SU(2) coefficient is read.
//!
//! Run as blocked_action_engine > RECEIPT. The receipt is deterministic; timings go to stderr.
//! SABOTAGE=<mode> plants one error: dropped_multiplicity (the orbit factor of every class),
//! dropped_multinomial (the per-plaquette 1/m!), disconnected_cluster (compatible pairs left in
//! the logarithm), 2i_beyond_degree_11, wrong_sign. Each must stop the run with a FAILED row
//! naming its check.

#![allow(clippy::needless_range_loop)]

use std::cmp::Ordering;
use std::collections::{BTreeMap, BTreeSet, HashMap, HashSet};
use std::hash::{BuildHasherDefault, Hasher};
use std::io::Write as IoWrite;
use std::time::Instant;

// ---------------------------------------------------------------- hashing without randomness

#[derive(Default, Clone, Copy)]
struct Fx(u64);

impl Hasher for Fx {
    fn finish(&self) -> u64 {
        self.0
    }
    fn write(&mut self, bytes: &[u8]) {
        for &b in bytes {
            self.0 = (self.0.rotate_left(5) ^ b as u64).wrapping_mul(0x517c_c1b7_2722_0a95);
        }
    }
    fn write_u8(&mut self, v: u8) {
        self.write_u64(v as u64);
    }
    fn write_u16(&mut self, v: u16) {
        self.write_u64(v as u64);
    }
    fn write_u32(&mut self, v: u32) {
        self.write_u64(v as u64);
    }
    fn write_u64(&mut self, v: u64) {
        self.0 = (self.0.rotate_left(5) ^ v).wrapping_mul(0x517c_c1b7_2722_0a95);
    }
    fn write_usize(&mut self, v: usize) {
        self.write_u64(v as u64);
    }
}

type FxB = BuildHasherDefault<Fx>;

// ---------------------------------------------------------------- big integers

fn mag_trim(v: &mut Vec<u32>) {
    while let Some(&0) = v.last() {
        v.pop();
    }
}

fn mag_cmp(a: &[u32], b: &[u32]) -> Ordering {
    if a.len() != b.len() {
        return a.len().cmp(&b.len());
    }
    for i in (0..a.len()).rev() {
        if a[i] != b[i] {
            return a[i].cmp(&b[i]);
        }
    }
    Ordering::Equal
}

fn mag_add(a: &[u32], b: &[u32]) -> Vec<u32> {
    let n = a.len().max(b.len());
    let mut out = Vec::with_capacity(n + 1);
    let mut carry = 0u64;
    for i in 0..n {
        let s = carry + *a.get(i).unwrap_or(&0) as u64 + *b.get(i).unwrap_or(&0) as u64;
        out.push((s & 0xffff_ffff) as u32);
        carry = s >> 32;
    }
    if carry > 0 {
        out.push(carry as u32);
    }
    out
}

fn mag_sub(a: &[u32], b: &[u32]) -> Vec<u32> {
    let mut out = Vec::with_capacity(a.len());
    let mut borrow = 0i64;
    for i in 0..a.len() {
        let mut s = a[i] as i64 - borrow - *b.get(i).unwrap_or(&0) as i64;
        if s < 0 {
            s += 1i64 << 32;
            borrow = 1;
        } else {
            borrow = 0;
        }
        out.push(s as u32);
    }
    mag_trim(&mut out);
    out
}

fn mag_mul(a: &[u32], b: &[u32]) -> Vec<u32> {
    if a.is_empty() || b.is_empty() {
        return Vec::new();
    }
    let mut out = vec![0u32; a.len() + b.len()];
    for i in 0..a.len() {
        let mut carry = 0u64;
        for j in 0..b.len() {
            let cur = out[i + j] as u64 + a[i] as u64 * b[j] as u64 + carry;
            out[i + j] = (cur & 0xffff_ffff) as u32;
            carry = cur >> 32;
        }
        let mut k = i + b.len();
        while carry > 0 {
            let cur = out[k] as u64 + carry;
            out[k] = (cur & 0xffff_ffff) as u32;
            carry = cur >> 32;
            k += 1;
        }
    }
    mag_trim(&mut out);
    out
}

fn mag_divrem(a: &[u32], b: &[u32]) -> (Vec<u32>, Vec<u32>) {
    assert!(!b.is_empty(), "division by zero");
    if mag_cmp(a, b) == Ordering::Less {
        return (Vec::new(), a.to_vec());
    }
    if b.len() == 1 {
        let d = b[0] as u64;
        let mut q = vec![0u32; a.len()];
        let mut r = 0u64;
        for i in (0..a.len()).rev() {
            let cur = (r << 32) | a[i] as u64;
            q[i] = (cur / d) as u32;
            r = cur % d;
        }
        mag_trim(&mut q);
        let mut rv = vec![r as u32];
        mag_trim(&mut rv);
        return (q, rv);
    }
    let bits = a.len() * 32;
    let mut q = vec![0u32; a.len()];
    let mut r: Vec<u32> = Vec::new();
    for bit in (0..bits).rev() {
        let mut carry = (a[bit / 32] >> (bit % 32)) & 1;
        for limb in r.iter_mut() {
            let next = *limb >> 31;
            *limb = (*limb << 1) | carry;
            carry = next;
        }
        if carry > 0 {
            r.push(carry);
        }
        if mag_cmp(&r, b) != Ordering::Less {
            r = mag_sub(&r, b);
            q[bit / 32] |= 1 << (bit % 32);
        }
    }
    mag_trim(&mut q);
    (q, r)
}

#[derive(Clone, PartialEq, Eq, Hash, Debug, Default)]
struct Big {
    neg: bool,
    mag: Vec<u32>,
}

impl Big {
    fn from_u128(mut v: u128) -> Big {
        let mut mag = Vec::new();
        while v > 0 {
            mag.push((v & 0xffff_ffff) as u32);
            v >>= 32;
        }
        Big { neg: false, mag }
    }
    fn from_i128(v: i128) -> Big {
        let mut b = Big::from_u128(v.unsigned_abs());
        b.neg = v < 0 && !b.mag.is_empty();
        b
    }
    fn is_zero(&self) -> bool {
        self.mag.is_empty()
    }
    fn to_i128(&self) -> Option<i128> {
        if self.mag.len() > 4 {
            return None;
        }
        let mut u: u128 = 0;
        for (k, &l) in self.mag.iter().enumerate() {
            u |= (l as u128) << (32 * k);
        }
        if u > i128::MAX as u128 {
            return None;
        }
        let s = u as i128;
        Some(if self.neg { -s } else { s })
    }
    fn negate(&self) -> Big {
        Big {
            neg: !self.neg && !self.mag.is_empty(),
            mag: self.mag.clone(),
        }
    }
    fn add(&self, o: &Big) -> Big {
        if self.neg == o.neg {
            let mag = mag_add(&self.mag, &o.mag);
            Big {
                neg: self.neg && !mag.is_empty(),
                mag,
            }
        } else {
            match mag_cmp(&self.mag, &o.mag) {
                Ordering::Equal => Big::default(),
                Ordering::Greater => Big {
                    neg: self.neg,
                    mag: mag_sub(&self.mag, &o.mag),
                },
                Ordering::Less => Big {
                    neg: o.neg,
                    mag: mag_sub(&o.mag, &self.mag),
                },
            }
        }
    }
    fn mul(&self, o: &Big) -> Big {
        let mag = mag_mul(&self.mag, &o.mag);
        Big {
            neg: (self.neg != o.neg) && !mag.is_empty(),
            mag,
        }
    }
    fn divrem(&self, o: &Big) -> (Big, Big) {
        let (q, r) = mag_divrem(&self.mag, &o.mag);
        (
            Big {
                neg: (self.neg != o.neg) && !q.is_empty(),
                mag: q,
            },
            Big {
                neg: self.neg && !r.is_empty(),
                mag: r,
            },
        )
    }
    fn gcd(a: &Big, b: &Big) -> Big {
        let mut x = Big {
            neg: false,
            mag: a.mag.clone(),
        };
        let mut y = Big {
            neg: false,
            mag: b.mag.clone(),
        };
        while !y.is_zero() {
            let (_, r) = x.divrem(&y);
            x = y;
            y = r;
        }
        x
    }
    fn dec(&self) -> String {
        if self.mag.is_empty() {
            return "0".to_string();
        }
        let mut chunks: Vec<u32> = Vec::new();
        let mut cur = self.mag.clone();
        while !cur.is_empty() {
            let (q, r) = mag_divrem(&cur, &[1_000_000_000]);
            chunks.push(*r.first().unwrap_or(&0));
            cur = q;
        }
        let mut s = String::new();
        if self.neg {
            s.push('-');
        }
        s.push_str(&chunks[chunks.len() - 1].to_string());
        for k in (0..chunks.len() - 1).rev() {
            let t = chunks[k].to_string();
            for _ in t.len()..9 {
                s.push('0');
            }
            s.push_str(&t);
        }
        s
    }
}

// ---------------------------------------------------------------- exact rationals

#[derive(Clone, PartialEq, Eq, Hash, Debug)]
enum Q {
    S(i128, i128),
    B(Box<(Big, Big)>),
}

fn gcd_u(mut a: u128, mut b: u128) -> u128 {
    while b != 0 {
        let t = a % b;
        a = b;
        b = t;
    }
    a
}

fn small_add(an: i128, ad: i128, bn: i128, bd: i128) -> Option<Q> {
    let g = gcd_u(ad as u128, bd as u128) as i128;
    let x = an.checked_mul(bd / g)?;
    let y = bn.checked_mul(ad / g)?;
    let n = x.checked_add(y)?;
    let d = (ad / g).checked_mul(bd)?;
    Q::small(n, d)
}

fn small_mul(an: i128, ad: i128, bn: i128, bd: i128) -> Option<Q> {
    let g1 = gcd_u(an.unsigned_abs(), bd as u128) as i128;
    let g2 = gcd_u(bn.unsigned_abs(), ad as u128) as i128;
    let n = (an / g1).checked_mul(bn / g2)?;
    let d = (ad / g2).checked_mul(bd / g1)?;
    Q::small(n, d)
}

impl Q {
    fn zero() -> Q {
        Q::S(0, 1)
    }
    fn one() -> Q {
        Q::S(1, 1)
    }
    fn int(v: i128) -> Q {
        Q::frac(v, 1)
    }
    fn frac(n: i128, d: i128) -> Q {
        match Q::small(n, d) {
            Some(q) => q,
            None => Q::from_big(Big::from_i128(n), Big::from_i128(d)),
        }
    }
    fn small(n: i128, d: i128) -> Option<Q> {
        assert!(d != 0, "zero denominator");
        if n == i128::MIN || d == i128::MIN {
            return None;
        }
        let (n, d) = if d < 0 { (-n, -d) } else { (n, d) };
        if n == 0 {
            return Some(Q::S(0, 1));
        }
        let g = gcd_u(n.unsigned_abs(), d as u128) as i128;
        Some(Q::S(n / g, d / g))
    }
    fn from_big(n: Big, d: Big) -> Q {
        assert!(!d.is_zero(), "zero denominator");
        if n.is_zero() {
            return Q::zero();
        }
        let g = Big::gcd(&n, &d);
        let (mut n, _) = n.divrem(&g);
        let (mut d, _) = d.divrem(&g);
        if d.neg {
            n = n.negate();
            d = d.negate();
        }
        if let (Some(a), Some(b)) = (n.to_i128(), d.to_i128()) {
            return Q::S(a, b);
        }
        Q::B(Box::new((n, d)))
    }
    fn parts(&self) -> (Big, Big) {
        match self {
            Q::S(n, d) => (Big::from_i128(*n), Big::from_i128(*d)),
            Q::B(b) => (b.0.clone(), b.1.clone()),
        }
    }
    fn is_zero(&self) -> bool {
        matches!(self, Q::S(0, _))
    }
    fn add(&self, o: &Q) -> Q {
        if let (Q::S(an, ad), Q::S(bn, bd)) = (self, o) {
            if let Some(q) = small_add(*an, *ad, *bn, *bd) {
                return q;
            }
        }
        let (an, ad) = self.parts();
        let (bn, bd) = o.parts();
        Q::from_big(an.mul(&bd).add(&bn.mul(&ad)), ad.mul(&bd))
    }
    fn neg(&self) -> Q {
        match self {
            Q::S(n, d) => Q::S(-n, *d),
            Q::B(b) => Q::B(Box::new((b.0.negate(), b.1.clone()))),
        }
    }
    fn sub(&self, o: &Q) -> Q {
        self.add(&o.neg())
    }
    fn mul(&self, o: &Q) -> Q {
        if let (Q::S(an, ad), Q::S(bn, bd)) = (self, o) {
            if *an == 0 || *bn == 0 {
                return Q::zero();
            }
            if let Some(q) = small_mul(*an, *ad, *bn, *bd) {
                return q;
            }
        }
        let (an, ad) = self.parts();
        let (bn, bd) = o.parts();
        Q::from_big(an.mul(&bn), ad.mul(&bd))
    }
    fn inv(&self) -> Q {
        let (n, d) = self.parts();
        Q::from_big(d, n)
    }
    fn div(&self, o: &Q) -> Q {
        self.mul(&o.inv())
    }
    fn show(&self) -> String {
        match self {
            Q::S(n, 1) => n.to_string(),
            Q::S(n, d) => n.to_string() + "/" + &d.to_string(),
            Q::B(b) => {
                if b.1.mag == [1] {
                    b.0.dec()
                } else {
                    b.0.dec() + "/" + &b.1.dec()
                }
            }
        }
    }
}

fn pow2_inv(k: usize) -> Q {
    let mut q = Q::one();
    for _ in 0..k {
        q = q.mul(&Q::frac(1, 2));
    }
    q
}

// ---------------------------------------------------------------- power series in beta

const TOPS: usize = 12;

#[derive(Clone, Debug, PartialEq)]
struct Ser(Vec<Q>);

impl Default for Ser {
    fn default() -> Ser {
        Ser::zero()
    }
}

impl Ser {
    fn zero() -> Ser {
        Ser(vec![Q::zero(); TOPS + 1])
    }
    fn one() -> Ser {
        let mut s = Ser::zero();
        s.0[0] = Q::one();
        s
    }
    fn add(&self, o: &Ser) -> Ser {
        Ser(self
            .0
            .iter()
            .zip(o.0.iter())
            .map(|(a, b)| a.add(b))
            .collect())
    }
    fn scale(&self, c: &Q) -> Ser {
        Ser(self.0.iter().map(|a| a.mul(c)).collect())
    }
    fn mul(&self, o: &Ser) -> Ser {
        let mut out = Ser::zero();
        for i in 0..=TOPS {
            if self.0[i].is_zero() {
                continue;
            }
            for k in 0..=(TOPS - i) {
                if !o.0[k].is_zero() {
                    out.0[i + k] = out.0[i + k].add(&self.0[i].mul(&o.0[k]));
                }
            }
        }
        out
    }
    fn inv(&self) -> Ser {
        let mut out = Ser::zero();
        out.0[0] = self.0[0].inv();
        for k in 1..=TOPS {
            let mut s = Q::zero();
            for i in 1..=k {
                s = s.add(&self.0[i].mul(&out.0[k - i]));
            }
            out.0[k] = s.neg().mul(&out.0[0]);
        }
        out
    }
}

/// N[m][n]: closed walks of the SU(2) McKay graph, the multiplicity of spin n/2 in (1/2)^m.
fn mckay(mmax: usize) -> Vec<Vec<i128>> {
    let mut rows = vec![vec![0i128; mmax + 2]; mmax + 1];
    rows[0][0] = 1;
    for m in 0..mmax {
        for n in 0..=m {
            let v = rows[m][n];
            if v != 0 {
                if n >= 1 {
                    rows[m + 1][n - 1] += v;
                }
                rows[m + 1][n + 1] += v;
            }
        }
    }
    rows
}

/// wt[n] = c_n / c_0 = (n + 1) t_(n+1): the activity of one plaquette at spin n/2, the
/// per-plaquette multinomial 1/m! folded by the McKay powers: c_n = sum_m beta^m N_m(n)/(2^m m!).
fn spin_weights() -> Vec<Ser> {
    let nk = mckay(TOPS);
    let mut fact: Vec<i128> = vec![1; TOPS + 1];
    let drop = sabotage() == "dropped_multinomial";
    for m in 1..=TOPS {
        fact[m] = if drop { 1 } else { fact[m - 1] * m as i128 };
    }
    let mut c: Vec<Ser> = Vec::new();
    for n in 0..=TOPS {
        let mut s = Ser::zero();
        for m in n..=TOPS {
            if nk[m][n] != 0 {
                s.0[m] = Q::frac(nk[m][n], (1i128 << m) * fact[m]);
            }
        }
        c.push(s);
    }
    let inv0 = c[0].inv();
    c.iter().map(|s| s.mul(&inv0)).collect()
}

// ---------------------------------------------------------------- the lattice, doubled coordinates

const VOFF: u32 = 1 << 20;

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash)]
struct G {
    perm: [usize; 4],
    sign: [i32; 4],
}

struct Lat {
    d: usize,
    n: [i32; 4],
    m: [i32; 4],
    stride: [usize; 4],
    plaq_cell: Vec<u32>,
    cell_plaq: Vec<u32>,
    link_cell: Vec<u32>,
    cell_link: Vec<u32>,
    plaq_links: Vec<[u32; 4]>,
    link_plaqs: Vec<Vec<u32>>,
    link_kind: Vec<u8>,
    link_coarse: Vec<u32>,
    cm: [i32; 4],
    cstride: [usize; 4],
    pg: Vec<G>,
    pos_v: u8,
}

fn permutations(d: usize) -> Vec<Vec<usize>> {
    if d == 0 {
        return vec![Vec::new()];
    }
    let mut out = Vec::new();
    for p in permutations(d - 1) {
        for k in 0..=p.len() {
            let mut q = p.clone();
            q.insert(k, d - 1);
            out.push(q);
        }
    }
    out.sort();
    out
}

impl Lat {
    fn new(d: usize, n: [i32; 4], pos_v: u8) -> Lat {
        let mut m = [1i32; 4];
        let mut cm = [1i32; 4];
        for k in 0..d {
            assert!(n[k] % 2 == 0 && n[k] >= 2, "fine sides even");
            m[k] = 2 * n[k];
            cm[k] = n[k];
        }
        let mut stride = [0usize; 4];
        let mut cstride = [0usize; 4];
        let mut acc = 1usize;
        let mut cacc = 1usize;
        for k in 0..4 {
            stride[k] = acc;
            cstride[k] = cacc;
            if k < d {
                acc *= m[k] as usize;
                cacc *= cm[k] as usize;
            }
        }
        let ncell = acc;
        let mut lat = Lat {
            d,
            n,
            m,
            stride,
            plaq_cell: Vec::new(),
            cell_plaq: vec![u32::MAX; ncell],
            link_cell: Vec::new(),
            cell_link: vec![u32::MAX; ncell],
            plaq_links: Vec::new(),
            link_plaqs: Vec::new(),
            link_kind: Vec::new(),
            link_coarse: Vec::new(),
            cm,
            cstride,
            pg: Vec::new(),
            pos_v,
        };
        for cell in 0..ncell {
            let c = lat.coords(cell);
            let odd = (0..d).filter(|&k| c[k] % 2 != 0).count();
            if odd == 1 {
                lat.cell_link[cell] = lat.link_cell.len() as u32;
                lat.link_cell.push(cell as u32);
            } else if odd == 2 {
                lat.cell_plaq[cell] = lat.plaq_cell.len() as u32;
                lat.plaq_cell.push(cell as u32);
            }
        }
        lat.link_plaqs = vec![Vec::new(); lat.link_cell.len()];
        for p in 0..lat.plaq_cell.len() {
            let c = lat.coords(lat.plaq_cell[p] as usize);
            let dims: Vec<usize> = (0..d).filter(|&k| c[k] % 2 != 0).collect();
            let (mu, nu) = (dims[0], dims[1]);
            let cells = [
                lat.shift(c, nu, -1),
                lat.shift(c, mu, 1),
                lat.shift(c, nu, 1),
                lat.shift(c, mu, -1),
            ];
            let mut ls = [0u32; 4];
            for k in 0..4 {
                let l = lat.cell_link[lat.cell(cells[k])];
                assert!(l != u32::MAX);
                ls[k] = l;
                lat.link_plaqs[l as usize].push(p as u32);
            }
            lat.plaq_links.push(ls);
        }
        for l in 0..lat.link_cell.len() {
            let c = lat.coords(lat.link_cell[l] as usize);
            let mu = (0..d).find(|&k| c[k] % 2 != 0).unwrap_or(0);
            let line = (0..d).all(|k| k == mu || c[k] % 4 == 0);
            if line {
                let pos = if c[mu] % 4 == 1 { 1u8 } else { 2u8 };
                lat.link_kind.push(pos);
                let mut cc = [0i32; 4];
                for k in 0..d {
                    cc[k] = if k == mu {
                        2 * (c[k] / 4) + 1
                    } else {
                        c[k] / 2
                    };
                }
                lat.link_coarse.push(lat.ccell(cc) as u32);
            } else {
                lat.link_kind.push(0);
                lat.link_coarse.push(u32::MAX);
            }
        }
        for p in permutations(d) {
            for s in 0..(1u32 << d) {
                let mut g = G {
                    perm: [0, 1, 2, 3],
                    sign: [1; 4],
                };
                for k in 0..d {
                    g.perm[k] = p[k];
                    g.sign[k] = if (s >> k) & 1 == 1 { -1 } else { 1 };
                }
                if (0..d).all(|k| n[g.perm[k]] == n[k]) {
                    lat.pg.push(g);
                }
            }
        }
        lat
    }
    fn coords(&self, cell: usize) -> [i32; 4] {
        let mut c = [0i32; 4];
        let mut r = cell;
        for k in 0..self.d {
            c[k] = (r % self.m[k] as usize) as i32;
            r /= self.m[k] as usize;
        }
        c
    }
    fn cell(&self, c: [i32; 4]) -> usize {
        let mut s = 0usize;
        for k in 0..self.d {
            s += c[k].rem_euclid(self.m[k]) as usize * self.stride[k];
        }
        s
    }
    fn shift(&self, mut c: [i32; 4], k: usize, by: i32) -> [i32; 4] {
        c[k] = (c[k] + by).rem_euclid(self.m[k]);
        c
    }
    fn ccoords(&self, cell: usize) -> [i32; 4] {
        let mut c = [0i32; 4];
        let mut r = cell;
        for k in 0..self.d {
            c[k] = (r % self.cm[k] as usize) as i32;
            r /= self.cm[k] as usize;
        }
        c
    }
    fn ccell(&self, c: [i32; 4]) -> usize {
        let mut s = 0usize;
        for k in 0..self.d {
            s += c[k].rem_euclid(self.cm[k]) as usize * self.cstride[k];
        }
        s
    }
    fn cshift(&self, mut c: [i32; 4], k: usize, by: i32) -> [i32; 4] {
        c[k] = (c[k] + by).rem_euclid(self.cm[k]);
        c
    }
    fn nplaq(&self) -> usize {
        self.plaq_cell.len()
    }
    fn coarse_sites(&self) -> usize {
        (0..self.d).map(|k| (self.cm[k] / 2) as usize).product()
    }
    fn letter_of_link(&self, l: usize, inv: bool) -> Option<u32> {
        let i = inv as u32;
        match self.link_kind[l] {
            0 => Some(((l as u32) << 1) | i),
            kind => {
                if kind - 1 == self.pos_v {
                    Some(((VOFF + self.link_coarse[l]) << 1) | i)
                } else {
                    None
                }
            }
        }
    }
    fn plaq_word(&self, p: usize) -> Vec<u32> {
        let mut w = Vec::with_capacity(4);
        for k in 0..4 {
            if let Some(x) = self.letter_of_link(self.plaq_links[p][k] as usize, k >= 2) {
                w.push(x);
            }
        }
        w
    }
    fn apply(&self, g: &G, c: [i32; 4], sides: &[i32; 4]) -> [i32; 4] {
        let mut y = [0i32; 4];
        for k in 0..self.d {
            y[g.perm[k]] = (g.sign[k] * c[k]).rem_euclid(sides[g.perm[k]]);
        }
        y
    }
    fn link_of_cell(&self, c: [i32; 4]) -> usize {
        let l = self.cell_link[self.cell(c)];
        assert!(l != u32::MAX);
        l as usize
    }
    fn coarse_link_positions(&self, ccell: usize) -> (usize, usize) {
        let c = self.ccoords(ccell);
        let mu = (0..self.d).find(|&k| c[k] % 2 != 0).unwrap_or(0);
        let mut f = [0i32; 4];
        for k in 0..self.d {
            f[k] = if k == mu {
                4 * (c[k] / 2) + 1
            } else {
                2 * c[k]
            };
        }
        let p0 = self.link_of_cell(f);
        f[mu] += 2;
        let p1 = self.link_of_cell(f);
        (p0, p1)
    }
}

// ---------------------------------------------------------------- canonical forms under the group

#[derive(Clone, Debug)]
struct Canon {
    key: Vec<u32>,
    nmatch: usize,
    tstab: usize,
}

/// Canonical form of a labeled cell set under translations by `step` in every doubled
/// coordinate and the point group: the least sorted image, anchors read by residue.
fn canon_generic(
    lat: &Lat,
    items: &[([i32; 4], u32)],
    sides: &[i32; 4],
    step: i32,
    stride: &[usize; 4],
) -> Canon {
    let d = lat.d;
    let enc = |c: &[i32; 4], lab: u32| -> u32 {
        let mut s = 0usize;
        for k in 0..d {
            s += c[k].rem_euclid(sides[k]) as usize * stride[k];
        }
        (s as u32) * 4 + lab
    };
    let resid = |c: &[i32; 4]| -> u32 {
        let mut r = 0u32;
        for k in 0..d {
            r = r * (step as u32) + c[k].rem_euclid(step) as u32;
        }
        r
    };
    let mut best: Option<Vec<u32>> = None;
    let mut nmatch = 0usize;
    for g in &lat.pg {
        let img: Vec<([i32; 4], u32)> = items
            .iter()
            .map(|(c, lab)| (lat.apply(g, *c, sides), *lab))
            .collect();
        let minr = img
            .iter()
            .map(|(c, lab)| (resid(c), *lab))
            .min()
            .unwrap_or((0, 0));
        let mut gbest: Option<Vec<u32>> = None;
        for (a, lab) in &img {
            if (resid(a), *lab) != minr {
                continue;
            }
            let mut t = [0i32; 4];
            for k in 0..d {
                t[k] = a[k] - a[k].rem_euclid(step);
            }
            let mut v: Vec<u32> = img
                .iter()
                .map(|(b, l2)| {
                    let mut x = [0i32; 4];
                    for k in 0..d {
                        x[k] = b[k] - t[k];
                    }
                    enc(&x, *l2)
                })
                .collect();
            v.sort_unstable();
            if gbest.as_ref().map_or(true, |gb| v < *gb) {
                gbest = Some(v);
            }
        }
        let gb = gbest.unwrap_or_default();
        match best.as_ref().map(|b| gb.cmp(b)) {
            None | Some(Ordering::Less) => {
                best = Some(gb);
                nmatch = 1;
            }
            Some(Ordering::Equal) => nmatch += 1,
            _ => {}
        }
    }
    // translation stabilizer of the set itself
    let mut orig: Vec<u32> = items.iter().map(|(c, lab)| enc(c, *lab)).collect();
    orig.sort_unstable();
    let mut ts: BTreeSet<Vec<i32>> = BTreeSet::new();
    let (a0, l0) = items[0];
    for (a, lab) in items {
        if *lab != l0 || resid(a) != resid(&a0) {
            continue;
        }
        let mut t = [0i32; 4];
        for k in 0..d {
            t[k] = a[k] - a0[k];
        }
        let mut v: Vec<u32> = items
            .iter()
            .map(|(b, l2)| {
                let mut x = [0i32; 4];
                for k in 0..d {
                    x[k] = b[k] + t[k];
                }
                enc(&x, *l2)
            })
            .collect();
        v.sort_unstable();
        if v == orig {
            ts.insert((0..d).map(|k| t[k].rem_euclid(sides[k])).collect());
        }
    }
    Canon {
        key: best.unwrap_or_default(),
        nmatch,
        tstab: ts.len().max(1),
    }
}

fn canon_plaqs(lat: &Lat, plaqs: &[u32]) -> Canon {
    let items: Vec<([i32; 4], u32)> = plaqs
        .iter()
        .map(|&p| (lat.coords(lat.plaq_cell[p as usize] as usize), 0))
        .collect();
    canon_generic(lat, &items, &lat.m, 4, &lat.stride)
}

fn canon_coarse(lat: &Lat, cells: &[(u32, u32)]) -> Canon {
    let items: Vec<([i32; 4], u32)> = cells
        .iter()
        .map(|&(c, lab)| (lat.ccoords(c as usize), lab))
        .collect();
    canon_generic(lat, &items, &lat.cm, 2, &lat.cstride)
}

fn plaqs_from_key(lat: &Lat, key: &[u32]) -> Vec<u32> {
    let mut v: Vec<u32> = key
        .iter()
        .map(|&k| lat.cell_plaq[(k / 4) as usize])
        .collect();
    v.sort_unstable();
    v
}

// ---------------------------------------------------------------- the search for closed supports

const KMAX: usize = 12;

struct Search<'a> {
    lat: &'a Lat,
    even: bool,
    max: usize,
    cur: Vec<u32>,
    in_s: Vec<bool>,
    cover: Vec<u8>,
    visited: HashSet<[u16; KMAX], FxB>,
    closed: Vec<Vec<u32>>,
    states: u64,
    req: Vec<usize>,
}

impl<'a> Search<'a> {
    fn new(lat: &'a Lat, even: bool, max: usize) -> Search<'a> {
        assert!(max <= KMAX);
        Search {
            lat,
            even,
            max,
            cur: Vec::new(),
            in_s: vec![false; lat.nplaq()],
            cover: vec![0; lat.link_cell.len()],
            visited: HashSet::default(),
            closed: Vec::new(),
            states: 0,
            req: Vec::new(),
        }
    }
    fn push(&mut self, p: u32) {
        self.cur.push(p);
        self.in_s[p as usize] = true;
        for &l in &self.lat.plaq_links[p as usize] {
            self.cover[l as usize] += 1;
        }
    }
    fn pop(&mut self) {
        let p = self.cur.pop().unwrap_or(0);
        self.in_s[p as usize] = false;
        for &l in &self.lat.plaq_links[p as usize] {
            self.cover[l as usize] -= 1;
        }
    }
    fn bad(&self, l: usize) -> bool {
        if self.lat.link_kind[l] != 0 {
            return false;
        }
        let c = self.cover[l];
        if self.even {
            c % 2 == 1
        } else {
            c == 1
        }
    }
    fn run_from(&mut self, seed: u32) {
        self.push(seed);
        self.rec();
        self.pop();
    }
    fn rec(&mut self) {
        let mut key = [u16::MAX; KMAX];
        let mut sorted = self.cur.clone();
        sorted.sort_unstable();
        for (k, &p) in sorted.iter().enumerate() {
            key[k] = p as u16;
        }
        if !self.visited.insert(key) {
            return;
        }
        self.states += 1;
        let mut bads: Vec<u32> = Vec::new();
        for &p in &self.cur {
            for &l in &self.lat.plaq_links[p as usize] {
                if self.bad(l as usize) {
                    bads.push(l);
                }
            }
        }
        bads.sort_unstable();
        bads.dedup();
        let rem = self.max - self.cur.len();
        if !self.req.is_empty() {
            let missing = self.req.iter().filter(|&&l| self.cover[l] == 0).count();
            if missing.div_ceil(2) > rem {
                return;
            }
        }
        if bads.is_empty() {
            if self.req.iter().all(|&l| self.cover[l] > 0) {
                self.closed.push(sorted.clone());
            }
            if rem == 0 {
                return;
            }
            let mut cands: Vec<u32> = Vec::new();
            for &p in &self.cur {
                for &l in &self.lat.plaq_links[p as usize] {
                    if self.lat.link_kind[l as usize] == 0 {
                        for &q in &self.lat.link_plaqs[l as usize] {
                            if !self.in_s[q as usize] {
                                cands.push(q);
                            }
                        }
                    }
                }
            }
            cands.sort_unstable();
            cands.dedup();
            for q in cands {
                self.push(q);
                self.rec();
                self.pop();
            }
            return;
        }
        if rem == 0 {
            return;
        }
        let mut counts: Vec<(u32, usize)> = Vec::new();
        for &l in &bads {
            for &q in &self.lat.link_plaqs[l as usize] {
                if !self.in_s[q as usize] {
                    match counts.iter_mut().find(|(x, _)| *x == q) {
                        Some(e) => e.1 += 1,
                        None => counts.push((q, 1)),
                    }
                }
            }
        }
        let kmax = counts.iter().map(|e| e.1).max().unwrap_or(0);
        if kmax == 0 || bads.len().div_ceil(kmax) > rem {
            return;
        }
        let e = bads[0] as usize;
        let opts: Vec<u32> = self.lat.link_plaqs[e]
            .iter()
            .copied()
            .filter(|&q| !self.in_s[q as usize])
            .collect();
        for q in opts {
            self.push(q);
            self.rec();
            self.pop();
        }
    }
}

// ---------------------------------------------------------------- exact SU(2) integration of trace words

type Word = Vec<u32>;
type Term = Vec<Word>;
type Poly = HashMap<Term, Q, FxB>;

fn word_inv(w: &[u32]) -> Word {
    w.iter().rev().map(|&l| l ^ 1).collect()
}

fn reduce_word(w: &[u32]) -> Word {
    let mut st: Vec<u32> = Vec::with_capacity(w.len());
    for &l in w {
        if let Some(&t) = st.last() {
            if t == l ^ 1 {
                st.pop();
                continue;
            }
        }
        st.push(l);
    }
    let mut a = 0usize;
    let mut b = st.len();
    while b >= a + 2 && st[a] == st[b - 1] ^ 1 {
        a += 1;
        b -= 1;
    }
    st[a..b].to_vec()
}

fn canon_word(w: &[u32]) -> Word {
    let r = reduce_word(w);
    let n = r.len();
    if n == 0 {
        return r;
    }
    let ri = word_inv(&r);
    let mut best = r.clone();
    for cand in [&r, &ri] {
        for s in 0..n {
            let rot: Vec<u32> = cand[s..].iter().chain(cand[..s].iter()).copied().collect();
            if rot < best {
                best = rot;
            }
        }
    }
    best
}

fn make_term(words: Vec<Word>, coef: Q) -> (Term, Q) {
    let mut c = coef;
    let mut ws: Vec<Word> = Vec::with_capacity(words.len());
    for w in words {
        let cw = canon_word(&w);
        if cw.is_empty() {
            c = c.mul(&Q::int(2));
        } else {
            ws.push(cw);
        }
    }
    ws.sort();
    (ws, c)
}

fn poly_add(p: &mut Poly, t: Term, c: Q) {
    if c.is_zero() {
        return;
    }
    let mut remove = false;
    match p.get_mut(&t) {
        Some(v) => {
            *v = v.add(&c);
            remove = v.is_zero();
        }
        None => {
            p.insert(t.clone(), c);
        }
    }
    if remove {
        p.remove(&t);
    }
}

fn poly_from(words: Vec<Word>, c: Q) -> Poly {
    let mut p = Poly::default();
    let (t, c) = make_term(words, c);
    poly_add(&mut p, t, c);
    p
}

fn poly_mul(a: &Poly, b: &Poly) -> Poly {
    let mut out = Poly::default();
    for (ta, ca) in a {
        for (tb, cb) in b {
            let mut w = ta.clone();
            w.extend(tb.iter().cloned());
            w.sort();
            poly_add(&mut out, w, ca.mul(cb));
        }
    }
    out
}

fn poly_scale(a: &Poly, c: &Q) -> Poly {
    let mut out = Poly::default();
    for (t, v) in a {
        poly_add(&mut out, t.clone(), v.mul(c));
    }
    out
}

fn poly_sum(a: &Poly, b: &Poly) -> Poly {
    let mut out = a.clone();
    for (t, v) in b {
        poly_add(&mut out, t.clone(), v.clone());
    }
    out
}

fn poly_const(a: &Poly) -> Q {
    a.get(&Vec::new()).cloned().unwrap_or_else(Q::zero)
}

fn poly_vars(a: &Poly) -> BTreeSet<u32> {
    let mut s = BTreeSet::new();
    for t in a.keys() {
        for w in t {
            for &l in w {
                s.insert(l >> 1);
            }
        }
    }
    s
}

struct Wein {
    pairs: Vec<Vec<(usize, usize)>>,
    w: Vec<Vec<Q>>,
}

fn nc_matchings(items: &[usize]) -> Vec<Vec<(usize, usize)>> {
    if items.is_empty() {
        return vec![Vec::new()];
    }
    let mut out = Vec::new();
    let mut j = 1;
    while j < items.len() {
        for a in nc_matchings(&items[1..j]) {
            for b in nc_matchings(&items[j + 1..]) {
                let mut m = vec![(items[0], items[j])];
                m.extend(a.iter().copied());
                m.extend(b.iter().copied());
                out.push(m);
            }
        }
        j += 2;
    }
    out
}

/// The sparse vector of epsilon_sigma: for each pair (a < b), i_a = 0, i_b = 1 with sign +1
/// or i_a = 1, i_b = 0 with sign -1. Keys are bit masks of the indices equal to 1.
fn eps_vector(m: &[(usize, usize)]) -> HashMap<u32, i32, FxB> {
    let mut v: HashMap<u32, i32, FxB> = HashMap::default();
    let k = m.len();
    for choice in 0..(1u32 << k) {
        let mut mask = 0u32;
        let mut sign = 1i32;
        for (t, &(_, b)) in m.iter().enumerate() {
            if (choice >> t) & 1 == 0 {
                mask |= 1 << b;
            } else {
                mask |= 1 << m[t].0;
                sign = -sign;
            }
        }
        v.insert(mask, sign);
    }
    v
}

fn mat_inverse(a: &[Vec<Q>]) -> Vec<Vec<Q>> {
    let n = a.len();
    let mut m: Vec<Vec<Q>> = a.to_vec();
    let mut inv: Vec<Vec<Q>> = (0..n)
        .map(|i| {
            (0..n)
                .map(|j| if i == j { Q::one() } else { Q::zero() })
                .collect()
        })
        .collect();
    for col in 0..n {
        let piv = (col..n)
            .find(|&r| !m[r][col].is_zero())
            .expect("singular Gram matrix");
        m.swap(col, piv);
        inv.swap(col, piv);
        let pv = m[col][col].inv();
        for j in 0..n {
            m[col][j] = m[col][j].mul(&pv);
            inv[col][j] = inv[col][j].mul(&pv);
        }
        for r in 0..n {
            if r != col && !m[r][col].is_zero() {
                let f = m[r][col].clone();
                for j in 0..n {
                    let a1 = m[col][j].mul(&f);
                    m[r][j] = m[r][j].sub(&a1);
                    let b1 = inv[col][j].mul(&f);
                    inv[r][j] = inv[r][j].sub(&b1);
                }
            }
        }
    }
    inv
}

fn build_wein(d: usize) -> Wein {
    let items: Vec<usize> = (0..d).collect();
    let pairs = nc_matchings(&items);
    let vecs: Vec<HashMap<u32, i32, FxB>> = pairs.iter().map(|m| eps_vector(m)).collect();
    let k = pairs.len();
    let mut gram = vec![vec![Q::zero(); k]; k];
    for i in 0..k {
        for j in 0..k {
            let mut s = 0i128;
            for (mask, sg) in &vecs[i] {
                if let Some(t) = vecs[j].get(mask) {
                    s += (*sg as i128) * (*t as i128);
                }
            }
            gram[i][j] = Q::int(s);
        }
    }
    Wein {
        pairs,
        w: mat_inverse(&gram),
    }
}

#[derive(Default)]
struct DegLog {
    hist: BTreeMap<usize, u64>,
    steps: u64,
    local_max: usize,
}

impl DegLog {
    /// Written before each link's integral: its degree, the multiplicities of the term's
    /// plaquettes on it with every inserted coarse functional counted.
    fn record(&mut self, d: usize) {
        *self.hist.entry(d).or_insert(0) += 1;
        self.steps += 1;
        self.local_max = self.local_max.max(d);
    }
    fn take_local(&mut self) -> usize {
        let m = self.local_max;
        self.local_max = 0;
        m
    }
    fn max(&self) -> usize {
        self.hist.keys().next_back().copied().unwrap_or(0)
    }
    fn show(&self) -> String {
        let parts: Vec<String> = self
            .hist
            .iter()
            .map(|(d, c)| d.to_string() + ":" + &c.to_string())
            .collect();
        parts.join(",")
    }
}

struct Integrator {
    wein: Vec<Option<Wein>>,
    deg: DegLog,
}

enum Item {
    W(Word),
    E(i32),
}

impl Integrator {
    fn new() -> Integrator {
        Integrator {
            wein: (0..30).map(|_| None).collect(),
            deg: DegLog::default(),
        }
    }
    fn wein(&mut self, d: usize) -> &Wein {
        if self.wein[d].is_none() {
            self.wein[d] = Some(build_wein(d));
        }
        self.wein[d].as_ref().expect("weingarten")
    }
    /// Haar integral over the variable x of every term: each occurrence of x as a 2 x 2
    /// matrix, U^-1 = eps^T U^T eps, then int U^(x)d = sum W(sigma,tau) eps_sigma eps_tau^T.
    fn integrate_var(&mut self, poly: &Poly, x: u32) -> Poly {
        let mut out = Poly::default();
        for (term, coef) in poly.iter() {
            let mut occ: Vec<(usize, usize, bool)> = Vec::new();
            for (wi, w) in term.iter().enumerate() {
                for (k, &l) in w.iter().enumerate() {
                    if l >> 1 == x {
                        occ.push((wi, k, l & 1 == 1));
                    }
                }
            }
            let d = occ.len();
            if d == 0 {
                poly_add(&mut out, term.clone(), coef.clone());
                continue;
            }
            self.deg.record(d);
            if d % 2 == 1 {
                continue;
            }
            let base: Vec<Word> = term
                .iter()
                .enumerate()
                .filter(|(wi, _)| !occ.iter().any(|o| o.0 == *wi))
                .map(|(_, w)| w.clone())
                .collect();
            let mut segs: Vec<Word> = Vec::with_capacity(d);
            let mut seg_after: Vec<usize> = Vec::with_capacity(d);
            let mut seg_before: Vec<usize> = Vec::with_capacity(d);
            let mut r = 0;
            while r < d {
                let wi = occ[r].0;
                let mut e = r;
                while e < d && occ[e].0 == wi {
                    e += 1;
                }
                let w = &term[wi];
                let cnt = e - r;
                for a in 0..cnt {
                    let ra = r + a;
                    let rb = r + (a + 1) % cnt;
                    let pa = occ[ra].1;
                    let pb = occ[rb].1;
                    let mut s = Vec::new();
                    let mut k = (pa + 1) % w.len();
                    while k != pb {
                        s.push(w[k]);
                        k = (k + 1) % w.len();
                    }
                    segs.push(s);
                    seg_after.push(ra);
                    seg_before.push(rb);
                }
                r = e;
            }
            let nn = 4 * d;
            let mut attach: Vec<(usize, bool)> = vec![(usize::MAX, false); nn];
            for s in 0..d {
                let (ra, rb) = (seg_after[s], seg_before[s]);
                let left = 2 * d + 2 * s;
                let right = left + 1;
                let (pl, el) = if !occ[ra].2 {
                    (2 * ra + 1, false)
                } else {
                    (2 * ra, true)
                };
                attach[left] = (pl, el);
                attach[pl] = (left, el);
                let (pr, er) = if !occ[rb].2 {
                    (2 * rb, false)
                } else {
                    (2 * rb + 1, true)
                };
                attach[right] = (pr, er);
                attach[pr] = (right, er);
            }
            let wn = self.wein(d);
            let k = wn.pairs.len();
            let mut results: Vec<(Vec<Word>, Q)> = Vec::new();
            for si in 0..k {
                for ti in 0..k {
                    let wv = &wn.w[si][ti];
                    if wv.is_zero() {
                        continue;
                    }
                    let mut pair = vec![usize::MAX; nn];
                    for &(a, b) in &wn.pairs[si] {
                        pair[2 * a] = 2 * b;
                        pair[2 * b] = 2 * a;
                    }
                    for &(a, b) in &wn.pairs[ti] {
                        pair[2 * a + 1] = 2 * b + 1;
                        pair[2 * b + 1] = 2 * a + 1;
                    }
                    let mut seen = vec![false; nn];
                    let mut words = base.clone();
                    let mut sign = 1i32;
                    let mut zero = false;
                    for start in 0..d {
                        let s_node = 2 * d + 2 * start;
                        if seen[s_node] {
                            continue;
                        }
                        let mut items: Vec<Item> = Vec::new();
                        let mut node = s_node;
                        loop {
                            seen[node] = true;
                            let s = (node - 2 * d) / 2;
                            let is_left = (node - 2 * d) % 2 == 0;
                            let other = if is_left { node + 1 } else { node - 1 };
                            if is_left {
                                items.push(Item::W(segs[s].clone()));
                            } else {
                                items.push(Item::E(1));
                                items.push(Item::W(word_inv(&segs[s])));
                                items.push(Item::E(-1));
                            }
                            seen[other] = true;
                            let (port, eps) = attach[other];
                            if eps {
                                items.push(Item::E(-1));
                            }
                            seen[port] = true;
                            let p2 = pair[port];
                            items.push(Item::E(if port / 2 < p2 / 2 { 1 } else { -1 }));
                            seen[p2] = true;
                            let (end, eps2) = attach[p2];
                            if eps2 {
                                items.push(Item::E(1));
                            }
                            if end == s_node {
                                break;
                            }
                            node = end;
                        }
                        match reduce_loop(&items) {
                            None => {
                                zero = true;
                                break;
                            }
                            Some((sg, w)) => {
                                sign *= sg;
                                words.push(w);
                            }
                        }
                    }
                    if zero {
                        continue;
                    }
                    let c = coef.mul(wv).mul(&Q::int(sign as i128));
                    results.push((words, c));
                }
            }
            for (words, c) in results {
                let (t, c2) = make_term(words, c);
                poly_add(&mut out, t, c2);
            }
        }
        out
    }
    fn integrate_vars(&mut self, poly: &Poly, vars: &[u32]) -> Poly {
        let mut p = poly.clone();
        for &x in vars {
            p = self.integrate_var(&p, x);
            if p.is_empty() {
                break;
            }
        }
        p
    }
    fn integrate_all(&mut self, poly: &Poly) -> Q {
        let vars: Vec<u32> = poly_vars(poly).into_iter().collect();
        let p = self.integrate_vars(poly, &vars);
        for t in p.keys() {
            assert!(t.is_empty(), "a variable left after integrating all");
        }
        poly_const(&p)
    }
    fn inner(&mut self, a: &Poly, b: &Poly) -> Q {
        let p = poly_mul(a, b);
        self.integrate_all(&p)
    }
}

/// A traced loop: words joined by runs of epsilon; each run must hold an even count, so the
/// loop is a sign times the trace of a word, and a loop with no letters reads +-2 or 0.
fn reduce_loop(items: &[Item]) -> Option<(i32, Word)> {
    let first = items
        .iter()
        .position(|it| matches!(it, Item::W(w) if !w.is_empty()));
    match first {
        None => {
            let mut k = 0usize;
            let mut s = 1i32;
            for it in items {
                if let Item::E(e) = it {
                    k += 1;
                    s *= e;
                }
            }
            if k % 2 == 1 {
                return None;
            }
            if (k / 2) % 2 == 1 {
                s = -s;
            }
            Some((s, Vec::new()))
        }
        Some(i0) => {
            let n = items.len();
            let mut word: Word = Vec::new();
            let mut sign = 1i32;
            let mut run = 0usize;
            let mut rs = 1i32;
            for t in 0..=n {
                let it = &items[(i0 + t) % n];
                match it {
                    Item::E(e) => {
                        run += 1;
                        rs *= e;
                    }
                    Item::W(w) => {
                        if w.is_empty() {
                            continue;
                        }
                        if t > 0 || run > 0 {
                            assert!(run % 2 == 0, "an odd run of epsilon between words");
                            if (run / 2) % 2 == 1 {
                                rs = -rs;
                            }
                            sign *= rs;
                        }
                        run = 0;
                        rs = 1;
                        if t < n {
                            word.extend(w.iter().copied());
                        }
                    }
                }
            }
            Some((sign, word))
        }
    }
}

// ---------------------------------------------------------------- quaternions for evaluation

/// a + b phi, phi^2 = phi + 1
#[derive(Clone, Copy, PartialEq, Eq, Debug, Default)]
struct Zp(i128, i128);

impl Zp {
    fn add(self, o: Zp) -> Zp {
        Zp(self.0 + o.0, self.1 + o.1)
    }
    fn sub(self, o: Zp) -> Zp {
        Zp(self.0 - o.0, self.1 - o.1)
    }
    fn mul(self, o: Zp) -> Zp {
        Zp(
            self.0 * o.0 + self.1 * o.1,
            self.0 * o.1 + self.1 * o.0 + self.1 * o.1,
        )
    }
}

/// A quaternion with Z[phi] coordinates, divided by 2^e.
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
struct Qp {
    c: [Zp; 4],
    e: u32,
}

fn qp_mul(p: &Qp, q: &Qp) -> Qp {
    let [a, b, c, d] = p.c;
    let [e, f, g, h] = q.c;
    Qp {
        c: [
            a.mul(e).sub(b.mul(f)).sub(c.mul(g)).sub(d.mul(h)),
            a.mul(f).add(b.mul(e)).add(c.mul(h)).sub(d.mul(g)),
            a.mul(g).sub(b.mul(h)).add(c.mul(e)).add(d.mul(f)),
            a.mul(h).add(b.mul(g)).sub(c.mul(f)).add(d.mul(e)),
        ],
        e: p.e + q.e,
    }
}

fn qp_conj(p: &Qp) -> Qp {
    Qp {
        c: [
            p.c[0],
            Zp(-p.c[1].0, -p.c[1].1),
            Zp(-p.c[2].0, -p.c[2].1),
            Zp(-p.c[3].0, -p.c[3].1),
        ],
        e: p.e,
    }
}

fn zp_even(z: Zp) -> bool {
    z.0 % 2 == 0 && z.1 % 2 == 0
}

fn qp_reduce(mut p: Qp) -> Qp {
    while p.e > 0 && p.c.iter().all(|z| zp_even(*z)) {
        for k in 0..4 {
            p.c[k] = Zp(p.c[k].0 / 2, p.c[k].1 / 2);
        }
        p.e -= 1;
    }
    p
}

/// The binary icosahedral group 2I (120) and the binary tetrahedral group 2T (24), as unit
/// quaternions with coordinates in Z[phi] / 2, closed under products.
fn group_2i() -> Vec<Qp> {
    let z = Zp(0, 0);
    let one = Zp(2, 0);
    let mut gens: Vec<Qp> = Vec::new();
    for k in 0..4 {
        for s in [1i128, -1] {
            let mut c = [z; 4];
            c[k] = Zp(2 * s, 0);
            gens.push(Qp { c, e: 1 });
        }
    }
    for s in 0..16u32 {
        let mut c = [z; 4];
        for k in 0..4 {
            c[k] = if (s >> k) & 1 == 1 {
                Zp(-1, 0)
            } else {
                Zp(1, 0)
            };
        }
        gens.push(Qp { c, e: 1 });
    }
    let even_perms: Vec<[usize; 4]> = permutations(4)
        .into_iter()
        .filter(|p| {
            let mut inv = 0;
            for i in 0..4 {
                for j in i + 1..4 {
                    if p[i] > p[j] {
                        inv += 1;
                    }
                }
            }
            inv % 2 == 0
        })
        .map(|p| [p[0], p[1], p[2], p[3]])
        .collect();
    let base = [Zp(0, 0), Zp(1, 0), Zp(0, 1), Zp(-1, 1)];
    for p in &even_perms {
        for s in 0..8u32 {
            let mut c = [z; 4];
            for k in 0..4 {
                let mut v = base[k];
                if k >= 1 && (s >> (k - 1)) & 1 == 1 {
                    v = Zp(-v.0, -v.1);
                }
                c[p[k]] = v;
            }
            gens.push(Qp { c, e: 1 });
        }
    }
    let _ = one;
    close_group(gens)
}

fn group_2t() -> Vec<Qp> {
    let z = Zp(0, 0);
    let mut gens: Vec<Qp> = Vec::new();
    for k in 0..4 {
        for s in [1i128, -1] {
            let mut c = [z; 4];
            c[k] = Zp(2 * s, 0);
            gens.push(Qp { c, e: 1 });
        }
    }
    for s in 0..16u32 {
        let mut c = [z; 4];
        for k in 0..4 {
            c[k] = if (s >> k) & 1 == 1 {
                Zp(-1, 0)
            } else {
                Zp(1, 0)
            };
        }
        gens.push(Qp { c, e: 1 });
    }
    close_group(gens)
}

fn qp_norm_one(p: &Qp) -> bool {
    let mut s = Zp(0, 0);
    for k in 0..4 {
        s = s.add(p.c[k].mul(p.c[k]));
    }
    s == Zp(1i128 << (2 * p.e), 0)
}

fn close_group(gens: Vec<Qp>) -> Vec<Qp> {
    let norm = |p: Qp| -> Qp {
        let r = qp_reduce(p);
        let mut q = r;
        while q.e < 1 {
            for k in 0..4 {
                q.c[k] = Zp(q.c[k].0 * 2, q.c[k].1 * 2);
            }
            q.e += 1;
        }
        q
    };
    let mut elems: Vec<Qp> = Vec::new();
    for g in gens {
        let g = norm(g);
        assert!(qp_norm_one(&g), "a generator off the unit sphere");
        if !elems.contains(&g) {
            elems.push(g);
        }
    }
    loop {
        let mut added = false;
        let n = elems.len();
        for i in 0..n {
            for j in 0..n {
                let p = norm(qp_mul(&elems[i], &elems[j]));
                if !elems.contains(&p) {
                    elems.push(p);
                    added = true;
                }
            }
        }
        if !added {
            break;
        }
    }
    elems.sort_by(|a, b| {
        a.c.iter()
            .map(|z| (z.0, z.1))
            .cmp(b.c.iter().map(|z| (z.0, z.1)))
    });
    elems
}

/// Rational quaternions (w, x, y, z) / den for the order-4 benchmark.
#[derive(Clone, Debug, PartialEq)]
struct Qq {
    w: Q,
    x: Q,
    y: Q,
    z: Q,
}

fn qq_mul(p: &Qq, q: &Qq) -> Qq {
    Qq {
        w: p.w
            .mul(&q.w)
            .sub(&p.x.mul(&q.x))
            .sub(&p.y.mul(&q.y))
            .sub(&p.z.mul(&q.z)),
        x: p.w
            .mul(&q.x)
            .add(&p.x.mul(&q.w))
            .add(&p.y.mul(&q.z))
            .sub(&p.z.mul(&q.y)),
        y: p.w
            .mul(&q.y)
            .sub(&p.x.mul(&q.z))
            .add(&p.y.mul(&q.w))
            .add(&p.z.mul(&q.x)),
        z: p.w
            .mul(&q.z)
            .add(&p.x.mul(&q.y))
            .sub(&p.y.mul(&q.x))
            .add(&p.z.mul(&q.w)),
    }
}

fn qq_conj(p: &Qq) -> Qq {
    Qq {
        w: p.w.clone(),
        x: p.x.neg(),
        y: p.y.neg(),
        z: p.z.neg(),
    }
}

fn qq_one() -> Qq {
    Qq {
        w: Q::one(),
        x: Q::zero(),
        y: Q::zero(),
        z: Q::zero(),
    }
}

/// The value of a polynomial in trace words at rational quaternions for its variables.
fn eval_poly_qq(p: &Poly, val: &HashMap<u32, Qq, FxB>) -> Q {
    let mut total = Q::zero();
    for (t, c) in p {
        let mut prod = c.clone();
        for w in t {
            let mut q = qq_one();
            for &l in w {
                let v = val.get(&(l >> 1)).expect("an unassigned variable");
                q = qq_mul(&q, &if l & 1 == 1 { qq_conj(v) } else { v.clone() });
            }
            prod = prod.mul(&q.w.mul(&Q::int(2)));
            if prod.is_zero() {
                break;
            }
        }
        total = total.add(&prod);
    }
    total
}

/// a + b phi with rational a, b.
#[derive(Clone, Debug, PartialEq)]
struct Qf(Q, Q);

fn qf_show(a: &Qf) -> String {
    if a.1.is_zero() {
        return a.0.show();
    }
    let b = a.1.show() + "phi";
    if a.0.is_zero() {
        return b;
    }
    if b.starts_with('-') {
        a.0.show() + &b
    } else {
        a.0.show() + "+" + &b
    }
}

fn qf_mul(a: &Qf, b: &Qf) -> Qf {
    Qf(
        a.0.mul(&b.0).add(&a.1.mul(&b.1)),
        a.0.mul(&b.1).add(&a.1.mul(&b.0)).add(&a.1.mul(&b.1)),
    )
}

/// The value of a polynomial in trace words at elements of 2I, in Q(phi).
fn eval_poly_qp(p: &Poly, val: &HashMap<u32, Qp, FxB>) -> Qf {
    let mut total = Qf(Q::zero(), Q::zero());
    for (t, c) in p {
        let mut prod = Qf(c.clone(), Q::zero());
        for w in t {
            let mut q = Qp {
                c: [Zp(1, 0), Zp(0, 0), Zp(0, 0), Zp(0, 0)],
                e: 0,
            };
            for &l in w {
                let v = val.get(&(l >> 1)).expect("an unassigned variable");
                q = qp_reduce(qp_mul(&q, &if l & 1 == 1 { qp_conj(v) } else { *v }));
            }
            let den = Q::frac(1i128 << q.e, 2);
            prod = qf_mul(
                &prod,
                &Qf(Q::int(q.c[0].0).div(&den), Q::int(q.c[0].1).div(&den)),
            );
        }
        total = Qf(total.0.add(&prod.0), total.1.add(&prod.1));
    }
    total
}

// ---------------------------------------------------------------- receipt output

struct Out {
    rows: Vec<String>,
    failed: Vec<String>,
    misses: Vec<String>,
    t0: Instant,
}

impl Out {
    fn row(&mut self, s: String) {
        let line = s + "|json=0";
        println!("{}", line);
        self.rows.push(line);
    }
    fn note(&self, s: &str) {
        let ms = self.t0.elapsed().as_millis();
        eprintln!("RUN|ms={}|{}", ms, s);
    }
    fn fail(&mut self, name: &str, detail: &str) {
        let line = "FAILED|check=".to_string() + name + "|" + detail + "|json=0";
        println!("{}", line);
        let _ = std::io::stdout().flush();
        self.failed.push(name.to_string());
        eprintln!("{}", line);
        std::process::exit(1);
    }
    fn check(&mut self, name: &str, ok: bool, detail: &str) {
        if !ok {
            self.fail(name, detail);
        }
    }
    /// One predicted coefficient: the read value beside the frozen value. A DERIVED row that
    /// misses stops the run; a CONJECTURE row that misses is kept and stated.
    fn read(&mut self, row: &str, item: &str, read: &str, frozen: &str, derived: bool) {
        let met = read == frozen;
        let tag = if derived { "DERIVED" } else { "CONJECTURE" };
        self.row(
            "YM4_03C_READ|row=".to_string()
                + row
                + "|item="
                + item
                + "|read="
                + read
                + "|frozen="
                + frozen
                + "|frozen_tag="
                + tag
                + "|result="
                + if met { "MET" } else { "MISS" },
        );
        if !met {
            self.misses.push(row.to_string() + ":" + item);
            if derived {
                self.fail(
                    &(row.to_string() + "_" + item),
                    &("read=".to_string() + read + "|frozen=" + frozen),
                );
            }
        }
    }
}

fn sabotage() -> String {
    std::env::var("SABOTAGE").unwrap_or_default()
}

// ---------------------------------------------------------------- G1 and P9: the designs

fn chi_zp(t: Zp, n: usize) -> Zp {
    // chi_{n/2} at trace t: chi_0 = 1, chi_1/2 = t, chi_k = t chi_{k-1} - chi_{k-2}
    let mut prev = Zp(0, 0);
    let mut cur = Zp(1, 0);
    for _ in 0..n {
        let next = t.mul(cur).sub(prev);
        prev = cur;
        cur = next;
    }
    cur
}

fn section_designs(out: &mut Out, ig: &mut Integrator, g2i: &[Qp], g2t: &[Qp]) {
    out.note("designs");
    out.check("G1_2I_order_120", g2i.len() == 120, &g2i.len().to_string());
    out.check("G1_2T_order_24", g2t.len() == 24, &g2t.len().to_string());
    // traces as Z[phi]: t = 2 Re(q) = c0 * 2 / 2^e with e = 1, so t = c0
    let trace = |q: &Qp| -> Zp {
        assert!(q.e == 1);
        q.c[0]
    };
    let mut sums_2i: Vec<String> = Vec::new();
    let mut ok2i = true;
    for n in 0..=14 {
        let mut s = Zp(0, 0);
        for q in g2i {
            s = s.add(chi_zp(trace(q), n));
        }
        let want = if n == 0 || n == 12 {
            Zp(120, 0)
        } else if (1..=11).contains(&n) {
            Zp(0, 0)
        } else {
            s
        };
        ok2i &= s == want;
        sums_2i.push(
            s.0.to_string()
                + (if s.1 != 0 {
                    "+".to_string() + &s.1.to_string() + "phi"
                } else {
                    String::new()
                })
                .as_str(),
        );
    }
    let mut sums_2t: Vec<String> = Vec::new();
    let mut ok2t = true;
    for n in 0..=8 {
        let mut s = Zp(0, 0);
        for q in g2t {
            s = s.add(chi_zp(trace(q), n));
        }
        let want = if n == 0 || n == 6 {
            Zp(24, 0)
        } else if (1..=5).contains(&n) {
            Zp(0, 0)
        } else {
            s
        };
        ok2t &= s == want;
        sums_2t.push(s.0.to_string());
    }
    out.check("P9_class_sums_2I", ok2i, &sums_2i.join(","));
    out.check("P9_class_sums_2T", ok2t, &sums_2t.join(","));
    out.row("YM4_03C_DESIGNS|sum_chi_n/2_over_2I_n=0..14=".to_string() + &sums_2i.join(",") + "|sum_chi_n/2_over_2T_n=0..8=" + &sums_2t.join(",") + "|reading=2I_averages_equal_Haar_on_one_link_through_degree_11,2T_through_5|tag=MEASURED");
    // E[chi_1/2^m]: SU(2) by the integrator, 2I and 2T by their elements
    let mut su2: Vec<Q> = Vec::new();
    for m in 0..=12usize {
        let p = poly_from(vec![vec![0u32 << 1]; m], Q::one());
        let v = ig.integrate_all(&p);
        su2.push(v);
    }
    let avg = |g: &[Qp], m: usize| -> Q {
        let mut s = Zp(0, 0);
        for q in g {
            let t = trace(q);
            let mut v = Zp(1, 0);
            for _ in 0..m {
                v = v.mul(t);
            }
            s = s.add(v);
        }
        assert!(s.1 == 0, "a phi part in a class sum");
        Q::frac(s.0, g.len() as i128)
    };
    let sab = sabotage() == "2i_beyond_degree_11";
    let top_2i = if sab { 12 } else { 11 };
    let mut rows_m: Vec<String> = Vec::new();
    for m in 0..=12usize {
        let a2i = avg(g2i, m);
        let a2t = avg(g2t, m);
        rows_m.push(m.to_string() + ":" + &su2[m].show() + ":" + &a2i.show() + ":" + &a2t.show());
        if m <= top_2i {
            out.check(
                "G1_2I_within_degree_11",
                a2i == su2[m],
                &("m=".to_string()
                    + &m.to_string()
                    + "|2I="
                    + &a2i.show()
                    + "|SU2="
                    + &su2[m].show()),
            );
        }
        if m <= 5 {
            out.check("G1_2T_within_degree_5", a2t == su2[m], &m.to_string());
        }
    }
    let catalan = [1i128, 1, 2, 5, 14, 42, 132];
    let cat_ok = (0..=6).all(|k| su2[2 * k] == Q::int(catalan[k]))
        && (0..6).all(|k| su2[2 * k + 1].is_zero());
    out.check("P9_SU2_moments_are_Catalan", cat_ok, "");
    let neg6 = avg(g2t, 6);
    let neg12 = avg(g2i, 12);
    out.check(
        "P9_negative_control_2T_degree_6",
        neg6 == Q::int(6) && su2[6] == Q::int(5),
        &neg6.show(),
    );
    out.check(
        "P9_negative_control_2I_degree_12",
        neg12 == Q::int(133) && su2[12] == Q::int(132),
        &neg12.show(),
    );
    out.row("YM4_03C_MOMENTS|m:SU2:2I:2T=".to_string() + &rows_m.join(",") + "|tag=MEASURED");
    out.read("P9", "E[chi_1/2^6]_SU2", &su2[6].show(), "5", true);
    out.read("P9", "E[chi_1/2^6]_2T", &neg6.show(), "6", true);
    out.read("P9", "E[chi_1/2^12]_SU2", &su2[12].show(), "132", true);
    out.read("P9", "E[chi_1/2^12]_2I", &neg12.show(), "133", true);
    // one-link tensors: (1/|G|) sum_g g^(x)d against the Weingarten projector, entry by entry, d <= 6
    let mut tensor_rows: Vec<String> = Vec::new();
    for (name, grp, top) in [("2I", g2i, 6usize), ("2T", g2t, 6usize)] {
        for d in (2..=top).step_by(2) {
            let equal = tensor_equal(ig, grp, d);
            let within = (name == "2I" && d <= 11) || (name == "2T" && d <= 5);
            out.check(
                "G1_one_link_tensor",
                equal == within,
                &(name.to_string() + "_d=" + &d.to_string()),
            );
            tensor_rows.push(
                name.to_string()
                    + "_d="
                    + &d.to_string()
                    + ":"
                    + if equal { "equal" } else { "differs" },
            );
        }
    }
    out.row(
        "YM4_03C_ONE_LINK_TENSORS|".to_string()
            + &tensor_rows.join(",")
            + "|entries=2^d_x_2^d_exact_in_Z[phi,i]|tag=MEASURED",
    );
}

/// Compare the group average of g^(x)d with the SU(2) projector sum W eps_sigma eps_tau^T.
fn tensor_equal(ig: &mut Integrator, grp: &[Qp], d: usize) -> bool {
    let wn = ig.wein(d);
    let k = wn.pairs.len();
    let vecs: Vec<HashMap<u32, i32, FxB>> = wn.pairs.iter().map(|m| eps_vector(m)).collect();
    let size = 1usize << d;
    // projector P[i][j] = sum_{s,t} eps_s(i) W[s][t] eps_t(j)
    let mut pm = vec![vec![Q::zero(); size]; size];
    for s in 0..k {
        for t in 0..k {
            let w = &wn.w[s][t];
            if w.is_zero() {
                continue;
            }
            for (mi, si) in &vecs[s] {
                for (mj, sj) in &vecs[t] {
                    let cur = &pm[*mi as usize][*mj as usize];
                    pm[*mi as usize][*mj as usize] = cur.add(&w.mul(&Q::int((*si * *sj) as i128)));
                }
            }
        }
    }
    // matrices of the group elements: [[w+ix, y+iz],[-y+iz, w-ix]] / 2, entries (re, im) in Z[phi]
    let mats: Vec<[[(Zp, Zp); 2]; 2]> = grp
        .iter()
        .map(|q| {
            let [w, x, y, z] = q.c;
            let ng = |a: Zp| Zp(-a.0, -a.1);
            [[(w, x), (y, z)], [(ng(y), z), (w, ng(x))]]
        })
        .collect();
    for i in 0..size {
        for j in 0..size {
            let mut re = Zp(0, 0);
            let mut im = Zp(0, 0);
            for mt in &mats {
                let mut a = (Zp(1, 0), Zp(0, 0));
                for r in 0..d {
                    let e = mt[(i >> r) & 1][(j >> r) & 1];
                    a = (
                        a.0.mul(e.0).sub(a.1.mul(e.1)),
                        a.0.mul(e.1).add(a.1.mul(e.0)),
                    );
                }
                re = re.add(a.0);
                im = im.add(a.1);
            }
            // sum / (|G| 2^d) == P[i][j]
            let target = pm[i][j].mul(&Q::int(grp.len() as i128 * (1i128 << d)));
            if im != Zp(0, 0) || re.1 != 0 || Q::int(re.0) != target {
                return false;
            }
        }
    }
    true
}

/// The fold a^m = 2^-m sum_n N_m(n) chi_n/2, as an identity of integer polynomials in t = Tr U
/// (t^m = sum_n N_m(n) U_n with U_n the Chebyshev polynomials of chi), for every m <= 12, and
/// the Haar orthonormality <chi_j, chi_k> = delta_jk read by the integrator for 2j + 2k <= 12:
/// one integral per support and spin pattern then serves every multiplicity vector.
fn section_mckay_fold(out: &mut Out, ig: &mut Integrator) {
    let nk = mckay(12);
    let mut polys = 0usize;
    for m in 0..=12usize {
        let mut lhs = vec![0i128; m + 1];
        lhs[m] = 1;
        let mut rhs = vec![0i128; m + 1];
        for n in 0..=m {
            if nk[m][n] == 0 {
                continue;
            }
            for (k, &c) in cheb(n).iter().enumerate() {
                rhs[k] += nk[m][n] * c;
            }
        }
        out.check(
            "E3_mckay_fold_polynomial",
            lhs == rhs,
            &("m=".to_string() + &m.to_string()),
        );
        polys += 1;
    }
    let mut pairs = 0usize;
    for j in 0..=6usize {
        for k in 0..=(12 - j).min(6) {
            let v = ig.inner(&chi_poly(&[0u32], j), &chi_poly(&[0u32], k));
            let want = if j == k { Q::one() } else { Q::zero() };
            out.check(
                "E3_character_orthonormality",
                v == want,
                &("2j=".to_string() + &j.to_string() + "|2k=" + &k.to_string()),
            );
            pairs += 1;
        }
    }
    out.row(
        "YM4_03C_MCKAY_FOLD|identity=t^m=sum_n_N_m(n)_chi_n/2(t)_as_integer_polynomials|m=0..12="
            .to_string()
            + &polys.to_string()
            + "_equal|orthonormality_<chi_j,chi_k>_by_the_integrator_2j,2k<=6="
            + &pairs.to_string()
            + "_equal|tag=MEASURED",
    );
}

// ---------------------------------------------------------------- the integrator against 2I, term by term

struct Lcg(u64);

impl Lcg {
    fn next(&mut self, bound: u64) -> u64 {
        self.0 = self
            .0
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        (self.0 >> 33) % bound
    }
}

fn section_integrator_checks(out: &mut Out, ig: &mut Integrator, g2i: &[Qp]) {
    out.note("integrator checks");
    // literal 2I averages over two integrated variables, with two more fixed at elements of 2I;
    // every integrated variable's degree is written before its average and stays <= 11.
    let mut rng = Lcg(20261108);
    let mut checked = 0usize;
    let mut max_deg = 0usize;
    let mut degs: BTreeMap<usize, usize> = BTreeMap::new();
    for _case in 0..48 {
        let nw = 1 + rng.next(3) as usize;
        let mut words: Vec<Word> = Vec::new();
        for _ in 0..nw {
            let len = 1 + rng.next(5) as usize;
            let w: Word = (0..len)
                .map(|_| ((rng.next(4) as u32) << 1) | (rng.next(2) as u32))
                .collect();
            words.push(w);
        }
        let p = poly_from(words.clone(), Q::one());
        let deg = |x: u32| -> usize {
            words
                .iter()
                .map(|w| w.iter().filter(|&&l| l >> 1 == x).count())
                .sum()
        };
        let (d0, d1) = (deg(0), deg(1));
        if d0 > 11 || d1 > 11 {
            continue;
        }
        *degs.entry(d0.max(d1)).or_insert(0) += 1;
        max_deg = max_deg.max(d0.max(d1));
        let sym = ig.integrate_vars(&p, &[0, 1]);
        let fix2 = g2i[rng.next(120) as usize];
        let fix3 = g2i[rng.next(120) as usize];
        let mut val: HashMap<u32, Qp, FxB> = HashMap::default();
        val.insert(2, fix2);
        val.insert(3, fix3);
        let symv = eval_poly_qp(&sym, &val);
        let mut acc = Qf(Q::zero(), Q::zero());
        for a in g2i {
            for b in g2i {
                val.insert(0, *a);
                val.insert(1, *b);
                let v = eval_poly_qp(&p, &val);
                acc = Qf(acc.0.add(&v.0), acc.1.add(&v.1));
            }
        }
        let n2 = Q::int(120 * 120);
        let lit = Qf(acc.0.div(&n2), acc.1.div(&n2));
        out.check(
            "G1_integrator_equals_2I_term_by_term",
            lit == symv,
            &("case=".to_string() + &checked.to_string()),
        );
        checked += 1;
    }
    // terms built to carry degree 7 to 11 on the first integrated link
    for target in 7..=11usize {
        for variant in 0..2u64 {
            let mut words: Vec<Word> = Vec::new();
            let mut left = target;
            while left > 0 {
                let k = left.min(1 + rng.next(3) as usize);
                let mut w: Word = Vec::new();
                for _ in 0..k {
                    w.push(rng.next(2) as u32);
                    if rng.next(2) == 0 {
                        w.push((((1 + rng.next(3)) as u32) << 1) | (rng.next(2) as u32));
                    }
                }
                left -= k;
                words.push(w);
            }
            let _ = variant;
            let p = poly_from(words.clone(), Q::one());
            let deg = |x: u32| -> usize {
                words
                    .iter()
                    .map(|w| w.iter().filter(|&&l| l >> 1 == x).count())
                    .sum()
            };
            let (d0, d1) = (deg(0), deg(1));
            if d0 > 11 || d1 > 11 {
                continue;
            }
            *degs.entry(d0.max(d1)).or_insert(0) += 1;
            max_deg = max_deg.max(d0.max(d1));
            let sym = ig.integrate_vars(&p, &[0, 1]);
            let mut val: HashMap<u32, Qp, FxB> = HashMap::default();
            val.insert(2, g2i[rng.next(120) as usize]);
            val.insert(3, g2i[rng.next(120) as usize]);
            let symv = eval_poly_qp(&sym, &val);
            let mut acc = Qf(Q::zero(), Q::zero());
            for a in g2i {
                for b in g2i {
                    val.insert(0, *a);
                    val.insert(1, *b);
                    let v = eval_poly_qp(&p, &val);
                    acc = Qf(acc.0.add(&v.0), acc.1.add(&v.1));
                }
            }
            let n2 = Q::int(120 * 120);
            let lit = Qf(acc.0.div(&n2), acc.1.div(&n2));
            out.check(
                "G1_integrator_equals_2I_term_by_term",
                lit == symv,
                &("degree=".to_string() + &target.to_string()),
            );
            checked += 1;
        }
    }
    // the guards above leave out every term past degree 11; this check stops the run if one reached its 2I average
    out.check(
        "G1_2I_term_check_within_degree_11",
        max_deg <= 11,
        &("max_link_degree=".to_string() + &max_deg.to_string()),
    );
    let hist: Vec<String> = degs
        .iter()
        .map(|(d, c)| d.to_string() + ":" + &c.to_string())
        .collect();
    out.row(
        "YM4_03C_INTEGRATOR_VS_2I|terms=".to_string()
            + &checked.to_string()
            + "|integrated_links_per_term=2|max_link_degree="
            + &max_deg.to_string()
            + "|terms_by_max_degree="
            + &hist.join(",")
            + "|equal="
            + &checked.to_string()
            + "|tag=MEASURED",
    );
}

/// Positive and negative controls of the readout on the d = 4 coarse lattice: each named
/// functional read back with coefficient 1 and residual 0; a spin-2 plaquette, outside the
/// named list, shows as a residual of exactly its norm.
fn section_readout_controls(out: &mut Out, ig: &mut Integrator) {
    let lat = Lat::new(4, [6, 6, 6, 6], 1);
    let mut eng = Engine {
        offered: BTreeMap::new(),
        lat: &lat,
        shapes: BTreeMap::new(),
        norms: HashMap::new(),
        readouts: 0,
    };
    // P at 0 in plane (0,1); Q at 0 in plane (0,2) shares the link (0, e_0); R coplanar with P
    // shares (e_0, e_1)... ; S parallel to P at e_2, sharing no link
    let (_, wp) = cplaq(&lat, [1, 1, 0, 0]).expect("P");
    let (_, wq) = cplaq(&lat, [1, 0, 1, 0]).expect("Q");
    let (_, wr) = cplaq(&lat, [3, 1, 0, 0]).expect("R");
    let (_, ws) = cplaq(&lat, [1, 1, 2, 0]).expect("S");
    let shared = lat.ccell([1, 0, 0, 0]);
    let shared_pr = lat.ccell([2, 1, 0, 0]);
    let chair = six_loop_of(&[0; 4], &wp, &[0; 4], &wq, shared);
    let rect = six_loop_of(&[0; 4], &wp, &[0; 4], &wr, shared_pr);
    // the twisted hexagon x -> +0 -> +1 -> +2 -> -0 -> -1 -> -2
    let hex_cells = [
        lat.ccell([1, 0, 0, 0]),
        lat.ccell([2, 1, 0, 0]),
        lat.ccell([2, 2, 1, 0]),
        lat.ccell([1, 2, 2, 0]),
        lat.ccell([0, 1, 2, 0]),
        lat.ccell([0, 0, 1, 0]),
    ];
    let hex: Word = vec![
        vletter(hex_cells[0], false),
        vletter(hex_cells[1], false),
        vletter(hex_cells[2], false),
        vletter(hex_cells[3], true),
        vletter(hex_cells[4], true),
        vletter(hex_cells[5], true),
    ];
    let n1 = poly_sum(
        &poly_mul(&tr_poly(&wp), &tr_poly(&wq)),
        &poly_scale(&tr_poly(&chair), &Q::frac(-1, 2)),
    );
    let n1c = poly_sum(
        &poly_mul(&tr_poly(&wp), &tr_poly(&wr)),
        &poly_scale(&tr_poly(&rect), &Q::frac(-1, 2)),
    );
    let tests: Vec<(&str, Poly, &str)> = vec![
        ("plaq_half", chi_poly(&wp, 1), "plaq_half:1"),
        ("plaq_one", chi_poly(&wp, 2), "plaq_one:1"),
        ("plaq_threehalf", chi_poly(&wp, 3), "plaq_threehalf:1"),
        ("chair", tr_poly(&chair), "chair:1"),
        ("rect", tr_poly(&rect), "rect:1"),
        ("twisted_hex", tr_poly(&hex), "twisted_hex:1"),
        ("n1_perpendicular", n1, "n1:1"),
        ("n1_coplanar", n1c, "n1:1"),
        (
            "pair_parallel_distance_1",
            poly_mul(&tr_poly(&wp), &tr_poly(&ws)),
            "pair:1",
        ),
        (
            "product_P_Q",
            poly_mul(&tr_poly(&wp), &tr_poly(&wq)),
            "chair:1/2,n1:1",
        ),
    ];
    let mut rows: Vec<String> = Vec::new();
    for (name, f, want) in tests {
        let r = eng.readout(ig, &f);
        let mut got: Vec<String> = r
            .coef
            .iter()
            .map(|(k, c)| k.0.clone() + ":" + &c.show())
            .collect();
        got.sort();
        let g = got.join(",");
        out.check(
            "E6_readout_control",
            g == want && r.residual.is_zero(),
            &(name.to_string() + "|read=" + &g + "|residual=" + &r.residual.show()),
        );
        rows.push(name.to_string() + "=" + &g);
    }
    // outside the list: chi_2(V_P), spin 2 on four links; its norm is 1
    let r = eng.readout(ig, &chi_poly(&wp, 4));
    out.check(
        "E6_readout_negative_control",
        r.coef.is_empty() && r.residual == Q::one(),
        &r.residual.show(),
    );
    out.row(
        "YM4_03C_READOUT_CONTROLS|".to_string()
            + &rows.join(",")
            + "|chi_2(V_P)_residual="
            + &r.residual.show()
            + "_its_norm|tag=MEASURED",
    );
}

// ---------------------------------------------------------------- polymers: spins, activities, readouts

/// The number of SU(2) invariants in the tensor product of spins n_k / 2.
fn invariants(spins: &[usize]) -> i128 {
    let mut mult: Vec<i128> = vec![1];
    for &n in spins {
        let mut next = vec![0i128; mult.len() + n + 1];
        for (j, &c) in mult.iter().enumerate() {
            if c == 0 {
                continue;
            }
            let mut k = j.abs_diff(n);
            while k <= j + n {
                next[k] += c;
                k += 2;
            }
        }
        while next.len() > 1 && *next.last().unwrap_or(&0) == 0 {
            next.pop();
        }
        mult = next;
    }
    mult[0]
}

fn cheb(n: usize) -> Vec<i128> {
    let mut a: Vec<i128> = vec![1];
    let mut b: Vec<i128> = vec![0, 1];
    if n == 0 {
        return a;
    }
    for _ in 1..n {
        let mut c = vec![0i128; b.len() + 1];
        for (k, &v) in b.iter().enumerate() {
            c[k + 1] += v;
        }
        for (k, &v) in a.iter().enumerate() {
            c[k] -= v;
        }
        a = b;
        b = c;
    }
    b
}

/// All spin assignments on a support (n_p = 2 j_p >= 1) with total at most `budget` whose every
/// off link admits an invariant.
fn spin_assignments(lat: &Lat, s: &[u32], budget: usize) -> Vec<Vec<usize>> {
    let mut out = Vec::new();
    let k = s.len();
    if k > budget {
        return out;
    }
    let mut cur = vec![1usize; k];
    let mut link_ps: HashMap<u32, Vec<usize>, FxB> = HashMap::default();
    for (i, &p) in s.iter().enumerate() {
        for &l in &lat.plaq_links[p as usize] {
            if lat.link_kind[l as usize] == 0 {
                link_ps.entry(l).or_default().push(i);
            }
        }
    }
    let links: Vec<Vec<usize>> = {
        let mut v: Vec<(u32, Vec<usize>)> = link_ps.into_iter().collect();
        v.sort();
        v.into_iter().map(|e| e.1).collect()
    };
    fn rec(
        i: usize,
        left: usize,
        cur: &mut Vec<usize>,
        links: &[Vec<usize>],
        out: &mut Vec<Vec<usize>>,
    ) {
        if i == cur.len() {
            for ps in links {
                let sp: Vec<usize> = ps.iter().map(|&q| cur[q]).collect();
                if invariants(&sp) == 0 {
                    return;
                }
            }
            out.push(cur.clone());
            return;
        }
        for extra in 0..=left {
            cur[i] = 1 + extra;
            rec(i + 1, left - extra, cur, links, out);
        }
        cur[i] = 1;
    }
    rec(0, budget - k, &mut cur, &links, &mut out);
    out
}

/// Phi_S(j; V) = E_V[prod_p chi_{j_p}(U_p)] as a polynomial in coarse trace words.
fn polymer_phi(lat: &Lat, ig: &mut Integrator, s: &[u32], spins: &[usize]) -> Poly {
    let mut poly = Poly::default();
    poly_add(&mut poly, Vec::new(), Q::one());
    for (i, &p) in s.iter().enumerate() {
        let w = lat.plaq_word(p as usize);
        let ch = cheb(spins[i]);
        let mut f = Poly::default();
        for (k, &c) in ch.iter().enumerate() {
            if c != 0 {
                let (t, cc) = make_term(vec![w.clone(); k], Q::int(c));
                poly_add(&mut f, t, cc);
            }
        }
        poly = poly_mul(&poly, &f);
    }
    let mut offs: Vec<(usize, u32)> = Vec::new();
    let mut seen: BTreeSet<u32> = BTreeSet::new();
    for &p in s {
        for &l in &lat.plaq_links[p as usize] {
            if lat.link_kind[l as usize] == 0 && seen.insert(l) {
                let cnt = s
                    .iter()
                    .filter(|&&q| lat.plaq_links[q as usize].contains(&l))
                    .count();
                offs.push((cnt, l));
            }
        }
    }
    offs.sort();
    let vars: Vec<u32> = offs.iter().map(|e| e.1).collect();
    ig.integrate_vars(&poly, &vars)
}

#[derive(Clone)]
struct Cand {
    tag: &'static str,
    shape: Vec<(u32, u32)>,
    f: Poly,
}

fn vletter(c: usize, inv: bool) -> u32 {
    ((VOFF + c as u32) << 1) | inv as u32
}

/// The coarse plaquette at a coarse doubled center, as its four coarse link cells in word order.
fn cplaq(lat: &Lat, c: [i32; 4]) -> Option<([usize; 4], Word)> {
    let dims: Vec<usize> = (0..lat.d).filter(|&k| c[k] % 2 != 0).collect();
    if dims.len() != 2 {
        return None;
    }
    let (mu, nu) = (dims[0], dims[1]);
    let cells = [
        lat.ccell(lat.cshift(c, nu, -1)),
        lat.ccell(lat.cshift(c, mu, 1)),
        lat.ccell(lat.cshift(c, nu, 1)),
        lat.ccell(lat.cshift(c, mu, -1)),
    ];
    let w = vec![
        vletter(cells[0], false),
        vletter(cells[1], false),
        vletter(cells[2], true),
        vletter(cells[3], true),
    ];
    Some((cells, w))
}

fn tr_poly(w: &[u32]) -> Poly {
    poly_from(vec![w.to_vec()], Q::one())
}

fn chi_poly(w: &[u32], n: usize) -> Poly {
    let ch = cheb(n);
    let mut f = Poly::default();
    for (k, &c) in ch.iter().enumerate() {
        if c != 0 {
            let (t, cc) = make_term(vec![w.to_vec(); k], Q::int(c));
            poly_add(&mut f, t, cc);
        }
    }
    f
}

fn loop6_tag(dirs: &[(usize, i32)]) -> &'static str {
    let nd: BTreeSet<usize> = dirs.iter().map(|e| e.0).collect();
    if nd.len() == 2 {
        return "rect";
    }
    let anti = (0..3).all(|i| dirs[i].0 == dirs[i + 3].0 && dirs[i].1 == -dirs[i + 3].1);
    if anti {
        "twisted_hex"
    } else {
        "chair"
    }
}

/// The named functionals of note section 4 with their links inside the support `a`.
fn candidates(lat: &Lat, a: &BTreeSet<usize>) -> Vec<Cand> {
    let mut out: Vec<Cand> = Vec::new();
    let mut plaqs: Vec<([usize; 4], Word)> = Vec::new();
    let mut seenp: BTreeSet<usize> = BTreeSet::new();
    let mut tubes: Vec<usize> = Vec::new();
    for &l in a {
        let c = lat.ccoords(l);
        let mu = (0..lat.d).find(|&k| c[k] % 2 != 0).unwrap_or(0);
        if lat.cm[mu] == 2 {
            tubes.push(l);
        }
        for nu in 0..lat.d {
            if nu == mu {
                continue;
            }
            for s in [-1, 1] {
                let pc = lat.cshift(c, nu, s);
                let pcell = lat.ccell(pc);
                if seenp.contains(&pcell) {
                    continue;
                }
                if let Some((cells, w)) = cplaq(lat, pc) {
                    if cells.iter().all(|x| a.contains(x)) {
                        seenp.insert(pcell);
                        plaqs.push((cells, w));
                    }
                }
            }
        }
    }
    for (cells, w) in &plaqs {
        let shape: Vec<(u32, u32)> = cells.iter().map(|&c| (c as u32, 0)).collect();
        out.push(Cand {
            tag: "plaq_half",
            shape: shape.clone(),
            f: chi_poly(w, 1),
        });
        out.push(Cand {
            tag: "plaq_one",
            shape: shape.clone(),
            f: chi_poly(w, 2),
        });
        out.push(Cand {
            tag: "plaq_threehalf",
            shape,
            f: chi_poly(w, 3),
        });
    }
    for &t in &tubes {
        let w = vec![vletter(t, false)];
        out.push(Cand {
            tag: "tube_half",
            shape: vec![(t as u32, 0)],
            f: chi_poly(&w, 1),
        });
        out.push(Cand {
            tag: "tube_one",
            shape: vec![(t as u32, 0)],
            f: chi_poly(&w, 2),
        });
    }
    for i in 0..tubes.len() {
        for j in i + 1..tubes.len() {
            let (a1, a2) = (tubes[i], tubes[j]);
            let f = poly_mul(
                &tr_poly(&[vletter(a1, false)]),
                &tr_poly(&[vletter(a2, false)]),
            );
            out.push(Cand {
                tag: "tube_pair",
                shape: vec![(a1 as u32, 0), (a2 as u32, 0)],
                f,
            });
        }
    }
    // simple 6-cycles through coarse sites, links of a only, self-loops left out
    let mut adj: Adj = BTreeMap::new();
    for &l in a {
        let c = lat.ccoords(l);
        let mu = (0..lat.d).find(|&k| c[k] % 2 != 0).unwrap_or(0);
        let s0 = lat.ccell(lat.cshift(c, mu, -1));
        let s1 = lat.ccell(lat.cshift(c, mu, 1));
        if s0 == s1 {
            continue;
        }
        adj.entry(s0).or_default().push((s1, l, false, mu, 1));
        adj.entry(s1).or_default().push((s0, l, true, mu, -1));
    }
    let mut cycles: BTreeSet<Vec<usize>> = BTreeSet::new();
    let starts: Vec<usize> = adj.keys().copied().collect();
    for &st in &starts {
        let mut path: Vec<(usize, usize, bool, usize, i32)> = Vec::new();
        let mut sites: Vec<usize> = vec![st];
        cyc_dfs(&adj, st, st, &mut sites, &mut path, &mut cycles, &mut out);
    }
    // pairs of coarse plaquettes
    for i in 0..plaqs.len() {
        for j in i + 1..plaqs.len() {
            let (ci, wi) = &plaqs[i];
            let (cj, wj) = &plaqs[j];
            let shared: Vec<usize> = ci.iter().copied().filter(|x| cj.contains(x)).collect();
            let mut shape: Vec<(u32, u32)> =
                ci.iter().chain(cj.iter()).map(|&c| (c as u32, 0)).collect();
            shape.sort();
            shape.dedup();
            if shared.len() == 1 {
                // N1 = chi(P) chi(Q) - (1/2) chi(loop), spin 1 on the shared link
                let loopw = six_loop_of(ci, wi, cj, wj, shared[0]);
                let f = poly_sum(
                    &poly_mul(&tr_poly(wi), &tr_poly(wj)),
                    &poly_scale(&tr_poly(&loopw), &Q::frac(-1, 2)),
                );
                let sh: Vec<(u32, u32)> = shape
                    .iter()
                    .map(|&(c, _)| (c, if c as usize == shared[0] { 1 } else { 0 }))
                    .collect();
                out.push(Cand {
                    tag: "n1",
                    shape: sh,
                    f,
                });
            } else if shared.is_empty() {
                out.push(Cand {
                    tag: "pair",
                    shape,
                    f: poly_mul(&tr_poly(wi), &tr_poly(wj)),
                });
            }
        }
    }
    out
}

fn six_loop_of(_ci: &[usize; 4], wi: &[u32], _cj: &[usize; 4], wj: &[u32], shared: usize) -> Word {
    // rotate each plaquette word so the shared link comes first, then join P with Q^-1 or Q
    let rot = |w: &[u32]| -> Word {
        let k = w
            .iter()
            .position(|&l| ((l >> 1) - VOFF) as usize == shared)
            .unwrap_or(0);
        w[k..].iter().chain(w[..k].iter()).copied().collect()
    };
    let p = rot(wi);
    let q = rot(wj);
    // p = s A, q = s' B with s, s' the shared letter in either orientation: the loop is A B^-1 ...
    let qa: Word = if p[0] == q[0] {
        word_inv(&q)
    } else {
        q[1..].iter().chain(q[..1].iter()).copied().collect()
    };
    let mut w = p.clone();
    w.extend(qa.iter().copied());
    reduce_word(&w)
}

/// Coarse sites to (neighbor site, coarse link, traversed backward, direction, sign).
type Adj = BTreeMap<usize, Vec<(usize, usize, bool, usize, i32)>>;

fn cyc_dfs(
    adj: &Adj,
    st: usize,
    at: usize,
    sites: &mut Vec<usize>,
    path: &mut Vec<(usize, usize, bool, usize, i32)>,
    seen: &mut BTreeSet<Vec<usize>>,
    out: &mut Vec<Cand>,
) {
    if path.len() == 6 {
        return;
    }
    if let Some(nb) = adj.get(&at) {
        for &(to, l, inv, mu, sg) in nb {
            if path.iter().any(|e| e.1 == l) {
                continue;
            }
            if to == st && path.len() == 5 {
                let mut full = path.clone();
                full.push((to, l, inv, mu, sg));
                let mut key: Vec<usize> = full.iter().map(|e| e.1).collect();
                key.sort();
                if seen.insert(key.clone()) {
                    let w: Word = full.iter().map(|e| vletter(e.1, e.2)).collect();
                    let dirs: Vec<(usize, i32)> = full.iter().map(|e| (e.3, e.4)).collect();
                    let tag = loop6_tag(&dirs);
                    out.push(Cand {
                        tag,
                        shape: key.iter().map(|&c| (c as u32, 0)).collect(),
                        f: tr_poly(&w),
                    });
                }
                continue;
            }
            if to == st || sites.contains(&to) || to < st {
                continue;
            }
            sites.push(to);
            path.push((to, l, inv, mu, sg));
            cyc_dfs(adj, st, to, sites, path, seen, out);
            path.pop();
            sites.pop();
        }
    }
}

/// Coarse V-support of a polynomial.
fn vsupport(p: &Poly) -> BTreeSet<usize> {
    poly_vars(p)
        .into_iter()
        .filter(|&v| v >= VOFF)
        .map(|v| (v - VOFF) as usize)
        .collect()
}

#[derive(Default, Clone)]
struct ShapeInfo {
    name: String,
    per_site_num: i128,
    per_site_den: i128,
}

struct Readout {
    /// (tag, canonical shape key) -> coefficient of each placed functional of that shape
    coef: Vec<((String, Vec<u32>), Q)>,
    residual: Q,
    mean: Q,
}

struct Engine<'a> {
    offered: BTreeMap<String, usize>,
    lat: &'a Lat,
    shapes: BTreeMap<(String, Vec<u32>), ShapeInfo>,
    norms: HashMap<(String, Vec<u32>), Q>,
    readouts: u64,
}

impl<'a> Engine<'a> {
    fn shape_key(&mut self, tag: &str, shape: &[(u32, u32)]) -> (String, Vec<u32>) {
        let c = canon_coarse(self.lat, shape);
        let key = (tag.to_string(), c.key.clone());
        if !self.shapes.contains_key(&key) {
            let pg = self.lat.pg.len() as i128;
            let st = (c.nmatch * c.tstab) as i128;
            self.shapes.insert(
                key.clone(),
                ShapeInfo {
                    name: tag.to_string(),
                    per_site_num: pg,
                    per_site_den: st,
                },
            );
        }
        key
    }
    fn readout(&mut self, ig: &mut Integrator, phi: &Poly) -> Readout {
        self.readouts += 1;
        let a = vsupport(phi);
        let mean = ig.integrate_all(phi);
        let mut coef = Vec::new();
        let mut captured = Q::zero();
        for cand in candidates(self.lat, &a) {
            *self.offered.entry(cand.tag.to_string()).or_insert(0) += 1;
            let key = self.shape_key(cand.tag, &cand.shape);
            let b = ig.inner(&cand.f, phi);
            if b.is_zero() {
                continue;
            }
            let g = match self.norms.get(&key) {
                Some(g) => g.clone(),
                None => {
                    let g = ig.inner(&cand.f, &cand.f);
                    self.norms.insert(key.clone(), g.clone());
                    g
                }
            };
            let c = b.div(&g);
            captured = captured.add(&b.mul(&c));
            coef.push((key, c));
        }
        let total = ig.inner(phi, phi).sub(&mean.mul(&mean));
        Readout {
            coef,
            residual: total.sub(&captured),
            mean,
        }
    }
}

// ---------------------------------------------------------------- the coefficient table

#[derive(Default)]
struct Table {
    /// log rho coefficient series per shape
    logc: BTreeMap<(String, Vec<u32>), Ser>,
    /// the single-polymer part (the partition function's families of one polymer)
    single: BTreeMap<(String, Vec<u32>), Ser>,
    /// the cluster part
    cluster: BTreeMap<(String, Vec<u32>), Ser>,
    /// Parseval residual weighted, per order
    residual: Ser,
    parts: Vec<String>,
}

fn add_into(m: &mut BTreeMap<(String, Vec<u32>), Ser>, k: &(String, Vec<u32>), s: &Ser) {
    let e = m.entry(k.clone()).or_insert_with(Ser::zero);
    *e = e.add(s);
}

// ---------------------------------------------------------------- one dimension: search, Z2, SU(2)

struct ClassRec {
    plaqs: Vec<u32>,
    nmatch: usize,
    tstab: usize,
}

fn classes_from(lat: &Lat, sets: &[Vec<u32>]) -> (Vec<ClassRec>, usize) {
    let mut by: BTreeMap<Vec<u32>, ClassRec> = BTreeMap::new();
    let mut tnorm: HashSet<Vec<u32>, FxB> = HashSet::default();
    let mut distinct = 0usize;
    for s in sets {
        // translation-normalized placed form first, then the full canonical form
        let mut v: Vec<u32> = s.clone();
        v.sort_unstable();
        if !tnorm.insert(v.clone()) {
            continue;
        }
        distinct += 1;
        let c = canon_plaqs(lat, &v);
        by.entry(c.key.clone()).or_insert_with(|| ClassRec {
            plaqs: plaqs_from_key(lat, &c.key),
            nmatch: c.nmatch,
            tstab: c.tstab,
        });
    }
    (by.into_values().collect(), distinct)
}

fn off_links_of(lat: &Lat, s: &[u32]) -> BTreeSet<u32> {
    let mut o = BTreeSet::new();
    for &p in s {
        for &l in &lat.plaq_links[p as usize] {
            if lat.link_kind[l as usize] == 0 {
                o.insert(l);
            }
        }
    }
    o
}

fn even_closed(lat: &Lat, s: &[u32]) -> bool {
    let mut c: HashMap<u32, u32, FxB> = HashMap::default();
    for &p in s {
        for &l in &lat.plaq_links[p as usize] {
            if lat.link_kind[l as usize] == 0 {
                *c.entry(l).or_insert(0) += 1;
            }
        }
    }
    c.values().all(|v| v % 2 == 0)
}

/// Z2: the coarse links carrying an odd count of position-1 occurrences.
fn z2_cycle(lat: &Lat, s: &[u32]) -> BTreeSet<u32> {
    let mut c: BTreeMap<u32, u32> = BTreeMap::new();
    for &p in s {
        for &l in &lat.plaq_links[p as usize] {
            if lat.link_kind[l as usize] == 2 {
                *c.entry(lat.link_coarse[l as usize]).or_insert(0) += 1;
            }
        }
    }
    c.into_iter()
        .filter(|e| e.1 % 2 == 1)
        .map(|e| e.0)
        .collect()
}

fn coarse_tag_z2(lat: &Lat, cyc: &BTreeSet<u32>) -> String {
    // name the Z2 character by its links: a plaquette, a 6-loop, a pair, or other
    let a: BTreeSet<usize> = cyc.iter().map(|&c| c as usize).collect();
    let cands = candidates(lat, &a);
    for c in &cands {
        let cells: BTreeSet<usize> = c.shape.iter().map(|e| e.0 as usize).collect();
        if cells == a
            && (c.tag == "plaq_half"
                || c.tag == "chair"
                || c.tag == "rect"
                || c.tag == "twisted_hex"
                || c.tag == "pair")
        {
            return if c.tag == "plaq_half" {
                "W_P".to_string()
            } else {
                "W_".to_string() + c.tag
            };
        }
    }
    "W_other_".to_string() + &a.len().to_string()
}

struct DimResult {
    offered: BTreeMap<String, usize>,
    table: Table,
    shapes: BTreeMap<(String, Vec<u32>), ShapeInfo>,
    stats: Vec<String>,
    max_extent: i32,
}

fn small_class_search(lat: &Lat, max: usize, out: &mut Out) -> (Vec<ClassRec>, u64) {
    // seeds: one plaquette from each orbit of single plaquettes
    let mut reps: BTreeMap<Vec<u32>, u32> = BTreeMap::new();
    for p in 0..lat.nplaq() as u32 {
        let c = canon_plaqs(lat, &[p]);
        reps.entry(c.key).or_insert(p);
    }
    let mut srch = Search::new(lat, false, max);
    for &seed in reps.values() {
        srch.run_from(seed);
    }
    let (cl, _) = classes_from(lat, &srch.closed);
    out.note(
        &("small search plaquette_orbits=".to_string()
            + &reps.len().to_string()
            + "|classes="
            + &cl.len().to_string()),
    );
    (cl, srch.states)
}

fn partners(lat: &Lat, s1: &[u32], max: usize) -> (Vec<Vec<u32>>, u64) {
    let offs = off_links_of(lat, s1);
    let mut seeds: BTreeSet<u32> = BTreeSet::new();
    for &l in &offs {
        for &q in &lat.link_plaqs[l as usize] {
            seeds.insert(q);
        }
    }
    let mut srch = Search::new(lat, false, max);
    for &sd in &seeds {
        srch.run_from(sd);
    }
    let mut found: BTreeSet<Vec<u32>> = BTreeSet::new();
    for s in &srch.closed {
        let o2 = off_links_of(lat, s);
        if o2.iter().any(|l| offs.contains(l)) {
            found.insert(s.clone());
        }
    }
    (found.into_iter().collect(), srch.states)
}

fn run_dimension(
    out: &mut Out,
    ig: &mut Integrator,
    lat: &Lat,
    label: &str,
    top: usize,
    wts: &[Ser],
    z2: bool,
) -> DimResult {
    let mut stats: Vec<String> = Vec::new();
    let sab = sabotage();
    // ---- E1, E2: supports holding position 0 of the coarse link l0 = (0, e_0)
    let (p0, p1) = lat.coarse_link_positions(lat.ccell([1, 0, 0, 0]));
    let seeds: Vec<u32> = lat.link_plaqs[p0].clone();
    let mut costs: Vec<String> = Vec::new();
    for mx in [6usize, 8] {
        if mx >= top {
            continue;
        }
        let t = Instant::now();
        let mut sm = Search::new(lat, false, mx);
        for &sd in &seeds {
            sm.run_from(sd);
        }
        let (cl, _) = classes_from(lat, &sm.closed);
        out.note(
            &(label.to_string()
                + "|cost_at_max_size="
                + &mx.to_string()
                + "|ms="
                + &t.elapsed().as_millis().to_string()),
        );
        costs.push(
            "max_size_".to_string()
                + &mx.to_string()
                + ":states="
                + &sm.states.to_string()
                + ":classes="
                + &cl.len().to_string(),
        );
    }
    let t_search = Instant::now();
    let mut srch = Search::new(lat, false, top);
    for &sd in &seeds {
        srch.run_from(sd);
    }
    let held: Vec<Vec<u32>> = srch
        .closed
        .iter()
        .filter(|s| {
            s.iter()
                .any(|&p| lat.plaq_links[p as usize].contains(&(p1 as u32)))
        })
        .cloned()
        .collect();
    let (classes, distinct) = classes_from(lat, &held);
    let search_ms = t_search.elapsed().as_millis();
    out.note(
        &(label.to_string()
            + "|search_states="
            + &srch.states.to_string()
            + "|closed_placed="
            + &srch.closed.len().to_string()
            + "|holding_both_positions="
            + &held.len().to_string()
            + "|classes="
            + &classes.len().to_string()
            + "|ms="
            + &search_ms.to_string()),
    );
    let mut by_size: BTreeMap<usize, usize> = BTreeMap::new();
    for c in &classes {
        *by_size.entry(c.plaqs.len()).or_insert(0) += 1;
    }
    let bs: Vec<String> = by_size
        .iter()
        .map(|(k, v)| k.to_string() + ":" + &v.to_string())
        .collect();
    out.row(
        "YM4_03C_SUPPORTS|".to_string()
            + label
            + "|seeds=plaquettes_at_position_0_of_l0="
            + &seeds.len().to_string()
            + "|max_size="
            + &top.to_string()
            + "|closure=every_off_link_in_at_least_two_plaquettes,connected_through_off_links|search_states="
            + &srch.states.to_string()
            + "|closed_placed_sets="
            + &srch.closed.len().to_string()
            + "|placed_holding_both_positions_of_l0="
            + &distinct.to_string()
            + "|classes_by_size="
            + &bs.join(",")
            + "|classes="
            + &classes.len().to_string()
            + "|tag=MEASURED",
    );
    stats.push("search_states=".to_string() + &srch.states.to_string());
    if !costs.is_empty() {
        out.row(
            "YM4_03C_SEARCH_COST|".to_string()
                + label
                + "|"
                + &costs.join(",")
                + "|max_size_"
                + &top.to_string()
                + ":states="
                + &srch.states.to_string()
                + ":classes="
                + &classes.len().to_string()
                + "|tag=MEASURED",
        );
    }
    // the small classes (cost <= top - 4) for clusters, from every plaquette orbit
    let small_max = top.saturating_sub(4).max(4);
    let (small, small_states) = small_class_search(lat, small_max, out);
    let mut small_sizes: BTreeMap<usize, usize> = BTreeMap::new();
    for c in &small {
        *small_sizes.entry(c.plaqs.len()).or_insert(0) += 1;
    }
    let ss: Vec<String> = small_sizes
        .iter()
        .map(|(k, v)| k.to_string() + ":" + &v.to_string())
        .collect();
    out.row(
        "YM4_03C_SMALL_SUPPORTS|".to_string()
            + label
            + "|seeds=one_plaquette_per_orbit|max_size="
            + &small_max.to_string()
            + "|search_states="
            + &small_states.to_string()
            + "|classes_by_size="
            + &ss.join(",")
            + "|tag=MEASURED",
    );
    let min_size = small.iter().map(|c| c.plaqs.len()).min().unwrap_or(0);
    out.check(
        &("minimum_support_size_".to_string() + label),
        min_size == 4,
        &min_size.to_string(),
    );
    let pg = lat.pg.len() as i128;
    let orbit_factor = |c: &ClassRec| -> Q {
        if sab == "dropped_multiplicity" {
            Q::one()
        } else {
            Q::frac(pg, (c.nmatch * c.tstab) as i128)
        }
    };
    // per-class stabilizers into the records
    let mut stab_rows: Vec<String> = Vec::new();
    for c in classes.iter().take(4) {
        stab_rows.push(c.plaqs.len().to_string() + ":" + &(c.nmatch * c.tstab).to_string());
    }
    // ---- E0: the Z2 control on the same classes
    let mut eng = Engine {
        offered: BTreeMap::new(),
        lat,
        shapes: BTreeMap::new(),
        norms: HashMap::new(),
        readouts: 0,
    };
    let mut table = Table {
        residual: Ser::zero(),
        ..Default::default()
    };
    if z2 {
        let mut z2c: BTreeMap<String, Ser> = BTreeMap::new();
        let mut z2counts: BTreeMap<String, BTreeMap<usize, Q>> = BTreeMap::new();
        for c in &classes {
            if !even_closed(lat, &c.plaqs) {
                continue;
            }
            let cyc = z2_cycle(lat, &c.plaqs);
            if cyc.is_empty() {
                continue;
            }
            let name = coarse_tag_z2(lat, &cyc);
            let shp: Vec<(u32, u32)> = cyc.iter().map(|&x| (x, 0)).collect();
            let key = eng.shape_key(if name == "W_P" { "plaq_half" } else { "z2" }, &shp);
            let info = eng.shapes.get(&key).cloned().unwrap_or_default();
            let f = orbit_factor(c).mul(&Q::frac(info.per_site_den, info.per_site_num));
            let mut s = Ser::zero();
            s.0[c.plaqs.len()] = f.clone();
            let e = z2c.entry(name.clone()).or_insert_with(Ser::zero);
            *e = e.add(&s);
            let m = z2counts.entry(name).or_default();
            let v = m.entry(c.plaqs.len()).or_insert_with(Q::zero);
            *v = v.add(&f);
        }
        // clusters: ordered incompatible pairs, -1/2 u^(|g1|+|g2|), g1 over small classes
        for c1 in &small {
            if !even_closed(lat, &c1.plaqs) {
                continue;
            }
            let rem = top - c1.plaqs.len();
            if rem < 4 {
                continue;
            }
            let (ps, _) = partners(lat, &c1.plaqs, rem);
            let cyc1 = z2_cycle(lat, &c1.plaqs);
            for s2 in &ps {
                if !even_closed(lat, s2) {
                    continue;
                }
                let cyc2 = z2_cycle(lat, s2);
                let cyc: BTreeSet<u32> = cyc1.symmetric_difference(&cyc2).copied().collect();
                if cyc.is_empty() {
                    continue;
                }
                let name = coarse_tag_z2(lat, &cyc);
                let shp: Vec<(u32, u32)> = cyc.iter().map(|&x| (x, 0)).collect();
                let key = eng.shape_key(if name == "W_P" { "plaq_half" } else { "z2" }, &shp);
                let info = eng.shapes.get(&key).cloned().unwrap_or_default();
                let f = orbit_factor(c1)
                    .mul(&Q::frac(info.per_site_den, info.per_site_num))
                    .mul(&Q::frac(-1, 2));
                let mut s = Ser::zero();
                s.0[c1.plaqs.len() + s2.len()] = f.clone();
                let e = z2c.entry(name.clone()).or_insert_with(Ser::zero);
                *e = e.add(&s);
                let m = z2counts.entry(name.clone() + "_clusters").or_default();
                let v = m.entry(c1.plaqs.len() + s2.len()).or_insert_with(Q::zero);
                *v = v.add(&f);
            }
        }
        for (name, s) in &z2c {
            let terms: Vec<String> = (0..=top)
                .filter(|&k| !s.0[k].is_zero())
                .map(|k| s.0[k].show() + "u^" + &k.to_string())
                .collect();
            out.row(
                "YM4_03C_Z2|".to_string()
                    + label
                    + "|character="
                    + name
                    + "|log_rho_coefficient="
                    + &(if terms.is_empty() {
                        "0".to_string()
                    } else {
                        terms.join("+")
                    })
                    + "|through=u^"
                    + &top.to_string()
                    + "|tag=MEASURED",
            );
        }
        for (name, m) in &z2counts {
            let parts: Vec<String> = m
                .iter()
                .map(|(k, v)| k.to_string() + ":" + &v.show())
                .collect();
            out.row(
                "YM4_03C_Z2_PARTS|".to_string()
                    + label
                    + "|character="
                    + name
                    + "|by_size="
                    + &parts.join(",")
                    + "|tag=MEASURED",
            );
        }
        let get = |n: &str, k: usize| -> String {
            z2c.get(n)
                .map(|s| s.0[k].show())
                .unwrap_or_else(|| "0".to_string())
        };
        let dval = if lat.d == 4 { "16" } else { "8" };
        out.read(
            "P8c",
            &(label.to_string() + "_W_P_u^4"),
            &get("W_P", 4),
            "1",
            true,
        );
        out.read(
            "P8c",
            &(label.to_string() + "_W_P_u^6"),
            &get("W_P", 6),
            "0",
            true,
        );
        out.read(
            "P8c",
            &(label.to_string() + "_W_P_u^8"),
            &get("W_P", 8),
            dval,
            true,
        );
        out.read(
            "P8c",
            &(label.to_string() + "_W_P_u^10"),
            &get("W_P", 10),
            "0",
            true,
        );
        for k in [4usize, 6, 8] {
            out.read(
                "P8",
                &(label.to_string() + "_W_PW_Q_perpendicular_u^" + &k.to_string()),
                &get("W_chair", k),
                "0",
                true,
            );
        }
        out.read(
            "P8",
            &(label.to_string() + "_W_PW_Q_perpendicular_u^10"),
            &get("W_chair", 10),
            "3",
            true,
        );
        let others: Vec<String> = z2c
            .iter()
            .filter(|(n, s)| *n != "W_P" && *n != "W_chair" && s.0.iter().any(|q| !q.is_zero()))
            .map(|(n, _)| n.clone())
            .collect();
        out.row(
            "YM4_03C_Z2_OTHER_CHARACTERS|".to_string()
                + label
                + "|nonzero_through_u^"
                + &top.to_string()
                + "="
                + &(if others.is_empty() {
                    "none".to_string()
                } else {
                    others.join(",")
                })
                + "|tag=MEASURED",
        );
        z2_parallel(out, lat, label);
    }
    // ---- E3..E6: SU(2) polymers on every class, their activities and readouts
    out.note(&(label.to_string() + " su2 polymers"));
    let t_su2 = Instant::now();
    let mut npoly = 0u64;
    let mut nzero = 0u64;
    let mut odd_nonzero = 0u64;
    let mut vindep = 0u64;
    let mut max_extent = 0i32;
    let mut class_rows: Vec<String> = Vec::new();
    let mut brute_2i = Big::from_u128(0);
    for (ci, c) in classes.iter().enumerate() {
        let spins_all = spin_assignments(lat, &c.plaqs, top);
        let of = orbit_factor(c);
        let noff = off_links_of(lat, &c.plaqs).len();
        for spins in spins_all {
            let cost: usize = spins.iter().sum();
            ig.deg.take_local();
            let phi = polymer_phi(lat, ig, &c.plaqs, &spins);
            let deg_off = ig.deg.take_local();
            let mut b = Big::from_u128(1);
            for _ in 0..noff {
                b = b.mul(&Big::from_u128(120));
            }
            brute_2i = brute_2i.add(&b);
            npoly += 1;
            let sp: String = spins
                .iter()
                .map(|x| x.to_string())
                .collect::<Vec<_>>()
                .join("");
            let head = "YM4_03C_CLASS|".to_string()
                + label
                + "|class="
                + &ci.to_string()
                + "|plaquettes="
                + &c.plaqs.len().to_string()
                + "|off_links="
                + &noff.to_string()
                + "|stabilizer="
                + &(c.nmatch * c.tstab).to_string()
                + "|orbit_per_coarse_site="
                + &Q::frac(pg, (c.nmatch * c.tstab) as i128).show()
                + "|spins_2j="
                + &sp
                + "|cost="
                + &cost.to_string()
                + "|max_off_link_degree="
                + &deg_off.to_string();
            if phi.is_empty() {
                nzero += 1;
                class_rows.push(head + "|phi=0");
                continue;
            }
            if cost % 2 == 1 {
                odd_nonzero += 1;
            }
            let a = vsupport(&phi);
            if a.is_empty() {
                vindep += 1;
                class_rows.push(head + "|phi=constant_" + &poly_const(&phi).show());
                continue;
            }
            max_extent = max_extent.max(extent(lat, &c.plaqs));
            let r = eng.readout(ig, &phi);
            let deg_v = ig.deg.take_local();
            let rc: Vec<String> = r
                .coef
                .iter()
                .map(|(k, cf)| k.0.clone() + ":" + &cf.show())
                .collect();
            class_rows.push(
                head + "|max_V_link_degree_in_readout="
                    + &deg_v.to_string()
                    + "|coarse_links_in_phi="
                    + &a.len().to_string()
                    + "|readout_of_phi="
                    + &rc.join(",")
                    + "|parseval_residual="
                    + &r.residual.show(),
            );
            let mut w = Ser::one();
            for &n in &spins {
                w = w.mul(&wts[n]);
            }
            let wres = w.scale(&r.residual.mul(&of));
            table.residual = table.residual.add(&wres);
            let _ = r.mean;
            for (key, cf) in &r.coef {
                let info = eng.shapes.get(key).cloned().unwrap_or_default();
                let f = of
                    .mul(cf)
                    .mul(&Q::frac(info.per_site_den, info.per_site_num));
                let s = w.scale(&f);
                add_into(&mut table.logc, key, &s);
                add_into(&mut table.single, key, &s);
                if key.0 == "plaq_half" && (!s.0[10].is_zero() || !s.0[8].is_zero()) {
                    table.parts.push(
                        "size=".to_string()
                            + &c.plaqs.len().to_string()
                            + ":spins="
                            + &spins
                                .iter()
                                .map(|x| x.to_string())
                                .collect::<Vec<_>>()
                                .join("")
                            + ":b8="
                            + &s.0[8].show()
                            + ":b10="
                            + &s.0[10].show(),
                    );
                }
            }
        }
    }
    for r in class_rows {
        out.row(r + "|tag=MEASURED");
    }
    let su2_ms = t_su2.elapsed().as_millis();
    out.note(
        &(label.to_string()
            + " su2 singles done|polymers="
            + &npoly.to_string()
            + "|ms="
            + &su2_ms.to_string()),
    );
    // ---- clusters: g1 over small classes with cost <= top - 4, g2 placed and incompatible
    let mut ncl = 0u64;
    let mut cluster_states = 0u64;
    let mut cluster_rows: BTreeMap<String, usize> = BTreeMap::new();
    let mut min_cost = usize::MAX;
    for c1 in &small {
        for sp1 in spin_assignments(lat, &c1.plaqs, top) {
            let phi1 = polymer_phi(lat, ig, &c1.plaqs, &sp1);
            if !phi1.is_empty() {
                min_cost = min_cost.min(sp1.iter().sum());
            }
        }
    }
    out.check(
        &("minimum_polymer_cost_".to_string() + label),
        min_cost == 4,
        &min_cost.to_string(),
    );
    out.row(
        "YM4_03C_CLUSTER_ORDER|".to_string()
            + label
            + "|minimum_polymer_cost="
            + &min_cost.to_string()
            + "|so_clusters_of_three_or_more_start_at=beta^"
            + &(3 * min_cost).to_string()
            + "|above_the_top="
            + &(3 * min_cost > top).to_string()
            + "|tag=DERIVED_from_MEASURED",
    );
    for c1 in &small {
        let of = orbit_factor(c1);
        for sp1 in spin_assignments(lat, &c1.plaqs, top - min_cost) {
            let c1cost: usize = sp1.iter().sum();
            let phi1 = polymer_phi(lat, ig, &c1.plaqs, &sp1);
            if phi1.is_empty() {
                continue;
            }
            let rem = top - c1cost;
            let (ps, st) = if sab == "disconnected_cluster" {
                partners_with_compatible(lat, &c1.plaqs, rem)
            } else {
                partners(lat, &c1.plaqs, rem)
            };
            cluster_states += st;
            let mut w1 = Ser::one();
            for &n in &sp1 {
                w1 = w1.mul(&wts[n]);
            }
            for s2 in &ps {
                for sp2 in spin_assignments(lat, s2, rem) {
                    let phi2 = polymer_phi(lat, ig, s2, &sp2);
                    if phi2.is_empty() {
                        continue;
                    }
                    let prod = poly_mul(&phi1, &phi2);
                    if vsupport(&prod).is_empty() {
                        continue;
                    }
                    ncl += 1;
                    ig.deg.take_local();
                    let r = eng.readout(ig, &prod);
                    let deg_v = ig.deg.take_local();
                    let rc: Vec<String> = r
                        .coef
                        .iter()
                        .map(|(k, cf)| k.0.clone() + ":" + &cf.show())
                        .collect();
                    let key = "g1_plaquettes=".to_string()
                        + &c1.plaqs.len().to_string()
                        + ",g1_spins_2j="
                        + &sp1
                            .iter()
                            .map(|x| x.to_string())
                            .collect::<Vec<_>>()
                            .join("")
                        + ",g2_plaquettes="
                        + &s2.len().to_string()
                        + ",g2_spins_2j="
                        + &sp2
                            .iter()
                            .map(|x| x.to_string())
                            .collect::<Vec<_>>()
                            .join("")
                        + ",g1_orbit_per_site="
                        + &of.show()
                        + ",max_V_link_degree="
                        + &deg_v.to_string()
                        + ",readout_of_phi1phi2="
                        + &rc.join(";")
                        + ",residual="
                        + &r.residual.show();
                    *cluster_rows.entry(key).or_insert(0) += 1;
                    let mut w = w1.clone();
                    for &n in &sp2 {
                        w = w.mul(&wts[n]);
                    }
                    let half = Q::frac(-1, 2);
                    table.residual = table
                        .residual
                        .add(&w.scale(&r.residual.mul(&of).mul(&half)));
                    for (key, cf) in &r.coef {
                        let info = eng.shapes.get(key).cloned().unwrap_or_default();
                        let f = of
                            .mul(cf)
                            .mul(&Q::frac(info.per_site_den, info.per_site_num))
                            .mul(&half);
                        let s = w.scale(&f);
                        add_into(&mut table.logc, key, &s);
                        add_into(&mut table.cluster, key, &s);
                        if key.0 == "plaq_half" && (!s.0[10].is_zero() || !s.0[8].is_zero()) {
                            table.parts.push(
                                "cluster_size=".to_string()
                                    + &c1.plaqs.len().to_string()
                                    + "+"
                                    + &s2.len().to_string()
                                    + ":b8="
                                    + &s.0[8].show()
                                    + ":b10="
                                    + &s.0[10].show(),
                            );
                        }
                    }
                }
            }
        }
    }
    if sab == "wrong_sign" {
        for v in table.logc.values_mut() {
            *v = v.scale(&Q::int(-1));
        }
    }
    out.note(&(label.to_string() + " clusters done|pair_terms=" + &ncl.to_string()));
    for (k, n) in &cluster_rows {
        out.row(
            "YM4_03C_CLUSTER|".to_string()
                + label
                + "|ordered_pairs="
                + &n.to_string()
                + "|"
                + k
                + "|weight=-1/2_each|tag=MEASURED",
        );
    }
    out.row(
        "YM4_03C_POLYMERS|".to_string()
            + label
            + "|spin_assignments_integrated="
            + &npoly.to_string()
            + "|integrated_to_zero="
            + &nzero.to_string()
            + "|odd_cost_nonzero="
            + &odd_nonzero.to_string()
            + "|nonzero_V_independent="
            + &vindep.to_string()
            + "|pair_cluster_terms="
            + &ncl.to_string()
            + "|partner_search_states="
            + &cluster_states.to_string()
            + "|readouts="
            + &eng.readouts.to_string()
            + "|max_fine_extent_of_a_V-dependent_support="
            + &max_extent.to_string()
            + "|fine_side="
            + &lat.n[0].to_string()
            + "|tag=MEASURED",
    );
    stats.push("polymers=".to_string() + &npoly.to_string());
    stats.push(
        "brute_2I_products_replaced=sum_over_polymers_120^off_links=".to_string() + &brute_2i.dec(),
    );
    stats.push("odd_nonzero=".to_string() + &odd_nonzero.to_string());
    stats.push("max_extent=".to_string() + &max_extent.to_string());
    stats.push("search_ms=".to_string() + &search_ms.to_string());
    stats.push("su2_ms=".to_string() + &su2_ms.to_string());
    let _ = stab_rows;
    DimResult {
        offered: eng.offered.clone(),
        table,
        shapes: eng.shapes,
        stats,
        max_extent,
    }
}

fn partners_with_compatible(lat: &Lat, s1: &[u32], max: usize) -> (Vec<Vec<u32>>, u64) {
    // the planted error: partners also from supports that share only line links with s1
    let (mut ps, st) = partners(lat, s1, max);
    let mut seeds: BTreeSet<u32> = BTreeSet::new();
    for &p in s1 {
        for &l in &lat.plaq_links[p as usize] {
            if lat.link_kind[l as usize] != 0 {
                for &q in &lat.link_plaqs[l as usize] {
                    seeds.insert(q);
                }
            }
        }
    }
    let mut srch = Search::new(lat, false, max);
    for &sd in &seeds {
        srch.run_from(sd);
    }
    let have: BTreeSet<Vec<u32>> = ps.iter().cloned().collect();
    let mut extra: BTreeSet<Vec<u32>> = BTreeSet::new();
    for s in &srch.closed {
        if !have.contains(s) {
            extra.insert(s.clone());
        }
    }
    ps.extend(extra);
    (ps, st + srch.states)
}

fn extent(lat: &Lat, s: &[u32]) -> i32 {
    // the fine extent, read in each direction from coordinates unwrapped about the first plaquette
    let c0 = lat.coords(lat.plaq_cell[s[0] as usize] as usize);
    let mut mx = 0i32;
    for k in 0..lat.d {
        let mut lo = 0i32;
        let mut hi = 0i32;
        for &p in s {
            let c = lat.coords(lat.plaq_cell[p as usize] as usize);
            let mut dlt = (c[k] - c0[k]).rem_euclid(lat.m[k]);
            if dlt > lat.m[k] / 2 {
                dlt -= lat.m[k];
            }
            lo = lo.min(dlt);
            hi = hi.max(dlt);
        }
        mx = mx.max((hi - lo) / 2 + 1);
    }
    mx
}

fn z2_parallel(out: &mut Out, lat: &Lat, label: &str) {
    // P = coarse plaquette at 0 in plane (0,1); Q = P + e_2, parallel at coarse distance 1
    let pc = [1, 1, 0, 0];
    let qc = [1, 1, 2, 0];
    let req_of = |c: [i32; 4]| -> Vec<usize> {
        let (cells, _) = cplaq(lat, c).expect("coarse plaquette");
        let mut v = Vec::new();
        for cl in cells {
            let (a, b) = lat.coarse_link_positions(cl);
            v.push(a);
            v.push(b);
        }
        v
    };
    let cyc_of = |c: [i32; 4]| -> BTreeSet<u32> {
        let (cells, _) = cplaq(lat, c).expect("coarse plaquette");
        cells.iter().map(|&x| x as u32).collect()
    };
    let target: BTreeSet<u32> = cyc_of(pc)
        .symmetric_difference(&cyc_of(qc))
        .copied()
        .collect();
    let (p0, _) = lat.coarse_link_positions(lat.ccell([1, 0, 0, 0]));
    // connected polymers with the character W_P W_Q through u^12
    let mut srch = Search::new(lat, true, 12);
    let mut req = req_of(pc);
    req.extend(req_of(qc));
    srch.req = req;
    for &sd in &lat.link_plaqs[p0].clone() {
        srch.run_from(sd);
    }
    let mut connected: BTreeMap<usize, usize> = BTreeMap::new();
    for s in &srch.closed {
        if z2_cycle(lat, s) == target {
            *connected.entry(s.len()).or_insert(0) += 1;
        }
    }
    // pairs: polymers with character W_P against polymers with W_Q, sizes summing to <= 12
    let list_for = |c: [i32; 4]| -> Vec<Vec<u32>> {
        let mut s2 = Search::new(lat, true, 8);
        s2.req = req_of(c);
        let (cells, _) = cplaq(lat, c).expect("coarse plaquette");
        let (a0, _) = lat.coarse_link_positions(cells[0]);
        for &sd in &lat.link_plaqs[a0].clone() {
            s2.run_from(sd);
        }
        let want = cyc_of(c);
        let mut v: BTreeSet<Vec<u32>> = BTreeSet::new();
        for s in &s2.closed {
            if z2_cycle(lat, s) == want {
                v.insert(s.clone());
            }
        }
        v.into_iter().collect()
    };
    let lp = list_for(pc);
    let lq = list_for(qc);
    let mut incompatible = 0usize;
    for a in &lp {
        let oa = off_links_of(lat, a);
        for b in &lq {
            if a.len() + b.len() > 12 {
                continue;
            }
            let ob = off_links_of(lat, b);
            if oa.iter().any(|l| ob.contains(l)) {
                incompatible += 1;
            }
        }
    }
    let conn: Vec<String> = connected
        .iter()
        .map(|(k, v)| k.to_string() + ":" + &v.to_string())
        .collect();
    out.row(
        "YM4_03C_Z2_PARALLEL|".to_string()
            + label
            + "|pair=P_and_P+e2|search_states="
            + &srch.states.to_string()
            + "|connected_polymers_with_W_PW_Q_by_size="
            + &(if conn.is_empty() {
                "none".to_string()
            } else {
                conn.join(",")
            })
            + "|W_P_polymers_size<=8="
            + &lp.len().to_string()
            + "|W_Q_polymers_size<=8="
            + &lq.len().to_string()
            + "|incompatible_pairs_size<=12="
            + &incompatible.to_string()
            + "|clusters_of_three=only_three_fillings,character_W_P_or_W_Q|tag=MEASURED",
    );
    let coef = if connected.is_empty() && incompatible == 0 {
        "0"
    } else {
        "nonzero"
    };
    out.read(
        "P8",
        &(label.to_string() + "_W_PW_Q_parallel_through_u^12"),
        coef,
        "0",
        true,
    );
}

// ---------------------------------------------------------------- P1: the order-4 benchmark

struct Stream(u64);

impl Stream {
    fn next(&mut self, bound: u64) -> u64 {
        self.0 = self
            .0
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        (self.0 >> 33) % bound
    }
}

fn quaternion_pool(seed: u64, size: usize) -> Vec<[i128; 5]> {
    let mut st = Stream(seed);
    let mut pool = Vec::new();
    while pool.len() < size {
        let a = st.next(7) as i128 - 3;
        let b = st.next(7) as i128 - 3;
        let c = st.next(7) as i128 - 3;
        let d = st.next(7) as i128 - 3;
        if a != 0 || b != 0 || c != 0 || d != 0 {
            // (a + bi + cj + dk)^2 / |.|^2
            let s = [
                a * a - b * b - c * c - d * d,
                2 * a * b,
                2 * a * c,
                2 * a * d,
            ];
            let n = a * a + b * b + c * c + d * d;
            pool.push([s[0], s[1], s[2], s[3], n]);
        }
    }
    pool
}

fn qq_of(q: &[i128; 5]) -> Qq {
    Qq {
        w: Q::frac(q[0], q[4]),
        x: Q::frac(q[1], q[4]),
        y: Q::frac(q[2], q[4]),
        z: Q::frac(q[3], q[4]),
    }
}

fn section_p1(out: &mut Out, ig: &mut Integrator, g2t: &[Qp]) {
    out.note("P1 benchmark");
    let pool: Vec<[i128; 5]> = quaternion_pool(2026, 40)
        .into_iter()
        .filter(|q| q[1] != 0 || q[2] != 0 || q[3] != 0)
        .take(12)
        .collect();
    for (sides, want) in [
        ([2, 2, 2, 2], "-24359/438048"),
        ([4, 2, 2, 2], "-5693581/33434856"),
    ] {
        for position in [0u8, 1u8] {
            let lat = Lat::new(4, sides, position);
            // coarse links in the order of the YM4-03 test: coarse sites lexicographic, then direction
            let csides: Vec<i32> = (0..4).map(|k| lat.cm[k] / 2).collect();
            let mut corder: Vec<usize> = Vec::new();
            for x0 in 0..csides[0] {
                for x1 in 0..csides[1] {
                    for x2 in 0..csides[2] {
                        for x3 in 0..csides[3] {
                            for mu in 0..4 {
                                let mut c = [2 * x0, 2 * x1, 2 * x2, 2 * x3];
                                c[mu] += 1;
                                corder.push(lat.ccell(c));
                            }
                        }
                    }
                }
            }
            let count = corder.len();
            let assign = |pick: &dyn Fn(usize) -> Qq| -> HashMap<u32, Qq, FxB> {
                let mut m: HashMap<u32, Qq, FxB> = HashMap::default();
                for (k, &c) in corder.iter().enumerate() {
                    m.insert(VOFF + c as u32, pick(k));
                }
                m
            };
            let va = assign(&|k| qq_of(&pool[k % 12]));
            let mut vint: HashMap<u32, ([i128; 4], i128), FxB> = HashMap::default();
            for (k, &c) in corder.iter().enumerate() {
                let q = pool[k % 12];
                vint.insert(VOFF + c as u32, ([q[0], q[1], q[2], q[3]], q[4]));
            }
            let vb = assign(&|k| qq_of(&pool[(k * 5 + 3) % 12]));
            let v1 = assign(&|_| qq_one());
            // the admissible multisets, as test_one_scale_blocking.py enumerates them
            let nl = lat.link_cell.len();
            assert!(nl <= 128);
            let masks: Vec<u128> = (0..lat.nplaq())
                .map(|p| {
                    lat.plaq_links[p]
                        .iter()
                        .fold(0u128, |m, &l| m ^ (1u128 << l))
                })
                .collect();
            let mut groups: BTreeMap<u32, u128> = BTreeMap::new();
            let mut off_mask = 0u128;
            for l in 0..nl {
                if lat.link_kind[l] == 0 {
                    off_mask |= 1u128 << l;
                } else {
                    *groups.entry(lat.link_coarse[l]).or_insert(0) |= 1u128 << l;
                }
            }
            let gl: Vec<u128> = groups.values().copied().collect();
            let admissible = |m: u128| -> bool {
                m & off_mask == 0 && gl.iter().all(|&g| m & g == 0 || m & g == g)
            };
            let touching: Vec<usize> = (0..lat.nplaq())
                .filter(|&p| lat.plaq_word(p).iter().any(|&x| x >> 1 >= VOFF))
                .collect();
            let tset: BTreeSet<usize> = touching.iter().copied().collect();
            let n = lat.nplaq();
            let mut lists: BTreeMap<usize, Vec<Vec<(usize, usize)>>> = BTreeMap::new();
            let mut one: Vec<Vec<(usize, usize)>> = Vec::new();
            for &p in &touching {
                if admissible(masks[p]) {
                    one.push(vec![(p, 1)]);
                }
            }
            lists.insert(1, one);
            let mut two = Vec::new();
            for p in 0..n {
                for q in p..n {
                    if admissible(masks[p] ^ masks[q]) && (tset.contains(&p) || tset.contains(&q)) {
                        two.push(if p == q {
                            vec![(p, 2)]
                        } else {
                            vec![(p, 1), (q, 1)]
                        });
                    }
                }
            }
            lists.insert(2, two);
            let mut pairs: HashMap<u128, Vec<(usize, usize)>, FxB> = HashMap::default();
            for p in 0..n {
                for q in p..n {
                    pairs.entry(masks[p] ^ masks[q]).or_default().push((p, q));
                }
            }
            let mut totals: Vec<u128> = vec![0];
            for &g in &gl {
                let ext: Vec<u128> = totals.iter().map(|t| t ^ g).collect();
                totals.extend(ext);
            }
            for size in [3usize, 4] {
                let mut found: BTreeSet<Vec<usize>> = BTreeSet::new();
                if size == 3 {
                    for &p in &touching {
                        for &t in &totals {
                            if let Some(v) = pairs.get(&(masks[p] ^ t)) {
                                for &(q, r) in v {
                                    let mut k = vec![p, q, r];
                                    k.sort();
                                    found.insert(k);
                                }
                            }
                        }
                    }
                } else {
                    for &p in &touching {
                        for q in 0..n {
                            for &t in &totals {
                                if let Some(v) = pairs.get(&(masks[p] ^ masks[q] ^ t)) {
                                    for &(r, s) in v {
                                        let mut k = vec![p, q, r, s];
                                        k.sort();
                                        found.insert(k);
                                    }
                                }
                            }
                        }
                    }
                }
                let mut lst = Vec::new();
                for items in found {
                    let mut cnt: BTreeMap<usize, usize> = BTreeMap::new();
                    for p in items {
                        *cnt.entry(p).or_insert(0) += 1;
                    }
                    lst.push(cnt.into_iter().collect::<Vec<_>>());
                }
                lists.insert(size, lst);
            }
            let mut sums: BTreeMap<(usize, usize), Q> = BTreeMap::new();
            for vi in 0..3 {
                for size in 1..=4 {
                    sums.insert((vi, size), Q::zero());
                }
            }
            let mut lit_checked = 0usize;
            for (&size, lst) in &lists {
                for ms in lst {
                    let mut words: Vec<Word> = Vec::new();
                    let mut den = 1i128;
                    for &(p, m) in ms {
                        for _ in 0..m {
                            words.push(lat.plaq_word(p));
                        }
                        let mut f = 1i128;
                        for k in 2..=m as i128 {
                            f *= k;
                        }
                        den *= f;
                    }
                    let poly = poly_from(words, pow2_inv(size).div(&Q::int(den)));
                    let offs: Vec<u32> =
                        poly_vars(&poly).into_iter().filter(|&v| v < VOFF).collect();
                    let sym = ig.integrate_vars(&poly, &offs);
                    for (vi, vals) in [&v1, &va, &vb].iter().enumerate() {
                        let v = eval_poly_qq(&sym, vals);
                        let e = sums.entry((vi, size)).or_insert_with(Q::zero);
                        *e = e.add(&v);
                    }
                    // the 2T route, term by term, at V_a on the first lattice at position 1
                    if sides[0] == 2 && position == 1 {
                        let lit = literal_2t(&lat, ms, &vint, g2t);
                        let symv = eval_poly_qq(&sym, &va).mul(&Q::int(den));
                        out.check(
                            "G1_P1_terms_2T_equal_SU2",
                            lit == symv,
                            &("size=".to_string() + &size.to_string()),
                        );
                        lit_checked += 1;
                    }
                }
            }
            let independent =
                (1..=3).all(|s| sums[&(0, s)] == sums[&(1, s)] && sums[&(1, s)] == sums[&(2, s)]);
            out.check("P2_V_independent_below_order_4", independent, "");
            // the law: (1/128)(coarse chi(V_a) - coarse chi(1))
            let coarse_chi = |vals: &HashMap<u32, Qq, FxB>| -> Q {
                let mut s = Q::zero();
                for site in 0..lat.coarse_sites() {
                    let mut c = [0i32; 4];
                    let mut r = site;
                    for k in 0..4 {
                        let side = (lat.cm[k] / 2) as usize;
                        c[k] = 2 * (r % side) as i32;
                        r /= side;
                    }
                    for mu in 0..4 {
                        for nu in mu + 1..4 {
                            let mut pc = c;
                            pc[mu] += 1;
                            pc[nu] += 1;
                            let (_, w) = cplaq(&lat, pc).expect("coarse plaquette");
                            let mut q = qq_one();
                            for &l in &w {
                                let v = vals.get(&(l >> 1)).expect("V");
                                q = qq_mul(&q, &if l & 1 == 1 { qq_conj(v) } else { v.clone() });
                            }
                            s = s.add(&q.w.mul(&Q::int(2)));
                        }
                    }
                }
                s
            };
            let law = Q::frac(1, 128).mul(&coarse_chi(&va).sub(&coarse_chi(&v1)));
            let read = sums[&(1, 4)].sub(&sums[&(0, 4)]);
            let counts: Vec<String> = (1..=4).map(|s| lists[&s].len().to_string()).collect();
            let lab = sides
                .iter()
                .map(|x| x.to_string())
                .collect::<Vec<_>>()
                .join("x");
            out.row(
                "YM4_03C_P1_BENCHMARK|fine=".to_string()
                    + &lab
                    + "|coarse_links="
                    + &count.to_string()
                    + "|V_at_position="
                    + &position.to_string()
                    + "|survivors_size_1,2,3,4="
                    + &counts.join(",")
                    + "|V_independent_below_order_4="
                    + &(independent as u8).to_string()
                    + "|E[X^4]/4!_difference="
                    + &read.show()
                    + "|law="
                    + &law.show()
                    + "|2T_terms_checked="
                    + &lit_checked.to_string()
                    + "|tag=MEASURED",
            );
            out.read(
                "P1",
                &("fine_".to_string() + &lab + "_position_" + &position.to_string()),
                &read.show(),
                want,
                true,
            );
        }
    }
}

/// E_V[prod a_p^m] by averages over 2T on the free off links after fixing a gauge at the sites
/// that touch no line link; every free link's degree is checked <= 5 before its average.
fn iq_mul(p: &[i128; 4], q: &[i128; 4]) -> [i128; 4] {
    let [a, b, c, d] = *p;
    let [e, f, g, h] = *q;
    [
        a * e - b * f - c * g - d * h,
        a * f + b * e + c * h - d * g,
        a * g - b * h + c * e + d * f,
        a * h + b * g - c * f + d * e,
    ]
}

fn literal_2t(
    lat: &Lat,
    ms: &[(usize, usize)],
    vals: &HashMap<u32, ([i128; 4], i128), FxB>,
    g2t: &[Qp],
) -> Q {
    let mut deg: BTreeMap<u32, usize> = BTreeMap::new();
    for &(p, m) in ms {
        for &l in &lat.plaq_links[p] {
            if lat.link_kind[l as usize] == 0 {
                *deg.entry(l).or_insert(0) += m;
            }
        }
    }
    let off: Vec<u32> = deg.keys().copied().collect();
    for &l in &off {
        assert!(deg[&l] <= 5, "beyond the 2T design degree");
    }
    let ends = |l: u32| -> (usize, usize) {
        let c = lat.coords(lat.link_cell[l as usize] as usize);
        let mu = (0..lat.d).find(|&k| c[k] % 2 != 0).unwrap_or(0);
        (
            lat.cell(lat.shift(c, mu, -1)),
            lat.cell(lat.shift(c, mu, 1)),
        )
    };
    let pure = |s: usize| -> bool {
        let c = lat.coords(s);
        (0..lat.d).filter(|&k| (c[k] / 2) % 2 != 0).count() >= 2
    };
    let mut anchored: BTreeSet<usize> = BTreeSet::new();
    for &l in &off {
        let (a, b) = ends(l);
        for s in [a, b] {
            if !pure(s) {
                anchored.insert(s);
            }
        }
    }
    let mut fixed: BTreeSet<u32> = BTreeSet::new();
    loop {
        let mut changed = true;
        while changed {
            changed = false;
            for &l in &off {
                if fixed.contains(&l) {
                    continue;
                }
                let (a, b) = ends(l);
                if a == b {
                    continue;
                }
                if anchored.contains(&a) != anchored.contains(&b) {
                    let o = if anchored.contains(&a) { b } else { a };
                    fixed.insert(l);
                    anchored.insert(o);
                    changed = true;
                }
            }
        }
        let root = off.iter().find(|&&l| {
            !fixed.contains(&l) && {
                let (a, b) = ends(l);
                a != b && !anchored.contains(&a) && !anchored.contains(&b)
            }
        });
        match root {
            Some(&l) => {
                anchored.insert(ends(l).0);
            }
            None => break,
        }
    }
    let free: Vec<u32> = off.iter().copied().filter(|l| !fixed.contains(l)).collect();
    let k = free.len();
    // integer quaternions: 2T elements times 2 with denominator 2, V with its own denominator,
    // a fixed link the identity with denominator 1; each word's denominator is then fixed.
    let elems: Vec<[i128; 4]> = g2t
        .iter()
        .map(|q| [q.c[0].0, q.c[1].0, q.c[2].0, q.c[3].0])
        .collect();
    let mut slot: HashMap<u32, usize, FxB> = HashMap::default();
    for (t, &l) in free.iter().enumerate() {
        slot.insert(l, t);
    }
    let words: Vec<(Word, usize)> = ms.iter().map(|&(p, m)| (lat.plaq_word(p), m)).collect();
    let mut den_all = Q::one();
    for (w, m) in &words {
        let mut dw = 1i128;
        for &l in w {
            let v = l >> 1;
            if slot.contains_key(&v) {
                dw *= 2;
            } else if let Some((_, dn)) = vals.get(&v) {
                dw *= dn;
            }
        }
        for _ in 0..*m {
            den_all = den_all.mul(&Q::int(dw));
        }
    }
    let mut total: i128 = 0;
    let mut idx = vec![0usize; k];
    loop {
        let mut prod: i128 = 1;
        for (w, m) in &words {
            let mut q = [1i128, 0, 0, 0];
            for &l in w {
                let v = l >> 1;
                let mut e = if let Some(&t) = slot.get(&v) {
                    elems[idx[t]]
                } else if let Some((num, _)) = vals.get(&v) {
                    *num
                } else {
                    [1, 0, 0, 0]
                };
                if l & 1 == 1 {
                    e = [e[0], -e[1], -e[2], -e[3]];
                }
                q = iq_mul(&q, &e);
            }
            for _ in 0..*m {
                prod *= q[0];
            }
        }
        total += prod;
        let mut t = 0;
        while t < k {
            idx[t] += 1;
            if idx[t] < elems.len() {
                break;
            }
            idx[t] = 0;
            t += 1;
        }
        if t == k {
            break;
        }
    }
    let mut n = Q::one();
    for _ in 0..k {
        n = n.mul(&Q::int(elems.len() as i128));
    }
    Q::int(total).div(&n).div(&den_all)
}

// ---------------------------------------------------------------- the 2I route on the filling family

fn section_filling_2i(out: &mut Out, ig: &mut Integrator, lat: &Lat, g2i: &[Qp]) {
    out.note("filling by 2I");
    // the filling of the coarse plaquette at 0 in plane (0,1), spins all 1/2 and all 1
    let mut plaqs: Vec<u32> = Vec::new();
    for s in 0..2 {
        for r in 0..2 {
            let c = [2 * s + 1, 2 * r + 1, 0, 0];
            plaqs.push(lat.cell_plaq[lat.cell(c)]);
        }
    }
    plaqs.sort();
    let mut rng = Lcg(4242);
    let mut rows: Vec<String> = Vec::new();
    for spin in [1usize, 2] {
        let spins = vec![spin; 4];
        let phi = polymer_phi(lat, ig, &plaqs, &spins);
        // gauge at the center: fix the internal link toward -e_0... the first internal link
        let center = lat.cell([2, 2, 0, 0]);
        let mut internal: Vec<u32> = Vec::new();
        for k in 0..2 {
            for s in [-1, 1] {
                let c = lat.shift(lat.coords(center), k, s);
                internal.push(lat.link_of_cell(c) as u32);
            }
        }
        let maxdeg = 2 * spin;
        assert!(maxdeg <= 11);
        for _trial in 0..2 {
            let mut val: HashMap<u32, Qp, FxB> = HashMap::default();
            for v in vsupport(&phi) {
                val.insert(VOFF + v as u32, g2i[rng.next(120) as usize]);
            }
            let symv = eval_poly_qp(&phi, &val);
            let one = Qp {
                c: [Zp(2, 0), Zp(0, 0), Zp(0, 0), Zp(0, 0)],
                e: 1,
            };
            val.insert(internal[0], one);
            // every letter carries denominator 2, so a word of L letters has trace c0 / 2^(L-1):
            // chi_1/2 = c0 / 2^(L-1), chi_1 = (c0^2 - 4^(L-1)) / 4^(L-1); numerators summed in Z[phi]
            let words: Vec<Word> = plaqs.iter().map(|&p| lat.plaq_word(p as usize)).collect();
            let mut den_exp = 0u32;
            for w in &words {
                let l = w.len() as u32;
                den_exp += if spin == 1 { l - 1 } else { 2 * (l - 1) };
            }
            let mut acc = Zp(0, 0);
            for a in g2i {
                for b in g2i {
                    for c in g2i {
                        val.insert(internal[1], *a);
                        val.insert(internal[2], *b);
                        val.insert(internal[3], *c);
                        let mut prod = Zp(1, 0);
                        for w in &words {
                            let mut q = Qp {
                                c: [Zp(1, 0), Zp(0, 0), Zp(0, 0), Zp(0, 0)],
                                e: 0,
                            };
                            for &l in w {
                                let v = val.get(&(l >> 1)).expect("value");
                                q = qp_mul(&q, &if l & 1 == 1 { qp_conj(v) } else { *v });
                            }
                            let c0 = q.c[0];
                            let chi = if spin == 1 {
                                c0
                            } else {
                                c0.mul(c0).sub(Zp(1i128 << (2 * (w.len() as u32 - 1)), 0))
                            };
                            prod = prod.mul(chi);
                        }
                        acc = acc.add(prod);
                    }
                }
            }
            let n3 = Q::int(120 * 120 * 120).mul(&Q::int(1i128 << den_exp));
            let lit = Qf(Q::int(acc.0).div(&n3), Q::int(acc.1).div(&n3));
            out.check("G1_filling_2I_equals_SU2", lit == symv, &spin.to_string());
            rows.push(
                "spin=".to_string()
                    + if spin == 1 { "1/2" } else { "1" }
                    + ":link_degree="
                    + &maxdeg.to_string()
                    + ":value="
                    + &qf_show(&symv),
            );
        }
    }
    out.row("YM4_03C_FILLING_BY_2I|free_internal_links=3_after_the_gauge_at_the_center|averages=120^3_per_value|".to_string() + &rows.join(",") + "|equal_to_the_exact_integral=" + &rows.len().to_string() + "|tag=MEASURED");
}

// ---------------------------------------------------------------- reading the table

fn get_coef(res: &DimResult, tag: &str) -> Vec<Ser> {
    res.table
        .logc
        .iter()
        .filter(|(k, _)| k.0 == tag)
        .map(|(_, s)| s.clone())
        .collect()
}

fn one_coef(res: &DimResult, tag: &str) -> Ser {
    let v = get_coef(res, tag);
    let mut s = Ser::zero();
    for x in v {
        s = s.add(&x);
    }
    s
}

fn shape_count(res: &DimResult, tag: &str) -> usize {
    res.table
        .logc
        .iter()
        .filter(|(k, s)| k.0 == tag && s.0.iter().any(|q| !q.is_zero()))
        .count()
}

fn s_eff(c: &Q) -> Q {
    c.neg()
}

fn report_dimension(out: &mut Out, res: &DimResult, label: &str, top: usize, read_parseval: bool) {
    // the coefficient table: S_n = - [beta^n] log rho, for every shape with a nonzero entry
    for ((tag, key), s) in &res.table.logc {
        if s.0.iter().take(top + 1).all(|q| q.is_zero()) {
            continue;
        }
        let info = &res.shapes[&(tag.clone(), key.clone())];
        let per_site = Q::frac(info.per_site_num, info.per_site_den);
        let terms: Vec<String> = (0..=top)
            .filter(|&k| !s.0[k].is_zero())
            .map(|k| "b".to_string() + &k.to_string() + ":" + &s.0[k].show())
            .collect();
        let sterm: Vec<String> = (0..=top)
            .filter(|&k| !s.0[k].is_zero())
            .map(|k| "S_".to_string() + &k.to_string() + ":" + &s_eff(&s.0[k]).show())
            .collect();
        out.row(
            "YM4_03C_TABLE|".to_string()
                + label
                + "|functional="
                + &info.name
                + "|placements_per_coarse_site="
                + &per_site.show()
                + "|log_rho="
                + &terms.join(",")
                + "|S_eff="
                + &sterm.join(",")
                + "|tag=MEASURED",
        );
    }
    let resid: Vec<String> = (0..=top).map(|k| res.table.residual.0[k].show()).collect();
    out.row("YM4_03C_PARSEVAL|".to_string() + label + "|residual_by_order_b0..b" + &top.to_string() + "=" + &resid.join(",") + "|reading=0_means_every_class's_function_lies_in_the_span_of_the_named_functionals|tag=MEASURED");
    let zero = res
        .table
        .residual
        .0
        .iter()
        .take(top + 1)
        .all(|q| q.is_zero());
    if !read_parseval {
        return;
    }
    out.read(
        "P13",
        &(label.to_string() + "_parseval_residual_through_b" + &top.to_string()),
        if zero { "0" } else { "nonzero" },
        "0",
        false,
    );
}

fn sum_tag(res: &DimResult, tag: &str, which: &str) -> Ser {
    let m = match which {
        "single" => &res.table.single,
        "cluster" => &res.table.cluster,
        _ => &res.table.logc,
    };
    let mut s = Ser::zero();
    for (k, v) in m {
        if k.0 == tag {
            s = s.add(v);
        }
    }
    s
}

fn read_rows(out: &mut Out, res: &DimResult, d: usize, top: usize) {
    let lab = if d == 4 { "d4" } else { "d3" };
    let half = one_coef(res, "plaq_half");
    let onec = one_coef(res, "plaq_one");
    let chair = one_coef(res, "chair");
    let rect = one_coef(res, "rect");
    out.check(
        &("one_plaquette_shape_".to_string() + lab),
        get_coef(res, "plaq_half").len() <= 1,
        "",
    );
    // P2 and P3
    for k in 1..4 {
        let any = res.table.logc.values().any(|s| !s.0[k].is_zero());
        out.read(
            "P2",
            &(lab.to_string() + "_any_V-dependent_coefficient_b" + &k.to_string()),
            if any { "nonzero" } else { "0" },
            "0",
            true,
        );
    }
    let odd_any: Vec<String> = (1..=top)
        .filter(|k| k % 2 == 1)
        .filter(|&k| res.table.logc.values().any(|s| !s.0[k].is_zero()))
        .map(|k| k.to_string())
        .collect();
    out.read(
        "P3",
        &(lab.to_string() + "_odd_orders_b1..b9"),
        if odd_any.is_empty() { "0" } else { "nonzero" },
        "0",
        true,
    );
    // P1 statement 2, P4, P5
    let others_at = |k: usize, allowed: &[&str]| -> String {
        let v: Vec<String> = res
            .table
            .logc
            .iter()
            .filter(|(key, s)| !s.0[k].is_zero() && !allowed.contains(&key.0.as_str()))
            .map(|(key, _)| key.0.clone())
            .collect();
        if v.is_empty() {
            "none".to_string()
        } else {
            v.join(",")
        }
    };
    out.read(
        "P1",
        &(lab.to_string() + "_b4_chi_1/2(V_P)_log_rho"),
        &half.0[4].show(),
        "1/128",
        true,
    );
    out.read(
        "P1",
        &(lab.to_string() + "_S_4_chi_1/2(V_P)"),
        &s_eff(&half.0[4]).show(),
        "-1/128",
        true,
    );
    out.read(
        "P1",
        &(lab.to_string() + "_b4_other_functionals"),
        &others_at(4, &["plaq_half"]),
        "none",
        true,
    );
    out.read(
        "P4",
        &(lab.to_string() + "_b6_chi_1/2(V_P)_log_rho"),
        &half.0[6].show(),
        "-1/768",
        true,
    );
    out.read(
        "P4",
        &(lab.to_string() + "_b6_other_functionals"),
        &others_at(6, &["plaq_half"]),
        "none",
        true,
    );
    let p5 = if d == 4 { "1/1536" } else { "5/12288" };
    out.read(
        "P5",
        &(lab.to_string() + "_b8_chi_1/2(V_P)_log_rho"),
        &half.0[8].show(),
        p5,
        true,
    );
    out.read(
        "P5",
        &(lab.to_string() + "_b8_chi_1(V_P)_log_rho"),
        &onec.0[8].show(),
        "-19/884736",
        true,
    );
    out.read(
        "P5",
        &(lab.to_string() + "_b8_other_functionals"),
        &others_at(8, &["plaq_half", "plaq_one"]),
        "none",
        true,
    );
    // P6 the chair, P7 the rectangle
    let below: Vec<String> = (0..10)
        .filter(|&k| !chair.0[k].is_zero())
        .map(|k| "b".to_string() + &k.to_string() + ":" + &chair.0[k].show())
        .collect();
    out.read(
        "P6",
        &(lab.to_string() + "_chair_below_b10"),
        &(if below.is_empty() {
            "0".to_string()
        } else {
            below.join(",")
        }),
        "0",
        false,
    );
    out.read(
        "P6",
        &(lab.to_string() + "_b10_chi_1/2(V_chair)_log_rho"),
        &chair.0[10].show(),
        "3/524288",
        false,
    );
    out.read(
        "P6",
        &(lab.to_string() + "_S_10_chair"),
        &s_eff(&chair.0[10]).show(),
        "-3/524288",
        false,
    );
    let rect_any = (0..=10).any(|k| !rect.0[k].is_zero());
    out.read(
        "P7",
        &(lab.to_string() + "_rectangle_through_b10"),
        if rect_any { "nonzero" } else { "0" },
        "0",
        true,
    );
    // P11, P12
    let p11 = if d == 4 {
        "-467/2211840"
    } else {
        "-1013/8847360"
    };
    out.read(
        "P11",
        &(lab.to_string() + "_b10_chi_1/2(V_P)_log_rho"),
        &half.0[10].show(),
        p11,
        false,
    );
    out.read(
        "P12",
        &(lab.to_string() + "_b10_chi_1(V_P)_log_rho"),
        &onec.0[10].show(),
        "7/884736",
        false,
    );
    // P13: the functionals with a nonzero coefficient through beta^10
    let mut nonzero: BTreeSet<String> = BTreeSet::new();
    for (key, s) in &res.table.logc {
        if s.0.iter().take(11).any(|q| !q.is_zero()) {
            nonzero.insert(key.0.clone());
        }
    }
    let nz: Vec<String> = nonzero.iter().cloned().collect();
    for tag in [
        "n1",
        "rect",
        "pair",
        "twisted_hex",
        "plaq_threehalf",
        "tube_half",
        "tube_one",
    ] {
        let s = one_coef(res, tag);
        let any = s.0.iter().take(11).any(|q| !q.is_zero());
        let offered = res.offered.get(tag).copied().unwrap_or(0);
        out.read(
            "P13",
            &(lab.to_string()
                + "_"
                + tag
                + "_through_b10_offered_to_"
                + &offered.to_string()
                + "_readouts"),
            if any { "nonzero" } else { "0" },
            "0",
            false,
        );
    }
    out.read(
        "P13",
        &(lab.to_string() + "_nonzero_functionals_through_b10"),
        &nz.join(","),
        "chair,plaq_half,plaq_one",
        false,
    );
    out.row(
        "YM4_03C_SHAPES|".to_string()
            + lab
            + "|plaq_half_shapes="
            + &shape_count(res, "plaq_half").to_string()
            + "|chair_shapes="
            + &shape_count(res, "chair").to_string()
            + "|tag=MEASURED",
    );
    // G2: the two series and the cancellations
    let one_single = sum_tag(res, "plaq_one", "single");
    let one_cluster = sum_tag(res, "plaq_one", "cluster");
    let half_single = sum_tag(res, "plaq_half", "single");
    let half_cluster = sum_tag(res, "plaq_half", "cluster");
    let pair_log = sum_tag(res, "pair", "log");
    let pair_from_family = half_single.0[4].mul(&half_single.0[4]);
    out.row(
        "YM4_03C_G2|".to_string()
            + lab
            + "|rho_over_int_rho_b8_chi_1(V_P)="
            + &one_single.0[8].show()
            + "|rho_over_int_rho_b8_disjoint_pair=(b4_of_chi_1/2)^2="
            + &pair_from_family.show()
            + "|log_rho_b8_chi_1(V_P)="
            + &onec.0[8].show()
            + "|log_rho_b8_disjoint_pair="
            + &pair_log.0[8].show()
            + "|cancellation_on_chi_1=the_self-cluster_-1/2z_F^2="
            + &one_cluster.0[8].show()
            + "|cancellation_on_the_pair=the_compatible_family_z_Pz_Q_against_-1/2(2z_Pz_Q)_of_the_log=-"
            + &pair_from_family.show()
            + "|chi_1/2_b10_single="
            + &half_single.0[10].show()
            + "|chi_1/2_b10_clusters="
            + &half_cluster.0[10].show()
            + "|tag=MEASURED",
    );
    out.read(
        "G2",
        &(lab.to_string() + "_rho_b8_chi_1(V_P)"),
        &one_single.0[8].show(),
        "1/110592",
        true,
    );
    out.read(
        "G2",
        &(lab.to_string() + "_rho_b8_disjoint_pair"),
        &pair_from_family.show(),
        "1/16384",
        true,
    );
    out.read(
        "G2",
        &(lab.to_string() + "_log_rho_b8_disjoint_pair"),
        &pair_log.0[8].show(),
        "0",
        true,
    );
    out.read(
        "G2",
        &(lab.to_string() + "_self_cluster_b8_chi_1"),
        &one_cluster.0[8].show(),
        "-1/32768",
        true,
    );
}

// ---------------------------------------------------------------- main

fn binom_big(n: u64, k: u64) -> Big {
    let mut num = Big::from_u128(1);
    let mut den = Big::from_u128(1);
    for i in 0..k {
        num = num.mul(&Big::from_u128((n - i) as u128));
        den = den.mul(&Big::from_u128((i + 1) as u128));
    }
    num.divrem(&den).0
}

fn main() {
    let mut out = Out {
        rows: Vec::new(),
        failed: Vec::new(),
        misses: Vec::new(),
        t0: Instant::now(),
    };
    let sab = sabotage();
    let top: usize = std::env::var("YM4_03C_TOP")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(10);
    out.row(
        "YM4_03C_ENGINE|stage=2|seat=ACER-CLAUDE-FABLE5|lane=second_seat_engine_lane|prediction=docs/PREDICTION-YM4-03C.hbp|pin=ddd7b779d60e04f2dca1f866ff56f1194107dd10a8470088dee4f0ab3336b881|top=beta^".to_string()
            + &top.to_string()
            + "|arithmetic=integer_and_exact_rational,float_used=0|sabotage="
            + if sab.is_empty() { "none" } else { &sab },
    );
    if let Some(n) = std::env::var("YM4_03C_COST_PROBE")
        .ok()
        .and_then(|s| s.parse::<usize>().ok())
    {
        // the cost measurement: the d = 4 support search alone at max size n
        let lat = Lat::new(4, [6, 6, 6, 6], 1);
        let (p0, _) = lat.coarse_link_positions(lat.ccell([1, 0, 0, 0]));
        let t = Instant::now();
        let mut srch = Search::new(&lat, false, n);
        for &sd in &lat.link_plaqs[p0].clone() {
            srch.run_from(sd);
        }
        let (cl, distinct) = classes_from(&lat, &srch.closed);
        eprintln!(
            "COST_PROBE|max_size={}|states={}|closed={}|distinct={}|classes={}|ms={}",
            n,
            srch.states,
            srch.closed.len(),
            distinct,
            cl.len(),
            t.elapsed().as_millis()
        );
        return;
    }
    let mut ig = Integrator::new();
    let g2i = group_2i();
    let g2t = group_2t();
    section_designs(&mut out, &mut ig, &g2i, &g2t);
    section_integrator_checks(&mut out, &mut ig, &g2i);
    section_readout_controls(&mut out, &mut ig);
    let wts = spin_weights();
    let t2: Vec<String> = (0..=9)
        .filter(|&k| !wts[1].0[k].is_zero())
        .map(|k| "b".to_string() + &k.to_string() + ":" + &wts[1].0[k].mul(&Q::frac(1, 2)).show())
        .collect();
    out.row(
        "YM4_03C_T_SERIES|t_2=".to_string()
            + &t2.join(",")
            + "|route=McKay_powers,the_per-plaquette_multinomial_1/m!_folded|tag=MEASURED",
    );
    section_mckay_fold(&mut out, &mut ig);
    // ---- d = 4 on fine 6^4: the Z2 control, then SU(2)
    let lat4 = Lat::new(4, [6, 6, 6, 6], 1);
    out.row(
        "YM4_03C_LATTICE|d=4|fine=6x6x6x6|coarse=3x3x3x3|plaquettes=".to_string()
            + &lat4.nplaq().to_string()
            + "|links="
            + &lat4.link_cell.len().to_string()
            + "|point_group="
            + &lat4.pg.len().to_string()
            + "|multisets_of_10_replaced=C(7785,10)="
            + &binom_big(7785, 10).dec()
            + "|tag=MEASURED",
    );
    let res4 = run_dimension(&mut out, &mut ig, &lat4, "d4", top, &wts, true);
    report_dimension(&mut out, &res4, "d4", top, true);
    if top >= 10 {
        read_rows(&mut out, &res4, 4, top);
    }
    section_filling_2i(&mut out, &mut ig, &lat4, &g2i);
    // ---- d = 3 on fine 6^3
    let lat3 = Lat::new(3, [6, 6, 6, 1], 1);
    out.row(
        "YM4_03C_LATTICE|d=3|fine=6x6x6|coarse=3x3x3|plaquettes=".to_string()
            + &lat3.nplaq().to_string()
            + "|point_group="
            + &lat3.pg.len().to_string()
            + "|tag=MEASURED",
    );
    let res3 = run_dimension(&mut out, &mut ig, &lat3, "d3", top, &wts, true);
    report_dimension(&mut out, &res3, "d3", top, true);
    if top >= 10 {
        read_rows(&mut out, &res3, 3, top);
    }
    // ---- P10b: tubes on fine 2x6x6x6
    let lat_t = Lat::new(4, [2, 6, 6, 6], 1);
    let res_t = run_dimension(
        &mut out,
        &mut ig,
        &lat_t,
        "tube_2x6x6x6",
        top.min(8),
        &wts,
        false,
    );
    let tube = one_coef(&res_t, "tube_one");
    let tube_rows: Vec<String> = (0..=8).map(|k| tube.0[k].show()).collect();
    out.row(
        "YM4_03C_TUBE|fine=2x6x6x6|coarse=1x3x3x3|chi_1(V_l)_l_in_direction_0_b0..b8=".to_string()
            + &tube_rows.join(",")
            + "|readout=<chi_1(V_l),f>/<chi_1(V_l),chi_1(V_l)>,the_spin-1_component_on_l_with_spin_0_on_every_other_coarse_link"
            + "|basis=on_coarse_side_1_a_plaquette_of_a_plane_(0,nu)_holds_its_nu_link_twice,so_its_character_is_not_one_basis_element"
            + "_and_this_lattice's_table_and_Parseval_reading_stay_out;P10b_reads_the_tube_projection_alone|tag=MEASURED",
    );
    let below = (0..8).any(|k| !tube.0[k].is_zero());
    out.read(
        "P10b",
        "b8_chi_1(V_l)_tube",
        &tube.0[8].show(),
        "3/16384",
        false,
    );
    out.read(
        "P10b",
        "below_b8",
        if below { "nonzero" } else { "0" },
        "0",
        false,
    );
    // ---- P10a: nothing winds at coarse side 3
    for (res, lab) in [(&res4, "d4"), (&res3, "d3")] {
        let fits = res.max_extent < 6;
        out.read(
            "P10a",
            &(lab.to_string()
                + "_every_V-dependent_support_through_b10_spans_fewer_than_6_fine_sites"),
            if fits { "fit" } else { "wraps" },
            "fit",
            true,
        );
    }
    out.row("YM4_03C_P10A_RANGE|beta^11=odd,so_0_by_P3's_staggered_sign,DERIVED|the_engine's_range=beta^0..beta^10|the_strip_of_12_at_L=3=beta^12,outside_the_range|tag=DERIVED".to_string());
    // ---- P1 statement 1: the order-4 benchmark on the YM4-03 lattices
    section_p1(&mut out, &mut ig, &g2t);
    // ---- degrees and the account
    out.row("YM4_03C_LINK_DEGREES|every_exact_SU(2)_integration_step_by_degree=".to_string() + &ig.deg.show() + "|steps=" + &ig.deg.steps.to_string() + "|max_degree=" + &ig.deg.max().to_string() + "|2I_uses=degree<=11_each,written_in_YM4_03C_INTEGRATOR_VS_2I_and_YM4_03C_FILLING_BY_2I|tag=MEASURED");
    let st4: Vec<String> = res4
        .stats
        .iter()
        .filter(|s| !s.contains("_ms="))
        .cloned()
        .collect();
    let st3: Vec<String> = res3
        .stats
        .iter()
        .filter(|s| !s.contains("_ms="))
        .cloned()
        .collect();
    out.row("YM4_03C_AVOIDED|d4=".to_string() + &st4.join(",") + "|d3=" + &st3.join(",") + "|in_place_of=C(7785,10)_multisets_on_fine_6^4,120^k_products_over_k_free_links,a_log_of_the_whole_partition_function|tag=MEASURED");
    let misses = if out.misses.is_empty() {
        "none".to_string()
    } else {
        out.misses.join(",")
    };
    out.row(
        "YM4_03C_DONE|rows=".to_string() + &(out.rows.len() + 1).to_string() + "|misses=" + &misses,
    );
    for s in res4
        .stats
        .iter()
        .chain(res3.stats.iter())
        .chain(res_t.stats.iter())
    {
        out.note(s);
    }
    for p in &res4.table.parts {
        out.note(&("part|d4|".to_string() + p));
    }
}
