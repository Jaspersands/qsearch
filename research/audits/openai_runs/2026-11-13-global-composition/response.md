## Verdict

**The remaining global interfaces can be closed, conditional on a uniform native complete-image routine at every finite prime dividing \(2\operatorname{disc}(f)\).** The proposed torsion repair and the \(T\)-unit valuation-kernel construction are valid. No odd-degree-field, Galois, totally real, good-dyadic, or small-odd-prime promise is needed.

This is a **conditional composition theorem**, not an admission of the supplied local candidate. That candidate is explicitly still under audit and states a fixed-\(2\) contract; it does not establish the all-prime premise below.

I use the supplied Biasse–Song and Poteaux–Weimann results at their stated scope. In particular, the quantum primitive is the **complete algorithm of Biasse–Song Theorem 1**, including exact compact recovery—not Theorem 5 treated as a free HSP oracle.

---

# 1. Precise conditional theorem

Let
\[
f\in\mathbf Z[x],\qquad \deg f=n=2g+1,
\]
be monic and squarefree, and let \(\ell\) be its explicit input bit length. Set
\[
C:y^2=f(x),\qquad J=\operatorname{Jac}(C).
\]

Assume:

1. **GRH class-generator premise.** For every number-field factor \(K\) of
   \[
   L=\mathbf Q[x]/(f),
   \]
   the GRH generating-prime assertion quoted in Biasse–Song §8.2 applies to \(\operatorname{Cl}(\mathcal O_K)\).

2. **Local premise, still unproved here.** There is one uniform native routine which, on input \((f,p,\epsilon)\), for a prime \(p\mid 2\operatorname{disc}(f)\):
   - runs in bounded time
     \[
     \operatorname{poly}(\ell,n,\log p,\log(1/\epsilon));
     \]
   - returns the **complete** image
     \[
     \delta_p\bigl(J(\mathbf Q_p)/2J(\mathbf Q_p)\bigr)
       \subset L_p^\times/L_p^{\times2};
     \]
   - supplies explicit finite coordinate data sufficient to interpret that subspace and compare it with elements of the native algebra \(L_p=\mathbf Q_p[x]/(f)\);
   - has total failure/abort probability at most \(\epsilon\).

   “Explicit coordinates” must include actual maps or finite representatives identifying the coordinates with the native algebra. Bare binary vectors in an unnamed coordinate space do not satisfy this premise.

Then, using the quoted arithmetic theorems, there is a bounded-error quantum algorithm returning
\[
\dim_{\mathbf F_2}\operatorname{Sel}^{(2)}(J/\mathbf Q)
\]
with error at most \(\eta\), in
\[
\operatorname{poly}(\ell,g,\log(1/\eta))
\]
bit time.

If the stipulated local routine is classical, as intended in the supplied candidate, the only quantum ingredients needed in this composition are integer factorization and complete compact \(T\)-unit computation.

The output is the Selmer **dimension**, not Mordell–Weil rank, rational points, or covering curves.

---

# 2. Native arithmetic, maximal orders, and the GRH factor base

Write
\[
f=\prod_{i=1}^{t} f_i,\qquad
K_i=\mathbf Q[x]/(f_i),\qquad d_i=[K_i:\mathbf Q],
\]
so \(\sum_i d_i=n\).

Let
\[
D_f=\operatorname{disc}(f),\qquad
h=\left\lceil\log_2(2|D_f|)\right\rceil.
\]
For maximum coefficient bit length \(B\), the resultant determinant gives
\[
h=O\!\left(n(B+\log n)\right).
\]

### 2.1 Factoring and discriminants

Factoring \(f\) over \(\mathbf Q\) is a classical polynomial-bit operation. Its monic integral factors have polynomial-size encodings.

Quantum-factor \(|D_f|\), handling \(2\) separately if necessary. A complete factorization can be checked by primality tests and multiplication. The identity
\[
D_f=
\prod_i\operatorname{disc}(f_i)
\prod_{i<j}\operatorname{Res}(f_i,f_j)^2
\]
shows that every prime dividing a factor discriminant already divides \(D_f\). Thus one factorization of \(D_f\) suffices to obtain the needed factorizations of the factor discriminants.

