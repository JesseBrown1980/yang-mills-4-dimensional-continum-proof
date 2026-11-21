# YM4-WG09 — exact second- and third-order SU(2) six-mode perturbative pilot
**21 November 2026. Evidence status: exact local Haar computation; finite-beta fourth-order remainder OPEN.**

This is a continuation of WG06–WG08 and draft PR #96's G48 symmetry orbital reduction. The exact original continuous-SU(2) 24-link, L=2 spatial Haar calculation uses quaternion coordinate tensors E(q_a q_b)=delta_ab/4 and E(q_a q_b q_c q_d)=(delta_ab delta_cd+delta_ac delta_bd+delta_ad delta_bc)/24. The 24-point Hurwitz rule supplies an exact fourth-order check. It is not a substitution of a finite group for SU(2).

## Second-order degenerate coefficient
Let E be the 42-state electric space, P_+ the six-dimensional magnetic +sqrt(8)/8 spectral projector, P_vac=|1><1|, and t=kappa_1(beta)^4. In the original isospectral operator J=K^(1/2)exp(beta V)K^(1/2), expand the 42-state vacuum-reduced Schur operator relative to t. Its beta^2 coefficient is H2=(1/2)E V² E - E V P_vac V E, plus the electric-tail correction.

Exact quartic SU(2) Haar contractions give, in the six normalized K4,2 Perron vectors,
    P_+ V² P_+ = (381/64) I_6 + J_6,
    P_+ V P_vac V P_+ = (1/2) J_6,
so P_+ H2 P_+ = (381/128) I_6. The 12 neutral two-link spin-one electric tail loops are the only additional order-beta^4 electric states (ratio kappa_2²/t -> 4/9). Their E-to-tail magnetic matrix elements vanish: link-center parity forces a basis plaquette i equal the inserted plaquette p; then chi_1(U_p)^2=1+chi_2(U_p), orthogonal under original linkwise SU(2) Haar to any *two-link* spin-one loop. Higher gauge-invariant electric states have total representation index at least six: on the bipartite cubic graph, Gauss center parity forces that index sum even. Hence K_R/t=O(beta²) on the remaining electric tail, giving no contribution to beta² or beta³ coefficients. (An explicit uniform constant for the remainder remains to be certified.)

**Result:** the sixfold magnetic-slope degeneracy survives through beta². Neither b nor c splits the six modes at second order.

## First possible splitting: third order
The original fourth-Haar rule is still sufficient for the nonvanishing terms in E V³ E, because any link appears at most five times in the five factors and Haar parity removes odd degrees. Exact enumeration finds sum of plaquette-double-winding and reverse (PD+DP) four-trace coefficients:
- 40 for each block's diagonal matrix element;
- 6 for each ordered pair of distinct blocks.

The beta³ vacuum subtraction is -sqrt(2)/8 in every six-mode entry, and cancels the direct off-diagonal V³/6 term. The remaining third-order splitting comes from H2-mediated coupling through the other 36 electric modes. With M=A/8, A³=8A, the complementary inverse is
    (mu_+ - M_Q)^(-1) Q = sqrt(2) P_- + 2 sqrt(2) P_0,
where P_- = A²/16 - sqrt(2) A/8 and P_0 = I - A²/8. Therefore the internal mixing is
    sqrt(2) P_+ H2 (P_- + 2 P_0) H2 P_+.
Its diagonal is (561/16384)sqrt(2), opposite-pair entry sqrt(2)/32, and other-axis entry sqrt(2)/64.

The complete leading **third-order coefficient** on the six positive-slope modes is exactly
    H3_eff = sqrt(2) [ (36499/49152) I_6 + (1/32) O + (1/64) X ].
Its three symmetry eigenvalues have multiplicities 1,2,3; the fully invariant eigenvalue exceeds the even sector by 3sqrt(2)/32 and the odd sector by sqrt(2)/8, in units of t beta³.

Both leading splitting signs are strictly positive. This gives **asymptotic positive third-order ordering** of the WG08 identified Wilson-coupled symmetric mode, subject to the genuine full-operator expansion and remainder validation. The actual first-neutral finite-beta spectral order is **HOLD pending an explicit, uniform fourth-order Schur/Feshbach bound**. We do not promote the asymptotic coefficient as a completed nonperturbative finite-beta ordering certificate.

## Reproduction and next acceptance
The hosted source in `tests/ym4_su2_six_perturbative_haar.py`, using the standard library and the repository-approved integer-pair `R` arithmetic, recomputes the 42-state and 48-action structure, exact linkwise second/fourth SU(2) moments, all 42x42 V² Haar elements, the three V³ orbitals, the vacuum and 36-state mixing coefficients. Its replayed deterministic HBP receipt has SHA-256 \`4ce90dd38ee088e580b4b95bbf549f88379f3a8a1e8dd0b0425b9c20537f53b4\`. Its source and HBP are committed in the atlas, and the dedicated [hosted WG09 original-SU2 Haar workflow](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/44947346077) has passed duplicate replay, exact receipt comparison, SHA-256 verification and the repository no-floating-point source gate. A separate independently authored clean-room third-order Haar calculation and the finite-beta full-operator remainder remain OPEN.

**Next:** bound the exact fourth-order remainder of the full physical transfer and Schur complement (including the 12 spin-one states and the complete higher-spin tail) with constants strong enough to preserve the strict third-order gaps at a specified rational beta cutoff. Then combine that finite-beta ordering with WG08's positive true-vacuum Wilson overlap. Large volume, continuum limit, OS reconstruction, and uniform mass gap remain OPEN.

## Explicit fourth-order acceptance budget

Let the fully symmetry-reduced, vacuum-and-tail-corrected six-mode effective transfer divided by the electric scale t be compared with the exact third-order polynomial

    I + (sqrt(2)/4) beta I + (381/128) beta^2 I
      + beta^3 sqrt(2) [ (36499/49152) I + (1/32) O + (1/64) X ].

A sufficient final gate is a *proved* operator-norm remainder

    ||H_six(beta) - H_poly(beta)|| <= C beta^4,

valid for 0<beta<=beta0, with the precise energy-dependent Schur/Feshbach identification and all physical tail sectors controlled. This formula is a target, not an established remainder estimate.

The smallest third-order symmetry splitting is 3sqrt(2)/32, strictly larger than 21/160 because sqrt(2)>7/5 (verified by 2>49/25). Weyl's inequality gives the guaranteed leading-sector separation

    normalized_gap > beta^3 [21/160 - 2 C beta].

Therefore, once an exact rational constant C>0 and its validity interval beta0 are accepted, taking

    0<beta <= min(beta0, 1/1000000, 21/(640 C))

makes the bracket strictly larger than 21/320 and yields a strictly positive symmetry-order gap in the normalized six-mode transfer. The actual physical eigenvalue gap is that estimate multiplied by t and the common positive Wilson magnetic factor.

This is a ready-to-check acceptance inequality for the next WG09 certificate. The unresolved work is to produce **C** and prove its uniform validity from the original infinite-dimensional operator; no numerical value for C is asserted here.
