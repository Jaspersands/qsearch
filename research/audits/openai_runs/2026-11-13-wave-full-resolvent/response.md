Let \(A_0=I-K=P(T_x,T_y)\), \(\eta=L^{-1}\), and \(G=A^{-1}\delta_0\). For the specified five-source input,
\[
f_5=A_0\delta_0,
\]
the exact response is
\[
\boxed{u_5=A^{-1}(A-i\eta I)\delta_0=\delta_0-i\eta G.} \tag{1}
\]

Writing
\[
p(k)=-3+2\cos(2\pi k_x/L)+2\cos(2\pi k_y/L),\qquad N=L^2,
\]
and using the unitary Fourier transform,
\[
\widehat u_5(k)=\frac1{\sqrt N}\frac{p(k)}{p(k)+i\eta}.
\]
Consequently,
\[
\boxed{Z_5:=\|u_5\|^2=1-\eta^2Z_0,\qquad
Z_0:=\|G\|^2=\frac1N\sum_k\frac1{p(k)^2+\eta^2}.} \tag{2}
\]

**Decisive result.** Analytically, \(Z_0=\Theta(L)\). Thus the original source LCU has success \(\Theta(L^{-1})\), whereas deflating the localized term in (1) removes that normalization problem. I can pay for the lattice dyadic-shell construction and give a complete algorithm for one restricted, recoverable quotient family. I cannot justify a universal polynomial source-deflation operation. The precise remaining theorem is stated in Section 5; it is a constructive, quantitative condition, not an unknown-overlap assumption.

## 1. Proved: the five-source obstruction concerns the requested spatial sample

### Lattice resolvent bound

There are absolute constants; for example, the following conservative bounds suffice:
\[
\boxed{\frac{L}{1024}\le Z_0\le128L.} \tag{3}
\]

Here is an elementary proof, using the actual lattice symbol.

Let
\[
M(t)=\#\{k:|p(k)|\le t\}.
\]
For \(0<t\le1/8\), partition the near-resonant set into signed coordinate sectors, choosing the dependent coordinate to have the larger absolute angle. In each sector its derivative has magnitude at least \(1\): indeed,
\[
\cos\theta_x+\cos\theta_y\in[23/16,25/16],
\]
and the larger absolute angle has cosine at most \(25/32\). For each independent grid coordinate, the allowed dependent-coordinate interval therefore has angular length at most \(2t\). Counting grid points in these intervals gives
\[
M(t)\le 8L(Lt/\pi+1)\le8N t+8L. \tag{4}
\]
In particular, \(M(t)\le16Nt\) when \(t\ge\eta\).

Splitting the resolvent sum into \(|p|\le\eta\), dyadic bands up to \(1/8\), and the remaining region proves the upper bound in (3). For example, the inner region contributes at most \(16L\), the dyadic regions at most \(64L\), and the final region at most \(256\). The finitely many smaller \(L\) satisfy the stated bound directly from \(|a|\ge\eta\).

For the lower bound, take \(0\le k_x\le\lfloor L/16\rfloor\). The continuous lattice resonance has
\[
\theta_y=\arccos(3/2-\cos\theta_x).
\]
Rounding this \(\theta_y\) to the nearest grid angle gives \(|p(k)|\le2\pi/L\). There are at least \(L/16\) such points, so
\[
Z_0\ge \frac{L}{16(4\pi^2+1)}\ge \frac{L}{1024}.
\]
No continuum-circle approximation or numerical asymptotic is used.

### Consequences for normalization and sampling

Since \(\|A\|^2\le50\) and \(\|f_5\|^2=13\),
\[
13/50\le Z_5\le1.
\]
The five weights have \(\ell_1\)-norm \(7\), hence the usual source LCU succeeds with
\[
p_{\rm source}=\frac{Z_5}{49Z_0}=\Theta(L^{-1}). \tag{5}
\]
This is exponential in \(n\). It is a failure of that implementation, not a quantum lower bound.

Equation (1) gives the stronger spatial statement
\[
P_{f_5}(x\ne0)
 =\frac{\eta^2\bigl(Z_0-|G(0)|^2\bigr)}{Z_5}
 \le \frac{512}{L}.
\]
Therefore
\[
\boxed{\operatorname{TV}(P_{f_5},\delta_0)\le \min(1,512/L).} \tag{6}
\]

