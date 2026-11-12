# Row-creation contraction audit

**Disposition: no unrestricted polynomial classical contraction is established.** There is an exact all-degree commutation reduction, but it leaves shape-dependent operators between the otherwise elementary Hall contractions. The simplest scalar and degree-only closures are false. A literal universal linear transfer-state construction also has an exponential-rank obstruction, under a stated assumption.

The positive absolute-path operators cannot simply replace the signed operators in normalized Born sampling. The proposed one-row proportionality is correct; nevertheless, normalized proportionality fails already at degree four, including at a reached derivative history. An unbounded-Durfee family gives an all-degree support falsifier.

These are falsifiers of specified constructions—not hardness results or evidence of a quantum separation. All calculations below are algebraic deductions from the supplied formulas; no external source inspection or execution was performed.

## 1. The doubled quantity that must be contracted

Write
\[
b_k=3k\partial_{p_k},\qquad b_k^*=p_k,\qquad
\mathcal R_\lambda=R_{\lambda_1}\cdots R_{\lambda_\ell}.
\]
For a derivative history with multiplicities \(h=(h_1,h_2,\ldots)\), define
\[
Q_h=\prod_k b_k^{h_k},\qquad
N_h=\|Q_hJ_\lambda\|^2,\qquad
d=D-\sum_k kh_k.
\]
The required doubled contraction is exactly
\[
N_h=
\langle 1,\,
R_{\lambda_\ell}^*\cdots R_{\lambda_1}^*
\Bigl(\prod_kp_k^{h_k}\Bigr)
\Bigl(\prod_kb_k^{h_k}\Bigr)
R_{\lambda_1}\cdots R_{\lambda_\ell}1
\rangle.                                                     \tag{1}
\]

Hall adjointness and Euler’s identity give
\[
\sum_{k=1}^{d}N_{h+e_k}=3dN_h.
\]
Thus the next-part probabilities are
\[
q_h(k)=\frac{N_{h+e_k}}{3dN_h}.
\]
There are at most \(D\) selections and \(O(D^2)\) candidate-norm queries. The unpaid task is computing these quantities at reached histories—not generating a short expression for \(J_\lambda\).

## 2. Commuting before expansion: an exact reduction

Put
\[
C_r(u)=[t^r]\exp B_\infty(t,p,u),
\qquad
R_r=(-1)^r C_r(-3r).
\]

### 2.1 What the catalytic operator actually does

At \(\alpha=3\), the displayed source operator gives
\[
(\Gamma_Y+uY_+)(y_jf)
=
\sum_{i\ge1}y_{j+i+1}b_if
+\sum_{i=1}^{j}y_{j+1-i}p_if
+(u+2j)y_{j+1}f.                                             \tag{2}
\]
In particular, with
\[
L_+=\sum_{i\ge1}i p_{i+1}\partial_{p_i},
\]
\[
B_1(u)=L_++\frac u3p_1.                                      \tag{3}
\]

The catalytic index is only \(O(D)\) after degree truncation. But its entries in (2) are polynomials in all the occupation modes. A small catalytic index is not a small contraction state.

### 2.2 Exact diagonal conjugation

There is a useful consequence of supplied Theorem 5.2. For generic real \(u\), define the formal diagonal operator
\[
T_uJ_\nu=J_\nu(u)J_\nu,
\]
where \(J_\nu(u)\) denotes the specialization used in the supplied \(\tau_b\).

Let \(U_m(\eta,\nu)\) be the coefficient of \(J_\eta\) in \(p_mJ_\nu\). Hall adjointness gives
\[
\partial_{q_m}J_\eta(q)
=\frac1{3m}\sum_\nu
U_m(\eta,\nu)\frac{H_\eta}{H_\nu}J_\nu(q).
\]
Comparing Jack coefficients in
\[
\frac{t^m}{m}B_m(p,u)\tau_b=\partial_{q_m}\tau_b
\]
therefore proves
\[
\boxed{\displaystyle B_m(p,u)=\frac13T_up_mT_u^{-1}.}         \tag{4}
\]

Define multiplication and translation operators
\[
G(t)=\exp\!\left(\sum_{k\ge1}\frac{t^kp_k}{3k}\right),
\qquad
S(t)=G(t)^*=\exp\!\left(\sum_{k\ge1}t^k\partial_{p_k}\right).
\]
Equation (4) yields the all-degree identities
\[
\exp B_\infty(t,p,u)=T_uG(t)T_u^{-1},
\]
\[
\bigl(\exp B_\infty(s,p,u)\bigr)^*
=T_u^{-1}S(s)T_u.
\]

Consequently, even the contraction of one generating creator with its adjoint becomes
\[
\boxed{\displaystyle
T_u^{-1}S(s)\,T_u^2\,G(t)T_u^{-1}.}                           \tag{5}
\]

