# VOL14-D2 review: weighted locality, method ceilings, and D3 planning

**Provenance:** written by Claude (AI) on 25 Nov 2026. This is AI verification, not human review. Floating-point numerics are exploratory and are not certificates.

**State reviewed:**
- PR #126 at `9394b89`, which includes the D2 commits `3e3b0cd` (sealed expectations) and `0859e37` (certificate).
- PR #125 at `92bc81c`.
- `main` at `6bb6873`.
- Read through anonymous git. Hosted CI was not visible to this session, so the hosted-replay claims in the notes rest on the author's report.

## 1. Verdicts

| Item | Verdict |
|---|---|
| D2 replay | Receipt byte-identical, also under `-O`; D1 receipt still identical on the D2 tree; no-float gate 190 files, 0 failures; docs integrity 100 files, 0/0; merges cleanly with `main`. Expectations sealed about a minute before the certificate commit, and labelled not blind. |
| D2 Hessian stencil | **Matches an independent construction exactly:** same 33 offsets, same 525,780 nonzeros, maximum difference 1.9×10⁻¹⁴. |
| D2 written argument | **Correct.** No gaps found (§3). |
| Sharpness of the D2 constants | They are essentially optimal *for this method* (§4). Further gains need a different method. |
| D3 route | D2 already gives uniform Dirichlet-inverse bounds on every patch (§5.1). A finite-range approximate inverse was tested and **does not** certify a better rate at practical sizes (§5.2). Build the background Hessian first (§5.4). |
| PR #125 archive | Review 07 is archived verbatim with a clearly separated addendum. The recorded SHA-256 `842d19fb…ad56` matches the script I wrote. The D1 note's range-two edit is accurate. |

## 2. Independent stencil check

I rebuilt the ambient Hessian H = P Tᵀ dᵀ d T P from the written definitions: the VOL14-C linearization L, the coordinate-ordered tree, P as the orthogonal projector onto Z, and T = (I − RL)P. I then compared it, block by block, with the checker's integer stencil divided by D².

- Offsets: 33 and 33, identical sets.
- Nonzeros: 525,780 and 525,780.
- Largest entrywise difference: 1.9×10⁻¹⁴.

## 3. The written argument

- **T P rows.** L's only crossing coefficients lie on its own face and equal 1/27 each, so L P keeps exactly the non-tree internal coefficients. A crossing row of T P is therefore δ − (face mean) − (L P), and every other non-tree row is δ. Correct; this is also what makes the stencils agree.
- **Range.** A (μ, ν) plaquette row of K = dTP reaches blocks 0, e_μ, e_ν and e_μ+e_ν only. Correct, and enforced by `K_range`.
- **Folded envelope bound.** Coarse shifts are isometries of ℓ² over coarse sites, including on small tori where offsets wrap. Correct.
- **Hermitian part of W H W⁻¹.** H is real symmetric, so the (x, z) entry of the Hermitian part is H_xz·cosh(log(W_x/W_z)). The bound |log(W_x/W_z)| ≤ ℓ(a)·log t follows from the triangle inequality for the graph distance. cosh(ℓ log t) − 1 equals (p−q)²/(2pq) for ℓ = 1 and (p²−q²)²/(2p²q²) for ℓ = 2. All correct.
- **Weighted Schur test on F.** The checker verifies that F is symmetric before applying the single-vector test. Correct.
- **Restriction to Z.** W commutes with P, so W H W⁻¹ maps Z to Z, and Re ⟨z, H_W z⟩ ≥ (1/105 − ‖F‖)‖z‖². Correct.
- **Covariance.** ‖W T W⁻¹‖ ≤ t·√13, because the bound 13 applies to the folded envelope, not only to the operator. Then 220·13·65² = 12,083,500 < 3000·64² = 12,288,000. Correct.
- **Complex strip.** H(k+iη)* = Σ H_b e^{ik·b} e^{η·b}, so the Hermitian part is Σ H_a e^{ik·a} cosh(η·a). The real-axis floor holds at every real k: the D1 curvature identities are local linear identities, so they hold for quasi-periodic fields, and ‖T(k)z‖ ≥ ‖z‖ because R L(k) z is constant on each face while z has mean zero there. Correct.
- **Chebyshev variant.** 57·105 = 5985 < 79² gives q < 39/40, with prefactor 2·105·13 = 2730. Correct.

