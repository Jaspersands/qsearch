## Outcome

I do **not** obtain a polynomial-time reconstruction algorithm or a general impossibility theorem for resultant-phase synthesis.

I do obtain a **source-level falsifier for a concrete broad-state construction**: prepare public coefficient labels, coherently select base-field query lists from those labels, multiply native signs, and optionally combine such products through a clean public prepare/postselect operation. Even though the coefficient support is now almost the entire coefficient space, this construction cannot synthesize the desired resultant-phase state with inverse-polynomial heralding probability and constant conditional fidelity.

This is not another analysis of the closed split-support receiver. The obstruction concerns the **relative phases between different nonsplit factor classes**.

## 1. Cheapest classical and black-box attacks

Write \(F_C(x)=\lambda_p(C(x))\), where \(\lambda_p(0)=1\).

For distinct monic squarefree degree-\(d\) polynomials \(Q,C\), removing their common square factor and applying the Weil bound gives
\[
\left|\frac1p\sum_x F_Q(x)F_C(x)\right|
 \le \frac{2d-1}{\sqrt p}+\frac{2d}{p}.
\]
Consequently, at \(p\ge256d^2\), a wrong candidate agrees with \(F_Q\) on at most \(3/4\) of the field.

Thus
\[
n=\left\lceil
\frac{d\log p+\log(1/\eta)}{\log(4/3)}
\right\rceil
\]
independent uniform chosen-BIT queries suffice for empirical exhaustive reconstruction: enumerate the \(p^d\) monic candidates and retain those matching the transcript. A union bound gives failure at most \(\eta\).

This establishes:

* polynomial native **query** cost;
* \(p^d\operatorname{poly}(d,\log p,\log(1/\eta))\) classical enumeration time;
* cheap verification of a supplied candidate using fresh samples.

Generic search over candidates still has field-size-exponential cost. The supplied full-table classical decoder also charges \(p\) input accesses and polynomial-\(p\) processing under its stated promises. It does not give a uniform polynomial-\(\log p\) algorithm.

Native interpolation remains unavailable: a character bit is not a field value. None of these observations establishes classical hardness.

## 2. A genuinely broad resultant-phase state would suffice

Set
\[
m=2d-1,\qquad V=\mathbb F_p^{m+1}.
\]
Let \(\mathcal S_m\) contain **all** squarefree polynomials of exact degree \(m\), with arbitrary nonzero leading coefficient—not only split polynomials. Its size is
\[
M=(p-1)(p^m-p^{m-1}),\qquad
\delta=\frac{M}{|V|}=(1-1/p)^2.
\]

Consider the target state
\[
|T_Q\rangle=
\frac1{\sqrt M}\sum_{R\in\mathcal S_m}
\lambda_p(\operatorname{Res}(Q,R))\,|R\rangle.                 \tag{1}
\]

The unsigned label preparation is inexpensive: prepare uniform coefficients, test exact degree and squarefreeness by public polynomial arithmetic, and herald success. The ideal success probability is \(\delta\), and the arithmetic and approximate state-preparation costs are polynomial in \(d,\log p\), and the requested precision. No factorization of \(Q\) is involved.

To check that (1) is sufficient, use the virtual norm-character state from the supplied note. If the irreducible factor degrees of \(Q\) are \(d_j\), its unit fraction is
\[
u=\prod_j(1-p^{-d_j})\ge1-\frac d p.
\]
The fraction of ambient labels both in \(\mathcal S_m\) and coprime to \(Q\) is at least \(\delta+u-1\). Hence
\[
|\langle N_Q|T_Q\rangle|^2
 \ge \frac{(\delta+u-1)^2}{\delta u}
 \ge \left(1-\frac{d+2}{p}\right)^2.                         \tag{2}
\]
The supplied virtual Fourier/Hankel argument therefore gives correct decoding probability at least
\[
1-\frac{2(d+2)}p.
\]

So this is a valid constructive target. If its synthesis had

* heralding probability \(s\ge1/\operatorname{poly}(d,\log p)\);
* sufficiently small conditional state error;
* cost \(\operatorname{poly}(d,\log p,\log(1/\epsilon))\);

then \(O(s^{-1}\log(1/\eta))\) attempts, followed by fresh chosen-BIT verification, would give the requested reconstruction.

All remaining costs are polynomial: \(2d\) field QFTs, an \(O(d^3)\)-field-operation Hankel solve, public candidate evaluation, bounded uniform sampling, and the \(d\log p\)-bit output. Circuit error must be below the claimed joint success probability; this requires logarithmic precision in its reciprocal, not a free exact preparation.

The missing operation is precisely the phase in (1).

## 3. The direct native phase-lift candidate

There is a useful preliminary observation. Write a squarefree public mask as
\[
R=aBL,
\]
where \(L\) is completely split and \(B\) has no rational linear factors.

For **fixed** \(B\), and targets coprime to \(B\), the unknown factor
\[
\chi_p(\operatorname{Res}(Q,B))
\]
is only a common global phase. Native queries at the roots of \(L\), with the correct public scalar factor, can therefore prepare that one factor class up to global phase.

