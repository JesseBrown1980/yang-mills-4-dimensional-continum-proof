# YM4-VOL10 — original SU(2) Wilson finite-box occupancy and exact bad-island acceptance threshold

**2026-11-22 · Proven elementary consequences of VOL09 and a conditional independent-set cluster theorem.** The conclusions are carefully separated:

- **A (original continuous SU(2) theorem):** finite-box bad-star occupancy and bad-count tail under the *actual periodic Wilson Gibbs measure*, plus a four-to-one gauge-invariant original Wilson plaquette-defect budget, uniformly in total lattice volume.
- **B (combinatorial theorem):** a sufficient **joint** bad-star certificate for exponential connected-island tails on the actual four-dimensional link-sharing graph, whose maximum degree is 18.
- **C (adversarial control):** the VOL09 one-star marginal, even if arbitrarily small, does not logically imply the required joint certificate. The explicit counterexample is an abstract correlated indicator law, **not** an asserted Wilson measure.
- **D (continuum):** block conditioning, multiscale bad-island activity, full all-Gauss-sector physical-scale contraction and eleven original continuum gates remain OPEN.

The source theorem is [VOL09](NOTE-YM4-VOL09-PERIODIC-GOOD-STAR-FREQUENCY-20261122.md), which derives for original continuous SU(2) Wilson theory on every isotropic periodic \(L^4\) torus, \(L\ge3\), and \(\beta\ge1\),
\[
p_\beta(\epsilon):=\sup_e\mu_{\beta,L}(\mathcal G_\epsilon(e)^c)
\le \min\left(1,\frac{24}{\epsilon\beta}
[1+\tfrac43\log(1536\beta^{3/2})]\right).
\tag{1}
\]
Here \(e\) is an **original oriented link**, and \(\mathcal G_\epsilon(e)\) is the gauge-invariant good-star event defined by the 15 double-staple Wilson traces of [VOL08](NOTE-YM4-VOL08-ORIGINAL-SU2-WILSON-STAR-20261122.md). The probability is periodic *equilibrium* probability, not a uniform assertion over adversarial exterior conditioning.

## A. Actual original SU(2) finite-box occupancy and bad-count control

Fix a set \(Q\) of \(b^4\) vertex sites in \(L^4\), with \(1\le b\le L\); include all **four positively oriented original links based at these sites**, whether or not the link endpoint lies inside \(Q\). There are exactly \(M(Q)=4b^4\) distinct original links; for \(b=L\), this is the entire periodic torus. Define \(B_e=\mathbf1_{\mathcal G_\epsilon(e)^c}\) and \(N_Q=\sum_{e\text{ based in }Q}B_e\). Linearity of expectation, no independence assumed, gives
\[
\boxed{\mathbb E_{\mu_{\beta,L}}N_Q\le4b^4p_\beta(\epsilon).}\tag{2}
\]
Therefore, for every integer \(r\ge1\),
\[
\boxed{\Pr(N_Q\ge r)\le
\min\left(1,\frac{4b^4p_\beta(\epsilon)}r\right).}\tag{3}
\]
The case \(r=1\) is the explicit *box occupancy* bound. More generally, if \(Q\) contains a connected subset of \(r\) bad stars in the **plaquette-sharing-link graph**, then \(N_Q\ge r\); the same right side applies.

