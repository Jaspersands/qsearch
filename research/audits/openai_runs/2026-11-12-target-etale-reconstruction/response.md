## Verdict

**The finite-étale-order repair works under the stated effective input promises.** In particular, the earlier \(p\)-scaled-encoding counterexample no longer obstructs reconstruction: it changes an integral presentation, not the rational finite étale algebra or its unique unramified \(\mathbf Z_p\)-model.

Two statements need precise interpretations:

1. The reconstructed algebra is
   \[
   A=(\overline{\mathbf Q}^{\,S})^{G_{\mathbf Q}},
   \qquad
   A\otimes_{\mathbf Q}\overline{\mathbf Q}\simeq
   \overline{\mathbf Q}^{\,S},
   \]
   **not generally the split algebra \(\mathbf Q^{|S|}\)**.
2. Operation maps extend over the **\(p\)-local maximal orders and their tensors**. A globally computed \(p\)-maximal order need not be preserved integrally at other primes. Transported rational coefficients need only have denominators prime to \(p\).

These require no new geometric promise. Below is a complete quotient-first implementation and proof.

I retain as assumptions—not as conclusions of finite tests—the genuine presented frame/evaluation/descent data, the actual globally stable \(E\), complete auxiliary torsion and compatible lifts, effective closed-coordinate height and avoidance bounds, the charged good auxiliary model/RR interface, and unramifiedness of \(E\) at \(p\). Also \(p\ne\ell\), as required by the stated final correction.

Put
\[
s=|\Gamma|,\qquad M=\ell^R,\qquad N=sM.
\]
All are polynomial in numerical \(\ell\) for fixed \(n,r,R\).

---

## 1. Auxiliary choices can be scheduled without circularity

### Basepoint and prime

Freeze the **entire list**
\[
a_k=a_0+pk,\qquad 0\le k\le L,
\]
before choosing \(P\). Choose the final \(k\) only after reduction at \(P\).

Enlarge the known avoidance bound to include branch values, the excluded affine charts, and \(a=0\) if the admitted height statement requires nonzero \(a\). Choose \(P\) larger than:

- this avoidance bound;
- \(2g_{\max}-1\);
- the uniform bad-\(c\) and bad-\(u\) bounds below;

and exclude \(p,\ell\), the required deck-order primes, and the explicit model certificate.

The fixed normalization and fixed-pole RR spaces can be certified before selecting the final \(a_k\). The \(b\)- and torsion-dependent choices below use **residue rank tests and unit pivots**, rather than a subsequently invented denominator that \(P\) must avoid. If the supplied fixed-data certificates depend on \(a_k\), there are only polynomially many candidates to process.

A polynomial-bit nonzero certificate integer excludes only polynomially many primes. An elementary small-prime search above a polynomial numerical threshold therefore still has a polynomial numerical bound. It uses primality testing and gcds with that integer, not its factorization.

Because \(P\ne p\) and \(P>L\), the \(a_k\) are distinct modulo \(P\). At most \(L\) residue base values are bad, so one works. Testing **every** point above a candidate, and every supplied class, makes the successful fibre uniformly admissible.

The origin used by the auxiliary torsion algorithm need not be this final canonical basepoint. High-degree Jacobian arithmetic can first supply \(E\); the subsequent canonical-basepoint search uses that already enumerated group.

There is also a useful simplification:

> On the quotient-first route, target unramifiedness of the frame fibre is unnecessary. Only \(E\) must be unramified at \(p\).

Thus, if an unbranched \(a_0\in\mathbf F_p\) is unavailable—for example, a small \(p\) with no rational point in the native open base—the isolated last stage may discard the target congruence and choose an auxiliary-admissible rational fibre. This introduces no target-encoding search. If the prescribed \(a_0\) exists, the proposed progression works as written.

### One auxiliary field, not a factor-degree lcm

A regular constant-\(\Gamma\) torsor over \(\mathbf F_P\) has Frobenius acting by a single element of \(\Gamma\). Its entire geometric fibre is therefore rational over \(\mathbf F_{P^s}\).

If the already-paid universal torsion/evaluation field has degree \(f_0\), an extension of degree \(sf_0\) suffices. This is a bounded product of supplied polynomial quantities, not an lcm over independently chosen support fields.

Closed divisors need no further support splitting.

---

## 2. Closed canonical extraction has a polynomial linear-algebra implementation

This is a bridge that can be proved directly from the charged RR interface.

