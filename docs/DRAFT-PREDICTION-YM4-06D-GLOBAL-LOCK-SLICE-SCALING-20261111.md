# DRAFT for correction — YM4-06D: the global lock under slice refinement (3+1 dimensions)

**Status: DRAFT. Nothing in this file is frozen, and nothing was computed for it.** It is put up for the operator and GPT-6 to correct. A prediction file (`.hbp`, committed alone) follows only after the corrections, and before any run. The r = 9 one-shot of the finite repository is a separate lane with its own release gates and is untouched by this file.

Written 2026-11-11 by the local seat (Opus 5.5). Tags: **DERIVED** = follows by a written argument from stated inputs; **MEASURED** = a number in a named receipt; **NAMED** = stated from the literature or from a document, without a check here; **CONJECTURE** = a prediction that a run can refute; **OPEN** = undefined or undecided, a question to the reviewers.

## 0. The claim under test, in the operator's terms and in testable terms

The operator's statement (2026-11-11): the universe is discrete and sliced frame by frame; a global hash lock is a global state that every local part answers to, as entanglement does; with it, a four-dimensional mass gap can be shown, and the discrete system looks continuous.

The sources read for this draft: Law 34 (Brown–Schrödinger), Law 66 (the lighthouse loop), Law 67, Law 70 (levels of shadow cats) and Law 71 (hotter black), in `canon/` of the HTTP-0 repository.

Testable form used here:

1. **The lock.** The global state is the flat-sector label of a lattice gauge field: no single plaquette reads it, and it constrains every plaquette. In Law 71.9's ledgers it belongs to **SH** (shadow state and lineage). **SHA** is the byte-integrity commitment and is never an input to a spectral quantity.
2. **Frame by frame.** One frame to the next is one application of a transfer operator T_a. Law 71.13's chain freeze(IS_k) → pump → verify → freeze(IS_{k+1}) is that step.
3. **The mass.** m(a) = −log(λ₂(T_a)/λ₁(T_a)) / a, with the eigenvalues taken on the gauge-invariant space.
4. **Law 70's form.** A pass with n equally populated levels keeps (n − 1)/n. With n = 3^k and slice spacing a₀/3^k the mass obeys 1/a₀ ≤ m_k ≤ 3^k/((3^k − 1)a₀) (GitRAM PR #7, a constructed noninteracting model). The form restates a gap; a₀ is the correlation time 1/m. Whether an interacting gauge operator has it is what the rows below ask.

## 1. Definitions

**Model.** Periodic cubic spatial lattice (ℤ/L)³ with N_ℓ = 3L³ links, gauge group G, and, as in YM4-06B,

```text
H(r)/J_E = E + r·M,   E = Σ_links (3I − Σ_transpositions L_{link,τ}),   M = Σ_faces (2 − χ_std(U_face))      (G = S₃)
```

Levels e₁ ≤ e₂ ≤ … of H/J_E on the gauge-invariant space, with multiplicity.

**Transfer operator (proposed; to be corrected).** In units J_E = 1 and temporal step a:

```text
T_a = exp(−a·r·M/2) · exp(−a·E) · exp(−a·r·M/2)
```

It is symmetric, positive definite and gauge invariant; exp(−a·E) is a product over links because the link terms commute. Eigenvalues λ₁ ≥ λ₂ ≥ … > 0. Define μ_j(a) = −log(λ_j/λ₁)/a.

