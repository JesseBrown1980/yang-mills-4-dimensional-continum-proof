# YM4-WG01 — physical Wilson Gram bounds and first-eigenstate projector gate

**21 November 2026.** Status: exact analytic improved full-original-4D physical Wilson C2/C4 upper bounds at two small Wilson couplings; first excited physical Wilson spectral weight **HOLD**, with an independently reproducible obstruction and an actionable conditional rank-one projector witness. Predicted outcomes were frozen at commit f39c00fc7c0dc9a7cab962af490dc941d95d38c0 before the producer and independent checker.

## 1. The source is the original full four-dimensional Wilson transfer

This certificate uses [YM4-WV01](NOTE-YM4-WV01-WILSON-PHYSICAL-VACUUM-TRACE-20261121.md) without modifying its original 2×2×2 spatial source, normalized fundamental Wilson observable, physical SU(2) Gauss projector, full 24-link timelike transfer, 24 magnetic plaquettes, or true infinite-time vacuum. The original 480-plaquette periodic trace and its quantitatively controlled limit were accepted by [YM4-WC01](NOTE-YM4-WC01-ORIGINAL-4D-WILSON-CYLINDER-20261121.md).

Let R be the positive normalized physical transfer T_phys/Lambda0, Omega its normalized vacuum, W the gauge-invariant spatial Wilson half-trace, and u=(W-<Omega,W Omega>)Omega. The positive compact spectral measure nu of u is supported in (0,q], where the original [YM4-02d](NOTE-YM4-02d-QUANTITATIVE-GAP.md) gives

    q <= tanh(24 beta) <= 24 beta.

The vacuum is simple and the original transfer is injective; nu has no atom at 0, and C0=||u||^2 is strictly positive by WV01. Consequently C2=||R u||^2>0 and C4=||R^2 u||^2>0 analytically, although this alone provides no effective positive rational numerical lower bounds.

## 2. Exact even-time Wilson Krylov Gram and sharper bounds

The Gram matrix of the physical Wilson vectors u and R²u is

    G_even = [[C0, C2], [C2, C4]].

Positivity of the original transfer gives its exact determinant

    det G_even = C0*C4 - C2² >= 0.

The physical spectral support t in (0,q] immediately gives

    0 < C2 <= q² C0,
    0 < C4 <= q² C2 <= q⁴ C0.

These inequalities are source-normalized, full-Gauss and full-magnetic at the fixed spatial three-torus; they apply to the true vacuum moments from WV01. The integer-only verifier combines the exact parent C0 upper bound with q=24 beta, using the same Wilson coupling and vacuum.

At beta=1/10000:
- C2 <= 0.000001440139406101 (outward rounded at denominator 10^18).
- C4 <= 0.000000000008295202979139 (outward rounded at denominator 10^24).

At beta=1/100000:
- C2 <= 0.000000014400001334 (outward rounded at denominator 10^18).
- C4 <= 0.000000000000000829440077 (outward rounded at denominator 10^24).

The sharpened C4 upper bounds are millions of times smaller than the preceding broad WC01/WV01 Taylor-plus-trace bounds. These are upper bounds; direct lower moment certificates and actual first-eigenstate isolation remain separate.

## 3. Why first-state weight cannot yet be read from C0,C2,C4

Fix any of the two original beta values and q=24 beta. Consider the **same** four strictly ordered physical excited eigenratio values

    t=(3q/4, q/2, q/3, q/4).

Define two positive spectral weights on these eigenvalues:

    A=(0, 1/12, 1/12, 1/12)
    B=(21/4000, 1/12-182/4000,
       1/12+486/4000, 1/12-325/4000).

Every listed weight is nonnegative, and the weights in each case sum to C0=1/4. A direct exact-rational calculation proves that BOTH choices have the *same* C0,C2,C4:

    C0 = 1/4,
    C2 = (61/1728) q²,
    C4 = (1633/248832) q⁴.

Their even Gram determinant equals (589/1492992) q⁴ >0. They also satisfy both original WV01 parent moment intervals, the improved WG01 upper caps, the global physical excited eigenratio bound, and the full WV01 excited trace-squared envelope (their four eigenratios together fit under that envelope). They are two **adversarial positive spectral models**, not a computation of the actual physical SU(2) spectrum.

But the first excited eigenvector has **zero** Wilson weight in A and **21/4000** weight in B. Hence C0,C2,C4 (even known *exactly*), the global eigenratio cap, and the present trace envelope cannot isolate the actual first-state Wilson overlap. A PASS for that overlap must include an additional spectral isolation/projection certificate.

## 4. Conditional first-eigenprojector/Feshbach acceptance witness

Suppose a separately proved physical spectral certificate isolates a **rank-one actual first excited eigenprojection** P1, proves its eigenratio t1<=b, and proves every other nonvacuum eigenratio <=c<b. If the physical source has C2>=m2 and C0<=M0, then

    C2 <= b²*w1 + c²*(C0-w1),
    w1=||P1 u||²,

so the valid dual lower bound is

    w1 >= max(0,(m2 - c²*M0)/(b²-c²)).

This is an exact pointwise spectral inequality. It makes clear the three **independent** proof inputs required for a physical PASS: (i) a valid physical projector and rank-one isolation, (ii) an upper bound on the remaining physical eigenratios, and (iii) an effective positive lower bound for C2 relative to c² C0. Merely asserting an isolation flag is not evidence of (i).

An independent *two-state toy* with eigenratios (3q/4,q/4), source weights (1/8,1/8), certified remainder cap c=q/2 and top b=3q/4 yields a positive rational lower bound **1/20**, strictly below the actual first weight 1/8. This verifies the formula under genuinely explicit isolation assumptions.

For the original 4D source, the available WV01 numerical lower on C2 is still **0**, and no rank-one physical first-eigenspace isolation certificate has been constructed. The new acceptance gate therefore returns **HOLD**, independently of the strict analytic fact that C2>0. First spectral weight is an open mathematical task.

## 5. Engineering disposition and next physical research objective

The producer and separate independent tests verify all frozen numeric caps, exact 4×4 spectral counterexamples, the Gram determinant, point-mass equality cases, conditional first-projector dual, genuine original WV01 source binding, wrong-beta, negative weights, invalid spectrum, unordered isolation and attempted first-state promotion. All outputs have canonical deterministic HBP receipts and run under the repository's no-floating-point gate.

    python3 -B tests/test_ym4_wilson_first_projector_gram_gate.py -v
    python3 -B tests/ym4_wilson_first_projector_gram_gate.py

**Next physical certificate:** obtain a true original-operator *source-adapted* lower bound on C2 (or another higher moment), and a finite-rank physical Gauss/spin-network spectral projector that isolates the first excited physical subspace, with a quantified complement Schur/Feshbach resolvent bound. A source-visible excited mode could then be proved, compared to the physical first eigenvalue, and assigned its genuinely isolated Wilson weight.

The full continuum mass-gap and weak-coupling/volume-uniform obligations remain OPEN. These tighter fixed-L Wilson upper bounds help set rigorous truncation/error budgets but do not prove a continuum energy scale.
