## 2. Native tagged presentations can have bounded-height basis elements

### 2.1 Normalize target ideals, retaining the tags

Operation 2 applies to any integral squarefree target \(J\), not just a residual ideal. Compute
\[
(w)J=M,\qquad \log NM\le \Lambda_K=O(n_K^2+\log|D_K|).
\]
Then
\[
([x],c)\longmapsto
\left([x\prod_j w_j^{c_j}],c\right)
\]
identifies the presentation with targets \(J_j\) with the presentation whose targets are the outside-\(S\) odd parts of \(M_j\).

The inverse map divides by the recorded \(w_j^{c_j}\). Tags remain formal coordinates even when normalized ideals coincide or become trivial.

Consequently, **every native \(U\)-call can use targets with**
\[
\log NJ_j\le \Lambda:=\max_i\Lambda_{F_i}.
\tag{1}
\]
Norm push-down preserves this bound.

### 2.2 Sparse tags, without computing a class group

For
\[
G_K(S;J)=
\{([x],c):\operatorname{div}_{\notin S}(x)=\textstyle\sum c_jJ_j\bmod2\},
\]
the image of the tag projection is
\[
\ker\!\left(\mathbf F_2^r\longrightarrow \mathrm{Cl}_S(K)/2\mathrm{Cl}_S(K)\right).
\tag{2}
\]

This is an existence statement used for a dimension bound; the algorithm does not construct that class group.

A crude sufficient bound is available from Minkowski and HNF counting. Every ideal class has an integral representative of norm at most
\[
2^{O(n_K)}|D_K|^{1/2}.
\]
Counting HNF lattices up to that index gives
\[
c_K:=\log_2 h_K
   \le O\!\left(n_K^2(\log|D_K|+n_K)\right).
\tag{3}
\]
No regulator lower bound or unread Friedman estimate is needed.

A subspace of \(\mathbf F_2^r\) of codimension \(c\) has a basis with tag weight at most \(c+1\): take a parity-check matrix, choose pivot columns, and use one nonpivot column at a time. Applying this to the **computed pair basis**, by binary linear algebra, yields:

- a basis of the zero-tag kernel;
- lifts of a sparse basis of the tag image.

After forming the required products, apply Operation 3. Their odd support lies in \(S\) and at most \(c_K+1\) bounded-norm targets. Thus every native output representative has height bounded by \(W\), independently of \(r\).

The same argument applies to the first-child local-norm intersection \(H\). If it imposes \(\ell_K\) binary local conditions, its tag-image codimension is at most \(c_K+\ell_K\). Hence its basis pairs can also be made sparse before the norm lifts.

In particular,
\[
\dim H\le r+D_K,\qquad
D_K:=\dim K(S,2)\le n_K+|S_K|+c_K.
\tag{4}
\]

Dense intermediate products are still expanded and charged. Their size is polynomial in the batch size and \(W\); the reset occurs **before** they become inputs to a conic call.

---

## 3. The crucial witness-shortening deduction

### Lemma: shorten a known ternary witness

Given a nonsingular ternary over an original tower field \(K\), and an expanded nonzero isotropic vector, one can produce another expanded isotropic vector satisfying
\[
\mathcal H_K(\text{new vector})
 \le C\bigl(\mathcal H_K(\text{input coefficients})+W\bigr),
\tag{5}
\]
where \(C\) is absolute.

Its runtime is polynomial in the supplied witness size and coefficient data, with integer factorization charged. The bound in (5) is independent of the supplied witness’s height.

This is **not** a method for finding the first witness.

### Construction

Write the equation as
\[
x^2-dy^2=az^2,\qquad d,a\in K^\times.
\tag{6}
\]

If \(d\) is a square, a binary zero is obtained by an exact field square-root computation. Otherwise put
\[
L=K(\sqrt d).
\]
For an existing witness, \(z\ne0\), so
\[
\beta=\frac{x+y\sqrt d}{z},\qquad N_{L/K}\beta=a.
\]

Let \(S^\ast\) contain:

- all dyadic primes of \(K\);
- all numerator and denominator primes of \(a,d\).

Outside \(S^\ast\), the extension is unramified and the norm parity is zero. Thus the outside-\(S^\ast\) parity of \(\beta\) is the pullback of a lower parity ideal \(R\):

- at split primes the two parities agree;
- at inert primes there is only one parity to record.

