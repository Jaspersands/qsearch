## Result and scope

A complete **supplied-zeta construction is possible without splitting all of \(J[\ell]\)**. The useful reduction is:

1. Make the deck transformations rational over a polynomial-degree constant extension.
2. Work with Frobenius-primary subspaces whose irreducible factors have bounded degree.
3. Certify each needed primary subspace using its **Weil-dual, reciprocal-twist primary subspace**.
4. Compute the \(G\)-equivariant homomorphisms by linear algebra.
5. Descend the resulting, complete module to a small common field and construct actual divisor representatives there.

Couveignes’s possible strict-subgroup output is not a completeness certificate. Below, it is wrapped in exact rank and final-dimension certificates.

There is one specification issue concerning Frobenius:

> The curve and its marked geometric deck group determine genuine Frobenius on the isotypic span in \(J[\ell]\). If Frobenius merely normalizes \(G\), they do not, by themselves, determine a uniquely normalized Frobenius on the separate multiplicity space \(W\). One must specify the arithmetic linearization of the coefficient module \(M^*\), or accept the exact compatible family described below.

This is a scalar ambiguity, not a torsion-computation obstruction. In the constant-\(G\), constant-coefficient convention, the linearization is \(I\), and the algorithm produces the requested \(W\)-matrix with no additional Frobenius advice.

I take the already established geometric dimension
\[
m:=\dim_{\mathbf F_\ell}W=(r-2)n
\]
as given. I do not revisit the closed group-cohomology lemma or use the erroneous parabolic stopping dimension.

---

## 1. Countertests before choosing the fields

These are exact symbolic checks, not executed numerical controls.

### 1.1 A small target does not make the ambient splitting field small

On a \(2s\)-dimensional symplectic space, take
\[
F=\operatorname{diag}(A,qA^{-t}),
\]
where \(A\) is multiplication by a primitive element of \(\mathbf F_{\ell^s}\). This is a \(q\)-similitude, and its order is divisible by \(\ell^s-1\). Adding a fixed small summand does not remove that large order.

This is a linear-algebra falsifier of a proposed ambient-field bound, not a claim that every such matrix is realized by the covers in the contract. It shows why a bound using the target dimension cannot be applied to all of \(J[\ell]\).

### 1.2 Eigenvalue orders do not kill unipotent parts

For
\[
F=\lambda(I+N),\qquad N^u=0,
\]
the factor \(\ell^{\deg f}-1\), where \(f\) is the minimal polynomial of \(\lambda\), kills the semisimple part but need not kill \(I+N\). An additional
\[
\ell^{\lceil\log_\ell u\rceil}
\]
is sufficient and can be necessary.

Thus a large ambient \(f\)-primary block cannot be rationalized using only the nilpotence bound for the small target \(W\).

### 1.3 Pairing a primary block with itself can give rank zero

For
\[
F=\operatorname{diag}(a,q/a)
\]
on a symplectic plane, the \(a\)-eigenline is isotropic unless it coincides with its dual block. Its correct partner is the \(q/a\)-eigenline.

In particular, rational \(\ell\)-torsion can have a degenerate restricted Weil pairing. “The pairing on the returned subgroup is singular” is not a certificate of incompleteness unless the correct dual blocks have been included.

### 1.4 One unsuccessful torsion run proves no absence

Couveignes Theorem 1 explicitly permits a strict subgroup. Moreover, even a correct computation over a field not splitting the target can return too little.

Neither failure to find another point nor failure to reach \(m\) at one extension certifies that the missing classes do not exist.

### 1.5 Rational divisor classes do not give a polynomial common support field

An effective rational divisor of degree \(g\) can have closed support points with degrees forming a partition of \(g\). Their least common multiple need not be polynomial in \(g\). For instance, partitions consisting of distinct primes give a superpolynomial product.

Consequently, “each support degree is at most \(g\)” does **not** pay a common field in which all support points are rational. Below I give both rational-divisor coordinates and, if desired, a construction with individually rational support points in one polynomial-degree field.

### 1.6 Normalizer data do not determine the coefficient-module scalar