Work componentwise. Let \(D\) be the unique effective degree-\(g\) divisor representing \(t+gb\), with
\[
h^0(t+gb)=1
\]
on the auxiliary special fibre.

If a known divisor \(H\) represents \(t+gb\), compute a nonzero
\[
f\in L(H),\qquad D=H+\operatorname{div}(f).
\]
Then, for any pole divisor \(A\),
\[
L(A-D)=f\,L(A-H).
\]
Thus the needed spaces can be computed from the class representation and ordinary closed RR; they do not presuppose split support.

Choose \(A=k\pi^{-1}(\infty)\), disjoint from \(D\), with
\[
\deg(A-D)\ge 2g.
\]
Set
\[
V=L(A),\qquad W=L(A-D).
\]
The restriction sequence gives
\[
V/W \simeq H^0(D,\mathcal O_D).
\tag{1}
\]
Indeed \(H^1(A-D)=0\), and \(A\) is trivialized along \(D\).

This gives the closed divisor algebra explicitly:

- choose a complement to \(W\) in \(V\);
- calculate products of complement representatives in \(L(2A)\);
- reduce them modulo \(L(2A-D)\);
- solve for the resulting multiplication matrices.

For \(x,y\), use sufficiently large RR spaces containing their products with the representatives; if necessary add their known pole divisors. Those poles are among the forbidden supports. All dimensions and pole degrees are polynomial.

At auxiliary precision, the quotient in (1) is free of rank \(g\). The successful residue rank tests provide unit minors, so these systems lift using unit pivots.

The canonical divisor itself lifts compatibly: degree \(g\) and residue \(h^0=1\) imply residue \(h^1=0\). The rank-one section space consequently has good base change, and a primitive section defines the flat degree-\(g\) divisor. This also explains why nonreduced support is harmless.

### The zero class is not an exception

For \(t=0\), the canonical divisor is \(gb\). The construction above uses poles at infinity, not a demand that \(D\) avoid its own origin. It never normalizes a section by requiring a nonzero value at \(b\).

Thus \(gb\) does not cause a compulsory forbidden-pole collision. Its multiplicities are retained in the quotient algebra.

All these RR calculations are componentwise. A nonzero section on a disconnected union must not be mistaken for a nonzero rational function on every component.

### Choosing \(c\) and constructing \(A,B,C\)

For each encoded divisor, a bad \(c\) arises from either:

- two distinct support points having equal \(x+cy\); or
- \(\eta=F_y-cF_x\) vanishing at a support point.

There are at most
\[
\binom g2+g
\]
bad values per divisor over the algebraic closure. The total number of encoded divisors is polynomial, so a common polynomial-sized interval contains a successful \(c\), provided \(P\) was chosen above its uniform bad-value bound.

Test this without splitting support:

- \(\eta\) is invertible in the closed quotient;
- \(1,z,\ldots,z^{g-1}\), \(z=x+cy\), form a basis.

Then obtain \(A\) from multiplication by \(z\), and solve for \(B,C\). These normalized outputs are intrinsic; arbitrary intermediate RR pivots do not affect them or their Galois equivariance.

They are \(P\)-integral, and the relevant basis determinants are \(P\)-units.

---

## 3. The all-pairs encoding genuinely descends over \(\mathbf Q\)

For each \((b,t)\), encode \(b\), the cyclotomic coordinate, and the canonical divisors based at \(R_gb\), for every fixed \(g\in\Gamma\), on the appropriate component.

The decisive identity is
\[
\sigma D_{b,t,g}=D_{\sigma b,\sigma t,g}.
\tag{2}
\]
It follows from:

- constant rational deck maps, so \(\sigma R_g=R_g\sigma\);
- actual Galois action on component classes;
- uniqueness of the canonical divisor;
- the supplied genuine component descent.

Consequently
\[
\sigma\operatorname{enc}(b,t)
 =\operatorname{enc}(\sigma b,\sigma t).
\tag{3}
\]

This uses actual scalar coordinates of the descended functions. It does **not** use coordinate vectors in an arbitrary global number-field basis.

The encoding is injective modulo \(P\):

- the included fibre coordinates distinguish different \(b\)'s;
- for a fixed \(b\), differing classes differ on some component;
- the all-\(g\) tuple includes that component;
- its canonical closed divisor determines the class.