For any fixed \(C\), (4) also gives
\[
\frac{\|\Pi_{\{|p|\le C/L\}}u_5\|^2}{\|u_5\|^2}
=O((C+1)/L). \tag{7}
\]
This is not merely a state-overlap objection. Any normalized state supported on a Fourier set of size \(M\) has spatial probability at the origin at most \(M/N\), by Cauchy–Schwarz. Thus **any** state confined to \(|p|\le C/L\) has spatial Born law \(Q\) satisfying
\[
\operatorname{TV}(P_{f_5},Q)\ge1-O((C+1)/L). \tag{8}
\]
A fixed-width resonant band can therefore fail almost maximally for the native classical sample.

## 2. Explicit deflation operation—and its exact limitation

Represent the source as a Laurent polynomial \(F\). For any Laurent polynomial \(H\), define
\[
R=F-PH,\qquad S=R-i\eta H=F-(P+i\eta)H.
\]
Then, exactly on the torus,
\[
\boxed{A^{-1}f=h+A^{-1}s.} \tag{9}
\]
Here \(h,s\) are the spatial coefficient vectors of \(H,S\), after reducing exponents modulo \(L\) and combining duplicates.

This is the appropriate damped deflation identity. Dividing by \(P\) does **not** remove the correction \(-i\eta A^{-1}h\).

### A concrete operation: monic Laurent division

Set
\[
C(X)=X+X^{-1}-3,\qquad Q(X,Y)=YP=Y^2+C(X)Y+1.
\]
After a monomial shift making the dividend polynomial in \(Y\), divide by this monic quadratic over
\(\mathbb Q(i)[X^{\pm1}]\). Shifting back produces an exact decomposition \(F=PH+R\).

This is useful when the occupied coordinate span is polynomially bounded. It is not a paid universal sparse operation.

### Exact counterexample to unrestricted explicit-list division

Take
\[
D=2^{n-2},\qquad F=1+X^D+Y^D.
\]
This has three source sites and \(O(n)\) coordinate bits. Dividing
\[
YF=Y^{D+1}+(1+X^D)Y
\]
by \(Q\) produces quotient
\[
H_D=\sum_{j=0}^{D-1}t_j(C)Y^{D-1-j},
\]
where
\[
t_0=1,\quad t_1=-C,\quad t_j=-Ct_{j-1}-t_{j-2}.
\]
The coefficient of \(X^j\) in \(t_j(C(X))\) is \((-1)^j\). Hence the quotient has at least \(D\) nonzero monomials:
\[
\boxed{\text{explicit quotient output length is }\Omega(L).} \tag{10}
\]

This refutes the blanket implementation “compute the full Laurent normal form and then prepare its quotient.” It does not refute selective division or a suitably paid compressed representation.

Two further distinctions matter:

* **Ordinary Laurent nondivisibility is not quantitative noncancellation.**  
  \(F=P+L^{-2}\) is not divisible by \(P\), but
  \[
  A^{-1}f=\delta_0+(L^{-2}-i/L)G
  \]
  still approaches \(\delta_0\), and its undeﬂated source LCU still has success \(\Theta(L^{-1})\). Partial deflation, not a binary divisibility test, is needed.

* **Divisibility in the finite torus algebra is different.**  
  In fact \(P(T_x,T_y)\) is invertible for dyadic \(L\). Modulo \(2\), write it as \(I+\mathcal S\), with
  \(\mathcal S=T_x+T_x^{-1}+T_y+T_y^{-1}\). Commutativity and \(L=2^n\) give
  \[
  \mathcal S^L=0,\qquad (I+\mathcal S)^L=I.
  \]
  Thus its integer determinant is odd. Every source has a torus quotient by \(P\); this algebraic fact supplies neither a short quotient nor an efficient preparation.

The missing operation must consequently be **selective, output-sensitive, and quantitatively conditioned**.

## 3. Proved construction: dyadic shells without a shell-normalizer oracle

The geometry can be paid independently of the unresolved source operation.

### Computable partition

Compute a deterministic approximation \(\widetilde p(k)\) satisfying
\[
|\widetilde p(k)-p(k)|\le\eta/16.
\]
Use the partition
\[
\begin{aligned}
\mathcal S_0&=\{|\widetilde p|\le\eta\},\\
\mathcal S_j&=\{2^{j-1}\eta<|\widetilde p|\le2^j\eta\},
\qquad 1\le j\le J=n+3.
\end{aligned}
\]
It covers every mode. Defining
\[
t_j=2^j\eta,\qquad d_0=\eta,\qquad d_j=t_j/4\quad(j\ge1),
\]
gives
\[
|a(k)|\ge d_j\quad(k\in\mathcal S_j). \tag{11}
\]

