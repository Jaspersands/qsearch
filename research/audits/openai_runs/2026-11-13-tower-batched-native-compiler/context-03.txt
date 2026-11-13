## Disposition

**I do not obtain an end-to-end uniform factoring reduction.** I can, however, sharpen the remaining gate and decisively falsify the apparent closure that solves the final quaternary form by passing back to a conic over its quadratic discriminant extension.

There is also a useful positive deduction:

> **For a promised split quaternion algebra, Kutas’s six-dimensional step can be replaced by one isotropic quaternary problem over the base.** Consequently, a promised isotropic ternary over \(L=F(\sqrt d)\) reduces to at most **two specialized quaternary problems and one ternary problem over \(F\)**.

The unresolved quaternary problem is not made substantially narrower by its displayed quaternion shape. Its nonsquare-discriminant case is exactly the quadratic-embedding problem that becomes the same descended conic over \(L\). This creates an identical-instance cycle, not merely an unfavorable branching bound.

All deductions below use the supplied material and explicit algebra. No code or additional files were accessed.

---

## 1. The precise subproblems

Work in characteristic zero. Degenerate input forms can be handled by exact linear algebra, so consider nonsingular forms.

Write:

- \(\mathsf C(F)\): construct a nonzero zero of a promised isotropic ternary over \(F\).
- \(\mathsf E(F;a,b,\delta)\): construct a nonzero zero of
  \[
  E(a,b;\delta)=aX^2+bY^2-abZ^2-\delta T^2,
  \qquad a,b,\delta\in F^\times,
  \tag{1}
  \]
  promised isotropic.

These are **names for charged, potentially unimplemented subproblems**, not granted oracles.

The genuinely unresolved part of \(\mathsf E\) is \(\delta\notin F^{\times2}\). When \(\delta\) is a square, (1) is, after a coordinate rescaling and multiplication by \(-1\), a quaternion norm form.

Let \(B=(a,b)_F\), with generators \(i^2=a\), \(j^2=b\), \(ij=-ji\). For
\[
s=Xi+Yj+Zij
\]
one has
\[
s^2=aX^2+bY^2-abZ^2.
\]
Thus (1) is precisely the problem of finding either a nilpotent in \(B\), or an embedding of \(F(\sqrt\delta)\) into \(B\).

---

## 2. Proved improvement: eliminate the six-dimensional call in the promised split case

Let
\[
L=F(\theta),\qquad \theta^2=d,
\]
and let
\[
A=(\alpha,\beta)_L\simeq M_2(L).
\]
Define the \(F\)-linear coefficient map
\[
\lambda:L\longrightarrow F,\qquad \lambda(x+y\theta)=y.
\]

The pure-square form of \(A\) is
\[
q_A=\langle\alpha,\beta,-\alpha\beta\rangle.
\]
Kutas’s six-dimensional form is the transfer
\[
T=\lambda_*q_A.
\]

### 2.1 The six-form is hyperbolic, not merely isotropic

Because \(A\) is split, its traceless matrices can be written
\[
\begin{pmatrix}x&y\\z&-x\end{pmatrix},
\]
whose square is \((x^2+yz)I\). Hence
\[
q_A\simeq \langle1\rangle\perp\mathbb H_L.
\]

Now
\[
\lambda\big((x+y\theta)^2\big)=2xy,
\]
so \(\lambda_*\langle1\rangle\simeq\mathbb H_F\). Also the transfer of a hyperbolic plane over \(L\) is two hyperbolic planes over \(F\). Therefore
\[
\boxed{T\simeq 3\mathbb H_F.}
\tag{2}
\]

This deduction uses the **split promise**. It does not extend to an arbitrary quaternion algebra merely from Kutas’s indefiniteness argument.

### 2.2 A particular four-dimensional restriction is isotropic

Restrict \(T\) to the first two quaternion coordinates:
\[
R=\lambda_*\langle\alpha,\beta\rangle.
\tag{3}
\]
A three-dimensional totally isotropic subspace of the six-dimensional hyperbolic space (2) meets every four-dimensional subspace nontrivially:
\[
3+4-6=1.
\]
Consequently, \(R\) is isotropic.

Write
\[
\alpha=r_1+t_1\theta,\qquad
\beta=r_2+t_2\theta.
\]
If \(t_1=0\) or \(t_2=0\), a quaternion generator already has square in \(F\), so no isotropy call is needed. Otherwise,
\[
R\simeq
\left\langle
t_1,-\frac{N_{L/F}(\alpha)}{t_1},
t_2,-\frac{N_{L/F}(\beta)}{t_2}
\right\rangle.
\tag{4}
\]