Factor the expanded \(\beta\) to construct \(R\). Apply Operation 2 in \(K\):
\[
(w)R=M,\qquad \log NM=O(n_K^2+\log|D_K|).
\]
Replace \(\beta\) by \(w\beta\). Its norm class is unchanged, and its outside-\(S^\ast\) odd support is now the pullback of \(\operatorname{odd}(M)\).

Apply Operation 3 **in \(L\)**:
\[
\beta_0=w\beta\,\gamma^2.
\]
It is integral and has bounded archimedean size. Its odd ideal satisfies
\[
\log NJ_{\beta_0}
 \le 2\sum_{\mathfrak p\in S^\ast}\log N\mathfrak p+2\log NM.
\tag{7}
\]

Crucially, the **true field discriminant**, not the discriminant of a poorly scaled defining order, obeys
\[
\log|D_L|
 \le 2\log|D_K|+3n_K\log2
       +\sum_{v_{\mathfrak p}(d)\ {\rm odd}}\log N\mathfrak p.
\tag{8}
\]
The last sum is at most \(2\mathcal H_K(d)\).

Operation 3 and (7)–(8) therefore give
\[
\mathcal H_L(\beta_0)
 \le C_1\bigl(\mathcal H_K(a)+\mathcal H_K(d)
                    +n_K^2+\log|D_K|\bigr).
\tag{9}
\]

Write
\[
\beta_0=x_0+y_0\sqrt d.
\]
Since \(N\beta_0/a\) is a square in \(K\), compute
\[
z_0=\sqrt{N\beta_0/a}.
\]
Trace/component extraction and the height identity for a square root now prove (5). The new vector is \((x_0,y_0,z_0)\).

### Paying for the auxiliary field

This auxiliary field is never used as a recursive conic field.

An implementable preparation is:

1. clear denominators by replacing \(d\) with \(m^2d\);
2. form the explicit rank-\(2n_K\) order \(O_K[\sqrt{m^2d}]\);
3. factor its integer discriminant;
4. compute its maximal order by \(p\)-maximalization at those factored primes;
5. construct basis conversions and certified embeddings.

The initial order discriminant has polynomial bit length in the current coefficient data. The standard \(p\)-radical/multiplier-order procedure uses finite-field algebra and HNF; each strict enlargement reduces the discriminant by a factor divisible by \(p^2\), giving a polynomial iteration bound. No unit, class-group or principalization oracle is involved.

Temporary preparation sizes may contain degree factors. They are polynomial-sized workspaces, not recursively propagated height bounds. Equation (8), using the maximal-order discriminant, is what controls the shortened output.

**This postprocessor is what removes the adaptive height-slope recurrence.** Merely resetting the three coefficients would not do so.

---

## 4. ERH gluing with one coefficient tag per form

Consider a ready batch of promised isotropic quaternaries over one original field \(K\).

### 4.1 Normalize coefficients and validate the prime theorem application

For each form \(q\), square-normalize its four coefficients using Operation 3, recording the coordinate rescalings. Let \(S_q\) contain \(S_K\), dyadic primes, and all primes of the resulting coefficients. If the incoming coefficient height is \(H\), then
\[
w_q:=\sum_{\mathfrak p\in S_q}\log N\mathfrak p
      \le C(H+W).
\tag{10}
\]

For
\[
q=\langle a_1,a_2,a_3,a_4\rangle,\quad
d_1=-a_1a_2,\quad d_2=-a_3a_4,
\]
use the stipulated modulus
\[
\mathfrak m_0=\prod_{\mathfrak p\in S_q}
                   \mathfrak p^{2v_{\mathfrak p}(2)+1},
\]
with all real places.

The quadratic characters factor through this modulus. The subgroup
\[
H_0=\ker\bigl(\mathrm{Cl}_{\mathfrak m}(K)
                    \longrightarrow\mathrm{Gal}(K(\sqrt{d_1},\sqrt{d_2})/K)\bigr)
\]
has index at most four.

The supplied Wesolowski theorem therefore applies under **full ERH for the relevant Hecke \(L\)-functions**. Its displayed constants are dominated by
\[
X_q=(32L_q)^2,\qquad
L_q=2+n_K+\operatorname{bits}|D_K|
                  +\operatorname{bits}N\mathfrak m_0.
\tag{11}
\]
Use primes of norm at most \(X_q\), avoiding the excerpt’s strict-versus-nonstrict endpoint issue. If \(H_0\) is trivial, the generation assertion is vacuous and the replacement argument still works.

There is no construction of a ray group or class field.

### 4.2 Replace many coefficient-prime tags by one tag

