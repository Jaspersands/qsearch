# Three-Point Anisotropic Residual Decoding

2026-10-20. LOCAL DERIVATION REVIEW PENDING. Known DQI, finite-field Gauss
sums and collaborative Reed-Solomon decoding ingredients. No novelty,
classical hardness or quantum speedup is claimed.

Producer: `theorems/cubic_orbit_decoder.py`.
Tests: `tests/test_cubic_orbit_decoder.py`.
Artifact: `research/phase_workbench/cubic_orbit_decoder.json` (schema v2).

## Research Decision

The paired candidate now has a real adaptive classical baseline,632/1026
(and 633/1026 after re-anchoring), not merely an interpolation witness.
It still needs a stronger portfolio. That score does NOT transfer to the
new task below.

Fixing one of its E/O components gives reflection-symmetric value lists
of typical size about p/2. The standard dense-list interpolation sufficient
condition scales as agreement > sqrt((K-1)*sum_i |L_i|), which is generally
vacuous at these parameters. This observation does not rule out specialized
list recovery, soft weights or optimization of just one witness.
See [Koetter--Vardy](https://www.site.uottawa.ca/~zhcheng/RS_soft_decision.pdf).
No new list-recovery impossibility result or solver is claimed.

Instead of a seed campaign, this pass tests a constructive question:
can three collaborative rows come from ONE original polynomial syndrome,
with a provable actual source law, without introducing obvious local
accepted affine lines? The answer supplied here is a local derivation plus
exact algebraic/basis controls and a matched 3-point intrinsic-manifold
classical baseline, still awaiting independent review.

## Explicit Changed Problem

Let p=1 mod3 be an odd prime, zeta a primitive cube root in F_p, and eta a
nonsquare. Partition nonzero evaluation points into disjoint ordered orbits

    (a_i, zeta*a_i, zeta^2*a_i),  i=1,...,M.

The reference chooses the least unused a_i, in ascending order. Cubes
z_i=a_i^3 are distinct. Public inputs are nonzero b_i and explicit halfsets
F_i of size(p-1)/2. Return ONE polynomial deg(P)<n=3K maximizing

    S(P) = sum_i 1[r_i(P) in F_i],
    r_i(P) = P(zeta^2*a_i)
             + b_i*(P(a_i)^2-eta*P(zeta*a_i)^2).

This is not the published overlapping chain, the earlier paired task, or
the coefficient-square restriction in quadratic OPI. All input tables are
public; no membership-oracle lower bound applies. There is no reduction to
a recognized hard task or proof that this purpose-built task is natural.

The native control uses p2053,M684,n204 and the first684 public halfsets/
multipliers from the frozen RDQINumerics reference. The changed pairing,
dimension, complete orbit map and source provenance are saved.

## Actual Source And Deterministic Preparation

Write rho=|F_i|/p and h_i(r)=(1[r in F_i]-rho)/sqrt(rho*(1-rho)).
The independent three-variable source predicate is
h_i(z+b_i*(x^2-eta*y^2)). For normalized Fourier coefficients with negative
exponent, the coefficient at(u0,u1,v) is zero if v=0. Otherwise it is

    -hhat_i(v)/p *
      exp(2*pi*i*(-u0^2+eta^(-1)*u1^2)/(4*b_i*v*p)),

where field division and reduction modulo p precede the exponential.
The two quadratic Gauss factors multiply to chi(eta)=-1.
Thus conditional on any v!=0, u0,u1 are independent UNIFORM field elements;
v follows the actual fixed-table law |hhat_i(v)|^2. The three folded rows
below are NOT independent uniform rows.

The coherent phase matters. Removing the minus sign leaves all local
sampling probabilities unchanged but multiplies every active orbit by -1.
Across a superposition of shell weights this changes the state. The
source-phase control checks COMPLEX amplitudes against a direct 3D FFT and
checks that omitting the sign makes the empty-plus-active test orthogonal.

This is important prior-art hygiene:
[Cohen Hillel v2](https://arxiv.org/html/2510.08061v2) explicitly flags an
exponentially unlikely Step7 postselection that invalidates its proposed
general quadratic-DQI algorithm. We do not use that step or claim to repair
that paper. Our source is a restricted disjoint-block construction with
orthogonal inactive/active labels and an explicit reversible phase.

## Three Rows From One Syndrome And Correlated Rank Bound

For an active orbit let its three Fourier frequencies be u_i0,u_i1,v_i.
The original polynomial syndrome has n entries

    s_k = sum_(i,l) u_il*(a_i*zeta^l)^k.

Split this ONE vector by k mod3:

    A_ir = sum_l u_il*(a_i*zeta^l)^r,  r=0,1,2,
    s_(3j+r) = sum_i A_ir*z_i^j,       0<=j<K.

These are three shared-support Prony sequences ([Schmidt--Sidorenko--Bossert](https://arxiv.org/abs/cs/0610074),
[Yu--Loeliger](https://arxiv.org/abs/1612.07854)). Existing `decode_burst`
performs cap-rank checking, locator recovery, root search, value recovery
and whole-syndrome replay.

Assume m divides p-1, n=mK, source support size <=D, decoder cap C>=D, and
L=n-mC>=D. For a nullvector of exact support T, |T|=t:

    r_t = rank(A) = min(L,(m-1)t),
    rank([A B]) = min(L,mt),
    d_t = t-min(L,mt)+r_t,
    epsilon <= sum_(t=1)^D binom(D,t) * (p^d_t-1)/[(p-1)*p^r_t].

Use C=D+1 for the observable guard so accepted source and target score
operators agree exactly.

## Completed Native Evidence And Three-Point Classical Intrinsic Portfolio (Schema v2)

At p2053,M684,n204,D50,C51 the saved rational guide gives:

| Quantity | Conservative Value |
|---|---|
| Source mean fraction | 0.7424410733674203 |
| Source rank-failure mass upper | 2.432249869275868e-7 |
| Ideal one-attempt mean, ABSTAIN scored0 | 0.7419477144537232 |
| Ideal one-attempt probability of score>=493/684 | >0.08068 |
| Generic scalar guarantee, degree33, same task | 0.695086802760714 |

In `schema: cubic-orbit-decoder-v2`, `cubic_information_map`,
`coefficients_from_cubic_information`, `cubic_intrinsic_greedy_search`, and
`cubic_classical_portfolio` implement exact 3-point information-manifold search
for $P(X) = P_0(X^3) + X P_1(X^3) + X^2 P_2(X^3)$ ($\deg P_r < K = 68$):

- At each of the $K=68$ selected information orbits $j \in I$, choosing
  $x_j = P(a_j) \in \mathbb{F}_p$, $y_j = P(\zeta a_j) \in \mathbb{F}_p$, and
  $r_j \in F_j$ uniquely determines $w_j = P(\zeta^2 a_j) = (r_j - b_j(x_j^2 - \eta y_j^2)) \bmod p$.
- Cyclic $3 \times 3$ Lagrange blocks $C_{s,i,j} = 3^{-1} \ell_j(a_i^3)(1 + (a_i/a_j)\zeta^s + (a_i/a_j)^2 \zeta^{2s}) \bmod p$
  propagate exact quartic `root_x` and `root_y` curves (degree $\le 4$) and
  quadratic `residual` curves (degree $\le 2$) across all $M=684$ orbits while
  preserving all $K=68$ pinned orbit predicates.
- On the native $(p=2053, M=684, n=204)$ instance (`seed=62947`):
  - `primary_information_set_I0` ($I_0 = 0..67$, 2 sweeps, $408$ coordinate scans,
    $702{,}264$ candidate evaluations, $480{,}348{,}576$ predicate lookups):
    improves the initial feasible witness from **`387 / 684` to `435 / 684`**.
  - `reanchored_information_set_escape` (pivoting to $K=68$ passing orbits of
    the `435/684` polynomial, 1 sweep, $204$ coordinate scans, $351{,}132$
    candidate evaluations): escapes the $I_0$ manifold and reaches **`438 / 684`**
    (`0.640351`), with all $204$ original polynomial coefficients reconstructed
    and independently verified at all three points of every orbit via Horner evaluation.

## Reproduction

```sh
python theorems/cubic_orbit_decoder.py --reference /path/to/RDQINumerics/data/reference --write
python -m pytest -q tests/test_cubic_orbit_decoder.py -W error::RuntimeWarning
```