For each \(i\),
\[
\operatorname{disc}(f_i)
=[\mathcal O_{K_i}:\mathbf Z[\theta_i]]^2\Delta_{K_i},
\]
and consequently
\[
\log|\Delta_{K_i}|\le h,\qquad
\log[\mathcal O_{K_i}:\mathbf Z[\theta_i]]\le h/2.
\]

### 2.2 Maximal orders

The supplied Poteaux–Weimann Theorem 1 applies to each irreducible \(f_i\), now with the required discriminant factorization.

Its displayed bound is a **word-operation bound**, not a license to omit native coefficient access or bit sizes. The composition additionally charges:

- reading and factoring the native polynomial;
- computing discriminants and resultants;
- arithmetic on the polynomial-size coefficient, index, and discriminant data;
- forming multiplication tables and basis-conversion matrices.

The index and discriminant parameters in the displayed bound are polynomially bounded by \(h\). The triangular basis has polynomial-size exact data. Charging polynomial-bit arithmetic for these words therefore gives the polynomial-bit consequence needed here; no sharper bit exponent is claimed.

An LLL-reduced integral basis, certified embedding approximations, and conversion matrices can then be prepared in polynomial bit time. These are part of the input preparation for Biasse–Song §8.1, not free advice.

### 2.3 The bad-prime set

Put
\[
P_0=\{p:p\mid 2D_f\},\qquad s=|P_0|\le h+1,
\]
and let \(S_i\) contain **all** prime ideals of \(K_i\) above \(P_0\).

Prime decomposition must use the maximal order. Factoring \(f_i\bmod p\) alone is not valid when \(p\) divides the power-basis index.

Prime decomposition in the computed maximal order is polynomial in the degree, coefficient-data size, and \(\log p\), using finite-algebra and finite-field algorithms. Randomized finite-field factorizations can be verified and truncated with logarithmic retry budgets.

### 2.4 GRH generating primes

For \(K_i\ne\mathbf Q\), enumerate the prime ideals of norm at most a computable integer cutoff
\[
M_i=O\!\left((\log|\Delta_{K_i}|)^2\right)
\]
which is at least the quoted \(48(\log|\Delta_{K_i}|)^2\).

Using a conservative integer upper bound avoids an unnecessary exact comparison with a transcendental logarithmic cutoff. Enumerating a slightly larger set preserves generation.

This is genuinely polynomial enumeration:

- every underlying rational prime is at most \(M_i\);
- \(M_i=O(h^2)\);
- there are at most \(d_i\) prime ideals above a rational prime;
- ideal norms and HNF ideal representations have polynomial bit size.

Let this set be \(R_i\), and set
\[
T_i=S_i\cup R_i.
\]
Then \(T_i\) generates the ordinary ideal class group under the stated GRH premise.

For \(K_i=\mathbf Q\), use
\[
\operatorname{Cl}(\mathbf Z)=0
\]
directly. Do not apply the logarithmic discriminant formula to \(\Delta_{\mathbf Q}=1\).

With
\[
q=\sum_i |T_i|,
\]
one has the conservative bound
\[
q=O\!\left(n(s+h^2)\right).
\]
Also
\[
\max_{\mathfrak p\in T_i}\log N\mathfrak p=O(nh).
\]

Thus every parameter in the quoted complete \(T\)-unit theorem is polynomial in the native input size.

No explicit class-group invariant factors or principal-ideal generators are needed in the subsequent construction.

---

# 3. Complete compact units and the torsion repair

For each non-rational field, invoke the complete Biasse–Song \(T_i\)-unit algorithm.

Writing \(r_{1,i},r_{2,i}\) for the signature, it must supply lifts of a basis of
\[
U_{T_i}/\mu(K_i),
\]
whose rank is
\[
r_{1,i}+r_{2,i}-1+|T_i|.
\]

This means the complete free quotient, not merely independent valid units.

The supplied source distinction matters:

- Theorem 5 produces controlled approximate HSP lattice data.
- The complete Theorem 1 construction and §8.1/Proposition 7 perform the additional recovery.
- The logarithmic free basis does not itself supply the torsion squareclass.

Use compact base \(l=2\). Fractional-unit corrections must also remain compact: a huge rational product
\[
\prod p^{e_p}
\]
is stored through the small primes and binary exponents, not expanded.

## 3.1 The proposed torsion extraction is valid

Start with
\[
\zeta_2=-1.
\]
Given a primitive \(2^a\)-th root \(\zeta_{2^a}\in K\), factor
\[
X^2-\zeta_{2^a}
\]
over \(K\).

- If there is a root, either root is primitive of order \(2^{a+1}\).
- If there is no root, \(K\) contains no primitive \(2^{a+1}\)-th root: if it contained one, its \(2\)-primary roots-of-unity subgroup would make the current \(\zeta_{2^a}\) a square.

Since
\[
[\mathbf Q(\zeta_{2^a}):\mathbf Q]=2^{a-1}\le [K:\mathbf Q],
\]
there are only \(O(\log [K:\mathbf Q])\) tests.

### Polynomial-size representatives

Height zero alone needs to be connected to the chosen basis. That connection is available.

Let \(\omega_1,\dots,\omega_d\) be a controlled integral basis. For a root of unity \(\zeta\), write
\[
\zeta=\sum_j c_j\omega_j.
\]
The trace equations are
\[
\sum_j \operatorname{Tr}(\omega_i\omega_j)c_j
=\operatorname{Tr}(\zeta\omega_i).
\]
All conjugates of \(\zeta\) have absolute value \(1\). Therefore the right-hand sides and trace-matrix entries have polynomial bit length. Its determinant is the nonzero field discriminant. Cramer bounds give polynomial-bit coordinates \(c_j\).

Consequently the successive quadratic factorizations remain polynomial-bit computations over an explicitly presented number field. They do not incur an iterated height blow-up.

### Why one such root is enough

Write
\[
|\mu(K)|=2^a m,\qquad m\ \text{odd}.
\]
A primitive \(2^a\)-th root generates
\[
\mu(K)/\mu(K)^2\cong\mathbf F_2.
\]
The odd-order subgroup contributes nothing modulo squares.

Moreover, a root of unity which is a square in \(K^\times\) is already a square in \(\mu(K)\): if \(x^2\) has finite order, then \(x\) has finite order.

Thus the final root supplies exactly the missing torsion bit. No full roots-of-unity enumeration or discrete logarithm is required.

**Append this bit separately in every field factor.** In a field such as \(\mathbf Q(i)\), appending \(-1\) would fail because \(-1\) is already a square.

## 3.2 Correct initial dimensions

Put
\[
\rho_i=r_{1,i}+r_{2,i}.
\]
The resulting basis of \(U_{T_i}/U_{T_i}^2\) has dimension
\[
m_i=\rho_i+|T_i|.
\]
Hence
\[
m=\sum_i m_i=\sum_i\rho_i+q\le n+q.
\]

A generator belonging to one field factor is embedded in \(L^\times\) with value \(1\), not \(0\), in all other factors.

---

# 4. The valuation kernel gives all virtual squareclasses

Define
\[
K_i(S_i,2)=
\left\{\alpha\in K_i^\times/K_i^{\times2}:
v_{\mathfrak q}(\alpha)\equiv0\pmod2
\ \text{for }\mathfrak q\notin S_i
\right\}.
\]

Consider
\[
V_i:U_{T_i}/U_{T_i}^2
\longrightarrow
\mathbf F_2^{T_i\setminus S_i}
\]
given by prime-ideal valuation parities.

There are two separate assertions to prove.

## 4.1 Injection into field squareclasses

If \(u\in U_{T_i}\) and \(u=x^2\) for \(x\in K_i^\times\), then outside \(T_i\),
\[
0=v_{\mathfrak q}(u)=2v_{\mathfrak q}(x).
\]
Thus \(x\in U_{T_i}\). Therefore
\[
U_{T_i}/U_{T_i}^2\hookrightarrow K_i^\times/K_i^{\times2}.
\]