At every place of \(S_q\), choose a local squareclass \(b_v\) satisfying the two binary norm conditions
\[
(b_v,d_1)_v=(a_1,d_1)_v,\qquad
(b_v,d_2)_v=(-a_3,d_2)_v.
\tag{12}
\]
This is local squareclass linear algebra. At most two character equations occur at each place.

Define one parity ideal
\[
J_q=\prod_{\substack{\mathfrak p\in S_q\setminus S_K\\
                         v_{\mathfrak p}(b_v)\ {\rm odd}}}\mathfrak p.
\tag{13}
\]

Why is fixing these local choices legitimate? A nonsingular isotropic quadric with a rational point is rational and has weak approximation. Local points realizing the chosen nonzero common values can therefore be approximated by a global point. This is only an **existence argument** using the isotropy promise; no global point is requested computationally.

For the resulting unknown common value \(b_0\), let \(A\) be its odd ideal outside \(S_q\). Every prime dividing \(A\) splits in both quadratic extensions. The prime-generator theorem gives
\[
A=(\alpha)\prod_{\mathfrak p\in P_q}\mathfrak p^{e_{\mathfrak p}}\,C^2,
\qquad e_{\mathfrak p}\in\{0,1\},
\tag{14}
\]
where \(P_q\) consists of the allowed small split primes and \(\alpha\) is ray-principal.

The modulus ensures that \(\alpha\) is a local square at every finite place in \(S_q\), and positive at every real place. Thus \(b_0/\alpha\):

- has the chosen local classes at \(S_q\);
- has outside-\(S_K\) parity
  \[
  J_q+\sum_{\mathfrak p\in P_q}e_{\mathfrak p}\mathfrak p.
  \]

Accordingly, one calls tagged \(U\) with **one target \(J_q\)** plus small-prime targets, then imposes (12) and the appropriate tag restrictions.

This avoids a factor proportional to the number of coefficient primes for every quaternary.

### 4.3 Shared small-prime presentation

For all currently ready quaternaries, enumerate rational primes through
\[
X_{\rm batch}=\max_q X_q.
\]
Decompose them in \(K\), retaining all degree-one prime ideals outside \(S_K\). This gives a common pool of at most
\[
P_{\rm batch}\le n_K X_{\rm batch}
\tag{15}
\]
ideals.

Each form has its own allowed-column mask:

- outside its \(S_q\);
- both residue-square tests pass.

Normalize all \(J_q\) and pool ideals by Operation 2, retaining their scalar corrections. Build **one** common tagged \(U\)-presentation.

For form \(q\), impose:

- its own coefficient tag equals \(1\);
- all other coefficient tags and unrelated request tags equal \(0\);
- disallowed prime tags equal \(0\);
- the local equations (12), corrected by the recorded target-rescaling scalars.

These are binary affine equations on the common pair space.

### 4.4 Keep the selected common value’s height linear

Using every small prime in a returned product would give an unnecessarily quadratic height bound. Instead, project the affine system to its prime-tag variables.

By (2), the tag-image codimension is at most \(c_K\). Adding the local conditions increases codimension by at most
\[
2|S_q|+2r_1.
\]
Hence Gaussian elimination can choose a solution with at most
\[
\rho_q=c_K+2|S_q|+2r_1
\tag{16}
\]
nonzero prime tags.

The reset common value \(b\) consequently has odd-support weight at most
\[
O(W)+w_q+\rho_q\log X_q.
\tag{17}
\]

There is an elementary uniform bound
\[
\rho_q\log X_q\le Cw_q+\operatorname{poly}(n_K,\log|D_K|,c_K,W_{S_K}).
\tag{18}
\]
Indeed, if \(t=|S_q|\), sorting the prime ideals by norm gives
\[
w_q\ge t\log(t/n_K)-t.
\]
For large \(w_q\), split into \(t\le\sqrt{w_q}\) and \(t>\sqrt{w_q}\); both give \(t\log X_q=O(w_q)\). The remaining bounded range is absorbed by a fixed polynomial in the field data.

After Operation 3,
\[
\boxed{\mathcal H_K(b)\le C(H+W).}
\tag{19}
\]

Now solve the two ternaries
\[
a_1x_1^2+a_2x_2^2=bz_1^2,\qquad
-a_3y_1^2-a_4y_2^2=bz_2^2.
\]
They are charged \(C_K\)-calls. Cross multiplication,
\[
(x_1z_2,x_2z_2,y_1z_1,y_2z_1),
\]
glues their answers without unnecessary inversions. Binary-isotropic and zero-coordinate cases are handled directly.

---

