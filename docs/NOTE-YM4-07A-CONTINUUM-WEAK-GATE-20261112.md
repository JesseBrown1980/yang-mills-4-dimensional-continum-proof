# YM4-07A — physical weak-coupling continuum first-gap gate and exact falsifiers

**2026-11-12. Priority:** the actual open four-dimensional continuum Yang–Mills mass gap. This note **does not solve** that problem, does not claim a new literature result, and must not be taken as an extension of the β=1/8 finite-volume theorem to weak coupling. The official Clay status was **unsolved** when checked on November 12, 2026: https://www.claymath.org/millennium/yang-mills-the-maths-gap/. No finite-lattice CI result can override the missing continuum argument.

**Prediction provenance:** 24 frozen rows in `docs/PREDICTION-YM4-07A-CONTINUUM-WEAK-GATE-20261112.hbp`, committed as the first file on this branch at `b99c9dbf21e2c93c2946c50fdacfa231b9704c9f`, before the hosted checker. **Caveat:** unlike the earlier blind-seat prediction freezes, a local proof/prototype and rational test were executed before GitHub filing. This is an *immutable hosted-replay freeze*, not an independent blind forecast. No main/PR #65–69 or finite r=9 branch is modified.

## 1. The physical-time target — the quantity that must survive

Let a_k=a_0/3^k, let β_k be the bare isotropic coupling on an asymptotically free continuum trajectory (β_k→∞), and take spatial sizes L_k such that physical spatial extent a_k L_k→∞, or prove infinite-volume first in an equivalent compatible order. Set the normalized one-step *full center-neutral physical* transfer P_k=T_k/λ_0(T_k), with first neutral nonvacuum ratio r_k. A sufficient finite-cutoff gap target is

    inf_k {-log(r_k)/a_k} >= m_* > 0,
    equivalently r_k <= exp(-m_* a_k).

**But this is not alone a Clay proof:** independently construct a **nontrivial** continuum limit of renormalized gauge-invariant local Schwinger functions satisfying suitable Osterwalder–Schrader axioms and show the physical-time semigroups/observables converge into that nontrivial OS Hilbert space. Under this assumption a full nonvacuum norm estimate passes to the reconstructed semigroup and yields spec(H)|_{Ω⊥}≥m_*. The local sector must be dense in the reconstructed vacuum Hilbert space; selected-loop decay alone is insufficient. The fixed finite-torus first charged winding/torelon gap is **not** the desired local center-neutral gap.

The **other side matters, too**: an unrenormalized fixed nonzero lattice-unit gap, r_k≤q<1 for all k, would give P_k^{floor(t/a_k)}→|Ω_k⟩⟨Ω_k| for every t>0. In a nontrivial common continuum Hilbert space this cannot be a strongly continuous semigroup at t=0. It is therefore invalid to market an arbitrarily large physical gap from a fixed β strong-coupling r<1 as a nontrivial continuum theory. This argument assumes vacuum-compatible maps and strong semigroup convergence; the mere inequality r≤q does not by itself construct the limit.

For the familiar SU(2) Wilson convention β=4/g_0², one-loop asymptotic freedom predicts approximately β(a)~(11/(3π²)) log(1/aΛ) up to subleading logs and nonperturbative scale-setting. This is a **perturbative direction**, not an exact certified RG trajectory. Background SU(N) b0=11N/(48π²) and a→0 at g→0: https://library.oapen.org/bitstream/handle/20.500.12657/50492/9789814365871.pdf?isAllowed=y&sequence=1 . The integer checker uses an explicitly **artificial growing proxy** β_k=2+k only to falsify inappropriate extrapolation of sufficient conditions.

## 2. Actual all-β pure-temporal SU(2) representation reference (known mathematics)

The normalized SU(2) Wilson temporal link convolution has eigenvalues t_n(β)=I_{n+1}(β)/I_1(β), n≥0, β>0, with t_0=1. The **classical** modified-Bessel Turán inequality

    I_j(β)^2 > I_{j-1}(β) I_{j+1}(β) > 0  (j>=1, β>0)

says adjacent ratios I_{j+1}/I_j decrease strictly with j. Thus, with u=I_2/I_1=t_1∈(0,1),

    0<t_n = prod_{j=1}^n I_{j+1}/I_j < u^n (n>=2).

This is an imported, published special-functions inequality, **not a new mathematical proof by this verifier**. A reference with proof is Á. Baricz et al.'s cited Turán literature and Z.-H. Yang & J.-F. Tian, *Convexity of ratios of the modified Bessel functions ...* (2022), freely available at https://pmc.ncbi.nlm.nih.gov/articles/PMC9361280/. The independent checker re-evaluates the inequalities in exact rational positive Bessel-series intervals at β=2,4,8,16 for orders through 14, but finite samples do **not** prove the all-β theorem.

On a 3D periodic **side-2** spatial lattice, every nonconstant physical spin-network must contain a cycle. The shortest cycles have two links and are noncontractible winding loops. A fundamental two-link loop is spatial-center charged and has eigenvalue u². In the center-neutral sector, two-link loops require even irrep n≥2, with eigenvalue t_n²<u^{2n}≤u^4. A four-link fundamental plaquette is neutral and has eigenvalue **exactly u^4**. Every other neutral support uses ≥4 occupied nontrivial links, with eigenvalue ≤u^4. Consequently for **all β>0 in the pure-temporal model (β_s=0)**,

    λ_{1,physical}(B)=u²,   λ_{1,neutral}(B)=u⁴.

