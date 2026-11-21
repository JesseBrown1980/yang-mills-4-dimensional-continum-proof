# YM4-SU2-WT01 — Wilson-action local SU(2) character transfer and exact Wilson moments

Date: 2026-11-21. Source scope: original continuous SU(2) Wilson plaquette, normalized Haar; one periodic spatial-circle link with a timelike plaquette, and a separate six-staple conditional 4D Wilson-link calculation. Status: exact analytic identities with independently tested rational error bounds. Full interacting 3+1-dimensional physical transfer, 4D source moments and continuum mass gap: OPEN.

## Provenance and why the kernel is derived

The original 4D definition in [PROBLEM.md](../../PROBLEM.md) and [YM4-02c](../LEMMA-0004-REFLECTION-TRANSFER.md) uses, for each SU(2) plaquette,
w_beta(U) = exp[-beta*(1 - Tr(U)/2)].
After removing the U-independent factor exp(-beta), the normalized temporal coupling between consecutive spatial-link holonomies U,V in temporal gauge has exactly the SU(2) Wilson weight exp[beta*Tr(U V^{-1})/2]. There is no arbitrary 2x2 matrix in this construction.

On a one-link periodic spatial circle, residual Gauss transformations act by conjugation U -> g U g^{-1}, and the gauge-invariant Hilbert space is the class-function subspace of L^2(SU(2), Haar). The orthogonal Gauss projector is

    P_G f(U) = integral_SU2 dg f(g U g^{-1}).

The finite one-link example is a genuine Wilson-action transfer calculation; it is the k=1 spatial-circle specialization of the general transfer setting. The full 4D (k=3) spatial links, all magnetic plaquettes, their coupled Gauss constraints and the 4D physical vacuum are distinct requirements.

## Exact character representation

Write SU(2) holonomy eigenvalues exp(+i theta), exp(-i theta), and define x=cos(theta)=Tr(U)/2. The spin-r/2 character is chi_r(U)=sin((r+1)theta)/sin(theta), with r=0,1,2,..., dimension d_r=r+1.

The Haar integral is

    Z_beta = integral_SU2 exp(beta*x) dU = 2*I_1(beta)/beta,

with I_m the modified Bessel function. Character orthogonality and the Wilson expansion yield

    exp(beta*x) =
        sum_{r>=0} [2*(r+1)*I_(r+1)(beta)/beta] chi_r(U).

Therefore the normalized central convolution operator

    (T_beta f)(U) =
        integral_SU2 dV exp[beta*Tr(U V^{-1})/2] f(V) / Z_beta

is a positive self-adjoint operator on class functions, with exact character eigenvalues

    T_beta chi_r = lambda_r chi_r,
    lambda_r = I_(r+1)(beta)/I_1(beta).

The trivial character has lambda_0=1. Every beta>0 gives strictly positive character coefficients and absolute convergence. The operator is trace-class because the coefficients have factorial decay at fixed beta. These are standard compact-group character facts; our numerical certificates verify the specific beta values independently.

The normalized fundamental Wilson observable is W(U)=Tr(U)/2=chi_1(U)/2. On this one-link circle the normalized vacuum is chi_0=1. Since W*chi_0=chi_1/2 and chi_1 is orthogonal to chi_0, the connected correlator is exactly

    C_n = <vacuum, W T_beta^n W vacuum> = (1/4)*lambda_1^n

for n>=0, where lambda_1=I_2(beta)/I_1(beta).
Thus C0=1/4 and the one-link W-visible nonzero squared overlap is exactly 1/4. C2 and C4 are enclosed by exact rational inequalities, not guessed from small sample sizes.

## Integer rational Bessel and character-cutoff certificates

Define the scaled Bessel series

    J_m(beta) = sum_{k>=0} (beta^2/4)^k / [k!*(k+m)!],
    I_m(beta) = (beta/2)^m J_m(beta).

For beta positive rational, each term is rational. After retaining k=0,...,N, the first omitted term a_(N+1) is positive, and the ratio of all subsequent terms is at most

    q = (beta^2/4) / [(N+2)*(N+2+m)].