Using a finite-bit symbol for membership avoids any requirement to resolve exact transcendental boundary comparisons. The inverse amplitude still uses the actual symbol to the separately budgeted accuracy.

### Known-size candidate covers

For a sufficiently narrow shell, use eight signed coordinate sectors. In the sector \(0\le\theta_x\le\theta_y\), near resonance,
\[
\theta_y^{(0)}(\theta_x)=\arccos(3/2-\cos\theta_x).
\]
The dependent-coordinate derivative is bounded away from zero. Therefore every point with \(|p|\le2t_j\) lies within
\[
O(Lt_j+1)
\]
grid offsets of this graph.

A candidate register consists of:

1. a signed sector;
2. an independent coordinate;
3. a padded, power-of-two interval of offsets.

Its known size \(K_j\) satisfies
\[
K_j\le C N t_j
\]
for narrow shells. Reject candidates outside the canonical sector or outside \(\mathcal S_j\). Choose a fixed tie rule on sector boundaries.

On acceptance, the candidate map is injective: the sector, independent coordinate and offset are recoverable from \(k\). They can therefore be coherently erased. The successful, unnormalized state is exactly
\[
\frac1{\sqrt{K_j}}\sum_{k\in\mathcal S_j}|k\rangle. \tag{12}
\]
No value of \(|\mathcal S_j|\) is needed.

For the constant number of wide shells, use the full grid as the candidate set, so \(K_j=N\). Small fixed grids can use this construction throughout. Thus the explicitly computable quantity
\[
\boxed{\mathcal B_L^2:=\frac1N\sum_{j=0}^J\frac{K_j}{d_j^2}
\le C_*L} \tag{13}
\]
has an absolute, constructible constant \(C_*\). The bound follows from
\(\sum_j t_j^{-1}=O(L)\) for narrow shells and a constant wide-shell contribution.

This construction needs \(O(n)\) shells, not an annulus oracle. Cosine evaluation and inversion on the displayed compact argument range can be performed by finite rational approximation and bisection. Graph placement and membership require \(O(n)\) precision bits. Padding covers rounding errors.

## 4. One explicit deflation-and-shell circuit

Suppose preprocessing has produced a polynomial-size explicit \(H\), and rational bounds
\[
b_j\ge\max_{k\in\mathcal S_j}|S(k)|,
\qquad S=F-(P+i\eta)H.
\]
Define
\[
\boxed{\beta^2=\frac1N\sum_j K_j\,\frac{b_j^2}{d_j^2}.} \tag{14}
\]

Prepare shell label \(j\) with amplitude proportional to
\(\sqrt{K_j}b_j/d_j\), then its uniform candidate register. After the geometric acceptance test, rotate a success flag with complex amplitude
\[
\frac{d_jS(k)}{b_ja(k)}.
\]
Its magnitude is at most one. Erase the candidate registers and the shell label on success. The resulting good component is
\[
\frac1{\beta\sqrt N}\sum_k\frac{S(k)}{a(k)}|k\rangle. \tag{15}
\]
Zero-bound shells are omitted; their residual is certified zero.

Let
\[
a_H=\|h\|,\qquad D=a_H+\beta.
\]
Prepare \(h/a_H\) directly from its explicit coefficient list, including its complex phases, and Fourier transform it. Combine this branch with (15), using positive branch weights \(a_H,\beta\). A two-branch LCU then has good component
\[
\frac{\widehat h+\widehat{A^{-1}s}}D=\frac{\widehat u}D.
\]
Therefore its exact success is
\[
\boxed{p_{\rm good}=\frac{\|u\|^2}{(\|h\|+\beta)^2}.} \tag{16}
\]
The final inverse QFT and measurement output the requested lattice site.

This uses no arbitrary-weight source-register uncomputation trick. Arbitrary phases are in the explicitly prepared \(h\) and in the evaluated complex value \(S(k)\).

The easy choice \(b_j=\|s\|_1\) only gives
\[
\beta^2=O(L\|s\|_1^2).
\]
Thus shells alone reproduce the bad global scaling. Deflation must make the residual bounds small enough **and** prevent destructive recombination with \(h\).

For the five-source example, \(H=1\), \(S=-i\eta\), so
\[
\beta^2=\eta^2\mathcal B_L^2=O(L^{-1}).
\]
Equations (2) and (16) then give constant success for sufficiently large \(L\). Every spectral shell is retained.

## 5. Conditional statement: the precise missing source theorem

For this explicit sparse-output route, the remaining theorem is the following.

