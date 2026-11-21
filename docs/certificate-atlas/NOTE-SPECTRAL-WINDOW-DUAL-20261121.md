# YM4-SW01 — exact positive-measure dual certificate for physical Wilson spectral windows

**21 November 2026.** The [frozen integer predictions](PREDICT-SPECTRAL-WINDOW-DUAL-20261121.hbp) were committed at `9d0e6a791de88d6d87bb770b6046b46c66557012`, **before** its independent exact checker. This note provides an analytically proven finite-dimensional **dual-polynomial witness** for extracting a *positive lower bound on Wilson spectral weight in a physical transfer-energy window* from certified Euclidean moments. It is compatible with the original 4D continuous-SU(2) transfer and Wilson source normalization, but the current 4D numerical moments are still missing.

## 1. Precise physical spectral measure

Let \(T_{\rm phys}\) be the **gauge-invariant positive, compact** original Wilson transfer on the finite-volume physical OS Hilbert space, with simple vacuum Perron eigenvalue \(\lambda_0>0\), normalized vacuum \(\Omega\), and \(S=T_{\rm phys}/\lambda_0\). Then \(S\) is a positive contraction, \(0\le S\le I\), and \(S\Omega=\Omega\).

For a bounded, real, **gauge-invariant** spatial Wilson operator \(F\), put
\[
 m=\langle\Omega,F\Omega\rangle,\qquad
 u=(F-m)\Omega \perp\Omega,\qquad
 C_n=\langle u,S^n u\rangle\quad(n\in\mathbb N_0).
\]
These are **vacuum-connected, physically normalized** Euclidean Wilson moments at separations \(na\), not raw unnormalized \(T^n\) moments. By the spectral theorem, there is a positive finite measure \(\nu\) supported in \([0,1]\), with
\[
 C_n=\int_{[0,1]}t^n\,d\nu(t),\quad C_0=\nu([0,1]),\quad \nu(\{1\})=0
\]
when the vacuum is simple. For an eigenstate \(j\ge1\), the atomic weight is
\(w_j=|\langle j|u\rangle|^2\) at \(t_j=\lambda_j/\lambda_0=e^{-aE_j}\). For a continuous spectrum in a later limit the same positive-measure argument applies whenever the spectral measure exists and is appropriately bounded.

## 2. Exact dual polynomial lower certificate

Fix rational \(0<q<1\) and positive integer \(n\). The polynomial
\[
 p_{q,n}(t)=\frac{t^n-q^n}{1-q^n}
\]
is **nonpositive on** \(0\le t\le q\), and **at most 1** on \(q<t\le1\). Thus, pointwise on the entire spectral domain,
\[
 \mathbf 1_{(q,1]}(t)\ge p_{q,n}(t).
\]
Integrating against the *positive* physical Wilson spectral measure gives the **exact, certified lower bound**
\[
 \boxed{\quad \nu((q,1])\ge
 \max\left\{0,\frac{C_n-q^n C_0}{1-q^n}\right\}.\quad}
\]
This is a constructive feasible **dual polynomial witness**: its pointwise sign is the proof, and the inequality is an exact positive-measure consequence, not a truncated-moment numerical inversion.

For interval-certified data \(C_n\ge\underline C_n\), \(C_0\le\overline C_0\), the same witness gives
\[
 \boxed{\quad \nu((q,1])\ge
 \max\left\{0,\frac{\underline C_n-q^n\overline C_0}{1-q^n}\right\}.\quad}
\]
This remains rigorous if the data are obtained from our original 4D Wilson certificate with certified **physical** transfer normalization, source-centering and Fourier/operator truncation errors. In the \(\beta=64\) YM4-07I2 framework, the four-step connected Wilson comparison error \(\epsilon_4<1/50000\) is one possible component of the moment interval; the exact **computed** approximate moment is still OPEN, and the \(C_0\) error budget must be certified separately.

The energy cutoff is \(t>q \Longleftrightarrow E<-\log(q)/a\). Hence the formula certifies **total Wilson spectral weight below an energy threshold**. A bound on **one specified first excited state** requires a **separate verified rank-one spectral projector** for the only Wilson-coupled eigenspace in \((q,1)\), plus proof that its energy is the *first physical nonvacuum energy* rather than merely the first excitation seen by this Wilson source. Degenerate eigenspaces carry aggregated projector weight, not the weight of an individual eigenvector. The current exact checker has **no isolation proof object and refuses first-eigenstate promotion even when a caller asserts an isolation flag**. Its output is exclusively the total weight in the energy window.

## 3. Prediction-first exact rational calibration

The independent *toy spectral-measure fixture*
\[
 \nu=\tfrac14\delta_{1/2}+\tfrac34\delta_{1/4},\quad
 C_0=1,\ C_2=7/64,\ C_4=19/1024
\]
represents a positive spectral measure, **not a computed SU(2) 4D Wilson spectrum**. At the chosen threshold \(q=1/3\), the dual witness at moment power \(n=2\) produces **HOLD** because \(7/64<1/9\). At \(n=4\), the same positive fixture produces the exact strict lower bound
\[
 \frac{19/1024-1/81}{1-1/81}=\boxed{\frac{103}{16384}}>0,
\]
while its actual low-energy-window weight is \(1/4\). The dual is conservative but valid.

If independently certified source and fourth-moment intervals satisfy
\[
 C_4\ge19/1024-1/1000,\qquad C_0\le1+1/1000,
\]
the robust integer-only certificate still gives
\[
 \boxed{\nu((1/3,1])\ge\frac{53879}{10240000}>0.}
\]
At \(q=1/2\), the same fourth moment does **not** certify a positive window: the un-clipped dual expression equals \(-3/64\), and the nonnegative lower bound becomes zero (**HOLD**).

## 4. External certificates and compatibility

- [Abbott et al., *Causal bootstrap: Bounding smeared spectral functions from nonperturbative Euclidean data*, PRD 114 (2026) 074510](https://doi.org/10.1103/m9kj-y6t3) develops more flexible spectral-kernel/semidefinite dual constructions. Our one-polynomial feasible witness is derived **independently** from positivity, not claimed as a direct imported theorem or the full published dual program.
- [*Kernel transformations and bounds for smeared spectral functions*, PRD 114 (2026) 094510](https://doi.org/10.1103/f4h2-pg8m) offers additional methods to change the target energy smearing. A general new kernel requires an **independently verified pointwise or interval dual inequality**, not unverified numerical optimization.
- The [4D YM4-07I2 connected physical Wilson comparison](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/blob/ed6851e499c98e351816e9134d15d52e500f2577/docs/NOTE-YM4-07I-FINITE-4D-SU2-PHYSICAL-VACUUM-PROJECTOR-20261121.md) supplies one strict error envelope at finite volume and \(\beta=64\), while its physical connected moment value remains OPEN in the current research.
- A proposed multi-window dual certificate must carry its **positive spectral measure, interval inputs, valid polynomial minorant, exact rational proof and spectral-state isolation** as separate verification objects.

**Acceptance:** algebraic spectral-window inequality **ANALYTIC EXACT** for any positive contraction; prediction-first integer tests including HOLD controls; original 4D positive source moments **MISSING**; actual SU2 first-excited weight **OPEN**; continuum mass gap **OPEN**. The new checker reproduces the rational fixture and rejects inadmissible attempts to interpret the total window weight as one particular eigenstate.