A zero of (4) constructs the required nonzero traceless element \(u\) with \(u^2\in F\), exactly as the original six-form did.

Moreover, (4) is similar to
\[
E\left(
\frac{t_1t_2}{N(\alpha)},
-\frac{t_2}{t_1};
\frac{N(\beta)}{N(\alpha)}
\right).
\tag{5}
\]
Thus the six-dimensional step reduces to one instance of the same embedding-form family.

This is an existence-preserving reduction; the hyperbolic subspace used in its proof is **not supplied computationally**.

### 2.3 The middle four-form really is a base conic problem

After \(u^2=a\in F^\times\), the anticommuting-element step produces the form
\[
\langle 1,d-f^2,-a,-a(d-f^2)\rangle.
\tag{6}
\]
Unlike (1), this is a quaternion norm form, with square determinant. The split promise guarantees its isotropy, as in the supplied Proposition 15/Corollary 19 argument.

It therefore requires one base ternary solve, not an arbitrary quaternary solver.

Finally, Remark 21 gives (1) with \(\delta=d\).

### Resulting reduction

In the generic branch,
\[
\boxed{
\mathsf C(L)
\ \longrightarrow\
\mathsf E(F;\delta_R),\quad
\mathsf C(F),\quad
\mathsf E(F;d),
}
\tag{7}
\]
where
\[
\delta_R=\frac{N_{L/F}(\beta)}{N_{L/F}(\alpha)}.
\]
Early zero-divisor branches omit calls.

This closes the six-dimensional issue **into the quaternary issue**. It does not close the quaternary issue into lower-field ternaries.

---

## 3. Why the final specialized quaternary is a genuine gate

### 3.1 Its shape does not exclude general quaternaries of that discriminant

Let
\[
q=\langle c_1,c_2,c_3,c_4\rangle,
\qquad c_i\ne0.
\]
Multiplying by
\[
\mu=-\frac{c_3}{c_1c_2}
\]
gives
\[
\mu q=E(a,b;\delta)
\]
with
\[
a=-\frac{c_3}{c_2},\qquad
b=-\frac{c_3}{c_1},\qquad
\delta=\frac{c_3c_4}{c_1c_2}.
\tag{8}
\]
The squareclass of \(\delta\) is the determinant squareclass of \(q\).

Therefore:

> Up to similarity and coordinate changes, the final quaternion embedding forms comprise all nonsingular quaternary forms with the specified nonsquare discriminant.

There is still a useful distinction between their split-\(B\) and division-\(B\) cases. But the promise that \(B\) splits over \(F(\sqrt d)\) does **not** force \(B\) to split over \(F\).

### 3.2 The embedding form and the larger-field conic are constructively equivalent

Put \(L=F(\theta)\), \(\theta^2=\delta\), with \(\delta\) nonsquare.

**From an \(E\)-witness to a zero divisor over \(L\).**  
Given
\[
aX^2+bY^2-abZ^2=\delta T^2,
\]
put \(s=Xi+Yj+Zij\). Then
\[
w=s-T\theta
\]
is a nonzero zero divisor in \(B_L\). This also handles \(T=0\), when \(s\) is a nonzero nilpotent.

**Conversely, from a zero divisor over \(L\) to an \(E\)-witness.**  
Write a nonzero zero divisor as
\[
w=U+\theta V,\qquad U,V\in B.
\]
Expanding its reduced norm gives
\[
N(U)+\delta N(V)=0,\qquad
\operatorname{Trd}(U\bar V)=0.
\tag{9}
\]
If \(N(V)\ne0\), then
\[
s=UV^{-1}
\]
has reduced trace zero and reduced norm \(-\delta\), hence \(s^2=\delta\). Its three pure coordinates, together with \(T=1\), solve (1).

If \(V\ne0\) and \(N(V)=0\), then \(V\) is already a base-field zero divisor. If its trace is zero it is nilpotent. Otherwise, set
\[
e=\frac{V}{\operatorname{Trd}(V)}
\]
and choose a basis element \(b_0\in B\) for which
\[
e b_0(1-e)\ne0.
\]
Such an element exists; it is a nonzero nilpotent and gives a solution with \(T=0\). If \(V=0\), use \(U\) instead.

