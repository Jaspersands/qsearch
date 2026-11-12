## Disposition

**The ideal inverse-branching boundary observation is correct. It does not, by itself, give efficient prefix-amplitude evaluation.** The construction does permit a useful polynomial-dimensional description of the **ideal spectral dynamics within one branching block**, conditional on the remaining path records. What is missing is an efficient conversion of those spectral coordinates into occupation amplitudes—and, for the actual compiled circuit, control of amplitudes at prefixes of the native simulation and arithmetic circuits.

Applying the actual BGL algorithm therefore gives a precise conditional classical sampler, described below, but **the supplied material does not pay its amplitude subroutine for unrestricted \(\lambda\)**. This is not a hardness result, and it does not invalidate the reviewed quantum transform.

All statements below are deductions from the supplied material or explicitly identified obligations. No computation or external source lookup was performed.

---

## 1. What the remaining records determine

Write a removal chain as
\[
\lambda^{(D)}=\lambda,\qquad
\lambda^{(j-1)}=\lambda^{(j)}-r_j,\qquad
c_j=c(r_j).
\]
After the ideal \(C\)-down circuit, the path amplitude is
\[
\prod_{j=1}^{D}\sqrt{q_{\lambda^{(j)},r_j}}.
\]

Now execute the ideal inverse circuits through \(B_n^\dagger\). Let
\[
h=(c_D,\ldots,c_{n+1})
\]
denote the unconsumed records. Starting from the explicit input \(\lambda\), a valid \(h\) determines every removal down to a unique shape
\[
\nu(h)=\lambda^{(n)}\subseteq\lambda.
\]
This uses uniqueness of a removable corner of a specified content within a fixed shape—not uniqueness of content globally.

Define
\[
Q(h)=\prod_{j=n+1}^{D}q_{\lambda^{(j)},r_j}.
\]
Then the exact boundary state is
\[
|\Psi_n\rangle
=
\sum_{h\text{ valid}}
\sqrt{Q(h)}\,
|\widehat J_{\nu(h)}\rangle\,|h\rangle\,|0_{\mathrm{erased/work}}\rangle.
\tag{1}
\]

**Proof.** For each fixed upper history \(h\), its remaining lower-path superposition is exactly the \(B_n,\ldots,B_1\) downward image of \(\widehat J_{\nu(h)}\), with the same positive branching amplitudes as the \(C\)-down circuit. Applying the corresponding inverse restores \(\widehat J_{\nu(h)}\) and erases those lower records. Different upper histories remain orthogonal.

Thus, for an occupation partition \(\mu\vdash n\),
\[
\langle \mu,h,0|\Psi_n\rangle
=
\sqrt{Q(h)}\,
a_{\nu(h)}(\mu),
\qquad
a_\nu(\mu)
=
\theta_\mu(\nu)
\sqrt{\frac{z_\mu\,3^{\ell(\mu)}}{H_\nu}}.
\tag{2}
\]

### What is efficiently computable here

For a specified history:

* validity and the resulting subshape are computable by polynomial-time shape operations;
* each \(q\) is a product/quotient of \(O(D)\) integers of magnitude \(O(D)\);
* the numerator and denominator of \(Q(h)\) have \(O(D^2\log(D+1))\) bits;
* \(H_\nu\), \(z_\mu\), and \(3^{\ell(\mu)}\) have \(O(D\log(D+1))\) bits.

Products, divisions, and square roots to \(b\) output bits therefore cost \(\operatorname{poly}(D,b)\) bit operations. For example, a deliberately loose schoolbook bound for all these known scalar calculations is
\[
O\!\left(D^3\bigl(D^2\log(D+1)+b\bigr)^3\right).
\]

**The unpaid quantity in (2) is \(\theta_\mu(\nu)\), not the path weight or normalization.** At \(n=D\), the history is empty and (2) is precisely an arbitrary normalized Jack occupation coefficient of the original input.

This establishes a reduction to one coefficient per ideal boundary query. It does **not** establish a polynomial-time algorithm for that coefficient.

Also, (1) is an ideal identity. For the compiled circuit, the supplied hybrid bounds give a global small-norm error at these boundaries. They do not give a uniform conditional error after selecting an arbitrarily rare record \(h\).

---

## 2. How far the ideal within-block contraction goes

There is more exploitable structure than just (1), but it stops short of an amplitude algorithm.

