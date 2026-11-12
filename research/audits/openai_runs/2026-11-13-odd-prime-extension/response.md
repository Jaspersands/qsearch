## Verdict

**The shifted-quotient construction extends to odd \(p\).** In particular, the odd torsion in \(J(\mathbf Q_p)/E\) does not obstruct saturation, and actual representatives need not be torsion points.

Below is a quantified construction, **using the supplied characteristic-zero materializer and Stoll determinant lemmas, and the finite OM/SFL–Okutsu backend specified below**. The substantive odd-prime changes are paid explicitly:

- \([2]\) is an automorphism on the fixed formal subgroup \(E\).
- The formal sampler pays all logarithmic integration denominators.
- The local inverse-function determinant has \(g(A+2)\), not the dyadic \(g(A+1)\).
- The pencil discriminant pays \(N'v_p(N')\).
- The mixed-resultant and Stoll identities use \(v_p(2)=0\).
- Finite-field operations cost polynomial time in \(\log q\); no residue-field enumeration is used.
- A fixed pole cap and an explicit additive DAG ledger prevent an iterative precision explosion.

This is a proof-level composition result from the supplied lemmas and source algorithms. I have not inspected additional repository material or executed controls. It establishes neither the global quantum composition nor a speedup.

---

# 1. Quantified theorem and source boundary

Let
\[
f\in\mathbf Z[x],\qquad \deg f=n=2g+1,\qquad g\ge1,
\]
be monic and squarefree, with coefficient bit length at most \(B\). Let \(p\) be an odd prime, supplied in binary, and \(0<\eta<1\).

There is a bounded randomized classical algorithm which returns either:

1. finite local-field and squareclass-coordinate descriptions for
   \[
   L=\mathbf Q_p[x]/f,
   \]
   together with a basis of the **complete** image of
   \[
   J(\mathbf Q_p)/2J(\mathbf Q_p)\longrightarrow L^\*/L^{\*2};
   \]
   or
2. `ABORT`.

Every returned basis is correct. The probability of `ABORT` is at most \(\eta\). Its bit running time is polynomial in
\[
g,\ B,\ \log p,\ \log(1/\eta).
\]

An explicit, deliberately excessive polynomial clock is given in §9.

### Source premises

The construction uses these supplied results as mathematical lemmas:

- the odd-prime seed determinant and index theorem in `LOCAL_HALVING_SATURATION`;
- the graph-ideal product bound and two-section materializer;
- the characteristic-zero Stoll determinant/resultant identities;
- the OM/SFL factorization algorithm with the complexity stated in supplied Theorem 5.18;
- the supplied Okutsu basis proposition.

The last two are **finite algorithms**, not exact \(p\)-adic oracles. Section 8 specifies how their output is turned into finite field models, actual root selectors, squareclasses, and square roots.

The usual confidence encoding is understood. Reading a longer nonstandard encoding of \(\eta\) must additionally be charged by its actual length.

---

# 2. Native parameters and the fixed quotient

Write
\[
\ell=\operatorname{bitlength}(p),\qquad
\lambda=\lceil\log_2(g+1)\rceil,\qquad
D=v_p(\operatorname{Disc}f).
\]

The discriminant is a nonzero integer. Computing it and determining its \(p\)-valuation require polynomial integer bit work; no integer factorization is needed.

Set
\[
n_s=4g^2,\qquad t_i=p^{n_s}i,\quad 1\le i\le g.
\]
Use the actual near-infinity points
\[
P(t)=\left(t^{-2},t^{-n}\sqrt{F(t^2)}\right)-\infty,
\qquad F(z)=z^nf(1/z),
\]
with the square root congruent to \(1\) modulo \(p\).

Let \(E=L_p\) be their closed \(\mathbf Z_p\)-span. This subgroup is fixed for the entire run.

The supplied odd-prime determinant theorem gives
\[
D_p=
n_sg^2+\sum_i v_p(i)
+\sum_{i<j}v_p(j^2-i^2)
-\sum_{k=0}^{g-1}v_p(2k+1).
\]
It is the exact valuation of the standard logarithmic determinant. Also define
\[
H=
n_sg(g-1)+\sum_{i<j}v_p(j^2-i^2).
\]