Without the intervening \(T_u^2\), Hall contraction would be elementary:
\[
S(s)G(t)=(1-st)^{-1/3}G(t)S(s).
\]
The actual doubled expression instead contains shape-dependent diagonal operators between translations and multiplications. Different rows also introduce ratios of different \(T_u\)'s, and the derivative-history insertions remain.

This is a precise bottleneck: **the scalar Hall kernel does not contract the intervening shape-dependent operators.**

There is also a specialization issue. At \(u=-3r\), some eigenvalues of \(T_u\) vanish. Equation (4) is a generic-\(u\) identity followed by coefficientwise specialization of the original polynomial operators. It does **not** authorize division by those zero eigenvalues. Treating \(T_u\), its inverse, or their matrix elements as an oracle would conceal the task being audited.

## 3. The simplest commutator closures fail

### 3.1 Row one: scalar Wick contraction fails, but an \(sl_2\) closure survives

Equation (3) gives
\[
R_1=p_1-L_+.
\]
Its Hall adjoint is
\[
R_1^*=3\partial_{p_1}-L_-,
\qquad
L_-=\sum_{i\ge1}(i+1)p_i\partial_{p_{i+1}}.
\]
Writing
\[
\mathsf N=\sum_{i\ge1}i p_i\partial_{p_i},
\]
direct commutation gives
\[
\boxed{[R_1^*,R_1]=3+2\mathsf N.}                             \tag{6}
\]

So these are not scalar-contraction bosons. For example,
\[
R_1^21=p_1^2-p_2,\qquad
\|R_1^21\|^2=18+6=24,
\]
where a scalar Wick rule using \(\|R_11\|^2=3\) would give \(2\cdot3^2=18\).

However, (6) does close with the degree operator. Rejecting that particular Wick rule does not yet defeat a degree-augmented transfer state.

### 3.2 Row two defeats the degree-only extension

From the source exponential,
\[
R_2=\frac12\bigl(B_2(-6)+B_1(-6)^2\bigr).
\]
Equation (2) gives, with \(x=p_1^2\) and \(y=p_2\),
\[
\begin{aligned}
R_21&=x+3y,\\
R_2x&=p_1^4+p_1^2p_2+p_2^2-6p_1p_3+3p_4,\\
R_2y&=p_1^2p_2+4p_2^2-2p_1p_3-3p_4.
\end{aligned}                                                \tag{7}
\]
The degree-four power-sum norms, in the displayed order, are
\[
1944,\quad108,\quad72,\quad27,\quad12.
\]
Using these and \(R_2^*x=R_2^*y=18\), one obtains
\[
\boxed{\displaystyle
[R_2^*,R_2]\big|_{\operatorname{span}\{x,y\}}
=
\begin{pmatrix}
160&16\\
48&192
\end{pmatrix}.}                                               \tag{8}
\]
Equivalently,
\[
[R_2^*,R_2]J_{(2)}=208J_{(2)},\qquad
[R_2^*,R_2]J_{(1,1)}=144J_{(1,1)}.
\]
Both inputs have degree two. Thus a closure of the form
\([R_r^*,R_s]=F_{rs}(\mathsf N)\) is false.

Derivative commutation also fails to close by merely lowering a row label. Directly from \(B_1,B_2\),
\[
\boxed{[b_1,R_2]=3(R_1+p_1).}                                \tag{9}
\]
The vacuum value might suggest \(6R_1\), but on \(p_1\) the two operators give
\[
[b_1,R_2]p_1=6p_1^2-3p_2,
\qquad
6R_1p_1=6p_1^2-6p_2.
\]
For the valid shape \((2,1)\),
\[
J_{(2,1)}=p_1^3+2p_1p_2-3p_3,\qquad
b_1J_{(2,1)}=9p_1^2+6p_2.
\]
The incorrect row-lowering commutator would instead produce
\(9p_1^2+3p_2\).

These exact calculations falsify scalar-pairing, degree-only, and simple row-lowering closures. They do **not** exclude a different determinant or a larger, genuinely polynomial closure.

### 3.3 An all-degree obstruction to a literal universal linear boundary state

A stronger statement holds for one precisely defined transfer-state model.

**Assumption:** At a degree-\(d\) cut, arbitrary legal bra and ket row words are represented by a common \(w(d)\)-component linear boundary state, and their Hall inner product is obtained from a fixed bilinear pairing of those states.

For every \(\nu\vdash d\), the source row formula supplies the state \(J_\nu\). Their Gram matrix is
\[
\langle J_\mu,J_\nu\rangle=\delta_{\mu\nu}H_\nu,
\]
of rank \(p(d)\). Any such boundary factorization therefore requires
\[
\boxed{w(d)\ge p(d).}                                        \tag{10}
\]
This is superpolynomial. An elementary lower bound follows by choosing subsets of parts \(2,\ldots,\lfloor\sqrt d\rfloor+1\), then filling the remaining degree with ones.

