# YM4-02a — exact Haar moments for the finite four-dimensional SU(2) Wilson lattice

**Status:** elementary Haar lemma DERIVED, incidence hypotheses EXACT-TEST; continuum existence OPEN; physical mass gap OPEN. This is a scoped subtask of [YM4-02](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/2).

Let `Λ = (Z/2Z)^4`. There are 16 sites, 64 positive links and 96 positive-orientation plaquettes, indexed by `x` and `μ<ν`. Each positive link carries independent, normalized `SU(2)` Haar measure under the **unweighted product measure**, i.e. at `β=0`.

Write a unit quaternion `U=(a,b,c,d)` so that `(1/2)Re Tr U = a`. Haar on `SU(2)` corresponds to uniform probability on `S^3`; invariance and `a²+b²+c²+d²=1` give

```text
E_Haar[a]=0,      E_Haar[a²]=1/4.
```

For a plaquette `p`, its ordered Wilson holonomy `U_p` is the product of four link matrices, two inverted. Every plaquette on this chosen lattice uses **four distinct link variables**. By left/right/inversion invariance of Haar, `U_p` is Haar distributed if just one of its links is integrated out with all others fixed. Thus with `A_p=(1/2)Re Tr U_p`,

```text
E[A_p]=0,          E[A_p²]=1/4.
```

For two distinct plaquettes `p≠q`, their link supports share at most two of their four positive links; each has an exclusive Haar variable. Integrating an exclusive variable in `A_p A_q` first gives `E[A_p A_q]=0`. **This covariance statement uses the independent product Haar measure at β=0, not the interacting Wilson measure at β>0.**

Set `X = sum_p A_p`, `N_p=96`. Then

```text
E[X]=0,
Var(X)=N_p / 4 = 24.
S_W(β)=β(N_p-X),
Z(β)=E_productHaar[exp(-S_W(β))].
```

Because every finite-volume Wilson-action summand is bounded and `β` is finite, differentiation at zero under the integral is justified. Consequently:

```text
Z(0)=1
(d/dβ)log Z(β)|_{β=0} = -96
(d²/dβ²)log Z(β)|_{β=0} = 24
Z'(0)=-96
Z''(0)=9240.
```

Equivalently `Z(β)=1−96β+4620β²+O(β³)` near zero. The finite measure is positive for each `β≥0`, and `0<Z(β)≤1` for the indicated normalized Wilson action. These statements are standard finite-cutoff SU(2) facts, not a four-dimensional continuum theorem.

## Reproducible geometry and fault controls

Run `python3 -I tests/test_haar_moments_4d.py`. The checker independently enumerates all 96 oriented plaquettes and all 4,560 unordered pairs on the four-dimensional periodic lattice. Distinct pairs share 0, 1 or 2 positive links in counts 3,696; 768; and 96. The 64 positive links each occur in six plaquettes. It uses the **proved** SU(2) Haar moment formula above as mathematical input and exact integer/rational arithmetic to obtain the derivatives. It deliberately duplicates a plaquette support or removes one link; both must be rejected.

**Important limitation:** the executable does not compute the Haar integral from first principles or establish reflection positivity. It checks the combinatorial premises and the arithmetic consequences of Haar orthogonality. The next substantial task is to match the finite Wilson measure to a reflection-positive transfer kernel and its gauge projection, and then begin an explicit gauge-equivariant blocking construction.

References: Osterwalder–Seiler, *Gauge field theories on a lattice* (1978), DOI 10.1016/0003-4916(78)90039-8; Clay/Jaffe–Witten official problem statement.
