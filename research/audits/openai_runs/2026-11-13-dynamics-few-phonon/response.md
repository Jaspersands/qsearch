## Result

**Yes. For every fixed initial boson count \(k\), the full native occupation law has a uniform classical sampler with**
\[
T_{\mathrm{bit}}=(D+1)^{O(k)}\operatorname{poly}(L,b),
\qquad
\operatorname{TV}\le 2^{-b}.
\]
The exponent in \(D\) depends on \(k\); this is not an unrestricted-input polynomial-time result.

The proposed support bound is **true**:
\[
[p_\mu]P_\lambda(q,t)=0
\quad\text{if}\quad
\ell(\mu)=k,\qquad \lambda_{3k+1}>k,\qquad q=t^3.
\]
Its proof below uses independent auxiliary variables, not coefficientwise inference from a univariate zero.

The sampling ingredient beyond spectral sparsity is a **polynomial-size, annihilator-invariant downward closure**. Exact Pieri matrices on that closure give all required conditional norms, including interference. No Macdonald power-sum coefficient oracle is needed.

All symmetric-function identities used below are supplied in the extracts or derived from them.

---

## 1. Falsification first: replacing the coherent sum by a mixture is already wrong

There is an exact native degree-two control. Set \(D=2\), so \(t=2/3\), and
\[
r_1=\frac{19}{9},\qquad r_2=\frac{133}{81}.
\]
The supplied row generating function and elementary generating function give
\[
g_2=\frac{p_1^2}{2r_1^2}+\frac{p_2}{2r_2},
\qquad
e_2=\frac{p_1^2-p_2}{2}.
\]
Their normalized occupation vectors, in the order \((|2\rangle,|11\rangle)\), are
\[
v_{(2)}=\left(\sqrt{\frac{19}{26}},\sqrt{\frac7{26}}\right),
\qquad
v_{(11)}=\left(-\sqrt{\frac7{26}},\sqrt{\frac{19}{26}}\right).
\]

For input \((2)\) at \(\tau=0\), the correct output is deterministically \((2)\). Sampling an eigenlabel first and then its occupation law instead produces \((11)\) with probability
\[
2\frac{19}{26}\frac7{26}=\frac{133}{338}.
\]
Thus even this two-dimensional spectral-support shortcut fails exactly. This is a falsifier of that shortcut, not an obstruction to classical sampling.

The construction below retains the coherent vector and squares only after contraction.

---

# Part I. A complete one-boson sampler

## 2. The one-boson downward closure is polynomial

Throughout the entire computation—including all lower degrees—keep
\[
t=\frac D{D+1},\qquad q=t^3,\qquad
r_n=\frac{1-q^n}{1-t^n}=1+t^n+t^{2n}.
\]

The supplied one-boson formula implies that the exact spectral support of \(p_D\) is
\[
\mathcal H_{3,1}(D)=\{\lambda\vdash D:\lambda_4\le1\}.
\]
Indeed, outside this set the box \((i,j)=(3,1)\) gives a zero; inside it there is no nonorigin box with \(i=3j\).

Retain the downward-closed set
\[
\mathcal S=\{\lambda:|\lambda|\le D,\ \lambda_4\le1\}.
\]
A shape in this set is determined by its first three row lengths and the number of subsequent one-box rows. Therefore
\[
|\mathcal S|\le (D+1)^4.
\]

Work in the unnormalized Macdonald \(P\)-basis. Write
\[
h_\lambda=\langle P_\lambda,P_\lambda\rangle_{q,t},
\qquad Q_\lambda=P_\lambda/h_\lambda.
\]
This avoids square roots throughout the classical computation.

---

## 3. Paid annihilation matrices on the downward closure

The following construction works for any finite downward-closed set of shapes.

### 3.1 Norms from the two supplied Pieri formulas

Let \(\phi_{\lambda/\eta}\) and \(\psi_{\lambda/\eta}\) denote the supplied coefficients in
\[
P_\eta g_n=\sum_\lambda\phi_{\lambda/\eta}P_\lambda,
\qquad
Q_\eta g_n=\sum_\lambda\psi_{\lambda/\eta}Q_\lambda,
\]
where \(g_n=Q_{(n)}(q,t)\).