All these maps use a constant number of quaternion operations and fixed-size linear systems. They are constructive, not just existence equivalences.

A zero divisor can also be converted to a ternary-conic witness by fixed-size linear algebra: its two-dimensional left ideal is totally isotropic for the norm, and intersects the three-dimensional subspace \(\langle1,i,j\rangle\) nontrivially.

Thus
\[
\boxed{
\mathsf E(F;a,b,d)
\quad\longleftrightarrow\quad
\mathsf C_{(a,b)}(F(\sqrt d)).
}
\tag{10}
\]

### 3.3 The attempted closure returns the identical instance

Suppose the proposed implementation of \(\mathsf E(F;a,b,d)\) is:

1. solve the conic \(\langle1,-a,-b\rangle\) over \(L=F(\sqrt d)\);
2. apply the preceding back-map.

Its associated quaternion is exactly
\[
A=(a,b)_L.
\]
Both displayed generators already have squares in \(F\). Kutas’s first two steps can therefore retain those generators and reach exactly the original base quaternion \(B=(a,b)_F\). Remark 21 then asks for
\[
E(a,b;d)
\]
again.

The dependency is
\[
\boxed{
\mathsf E(F;a,b,d)
\longrightarrow
\mathsf C_{(a,b)}(L)
\longrightarrow
\mathsf E(F;a,b,d).
}
\tag{11}
\]

No degree, tower height, coefficient height, or instance parameter has decreased. This is a decisive falsification of **that closure**, independently of any complexity estimate.

---

## 4. Concrete algebraic falsifier on allowed towers of arbitrary height

For any \(m\ge0\), choose distinct primes
\[
p_1,\ldots,p_m\equiv1\pmod{12}
\]
and take
\[
F=\mathbb Q(\sqrt{p_1},\ldots,\sqrt{p_m}),\qquad
L=F(\sqrt{-3}).
\]
This is an allowed quadratic tower of total degree \(2^{m+1}\). One may take
\[
S_{\mathbb Q}=\{2,3,p_1,\ldots,p_m\}.
\]
The required maximal-order and embedding data remain charged input.

Consider
\[
B=(-1,-1)_F.
\]

- \(F\) is totally real, so \(B\) is a division algebra: its reduced norm is a sum of four squares.
- Nevertheless \(B_L\) is split. With \(i^2=j^2=(ij)^2=-1\),
  \[
  (i+j+ij)^2=-3.
  \]
- The final embedding form is
  \[
  E(-1,-1;-3)=-X^2-Y^2-Z^2+3T^2,
  \tag{12}
  \]
  with isotropic vector \((1,1,1,1)\).

Every **coordinate ternary restriction** of (12) is anisotropic:

1. The restriction \(T=0\) is negative definite at a real place.
2. Every other restriction is equivalent to
   \[
   -U^2-V^2+3T^2.
   \]
   Since each \(p_j\) is a square in \(\mathbb Q_3\), the prime \(3\) splits completely in \(F\). At a completion \(F_{\mathfrak p}\simeq\mathbb Q_3\), a nonzero sum \(U^2+V^2\) has even \(3\)-adic valuation, while \(3T^2\) has odd valuation. Hence this ternary is anisotropic.

Also,
\[
\det E(-1,-1;-3)\equiv-3\pmod{F^{\times2}},
\]
so (12) cannot be a quaternion norm/Pfister form in disguise.

For complete verification of the original conic promise, with \(\theta^2=-3\),
\[
\left(\frac{1+\theta}{2}\right)^2+
\left(\frac{1-\theta}{2}\right)^2+1=0.
\]
Thus \(\langle1,1,1\rangle\) over \(L\) is an explicit valid input producing the descended quaternion above.

This single family falsifies the shortcuts:

- “split over the quadratic extension implies split over the base”;
- “the final four-form can be solved by selecting one coordinate ternary”;
- “the final four-form is another instance of the middle Pfister-form step.”

It also realizes the identical-instance cycle (11) at arbitrary tower depth.

**This is intentionally not a hard-instance claim:** both displayed witnesses are small and explicit. Its role is to refute algebraic implications used in a proposed descent.

---

## 5. Auxiliary quadratic extensions do not lower the induction parameter