Put
\[
u_\nu=|\widehat J_\nu\rangle|\ell=0\rangle,\qquad
b_{\nu,a}(m,\ell)=\langle m,\ell|v_{\nu,a}\rangle.
\]
The reviewed cyclic decomposition gives
\[
Z_\nu=\operatorname{span}\{v_{\nu,a}:a\in A_\nu\},
\]
with
\[
L|_{Z_\nu}=\operatorname{diag}(a:a\in A_\nu),\qquad
u_\nu=\sum_{a\in A_\nu}\sqrt{\tau_{\nu,a}}\,v_{\nu,a}.
\]
Consequently, in this spectral basis,
\[
P_0|_{Z_\nu}=t_\nu t_\nu^\dagger,
\qquad
(t_\nu)_a=\sqrt{\tau_{\nu,a}}.
\tag{3}
\]

The corner data therefore specify small matrices for:

* ideal evolution \(e^{itL}\);
* ideal content projectors;
* marker-zero reflection;
* their products \(W_c\);
* the ideal controlled QPE operations built from those operators.

For a fixed \(c\), the polar dynamics on the promised input lie in the plane spanned by \(u_\nu\) and \(v_{\nu,c}\). The scalar QPE amplitudes on that plane can be calculated using the displayed \(2\times2\) rotation and the explicitly charged QPE clock.

Within one inverse \(B_n\) block, fixing the upper history determines a parent shape \(\sigma\vdash n\). Before the recorded corner is erased, only children \(\sigma-r\) occur. Thus the ideal spectral calculation can be performed in
\[
\bigoplus_{r\in R_\sigma} Z_{\sigma-r},
\]
whose dimension is at most \(O(D^2)\), even using the crude corner bound. The phase-register dimensions are also polynomial for the stated compiler.

**This is a genuine constructive simplification:** no enumeration of the entire subshape down-set is needed to propagate these ideal abstract spectral coordinates within a fixed queried block.

### The missing change of coordinates

To answer BGL’s computational-basis query, however, one must calculate quantities such as
\[
\sum_{\nu,a}\beta_{\nu,a}\,b_{\nu,a}(m,\ell).
\tag{4}
\]
The coefficients \(\beta_{\nu,a}\) can be obtained from the small spectral calculation. The occupation overlaps \(b_{\nu,a}\) have not been paid.

Indeed,
\[
P_0v_{\nu,a}=\sqrt{\tau_{\nu,a}}\,u_\nu
\]
implies
\[
b_{\nu,a}(m,0)
=
\sqrt{\tau_{\nu,a}}\,a_\nu(m).
\tag{5}
\]
So even marker-zero Lax coefficients contain the original Jack coefficient problem.

Spectral interpolation does not presently close this gap. On \(Z_\nu\),
\[
v_{\nu,c}
=
\frac{1}{\sqrt{\tau_{\nu,c}}}
\prod_{\substack{a\in A_\nu\\a\ne c}}
\frac{L-aI}{c-a}\,u_\nu.
\tag{6}
\]
The interpolation coefficients are computable corner quantities. But evaluating an occupation coordinate of (6) requires matrix elements of powers of the occupation-sparse \(L\) against \(u_\nu\). Direct walk expansion can have \((2D+1)^{|A_\nu|-1}\) terms and still calls for Jack occupation coefficients. No polynomial compression of that expansion is supplied.

This is a failure of that evaluation method, **not a lower bound**.

### The native \(V\) is not the main obstacle

At its ideal boundary,
\[
\langle m,\ell|V|\widehat J_\sigma\rangle
=
\sqrt{\frac{(\ell+1)(m_{\ell+1}+1)}{n}}\,
a_\sigma(m+e_{\ell+1}).
\tag{7}
\]
Thus the known occupation-controlled preparation/decrement structure of \(V\) reduces these queries to ordinary Jack amplitudes and computable mode weights. The unresolved coefficient evaluation remains; \(V\) does not remove it.

Likewise, the classical-label \(C\)-down preparation admits a transparent amplitude calculation: a queried path fixes completed decisions, and the current binary-prefix rotation has computable rational conditional weights. Sampling those paths is easy, but it is not the native Born sampler—the subsequent coherent inverse cannot be replaced by measuring a path first.

---

## 3. The actual simulation prefixes do not retain the ideal cyclic invariant

