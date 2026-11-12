## Verdict

**I do not close the full finite-place gate.** I can construct the aligned valuation rows at a **supplied prime**, with polynomial sparse-bit cost, without a constant-field basis or a hidden local-lattice oracle. The remaining unpaid operation is precise:

> Produce a polynomial-bit explicit nonzero integer divisible by the content of an implicit sparse Sylvester resultant—or otherwise certify a polynomial-bit integer covering all its prime divisors.

Modular PIT does not produce such an integer. Below are:
1. a paid known-prime compiler;
2. a native irreducible, growing-\(\delta\) family with **nonzero Alg** falsifying natural content/gcd/evaluation shortcuts;
3. an exact reduction showing that irreducibility does not simplify the requested resultant-support operation;
4. a paid torsion/identity step.

These are deductions, not an impossibility or hardness claim. No computation was executed.

---

## 1. Exactly what global support discovery must supply

Let \(N\) be the native input length. Using the companion representation and formal denominator clearing, write
\[
M(u_i)=A_i/D^\delta,\qquad H_i=\det A_i\ne0,
\]
so
\[
N_{F/\mathbb Q(T)}(u_i)=H_i/D^{\delta^2}.
\]
The matrices and polynomials need not be expanded. Formal norm bounds give computable
\[
\log_2\|D\|_1,\ \log_2\|H_i\|_1\le B=\operatorname{poly}(N),
\qquad
\log \deg_T H_i=\operatorname{poly}(N).
\]

Define the following **proof-only** prime set:
\[
P=\operatorname{Supp}\!\left(
\operatorname{cont}(D)\prod_i\operatorname{cont}(H_i)
\right).
\]

### Why this support suffices

For \(p\nmid\operatorname{cont}(D)\), every coefficient of monic \(f\), and every original \(u_i\), is integral for the \(p\)-Gauss valuation. Thus every extension \(w\) satisfies \(w(u_i)\ge0\).

If also \(p\nmid\operatorname{cont}(H_i)\), then
\[
v_{p,\mathrm{Gauss}}\!\left(N(u_i)\right)=0.
\]
The norm valuation is a positive weighted sum of the extension valuations. Consequently every \(w(u_i)=0\).

Therefore all nonzero rows occur over \(P\). Moreover,
\[
|P|\le \log_2|\operatorname{cont}(D)|
       +\sum_i\log_2|\operatorname{cont}(H_i)|
       =\operatorname{poly}(N).
\]
There are at most \(\delta\) extensions per prime. This proves a polynomial output-size bound; it does **not** find the primes.

No additional field-lattice denominator oracle is needed for this support argument. Local lattice normalization can be computed at the primes that are actually supplied.

### A sufficient global certificate

For each \(H_i\), it would suffice to compute an explicit nonzero integer \(C_i\), of polynomial bit length, with a proved guarantee
\[
\operatorname{cont}(H_i)\mid C_i. \tag{1}
\]
Factoring
\[
\operatorname{cont}(D)\prod_i C_i
\]
then gives a paid superset of the required primes. Extra primes cause no correctness problem.

Existence of a suitable \(C_i\) is trivial: any nonzero coefficient works. **Computing one is not paid by PIT.** Neither a nonzero modular evaluation nor its least integer representative is generally divisible by the content.

---

## 2. A constructive known-prime compiler, including alignment

Here is how to handle a supplied polynomial-bit prime \(p\). This part does not require discovering the constant field.

### 2.1 Preserve joint valuation data, not just separate norms

Form the proof-only joint characteristic polynomial
\[
\mathcal C(T,Z)
 =\det\!\left(D^\delta Z_0 I+\sum_{i=1}^k Z_iA_i\right).
\]
It has at most
\[
S=\binom{k+\delta}{\delta}
\]
coefficient polynomials in \(T\). Although \(S\) can be exponential, \(\log S\) is polynomial.

Formal determinant bounds give:

* coefficient-polynomial \(\ell_1\)-norm at most \(2^{B_1}\), with \(B_1=\operatorname{poly}(N)\);
* \(T\)-degree at most \(d_1\), with \(\log d_1=\operatorname{poly}(N)\).

Include the input denominators, cleared discriminant numerator, and norm numerators in these bounds.