For q<1, the exact enclosing interval is

    sum_(k=0)^N a_k <= J_m(beta)
      <= sum_(k=0)^N a_k + a_(N+1)/(1-q).

Using J_1 and J_(r+1) gives rational endpoints for lambda_r and for C2 and C4. The engine uses 21 terms (N=20) at beta 1 and 4, and checks the lambda_1 enclosure width is strictly below 10^-25.

There is also a **uniform** pointwise group-kernel bound on truncating the normalized Wilson character expansion after r=M. Since |chi_r(U)|<=r+1 and J_(r+1)<=exp(beta^2/4)/(r+1)! while J_1>=1,

    || K_beta - sum_(r=0)^M (r+1)*lambda_r*chi_r ||_infinity
       <= exp(beta^2/4) *
          sum_(r=M+1)^infinity (r+1)*(beta/2)^r/r!.

For beta=1 use exp(1/4)<=4/3. For beta=4 use exp(4)<3^4=81. The ratio of successive majorants after r is

    (beta/2)*(r+2)/(r+1)^2.

These exact rational upper bounds are below 10^-12 for beta=1, M=12 and beta=4, M=24. Their size is a fixed-beta, single SU(2) kernel bound. The full 4D tensor-product and spatial-volume truncation errors have to be proved separately.

## Additional exact 4D six-staple source match

The existing [YM4-05A](../NOTE-YM4-05A-CHARACTER-WEAK-COUPLING-20261107.md) establishes that an actual 4D link contributes six staple holonomies, and its fixed-staple Haar factor is

    Z_beta(Q) = sum_{m>=0} (beta^2 Q)^m / [4^m*m!*(m+1)!].

For six aligned identity staples Q=36, so the conditional density is proportional to exp(6 beta*x). Its exact conditional mean half-trace is

    E_beta[x | all six staples=I] = I_2(6 beta)/I_1(6 beta).

Thus actual four-dimensional local beta=1/6 matches the beta=1 one-link Bessel-ratio certificate, and local beta=2/3 matches the beta=4 certificate. This is a **conditional local 4D Haar quantity**, not a bulk 4D Wilson time-correlation, transfer eigenvalue or first physical state.

## Frozen predictions and independent acceptance

Prediction artifact [PREDICT-YM4-WILSON-SU2-LOCAL-TRANSFER-20261121.hbp](certificate-atlas/PREDICT-YM4-WILSON-SU2-LOCAL-TRANSFER-20261121.hbp) was committed as 62287cd957d361a69dd257faadd6daf44dba3ec9 before implementation or tests.

The independent checker constructs SU(2) Chebyshev characters by an integer recurrence and integrates their products with independent exact Catalan Haar monomial moments. It checks up to 81 orthogonality cases plus 45 distinct Wilson exponential coefficients, including the d_r character factor. It separately checks the existing 4D Q=36 Haar partition from the six-staple sum. Deliberate wrong-beta, insufficient-tail, wrong half-trace, wrong representation dimension, and non-class-matrix-entry controls are recorded.

    python3 -B tests/test_ym4_su2_wilson_local_transfer.py
    python3 -I -B tests/ym4_su2_wilson_local_transfer.py

The dedicated workflow confirms the historical prediction commit predates both implementation files, runs exact tests, matches two unmodified production transcripts and stores a SHA-256 receipt.

## Next original 4D physical-observable gates

1. Lift from this single Wilson factor to the original 4D spatial-slice graph with three link directions and all plaquettes; enforce all Gauss laws on actual coupled link states.
2. Build actual gauge-invariant Wilson-network source vectors. Derive the original 4D transfer under the correct boundary conditions rather than tensoring one-link factors without magnetic interactions.
3. With explicitly bounded character truncations for the full system, calculate original physical C0, C2 and C4 and evaluate exact spectral-window inequalities.
4. Derive physical-size, volume- and tuning-uniform full-spectrum estimates for a genuine 4D mass gap.

The finite S3 certificate, the metatagged frame automaton and this continuous-SU(2) local kernel are kept as three different models. Their reproducibility methods are reusable; physical transfer requires proved mathematical intertwiners and normalization.