Suppose \(A\) implements the Frobenius automorphism \(\alpha\) of \(G\):
\[
A\rho^*(g)A^{-1}=\rho^*(\alpha(g)).
\]
Then \(cA\) implements the same automorphism for every \(c\in\mathbf F_\ell^\times\). If the induced multiplicity-space matrix is \(B\), replacing \(A\) by \(cA\) replaces it by \(c^{-1}B\).

Even specifying a symplectic multiplier does not necessarily resolve this: \(A\) and \(-A\) have the same multiplier. This ambiguity must not be hidden by choosing an arbitrary intertwiner and calling its resulting \(B\) the original Lefschetz-module Frobenius.

---

## 2. Precise supplied-zeta theorem

Write:

- \(g=g(C)\), distinct from the fixed fibre genus;
- \(d=\deg C\) in the supplied plane presentation;
- \(D=\deg(C\to\mathbf P^1)=|G|\);
- \(V=J_C[\ell](\overline{\mathbf F}_q)\);
- \(S=M^*\), with its specified \(n\)-dimensional representation \(\rho^*\);
- \(W=\operatorname{Hom}_G(S,V)\), of known dimension \(m\).

Use the canonical, Galois-equivariant Kummer identification
\[
H^1(C_{\overline{\mathbf F}_q},\mu_\ell)=J_C[\ell].
\]
There is no silent replacement here by untwisted \(H^1(C,\mathbf F_\ell)\).

### Theorem

Assume the contract’s curve, cover, deck-action and dimension promises, and supply the genuine zeta numerator of \(C/\mathbf F_q\). Use the finite-field normalization, divisor, factorization and Riemann–Roch primitives stipulated in the supplied audit, charging their model sizes, numerical divisor degrees and numerical characteristic \(P\).

Then, for every \(0<\eta<1\), there is a classical, finite-clock randomized algorithm that either returns `FAIL` or returns:

1. a certified basis \(\phi_1,\ldots,\phi_m\) of the **complete** space \(W\);
2. the \(n\) component torsion classes of each \(\phi_i\), represented by explicit divisors over one common finite field;
3. if requested, representatives whose individual support points all have coordinates in one common polynomial-degree field;
4. the genuine arithmetic \(q\)-Frobenius on the isotypic span
   \[
   E=\sum_{\phi\in W}\phi(S)\subseteq V;
   \]
5. for any specified compatible arithmetic linearization \(A\) on \(S\), the exact matrix
   \[
   F_W(\phi)=F_q\circ\phi\circ A^{-1}.
   \]

In the normalizer case, if no coefficient linearization is specified, the algorithm instead returns the actual \(F_E\), the induced automorphism \(\alpha\) of \(G\), and all compatible pairs
\[
(cA_0,c^{-1}B_0),\qquad c\in\mathbf F_\ell^\times.
\]
Here compatibility with the natural representation is checked by explicit intertwiner equations. In the intended symplectic-normalizer case those equations have an invertible solution.

Every returned answer is exact. With valid inputs, the probability of returning `FAIL` is at most \(\eta\). The cost is
\[
\operatorname{poly}_{n,r}\!\left(
\ell,\ P,\ d,\ g,\ \text{charged presented bits},\ \log(1/\eta)
\right).
\]
In particular, under the contract’s polynomial degree/genus bounds, this has the requested supplied-zeta complexity.

The proof and the field bounds follow.

---

## 3. Paid preprocessing: deck field, smooth model and degree-one divisor

Couveignes Theorem 1 does not supply its own smooth model or degree-one divisor. They must be prepared before applying it.

### 3.1 A polynomial common deck field

For prime \(\ell\) and fixed \(n\), choose a fixed-size elementary generating set
\[
\Gamma=\{g_1,\ldots,g_s\}
\]
of \(G=\operatorname{Sp}_n(\mathbf F_\ell)\), with \(s=O(n^2)\). Parameter \(1\) root elements suffice because \(\ell\) is prime.

Arithmetic Frobenius permutes the geometric deck transformations, giving
\[
\alpha\in\operatorname{Aut}(G).
\]
An automorphism is determined by the images of \(\Gamma\), so
\[
|\operatorname{Aut}(G)|\le |G|^s.
\]
Hence all deck transformations are defined over an extension of degree at most
\[
B_D:=|G|^s.
\]

This gives a finite constructive search:

- for \(a=1,\ldots,B_D\), apply \(q^a\)-power Frobenius to the coefficients of the \(s\) generator maps;
- compare the resulting rational maps with the original maps in the curve’s function field;
- stop at the first common period \(a_D\).

The equalities are exact function-field equalities. Descent of the coefficients to the corresponding finite subfields is finite-field linear algebra. This does not take an uncontrolled least common multiple of fields supplied for arbitrarily many deck maps.

All deck maps are then rational over \(\mathbf F_{q^{a_D}}\).

### 3.2 A rational point, not a free Picard representative

Normalize the supplied separable function-field model using the charged normalization primitive.

From a separable presentation over \(\mathbf P^1\), compute a bad-fibre polynomial containing the leading-coefficient, denominator and discriminant obstructions. Let its degree be \(\Delta\); it is polynomial in the charged presentation degrees.

Choose
\[
u=\min\{j\ge1:q^{a_Dj}>\Delta\}.
\]
Test \(\Delta+1\) distinct values of the base coordinate over \(\mathbf F_{q^{a_Du}}\). At least one avoids the bad fibres. Factor that fibre and choose **one** irreducible factor, of residue degree \(e\le D\).

After extending to
\[
k_0=\mathbf F_{q^b},\qquad b=a_Due,
\]
there is an explicit rational point \(O\in C(k_0)\). In particular,
\[
b\le |G|^s D\max\!\left(1,\left\lceil\log_2(\Delta+1)\right\rceil\right).
\]

If the chosen Riemann–Roch representation requires a rational infinite place, replace the base coordinate \(t\) by \(1/(t-a)\), where \(a\) was the chosen fibre value. The selected point is then a rational place above infinity. No splitting field of the other infinite places is needed.

This pays Couveignes’s degree-one-divisor hypothesis with the particularly convenient choice \(O^+=O\), \(O^-=0\).

### 3.3 Derived zeta polynomials are charged, not oracles

Let \(\chi\) be the supplied characteristic polynomial of \(F_q\) on \(J\). For every extension degree \(v\) used below, compute
\[
\chi_v(X)=\prod_{i=1}^{2g}(X-\alpha_i^v)
\]
by exact resultant, companion-matrix or power-sum arithmetic.

Its coefficient bit sizes are \(O(gv\log q+g)\), and the computation is polynomial in those quantities. In particular,
\[
\#J(\mathbf F_{q^v})=\chi_v(1)
\]
is available exactly.

No zeta computation from the original plane equation has been performed at this step.

---

## 4. Why only bounded-degree Frobenius factors are needed

Set
\[
F_0:=F_q^b,\qquad q_0=q^b.
\]
All deck maps are rational over \(k_0\), so \(F_0\) commutes with \(G\).

The natural module \(S=M^*\) is absolutely simple and
\[
\operatorname{End}_G(S)=\mathbf F_\ell.
\]
Therefore evaluation gives an injection
\[
S\otimes_{\mathbf F_\ell}W\longrightarrow V,
\qquad v\otimes\phi\longmapsto\phi(v),
\]
whose image is \(E\). Thus
\[
E\simeq S\otimes W,\qquad \dim E=nm.
\]

This uses semisimplicity of the socle, not semisimplicity of the entire modular \(G\)-module. In particular, it does **not** average over \(G\); \(\ell\mid |G|\).

Because \(F_0\) commutes with \(G\), on \(E\) it has the form
\[
F_0|_E=I_S\otimes B_0
\]
for an invertible \(m\times m\) matrix \(B_0\).

Factor
\[
\overline{\chi_b}(X)=\prod_f f(X)^{e_f}
\]
over \(\mathbf F_\ell\), and let
\[
V_f=\ker f(F_0)^{e_f}.
\]
Every irreducible factor appearing in \(B_0\) has degree at most \(m\). Consequently
\[
W=\bigoplus_{\deg f\le m} W_f,
\qquad
W_f:=\operatorname{Hom}_G(S,V_f).
\tag{1}
\]

This is the key reduction. The full ambient dimension \(2g\) controls some nilpotent powers, but it does not enter the exponent \(\ell^{\deg f}\) for a required factor.

---

## 5. Primary fields and the correct pairing partners

Define
\[
\gamma=\min\{j\ge0:\ell^j\ge2g\}.
\]