Choose an explicitly represented field \(\mathbb F_q\), \(q=p^r\), with
\[
q>\frac{4(S+\operatorname{poly}(N))(d_1+1)}{\varepsilon},
\]
and also \(q\) larger than a fixed polynomial in \(\delta\). Thus
\[
r\log p=\operatorname{poly}(N,\log p,\log(1/\varepsilon)).
\]

For each nonzero coefficient polynomial \(G(T)\), divide it **for the proof only** by its maximal coefficientwise power of \(p\). Its reduction is nonzero. Schwartz–Zippel and a union bound show that a uniform \(t\in\mathbb F_q^s\), with probability at least \(1-\varepsilon\), preserves the Gauss valuation of **every coefficient of \(\mathcal C\)** and of the additional listed polynomials.

No coefficient is extracted and no exponential list is enumerated.

### 2.2 Why this preserves the aligned rows

Over an algebraic closure of the Gauss completion, let
\[
a_{\ell i}=w\!\left(u_i^{(\ell)}\right),\qquad 1\le\ell\le\delta,
\]
with valuations normalized by \(w(p)=1\).

The weighted Gauss valuation of the normalized joint characteristic polynomial is the function
\[
F(x_0,\ldots,x_k)
 =\sum_{\ell=1}^{\delta}
   \min\{x_0,x_1+a_{\ell1},\ldots,x_k+a_{\ell k}\}. \tag{2}
\]
Preserving all coefficient valuations preserves this entire function.

Crucially, (2) determines the **joint multiset of row vectors**
\[
(a_{\ell1},\ldots,a_{\ell k}).
\]
Indeed, away from ties, its derivative with respect to \(x_0\), evaluated at \(x_0=0,\ x_i=-t_i\), counts
\[
\#\{\ell:a_{\ell i}>t_i\text{ for every }i\}.
\]
These joint upper-orthant counts determine the finite multiset.

Thus the specialization preserves aligned valuation tuples—not merely each element’s separate valuation distribution. This avoids the conjugate-matching failure illustrated in the supplied notes.

### 2.3 Compute the specialized rows without a local-factor oracle

Lift \(\mathbb F_q\) to an unramified \(p\)-adic coefficient ring, represented modulo \(p^K\). Evaluate all sparse input coefficients by binary powering.

A polynomial amount of \(p\)-adic precision suffices:

* the preserved denominator, discriminant and norm valuations are bounded by their polynomial logarithmic coefficient bounds;
* scaling \(Y\) by \(p^a\), for polynomially bounded \(a\), gives an integral monic presentation;
* its discriminant valuation is \(O(\delta^2 B_1)\);
* a polynomial scaling makes every original \(u_i\) integral, with polynomially bounded total norm valuation.

For example, after enlarging \(B_1\) to include the denominator-clearing bounds, a conservative allocation
\[
K=100(\delta+k+1)^4(B_1+1)^2
\]
base-\(p\) digits dominates the following normalization and determinant precision losses. The charged bit precision is \(K\log p\), not an uncharged real-precision parameter.

An elementary order-normalization algorithm supplies the local lattice:

1. Start with the integral monogenic order \(A\).
2. Compute the nilradical of \(A/pA\). Over \(\mathbb F_q\), it is the kernel of a sufficiently high Frobenius power; this is finite-field linear algebra.
3. Let \(I\) be its inverse image in \(A\), and replace
   \[
   A\longmapsto (I:I)=\{x:xI\subseteq I\}.
   \]
   Since \(pA\subseteq I\), this enlargement lies in \(p^{-1}A\) and is found by linear algebra over the residue field.
4. Every strict enlargement decreases discriminant valuation by at least two. Hence there are only polynomially many iterations.

The stopping criterion is justified, not assumed. If the integral closure \(O\) strictly contains \(A\), the finite module \(O/A\) has a nonzero element annihilated by \(I\). A representative \(x\notin A\) then satisfies \(xI\subseteq I\), so \((I:I)\ne A\). Conversely, for a product of DVRs, the radical’s multiplier ring is the order itself.

Decompose the resulting finite residue algebra using ordinary dense finite-field factorization of degree at most \(\delta\), and lift its idempotents. Use those **same idempotents for every original \(u_i\)**. Component multiplication determinants give
\[
w_j(u_i)=
\frac{v_p\!\left(N_{L_j/L}(u_i)\right)}{[L_j:L]}.
\]
The norm bounds ensure that the allocated precision determines these valuations exactly.