No squareclass relations are lost by using the \(T_i\)-unit quotient.

## 4.2 Surjectivity onto \(K_i(S_i,2)\)

Let \([\alpha]\in K_i(S_i,2)\), and form
\[
\mathfrak a=
\prod_{\mathfrak q\notin T_i}
\mathfrak q^{v_{\mathfrak q}(\alpha)/2}.
\]
Because \(T_i\) generates \(\operatorname{Cl}(K_i)\), there is a fractional \(T_i\)-supported ideal \(\mathfrak b\) with
\[
[\mathfrak b]=[\mathfrak a].
\]
Choose \(x\in K_i^\times\) such that
\[
(x)=\mathfrak a\mathfrak b^{-1}.
\]
Then
\[
u=\alpha/x^2
\]
has zero valuation outside \(T_i\), so \(u\in U_{T_i}\). At every prime in \(T_i\setminus S_i\), its valuation remains even.

Thus
\[
\boxed{\ker V_i\cong K_i(S_i,2).}
\]

The ideal and generator in this proof are existential completeness witnesses. The algorithm does **not** have to construct them: the complete \(T_i\)-unit basis and binary kernel already produce the squareclasses.

## 4.3 Dimension check

There is an exact sequence
\[
0\longrightarrow
\mathcal O_{K_i,S_i}^{\times}/
\mathcal O_{K_i,S_i}^{\times2}
\longrightarrow K_i(S_i,2)
\longrightarrow
\operatorname{Cl}(\mathcal O_{K_i,S_i})[2]
\longrightarrow0.
\]
Hence
\[
\dim K_i(S_i,2)
=
\rho_i+|S_i|
+\dim\operatorname{Cl}(\mathcal O_{K_i,S_i})[2].
\]

Equivalently,
\[
\operatorname{rank}V_i
=
|T_i\setminus S_i|
-\dim\operatorname{Cl}(\mathcal O_{K_i,S_i})[2].
\]

This explicitly shows why replacing the kernel by genuine \(S_i\)-units would be wrong: it could omit the \(S_i\)-class-group \(2\)-torsion contribution.

These dimension identities are consistency checks, not substitutes for the complete-unit success guarantee.

---

# 5. The rational norm condition, with all rows paid

Let
\[
L(S,2)=\prod_i K_i(S_i,2).
\]

Initially build norm rows for every rational prime lying below some \(T_i\), together with one rational-sign row. For an original compact \(T_i\)-unit \(u\),
\[
v_p(N_{K_i/\mathbf Q}u)
=
\sum_{\mathfrak p\mid p}
f_{\mathfrak p}\,v_{\mathfrak p}(u).
\]
The weights are residue degrees, and the valuations are normalized prime-ideal valuations.

The sign of the norm is the product of the signs at the real embeddings; complex pairs contribute positively.

These rows can be computed without expanding units:

- use the exact original valuations supplied by the source, or sum compact-atom valuations with binary exponents;
- compute norm signs from small atoms and exponent parities.

After imposing the \(T_i\setminus S_i\) valuation kernels, all norm rows outside \(P_0\) vanish automatically. Retaining them is harmless and useful for bookkeeping.

The resulting space is
\[
H_S=
\ker\!\left(
N:L(S,2)\longrightarrow
\mathbf Q^\times/\mathbf Q^{\times2}
\right).
\]

There is also an exact rank check. Its norm image is
\[
\mathbf Q(P_0,2)=\langle -1,\ p:p\in P_0\rangle.
\]
Indeed, diagonal rational classes lie in \(L(S,2)\), and
\[
N_{L/\mathbf Q}(a)=a^n\equiv a\pmod{\mathbf Q^{\times2}}
\]
because \(n\) is odd. Therefore
\[
\boxed{\dim H_S=\dim L(S,2)-(s+1).}
\]

This is the odd-degree norm-kernel model from Stoll, not a quotient by diagonal rational squareclasses.

### Important bookkeeping distinction

A parity representative of a compact unit can have additional prime support with even valuations. It need not be a \(T_i\)-unit as an actual element.

