# Finite-grid stability of the dyadic geometric good set

2026-11-13. Independent proof after the stable coordinate-Haar-tail review,
the parent `abel-grid-proposal.md`, STATE/TRAPS and the proved sigma
parameterization. No API, network, Git or numerical experiment. The empty
paid response supplies no mathematical premise.

**Disposition.** The proposed bridge works. A scaled affine etale chart,
followed by Weil restriction and the Neron mapping property, pays the
ACTUAL formal-group domain even for nonintegral support centers. An
explicit inverse-function bound then makes the strengthened good set
invariant under a polynomial-depth subgroup. Coupling Haar parameters
to their residues therefore proves the same good-event probability for
the exact finite integer grid, uniformly in every incoming translate.
No canonical-divisor computation or RR materialization is inferred.

## 1. Strengthen the Haar event to include branch distance

Use all constants of
`2026-11-13-kummer-coordinate-haar-tail.md`, in particular

    n=2g+1,  Delta_*=g(1+ceil(log_2 g)),
    A_tail=A_count+a_free+Delta_*+3+2ceil(log_2 g).

Let `G_s` consist of the points whose ACTUAL reduced degree-`g` divisor
has `g` distinct finite geometric x-coordinates and satisfies

    v(x_i)>=-2s,
    -n s <= v(y_i) <= n s,
    v(x_i-x_j)<=2s  for i!=j.                         (1)

Here `v=v_2`, `s>=0` is integral, and the degree-drop, repeated-support,
infinity and branch loci are excluded. As before their exact algebraic
loci have Haar measure zero; neighborhoods, not this assertion alone,
will pay the finite-grid conclusion.

Set `A_good=A_tail+1`. Then

    mu_omega(G \ G_s) <= 2^(A_good-s).                (2)

Only the additional upper bound on `v(y_i)` needs proof. On an integral
x-free cover chart, `v(y_i)>n s` implies `v(f(x_i))>2n s`.
Factor the monic degree-`n` polynomial in the algebraic closure. Some
root satisfies `v(x_i-theta)>2s`. Freezing all parameter coordinates
but the integral-basis coordinate `1` bounds each tube by
`2^(a_free-2s)`; there are `n` roots. On a y-free chart the bound is
`2^(a_free-n s)`. The infinity region has `v(y)<0`, so contributes
nothing. These arguments apply separately to each embedding of a closed
point; they do not assert independence of conjugates.

The union over at most `g` points has parameter measure at most
`g(n+1) 2^(a_free-s)`. This is no larger than the old safe per-chart
bound `g^2 2^(a_free+Delta_*+3-s)`. The existing area inequality and
chart count therefore prove (2), with the stated extra factor two.

## 2. A uniform local stability depth

Define the following computable integers:

    A=4n s+4,
    K=g(A+1)+s*g(g-1)+g*n*s+ceil(Delta_*/2),
    Q=2K+1.                                         (3)

Let `K_2` denote the kernel of reduction modulo `4` in the ACTUAL Neron
model of the Jacobian over `Z_2`. The standard differential logarithm
`log_omega` is injective on `K_2`. The model and its differential lattice
are used for proof only and are not algorithm inputs.

**Local stability theorem.** For every `P in G_s` and every `e in K_2`
with `log_omega(e) in 2^Q Z_2^g`, one has

    P+e in G_s.                                     (4)

The SAME caps in (1) survive. Whenever `G_s` is nonempty, the proof also
shows that `2^Q Z_2^g` is contained in `log_omega(K_2)`. There is no unspecified
comparison with a Neron differential basis in the numerical value of `Q`.

### 2.1. Scaled support charts and their Taylor estimates

Decompose the good divisor into closed points over fields `E_i/Q_2`,
with total degree `g`. Choose integral bases of their rings of integers;
all choices and fields in this paragraph are proof-only. At one center
`(x,y) in C(E)`, put

    F(z)=[f(x+2^A z)-y^2]/y^2.

Its degree-`k` coefficient, for `k>=1`, has valuation at least

    A k-2s(n-k)-2n s >=4k.                           (5)

This uses the two-sided y bound and the lower x bound in (1), and the
integrality of `f`. The binomial expansions of `(1+F)^(1/2)` and
`(1+F)^(-1/2)` have degree-`k` coefficients of valuation at least `2k`:
the coefficient of the `r`th binomial term loses at most `2r`, with
`r<=k`. Both series are restricted and converge on `O_E`.