BGL cannot treat a whole \(B_n^\dagger\), QPE, or Hamiltonian simulation as a constant-support gate. Doing so would make its fiber contain exponentially many computational basis strings. The algorithm must descend to the chosen bounded-support gate compilation.

The reviewed native simulation uses terms
\[
L=H_{\mathrm{diag}}+\sum_{k,\mathrm{parity}}H_{k,\mathrm{parity}}
\]
and product-formula words in their exponentials. These individual matching terms need not preserve \(Z_\nu\).

Here is an exact small algebraic falsifier of **termwise** cyclic closure. In degree two, use
\[
a=|m_1=2,\ell=0\rangle,\quad
b=|m_2=1,\ell=0\rangle,\quad
c=|m_1=1,\ell=1\rangle,\quad
d=|m=0,\ell=2\rangle.
\]
The supplied native \(L\) has edges
\[
a\leftrightarrow c:\sqrt6,\qquad
c\leftrightarrow d:\sqrt3,\qquad
b\leftrightarrow d:\sqrt6,
\]
and diagonal \(0,0,2,4\).

Its addable-content cyclic subspace for \((2)\) is generated by
\[
u_{(2)}=\tfrac12 a+\tfrac{\sqrt3}{2}b,\qquad
Lu_{(2)}=\tfrac{\sqrt6}{2}c+\tfrac{3\sqrt2}{2}d.
\]
These formulas can be checked directly: \(L^2u_{(2)}=5Lu_{(2)}+6u_{(2)}\), giving the addable eigenvalues \(6,-1\).

But the mode-2 matching term \(K\) satisfies
\[
Ku_{(2)}=\tfrac{3\sqrt2}{2}d\notin
\operatorname{span}\{u_{(2)},Lu_{(2)}\}.
\]
Therefore its rotation generically leaves that cyclic subspace.

This disproves an exact argument that *every native simulation prefix* can be tracked in the same corner-indexed space. It does not rule out a different efficient approximation or contraction algorithm.

There are two further precision issues:

1. Actual prefixes can include partially computed matching labels, arithmetic workspace, controlled rotations, and partially uncomputed QPE registers. A proposed evaluator must cover these states too.
2. Small error at complete simulation or branching boundaries is not enough for BGL’s robustness lemma. That lemma charges the **sum of prefix-state errors**, not just the final preparation error.

Thus “replace each compiled prefix by the corresponding ideal Jack/corner state” requires a new uniform error proof. The existing endpoint error allocation does not supply it.

---

## 4. Applying actual BGL Algorithm 2, with precision charged

Fix an elementary, phase-tracked compilation of the entire preparation circuit, including loading the explicit \(\lambda\):
\[
U=G_m\cdots G_1,\qquad \operatorname{supp}(G_t)\le k,
\]
where \(k=O(1)\). Let \(n\) include all data, path, phase, and arithmetic qubits.

For each step, BGL keeps the bits outside \(\operatorname{supp}(G_t)\) fixed and resamples the at most \(2^k\) strings in that fiber using the probabilities of the **entire prefix** \(G_t\cdots G_1\). This is the actual gate-by-gate rule, not a final-amplitude or marginal sampler.

### The charged circuit clock

Take preparation accuracy \(\eta=\epsilon/4\), and put
\[
N=D+1,\qquad \zeta=\frac{\epsilon}{64N}.
\]
For the reviewed polar compiler,
\[
h=\zeta/4,\qquad \xi=\zeta^2/64,\qquad
M<2^{15}\zeta^{-4}.
\]
Also
\[
M_0\in[8N,16N),\qquad L_0=\log_2M_0.
\]

A safe internal simulation accuracy for content extraction inside a polar call is
\[
\rho=\frac{\zeta}{1024ML_0}.
\]
The stated product formula then uses
\[
R=\left\lceil\frac{260(8N^2)^2}{\rho}\right\rceil.
\]
Across all stages, the number of native matching/diagonal component exponentials is bounded by
\[
O\!\left(DML_0R(2D+1)\right)
=
O\!\left(N^{15}\epsilon^{-9}L_0^2\right).
\tag{8}
\]