**The two observables, never merged** (GPT-6's ruling of 2026-11-11):

- first excitation: δ₁ = e₂ − e₁, and m_first(a) = μ₂(a);
- separation above the flat cluster: δ_flat = e_{F+1} − e_F with F the number of flat sectors (F = 21 for S₃ in three dimensions, 8 in two), and m_lock(a) = μ_{F+1}(a) − μ_F(a).

**Lock cost.** κ(G, L) = the smallest magnetic cost of a nonflat configuration. MEASURED and DERIVED in YM4-06A for S₃: κ = min(8, 3·L_min). It is a classical quantity and enters no row as a spectral scale; it appears only as a diagnostic.

**Refinement step k.** Level count n = 3^k.
- *Time only:* spatial lattice fixed, a_k = a₀/3^k.
- *Space and time:* L_k = 3^k·L₀ at fixed physical side, with a coupling r_k and an energy unit J_{E,k} to be specified by a trajectory. Physical masses are M_first(k) = J_{E,k}·δ₁(L_k, r_k) and M_lock(k) = J_{E,k}·δ_flat(L_k, r_k).

**Ledgers per frame (Law 71.9).** HBP: the tuple body with the measured values. HBI: its row index. SHA: sha256 of every frozen and derived object. SH: for each frame, the sector label, the level k, the cycle state (C0, C1, C2 with R³ = identity), and the hash of the frame it was derived from.

## 2. Rows proposed for the freeze

### A. Time refinement (controls; expected to hold)

| Row | Statement | Tag | Falsifier |
|---|---|---|---|
| A1 | For fixed L and r, A(k) := 3^k·(1 − λ₂(T_{a_k})/λ₁(T_{a_k})) converges to a₀·δ₁, from below once k is large. Equivalently a₀*(k) := 3^k·log(3^k/(3^k − 1))/m_first(a_k) converges to 1/δ₁: Law 70's form holds in the limit with a₀ the correlation time. | DERIVED (symmetric splitting, finite dimension) | A limit outside the enclosure of a₀·δ₁ |
| A2 | The same for the lock: 3^k·(1 − λ_{F+1}/λ_F) converges to a₀·δ_flat. | DERIVED | as A1 |
| A3 | If the spacing is held at a₀ while n = 3^k grows, a spectrum of the form (n − 1)/n has mass tending to 0 (the control of GitRAM PR #7). A run that reports a positive limit without shrinking the spacing is rejected. | DERIVED | — (a gate on the readout) |

### B. Equal population (Law 70's condition)

Slice the interval a₀ into n steps of two sizes, b/2 and 3b/2 alternating, with b = a₀/n, and compare with n equal steps. The uneven mass is read from the symmetric two-step block P = T_{3b/2}^{1/2}·T_{b/2}·T_{3b/2}^{1/2}, which covers the time 2b: m_uneven = −log(λ₂(P)/λ₁(P))/(2b).

| Row | Statement | Tag | Falsifier |
|---|---|---|---|
| B1 | The deviation of the mass from δ₁ under the uneven slicing, divided by the deviation under equal slicing, tends to 7/4 as k grows (the ratio of Σ b_i³). | DERIVED at leading order | A limit other than 7/4 |
| B2 | Direction, as in Law 70 ("uneven levels survive more than the law allows"): the uneven slicing gives the larger survival λ₂/λ₁ per interval, which is the smaller mass. | CONJECTURE | The uneven slicing gives the smaller survival |

### C. Space and time refinement (the rows that decide the claim)

| Row | Statement | Tag | Falsifier or what is missing |
|---|---|---|---|
| C0 | The trajectory. In the Kogut–Susskind normalisation of a gauge Hamiltonian in 3+1 dimensions, J_E ∝ g²/a and J_B ∝ 1/(g²a), so r = J_B/J_E ∝ 1/g⁴ and both scales grow like 1/a. | NAMED; the S₃ model has no Lie-algebra normalisation, so the map (g, a) → (r, J_E) for it is **OPEN** | Reviewers to fix the convention before the freeze |
| C1 | Fixed alphabet. For a fixed finite group, M_lock(k) = J_{E,k}·δ_flat ≈ κ·J_{B,k}, which grows without bound along any trajectory with J_B ∝ 1/a. The lock of a fixed finite alphabet gives an infinite mass in the limit, and the model leaves the continuum theory (the freezing of finite-subgroup approximations, NAMED). | CONJECTURE beyond 2×2×2; on 2×2×2 it rests on δ_flat ≥ 6r − 72 (YM4-06B) and on the two-sided bounds of GitRAM PR #6, both awaiting review | M_lock bounded along such a trajectory |
| C2 | The scaling Law 70 needs. A finite, positive lock mass in the limit requires the lock's log-ratio per slice, a_k·M_lock(k), to fall like 1/3^k. With a fixed alphabet it stays of order κ·(J_B·a) ∝ κ/g², which does not fall: the level count n of Law 70 does not grow when only the slices are tripled. It grows only if the alphabet is refined with the slices, with lock cost κ_k ∝ 3^{−k}. | DERIVED from the definitions and C0 | — |
| C3 | The operator's mechanism, in this form: there is a sequence of alphabets A_k for SU(2), refined with the slices, with κ(A_k)·3^k → κ* in (0, ∞); along it M_lock → κ*·(J_B·a)/a₀, finite and positive. | CONJECTURE, and **OPEN in its definition**: S₃, 2T, 2O and 2I are four separate examples and no refining sequence (GPT-6); an admissible sequence A_k (finite partitions of SU(2) compatible with gauge invariance) has to be defined before this row can be frozen | To be written once A_k is defined |
| C4 | First excitation at fixed alphabet. δ₁ is the splitting inside the flat cluster (fourth order on 2×2×2 for S₃, GitRAM PR #6, exploratory). Along growing L_k the splitting closes, so M_first is the tunnelling rate between lock sectors and no mass gap; the mass of the locked phase is M_lock. | CONJECTURE | M_first bounded below along the trajectory |
| C5 | Continuous SU(2) control. YM4-06A gives exact families with action tending to 0 above the flat set, so κ = 0 and there is no classical lock mass. A positive SU(2) gap, where one is proved (YM4-02d, YM4-02e at tanh β < 1/14), is a quantum transfer-operator bound and no lock effect. | DERIVED from the cited results | — |
| C6 | Counter-family control. The exact family of YM4 PR #34 (positive gap at every level, the power-of-three jump law holds, physical gap tends to 0) must be read as "gap closes" by the same readout that reads rows C1 to C4. | control | The readout reports a positive limit for that family |

### D. The lock as a state (the SH ledger)

| Row | Statement | Tag | Falsifier |
|---|---|---|---|
| D1 | The sector label is exactly conserved by exp(−a·r·M) and is changed by exp(−a·E) only through paths that leave the flat set; on 2×2×2 for S₃ the flat levels first split at fourth order (NAMED from GitRAM PR #6, exploratory and awaiting review). The off-diagonal part of the effective F×F block is the per-frame lock-violation amplitude. | DERIVED in structure; the order and the size to be MEASURED under a frozen row | A splitting of the flat levels at an order below the one frozen |
| D2 | The residue (C0 + C1 + C2) mod 3 of Law 71.13 is unchanged by the blocking 27 → 9 → 3 → 1 and by the cycle R (YM4 PR #34, hosted). It is recorded per frame in SH. | anchor, already MEASURED there | — |
| D3 | A change of one local trit changes the SHA Merkle root of the frame and leaves distant trits unchanged (GitRAM PR #7). This is a property of the commitment and is recorded as such; no row reads a mass from it. | anchor | — |

## 3. What can be computed, and where

Orbit counts by Burnside, (1/|G|)·Σ_g |C(g)|^(E − V + 1). The formula reproduces the 3×4 count 2,177,317,873 (MEASURED in the finite repository). The three-dimensional figures are DERIVED from it and unmeasured.

| Lattice, group | Gauge orbits | Route |
|---|---|---|
| 2×2 (two dimensions), S₃ | 1,393 | exact T_a; rows A1, A2, B1, B2 can be measured in full |
| 2×2×2, ℤ₃ | about 1.3 × 10⁸ | exact, abelian control |
| 2×2×2, S₃ | 2,821,153,019,713 | the F = 21 effective block with remainder bounds (as GitRAM PR #6); one symmetry sector of about 7 × 10⁹ states would need a key table of roughly 59 GB, which the 300 GB Host8 store can hold, with rows computed on the fly |
| 2×2×2, Q8 and larger | about 2.8 × 10¹⁴ and up | no exact route; series, no-store vector bounds, transfer bounds |
| any 6×6×6 | — | no exact route; rows C1 to C4 at k ≥ 1 rest on bounds and series |

So rows A and B are measurable now on small lattices. Rows C are measurable at k = 0 and, beyond it, only through bounds; C3 cannot be measured until its alphabet sequence is defined.

## 4. Questions for the operator and GPT-6

1. Is the transfer operator of section 1 the one to freeze, or the Wilson Euclidean transfer matrix of Lemma 0004 with an anisotropy parameter?
2. Row C0: which map from (g, a) to (r, J_E) for the finite-group models?
3. Row C3: what is an admissible alphabet sequence A_k? Without it the operator's mechanism has no frozen row.
4. Row B2 and row C4 are stated as conjectures with a direction. Are the directions the ones the operator predicts?
5. Row C1 says a fixed finite alphabet gives an infinite lock mass in the limit. If the operator's picture is that the alphabet is fixed (ternary) while only the slices refine, then C1 is the prediction to test and C3 is withdrawn; which is it?
6. Should the SH row carry anything beyond sector label, level, cycle state and parent hash?

## 5. Scope

Each row is a statement about a finite lattice or about a stated sequence of them. The Clay problem (target 3 of the README) is OPEN. Nothing here is a measurement, and no row is frozen.
