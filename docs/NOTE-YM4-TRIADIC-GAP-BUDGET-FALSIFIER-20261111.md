# YM4-06B — the PR #34 counterfamily must FAIL the triadic physical-gap error budget

**Date:** November 11, 2026. **Status:** explicit algebraic falsification of an incorrectly interpreted sufficient condition. This is a rigorous two-level transfer-operator toy theorem, **not** a proof of weak-coupling 4D SU(2) spectral control.

**Motivation:** PR #34 already warned that a small raw block defect `|q_j^3-q_(j-1)| <= 6 a_j^2` does not keep the first physical gap open. The later proposed certificate
[
\gamma_{k+1}\ge \gamma_k/3-\varepsilon_k,quad
a_{k+1}=a_k/3,quad
\sum_{k\ge0}\varepsilon_k/a_{k+1}<m_0,
\qquad m_k:=\gamma_k/a_k
]
is algebraically sound but must reject that family. **It does reject it.** A separate 11-row prediction file was frozen at commit `66e797cc671c12aa452a878a4d7f84979ce28eb9` before the independent test implementation.

## 1. Correct quantity: first-gap log defect, not a raw matrix-entry difference

For the genuine physical first excitation, put `q_k=lambda_1(T_k)/lambda_0(T_k)`, `gamma_k=-ln q_k` and `m_k=gamma_k/a_k`. **No predetermined visible mode can be substituted for lambda_1.**

The smallest nonnegative error that makes the one-step inequality true is

[
\varepsilon_k^{\min}
=\max\{0,\;\gamma_k/3-\gamma_{k+1}\}.
\tag{G1}
]

If these errors are independently bounded by a sequence `b_k` with `sum b_k/a_(k+1)<m_0`, then the full first physical gap remains bounded below by a strictly positive number. This is a **conditional sufficient criterion** and not an existence theorem for a scale-blocking operator.

One cannot replace `epsilon_k` with `|q_(k+1)^3-q_k|` without a proof converting that raw error to a **log first-gap error** and preserving the physical operator's complete vacuum complement.

## 2. PR #34's two-state collapsing family: exact failure of strict budget

For all integers `k>=0`, take

[
a_k=3^{-k},\qquad
T_k=\operatorname{diag}(1,q_k),\qquad
q_k=\frac{1}{1+a_k^2}=\frac{3^{2k}}{3^{2k}+1}.
]

The first physical gap is

[
m_k=3^k\ln(1+3^{-2k}),\qquad
0<m_k\le3^{-k}\longrightarrow0.
\tag{G2}
]

Let `x=a_(k+1)^2`. Then `0<x<=1/9` and

[
q_{k+1}^3-q_k
=\frac{6x-3x^2-x^3}{(1+x)^3(1+9x)}
\in(0,6x).
\tag{G3}
]

Thus the **raw eigenvalue defect really is O(a_(k+1)^2)** and matches the counterfamily's published small-defect statement. But because `q_(k+1)^3>q_k`, the minimum logarithmic first-gap defect is **strictly positive**:

[
\varepsilon_k^{\min}
=\frac13\ln\left(\frac{q_{k+1}^3}{q_k}\right)
=\frac13\ln\left(\frac{1+9x}{(1+x)^3}\right)>0.
\tag{G4}
]

Divide by the **finer** `a_(k+1)=a_k/3` and sum. For any `K>=1` the weighted errors telescope:

[
\sum_{k=0}^{K-1}\frac{\varepsilon_k^{\min}}{a_{k+1}}
=\sum_{k=0}^{K-1}(m_k-m_{k+1})
=m_0-m_K.
\tag{G5}
]

Equivalently, the logarithms may be avoided completely with the **exact rational** product identity

[
\prod_{j=1}^{K}
\left(\frac{q_j^3}{q_{j-1}}\right)^{3^{j-1}}
=\frac{q_K^{3^K}}{q_0}.
\tag{G6}
]

The independent integer-only checker validates (G3) and (G6), with complete rational arithmetic at `K=1,...,6`; the proof establishes every `K`. From (G2), `m_K ->0`, so (G5) yields

[
\boxed{
\sum_{k=0}^{\infty}\frac{\varepsilon_k^{\min}}{a_{k+1}}
=m_0=\ln2.
}
\tag{G7}
]