For an irreducible factor \(f\) of degree \(a\le m\), put
\[
h_f=(\ell^a-1)\ell^\gamma,\qquad
K_f=\mathbf F_{q^{bh_f}}.
\tag{2}
\]

### 5.1 Rationality of the entire primary block

Over \(\overline{\mathbf F}_\ell\), the eigenvalues on \(V_f\) lie in \(\mathbf F_{\ell^a}^\times\), so their orders divide \(\ell^a-1\). After that power, only a unipotent part remains. Its nilpotence index is at most \(2g\), and the additional \(\ell^\gamma\) kills it.

Hence
\[
V_f\subseteq J[\ell](K_f).
\]

The bound is
\[
h_f<2g\,\ell^{m+1}.
\tag{3}
\]
There is no full-\(J[\ell]\) splitting assertion.

### 5.2 Reciprocal-twist partner

For monic \(f\) of degree \(a\), define
\[
f^\dagger(X)=\frac{X^a f(q_0/X)}{f(0)}.
\tag{4}
\]
Its roots are \(q_0/\lambda\) for roots \(\lambda\) of \(f\). It is irreducible of the same degree.

The Weil pairing satisfies
\[
e_\ell(F_0x,F_0y)=e_\ell(x,y)^{q_0}.
\]
It follows that \(V_f\) pairs trivially with every primary block except \(V_{f^\dagger}\), and
\[
V_f\times V_{f^\dagger}\longrightarrow\mu_\ell
\]
is perfect. In particular,
\[
e_{f^\dagger}=e_f,\qquad
\dim V_f=e_f\deg f.
\tag{5}
\]

Both blocks split over the same field \(K_f\). Also \(\ell-1\mid h_f\), so \(\mu_\ell\subset K_f\).

This covers self-dual factors as well as distinct reciprocal-twist pairs. No nondegeneracy of the Weil pairing on \(E\) itself is assumed.

---

## 6. Certified construction of each full primary block

Process the pairs \(\{f,f^\dagger\}\) with \(\deg f\le m\), processing a pair only once.

### 6.1 Use Couveignes under its actual hypotheses

Apply the supplied Theorem 1 over \(K_f\), with:

- the base-changed plane curve;
- the effective smooth model;
- the rational degree-one divisor \(O\);
- requested torsion exponent \(n_{\mathrm{Couv}}=\ell\);
- the exactly derived zeta polynomial over \(K_f\).

The theorem returns nothing, a strict subgroup, or a complete rational \(\ell\)-torsion basis. Its success probability is at least \(1/2\).

Check every returned divisor class for degree zero and \(\ell\)-torsion. Reject malformed or oversized output.

### 6.2 Exact primary projection

Compute the CRT idempotent
\[
p_f(X)\in \mathbf F_\ell[X]/(\overline{\chi_b})
\]
which is \(1\) modulo \(f^{e_f}\) and \(0\) modulo the other primary factors.

For each returned class \(t_i\), form
\[
a_i=p_f(F_0)t_i,\qquad
b_i=p_{f^\dagger}(F_0)t_i.
\]
Coefficients in \(\mathbf F_\ell\) mean integer scalar multiplication of divisor classes, not an embedding into the characteristic-\(P\) ground field.

Reduce after arithmetic operations to representatives
\[
G-gO,\qquad G\ge0,\quad \deg G=g,
\tag{6}
\]
using Riemann–Roch. The usual genus-\(g\) existence is constructive because \(O\) is an actual rational point.

### 6.3 Completeness certificate

Choose a primitive \(\ell\)-th root \(\zeta\in K_f\), and form
\[
P_{ij}=\log_\zeta e_\ell(a_i,b_j)\in\mathbf F_\ell.
\]
The logarithms are obtained by an explicit table of length \(\ell\).

Let
\[
u_f=e_f\deg f.
\]
Accept the trial only if
\[
\operatorname{rank}P=u_f.
\tag{7}
\]

All \(a_i\) lie in the known \(u_f\)-dimensional space \(V_f\), and all \(b_i\) lie in its \(u_f\)-dimensional perfect dual. Thus (7) certifies that both lists span their **entire** primary blocks. Select an invertible \(u_f\times u_f\) minor to obtain bases and an explicit duality matrix.

