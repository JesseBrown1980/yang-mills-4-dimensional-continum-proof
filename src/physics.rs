//! Finite four-dimensional continuous SU(2) control with rational quaternions.
//! This is not a continuum-limit computation or a physical mass-gap certificate.
#![allow(clippy::many_single_char_names)]

use std::array;

pub const SITE_COUNT: usize = 16;
pub const LINK_COUNT: usize = 64;
pub const PLAQUETTE_COUNT: usize = 96;
pub const SHARD_COUNT: usize = 4;

pub fn require(ok: bool, message: &str) -> Result<(), String> {
    if ok {
        Ok(())
    } else {
        Err(message.to_owned())
    }
}

fn gcd(mut x: i128, mut y: i128) -> i128 {
    x = x.abs();
    y = y.abs();
    while y != 0 {
        (x, y) = (y, x % y);
    }
    x.max(1)
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Fraction {
    pub n: i128,
    pub d: i128,
}

impl Fraction {
    pub fn new(n: i128, d: i128) -> Self {
        assert!(d > 0, "nonpositive fraction denominator");
        if n == 0 {
            return Self { n: 0, d: 1 };
        }
        let f = gcd(n, d);
        Self { n: n / f, d: d / f }
    }

    pub fn zero() -> Self {
        Self::new(0, 1)
    }

    pub fn plus(self, rhs: Self) -> Self {
        let n1 = self
            .n
            .checked_mul(rhs.d)
            .expect("fraction multiply overflow");
        let n2 = rhs
            .n
            .checked_mul(self.d)
            .expect("fraction multiply overflow");
        let n = n1.checked_add(n2).expect("fraction add overflow");
        let d = self
            .d
            .checked_mul(rhs.d)
            .expect("fraction denominator overflow");
        Self::new(n, d)
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Quat {
    n: [i128; 4],
    d: i128,
}

impl Quat {
    pub fn new(n: [i128; 4], d: i128) -> Self {
        assert!(d > 0, "nonpositive quaternion denominator");
        let mut factor = d;
        for c in n {
            factor = gcd(factor, c);
        }
        let n = n.map(|c| c / factor);
        let q = Self { n, d: d / factor };
        assert!(q.is_unit(), "nonunit quaternion");
        q
    }

    pub fn identity() -> Self {
        Self {
            n: [1, 0, 0, 0],
            d: 1,
        }
    }

    pub fn axis(axis: usize, trit: i8) -> Self {
        assert!(axis < 3 && (-1..=1).contains(&trit), "invalid generator");
        if trit == 0 {
            return Self::identity();
        }
        let mut n = [3, 0, 0, 0];
        n[axis + 1] = 4 * i128::from(trit);
        Self::new(n, 5)
    }

    pub fn is_unit(self) -> bool {
        let n2: i128 = self
            .n
            .iter()
            .map(|x| x.checked_mul(*x).expect("norm overflow"))
            .sum();
        n2 == self
            .d
            .checked_mul(self.d)
            .expect("norm denominator overflow")
    }

    pub fn inverse(self) -> Self {
        Self {
            n: [self.n[0], -self.n[1], -self.n[2], -self.n[3]],
            d: self.d,
        }
    }

    pub fn mul(self, rhs: Self) -> Self {
        let [a, b, c, d] = self.n;
        let [e, f, g, h] = rhs.n;
        let x = [
            a * e - b * f - c * g - d * h,
            a * f + b * e + c * h - d * g,
            a * g - b * h + c * e + d * f,
            a * h + b * g - c * f + d * e,
        ];
        Self::new(
            x,
            self.d
                .checked_mul(rhs.d)
                .expect("quaternion denominator overflow"),
        )
    }

    pub fn scalar(self) -> Fraction {
        Fraction::new(self.n[0], self.d)
    }
}

pub struct Rng {
    x: u64,
}
impl Rng {
    fn new(seed: u64) -> Self {
        Self {
            x: if seed == 0 { 1 } else { seed },
        }
    }

    fn next(&mut self) -> u64 {
        let mut x = self.x;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.x = x;
        x
    }

    fn trit(&mut self) -> i8 {
        (self.next() % 3) as i8 - 1
    }
}

pub fn seed_for_shard(shard: usize) -> u64 {
    assert!(shard < SHARD_COUNT, "invalid shard");
    20_261_103 + 104_729 * (shard as u64 + 1)
}

pub fn candidate(shard: usize) -> [i8; LINK_COUNT] {
    let mut rng = Rng::new(seed_for_shard(shard));
    array::from_fn(|_| rng.trit())
}

pub fn trit_word(trits: &[i8; LINK_COUNT]) -> String {
    trits
        .iter()
        .map(|t| match t {
            -1 => '-',
            0 => '0',
            1 => '+',
            _ => panic!("invalid trit"),
        })
        .collect()
}

fn next_site(site: usize, direction: usize) -> usize {
    assert!(site < SITE_COUNT && direction < 4);
    site ^ (1 << direction)
}

fn link_index(site: usize, direction: usize) -> usize {
    site * 4 + direction
}

fn plaquette(links: &[Quat; LINK_COUNT], site: usize, mu: usize, nu: usize) -> Quat {
    links[link_index(site, mu)]
        .mul(links[link_index(next_site(site, mu), nu)])
        .mul(links[link_index(next_site(site, nu), mu)].inverse())
        .mul(links[link_index(site, nu)].inverse())
}

fn action(links: &[Quat; LINK_COUNT]) -> (Fraction, usize) {
    let mut result = Fraction::zero();
    let mut seen = 0;
    for x in 0..SITE_COUNT {
        for mu in 0..4 {
            for nu in mu + 1..4 {
                let p = plaquette(links, x, mu, nu);
                result = result.plus(Fraction::new(p.d - p.n[0], p.d));
                seen += 1;
            }
        }
    }
    (result, seen)
}

fn gauge_field(shard: usize) -> [Quat; SITE_COUNT] {
    let mut rng = Rng::new(seed_for_shard(shard) ^ 0xa5b3_9f71_a5b3_9f71);
    array::from_fn(|x| Quat::axis(x % 3, rng.trit()))
}

fn gauge_transform(
    links: &[Quat; LINK_COUNT],
    gauge: &[Quat; SITE_COUNT],
    broken_endpoint: bool,
) -> [Quat; LINK_COUNT] {
    array::from_fn(|link| {
        let x = link / 4;
        let mu = link % 4;
        let at_end = gauge[next_site(x, mu)];
        gauge[x].mul(links[link]).mul(if broken_endpoint {
            at_end
        } else {
            at_end.inverse()
        })
    })
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Evaluation {
    pub action: Fraction,
    pub checked_plaquettes: usize,
    pub fault_controls: usize,
}

pub fn evaluate(shard: usize, trits: &[i8; LINK_COUNT]) -> Result<Evaluation, String> {
    require(shard < SHARD_COUNT, "invalid shard index")?;
    require(trits.iter().all(|t| (-1..=1).contains(t)), "invalid trit")?;
    require(
        Quat::axis(0, 1).mul(Quat::axis(1, 1)) != Quat::axis(1, 1).mul(Quat::axis(0, 1)),
        "noncommutativity control failed",
    )?;
    let links: [Quat; LINK_COUNT] = array::from_fn(|i| Quat::axis((i % 4) % 3, trits[i]));
    let gauge = gauge_field(shard);
    let transformed = gauge_transform(&links, &gauge, false);
    let (reference, count) = action(&links);
    let (altered, transformed_count) = action(&transformed);
    require(
        count == PLAQUETTE_COUNT && transformed_count == count,
        "wrong plaquette count",
    )?;
    require(
        altered == reference,
        "Wilson action changed under gauge transform",
    )?;
    let mut checked = 0;
    for (site, at_site) in gauge.iter().enumerate() {
        for mu in 0..4 {
            for nu in mu + 1..4 {
                let p = plaquette(&links, site, mu, nu);
                let pt = plaquette(&transformed, site, mu, nu);
                let expected = at_site.mul(p).mul(at_site.inverse());
                require(pt == expected, "SU2 plaquette conjugation failed")?;
                require(p.scalar() == pt.scalar(), "Wilson trace invariance failed")?;
                checked += 1;
            }
        }
    }
    require(
        checked == PLAQUETTE_COUNT,
        "not all four-dimensional plaquettes checked",
    )?;
    let (broken_action, broken_count) = action(&gauge_transform(&links, &gauge, true));
    require(
        broken_count == PLAQUETTE_COUNT,
        "broken control did not cover all plaquettes",
    )?;
    require(
        broken_action != reference,
        "wrong-endpoint negative control undetected",
    )?;
    let artificially_shifted = reference.plus(Fraction::new(1, 1_000_000));
    require(
        artificially_shifted != altered,
        "trace-corruption negative control undetected",
    )?;
    Ok(Evaluation {
        action: reference,
        checked_plaquettes: checked,
        fault_controls: 2,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn quaternion_group_and_inverse() {
        for axis in 0..3 {
            for sign in [-1, 0, 1] {
                let q = Quat::axis(axis, sign);
                assert!(q.is_unit());
                assert_eq!(q.mul(q.inverse()), Quat::identity());
            }
        }
        assert_ne!(
            Quat::axis(0, 1).mul(Quat::axis(1, 1)),
            Quat::axis(1, 1).mul(Quat::axis(0, 1))
        );
    }

    #[test]
    fn four_shards_exact_gauge_test() {
        for id in 0..SHARD_COUNT {
            let c = candidate(id);
            let e = evaluate(id, &c).expect("finite 4D gauge test failed");
            assert_eq!(e.checked_plaquettes, 96);
            assert_eq!(e.fault_controls, 2);
            assert!(e.action.n > 0);
        }
    }

    #[test]
    fn trits_have_fixed_length() {
        for id in 0..SHARD_COUNT {
            assert_eq!(trit_word(&candidate(id)).len(), LINK_COUNT);
        }
    }
}