For a conic over \(F_i\), the base in (7) is \(F_{i-1}\). If the transfer quaternary is solved by adjoining \(\sqrt{\delta_R}\), then, when \(\delta_R\) is nonsquare,
\[
[F_{i-1}(\sqrt{\delta_R}):\mathbb Q]=2^i.
\]
That is the **same absolute degree and tower depth as the original conic field**, not a lower one.

The auxiliary extension need not equal the original extension. For example, over \(L=\mathbb Q(\sqrt2)\), take
\[
\alpha=1+\sqrt2,\qquad \beta=3-\sqrt2.
\]
The quaternion \((\alpha,\beta)_L\) is split because
\[
\beta=4-\alpha
=N_{L(\sqrt\alpha)/L}(2+\sqrt\alpha).
\]
But
\[
\delta_R=\frac{N(\beta)}{N(\alpha)}=-7.
\]
Thus the auxiliary quadratic field is \(\mathbb Q(\sqrt{-7})\), not \(\mathbb Q(\sqrt2)\).

If both quadratic extensions must be retained and are distinct, their compositum has degree
\[
2^{i+1}
\]
and tower depth \(i+1\). More generally, \(k\) independent auxiliary quadratic adjunctions multiply absolute degree by \(2^k\).

Maximal-order data for these new fields are not part of the supplied tower input. Their construction and representation would also need to be paid. Even granting that construction does not repair the nondecreasing recursion.

---

## 6. Exact dependency recurrence—and where the clock stops

Let \(I\) be a ternary input over \(F_i\). In the generic branch, define:

- \(R(I)\): the embedding-form normalization of (4);
- \(P(I,v_1)\): the middle base conic after receiving the first witness;
- \(D(I,v_1,v_2)\): the final embedding form with discriminant \(d_i\).

The charged execution recurrence is
\[
\begin{aligned}
T_{\mathsf C,i}(I)
={}&T_{\mathsf E,i-1}(R(I))\\
&+T_{\mathsf C,i-1}(P(I,v_1))\\
&+T_{\mathsf E,i-1}(D(I,v_1,v_2))\\
&+A_i(I,v_1,v_2,v_3).
\end{aligned}
\tag{13}
\]
Early exits delete terms. Here \(A_i\) includes reading the required data, coordinate conversions, exact field arithmetic, witness verification, and expanded output. Each subproblem cost includes all its own factorization queries.

The dependency graph is therefore
```text
C_i
 ├─ E_{i-1}(norm-ratio discriminant)   [six-form replacement]
 ├─ C_{i-1}                           [middle Pfister step]
 └─ E_{i-1}(d_i)                      [quadratic embedding]
       └─ C_i with descended coefficients
            └─ the same E_{i-1}(d_i)
```

The last two edges describe the invalid extension-based substitution, not a completed algorithm.

For already descended inputs, the first two searches disappear:
\[
T_{\mathsf C,i}^{\rm descended}(a,b)
=
T_{\mathsf E,i-1}(a,b;d_i)+A_i.
\tag{14}
\]
Using the larger-field conic as the implementation of that \(\mathsf E\)-call recreates (14) on the same parameters. There is no finite recursive clock to expand.

Granting the fixed-degree rational backend from the supplied note provides the rational leaves. It does not provide the missing \(\mathsf E\)-recurrence at positive tower height.

### What constant branching would establish—conditionally

If a new, strictly descending implementation supplied a uniform maximum of \(k\) recursive children per node, then the node-count recurrence would be
\[
Q_0=1,\qquad Q_i=1+kQ_{i-1},
\]
hence
\[
Q_h=
\begin{cases}
h+1,&k=1,\\[2mm]
\dfrac{k^{h+1}-1}{k-1},&k>1.
\end{cases}
\tag{15}
\]
Since \(h=\log_2N\), this is polynomial in \(N\) for constant \(k\).

Equation (15) is **conditional**: no such missing \(\mathsf E\)-row has been constructed here. A complete-squareclass implementation would need its own amortized support and call-count proof; counting a growing-degree batch as one free call would not establish (15).

---

## 7. Expanded heights, factoring interfaces, and randomized caps

### 7.1 What the algebraic wrapper actually bounds

In an integral basis of a degree-\(n\) field, represent an element as
\[
x=\frac{\sum_j x_j e_j}{q}
\]
with integer numerator coordinates and one positive integer denominator. Let \(H(x)\) bound their binary lengths, and let \(\mu\) bound the multiplication-table entry lengths.