Let the tuple length be \(m\). For
\[
\gamma_u=\sum_{j=0}^{m-1}u^j\operatorname{enc}_j,
\]
each pair of distinct tuples excludes at most \(m-1\) values of \(u\). Hence
\[
C_u=(m-1)\binom N2
\]
is a valid bound. Testing \(0,\ldots,C_u\), with \(P>C_u\), finds a separator modulo \(P\). All pairwise differences of its values are then \(P\)-units.

This is only an **auxiliary-prime** separation argument.

For completeness, the existential global degree bound is valid. The field trivializing the torsor has degree at most \(s\); the field trivializing \(E\) has degree at most \(|\mathrm{GL}_R(\mathbf F_\ell)|\). Uniqueness puts every encoded scalar in their compositum. No construction of that compositum is needed.

---

## 4. Certified rational reconstruction follows from explicit height bounds

Write
\[
\alpha_v=\gamma(\operatorname{enc}(v)),\qquad v\in S.
\]
If every scalar coordinate has absolute logarithmic height at most \(H\), and \(0\le u\le U\), a safe bound is
\[
H_\alpha
 =mH+m^2\log(U+2)+\log(m+1).
\]

Form
\[
Q(X)=\prod_{v\in S}(X-\alpha_v).
\]
Its coefficients are rational by (3). Each has height at most
\[
N(H_\alpha+\log 2).
\]

Define the Lagrange polynomials
\[
\lambda_v(X)=
\frac{\prod_{w\ne v}(X-\alpha_w)}
     {\prod_{w\ne v}(\alpha_v-\alpha_w)}.
\]
A safe bound for the height of each coefficient is
\[
H_\lambda
 =3(N-1)H_\alpha+2(N-1)\log 2.
\tag{4}
\]
The numerator bound comes from the coefficient norm of a product of linear factors; the denominator bound comes from
\(h(\alpha_v-\alpha_w)\le 2H_\alpha+\log 2\).

For an equivariant unary or binary map, interpolate its output separator value:
\[
T_f(X)=\sum_v\alpha_{f(v)}\lambda_v(X),
\]
\[
T_h(X,Y)=
 \sum_{v,w}\alpha_{h(v,w)}\lambda_v(X)\lambda_w(Y).
\]
Uniqueness and equivariance make their coefficients rational. Binary coefficients have height at most
\[
N^2(H_\alpha+2H_\lambda)+2\log N.
\tag{5}
\]
Coordinate tables use \(H\) instead of \(H_\alpha\). Boolean relation tables use output height zero. Thus a known polynomial \(K\) bounds every rational coefficient to be reconstructed.

No global field basis occurs in (4)–(5).

All interpolation denominators are \(P\)-units. Therefore all these rational coefficients are \(P\)-integral. Choose an integer bound \(T\ge e^K\) and precision \(e\) with
\[
P^e>2T^2.
\tag{6}
\]
Numerators and reduced denominators are bounded by \(T\), and denominators are prime to \(P\). Rational reconstruction is unique: two candidates would give a nonzero integer \(ab'-a'b\), divisible by \(P^e\), of absolute value at most \(2T^2\).

The local field is represented in a charged integral basis. Rational invariant coefficients lie in the base \(\mathbf Q_P\), so they can be read in that basis and reconstructed by exact integer arithmetic. Unit-pivot extraction and unit interpolation prevent an uncharged precision loss.

This constructs exactly
\[
A=\mathbf Q[X]/(Q)
\]
and all requested tables.

**Auxiliary Frobenius invariance alone would not prove rationality.** The full Galois proof (2)–(3), not a numerical local test, is what justifies reconstruction over \(\mathbf Q\).

---

## 5. The quotient \(S\to E\) is explicit and needs no global labels

The auxiliary enumeration already labels each local element as \((b,t)\), using the supplied exact class arithmetic. It therefore gives the Boolean values
\[
r(v,w)=
 \begin{cases}
 1,&t(v)=t(w),\\
 0,&t(v)\ne t(w).
 \end{cases}
\]
These values are Galois-invariant as a relation, regardless of the arbitrary local enumeration.

Interpolate and reconstruct
\[
r=\sum_{t(v)=t(w)}\lambda_v\otimes\lambda_w
 \in A\otimes_{\mathbf Q}A.
\]
This is an idempotent.

Now compute the rational linear kernel
\[
C=
\left\{
f\in A:
r(f\otimes1-1\otimes f)=0
\right\}.
\tag{7}
\]
This is a linear system with \(N\) unknowns and at most \(N^2\) equations.

