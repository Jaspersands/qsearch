## Status

I cannot close the requested polynomial-BIT ONE-HALF theorem. In particular, I cannot derive uniform polynomial bounds for the nonzero Smith valuations of the selected Stoll \(M_j\) and augmented \(B_j\), including their construction losses.

There are, however, two exact representative-choice deductions available:

1. a **native, polynomial-depth, full-dimensional sampler inside the actual fixed \(E\)**, with actual-point certificates; and
2. a **deterministic finite-grid repair of the source branch resultant**, preserving the same actual point and charging all coefficient denominators.

The second deduction supplies a genuine discriminant-based conditioning bound, but not the missing Stoll-minor bound. Neither deduction proves impossibility of the full task.

All arguments below are symbolic; no computation or new finite control was performed.

---

## 1. A certified native grid inside the fixed \(E\)

Let \(n_s\ge 2\) be the exponent **actually used in the fixed seeds**
\[
t_i=2^{n_s}i,\qquad 1\le i\le g.
\]
Thus this construction does not replace \(L\) or change the allowed error subgroup.

Write
\[
F(z)=z^{2g+1}f(1/z),
\]
and, for \(t\in4\mathbb Z_2\setminus\{0\}\), define the actual point class
\[
\mathcal P(t)=
\left[
\left(t^{-2},\,t^{-(2g+1)}\sqrt{F(t^2)}\right)-\infty
\right],
\]
where the square root is the unique one congruent to \(1\bmod 8\).

Use the already established seed determinant valuation
\[
D_0=v_2\det\bigl(\ell_k(t_i)\bigr)_{\substack{0\le k<g\\1\le i\le g}},
\]
where
\[
\ell_k(t)=-\sum_{a\ge0}\frac{c_a t^{2(k+a)+1}}{2(k+a)+1},
\qquad v_2(c_a)\ge-2a.
\]

Set
\[
H=n_sg(g-1)+\sum_{i<j}v_2(j^2-i^2),
\qquad R=D_0+1,
\]
and define
\[
\sigma(z)=
\sum_{i=1}^g
\bigl(\mathcal P(t_i+2^Rz_i)-\mathcal P(t_i)\bigr),
\qquad z\in\mathbb Z_2^g.
\]

### Lemma 1 — legal, quantitatively full-dimensional perturbations

The following hold uniformly for every native \(f\), including arbitrary bad reduction.

1. **Every \(\sigma(z)\) lies in the original \(E=2L\).**

2. Put
   \[
   W_{ki}=-\frac{t_i^{2k}}{\sqrt{F(t_i^2)}}.
   \]
   The image \(\mathcal U=\sigma(\mathbb Z_2^g)\) is a subgroup of \(E\), and
   \[
   \log\mathcal U=2^RW\mathbb Z_2^g.
   \]
   In particular,
   \[
   2^{R+H}\mathbb Z_2^g
   \subseteq \log\mathcal U
   \subseteq 2^R\mathbb Z_2^g.
   \]

3. For every \(m\ge1\), sampling each \(z_i\) uniformly from
   \[
   \{0,\ldots,2^m-1\}
   \]
   gives an **exact uniform sample of**
   \[
   \mathcal U/2^m\mathcal U.
   \]
   No enumeration of this quotient is required.

4. The sampled shift has an actual-point certificate constructible in bit cost
   \[
   \operatorname{poly}(g,B,n_s,R,m,Q)
   \]
   for requested absolute coordinate precision \(Q\). For the standard choice \(n_s=2\), \(R=O(g^2\log(g+1))\).

### Proof of membership in \(E\)

Let
\[
S=(\ell_k(t_i)).
\]
Its entries are integral. The adjugate identity therefore gives
\[
2^{D_0}\mathbb Z_2^g\subseteq S\mathbb Z_2^g=\log L,
\]
hence
\[
2^{D_0+1}\mathbb Z_2^g\subseteq 2\log L=\log E. \tag{1}
\]