A field multiplication has coordinate-height bound
\[
H(xy)\le H(x)+H(y)+\mu+2\lceil\log_2n\rceil+O(1).
\]
Inversion is charged as an \(n\times n\) rational linear solve, with polynomial bit complexity and height bounded by
\[
O\!\left(n\bigl(H(x)+\mu+\log n\bigr)\right).
\]
Consequently the fixed-rank wrappers above have bounds of the form
\[
H(I_j)\le c n^r
\left(B+H(I)+\sum_{k<j}H(v_k)+1\right),
\tag{16}
\]
and an analogous bound for the reconstructed output, for absolute constants \(c,r\).

**Equation (16) is not an expanded witness-height theorem for \(\mathsf E\).** It charges supplied witnesses; it does not bound the height of witnesses that an unimplemented solver will find.

Nor may polynomial-per-level bounds simply be composed and called polynomial. For example, the recurrence
\[
K_{i-1}\le c\,2^{ri}K_i
\]
expands to
\[
K_0\le
c^h\,2^{r h(h+1)/2}K_h
=
N^{\log_2c+r(h+1)/2}K_h.
\tag{17}
\]
This is only an illustration of the accounting danger, **not a lower bound** on actual witness heights.

A successful closure must supply a global expanded-height bound, or a recurrence whose expansion proves one.

### 7.2 Numerator and denominator norm factorization

For a nonzero \(x=A/q\) as above, suppose \(|x_j|,q\le2^H\). Hadamard’s bound on the multiplication matrix of \(A\) gives
\[
\log_2|N_{F/\mathbb Q}(A)|
\le
n(H+\mu)+\frac{3n}{2}\log_2n.
\]
Thus an integer covering all numerator **and denominator** support is
\[
q\,|N_{F/\mathbb Q}(A)|,
\]
with bit length at most
\[
(n+1)H+n\mu+\frac{3n}{2}\log_2n+O(1).
\tag{18}
\]

This is the paid support-factorization interface available for an expanded witness. It is polynomial-sized only after \(H\) has been bounded globally. Compact circuits do not provide this interface for free.

Reading the explicit input costs at least \(\Omega(B)\), and writing witnesses or squareclass representatives costs their full expanded bit length. The displayed reductions use exact arithmetic; no uncharged floating-point or \(p\)-adic precision is hidden in them.

### 7.3 Finite randomized caps

The algebraic reductions above are deterministic. They do not provide a randomized solver for the missing gate.

Conditionally, if there were at most \(Q\) randomized calls and each independently verified attempt succeeded with a **proved** probability at least \(p_0>0\), a valid per-call repetition cap would be
\[
R=
\left\lceil
\frac{\log(Q/\eta)}{-\log(1-p_0)}
\right\rceil.
\tag{19}
\]
Polynomial time would require a polynomial bound on \(Q\), on \(p_0^{-1}\), and on each attempt’s bit cost and output height.

None of those requirements can be replaced by an unbounded auxiliary-prime search or by the assertion that trials “usually work.” For the identical-instance recursive substitution, a cutoff merely aborts the looping branch; it does not produce bounded-error success.

The algebraic results and counterexample here are unconditional. **No GRH hypothesis is asserted to close the missing gate.**

---

## 8. Exact remaining obligation

The remaining constructive statement is:

> For every supplied quadratic tower to \(F_i\), and every \(a,b,\delta\in F_i^\times\) with \(\delta\) nonsquare and \((a,b)_{F_i}\) split by \(F_i(\sqrt\delta)\), construct a nonzero expanded-coordinate solution of  
> \[
> aX^2+bY^2-abZ^2=\delta T^2,
> \]
> with uniform polynomial bit cost, polynomial-bit integer-factorization queries explicitly charged, a global polynomial expanded-height bound, and a finite error cap.  
> If implemented by tower descent, its recursive calls must have a proved decreasing parameter and uniformly controlled branching. Calling the conic over \(F_i(\sqrt\delta)\) is not such a decrease.

This obligation already occurs when the first two quaternion-descent searches are unnecessary. The support-obstruction quotient does not supply this missing witness.

**Conclusion:** the six-dimensional part can be reduced away in the promised split case, but the final quaternary embedding gate remains. The larger-field-conic substitution is demonstrably circular, and the displayed family falsifies the relevant base-ternary/Pfister shortcuts. This does **not** prove that another factoring-oracle construction is impossible, or establish hardness or a quantum speedup.