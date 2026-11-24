# YM4 VOL34 extension — exact periodic-sphere alias and controlled L8 screening

**24 November 2026 · original continuous SU2 finite Wilson model · exact integer geometry / provisional independent Metropolis sampling.**

## 1. New exact geometric correction: a one-site periodic alias at L6

The genuine original two-ended Wilson shell-average covariance uses a **periodic** four-dimensional spatial-site displacement histogram. The exact common-plaquette coefficient \(J=|S_R(c)\cap S_R(z)|\) must be computed in the **actual periodic L lattice**, not copied from an infinite lattice or a previous volume.

For an R=2 original 4D Euclidean integer shell and transfer-axis endpoint separation d=2, the **unwrapped** shared integer sites satisfy \(x_2=1\) and \(x_0^2+x_1^2+x_3^2=3\), giving exactly eight solutions \((\pm1,\pm1,1,\pm1)\). On the L6 torus, a *ninth* shared site appears because the central sphere point \((0,0,-2,0)\equiv(0,0,4,0)\pmod 6\) coincides with the outer sphere point \((0,0,2+2,0)\). This extra alias disappears on L8 and L10. Therefore:
\[
 \boxed{J_{R=2,d=2}^{L=6}=9,\qquad
        J_{R=2,d=2}^{L=8}
       =J_{R=2,d=2}^{L=10}=8.} \tag{34.1}
\]
The four original R1/R2,d2/d3 spherical cases have exact \((N,J,\text{unique displacement bins})\):

| L | R1,d2 | R1,d3 | R2,d2 | R2,d3 |
|---:|---|---|---|---|
| 6 | (8,1,33) | (8,0,33) | (24,9,129) | (24,0,129) |
| 8 | (8,1,33) | (8,0,33) | (24,8,165) | (24,0,165) |
| 10 | (8,1,33) | (8,0,33) | (24,8,169) | (24,0,169) |

The [new strict integer checker](../../tests/ym4_vol34_periodic_alias_verifier.py) independently re-enumerates these twelve original periodic cases, all exact ordered pair counts, the zero-displacement histogram bin, the eight unwrapped shared solutions and the unique L6 alias. Its [frozen HBP](YM4-VOL34-PERIODIC-ALIAS-20261124.hbp) is accepted **as exact lattice geometry**, independent of all numerical field measurements.

**Scientific consequence:** the true same-plaquette diagonal term is \(J K_\beta(0)/N^2\). Using the L6 value \(J=9\) for L8 would **oversubtract** exactly one true self-covariance per 576 ordered pairs, falsely creating a negative L8 residual of about \(-K_\beta(0)/576\). The L8 numerical reconstruction below uses the corrected **J=8**. The new finite-size geometry is itself a useful certificate for screening periodic-wrap artifacts.

## 2. Completed L8 Metropolis screening, with separate Haar controls

The same independent continuous-SU2 C++17 original Wilson Metropolis engine and original 4D direct-vs-histogram spherical measurement program used in VOL34 was applied at **even L=8**, with the same beta-two coupling and original transfer direction x2. Here d=3 is **shorter than half the periodic temporal extent** L/2=4, whereas d=3=L/2 on L6.

- beta two: **three complete independent seeds** 15211, 15313, 15427, 1,000 thermalization sweeps each, 280 saved configurations per seed separated by four complete sweeps, **840 saved configurations** in total.
- beta zero: **three separate independent Haar-control seeds** 16211, 16319, 16433, each with 20 refresh sweeps and 280 independent-Haar configurations, **840** total.
- A fourth interacting seed 15541 was interrupted after only 95 of its planned 280 retained frames; the incomplete sample is **excluded from every reported mean and comparison**. The intended six-chain interacting extension exceeded the runtime limit.

Pilot means in the unshifted spatial 0–1 Wilson trace normalization (standard errors across **three** independent seed means):

| L8 observable | beta zero ± seed-SE | beta two ± seed-SE |
|---|---:|---:|
| Nearest temporal \(K_\beta(e_2)\) | \(+0.00004749\pm0.00008086\) | **\(+0.00393156\pm0.00010011\)** |
| R1,d2 offdiagonal | \(+0.00000464\pm0.00001405\) | \(+0.00007005\pm0.00000965\) |
| R1,d3, J=0 offdiagonal | \(+0.00000315\pm0.00002400\) | \(+0.00008811\pm0.00002455\) |
| R2,d2, **J=8** offdiagonal | \(+0.00000189\pm0.00000358\) | \(+0.00000963\pm0.00000708\) |
| R2,d3, J=0 offdiagonal | \(+0.00000761\pm0.00003167\) | \(+0.00006561\pm0.00000444\) |

The L8 original SU2 beta-two nearest-slice signal \(K(e_2)=0.00393156\pm0.00010011\) is compatible with the larger L6 independent estimate \(0.00403175\pm0.00005137\) and with the previous heat bath. At R1,d3 and R2,d3, the L8 beta-two distinct-plaquette residuals are **positive in the three completed chains** and approximately **smaller** than the L6 values \(0.00014877\) and \(0.00013400\). This is compatible with reduced small-volume periodic contributions, but no physical decay rate is fitted.

**Statistical hold:** only three completed chains per L8 coupling mean large t-multipliers and unstable variance estimates. The L8 beta-two-minus-Haar d3 contrasts **have not been established as statistically resolved** with these samples. They are a screening result guiding the next properly powered test, not a replica of L6's four-case multiple-testing outcome.

## 3. Provenance and next target

The exact geometric HBP is machine-checkable with integers only. The L8 beta-two and beta-zero raw numerical configuration files are available in the conversation research bundle and explicitly separated from the strict no-float repository kernel. A single CSV combining the **six complete L8 chains (1,680 saved configurations)** has SHA-256 **768c0dd4ca2169fedcee91179837b130e323d33e71c49c8c443a94e9d2da8000**. No incomplete chain is included.

**Next experimental acceptance:** collect more complete L8 and larger-L original Wilson chains with d fixed below L/2, independently assess autocorrelation/time-block effects, then resolve *whether the difference between L6 and L8 offdiagonal radial signals persists beyond their seed-SE*. In parallel, the mathematical main target remains a **volume- and beta(a)-uniform upper Wilson covariance-decay bound** sufficient for the continuum mass gap. No inference about actual L128 production beta=9^12 spherical field readings or the eleven continuum-construction gates is drawn from this finite screening.
