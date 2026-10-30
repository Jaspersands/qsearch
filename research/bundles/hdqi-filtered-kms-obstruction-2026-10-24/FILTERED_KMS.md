# Two Thermal Comparison Obstructions, Not A Parent Gap Obstruction

Status: LOCAL MATHEMATICAL DEDUCTIONS, NOT INDEPENDENTLY REVIEWED. Exact
rational countercertificates and small physical-matrix controls accompany
the arguments. No new quantum algorithm, classical hardness or novelty
claim is made. The earlier trace-metric lemma is not contradicted.

## Research Decision

The previous thermal-flow bundle ruled out a real-time proof shortcut but
explicitly left coherent Gaussian cancellation open. This pass closes two
specific follow-up shortcuts while keeping the parent-gap question open:

1. Retaining Gaussian phases does NOT give a uniformly vanishing relative
   derivative/filter commutator bound in the SAME KMS gradient metric.
2. The actual filtered parent form does NOT uniformly dominate the RAW
   physical-commutator thermal form, even at arbitrarily small fixed
   beta^2(d+1). This is a different statement in a different metric.

The SAME counterexample family has a parent gap at least 25/36 and a
classical envelope at most 128/127 in the fixed certificate below. Failure
of either stronger comparison therefore cannot be treated as failure of
state preparation. Stop extending these star witnesses after this pass.
The constructive target is a direct filtered-form Poincare inequality
relative to thermal variance, not either disproved comparison.