Thus

    x(z)=x+2^A z,
    y(z)=y sqrt(1+F(z))                              (6)

are actual points, with the square root taking value `1` at zero.
Throughout this whole parameter ball, `v(y(z))=v(y)` and
`v(x(z))>=-2s`. Across all geometric embeddings, the x increments have
valuation at least `A>2s`, so the pairwise x-difference valuations are
unchanged. Hence every such tuple continues to satisfy (1).

For `omega_j=x^j dx/(2y)`, `0<=j<g`, its pullback coefficient of `z^k`
has valuation at least

    B+2k,    B=A-1-ns-2(g-1)s=(4g+5)s+3.             (7)

Indeed expand `(x+2^A z)^j`, paying the x poles, and multiply by the
inverse square-root series. Termwise integration therefore gives
degree-`q` coefficients of valuation at least

    B+2(q-1)-v_2(q).                                (8)

This explicitly pays the integration denominators. Substituting an
integral-basis expression for `z` introduces integral multinomial
coefficients and integral basis products; taking the trace introduces
no negative valuation. The bounds therefore also hold in the `g`
ordinary `Z_2` parameter coordinates.

### 2.2. Why these are actual points in the injective formal domain

The nonintegrality of the center prevents using an unscaled affine
curve model directly. The following replacement handles it.

Over `O_E` take the affine scheme

    v+2v^2=F(z)/8,

localized where `1+4v` is invertible. By (5), its right side has integral
coefficients. Its derivative in `v` is `1+4v`, so the map to the affine
z-line is etale on this scheme. It is smooth over `O_E` and has the
integral center `(0,0)`.

Its generic fiber maps regularly to `C_E` by

    (z,v) -> (x+2^A z, y(1+4v)).                      (9)

Only this generic morphism uses the possibly nonintegral constants `x,y`.
The equation ensures that (9) lands on the curve. The analytic section
`v=(sqrt(1+F)-1)/4` is integral and restricted. Its degree-`k`
coefficients have valuation at least `2k-2`, so `z in4O_E` implies
`v in4O_E`.

Weil restriction along the finite free ring `O_E/Z_2` is available for
this affine scheme. Its map to affine `[E:Q_2]`-space is etale: formal
etaleness follows by the unique lifting property after base change,
and finite presentation is preserved. In particular this works for
RAMIFIED `E`; no unramified-field promise is being inserted.

Take the product of these restrictions and the generic trace-Abel map

    Phi = sum_i Trace_(E_i/Q_2)([P_i(z_i,v_i)-P_i(0,0)]).

It is a morphism from the smooth generic fiber to `J`. The Neron mapping
property extends it to the smooth `Z_2` scheme. Its integral center maps
to the identity. Consequently parameter points congruent to the center
modulo `4` map into actual `K_2`. This is why we henceforth set `z=4t`
in every integral-basis coordinate.

For clarity, the required logarithm fact does not require a quantitative
Neron-basis comparison. In integral formal coordinates, invariant
differentials are integral; radial integration bounds a degree-`q`
formal-log coefficient below by `-v_2(q)`. On `4Z_2^g`, the normalized
logarithm is `t` plus a strictly contracting restricted integral series.
It is therefore injective there. Changing to the rational basis
`omega_j` is an invertible linear map and preserves injectivity.

### 2.3. Quantitative inverse function theorem

Let

    Psi(t)=log_omega(Phi(4t)).

The actual logarithm is defined by the preceding paragraph. Its
differential and value at zero identify it with the integrated series
in (8). After `z=4t`, a degree-`q` coefficient has valuation at least
`B+4q-2-v_2(q)`. In particular all coefficients are integral and
restricted. Write `Psi(t)=L t+H(t)`, with `H` of order at least two.

Let `d_E` be the discriminant exponent of each support field. The
derivative determinant is, up to sign,

    det L = 2^(g(A+2))
            Vand(x_1,...,x_g) * product_i det(embedding_matrix(E_i))
            / product_(l=1)^g (2y_l).

Its valuation is therefore

    g(A+1)+sum_(i<j)v(x_i-x_j)-sum_i v(y_i)
             +(1/2)sum_E d_E <= K.                  (10)

The last inequality uses (1) and
`sum_E d_E<=Delta_*`, already proved in the Haar review. The determinant
is nonzero; the embedding matrices handle conjugate coordinates exactly.
Since `L` is integral, its inverse has entries of valuation at least `-K`.

