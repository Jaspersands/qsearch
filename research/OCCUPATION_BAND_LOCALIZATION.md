# Occupation-Band Localization with the Cross Block Charged

Status: derived, review pending. No independent proof, formal certificate,
established novelty, efficient algorithm or speedup is claimed.

The separate [low-support](LOW_OCCUPATION_SELECTOR_BOUND.md) and
[high-occupation](MASK_TAIL_FIDELITY_OBSTRUCTION.md) bounds cannot simply be
combined by discarding coherence. Here the actual low/high cross block is
bounded. The result rules out masks with negligible intermediate-band mass
in a particular architecture; it does NOT rule out that intermediate band.

## Claim

Keep the established fixed common-query architecture: even n>=8, G=S_n,
D=n!, one shared uniform fixed-point-free involution h in a class C of size
M=(n-1)!!, standard mixed coset inputs rho_0=I/D and rho_h=(I+R(h))/D,
K copies, a fixed common group-algebra unitary U=sum_g a_g R(g), a fixed
irrep partition with classical source records, and a fixed source-independent
pure selector mask alpha. All physical inputs are discarded, while the
final source/selector POVM is unrestricted. No hidden-correlated prior
transcript or side information is available. Average h AFTER products.

Choose integer thresholds 0<=t<s<=K. Let the low sector contain weights
<=t, the high sector weights >=s, and the middle sector weights strictly
between them. Suppose alpha has middle mass at most pi. Put

    N_L = sum_(i=0)^t binomial(K,i),
    Ebar = M/(M-K),  L=n(n-1)/2,                  assuming K<M,
    B_cross = sqrt((K+2^t-1)/(M-K)) + sqrt(Ebar/M)
        + D sqrt(Ebar)*(4/L)^((s-t)/2)
        + D*(1/L)^((s-t)/2).                                (1)

Let T_low and T_high be valid total class-decision bounds for normalized
masks wholly supported in their respective sectors. The derived bound is

    T_full <= min(1, raw_copy_bound,
        max(T_low,T_high) + sqrt(N_L)*B_cross/2 + 2sqrt(pi)). (2)

For K=n^2, t=n/4 and s=3n, all terms other than 2sqrt(pi) are
superpolynomially small. Thus a nonnegligible total signal requires
nonnegligible middle mass. This is a NECESSARY condition, not an algorithm.
It does not establish a useful final measurement or classical separation.

## Source Norm and Conventions

For source category j define p_j(g)=Tr(P_j R(g))/D, q0_j=p_j(e)>0,
qh_j=q0_j+p_j(h), and q_eta,J=prod_i q_eta,ji. All source masses remain
inside the calculation. As shown in the vacuum note,

    sum_j |p_j(g)|^2/q0_j <= 1/|class(g)|,
    v=sum_j (qh_j-q0_j)^2/q0_j <=1/M,
    sum_J qh_J^2/q0_J=(1+v)^K<=Ebar.                     (3)

The source law is independent of which conjugate h was drawn, but the
noncentral query response generally is NOT. For source vectors use
||x||_w^2=sum_J |x_J|^2/q0_J. The empty query is zeta I, where
zeta=sum_g a_g and |zeta|=1. Also sum_g |a_g|^2=1.

The actual naturally weighted Schur coefficient is

    C_(eta,J)(S,T)=Tr(U_T^dagger U_S sigma_(eta,J)),
    A_J(S,T)=E_h C_(h,J)(S,T)-C_(0,J)(S,T).