Therefore:

- original full-unit valuations establish support and supply the global valuation/norm bookkeeping;
- parity representatives supply squareclass evaluations;
- one must not replace exact original valuations by the exact valuations of a small representative and then claim their supports agree.

Their valuation **parities** agree; their valuations need not.

---

# 6. Compact localization and precision

## 6.1 Never expand a unit

Represent each source output as
\[
u=\prod_{a=1}^{A_u}\gamma_a^{e_a},
\]
where the atoms \(\gamma_a\) have polynomial-size exact encodings, the number of atoms is polynomial, and the exponents have polynomial bit length.

Modulo squares,
\[
[u]=\sum_a(e_a\bmod2)[\gamma_a].
\]

For an integral base-\(2\) compact representation, only its initial atom survives. Fractional corrections must still be included; their odd exponent parities can matter.

Subsequent global basis changes are stored as binary matrices. There is no need to multiply out even the new global squareclass representatives.

## 6.2 Rational square clearing and a valuation bound

For an atom \(\gamma\in K_i^\times\), choose a positive integer \(d\) clearing its integral-basis coordinate denominators. Then
\[
\alpha=d^2\gamma\in\mathcal O_{K_i}
\]
is integral and represents the same squareclass at every place.

Its norm is a nonzero integer computable by a polynomial-size determinant. Define
\[
V_\alpha=\left\lceil\log_2|N_{K_i/\mathbf Q}(\alpha)|\right\rceil+1.
\]
Then, at every finite prime ideal,
\[
0\le v_{\mathfrak p}(\alpha)\le V_\alpha.
\]
This follows from
\[
|N(\alpha)|=\prod_{\mathfrak p}
(N\mathfrak p)^{v_{\mathfrak p}(\alpha)}.
\]

No factorization of the atom norm is required merely to obtain this bound.

All these norms and bounds have polynomial bit length. In particular, the point-source valuation cap from a local geometric construction is **not** reused as a bound for arbitrary global units.

## 6.3 Coefficient, integral-basis, and CRT conversions

Let
\[
\mathcal O_L=\prod_i\mathcal O_{K_i},\qquad
R=\mathbf Z[x]/(f).
\]
Then
\[
D_f=[\mathcal O_L:R]^2\prod_i\Delta_{K_i}.
\]
Thus the monogenic-to-maximal-order index and the native CRT denominator losses are controlled by \(D_f\). At \(p\), their relevant denominator exponents are bounded by \(O(v_p(D_f))\).

This pays the transition between:

- native polynomial coordinates;
- the product of global integral bases;
- local integral-component coordinates.

The identification is induced by the same native element \(\theta=x\bmod f\). It is not an uncharged search for an isomorphism between abstract local fields.

## 6.4 Squareclass frames are polynomial-size

The global maximal orders also allow a direct construction of local arithmetic frames. Decompose \(\mathcal O_L/p\), lift its idempotents, and obtain the complete local integral components modulo the requested \(p\)-adic precision. Finite-algebra decomposition, idempotent lifting, and integral component bases are polynomial operations.

Uniformizers can be obtained from the prime-ideal/reduction data, with verified randomized selection if desired. Sampling in the maximal ideal and testing membership outside its square succeeds with probability at least \(1/2\).

For a component \(E/\mathbf Q_p\):

- **Odd \(p\):** valuation parity and the quadratic character of the residue unit give two coordinates. Euler powering uses \(O([k_E:\mathbf F_p]\log p)\)-bit exponents; it does not enumerate the residue field or require a discrete logarithm.
- **\(p=2\):** write \(e=v_E(2)\), \(f_E=[k_E:\mathbf F_2]\), and use
  \[
  U_{2e+1}\subset E^{\times2}.
  \]
  The \(2ef_E=2[E:\mathbf Q_2]\) generators
  \[
  1+\pi^j\beta_\ell,
  \qquad 1\le j\le2e,\quad 1\le\ell\le f_E,
  \]
  give a triangular presentation of \(U_1/U_{2e+1}\). Collect the square of each generator into higher filtration levels. The relation matrix has diagonal \(2\), determinant \(2^{2ef_E}\), and presents the group exactly because the filtration gives that same group order.

  Quotient this relation lattice by squares using integer or binary linear algebra. No saturation and no unit-group enumeration is involved.