If Couveignes returns the full rational torsion, this rank test necessarily succeeds. A strict subgroup may also pass, but only when its projections already contain both full blocks—which is sufficient.

No unsuccessful trial is interpreted as evidence that a block is absent.

### 6.4 Coordinates are now genuine and paid

If \(a_1,\ldots,a_{u_f}\) is the selected basis and \(b_1,\ldots,b_{u_f}\) the selected dual list, then coordinates of any \(x\in V_f\) are obtained from
\[
\bigl(\log_\zeta e_\ell(x,b_j)\bigr)_j
\]
by multiplication by the inverse pairing matrix.

One can additionally verify the resulting class equality by Riemann–Roch. This avoids invoking Couveignes’s coordinate routine against an uncertified strict subgroup.

---

## 7. Compute the complete \(G\)-module \(W\)

Because deck transformations are rational over \(k_0\) and commute with \(F_0\), they preserve each \(V_f\) and its field \(K_f\).

For every generator \(g\in\Gamma\):

1. apply its supplied deck map to each primary-basis divisor;
2. compute the resulting coordinates by the certified pairing matrix;
3. verify the resulting class equalities.

This gives exact matrices \(R_f(g)\) on \(V_f\).

Compute \(W_f\) as the solution space of
\[
R_f(g)X=X\rho^*(g)
\qquad(g\in\Gamma),
\tag{8}
\]
where \(X\) is a \(u_f\times n\) matrix over \(\mathbf F_\ell\).

Each solution gives an explicit homomorphism \(S\to V_f\), with its \(n\) components constructed as divisor-class combinations and reduced as in (6).

Equation (1) proves that the direct sum of these solution spaces is all of \(W\). Require
\[
\sum_f\dim W_f=m.
\tag{9}
\]

The accepted basis is certified by:

- \(\ell\)-torsion of all components;
- the generator equivariance equations;
- independence in the certified primary coordinates;
- the known upper bound \(\dim W=m\).

For an entirely direct final check, enumerate the \(\ell^m-1\) nonzero combinations of the proposed homomorphisms and verify that each has at least one nonprincipal component. Since \(m\) is fixed, this is polynomial in \(\ell\). Degree-zero principality is an exact Riemann–Roch test.

Thus stopping at dimension \(m\) is justified. No parabolic target is used.

---

## 8. One common field, with a sharper bound

Let
\[
\mathcal S=\{f:W_f\ne0\},\qquad a_f=\deg f.
\]
Write \(m_f=\dim W_f\). The action of \(F_0\) on a nonzero \(W_f\) is \(f\)-primary, so
\[
a_f\mid m_f,\qquad a_f\le m_f.
\]
Therefore
\[
\sum_{f\in\mathcal S}a_f\le \sum_fm_f=m.
\tag{10}
\]

All selected component divisors and their required dual bases can first be embedded in
\[
K_H=\mathbf F_{q^{bH}},
\quad
H=\ell^\gamma
\operatorname{lcm}_{f\in\mathcal S}(\ell^{a_f}-1).
\]
Using (10),
\[
H\le \ell^\gamma\prod_{f\in\mathcal S}(\ell^{a_f}-1)
<2g\,\ell^{m+1}.
\tag{11}
\]

This is not an arbitrary least common multiple of all working fields. Only factors supporting the fixed-dimensional \(W\) enter.

### 8.1 Descend to the small target field

