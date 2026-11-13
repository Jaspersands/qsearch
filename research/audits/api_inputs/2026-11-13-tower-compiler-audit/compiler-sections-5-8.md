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

