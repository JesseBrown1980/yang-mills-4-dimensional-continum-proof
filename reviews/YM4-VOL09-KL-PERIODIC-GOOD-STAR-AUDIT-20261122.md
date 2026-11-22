# YM4-VOL09 independent analytical audit — relative entropy, Haar cap and gauge-star conversion

**2026-11-22.** This review reconstructs the proof of [VOL09 original Wilson periodic good-star frequency](../docs/certificate-atlas/NOTE-YM4-VOL09-PERIODIC-GOOD-STAR-FREQUENCY-20261122.md) through finite-volume **relative entropy** rather than invoking convexity of the logarithmic partition function as a black box. This is a second proof route by the same assistant, not an external human review. The exact integer checker independently verifies arithmetic endpoints; continuous SU2 Haar integration and the entropy comparison remain analytical theorems.

## 1. Review the original Wilson normalization and measures

On the isotropic periodic 4D torus \(L^4\), \(L\ge3\), let \(E=4L^4\) and \(P=6L^4\). The energy variable is \(A=\sum_p\frac12\mathrm{Tr}U_p\le P\), the reference measure is product **normalized** SU2 Haar, and \(d\mu_\beta=e^{\beta A}d{\rm Haar}/Z_\beta\). The finite Gibbs density is strictly positive for finite \(\beta\), so all relative entropies below are well-defined.

Fix \(\beta\ge1\) and choose the link Haar cap \(B_r(I)\) of geodesic radius \(r=1/(4\sqrt\beta)\). The exact SU2 polar measure is \(2\pi^{-1}\sin^2\theta\,d\theta\), so \(\Pr_{\rm Haar}(B_r)\ge r^3/24=(1536\beta^{3/2})^{-1}\). This inequality uses only \(\sin\theta\ge\theta/2\) on \([0,1/4]\); it does not approximate the SU2 measure by a Euclidean Gaussian. A product of four group elements in \(B_r\) has SU2 geodesic distance \(\le4r\) from identity; consequently every original plaquette is \(\ge1-1/(2\beta)\). Therefore
\[
\log Z_\beta\ge\beta P-\frac P2-E\log(1536\beta^{3/2}).
\]
A separate check uses \(A\le P\) to give \(\log Z_{\beta/2}\le\beta P/2\).

## 2. Independent KL derivation of the same volume-uniform coefficient

Compute the density ratio explicitly:
\[
\log\frac{d\mu_\beta}{d\mu_{\beta/2}}
=\frac{\beta}{2}A-\log Z_\beta+\log Z_{\beta/2}.
\]
Its expectation under \(\mu_\beta\) is a Kullback–Leibler divergence, hence nonnegative:
\[
\frac\beta2\,\mathbb E_\beta A
\ge \log Z_\beta-\log Z_{\beta/2}.
\]
Substitute the independently checked partition bounds:
\[
\mathbb E_\beta A
\ge P-\frac P\beta-\frac{2E}{\beta}\log(1536\beta^{3/2}).
\]
Since periodic rotations/translations make every original plaquette expectation equal and \(E/P=2/3\),
\[
\boxed{\mathbb E_\beta(1-W_p)
\le\frac1\beta+\frac4{3\beta}\log(1536\beta^{3/2}).}
\]
The coefficient \(4/3\) is independently recovered from the exact 4D link/plaquette ratio, and both normalization and two-temperature factors were audited. No volume-dependent entropy remains after dividing by \(P\).

## 3. Gauge-invariant star event and the actual probability bound

VOL08 defines six preferred unit quaternions \(s_i\) and one original link quaternion \(u\), with full plaquette \(W_i=u\cdot s_i\). On the full continuous SU2 quaternion sphere,
\[
|s_i-s_j|^2\le2(|s_i-u|^2+|s_j-u|^2).
\]
If all six \(W_i\ge1-\epsilon/4\), each pair satisfies \(s_i\cdot s_j\ge1-\epsilon\). This conclusion uses **closed double-staple Wilson loops** and is gauge invariant, with no gauge choice. The contrapositive, sixfold union and Markov yield the precise bound
\[
\Pr_\beta(\mathcal G_\epsilon^c)\le
\min\!\left\{1,\frac{24}{\epsilon\beta}
\left[1+\frac43\log(1536\beta^{3/2})\right]\right\}.
\]
It applies to every **individual** original star on any periodic isotropic \(L^4\), \(L\ge3\), uniformly in \(L\).

The integer verifier checks the exact partial series \(e^8>\sum_{j=0}^8 8^j/j!=556403/315>1536\) and \(e^{3/2}>29/8>3\). Thus \(\beta=9^k\) gives \(\Pr(\mathcal G_\epsilon^c)\le8(35+18k)/(\epsilon9^k)\). The fixtures \(\epsilon=1/2,k=5\to2000/59049\) and \(\epsilon=1/81,k=8\to1432/531441\) recompute exactly.

## 4. Scope, adversarial interpretation and peer acceptance

**Analytic result PASS by two equivalent methods:** finite Gibbs convex free-energy secant (main note), and direct Gibbs-to-Gibbs KL nonnegativity (this review). The origin and count of the six Wilson plaquettes, Haar cap and gauge-invariant star are checked independently of the rational code. 

**What is established:** an unconditional \(\beta\)-dependent marginal probability of bad-star exteriors under the original continuous-SU2 periodic equilibrium measure, with a volume-independent ceiling tending to zero even for shrinking \(\epsilon\).

**What remains:** correlated bad-star cluster/island tails; uniform estimates conditional on **adversarial exterior data**; a quantitative good-block coupling and temporal physical-size contraction; renormalized source weights and OS continuum reconstruction. VOL08's adversarial one-external-link TV examples remain valid because low Gibbs probability is not the same as impossibility for a fixed exterior. A high-probability marginal event does not imply a Dobrushin–Shlosman block condition.

This audit is ready for outside independent mathematical signoff after the hosted rational tests. The latest external one-cube reference is [Bhattacharjee–Bhattacharya–Lockwood–Romanov, version 7](https://hexagonmath.org/2610.00341v7). Its block-island methodology is a relevant attributed research direction, while its unproved continuum cube hypothesis and our eleven original continuum gates remain OPEN.