After extending scalars to \(\overline{\mathbf Q}\), condition (7) says precisely that \(f\) is constant on each equivalence class. Hence
\[
C\otimes\overline{\mathbf Q}
 \simeq \overline{\mathbf Q}^{\,E},
\qquad
\dim_{\mathbf Q}C=M.
\]
It is a finite étale subalgebra of \(A\), and it is the coordinate algebra of the **actual** Galois set \(E\).

### Transporting the group operations

The binary map on \(S\),
\[
((b,t),(c,u))\longmapsto(b,t+u),
\]
is not a group law on \(S\). It is an equivariant auxiliary map whose restriction to functions in \(C\) gives
\[
\Delta:C\longrightarrow C\otimes C.
\]
Compute \(\Delta\) by applying the reconstructed map and solving in the known basis of \(C\otimes C\subset A\otimes A\).

Likewise:

- inversion and scalar maps preserve \(C\);
- actual deck action on \(t\) preserves \(C\);
- \(z_0^*f\), for \(f\in C\), is a scalar multiple of \(1\), defining
  \(\epsilon:C\to\mathbf Q\).

These are polynomial-size rational linear systems. Their identities hold because, after scalar extension, they are exactly the operations on \(E\).

This closes the relation-table/equalizer obligation without reconstructing any global Galois labels.

---

## 6. Known-prime maximalization is sufficient—and can be proved here

### Construct an initial order

Choose a rational basis
\[
1,v_2,\ldots,v_M
\]
of \(C\). Let \(D\) clear all structure-constant denominators. Then
\[
\Lambda_0=\mathbf Z\,1+\sum_{i=2}^M\mathbf Z\,Dv_i
\]
is a ring: the products of the scaled basis elements have integral coefficients in that basis.

It is a full order, with polynomial-bit structure constants and nonzero discriminant \(\Delta_0\).

### The supplied idealizer algorithm

For a current order \(\Lambda\), choose \(t>0\) with \(p^t>M\), and compute
\[
\mathfrak j/p\Lambda
 =\ker\bigl(x\mapsto x^{p^t}:\Lambda/p\Lambda\to\Lambda/p\Lambda\bigr).
\]
This kernel is the nilradical: a nilpotent element in an \(M\)-dimensional algebra has nilpotence index at most \(M\).

Then replace
\[
\Lambda\quad\text{by}\quad
\Lambda'=(\mathfrak j:\mathfrak j).
\]

Because \(p\Lambda\subset\mathfrak j\),
\[
\Lambda\subset\Lambda'\subset p^{-1}\Lambda.
\]
Every strict step has index \(p^a\), \(a\ge1\), and divides the discriminant by \(p^{2a}\). There are therefore at most
\[
\frac12v_p(\Delta_0)
\]
strict steps.

Powering uses \(O(\log p+\log M)\) exponent bits, not \(p\) operations. The kernels, idealizers and lattice changes are polynomial-size linear/HNF calculations.

All intermediate orders lie in the trace-dual lattice of \(\Lambda_0\). That lattice has quotient size \(|\Delta_0|\) over \(\Lambda_0\), giving polynomial bounds on intermediate denominators and HNF entries.

### Independent stopping proof in the needed unramified case

This avoids relying solely on the supplied proposition’s name or its referenced criterion.

Let
\[
C_p=C\otimes\mathbf Q_p,\qquad
\mathcal O=\text{its maximal }\mathbf Z_p\text{-order}.
\]
Unramifiedness of \(E\) implies that \(C_p\) is a product of unramified extensions, so \(\mathcal O\) is finite étale over \(\mathbf Z_p\).

For a local order \(B\subset\mathcal O\), its nilradical preimage is
\[
J=B\cap p\mathcal O.
\tag{8}
\]
Indeed, nilpotence modulo \(pB\) implies membership in \(p\mathcal O\). Conversely, if \(p^a\mathcal O\subset B\), sufficiently high powers of an element of \(B\cap p\mathcal O\) lie in \(pB\).

Suppose \(B\ne\mathcal O\), and take the smallest \(a\ge1\) with
\(p^a\mathcal O\subset B\). Then
\[
p^{a-1}\mathcal O\not\subset B,
\]
but, using (8),
\[
(p^{a-1}\mathcal O)J\subset p^a\mathcal O\subset J.
\]
Thus
\[
p^{a-1}\mathcal O\subset(J:J),
\]
so the idealizer strictly enlarges \(B\).