**Two edits I'd suggest for the D2 note** (both are statements of scope, not errors):
1. The bound 3000·(64/65)^r drops below 1 only for r ≥ 517 coarse spacings. The Chebyshev variant needs r ≥ 627 and has rate ln(40/39)/2 ≈ 0.0127. The D1 note now carries the matching sentence.
2. Record the method ceilings from §4, so that readers do not expect a refined envelope to approach the measured strip.

## 4. How tight D2 is, and where this method stops

**The certificates are already close to optimal for the folded method:**

| Quantity | Certified | Exact value for the same folded object | True operator |
|---|---|---|---|
| ‖T P‖² | ≤ 13 | 12.08 | 7.30 (sup over k) |
| ‖K‖² = ‖H‖ | ≤ 57 | 56.02 | 16.23 |
| ‖F‖ at t = 65/64 | ≤ 23/4620 = 0.004978 | 0.004823 | — |

The weight 65/64 sits within 2% of the largest the method allows with a floor of 1/220 (η ≈ 0.01575). The checker's rejection of 33/32 is consistent: ‖F(ln 33/32)‖ ≈ 0.0190.

**Ceilings.** All rates are per coarse step, and "polystrip" means |Im k_j| ≤ η for all four coordinates.

| Method | Polystrip width |
|---|---|
| D2 as certified | 0.0155 |
| Folded accretivity, if the floor stays 1/105 | ≤ 0.022 |
| Folded accretivity, even with the measured floor 0.0326 | ≤ 0.040 |
| Exact accretivity with linear exponential weights: the largest η with Re H(k+iη) ≻ 0 for all k | ≈ 0.15 (≈ 0.25 along a single axis) |
| True singularity distance (sampled) | ≈ 1.5 |

At the certified η = 0.0155 the true Hermitian-part floor is still 0.0324, seven times the certified 1/220. At η = 0.1 it is 0.0214.

**The true strip is about 1.5 in all four coordinates, on the points I sampled.** σ_min of H(k+iη·s) over the eight sign patterns s, at 16 symmetric points plus 40 random real parts:

| η | 0.5 | 1.0 | 1.25 | 1.5 |
|---|---|---|---|---|
| min σ_min | 0.028 | 0.017 | 0.0053 | 0.0032 |

Together with the axis singularity near η ≈ 1.51 reported in review 07, this puts the true polystrip at about 1.5. You are right that sampling cannot exclude singularities elsewhere. This table adds polystrip corners to review 07's axis lines, but it is still a sample.

**Consequence.** Refining envelopes can gain at most about 2.6× over D2. Certifying exact accretivity, rather than its envelope, could gain about 10×. Reaching the true rate needs a method that uses the inverse itself, not just positivity of H. §5 tests one.

## 5. A quantitative route for D3

### 5.1 Why the certified rate decides whether a random walk is viable

A random-walk expansion converges when the weighted size of one step, summed over the neighbouring cubes, is below 1. Roughly, this needs e^{−m·w} · C · N < 1, where:
- m is the certified rate per coarse step;
- w is the margin between a cube and its enlargement, in blocks;
- C is a prefactor, roughly ‖H‖·‖G‖;
- N is the number of neighbouring cubes, 80 in 4D.

| Rate used | Margin needed (blocks) |
|---|---|
| D2's m = 0.0155, with C ≈ 16·3000 | ≈ 1,000 |
| Measured m ≈ 1.5, with C ≈ 16·30 | ≈ 7 |

The random walk is the tool for handling background dependence; it does not by itself improve the rate. With D2's rate, cubes would need margins of order 10³ blocks. That is admissible in an analytic proof, where the cube side only enters the constants, but no finite computation can certify cubes of that size.

