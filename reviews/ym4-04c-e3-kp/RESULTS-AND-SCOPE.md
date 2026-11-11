# YM4-04C E3 — frozen C05, C06 and C14 coupling edges, independently certified

**November 11, 2026. Status: exact arithmetic reproduced, NOT a new blind prediction.** The original 42-line YM4-04C prediction at commit \`6ebf63272ae230bfb08ef48b3156cb4202c24627\`, SHA256 \`c74e6388295a6309674268dd18deba3728a4eb627a1530c42054182b2fadc404\`, remains untouched. Its C05/C06/C14 rows were tagged \`prefreeze=COMPUTED\`. The refined polymer head (C03) was independently reproduced in stacked draft PR #60 on \(8^4,12^4\), all three off-link classes through \(n=12\), and has status \`prefreeze=CROSS_READ\`.

## 1. The frozen sufficient certificate — not the actual infinite sum

Define
\[
 F_{20}(n)=\frac{\binom{20n}{n}}{19n+1},\quad
 \mu=\frac{20^{20}}{19^{19}},\quad
 c_0(\beta)=\sum_{m=0}^\infty
   \frac{(\beta^2/4)^m}{m!(m+1)!},
\]
\[
 \varepsilon_6(\beta)^6
 =\sum_{j=0}^6(-1)^{6-j}\binom6j
 \frac{c_0(j\beta)}{c_0(\beta)^j}.
\]
The exact finite C03 counts give
\[
 (N_4,\ldots,N_{10})=(1,0,12,0,32,32,304).
\]
The *crude* head is \(N_n=6F_{20}(n)\); the *headfree* lower comparison is \(N_n=0\), \(4\le n\le10\).

At \(x=\varepsilon_6(\beta_0)\exp(2\alpha+\theta)\), the **frozen certified upper majorant**, not the sharper actual infinite sum, is
\[
 U_N(x)=\sum_{n=4}^{10}N_nx^n
 +\sum_{n=11}^{48}6F_{20}(n)x^n
 +\underbrace{\frac{6F_{20}(49)x^{49}}{1-\mu x}}_{\text{mandatory n=49 geometric tail}},
 \qquad \mu x<1.
\]
The C0 certificate reads MET when **some** \(0<\alpha\le1/4,\ \theta\ge1/4\) satisfies the pole gate and \(U_N(x)\le\alpha\). It reads NOT_MET when the stated majorant has **no** qualifying pair.

This distinction is essential: because \(F_{20}(n+1)/F_{20}(n)<\mu\), \(U_N(x)\) bounds the true polymer power series *from above*. A NOT_MET of \(U_N\) does **not** imply that the actual infinite series, a sharper KP certificate, or the physical gauge theory fails. The pole at \(\mu x=1\) is a singularity of the chosen bounding expression, not a physical phase transition.

Both exact engines test **that same frozen \(U_N\)**, including the \(n=49\) tail in its upper AND lower outward-rounded enclosures. This resolves a subtle trap: using a tighter \(n=1000\) series and claiming MET beyond these frozen NOT_MET edges would change the certificate, not refute the frozen statements.

## 2. Exact MET and NOT_MET proofs

The new engine \`tests/test_ym4_04c_e3_kp_edges.py\` uses **256-bit scaled integer intervals**, positive Taylor sums with explicit geometric remainder for \(\exp\) and \(c_0\), exact sixth-power binomial enclosures and integer bisection for \(\varepsilon_6\). Every intermediate multiplication, division and root enclosure rounds outward. No floating-point, decimal/fractions library, unsafe, Node/V8 or JSON is involved.

For a MET result, it gives an explicit rational \(\alpha\) such that the *upper* endpoint \(U_N^+(\varepsilon_6^+\exp(2\alpha+1/4)^+)\le\alpha\) and the pole is avoided. At \(\theta=1/4\), the following points are checked:

| Frozen row | Head | \(\beta_0\) | Read | Explicit witness / proof |
|---|---|---:|---|---|
| C05 | crude | 0.01904 | MET | \(\alpha=200/4000=0.05\) |
| C05 | crude | 0.01905 | NOT_MET | Global convex tangent certificate |
| C05 control | crude | 0.02 | NOT_MET | Global convex tangent |
| C06 control | refined | 0.02 | MET | \(\alpha=25/4000\) |
| C06 | refined | 0.02075 | MET | \(\alpha=78/4000\) |
| C06 | refined | 0.02076 | NOT_MET | Global convex tangent |
| C06 universal head bound | headfree | 0.02076 | NOT_MET | Global convex tangent |

For NOT_MET, set \(g(\alpha)=U_N(\varepsilon_6e^{2\alpha+1/4})-\alpha\), a convex function on the finite pole-free domain because \(U_N\) has nonnegative coefficients. At an exact rational trial point \(\alpha_m\), the engine encloses \(g(\alpha_m)\) and \(g'(\alpha_m)=2xU_N'(x)-1\). The convex supporting-line inequality, uniformly for \(0\le\alpha\le1/4\),
\[
 g(\alpha)\ge g^-(\alpha_m)
 - \max(|g'^-(\alpha_m)|,|g'^+(\alpha_m)|)
   \max(\alpha_m,1/4-\alpha_m),
\]
has **strictly positive** certified right side at each stated NOT_MET point. The lower-bound witnesses include:
- C05 crude \(\beta_0=0.01905\), \(\alpha_m=0.053646938852\): global margin \(>0.000014227943\);
- C05 crude \(\beta_0=0.02\): margin \(>0.024350135988\);
- C06 refined \(\beta_0=0.02076\), \(\alpha_m=0.020978393291\): margin \(>0.000112354444\);
- C06 headfree \(\beta_0=0.02076\): margin \(>0.000112244854\).

For larger \(\theta\), \(x\) increases and \(U_N\) is nondecreasing in \(x\); thus **C05/C06** MET feasibility is strongest at \(\theta=1/4\). The interpretation of these pointwise brackets as the largest \(\beta_0\) on the complete \(10^{-5}\) grid uses the frozen monotonicity lemma 3.32, a named mathematical input to the final release.

## 3. C14 has an additional threshold, not merely C0 feasibility

For the frozen G0/G1 constants \(\kappa=1/4\) and \(\delta_1=6\alpha_-(\theta=1/4)\), the self-map threshold is defined by
\[
 \delta'=\delta e^\delta,\qquad
 \lambda(\delta)=\delta'+\log(1+\delta')\le\kappa.
\]
Exact integer Taylor and \(\log(1+u)=2\sum_{k\ge0}\frac{(u/(2+u))^{2k+1}}{2k+1}\) enclosures certify
\[
 \boxed{0.114846768<\delta_{\rm crit}<0.114846769}.
\]

Exact least-root bracketing (a NOT_MET lower root and MET upper root) yields:

| \(\beta_0\) | Refined \(\delta_1\) enclosure | Self-map |
|---:|---|---|
| 0.02074 | \(0.1088558495475\) | MET |
| 0.02075 | \([0.1158911083192,0.1158911083193]\) | NOT_MET |
| 1/64 | \([0.0010173855728,0.0010173855729]\) | MET |

The lower headfree control yields \(\delta_1\ge0.1158861245891>\delta_{\rm crit}\) at \(\beta_0=0.02075\). Thus the C06 one-step read remains MET at that coupling, but the stricter C14 self-map read is NOT_MET. Frozen C14's full \(\theta\)-optimization claim uses note Lemma 3.31; the conversion of arithmetic to the all-\(k\) blocked-action theorem remains **conditional on the independent acceptance of G0 and G1**.

## 4. Separate independent checker, C04 attack and limits

\`reviews/ym4-04c-check/e3_kp_second_seat.py\` uses the **previously authored second-seat** \`ilib.py\`, \`polylib.py\` and \`g1lib.py\` in \`reviews/opus55-ym4-04c-g-attack/L5-numbers/\`. It does not import, share interval operations with or copy the new 256-bit engine. It recomputes the same C05/C06 witness inequalities, global C05/C06 NOT_MET tangents, the independent \(\lambda(\delta_{\rm crit})\) crossing and the C14 threshold conditions at **640-bit integer precision**.

The separate C04 guard verifies \(\mu\varepsilon_6 e^{1/4}>1\) at \(\beta_0=1/40\) and \(0.02248\), before any C05/C06/C14 reads. The planted \`missing_tail\` fault now actually substitutes the *head-only* certificate and drops the pole guard; that mutant spuriously reads MET at \(\beta_0=1/40,\alpha=2^{-22}\), and the true C04 guard **must reject it**. Other deliberate faults choose a crude head in place of refined, flip NOT_MET to MET, and falsify the upper \(\delta_{\rm crit}\) side. These are section-specific faults, **not the complete 12-fault YM4-04C release matrix**.

The initial hosted run passed both independent E3 routes and all four controls. The final-head gate must also regenerate all three committed engine/second-seat/manifest receipts byte for byte. The inherited \`no-float-list-unchanged\` human-review failure from the separate original evidence chain is **not bypassed**.

**Still open:** E4 full \(c_{\rm fin}\) and all-step contraction, E5 remaining edge points, E6 gauge integrals, the W lane, the full independent native Rust YM4-04C checker and complete E0–E9 gates. This certified finite strong-coupling window neither establishes the physically matched weak-coupling trajectory nor proves a continuum Yang–Mills mass gap. The separate 3×4 S₃ r=9 blind run remains untouched. No merges are authorized by this reproduction.