For \(t\in4\mathbb Z_2\), changing \(t\) by \(2^Rz\) changes every \(\ell_k(t)\) by an element of \(2^R\mathbb Z_2\). Consequently
\[
\log\sigma(z)\in2^R\mathbb Z_2^g.
\]
Equation (1), together with injectivity of the logarithm on the torsion-free formal neighborhood already used for the seeds, proves
\[
\sigma(z)\in E.
\]

This is an \(E\)-membership proof, not merely a Kummer-label argument.

### Proof of quantitative openness and uniformity

The derivative matrix is \(W\), and its determinant is a Vandermonde determinant times units. Thus
\[
v_2(\det W)=H.
\]
Moreover,
\[
D_0-H=n_sg+\sum_i v_2(i)\ge2g. \tag{2}
\]

The coefficient of \(z_i^a\), \(a\ge1\), in
\[
\ell_k(t_i+2^Rz_i)-\ell_k(t_i)
\]
has valuation at least
\[
(R-1)a+1.
\]
Indeed, expand each odd power in the displayed logarithm series and use
\(v_2(t_i)\ge2\) and \(v_2(c_b)\ge-2b\).

It follows that
\[
\log\sigma(z)=2^RW\bigl(z+\varepsilon(z)\bigr),
\]
where \(\varepsilon\) is a convergent restricted power series whose coefficients have valuation at least
\[
R-H-1=D_0-H\ge2.
\]
Therefore \(z\mapsto z+\varepsilon(z)\) is a bijection of \(\mathbb Z_2^g\), obtained by strict contraction, and induces a permutation modulo every \(2^m\). This proves the asserted image and finite-grid distribution.

The ball inclusion follows again from the adjugate identity for \(W\). No logarithm or matrix inverse must be numerically evaluated to generate the samples; they are used in the proof.

### Actual-point and precision costs

Let
\[
T_{\max}=n_s+\lfloor\log_2g\rfloor.
\]
Here \(R>T_{\max}\), so
\[
v_2(t_i+2^Rz_i)=v_2(t_i).
\]
Thus the individual sampled curve points have pole valuations bounded by
\[
-v_2(x)\le2T_{\max},\qquad
-v_2(y)\le(2g+1)T_{\max}.
\]

For each sampled parameter \(t\),
\[
F(t^2)\equiv1\pmod {16}.
\]
Its selected square root can be computed without a root oracle. For example, writing \(u=F(t^2)-1\), the binomial series
\[
(1+u)^{1/2}=\sum_{a\ge0}\binom{1/2}{a}u^a
\]
has its \(a\)-th term of valuation at least \(2a\). Truncating after
\[
O\bigl(Q+(2g+1)T_{\max}\bigr)
\]
terms therefore suffices for absolute \(Q\)-digit precision in \(y\). Exact-rational evaluation of this truncation has polynomial intermediate bitlength.

An actual-point certificate consists of the exact integer \(t\), the defining equation for the square root, its residue \(1\bmod8\), and certified coordinate approximations. The shift is stored as a signed divisor expression of length \(2g\). No compositum of the quadratic fields is constructed.

**Boundary:** this pays construction of an actual shift. It does **not** pay reduction of \(h+\sigma(z)\) to a suitably conditioned Mumford representation.

### Application to the halving contract

For simultaneous movement of a point and its halves, use
\[
h_z=h+2\sigma(z).
\]
Then \(h_z+E=h+E\) exactly. If \(2q=h\), then
\[
2\bigl(q+\sigma(z)\bigr)=h_z.
\]
Thus the perturbation moves every half through a known full-dimensional formal neighborhood while preserving the allowed input coset. An exact half \(q_z\) of \(h_z\) satisfies the explicit residual certificate
\[
2q_z-h=2\sigma(z)\in E.
\]

This settles lawful perturbation and its sampling distribution. **It is not yet a success bound for Stoll conditioning.**

---

## 2. A paid finite-grid branch-resultant repair

There is also a useful correction and strengthening of the constant-parameter chart replacement in the supplied Stoll excerpt.

Let \(n=2g+1\), and let
\[
P=[a,b],\qquad \deg a=e\le g,\quad a\text{ monic},\quad \deg b<e,
\]
be an actual Mumford point certificate. Suppose its coefficient pole bound is
\[
v_2(a_i),v_2(b_i)\ge-S_0.
\]
This bound is obtainable from a certified finite representation; it is not an exact-rank or conditioning oracle. However, proving that its **numerical value** is polynomial in the native input remains necessary.

