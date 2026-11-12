## Verdict

**The contraction repair is valid for regular models with reduced nodal fibres, with the canonical Arakelov metrics.** Its sharper form is
\[
\boxed{\quad
\frac{I_Y(b,P)}{[L:\mathbf Q]}
\le d\bigl(h_Z(b)-h_Y(b)\bigr)
\le d\,h_Z(b).
\quad}                                                     \tag{1}
\]
Here \(L\) is any field over which the stated models and sections exist. The constants \(1\) and \(d\) are exact; there is no factor depending on the extension degree or number of contractions.

There is an important qualification concerning “including nodes”: **a contraction between regular reduced semistable models does not contract a rational bridge to a node.** Such a contraction leaves the category required by the book. Sections through exceptional tails are fully covered.

I also prove a further, separate estimate for the normalized vertical pole term:
\[
\boxed{\quad
M_Y(\pi)\le d\,\Delta_Y+d\bigl(h_Z(b)-h_Y(b)\bigr),
\quad}                                                     \tag{2}
\]
where \(\Delta_Y\) is the normalized weighted number of nodes. This pays the vertical pole term once \(\Delta_Y\) is paid. It gives a branch-polynomial bound in genus one from the supplied controlled-\(b\) estimate. The branch-only polynomial assertion in arbitrary genus is separated below.

---

## 1. Conventions and the exact contraction identities

Work over \(S=\operatorname{Spec}O_L\), and put \(n=[L:\mathbf Q]\). Assume:

* \(Z\) and \(Y\) are proper regular models of the same smooth geometrically connected positive-genus curve;
* their fibres are reduced, split and nodal;
* \(f:Z\to Y\) contracts the smooth rational \((-1)\)-tails, and \(Y\) is relatively minimal;
* \(\pi_Z:Z\to\mathbf P^1_{O_L}\) is a morphism to the **standard integral target**;
* \(b\) is a section with \(\pi(b)=a\in\mathbf Z\);
* the generic pole divisor is
  \[
  P=\sum_i m_i p_i,\qquad m_i>0,\qquad \sum_i m_i=d,
  \]
  with the \(p_i\) sections after the allowed extension.

Closures on different models are denoted by the same letters when unambiguous.

Use the canonical probability Arakelov measure and the Green function
\(\operatorname{gr}=\log G\), normalized to have mean zero. Define
\[
h_X(b)=\frac1n\widehat{\deg}\,b^*\overline\omega_{X/S}.
\]
With the adjunction Arakelov metric,
\[
(b,b)_X=-(b,\overline\omega_{X/S})_X=-n h_X(b).                \tag{3}
\]
No additive metric-normalization constant is being suppressed.