This is a native-component count, not an elementary gate count. Each component additionally pays reversible arithmetic and gate synthesis. The required elementary angle precision is
\[
O(\log N+\log(1/\epsilon))
\]
bits; exact corner-prefix arithmetic can use
\[
O(D^2\log N)
\]
bits. Multiplying (8) by the reviewed fixed polynomial arithmetic/synthesis overhead gives the admitted
\[
m=\operatorname{poly}(D,1/\epsilon).
\]
The excerpts do not specify a unique elementary synthesis exponent, so assigning a more precise elementary-gate power would be unwarranted.

Input loading costs \(O(D\log N)\) bit access/gates under the explicit-partition encoding. Unused qubits can be removed, giving the safe bound
\[
n=O(m+D\log N).
\]
Producing the output occupation list costs \(O(D\log N)\) bits. There is no hidden quantum input.

### A sufficient, bit-safe amplitude interface

Suppose a deterministic routine returns
\[
\widetilde a_t(x)
\quad\text{with}\quad
\left|\widetilde a_t(x)
-\langle x|G_t\cdots G_1|0^n\rangle\right|\le 2^{-b}
\tag{9}
\]
uniformly, including workspace bits. Define the implicit vector
\[
|\phi_t\rangle=\sum_x\widetilde a_t(x)|x\rangle.
\]
Then
\[
\|\phi_t-\psi_t\|\le 2^{n/2-b}.
\]
Choose, allowing a fixed extra bit for complex rounding,
\[
b=
\left\lceil \frac n2+\log_2\frac{128m}{\epsilon}\right\rceil.
\tag{10}
\]

For a current BGL fiber \(S\), query the at most \(2^k\) values
\(\widetilde a_{t-1}(z)\), \(z\in S\), and form
\[
r_t(y)=
\left|\sum_{z\in S}(G_t)_{yz}\widetilde a_{t-1}(z)\right|^2.
\tag{11}
\]
Resample proportionally to \(r_t(y)\).

Equation (11) is precisely the supplied robustness lemma’s \(R_t\), up to a global normalization that cancels in the fiber. Its total variation error is bounded by
\[
8\sum_{t=1}^{m-1}\|\phi_t-\psi_t\|
\le \epsilon/8
\]
with the above conservative constants.

This avoids silently assuming lower bounds on the probabilities of visited fibers. An arbitrary convention can be used on a zero approximate fiber; its contribution is covered by the same distributional comparison.

For a fixed algebraic finite gate set, such as a phase-tracked Clifford+\(T\) compilation, (11) involves constant-degree algebraic numbers of \(O(b)\) bit height. Zero tests and comparisons can be performed in polynomial bit time. Using
\[
b_{\mathrm{rand}}
=
\left\lceil\log_2\frac{8m\,2^k}{\epsilon}\right\rceil
\]
random bits per resampling gives at most another \(\epsilon/8\) total variation error. The preparation error contributes at most \(\epsilon/4\).

Hence a sufficient conditional runtime is
\[
T_{\mathrm{compile}}
+
O\!\left(
m\,2^k\left[
T_{\mathrm{amp}}(D,\epsilon,b)
+\operatorname{poly}\!\left(b,\log\frac m\epsilon\right)
\right]\right)
+
O(D\log N).
\tag{12}
\]

The exponentially small absolute accuracy in (9) requires only polynomially many **bits**, because \(b=O(n+\log(m/\epsilon))\). But the evaluator must actually run in polynomial time in that precision. Fixed inverse-polynomial absolute accuracy per queried coefficient is not justified by the BGL lemma.

A randomized evaluator could replace (9), but it would need a uniform success/error guarantee on adaptive queries and a paid total failure budget. “Works on typical examples” is insufficient.

### Precisely what remains unpaid

The missing routine is
\[
(\lambda,t,x,b)\longmapsto
\langle x|G_t\cdots G_1|0^n\rangle
\quad\text{to error }2^{-b},
\tag{13}
\]
for the actual compiled prefixes, in
\(\operatorname{poly}(D,1/\epsilon,b)\) bit time—or a substitute family of efficiently evaluable \(\phi_t\) satisfying the required summed norm-error bound.

Uniform all-string evaluation is a clean sufficient interface, not a necessity theorem for every possible classical sampler. A more tailored evaluator for the adaptively queried strings could also work, but needs its own rigorous error analysis.

---

## 5. A fully paid implementation exists, but gives no improvement

One can pay (13) by maintaining the full \(2^n\)-entry state vector of the elementary circuit and executing BGL’s fiber update at each gate.