Set
\[
\gamma_m=\min\{j\ge0:\ell^j\ge m\},
\qquad
h_0=\ell^{\gamma_m}
\operatorname{lcm}_{f\in\mathcal S}(\ell^{a_f}-1).
\tag{12}
\]
Since \(F_0|_E=I_S\otimes B_0\), the nilpotence index relevant to \(E\) is at most \(m\). Hence
\[
E\subseteq J[\ell](K_0'),\qquad
K_0'=\mathbf F_{q^{bh_0}},
\]
and
\[
h_0\le \ell^{m+\lceil\log_\ell m\rceil}.
\tag{13}
\]

Rationality of the classes alone is not treated as an explicit descent algorithm. Construct their representatives as follows.

Run Couveignes Theorem 1 over \(K_0'\). For each returned class \(t_i\), form
\[
t_i'=p_{\mathcal S}(F_0)t_i,
\qquad
p_{\mathcal S}=\sum_{f\in\mathcal S}p_f.
\]
These are actual divisors over \(K_0'\).

Embed them into \(K_H\), compute their coordinates in
\[
\bigoplus_{f\in\mathcal S}V_f
\]
using the already certified dual bases, and solve for all \(nm\) component classes of the constructed \(W\)-basis.

Accept only if all those components are expressed. Verify the class equalities and reduce the resulting \(K_0'\)-divisors to degree \(g\).

A correct Couveignes run necessarily succeeds because \(E\subseteq J[\ell](K_0')\). A strict-subgroup run is accepted only if it already contains everything required.

This is a constructive descent with a finite success certificate, not a claim that rational classes automatically come with low-degree support coordinates.

---

## 9. If all individual support points must lie in one common field

The preceding output is already explicit arithmetic divisor data: effective closed divisors over one field, represented by ideals or equivalent normalization data. That is sufficient for the Riemann–Roch/Kummer-function steps of the supplied parabolic filter.

A stronger output, with individually rational support points, is also obtainable without an exponential support-field compositum.

### Prime-representative lemma

Let \(X/\mathbf F_Q\) be smooth of genus \(g\ge1\), with \(O\in X(\mathbf F_Q)\), and assume
\[
Q\ge64(g+1)^2.
\]
Put
\[
L=4g+4.
\]
For every degree-zero rational divisor \(D\), a uniformly chosen effective divisor in the complete linear system \(|D+LO|\) is a single closed point of degree \(L\) with probability at least
\[
\frac1{8L}.
\tag{14}
\]

#### Proof of the probability bound

Let \(A=J(\mathbf F_Q)\), \(h=|A|\), and assign to a closed point \(P\) of degree \(d\) the class
\[
a(P)=[P-dO]\in A.
\]
Use character orthogonality on \(A\). The unramified character \(L\)-functions, normalized to be trivial at \(O\), have degree \(2g-2\) for nontrivial characters and reciprocal roots of absolute value \(\sqrt Q\). This follows from the unramified Lang-cover construction and the Weil bounds; that cover is used only in the proof, never constructed by the algorithm.

For a fixed class \(a\), if \(\pi_L(a)\) counts degree-\(L\) closed points with class \(a(P)=a\), the logarithmic derivative coefficients and character orthogonality give
\[
L\pi_L(a)
\ge
\frac{Q^L}{h}-(8g+4)Q^{L/2}.
\]
The displayed constant also bounds the contribution of proper prime powers.

Now
\[
h\le(\sqrt Q+1)^{2g}\le2Q^g,
\]
and our choices of \(Q,L\) imply
\[
\pi_L(a)\ge \frac{Q^{L-g}}{4L}.
\]
Riemann–Roch gives exactly
\[
\frac{Q^{L+1-g}-1}{Q-1}\le2Q^{L-g}
\]
effective divisors in each degree-\(L\) rational divisor class. Their ratio proves (14). ∎

### Constructive use

Choose
\[
t=\min\{j\ge1:(q^{bh_0})^j\ge64(g+1)^2\},
\qquad Q=q^{bh_0t}.
\]
Then \(t=O(\log(g+1))\).

For each of the at most \(nm\) component divisors \(D\):

1. compute \(L(D+LO)\);
2. sample a nonzero section uniformly;
3. compute and factor the resulting effective divisor;
4. accept only if it is one closed point \(P\) of degree \(L\).

The returned representative is
\[
P-LO\sim D.
\]
All these degree-\(L\) points split over the **same** extension \(\mathbf F_{Q^L}\). Thus all component divisors can be output with individually rational support coordinates in
\[
K_{\mathrm{out}}
=\mathbf F_{q^{bh_0tL}}.
\tag{15}
\]

The numerical positive and negative divisor degrees are both \(L=4g+4\). The common field degree satisfies
\[
[K_{\mathrm{out}}:\mathbf F_q]
\le
b(4g+4)\,t\,
\ell^{m+\lceil\log_\ell m\rceil}.
\tag{16}
\]

This closes the support-field gap. It does not infer a common support field from the class field, and it does not split arbitrary degree-\(g\) effective divisors.

---

## 10. Genuine arithmetic Frobenius

Fix the convention that \(G\) acts on divisor classes by pushforward, equivalently inverse pullback. Compute the deck automorphism
\[
\alpha(g)=F_qgF_q^{-1}
\]
by applying \(q\)-power Frobenius to coefficients of the deck maps and comparing the resulting maps.

### 10.1 Arithmetic linearization on \(M^*\)

Solve
\[
A\rho^*(g)=\rho^*(\alpha(g))A
\qquad(g\in\Gamma).
\tag{17}
\]
This is linear algebra in \(n^2\) unknowns over \(\mathbf F_\ell\). For the stipulated natural-module normalizer action, a nonzero solution exists and is invertible. By absolute simplicity, its solution space is one-dimensional.

If the intended input does not guarantee preservation of the natural representation, (17) is an exact test of that requirement. Failure is a specification falsifier, not a reason to invent a Frobenius matrix on \(W\).

If the native coefficient module supplies a Frobenius \(T\) on \(M\), use \(A=T^{-t}\) on \(M^*\), with all conventions explicit.

### 10.2 Compute the matrix from divisors, not from the zeta polynomial

For each basis homomorphism \(\phi_j\), compute the \(n\) components of
\[
\psi_j=F_q\circ\phi_j\circ A^{-1}
\tag{18}
\]
by raising actual point coordinates or divisor coefficients to their \(q\)-th powers and taking the indicated divisor-class combinations.

Equation (17) proves that \(\psi_j\in W\). Since the constructed \(W\)-basis is complete, determine its coordinates by either certified block coordinates or exhaustive enumeration of \(\mathbf F_\ell^m\), with exact Riemann–Roch class comparisons. The latter costs only \(\ell^m\) per column.

This returns \(B_A\), and every column is certified by actual divisor-class equalities.

The fact that the auxiliary point \(O\) need not be \(\mathbf F_q\)-rational causes no problem: \(F_q(O)\) is computed and retained in those divisor equalities.

Under evaluation \(E=S\otimes W\),
\[
F_q|_E=A\otimes B_A.
\tag{19}
\]
Thus the algorithm has computed genuine arithmetic Frobenius, not merely a matrix with a plausible characteristic polynomial.

### 10.3 What is determined without an arithmetic coefficient convention?

Choose one normalized nonzero solution \(A_0\) of (17), and compute \(B_0\) from (18). Then all compatible choices are
\[
(A_c,B_c)=(cA_0,c^{-1}B_0),
\qquad c\in\mathbf F_\ell^\times,
\]
and all give the same actual matrix
\[
A_c\otimes B_c=F_q|_E.
\]

Therefore:

- **Determined by the cover:** \(\alpha\), \(E\), and actual \(F_q|_E\).
- **Determined after fixing the arithmetic coefficient module:** the unique corresponding \(F_W\).
- **Not determined by conjugation on \(G\) alone:** the coefficient-module scalar.

In the constant-\(G\), constant-\(M^*\) associated-system convention, take \(A=I\). In a Lefschetz application, an arbitrary normalization of (17) must not silently replace the original arithmetic coefficient representation.

---

## 11. Finite clocks, precision and failure handling

### 11.1 Couveignes’s internal extension remains polynomial

The excerpt’s construction explains why Theorem 1 does not require the full ambient splitting field.

For a call requesting \(\ell\)-torsion, put
\[
\iota=\max(48g,24d,720),
\]
and let \(\delta\) be the smallest integer with \(\ell^\delta>\iota\). Section 8 uses internal torsion exponent
\[
\ell^{\delta+1}\le \ell^2\iota
\]
and the extension degree
\[
A_{\mathrm{int}}
=(\ell-1)\ell^{\gamma+\delta}
<2g\,\iota\,\ell^3.
\tag{20}
\]
It handles the \(1\)- and \(Q\)-primary divisible groups over this extension, not the full torsion splitting field.

The exhaustive roots-of-unity discrete logarithms have size at most \(\ell^2\iota\), hence polynomial cost. The bounded-index correction has index at most \(\iota\), not the order of a large Jacobian group.

For every actual working field \(R\), the needed \(\ell\)-adic exponent is bounded by
\[
v_\ell(\#J(R))
\le
2g\log_\ell(\sqrt{|R|}+1).
\]
Taking this bound plus the internal torsion exponent’s valuation gives an explicit finite precision for the finite \(\ell\)-adic polynomial calculations. The corresponding bit precision is polynomial in \(g\) and \(\log |R|\).

Exact group orders are obtained from the derived zeta polynomials. Removing their \(\ell\)-parts uses repeated division, not integer factorization of the full group order.

### 11.2 Bounded repetitions

There are at most \(2g\) primary factors and one final descent task.

Let \(T_C\) denote the polynomial time bound of the actual Theorem 1 implementation. If its bound is expected time, cap a call at \(4T_C\). Since correctness has probability at least \(1/2\), the capped call still has probability at least \(1/4\) of producing a correct answer. If a worst-case polynomial clock is available, the original \(1/2\) success bound can be used.

For each primary or descent task, use at most
\[
R_C=
\left\lceil
\frac{\log(4(2g+1)/\eta)}{\log(4/3)}
\right\rceil
\tag{21}
\]
independent capped calls. An exhausted task returns `FAIL`.

For fully split support coordinates, use at most
\[
R_{\mathrm{move}}
=
\left\lceil
8L\log\!\left(\frac{4\max(1,nm)}{\eta}\right)
\right\rceil
\tag{22}
\]
section samples per component. The prime-representative lemma bounds the total failure probability by the allocated budget.

Finite-field factorization, field embeddings and other verified Las Vegas primitives are likewise capped and retried with a global error allocation. Factorizations, irreducibility, map equalities, torsion, pairing ranks and final divisor equalities are verified exactly.

The supplied excerpts state polynomial subroutine bounds but do not specify a numerical bit-operation exponent. Equations (20)–(22) give the extension, precision and repetition clocks; the bit clock uses the stated polynomial bounds of those arithmetic primitives rather than an invented exponent.

### 11.3 Charged arithmetic and output

The accounting includes:

- reading the plane model, cover map, deck maps and supplied zeta numerator;
- normalization and local-place data;
- every constant-field construction and embedding;
- exact derived zeta polynomials and Jacobian orders;
- divisor arithmetic with reduction after large scalar multiplication;
- pairing functions and roots-of-unity tables;
- numerical Riemann–Roch divisor degrees;
- all output field coefficients and support coordinates.

With rational closed-divisor output, component representatives have degree \(g\) as in (6). With individually rational supports, they have positive and negative degree \(4g+4\), in the common field (15).

There is no quantum state preparation, quantum factoring or hidden large-group discrete-log oracle.

---

## 12. What this closes, and what it does not

### Closed supplied-zeta obligation

Subject to the stated geometric dimension and arithmetic coefficient convention, the construction supplies:

- the complete \(W\), not an uncertified subgroup;
- actual torsion-divisor coordinates;
- one charged common field, including an optional fully split support-coordinate version;
- genuine arithmetic Frobenius computed on those coordinates;
- finite clocks and explicit failure handling.

The exponential full-\(J[\ell]\) splitting field is unnecessary.

### Native plane-model zeta computation remains a separate charge

The supplied theorem assumes the zeta numerator. This proof does not compute it from the native plane equation.

The native cost therefore has the honest form
\[
T_{\mathrm{native}}
=
T_{\mathrm{zeta}}(C/\mathbf F_q)
+
\operatorname{poly}_{n,r}
\bigl(\ell,P,\text{presented size},\log(1/\eta)\bigr),
\]
together with any required native determination of the coefficient-module arithmetic linearization.

To remove the supplied-zeta qualifier, one must provide an exact native zeta algorithm with the required uniform dependence on numerical \(P\), plane-model degree and bit size. A bound such as \(P^{O(d)}\), or enumeration over \(\mathbf F_{q^{O(g)}}\), would not meet the target when \(d,g\) grow with \(\ell\).

This is an uncharged obligation in the supplied material, **not a claim that native classical zeta computation is hard or unknown**.

Finally, none of the construction proves uniform number-field lifting heights, pays arithmetic reconstruction, or rehabilitates the false descent theorem. It removes the finite-field torsion-coordinate blocker in the supplied-zeta setting; the parabolic filter and the subsequent arithmetic-height obligations remain distinct.