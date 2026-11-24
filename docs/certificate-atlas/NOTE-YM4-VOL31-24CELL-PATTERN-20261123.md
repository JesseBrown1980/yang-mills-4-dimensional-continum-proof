# YM4 VOL31 — exact 24-cell recurrence and two-ended four-sphere band signature

**23 November 2026 · exact integer geometric theorem, 20-frame certificate.** This note recognizes and independently certifies the visible repeated band structures in the existing [VOL30 two-ended 3D spherical Fischer player](vol30-spherical-fischer.html). The point cloud is the original **four-dimensional integer lattice geometry**, with continuous SU(2) gauge variables only in the *separately proved* Wilson Gibbs formulas of VOL30. This stage establishes a deterministic pattern fingerprint to test against later actual field measurements.

## 1. What repeats in the displayed 4D spherical shells

Define the original exactly enumerated integer-lattice sphere
\[
  S_R=\{x=(x_0,x_1,x_2,x_3)\in\mathbb Z^4:
      x_0^2+x_1^2+x_2^2+x_3^2=R^2\}.
\]
The geometric pattern visible in the 3D projection is especially strong for \(R=2,4,8,16\). In fact the **exact 4D sets** satisfy
\[
 \boxed{S_{2^k}=2^{k-1}S_2,\qquad
        |S_{2^k}|=24\quad(k\ge1).} \tag{31.1}
\]
The base set, in integer coordinates, has precisely two disjoint classes:
\[
 S_2=
 \underbrace{\{\text{8 coordinate permutations of }(\pm2,0,0,0)\}}
                _{\text{8 axial vertices}}
 \ \cup\
 \underbrace{\{(\pm1,\pm1,\pm1,\pm1)\}}
                _{\text{16 diagonal vertices}}. \tag{31.2}
\]
Its normalized set \(S_2/2\) is the vertex set of a **regular 24-cell** on the unit three-sphere \(S^3\subset\mathbb R^4\), and equally the **24 Hurwitz unit quaternions** of the binary tetrahedral group. This connects directly to the **24 Hurwitz points previously used only for exact continuous-Haar moment cubature** in VOL23–25: the two computations use identical 24 normalized quaternion addresses. The group/24-cell relationship is classical geometry; the application as an explicitly frozen pattern across these spherical-player frames is new *within this project*. The 24-point finite set is a geometric/cubature witness and is not substituted for the original continuous SU(2) Wilson Gibbs measure.

**Elementary proof of (31.1).** Squares modulo 8 are only \(0,1,4\). If four integer squares sum to a multiple of 8, the number of odd coordinates must be zero: with 1,2,3 odds, the odd contribution cannot be canceled by multiples of 4, and with 4 odds the sum is 4 modulo 8. Therefore if \(R=2^k,\ k\ge2\), every component of a point of \(S_R\) is even, since \(R^2=4^k\) is divisible by 8. Divide every coordinate by 2 to obtain a bijection \(S_{2^k}\leftrightarrow S_{2^{k-1}}\). Repeat down to \(S_2\). Equation (31.2) explicitly enumerates 24 base points. This proof is independent of the general classical Jacobi four-square formula, which also yields 24 for any even power of 2; see NIST DLMF §27.13 and the classic 24-cell coordinates.

## 2. Five identical 4D bands, with an exact size signature

The true 4D x2-coordinate slices of every \(S_{2^k}\), \(k\ge1\), have only **five distinct levels**. In normalized shell coordinates, they are
\[
 \boxed{\begin{array}{c|ccccc}
 x_2/(2^{k-1}) & -2&-1&0&1&2\\
 \text{point count} &1&8&6&8&1
 \end{array}}. \tag{31.3}
\]
The repeated **1–8–6–8–1** band signature and the 8+16 axial/diagonal orbit split are mathematically exact, not an impression created by the 3D camera. These counts are preserved by every 9-step/20-step Bobby Fischer freeze-and-rewind. The original viewer's declared 4D-to-3D projection changes depth and visual density; the certificate refers to the preserved original \(x_2\) coordinates.

For all **twenty** frames \(R=2,\dots,21\), the [strict integer verifier](../../tests/ym4_vol31_pattern_verify.py) independently enumerates the complete original four-square point sets, the per-level 4D histogram, total site counts, opposite-end reflection and shared shell sites. It cross-references the frozen [VOL30 20-frame inventory](YM4-VOL30-SPHERE-FRAMES-20261123.json) by exact expected counts.

## 3. The midpoint contact and the R=16 gap

Keep the two original endpoints \(c=(0,0,0,0)\) and \(z=(0,0,24,0)\) in the VOL30 original even 4D torus with L=128. A point lies on both radius-R integer spherical shells if and only if
\[
 \|x-c\|^2=\|x-z\|^2=R^2
 \iff
 x_2=12,\quad x_0^2+x_1^2+x_3^2=R^2-144. \tag{31.4}
\]
At \(R=12\), the unique shared site is \((0,0,12,0)\). At \(R=16\) the residual is \(112=16\cdot7\), which cannot be expressed as a sum of three integer squares: a sum of three squares divisible by 4 must have all components even; apply this twice to reduce 112 to 7, whose three-square representation is impossible modulo 8. Thus
\[
 \boxed{|S_{12}(c)\cap S_{12}(z)|=1,\quad
 |S_{16}(c)\cap S_{16}(z)|=0.} \tag{31.5}
\]
The ideal smooth four-dimensional Euclidean spheres intersect for R>12, but their lattice **exact-radius** sampled integer shells can still have zero shared points; this is an arithmetic selection rule, not an interruption of physical field propagation.

The first shared point occurs during the **20-step R2–R21** playback, while the **9-step R2–R10** playback ends before contact. Both forward and reverse runs reconstruct the same canonical four-dimensional coordinates and stage-specific shell counts.

## 4. Quantitative full-frame geometric measurement and next physical acceptance

The strict integer checker and frozen receipt report each \((R,|S_R|,J_R,L_R)\), where \(J_R\) is the exact intersection count of the two four-dimensional shells and \(L_R\) is the number of nonempty \(x_2\) bands. Three independent methods check the geometric fingerprint: two-square composition for \(|S_R|\), three-square direct enumeration for \(J_R\), and exact reflection \(x_2\mapsto24-x_2\). The four power-of-two frames are also compared **set for set**, not merely by point counts, to dilations of \(S_2\). This provides a 20-step exact geometric pattern certificate.

**Conformity conclusion:** The geometry is fully certified for the finite 4D lattice chart and is consistent with the continuous SU(2) mathematical **link-group** model used in VOL30; the 24 normalized vertices also match VOL23's Hurwitz/SU2 Haar-moment test addresses. The regular 24-cell and Jacobi identities are established mathematical structures, not a newly proved physical Yang–Mills phenomenon.

**Physical measurement acceptance:** Quantitative original continuous-SU2 gauge-field expectation values on each shell, the true two-ended predictors \(W_R\), a source-specific physical radial-correlation profile, upper exponential decay, beta(a), and all eleven continuum-construction gates remain **OPEN**. The next numerical test must compare *independently computed Wilson observables*, not just site counts, with the predicted symmetry and the already certified two-sided correlation interval. No field spectrum is inferred from a 24-cell point arrangement.

**Artifacts:** the strict integer test, [VOL31 frozen geometric receipt](YM4-VOL31-SPHERICAL-PATTERN-20261123.hbp), [VOL30 3D forward/reverse player](vol30-spherical-fischer.html), [candidate certificate atlas](index.html#ym4-vol30-candidate), and a separate hosted replay. Preserve \`main\` and the production 115-node accepted atlas inventory while the research candidate undergoes review.
