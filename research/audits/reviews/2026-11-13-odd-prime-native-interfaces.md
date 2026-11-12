# Odd-prime interfaces: sampler, Haar grid, pencil and local fields

2026-11-13. Independent audit of the completed 898-line odd-prime report,
especially Sections 3--4, 6 and 8, against the parent bridge and the
retained dyadic proofs. STATE and the relevant topic/review files were
read. No API, network, Git or numerical controls.

**Scoped conclusion.** The changed-characteristic arguments work uniformly
in odd primes supplied in binary. The explicit radii in Sections 3--4 are
sufficient. Add a localization to the displayed smooth support chart,
charge bounded-rejection random-bit consumption, and use the already
checked ACTUAL-factor OM backend. The pencil must pay `N' v_p(N')`.
No native counterexample to these interfaces was found. Section 7 gives
the repaired complete odd-prime composition from the separately proved
materializer, ONE-HALF ledger and finite-presentation theorem. It replaces
the report's unsupported `Lambda^80` clock with explicit operation guards,
a justified group-node bound and a compute-once precision schedule.

Throughout, `v=v_p` is extended by `v(p)=1`; numerical precision below
means p-adic digits, each costing `O(log p)` bits. Let `n=2g+1`, `g>=1`,
`D=v(Disc f)`, and `lambda=ceil(log_2(g+1))`.

## 1. Actual sampler and congruence coupling

Use the supplied, previously proved odd-prime seed determinant with
`N_s=4g^2`, `t_i=p^N_s i`, and

    P(t)=(t^-2, t^-n sqrt(F(t^2)))-infinity,
    F(z)=z^n f(1/z),                 sqrt congruent 1 modulo p.

The seed logarithm matrix `V` is integral: each integrated term has the
form `c t_i^a/a`, with `c in Z_p`, and `a v(t_i)-v_p(a)>=0`.
Retain the known exact determinant valuation

    D_p=N_s g^2+sum_i v(i)+sum_(i<j) v(j^2-i^2)
                         -sum_(j=0)^(g-1) v(2j+1).

For the reversed standard differential basis the derivative columns are
`-t_i^(2j) F(t_i^2)^(-1/2)`. Thus the derivative determinant is EXACTLY
a Vandermonde times unit column factors, giving

    H=N_s g(g-1)+sum_(i<j) v(j^2-i^2).

No additional alternant-error estimate is needed for this derivative.
The report's choice

    R=D_p+H+N_s+lambda+10

satisfies `R>=D_p`, `R>=H+2` and `R>v(t_i)` for all i. Hence every
parameter `t_i+p^R z_i` is nonzero and has the same valuation as `t_i`.

The integration denominators are paid explicitly. In a term
`c t^a/a`, the coefficient of `z^q` after translating by `p^R z` is

    c p^(Rq) binom(a,q) t_i^(a-q)/a
      =c p^(Rq) binom(a-1,q-1) t_i^(a-q)/q.

It has valuation at least `Rq-v_p(q)`, and the sum over a converges.
After extracting `p^R W`, nonlinear coefficients have valuation at least

    (q-1)R-v_p(q)-H >=1,       q>=2,

and tend to infinity. The resulting map `z -> z+epsilon(z)` is an
integral strict contraction perturbation of the identity. It is a
measure-preserving bijection and respects every congruence modulo `p^m`.

The near-infinity chart is smooth over Z_p: in coordinates
`u=1/x`, `w=y/x^(g+1)`, its equation is `w^2=uF(u)` and its u derivative
is a unit at infinity. The seed parameters and their translated parameters
are in `p^2 Z_p`. The Neron mapping property therefore places these
ACTUAL points and their differences in `K_2`. Formal log is injective on
`K_2`: in integral formal coordinates, degree-q coefficients lose at most
`v_p(q)`, and substitution of `p^2` makes the normalized nonlinear part
strictly contracting. Passing to standard rational differentials preserves
injectivity without requiring a quantitative Neron-basis comparison.

Consequently the actual sampler image is a subgroup U, with

    log U=p^R W Z_p^g,       mu_omega(U)=p^(-gR-H),
    U subset E=closed Z_p-span of the seeds.

