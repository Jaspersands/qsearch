## Verdict

**The arbitrary singular-plane-input bridge is not established by the supplied sources.** This is a missing uniform bit-complexity lemma, not a counterexample to the bridge or evidence of hardness.

Two narrower conclusions can be proved:

1. A **certified two-chart normalization presentation** suffices to construct the requested \(M\), one basepoint field, and polynomial-size exact RR coordinates.
2. Once such an \(M\) exists with polynomial bit length, finding a **numerically polynomial auxiliary prime** is elementary and requires no integer factorization.

There is also a genuine \(F\)-only subclass: **smooth projective plane curves**, with growing genus. That subclass does not settle the allowed singular input.

## 1. Attack on the proposed transfer

- **Kozen’s output is local resolution data.** Its stated problem is exceptional places, local parameters and birational reparametrizations. The passive-factorization representation avoids constructing a splitting field. Neither that statement nor the supplied analysis provides a global proper smooth arithmetic model, compatible specialization certificates, or number-field RR coefficient bounds.
- **Abelard explicitly excludes the needed costs.** Lines 86–91 count field operations and disclaim coefficient growth and extension costs. The arithmetic-operation bounds cannot be promoted to the requested bit bound.
- Spreading out a characteristic-zero normalization proves existence of *some* finite exceptional set. It does not establish polynomial construction time or polynomial \(\log |M|\).
- A polynomial-size arithmetic circuit alone does not bound coefficient bits: repeated squaring already demonstrates the distinction.
- For a singular projective plane equation, its plane discriminant vanishes identically. Taking that discriminant as \(M\) produces \(M=0\), not a certificate.

Thus the local-resolution, arithmetic-normalization and RR-height transfers must be proved separately.

## 2. A sufficient, explicit weaker input

Let \(d=[K(C):K(x)]\le D\). In addition to \(F\), supply the following data, **not RR bases**.

### Two finite free algebras

Supply bases \(e_0,e_\infty\) and multiplication tables for
\[
B_0/K[x],\qquad B_\infty/K[u],\quad u=x^{-1},
\]
both free of rank \(d\), together with:

- rational-function coordinates and inverse generic identifications with \(K(C)\);
- an algebra-compatible transition
  \[
  e_\infty=e_0T(x),\qquad
  T,T^{-1}\in\operatorname{Mat}_d(K[x,x^{-1}]);
  \]
- explicit identities verifying multiplication, the generic identifications and the transition.

### Smoothness and coverage certificates

Supply a finite standard-smooth atlas for these algebras: localized presentations with \(s\) variables, \(s-1\) equations and an invertible specified Jacobian minor, plus inverse-map and covering identities. The identities must be explicitly encoded, not merely asserted.

Let \(A\) bound all relevant polynomial degrees and Laurent exponents, and let the complete coefficient, field and certificate bit sizes be charged.

These data glue to a finite flat morphism
\[
\mathcal C\longrightarrow \mathbf P^1
\]
after clearing finitely many scalar denominators. Hence the model is proper and flat; the atlas certifies smoothness. Its generic fiber is \(C\). Proper smoothness and geometric connectedness of the generic fiber give geometrically connected smooth fibers after this localization.

**This input allows singularities in the displayed plane equation.** Smoothness is certified on its normalization, not assumed for \(F\).

The unresolved native claim is that these certificates can always be *constructed from \(F\)* with \(A\), coefficient heights and total encoding length polynomial in the original sizes.

## 3. One basepoint field and an explicit RR system

### One regular-fiber point

Form a nonzero bad-fiber polynomial incorporating:

- the leading coefficient and separability resultant of \(F\);
- denominators and determinants needed for the supplied generic identifications.

Its degree is polynomial in \(D\) and the certified presentation size. Testing
\[
a=0,1,\ldots,\deg B
\]
finds \(B(a)\ne0\).

Choose one irreducible factor \(q(Y)\) of the squarefree fiber polynomial \(F(a,Y)\), using exact number-field **polynomial** factorization, with its bit cost charged. This is not integer factorization. Set
\[
L=K[b],\qquad q(b)=0,\qquad O=(a,b).
\]
Then
\[
[L:K]\le d\le D.
\]

