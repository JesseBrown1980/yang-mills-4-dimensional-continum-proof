# YM4-04C staged engine: E2g/C04 Fuss–Catalan polymer tail

**2026-11-11. A first executable stage of the frozen YM4-04C engine, not the completed YM4-04C project.** This work is stacked on the independently filed G-attack in PR #46, which itself targets the 42-line freeze at commit \`6ebf63272ae230bfb08ef48b3156cb4202c24627\`. The first 42 prediction rows are reproduced byte-for-byte with original SHA256 \`c74e6388295a6309674268dd18deba3728a4eb627a1530c42054182b2fadc404\`. The freeze and attack are not amended.

## What is actually computed

The frozen polymer certificate uses \(\varepsilon_6(\beta)=\|K\|_{L^6(SU(2))}\), with \(K=e^{\beta a}/c_0(\beta)-1\), \(a(U)=\tfrac12\mathrm{ReTr}U\), \(c_0(\beta)=\int e^{\beta a(U)}\,dU\), and the Fuss–Catalan growth constant \(\mu=20^{20}/19^{19}\). For the KP tail, \(x=\varepsilon_6 e^{2\alpha+\theta}\), where \(\alpha\ge0,\theta\ge1/4\); the frozen tail is only defined when \(\mu x<1\).

The first engine computes exact positive-series *rational intervals*
\[
 c_0(\beta)=\sum_{m\ge0}\frac{(\beta^2/4)^m}{m!(m+1)!}
\]
using nine-degree partial sums and a rigorously bounded positive geometric remainder. Independently it encloses \(\exp(1/4)\) by positive rational Taylor sums and a geometric remainder. It then derives the exact interval for
\[
 \varepsilon_6(\beta)^6=
 \sum_{j=0}^{6}(-1)^{6-j}\binom6j
 \frac{c_0(j\beta)}{c_0(\beta)^j}.
\]
No numerical floating-point evaluation, estimated cancellation, unguarded negative exponent, or discarded tail enters the comparison. Strict tests are made on the **sixth power**, not by taking an approximate sixth root. The printed decimal sixth-root brackets are *display only*, derived by integer bisection with outward rounding.

| Bare coupling \(\beta_0\) | Certified \(\mu e^{1/4}\varepsilon_6\) bracket | C04 conclusion |
|---|---|---|
| 1/40 = 0.025 | (1.112522354, 1.112522355) | **Tail pole already crossed:** C0 NOT_MET |
| 0.02247 | (0.999913588, 0.999913589) | Pole **not** crossed at \(\alpha=0,\theta=1/4\), but MET is **not** established |
| 0.02248 | (1.000358668, 1.000358669) | **Tail pole already crossed:** C0 NOT_MET |

The first and third comparisons strictly exceed the **original frozen** thresholds \(1.1125\) and \(1.00035\) without changing those thresholds.

The source-disjoint check under \`reviews/ym4-04c-check/\` computes the same integral via the **SU(2) even Haar moments** \(\mathbb E[a^{2m}] = \mathrm{Catalan}_m/4^m\), with a different positive series and a different geometric-tail bound. It independently certifies the same three *inequalities*, not merely the engine's receipt hashes. This is a partial independent numerical proof check, **not** the final independent Rust 1.81 checker prescribed for all of YM4-04C.

## Tests, integrity and faults

The hosted workflow verifies original 42-line freeze SHA, G-attack PR #46 ancestry, both exact code paths, the existing comprehensive no-float source gate, and three fail-closed faults. The faults are (1) removing the Fuss–Catalan tail and its mandatory pole condition, (2) falsely asserting the wall at 0.02247 has already crossed, and (3) substituting the wrong Fuss–Catalan growth constant. Both receipts and SHA256SUMS are committed in \`evidence/\`; final-head CI regenerates and compares all three byte-for-byte.

The C04 numbers were tagged \`prefreeze=COMPUTED\` in the original 42-line freeze. **They are therefore reproducibility checks, NOT new blind predictions.** No confirmed-prediction counter is incremented.

## Blockers not hidden by this PASS

- The comprehensive YM4-04C engine (\`E0\`–\`E9\`, \`C01\`–\`C19\`, \`W01\`–\`W07\`) is **not** implemented or run by this stage. In particular **C03 refined polymer counts to n=12** and the G0/G1 all-\(k\) contraction readouts remain unverified by the staged engine.
- Original pre-freeze scratch artifacts and full three-manifest replay are in **separate, still-open PR #45**. This branch does **not** silently copy, discard or claim to have replayed those files.
- The full independent Rust checker, all planned 12 sabotages, four false claims, and twice clean full run are **OPEN**.
- Passing a **strong-coupling** polymer-tail test does not show a weak-coupling continuum trajectory or positive 4D continuum mass gap. The C04 pole identifies where this particular positive tail certificate stops, not a physical phase transition.
- The separate frozen 3×4 S₃ r=9 one-shot is not launched.

**Next executable stage:** E0 4D link/off-link incidence and exact exhaustive small polymer counts, then E1/C03 closed-set counts, followed by E3 KP search (and independent Rust counterpart) and only then the broader engine/receipt gate. The original freeze, corrected G-attack and separate PR #45 evidence must remain attributable.
