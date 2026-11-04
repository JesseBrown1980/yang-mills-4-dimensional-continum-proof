# GPT-6's independent review of the periodic 1×L lattice

The independent GPT-6 seat's two reports, as the operator relayed them on November 4, 2026 UTC, five minutes apart: the 1×1 section of the first, and the second whole apart from its run-time line, the URL on its PR #11 link and the table named below. The quoted text is verbatim. The relay dropped some inline symbols, and those gaps stay as they arrived, so the receipts and [Lemma 0003](../../docs/LEMMA-0003-SUBGROUP-DESIGNS.md) carry the formulas in full.

## The 1×1 counterexample, as relayed

> I can also confirm the 1×1 counterexample without relying on the second seat's code.
>
> For independent Haar-distributed , the character integral for their commutator is
>
> \\mathbb E\[\\chi_j(C)\]=\\frac{1}{2j+1}.
>
> Writing , the SU(2) character identities give
>
> \\mathbb E\[a\]=\\frac14,\\qquad
> \\mathbb E\[a^2\]=\\frac14\\left(1+\\frac13\\right)=\\frac13.
>
> For Q₈, every commutator is or , so identically. Therefore,
>
> \\boxed{\\mathbb E_{Q_8}\[a^2\]=1
> \\ne \\frac13=\\mathbb E_{SU(2)}\[a^2\].}
>
> This independently confirms that the Q₈ and SU(2) Wilson expansions agree at first order on the 1×1 torus but differ at second order. It is a genuine geometric limitation, not a numerical error.

## The 1×L theorem, as relayed

> ### GPT-6 independent verdict — the 1×L theorem holds
>
> Independently derived
>
> I checked the proposed proof independently and compared its consequences against the exact receipts in PR #11.
>
> The result is stronger than the earlier empirical statement: for every periodic two-dimensional lattice , with , a finite subgroup of SU(2) whose uniform average agrees with Haar through polynomial degree gives the same Wilson partition-function Taylor coefficients through order .
>
> The fact that a plaquette contains a repeated link does not reduce the guaranteed order to on this family.
>
> ### Independent derivation
>
> Write
>
> P_x=A_xV_xA_{x+1}^{-1}V_x^{-1},
> \\qquad
> X=\\sum_{x=0}^{L-1}\\frac12\\operatorname{Tr}P_x.
>
> Consider any monomial contributing to :
>
> \\prod_x \\left(\\frac12\\operatorname{Tr}P_x\\right)^{m_x},
> \\qquad \\sum_xm_x=k\\le t.
>
> First, each has polynomial degree . Its subgroup average therefore equals its SU(2) Haar integral.
>
> Next, expand each plaquette power into SU(2) characters. Orthogonality in the integrations forces a common representation index around the ring. I independently obtained the identity
>
> \\int\\prod_xdA_x
> \\prod_x\\chi_{n/2}(P_x)
> =
> \\frac{|\\chi_{n/2}(V_0V_1\\cdots V_{L-1})|^2}{(n+1)^L}.
>
> Only contributes.
>
> The remaining expression has degree in each , and
>
> 2n\\le2\\min_xm_x
> \\le\\frac{2k}{L}\\le k\\le t.
>
> Thus the subgroup averages over the are exact as well.
>
> Conclusion: every moment equals for , establishing the claimed Taylor-coefficient agreement.
>
> ### Independent exact checks
>
> I derived an additional closed formula that can be placed in Lemma 0003:
>
> \\boxed{
> \\mathbb E_{\\mathrm{SU}(2)}
> \\left\[\\prod_x a(P_x)^{m_x}\\right\]
> =
> \\frac{1}{2^k}
> \\sum_{n=0}^{\\min_xm_x}
> \\frac{\\prod_x B(m_x,n)}{(n+1)^L}
> }
>
> where , and
>
> B(m,n)=
> \\frac{n+1}{m+1}
> \\binom{m+1}{(m-n)/2}
>
> when and is even, and zero otherwise.
>
> This gives an independent way to calculate every SU(2) moment on , without substituting a finite subgroup for Haar integration.
>
> I then separately enumerated Q₈ and 2T link assignments, using their group multiplication laws and exact rational arithmetic.
>
> Every result agrees with the filed second-seat measurements.
>
> For example, the independent SU(2) calculation gives
>
> \\begin{aligned}
> \\mathbb E\[X^2\]_{1\\times2}&=\\frac58,\\\\
> \\mathbb E\[X^3\]_{1\\times3}&=\\frac3{32},\\\\
> \\mathbb E\[X^4\]_{1\\times3}&=\\frac32,\\\\
> \\mathbb E\[X^5\]_{1\\times3}&=\\frac{15}{32}.
> \\end{aligned}
>
> ### Final independent decision
>
> PASS — the proposed 1×L theorem, for .
>
> I found no missing hypothesis in the stated character-orthogonality and degree-counting argument. It establishes the result for arbitrary qualifying finite subgroups, not just the specific Q₈ and 2T examples.
>
> I recommend adding the theorem and the closed moment formula to PR #11 with the scope:
>
> DERIVED and independently mathematically checked; exact Q₈ and 2T controls reproduced.
>
> The corresponding result for higher-dimensional lattices with one collapsed direction remains OPEN. Nothing here promotes the finite-subgroup bridge to a uniform approximation of SU(2) at large , and YM4-02c remains on its separate HOLD.

Its table names Q8 and 2T on 1×2 and 1×3, and its order cells arrived empty, so it is left out. Those values are the rows of [`tests/ONE_BY_L_RECEIPT.txt`](../../tests/ONE_BY_L_RECEIPT.txt).
