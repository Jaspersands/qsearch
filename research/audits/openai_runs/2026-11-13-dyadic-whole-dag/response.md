## Verdict

**I do not find a fatal precision obstruction. The composition can be completed, but not by the coefficient-cap argument in the last paragraph of the candidate.**

A repaired algorithm needs four explicit changes:

1. Use the **computable upper bound** \(\bar\kappa\), not the unknown actual \(\kappa\), in all budgets.
2. Freeze every factor selector, square-root ball, pivot choice and random integer. Refinement must evaluate the **same exact DAG**, not rerun selection.
3. Add bounded nonzero/valuation tests for generic labels and for the final Stoll inverse. Failure means ABORT, not an inferred exact zero.
4. Replace unspecified presentation recombinations by the binary relation-matrix procedure below. This justifies a group-operation cap without large exponents.

With these changes, the supplied algebraic lemmas support an additive precision ledger and a polynomial total bit clock. I give that ledger below. This is a paper-level result for the repaired classical algorithm—not certification of an implementation, and not a quantum/global-descent result.

---

# 1. Separate conclusions

### Exact correctness

Every accepted operation can be given an exact algebraic certificate. In particular:

- finite approximations are not themselves treated as points;
- no approximate zero is used to prove polynomial divisibility;
- no equality test between arbitrary \(2\)-adic points is needed;
- an accepted output basis is the complete local image, by finite-group saturation—not by sampling evidence.

These statements can hold **on every execution**, including executions outside the geometric good event.

### Finite success probability

The geometric grid and scalar-pencil bounds give a uniform conditional failure bound at each adaptive call. Accepted source/resultant caps then make the local backend terminate at fixed precision.

One must budget failures for actual calls, including source tests and backend truncation. With the budget below, the probability of ABORT is at most \(\eta\).

### Bit clock

The decisive fact is not merely that stored coefficients have bounded poles. It is that:

- every division has a bounded, visible denominator valuation;
- every rank computation either has a structurally known rank or uses a visible unit/determinant certificate;
- every selected root has a fixed isolating ball and a bounded derivative valuation;
- conversions are between fixed lattices with discriminant-controlled denominators.

These facts yield \(P_{\rm in}\le P_{\rm out}+C\) with one native polynomial \(C\), independent of ancestry.

---

# 2. Native parameters and finite operation budget

Assume \(g\ge1\); genus zero is trivial. Write \(n=2g+1\), and compute the nonzero integer discriminant and
\[
D=v_2(\operatorname{disc}f).
\]
Reading \(f\), computing its discriminant and extracting \(D\) cost polynomial bit time in \(n,B\).

Use
\[
\bar\kappa
 =D_0+2g(4D+12)+g(2\lceil\log_2g\rceil+4)+3g.
\]
Dropping the \(-t\) in the supplied index bound is harmless and avoids a dependency on later preprocessing.

Set
\[
T_0=4(\bar\kappa+3g+10)^4,\qquad
k=\left\lceil\log_2\frac{16T_0}{\eta}\right\rceil.
\]
Compute \(s,R,H_{\rm seed},Q,m_{\rm grid}\) from the finite-grid formulas, using this \(k\).

The coefficient cap can be fixed once, without any subsequent enlargement:
\[
\nu=2+\lceil\log_2g\rceil,\qquad
S_0=\max\{1,n\nu,(6g-3)s\}.
\]
This covers:

- the initial formal points, since \(v_2(t_i)\le\nu\);
- their sampled replacements, because \(v_2(t_i+2^Rz_i)=v_2(t_i)\);
- initial branch divisors, whose coefficients are integral;
- every accepted canonical output and every accepted half.

Use \(L_{\rm scale}=S_0\) throughout. Thus
\[
D_L=D+2S_0n(n-1)
\]
is a fixed native parameter, not a quantity recursively recomputed from an ancestor’s intermediate cap.

## An explicit presentation procedure

Let \(r_0=g+t\). Maintain generators \(P_1,\dots,P_r\) and an integer relation matrix, initially
\[
\mathcal R_0=2I_{r_0}.
\]