The Gaussian parent factorization is adapted from known machinery;
[Leng--Jiang--Lin, Appendix A.4.3](https://arxiv.org/html/2604.22996v1)
is the external dependency, not a source for our counterexample.
The broader motivation is the degree-scale preparation question in
[Hastings--Schmidhuber, Section VII.2](https://arxiv.org/html/2610.03697v1).
Neither cited paper is asserted to make the failed comparisons below.

## Input, Algebra And Witness

Keep exactly the earlier public unit-coupling star, with center 0 and
d>=2 leaves. All normalized traces below are over its 2^(d+1)-dimensional
canonical coefficient representation:

    A=O_0=X_0, B_j=O_j=Z_0 X_j, H=A+sum_j B_j,
    C_j=B_1 B_j (j>=2), P=product_(j>=2)(I+C_j)/2,
    w=tau(P)=2^(-(d-1)), S=exp(-beta H/2),
    ||T||_beta^2=tau(S T^dagger S T).

The C_j are independent central involutions. In P's sector, the algebra
is a two-by-two block with A=sigma_x, B_1=sigma_z and H_d=A+d B_1.
Define r=sqrt(d^2+1), h=H_d/r, Y=i A B_1 and R=(d A-B_1)/r.
The new witness W=P R is the previous witness P Y after a quarter rotation.
It is Hermitian, anticommutes with H, has tau(S^2 W)=0 and norm squared w.
Thus its KMS variance equals w. Dividing the KMS inner product by a Gibbs
partition function changes none of the ratios in this note.

For a sector H_a=sigma_x+a sigma_z and traceless Hermitian
T=t_x sigma_x+t_y sigma_y+t_z sigma_z, elementary two-by-two multiplication gives

    ||T||_(beta,a)^2 = t_x^2+t_y^2+t_z^2
       +(t_x+a t_z)^2/(1+a^2) * [cosh(beta sqrt(1+a^2))-1].

Set a=d-2, r_a=sqrt(a^2+1), u=beta r, v=beta r_a.
For partial_i=(I-Ad_Zi)/2 the SAME-KMS gradient of W is E_beta(W)=w G, where

    G = d/2 + d^2/r^2
      + d^2/r^4 (cosh(u)-1)
      + d/(r^2 r_a^2) (cosh(v)-1).

This identity was derived in the previous thermal-flow note and is
independently rechecked here, including its normalization.

## Coherent Filter Still Fails In The Same-KMS Gradient

Let L=ad_H. Consider either the public jump filter or the symmetric filter:

    f_s(z)=exp(-z^2/8-z/4+i s z),
    g_s(z)=exp(-z^2/8+i s z).

Both equal 1 at zero. W has only Liouvillian frequencies +/-2r. Write
b_s=(f_s(2u)+f_s(-2u))/2, with the same definition using g for that case.
The zero-frequency component of [partial_0,f_s(beta L)]W is exactly

    (b_s-1) * P (d/r^2) h.

Proof: partial_0(W)=P(d/r)A=P[(d/r^2)h+(d^2/r^2)R]. The filter sends
R to b_s R plus a multiple of Y; partial_0(Y)=Y has no zero component.
The filter leaves h fixed. Subtracting the two orders gives the expression.
Distinct Bohr-frequency subspaces are orthogonal in the KMS inner product,
since S commutes with H. Also ||P h||_beta^2=w cosh(u). Consequently

    sum_i ||[partial_i,f_s(beta L)]W||_beta^2 / E_beta(W)
       >= (d^2/r^4) cosh(u) |1-b_s|^2 / G.

For all real s, |b_s|<=F=exp(-u^2/2+u/2), for BOTH filters. If u>1,
replace |1-b_s| by 1-F. At beta=c/sqrt(d+1), every fixed c>0 gives
u~c sqrt(d). The lower bound tends to 1, uniformly in s: the third term
dominates G; the fourth is smaller by O(1/d), and F tends to zero.
Thus there cannot be a universal bound B(kappa)->0 as kappa->0 for this
ratio, with kappa=beta^2(d+1). It also fails after any normalized positive
average in s. This is a statement about the SAME-KMS auxiliary gradient,
not the actual parent Dirichlet form.

## Correct Metric For The Actual Parent

The unfiltered physical-commutator reference is

    Gamma_raw(X) = (1/4) sum_i ||[Z_i,X]||_beta^2
                 = sum_i tau(S (partial_i X)^dagger S_i partial_i X),
    S_i = Z_i S Z_i = exp[-beta(H-2 O_i)/2].

The identity follows from [Z_i,X]=2 Z_i partial_i X. Multiplication by
Z_i is isometric in the TRACE norm but is not generally isometric in KMS.
Thus Gamma_raw is a component-dependent two-sided metric, NOT E_beta.

The actual parent from FILTERED_PARENT.md instead has

    B_i(s)=g_s(beta ad_H)(Z_i),
    Gamma_g,s(X)=(1/4) sum_i ||[B_i(s),X]||_beta^2,
    Gamma_g(X)=integral 2 sech(2 pi s) Gamma_g,s(X) ds.

For coefficient vector T, the associated thermal variable is
X=S^(-1/2) T S^(-1/2). Our W anticommutes with H, so
S^(1/2) W S^(1/2)=W: it is also the corresponding coefficient operator.
The executable checks the formula directly against Q_i(s) on W|0>, using
the existing public coefficient-parent formula, not only a thermal rewrite.

Scoped erratum: RELATIVE_FLOW.md writes [n_i,O_i]=-O_i Z_i. The correct
sign for n_i=(I-Z_i)/2 is PLUS, as is the sign of the following displayed
[n_i,L]=J_i O_i Z_i(I-P_i). Its squared Gram bounds and directly computed
executable commutators are unchanged. Earlier hashed artifacts
remain unedited; the correction is recorded and tested here.

## Exact Actual-Form Formula

Define eta=(1+d a)/(r r_a), Delta=r-r_a and Sigma=r+r_a. Then

    L_raw=(1+eta) cosh(beta Delta/2)+(1-eta) cosh(beta Sigma/2),
    L_g=(1+eta) exp(-beta^2 Delta^2/4) cosh(beta Delta/2)
          +(1-eta) exp(-beta^2 Sigma^2/4) cosh(beta Sigma/2),

    Gamma_raw(W)/w = d^2/r^2 + (d/4)L_raw,
    Gamma_g,s(W)/w = d^2/r^2
        + exp(-u^2)cosh(u)sin^2(2us)/r^2 + (d/4)L_g,
    Gamma_g(W)/w = d^2/r^2
        + exp(-u^2)(cosh(u)-1)/(2r^2) + (d/4)L_g.

Center derivation: on this sector Z_0=(d h-R)/r. Gaussian filtering fixes
h and rotates R with magnitude exp(-u^2/2). Commuting with R gives the
Y component of squared norm d^2/r^2 and an orthogonal h component with
the displayed oscillating squared norm.

Leaf derivation: Z_j switches P to a sector with leaf sum a, with the
j=1 sector conjugated by A to the same block. Between the two sectors
the squared energy-eigenvector overlaps are (1+sigma*tau*eta)/2. Each
of the two off-diagonal commutator blocks contributes half the thermal
norm. Since R S_d R=S_d^(-1), their sum is the overlap-weighted sum of
exp(-beta omega/2-beta^2 omega^2/4), with
omega=tau*r_a-sigma*r. Pairing +/- frequencies gives L_g. Removing
the Gaussian gives L_raw. Time phases cancel in these block norms.
The outer density has characteristic function sech(t/4), so the center's
average sine square is (1-sech(u))/2, giving the integrated formula.

Numerical pitfall: use

    1-eta = 4/[r r_a (r r_a+1+d a)],
    Delta = (4d-4)/(r+r_a),

not subtracting nearly equal floating-point numbers. The rare term
(1-eta) is exactly the term that becomes exponentially important.

## Failure Of Uniform Raw-Form Domination

Since exp(-z^2/4)cosh(z/2)<=exp(1/4), both leaf terms give L_g<=2exp(1/4).
The center obeys exp(-u^2)cosh(u)<=exp(1/4). Hence, for all beta,s,

    d^2/r^2 <= Gamma_g,s(W)/||W||_beta^2 <= exp(1/4)(1+d/2).

On the other hand, 1-eta>=2/(r^2 r_a^2) and Sigma/2>=d-1 give

    Gamma_raw(W)/w >= d/(2r^2 r_a^2) cosh(beta(d-1)).

For beta=c/sqrt(d+1), the filtered/raw ratio is therefore
O(d^4 exp(-c sqrt(d))) -> 0, uniformly in s and after the outer average.
No universal positive multiplicative domination of Gamma_raw by Gamma_g
is possible at any fixed positive kappa=c^2. In particular a relative
comparison tending to 1 at small kappa is false.

This is NOT a gap counterexample. W's ACTUAL Rayleigh quotient is at
least d^2/(d^2+1)>=4/5. It rules out using an overstrong reference form,
not a direct lower bound by thermal variance.

## Rational Certificate And Opposite Controls

At d=2^20 and beta=1/8200, kappa<1/64. Use 24 nonconstant even Taylor
terms to lower-bound cosh(beta*d) by T and cosh(beta*(d-1)) by T_leaf.
For u0=beta*d>1, exp[-u(u-1)/2]<=1/[1+u0(u0-1)/2]=F_up.
With A=d^2/r^4, B=d/(r^2 r_a^2), C=d/2+d^2/r^2, the exact bounds are

    same-KMS commutator ratio >= A(1-F_up)^2/(A+B+C/T) > 99/100,
    actual filtered/raw ratio <= [(4/3)(1+d/2)] /
                           [d*T_leaf/(2r^2 r_a^2)] < 1/10^15.

The first lower bound is approximately 0.9997525464; the second upper
bound is approximately 1.294031279e-16. Decisions use Fraction comparisons,
not these decimal approximations. exp(1/4)<4/3 supplies the rational upper.
No dimension-2^(d+1) object is constructed for the certificate.

The earlier mass lemma applies because total squared mass M=d+1. It gives
the SAME parent's gap >=25/36 for kappa<=1/64, along the entire beta path.
The prior classical moment/envelope bound gives C<=128/127. These are
reused results from GAP_AND_BASELINE.md, not fresh gap or sampling claims.

## Adversarial Scope And Next Decision

The witnesses lie in exponentially rare sectors. This is legitimate for
a universal quadratic-form comparison, which quantifies over every vector,
but does NOT establish typical-input hardness or an efficiently observable
signal. The controls are exponential references, not scalable algorithms.
Classical easiness and the positive gap are deliberate opposite controls.

Remaining falsifier of the mathematical deduction: a mismatch in the
two-sector overlap weights, tagged KMS metric or coefficient-parent map.
Independent physical matrices test each, but are not an independent proof
review. The integrated formula is also checked by physical quadrature.

Next constructive question: can filtered local conditional expectations
or a connected-cluster expansion establish a direct VARIANCE inequality
at small beta^2(d+1), with constants uniform in total mass? Before a new
implementation, compare it against the existing classical decoded-output
baselines. A pilot preparation theorem alone is not a new speedup.
Do not respond to this result with more star/seed/temperature sweeps or by
loosening either failed comparison's constants.
