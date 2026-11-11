# YM4-06H — 4D Wilson, a volume-independent STRONG-COUPLING physical-transfer bound

**Date: 2026-11-11. Status: prediction-first exact-integer hosted checks plus an analytical covariance-to-transfer argument using established named theorems. Independent theorem review is required before acceptance.** This note does not claim a continuum Yang–Mills mass gap and does not extend the old temporal beta_t=1 result.

**Frozen BEFORE any verifier source:** docs/PREDICTION-YM4-06H-4D-UNIFORM-TRANSFER-20261111.hbp at commit fbac66298dcf6a9b0c1bde42eced49b886ba5b3e. The test checks that this file remains byte-identical to its original freeze.

## 1. The full interacting four-dimensional model

Take periodic three-dimensional spatial sides L>=2 and Euclidean temporal length Nt>=2, eventually Nt->infinity. At each positive oriented edge e there is an SU(2) link U_e integrated against normalized Haar measure. The **anisotropic** Wilson Gibbs action is

\[
 d\mu_{\Lambda,\beta_s,\beta_t}(U)\propto
 \exp\Big[
   \beta_s\!\sum_{p\ {\rm spatial}}\tfrac12\operatorname{Tr}U_p+
   \beta_t\!\sum_{p\ {\rm temporal}}\tfrac12\operatorname{Tr}U_p
 \Big]\,\prod_e dU_e .
\]

The constants exp(−beta per face) in the standard Wilson weight cancel from normalized expectations. Both couplings here are **strictly positive**. The primary **new strong-coupling point** is

\[
 \boxed{\beta_s=1/128,\qquad\beta_t=1/32.}
\]

This is not the YM4-06F point beta_t=1; that earlier point is excluded by the simple four-dimensional Dobrushin criterion.

Each cubic spatial edge belongs to **four spatial and two temporal plaquettes**; each temporal edge belongs to **six temporal plaquettes and no spatial plaquettes**. Every 4D face has four distinct link variables for L,Nt>=2 and three other edges for each one of them. On all links, the number of co-plaquette neighboring-link incidences is exactly 6×3=18. This geometry is independent of the total number of faces.

The hosted test reconstructs EVERY face and EVERY link on periodic spacetime lattices (L,Nt)=(2,3),(3,3),(3,6),(5,3),(9,3),(27,2). At (27,2) there are **39,366 sites, 157,464 links and 236,196 4D plaquettes**. It checks that all link pairs in a face have temporal anchor distance at most one frame, and independently verifies SU(2) plaquette trace covariance under nonuniform eight-element quaternion gauge transformations at all vertices. Exact nonflat witnesses occur in both spatial and temporal plaquettes. Those quaternion configurations are **witnesses only**, not a replacement for continuous SU(2) integration.

## 2. A Dobrushin influence coefficient that does NOT contain |plaquettes|

Represent SU(2) as the unit-quaternion sphere S³. For any edge i, holding other links fixed gives a single-link conditional distribution proportional to exp(h_i·U_i) relative to Haar. Each face p incident on i contributes a vector of norm beta_p to h_i.

When the background changes only at another edge j, the field changes by at most 2 times the sum of beta_p over their jointly incident faces. For the exponential family exp(h·X), the total-variation distance of conditional probabilities is bounded by ||h−h'||/2: interpolate linearly in h, differentiate E_h f for 0<=f<=1, write the covariance with (h−h')·X, then use Cauchy–Schwarz and |X|=1. Therefore the Dobrushin interdependence entries satisfy the **exact analytic inequality**

\[
 c_{ij}\le\sum_{p\ni i,j}\beta_p.
\]

Each link in a face sees three other links. Hence, for every spatial link i,

\[
 \sum_{j\ne i}c_{ij}\le 3(4\beta_s+2\beta_t)
      =12\beta_s+6\beta_t,
\]

and for every temporal link i,

\[
 \sum_{j\ne i}c_{ij}\le 3(6\beta_t)=18\beta_t.
\]

Thus, for ALL finite spatial L and ALL temporal lengths Nt,

\[
 \boxed{\alpha\le\max(12\beta_s+6\beta_t,\ 18\beta_t).}
\]

At the frozen primary coupling, the spatial influence sum is 9/32 and temporal is 9/16:

\[
 \boxed{\alpha\le 9/16<1,\quad\text{independent of }L,N_t,|\mathcal P|.}
\]

The hosted Rust 1.81 source checks these exact reduced rational fractions with no floating-point arithmetic.

Two additional nonzero-coupling controls at fixed beta_s=1/128 are beta_t=1/64, giving alpha<=9/32, and beta_t=1/128, giving alpha<=9/64. The tests intentionally REJECT beta_t=1/16 (alpha_t=9/8>1) and beta_t=1 (alpha_t=18>1). This proves the criterion is **not** silently extended into the wrong coupling range.

## 3. Temporal clustering from a standard covariance inequality

We now state the analytical bridge, not a computation of the full transfer eigenvalues.

Under alpha<1, the Dobrushin–Föllmer covariance comparison for bounded cylinder observables F,G on the 4D Wilson Gibbs measure bounds their connected correlation using the interdependence matrix C=(c_ij):

\[
 |\operatorname{Cov}(F,G)|
 \le C_{F,G}\!\sum_{i\in\operatorname{supp}F,\
                    j\in\operatorname{supp}G}
      \big[(I-C)^{-1}\big]_{ij},
 \qquad (I-C)^{-1}=\sum_{n\ge0}C^n.
\]

Here C_{F,G} depends on their coordinate oscillations (and possibly on fixed finite spatial L), but NOT on the separation in Euclidean time. The exact prefactor is irrelevant to the limiting exponential rate; it must not be silently replaced by one in a finite-time numerical estimate.