Put
\[
c=\frac{f-b^2}{a},\qquad m=n-e,\qquad S=(m+2)S_0.
\]
Monic long division gives coefficient valuations at least \(-S\) for \(a,b,c\).

For an integer parameter \(u\), set
\[
A_u=c-2ub-u^2a,\qquad \beta_u=-b-ua.
\]
The supplied Stoll identity gives
\[
[A_u,\beta_u]=[a,b].
\]
Since \(m>e\), \(A_u\) remains monic of degree \(m\), for every \(u\).

Write
\[
D=v_2(\operatorname{disc}f),\qquad
K_{\rm br}=D+2nS+v_2((2n)!).
\]

### Lemma 2 — deterministic branch avoidance with a numerical certificate

Among
\[
u=0,1,\ldots,2n
\]
there is at least one satisfying
\[
v_2\!\left(\operatorname{Res}_x(f,2^SA_u)\right)\le K_{\rm br}. \tag{3}
\]

Consequently:

* \(\gcd(A_u,f)=1\);
* the point is unchanged, hence certainly remains in the same \(E\)-coset;
* the integral Sylvester matrix of \(f\) and \(2^SA_u\) is invertible and every Smith valuation is at most \(K_{\rm br}\).

This is a bound for an actual source gcd/CRT operation—not a bound for \(M_j\) or \(B_j\).

### Proof of the discriminant bound

Let
\[
\mathscr R(U)=\operatorname{Res}_x(f,2^SA_U)\in\mathbb Z_2[U].
\]
Its degree is at most \(2n\).

