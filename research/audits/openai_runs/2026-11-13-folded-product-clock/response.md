## Verdict

**The finite-bit sampler can be made rigorous under the two admitted structural hypotheses.** The covariance signs and prefix Pfaffian formula are correct. Rational circle points avoid a field-degree blowup, and explicit common-denominator bounds give a polynomial clock even at exponentially small prefixes.

The cheapest genuine clock counterexample is to **literal exact sampling with bounded fair bits**: \(p=1/3\) cannot be sampled exactly using a fixed maximum number of fair bits, since every resulting probability is dyadic. This also rules out exact fixed-clock sampling of general algebraic Gaussian probabilities. It does **not** refute the requested \(\epsilon\)-TV task; dyadic approximation repairs it.

Below is a constructive bit-complexity proof, not an inference from finite controls or an ACCEPT label.

## 1. Normalization and the fragment interface

Accept the stated folded bijection. Within a fragment, all physical words have the same physical particle count \(M_\lambda\): adjacent effective-particle exchanges connect its fixed-weight sector and preserve physical count. Consequently, a homogeneous product state has one common complex amplitude throughout that fragment. Its fragment weight is
\[
w_\lambda=\binom{\ell}{m}p^{M_\lambda}(1-p)^{N+2-M_\lambda}.
\]
Sampling an IID physical word and retaining its label therefore samples the correct fragment weight. Conditional on that label, the state is \(|D_{\ell,m}\rangle\). Cross-fragment coherences cannot affect computational-basis output probabilities because evolution preserves labels and their computational supports are disjoint.

For \(0<m<\ell\), put \(n=\ell+1\), \(z=m/(\ell-m)\), and \(s=m\bmod2\). Every even principal Pfaffian of the stated sign matrix \(J\) equals \(1\), by its alternating Pfaffian recurrence. Thus the unnormalized Gaussian has coefficient \(z^{|T|/2}\) on each even occupied set \(T\), and squared norm
\[
D_z=\sum_{r\ {\rm even}}\binom nr z^r
=\frac{(1+z)^n+(1-z)^n}{2}.
\]
The acceptance probability is exactly
\[
a_{\ell,m}=\frac{\binom{\ell}{m}z^{m+s}}{D_z}.
\]
Writing \(r=m/\ell\),
\[
a_{\ell,m}
=\frac{2\,\Pr[\operatorname{Bin}(\ell,r)=m]\,
r^s(1-r)^{1-s}}
{1+(1-2r)^n}.
\]
Here \(m\) is a binomial mode, so its probability is at least \(1/(\ell+1)\); the spectator factor is at least \(1/\ell\), and the denominator is at most \(2\). Hence
\[
a_{\ell,m}\ge \frac1{\ell(\ell+1)}.
\]
Physical number-preserving unitary evolution commutes with the acceptance projector, preserving both this probability and the normalized projected-state identity.

Handle \(\ell=0\), \(m=0\), and \(m=\ell\) directly. No Gaussian normalization square root is needed by the sampler.

**Important:** retain the sampled label throughout rejection. Resampling labels after rejection would generally bias them by their different acceptance probabilities.

## 2. Binary-time approximation in one small field

For the selected length, use
\[
K=\mathbb Q(\zeta_c),\qquad c=4n,\qquad D=[K:\mathbb Q]\le4n.
\]
There is no need to represent the normalization square root in \(S\):
\[
U'_{ab}=\frac2n\sum_{j=1}^{\ell}
\sin\frac{\pi aj}{n}\sin\frac{\pi bj}{n}\,d_j\in K.
\]
Indeed, \(i=\zeta_c^n\), and all displayed sines belong to \(K\). Discrete sine orthogonality proves exact unitarity whenever \(|d_j|=1\).

Use rational circle points, not independently normalized rounded complex numbers. Choose a rotation \(\rho\in\{1,i,-1,-i\}\) so that the target phase, after rotation, has real part bounded positively away from zero. A constant-accuracy estimate suffices to choose such a chart with a fixed margin. Approximate its bounded stereographic coordinate by a dyadic rational \(v\), and set
\[
d_j=\rho\,\frac{1-v^2+2iv}{1+v^2}.
\]
This is exactly unit modulus, lies in \(\mathbb Q(i)\subset K\), and approximates the desired phase with error \(O(|\Delta v|)\). Its rational numerator and denominator have \(O(b)\) bits for \(b\)-bit accuracy.