The last inclusion follows from `p^D_p Z_p^g subset V Z_p^g` and actual
log injectivity. Moreover

    z=z' mod p^m  =>  sigma(z)-sigma(z') in p^m U.      (1)

Since 2 is a unit, `2U=U`. The shifted quotient uses the SAME fixed E;
representatives do not have to be literal 2-primary torsion points.

## 2. Uniform Haar tail with the report's numerical constants

The retained proof-only volume cover was already formulated over Q_p.
Its count and tube estimates remain valid with the following conservative
choices from the odd-prime report:

    M=2lambda+4,  N_c=4D+12,  a_free=3D+10,
    Delta_*=g(1+lambda),
    A_count=3g+gM+2gN_c,
    A_tail=A_count+a_free+Delta_*+3+2lambda,
    A_good=A_tail+1.

Here are the changed-characteristic checks, including dependent conjugates.

* A degree-d support field has discriminant exponent at most
  `d(1+log_p d)`. Over its maximal unramified subfield, derivative terms
  of an Eisenstein polynomial have distinct valuation residues modulo
  the ramification index. The leading derivative term bounds the
  different by `e v_p(e)+e-1`. Summing over support fields of total
  degree g gives the stated `Delta_*`.
* Matching Eisenstein coefficients modulo `p^M` gives a root in the
  same field by Hensel, because `M>2(v_p(e)+1)`. That root remains a
  uniformizer and generates the totally ramified extension. Therefore
  the earlier count `4^g p^(gM)` for ordered support-field tuples remains
  valid; these types are counted, not enumerated. Including chart
  choices gives `8^g p^(gM+2gN_c)<=p^A_count`.
* In an integral basis containing 1, the difference of two distinct
  embedding rows has a coefficient of valuation at most half the field
  discriminant exponent. Thus conjugate support coordinates use a
  nonzero difference LINEAR FORM, not an independence assertion. The
  sum form has coefficient 2, now of valuation zero. Keeping the
  dyadic one-digit allowance is conservative.
* An affine linear tube has measure at most `p^(a+b-q)` with free
  coordinate scale `p^a` and linear-form content at most b. A quadratic
  tube is covered by two root tubes, costing a factor `2<=p`. The
  infinity parameter w has `v(x)=-2v(w)`, `v(y)=-n v(w)` and its pole
  tail has measure at most `p^-s`.
* For the extra upper branch cap `v(y)<=ns`, an x-free chart has bad
  measure at most `n p^(a_free-2s)`, by factoring f over the algebraic
  closure for analysis. A y-free chart contributes at most
  `p^(a_free-ns)`. Infinity contributes nothing. These fit the added
  factor p in `A_good`.

The trace-product chart Jacobian is integral. Its area inequality holds
for every measurable parameter subset, so the preceding estimates transfer
to actual reduced divisors. On the full-measure degree-g reduced chart,
every effective degree-g preimage is the same divisor. No favorable
representative is substituted for the actual one.

Hence, for the set G_s of actual degree-g reduced divisors with distinct
finite x coordinates and

    v(x_i)>=-2s,    -ns<=v(y_i)<=ns,
    v(x_i-x_j)<=2s  for i!=j,

one has `mu_omega(J(Q_p) minus G_s)<=p^(A_good-s)`.
In particular, choosing

    s=A_good+gR+H+2g+2+k

bounds the simultaneous Haar failure for `h+2sigma(z)` and EVERY rational
half `q+sigma(z)` by

    (1+4^g) p^(A_good+gR+H-s) <=2^-k.                 (2)

This is uniform in every incoming `h in 2J(Q_p)`, including adaptive
incoming representatives. The single-point version needs no divisibility
promise. On G_s the familiar coefficient cap is `(6g-3)s`, with
`v Disc(a)<=2g(g-1)s` and `v Res(a,f)<=2gns`.

## 3. Local inverse radius and the required chart localization

Set

    A=4ns+4,
    K=g(A+2)+s g(g-1)+gns+ceil(Delta_*/2),
    Q=2K+1,             m_grid=max(0,Q-R).