For an arbitrary dyadic unit, raising it to \(2^{f_E}-1\) removes its residue component and preserves its squareclass. That exponent has only \(f_E\) bits.

Thus the local ambient squareclass dimensions are
\[
\dim L_p^\times/L_p^{\times2}
=
\begin{cases}
2c_p,&p\ne2,\\
n+2c_p,&p=2,
\end{cases}
\]
where \(c_p\) is the number of local field factors. Both are \(O(n)\).

These constructions concern **coordinates**, not generation of the local Kummer image. The latter remains the explicit conditional premise.

## 6.5 Precision and common frames

Let \(V_{\max}\) be the maximum atom bound used at a given prime. After normalizing an atom of local valuation \(m\), a conservative integral-matrix inversion bound loses at most a constant multiple of
\[
f_E m\le nV_{\max}
\]
rational \(p\)-adic digits.

The remaining unit precision is small:

- residue precision at odd \(p\);
- precision through \(\pi^{2e+1}\) at \(2\), covered by a constant number of rational \(2\)-adic digits after normalization.

Record the fixed conversion losses in a guard \(\Gamma_p\). The native-to-integral/CRT contribution is polynomially bounded by the discriminant valuation; any returned coordinate presentation must likewise be explicitly interpretable, not hide arbitrary conditioning.

For example, after those fixed guards are recorded, a conservative working precision of the form
\[
Q_p\ge
2\Gamma_p+2nV_{\max}+4n+10
\]
is sufficient for the external atomic localization, enlarged to the precision needed by the local-image routine itself. The bit cost is \(Q_p\log p\), hence polynomial.

Fix **one frame per prime**. Either:

1. evaluate every global atom in the routine’s explicit frame; or
2. translate the routine’s frame generators into the independently computed frame.

Refinement preserves the chosen component selectors and coordinate definitions. Mixing independently chosen nonsquares, uniformizers, residue bases, or dyadic relation bases without translation is invalid.

At real embeddings, atom signs are computable with polynomial precision: their exact heights and nonzero norms give polynomial separation bounds. One never attempts to determine the sign of an expanded exponentially large or small unit numerically.

---

# 7. The real image is complete with only \(O(g)\) generators

Let the real roots of \(f\) be
\[
r_1<r_2<\cdots<r_R,\qquad R=2k+1.
\]
Then
\[
L_\mathbf R^\times/L_\mathbf R^{\times2}
\cong\mathbf F_2^R.
\]

Because \(f\) is monic of odd degree, its bounded positive intervals are
\[
(r_{2j-1},r_{2j}),\qquad 1\le j\le k,
\]
and it is also positive on \((r_R,\infty)\).

Choose a real point with \(x\)-coordinate in each bounded positive interval, and a reference point in the unbounded interval. The corresponding Kummer sign vectors are
\[
w_j=e_{2j}+e_{2j+1}+\cdots+e_R.
\]
They are independent. Equivalently, their span has basis
\[
e_2+e_3,\ e_4+e_5,\ \ldots,\ e_{R-1}+e_R.
\]

These vectors give the **whole** real image:

- the rational point at infinity ensures that real Jacobian classes can be represented by real degree-zero divisors;
- move their supports away from the branch divisor;
- a conjugate pair of nonreal points contributes
  \[
  (x-r_a)(\bar x-r_a)=|x-r_a|^2>0
  \]
  at every real root;
- every real point contributes one of the displayed interval sign vectors or zero.

Therefore
\[
\boxed{\dim\delta_\infty(J(\mathbf R)/2J(\mathbf R))=k=(R-1)/2.}
\]

Real-root isolation, interval selection, and these sign vectors have polynomial bit complexity. There is no enumeration of \(2^g\) connected components.

---

# 8. Why places outside \(P_0\) require no further calls