All operations have polynomial cost in
\[
N,\ \log p,\ \log(1/\varepsilon).
\]
Binary \(T\)-degrees enter through modular powering and \(\log d_1\), never through a numerical-degree loop. The output has at most \(\delta\) rational rows. The joint-characteristic argument proves that these are exactly the original Gauss-extension row tuples, allowing duplicates.

Once the prime support is complete, restrictions of these places cover every finite place of the constant field. Hence their kernel intersected with the supplied Alg is exactly the algebraic-unit lattice.

---

## 3. A native growing-\(\delta\) falsifier with nonzero Alg

The following family catches three tempting implementations: using only input coefficient contents, taking gcds of modular residues, and factoring expanded rational evaluations.

Let
\[
P(Z)=Z^3+3Z+3,
\]
let \(d\ge1\), and let \(M\ge2\) be binary encoded. Put
\[
f(T,Y)=P(Y^d-T^M),\qquad \delta=3d.
\]
This has only four nonzero \(Y\)-coefficients:
\[
Y^{3d}-3T^M Y^{2d}
 +(3T^{2M}+3)Y^d
 -T^{3M}-3T^M+3.
\]

Let
\[
A(T)=T^M(T^{2M}-1),
\]
and supply the original sparse atoms
\[
u_1=A(T)(Y^d-T^M-1),\qquad u_2=A(T).
\]

### Irreducibility

\(P\) is Eisenstein at \(3\). If \(\alpha\) is a root and \(K=\mathbb Q(\alpha)\), then \(T^M+\alpha\) is squarefree in \(K[T]\). At any irreducible factor of it,
\[
Y^d-(T^M+\alpha)
\]
is Eisenstein. Its degree over \(K(T)\) is \(d\).

Since \(\alpha=Y^d-T^M\), the total degree over \(\mathbb Q(T)\) is \(3d\), proving that the displayed native \(f\) is irreducible.

### Alg is nonzero, and the omitted prime matters

Set \(c=\alpha-1\). Then
\[
u_1/u_2=c,\qquad
\mathrm{Alg}=\mathbb Z(1,-1).
\]
Moreover,
\[
N_{K/\mathbb Q}(c)=-P(1)=-7,
\]
so
\[
N_F(u_1)=(-7)^d A(T)^{3d},\qquad
N_F(u_2)=A(T)^{3d}. \tag{3}
\]

All nontrivial contents of the **input coefficient polynomials** are supported at \(3\). Nevertheless, the relevant vertical support is \(7\).

At \(7\),
\[
P(Z)\equiv (Z-1)(Z^2+Z+4),
\]
with the factors coprime. The constant \(c\) has valuation \(1\) at the degree-one place and valuation \(0\) at the other place. Since primitive \(A(T)\) has Gauss valuation zero, a required row is
\[
(1,0).
\]
It excludes \((1,-1)\) from the unit kernel. In fact that unit kernel inside Alg is zero.

Thus an input-content-only gcd-free implementation gives a wrong answer **on a nonzero Alg lattice**.

### Why modular residues are not content witnesses

If \(H(t)=c\,b\), then
\[
H(t)\bmod m=c\,b-mq.
\]
Unless the modulus is already known to be divisible by \(c\), its integer representative need not be divisible by \(c\).

For example, take \(M=2^n+1\), \(n\ge2\), specialize \(T=2\) modulo \(5\), and use (3). Then \(A(2)\equiv1\pmod5\); the nonzero norm residues lie in \(\{1,2,3,4\}\). Factoring or gcd-ing those representatives need not reveal \(7\).

Choosing larger moduli does not fix the general inference: the coefficient-height bound is not a bound on the expanded integer value at \(T=2\).

### Why enormous evaluations are genuinely uncharged here

Every rational \(a\) for which both atoms remain nonzero satisfies
\[
a\notin\{0,1,-1\}.
\]
Writing \(a\) in lowest terms shows
\[
h(A(a))\ge M h(a)\ge M\log2.
\]
Thus the expanded value of \(N_F(u_2(a))\) has height at least \(3dM\log2\), exponential in \(\log M\).

This family is **not claimed hard**: its displayed factorization makes it easy. It is an exact falsifier of the three implementation rules above, not a lower bound against other algorithms.

---

## 4. An exact reduction for the support-discovery obligation

Consider the independent input problem:

* sparse \(g,h\in\mathbb Z[T][Y]\);
* \(g\) monic of numerical \(Y\)-degree \(\delta\);
* \(\deg_Yh<\delta\);
* \(\gcd(g,h)=1\) over \(\mathbb Q(T)[Y]\);
* binary \(T\)-degrees.

Find all primes for which \(g,h\) acquire a common factor over \(\mathbb F_p(T)\), allowing \(h\bmod p=0\).

Introduce one new parameter \(X\), and set
\[
f(T,X,Y)=g(T,Y)+Xh(T,Y),\qquad u=h(T,Y).
\]
This is a polynomial-size native construction.

Because \(g,h\) are coprime, the polynomial linear in \(X\) is primitive and irreducible over \(\mathbb Q(T)[Y,X]\). Since it is monic in \(Y\), it remains irreducible over \(\mathbb Q(T,X)[Y]\). Also
\[
N_f(u)=\operatorname{Res}_Y(g+Xh,h)
      =\operatorname{Res}_Y(g,h). \tag{4}
\]

Consequently, complete norm-support discovery for promised native irreducible inputs solves the bad-modular-gcd-prime problem for **arbitrary such sparse resultant pairs**. Conversely, that problem supplies the needed support.

Equation (4) rules out an argument that monicity and promised irreducibility somehow make the norm-content witness automatic.

**Scope limitation:** for arbitrary pencil examples, Alg can be zero. This is a reduction for the expressly requested complete-support operation, not a hardness reduction for every conceivable kernel-only unit algorithm. The family in §3 separately shows that the proposed shortcuts fail when Alg is nonzero. Combining these statements into an impossibility theorem would be invalid.

The missing constructive obligation is therefore still (1), or a genuinely different support-discovery method. Integer factoring of explicit polynomial-bit integers does not, by itself, produce that witness.

---

## 5. Torsion and exact identity can be paid classically

Suppose the finite-place gate and the separately attacked archimedean/log-lattice gates eventually return a basis \(B_{\rm tor}\) for the exponent lattice whose products are roots of unity.

The supplied degree bound gives
\[
|\mu(E)|\le W:=2\delta^2
\]
for the relevant constant field \(E\).

A numerical phase computation is unnecessary:

1. Choose a large prime \(p>W\), and a good full finite-algebra specialization of the **original atoms**, using the retained coefficient/degree bounds.
2. Evaluate every \(B_{\rm tor}\)-basis product by binary powering. No characteristic-zero algebraic product is expanded.
3. Enumerate the subgroup generated by these images. It has at most \(W\) elements.

Reduction is injective on this torsion subgroup. If a nontrivial root \(\zeta\) of order \(n\le W\) reduced to \(1\), the identity
\[
1+\zeta+\cdots+\zeta^{n-1}=0
\]
would reduce to \(n=0\) in characteristic \(p\), impossible because \(p>W\).

The enumerated group is cyclic. Find a generator by enumeration, record each basis image as its power, and compute the resulting integer congruence kernel. Lifting through \(B_{\rm tor}\) gives the **full, possibly nonsaturated** identity-relation lattice.

This costs polynomially many explicit finite-algebra operations and uses neither general finite-field discrete logarithms nor an uncharged root-of-unity phase oracle.

### Algorithm classification

If (1) were supplied and its explicit integers factored, then—**conditional also on the separate archimedean and lattice proofs**—this route would be a randomized **classical factoring-oracle** algorithm.

It would not yet be an unconditional classical polynomial-time dequantization. Indeed, the demanded prime-labelled complete support compiler already factors explicit integers on inputs \(u=N\). A factor-free relation algorithm might avoid that stronger output requirement, but none is constructed here.

Using quantum factoring would pay the factoring calls, but would leave a quantum component rather than establish a full classical match.

---

## Admission boundary and cheapest falsifier

**Constructed:** supplied-prime aligned rows, their precision/lattice costs, and the final torsion/identity step.

**Still unpaid:** a complete polynomial-bit support witness for arbitrary implicit sparse resultant contents.

**Separately conditional:** the torus analytic/precision argument and logarithmic-lattice extraction. Nothing above validates those sketches.

The cheapest exact falsifier for an alleged finite-place implementation is §3 with \(d=2\) and a large binary \(M=2^n+1\): its returned rows must exclude \((1,-1)\) from the algebraic-unit kernel, and must account for prime \(7\). Passing that example would not establish the general support-discovery operation; producing and proving that operation remains the outstanding obligation.