These \(g_n\) are auxiliary Macdonald row functions, **not** the native vertex coefficients \(V_n\). The Hamiltonian is not being changed.

Comparing the two formulas gives
\[
\boxed{\quad
\frac{h_\lambda}{h_\eta}
=\frac{\psi_{\lambda/\eta}}{\phi_{\lambda/\eta}}.
\quad}                                                     \tag{1}
\]
Starting with \(h_\varnothing=1\), compute each norm along a one-box chain. Every intermediate shape is a subpartition of \(\lambda\), hence belongs to \(\mathcal S\). This supplies the norms without a hook-norm or coefficient oracle.

### 3.2 Adjoint row matrices

The supplied row generating function is
\[
G(z)=\sum_{n\ge0}g_nz^n
=\exp\!\left(\sum_{n\ge1}\frac{p_nz^n}{n r_n}\right).
\]
Since
\[
p_n^*=n r_n\partial_{p_n},
\]
its adjoint is
\[
G^*(z)=\exp\!\left(\sum_{n\ge1}z^n\partial_{p_n}\right).
\]

Let \(M_n\) be the matrix of \(g_n^*\) on the \(P\)-basis indexed by \(\mathcal S\). Adjointness and (1) give
\[
\boxed{\quad
M_nP_\lambda
=\sum_{\substack{\eta\subseteq\lambda\\
                 \lambda/\eta\text{ horizontal }n\text{-strip}}}
  \psi_{\lambda/\eta}P_\eta .
\quad}                                                     \tag{2}
\]
Thus these matrices are obtained directly from the explicit Pieri products. They preserve the downward closure.

### 3.3 Recovering the native annihilators

Define
\[
C_n=n\partial_{p_n},\qquad A_n=p_n^*=r_nC_n.
\]
Taking the logarithmic derivative of \(G^*(z)\) gives the matrix recurrence
\[
\boxed{\begin{aligned}
C_n&=nM_n-\sum_{j=1}^{n-1}M_jC_{n-j},\\
A_n&=r_nC_n .
\end{aligned}}                                             \tag{3}
\]
All matrices here act on \(\mathcal S\). Restriction is exact because every \(M_n\) lowers to subpartitions.

For example,
\[
C_1=M_1,\qquad C_2=2M_2-M_1^2.
\]
The subtractions are essential. This is not an absolute-history or positivity replacement.

### 3.4 The Pieri entries are finite rational computations

No infinite-product evaluation is required. For the supplied
\[
f(u)=\frac{(tu;q)_\infty}{(qu;q)_\infty},
\]
one has
\[
\frac{f(qu)}{f(u)}=\frac{1-qu}{1-tu}.
\]
Hence, for integers \(a>b\),
\[
\frac{f(q^at^c)}{f(q^bt^c)}
=\prod_{v=b}^{a-1}
  \frac{1-q^{v+1}t^c}{1-q^vt^{c+1}},                       \tag{4}
\]
with the inverse formula when \(a<b\).

In each pair factor of the supplied horizontal-strip Pieri products, the \(t\)-exponent \(c\) agrees. Interlacing ensures all starting \(q\)-exponents are nonnegative. At \(q=t^3\), (4) contains only factors
\[
1-t^e,\qquad 1\le e\le 4D+3.
\]
They are strictly positive. Thus every entry and norm is a computable rational, and **no coincident-content or spectral-gap division occurs**.

---

## 4. Native initialization and coherent evolution

For the one-boson input, calculate
\[
a_\lambda=(A_D)_{\varnothing,\lambda}.
\]
This is exactly
\[
a_\lambda=(p_D^*P_\lambda)_\varnothing
=\langle p_D,P_\lambda\rangle.
\]
Consequently
\[
p_D=\sum_{\lambda\vdash D,\ \lambda_4\le1}
       c_\lambda P_\lambda,
\qquad
c_\lambda=\frac{a_\lambda}{h_\lambda}.                     \tag{5}
\]
The exact checksum is
\[
\sum_\lambda c_\lambda^2h_\lambda=Dr_D.                    \tag{6}
\]

