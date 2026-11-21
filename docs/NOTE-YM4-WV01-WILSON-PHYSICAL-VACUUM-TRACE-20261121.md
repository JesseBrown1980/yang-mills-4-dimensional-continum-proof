# YM4-WV01 — exact original 4D physical-vacuum Wilson moment bridge

**Date:** November 21, 2026. **Scope:** continuous SU(2), original Wilson plaquette action, fixed spatial three-torus (Z/2Z)^3, time circumference 10 for the source measurements, and its infinite-time *fixed-spatial-lattice* positive physical transfer limit. **Result:** explicit exact rational enclosures for the physical-vacuum connected Wilson moments C_0,C_2,C_4 at beta=1/10000 and beta=1/100000, with a quantified finite-time correction. **Continuum uniformity and first-level Wilson spectral overlap:** OPEN.

## 1. Original 3+1-dimensional Wilson physical transfer

The exact [YM4-02c theorem](LEMMA-0004-REFLECTION-TRANSFER.md) identifies the transfer for the Wilson action and the physical Gauss projector; [YM4-02d](NOTE-YM4-02d-QUANTITATIVE-GAP.md) bounds the other eigenvalues at each fixed spatial lattice. [YM4-WT01](NOTE-YM4-SU2-WILSON-LOCAL-TRANSFER-20261121.md) establishes the **actual normalized SU(2) Wilson one-link Haar character coefficients**. [YM4-WC01](NOTE-YM4-WC01-ORIGINAL-4D-WILSON-CYLINDER-20261121.md) gives the original 480-plaquette Euclidean finite-T Wilson correlation intervals.

Let H=L^2(SU(2)^24, product Haar). Each of the eight spatial sites carries an independent SU(2) gauge transform; P is the orthogonal projector onto invariant functions. The original one-link normalized temporal Wilson convolution is k_beta(g)=w_beta(g)/int w_beta dHaar, with normalized spin-r character eigenvalues lambda_r=I_(r+1)(beta)/I_1(beta).

Let K_24 be the tensor product of 24 copies of that original one-link convolution, and let B(U) be the product of **all 24 original spatial magnetic Wilson plaquette factors** on one slice. The full positive, self-adjoint, trace-class physical transfer (up to the overall scalar temporal plaquette normalization that cancels from ratios) is

    T_phys = B^(1/2) P K_24 P B^(1/2).

All spatial magnetic interactions are present, all Gauss constraints act on the original spatial gauge group, and the temporal plaquette product is represented by K_24. The time-link Haar integration gives P on adjacent spatial slices, as in YM4-02c. The operator is positive and compact with simple largest eigenvalue Lambda0>0 and a positive invariant normalized vacuum Omega. The normalized transfer is R=T_phys/Lambda0, with spectrum 1,rho_1,rho_2,... in [0,1].

For W(U)=(1/2)ReTr U_(0,1)(0,0,0) the operator is a gauge-invariant bounded self-adjoint multiplication with ||W||<=1. Its **physical-vacuum connected** source moments are

    C_vac(n) = <Omega,W R^n W Omega>-<Omega,W Omega>^2,
             = sum_(j>=1) |<psi_j,W Omega>|^2 rho_j^n >= 0.

The YM4-WC01 original finite periodic cylinder correlators are, by the same operator, exact finite-T traces:

    E_T[W_0 W_t] = Tr(R^(T-t) W R^t W)/Tr(R^T),
    E_T[W_0] = Tr(R^T W)/Tr(R^T),
    C_T(t) = E_T[W_0 W_t]-E_T[W_0]^2.

The temporal plaquette normalization factors multiply partition function and numerator equally and therefore cancel. T=10 in the already accepted WC01 geometry.

## 2. The new exact-rational trace-class envelope

The spatial magnetic multiplier obeys 0<B<=1 and B>=exp(-2 beta N_s), N_s=24. Choose the physical trial vector f=B^(-1/2) times the constant function. Because P1=1, K_24 1=1,

    <f,T_phys f> =1,
    ||f||^2 =int B^(-1) dHaar <= exp(2 beta N_s).

The Rayleigh quotient gives

    Lambda0 >= exp(-2 beta N_s) >= 1-2 beta N_s = 1-48 beta.

The first inequality is a fixed-volume analytic statement; the final rational lower bound requires 48 beta<1.

Each SU(2) normalized one-link convolution has character-r eigenvalue lambda_r with *multiplicity* (r+1)^2 in L²(SU2). Thus

    Tr(K_one^2) = 1+sum_(r>=1) (r+1)^2 lambda_r^2.

Put y=beta²/4. The exact Wilson Bessel power series proves

    lambda_r <= exp(y)*(beta/2)^r/(r+1)!.