The supplied Stoll Lemma 4.1 and Proposition 4.2 identify the desired Selmer group with the norm-kernel classes satisfying all local Kummer conditions.

The chosen set
\[
\{\infty\}\cup P_0
\]
is conservative: Stoll Corollary 4.7 permits the smaller set using \(p^2\mid D_f\).

For completeness, the automatic condition outside the chosen set has a direct good-prime justification. If \(p\notin P_0\), then:

- \(p\ne2\);
- \(f\bmod p\) is squarefree;
- \(J\) has good reduction;
- \(L_p\) is an unramified étale algebra.

The local Kummer image is the unramified norm-square subgroup. In the squareclass model this is exactly the subgroup with even valuation in every field component and square rational norm.

One can check equality without enumerating \(J(\mathbf F_p)\): the formal reduction kernel is uniquely \(2\)-divisible, so
\[
J(\mathbf Q_p)/2J(\mathbf Q_p)
\cong J(\mathbf F_p)/2J(\mathbf F_p).
\]
Its dimension is \(c_p-1\), as is the unramified norm-kernel subgroup.

Thus the global valuation conditions and norm rows already enforce every local condition outside \(P_0\). All primes inside \(P_0\), including discriminant-valuation-one primes and every small bad prime, are handled by the conditional routine.

No good-reduction claim is made at an arbitrary bad prime.

---

# 9. Final linear algebra, operation counts, and output size

Use the original \(m\)-dimensional \(T\)-unit squareclass basis.

Let:

- \(V\) be the prime-ideal valuation matrix for all \(T_i\setminus S_i\);
- \(N\) be the rational norm matrix, including sign;
- \(R_p\) be the localization matrix in the common frame at \(p\);
- \(B_p\) be the complete local image matrix;
- \(A_p\) be a matrix with
  \[
  \ker A_p=\operatorname{im}B_p.
  \]

Construct the analogous real matrices. Then
\[
\boxed{
\dim\operatorname{Sel}^{(2)}(J/\mathbf Q)
=
m-\operatorname{rank}
\begin{pmatrix}
V\\
N\\
A_\infty R_\infty\\
(A_pR_p)_{p\in P_0}
\end{pmatrix}.
}
\]

This is exact on the joint success event.

A conservative resource ledger is:

| Item | Count/size |
|---|---:|
| Number fields | at most \(n\) |
| Rational bad primes | \(s=O(h)\) |
| Prime ideals in all \(T_i\) | \(q=O(n(s+h^2))\) |
| Initial squareclass columns | \(m\le n+q\) |
| Complete unit calls | at most \(n\) |
| Torsion quadratic tests | \(O(n\log n)\) |
| Conditional local-image calls | \(s\) |
| Local ambient rows | \(O(ns+n)\) |
| Compact atoms and their encodings | polynomial, by the unit theorem |
| Atomic local evaluations | polynomially many; no expanded products |

The binary matrix calculation can be performed in
\[
O((m+r)^3)
\]
bit operations for total row count \(r\), or faster with standard alternatives. All relevant dimensions are polynomial.

The returned integer is at most \(m\), so its own encoding needs only \(O(\log(m+1))\) bits.

No ideal-class group, residue field, Jacobian group, or compact exponent range is enumerated.

---

# 10. Quantum interfaces and failure amplification

## 10.1 What is and is not coherent

The algorithm is a classical controller invoking quantum arithmetic subroutines.

- The native coefficients, orders, ideals, and conversion tables are explicit classical data.
- Integer factoring and the Biasse–Song algorithm use quantum circuits.
- Their classical outputs are measured before the subsequent linear algebra and localization.
- The local Kummer routine is not required as a coherent oracle.
- There is no QRAM assumption and no quantum state of an expanded fundamental unit.

Polynomial-size input descriptions must be read and loaded into reversible arithmetic at polynomial cost.

For Biasse–Song, the complete Theorem 1 runtime is charged. Counting only the oracle calls in Theorem 5 would be insufficient. Its conditions—including the quoted \(r_{\rm HSP}\le\lambda/36\), the approximation parameter, and exact recovery—belong to that full construction.