The double expansion has coefficient a_g*conj(a_g'). Here g is the
LOW-side S index and g' the HIGH-side T index. Its local factors are

| Position | Factor |
|---|---|
| in S only | p_(eta,j)(g) |
| in T only | p_(eta,j)(g'^-1) |
| in both | p_(eta,j)(g'^-1 g) |
| in neither | q_(eta,j) |

In the implementation, rows are g', columns g, and the product table entry
is g'^-1 g. Swapping coefficient conjugation does not give the same column
for the dense complex noncentral controls.

## Four Terms in the Actual Cross Coefficient

Set L_(eta,J)(S)=Tr(U_S sigma_(eta,J)). Split the HIGH-side index g'
into e, h (under the alternative only), and the remainder. Then

    A_J(S,T) = conj(a_e)*[E_h L_h,J(S)-L_0,J(S)]
             + E_h [conj(a_h)*L_h,J(S)]
             + alternative_off_endpoint_J
             - null_off_endpoint_J.                         (4)

The e endpoint is immediate. For g'=h, R(h)rho_h=rho_h and cyclicity
of the trace remove R(h) on every T position, INCLUDING overlapping
positions. The source projectors commute with R(h). For example,
Tr(R(h)R(g)P_j rho_h)=Tr(R(g)P_j rho_h). The remaining expression is
L_h,J(S), not a response involving all of T.

The endpoint with a_h is an average of a PRODUCT. It cannot be replaced
by E_h conj(a_h) times E_h L_h,J(S). The query is fixed before inputs,
but these two quantities both depend on the shared hidden member.

### Endpoint Bounds

The first term is conj(a_e)/conj(zeta) times the vacuum column A(S,empty).
For |S|<=t its source norm is at most

    sqrt((K+2^t-1)/(M-K)),                                  (5)

by the compressed-input chi-square argument already established. This
compresses ONE entry, not the entire mask channel.

For each h, positivity gives |L_h,J(S)|<=qh_J, hence
||L_h(S)||_w<=sqrt(Ebar). Consequently

    ||E_h conj(a_h)L_h(S)||_w
       <=sqrt(Ebar)*E_h |a_h| <=sqrt(Ebar/M).                (6)

The last step uses uniform class averaging and sum_g |a_g|^2=1. It is not
a pointwise bound on a chosen coefficient a_h.

### Off-Endpoint Bounds

If g' is outside {e,h}, both g'^-1 and h g'^-1 are nonidentity. Every
nonidentity conjugacy class has size at least L for n>=8. Equation (3) and
the squared triangle bound therefore give

    sum_j |p_j(g'^-1)+p_j(h g'^-1)|^2/q0_j <=4/L.           (7)

All other local factors have source-weighted squared norm <=1+v, since
|p_(h,j)(x)|<=qh_j. Let b=|T minus S|. Factorization over positions bounds
the norm of each alternative product by
(4/L)^(b/2)*(1+v)^((K-b)/2). Triangle inequality and
sum_(g,g') |a_g a_g'| <=D give

    ||alternative_off_endpoint||_w
       <=D sqrt(Ebar)*(4/L)^(b/2).                          (8)

For the null, the exclusive factor has squared norm <=1/L, and every other
factor has norm <=1. Thus the null counterpart is <=D*(1/L)^(b/2).
Because b>=s-t and L>4, these decrease to the bounds in (1).

Only HIGH-EXCLUSIVE positions supply this uniform decay. On an overlapping
position, g'=g can give g'^-1 g=e and hence no decay at all. Counting all
of T, the whole union, or all overlapping positions here is invalid.
Combining (5)-(8) bounds ||A(S,T)||_w by B_cross for every low/high pair.

## From Entries to the Full Cross Block

First suppose the middle mass is zero. Write the mask as
sqrt(w_L) beta_L + sqrt(w_H) beta_H, with w_L+w_H=1 and normalized beta
supported in the indicated sectors. In source block J, the rectangular
output difference between the sectors is

    X_J=diag(alpha_L) A_J(L,H) diag(alpha_H)^dagger.

Its rank is at most N_L, regardless of the high-sector dimension. Also

    sum_J ||X_J||_2^2/q0_J
       <= w_L w_H B_cross^2.                               (9)

This exchanges mask probabilities with the source sum, so the mask must
be source independent. Rank comparison and weighted Cauchy give

    sum_J ||X_J||_1 <=sqrt(N_L w_L w_H)*B_cross
                     <=sqrt(N_L)*B_cross/2.               (10)

The Hermitian completion [0 X; X^dagger 0] has HALF trace norm ||X||_1,
so there is no extra factor two in (10). The pinched diagonal contribution
is w_L*T(beta_L)+w_H*T(beta_H)<=max(T_low,T_high). Triangle inequality
proves (2) for zero middle mass, retaining actual cross-sector coherence.

For middle mass pi_actual<=pi, the projector removing the middle has
failure probability pi_actual under BOTH hypotheses: output selector
diagonals have the input mask probabilities. Gentle projection contributes
at most sqrt(pi) per hypothesis in half trace norm, hence 2sqrt(pi) total.
The retained subnormalized mask contributes at most its normalized version,
so no division by a rare source probability or uncharged success factor is
introduced. This proves (2).

For completeness, the unnormalized gentle inequality can be checked on a
purification: the norm of the difference between a pure state and its
projected subnormalized state is sqrt(4pi_actual-3pi_actual^2)<=2sqrt(pi).
Partial trace contracts the trace norm. This is a standard gentle-projection
argument, not a new general quantum-information theorem.

## Scaling and Implementation

For K=n^2 and t=n/4, log N_L<=(n/4)log n+O(n). The first two cross
terms after sqrt(N_L) are negligible because M=exp((n/2)log n+O(n)).
For s=3n, b>=11n/4: even the D coefficient cost in (8) is dominated by
this decay after charging sqrt(N_L). The previous low and high bounds
are also negligible in these regimes.

Outward-rounded INTEGER envelopes are:

| n | pi | Cross contribution | Whole distance bound |
|---|---|---|---|
| 128 | 0 | not evaluated; low bound already vacuous | 1 |
| 1024 | 0 | 2^-344 | 2^-216 |
| 4096 | 0 | 2^-2395 | 2^-1883 |
| 4096 | <=2^-4096 | 2^-2395 | 2^-1883 |
| 4096 | <=1/4 | 2^-2395 | 1 |

These are conditional bound evaluations, not simulations at these degrees.
The implementation may replace a very large s by min(s,3n) for the high
tail comparison and a large s-t by min(s-t,4n) in (8). Both changes WEAKEN
decreasing bounds, and avoid exponentiation by the total copy budget.
The declared thresholds and evaluated thresholds are reported separately.
If the low bound is already vacuous, no composite improvement is claimed.

## Falsifiers and What Remains

Direct regular-basis S3 K2,3 and fixed-point-free S4 K2 controls independently
rebuild all 32 ordered cross pairs with |T|>|S| from the double character
kernel. They retain every source tuple and every hidden member, including
overlap and disjoint cases. All four weighted component bounds and the
high-side endpoint identities are checked. Forty-eight mask probes check
the pinched distance, the ACTUAL rectangular block norm, and its rank charge.
Positive finite cross-sector gains remain; this is not a zero-gain identity.

An exact S6 countercontrol uses the coefficient g'=g=v of the valid unitary
(I+iR(v))/sqrt(2), with v a fixed-point-free involution and h!=v. For
S={0},T={0,1}, the squared source norm is (16/15)*r_h(v), while falsely
charging overlap as another exclusive factor predicts r_h(v)^2. All 14
hidden members distinct from v strictly separate these quantities. These
are checks of a real coefficient mechanism, not invented oracle candidates.

The generic counterexample in the low-support note, where separate sectors
fail but their superposition succeeds, remains valid. What closes the
specified escape HERE is the new physical cross bound, not dephasing or a
general principle that sector information is additive.

The most important limitation: necessary middle mass does NOT justify
projecting the search onto the middle sector alone. Information may reside
in coherence between the middle and outside sectors. Nor can one restrict
to a single weight. Radialization of probabilities remains available only
with its existing covariance/unrestricted-measurement assumptions.

The intermediate occupation band, source-adaptive masks, useful retained
physical data, and multiple queries remain unresolved. The missing-harmonic
span measurement of [Moore and Russell](https://arxiv.org/html/quant-ph/0504067)
is not implemented by this discarded-input channel and is not ruled out.
Standard norm inequalities and character orthogonality may make the scoped
result a known or straightforward consequence of prior work; novelty and
independent proof review are still required. Do not count another restricted
bound as evidence that a breakthrough algorithm is near.

Implementation: `theorems/coset_mask_cross_sector.py`,
`source_selector_occupation_band_contract` in `core/isotypic_instruments.py`,
and `tests/test_coset_mask_cross_sector.py`. The existing binary-instrument
CLI/report records the separated-sector obstruction and keeps the
intermediate-band gate false. Next evaluate the unresolved band's actual
operator structure or a retained-physical primitive, not new phase-only
mutations inside an already excluded regime.