For \(\beta=9^k\), \(k\ge1\), [VOL09's exact rational upper envelope](YM4-VOL09-PERIODIC-GOOD-STAR-20261122.hbp) reads
\[
p_{9^k}(\epsilon)\le
\min(1,\frac{8(35+18k)}{\epsilon\,9^k}).
\]
Thus the original SU(2) box bound becomes
\[
\boxed{\Pr(N_Q\ge r)\le
\min\left(1,\frac{32b^4(35+18k)}
{r\epsilon\,9^k}\right).}\tag{4}
\]
This is an exact-rational **periodic Wilson Gibbs** statement in all finite volumes \(L\ge\max(3,b)\).

Explicit \(\epsilon=1/2\) examples:
- \(k=12,\beta=9^{12}=282429536481\), \(b=3^3=27\): probability of **any** bad star in \(Q\) is at most \(16064/531441<1/30\), independent of \(L\).
- Same \(k=12\), \(b=3^4=81\): the raw union envelope is \(16064/6561>1\); the valid probability bound is 1 and this method supplies no nontrivial occupancy certificate at that scale.
- \(k=16,\beta=9^{16}\), \(b=3^5=243\): the occupancy bound is \(20672/531441<1/25\).

The direct scaling criterion at fixed \(\epsilon>0\) is
\[
b(\beta)^4\frac{\log\beta}{\beta}\longrightarrow0
\quad\Longrightarrow\quad
\sup_{L\ge b(\beta)}\Pr(\exists\,e\in Q:B_e=1)\longrightarrow0.
\tag{5}
\]
For \(\epsilon(\beta)\downarrow0\), replace the numerator by \(b^4\log\beta/[\epsilon(\beta)\beta]\). Equation (5) is a **sufficient consequence of the upper bound**, not a necessary condition for true physical-cube goodness. If \(b^4\log\beta/(\epsilon\beta)\) diverges, this particular union certificate becomes vacuous; it does not prove the cube itself fails. A fixed physical-width cube typically requires \(b(a)\asymp1/a\) and a separate multiscale/renormalized estimate.

### A.1 Four-to-one original Wilson plaquette-defect budget

Define the **gauge-invariant original plaquette defect**
\(D_p=\mathbf1_{\{W_p<1-\epsilon/4\}}\).
The exact quaternion chordal implication in VOL09 gives, configuration by configuration,
\[
B_e\le\sum_{p\ni e}D_p.
\tag{5a}
\]
Every original four-dimensional plaquette meets precisely **four distinct positively oriented links**. Therefore on the entire periodic original lattice,
\[
\boxed{\sum_eB_e\le4\sum_pD_p.}
\tag{5b}
\]
The same inequality holds for a subset \(Q\) of links with the right side restricted to plaquettes touching \(Q\). Consequently a connected bad-star island with \(m\) links forces **at least \(\lceil m/4\rceil\) distinct original gauge-invariant Wilson plaquette defects**. This geometric lower bound on the **number of energetic defects** is valid for every SU(2) link configuration, without mixing assumptions.

It turns the next physics acceptance question into a concrete multi-defect statement: obtain a joint upper bound on simultaneous separated original plaquette defects that composes into a bad-island activity. The pointwise defect budget alone is deterministic and leaves their Gibbs correlations open.

## B. Actual original link graph: degree 18, deterministic animal enumeration

Let \(\mathcal H_L\) be the graph of original four-dimensional positively oriented links: two distinct vertices \(e,e'\) are adjacent exactly if they belong to a common *original Wilson plaquette*. Each link is incident on 6 distinct plaquettes, and each such plaquette contains 3 other original links. For periodic \(L\ge3\), the 18 neighbors are distinct, so the degree is exactly \(\Delta=18\). This is verified for every link on the original \(3^4\) and \(4^4\) lattices by [VOL08's exact geometry checker](../../tests/ym4_su2_vol08_wilson_star.py).

For any fixed root \(o\), the number of connected subsets of exactly \(m\) link-vertices containing \(o\) is at most
\[
\boxed{A_m(o)\le18^{2(m-1)}}.
\tag{6}
\]
Proof: choose a deterministic rooted spanning tree of each connected subset and its depth-first tour, of length exactly \(2(m-1)\). The walk starts at \(o\); each step has at most 18 choices. Distinct subsets have distinct tour vertex sets, yielding an injective encoding into such walks.

Every connected set \(A\) of \(m\) vertices contains an independent subset \(S(A)\) of size at least
\[
|S(A)|\ge\left\lceil\frac m{19}\right\rceil.
\tag{7}
\]
Indeed, greedily choose a vertex and remove it plus at most 18 neighbors. Independence here means **no two stars share an original Wilson plaquette**; it is a combinatorial relation, *not* probabilistic independence.

## C. Conditional SU(2) joint certificate needed for exponential islands

The exact unproved model-specific input is:

**VOL10-JOINT(\(\rho,\beta,\epsilon,L\))**: for **every** independent set of original link-vertices \(S\subset\mathcal H_L\),
\[
\boxed{\mu_{\beta,L}\bigl(\bigcap_{e\in S}\{B_e=1\}\bigr)\le\rho^{|S|}},
\qquad0<\rho<1.
\tag{8}
\]
If this is certified for the original periodic SU(2) Gibbs law, then every root bad-connected cluster \(C(o)\) obeys
\[
\boxed{
\Pr_{\beta,L}(|C(o)|\ge m)\le
\min\{1,\;18^{2(m-1)}\rho^{\lceil m/19\rceil}\}
}.
\tag{9}
\]
Proof: a cluster with at least \(m\) vertices contains a connected subset \(A\) of exactly \(m\) containing \(o\). Greedy independent extraction gives a deterministic \(S(A)\). If all of \(A\) is bad, all of \(S(A)\) are bad, of probability at most \(\rho^{\lceil m/19\rceil}\). Union over at most \(18^{2(m-1)}\) rooted animals.

In particular, a sufficient **concrete exact-integer activity floor** is
\[
\boxed{\rho\le18^{-57}
\quad\Longrightarrow\quad
\Pr_{\beta,L}(|C(o)|\ge m)\le18^{-m-2}.}
\tag{10}
\]
This uses \(\lceil m/19\rceil\ge m/19\) and \(\rho^{\lceil m/19\rceil}\le18^{-3m}\). The extreme threshold is deliberately conservative: it makes the missing **joint** input numerically testable without claiming an efficient multiscale estimate.

**Acceptance scope:** equations (6)–(10) are unconditional combinatorial/conditional-implication theorems. The SU(2) probability input (8) has **not** been obtained. A valid \(\rho\) may require nontrivial block decoupling and gauge-invariant averaging; the single-star envelope (1) supplies only the \(|S|=1\) case.

## D. Adversarial falsifier: an arbitrarily small marginal need not decay with island size

For any finite connected graph with \(N\) vertices and any \(p\in(0,1)\), let \(Z\sim{\rm Bernoulli}(p)\) and define \(B_e=Z\) simultaneously for **all** vertices. Every marginal satisfies \(\Pr(B_e=1)=p\), but
\[
\Pr(|C(o)|\ge m)=p,\quad1\le m\le N.
\]
For two distinct independent vertices \(e,e'\),
\(\Pr(B_e=B_{e'}=1)=p>p^2\).
Thus (8) cannot be inferred from VOL09's per-star probability alone, even with a uniform-in-volume marginal. This is an **abstract adversarial probability model**, used only to falsify a mistaken logical inference. No claim is made that these all-or-none indicator distributions are actual Wilson Gibbs measures.

## E. Acceptance tiers, prior art and next direct physics step

- **VOL10-BOX:** source-dependent, exact original continuous SU(2) periodic finite-box occupancy and \(r\)-star-count bound, uniformly in \(L\) — **ANALYTIC DERIVATION + EXACT INTEGER REPLAY**.
- **VOL10-ANIMAL:** degree-18 rooted-animal and independent-set combinatorics — **EXACT MATHEMATICAL DERIVATION**, finite original link graph and sampled animal enumerators as independent falsifiers.
- **VOL10-JOINT:** uniform joint bad-star probability (8) under the **original SU(2) conditional** or **periodic** laws — **OPEN**.
- **VOL10-ISLAND:** exponential cluster tail (9)/(10) — **CONDITIONAL ON VOL10-JOINT**.
- **VOL07 / physical cube / continuum:** the full all-Gauss-sector, boundary-conditioned, physical-size one-cube comparison and nontrivial continuum source construction — **OPEN**, including the eleven original continuum gates.

The most direct next acceptance calculation is to derive a *two-star or finite-packet joint bad-event bound for non-plaquette-sharing original SU(2) stars*, and check whether it composes into (8) under changing exterior fields. The literature's Dobrushin–Shlosman cube route and Bałaban bad-island decompositions use more refined weighted activities, see [Bhattacharjee et al., *One Cube Estimate Implies the Yang–Mills Mass Gap*, version 7](https://hexagonmath.org/2610.00341v7). That paper explicitly leaves its physical-size cube uniform continuum-tuning estimate open. The local exact inequalities here are independent finite-volume consequences of our VOL09 source and do not import its unproved continuum inputs.