For the volume/index bound, take
\[
M=2\lambda+4,\qquad N_c=4D+12,
\]
and
\[
K_{\rm idx}
=
3g+\bigl(D_p+gM+2gN_c\bigr)\ell.
\tag{2.1}
\]
This is an integer upper bound for the number of successful enlargements.

All these quantities are polynomial numerical quantities in the native input parameters. For example,
\[
D_p,\ H=O(g^4+g^2\log(g+1)).
\]

## 2.1 Why the odd part of the quotient is harmless

Put
\[
A=J(\mathbf Q_p)/E.
\]
It is finite. Since \(E\) is a torsion-free pro-\(p\) group and \(p\ne2\), multiplication by \(2\) is an automorphism of \(E\). Consequently
\[
J(\mathbf Q_p)/2J(\mathbf Q_p)\simeq A/2A,
\qquad
J(\mathbf Q_p)[2]\simeq A[2].
\tag{2.2}
\]

More generally,
\[
J(\mathbf Q_p)[2^\infty]\simeq A_{(2)}.
\]
For surjectivity, if \(2^k h\in E\), subtract from \(h\) the unique element of \(E\) whose \(2^k\)-multiple is \(2^kh\). This argument is for proof only; the algorithm never performs this torsion projection.

Let \(r\) be the number of irreducible local factors of \(f\), and
\[
t=r-1.
\]
Then
\[
\dim_{\mathbf F_2}J(\mathbf Q_p)/2J(\mathbf Q_p)=t.
\]

The algorithm builds only a subgroup \(B\subset A_{(2)}\), initially
\[
B_0=A[2].
\]
It does **not** require its actual point representatives to lie in \(J[2^\infty]\).

If \(b\in B\setminus2B\) has zero Kummer label, an actual representative \(h\) satisfies \(h\in2J(\mathbf Q_p)\). Any actual half, including a half after an \(E\)-shift, gives a quotient element \(q\) with
\[
2q=b,\qquad q\notin B.
\]
Its odd-primary component is zero because multiplication by \(2\) is invertible on the odd part of \(A\). Thus adjoining it doubles \(B\) inside \(A_{(2)}\).

This is the required quotient invariant.

---

# 3. An actual formal sampler with an explicit radius

Choose
\[
R=D_p+H+n_s+\lambda+10.
\tag{3.1}
\]
This is intentionally larger than necessary. It ensures
\[
R\ge D_p,\qquad R\ge H+2,\qquad
R>n_s+\max_i v_p(i).
\]

Define
\[
\sigma(z)=
\sum_{i=1}^g
\bigl(P(t_i+p^Rz_i)-P(t_i)\bigr),
\qquad z\in\mathbf Z_p^g.
\tag{3.2}
\]

All the points in this expression are actual points, specified by rational parameters and Hensel-selected square roots.

## 3.1 Logarithmic lattice and denominator payment

For the reversed standard differential basis,
\[
\frac{d}{dt}\log_\omega P(t)
=
-\left(t^{2k}F(t^2)^{-1/2}\right)_{k=0}^{g-1}.
\]
For odd \(p\), the coefficients of \(F(t^2)^{-1/2}\) are \(p\)-integral.

Let \(W\) be the derivative matrix at the \(t_i\). Its entries are integral and
\[
v_p(\det W)=H.
\]
Expanding the logarithmic increments gives
\[
\log_\omega\sigma(z)
=
p^R W\bigl(z+\varepsilon(z)\bigr).
\tag{3.3}
\]
A term of degree \(q\ge2\), after this normalization, has valuation at least
\[
(q-1)R-v_p(q)-H.
\tag{3.4}
\]
Here \(v_p(q)\) is the integration-denominator cost. It has not been treated as zero.

Because \(R\ge H+2\), (3.4) is at least \(1\), and tends to infinity with \(q\). Thus \(\varepsilon\) is a strict integral contraction. The map
\[
z\longmapsto z+\varepsilon(z)
\]
is a measure-preserving bijection of \(\mathbf Z_p^g\).

The points involved lie in the actual Néron \(K_2\), where the logarithm is injective. Therefore
\[
U:=\sigma(\mathbf Z_p^g)
\]
is an actual subgroup, with
\[
\log_\omega U=p^R W\mathbf Z_p^g,\qquad
\mu_\omega(U)=p^{-gR-H}.
\tag{3.5}
\]