Coefficient bounds for this field are polynomial: evaluation at \(a\), scaling to an integral monic polynomial, root bounds, and bounds for coefficients of monic factors give polynomial coordinate heights in the charged number-field basis. A scaled power-basis order in \(L\) suffices; its discriminant is computed by a trace determinant. **No maximal-order computation is required.**

All subsequent calculations use this one field \(L\). Finite product or truncated algebras below are represented by multiplication tables, not replaced by composita of their residue fields.

### RR without an uncharged RR theorem

Take \(k\ge1\), and write
\[
h=(x-a)^k f.
\]
For \(f\in L(kO)\), \(h\) is regular over finite \(x\), and has poles bounded by \(k\,x^*(\infty)\). Thus
\[
h=e_0v(x),\qquad v\in L[x]^d,
\]
and
\[
x^{-k}T^{-1}(x)v(x)\in L[x^{-1}]^d. \tag{1}
\]

Conversely, this gives the required infinity condition.

Because both \(T\) and \(T^{-1}\) have Laurent exponents in \([-A,A]\), every solution of (1) satisfies
\[
\deg v_i\le k+A.
\]
Consequently there are
\[
N=d(k+A+1)
\]
unknown coefficients. Equation (1) imposes at most \(2dA\) coefficient equations.

For the finite-fiber conditions, use the algebra
\[
E_k=(B_0\otimes_K L)/(x-a)^k,
\qquad \dim_L E_k=dk.
\]
Its reduction at \(x=a\) is étale. The rational point \(O\) determines one idempotent \(\epsilon_1\). Compute it by linear algebra, then lift it uniquely to \(\epsilon_k\in E_k\). For example,
\[
e\longmapsto 3e^2-2e^3
\]
doubles the order of its idempotency defect.

Impose
\[
(1-\epsilon_k)h=0\quad\text{in }E_k. \tag{2}
\]
These are at most \(dk\) further linear equations. They impose order-\(k\) vanishing at every other point of the fiber **without splitting those points**.

The kernel of (1)–(2) is exactly
\[
L(kO)=
\left\{
\frac{e_0v(x)}{(x-a)^k}
\right\}.
\]

This gives an explicit system with

\[
\boxed{\text{columns }d(k+A+1),\qquad
\text{rows }\le d(k+2A).}
\]

### Bit and output bounds

Let \(m=[L:\mathbf Q]\), and let \(h_*\) bound a common-denominator encoding of the field tables, supplied matrices and computed fiber-idempotent data. Computing \(\epsilon_1\) uses determinants of polynomial-size matrices, so \(h_*\) is polynomial in the charged data.

There are \(O(\log k)\) idempotent updates. Their composed polynomial degree is at most
\[
3^{\lceil\log_2 k\rceil}\le 3k^2.
\]
Using common denominators throughout, this gives a conservative matrix-entry bit bound of the form
\[
B_{\rm sys}
=
O\!\left((k+A+1)^2
 \bigl(h_*+A\log(|a|+2)+\log(md(k+A+2))\bigr)\right),
\]
after charging the coordinate-conversion tables.

Expanding over \(\mathbf Q\) gives at most \(mN\) columns. Fraction-free linear algebra and determinant bounds give kernel-coordinate bits
\[
O\!\left(mN\bigl(B_{\rm sys}+\log(mN)\bigr)\right).
\]
An \(L\)-basis can be selected from these vectors by exact independence tests.

Thus the rational-function degrees, coefficient bits, computation time and **total output size** are polynomial in the certified input and numerical \(k\). Computing the finitely many spaces with \(k\le c(g+1)\), for fixed \(c\), remains polynomial. No constant exponential in \(g\) is being suppressed.

## 4. Constructing the integer certificate \(M\)

Collect:

1. denominators of field, algebra, atlas, transition and generic-identification data;
2. the order discriminants for \(K\) and \(L\);
3. nonzero coefficients ensuring that generic-identification denominators remain nonzero polynomials;
4. the regular-fiber and point-extension discriminants;
5. denominators and selected nonzero rank minors for the RR systems being retained.

