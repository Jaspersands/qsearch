# Inverse Trace: Ray-Class Scope And A Direct HSP Barrier

29 October 2026. Mathematical sidecar; no implementation or quantum-algorithm
claim. The new bounded-effective-divisor reduction received **independent
automated review by Kierkegaard**, with the scalar-normalization wording fix
below applied. This is not human peer review or proof-assistant/kernel
verification. Known principality algorithms do not establish the required
selection algorithm. No hardness, novelty, or uniform-sampling claim is made.

## Native Relation And Exact Polynomial Lift

Keep the original distinct points alpha_i in k=F_q, q=2^n with odd prime n,
N=n^2 and K=floor(N/8). The relation is Hx=0, H_(j,i)=alpha_i^j for
0<=j<K, and Tr(inv0(x_i))=b_i, with inv0(0)=0. Put
P=prod_i(X-alpha_i), D=P', and r=N-K-1. Choose the Artin-Schreier-reduced
polynomial C with Tr(C(alpha_i))=b_i, as in
[Sparse Targets](INVERSE_TRACE_NORM_ATTACK.md#sparse-targets-exact-remaining-problem-and-a-failed-extension).

Native search is exactly the following polynomial search:

\[
\deg A\le r,\quad \deg U<N,\quad
U^2+UA+CA^2\equiv D^2\pmod P,\qquad
A(\alpha_i)\ne0\quad\text{if }b_i=1.
\]

The output is x_i=A(alpha_i)/D(alpha_i), **without squaring** and without
changing the evaluation points. Weighted interpolation identifies deg A<=r
with Hx=0. At A_i!=0, division by A_i^2 gives
x_i^(-2)=(U_i/A_i)^2+U_i/A_i+C_i, proving the required trace. At A_i=0
the congruence forces U_i=D_i; the output zero is allowed only if b_i=0.
Conversely, a native word determines A. For x_i!=0 the equation
z_i^2+z_i=C_i+x_i^(-2) has exactly two roots; choose one and set U_i=A_i*z_i.
For x_i=0 set U_i=D_i. Interpolation gives deg U<N. These operations are
polynomial-time. Omitting the one-target nonvanishing condition admits the
unhelpful solution U=D,A=0.

## Pole Bound And Residue Image

Assume C has positive odd degree 2g+1 and g>=K, the failed extension's
regime. Let Xcal be the smooth projective curve of Y^2+Y=C(X), with
involution sigma(Y)=Y+1. It has genus g and one rational infinite place O;
-v_O(X)=2 and -v_O(Y)=2g+1. Its affine coordinate ring is k[X]+k[X]Y.
Set d=2r+2g+1. The opposite parities of the two pole orders imply

\[
L(dO)=\{U+AY:\deg U\le r+g,\ \deg A\le r\}.
\]

Since r+g>=N-1, every native lift above belongs to this space. Conversely,
reducing U modulo P preserves the congruence and A. Thus this pole bound
does not restrict native support when g>=K; no such equivalence with this
particular pole bound is asserted for g<K.

Let M be the reduced pullback of the N evaluation places. It has degree
2N and M=div(P)+2NO. Evaluation at M has kernel P*L((d-2N)O).
Here dim L(dO)=2N+g-2K, while d-2N=2g-2K-1 admits only X^j with
0<=j<=g-K-1, giving kernel dimension g-K (zero when g=K). Consequently
the residue image has **exact dimension 2N-K**, hence codimension K.
Increasing genus does not make this evaluation map surjective.

## Ray Convention And Bounded Effective Selection

Write R=prod_i R_i, R_i=k[Y]/(Y^2+Y-C(alpha_i)), and
T=ker(N:R^* -> (k^*)^N). The algebra R_i is k x k when b_i=0 and F_(q^2)
when b_i=1; the corresponding norm-one groups have orders q-1 and q+1.

Use the **additive, positive-divisor convention**
Pic_M^0=Div_M^0/{div(f):f|_M=1}. For a in R^*, choose a function f regular
and invertible at M with f|_M=a, and define delta(a)=[div(f)]_M.
This is independent of the lift and satisfies delta(ab)=delta(a)+delta(b).
Its kernel is precisely the diagonal k^*: constants have zero divisor,
and equality modulo a function with residue 1 leaves only a global constant.
Thus delta factors injectively through R^*/k^*, not through a quotient by
independent coordinatewise constants. The restriction delta|_T is injective:
a diagonal constant in T has c^2=1, hence c=1 in characteristic two.
An opposite-sign convention for delta would reverse the sign below.

The independently automated-reviewed reduction asks for E and t satisfying

\[
E\ge0,\quad\deg E=d,\quad\operatorname{supp}(E)\cap M=\varnothing,
\qquad [E-dO]_M=\delta(Dt),\qquad
t\in T,\quad t_i\ne1\ \text{whenever }b_i=1.
\]

**E may contain O.** If h has pole order e<=d, its associated divisor is
E=div(h)+dO=(h)_0+(d-e)O. Excluding O would incorrectly require exact
pole order d and discard lower-degree witnesses. No monicity is imposed.

To prove the forward direction, take a native lift h=U+AY, let t=h/D at
M, and use its norm congruence. For the converse, the ray equality implies
that E-dO is principal. Compute a nonzero h0 in L(dO-E); its divisor is
exactly E-dO, and this space is one-dimensional. The equality of ray
classes implies h0|_M=cDt for **one** c in k^*. Set h=h0/c. Given the ray
equality, this same scalar can alternatively be recovered because all
ratios N(h0_i)/D_i^2 equal the same gamma=c^2; the unique square root in k
recovers c. Equal norm ratios alone do not identify the prescribed t.
Independent local rescalings are not permissible.
Now h belongs to L(dO), has residue Dt, and yields the required U,A.

For t_i=u_i+a_i Y of norm one, t_i+sigma(t_i)=a_i, so
x_i=a_i=t_i+t_i^(-1). Also a_i=0 iff t_i=1. Therefore exclusion of the
identity is required at one-targets and must NOT be imposed at zero-targets.
The condition t in T already makes every local component a unit.

This is a selection problem for E with its ray and local restrictions,
not just class membership for an E already supplied. Ordinary effective
representatives in a Jacobian can be computed using Riemann-Roch; that
fact does not supply this constrained representative. All generators of
a fixed affine principal ideal differ only by k^*: a unit has divisor
supported at O, hence zero divisor. There is no nonconstant affine unit
available to shorten its generator. Once the correct E is supplied,
bounded-height Riemann-Roch and the normalization above suffice classically.

## Direct Odd-Order Inversion Barrier

The natural proposed HSP oracle is S:T -> k^K, where
S_j(t)=sum_i alpha_i^j*(t_i+t_i^(-1)). Its zero condition is exactly the
K degree constraints on interpolated A. T has odd order and
S(t)=S(t^(-1)). If S hid a subgroup J, equality of these two outputs
would force t^2 in J for every t. Squaring is bijective on T, so J=T;
S would be constant. It is not: choose a nonidentity element in one
coordinate and identities elsewhere. Its trace t_i+t_i^(-1) is nonzero,
so the zeroth syndrome differs from S(1)=0.

Thus this oracle's fibers are not a subgroup-coset partition. Appending
the local nonvanishing flags retains inversion invariance and nonconstancy,
so does not repair it. This excludes the direct abelian-HSP invocation,
not every possible quantum reduction or a differently constructed oracle.

## Primary Sources And Paid Scope

- [Kedlaya, Quantum computation of zeta functions of curves](https://arxiv.org/pdf/math/0411623):
  Theorem 1 is polynomial in g and log q for an explicitly represented
  smooth projective geometrically irreducible curve; Section 6 specifies
  the plane-model input and effective arithmetic. Lemma 10 constructs
  generators under sqrt(q)>16g; Proposition 11 uses that condition over
  the chosen constant field. It eventually holds here with g=Theta(N),
  but fails at n17,g143. The zeta theorem is not a ray-representative theorem.
- [Eisentrager--Hallgren, Computing the unit group, class group, and compact representations in algebraic function fields](https://msp.org/obs/2013/1-1/obs-v1-n1-p17-s.pdf):
  Theorems 5.1--5.3 concern units, principality and ideal class groups;
  principal ideals are supplied in HNF, with valuation/compact output.
  Section 2 assumes an explicit function field with full constant field
  k and a degree-one infinite place. Appendix A invokes Kedlaya's generator
  condition and discusses constant extension. Theorem B.9 concerns
  classical Riemann-Roch computation with explicit divisor data and charged
  height. Here O is already rational. Any constant extension used for
  computation still requires descent; an extension-field witness is not
  a native answer.

Group generators, relations, coherent arithmetic, residue maps and source
preparation must all be charged, with g growing rather than fixed. Even
granting polynomial-cost ray-group access does not supply the selection
step. A hypothetical bounded-selection solver would cost
T_presentation+T_selection+poly(N,n,g); this is a conditional accounting,
not a constructed algorithm. Local arithmetic and the syndrome oracle
need polynomial-size finite-field circuits, not enumerated field tables.
Verify the explicit output by checking degrees, the norm congruence,
one-target nonvanishing, and every original parity and trace equation.
No rejection-counting result or claimed quantum speedup is added here.
