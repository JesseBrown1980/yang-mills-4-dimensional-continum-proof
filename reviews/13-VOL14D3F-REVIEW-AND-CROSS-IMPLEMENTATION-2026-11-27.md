# VOL14-D3F review and cross-implementation check on the rational staggered fixture

**Provenance:** written by Claude (AI) on 27 Nov 2026. This is AI verification, not human review. Floating-point numerics are exploratory; **none is a certificate.**

**State reviewed:**
- PR #136 at `dffc5b7`, then at `1cda961` after the no-float fix; seal in `32a0c69`.
- Stacked on #135 at `ea135f0`.

## 1. Verdicts

| Item | Verdict |
|---|---|
| Replay | Both checkers together reproduce the receipt byte-identically (about 19 s) at `dffc5b7` and at `1cda961`, and the receipt equals the seal. |
| **Hosted CI at `dffc5b7`** | **8 of 16 failed.** Every failure (atlas-source-and-falsifiers ×2, exact-dual-window ×2, exact-replay, gaussian-integer-replay, no-float, no-float-base) was the no-float gate flagging `Q**(8-2*k)` at line 145 of `tests/ym4_vol14d3f_rational_fixture.py` as "power with an unproven exponent". The exponent is nonnegative because k ≤ 4, but the gate cannot prove that. |
| Fix | A two-line patch (`QPOW=(Q**8,Q**6,Q**4,Q**2,1)` and `QPOW[k]`), applied as `1cda961`: receipt unchanged, local gate `failed=0`, hosted CI 14 of 14 successful at inspection. Note that the gate reads git blobs, so a working-tree edit has to be staged before it is visible to the gate. |
| Rational fixture | **Independently decoded and confirmed.** SHA-256 `305b5acb…` matches. Unit norm holds exactly by construction (stereographic form). Tiled onto the 12⁴ fine torus, all tree links are exactly the identity under review 09's tree convention, θ_max = 0.027765 / 0.033317 (matching 0.0277646 / 0.0333172), and the relative stationarity residuals are 4.3×10⁻¹⁰ / 3.3×10⁻¹⁰, consistent with the defect bounds. |
| Neutral face identity (DG R)_neutral = \|V\|² | **Correct:** with an Abelian background every path crosses one face link, so δV = V·iY. |
| Symmetry reduction | **Count reproduced independently:** 128 characters, (128 + 16)/2 = 72 neutral representatives, 128 charged, dimension 2·240 = 480; coverage 128·480 neutral + 2·128·480 charged = 184,320. Valid because the background and multipliers are periodic and Abelian, so the residual U(1) colour symmetry holds. |
| Tent-compensated gluing | **Exact identity:** Σ_c w(x−c)w(x+a−c) = g(a) independently of x, so ⟨z, Az⟩ = N⁻¹Σ_c⟨wz, A♯wz⟩. See the practicality remark in §3. |
| KKT congruence | **Correct:** inertia(bordered) = inertia(A_c) + (m, m, 0). |
| Flat calibration at R = 99 | Replayed; consistent with D2. |

## 2. Cross-implementation on the D3F fixture

Review 12's operator (`12-aug.py`: matrix-free G-chart, validated to 2×10⁻⁹) was run on the rational fixture tiled to the 4⁴ coarse torus, over all 184,320 Z coordinates with random starts and no subspace restriction.

| | δ = 1/30 | δ = 1/36 |
|---|---|---|
| Wilson-only lowest relative eigenvalue (this review) | **0.6110654** (residual 3.8×10⁻¹⁰) | **0.6629196** (residual 1.6×10⁻¹⁰) |
| D3E Wilson-only (author) | 0.6110654 | — |
| Augmented lowest relative eigenvalue (this review) | **0.6116457** (residual 6.8e-09, 113 matvecs) | **0.6629920** (residual 8.0e-09, 100 matvecs) |
| D3E augmented (author) | 0.6116457 | 0.6629920 |

