# YM4 VOL13 pilot — exact four-dimensional centre cocycle and periodic gauge-frame reconstruction

**23 November 2026 — mathematical centre-sector theorem and original 4D exact-integer reconstruction controls.** This is the first constructive frame test following [VOL12 beta-uniform aligned one-link transport](NOTE-YM4-VOL12-GOOD-STAR-RADIAL-TRANSPORT-20261123.md). All variables remain genuine original SU(2) link variables, restricted to its exact centre subgroup {+I,-I} for this scoped pilot.

## 1. Gauge-frame compatibility criterion in the centre

Let \(r_{x,\mu}\in\{\pm I\}\) be a centre-valued ratio on each original positive link of the periodic 4D torus \((\mathbb Z/L)^4\). A periodic centre-valued vertex gauge frame \(g_x\in\{\pm I\}\) realizes the ratio exactly when
\[
r_{x,\mu}=g_xg_{x+\hat\mu}^{-1}.
\tag{F1}
\]

**Exact criterion:** Such a frame exists if and only if every original plaquette ratio product is +I and all four fundamental noncontractible winding-loop ratio products are +I:
\[
\boxed{
\prod_{\partial p}r_e=I\quad\text{for every plaquette }p,
\qquad
\prod_{e\in \gamma_\mu}r_e=I\quad(\mu=0,1,2,3).
}
\tag{F2}
\]

Necessity follows by telescoping vertex factors around any loop. For sufficiency, pick a root vertex and set its frame to identity. Define \(g_x\) by the ordered ratio product along any lattice path from the root. In the abelian centre, any two paths between the same vertices differ by a finite product of plaquette boundaries and four fundamental torus winding cycles. The hypotheses in F2 make their ratio product +I; hence \(g_x\) is path-independent and periodic and satisfies F1.

This is the exact centre-valued \(H^1(T^4,\mathbb Z_2)\cong(\mathbb Z_2)^4\) obstruction statement expressed in original lattice variables. It is a **specific algebraic subproblem**, not a proof that general noncommutative SU(2) link rotations admit a common endpoint gauge frame.

## 2. Constructive verified witnesses

The [integer-only original 4D verifier](../../tests/ym4_vol13_center_frame_cocycle.py) generates full L=4 and L=6 positive-link graphs and tests:

- **Positive control:** an explicit nonconstant periodic vertex gauge \(g_x=(-1)^{[x_0+2x_1+3x_2+5x_3]\bmod3=0}\) and the corresponding ratio \(r_{x,\mu}=g_xg_{x+\hat\mu}^{-1}\). Every original plaquette ratio is +1, all four Polyakov ratio loops are +1, and breadth-first propagation reconstructs a consistent periodic site gauge on all \(L^4\) vertices.
- **Global obstruction:** \(r_{x,0}=-I\) on the periodic cut \(x_0=L-1\), +I on all other links. Every original plaquette ratio is +I but the direction-0 Polyakov ratio is -I. The explicit site-frame BFS correctly rejects a globally periodic frame.
- **Local obstruction:** flip one original positive link alone. At least one original plaquette ratio is -I, and the gauge-frame reconstruction rejects it.

The positive and two negative controls are checked for all \(6L^4\) original plaquettes, with exact integer centre products. The frozen [HBP receipt](YM4-VOL13-CENTER-FRAME-20261123.hbp) records the accepted scope. All tests use original 4D torus incidence rather than a generic abstract graph.

## 3. Interface to the original SU(2) Haar radial transport theorem

VOL12 proves that two good-star original continuous SU(2) one-link conditionals have orientation-aligned total variation **strictly below 1/24 at every beta**. This uses each link's preferred unit quaternion \(v_e=H_e/\|H_e\|\). Applying the preferred rotations to every link independently is a valid single-link coupling, but it does not automatically give a common endpoint gauge transformation \(g_x\).

This centre pilot isolates two exact classes of frame mismatch: **local plaquette inconsistency** (curvature) and **global winding inconsistency** (nontrivial holonomy). The corresponding full SU(2) nonabelian version must compare cycle holonomies up to conjugacy and quantify small residual plaquette errors after choosing a spanning-tree gauge. In the original physical all-sector setting it must retain centre/Polyakov sector information instead of allowing it to disappear during quotienting.

**Next mathematical target:** construct a gauge-covariant SU(2) multi-link frame on good-star connected collars, quantify the residual aligned-Wilson source transport cost across elementary plaquette cycles and winding cycles, and add that frame mismatch to the beta-uniform \(1/24\) single-link budget. Then certify a genuine \( \delta_{\rm good}(b) \) in the [VOL12 averaged boundary covariance interface](NOTE-YM4-VOL12-AVERAGED-BOUNDARY-COUPLING-20261123.md).

**Status:** exact centre cocycle criterion ANALYTIC; original 4D L=4/L=6 centre frame reconstruction and red controls INTEGER REPLAY PASS (hosted receipt pending workflow). Full nonabelian SU(2) collar gauge-frame coupling, global all-Gauss-sector transport, physical-size cube, coarse blocked measure and all eleven continuum obligations OPEN. [Tracking issue #115](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/115).