This correctly extends the *electric reference ordering* beyond β=1/8, but it is **not a proof about the isotropic spatially interacting transfer**, in which β_s=β_t=β. The center-sector separation persists because the full transfer commutes with the one-form center symmetry; the exact eigenvalue ordering need not survive without an independent interacting estimate.

## 3. Precise existing-method failure at isotropic β=2

For L=2 (N_s=24), the interacting Wilson spatial factor A gives the trivial global comparison 0<A≤1 and A≥e^{-96} at β=2. The improved SU(2) Haar vacuum floor in 06H gives λ0(T)≥(37/25)e^{-48}, with the neutral excited upper bound λ1,neutral(T)≤u^4 from the full-sector min–max comparison. The ratio ceiling produced by these bounds is therefore u^4 / [(37/25)e^{-48}]. The **checker verifies this ceiling is >1**, by rigorously verifying u>2/5 and

    (37/25)e^{-48} < 37/(25*1201) < (2/5)^4 < u^4.

Thus **at β=2 the currently proved ratio upper is vacuous**, even though the actual finite isotropic transfer may have a positive spectral gap. This is a demonstrated breakdown of the *certificate*, **not** a gap closure in Yang–Mills. The 06F Fourier tail can be arbitrarily small with a high cutoff N; it does not bound the actual interacting second eigenvalue sharply enough.

Likewise, the earlier volume-independent **sufficient** Dobrushin coefficient upper bound from draft PR #57 is α_bound=9β at isotropic β_s=β_t=β. At β≥2, the sufficient α_bound<1 test is **NOT MET**. The failure of the upper-bound criterion does not mean the true conditional influence α≥1, nor does it disprove a physical mass gap. A wholly different weak-coupling/local-field method is required.

## 4. Seven explicit counterfamilies and limit controls

Use normalized P_k and n=3^k lattice ticks per one unit of physical time:

1. **Finite nonzero mass:** r^A_k=n/(n+1). Then m^A_k=n log(1+1/n)→1 and (r^A_k)^n→e^{-1}. The exact checker verifies 1/3 < (r^A_k)^n ≤1/2 through k=7.
2. **Gap collapse:** r^B_k=n²/(n²+1). Then m^B_k=n log(1+1/n²)→0 and (r^B_k)^n→1. It verifies the exact Bernoulli lower bound (r^B_k)^n>1-1/n.
3. **Infinite physical mass / vacuum-only positive-time limit:** r^C_k=1/2. Then m^C_k=n log2→∞ and (r^C_k)^n→0.
4. **Dark-state deception:** a complete positive transfer diag(1,r^A_k,r^B_k) has true first ratio r^B_k for n>1, although a chosen center-neutral observable overlapping only the r^A_k state has stable decay mass 1. This demonstrates that local witness decay cannot be naively promoted to the *full finite-lattice* spectral gap; it also illustrates why the continuum Hilbert-space limit and density of observables must be specified.
5. **Physical space:** L_k=2*3^k has a_k L_k=2, not infinite volume. L_k=2*3^{2k} gives a_k L_k=2*3^k→∞; for the latter the actual spatial plaquette census is 24*3^{6k}. Keeping L=2 while letting a→0 is even further from physical R³.
6. **Sufficient-coupling criterion:** the proxy β_k=2+k produces α_bound=9(2+k)>1 at every k. It is only the known Dobrushin *test* that fails, not the Yang–Mills theory.
7. **Known special-functions ordering versus interacting spectral uncertainty:** all tested β=2,4,8,16 satisfy strict Turán and t_n<u^n with exact positive-series interval arithmetic; a false assertion reversing those inequalities is detected. This baseline is not a weak-coupling interacting spectral bound.

All intentionally wrong inputs must fail with named diagnostics. No probabilistic Monte Carlo, hidden floating-point calculations, Q8 substitution, JSON or external network dependency is used in the checker.

## 5. Exact work required to cross the open boundary

The first *unproved theorem* to target is a nonextensive scale-to-scale **interacting full-neutral transfer comparison** along genuine SU(2) β_k→∞, with physical a_k→0 and L_k a_k→∞. The exact abstract Schur machinery on draft PR #66 can turn certified retained, leakage and dark complement estimates (u_k, ζ_k, ρ_k) into r_{k+1}≤τ_k. A sufficient triadic relative budget, from draft PR #65, is

    r_{k+1} <= r_k^(1/3) (1+x_k), x_k>=0,
    sum_k log(1+x_k)/a_{k+1} < m_0.

Then m_K≥m_0-sum_{k<K}log(1+x_k)/a_{k+1}>0. The algebra is correct; **the missing physically noncircular estimate** is bounding τ_k and x_k **without inserting the unknown true mass gaps** and with the whole center-neutral physical complement controlled. It must be robust at β_k large, not based on e^{-cβN_s} or small-β Dobrushin conditions. A useful first deliverable would be one explicit β=2, L=2 interacting neutral second-eigenvalue upper bound strictly below a comparably certified leading eigenvalue, and a credible local mechanism whose constants do not deteriorate with L or k. Neither exists in the current verified PR sequence.

Separately, a continuum proof needs renormalized local field/Schwinger-function convergence (possibly via a compatible infinite-volume route), OS positivity and reconstruction, nontriviality and strong semigroup convergence. A physical mass gap alone on finite regulators is not enough. These are **distinct mandatory independent proof gates**, not TODOs that can be assumed away.

**Evidence boundary:** analytic model comparisons and exact rational sample checks are verified independently as algebra; universal Bessel Turán and OS reconstruction are imported classical results and must be cited; the interacting β(a)→∞ mass bound and continuum existence are **OPEN**. Keep PR DRAFT; do not merge old #67–69 or modify the finite Round 5 / r=9 launch HOLD.