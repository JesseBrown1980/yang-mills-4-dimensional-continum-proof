# DRAFT for correction — YM4-06D: global lock under slice refinement (3+1 dimensions)

**Status: DRAFT, NOT FROZEN. No YM4-06D spectral computation was run.** Revision of the local-seat draft, with GPT-6's mathematical review applied 2026-11-11. The first prediction-only HBP commit must follow approval of the definitions, and must precede any measurement. The 3×4 r=9 blinded finite-model lane is untouched.

Tags: **DERIVED** (short proof from specified hypotheses); **MEASURED** (pinned prior result); **NAMED** (literature or repo statement not independently checked here); **CONJECTURE** (new refutable claim); **OPEN** (required construction or bound missing). A derived fact about a toy or finite model is never an established 4D continuum result.

## 0. The physical question and the two global records

The operator's hypothesis is that reality is discrete and advances in slices, with local changes consistent with a global state that behaves like a lock. Its mathematical test is whether an interacting gauge-invariant transfer operator can preserve a **positive physical first-excitation mass**, as spatial and temporal spacing tend to zero and the physical volume is controlled.

These are **different** objects:

1. **Gauge/global state:** for finite S₃ on a torus, the flat holonomy triple, modulo conjugation, gives 21 flat configuration orbits in three spatial dimensions. Local plaquette holonomies cannot determine which flat orbit holds. The *quantum* Hamiltonian may mix them through nonflat intermediate configurations; a flat configuration label is not automatically a quantum superselection charge. For continuous untwisted SU(2), the flat moduli are continuous, not 21 isolated sectors. Any SU(2) physical lock observable must be gauge invariant and defined separately.
2. **SHA/SH/HASH records:** HBP holds the state/observable/residual tuples, HBI their ordered offsets, SHA the byte digests, SH the derived shadow/cycle/sector lineage, and HASH the canonical slice commitment. One local change can change the **metadata root** of a Merkle tree when the path is recomputed; this is not a physical force or an instantaneous signal between distant sites.
3. **One frame:** define the physical temporal frame as **one application of a specified positive transfer operator**. The freeze → pump → verify → freeze chain is a data-provenance analogy, not a derivation of the Wilson action or a transfer law.
4. **Observable:** if \(\lambda_1\ge\lambda_2\ge\cdots>0\) are eigenvalues on the **full gauge-invariant Hilbert space**, with multiplicities, set \(m_{\rm first}=-\log(\lambda_2/\lambda_1)/a_t\), where \(a_t\) is the *physical temporal spacing*. Do not use an observable's selected decay if it has zero overlap with the actual first excited state.