On `t=2^(K+1) zeta`,

    Psi(t)=2^(K+1) L [zeta+epsilon(zeta)],

where every coefficient of `epsilon` has valuation at least one and
its degree is at least two. Indeed a degree-`q` coefficient loses at
most `K+(K+1)` and gains `q(K+1)`. It is a strict contraction. Thus
`zeta -> zeta+epsilon(zeta)` is a bijection of `Z_2^g`, and

    Psi(2^(K+1)Z_2^g)=2^(K+1)L Z_2^g
                         contains 2^(2K+1)Z_2^g.    (11)

All corresponding group points lie in `K_2`. Injectivity of the actual
logarithm now identifies a solution of `Psi(t)=log_omega(e)` with the
ACTUAL increment `e`, not a torsion translate. The perturbed support
tuple satisfies (1); with distinct finite x-coordinates it is the
reduced degree-`g` divisor of `P+e`. This proves (4).

## 3. Exact finite-grid coupling, uniform in the incoming point

Retain the actual seed constants and subgroup from the native
perturbation theorem:

    U=sigma(Z_2^g) subset K_2,
    log_omega U=2^R W_seed Z_2^g subset 2^R Z_2^g,
    mu_omega(U)=2^(-gR-H_seed).

The reversed standard differential order is harmless. For Haar-uniform
`z in Z_2^g`, let `z_0` be its coordinatewise representative modulo
`2^m` in `{0,...,2^m-1}^g`. The already proved integral restricted
sigma coordinate map implies

    sigma(z)-sigma(z_0) in 2^m U,
    log_omega(sigma(z)-sigma(z_0)) in 2^(R+m)Z_2^g.    (12)

Both statements concern actual group points. Choose

    m=max(0,Q-R).                                    (13)

Then (4) implies pointwise in this coupling

    h+sigma(z) in G_s  => h+sigma(z_0) in G_s,
    h+2sigma(z) in G_s => h+2sigma(z_0) in G_s.        (14)

The second increment has one extra factor two. The same grid depth
works for both. The discrete `z_0` law is EXACTLY uniform on the finite
integer grid; no claim that its image is itself Haar on `U` is needed.

For an explicit joint halving guarantee, fix ANY actual `h in2J(Q_2)`.
Its rational halves form a set of size at most `2^(2g)`; they are
analysis objects and are never enumerated. For an integer `k>=0`, take

    s=A_good+gR+H_seed+2g+1+k,                       (15)

then compute (3) and (13). Translation invariance and (2) give

    Pr[h+2sigma(z) not in G_s]
       <=2^(A_good+gR+H_seed+g-s),
    Pr[q+sigma(z) not in G_s]
       <=2^(A_good+gR+H_seed-s)

for EACH rational half `q` of `h`. A union bound, with no independence
assumption, is at most

    2^(A_good+gR+H_seed-s)(2^g+2^(2g)) <=2^(-k).

By (14), the SAME bound holds for the exact finite uniform `z_0`.
Thus, uniformly in every such `h`, with probability at least `1-2^-k`,
the point `h+2sigma(z_0)` AND EVERY rational half
`q+sigma(z_0)` satisfy (1). For translates without a halving promise,
the single-point versions of (14) and the preceding probability bounds
remain valid.

All of `s,A,K,Q,m` are polynomial numerical quantities in the paid
native parameters and `k`. The sampled integers have `m` bits each;
neither support fields, charts, Neron data nor rational halves are
constructed or enumerated. Uniformity in `h` allows a union bound over
the already bounded adaptive saturation loop with a logarithmic
confidence allocation per call.

## 4. What this provides to the next interface

On (1), actual Mumford coefficient poles are at most `(6g-3)s`, and

    v Disc(a) <=2g(g-1)s,
    v Res(a,f) <=2g n s.

The analogous bounds hold for every half. These are exactly geometric
inputs for the separately proved pencil/Smith bridge. Any additional
actual formal-group error in `K_2` with standard log depth at least `Q`
also preserves (1), by (4).

This theorem pays the finite-grid probability/stability gate. It does
NOT compute the reduced divisor, select an RR kernel or ideal, certify
that an arbitrary coordinate approximation represents an actual point,
or supply a finite-precision local square-root/halving implementation.
Those constructive interfaces remain separate. No full local-image or
global Selmer algorithm is asserted by this review alone.