With certified rounding, a safe vector precision is
\[
b_{\mathrm{vec}}
=
\left\lceil \frac n2+\log_2\frac{C m^2}{\epsilon}\right\rceil
\]
for a fixed sufficiently large constant \(C\). Accumulated vector errors then satisfy the summed-prefix requirement. This yields a complete classical sampler with costs
\[
O\!\left(m\,2^n\,\operatorname{poly}(b_{\mathrm{vec}})\right)
\]
bit operations and
\[
O(2^n b_{\mathrm{vec}})
\]
memory, plus circuit compilation and output costs.

That is an actual, oracle-free BGL implementation, but not the requested matched improvement. The stronger supplied classical baseline remains
\[
\operatorname{poly}(D,\log(1/\epsilon))\,M(\lambda)^2,
\qquad
M(\lambda)\le \exp(O(\sqrt D)).
\]
No down-set recurrence needs to be repeated to make this comparison.

---

## 6. The ground-state route does not currently close the gap

For the BGL ground-state argument, one must exhibit an encoded Hamiltonian \(\mathsf H_\lambda\) with:

1. the desired state as its **unique ground state**, including treatment of invalid encodings;
2. constant Hamming-flip locality \(k\);
3. a quantitative gap \(\gamma\);
4. efficiently evaluable amplitude ratios;
5. a bound on
   \[
   s=\max_{x\ne y:\psi(y)\ne0}
   \frac{|\langle y|\mathsf H_\lambda|x\rangle\,\psi(x)|}
        {|\psi(y)|};
   \]
6. an efficiently obtained starting point with a certified bound on
   \(\log(1/\pi(x_{\mathrm{in}}))\).

Writing
\[
N_k=\sum_{j=0}^k\binom nj,
\]
the supplied proof gives the sufficient mixing scale
\[
T=
O\!\left(
\frac{N_k s}{\gamma}
\left[
\log\frac1\epsilon+
\log\frac1{\pi(x_{\mathrm{in}})}
\right]\right).
\tag{14}
\]
Finite-precision acceptance probabilities must then have uniformly controlled error \(O(\epsilon/T)\); ratio computation, zero handling, and random-bit costs are additional charged work.

None of the following substitutes for those obligations:

* integer separation of Lax contents;
* the lower bound on \(\tau\);
* the principal-square-root branch-cut gap;
* positivity of the corner branching probabilities.

Those are not a unique-ground-state gap or a sensitivity bound for an arbitrary excited Jack state in the occupation encoding.

A circuit-history construction does not eliminate the amplitude issue. Its history amplitudes have the form
\[
\Psi(t,x)=\frac{\langle x|G_t\cdots G_1|0\rangle}{\sqrt{m+1}},
\]
so it contains exactly the same prefix amplitudes. For ordinary propagation terms, sensitivity includes ratios proportional to
\[
\frac{|(G_t)_{xy}\,\psi_{t-1}(y)|}{|\psi_t(x)|}.
\tag{15}
\]
Cancellation in the denominator is not controlled by the positive corner probabilities. Even granting a specified local history construction and a polynomial gap, the supplied material does not establish the required sensitivity bound for this route.

No gapped local parent for unrestricted excited \(\lambda\) may therefore be assumed.

---

## Final proof obligations and falsifiers

A constructive unrestricted BGL result would be established by either:

* a polynomial-bit algorithm for (13), including native controlled simulation, QPE, arithmetic, and uncomputation prefixes; or
* efficiently evaluable approximate prefix vectors with a proved bound on their **summed** norm errors; or
* a ground-state construction paying every item leading to (14), including sensitivity and amplitude ratios.

The proposed corner-collapse argument must, at minimum:

* compute the occupation coefficients in (2) and (5), rather than name them;
* handle the loss of exact cyclic closure under native matching terms;
* justify all approximate-prefix substitutions at the precision demanded by BGL.

The degree-two calculation above falsifies exact termwise cyclic invariance. It does **not** falsify efficient classical sampling. Conversely, finite successful coefficient evaluations or small-degree prefix contractions would not establish the required uniform algorithm.

**Established:** the ideal boundary identity, polynomial-bit evaluation of its path factors, a polynomial-dimensional ideal spectral calculation within a queried block, and the explicit conditional BGL sampler.

**Not established:** a polynomial-time unrestricted prefix-amplitude evaluator, a qualifying ground-state route, a new unrestricted classical sampling improvement, or any classical hardness or quantum separation.