Therefore stabilization occurs exactly at \(\mathcal O\). This proves the required correctness, including products of fields and small \(p\).

### Operation maps extend \(p\)-locally

A rational algebra map sends integral elements to integral elements. Moreover,
\[
\mathcal O^{\otimes_{\mathbf Z_p}k}
\]
is finite étale and hence is the integral closure of \(\mathbf Z_p\) in
\(C_p^{\otimes_{\mathbf Q_p}k}\).

Consequently the group, scalar and deck maps extend to these orders. Transport their rational matrices into the computed \(p\)-maximal basis. Every resulting coefficient has nonnegative \(p\)-valuation, so its reduced denominator is prime to \(p\). Reduce those coefficients modulo \(p\).

There is no need for them to be integral at unrelated primes.

The result is the true finite étale Hopf algebra of the unramified specialization of \(E\).

### The old counterexample is repaired exactly

For
\[
Q=X(X-p),
\]
the initial order is generated by \(x=(0,p)\) in \(\mathbf Q^2\). Its nilradical preimage is \((p,x)\), whose idealizer contains
\[
e=x/p,\qquad e^2=e.
\]
The enlarged order is \(\mathbf Z^2\), and reduction gives \(\mathbf F_p^2\), not \(\mathbf F_p[X]/(X^2)\).

More generally, changing the original encoding by rational \(p\)-scaling does not change the descended algebra or its unique maximal unramified local order. This is a proof of encoding-independence, not an extrapolation from the two-point example.

---

## 7. Recovering the actual arithmetic Frobenius matrix

Let \(\bar C\) be the resulting rank-\(M\) finite étale \(\mathbf F_p\)-algebra. Compute
\[
F_{\mathrm{alg}}:a\longmapsto a^p
\]
in its presented basis.

This is initially an \(M\)-dimensional coordinate-algebra operator over \(\mathbf F_p\), **not yet** the desired \(R\)-dimensional operator over \(\mathbf F_\ell\).

### One splitting extension

Frobenius respects the reconstructed group operations. On the geometric elementary abelian group it therefore belongs to
\(\mathrm{GL}_R(\mathbf F_\ell)\). Its order is at most
\[
D_R=|\mathrm{GL}_R(\mathbf F_\ell)|.
\]
Find that order \(d\) by iterating the algebra Frobenius until it becomes the identity. This costs polynomial time since \(D_R\) is polynomial in numerical \(\ell\).

Then \(\mathbf F_{p^d}\) splits the whole algebra. No lcm over unrelated factors is used.

Construction of this finite field and pointwise splitting can be implemented by certifying randomized routines. For clarity, one does not need an unproved factoring oracle:

- a random monic degree-\(d\) polynomial has irreducibility probability at least \(1/(2d)\), and irreducibility is checked by powering and gcds;
- after extending scalars, the algebra is a product of copies of the field;
- random elements split it into smaller idempotent factors using quadratic-character values in odd characteristic, or the trace to \(\mathbf F_2\) in characteristic two;
- each nonsingleton factor has a constant probability of splitting, and all resulting idempotents are verified.

This gives expected polynomial time, or a polynomial capped run with explicit failure probability and **no incorrect acceptance**.

Evaluate the operation maps on the resulting geometric points. Greedily choose an \(\mathbf F_\ell\)-basis using the actual group law, recording coordinates of all \(M\) points.

For a character \(v:\bar C\to\mathbf F_{p^d}\),
\[
(\sigma_p v)(a)=v(a)^p=v(a^p).
\tag{9}
\]
Thus powering its evaluation coordinates gives its **arithmetic** Frobenius image. Express the images of the chosen group basis in that basis to obtain
\[
F_E\in\mathrm{GL}_R(\mathbf F_\ell).
\]
Evaluate the deck maps similarly.

This uses Frobenius on the finite étale coordinate algebra. It does not substitute inseparable curve-Frobenius pullback for Galois action on torsion divisors.

### A deterministic matrix-only alternative

If explicit geometric point coordinates are unnecessary, even the target splitting step can be avoided.