For proof only, let \(\theta\) run through the roots of \(f\). All are integral. Differentiating
\[
f=b^2+ac
\]
and evaluating at \(\theta\) gives
\[
f'(\theta)
 =2b(\theta)b'(\theta)+a'(\theta)c(\theta)+a(\theta)c'(\theta).
\]
The derivative evaluations \(a'(\theta),b'(\theta),c'(\theta)\) have valuation at least \(-S\). Hence
\[
\min\!\left\{
v_2(c(\theta)),\,
1+v_2(b(\theta)),\,
v_2(a(\theta))
\right\}
\le v_2(f'(\theta))+S. \tag{4}
\]

For a polynomial over a valued field, let its content valuation be the minimum coefficient valuation. Gauss valuation is multiplicative. Applying this to
\[
\mathscr R(U)=
\prod_\theta
2^S\bigl(c(\theta)-2Ub(\theta)-U^2a(\theta)\bigr)
\]
and using (4) yields
\[
\operatorname{content}_2(\mathscr R)
\le nS+\sum_\theta\bigl(v_2(f'(\theta))+S\bigr)
=D+2nS. \tag{5}
\]
The roots and their splitting field are used only in this proof, not constructed.

Now interpolate a polynomial of degree at most \(d=2n\) at \(0,\ldots,d\). Every Lagrange denominator divides \(d!\) in valuation:
\[
v_2(i!(d-i)!)\le v_2(d!).
\]
If all those values of \(\mathscr R\) were divisible by \(2^{K_{\rm br}+1}\), every coefficient would have valuation greater than \(D+2nS\), contradicting (5). This proves (3).

Notice the normalization: this is an **upper bound on the valuation of a scaled resultant**. It makes no incorrect positive lower-bound claim for an unscaled resultant with nonintegral coefficients.

### Entry construction and numerical clock

A conservative sufficient absolute precision for the input coefficients \(a,b\), merely to find and certify the successful \(u\), is
\[
P\ge K_{\rm br}+S+1.
\]
Monic division loses at most \(S\) digits under the above coefficient bounds. The scaled Sylvester entries can then be formed modulo \(2^{K_{\rm br}+1}\).

For each of the \(2n+1\) candidates, compute the determinant modulo that modulus using integer lifts. This requires only polynomial-size integer arithmetic; it does not require division by uncertain nonunits. A nonzero residue certifies the actual nonzero resultant.

If an inverse Sylvester map is required to absolute precision \(Q\), the conservative schedule
\[
P\ge Q+2K_{\rm br}+S+2
\]
also pays inverse-matrix sensitivity.

The total cost is polynomial in
\[
g,\ B,\ Q,\ \text{the numerical value }S_0.
\]
Also \(D\) is natively computable and polynomially bounded by the coefficient bits, via the integer discriminant/resultant.

**Unpaid parts of this repair:** it does not prove \(A_u\) squarefree, bound the Stoll square-root construction, or control a half approaching the theta/degree-drop locus. The latter is precisely something a same-point chart replacement cannot generally cure.

---

## 3. The specific remaining input

The unresolved input is now identifiable more sharply than “generic representatives exist.”

It is a **uniform arithmetic jet/content bound for the Stoll correspondence under the explicit perturbation above**.

For an actual half \(q\), put
\[
q_z=q+\sigma(z),\qquad h_z=2q_z.
\]
Pull back the relevant coordinate functions and regularity witnesses along these maps. A sufficient native theorem must provide polynomial bounds for:

1. **Chart construction:** denominators needed to obtain Mumford data for \(h_z\) and the eventual output, including a polynomial numerical pole bound \(S_0\).
2. **Root and degree operations:** the Stoll square root in \(\mathbb Q_2[x]/f\), squarefree/degree decisions, and the required subresultants.
3. **The actual Stoll minors:** after specified integral row/column scalings, suitable nonzero maximal minors of the relevant \(M_j\) and injective \(B_j\).
4. **Recovery and certification:** gcd/CRT reconstruction of the output and a certificate identifying an actual point behind its approximation.

The missing quantitative assertion is not merely that these witnesses are nonzero. After all denominators have been paid, one needs a bound of the form
\[
\min_{|\alpha|\le d}
v_2\!\left([z^\alpha]F_q(z)\right)\le C,
\qquad
C,d\le\operatorname{poly}(g,B),
\]
together with a uniform tail bound permitting finite-precision evaluation. It must hold for the witnesses actually used by the algorithm, uniformly over the relevant \(q\), without supplying \(q\), a model, or conditioning advice.

Why this would suffice for representative selection is quantitative. For an integral polynomial \(P\) of degree at most \(d\) and content valuation at most \(C\), the grid
\[
z\in\{0,\ldots,2^m-1\}^g
\]
satisfies
\[
\Pr\!\left[
v_2(P(z))>C+gd(m-1)
\right]\le \frac{gd}{2^m}. \tag{6}
\]
In one variable, factorization is used only for analysis: a root can be within valuation \(>m-1\) of at most one grid point. Induction on the variables gives (6). Union bounds then give a polynomial-random-bit sampler once the degree, content, normalization, and tail bounds are supplied. Any exponentially many half branches would enter only an analysis union bound; they must not be enumerated.

Lemma 2 proves such a content bound for **one particular witness**, the source branch resultant. I cannot establish it for the normalized Stoll minors and the other required witnesses.

A possible paid route would be an explicit, bounded-denominator jet/Bézout certificate controlled by powers of \(2\operatorname{disc}f\), with polynomial exponents and construction size. Generic nonvanishing or an unspecified effective Nullstellensatz does not supply those bounds.

### Falsifiers and scope

* A proposed uniform jet bound is refuted by a native family violating its stated bounds **for every witness/chart alternative permitted by that proposal**. One badly conditioned representative is not enough.
* Lemma 2 has a concrete falsifier: valid certified \(a,b\) satisfying its pole bound, but every \(u=0,\ldots,2n\) having scaled resultant valuation \(>K_{\rm br}\). An unscaled negative resultant valuation is not such a falsifier.
* Promoting the explicit \(E\)-sampler to a conditioning sampler without the missing content/tail bounds leaves the central proof obligation unpaid.
* A successful numerical kernel calculation without an actual-point certificate does not meet ONE-HALF.

**Bottom line:** lawful full-dimensional \(E\)-randomization and a bounded branch-resultant repair can be proved. Uniform conditioning of the complete native Stoll halving operation remains open; the named local blocker in the GRH two-Selmer-dimension composition is not removed.