If \(V\) is the seed logarithm matrix, its integral adjugate gives
\[
p^{D_p}\mathbf Z_p^g\subset V\mathbf Z_p^g=\log_\omega E.
\]
Hence \(U\subset E\), using injectivity in the actual formal domain—not merely equality of logarithms modulo torsion.

Furthermore,
\[
z\equiv z'\pmod{p^m}
\Longrightarrow
\sigma(z)-\sigma(z')\in p^mU,
\tag{3.6}
\]
and its standard logarithm lies in \(p^{R+m}\mathbf Z_p^g\).

No logarithm or Néron frame is computed by the algorithm.

---

# 4. Haar tail, actual local radius, and finite grid

Set
\[
\begin{aligned}
a_{\rm free}&=3D+10,\\
\Delta_*&=g(1+\lambda),\\
A_{\rm count}&=3g+gM+2gN_c,\\
A_{\rm tail}&=A_{\rm count}+a_{\rm free}+\Delta_*+3+2\lambda,\\
A_{\rm good}&=A_{\rm tail}+1.
\end{aligned}
\tag{4.1}
\]

Let \(\mathcal G_s\) denote the set whose actual reduced divisor has degree \(g\), distinct finite geometric \(x\)-coordinates, and
\[
v_p(x_i)\ge-2s,\qquad
-ns\le v_p(y_i)\le ns,\qquad
v_p(x_i-x_j)\le2s.
\tag{4.2}
\]

Then the supplied Haar proof adapts to give
\[
\mu_\omega\bigl(J(\mathbf Q_p)\setminus\mathcal G_s\bigr)
\le p^{A_{\rm good}-s}.
\tag{4.3}
\]

## 4.1 Changed hypotheses in the Haar argument

The following are the explicit payments.

- The field-type count is
  \[
  4^g p^{gM}.
  \]
  Including chart choices, the supplied cover has volume-count bound
  \[
  8^g p^{gM+2gN_c}\le p^{A_{\rm count}}.
  \]
  These fields and charts are never enumerated.

- For any support field \(E'/\mathbf Q_p\) of degree \(e\le g\),
  \[
  v_p(\operatorname{Disc}E')
  \le e(1+\log_p e).
  \]
  Summing over the support fields gives at most \(\Delta_*\).

- The same-closed-point collision argument still uses embedding **difference linear forms**, not independent conjugates. The embedding-matrix argument bounds their content by half the field discriminant exponent.

- For the plus linear form, the coefficient \(2\) is now a unit. Retaining the older one-digit allowance is safe.

- A degree-two root-tube union contributes a factor at most \(2\le p\). Thus the displayed exponents remain valid.

- Branch tails use the same factorization of \(f(x)\), with integral roots, and the same free-coordinate argument.

This establishes a uniform tail for actual reduced divisors, not merely for a choice of favorable representatives.

## 4.2 Confidence allocation and geometric parameters

Take
\[
T_0=4(K_{\rm idx}+3g+10)^4
\tag{4.4}
\]
and
\[
k=
\left\lceil\log_2(1/\eta)\right\rceil
+
\left\lceil
\log_2\!\bigl(256(n+1)(T_0+1)\bigr)
\right\rceil.
\tag{4.5}
\]

Choose
\[
s=A_{\rm good}+gR+H+2g+2+k.
\tag{4.6}
\]
Since \(2U=U\), for any actual \(h\in2J(\mathbf Q_p)\),
\[
\Pr\left[
h+2\sigma(z)\notin\mathcal G_s
\text{ or some half }q+\sigma(z)\notin\mathcal G_s
\right]
\le
(1+2^{2g})p^{A_{\rm good}+gR+H-s}
\le2^{-k}.
\tag{4.7}
\]
The set of halves is used only in this union bound.

## 4.3 Actual local inverse-function radius

Put
\[
\begin{aligned}
A_{\rm loc}&=4ns+4,\\
K_{\rm ch}
&=g(A_{\rm loc}+2)+s\,g(g-1)+gns+\lceil\Delta_*/2\rceil,\\
Q&=2K_{\rm ch}+1,\\
m_{\rm grid}&=\max(0,Q-R).
\end{aligned}
\tag{4.8}
\]

The change from the supplied dyadic formula is important:
\[
\boxed{g(A_{\rm loc}+2)\text{ replaces }g(A_{\rm loc}+1).}
\]
The denominator \(2y\) no longer contributes a factor of \(p\).

Here is the formal-domain payment. At a good support center \((x,y)\), set
\[
F_x(z)=\frac{f(x+p^{A_{\rm loc}}z)-y^2}{y^2}.
\]
Its degree-\(j\) coefficient has valuation at least \(4j\). Use the smooth affine scheme
\[
2v+p^2v^2=F_x(z)/p^2,
\tag{4.9}
\]
whose \(v\)-derivative is a unit. Its generic fiber maps to the curve by
\[
(z,v)\longmapsto
\bigl(x+p^{A_{\rm loc}}z,\ y(1+p^2v)\bigr).
\]
After \(z=p^2t\), these points are congruent to the center modulo \(p^2\). Weil restriction and the Néron mapping property therefore place the trace-Abel increments in the actual \(K_2\), including for ramified support fields.

Integration loses \(v_p(j)\) in degree \(j\); these losses are bounded exactly as in (3.4), rather than omitted. The derivative determinant has valuation
\[
g(A_{\rm loc}+2)
+\sum_{i<j}v_p(x_i-x_j)
-\sum_i v_p(y_i)
+\frac12\sum_{E'}v_p(\operatorname{Disc}E')
\le K_{\rm ch}.
\]
The integral inverse-function argument then contains
\[
p^{2K_{\rm ch}+1}\mathbf Z_p^g
\]
in the logarithmic image of the support chart.

Consequently, for \(P\in\mathcal G_s\),
\[
e\in K_2,\quad
\log_\omega e\in p^Q\mathbf Z_p^g
\Longrightarrow P+e\in\mathcal G_s.
\tag{4.10}
\]

## 4.4 Exact finite sampling

Sample
\[
z_i\in\{0,\ldots,p^{m_{\rm grid}}-1\}
\]
exactly uniformly. Couple this with Haar \(z\) by reduction modulo \(p^{m_{\rm grid}}\). Equations (3.6) and (4.10) transfer (4.7) to this exact finite grid.

The sample length is at most
\[
g\,m_{\rm grid}\ell
\]
bits, up to a constant overhead. Exact uniform sampling uses bounded rejection from a binary interval; it does not enumerate the grid.

The single-point version works for every incoming \(h\), without a divisibility promise.

---

# 5. Fixed pole cap and canonical materialization

Define
\[
S_{\rm seed}=n(n_s+\lambda)+1,
\qquad
S_0=\max\{1,S_{\rm seed},(6g-3)s\}.
\tag{5.1}
\]
Every stored canonical point must satisfy this fixed pole cap.

For each binary group operation, append \(2\sigma(z)\). The signed graph-block divisor has total degree
\[
m_D\le6g.
\]
Conjugating a negative graph block changes \(b\) to \(-b\). Repeated and coincident supports are allowed.

Use the fixed scaling
\[
X=p^{2S_0}x,\qquad Y=p^{nS_0}y.
\]
The scaled discriminant exponent is
\[
D_{\rm sc}=D+2S_0n(n-1).
\tag{5.2}
\]

All input graph blocks have degree at most \(g\), so their scaled \(b\)-polynomials are integral. On the good event the unknown true output is integral too.

At odd \(p\), the almost-inverse argument actually gives
\[
(\operatorname{Disc}f_{\rm sc})R\subset I I^{-1}\subset R,
\]
because \(2\) is a unit. It is harmless to retain the looser per-stage Smith cap
\[
D_{\rm sc}+2.
\tag{5.3}
\]

The two restriction maps at
\[
N=m_D+g,\qquad N+1
\]
are handled exactly by §6 of the supplied materializer proof. Its Gauss-primitivity argument remains valid: a monic polynomial of odd degree is not a square in \(\mathbf F_p(x)\), regardless of bad reduction.

Thus:

- product ranks are known algebraically;
- product saturation has the bound (5.3);
- accepted RR maps and leading coefficients are unit tests;
- extraction uses monic divisions only;
- scaling back loses at most \(nS_0\) digits.

The algorithm rejects a failed unit test or failed stored pole cap. It does not infer an exact rank drop from an approximate zero.

---

# 6. Scalar pencil: explicit odd-prime bounds

Given the materialized zero-label input \([a_0,b_0]\), let \(e=\deg a_0\), and set
\[
c=\frac{f-b_0^2}{a_0},\qquad
A_u=c-2ub_0-u^2a_0,\qquad
B_u=-b_0-u a_0.
\tag{6.1}
\]
These retain the exact same-class identity.

A sufficient common coefficient pole cap is
\[
S=(n+3)S_0+1.
\tag{6.2}
\]

Choose
\[
\tau=2g+k+\lceil\log_2(8n)\rceil,
\tag{6.3}
\]
and sample one exact uniform
\[
u\in\{0,\ldots,p^{\tau+1}-1\}.
\]

Define
\[
\begin{aligned}
K_{wr}&=gns,\\
K_{aw}&=nS_0+gS+K_{wr}+2g\tau,\\
K_{af}&=D+2nS+2n\tau,\\
K_{\rm disc}
&=(2n-2)S+2g(g-1)s
+n\lceil\log_2 n\rceil+4g\tau.
\end{aligned}
\tag{6.4}
\]

These are deliberately loose nonnegative caps.

## 6.1 Mixed resultant

At a root \(\beta\) of a half polynomial \(W\), put
\[
\mu_\beta=\min\{v_p(c(\beta)),v_p(b_0(\beta)),v_p(a_0(\beta))\}.
\]
Because \(2\) is a unit and \(f=b_0^2+a_0c\),
\[
\mu_\beta\le\tfrac12v_p(f(\beta)).
\]
Hence
\[
v_{G,u}\operatorname{Res}(W,A_u)
\le\tfrac12v_p\operatorname{Res}(W,f)
=v_p\operatorname{Res}(W,R_{\rm half})
\le K_{wr}.
\tag{6.5}
\]

For integrality, use
\[
\operatorname{Res}(p^{S_0}W,p^S A_u),
\]
paying \(dS_0+gS\), where \(d=\deg A_u\le n\). This is included in \(K_{aw}\).

## 6.2 Discriminant leading coefficient

The characteristic-zero identity is
\[
[u^{4g}]\operatorname{Disc}(A_u)
=\pm N'^{\,N'}\operatorname{Disc}(a_0),
\qquad N'=n-2e.
\tag{6.6}
\]
Therefore its valuation is
\[
N'v_p(N')+v_p\operatorname{Disc}(a_0),
\]
not merely the second term.

The cap in (6.4) pays
\[
N'v_p(N')\le n\lceil\log_2n\rceil
\]
and the integral-discriminant normalization \((2d-2)S\).