Using exp(y)<=1/(1-y), and (r!)²>=1, every positive tail term is bounded, and we obtain

    Tr(K_one^2) <= 1+y/(1-y)^3.

Because the gauge P is orthogonal and B^(1/2) has norm at most 1, the Hilbert–Schmidt ideal inequality gives

    Tr(T_phys^2) <= Tr(K_24^2)
                  = [Tr(K_one^2)]^24
                  <= [1+y/(1-y)^3]^24.

After normalizing by Lambda0²,

    1+sum_(j>=1) rho_j² = Tr(R²) <= M,
    M = [1+y/(1-y)^3]^24 / (1-48 beta)^2.

In particular E=M-1 is a certified bound on the **total squared excited-spectrum trace**, including all original gauge-invariant sectors. This is a true infinite-dimensional trace-norm estimate; no finite representation cutoff is substituted for the physical operator.

YM4-02d separately proves rho_j<=tanh(24 beta)<=q=24 beta for every j>=1. For integer k>=2,

    delta_k := sum_(j>=1) rho_j^k <= E * q^(k-2).

All displayed M,E,q,delta are explicit positive rationals at the two frozen couplings.

## 3. The exact periodic-to-vacuum conversion

For a time circumference T=10 and t=0,2,4, the periodic partition trace is 1+delta_T after division by Lambda0^T. Since 0<=R<=1 and ||W||<=1,

    |E_T[W_0W_t]-<Omega,W R^t W Omega>|
      <= delta_(T-t)+delta_T.

Likewise the thermal-to-vacuum one-point difference is <=2delta_T. Since each one-point expectation lies in [-1,1], the differences of their squares is <=4delta_T. Hence

    |C_T(t)-C_vac(t)| <= delta_(T-t)+5delta_T.       (WV01)

This is a bound on the **same** Wilson source and the **same** transfer normalization. It uses positivity, trace class, the physical Gauss projector and the true original spatial Wilson multiplier.

At beta=1/10000 the total excited squared-trace bound E is strictly less than 1/100. With q=24beta=0.0024, the t=4 connected thermal-to-vacuum error is strictly below 10^-12. At beta=1/100000, E<1/1000 and the t=4 error is strictly below 10^-17. The t=0 corrections are respectively below 10^-20 and 10^-30. The exact checkers recompute these claims from integer pairs.

Combining (WV01) with the original accepted WC01 periodic envelopes gives, at both positive original Wilson couplings, **rigorous physical-vacuum C0,C2,C4 intervals** for the original interacting 3D-spatial SU2 transfer. The time-separated vacuum lower bounds are zero by the positive spectral-measure theorem. The upper bounds are outward rounded and independently tested.

These fixed-lattice bounds verify the Wilson source is nontrivial, since C_vac(0)>0. They do not isolate its first excited eigenstate, and therefore cannot by themselves establish a first-Wilson-weight theorem or continuum physical gap. Uniform estimates on a lattice-spacing and spatial-volume family are still required.

## 4. Predictions, independent tests, and falsifiers

[Prediction freeze](certificate-atlas/PREDICT-YM4-WV01-WILSON-VACUUM-TRACE-20261121.hbp) committed at 7bf4baec72b1ecdc1a9736a787980994682fb8d0 before the producer and the test files.

The independent checker recomputes 24-link geometry and its original 480-plaquette WC01 parent; bounds character-Hilbert–Schmidt weight using fundamental and higher-representation Bessel interval data and squared representation dimensions; challenges the missing-vacuum trace subtraction and the finite-T range, explicitly rejects wrong magnetic and link counts, and verifies the spectral trace inequality on an unrelated exact rational positive 3-level operator. The repository's no-floating-point gate remains mandatory.

Reproduce with:

    python3 -B tests/test_ym4_wilson_vacuum_trace_bridge.py -v
    python3 -B tests/ym4_wilson_vacuum_trace_bridge.py

The hosted workflow freezes the exact source output and its checksum before changing the original proof-status ledger.

## 5. Remaining certificate obligations

YM4-Q04 now gains usable **small-coupling, fixed-volume physical-vacuum Wilson moment enclosures** from the complete 4D original measure and a checked trace-class error. The open work is quantitative at physically useful beta and larger spatial volumes, physical first-excitation Wilson weight, and efficient relative character-network truncations. Q07–Q10 retain their uniform weak-coupling, continuum construction, and mass-gap obligations.

A direct test for the physical first eigenstate still requires a source-sensitive spectral projector/Gram or Feshbach certificate, while full-volume all-scale Wilson certificates require new estimates beyond these fixed-geometry strong-coupling inequalities.