**Reading.**
- The two implementations agree to the 7 digits reported, on both the Wilson-only and the augmented floors.
- The implementations are independent. D3E uses JAX with a prefix DAG on the M = 2 source arrays and periodic extension. This review uses NumPy with factorized connector means and a central-difference G-chart matvec on the rational fixture tiled to M = 4.
- The fixture's rounding to n/2⁴⁰ (component changes below 9×10⁻¹³) leaves the floors unchanged at this precision.
- This validates both operators against each other on the harder known fixture. It is still numerical: no inertia certificate has been computed. The G-chart stationarity residuals are 3.3e-10 and 4.3e-10, equal to the F-chart residuals.

## 3. Remarks

1. **Both known hard fixtures are exactly Abelian.** The D3F staggered field and review 11/12's adversarial witness both have zero j and k components on every link. Their charged directions decouple by symmetry, and D3F's 200-sector reduction relies on that U(1) structure. The nonabelian backgrounds measured so far (review 09/10 random and smooth fields) had higher floors, but they were never adversarially optimized. **A uniform certificate must cover nonabelian backgrounds.** The next numerical test should be an adversarial search over coarse fields with two non-commuting colour components; the D3F reduction does not apply there.
2. **How large the gluing patches must be.** A♯ multiplies off-diagonal block couplings by (S/(S−R))^k, where k is the ℓ¹ length of the offset:

   | R | patch side (blocks) | factor for k = 1 | factor for k = 2 |
   |---|---|---|---|
   | 2 | 3 | 1.50 | 2.25 |
   | 3 | 5 | 1.19 | 1.41 |
   | 4 | 7 | 1.10 | 1.21 |
   | 5 | 9 | 1.06 | 1.13 |

   With a known augmented floor of about 0.61 against the 1/2 target, the relative margin is about 22%. Unless the patch-local floors sit well above the global one, this points to R ≥ 4–5. Such patches have about 1.7–4.7 million coordinates, so they need the exact symmetry and sparse elimination D3F already proposes; dense patches are out of reach.
3. **Near-stationarity in a certificate.** The rational fixtures have exact stationarity defects of at most 1.6×10⁻¹¹ per link component. A spectral certificate at such a point must carry the O(defect) difference between the Hessian at the fixture and at the exact nearby stationary point, which D3F lists as open. It is negligible numerically but has to appear in the certificate.

## 4. Paste-ready comment for PR #136

> AI review (Claude), 27 Nov 2026. VOL14-D3F at `1cda961`: the receipt replays byte-identically and equals the seal; no-float `failed=0` after the two-line `QPOW` fix (the 8 hosted failures at `dffc5b7` were all that gate); hosted CI 14/14 at inspection.
>
> Independent decode of the rational fixture: the hash matches, tree links are exactly the identity, θ_max = 0.027765 / 0.033317, and the relative stationarity residual is 4.3e-10 / 3.3e-10. The neutral face identity, the 200-sector count, the tent-compensated gluing identity and the KKT inertia shift are all correct.
>
> Cross-implementation on the tiled fixture (review 12's G-chart operator, full space, random start): Wilson-only 0.6110654 at 1/30, identical to D3E, and 0.6629196 at 1/36. Augmented: 0.6116457 at 1/30 and 0.6629920 at 1/36, against D3E's 0.6116457 and 0.6629920, so the two independent implementations agree to 7 digits.
>
> Remarks: both known hard fixtures are exactly Abelian, so nonabelian adversarial backgrounds remain untested. The compensated gluing amplifies off-diagonal couplings by (S/(S−R))^k, which suggests R ≥ 4–5 for a 22% margin. Floating point, not certificates.

## 5. Reproduction

The scripts are stored in the project as `reviews/13-*.py` and use the review 09–12 modules.

| Script | What it does |
|---|---|
| `13-rat_decode.py` | Decodes and tiles the D3F fixture and runs the checks. |
| `13-rat_eig.py` | The Wilson-only and augmented full-space solves, about 1 hour per tolerance with two in parallel on 2 cores. |