For each required nonzero algebraic scalar, clear its denominator to obtain an order element \(c\), and include
\[
\left|N_{L/\mathbf Q}(c)\right|
\]
in the product defining \(M\). Constants originally in \(K\) can be treated in \(K\) or \(L\). Include the rational denominator-clearing integers as well.

Every factor is nonzero. Norms and discriminants are determinants; neither computing nor using \(M\) requires factoring it. For a scalar of coordinate height \(b\), its norm has bit length bounded by
\[
O\!\left(m(b+\text{field-table bits}+\log m)\right).
\]
There are polynomially many factors, so \(\log |M|\) is polynomial in the certified input.

For every rational prime \(P\nmid M\):

- the smooth proper atlas and gluing identities survive;
- the supplied function-field identifications remain faithful;
- the chosen point extends over the chosen primes of \(L\);
- the retained RR systems preserve rank and their exact bases reduce compatibly.

This is a **sufficient**, deliberately nonminimal bad-prime certificate.

## 5. A numerically small auxiliary prime

This part is unconditional once \(M\) is available.

Let
\[
A_{\rm bad}=|M|\,\ell\,|G|,
\qquad
b=\left\lceil\log_2\max(2,A_{\rm bad})\right\rceil,
\]
with the encoding/computation of \(|G|\) charged. Let \(T\) be the required numerical lower bound, such as \(\max(D,2g)\).

There are at most \(b\) distinct prime divisors of \(A_{\rm bad}\), and at most \(T\) primes at most \(T\). Therefore, among the first
\[
r=\lceil T\rceil+b+1
\]
primes, one satisfies
\[
P>T,\qquad P\nmid A_{\rm bad}.
\]
The \(r\)-th prime is \(O(r\log(r+2))\). Sieve to this polynomial numerical bound and test remainders against \(A_{\rm bad}\).

This is deterministic polynomial bit work and uses **no integer factorization**. At this small \(P\), selecting residue-field factors can also be done in time polynomial in numerical \(P\) and the charged algebra degree. The resulting residue degree is at most \([L:\mathbf Q]\).

**Necessary interpretation:** the group condition is \(P\nmid\ell|G|\). If one literally requires \(P>\ell|G|\), a numerically polynomial \(P\) need not exist when only the *bit length* of \(|G|\) is polynomial.

## 6. An actual \(F\)-only subclass

If the **projective homogenization** of \(F\) is smooth, the preceding normalization input can be constructed directly.

A small linear coordinate change makes \(F\) monic in \(y\) of total degree \(D\). Then
\[
e_0=(1,y,\ldots,y^{D-1}),\qquad
e_\infty=(1,y/x,\ldots,(y/x)^{D-1}),
\]
and
\[
T=\operatorname{diag}(1,x^{-1},\ldots,x^{-(D-1)}).
\]
The two plane charts cover the curve. Their smoothness is certified by the nonzero homogeneous gradient resultant, excluding \(P\mid D\) and its norm. Resultant matrices here have polynomial size in \(D\) in **three projective variables**; determinant bounds pay coefficient growth.

The RR construction above applies with \(A=O(D)\). This subclass already has
\[
g=(D-1)(D-2)/2,
\]
so it is not a fixed-genus result.

It does **not** cover the requested singular plane presentations.

## Remaining obligation and falsifiers

**Missing lemma:** from arbitrary geometrically integral separable \(F\), construct the two normalization bases, Laurent transition, generic identifications, and smoothness/coverage certificates above, including infinity, with polynomial degrees, coefficient bits and total construction cost over the charged number field.

Neither supplied source proves that combined lemma.

Concrete rejection tests for a proposed closure:

- \(Y=P y\) can destroy the displayed reduction while preserving abstract good reduction. A certificate ignoring presentation denominators fails.
- A plane discriminant equal to zero on a singular input cannot be the required nonzero \(M\).
- A compositum of all branch fields is not justified by bounds on their individual degrees.
- A bound \(D^{O(g)}\), or field-operation counts without coefficient bounds, does not meet the native requirement.

These falsify shortcuts, not the existence of the general bridge. No finite examples or genus-31 controls settle the missing lemma. The established conclusions remain classical and do **not** pay torsion-coordinate reconstruction height or the numerical precision needed for rational reconstruction.