# YM4-WC01 — original interacting 4D SU(2) Wilson finite-cylinder moment enclosures

**Date:** 2026-11-21. **Status:** exact rational enclosures for original four-dimensional finite-periodic Euclidean connected Wilson correlators at two small positive Wilson couplings, subject to hosted verification. **Source:** the original 4D Wilson action and normalized SU(2) Haar measure as in PROBLEM.md, YM4-02a and YM4-02c.

## 1. The genuine 4D source and its exact graph

Let Lambda = (Z/2Z)^3 x (Z/10Z). There are exactly 80 vertices, 320 positive directed links and 480 independent positively oriented plaquette terms: 240 purely spatial and 240 involving the time direction. Each positive link belongs to exactly six plaquettes. Spatial link dimension per slice is 24, and all three spatial coordinate directions and every time-like plaquette are included.

For SU(2)-valued link fields U_l, a_p(U)=(1/2) ReTr U_p with U_p the four-link ordered holonomy, and the actual Wilson action is

    S_W(U;beta) = beta * sum_p (1 - a_p(U)).

For any bounded function F, its exact finite-volume Wilson expectation is

    <F>_beta = int[ F(U)*exp(beta*A(U)) ] dHaar(U)
               / int[exp(beta*A(U))] dHaar(U),
    A(U) = sum_p a_p(U).

The constant exp(-480 beta) cancels. Crucially, the weight exp(beta*A(U)) couples **all** 480 spatial and time-like plaquettes; this is a full finite 4D Wilson measure rather than a product of the one-link kernels from YM4-SU2-WT01.

Take a single normalized spatial Wilson plaquette W_t(U)=(1/2)ReTr U_(0,1)(0,0,0,t) at t=0,2,4. These are gauge invariant, bounded by one, and located on distinct time slices. Define the finite *periodic-cylinder* connected correlators

    C_T(0) = <W_0^2>_beta - <W_0>_beta^2,
    C_T(t) = <W_0 W_t>_beta - <W_0>_beta^2, t=2,4,

using exact periodic time translation symmetry. The time circumference **T=10** is held fixed, so these are finite-temperature/periodic Euclidean observables; the infinite-time vacuum correlator and its spectral moments remain a separate limit and OPEN acceptance gate.

## 2. Haar identities at beta=0

Write A=sum_p a_p. SU(2) normalized Haar gives E_Haar[x^2]=1/4 and E_Haar[x^4]=1/8 for x=(1/2)ReTr U. Every plaquette on Lambda contains four distinct links; every two distinct plaquettes share at most two, hence each has an exclusive link.

The exact product-Haar expectations needed through order two are:

    E[A] = 0,           E[A^2] = 480/4 = 120
    E[W_0] = 0,         E[W_0^2] = 1/4
    E[W_0 A] = 1/4,    E[W_0^2 A] = 0
    E[W_0 A^2] = 0,    E[W_0^2 A^2] = 481/16
    E[W_0 W_t] = 0,   E[W_0 W_t A] = 0
    E[W_0 W_t A^2] = 1/8, t in {2,4}.

The nonzero E[W_0 A]=1/4 is supported solely by the source plaquette itself. The 481/16 row is the 479 distinct other plaquettes, each contributing 1/16, plus the same plaquette's fourth moment of 1/8.

The 1/8 time-pair row consists of precisely two **ordered** plaquette choices, (p0,pt) and (pt,p0). For each, independence of disjoint time-slice Haar variables gives E[W_0^2]E[W_t^2]=1/16. The producer exhaustively checks the necessary mod-two link support, while the analytic Haar identities evaluate the surviving cases. The independent checker reconstructs link supports, checks overlap limits, directly enumerates each parity set, and separately tests exact rational quaternion gauge covariance across every plaquette.

Mod-two selection comes from the SU(2) centre: multiplying a selected link U_l by -I leaves Haar measure unchanged and changes the sign of every trace word containing that link an odd number of times. Any integrand with nonzero odd-edge support consequently integrates to zero. Parity is a **necessary** vanishing criterion; only the listed surviving cases are evaluated by Haar integration. This avoids pretending that every parity-even product has a universal value.

## 3. Exact full-action perturbation and certified remainder