At a good support point over a field E put
`F_x(z)=[f(x+p^A z)-y^2]/y^2`. Its degree-j coefficient has valuation
at least `Aj-2s(n-j)-2ns>=4j`. For odd p, the binomial coefficients of
both square-root series are p-integral, so their degree-j coefficients
also have valuation at least `4j`.

The report's chart is correct AFTER explicitly localizing at `1+p^2 v`:

    2v+p^2 v^2=F_x(z)/p^2,
    (z,v) |-> (x+p^A z, y(1+p^2 v)).                 (3)

Its v derivative is `2(1+p^2v)`. It is a unit at every integral point,
but is not automatically a unit in the unlocalized affine coordinate
ring. The localization makes the projection etale and the smooth-scheme
argument literal. It discards no integral points used here.

The branch through `(0,0)` has
`v=(sqrt(1+F_x)-1)/p^2`, with degree-j coefficient valuation at least
`4j-2`. After `z=p^2 t`, BOTH chart coordinates are congruent to the
center modulo p^2. Weil restriction along the finite free O_E/Z_p
extension is smooth, including ramified E; apply the Neron mapping
property to the generic trace-Abel map. The increments are actual K_2
points even though the original x,y center may be nonintegral.

For `omega_j=x^j dx/(2y)`, the degree-k pullback coefficient in z has
valuation at least `B_log+4k`, where

    B_log=A-ns-2(g-1)s=(4g+5)s+4.

Integration and `z=p^2 t` therefore give degree-q logarithm coefficients
of valuation at least

    B_log+6q-4-v_p(q).                               (4)

These are restricted integral series in ordinary Z_p coordinates after
integral-basis substitution and trace. This supplies the Taylor estimate
abbreviated in the paid report.

The derivative determinant is, up to a unit,

    p^(g(A+2)) Vand(x_i) product_E det(embedding matrix E)
                      / product_i (2y_i).

Its valuation is at most K, since `v_p(2)=0`. Thus `g(A+2)` is the
correct term; retaining the dyadic `g(A+1)` would underpay it. The
derivative matrix is integral. Scaling parameters by `p^(K+1)` and
using its adjugate turns the nonlinear part into a strict contraction.
The logarithmic image contains `p^(2K+1) Z_p^g`.

Actual K_2 log injectivity now gives the SAME-cap stability statement:

    P in G_s, e in K_2, log(e) in p^Q Z_p^g
        => P+e in G_s.                               (5)

The perturbation changes every x by valuation greater than `2s` and
multiplies y by a unit, so the coordinate and separation caps survive.
Combining (1) and (5) transfers (2) to the exact finite grid modulo
`p^m_grid`; multiplication by 2 incurs no additional depth loss.

## 4. Finite sampling: exact distribution and charged aborts

For `M0=p^m>1`, form the integer M0 and set
`b=bitlength(M0-1)=ceil(log_2 M0)<=m bitlength(p)`. Draw b uniform bits
and accept the resulting integer only if it is less than M0. Acceptance
probability is greater than one half. The FIRST accepted draw is exactly
uniform. For `m=0`, return zero without drawing bits.

With at most r attempts per coordinate, the chance any of g coordinates
aborts is at most `g 2^-r`. Conditional on completion the vector is
exactly uniform. Taking `r>=ceil(log_2(g/delta))+1` costs

    O(g r m bitlength(p))

random bits and polynomial integer work, with abort probability at most
delta. The scalar pencil has the same construction with `m=tau+1`.
Allocate delta to the whole adaptive call budget. The report's bound on
the LENGTH OF THE ACCEPTED SAMPLE is correct; total random-bit cost
also includes this bounded-rejection factor. No loop of length p or p^m
is used and no biased reduction of random binary integers is substituted.

## 5. Pencil when p divides N': explicit raw valuation caps

Let `K_af0=K_lab=2gns`, `K_disc0=2g(g-1)s`, and `K_wr=gns`.
With the visibly certified canonical input, the branch coefficient is

    [u^(2n)] Res(f,A_u)=(-1)^n Res(f,a0).

Thus branch content is at most `K_af0`; this simpler proof avoids any
question about derivative units. Let `N'=n-2e>0`, an odd integer. The
exact characteristic-zero discriminant identity gives content at most

    K_disc0+N' v_p(N').