**Verdict: REJECT.** The required **strict** inequality `sum epsilon_k/a_(k+1)<m_0` fails by equality. Larger purported upper bounds `epsilon_k>=epsilon_k^min` cannot rescue it. It is therefore consistent that `sum a_k` and `sum epsilon_k/a_(k+1)` both converge, yet the physical gap vanishes.

A further elementary point makes the distinction operational. Since `q_k>=1/2`, `ln(1+t)<=t`, and `D_j=q_j^3-q_(j-1)<=6 a_j^2`,

[
\frac{\varepsilon_{j-1}^{\min}}{a_j}
=\frac{\ln(1+D_j/q_{j-1})}{3a_j}
\le\frac{2D_j}{3a_j}\le4a_j.
]

The corresponding conservative total bound is `sum_(j>=1) 4 a_j=2`, which is **finite** but **larger** than `m_0=ln2`. Thus simply observing `O(a^2)` raw defects cannot discharge the positive-margin gate.

## 3. Correct positive control

For PR #34's stable family, take `q_k=1/(1+a_k)`. With `x=a_(k+1)>0`,

[
\frac{q_{k+1}^3}{q_k}
=\frac{1+3x}{(1+x)^3}<1,
]

so `gamma_(k+1)>gamma_k/3` and **`epsilon_k^min=0` for every k**. Its physical gap increases from `m_0=ln2` toward 1, so the strict-budget criterion passes with positive margin. The checker tests this by exact rational comparisons.

## 4. Three-state dark-excitation control

Let

[
T_k=\operatorname{diag}(1,q_k^{\rm dark},q_k^{\rm visible}),\quad
q_k^{\rm dark}=\frac1{1+a_k^2},\quad
q_k^{\rm visible}=\frac1{1+a_k}.
]

For `k>=1`, `q_k^dark>q_k^visible`. The **true** first excitation is dark and has `m_k->0`; the visible excitation has a stable physical decay scale and individually passes with `epsilon=0`. Consequently a theorem established only for the chosen Wilson/Shadow-Cat observable, a numerical Ritz sector, or a high-cluster gap must be marked **INSUFFICIENT**, even when the observed sector passes the budget. No conserved label or exact jump can turn that particular-observable bound into a complete physical gap.

The first-gap algebraic condition itself does **not** require a one-to-one identification of eigenvectors between scales if it is proved directly for the true `lambda_1/lambda_0` at every scale. It is any **derivation from a particular retained operator or subspace** that must certify full spectral coverage, vacuum uniqueness and gauge invariance.

## 5. Acceptance gate before adopting the certificate for 4D SU(2)

1. **Falsifier must fail:** PR #34 family B is tagged `FAIL_STRICT_BUDGET`, despite `D=O(a^2)`, with (G7) stated explicitly. The positive family A is `PASS`. The three-state visible-only control is `REJECT_UNSEEN_DARK`.
2. **Full physical spectrum:** identify `T_k` on the gauge-invariant Hilbert space, simple vacuum, and `lambda_1(T_k)` for the **whole vacuum orthogonal complement**, or an equivalent spectral projection/order theorem. If a numerical certificate concerns only one sector, prove the complementary-sector lower bound.
3. **Independent errors:** prove a bound `epsilon_k<=b_k` from the actual four-dimensional gauge-equivariant block/transfer comparison, without defining `b_k` from the unknown fine-scale first gap or presuming the desired continuum result.
4. **Physical units:** fix and track the temporal lattice spacing, not merely the exponent in a matrix jump. No time cubing identity is a spatial continuum refinement theorem.
5. **Total strict margin and reconstruction:** prove `sum b_k/a_(k+1)<m_0` with an explicit positive margin, plus a nontrivial continuum and the required reconstruction axioms. A convergent error series by itself is insufficient.

**Note about proof strength:** when `epsilon_k` is defined from the exact gaps as in (G1), the telescoping identity makes the criterion a restatement of a positive remaining gap in monotone-gap examples. A proof gains power only when `b_k` is obtained independently from an actual gauge-theoretic operator comparison. That is the major **OPEN** theorem.

## 6. Review boundaries and provenance

This new gate is a separate document and exact checker **based on main**, independent of PR #34's branch and the unrelated draft #64. It does not change PR #34, #33, the finite repository, the round-4 floor rehearsals, or the r=9 launch. All physical-gap, 4D weak-coupling and OS continuum statements remain **OPEN**.