At an unsuccessful label-rank test, find
\[
v\in\mathbb F_2^r
\]
whose label is zero but which is not in the relation subspace
\(\operatorname{im}(\mathcal R\bmod2)\). This is ordinary binary linear algebra.

Form
\[
h=\sum_{i:v_i=1}P_i
\]
using at most \(r-1\) binary group operations. After ONE-HALF returns \(Q\), append the relation
\[
2Q=\sum_i v_iP_i\quad\text{in }A.
\]

No large integer exponent is needed. Every new relation has coefficients in
\(\{-1,0,2\}\). The abstract presented group has twice the previous order; the actual subgroup also has twice the previous order because \(h\notin2B\). Hence the presentation remains exact.

There are at most \(\bar\kappa\) enlargements and fewer than
\[
(\bar\kappa+r_0+1)^2
\]
point-assembly and halving calls. The displayed \(T_0\) safely dominates this procedure. It is **not** thereby a proved bound for arbitrary unspecified HNF/SNF recombination code.

---

# 3. Precision conventions and elementary ledger

Use absolute precision in fixed coefficient bases:
\[
\widetilde x=x+O(2^P).
\]
For an extension field, use an integral basis and retain the normalized valuation \(v_2(2)=1\).

The following elementary bounds are sufficient.

| Operation | Required hypotheses | Sufficient input precision for \(P\) output digits |
|---|---|---:|
| \(x+y\), \(-x\) | none beyond supplied precision | \(P\) |
| \(xy\) | \(v(x),v(y)\ge-H\) | \(P+H\) |
| \(x^{-1}\) | fixed nonzero selector, \(v(x)\le H\) | \(P+2H+1\) |
| \(x/y\) | \(v(x)\ge-H,\ v(y)\le H\), \(y\ne0\) certified | \(P+3H+1\) |
| multiply by \(2^a\) | exact integer \(a\) | \(P+\max(0,-a)\) |
| monic polynomial division | bounded degrees and coefficient poles | additive polynomial guard |
| integral matrix inverse | \(v(\det M)\le K\), determinant visible | \(P+2K+1\) |
| integral known-rank saturation | rank \(r\); nonzero Smith exponents \(\le K\) | \(P+2rK+1\) |
| integral unit-pivot kernel/solve | selected minor is a unit | \(P\) |
| selected simple Hensel root | fixed root ball; derivative valuation bounded | \(P+\) fixed derivative/certificate guard |

For monic division, the quotient and remainder coefficients are integer polynomials in the input coefficients, of bounded degree. For inputs of degree at most \(d\) and pole cap \(S\), a guard such as \((d+2)S+1\) suffices. This is a precision statement, not just a coefficient-size statement.

For known-rank saturation, minimum-valuation DVR elimination finds the bounded pivots without enumerating minors. It stops after the structurally known rank. The sum of pivot valuations is at most \(rK\); recording the row/column operations and then normalizing a unit row minor gives the displayed guard. No test of the remaining entries for exact zero is required.

These rules apply with **frozen choices**. Repeating a pivot or root-selection procedure during refinement is not the same computational object.

---

# 4. Canonical materialization: the ledger closes

All blocks entering a group operation have degree at most \(g\). The high-degree pencil representation is internal to ONE-HALF and is not stored as a canonical block.

Appending the signed point blocks for \(2\sigma\) adds degree \(4g\). Thus a binary operation has
\[
m\le6g,
\]
including coincident, repeated and opposite supports.

After scaling by \(S_0\):

- every input graph polynomial is integral;
- the quotient-ring arithmetic modulo the monic \(A_{\rm in}\) is integral;
- the normalized preceding saturated basis is integral;
- all matrix-formation maps are integral polynomial maps and therefore lose no absolute digits.

At each product stage:

- the generic rank is known from divisor degree;
- the supplied almost-inverse argument gives nonzero Smith exponents at most \(D_L+2\);
- the matrix dimension is at most \(2m\le12g\).

There are at most \(6g\) stages. A sufficient guard for the complete product-saturation chain is therefore
\[
6g\bigl(24g(D_L+2)+1\bigr).
\]

At the two RR steps:

- full row rank modulo \(2\) is an actual finite test;
- the selected kernels and top-coefficient normalizations use unit pivots;
- these operations lose no further digits in the scaled lattice.