Put x = 480*beta, and restrict to rational beta>0 with x<1. Since each |a_p|<=1, |A|<=480. The scalar Taylor theorem with |e^y -1-y-y^2/2|<=x^3/[6(1-x)] for |y|<=x<1 gives a **uniform**, rigorously rational third-order remainder

    epsilon = x^3 / [6*(1-x)].

This covers the **full interacting Wilson weight** exp(beta*A), including all higher-order connected and disconnected contributions. Define the unnormalized Haar integrals Z, N1, N2, Nt, and denote their exact but unknown remainders r with |r|<=epsilon:

    Z  = 1 + 60*beta^2 + r_Z
    N1 = beta/4 + r_1
    N2 = 1/4 + (481/32)*beta^2 + r_2
    Nt = beta^2/16 + r_t           (t=2,4).

For Zlo=1+60 beta^2-epsilon >0 and Zhi=1+60 beta^2+epsilon, the original physical finite-periodic correlations obey the following fully rational bounds:

    U_mu = (beta/4 + epsilon)/Zlo
    (1/4 + 481 beta^2/32 - epsilon)/Zhi - U_mu^2 <= C_T(0)
    C_T(0) <= (1/4 + 481 beta^2/32 + epsilon)/Zlo.

Because Nt^(2)=(beta/4)^2 exactly, the disconnected beta-squared contribution cancels from C_T(t). More precisely

    C_T(t) = [Nt*Z-N1^2]/Z^2,
    |C_T(t)| <= B, t=2,4,

where

    B = { (beta^2/16)*(60 beta^2)
          + epsilon*[Zhi + beta^2/16 + beta/2] + epsilon^2 }/Zlo^2.

Every term and inequality uses exact integer pairs. A no-floating-point policy is enforced by the repository's existing checker. The resulting finite-time source is mathematically well normalized; taking T to infinity and isolating the vacuum remains to be established with its own quantitative convergence bound.

## 4. Two frozen acceptance windows

The prediction was committed at 23daf59d52e5087fd8308b9aa9ef8e882220766d before either producer or test implementation.

| Wilson beta | Certified C_T(0) deviation from 1/4 | Certified |C_T(2)| and |C_T(4)| |
|---:|---:|---:|
| 1/10000 | less than 1/10000 | less than 1/50000 |
| 1/100000 | less than 1/10000000 | less than 1/50000000 |

These are conservative error enclosures derived from the full 480-plaquette action, not Monte Carlo values or invented eigenvalues. The two nonzero-time enclosures are identical because the uniform remainder has no time-distance sensitivity beyond the exact second-order parity check. A distance-dependent positive spectral decay estimate requires further work.

The HBP receipt prints outward-rounded integer bounds on a fixed 10^12 denominator. The exact rational producer verifies every strict frozen inequality before printing. It also checks four-link plaquette orientation, all 320 six-staple incidence identities, no duplicate source plaquettes, 480 independently checked time/spatial plaquette terms, and disjoint source supports.

## 5. Relationship to the 4D Yang–Mills certificate atlas

This result supplies original interacting **finite-periodic 4D SU(2)** Wilson source correlator enclosures; it is a new fixed-size Q04-compatible source check. It builds on YM4-02a Haar moments, the original Wilson normalization in PROBLEM.md, and YM4-02c's reflection/transfer formulation.

It provides neither a constructive diagonalization of the full interacting gauge-projected transfer nor the infinite-T vacuum moment C_n = <Omega, W T^n W Omega> needed by the spectral-window dual. Therefore Q03, Q04's vacuum/source accuracy and Q05–Q11 continuum/physical requirements remain OPEN.

The next meaningful upgrade is a **time-uniform transfer trace-to-vacuum error bound** or an exact small-sector gauge projector/transfer computation that lets the present periodic C_T be converted to correctly normalized vacuum C_n. After that, original physical spectral weight and a full-spectrum gap require separate certificates.

## 6. Reproduction

    python3 -B tests/test_ym4_4d_wilson_cylinder_moments.py -v
    python3 -B tests/ym4_4d_wilson_cylinder_moments.py

The workflow verifies the freeze ancestry, original strict no-float gate, independent geometry/Haar tests, deterministic HBP and acceptance digest, and retains the artifact on GitHub Actions.