The additional term is mandatory if `p|N'`; it is at most
`n ceil(log_2 n)` and disappears when the reset input has `e=g`.
For every fixed half, the odd-prime mixed-content bound is

    v_G,u Res(W,A_u)<=v Res(W,f)/2<=K_wr.

Here 2 is a unit, so the dyadic extra g is unnecessary. It is harmless
to retain it for a common implementation.

For example choose `tau=k+2g+ceil(log_2(16n))+2` and accept only within

    K_af   = K_af0+2n tau,
    K_disc = K_disc0+N'v_p(N')+4g tau,
    K_aw   = K_wr+2g tau.                             (6)

The root-ball tail for a degree-d polynomial is `d p^-tau`. The union
degree is at most `2g 4^g+4g+2n<=2n 4^g`; therefore (6) has total
failure at most `2^-k`. Source half sets are fixed before choosing u.
Integral polynomial normalizations add the same valuation to content
and evaluation, so cancel from these RAW caps. Alternatively keep their
positive scaling terms; the report's looser Section 6.4 caps are valid.

Monic pencil division still requires `S_A=(n+3)S_store`. For all arithmetic
and off-event acceptance use the checked ONE-HALF ledger with
`S_hat=S_A+D+1`, the early W pole check, and the SEPARATE visible
`Res(U,W)` test. One may retain every conservative dyadic constant in
that ledger: at odd p the contributions of 2 and 4 only improve. A
visible augmented determinant alone still does not certify extraction.

## 6. Actual local fields and odd-prime roots

Use the ACTUAL-factor OM identifiers, fixed lower-frame basis numerators
and finite refinement procedure established in
`2026-11-13-native-local-squareclass-backend.md`. The primary chain there
(OM2012 Proposition 3.8/Corollary 3.10, algorithm INPUT/OUTPUT, Theorems
3.14/5.18, and the local Okutsu basis proposition) holds for every p.
It removes the report's approximant-field/Hensel-Krasner transfer step.
No field embedding or approximant-root identification is additional input.

The finite-ring construction generalizes directly. In a degree-d actual
field with computed integral multiplication table, the nilradical of
`O/pO` is the kernel of `z -> z^(p^h)` for `p^h>=d`; this map is
F_p-linear. Compute the residue field as its quotient. Recover the FULL
maximal-ideal lattice from the lifted kernel PLUS pO. Products of a
Z_p-basis of m modulo pm give `m^2/pm`, so choose a basis vector nonzero
in `m/m^2`. This deterministically supplies a uniformizer, also in the
unramified case. All matrix work is polynomial in d and log p.

For `a=pi^r u`, its squareclass is valuation parity plus the quadratic
character of `bar u` in the residue field k. The principal units are
squares by Hensel, since 2 is a unit. No discrete logarithm is needed.
Residue character evaluation is binary exponentiation with exponent
`(|k|-1)/2`, having only `O(d log p)` bits.

A residue square root can be found by Tonelli--Shanks with a verified
nonsquare. In a uniform draw from k a nonsquare occurs with probability
`(|k|-1)/(2|k|)>=1/3`; bounded trials therefore cost polynomially in the
confidence bits. Writing `|k|-1=2^a t`, t odd, the algorithm maintains
`x^2=alpha b` and strictly decreases the 2-power order of b. It uses
`O(log^2 |k|)` field multiplications. Exact uniform residue draws use
the same bounded rejection as Section 4.

For an actual square a, remove its even valuation, freeze one residue
root, and lift it with unit derivative. If `v_pi(a)=r`, a finite root
certificate is

    v_pi(a_tilde-a)>r,
    v_pi(s_tilde^2-a_tilde)>r,     v_pi(s_tilde)=r/2.

It names the unique root with `v_pi(s-s_tilde)>r/2`; the other root is
at distance exactly r/2. The stronger dyadic-style certificate with
threshold `2e+r` is also available by extra refinement. Never reselect
the residue root during refinement.