But coherently varying \(B\) requires the relative phases between these classes. Ignoring them is not harmless.

Here is a precise model encompassing the direct repair.

For \(A\subseteq\mathbb F_p\), define
\[
f_A(Q)=\prod_{x\in A}F_Q(x).
\]
For every public coefficient label \(R\), suppose the successful amplitude is
\[
h_R(Q)=\sum_A c_{R,A}f_A(Q),
\qquad
\sum_A|c_{R,A}|\le1,                                      \tag{3}
\]
where the coefficients are independent of \(Q\).

This includes:

* any public \(R\)-dependent query list followed by native phase kickback;
* arbitrary public diagonal corrections, including leading-coefficient factors;
* query locations unrelated to the rational roots of \(R\);
* a coherent superposition of public query lists, followed by a clean public prepare/postselect operation.

For the last case, the coefficients have the form
\(\overline{v_A}u_A\); their absolute sum is at most one by Cauchy–Schwarz. Repeated native sign queries cancel modulo two. The result below even permits every base-field point to occur.

The successful, unnormalized coefficient state is
\[
|\xi_Q\rangle=
\frac1{\sqrt M}\sum_{R\in\mathcal S_m}h_R(Q)|R\rangle.
\]
Let \(s_Q=\|\xi_Q\|^2\). Then
\[
J_Q:=|\langle T_Q|\xi_Q\rangle|^2
=s_Q\,
\operatorname{Fid}\!\left(
|T_Q\rangle,\frac{|\xi_Q\rangle}{\sqrt{s_Q}}
\right).                                                   \tag{4}
\]
Thus \(J_Q\) charges heralding probability, not merely conditional fidelity.

### Proved falsifier

For every \(d\ge3\) and odd prime \(p\ge256d^2\),
\[
\boxed{
\mathbb E_{\substack{Q\ \mathrm{monic\ irreducible}\\\deg Q=d}}
 J_Q
\le
\frac1{(1-1/p)(2d-1)!}
 +2p^{\,1-d/2}.
}                                                          \tag{5}
\]
Uniformly in this regime, the right side is
\[
\exp[-\Omega(d\log d)].
\]

Consequently, this phase-lift architecture cannot have both inverse-polynomial heralding probability and constant conditional fidelity for every target. More strongly, for any \(z>0\),
\[
\Pr_Q[J_Q\ge z]\le
\frac{(1-1/p)^{-1}/(2d-1)!+2p^{1-d/2}}{z}.                 \tag{6}
\]

The coefficient support in this theorem has density \((1-1/p)^2\). **No split-support packing bound or Fourier/Hankel success calculation is used in proving (5).**

## 4. Proof of the falsifier

### 4.1 Native products become character functions of an analysis-only root

Put \(q=p^d\), and let
\[
E_d=\{\theta\in\mathbb F_q:[\mathbb F_p(\theta):\mathbb F_p]=d\}.
\]
Every monic irreducible degree-\(d\) polynomial has exactly \(d\) roots in \(E_d\). Uniform averaging over \(E_d\) therefore equals uniform averaging over those polynomials for the functions below.

If \(Q\) is the minimal polynomial of \(\theta\), then
\[
F_Q(x)=\chi_q(x-\theta),\qquad x\in\mathbb F_p,
\]
and, whenever the resultant is nonzero,
\[
\chi_p(\operatorname{Res}(Q,R))=\chi_q(R(\theta)).           \tag{7}
\]
These follow from
\(\chi_p(N_{\mathbb F_q/\mathbb F_p}z)=\chi_q(z)\).

**This extension field is used only to prove an average bound. It is not an algorithmic input, an extension-field oracle, or a supplied quotient algebra.**

The number of excluded, non-full-degree elements satisfies
\[
B_d:=\sum_{\substack{e\mid d\\e<d}}p^e
\le \frac32\sqrt q,
\qquad |E_d|\ge q-B_d.                                     \tag{8}
\]

### 4.2 Different nonsplit factor classes have negligible correlation

For squarefree \(R\), let \(\operatorname{nsp}(R)\) be the monic product of its irreducible factors of degree at least two. Delete its scalar and all rational linear factors.