**D2 already supplies uniform Dirichlet bounds.** For any patch Δ, the restriction 1_Δ Re(H_W) 1_Δ is still ⪰ (1/220) on Z restricted to Δ. So every local Dirichlet inverse G_Δ = (1_Δ H 1_Δ)⁻¹ satisfies ‖W G_Δ W⁻¹‖ ≤ 220 at rate ln(65/64), for every patch and every target, with no further computation. This is a ready-made input for D3.

### 5.2 Negative result: a finite-range approximate inverse does not certify a better rate

**The method tested:**
1. Take G̃ to be the true inverse kernel of H|_Z (Bloch on an 8⁴ torus; sanity check ‖(HG)₀ − I‖ = 8×10⁻¹⁴), truncated to an offset set S.
2. Then R = I − H G̃ = H(G − G̃) has finite range.
3. If a certifiable bound on R is below 1, then H⁻¹ = G̃(I − R)⁻¹, and weighted versions give the rate.

**The inverse kernel has a broad near field.** The largest ‖G_X‖ at each ℓ¹ distance from 0 to 4 is 13.8, 5.14, 2.19, 0.166 and 0.029. That is a box truncation (|X_j| ≤ 2), which omits offsets such as (3, 0, 0, 0).

**Remainder at η = 0:**

| S | True sup over k of ‖R(k)‖ | Σ_X ‖R_X‖₂ | Σ_X ‖R_X‖_F | Folded envelope |
|---|---|---|---|---|
| ℓ¹ ≤ 1 (9 offsets) | — | — | — | 66.6 |
| ℓ¹ ≤ 2 (33) | 3.6 | 28.7 | 39.8 | 15.2 |
| ℓ^∞ ≤ 1 (81) | 1.06 | 10.5 | 14.2 | 6.76 |
| ℓ¹ ≤ 3, ℓ^∞ ≤ 2 | — | — | — | 6.33 |
| ℓ¹ ≤ 4, ℓ^∞ ≤ 2 (257) | 0.41 | 4.41 | 5.88 | 2.80 |

Even with 257 offsets of 240×240 blocks, the true remainder is 0.41, and every certifiable bound is above 1, before any weight is applied. The obstacle is mainly truncation, not folding: the envelope 2.8 is already better than the block-norm sum.

From the trend (about ÷2.3 per ℓ¹ shell), a certifiable envelope below 1/2 needs roughly ℓ¹ ≤ 6. That is about 1,300 offsets, roughly 7.5×10⁷ stored entries, and an exact convolution of order 10¹¹–10¹² operations. **I withdraw this route** as a practical D3 certificate in these coordinates.

**What remains open.** The ceiling table in §4 bounds what each method can reach:
- folded accretivity: about 0.02–0.04;
- exact accretivity: about 0.15, needing a certificate of Re H(k+iη) ⪰ c, for example a local positive-semidefinite (SOS) decomposition, whose feasibility I have not tested;
- the true rate, about 1.5: I see no cheap certified route.

So the key planning question is which rate the multiscale argument actually needs, given that the cube side and the coupling threshold can absorb a weak rate in an analytic proof.

### 5.3 Nonflat backgrounds: an order-of-magnitude budget

> **Superseded (review 09, 25 Nov 2026).** The 10⁻⁴ estimate below assumed an *absolute* perturbation budget. Review 09 built the background-dependent Hessian. A *relative-form* comparison, in a smooth background gauge, measures E_min ≈ −(7 to 12)·θ_p,max, which points to a tolerance near VOL14-C's δ = 1/30. That is a measurement, not a certificate. The text below is kept for the record.

D2's accretivity tolerates a background perturbation δH of the Hessian only if its weighted envelope is below 1/105 − ‖F(η)‖, which is at most 0.0095.
- Against an envelope ‖H‖ of 57, that is a relative change of about 2×10⁻⁴.
- With the true floor and norm (0.0326 and 16.2), the relative tolerance is about 1/(2κ) ≈ 10⁻³.

In block-tree gauge a background link deviates from the identity by up to about (path length) × (plaquette angle). With path lengths of order 10, the relative-tolerance estimates above point to plaquette angles of order 10⁻⁴ for the propagator analysis, far below VOL14-C's δ = 1/30.