> **Constructive conditioned deflation theorem — not proved here.**  
> There is a fixed polynomial \(q\) and a no-advice algorithm which, for every native sparse input and tolerance, outputs:
>
> * an explicit Laurent polynomial \(H\), with polynomially many terms and polynomial total coefficient bit length;
> * polynomial-bit rational bounds \(b_j\) valid on the computable shells above;
>
> in total polynomial bit work, including division, coefficient growth, output and certification, such that, with \(S=F-(P+i\eta)H\) and \(\beta\) from (14),
> \[
> \boxed{
> (\|h\|+\beta)^2
> \le q(n,m,B,1/\epsilon)\,\|A^{-1}f\|^2 .
> } \tag{D}
> \]

This is a sufficient remaining theorem for the specified route, not a necessary condition for every conceivable quantum algorithm.

It is deliberately stronger than “the remainder is nonzero” or “the remainder is not divisible by \(P\).” It also controls cancellation between the localized and radiative pieces. Separate lower bounds on their norms would not suffice.

### What would be paid if (D) were proved?

Let \(q=q(n,m,B,1/\epsilon)\). Equation (16) would give \(p_{\rm good}\ge1/q\). Run at most
\[
T=\left\lceil q\log(4/\epsilon)\right\rceil
\]
attempts, returning a fixed site if all fail. The ideal capped failure probability is at most \(\epsilon/4\).

Costs are then explicit:

* **Input:** read the coordinate and rational-weight lists, costing at least \(O(mn+B)\).
* **Source arithmetic:** evaluate the polynomial-size lists for \(H,S\); no QRAM is assumed.
* **Shells:** \(O(n)\) known-size covers, including all off-shell regions.
* **Norms:** \(\|h\|^2\) and \(\beta^2\) are computable from the output lists and known cover sizes. No estimate of \(Z=\|u\|^2\) is used.
* **Precision:** inverse and phase arithmetic require the \(n\) additional bits associated with \(\eta=2^{-n}\), plus coefficient-size and error-budget bits. Precision is not independent of \(n\).
* **Uncomputation:** polynomial evaluation, sector/offset registers and shell labels are erased before accepting.
* **Clock and readout:** \(T\) attempts, inverse QFTs, and a \(2n\)-bit classical output.

