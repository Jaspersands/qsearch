## Disposition

**At the level of the four-operation contract, I obtain a closing constructive recurrence.** Two additional deductions are essential:

1. **A gluing problem needs only one coefficient-support tag**, rather than one tag for every coefficient prime. The small-prime tags can be shared across an entire ready batch.
2. **An already computed ternary witness can be shortened using Operations 2 and 3.** This is a postprocessor, not a conic solver. It prevents the adaptive \(E/C/E\) stages from repeatedly composing an uncontrolled witness-height bound.

The second deduction uses a quadratic field only to shorten an **existing** witness. Its order, basis and embeddings are constructed and charged. No \(U\), conic or isotropy call is made over that auxiliary field. Thus it is not the prohibited discriminant-extension cycle.

What follows is an implementable proof-level schedule, not an executed implementation. I use the supplied Wesolowski excerpt, the stipulated bit interfaces of Operations 1–3, and the supplied fixed-rank descent identities. I do not treat the advisory reports’ complexity conclusions as established.

---

## 1. Accounting conventions

Write
\[
n_i=[F_i:\mathbf Q]=2^i,\qquad S_i=\{\mathfrak p\subset F_i:\mathfrak p\mid S_{\mathbf Q}\}.
\]

Let \(B\) include all supplied field, order, basis, embedding, tower-conversion and support data. All elements below are expanded, not compact circuits.

For height propagation, use the **extensive absolute height**
\[
\mathcal H_K(x)=[K:\mathbf Q]\,h(x).
\]
For a fixed-rank tuple, sum these heights.

This choice matters:

- \(h(x^{-1})=h(x)\);
- multiplication and addition have additive height bounds;
- a relative quadratic norm satisfies
  \[
  \mathcal H_F(N_{L/F}x)\le \mathcal H_L(x);
  \]
- extracting the two \(F\)-components of \(x\in L=F(\theta)\) uses
  \[
  \frac{x+\tau x}{2},\qquad \frac{x-\tau x}{2\theta},
  \]
  so it introduces a constant height factor plus charged tower data—not a factor \([F:\mathbf Q]\) at every level.

Conversion to expanded coordinates is charged separately. In the supplied integral basis,
\[
\ell_K(x)\le 2\mathcal H_K(x)+\kappa_K+O(1),
\]
where \(\kappa_K\) accounts for the inverse embedding matrix and basis conventions. These field-dependent quantities are bounded by a polynomial in the charged data.

Below, \(W=\operatorname{poly}(N,B)\) is one fixed, sufficiently large budget covering:

- all original-field discriminants, basis constants and tower radicals;
- \(S_i\)-support weights;
- the ideal-reset bounds;
- the class-number counting bounds used below;
- all field-only additive height terms.

It does **not** depend on a growing batch size or on a recursively returned witness.

---

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

## 5. One dependency-respecting batch schedule

Let
\[
\mathrm{Batch}_i(r,m,k)
\]
mean a ready collection consisting of:

- a tagged \(U_{F_i}\) request with \(r\) targets, possibly absent;
- \(m\) ternary requests;
- \(k\) quaternary requests.

Only ready inputs are admitted. In particular, a final Kutas quaternary is not prepared before the middle witness exists.

### Part A: common \(U\)-preparation

Normalize targets and prepare the \(k\) gluing requests as in §4. Let
\[
r'=r+k+P_i.
\]