The two output divisions are monic. Their exactness is supplied by the ideal identities
\[
ps-qr=\epsilon A_{\rm in},
\]
and the closure-under-\(Y\) argument. **A computed remainder that looks zero is not used as a certificate.**

Scaling back loses at most \(nS_0\) digits. Consequently the complete materializer has the explicit guard
\[
\boxed{
C_{\rm mat}
 =6g\bigl(24g(D_L+2)+1\bigr)+nS_0+1.
}
\]

This is independent of the history of its input points.

## Required finite acceptance checks

For every newly stored canonical point, require:

1. the stated unit RR tests;
2. the fixed coefficient pole cap \(S_0\);
3. visible nonzero discriminant and branch resultant within
   \[
   K_{\rm can,disc}=2g(g-1)s,\qquad
   K_{\rm lab}= \max\{D,2gns\}.
   \]

The third item may instead be implemented as bounded component-valuation tests before labeling. But some such check is necessary: a coefficient pole cap alone does not justify using \(a\bmod f\) as an element of \(L^\times\).

Initial branch torsion is a separate typed input, using its corrected representative. It is not passed through the generic \(a\bmod f\) labeling rule.

---

# 5. Pencil, Stoll solve and half extraction

Here are explicit native caps sufficient to instantiate the matrix review. Let
\[
S_A=(n+3)S_0,\qquad S=S_A.
\]
Monic division in
\[
c=(f-b_0^2)/a_0
\]
gives this pole cap for \(A_u,B_u\), uniformly for \(u\in\mathbb Z_2\). A sufficient precision guard for pencil formation is
\[
C_{\rm pen}=(n+4)S_0+1.
\]

Choose a scalar grid depth
\[
\tau=2g+k+\lceil\log_2(8n)\rceil+2.
\]
The root-ball estimate in the supplied pencil proof then pays the union over all halves and the visible source conditions.

The following nonnegative caps are sufficient:
\[
\begin{aligned}
K_{wr}&=gns,\\
K_{aw}&=g+gns+2g\tau,\\
K_{af}&=D+nS_A+2n\tau,\\
K_{\rm disc}&=2g(g-1)s+4g\tau.
\end{aligned}
\]

These are caps for the **raw valuations**. Computations of determinants and resultants must first clear the known coefficient poles. Negative resultant valuations are allowed; they are not silently replaced by nonnegative ones.

For example, clearing a Sylvester matrix of dimension at most \(2n\) by \(2^{S_A}\) shifts its determinant valuation by a known amount at most \(2nS_A\). A common fixed certificate-precision allowance is
\[
C_{\rm test}
 =2+K_{\rm disc}+K_{af}+K_{aw}+K_{\rm lab}
       +4n(S+S_0).
\]
This pays the source discriminant, source branch resultant, optional mixed-resultant check, and stored-output chart checks.

## Augmented Stoll matrix

Use the review’s identities, not a generic-rank assertion. With source degree \(\ell\le n\), the following slightly enlarged caps suffice:
\[
\begin{aligned}
D_B={}&2g+K_{aw}+K_{wr}+\lceil K_{af}/2\rceil\\
 &+\bigl[g(5g+12)+n+g\bigr]S,\\
S_s={}&(2g+2)S+2K_{wr},\\
S_M={}&(2g+3)S+2K_{wr},\\
K_B={}&(2n+1)S_M+D_B.
\end{aligned}
\]

Before forming the matrix, check the square-root coefficient cap \(S_s\). Then
\[
B'=2^{S_M}B_g
\]
is integral. Accept the solve only when its determinant is visible with valuation at most \(K_B\).