Compute the native rational eigenvalue \(E_\lambda\), and set
\[
z_\lambda=e^{-2\pi i\tau E_\lambda},\qquad
F=\sum_\lambda c_\lambda z_\lambda P_\lambda.
\]
Then \(F=e^{-iTH}p_D\), with \(\|F\|^2=Dr_D\).

For any homogeneous polynomial \(F\), its native occupation law is
\[
\pi_F(\nu)
=\frac{R_\nu\,|[p_\nu]F|^2}{\|F\|^2}.                     \tag{7}
\]
For the displayed evolved \(F\), this is precisely the contract’s coherent occupation law. The change from \(J\)-normalization to \(P\)-normalization cancels between coefficients and norms.

---

## 5. Sampling the full occupation by size-biased annihilation

Maintain the unnormalized coefficient vector \(v\) of a homogeneous polynomial \(F\) of current degree \(d\). For every \(1\le n\le d\), calculate
\[
W_n=\frac{\|A_nF\|^2}{r_n}
   =\frac1{r_n}\sum_\eta h_\eta |(A_nv)_\eta|^2.            \tag{8}
\]
Euler’s identity gives
\[
\sum_{n=1}^d W_n
=\sum_{n=1}^d\frac{\langle F,p_np_n^*F\rangle}{r_n}
=d\|F\|^2.                                                \tag{9}
\]

The ideal sampling step is:

1. Select \(n\) with probability \(W_n/(d\|F\|^2)\).
2. Record one part of size \(n\).
3. Replace \(v\leftarrow A_nv\) and \(d\leftarrow d-n\).
4. Stop at \(d=0\).

There are at most \(D\) steps.

### Proof that this samples (7)

In normalized occupation coordinates,
\[
A_n|\nu\rangle
=\sqrt{n r_n m_n(\nu)}\,|\nu-\{n\}\rangle.
\]
Therefore selecting \(n\) and then considering the normalized state \(A_nF\) is equivalent, on its occupation distribution, to:

* draw \(\nu\) from \(\pi_F\);
* select one part size \(n\) with probability \(n m_n(\nu)/d\);
* remove that part.

Repeating this procedure only changes the order in which the parts of the original \(\nu\) are revealed. The final multiset has law \(\pi_F\).

Crucially, the actual contracted expression is
\[
\|A_nF\|^2
=\sum_\eta h_\eta
 \left|\sum_\lambda (A_n)_{\eta\lambda}c_\lambda z_\lambda\right|^2,
\]
so all interference is retained. No occupation coefficients are enumerated.

---

## 6. Accuracy and finite BIT costs

This completes the one-boson algorithm after the following finite-precision implementation.

### 6.1 Binary time and phase precision

A common denominator for all degree-\(D\) eigenvalues is
\[
D^{3D}(D+1)^D.
\]
Thus \(E_\lambda\) has \(O(D\log(D+2))\) bits. Compute
\[
\{\tau E_\lambda\}\in[0,1)
\]
**exactly** before approximating the exponential. This costs polynomial time in \(L+D\log(D+2)\).

Choose complex dyadics \(\widetilde z_\lambda\) satisfying
\[
|\widetilde z_\lambda-z_\lambda|\le\delta,
\qquad \delta=2^{-(b+4)}.
\]
Elementary interval/Taylor evaluation of sine, cosine and \(\pi\) suffices in polynomial bit time; no exact-angle oracle is needed.

Let
\[
\widetilde F=\sum_\lambda c_\lambda\widetilde z_\lambda P_\lambda.
\]
Orthogonality gives
\[
\|\widetilde F-F\|\le\delta\|F\|.
\]
After normalization, the vector distance is at most \(2\delta\), so the corresponding occupation laws have TV distance at most \(2\delta\).