On a fixed unit-root ball the square map is an isometry, so its inverse
loses ZERO p-adic digits. Uniformizer normalization and native-coordinate
conversion keep the same fixed polynomial guards as the dyadic backend:
`v_p Norm(pi)=f_res`, adjugates pay powers of pi, and the total order/CRT
index is at most D/2. With coefficient poles S and a visible norm/resultant
cap K, use `V=n(K+nS+S+1)` and, conservatively,

    C_local=20(n+1)^2(D+V+1).

The OM source complexity includes log residue size; p-small operations
must be charged in bits. Initial expected polynomial source routines
can be truncated by independent bounded runs to an explicit ABORT
probability. Subsequent arithmetic in the fixed field/root selectors
is deterministic. The total local field degree remains n.

## 7. Explicit odd-prime composition and bounded probability clock

This section uses the retained PROVED graph-product/materializer,
Stoll-identity and finite-group lemmas; their correctness is not inferred
from the paid odd-prime report's verdict. Their characteristic changes
are covered above. In particular the materializer's primitive norm
argument still works: a monic odd-degree polynomial is not a square in
F_p(x). Its ideal-content bound only improves when 2 becomes a unit.
Minimum-entry DVR pivoting and its additive normalization losses work
over Z_p without change.

Let `ell=bitlength(p)`. Compute the following quantities before sampling:

    K_index=3g+(D_p+gM+2gN_c) ell,
    T0=4(K_index+3g+10)^4,
    k=ceil(log_2(100(n+1)(T0+1)/eta)).

Use this k in s and tau above. Set

    S0=max(1, n(N_s+lambda)+1, (6g-3)s),
    L=S0,              D_scale=D+2L n(n-1),
    H_mat=D_scale+2,
    C_mat=nL+72g^2 H_mat+2.                            (7)

This is the actual canonical-materializer precision lemma, measured now
in p-adic digits. It covers total signed input degree at most 6g.

For the half operation evaluate the EXACT finite list of numerical
formulas in Section 1 of
`2026-11-13-stoll-half-precision-ledger.md`, using S0, D and the caps
(6), with `K_lab=2gns` and `K_wr=gns`. Retain its conservative dyadic
`2g` summands; they remain upper bounds at odd p. In particular use

    S_A=(n+3)S0,          S_hat=S_A+D+1,
    C_half=C_pen+K_src+C_root+C_M+2K_B+C_X+2K_X+C_out.   (8)

Every quantity on the right of (8) is explicitly defined in that ledger,
including root-coordinate, divisor-variation and cleared-resultant
guards. This is a computable numerical definition, not an unknown
polynomial constant. Its early W cap and independent extraction-resultant
test are part of the algorithm. A half group node first materializes its
shifted input with (7), then uses (8).

For initialization set

    V_init=n(D+nS0+S0+1),
    C_init=20(n+1)^2(D+V_init+1)+nS0+D+10.

Known branch-factor representatives have norm valuation at most D.
Near-infinity seeds have norm valuation at most zero and their explicit
pole cap is included in S0. Thus C_init suffices for any initial labels;
the odd-prime initial group generators themselves are only the branch
2-torsion points.

Use the fixed numerical schedule

    C_max=C_mat+C_half+1,
    P_cert=2+C_mat+C_half+C_init+K_B+K_X+K_src,
    P_star=P_cert+T0 C_max.                            (9)

All quantities in (7)--(9) are polynomials in the native numerical
parameters and `log(1/eta)`, and are independent of requested descendant
precision. In particular none is a recurrence in an ancestor's newly
computed output height.

Compute initial point and fresh sampler SOURCE leaves to P_star digits.
For sampler coordinates `v(t)<=N_s+lambda`, a sufficient fixed source
guard is `10(n+1)(N_s+lambda)+10`: write the known integer t as a
known power of p times a unit; its inverse powers have at most
`n(N_s+lambda)` poles, and the selected near-1 square root has unit
derivative. The parameter integers have polynomial bit length.
Compute actual field/basis data once to P_star plus, for example,

    C_field=max(C_init,C_root,C_lab)+2D+10

digits. These are native source computations, not expansions of older
point expressions.