If \(B_H\) denotes the output coefficient bit length, a conservative arithmetic width is polynomial in
\[
n+B+B_H+\log(m+\#H)+\log(T/\epsilon).
\]
Approximating the entire capped circuit to trace-distance error at most \(\epsilon/4\) avoids hiding a postselection precision amplification. The resulting TV error is at most \(\epsilon\).

The supplied extracts do not establish (D). Nor do the algebraic examples above disprove it. **This is the universal stopping point.**

## 6. One RESTRICTED family with a complete algorithm

Use the same circuit on the following single source family.

### Promise

In the centered Laurent lift, the input has support in \([-d,d]^2\), where
\[
d\le(n+m+B)^c
\]
for a fixed constant \(c\), and
\[
\boxed{F=PH\quad\text{in }\mathbb Q(i)[X^{\pm1},Y^{\pm1}].} \tag{17}
\]
The quotient \(H\) is **not** supplied. The torus, damping and requested FULL spatial law are unchanged.

### A. Recover the quotient without advice

Perform monic \(Y\)-division of
\[
Y(X^dY^dF)
\]
by \(Q=YP\), then shift the quotient back.

There are \(O(d)\) division steps. Intermediate Laurent \(X\)-degree ranges remain \(O(d)\), so dense storage has \(O(d^2)\) entries. A common denominator for the input has \(O(B)\) bits; repeated multiplication by \(X+X^{-1}-3\) and addition cause only \(O(d)\) further coefficient bits, apart from bookkeeping. Thus division, exact remainder checking and explicit quotient output all cost \(\operatorname{poly}(d,B)\).

Moreover, an extreme \(Y\)-coefficient of \(PH\) comes uniquely from \(YH\) or \(Y^{-1}H\), and similarly for \(X\). Therefore
\[
\operatorname{supp}H\subseteq[-d+1,d-1]^2.
\]
Let \(s=\#\operatorname{supp}H=O(d^2)\), combining torus duplicates if necessary.

### B. Prove conditioning before running the quantum circuit

Here
\[
S=-i\eta H,\qquad u=h-i\eta A^{-1}h.
\]
The exact Fourier identity gives
\[
\|u\|^2=\|h\|^2-\eta^2\|A^{-1}h\|^2. \tag{18}
\]
Translation invariance, (3), and \(\|h\|_1\le\sqrt{s}\|h\|\) imply
\[
\eta^2\|A^{-1}h\|^2
\le\eta^2Z_0\|h\|_1^2
\le\frac{128s}{L}\|h\|^2. \tag{19}
\]

For rational bounds, use
\[
U=\sum_x\bigl(|\Re h(x)|+|\Im h(x)|\bigr),
\qquad U^2\le2s\|h\|^2,
\]
and set \(b_j=\eta U\) for every shell. Then
\[
\beta^2=\eta^2U^2\mathcal B_L^2
\le\frac{2C_*s}{L}\|h\|^2. \tag{20}
\]

All quantities needed for the following tests are explicit rational numbers:
\[
\frac{128s}{L}\le\frac14,
\qquad
\beta^2\le\frac14\|h\|^2. \tag{21}
\]
If both hold, (18)–(20) imply
\[
p_{\rm good}
\ge\frac{(3/4)\|h\|^2}{(3\|h\|/2)^2}
=\frac13. \tag{22}
\]

Run \(O(\log(1/\epsilon))\) capped attempts of the full-shell circuit, with the finite-precision budget described above. This prepares the **full** damped response, not a resonant truncation.

### C. Paid fallback when the tests fail

If either test in (21) fails, (20) implies
\[
L=O(s),
\]
with an absolute constant. Hence \(N=L^2=O(s^2)\).

In this branch, solve the native rational complex linear system explicitly. After multiplying by \(L\) and clearing input denominators, exact rational Gaussian elimination has polynomial bit complexity in \(N,n,B\); determinant bounds keep the resulting rational bit lengths polynomial. Then sample from the exact rational probabilities to TV error at most \(\epsilon\).

A finite-bit inverse-CDF sampler suffices: for a distribution on \(M\) sites, using \(r\) uniform random bits changes the distribution by at most \(M2^{-r}\). This requires no relative accuracy for exponentially small individual probabilities and has a fixed finite clock.

Thus this restricted endpoint has total bit/gate work
\[
\boxed{\operatorname{poly}(n,m,B,1/\epsilon),}
\]
including quotient recovery, all shell work, norms, precision, capped rejection and classical readout.

## 7. The same restricted endpoint has a polynomial classical sampler

This is not an advantage claim.

Let
\[
r=\frac{\eta^2\|A^{-1}h\|^2}{\|h\|^2}.
\]
Equation (18) and
\[
\Re\langle h,u\rangle=\|u\|^2
\]
imply normalized-state fidelity squared at least \(1-r\). Therefore the spatial laws satisfy
\[
\operatorname{TV}(P_h,P_f)\le\sqrt r
\le\sqrt{\frac{128s}{L}}. \tag{23}
\]

A complete classical algorithm is:

* If \(L\ge4\cdot128\,s/\epsilon^2\), sample the explicit distribution
  \(|h(x)|^2/\|h\|^2\), with sampling error at most \(\epsilon/2\).
* Otherwise,
  \[
  N=L^2=O(s^2/\epsilon^4),
  \]
  so use the exact rational full-grid solve and finite-bit sampling.

Both branches are polynomial in the native parameters under the same restricted promise. No Green-function sampler, evaluator or normalizer is assumed.

## Review conclusion and falsifiers

* **Proved:** the five-source LCU normalization is exponentially bad; fixed-width spectral restriction can fail almost maximally for the spatial sample; localized deflation fixes this example.
* **Proved construction:** actual-lattice dyadic candidate covers can be prepared and coherently erased with known sizes. No shell cardinality oracle is needed.
* **Exact counterexample:** unrestricted explicit-list Laurent division can output \(\Omega(L)\) terms from three sources.
* **Conditional:** universal polynomial performance requires a constructive source theorem such as (D). Neither nondivisibility nor a formal spectral partition proves it.
* **Complete restricted result:** polynomial-span undamped quotients are recoverable, admit the full-shell quantum algorithm, and have a polynomial classical match.

For any claimed universal preprocessor, an admissible sequence on which its output length, coefficient bit length, or
\[
\frac{(\|h\|+\beta)^2}{\|A^{-1}f\|^2}
\]
is superpolynomial falsifies that preprocessor. Failed attacks or finite successful grids do not establish a universal theorem or a lower bound.

The unresolved operation is therefore specifically **polynomial-cost, quantitatively conditioned selective deflation of arbitrary sparse Laurent sources**—not Fourier inversion, the number of shells, or an uncharged normalizer.