This phase accuracy is independent of \(|\tau|\). Only the exact modular multiplication depends on \(L\).

### 6.2 Bounded-clock conditional choices

After phase approximation, all vector coordinates, norms and weights (8) are exact complex or real rationals. Do not renormalize the vector after a selected annihilation.

At each step use
\[
M=b+2\left\lceil\log_2(D+1)\right\rceil+4
\]
random bits. Compute each cumulative probability exactly, round its boundary down to a multiple of \(2^{-M}\), and use a uniform \(M\)-bit integer.

With at most \(D\) outcomes, a conditional law changes by at most \(D2^{-M}\) in TV. Coupling over at most \(D\) steps gives total error at most \(D^22^{-M}\). Consequently
\[
\operatorname{TV}(\text{implemented output},\text{target})
\le 2\delta+D^22^{-M}<2^{-b}.                              \tag{10}
\]

Zero weights remain zero under this boundary rounding. Rare conditional events require neither relative-error estimates nor increased phase precision.

### 6.3 Explicit polynomial bit-size bounds

Let \(N\) be an upper bound on the number of retained shapes; for one boson,
\[
N=(D+1)^4.
\]

A Pieri coefficient uses \(O(D^3)\) factors from (4). Each factor has \(O(D\log(D+2))\) bits. Hence:

* Pieri coefficients have \(O(D^4\log(D+2))\) bits;
* norms computed along at most \(D\) one-box steps have
  \[
  B=O((D+1)^5\log(D+2))
  \]
  bits.

Form a common denominator \(\Delta\) for the primitive data
\[
M_n,\quad h_\lambda^{\pm1},\quad r_n^{\pm1}.
\]
There are at most \(O(DN^2)\) such rational entries, so one may take
\[
\log_2\Delta=O((D+1)(N+1)^2B).                            \tag{11}
\]

Recurrence (3) shows that \(C_n\) has denominator dividing \(\Delta^n\), and \(A_n\) has denominator dividing \(\Delta^{n+1}\). Using common-denominator arithmetic:

* initialization by annihilators of total degree \(D\);
* multiplication by dyadic phases;
* an entire subsequent removal trajectory of total degree at most \(D\);

produce coefficient denominators dividing
\[
2^{b+O(1)}\Delta^{4D+1}.
\]
Integer coefficient growth contributes only \(O(D(B+\log(DN+2)))\) additional bits. Thus all sampling-stage operands have bit length bounded by
\[
K=O\!\left(
b+(D+1)^7(N+1)^2\log(D+2)
\right).                                                  \tag{12}
\]
The same bound covers exact squared norms and conditional ratios. This explicitly prevents hidden exponential precision costs.

Dense construction of (3) costs \(O(D^2N^3)\) rational operations; Pieri-table construction costs \(O(D^3N^2)\). All conditional contractions together cost \(O(D^2N^2)\).

For example, conservative schoolbook bounds give
\[
\begin{aligned}
T_{\rm bit}=O\Big(&
 (D+1)^3(N+1)^3(K+1)^3\\
&+N\big(L+b+D\log(D+2)+1\big)^6\\
&+D\big(b+\log(D+2)\big)+L
\Big).                                                    \tag{13}
\end{aligned}
\]
The phase-evaluation exponent is deliberately loose. Space is bounded by
\[
O\!\left((D+1)(N+1)^2(K+1)+\operatorname{poly}(L+b+D)\right).
\]
The random-bit budget is at most \(DM\). Explicit input loading and writing the final partition cost \(O(D\log(D+2)+L)\) bits of access/output work and are included.

Equations (10)–(13) finish a bounded-clock polynomial-BIT sampler for \(k=1\).

---

# Part II. The hook bound for every fixed \(k\)

## 7. A multivariate proof—no univariate cancellation inference

Define
\[
\mathcal H_{u,v}=\{\lambda:\lambda_{u+1}\le v\}.
\]

### 7.1 A hook-vanishing specialization derived from Cauchy and Pieri