Finite intersections include \(\log\#k(s)\). Thus, for generically distinct sections,
\[
(b,p)_X=I_X(b,p)-\sum_{\sigma:L\hookrightarrow\mathbf C}
                         \operatorname{gr}_\sigma(b,p).      \tag{4}
\]
The sum is over all embeddings, with conjugate embeddings both counted.

### 1.1 Why nodes cause no omitted case

A section of a regular reduced semistable model cannot pass through a node. Locally at a split node the equation is
\[
xy=\varpi
\]
up to a unit. A section through the node would give both \(v(x)>0\) and \(v(y)>0\), contradicting \(v(x)+v(y)=1\).

If \(E\simeq\mathbf P^1_{k(s)}\) is a fibre component with \(E^2=-1\), then, writing the reduced fibre as \(F\),
\[
0=E\cdot F=E^2+E\cdot(F-E)
\]
gives \(E\cdot(F-E)=1\). Hence \(E\) is a tail. Its contraction is the inverse of a blowup at a **smooth point of the target fibre**.

Blowing up a node instead gives exceptional multiplicity \(2\) in the total fibre, so it does not produce another reduced semistable model. This also explains why a factorization between the models under consideration uses only smooth-fibre-point blowups.

A section may meet \(E\), but it meets it away from its attaching node. That case contributes exactly as follows.

### 1.2 One blowup

Let
\[
f:X'\longrightarrow X
\]
be the blowup of a smooth fibre point \(q\), with exceptional curve \(E\). For a section \(s\), let
\[
\epsilon_s=
\begin{cases}
1,&s\text{ passes through }q,\\
0,&\text{otherwise}.
\end{cases}
\]
A centre met by a section is \(k(s)\)-rational. Write \(w=\log\#k(s)\) for such a centre. The identities are
\[
\begin{aligned}
f^*s&=s'+\epsilon_sE,\\
\overline\omega_{X'/S}&=f^*\overline\omega_{X/S}+E,\\
E^2&=-w,\\
(f^*A,E)&=0,\\
(s',E)&=\epsilon_s w.
\end{aligned}                                               \tag{5}
\]
The exceptional divisor has trivial archimedean contribution. Consequently,
\[
\boxed{
\begin{aligned}
I_X(s,t)-I_{X'}(s',t')
   &=\epsilon_s\epsilon_t\,w,\\
n\bigl(h_{X'}(s')-h_X(s)\bigr)
   &=\epsilon_s\,w.
\end{aligned}}                                               \tag{6}
\]
Thus the proposed “at most” statement is an exact identity followed by
\(\epsilon_t\le1\).

More generally, if \(H\) is an effective horizontal divisor of generic degree \(e\), not containing \(s\), then
\[
I_X(s,H)-I_{X'}(s',H')
   =\epsilon_s\,\operatorname{mult}_q(H)\,w
   \le e\,\epsilon_s w.                                     \tag{7}
\]
Indeed, at a smooth fibre point,
\(\operatorname{mult}_q(H)\le i_q(H,F)\le H\cdot F=e\).
This version does not require splitting \(H\).

### 1.3 Telescoping

For each finite place \(s\), let \(T_s(b)\) be the number of contraction steps over \(s\) whose centre lies on the current image of \(b\). Then
\[
n\bigl(h_Z(b)-h_Y(b)\bigr)
   =\sum_s T_s(b)\log\#k(s).                                \tag{8}
\]
For each pole section,
\[
0\le I_Y(b,p_i)-I_Z(b,p_i)
   \le n\bigl(h_Z(b)-h_Y(b)\bigr).                            \tag{9}
\]

Since \(a\) is integral, its section of the standard \(\mathbf P^1_{O_L}\) is disjoint from infinity. The morphism \(\pi_Z\) therefore gives
\[
I_Z(b,P)=0.
\]
Summing (9) with multiplicities proves the first inequality of (1).

---

## 2. Minimal-height nonnegativity, including genus one

This concerns the **adjunction Arakelov height**, not the Faltings \(L^2\)-height of a differential.

For \(g\ge2\), apply the arithmetic Hodge-index inequality to the admissibly metrized generic-degree-zero divisor
\[
A=(2g-2)b-\overline\omega_Y.
\]
Using (3),
\[
A^2
 =\overline\omega_Y^{\,2}
     -4g(g-1)(b,\overline\omega_Y)\le0.
\]
The minimal-model nonnegativity \(\overline\omega_Y^{\,2}\ge0\), used in the reviewed book proof, gives
\[
h_Y(b)\ge
\frac{\overline\omega_Y^{\,2}}{4g(g-1)n}\ge0.                 \tag{10}
\]
Here the arithmetic Hodge-index inequality is a standard additional theorem being used explicitly; the displayed deduction is elementary.

For \(g=1\), the section makes the generic curve elliptic. On its minimal semistable regular model,
\(\omega_Y=p^*\lambda\), where \(\lambda=p_*\omega_Y\). With the adjunction metric, the discriminant section of \(\lambda^{12}\) has archimedean norm \(1\). For example, on
\(\mathbf C/(\mathbf Z+\tau\mathbf Z)\),
\[
\|dz\|_{\rm Ar}=\frac1{2\pi|\eta(\tau)|^2},
\qquad
\Delta=(2\pi)^{12}\eta(\tau)^{24},
\]
so \(\|\Delta(dz)^{12}\|=1\). The finite discriminant order of a semistable elliptic fibre is its number \(\delta_s\) of nodes. Hence
\[
\boxed{\quad
h_Y(b)=\frac1{12n}\sum_s\delta_s\log\#k(s)\ge0.
\quad}                                                     \tag{11}
\]
This proves the second inequality of (1) in every positive genus.

### The supplied nonminimal falsifier is respected

Blowing up a smooth point on a minimal semistable genus-one model gives
\[
\overline\omega_Z^{\,2}=-\log\#k(s),\qquad
(\omega_Z,E)=-\log\#k(s).
\]
Neither nonnegativity nor relative nefness of \(\omega_Z\) is used above. The proof applies these properties only on \(Y\), then accounts exactly for the exceptional contributions.

### Extension degree

After further field extension, resolving the singularities
\(xy=\varpi^e\) introduced at nodes is crepant. The original section \(b\) avoids those nodes, and its normalized height is unchanged. Archimedean sums repeat with the extension degree, while finite arithmetic degrees scale by that degree. Thus (1) has no hidden extension factor.

This is an existential field-enlargement argument, not an algorithm for constructing the extension or models.

### What fails if singular targets are admitted

Contracting a \((-2)\)-bridge to
\[
xy=\varpi^2
\]
is crepant, so the dualizing-height loss can be zero. The sections
\[
(x,y)=(\varpi,\varpi),\qquad
(x,y)=(c\varpi,\varpi/c),
\]
with \(c\) and \(c-1\) units, have disjoint reductions on the exceptional bridge of the resolution but meet on the singular target. Their naive intersection length there is \(1\).

That is **not** a counterexample to (1): the target is not regular, and those sections are not Cartier at the singular point. It falsifies an extension that silently permits node contractions while retaining the same intersection argument.

---

## 3. The book’s cross-intersection term and its negative sign

Use the supplied global Green lower bound with constants \(C_0\ge1\), absolute, and \(C_r\), depending only on \(r\):
\[
\operatorname{gr}_\sigma(b,p_i)
 \ge \log\operatorname{dist}_{\rm ch}(a,\infty)
       -\log(C_0d)-C_r d^3(d+L_\sigma).
\]
For the integer \(a\),
\[
-\log\operatorname{dist}_{\rm ch}(a,\infty)
   =\tfrac12\log(1+a^2).
\]
Put
\[
\mathcal A_\pi(a)=
\tfrac12\log(1+a^2)+\log(C_0d)
 +C_r d^3(d+\overline L),
\]
where the supplied arithmetic averaging gives
\[
\overline L\le1+r(r-1)(2h_B+\log2).                           \tag{12}
\]
Equations (4) and (9) yield
\[
\boxed{\quad
\frac{(b,p_i)_Y}{n}
 \le h_Z(b)-h_Y(b)+\mathcal A_\pi(a).
\quad}                                                     \tag{13}
\]

For \(D=gb\),
\[
\frac{(D,P)_Y}{n}
 \le gd\bigl(h_Z(b)-h_Y(b)+\mathcal A_\pi(a)\bigr).            \tag{14}
\]
This is the requested cross-intersection bridge.

The reviewed minus sign must be retained. Adjunction gives
\[
-\frac{(D,D-\omega_Y)}{2n}
   =\frac{g(g+1)}2\,h_Y(b).                                 \tag{15}
\]
Combining (13) and (15), for each pole section,
\[
\begin{aligned}
\frac{-\frac12(D,D-\omega_Y)+(D,p_i)}n
&\le g h_Z(b)+\frac{g(g-1)}2h_Y(b)+g\mathcal A_\pi(a)\\
&\le \frac{g(g+1)}2h_Z(b)+g\mathcal A_\pi(a).
\end{aligned}                                               \tag{16}
\]
In genus one the \(h_Y\)-term cancels exactly.

For completeness, define the still-explicit book remainder
\[
\begin{aligned}
\Delta_Y&=\frac1n\sum_s\delta_s\log\#k(s),\\
\Theta_Y&=\frac1n\sum_\sigma\log\|\vartheta\|_{\sigma,\sup},\\
H_{\det,Y}&=\frac1n\widehat{\deg}\det p_*\overline\omega_Y,\\
R_Y&=2g^2\Delta_Y+\Theta_Y+\frac g2\log2+\frac12H_{\det,Y}.
\end{aligned}
\]
For a torsion class satisfying the book’s uniqueness hypothesis for \(D_x\), applying Theorem 9.2.5 separately to the \(p_i\), and then summing, gives
\[
\frac{(D_x,P)_Y+d\log\#R^1p_*O_Y(D_x)}n
\le
d\left[
\frac{g(g+1)}2h_Z(b)+g\mathcal A_\pi(a)+R_Y
\right].                                                   \tag{17}
\]
Replacing a section by \(P\) without multiplying the other terms by \(d\) would be incorrect.

The supplied height estimate may be substituted for \(h_Z(b)\) **on the particular normalization–resolution model to which that estimate applies**. It cannot be asserted for arbitrary additional blowups. The dependence on \(h(a)\) must also remain unless the controlled small choice of \(a\) is actually used.

---

## 4. A further proved bound: the vertical pole budget

Define, on the relatively minimal model,
\[
m_s(\pi)=\max_{C\subset Y_s}\max\{0,-\operatorname{ord}_C(\pi)\},
\qquad
M_Y(\pi)=\frac1n\sum_s m_s(\pi)\log\#k(s).
\]
These are the vertical polar multiplicities and normalized budget relevant to Theorem 9.1.3.

First, contraction itself cannot increase the maximum:
\[
m_s(\pi\text{ on }Y)\le m_s(\pi\text{ on }Z),                \tag{18}
\]
because every component of \(Y_s\) has a strict transform on \(Z\) with the same divisorial valuation. No claim about resolution complexity follows from this observation alone.

There is a stronger useful estimate, namely (2).

### Proof of (2)

Set
\[
u=\pi-(a-1).
\]
The translation is integral, \(u(b)=1\), and \(u\) has the same horizontal poles and the same negative vertical valuations as \(\pi\).

Let \(Q\) be the horizontal closure of the generic zero divisor of \(u\), of degree \(d\). On \(Z\), the sections of the target with values \(a\) and \(a-1\) are disjoint at every finite place. Therefore \(b\) and \(Q\) are disjoint on \(Z\). Formula (7) gives, place by place,
\[
I_{Y,s}(b,Q)\le d\,T_s(b),                                  \tag{19}
\]
where \(I_{Y,s}\) denotes the unweighted intersection multiplicity.

Fix \(s\). Write
\[
\operatorname{div}_Y(u)=Q-P+\sum_C v_C C
\]
near this fibre. On its connected dual graph, let
\[
\alpha_C=Q\cdot C,\qquad \beta_C=P\cdot C.
\]
These are nonnegative, and
\[
\sum_C\alpha_C=\sum_C\beta_C=d.
\]
Intersecting the principal divisor with each component gives
\[
L v=\alpha-\beta,                                          \tag{20}
\]
where \(L\) is the graph Laplacian; self-loops do not affect it.

For any edge with \(v_C>v_{C'}\), take a superlevel cut separating its endpoints. Summing (20) over the high side gives
\[
\sum_{\text{edges crossing the cut}}(v_{\rm high}-v_{\rm low})
 =\sum_{\text{high side}}(\alpha_C-\beta_C)\le d.
\]
Every term on the left is nonnegative. Hence each edge difference is at most \(d\), and
\[
\max_Cv_C-\min_Cv_C\le d\,\delta_s.                          \tag{21}
\]

Let \(C_b\) be the component met by \(b\). Restricting the principal divisor to \(b\), and using \(u(b)=1\), gives
\[
0=I_{Y,s}(b,Q)-I_{Y,s}(b,P)+v_{C_b}.
\]
Consequently, by (19),
\[
v_{C_b}\ge-dT_s(b).
\]
Together with (21),
\[
m_s(\pi)\le d\bigl(T_s(b)+\delta_s\bigr).
\]
Multiply by \(\log\#k(s)\), sum, and use (8). This proves
\[
M_Y(\pi)\le d\Delta_Y+d(h_Z(b)-h_Y(b))
          \le d(\Delta_Y+h_Z(b)).
\]

This proof requires no splitting of \(Q\), no bound on the number of resolution blowups, and no supplied coefficients beyond the hypotheses already stated.

### Genus-one consequence

Equation (11) says \(\Delta_Y=12h_Y(b)\). Therefore
\[
\boxed{\quad M_Y(\pi)\le12d\,h_Z(b)\qquad(g=1).\quad}          \tag{22}
\]
For the supplied controlled choice of \(b\) and its reviewed cover-compatible height bound, this is a polynomial branch-height bound for the **normalized vertical pole budget in genus one**. It does not pay the theta or coordinate-model obligations.

---

## 5. Separate additional conjecture: branch-only vertical bounds in higher genus

The properly normalized assertion is:

> **Vertical-pole-budget conjecture.** For fixed \(r\), there are effective \(C_r,A\) such that every stated degree-\(d\) cover has
> \[
> M_Y(\pi)\le C_r d^A(1+h_B)
> \]
> on its relatively minimal split semistable regular model, independently of the field used to obtain that model.

The preceding lemma reduces this to a polynomial bound for \(\Delta_Y\), together with the supplied controlled-\(b\) bound. In the book’s conventions its Noether formula gives
\[
\Delta_Y
=12H_{\det,Y}-\frac{\overline\omega_Y^{\,2}}n
  -\overline{\delta}_{\rm Fal}+4g\log2
\le12H_{\det,Y}-\overline{\delta}_{\rm Fal}+4g\log2.            \tag{23}
\]
Thus a properly normalized polynomial **lower** bound for the archimedean Faltings delta invariant would complete this particular reduction. The supplied Faltings-height upper bound alone does not provide that lower bound. I do not promote the higher-genus branch-only conjecture from the supplied evidence.

Actual model data giving \(\Delta_Y\) already suffices through (2). Conversely, nothing proved here shows that arbitrary supplied-coordinate height must enter this intrinsic vertical budget.

### A literal, unnormalized multiplicity bound is false

Take
\[
E:y^2=x(x-1)(x-2),\qquad \pi=x/5.
\]
The degree is \(2\), the branch set is
\(\{0,1/5,2/5,\infty\}\), and \(h_B=\log5\). At \(5\), \(E\) has good reduction and \(x\) has vertical order \(0\). After an extension with ramification index \(e\) above \(5\), the good fibre satisfies
\[
m_s(\pi)=e.
\]
After any fixed preliminary extension needed for global split semistability, \(e\) can still be arbitrarily large.

Hence \(m_s(\pi)=O(\operatorname{poly}(d)(1+h_B))\) without ramification normalization is false. Its normalized contribution is instead \(\log5\); this example does **not** refute the conjecture for \(M_Y\).

---

## Scope and remaining gates

The new deductions are the exact contraction/telescoping formulas, (13)–(17), and the vertical-budget estimate (2). The Green estimate and the book theorem with its negative sign are source-dependent supplied inputs; minimal canonical nonnegativity, arithmetic Hodge index, and the genus-one discriminant identities have been identified explicitly.

This is not yet a coordinate-height theorem. In particular:

* the theta supremum remains explicit;
* higher-genus \(\Delta_Y\) has not been bounded here solely from the supplied quantitative inputs;
* Theorem 9.1.3’s étale-closure hypothesis must be checked: splitting supports into sections does **not** make their union étale if contractions make them intersect;
* avoidance of generic poles and the required integral coordinate model still have to be paid.

No construction cost, field-presentation size, numerical precision, or coordinate-output bound is claimed. The existential extensions and models used in the proof are not free algorithmic input.