Suppose
\[
\operatorname{nsp}(R)\ne\operatorname{nsp}(R').
\]
For any native query subsets \(A,A'\), the polynomial
\[
G(X)=R(X)R'(X)
       \prod_{x\in A\triangle A'}(x-X)
\]
has an irreducible factor of degree at least two with odd multiplicity. Therefore it is not a square over the algebraic closure. Moreover,
\[
\deg G\le2m+p.
\]

The finite-field quadratic-character Weil bound gives
\[
\left|\sum_{\theta\in\mathbb F_q}\chi_q(G(\theta))\right|
\le(2m+p-1)\sqrt q.
\]

Restricting to \(E_d\) costs at most \(B_d\). Replacing the zero-valued character by the padded resultant sign costs at most \(2m\), since only roots of \(RR'\) can be affected. Thus, with
\(g_R(Q)=\lambda_p(\operatorname{Res}(Q,R))\),
\[
\left|
\mathbb E_Q\,g_R(Q)g_{R'}(Q)f_A(Q)f_{A'}(Q)
\right|
\le
\frac{(2m+p-1)\sqrt q+B_d+2m}{q-B_d}
\le2p^{1-d/2}.                                            \tag{9}
\]
The last inequality uses \(m=2d-1\), \(d\ge3\), and \(p\ge256d^2\).

Thus arbitrary native parity queries do not supply appreciable correlation between distinct nonsplit factor classes.

### 4.3 No one class occupies much of the broad coefficient space

Fix a nonsplit part \(B\), and put \(s=m-\deg B\). Its class consists of
\[
R=aB\prod_{x\in T}(X-x),
\qquad a\ne0,\quad |T|=s.
\]
It therefore contains
\[
(p-1)\binom ps
\]
labels.

Its mass \(\mu_B\) under the uniform distribution on \(\mathcal S_m\) obeys
\[
\mu_B
=\frac{\binom ps}{p^m(1-1/p)}
\le\frac1{(1-1/p)m!}.                                     \tag{10}
\]
Indeed,
\[
\binom ps\le\frac{p^s}{s!}\le\frac{p^m}{m!},
\]
because \(m\le p\).

### 4.4 Expand the synthesis fidelity

Expand (4), substitute (3), and average over \(Q\).

* For two masks in the same nonsplit class, bound the correlation by one.
* For different classes, apply (9).
* The coefficient absolute sums are at most one.

It follows that
\[
\mathbb E_Q J_Q
\le \sum_B\mu_B^2+2p^{1-d/2}
\le \max_B\mu_B+2p^{1-d/2}.
\]
Equation (10) proves (5).

The squared overlap automatically accounts for arbitrary target-dependent global phases. A pointwise sign counterexample alone would not have done that.

## 5. Extensions, costs, and exact limits

### Polynomial-size phase combinations do not repair this architecture

If (3) instead satisfies
\[
\sum_A|c_{R,A}|\le L,
\]
the same proof gives
\[
\mathbb E_QJ_Q
\le L^2\left(
\frac1{(1-1/p)(2d-1)!}+2p^{1-d/2}
\right).                                                   \tag{11}
\]
Thus polynomial \(L\) still fails.

Likewise, restricting to a public subset of \(\mathcal S_m\) of relative density \(\alpha\) changes the class-size term to at most
\[
\frac1{\alpha(1-1/p)(2d-1)!}.
\]
Polynomial-density thinning does not fix the problem.

A uniform all-coefficient resultant-phase state cannot evade the test by retaining nonsquarefree or lower-degree labels: public degree/squarefreeness projection would produce (1) with constant probability.

### Approximation and postselection remain charged

If an implemented source differs from the specified ideal heralded operation by trace distance at most \(\epsilon\), the bound on \(J_Q\) increases by at most \(\epsilon\). To test a claimed joint success \(s_0f_0\), choose and charge \(\epsilon\ll s_0f_0\).

An approximation-error allowance is not evidence of additional useful success. Public preparation inverses, where used, must be explicitly constructed and paid; the argument supplies no inverse for an unknown state.

### What this does not prove

The bound is on **successful synthesis of (1)**. It is not an upper bound on arbitrary Hankel decoding success from an unrelated state.

It also does not rule out general chosen-BIT algorithms. Nonlinear processing of native answers, interleaved interference, or mixing coefficient labels can produce amplitudes outside (3), or with exponentially large parity-expansion norm.

Crucially, **large parity-expansion norm is not a gate lower bound**. A compact quantum circuit can generate exponentially many interfering terms. No general query lower bound, classical hardness, or quantum speedup follows from (5).

## 6. Remaining constructive obligation

Unrestricted efficient synthesis of (1) is essentially equivalent, in polynomial resources, to reconstruction:

* synthesis implies reconstruction by (2) and the paid receiver;
* reconstruction implies synthesis by computing the now-public resultant reversibly, applying its padded character phase, and uncomputing—charging the reconstruction, arithmetic, and any inverse circuit.

Therefore “prepare the broad resultant phase” is a legitimate target, but not a free primitive.

An admissible next proposal must provide an actual operation outside the falsified class and establish:

1. **Native derivation:** only the given base-field BIT oracle is used.
2. **Amplitude law:** explicit amplitudes or channel, not an asserted extension norm.
3. **Joint success:** every preparation and heralding flag is included.
4. **Precision:** error below the claimed recoverable-moment probability, at polynomial logarithmic precision cost.
5. **Readout and output:** a polynomial decoder, paid verification, and the \(d\log p\)-bit answer.

The immediate analytic falsifier is (11): if the proposed broad-state amplitudes reduce to a polynomial-\(\ell_1\) combination of public native sign products, reject that source mechanism without a parameter sweep.

**Disposition:** the direct broad-label parity/clean-LCU phase lift is ruled out. General collective resultant-phase synthesis—and hence the requested uniform polynomial reconstruction—remains open here. No repository changes, code execution, or new finite controls were performed.