Matrix formation has bounded-degree monic reductions. A sufficient guard is
\[
C_{B,\rm form}=8(n+1)^2(S_s+S+1).
\]
The solve itself needs at most
\[
P+2K_B+1
\]
digits of \(B'\).

The row \(w_g=1\) is an exact equation of the recorded solve, not an approximately monic coefficient.

## The last inverse is separately paid

It is not enough to say that the output coefficients are bounded.

From the explicit certificate in the matrix review,
\[
v\operatorname{Res}(U,W)
 \le K_U
 :=2g+K_{aw}+2K_{wr}+g(5g+12)S.
\]
Set
\[
E_U=(g+4)S,\qquad K_I=gE_U+K_U.
\]
The multiplication matrix of \(U\) modulo monic \(W\), and the reduced right-hand side \(-V\bmod W\), become integral after multiplication by \(2^{E_U}\). Their formation is paid by
\[
C_{U,\rm form}=8(n+1)^2(S+1).
\]

Accept the inverse only when the determinant of this cleared multiplication matrix is visible below \(K_I\). The solve then costs
\[
P+2K_I+1
\]
input digits.

Thus the potentially dangerous operation
\[
R=-V/U\bmod W
\]
has an explicit additive ledger. It does not rely merely on a final pole cap.

## Why accepted halves are exact

The recorded linear solve satisfies the Stoll congruences exactly. Together with the degree bounds, these imply
\[
V^2-fU^2=\epsilon A_uW^2:
\]
the difference is divisible by \(fA_u\), while its degree is smaller.

The visible final inverse gives \(\gcd(U,W)=1\), so
\[
R^2=f\bmod W.
\]
The divisor identity for \(Uy-V\) gives
\[
2[W,R]=[A_u,B_u].
\]
Hence
\[
2Q=h+2\sigma(z)
\]
is an exact identity of the named points.

Outside the good event the routine may abort. If it accepts, these algebraic deductions still establish the relation. No probabilistic interpretation of an approximate equality is involved.

---

# 6. Local-field backend: finite presentation and root consistency

This backend is implementable from the supplied primary statements, but several details must be made explicit.

## 6.1 Factors, bases and conversions

Use OM factorization at a base precision exceeding \(2D+2\), retaining:

- factor degrees and OM types;
- a fixed ordering of the actual factors;
- fixed finite approximants selecting those factors;
- fixed Okutsu numerator polynomials and denominator exponents.

The Okutsu basis proposition is applied **separately to each irreducible local factor**. It does not require first factoring the original integer polynomial over \(\mathbb Q\).

Subsequent refinement lifts these same selectors. It must not construct a fresh approximate field and silently identify it with the old one.

Let
\[
\mathcal O_L=\prod_i\mathcal O_{E_i}.
\]
The discriminant-index identity gives
\[
v_2[\mathcal O_L:\mathbb Z_2[\theta]]\le D/2.
\]
Consequently the fixed basis and CRT conversions have polynomial denominator guards. Clearing a conversion matrix by \(2^D\) produces an integral matrix whose determinant valuation is at most \(nD\). The matrix-inverse ledger therefore pays its refinement.

The OM Theorem 5.18 excerpt supplies polynomial cost in \(n,D,\nu\) for requested factor precision \(\nu\). At fixed prime \(2\), its residue-field operations must still be charged in their \(O(n)\)-bit representations. The finite-field factorization cost in the packet does that; no residue-element enumeration is needed.

## 6.2 Uniformizers need no unbounded search

Interpret “kernel of reduction” as the **\(\mathbb Z_2\)-lattice**
\[
\mathfrak m_E=\ker(\mathcal O_E\longrightarrow k_E),
\]
not merely as a list of nullspace vectors over \(\mathbb F_2\).

There is even a deterministic alternative to the proposed random draw:

1. compute a \(\mathbb Z_2\)-basis of \(\mathfrak m_E\);
2. inspect its images in \(\mathfrak m_E/\mathfrak m_E^2\);
3. choose any nonzero image.

Some basis vector has nonzero image. Membership is a finite computation: \(4\mathcal O_E\subseteq\mathfrak m_E^2\), so multiplication data modulo \(4\) suffice to construct the relevant quotient lattice.

If the proposed random method is retained instead, its probability claim is valid **for a uniform combination of a lattice basis of \(\mathfrak m_E\)**, since
\[
2\mathfrak m_E\subseteq\mathfrak m_E^2.
\]

## 6.3 The unit presentation is exact

For \(N=2e+1\),
\[
U_N\subseteq U_1^2
\]
by Hensel at \(1\). The generators
\[
g_{i,j}=1+\pi^i\beta_j,\qquad 1\le i<N,
\]
give normal forms in \(U_1/U_N\).

Each square lies at a later level. The relation matrix \(\mathcal R_U\) is triangular with diagonal \(2\), so the abstract presented group has order
\[
2^{(N-1)f_{\rm res}}=2^{2d_E}.
\]
Collection gives a surjection onto \(U_1/U_N\), whose filtration has exactly that order. Thus the presentation is exact.

Only finite quotient arithmetic is needed. Indeed \(N=2e+1\le3e\), so
\[
8\mathcal O_E\subseteq\pi^N\mathcal O_E.
\]
The entire initial unit presentation can be constructed in a finite quotient obtained from integral-basis arithmetic modulo \(8\), with the already paid basis conversions.

No enumeration of its \(2^{2d_E}\) elements is needed.

## 6.4 Solving for one square root is simpler than SNF

Suppose the collected unit has exponent vector \(c\in\{0,1\}^{M}\). To solve
\[
2x=c\quad\bmod\mathcal R_U\mathbb Z^M,
\]
first solve
\[
\mathcal R_U t=c\pmod2.
\]
Choose a binary solution \(t\), and put
\[
x=(c-\mathcal R_Ut)/2.
\]
This is an integer vector with polynomially bounded coefficients. It constructs the required \(v_0\) without large exponent expansion or sign enumeration.

Remove the Teichmüller unit using its selected residue root. Its defining equation \(z^{2^{f_{\rm res}}}-z\) is evaluated by binary powering; its derivative is a unit.

Finally,
\[
u/v_0^2\in U_N
\]
has a unique square root in the specified ball near \(1\). Store that ball and the exact defining input DAG.

**On refinement, do not recollect the unit and select a new \(x\).** Refine the already selected root against the same exact input. Otherwise a component sign can change and invalidate descendant identities.

## 6.5 Component valuations and precision

For an element \(\lambda\in L^\times\) with power-basis coefficient poles at most \(S_\lambda\),
\[
v_2(\lambda_i)\ge-S_\lambda.
\]
If
\[
v_2N_{L/\mathbb Q_2}(\lambda)\le K,
\]
then, writing \(d_i=[E_i:\mathbb Q_2]\),
\[
d_i v_2(\lambda_i)
 \le K+(n-d_i)S_\lambda.
\]
In particular,
\[
v_2(\lambda_i)\le K+(n-1)S_\lambda.
\]

This explicitly pays cancellations between positive and negative component valuations.

Use
\[
V_A=K_{af}+(n-1)S_A
\]
for square-root inputs, and
\[
V_{\rm lab}=K_{\rm lab}+(n-1)S_0
\]
for generic labels. Initial branch representatives have norm valuation at most \(D\), since their componentwise values give, up to sign, the square of the cross-factor resultant.

The selected square-root map has derivative \(2s\), with
\[
v_2(2s)\le1+V_A/2.
\]
Therefore its refinement loss is additive. A sufficiently deep fixed starting ball pays selection; subsequent precision is \(P+\) a fixed guard, not a new conditioning search.

For definiteness, if \(\mathscr H\) dominates the displayed native caps, the deliberately loose bound
\[
\boxed{
C_{\rm fld}(\mathscr H)
 =64(n+1)^4(D+\mathscr H+1)^2
}
\]
suffices for conversions, valuation normalization, collection and selected-root refinement.

This follows from:

- conversion determinants bounded by \(nD\);
- at most \(n\mathscr H\) uniformizer factors in valuation normalization;
- integral-basis multiplication with bounded operand poles;
- unit inverses in the unit quotient;
- the bounded square-root derivative;
- unit-derivative Teichmüller lifting.

The root refiner may perform \(O(\log P)\) Newton stages, but its **external input-precision requirement** remains \(P+C_{\rm fld}\). Its cost is polynomial in \(n,D,\mathscr H,P\).

---

# 7. One fixed additive guard for the whole DAG

For example, take
\[
\begin{aligned}
\mathscr H={}&1+B+R+m_{\rm grid}+\bar\kappa+n+D_L\\
 &+S_0+S_A+S_s+S_M+K_B+K_I\\
 &+V_A+V_{\rm lab}+K_{\rm disc}+K_{af}
   +24g(D_L+2).
\end{aligned}
\]
Every term is computed from the native input and confidence parameter.

A common guard can be chosen as
\[
\boxed{
\begin{aligned}
C=10\bigl[&
1+(n\nu+3)+C_{\rm mat}+C_{\rm pen}+C_{\rm test}\\
&+C_{\rm fld}(\mathscr H)
+C_{B,\rm form}+2K_B\\
&+C_{U,\rm form}+2K_I+2V_A+2S_A
\bigr].
\end{aligned}}
\]

This is intentionally conservative. The preceding rows establish, operation by operation,
\[
\boxed{P_{\rm in}\le P_{\rm out}+C.}
\]

The critical features are:

- \(S_0\) never changes;
- \(D_L\) never changes;
- resultants and pivots are bounded or visibly rejected;
- root selectors never change;
- \(C\) contains no ancestor precision, algebraic degree of an expanded expression, or unknown point condition number.

## Shared DAG size

A coarse explicit structural bound is
\[
N_{\rm DAG}
 =(T_0+1)\,[100(n+\mathscr H+1)]^{12}.
\]
This easily covers the bounded-size polynomial/matrix circuits, stored pivot lists, finite unit presentations, sampled integers and factor/root selector nodes. Hensel and factor nodes have polynomial-time refinement algorithms; their defining algebraic expressions are not expanded into global number fields.

The exact exponent is not important. The important distinction is that the bound is for the **shared representation**, not for expanded algebraic expressions.

## Adaptive construction does not justify “evaluate once at the final maximum”

That sentence in the candidate needs a scheduling argument. A simple repair avoids the issue entirely.

Take
\[
P_{\rm fin}=V_{\rm lab}+4+C_{\rm fld}(\mathscr H),
\qquad
P_{\max}=P_{\rm fin}+N_{\rm DAG}C.
\]
Give a node at DAG depth \(d\) the budget
\[
P_d=P_{\rm fin}+(N_{\rm DAG}-d)C.
\]
Every parent then already has at least \(P_d+C\) digits. Thus the adaptive construction can proceed without discovering a future precision deficit.

Alternatively, lazy refinement may be used and all reevaluations charged; polynomially many requests at polynomial precision still give polynomial total time. The static depth budget is cleaner.

Discarding cached digits is permissible. Discarding the exact DAG and replacing it by an unrelated approximate point is not.

---

# 8. Probability and stopping

On the joint good event for a call:

- the canonical materializer passes;
- source discriminant and branch tests pass;
- every possible backend square-root choice corresponds to a half covered by the geometric event;
- the scalar-pencil bounds pay the augmented Stoll matrix;
- the final inverse and output chart tests pass;
- label valuations are visible within the declared cap.

The source point and its set of halves are fixed before choosing the scalar \(u\). No independence between halves is used.

There are fewer than \(T_0\) geometric calls and fewer than \(T_0\) scalar-pencil calls. Their total failure probability is at most
\[
2T_0\,2^{-k}<\eta/4.
\]
Allocate the remaining budget to verified Las Vegas preprocessing. Given a polynomial expected-time bound, fixed-budget independent restarts amplify success to \(1-\eta/4\); exceeding the total budget returns ABORT. This costs a polynomial factor in \(\log(1/\eta)\), not \(1/\eta\).

For simplicity, a failed geometric or conditioning test can terminate the entire run with ABORT. No uncounted retry loop is needed.

## Why full rank proves completeness

Throughout the run, \(B\) contains \(A[2]\), so
\[
\dim_{\mathbb F_2}B/2B=g+t.
\]
If the label rank is smaller, the binary procedure finds a nonzero class in \(B/2B\) with zero label. Its half enlarges \(B\) by exactly two.

If the label rank reaches \(g+t\), then
\[
B+2A=A.
\]
The finite \(2\)-group \(A/B\) therefore satisfies \(2(A/B)=A/B\), forcing \(A/B=0\). Hence \(B=A\), and the returned labels span the complete local image.

This is an exact finite-group deduction. It does not use a point-equality oracle or infer completeness from sampled witnesses.

---

# 9. A source-boundary issue, and a native repair

The finite-grid proof in the packet imports \(A_{\rm tail}\) from a review whose full text is not included. That label alone cannot supply a native numerical constant.

This need not leave the repaired algorithm conditional. A coarser constant can be obtained directly from the attached volume-cover argument.

Put
\[
\begin{aligned}
N_c&=4D+12,\\
M&=2\lceil\log_2g\rceil+4,\\
\Delta&=g(1+\lceil\log_2g\rceil),\\
A_{\rm cov}&=3g+gM+2gN_c,
\end{aligned}
\]
and use
\[
\boxed{
\widehat A_{\rm good}
 =A_{\rm cov}+N_c+\Delta+g+10
       +2\lceil\log_2g\rceil.
}
\]

The cover has at most \(2^{A_{\rm cov}}\) product charts and Jacobian volume at most one per chart.

On an integral chart, the free coordinate is affine with scale valuation at most \(N_c\). A collision on a \(y\)-free chart implies
\[
v\bigl((y_i-y_j)(y_i+y_j)\bigr)>2s,
\]
so one linear factor has valuation \(>s\). On an infinity chart use
\[
w^2=uF(u),\qquad u=1/x,
\]
to obtain the analogous implication for \(w_i\pm w_j\).

For two embeddings of the same closed point, replace one row of the integral-basis embedding matrix by the sum or difference of the two rows. Its determinant is unchanged. Hence some coefficient of the relevant linear form has valuation at most \(d_E/2\); using a uniformizer-scaled infinity parameter adds at most \(f_E\). The supplied bound \(\sum d_E\le\Delta\) pays these dependent-conjugate tubes.

Branch tubes use either the free \(y\)-coordinate or
\[
f(x)=\prod_{\theta}(x-\theta).
\]
The union over at most \(g\) support coordinates and \(g^2\) collisions is covered by the displayed constant. Degree-drop and exact collision loci are included as limiting tubes.

Thus
\[
\mu_\omega(G\setminus G_s)
 \le2^{\widehat A_{\rm good}-s}.
\]
Use \(\widehat A_{\rm good}\) in the supplied finite-grid stability formulas. No support fields or charts are constructed by the algorithm.

This replaces an unavailable report constant by an explicit, looser native one.

---

# 10. Repaired theorem and remaining admission boundary

**Repaired native theorem.** For monic squarefree
\[
f\in\mathbb Z[x],\qquad \deg f=2g+1,
\]
and \(0<\eta<1\), the algorithm specified above, using the supplied materializer and Stoll identities together with the selected OM/Okutsu algorithms, has:

- a deterministic polynomial bit-time bound in \(g,B,\log(1/\eta)\);
- no incorrect accepted output;
- ABORT probability at most \(\eta\);
- output consisting of a basis of the complete local Kummer image in explicitly constructed finite squareclass coordinates.

The output coordinates comprise fixed local-factor selectors, fixed integral/residue data, uniformizers and unit generators, and binary quotient-coordinate maps. There are at most \(2n+r\le3n\) raw squareclass coordinates before quotient-basis reduction. No infinite \(2\)-adic coefficients are output.

All input reading, factor/basis refinement, finite-field arithmetic, point/root preparation, precision and output costs are included. This is entirely classical; it supplies no quantum state-preparation or coherent-oracle implementation and establishes no global speedup.

## Smallest useful falsification control

Before implementing the full loop, test the backend-to-Stoll refinement interface on
\[
f_N(x)=x\bigl(x^2-2^{2N+1}\bigr).
\]
Here
\[
L\simeq\mathbb Q_2\times\mathbb Q_2(\sqrt2),
\qquad D=6N+5.
\]
This single genus-one family simultaneously exercises:

- a growing order index;
- growing CRT denominators;
- ramified unit collection;
- selected square-root refinement;
- signed/nonintegral source resultants.

Reuse the same ancestors in a cancellation-heavy DAG, and request successive higher precisions without changing any selector. A change of root branch, a non-prefix-compatible refined point, or a required guard exceeding the declared additive bound is a decisive falsifier.

Passing finitely many instances would only check transcription and implementation. The theorem rests on the ledger and identities above, not on such controls.