This is a rough estimate. The real figure needs the background-dependent Hessian: the covariant curl, L_U and a tree gauge at U. If it holds, the propagator will need its own small-field tolerance, and a larger β, separate from the VOL14-C normalization tolerance. That belongs in the multiscale plan now. Certifying the true floor (0.0326 instead of 1/105) alone would roughly triple the budget.

### 5.4 Suggested D3 sequence

1. **Build the background-dependent constrained Hessian first** (covariant curl, L_U, tree gauge at U) and measure the envelope of δH per unit plaquette angle. This decides the propagator's small-field tolerance and is cheap compared with the alternatives.
2. **Extend D2 to backgrounds by perturbation.** Certify the envelope of δH_W below 1/105 − ‖F(η)‖ on the chosen small-field domain. If that works, D2's Dirichlet bounds (§5.1) carry over to every patch, uniformly in the background.
3. **Write down the polymer and random-walk bookkeeping with explicit constants,** and determine which rate and prefactor it actually needs. With a weak rate, this sets the cube side and the coupling threshold.
4. **Only if step 3 needs it, improve the rate.** Raise the certified floor toward 0.0326, or certify exact accretivity, whose ceiling is about 0.15. Do not plan on reaching the true rate of about 1.5 by certification.
5. **Freeze predictions** from §4 and §5.2 (polystrip ≈ 1.5, exact-accretivity ceiling ≈ 0.15, the truncation table) so later work can be scored against them.

## 6. Paste-ready comment for PR #126

> AI review (Claude), 25 Nov 2026. VOL14-D2 at `9394b89`: the receipt replays byte-identically (also under `-O`); the D1 receipt is unchanged; no-float gate 190/0; docs 100/0/0; the branch merges cleanly with `main`.
>
> An independent floating-point construction of P Tᵀ dᵀ d T P from the written definitions matches the integer stencil exactly: 33 offsets, 525,780 nonzeros, maximum difference 1.9×10⁻¹⁴. The written argument checks: the Hermitian part with cosh weights, the distance bound, the symmetric majorant, restriction to Z, the weighted T bound, the strip continuation and the real-axis floor at all k.
>
> The constants are close to optimal for the folded method: the exact folded norms are 12.08 (certified 13) and 56.02 (certified 57), and ‖F(ln 65/64)‖ = 0.00482 against a budget of 0.00498.
>
> Suggested additions to the note: (1) the bound is below 1 only for r ≥ 517; (2) folded accretivity cannot exceed η ≈ 0.022 with the 1/105 floor, or about 0.040 even with the measured floor; exact accretivity with exponential weights caps near 0.15; the sampled true polystrip is about 1.5. Floating point, not a certificate.

## 7. Reproduction

Scripts are numpy-only and stored outside the proof repository.

| Script | What it produces |
|---|---|
| `reviews/07-vol14d_bloch_crosscheck.py` | The operator construction, in Z coordinates. |
| `reviews/08-d2_xcheck.py` | The §2 stencil comparison; the §4 envelope norms and F ceilings. Loads the checker from a PR #126 worktree. |
| `reviews/08-d2_ceiling.py` | The §4 accretivity ceilings and polystrip σ_min. |
| `reviews/08-d3_parametrix.py` | §5.2: the truncated-inverse envelopes. Writes Goff.npy. |
| `reviews/08-d3_diag.py` | §5.2: true remainder norms and block-norm sums. |

**Sign convention.** With (Hu)_x = Σ_X H_X u_{x+X}, the symbol is H(k) = Σ_X H_X e^{ik·X}, and the real-space inverse is G_X = N⁻¹ Σ_k G(k) e^{−ik·X}. My first run of §5.2 used e^{+ik·X}, which gives G_Xᵀ and meaningless remainders; it was discarded. Review 07's real-space table is unaffected, because ‖C_{−X}‖ = ‖C_X‖.

Not done: certification of any number in §4 or §5, a test of the SOS route, the background-dependent Hessian, and any check of hosted CI.