A crucial locality assertion tested on **all four-dimensional faces** is that one co-plaquette influence step changes the link's anchored Euclidean time coordinate by at most **one**. If F depends only on spatial links in time slice 0 and G only on spatial links in time slice t, then in the infinite-time cylinder every path of C between their supports has length >=t. Consequently the geometric series begins no earlier than order t and

\[
 \boxed{
 |\operatorname{Cov}(F_0,G_t)|
 \le C'_{F,G,L}\frac{\alpha^t}{1-\alpha}.
 }
\]

For finite periodic Nt replace t by the cyclic separation min(t,Nt−t); send Nt to infinity **before** extracting t->infinity. The exact rational checker evaluates the geometric alpha^t/(1−alpha) factors at t=1,3,9,27 without taking a floating-point logarithm.

This uses the known Dobrushin covariance theorem (Föllmer 1982 / Künsch 1982). The source checks its **finite geometric hypotheses**, not a formalization of the general measure-theoretic theorem. A reviewer must verify the theorem's hypotheses and the time-slice support/covariance normalization.

## 4. Reflection positivity converts this into a physical transfer spectral bound

The standard Wilson plaquette action satisfies lattice reflection positivity and admits a positive self-adjoint transfer on the gauge-invariant spatial Hilbert space (Osterwalder–Seiler 1978; see this repository's Lemma 0004). For each **fixed finite spatial L**, take the infinite-time limit of normalized Euclidean correlations. They have the physical spectral form

\[
 \langle F_0 F_t\rangle_c
 =\sum_{n\ge2}|a_n(F)|^2
   \left(\frac{\lambda_n(T)}{\lambda_1(T)}\right)^t
\]

in a discrete/compact spectral setting, with a corresponding positive spectral integral in general. Terms are nonnegative. For every bounded gauge-invariant spatial-slice F, the Dobrushin comparison supplies an O(alpha^t) upper bound (at this L). Any physical transfer eigenvalue ratio strictly greater than alpha would be detected by some bounded F because such functions are dense in the finite-volume physical Hilbert space. That would contradict the asymptotic correlation bound. Therefore the proposed **fixed-lattice spacing, all-spatial-volume** physical transfer consequence is

\[
 \boxed{
 \frac{\lambda_2(T_{L,\beta_s,\beta_t})}
      {\lambda_1(T_{L,\beta_s,\beta_t})}
 \le\frac9{16}
 \quad\text{for every periodic spatial }L\ge2,
 }
\]

and at a declared reference a_t (not yet calibrated to physical seconds)

\[
 \boxed{m_{\rm first}(a_t,L)\ge\frac{\log(16/9)}{a_t}>0.}
\]

The RHS does **not** deteriorate with the number of spatial plaquettes or the spatial volume. In particular, this is a **full interacting gauge-invariant Wilson transfer** bound at a nonzero spatial plaquette coupling, *conditional on the standard covariance and reflection-positivity bridge being applied correctly*. The numerical verifier certifies the exact local premises, geometry and negative controls, while independent analysis of the bridge remains required.

At beta_t=1/64 and 1/128 the analogous candidate bounds are log(32/9)/a_t and log(64/9)/a_t, respectively; they use different temporal coupling points and must not be confused with the original beta_t=1.

## 5. What this solves and what it does NOT

**Addresses the current volume problem:** unlike the earlier finite-volume min–max bound e^{2 beta_s |plaquettes|}*(b1/b0)^g, the strong-coupling Dobrushin bound depends on the number of **plaquettes incident to a link**, not on the extensive total. It includes spatial and temporal interactions, at explicitly smaller temporal beta.

**Does not address the Clay continuum problem:** the couplings remain in a strong-coupling window, the physical temporal and spatial lattice spacings are not sent to zero along a matched asymptotically free renormalization trajectory, and no uniform physical positive mass after removal of the ultraviolet cutoff has been proved. The old beta_t=1 SU(2) transfer remains outside this criterion. SHA/HBI/HBP/SH/HASH certify output provenance and do not represent superluminal physical propagation.

**Verification boundaries:** Native Rust 1.81, strict Clippy, exact integers/rationals, six tested 4D geometries (including L27), six deliberately rejected controls counting HBP tampering, ordered five-ledger SHA-256 receipts. The *Dobrushin–Föllmer covariance comparison and Osterwalder–Seiler transfer theorem are imported mathematical results*; checking their combination for the precise 3+1D gauge action is the requested independent proof review.

**Primary literature:**
- K. Osterwalder and E. Seiler, "Gauge field theories on a lattice", Annals of Physics 110 (1978), 440–471, DOI 10.1016/0003-4916(78)90039-8.
- H. Föllmer, "A covariance estimate for Gibbs measures", Journal of Functional Analysis 46 (1982), 387–395, DOI 10.1016/0022-1236(82)90053-2.
- H. Künsch, "Decay of correlations under Dobrushin's uniqueness condition and its applications", Communications in Mathematical Physics 84 (1982), 207–222.
- This repository: docs/LEMMA-0004-REFLECTION-TRANSFER.md; YM4-06D/E/F fixed-volume transfer controls and YM4-06G classical spatial Dobrushin theorem.

**Independent review requests:** rederive the SU(2) 4D single-link conditional TV influence with the chosen Wilson trace normalization; check all spatial/temporal faces and time-anchor locality; confirm the exact constants in the imported covariance comparison; examine the time-cylinder limit, gauge-invariant spectral density and transfer normalization; and attack the claimed bound by counterexample at the explicitly frozen strong couplings. Keep DRAFT until those checks are complete.
