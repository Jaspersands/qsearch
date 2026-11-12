# Four-site Gaudin complement-entry series: independent disposition

2026-11-13. Narrow review of the new perturbative claim in the completed
`claude_runs/2026-11-13-gaudin-locality/response.md`. Current STATE was
read. One symbolic rational-function calculation on four independent
sites and ONE complementary entry was performed; no numerical instances,
N=6 calculation, parameter sweep, network, API, or Git.

**Accepted:** with the same convention as the previous exact review, for
any pairwise distinct real sites and complementary occupied two-subsets
v,w at N=4,M=2, the unique real antisymmetric joint generator satisfies

    <w|K(g)|v>
      = -(3/4)*(e_w-e_v)
         / product_(x in v,y in w)(eps_x-eps_y) * g^2
        + O(g^4)                                    (1)

near g=0. This includes accidental degeneracies among the pair sums e_S.
The radius and remainder bound may depend on the sites; no uniform
resource bound follows. One report sentence requires narrowing: when
`e_w=e_v`, (1) does NOT prove that this particular entry is nonzero or
not identically zero. At least two of the three complementary pairs have
nonzero displayed coefficients, which suffices for the claimed local
obstruction.

## 1. Normalization, signs, and the exact symbolic calculation

Here `e_S=sum_(i in S) eps_i`, where S records sites with n_i=1. For the
native charges,

    sum_i eps_i Q_i = E+(g/2) sum_(i<j)(P_ij-I)
                   = E+g*tau-2gI

on this sector, where `E=diag(e_S)` and tau is HALF the adjacency matrix
of the Johnson graph J(4,2). Dropping the scalar -2gI has no effect on
transport constraints. The generator convention is `A=iK`, `U'=K U`,
so `[H,H'-[K,H]]=0` for `H=E+g*tau`. Equivalently,

    [H,[H,K]]=[tau,E].                               (2)

On the open set where E has distinct entries, expand
`K=K0+g*K1+g^2*K2+...`. Off the diagonal,

    (K0)_mn=tau_mn/(e_n-e_m),
    (K1)_mn=[tau,K0]_mn/(e_n-e_m),

and set both diagonals to zero. These follow from (2) and
`[E,K0]=-tau`. The full second-order equation is

    ad_E^2 K2
      +(ad_E ad_tau+ad_tau ad_E)K1
      +ad_tau^2 K0=0.                                (3)

Keeping the full commutators in (3) matters; no equality involving a
nonzero diagonal of `[tau,K0]` is silently imposed on `[E,K1]`.

The independent calculation used Q(a,b,c,d), the six two-subsets in
lexicographic order, and v={a,b}, w={c,d}. Put

    Delta=c+d-a-b,
    Pi=(a-c)(a-d)(b-c)(b-d).

It verified K0 and K1 have zero complementary entries and that the
complementary entry of the final two terms in (3) is EXACTLY

    (3/4)*Delta^3/Pi.

Since `(ad_E^2 K2)_wv=Delta^2*(K2)_wv`, this gives (1)'s coefficient
`-(3/4)*Delta/Pi`. The independently expanded source also matches the
report's explicit four-middle-state recursion; its
`(tau*K0*tau)_wv` term vanishes by antisymmetry. The reported identity

    (c-d)^2+(a-b)^2+2(a-c)(b-d)+2(a-d)(b-c)=Delta^2

was checked as an exact polynomial identity.

The targeted script and exact result are retained in
`audits/reviews/2026-11-13-gaudin-complement-series/verify.py` and
`result.json`. They were run through the main Python interpreter and
Sage's `-c` interface. No floating arithmetic or eigenvalue solver was
used. Site relabeling and exchange of v,w give every other complementary
entry; exchanging v,w negates Delta and leaves Pi unchanged, as required
by antisymmetry.

## 2. Evenness is a JOINT-charge symmetry

Let C flip all four spins. It preserves the M=2 sector and satisfies

    C Q_i(g) C=I-Q_i(-g),        C V_i C=V_i.

The joint transport equations therefore send a solution K(g) to the
solution `-C K(g) C` at -g. Where the joint spectrum is simple the real
antisymmetric solution is unique, so

    K(-g)=-C K(g) C.                                 (4)

For complementary w=Cv, the right-hand entry is
`-K_(v,w)(g)=K_(w,v)(g)`. Every complementary entry is consequently EVEN
in g. Its constant term is zero: each V_i has only single-hop entries,
and the g=0 charges n_i distinguish any two computational basis states.
This proves the O(g^4) remainder in (1), rather than only O(g^3).

The argument uses the joint charges themselves; it does not assume that
the particular weighted Hamiltonian sum eps_i Q_i is nondegenerate.

## 3. Extension across accidental pair-sum degeneracies

At g=0 the tuple `(Q_i(0))=(n_i)` has simple joint spectrum independently
of all site values. A fully explicit separating auxiliary operator is

    B(g)=Q_1(g)+2Q_2(g)+4Q_3(g)+8Q_4(g).

Its six diagonal values at g=0 are distinct binary subset sums. For each
fixed tuple of distinct sites, B(g) stays simple for sufficiently small
g. The charges commute with B, so its real-analytic rank-one projectors
are the joint projectors. Their derivative gives the unique analytic
antisymmetric generator; equivalently use
`K=sum_v P_v' P_v`. These projectors and K also depend analytically on
the sites in a neighborhood avoiding site collisions.

Thus the coefficient K2 is continuous/analytic even when a pair sum of
E coincides with its complement. The generic calculation in Section 1
holds on a dense open subset of every such neighborhood. Its final
right side has only site-difference denominators, all nonzero at the
point in question. Continuity extends the identity to that point. In
particular Delta=0 gives K2_wv=0, with no division by a vanishing pair-sum
gap in the actual joint generator. Equation (4) also remains valid there.

## 4. Precisely what follows

For the three partitions with v containing the first site, write

    Delta_1=c+d-a-b,
    Delta_2=b+d-a-c,
    Delta_3=b+c-a-d.

If any TWO vanish, subtracting them forces two sites to coincide.
Therefore at least two are nonzero for pairwise distinct sites. Their
Pi denominators are nonzero as well. For each fixed site tuple, at least
one complementary entry is nonzero throughout some punctured interval
`0<|g|<g_*(eps)`. The previously proved support/gauge/sector argument then
excludes every exact at-most-three-site Hermitian JOINT AGP throughout
that interval.

This confirms the material strengthening from one exact instance to
EVERY distinct four-site tuple near zero coupling. It does not derive
an effective uniform g_*, establish nonvanishing at an arbitrary finite
g, or show that every complementary entry is nonzero. Statements about
isolated zeros apply only on an appropriate connected regular analytic
branch with a known nonidentically-zero entry; no global simplicity or
continuation assumption is silently added. The separate exact g=1/3
certificate remains the evidence at that coupling.

No growing-N locality theorem, branch-specific transport obstruction,
approximation bound, preparation no-go, or new polynomial preparation
mechanism follows. The report's suggested N=6 investigation was not run.