Equation (10) rules out a universal polynomial-width **linear boundary representation with arbitrary cross-contractions**. The native task only demands particular matched contractions. Shape-dependent nonlinear representations and formulas that avoid such a boundary factorization are outside this argument. It is not a native sampling lower bound.

## 4. Absolute-path positivity: the one-row check passes, the sampling closure fails

Let
\[
A_r=C_r(3r).
\]
Its path coefficients are nonnegative, unlike those defining \(R_r\).

### 4.1 The proposed one-row proportionality is correct

The one-row Hall reproducing identity is
\[
J_{(D)}(p)=3^DD!\,[s^D]
\exp\!\left(\sum_{k\ge1}\frac{p_ks^k}{3k}\right).
\]
It follows from Hall duality and monomial triangularity: specialization to one variable kills every Jack shape except a row. Hence
\[
J_{(D)}(u)=3^D(u/3)_D,
\]
where \((a)_D\) is the rising factorial.

Set every \(q_k=1\) in supplied Corollary 5.3. Only the one-row Jack survives, giving
\[
C_D(u)1=\frac{(u/3)_D}{D!}J_{(D)}.
\]
Therefore
\[
\boxed{\displaystyle
A_D1=\binom{2D-1}{D}J_{(D)}.}                                \tag{11}
\]

The scalar in (11) cancels completely from normalized Born probabilities. A large raw one-row cancellation ratio is therefore not a falsifier of normalized sampling.

### 4.2 Exact degree-four falsifier, including a reached history

For \(\lambda=(2,1,1)\), equations (2)–(7) give
\[
\begin{aligned}
f&=R_2R_1^21=J_{(2,1,1)}
   =p_1^4-3p_2^2-4p_1p_3+6p_4,\\
g&=A_2A_1^21
   =3p_1^4+18p_1^2p_2+11p_2^2+24p_1p_3+24p_4.
\end{aligned}                                                \tag{12}
\]

The target assigns zero probability to \(\mu=(2,1,1)\). The normalized Born law of \(g\) assigns
\[
\frac{18^2\,\|p_1^2p_2\|^2}{\|g\|^2}
=\frac{34992}{83664}
=\frac{243}{581}.
\]
Thus direct replacement by the normalized absolute-path state has
\[
\operatorname{TV}\ge\frac{243}{581}>0.418.
\]

The failure also occurs inside the adaptive norm sampler:
\[
b_1^2f=108p_1^2,\qquad
b_1^2g=324(p_1^2+p_2).
\]
After history \((1,1)\), the target probability of selecting \(k=2\) is zero. The absolute-path replacement gives
\[
\frac{\|b_2b_1^2g\|^2}{6\|b_1^2g\|^2}=\frac14.
\]
This target history is genuinely reached; its probability is \(9/16\).

So the obstruction is not merely a large common normalization factor, nor a postselected zero-probability history.

### 4.3 An unbounded-Durfee support falsifier