**Law 70 control, not a Yang–Mills premise.** GitRAM [PR #7](https://github.com/JesseBrown1980/GitRAM/pull/7) constructed a separate 3-state transfer operator with second eigenvalue \((n-1)/n\) and selected \(n=3^k,\ a_t=a_0/n\). It proves \(1/a_0\le m_k\le n/((n-1)a_0)\) for that operator. Here \(a_0\) is an externally chosen reference time, **not assumed to equal an unknown physical correlation time**. That transfer law has not been derived for the interacting gauge operator.

## 1. Operators and units to compare — GPT-6 correction

### 1A. Primary 4D SU(2) Wilson transfer

**Freeze this one as the primary physical comparison**, using the exact convention of [Lemma 0004](LEMMA-0004-REFLECTION-TRANSFER.md), §7, and [YM4-02d](NOTE-YM4-02d-QUANTITATIVE-GAP.md). On a periodic 3D spatial slice with spatial links \(U\), normalized SU(2) Haar integration, and gauge projector \(\mathcal P_G\), let

\[
w_\beta(g)=\exp[-\beta(1-\tfrac12{\rm Re\,Tr}\,g)],\quad
A_{\beta_s}(U)=\prod_{p\ \mathrm{spatial}}w_{\beta_s}(U_p),
\]
\[
B_{\beta_t}(U,V)=\prod_{\ell\ \mathrm{spatial}}w_{\beta_t}(U_\ell V_\ell^{-1}),\qquad
T_W=A_{\beta_s}^{1/2}B_{\beta_t}\mathcal P_G A_{\beta_s}^{1/2}.
\]

Here \(B_{\beta_t}\) is an **integral kernel**, not pointwise multiplication. The gauge projector integrates the gauge transform of \(V\). Use the physical gauge-invariant subspace throughout; do not count gauge-variant modes. The existing lemma establishes reflection/transfer positivity for Wilson weights \(\beta_s,\beta_t>0\) at **fixed** finite lattice and coupling. Its result is the right starting point, not a uniform continuum proof.

The **anisotropic** Wilson couplings \(\beta_s,\beta_t\), spatial spacing \(a_s\), temporal spacing \(a_t\), and any renormalized anisotropy require a declared matching convention. They are *not* all interchangeable. Use \(m_{\rm first}^{W}=-\log(\lambda_2(T_W)/\lambda_1(T_W))/a_t\). For an infinite-volume claim also control the spatial size \(R=L a_s\) as \(R\to\infty\).

### 1B. Separate finite S₃ Hamiltonian/Suzuki–Trotter control

For the finite S₃ controls, use the already specified Hamiltonian

\[
H_{S_3}/J_E=\mathcal E+r\mathcal M,\quad
\mathcal E=\sum_\ell(3I-\sum_{\tau\,{\rm transposition}}L_{\ell,\tau}),\quad
\mathcal M=\sum_p(2-\chi_{\rm std}(U_p)).
\]

Its **separate** symmetric split is

\[
T^{S_3}_{\rm Strang}(a_t)=
e^{-a_tJ_E r\mathcal M/2}
e^{-a_tJ_E\mathcal E}
e^{-a_tJ_E r\mathcal M/2}.
\]

For fixed finite lattice and \(r,J_E\), it is positive and gauge invariant. As \(a_t\to0\), \(-a_t^{-1}\log T^{S_3}_{\rm Strang}=H_{S_3}+O(a_t^2)\); **it is not exactly \(e^{-a_tH}\)**. This makes the controlled small-\(a_t\) limit an independent falsifier.

For \(F=21\) flat orbits on the 3D S₃ torus, keep **two observables**:

\[
m_{\rm first}^{S_3}=-a_t^{-1}\log(\lambda_2/\lambda_1),\qquad
m_{\rm cluster}^{S_3}=-a_t^{-1}\log(\lambda_{F+1}/\lambda_F).
\]

They converge for fixed lattice and fixed couplings to \(J_E(e_2-e_1)\) and \(J_E(e_{F+1}-e_F)\), respectively. Do **not** transfer the fixed integer \(F=21\) to SU(2); there is no analogous finite flat-cluster count there.

### 1C. Refinement, coupling and physical units

For spatial refinement index \(k\), set \(L_k=3^kL_0,\ a_{s,k}=a_{s,0}/3^k\) so the initial physical side \(R=L_ka_{s,k}\) remains fixed. Keep \(a_{t,k}\) separately specified (e.g. fixed anisotropy \(a_s/a_t\) after calibration).

In **standard 3+1D Kogut–Susskind SU(2) conventions**, the continuous-group Hamiltonian has \(J_E=c_Eg^2/a_s\) and \(J_B=c_B/(g^2a_s)\), with positive constants \(c_E,c_B\) determined by the precise definitions. Thus \(r=J_B/J_E=(c_B/c_E)g^{-4}\) **for that matched SU(2) Hamiltonian**. S₃ has no matching Lie algebra/Casimir normalization, so the \(r\) in \(H_{S_3}\) is an independent simulation coupling until a map is derived. **Do not extrapolate S₃ \(r\)-rows as a bare-SU(2) renormalization trajectory.**

The S₃ magnetic minimum \(\kappa=\min(8,3L_{\min})\) is a **classical diagnostic** from YM4-06A, not a spectral mass or an independently adjustable SU(2) alphabet resolution.

## 2. Rows for eventual pre-run freeze (revised)

### A. Time refinement controls — finite, fixed spatial lattice

| Row | Test | Status and falsifier |
|---|---|---|
| A1 | For fixed S₃ \(L,r,J_E\), \(n=3^k,\ a_t=a_0/n\): \(n[1-\lambda_2(T^{S_3})/\lambda_1(T^{S_3})]\to a_0J_E(e_2-e_1)\). Independently the logarithmic mass tends to \(J_E(e_2-e_1)\). | **DERIVED** from finite-dimensional Strang consistency. Falsify by a persistent discrepancy from independently bounded Hamiltonian levels. Not an exact Law 70 ratio at finite \(k\). |
| A2 | Replace \(\lambda_2/\lambda_1\) by \(\lambda_{22}/\lambda_{21}\) and \(e_2-e_1\) by \(e_{22}-e_{21}\). | **DERIVED**, same caveat. Keep a separate spectral enclosure. |
| A3 | In the *constructed Law 70 transfer*, retaining \(\lambda_n=(n-1)/n\) while holding \(a_t=a_0\) makes \(m_n\to0\). | **DERIVED**, negative toy control; it says nothing by itself about Wilson SU(2). |
| A4 | For the Wilson operator, compare its anisotropic transfer spectrum to a separately declared Hamiltonian continuum-time limit, **not** to an assumed S₃-to-SU(2) parameter identity. | **OPEN** matching requirement; discrepancy falsifies the chosen matching. |

### B. Unequal temporal slicing: an error-control test, not Law 70 population physics

At a fixed finite S₃ Hamiltonian set \(b=a_0/n\). Compare two equal Strang steps \(P_{\rm eq}=T_b^2\) to the **defined** symmetric unequal block \(P_{\rm un}=T_{3b/2}^{1/2}T_{b/2}T_{3b/2}^{1/2}\). Both have leading generator \(-2bH\), although \(T_h^{1/2}\ne T_{h/2}\) for finite \(h\). Read masses per **total clock time \(2b\)**.

| Row | Test | Status and falsifier |
|---|---|---|
| B1 | Under a nonzero leading second-order mass error and the appropriate symmetric-composition BCH expansion, test whether \([m_{\rm un}-\Delta]/[m_{\rm eq}-\Delta]\to7/4\), since \(((3/2)^3+(1/2)^3)/2=7/4\). | **CONJECTURE pending an explicit BCH derivation** and nonzero-denominator gate. A zero leading coefficient makes this ratio undefined, not a failure. |
| B2 | Measure the sign of \(m_{\rm un}-m_{\rm eq}\); allow either sign. | **OPEN**, prediction direction not supplied. Law 70's unequal **population** observation is not a derivation of this temporal-step sign. |

### C. Space/time and representation refinement — the decisive physics rows

| Row | Refined claim | Status and falsifier |
|---|---|---|
| C0 | Record the full trajectory \((a_{s,k},a_{t,k},L_k,\beta_{s,k},\beta_{t,k})\), with SU(2) physical scale/anisotropy setting independent of the measured gap. Keep S₃ \(r,J_E\) as independent controls. | **REQUIRED BEFORE FREEZE.** Kogut–Susskind \(g^2/a_s\) versus \(1/(g^2a_s)\) scaling is NAMED and convention-checked; **no S₃ map is implied**. |
| C1 | With a fixed finite group S₃ and a specifically chosen \(r_k,J_{E,k},L_k\), test whether \(m_{\rm cluster}\) grows without bound. | **CONJECTURE, trajectory-dependent.** It is **not** a theorem for every fixed finite alphabet; \(\kappa\) alone does not imply a gap. |
| C2 | For **any** transfer spectrum, a nonzero finite limiting mass \(m\) requires \(-\log(\lambda_2/\lambda_1)=a_t m+o(a_t)\), or equivalently \(1-\lambda_2/\lambda_1=a_tm+o(a_t)\). For the distinct S₃ cluster ratio use \(\lambda_{22}/\lambda_{21}\). | **DERIVED spectral requirement.** It does **not** require classical \(\kappa_k\sim3^{-k}\) or a changing trit symbol set. |
| C3 | **Concrete candidate for the operator's “fixed ternary symbols, more structure at each level”:** retain the digits \((-1,0,+1)\) for coding, and use the SU(2) Peter–Weyl representation cutoff \(q_k=3^k,\ j_{\max,k}=(q_k-1)/2\). On each link keep matrix-coefficient irreps \(j\le j_{\max,k}\), dimension \(d_k=\sum_{d=1}^{q_k}d^2=q_k(q_k+1)(2q_k+1)/6\), encoded in enough trits. | **PROPOSED DEFINITION, NOT AN ATTRIBUTED USER CHOICE OR A FROZEN PREDICTION.** The cutoff projector commutes with left/right gauge transformations; test projected-transfer positivity, gauge covariance, tail error and recovery as \(q_k\to\infty\). |
| C4 | On the gauge-invariant truncated SU(2) space, examine \(T_{W,k}^{(q)}=P_{q_k}T_{W,k}P_{q_k}\). Require errors between its first physical spectral ratios and the untruncated Wilson operator to be bounded independently of the measured gap. | **OPEN** quantitative cutoff/volume/spacing bounds. Projection preserves positivity and gauge symmetry, but locality and the continuum theory are **not proved** by this fact. |
| C5 | Continuous SU(2) has \(\inf_{U:\mathcal M(U)>0}\mathcal M(U)=0\) in the finite spatial geometry of YM4-06A. Therefore no positive **classical** nonflat-cost floor exists. | **DERIVED there.** This neither disproves nor establishes a quantum physical gap; a finite-box transfer bound is not a continuum-mass certificate. |
| C6 | Feed YM4 PR #34's exact counterfamily (positive finite gaps and valid ternary jumps, but vanishing physical gap) into the identical spectral readout. | **MANDATORY CONTROL.** The readout must return \(m_{\rm phys}\to0\). |
| C7 | At a declared SU(2) coupling/spacing trajectory, certify a strictly positive lower bound on \(-\log(\lambda_2/\lambda_1)/a_t\) uniform as \(a_s,a_t\to0\), *including representation truncation error and excited-state visibility*. Then control \(R\to\infty\) and the reconstruction/continuum limit. | **OPEN target.** No C3 representation cutoff, finite S₃ cluster gap, SHA digest or positive single-lattice gap discharges it. |
| C8 | Compare a **separate** family of finite SU(2) subgroup actions with the Wilson SU(2) control at matched finite lattice/coupling, recording any weak-coupling freezing. | **NAMED literature-backed negative control**, not an approximation sequence converging to SU(2). S₃, 2T, 2O, 2I are separate models. |

**Why C3 is a better-defined candidate than finite subgroups.** The Peter–Weyl link spaces form a nested sequence inside \(L^2(SU(2))\); the continuous SU(2) gauge action is preserved at each cutoff, and only the **number of trits needed to encode basis states** grows. For \(q=3,9,27\), the per-link dimensions are \(14,285,6930\) (requiring 3, 6 and 9 trits respectively). This is a finite-dimensional representation truncation, **not a new finite subgroup or a globally injective 256-bit hash**. Existing research notes that subgroup digitizations freeze at weak coupling and representation cutoffs need separate continuum error control.

### D. Lock, residuals and shadow-cat ledger

| Row | Statement | Status and falsifier |
|---|---|---|
| D1 | In S₃, the magnetic multiplication operator preserves flat basis configurations individually. Electric dynamics can connect flat states through nonflat paths. The 2×2×2 fourth-order **large-\(r\)** splitting from GitRAM PR #6 is a candidate effective off-diagonal amplitude; it is not fourth order in temporal frame spacing. | **MEASURED effective finite-model input awaiting independent spectral proof review**. A lower nonzero order in the same expansion falsifies it. |
| D2 | The order-three SH action \(C_0\to C_1\to C_2\to C_0\) and any \(27\to9\to3\to1\) modular residue preservation are ledger identities; a proposed physical SU(2) shadow observable must **independently pass exact local gauge invariance**. | **Existing finite bookkeeping control; physical operator OPEN.** Raw signed S₃ 3-cycle orientation fails gauge invariance under transposition conjugation (YM4 PR #34). |
| D3 | A leaf mutation can change the recomputed Merkle root, while an unmodified distant trit remains unchanged. | **MEASURED GitRAM PR #7 fixture property**, not instantaneous propagation, mass generation or a universal no-collision theorem. |
| D4 | Attach to each spectral row the exact transfer/Hamiltonian source and coupling, eigenvector or interval witness, a **norm residual and enclosure**, gauge projector/sector, temporal spacing, parent hash and shadow derivation. | **REQUIRED ACCEPTANCE.** HBI/HBP/SHA/SH/HASH proves provenance of a claimed residual; the residual bound itself must be mathematically checked. |

## 3. Computational plan and sizing (no execution in this PR)

The exact finite S₃ Burnside formula is \(|G|^{-1}\sum_{g\in G}|C(g)|^{E-V+1}\) on a connected graph. On a periodic 2×2×2 3D lattice \(E-V+1=17\).

| Space/group | Gauge orbit count or cutoff | Planned use |
|---|---:|---|
| 2D 2×2 S₃ | 1,393 | Entire matrix; time-splitting/BCH and shadow operator controls. |
| 3D 2×2×2 \(\mathbb Z_3\) | 129,140,163 | Abelian no-store / sector-controlled comparison; do not call full diagonalization easy. |
| 3D 2×2×2 S₃ | 2,821,153,019,713 | Effective 21-state spectral work and certified matrix-free enclosures in GitRAM PR #6. |
| 3D 2×2×2 Q8 | 562,962,838,323,200 | No full stored spectrum; rational series and no-store bounds. |
| SU(2) representation cutoff | \(d_k=q_k(q_k+1)(2q_k+1)/6\) per link | Gauge-invariant truncated transfers; no claim that full state space fits Host8. |
| 3D spatial \(6^3\) or larger | model dependent | Bounds, blocking and controlled truncations only; not a promised exact whole-spectrum run. |

The ~7-billion-size S₃ *symmetry* subspace and ~59-GB key-table estimate in the earlier draft are only feasibility hypotheses pending an independent exact sector-dimension calculation. Fits-in-300GB does not imply an eigensolver certificate. Host8 can stream bounded slices and their receipts, while matrix laws shorten permitted linear operations; a nonlinear jump needs its own reduction theorem.

Run order **after** the corrections are approved: (i) one isolated HBP prediction-only commit with both observable definitions and negative controls; (ii) 2D S₃ exact operator/time-refinement controls; (iii) fixed 3D S₃ and continuous SU(2) controls; (iv) SU(2) nested representation cutoffs with measured projection errors; (v) a conditional scale-uniform bound attempt with PR #34's vanishing-gap counterfamily. No row is to be silently converted from CONJECTURE or OPEN to DERIVED after seeing a result.

## 4. Resolution of the six reviewer questions

1. **Transfer:** Wilson/Lemma 0004 on gauge-invariant SU(2) is primary. The symmetric S₃ Strang split is a separate finite-model control.
2. **Coupling:** the \(g^2/a_s,\ 1/(g^2a_s)\) convention applies to an explicitly normalized SU(2) Kogut–Susskind Hamiltonian. S₃ \(r,J_E\) remain independent until a derived matching map exists.
3. **Growing state space:** adopt **as a candidate for operator approval** the nested SU(2) Peter–Weyl cutoff \(q_k=3^k\) while the underlying digital symbols remain ternary. No finite SU(2) subgroup sequence is asserted to converge to the group.
4. **Signs:** B1 needs a BCH coefficient and nonzero denominator; B2 and finite-volume C1/C4 gap directions remain genuinely refutable/open. No unsupported direction is attributed to Law 70.
5. **Fixed versus refining:** **fixed three-symbol encoding and a growing number of trits/basis states are compatible**, so the binary choice is false. A *fixed finite physical S₃ gauge group* remains a distinct negative/control lane.
6. **SH:** include sector and local-gauge witness, level/clock, C0/C1/C2 phase, immutable parent/derived hashes, source operator/couplings, eigenvalue/residual proof links, and an explicit tag distinguishing physical observables from metadata. SH does not change the dynamics.

## 5. Scope and references

The preceding definitions make the problem **testable**; they do not establish the Wilson transfer-spectrum scaling, the reconstructed continuum theory, a positive 4D infinite-volume Yang–Mills mass gap, or instantaneous physical signaling. They preserve the r=9 freeze separately.

Repository inputs: [Lemma 0004](LEMMA-0004-REFLECTION-TRANSFER.md), [YM4-02d](NOTE-YM4-02d-QUANTITATIVE-GAP.md), [YM4-03 blocking](NOTE-YM4-03-ONE-SCALE-BLOCKING.md), [YM4-06A](NOTE-YM4-06A-GLOBAL-LOCK-20261110.md), [counterfamily PR #34](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/34), [finite 3D spectral GitRAM PR #6](https://github.com/JesseBrown1980/GitRAM/pull/6), [Law 70 transfer GitRAM PR #7](https://github.com/JesseBrown1980/GitRAM/pull/7).

External convention and control sources (background, not a substitute for the repo proofs): Kogut–Susskind, *Phys. Rev. D* **11** (1975) 395; Hartung et al., *Digitising SU(2) gauge fields and the freezing transition*, *Eur. Phys. J. C* **82** (2022) 237; *Quantum simulation of lattice gauge theories in more than one space dimension—requirements, challenges and methods*, *Phil. Trans. R. Soc. A* (2022), representation cutoff section.

**NO PREDICTION FROZEN. NO YM4-06D RUN. NO 4D MASS-GAP CLAIM.**
