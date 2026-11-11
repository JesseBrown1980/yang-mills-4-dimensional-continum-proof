# YM4-04C E4/E5 — all-step contraction, independent checks, G0/G1 gate and weak-coupling barrier

**2026-11-11.** This is a staged proof-and-verification record, not a continuum Yang–Mills existence or mass-gap theorem. The original YM4-04C first 42 frozen prediction rows (commit \`6ebf63272ae230bfb08ef48b3156cb4202c24627\`, SHA256 \`c74e6388295a6309674268dd18deba3728a4eb627a1530c42054182b2fadc404\`) remain untouched. The new stage E4/E5 prediction was filed **before new verification code** as \`docs/PREDICTION-YM4-04C-E4-E5-20261111.hbp\` at commit \`70cceac39ef08bdee88a75bca82b9a9867502a97\`.

## 1. Exact G1 one-step coefficient and all-step implication

Write \(\kappa=1/4\), \(\delta'=\delta e^\delta\), and
\[
 \lambda(\delta)=\delta'+\log(1+\delta').
\]
For \(0<\delta\le\delta_{\rm crit}\) with \(\lambda(\delta_{\rm crit})=\kappa\), the frozen coefficient is
\[
 c_{\rm fin}(\delta)=\max\left\{
  e^{-4\kappa},\
  e^{\delta+\lambda(\delta)-5\kappa},\
  e^{\delta-\kappa/2}\sup_{f\in\mathbb Z,\ f\ge4}
    \left(e^{-(\kappa-\lambda(\delta))f}-e^{-\kappa f}\right)
 \right\}.
\]
The exact C13 bracket is \(0.114846768<\delta_{\rm crit}<0.114846769<1/8\). The second entry is at most \(e^{\delta-4\kappa}=e^{\delta-1}<1\) and the third is at most \(e^{\delta-\kappa/2}<1\); the first is \(e^{-1}<1\). Thus **without evaluating a finite sample of steps**, \(0<c_{\rm fin}(\delta)<1\) on the whole admissible domain. Every entry is nondecreasing in \(\delta\): \(\lambda(\delta)\) is increasing, each \(f\)-term is increasing, and positive products, suprema and maxima preserve monotonicity.

The **mathematical induction statement**, conditional on the G1 implication \(H_k(\kappa,\delta)\Rightarrow H_{k+1}(\kappa,c_{\rm fin}(\delta)\delta)\), is: if \(\lambda(\delta_1)\le\kappa\), let \(q=c_{\rm fin}(\delta_1)<1\). Then for every **integer step** \(1\le j\le K\),
\[
 \boxed{\delta_j\le q^{j-1}\delta_1,\qquad
   \sum_{j=1}^K\delta_j\le\frac{\delta_1}{1-q}.}
\]
Proof: assuming \(\delta_j\le\delta_1\), monotonicity gives \(\lambda(\delta_j)\le\kappa\) and \(c_{\rm fin}(\delta_j)\le q\), so G1 implies \(\delta_{j+1}\le q\delta_j\). The base case is \(j=1\). Sum the geometric bounds. **This is a proof for all finite j from the G1 theorem, not extrapolation from the number of numerical steps executed.** Uniformity in lattice size is inherited from G1's hypotheses; the numerical test alone cannot establish that uniformity.

The first engine uses 256-bit strictly outward-rounded integer interval arithmetic and an *actual integer-\(f\) supremum*, with a certified tail stopping rule: for every \(j>f\), its candidate term is at most \(e^{-(\kappa-\lambda^+)j}\le e^{-(\kappa-\lambda^+)(f+1)}\). Once that upper bound is below the observed best lower interval bound, the maximum is certified. It confirms \(f=9\) uniquely at \(\delta=1/10\), \(c_{\rm fin}\in(0.611173,0.611174)\), and \(f=13\) at \(\delta=11/100\), \(c_{\rm fin}\in(0.811310,0.811311)\). The exact flattening transition at \(0.078733761/0.078733762\) is also reproduced. The source-disjoint second checker uses the **pre-existing** independent council 640-bit libraries \`ilib.py\`, \`polylib.py\`, \`g1lib.py\`, whose \(f\)-tail implementation is different.

All frozen first-step \(c_{\rm fin}=e^{-1}\) readouts reproduced:

| Frozen | β | Head | δ₁ | δ₂ bound | Σδ bound |
|---|---|---|---|---|---|
| C07 | 0.01 | crude | 0.0055222253387… | 0.0020316 | 0.008737 |
| C08 | 0.01 | C03 | 0.0000047159850… | 0.0000017350 | 0.000007461 |
| C11 | 1/64 | crude | 0.0508265220700… | 0.018699 | 0.08041 |
| C12 | 0.02 | C03 | 0.0363235365281… | 0.013363 | 0.057463 |
| C14 | 1/64 | C03 | 0.001017385572… | 0.00037428 | 0.0016095 |

C13 crude self-map at 0.01767 is MET and at 0.01768 is NOT_MET. C14 refined at 0.02074 is MET and at 0.02075 is NOT_MET. The C16 20-scale, **fixed final \(4^4\)-torus**, bounds are \(\delta_{20}\le3.0940\times10^{-11}\) and \(\operatorname{osc}\log\rho_{20}\le5.828\times10^{-9}\). These are bounds on an effective action within the controlled strong-coupling family; they are not a measured physical mass or continuum spectrum. The first E4 checker directly tests the exact frozen integer thresholds; the second independently recomputes them.

## 2. G0/G1 independent proof gate: scoped project acceptance

The **independent second-seat G-attack** [PR #46](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/46) on the original freeze reports all **7/7 frozen acceptance checks and 62/62 lemma/remark steps REPRODUCED**, **0 refutations** and **0 unresolved steps**. The council checked the \((1+t)^f\) tree-graph step, the root \(m\ge1\) restriction, named integer constants, and planted faults. See \`reviews/opus55-ym4-04c-g-attack/filing/GATTACK-REPORT.md\`. The separately implemented E0, E1/C03, E3 and current E4/E5 checks now independently reproduce additional claimed arithmetic and finite combinatorics.

**Disposition under the frozen project's G_attack rules:** G0 and G1 satisfy their *internal mathematical review conditions*, once the two text completions below are applied. This does **not** convert imported results into formally verified proofs or prove applicability beyond the theorems' explicit assumptions. The mathematical statements are conditional implications from the stated hypotheses; any unverified assumption, such as actual initial control along a proposed physical weak-coupling trajectory, remains open.

Two minor defects in the G-attack were corrected **in the note text**, with no alteration to the original 42 frozen rows or any constant:

1. **K1 (object count):** replace the ambiguous \`#Γ≥2\` in Lemma 4.12 item 2 and Proposition 4.15's three-case decomposition and \(S_3\) with **\(\Gamma\ne\{o\}\)**. This is the object-count condition required for the tree-graph root decomposition, rather than the different size weight later denoted \(\#\Gamma=(1/2)\#\mathrm{line}(\Gamma)\).
2. **K2 (initial flat rate):** complete Lemma 4.19's proof. As \(\delta\downarrow0\), the second candidate tends to \(e^{-5\kappa}<e^{-4\kappa}\); for \(\lambda<\kappa/2\), the third candidate is at most \(e^{\delta-\kappa/2}\lambda/[e(\kappa-\lambda)]\to0\), because \(e^{-(\kappa-\lambda)f}-e^{-\kappa f}\le\lambda f e^{-(\kappa-\lambda)f}\) and \(\sup_{f\ge0}f e^{-(\kappa-\lambda)f}=1/[e(\kappa-\lambda)]\). Thus \(c_{\rm fin}=e^{-4\kappa}\) on a nonempty initial interval.

**Still imported/named, not machine-formally proved here:** Finner's generalized Hölder, the connected-graph exponential formula, Kotecký–Preiss cluster bounds, the full input action hypotheses, and the SU(2) Haar/Weyl integration formula. The independent council's re-derivation supports their use, but the hosted tests verify finite arithmetic and toy instances, not every measure-theoretic hypothesis. Do not assert scientific publication, Clay acceptance, or an unconditional Yang–Mills theorem.

## 3. E5 C15: exact six frozen Wilson norm/pole controls

On the unit-quaternion SU(2) sphere with normalized Haar measure, put \(a(U)=\tfrac12\operatorname{ReTr}U\in[-1,1]\),
\(c_0(\beta)=\int e^{\beta a(U)}dU\), and
\(\varepsilon_6(\beta)=\|e^{\beta a}/c_0(\beta)-1\|_{L^6}\). The fixed **Fuss–Catalan** tail has pole criterion \(\mu e^{1/4}\varepsilon_6(\beta)<1\) even at \(\alpha=0,\theta=\kappa\). The two arithmetic routes re-evaluate the exact Bessel/Haar six-moment formula with outward enclosures and reproduce:

| β | Frozen \(\mu e^{1/4}\varepsilon_6\) | Result for this C0 certificate |
|---|---:|---|
| 1/45 | (0.9888, 0.9889) | Below pole, but headfree \(n_{\max}=10\) still NOT_MET |
| 1/40 | (1.1125, 1.1126) | Above pole; NOT_MET |
| 1/18 | (2.473, 2.474) | Above pole; NOT_MET |
| 1/10 | (4.4575, 4.4576) | Above pole; NOT_MET |
| 1 | (50.40, 50.41) | Above pole; NOT_MET |
| 4 | (292.4, 292.5) | Above pole; NOT_MET |

At β=4, \(\varepsilon_6>1\), so the E5 engine uses a mathematically unbounded integer sixth-root interval helper rather than E3's earlier bisection precondition \(\varepsilon_6\le1\).

## 4. **New all-large-β obstruction to this particular certificate**

The following is an analytical inequality **for every β≥36**, not a finite-sampling extrapolation, and makes no assumption of monotonicity of \(\varepsilon_6(\beta)\).

Using the normalized SU(2) Haar formula \(c_0(b)=\frac2\pi\int_0^\pi e^{b\cos\theta}\sin^2\theta\,d\theta\) and the inequalities on \(0\le\theta\le\pi\)
\[
1-\cos\theta=2\sin^2(\theta/2)\ge\frac{2\theta^2}{\pi^2},
\qquad
\sin\theta\le\theta,
\]
the Gaussian integral yields for all \(b>0\)
\[
 c_0(b)\le\frac{\pi^{5/2}}{2^{5/2}}e^b b^{-3/2}
       <6e^b b^{-3/2}
\]
because \(\pi<4\) and \(2^{5/2}<6\).

For \(b\ge1\), integrate \(c_0(6b)\) only over \(0\le\theta\le1/\sqrt{6b}<\pi/2\). The bounds \(\cos\theta\ge1-\theta^2/2\), \(\sin\theta\ge2\theta/\pi\), \(e^{-1/2}>1/2\), \(\pi<4\) and \(6^{3/2}<15\) give
\[
 c_0(6b)\ge\frac{8e^{-1/2}}{3\pi^3(6b)^{3/2}}e^{6b}
           >\frac{e^{6b}}{720\,b^{3/2}}.
\]

Write \(X_b=e^{ba}/c_0(b)\), a probability-density random variable under Haar. Hence for every \(b\ge1\)
\[
 \|X_b\|_6^6=\frac{c_0(6b)}{c_0(b)^6}
 > \frac{b^{15/2}}{720\cdot6^6}
 \ge\frac{b^6}{720\cdot6^6}
 >\left(\frac{b}{18}\right)^6
\]
since \(720<3^6=729\). The reverse triangle inequality \(\|X_b-1\|_6\ge\|X_b\|_6-1\) gives
\[
 \boxed{\varepsilon_6(b)>b/18-1\ge1
      \quad\text{for all }b\ge36.}
\]
Therefore \(\mu e^{1/4}\varepsilon_6(b)>1\) for every \(b\ge36\), and the fixed-\(\mu\) \(F_{20}\)-tail KP certificate **cannot** produce a valid step-0 bound along any trajectory with bare \(b\to\infty\), irrespective of its finite head length. This is a **proof-method obstruction, not a proof that continuum SU(2) Yang–Mills has no positive gap**.

A different analytic approach must establish its own shrinking-spacing, increasing-coupling estimates and a physical gauge-invariant transfer spectral inequality \(-\log(\lambda_2/\lambda_1)/a_t\ge m_*>0\) with continuum and infinite-volume control. Neither the matrix laws nor HBI/HBP/SHA/SH/HASH commitments supply that bridge by themselves.

## 5. Integrity, tests, remaining research

- Prediction-only commit before code: \`70cceac3\`; six frozen C15 rows and new \(b\ge36\) analytic barrier named in it.
- Hosted native Python both routes: independent 256-bit engine and pre-existing 640-bit second-seat library, source no-float gate; 5/5 planted faults (wrong G0 factor, wrong maximizing f, missing 19 steps, missing pole guard, false weak-pass) must fail.
- Three source receipts \`ENGINE.hbp\`, \`SECOND.hbp\`, \`SHA256SUMS\` are immutable after acceptance; final-head CI must regenerate them byte-for-byte. The SHA commitments are data integrity only, not instantaneous physical causation.
- The inherited \`no-float-list-unchanged\` **human review FAILURE** from stacked YM4-04C evidence-list PR #45/#46 is not bypassed. No merge without resolving it on its own merits.
- The original full YM4-04C E0–E9/W12-fault release remains incomplete. In particular E6 gauge integrals, W-lane scale comparison, a native Rust independent complete checker and a **genuine weak-coupling continuum construction** are OPEN.
- The unrelated finite S₃ frozen \(r=9\) one-shot and Finite PR #160 remain untouched.

**Release recommendation:** ACCEPT E4 and E5 finite arithmetic; ACCEPT G0/G1 as *scoped internal project implications with the G_attack review and K1/K2 repairs*; HOLD formal external-input audit and every weak-coupling/continuum/mass-gap claim; KEEP this PR DRAFT.