The discrepancy extends to unrestricted shapes. Define
\[
n(\lambda)=\sum_i(i-1)\lambda_i,\qquad
n(\lambda')=\sum_i\binom{\lambda_i}{2},
\]
and
\[
G_\lambda=A_{\lambda_1}\cdots A_{\lambda_\ell}1,\qquad
c_\lambda=\prod_i\binom{2\lambda_i-1}{\lambda_i}.
\]
The creation operators imply
\[
\begin{array}{ll}
[p_1^D]J_\lambda=1,
&
[p_2p_1^{D-2}]J_\lambda=3n(\lambda')-n(\lambda),\\[2mm]
[p_1^D]G_\lambda=c_\lambda,
&
[p_2p_1^{D-2}]G_\lambda
=c_\lambda\bigl(3n(\lambda')+n(\lambda)\bigr).
\end{array}                                                  \tag{13}
\]

Here is a derivation from the new operators, without assuming an additional Jack character formula. Filter monomials by
\[
\delta(p_\mu)=|\mu|-\ell(\mu).
\]
Equation (2) shows that \(B_n\) never decreases this defect. Retaining only defect increases zero and one gives
\[
B_n(u)\equiv
\frac u3p_1^n
+\frac{u(u+2)n(n-1)}6p_2p_1^{n-2}
+n p_2p_1^{n-1}\partial_{p_1}.
\]
The terms arise respectively from one new-vertex step, two new/twist steps, and one merge step. Exponentiating this truncation and extracting \(t^r\) shows that, for
\[
f=c\bigl(p_1^d+\beta p_2p_1^{d-2}\bigr)
+\text{higher-defect terms},
\]
the leading coefficient is multiplied by \((u/3)_r/r!\), while
\[
\beta\longmapsto
\beta+3\binom r2+\frac{3rd}{u}.                               \tag{14}
\]
At \(u=-3r\), the final term is \(-d\); at \(u=3r\), it is \(+d\). Iterating proves (13).

Now take
\[
\lambda=(r^s),\qquad s=3r-2,\qquad r\ge2.
\]
This family has unbounded Durfee size. Since \(n(\lambda)=3n(\lambda')\),
\[
[p_2p_1^{D-2}]J_\lambda=0,
\qquad
[p_2p_1^{D-2}]G_\lambda=c_\lambda D(s-1)>0.
\]
The history consisting of \(D-2\) selections of \(1\) is reached because the \(p_1^D\) coefficient is nonzero. At that history, the target residual state is proportional to \(p_1^2\), whereas the absolute-path residual has a nonzero \(p_2\) component.

This is an all-degree falsifier of uniform scalar replacement by absolute-path norms. That history can be rare as degree grows; no asymptotic TV or rejection-cost lower bound is inferred from its existence alone.

## 5. What the exact recursion costs

Commutativity of the \(B_m(u)\) at fixed \(u\), supplied in the excerpt, gives an exact coefficient recursion. If
\[
F_n=[t^n]\exp B_\infty(t,p,u)f,
\]
then
\[
F_0=f,\qquad
nF_n=\sum_{m=1}^n B_m(u)F_{n-m}.                              \tag{15}
\]

Equation (15) is all-degree, but not a polynomial-dimensional contraction:

* Its polynomial number of coefficient indices does not eliminate the polynomial-valued states \(F_n\).
* An ambient power-sum implementation retains up to
  \[
  \sum_{d\le D}p(d)=\exp(O(\sqrt D))
  \]
  occupation labels.
* Attempting to recurse only their scalar pairings generates additional observables through the non-scalar commutators above.
* Equations (4)–(5) relocate this issue into shape-diagonal operators; they do not evaluate the needed matrix elements.

For the fully expanded implementation, precision is not the principal unresolved cost. A coarse polynomial bit bound follows directly from the path formula. Across a complete ket construction there are \(D\) catalytic edge steps. Path denominators come from the \(1/3\) in each \(B_n\), the factors \(1/n\), and exponential factorials. Taking
\[
L=\operatorname{lcm}(1,\ldots,3D),
\]
a common denominator \(L^{3D}\) suffices. Path counts and absolute weights are bounded by \(\exp(O(D\log D))\); applying a derivative history adds at most \(D\) factors of polynomial magnitude. Thus expanded coefficients and norms have polynomial bit length. This pays arithmetic height for expansion, **not** the number of retained coefficients or an unproved compressed contraction.

The supplied down-set method remains the strongest established shape-sensitive baseline here:
\[
\operatorname{poly}(D)\,M(\lambda)^2,
\]
with its stated exact expected-time and bounded-clock TV variants. No replacement for its unrestricted-shape cost has been proved.

## 6. Remaining proof obligations and final disposition

For a new contraction to yield the requested sampler, the missing claims are concrete:

1. **Closure:** An explicit polynomial-size representation must remain closed under the commutations in (1), including arbitrary reached derivative histories. It must retain the shape dependence exposed by (5), (8), and (9).
2. **Evaluation cost:** Its entries and updates must be computable from the explicit partition—not from \(T_u\)-matrix-element, coefficient, or partition-function oracles. Singular specializations and intermediate bit growth must be bounded.
3. **Adaptive accuracy:** For a relative-estimation route, accuracy \(O(\epsilon/D)\) and per-query failure probability \(O(\epsilon/D^2)\) suffice, provided the guarantees hold conditionally at every reached history. Zero norms need certified handling, or a proved alternative additive-error budget.
4. **Sampling overhead:** Any absolute-path reweighting needs an actual acceptance, variance, or mixing bound. The calculations above neither provide nor generally preclude such a bound.

Reading the explicit partition, computing the hook normalizer, and writing a partition output are polynomial in the charged numerical degree \(D\). There is no hidden input-state preparation. If exact conditional weights were available, the supplied finite-bit rounding argument would pay the final sampling error. The unavailable resource is the unrestricted adaptive contraction itself.

**Established:** exact generic-\(u\) conjugation; explicit failure of scalar, degree-only, and simple row-lowering closures; the stated universal-linear-boundary rank obstruction; verification of the one-row absolute-path identity; and finite plus all-degree falsifiers of normalized absolute-path replacement.

**Open:** a different determinant, nonlinear polynomial transfer state, or uniformly controlled estimator giving unrestricted polynomial Born sampling. Failure of the constructions audited here establishes neither classical hardness nor a quantum speedup.