Compute the identity-point idempotent \(e_0\in\bar C\) from
\[
e_0\ker\epsilon=0,\qquad \epsilon(e_0)=1.
\]
For any polynomial \(u\in\mathbf F_\ell[X]\), construct the group endomorphism \(u(F)\) using the Hopf addition, scalar maps and Frobenius. Then
\[
\operatorname{rank}_{\mathbf F_p}
 m_{\,u(F)^*e_0}
 =
 |\ker u(F_E)|
 =
 \ell^{\dim_{\mathbf F_\ell}\ker u(F_E)}.
\tag{10}
\]
All quantities on the left are computed by linear algebra in \(\bar C\).

Enumerate monic irreducibles over \(\mathbf F_\ell\) of degree at most \(R\), and apply (10) to their relevant powers. There are polynomially many because \(R\) is fixed. The resulting kernel dimensions determine all elementary divisors and therefore a rational-canonical matrix for \(F_E\), up to conjugacy.

Under the supplied natural-isotypic socle promise,
\[
E\simeq N^\vee\otimes W,\qquad F_E=I\otimes F_W.
\]
The natural module has scalar commutant: commuting with its transvections forces preservation of every line and hence a scalar endomorphism. Thus the kernel dimensions in (10) are \(n\) times the corresponding dimensions for \(F_W\). Dividing them by \(n\) determines \(F_W\) as well.

This provides a deterministic matrix output up to the allowed basis conjugation, while the finite étale Hopf algebra already represents the actual group.

---

## 8. Deck conventions and the arithmetic correction

With
\[
P(g)=(R_g)_*,\qquad A(g)=R_g^*=P(g^{-1}),
\]
the required equations are
\[
\phi g^T=P(g)\phi.
\]
They compute
\[
W=\operatorname{Hom}_\Gamma(N^\vee,E)
\]
by linear algebra over \(\mathbf F_\ell\). Arithmetic Frobenius acts by
\[
\phi\longmapsto F_E\phi.
\]
It preserves this solution space because the rational deck maps commute with Galois action.

The recovered matrices are ambiguous only by a common basis change. There is no free scalar: the entire finite group, its actual operations and its actual Frobenius have been reconstructed.

Under the supplied genuine-frame comparison,
\[
W\simeq H^1(U,R^1f_*\mathbf F_\ell)(2).
\]
Therefore
\[
F_{\mathrm{arith},\,H^1}
   =p^{-2}F_W,
\qquad
F_{\mathrm{geom},\,H^1}
   =(p^{-2}F_W)^{-1}.
\]
The same statement restricts to a **genuinely supplied** parabolic socle. Rank alone would not certify that restriction.

---

## 9. Cost accounting and falsifiers

All principal dimensions and output sizes are polynomial:

- \(N=s\ell^R\) pair labels;
- polynomially many componentwise closed RR calculations;
- one auxiliary extension of polynomial degree;
- polynomial encoding length and height bounds;
- precision \(e\log P=O(K+\log P)\);
- polynomially many rational interpolation coefficients;
- an \(N\)-variable quotient linear system;
- rank-\(M\) order arithmetic, with polynomial discriminant bit length;
- target field degree at most \(|\mathrm{GL}_R(\mathbf F_\ell)|\), if point realization is requested;
- all geometric point tables, group tables and output matrices.

Target powering costs polynomially in \(B=\log p\); no loop enumerates \(p\) values. Local field presentations, numerical lifts, rational reconstruction, basis changes and output writing are all charged. No quantum state preparation or quantum oracle is used.

Useful exact falsifiers include:

- no admissible auxiliary fibre within the certified avoidance bound;
- no successful \(c\) or \(u\) within their proved bounds;
- failure of the claimed unit-pivot or closed-quotient ranks;
- rational reconstruction inconsistent with its certified bounds;
- quotient dimension different from \(\ell^R\);
- failure of the reconstructed relation/group/deck identities;
- a final \(p\)-maximal discriminant divisible by \(p\);
- transported operation coefficients with unavoidable \(p\)-denominators;
- Frobenius order exceeding the group-theoretic bound;
- failure of the expected elementary-abelian group or intertwiner equations.

These are falsifiers and implementation controls. They do not replace the genuine-frame, completeness, height or native-comparison assumptions.

## Conclusion

**The smallest previously missing last-stage bridge is now closed conditionally:** effective Galois-equivariant reconstruction followed by explicit quotienting and known-prime maximalization recovers the actual unramified finite torsion group and its arithmetic Frobenius, even when every original target encoding collides.

No target-faithful coordinate selector is needed. The native frame/model construction, the supplied parabolic identification where applicable, and full surface \(P_2\) assembly remain outside this proof. No hardness or quantum-advantage conclusion follows.