Build one aggregate \(U_{F_i}\) with these \(r'\) targets:

1. **First child**
   \[
   \mathrm{Batch}_{i-1}(r',0,0)
   \]
   on the norm-parity targets.

2. Intersect local norms, make the resulting pair basis sparse, and reset its representatives. Its size satisfies
   \[
   s\le r'+D_{i-1}.
   \]
   Submit the \(s\) relative norm conics as
   \[
   \mathrm{Batch}_{i-1}(0,s,0).
   \]

3. From each returned witness form \(\beta\), factor it, construct the residual parity ideal, and apply Operation 2. Also apply Operation 3 to the adjusted \(\beta\); its odd support is now bounded by the sparse input tags and the reset residual.

   Submit the second child
   \[
   \mathrm{Batch}_{i-1}(s,0,0).
   \]

4. Reconstruct the pair basis, compute the coordinates of \(([d_i],0)\), remove precisely that kernel, and sparsify/reset the resulting basis. Record all coordinate transformations.

Extract the original \(U\)-request by tag restriction. For each quaternary, solve its affine gluing system and obtain its reset \(b\).

### Part B: the adaptive ternary stages

The quaternaries contribute two ternaries each. Set
\[
t=m+2k.
\]

For these \(t\) ternaries:

5. Prepare their first transfer restrictions and submit
   \[
   \mathrm{Batch}_{i-1}(0,0,t).
   \]

6. Only after those answers, prepare the middle Pfister/conic stages and submit
   \[
   \mathrm{Batch}_{i-1}(0,t,0).
   \]

7. Only after those answers, prepare the final embedding quaternaries and submit
   \[
   \mathrm{Batch}_{i-1}(0,0,t).
   \]

8. Reconstruct each ternary witness and run the shortening routine of §3. Then reconstruct the original quaternary witnesses and undo coefficient rescalings.

There are at most **six lower-field batches**: three from Part A and three from Part B.

At \(i=0\), tagged \(U_{\mathbf Q}\) is elementary. Ternaries use the fixed-rank rational factoring backend; quaternaries use the same gluing construction plus two rational ternaries. There is no number-field conic oracle at a leaf.

### Validation of the fixed-rank count

The supplied first-stage improvement checks algebraically: for a split quaternion,
\[
\lambda_*\langle\alpha,\beta,-\alpha\beta\rangle\simeq3\mathbb H,
\]
and every four-dimensional restriction meets a maximal three-dimensional isotropic subspace. The middle form is a split quaternion norm form and hence one base ternary. The last form is the stated embedding quaternary.

Thus the generic \(E/C/E\) sequence is legitimate; early zero-divisor branches only remove work.

No step solves an \(E\)-instance by asking for a conic over its discriminant extension.

---

## 6. The recurrences now close in the original input

### 6.1 Stable interface heights

The simultaneous induction is ordered as follows:

1. construct \(U_i\) using \(U_{i-1}\) and \(C_{i-1}\);
2. construct \(C_i\) using \(E_{i-1},C_{i-1},E_{i-1}\), then shorten;
3. construct \(E_i\) using \(U_i\) and two \(C_i\)’s.

The shortening lemma gives one universal output constant for \(C_i\), independent of \(i\):
\[
\mathcal H(C_i\text{ output})\le C_C(H+W).
\tag{20}
\]
Equation (19) and the two shortened ternaries give
\[
\mathcal H(E_i\text{ output})\le C_E(H+W).
\tag{21}
\]

The fixed-rank wrappers use a constant number of field operations and fixed-size linear systems. Therefore every child’s **stable input** satisfies
\[
H_{\rm child}\le C_\ast(H_{\rm parent}+W)
\tag{22}
\]
for an absolute \(C_\ast\).

Consequently,
\[
H_{\max}\le C_\ast^{h+1}W
          =O\!\left(WN^{\log_2 C_\ast}\right).
\tag{23}
\]

This is the required original-input bound. It is not a polynomial-per-level assertion.

Temporary products used in basis changes, target corrections and resets may have size polynomial in the current payload. They are explicitly expanded and charged, but are reset before becoming recursive coefficient inputs.

### 6.2 Batch and payload counts

There are at most
\[
K_{\rm batches}\le 1+6+\cdots+6^h=O(N^{\log_2 6})
\tag{24}
\]
batch nodes.

Let \(M_d\) be the sum of \(r+m+k\) over all batches at recursive depth \(d\). The six child payloads total at most
\[
\begin{aligned}
r'+s+s+3t
&\le 3r+3m+9k+3P_i+2D_{i-1}.
\end{aligned}
\]
Thus
\[
M_{d+1}\le9M_d+6^d(3P_{\max}+2D_{\max}).
\tag{25}
\]

By (11), (15) and (23),
\[
P_{\max}\le O\!\left(N(H_{\max}+W)^2\right)
          =\operatorname{poly}(N,B).
\]
Also \(D_{\max}=\operatorname{poly}(N,B)\) by (3)–(4). Hence
\[
\sum_{d=0}^h M_d
 =O\!\left(N^{\log_2 9}(P_{\max}+D_{\max}+1)\right)
 =\operatorname{poly}(N,B).
\tag{26}
\]

This pays for all adaptive stages and all added targets. It does not count a growing batch as a free call.

---

## 7. Expanded bit costs, coordinates and output

### Paid operations

| Work | Count/bound |
|---|---|
| Aggregate native \(U\)-constructions | At most \(K_{\rm batches}\) |
| Relative norm conics inside \(U\) | Included in the payload bound (26) |
| Fixed-rank ternary and quaternary jobs | Included in (26) |
| Auxiliary fields for witness shortening | At most one per ternary job; degree at most \(2N\); no recursive calls there |
| Small-prime enumeration/decomposition | At most polynomially many primes through \(X_{\max}\); cache by original field |
| Target and residual resets | Polynomial in aggregate payload |
| Coefficient, common-value and basis resets | Polynomial in aggregate payload |
| Kernel-coordinate evaluations | One per aggregate \(U\), plus recorded basis-view transformations |
| Integer factorizations | All coefficient-support, principal-ideal, residual, reset and auxiliary-order-discriminant factorizations; polynomially many polynomial-bit queries |

For an expanded element \(x=A/q\) in degree \(n\), a support-covering factorization query is
\[
q\,|N(A)|.
\]
If its coordinate bit height is \(\ell\) and multiplication-table height is \(\mu\), its bit length is bounded by
\[
(n+1)\ell+n\mu+O(n\log n).
\tag{27}
\]
Degrees are at most \(2N\), and all current expanded sizes are polynomial by (23), (26) and the reset interfaces. Thus the **total factorization-query bit mass**, not merely the query count, is polynomial.

Ordinary ideal HNF, relative norms, residue-square tests, Hilbert symbols, binary linear algebra and exact field arithmetic are charged at their current expanded sizes.

### Inversions and common denominators

An inversion is an \(n\times n\) rational linear solve. Its temporary arithmetic cost is polynomial in the expanded operand and field data. The intrinsic identity \(h(x^{-1})=h(x)\) prevents that implementation bound from being multiplied into the next level’s height estimate.

In coordinate recursion, if \(mx\) is integral in a quadratic extension and \(Nx=\sigma^2\), then
\[
(m\sigma)^2=N(mx)
\]
is integral. Integral closedness gives \(m\sigma\in O_F\). Thus the square root needs denominator dividing \(m\), not a new absolute-degree power of \(m\).

Norm/trace coordinate recursion uses the stored pairs, norm lifts and kernel coordinates. It makes no new conic calls. Its binary recursion has at most \(O(N)\) leaves per query and polynomial expanded bit cost in the query size and stored data.

### Precision

Operations 2 and 3 use their stipulated polynomial-bit rational-Gram approximations and exact LLL. Auxiliary-field embeddings and square roots are computed to certified precision determined by their explicit polynomial-bit defining data.

At dyadic places, local squareclass and Hilbert computations use finite precision sufficient for the exponent \(2v_{\mathfrak p}(2)+1\); there is no unbounded \(p\)-adic search. Real signs are certified from the charged algebraic embedding data.

### Final output height

At the root there are no outside-support tags. Operation 3 therefore gives each final representative \(x\) an odd ideal supported on \(S_h\), with
\[
\max_\sigma|\sigma x|
 \le
3\,2^{(N-1)/2}
\left(|D_{F_h}|\prod_{\mathfrak p\in S_h}N\mathfrak p\right)^{1/N}.
\tag{28}
\]
Together with the supplied basis conversion, this gives expanded polynomial coordinates.

The final basis has at most \(D_{\max}\) elements. All coordinate-map records—pair transformations, shortened norm lifts, kernel vectors and basis changes—also have polynomial total bit size. Arbitrary future coordinate queries must, of course, pay for reading their own expanded inputs and for any requested membership-support factorization.

---

## 8. Correctness and error scope

Correctness is simultaneous induction:

- **\(U\):** Operation 1’s exact pair sequence applies. Sparse basis changes and target rescalings are explicit isomorphisms. The kernel remains exactly \(\langle([d_i],0)\rangle\). No norm-image-surjectivity assumption is introduced.
- **\(E\):** the ERH prime theorem and (14) prove existence in the specified tagged affine slice; the computed complete \(U\)-basis finds it; two actual ternary solves construct the witness.
- **\(C\):** the supplied fixed-rank descent constructs a witness from strictly lower-field stages; §3 changes it to another valid witness without solving a new isotropy problem.
- **Coordinates:** recorded norm, trace, square-root and kernel operations implement the maps.

ERH is used for the gluing prime-generator theorem, not for the LLL resets or the witness-shortening lemma. The hypothesis is the full one specified in the contract.

If the factorization interface is exact, residual randomness can be confined to verified finite-field/rational backends with proved polynomial expected bounds. Restarting capped runs gives constant success probability per attempt; with the now-proved polynomial call bound \(Q\), use
\[
O(\log(Q/\eta))
\]
attempts per randomized task. LLL precision itself need not be randomized.

No quantum state preparation is assumed. This is a classical reduction with explicitly prepared integer query strings. Substituting a quantum factoring implementation would require paying its preparation, verification and error budget; it would not establish an advantage beyond factoring.

---

## 9. Audit obligations and falsifiers

The following are the material checks an implementation must satisfy.

1. **Witness shortening must use the original coefficient support \(S^\ast\), not the support of the returned witness.** Otherwise (7) would not erase witness-height dependence.
2. **Auxiliary maximal-order preparation must be paid.** Using the large defining-order discriminant in place of the true field discriminant in the output-height argument would also lose the linear bound.
3. **The common \(U\)-presentation must retain tags and scalar corrections.** Forgetting a tag with value class \(1\) invalidates the affine slices and kernel accounting.
4. **Prime-tag sparsity must be enforced after projecting the full affine pair system.** Merely returning an arbitrary linear-system solution does not prove (19).
5. **Every Kutas reconstruction branch must accept the returned valid point or take its documented zero-divisor exit.** Division-by-zero branches cannot be ignored.
6. **The schedule must respect preparation dependencies.** In particular, the middle and final stages cannot be prebatched using coefficients that do not yet exist.
7. **All factorization and LLL inputs must be expanded.** A compact expression is not a paid principal-ideal factorization interface.

Concrete falsifiers include:

- a correctly represented norm witness whose outside-\(S^\ast\) mismatch does not pull back;
- a failure of the shortened-witness bound (9) with correctly computed maximal-order data;
- a valid promised quaternary for which the complete tagged affine system is inconsistent despite the certified ERH cutoff and correct local masks;
- an execution whose child payload exceeds (25), or whose stable child coefficients violate (22).

Such a failure would invalidate a lemma or this implementation analysis. It would **not** establish a lower bound, classical hardness, or a quantum speedup.

### Bottom line

The original adaptive height composition is avoidable: shorten **known norm witnesses**, not just coefficients. Together with one-tag gluing, sparse prime selection and sparse native tag bases, this yields

\[
\boxed{
\text{polynomially many jobs}
\quad+\quad
\text{polynomial total expanded bit mass in the original }N,B.
}
\]

Thus, within the stated operation contract and under its full ERH hypothesis, the proposed schedule gives an end-to-end factoring reduction without a conic oracle, unit/class oracle, supplied-prime oracle, or discriminant-extension recursion cycle.