For alphabets \(X=(x_1,\ldots,x_u)\) and \(Y=(y_1,\ldots,y_v)\), define the algebra homomorphism
\[
\Phi_{u,v}(p_n)=p_n(X)-r_np_n(Y).                          \tag{14}
\]
I claim
\[
\boxed{\quad
\Phi_{u,v}(P_\lambda)=0
\quad\text{if }\lambda_{u+1}>v.
\quad}                                                     \tag{15}
\]

To prove it, apply (14) to one alphabet of the supplied Cauchy identity:
\[
\begin{aligned}
\sum_\lambda P_\lambda(Z)\Phi_{u,v}(Q_\lambda)
&=\exp\!\left(
 \sum_{n\ge1}\frac{p_n(Z)p_n(X)}{nr_n}
 -\sum_{n\ge1}\frac{p_n(Z)p_n(Y)}n
 \right)\\
&=\Pi(Z;X)\prod_{j=1}^{v}
       \left(\sum_{a\ge0}(-y_j)^a e_a(Z)\right).             \tag{16}
\end{aligned}
\]
In \(\Pi(Z;X)\), only shapes \(\eta\) with \(\ell(\eta)\le u\) occur.

Each of the \(v\) elementary factors in (16), by the supplied vertical-strip Pieri rule, adds at most one box to each row. Therefore every resulting \(\lambda\) satisfies
\[
\lambda_{u+1}\le v.
\]
Comparison of \(P_\lambda(Z)\)-coefficients proves (15), since \(Q_\lambda=P_\lambda/h_\lambda\) and \(h_\lambda>0\).

This proof is formal and degreewise finite. The alphabets are not a physical-position sampling measure.

### 7.2 Separating individual length-\(k\) coefficients

Now take \(u=3k\), \(v=k\), and specialize the \(3k\) \(X\)-letters to
\[
X=(x_1,tx_1,t^2x_1,\ldots,x_k,tx_k,t^2x_k).
\]
Because \(r_n=1+t^n+t^{2n}\),
\[
\Phi_{3k,k}(p_n)=r_n\sum_{j=1}^k(x_j^n-y_j^n).
\]
Set \(x_j=y_j+\epsilon_j\). For any homogeneous symmetric function \(F\) of degree \(D\),
\[
\boxed{\begin{aligned}
&[\epsilon_1\cdots\epsilon_k]\,
F\!\left\{p_n=r_n\sum_{j=1}^k
           \big((y_j+\epsilon_j)^n-y_j^n\big)\right\}\\
&\hspace{1cm}=
\sum_{\substack{\mu\vdash D\\\ell(\mu)=k}}
 R_\mu\,[p_\mu]F\;
 m_{(\mu_1-1,\ldots,\mu_k-1)}(y_1,\ldots,y_k).
\end{aligned}}                                             \tag{17}
\]

Here is why (17) separates exactly the desired coefficients:

* Every substituted \(p_n\) has zero constant term in the \(\epsilon\)'s.
* A single factor contributes dependence on only one \(\epsilon_j\) at a time.
* To obtain the squarefree product \(\epsilon_1\cdots\epsilon_k\), there must therefore be exactly \(k\) power-sum factors.
* The first derivative of the \(n\)-th factor contributes \(nr_ny_j^{n-1}\).
* Permuting equal parts contributes \(\prod_n m_n!\), giving exactly \(R_\mu\).

Distinct length-\(k\) partitions \(\mu\) give distinct monomial symmetric polynomials after subtracting one from every part and padding with zeros. Those polynomials are linearly independent.

If \(\lambda_{3k+1}>k\), (15) makes the left side of (17), with \(F=P_\lambda\), identically zero. Independence then proves
\[
\boxed{\quad
[p_\mu]P_\lambda=0
\quad\text{for every }\ell(\mu)=k
\text{ whenever }\lambda_{3k+1}>k.
\quad}                                                     \tag{18}
\]

This is an individual-coefficient proof, not a statement about a sum of same-length coefficients.

---

## 8. Turning (18) into the all-fixed-\(k\) sampler