For the full-degree reset chart, \(e=g\) and \(N'=1\). Nevertheless, the displayed uniform cap correctly covers the more general pencil interface.

## 6.3 Branch resultant and probability

The derivative/Bezout argument gives
\[
v_{G,u}\operatorname{Res}(f,p^S A_u)
\le D+2nS.
\tag{6.7}
\]
Differentiation only multiplies by integers; no derivative coefficient is assumed to be a unit.

For a nonzero polynomial \(P\) of degree at most \(d\) and Gauss valuation at most \(C\), exact uniform sampling modulo \(p^{\tau+1}\) gives
\[
\Pr[v_p(P(u))>C+d\tau]\le d\,p^{-\tau}.
\tag{6.8}
\]
The proof is the root-ball argument from the supplied review, now over \(\mathbf Q_p\).

Apply (6.8) to:

- the mixed resultant for every rational half;
- the source discriminant;
- the source branch resultant.

Their total degree sum is at most
\[
2g\,2^{2g}+4g+2n.
\]
The choice (6.3) makes the union failure probability at most \(2^{-k}\).

No half, root-support field, or scalar grid is enumerated.

---

# 7. Stoll accepted minors and an exact ONE-HALF

Use the supplied determinant identities over characteristic zero. The only valuation change in the Bezout-resultant identity is
\[
v_p(4^g)=0.
\]

Set
\[
\begin{aligned}
D_B={}&K_{aw}+K_{wr}+\lceil K_{af}/2\rceil\\
&+\bigl[g(5g+12)+n+g\bigr]S,\\
S_M={}&(2g+3)S+2K_{wr},\\
K_B={}&(2n+1)S_M+D_B.
\end{aligned}
\tag{7.1}
\]

Then the cleared augmented Stoll matrix has determinant valuation at most \(K_B\) on the joint good event. The same bound controls the nonzero Smith invariants of all truncated Stoll matrices, including monic normalization.

For the final inverse modulo \(W\), take
\[
\begin{aligned}
K_U&=K_{aw}+2K_{wr}+g(5g+12)S,\\
E_U&=(2g+3)S,\\
K_U^{\rm clr}&=gE_U+K_U.
\end{aligned}
\tag{7.2}
\]
Here \(E_U\) clears the multiplication-by-\(U\) matrix modulo \(W\); \(K_U^{\rm clr}\) bounds its determinant valuation.

An attempt does the following.

1. Materialize \(h_z=h+2\sigma(z)\).
2. Perform the finite visible input discriminant and branch tests.
3. Draw the pencil scalar.
4. Compute one actual square root
   \[
   s_{\rm root}^2=(-1)^d A_u\pmod f.
   \]
5. Solve the augmented system with \(w_g=1\), only if its determinant is visible below \(K_B\).
6. Require the fixed coefficient caps and visible nonzero resultants needed for the generic chart.
7. Invert \(U\) modulo \(W\) only with the bound \(K_U^{\rm clr}\).
8. Form
   \[
   Q=[W,-V/U\bmod W],
   \]
   and require the fixed stored pole cap.

The exact congruences and degree bounds imply
\[
V^2-fU^2=(-1)^d A_uW^2.
\]
Together with the accepted coprimality conditions, the divisor identity gives
\[
2Q=h+2\sigma(z).
\tag{7.3}
\]
Thus
\[
2Q-h\in E
\]
in the **original fixed quotient**.

Every inverse is certified nonzero at a fixed precision. An invisible determinant causes `ABORT`, not an exact-zero assertion. On the joint good event, every root choice supplied by the backend satisfies the caps.

---

# 8. Finite native field backend

Only the factors of the degree-\(n\) algebra \(L\) are constructed. The sum of their degrees is \(n\).

## 8.1 Finite field models and actual selectors

Use OM/SFL at an initial precision at least
\[
\nu_0=10n^2(D+1).
\tag{8.1}
\]
For each actual local factor \(F_i\), obtain an irreducible finite polynomial approximation \(P_i\) of the same degree.

It can be used as an exact finite field model
\[
E_i=\mathbf Q_p[\beta_i]/P_i.
\]
The faithful factor approximation identifies an actual root \(\theta_i\) of the original \(f\) in \(E_i\), specified by a finite Hensel selector near \(\beta_i\).

The discriminant bound pays this identification. All roots of \(f\) are integral, and individual root separations and derivative valuations are bounded by \(D\). Precision (8.1) is more than sufficient for the Hensel/Krasner identification. Also, discriminant congruence at precision \(>D\) preserves the relevant factor discriminant valuation.

Compute an Okutsu integral basis in each \(E_i\) using the supplied explicit basis formula. Its power-basis denominators are bounded by the order index, hence by \(D\). The full evaluation map
\[
L\longrightarrow\prod_i E_i,\qquad x\longmapsto(\theta_i)_i,
\]
and its inverse have polynomial, discriminant-controlled denominator guards.

Thus subsequent refinements refer to fixed actual fields and fixed actual roots—not to unrelated approximations.

## 8.2 Odd squareclasses

For \(E_i\) with ramification index \(e_i\), choose an actual uniformizer \(\pi_i\). OM data can supply it. Alternatively:

- compute a \(\mathbf Z_p\)-basis of the kernel of reduction;
- sample a uniform combination modulo \(p\);
- accept exactly when its normalized valuation is \(1\).

The image in \(\mathfrak m_i/\mathfrak m_i^2\) is uniform, so acceptance probability is \(1-1/q_i\ge2/3\). The valuation test uses bounded finite precision.

For every \(\alpha\ne0\),
\[
[\alpha]\longmapsto
\left(
v_{E_i}(\alpha)\bmod2,\quad
\chi_i\!\left(\overline{\alpha\pi_i^{-v_{E_i}(\alpha)}}\right)
\right)
\tag{8.2}
\]
gives two squareclass bits. Here \(\chi_i\) records square versus nonsquare in the residue field.

The reason no deeper unit presentation is needed is exact:
\[
1+\mathfrak m_i\subset E_i^{\*2},
\]
by Hensel with unit derivative \(2\).

Residue square roots are computed by checked randomized finite-field algorithms, for example Tonelli–Shanks with a checked nonsquare. Binary exponentiation costs polynomial time in
\[
\log q_i\le n\ell.
\]
There is no discrete logarithm and no enumeration up to \(q_i\).

For a square \(\alpha\), remove its even valuation, choose a residue square root, Hensel-lift the unit root, and restore the uniformizer power. Store the root selector for consistent refinement.

## 8.3 Valuation guards

If a monic polynomial \(a\) has coefficient poles at most \(S'\) and
\[
v_p\operatorname{Res}(f,a)\le K',
\]
then each component \(\alpha_i=a(\theta_i)\) satisfies
\[
-S'\le v_p(\alpha_i)\le K'+nS'.
\tag{8.3}
\]
Indeed all component valuations have the common lower bound, and their degree-weighted sum is the resultant valuation.

This prevents cancellation in a signed total resultant from hiding an unbounded component valuation.

For initial branch torsion, use the supplied exact branch representative. Its nonzero component valuations are bounded by the factor-resultant contributions to \(D\).

These guards pay valuation discovery, unit extraction, square-root refinement, and CRT conversion.

## 8.4 Source bit cost

Supplied Theorem 5.18 has polynomial dependence on degree, discriminant valuation, requested precision, and \(\log q\). A \(p\)-small operation is charged in bits, not at unit cost; schoolbook residue arithmetic already suffices for a polynomial bound. Valuation scans through finite digit arrays are charged too.

Checked Las Vegas finite-field routines are truncated by independent bounded runs. Doubling an expected polynomial clock gives a completion probability at least \(1/2\) per run; \(O(k)\) runs give failure at most \(2^{-k}\). Refinement inside fixed stored factor/root selectors is deterministic.

This is the source-backend premise. It supplies no additional native input.

---

# 9. Additive DAG ledger and total clock

The remaining composition issue is not resolved merely by bounding output poles. Here is an explicit ledger.

Let \(\Lambda\) be \(100\) times \(2\) plus the sum of
\[
\begin{gathered}
n,B,\ell,k,T_0,D,n_s,D_p,H,R,Q,m_{\rm grid},\tau,\\
S_0,S,D_{\rm sc},K_{wr},K_{aw},K_{af},K_{\rm disc},
S_M,K_B,K_U^{\rm clr}.
\end{gathered}
\tag{9.1}
\]
This is an explicit polynomial numerical quantity in the native parameters.

Use a shared DAG with scalar arithmetic nodes, fixed-field conversion nodes, and Hensel/root-selector nodes. Do not expand it into global rational functions or algebraic-number expressions.

## 9.1 Uniform numerical bounds

The following overbounds suffice:

| Operation | Certified denominator/loss source |
|---|---|
| Seed evaluation | \(n(n_s+\lambda)\) |
| Integral graph product | known-rank minor valuation \(\le12g(D_{\rm sc}+2)\) |
| RR solve/top normalization | unit pivots |
| Scaling back | \(nS_0\) |
| Pencil division | degree \(O(n)\), coefficient cap \(S\) |
| Stoll solve | \(K_B\) after clearing by \(S_M\) |
| Inverse modulo \(W\) | \(K_U^{\rm clr}\) |
| Field/basis/CRT conversion | polynomial in \(n,D\) |
| Component square root | (8.3), with fixed root selector |

Matrices and polynomial degrees are \(O(g)\). Selected subspaces can be represented by minors and adjugates after bounded-pivot selection. Division-free determinant computation avoids introducing uncharged factorial denominators.

With these implementations:

- every intermediate coefficient has pole at most \(\Lambda^4\);
- every scalar actually inverted has valuation at most \(\Lambda^4\);
- the DAG has at most
  \[
  N_{\rm DAG}=\Lambda^{10}
  \tag{9.2}
  \]
  arithmetic/root nodes.

These bounds include polynomially many product stages, matrix formation, adjugates, monic divisions, local-field coordinate operations, and bounded uniformizer powers.

For an arithmetic node, requested output precision \(P\) requires at most
\[
P+C_{\rm loss},\qquad C_{\rm loss}=4\Lambda^4,
\tag{9.3}
\]
input digits. This follows from the usual absolute-precision bounds for multiplication and inversion. A fixed Hensel square-root branch obeys the same bound after its derivative and coordinate-conversion guards are included.

Take
\[
P_{\rm final}=10\Lambda^4+10,
\]
and
\[
P_{\max}
=
P_{\rm final}+N_{\rm DAG}C_{\rm loss}.
\tag{9.4}
\]
In particular \(P_{\max}=O(\Lambda^{14})\).

Evaluate the DAG topologically at the maximum precision requested at each shared node. This is an **additive depth ledger**:
\[
P_{\rm final}+N_{\rm DAG}C_{\rm loss},
\]
not a recurrence replacing one pole bound by a polynomial of the preceding pole bound.

The fixed \(S_0\) is essential. Scaled models and accepted pivot caps do not grow with iteration number.

## 9.2 Bit clock

At precision \(P_{\max}\), coefficient buffers have polynomial bit length, at most \(O(\Lambda^{15})\). Charging:

- input reading and discriminant computation;
- all sampled integers;
- finite-field arithmetic;
- matrix arithmetic;
- native factor/root refinement;
- all input-DAG reevaluation;
- finite coordinate output;

a bound
\[
C_{\rm backend}\Lambda^{80}
\tag{9.5}
\]
bit operations is sufficient with naive arithmetic. The exponent is intentionally excessive. \(C_{\rm backend}\) is a fixed implementation constant for the stated finite source algorithms, not an input-dependent conditioning constant.

A clock overrun returns `ABORT`.

---

# 10. Finite presentation, stopping, and probability

Initialize with the \(t\) actual rational \(2\)-torsion classes obtained from local factors of \(f\), using complements when needed to keep graph degree at most \(g\).

Keep all old generators. When a nonzero class in \(B/2B\) has zero label, select a \(0/1\) representative vector \(v\), assemble an actual representative using the paid shifted group operations, and adjoin the successful half with relation
\[
2q_{\rm new}=\sum_j v_jq_j
\quad\text{in }A.
\tag{10.1}
\]

These triangular relations suffice. No exact equality test between \(p\)-adic points is used. Relations modulo \(2\) and label kernels are ordinary finite \(\mathbf F_2\)-linear algebra.

Every enlargement doubles \(B\), and all half choices differ by the already included \(A[2]\). There are at most \(K_{\rm idx}\) enlargements. The cap \(T_0\) covers the resulting point-operation and presentation work.

When label rank reaches \(t\), those labels span the complete local image, because the latter has dimension \(t\). Completeness is not inferred from sampling coverage.

For each fresh point reset and each scalar pencil, failure is at most \(2^{-k}\), uniformly conditional on the preceding history. Exact-grid rejection and backend truncation receive the same or smaller allocations. With (4.5), the adaptive union bound is strictly below \(\eta\).

On the complement of those failures, every fixed-cap test succeeds. On any other path, accepted algebraic identities still certify correctness; otherwise the algorithm aborts. Thus the algorithm has zero erroneous-output probability.

---

# 11. Audit boundary and falsifiers

The construction has concrete falsifiers, rather than a claim based on unsuccessful attacks:

1. **Sampler:** a violation of (3.4), \(U\subset E\), or the exact congruence coupling (3.6) for the stated \(R\).
2. **Geometry:** a counterexample to the odd-prime Haar or actual-\(K_2\) stability bounds under (4.2).
3. **Materializer:** an accepted unit-kernel computation that fails to represent the signed input divisor class.
4. **Pencil/Stoll:** a violation of the characteristic-zero determinant identities or of the paid resultant caps under their stated generic hypotheses.
5. **Precision:** an accepted inverted quantity exceeding the ledger’s bound, or a stored root selector whose consistent refinement requires more than the stated additive guard.
6. **Backend:** failure of the finite OM/SFL–Okutsu API to meet its stated correctness and polynomial bit-refinement contract.

The last item remains a source/implementation verification obligation, not permission to substitute an exact local-field oracle.

**Conclusion:** the proposed shifted quotient avoids the earlier odd-prime representative problem. With the supplied algebraic lemmas and the explicitly charged finite backend, it yields the requested complete odd-prime local Kummer image algorithm. It does not, by itself, establish the global GRH quantum endpoint, its access/state-preparation costs, or a speedup.