The HSP approximation parameter is also distinct from the user’s failure parameter \(\eta\). It need not be inverse-polynomial numerically; the relevant requirement is polynomial bit precision, as required by the complete algorithm.

If only Theorem 5 were available, without the efficient HSP construction and complete recovery reduction, that would be a genuine missing global interface. The quoted Theorem 1 is what supplies it here.

## 10.2 Completeness is a probabilistic event

Valid returned units do not certify that their subgroup is complete.

For each field, budget failure for the event that the source returns a complete free quotient and correct exact compact lifts. Carry the HSP generation failure through the source’s deterministic recovery; include any additional randomized arithmetic failures separately.

Do not multiply \(n\) unamplified \(2/3\)-success probabilities.

A safe implementation is:

1. Give all field computations a shared small constant failure budget, with individual HSP parameters \(O(1/n)\).
2. Give the \(s\) local calls a shared small constant budget, with individual errors \(O(1/s)\).
3. Give all other randomized arithmetic a shared constant budget.
4. Use verified Las Vegas routines with constant-factor time caps and logarithmically many fresh retries—not a cap proportional to \(1/\eta\).

A union bound then gives one complete run a fixed success probability greater than \(1/2\), say at least \(3/4\).

Repeat complete runs independently \(O(\log(1/\eta))\) times and majority-vote **only the final integer dimension**. Do not majority-vote arbitrary unit bases or coordinate frames.

Alternatively, the explicit logarithmic failure dependence can support a direct global error allocation. Either method meets the required polynomial dependence on \(\log(1/\eta)\).

---

# 11. Classical comparator and admission boundary

The matched classical comparator is the **same optimized Stoll two-descent**, using:

- classical integer factorization;
- the same maximal-order and local arithmetic;
- complete classical class-/\(S\)-unit methods with compact output;
- applicable \(2\)-primary, repeated-field, and early-termination optimizations.

Applicable rigorous subexponential methods should be retained with their actual degree/discriminant hypotheses. Heuristic index-calculus or factoring estimates must remain labeled heuristic. The supplied packet does not establish one uniform fastest classical bit bound for arbitrary growing-degree fields, so a universal subexponential comparator should not be invented.

In schematic form the matched classical cost is
\[
T_{\rm factor}^{\rm cl}
+\sum_i T_{T_i\text{-unit}}^{\rm cl}
+\operatorname{poly}(\ell,n),
\]
taking the best applicable justified classical methods, and using the same local premise if it is classical.

This comparison does **not** establish a speedup or a lower bound. The dimension-only problem might admit a classical algorithm avoiding complete unit computation. Hard intermediate tasks in this particular reduction do not prove hardness of its output.

## Remaining proof obligation

The substantive open algorithmic premise is the **uniform all-prime native complete-image routine**. It must cover arbitrary bad reduction, growing genus, large residue characteristic, interpretable finite coordinates, and bounded precision/retry costs.

The fixed-\(2\) candidate and the earlier promised-family controls do not discharge that obligation.

## Decisive failure modes

The conditional theorem would be misapplied if any of the following occurred:

- the local routine supplied only valid sampled labels rather than the complete image;
- its cost depended polynomially on \(p\) rather than \(\log p\);
- the unit primitive supplied only a finite-index subgroup without the stated completeness guarantee;
- torsion were omitted or replaced by diagonal \(-1\);
- the \(T\setminus S\) kernel were replaced by genuine \(S\)-units;
- original valuation bookkeeping were confused with the support of parity representatives;
- local columns used inconsistent frames or unpaid conversion precision;
- compact products, residue fields, or real components were expanded exponentially.

A future polynomial classical algorithm for the same output would undermine an advantage claim, **not** this conditional quantum upper bound.

**Bottom line:** the torsion, virtual-unit, norm, infinity, localization, and resource interfaces admit direct polynomial-bit proofs. With the stated all-prime local premise and the quoted complete quantum arithmetic theorem, the general GRH conditional Selmer-dimension composition follows. It is not yet an unconditional general Selmer algorithm, and no novelty, hardness, or quantum advantage follows from this audit.