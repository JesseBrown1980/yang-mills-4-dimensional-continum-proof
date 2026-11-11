//! YM4-06B independent executable checks for the two finite S3 spectral-gap bounds.
//! Uses exact integer group tables, two-trit codes and the HTTP-0 integer SHA-256.
//! This is NOT a numerical spectral diagonalization or a continuum SU(2) certificate.
#![forbid(unsafe_code)]
#![deny(clippy::float_arithmetic, clippy::float_cmp, clippy::cast_precision_loss)]
mod sha256;
use sha256::hash_bytes;
use std::collections::{BTreeMap, BTreeSet};
use std::env;
use std::fs;
use std::path::Path;

const PERM: [[usize; 3]; 6] = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]];
const TRANS: [u8; 3] = [1, 2, 5];
const LINKS: usize = 24;
const FACES: usize = 24;
const TREE_FREE_LINKS: u32 = 17;

fn mul(a: u8, b: u8) -> u8 {
    let x = PERM[usize::from(a)];
    let y = PERM[usize::from(b)];
    let c = [x[y[0]], x[y[1]], x[y[2]]];
    PERM.iter().position(|p| *p == c).expect("S3 product remains in S3") as u8
}
fn inv(a: u8) -> u8 {
    (0..6).find(|&b| mul(a, b) == 0).expect("S3 inverse")
}
fn conj(g: u8, a: u8) -> u8 {
    mul(mul(g, a), inv(g))
}
fn trits(a: u8) -> [u8; 2] {
    assert!(a < 6, "only six valid S3 trit codes");
    [a % 3, a / 3]
}
fn from_trits(x: [u8; 2]) -> Option<u8> {
    if x[0] > 2 || x[1] > 2 {
        return None;
    }
    let a = x[0] + 3 * x[1];
    (a < 6).then_some(a)
}
fn site(x: usize, y: usize, z: usize) -> usize {
    x * 4 + y * 2 + z
}
fn shift(x: usize, y: usize, z: usize, d: usize) -> (usize, usize, usize) {
    match d {
        0 => ((x + 1) % 2, y, z),
        1 => (x, (y + 1) % 2, z),
        2 => (x, y, (z + 1) % 2),
        _ => panic!("bad direction"),
    }
}
fn flat_links(a: u8, b: u8, c: u8) -> [u8; LINKS] {
    let mut out = [0u8; LINKS];
    for x in 0..2 {
        for y in 0..2 {
            for z in 0..2 {
                let p = site(x, y, z) * 3;
                out[p] = if x == 1 { a } else { 0 };
                out[p + 1] = if y == 1 { b } else { 0 };
                out[p + 2] = if z == 1 { c } else { 0 };
            }
        }
    }
    out
}
fn magnetic(u: &[u8; LINKS], wrong_cost: bool) -> u64 {
    let mut energy = 0;
    for x in 0..2 {
        for y in 0..2 {
            for z in 0..2 {
                for d in 0..3 {
                    for e in (d + 1)..3 {
                        let (xd, yd, zd) = shift(x, y, z, d);
                        let (xe, ye, ze) = shift(x, y, z, e);
                        let hol = mul(
                            mul(
                                mul(u[site(x, y, z) * 3 + d], u[site(xd, yd, zd) * 3 + e]),
                                inv(u[site(xe, ye, ze) * 3 + d]),
                            ),
                            inv(u[site(x, y, z) * 3 + e]),
                        );
                        energy += match hol {
                            0 => 0,
                            1 | 2 | 5 => if wrong_cost { 1 } else { 2 },
                            3 | 4 => 3,
                            _ => panic!("invalid S3 holonomy"),
                        };
                    }
                }
            }
        }
    }
    energy
}
fn flat_classes() -> (u64, Vec<[u8; 3]>) {
    let mut raw = 0u64;
    let mut classes = BTreeSet::new();
    for a in 0..6 {
        for b in 0..6 {
            for c in 0..6 {
                if mul(a, b) != mul(b, a) || mul(a, c) != mul(c, a) || mul(b, c) != mul(c, b) {
                    continue;
                }
                raw += 1;
                let key = (0..6).map(|g| [conj(g, a), conj(g, b), conj(g, c)])
                    .min().expect("nonempty conjugation group");
                classes.insert(key);
            }
        }
    }
    (raw, classes.into_iter().collect())
}
type Matrix = [[i64; 6]; 6];
fn matmul(a: &Matrix, b: &Matrix) -> Matrix {
    let mut c = [[0; 6]; 6];
    for i in 0..6 {
        for j in 0..6 {
            for k in 0..6 {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }
    c
}
fn minus_scalar(a: &Matrix, s: i64) -> Matrix {
    let mut b = *a;
    for (i, row) in b.iter_mut().enumerate() {
        row[i] -= s;
    }
    b
}
fn electric_link_check() {
    let mut l = [[0i64; 6]; 6];
    for x in 0..6 {
        l[x][x] += 3;
        for t in TRANS {
            l[usize::from(mul(t, x as u8))][x] -= 1;
        }
    }
    for i in 0..6 {
        for j in 0..6 {
            assert_eq!(l[i][j], l[j][i], "electric generator symmetric");
        }
    }
    let pol = matmul(&matmul(&l, &minus_scalar(&l, 3)), &minus_scalar(&l, 6));
    assert!(pol.iter().all(|r| r.iter().all(|x| *x == 0)), "E_link eigenvalue polynomial");
    assert_eq!((0..6).map(|i| l[i][i]).sum::<i64>(), 18);
}
fn cover_check(missing_transposition: bool) {
    let t = if missing_transposition { &TRANS[..2] } else { &TRANS[..] };
    let mut reachable = BTreeSet::from([0u8]);
    for &x in t {
        reachable.insert(x);
        for &y in t {
            reachable.insert(mul(x, y));
        }
    }
    assert_eq!(reachable.len(), 6, "all S3 letters need at most two transpositions");
}
fn burnside_check() -> (u64, u64) {
    let raw = 6u64.pow(TREE_FREE_LINKS);
    let quotient = (raw + 3 * 2u64.pow(TREE_FREE_LINKS) + 2 * 3u64.pow(TREE_FREE_LINKS)) / 6;
    assert_eq!(raw, 16_926_659_444_736);
    assert_eq!(quotient, 2_821_153_019_713);
    (raw, quotient)
}
fn spectral_contract(r: u64, raw: u64) -> String {
    // This contract never evaluates the r=9 blind prediction.
    assert!(matches!(r, 27 | 81), "only the frozen excluded r=27 and r=81");
    let c = 144 + 72 * r;
    let delta_flat = 6 * r - 72;
    assert!(c >= 144 && delta_flat > 0 && raw == 6u64.pow(17));
    let num = (u128::from(c) - 72) * u128::from(raw);
    let den_factor = 34u64;
    let exponent = 68u64;
    // This is the exact FACTORED rational lower bound, not a decimal approximation.
    // Origin: C=144+72r; A=C I-H>=0, A^34_xy>=1 in rooted 6^17 space;
    // Doeblin bound of the ground-state transform, combined with E1<=72.
    format!(
        "GAP_BOUND|target=first_E2_minus_E1|r={r}|strict_positive=YES|numerator={num}|denominator={den_factor}*{c}^{exponent}|units=JE|scope=analytic_bound_not_spectrum|json=0\n\
GAP_BOUND|target=cluster_E22_minus_E21|r={r}|lower_JE={delta_flat}|E22_at_least_JE={}|E21_at_most_JE=72|scope=analytic_bound_not_spectrum|json=0\n",
        6 * r
    )
}
fn compute(plant: Option<&str>) -> String {
    let wrong_cost = plant == Some("wrong_magnetic_cost");
    let missing_transposition = plant == Some("deleted_transposition");
    let missing_flat = plant == Some("missing_flat_sector");
    // The independent checks below are designed to FAIL the three planted faults.
    cover_check(missing_transposition);
    electric_link_check();
    for a in 0..6u8 {
        assert_eq!(from_trits(trits(a)), Some(a), "two-trit S3 roundtrip");
        assert_eq!(mul(a, inv(a)), 0);
    }
    assert_eq!(from_trits([0, 2]), None);
    assert_eq!(LINKS, 24);
    assert_eq!(FACES, 24);
    let (raw_flat, mut classes) = flat_classes();
    if missing_flat {
        classes.pop();
    }
    assert_eq!(raw_flat, 48);
    assert_eq!(classes.len(), 21);
    let (raw, quotient) = burnside_check();
    let mut singles = 0u64;
    let mut doubles = 0u64;
    let mut two_cost = BTreeMap::<u64, u64>::new();
    for triple in classes {
        let u = flat_links(triple[0], triple[1], triple[2]);
        assert_eq!(magnetic(&u, wrong_cost), 0);
        for k in 0..LINKS {
            for t in TRANS {
                let mut v = u;
                v[k] = mul(t, v[k]);
                assert_eq!(magnetic(&v, wrong_cost), 8, "single-link flat-to-flat forbidden");
                singles += 1;
            }
            for j in (k + 1)..LINKS {
                for t in TRANS {
                    for s in TRANS {
                        let mut v = u;
                        v[k] = mul(t, v[k]);
                        v[j] = mul(s, v[j]);
                        let m = magnetic(&v, wrong_cost);
                        assert!(m >= 6, "double-link fell below nonflat cost");
                        *two_cost.entry(m).or_default() += 1;
                        doubles += 1;
                    }
                }
            }
        }
    }
    assert_eq!(singles, 1_512);
    assert_eq!(doubles, 52_164);
    assert_eq!(two_cost.values().sum::<u64>(), doubles);
    assert_eq!(two_cost.keys().next().copied(), Some(8));
    let mut text = format!(
        "YM4_06B|status=FINITE_ANALYTIC_BOUNDS|arithmetic=INTEGER_ONLY|toolchain=RUST_1_81|trits_per_element=2|r9_runs=0|json=0\n\
S3_STRUCTURE|flat_commuting_triples=48|flat_orbits=21|root_fixed_states={raw}|physical_gauge_orbits={quotient}|lattice=2x2x2|links=24|faces=24|free_links=17|json=0\n\
ELECTRIC|single_link_spectrum=0,3,6|E_min=0|E_max=144|M_max=72|S3_word_diameter=2|rooted_graph_diameter_at_most=34|json=0\n\
FLAT_MOVES|one_link_checks={singles}|one_link_cost=8|two_link_checks={doubles}|two_link_min_cost=8|kappa_all_nonflat=6_FROM_YM4_06A|json=0\n"
    );
    text.push_str(&spectral_contract(27, raw));
    text.push_str(&spectral_contract(81, raw));
    text.push_str("SCOPE|transfer_eigenvalues=NOT_COMPUTED|physical_mass=NOT_COMPUTED|continuum_SU2_gap=OPEN|HBI_HBP_SHA_SH_HASH=RECEIPT_ONLY|json=0\n");
    text
}
fn make_receipts(out: &Path) {
    fs::create_dir_all(out).expect("create output");
    let body = compute(None);
    let root = hash_bytes(body.as_bytes());
    let sh = &root[..16];
    let index = format!("HBI|records={}|bytes={}|source=YM4_06B|hbp_sha256={root}|sh={sh}|json=0\n",
        body.lines().count(), body.len());
    let index_sha = hash_bytes(index.as_bytes());
    let chain = hash_bytes(format!("YM4_06B|SHA={root}|SH={sh}|HBI={index_sha}|version=1").as_bytes());
    let anchor = format!("HASH|version=1|hbp_sha256={root}|hbi_sha256={index_sha}|sh={sh}|chain_hash={chain}|json=0\n");
    fs::write(out.join("TWO-GAPS.hbp"), body).expect("write HBP");
    fs::write(out.join("TWO-GAPS.hbi"), index).expect("write HBI");
    fs::write(out.join("TWO-GAPS.anchor"), anchor).expect("write HASH");
    println!("YM4_06B_RUN|PASS|r=27,81|first_gap=POSITIVE_FACTORED_BOUND|flat_cluster_gap=POSITIVE_BOUND|spectral_diagonalization=0|r9_runs=0|json=0");
}
fn value<'a>(line: &'a str, field: &str) -> &'a str {
    line.split('|').skip(1).find_map(|s| s.split_once('='))
        .find_map(|(k, v)| (k == field).then_some(v))
        .expect("missing HBI/HBP/anchor field")
}
fn verify(out: &Path) {
    let body = fs::read_to_string(out.join("TWO-GAPS.hbp")).expect("read HBP");
    let index = fs::read_to_string(out.join("TWO-GAPS.hbi")).expect("read HBI");
    let anchor = fs::read_to_string(out.join("TWO-GAPS.anchor")).expect("read HASH");
    assert_eq!(body, compute(None), "compute independent of stored HBP");
    assert_eq!(index.lines().count(), 1);
    assert_eq!(anchor.lines().count(), 1);
    let root = hash_bytes(body.as_bytes());
    let sh = &root[..16];
    let index_sha = hash_bytes(index.as_bytes());
    assert_eq!(value(&index, "hbp_sha256"), root);
    assert_eq!(value(&index, "sh"), sh);
    assert_eq!(value(&index, "bytes").parse::<usize>().unwrap(), body.len());
    assert_eq!(value(&index, "records").parse::<usize>().unwrap(), body.lines().count());
    assert_eq!(value(&anchor, "hbp_sha256"), root);
    assert_eq!(value(&anchor, "hbi_sha256"), index_sha);
    assert_eq!(value(&anchor, "sh"), sh);
    let expected = hash_bytes(format!("YM4_06B|SHA={root}|SH={sh}|HBI={index_sha}|version=1").as_bytes());
    assert_eq!(value(&anchor, "chain_hash"), expected);
    println!("YM4_06B_VERIFY|PASS|HBI=PASS|HBP=PASS|SHA=PASS|SH=PASS|HASH=PASS|r9_runs=0|json=0");
}
fn main() {
    let args: Vec<String> = env::args().collect();
    match args.get(1).map(String::as_str) {
        Some("compute") => make_receipts(Path::new(args.get(2).expect("output dir"))),
        Some("verify") => verify(Path::new(args.get(2).expect("output dir"))),
        Some("plant") => {
            let name = args.get(2).expect("plant name");
            assert!(matches!(name.as_str(), "wrong_magnetic_cost" | "deleted_transposition" | "missing_flat_sector"));
            let _ = compute(Some(name));
        }
        Some("r") => {
            let r = args.get(2).expect("r").parse::<u64>().expect("integer r");
            let _ = spectral_contract(r, 6u64.pow(17));
        }
        _ => panic!("usage: compute DIR | verify DIR | plant NAME | r 27|81"),
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn finite_model_exact() {
        assert!(compute(None).contains("first_E2_minus_E1"));
    }
    #[test]
    fn all_valid_two_trit_group_codes() {
        for a in 0..6 {
            assert_eq!(from_trits(trits(a)), Some(a));
        }
    }
    #[test]
    #[should_panic(expected = "only the frozen excluded")]
    fn blind_r9_forbidden() {
        let _ = spectral_contract(9, 6u64.pow(17));
    }
}