Retain
\[
\mathcal S_k=\{\lambda:|\lambda|\le D,\ \lambda_{3k+1}\le k\}.
\]
This set is downward closed.

A shape in \(\mathcal S_k\) is encoded by:

* its first \(3k\) row lengths;
* for each of its first \(k\) columns, the number of boxes below row \(3k\).

These \(4k\) integers lie between \(0\) and \(D\), so
\[
|\mathcal S_k|\le (D+1)^{4k}.                              \tag{19}
\]

Use exactly the matrices, norms and sampler already constructed, now on \(\mathcal S_k\). For explicit input
\[
\mu=(\mu_1,\ldots,\mu_k),
\]
compute the row vector
\[
a_\lambda
=\big(A_{\mu_1}\cdots A_{\mu_k}P_\lambda\big)_\varnothing
=\langle p_\mu,P_\lambda\rangle,
\qquad
c_\lambda=a_\lambda/h_\lambda.                            \tag{20}
\]
This costs \(O(kN^2)\) rational operations once the matrices are available. It does not request any power-sum coefficient.

By (18),
\[
p_\mu=\sum_{\lambda\in\mathcal S_k,\ |\lambda|=D}
       c_\lambda P_\lambda,
\qquad
\sum_\lambda c_\lambda^2h_\lambda=R_\mu.                   \tag{21}
\]
Apply the native spectral phases and then the same annihilation sampler.

Substituting \(N=(D+1)^{4k}\) into the proved BIT bounds yields
\[
T_{\rm bit}=(D+1)^{O(k)}\operatorname{poly}(L,b).
\]
The output can have arbitrarily many bosons, up to \(D\); the promise is only on the initial count.

---

## 9. Sharpness and exact audit checks

The support result has an additional all-degree check. Define the number of resonant boxes
\[
\rho(\lambda)=\#\{(i,j)\in\lambda:i=3j\},
\]
with zero-based box coordinates. For a nonempty shape,
\[
\rho(\lambda)=\min\{k\ge1:\lambda_{3k+1}\le k\}.
\]

Equation (18) proves that every power-sum coefficient of length below \(\rho(\lambda)\) vanishes. Meanwhile the supplied principal specialization
\[
\epsilon_v(J_\lambda)
=t^{n(\lambda)}
 \prod_{(i,j)\in\lambda}(1-vt^{3j-i})
\]
has a zero of **exactly** order \(\rho(\lambda)\) at \(v=1\). Since the shorter coefficients have already been proved individually zero, its nonzero leading term implies that at least one coefficient of length \(\rho(\lambda)\) is nonzero.

Thus
\[
\boxed{\quad
\min\{\ell(\mu):[p_\mu]J_\lambda\ne0\}=\rho(\lambda).
\quad}                                                     \tag{22}
\]
This last use of principal specialization is an existential **nonvanishing** inference, not the invalid coefficientwise-vanishing inference.

For example, \(\lambda=(k^{\,3k+1})\) has \(\rho(\lambda)=k\), so the endpoint \(\lambda_{3k+1}=k\) is attained by some length-\(k\) input for every \(k\).

Useful exact implementation falsifiers are:

\[
\sum_\lambda \frac{a_\lambda^2}{h_\lambda}=R_\mu,
\qquad
\sum_n\frac{\|A_nF\|^2}{r_n}=d\|F\|^2,
\]
and deterministic output \(\mu\) at \(\tau=0\). The degree-two control above additionally falsifies any implementation that silently replaces the coherent contraction by an eigenstate mixture.

## Scope

The fixed-\(k\) obligation is complete under the supplied Cauchy, Pieri and native spectral identities. No unchecked Jack-to-Macdonald transfer, coefficient advice, position-space measure, or quantum-transform review is used.

The all-\(D\) sampler is an exact structural falsifier to a claimed classical obstruction **in the fixed-initial-boson regime**. Its exponent grows with \(k\); it establishes neither an unrestricted polynomial sampler nor hardness when \(k\) grows.