For the supplied native normalization, the target is
\[
e^{-it\lambda_j}=e^{\,it\cos(\pi j/n)}.
\]
If \(T\) is the input bit length of \(t\), precision
\[
O(T+b+\log n)
\]
suffices to compute the cosine, multiply by \(t\), and perform range reduction. Certified elementary series with explicit remainder bounds implement these operations in polynomial bit time. Near a range-reduction boundary, either adjacent quotient gives a bounded residual; no exact transcendental equality test is required.

Taking
\[
\max_j|d_j-e^{-it\lambda_j}|\le\gamma
\]
gives \(\|U'-U\|\le\gamma\). On the \(m\)-particle exterior power,
\[
\|\Gamma_m(U')-\Gamma_m(U)\|\le m\gamma
\]
by tensor-product telescoping. Thus the conditional output-distribution error is at most \(m\gamma\), **without division by the Gaussian acceptance probability**.

This uses one field per selected length. Taking a compositum over every possible length is unnecessary and is not covered by the \(O(\ell)\)-degree assertion.

## 3. Covariance: signs and invertibility

Use the convention
\[
M_{ab}=i\langle c_a c_b\rangle\quad(a\ne b).
\]
For the pairing state with matrix \(Z'\), its annihilators are \(a-Z'a^\dagger\), giving precisely
\[
A=\frac12\bigl(I-Z',-i(I+Z')\bigr).
\]
Antisymmetry of \(Z'\) implies
\[
AA^T=0,\qquad
AA^\dagger=\frac12(I+Z'Z'^\dagger)\succeq I/2.
\]
Thus the proposed inverse always exists.

Let
\[
P=A^\dagger(AA^\dagger)^{-1}A.
\]
It is a rank-\(n\) Hermitian projector. Isotropy gives \(P+P^T=I\). Normalizing the annihilators to canonical ones gives
\(\langle cc^T\rangle=2P\), hence
\[
\boxed{M=-i(I-2P)}.
\]
It is real antisymmetric and satisfies \(M^2=-I\).

For \(Z'=0\),
\[
M_{\rm grouped}=
\begin{pmatrix}0&I\\-I&0\end{pmatrix},
\]
so interleaving gives \(M_{2j-1,2j}=+1\), as required.

This construction does not use potentially singular postmeasurement covariance updates from the supplied excerpt.

## 4. Explicit coordinates and height bounds

“Polynomially many arithmetic operations” alone is insufficient. Use explicit power-basis coordinates
\[
x=\frac1Q\sum_{j=0}^{D-1}a_j\zeta_c^j,
\qquad a_j,Q\in\mathbb Z,\quad Q>0.
\]
Construct \(\Phi_c\) uniformly; since \(c=O(N)\), even trial division and elementary polynomial arithmetic suffice. No number-field or arithmetic-DAG advice is supplied.

Here are elementary bounds sufficient for the clock. Put \(\kappa=8c^2\). Cyclotomic coefficients have magnitude at most \(2^D\), since their roots have modulus one. Monic reduction then gives:

* multiplying integral coordinate vectors of heights \(h,h'\) produces height at most \(h+h'+\kappa\);
* conjugation increases height by at most \(\kappa\);
* an \(r\times r\) determinant of entries of height \(h\) has height at most
  \(r(h+\kappa+\lceil\log_2(2r)\rceil)\).

“Height” here means a bound on coefficient bit lengths. These estimates follow by bounding individual products and the number of determinant terms; those terms need not be enumerated.

For a nonzero integral element \(\alpha\), form its \(D\times D\) integer multiplication matrix \(T_\alpha\). Then
\[
\alpha^{-1}
\]
has a rational-coordinate representation obtained from
\(\operatorname{adj}(T_\alpha)e_0/\det T_\alpha\). The determinant is the nonzero integer field norm. Both numerator and denominator bit lengths are
\[
O\!\left(D(h+\kappa+\log D)\right).
\]
This explicitly pays algebraic inversion and its denominator.

For completeness, one deliberately loose uniform bound is as follows. Let \(b\) bound the rational phase numerator/denominator bit lengths, and set
\[
\begin{aligned}
h_0&=10n\bigl(b+\kappa+\lceil\log_2(2n)\rceil+1\bigr),\\
W&=h_0+\kappa+\lceil\log_2(2nD)\rceil+1,\\
H&=1000n^2DW.
\end{aligned}
\]
The construction admits covariance entries and **every** joint prefix probability with numerator coordinates and denominator bounded by \(2^H\).

To verify this bound, clear the phase denominators by their product. The sine formula, \(Z'\), and \(A\) give \(A=C/q_0\), with integral \(C\) and coordinate/denominator heights at most \(h_0\). Put
\[
B=CC^\dagger,\qquad \delta=\det B\ne0.
\]
The preceding estimates give, conservatively:

* entries of \(B\): height at most \(4W\);
* \(\delta\) and the minors of \(B\): height at most \(6nW\);
* rational coordinates of \(\delta^{-1}\): height at most \(8nDW\).

The scalar \(q_0\) cancels:
\[
P=C^\dagger B^{-1}C.
\]
Thus all covariance entries have one common integer denominator
\(Q=|\operatorname{Norm}(\delta)|\), and numerator/denominator heights at most \(20nDW\).

A \(2k\)-dimensional prefix Pfaffian has degree \(k\le n\). All prefix probabilities therefore have the common denominator
\[
(2Q)^n,
\]
after padding smaller prefixes, with coordinate heights below \(H\). This is uniform over exponentially many possible prefixes, without enumerating them.

Determinants and adjugates can be computed using matrix powers, Newton identities, and Cayley–Hamilton, with only small-integer divisions. Their intermediates have bounded polynomial degree and polynomial height. This supplies an explicit polynomial-bit implementation, not an arbitrary arithmetic circuit whose intermediates might swell.

## 5. Prefix Pfaffians and exact zero/sign tests

For one mode,
\[
i c_{2j-1}c_{2j}=1-2n_j,
\]
so the specified outcome projector is
\[
\frac{1+s_j i c_{2j-1}c_{2j}}2.
\]
Wick’s rule, followed by expansion using adjacent pairs from the added block diagonal matrix, gives
\[
\boxed{
p(s_1,\ldots,s_k)=
2^{-k}\Bigl(\prod_j s_j\Bigr)
\operatorname{Pf}\!\left(M_{\rm prefix}+\bigoplus_j s_jJ_2\right).
}
\]
For \(k=1\), this is \((1+s_1M_{12})/2\). The general expansion has the same sign because each added \(J_2\) occupies an adjacent pair.

There is a polynomial algorithm that avoids both exponential expansion and an ambiguous numerical square root. For any skew \(2k\times2k\) matrix \(X\), let \(J_0=\bigoplus J_2\) and write
\[
g(x)=\det(J_0+xX)=f(x)^2,\qquad
f(x)=\operatorname{Pf}(J_0+xX),\quad f(0)=1.
\]
Compute the first \(k\) coefficients of \(g(x)=\det(I-xJ_0X)\) using traces and Newton identities. Then
\[
f_0=1,\qquad
f_r=\frac12\left(g_r-\sum_{j=1}^{r-1}f_jf_{r-j}\right).
\]
The coefficient \(f_k\) is \(\operatorname{Pf}(X)\), including its sign. After clearing the matrix denominator, all divisions are by known small integers; the coefficient bounds above apply.

Zero testing is exact: reduce to the power basis and test all integer numerator coordinates.

For sign and approximation, a uniform separation bound follows directly from the field norm. If a represented nonzero real \(x=a/Q\) has height at most \(H\), every conjugate of \(a\) has magnitude at most \(D2^H\), while \(|\operatorname{Norm}(a)|\ge1\). Hence
\[
|x|\ge 2^{-H}(D2^H)^{-(D-1)}.
\]
Define
\[
L=DH+(D-1)\lceil\log_2D\rceil+2,\qquad \Delta=2^{-L}.
\]
Every nonzero prefix probability is at least \(\Delta\). Certified evaluation of the distinguished root \(\zeta_c=e^{2\pi i/c}\) to polynomially many bits now determines every nonzero real sign. No stability promise is imported.

## 6. Tiny conditional probabilities and bounded coins

At a reachable prefix let
\[
a=p(\text{prefix})>0,\qquad
b=p(\text{prefix followed by }0),\qquad q=b/a.
\]
Test \(b=0\) and \(b=a\) exactly and take the deterministic outcome in those cases. This prevents entering a zero-probability prefix through rounding.

Otherwise \(a\ge\Delta\) and \(0<b<a\). Approximate \(a,b\) to absolute error at most \(\delta\Delta/16\). Since \(b\le a\), their quotient has error below \(\delta/4\). Round and clamp it to a dyadic probability with denominator \(2^u\), where \(2^{-u}\le\delta/2\), and sample using exactly \(u\) fair bits.

The required evaluation precision is
\[
H+L+\log_2(1/\delta)+O(\log D),
\]
which is polynomial. Thus an exponentially small reachable prefix does not trigger an unbounded refinement loop.

An exact algebraic conditional ratio is also available: invert its integral prefix numerator using its multiplication matrix. This adds only another factor \(D\) to the height bound. Sampling need not perform that inversion.

With conditional probability error at most \(\delta\) at each of \(n\) positions, sequential coupling bounds the complete Gaussian proposal error by \(n\delta\). All probabilities are recomputed from the original covariance; conditional denominators are not recursively nested.

## 7. Complete TV budget and worst-case clock

Assume \(0<\epsilon<1\), and put
\[
n_{\max}=N+2,\qquad
a_*=\frac1{(N+1)(N+2)}.
\]

Use the following allocations.

1. **Label sampling.** Replace \(p\) by a dyadic \(p'\) satisfying
   \[
   |p-p'|\le\epsilon/(4n_{\max}).
   \]
   Sampling the physical IID word and encoding it changes the label distribution by at most \(\epsilon/4\). Exact integer division computes \(p'\), charging the input bit length of \(p\).

2. **Evolution approximation.** Choose phase error
   \[
   \gamma\le\epsilon/[4(N+1)].
   \]
   Every conditional fragment output changes by at most \(\epsilon/4\).

3. **Gaussian proposal sampling.** Require proposal TV error
   \[
   \tau=a_*\epsilon/8.
   \]
   Set per-bit error \(\delta=\tau/n_{\max}\). If \(P\) is the exact proposal and \(\widetilde P\) its finite-bit approximation, then
   \[
   \widetilde P(A)\ge a_*-\tau\ge a_*/2,
   \qquad
   d_{\rm TV}(P(\cdot|A),\widetilde P(\cdot|A))
   \le 2\tau/a_*\le\epsilon/4.
   \]

4. **Capped rejection.** Make at most
   \[
   R=2a_*^{-1}\left\lceil\log_2(4/\epsilon)\right\rceil
   \]
   independent proposals within the retained label. Failure probability is at most
   \(e^{-a_*R/2}\le\epsilon/4\). On failure, output any fixed valid word in that label.

Conditional on any success before the cap, the first accepted proposal has exactly the law \(\widetilde P(\cdot|A)\). Thus there is no additional \(R\tau\) error term.

The four contributions sum to at most \(\epsilon\).

Field construction, phase computation, covariance construction, each prefix calculation, certified evaluation, bounded coins, and decoding all have polynomial bit cost. There are at most \(R=O(N^2\log(1/\epsilon))\) proposals. Reading \(p,t\) and the accuracy specification is charged; writing the full \(N+2\)-bit output costs \(\Omega(N)\). No quantum state-preparation or sampling oracle is used. Every loop has a predetermined polynomial bound and can be padded to a fixed worst-case clock.

## Scope and falsifiers

The result is conditional on the admitted folded map and projected-Gaussian identity; their normalization interface has been checked above. It does not establish the optional coherent-amplitude/tractable-state interface or simulation of arbitrary unknown quantum inputs.

Implementation-level falsifiers include failure of exact \(U'^\dagger U'=I\), the stated covariance convention, the common-coordinate bounds, certified phase errors, or retaining the label throughout rejection. Independent square-root phase normalization, adaptive unbounded refinement, and exact non-dyadic coin claims would invalidate this proof.

**Conclusion:** there is no field-degree, cancellation, denominator, or tiny-prefix obstruction to this repaired construction. The explicit representation, separation, and TV arguments establish the requested full-output polynomial-BIT sampler under the stated structural hypotheses; failed attacks and finite examples are not being used as substitutes for that proof.