At group depth `j=1+max(parent depths)`, compute the node ONCE to
`P_star-j C_max` digits. Its parents have at least C_max extra digits.
A sum consumes C_mat; a shifted half consumes at most C_mat+C_half.
Every accepted node retains at least P_cert digits. Preserve its exact
actual-point DAG identity, scalar choices, root balls and visible solve
charts. No later re-evaluation, unbounded precision retry or symbolic
expansion is required.

Here is why T0 bounds this schedule. Let `A=J(Q_p)/E` and use its
2-primary subgroup `A_2` for the finite-group argument. Multiplication
by 2 is an automorphism of E, so

    J(Q_p)/2J(Q_p)=A_2/2A_2,
    A_2[2]=J(Q_p)[2],       dim_F2 A_2[2]=t=r-1<=2g.

The volume bound gives `log_2 |A|<=K_index`, so the number kappa of
index-two enlargements from `B0=A_2[2]` is at most K_index. An actual
representative of a class in A_2 may have an arbitrary E-component.
An actual half of such a representative, including the certified
E-shift, again has class in A_2, because multiplication by 2 is
invertible on the odd part of A.

Keep old generators and the exact triangular relations `2q_new=v`,
where v is a 0/1 sum chosen by binary linear algebra to be nonzero in
`B/2B` and to have zero Kummer label. Every successful half doubles B.
The determinant of the triangular relation matrix doubles as well, so
the finite presentation remains exact. No equality or E-membership
oracle is introduced. At label rank t, `B+2A_2=A_2`; the finite
2-group quotient then forces `B=A_2`, proving COMPLETE-image stopping.

At enlargement i, the sum has at most t+i terms. Hence total binary
additions plus half calls are at most

    kappa t+kappa(kappa-1)/2 <= K_index(2g+K_index).

T0 also covers initialization, half-input materializations and sampling
stages. Each group call uses bounded-size graph blocks; source leaves
and arithmetic matrices per call are polynomial in g. This proves the
node/depth bound used in (9), instead of asserting a `Lambda^10` count.

For a completely bounded randomness schedule, do the following.

* Give OM/finite-field-factorization setup abort probability at most
  `eta/20`, using independent runs of twice a proved expected
  polynomial source clock. Freeze the first completed actual-factor
  frame. Source algorithms return correct outputs on completion.
* Precompute ONE verified nonsquare in each residue field and reuse it
  for all later Tonelli--Shanks calls. In one trial draw a binary
  integer in the smallest power-of-two interval containing the field;
  reject values outside it, zero and squares. The chance of a verified
  nonsquare is at least 1/6. Since `(5/6)^4<1/2`, at most
  `4 ceil(log_2(20(n+1)/eta))` trials per field give total failure at
  most `eta/20`. All later residue roots and labels are deterministic.
* For every sigma-grid coordinate and every pencil scalar, use at most
  k of the exact binary-rejection trials in Section 4. The chance of
  failure per coordinate is at most `2^-k`. There are at most
  `(g+1)T0` such coordinates.

There are at most T0 geometric bad events and T0 pencil bad events,
each with conditional probability at most `2^-k`. Therefore all
sampling and geometric failures together have probability at most

    (g+3)T0 2^-k <= (n+1)T0 2^-k <= eta/100.

Including setup, the total is at most `eta/10+eta/100<eta`.
The estimates are uniform conditional on the entire past. Conditional
on a bounded grid draw completing, its accepted value remains exactly
uniform, so this argument does not alter the geometric distribution.

All rejected certificates return ABORT. Every accepted point, root and
relation has its exact source/DAG meaning even off the good event.
Outside the union just bounded, the proved caps guarantee every test
succeeds and finite-group stopping returns a basis of the complete local
Kummer image. Thus no erroneous basis is returned.

Finally, T0, the matrix sizes, coefficient poles, P_star, source-parameter
bit lengths and bounded random-trial counts are all polynomial. The
fixed algorithms at each node have proved polynomial BIT cost at these
precisions; a p-adic buffer of P digits costs `O(P log p)` bits. This
establishes a bounded polynomial bit algorithm without inventing an
unsupported universal exponent or implementation constant. It remains a
proof-level native algorithm, not an implementation or a claim about the
global Selmer/quantum composition.
