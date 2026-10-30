# Unknown-Rank Singular-Subspace Recovery In Split Orthogonal Groups

2026-10-27. Proposed constructive extension of the local maximal-only
three-probe reduction. This document supplies a proof, not a claim of
literature novelty, natural-input quantum advantage, or executed quantum
hardware. The implementation is a prime-field classical reference control.

## Contract

Let q be an odd prime power with a supplied effective field presentation.
Let V=F_q^n + F_q^n, Q(x,y)=x.y, and B its polar form. Let G be either
O^+(2n,q) or SO^+(2n,q). The ordinary coherent fixed-width oracle f obeys

    f(g)=f(h) iff g^-1 h belongs to P_U,

where P_U is the FULL setwise stabilizer in G of a totally singular space U
of UNKNOWN dimension k, promised 3<=k<=n. The goal is a basis of U.
No basis, dimension, classical membership oracle on vectors, coset-state
advice, or oracle outside G is supplied. All our queries lie in SO.

**Claim:** bounded-error recovery takes poly(n,log q,log(1/epsilon),label
width) time, using ordinary abelian HSP on explicit additive probe groups.
The algorithm below does not need k. It is not a flag algorithm and does
not cover k=1,2, characteristic two, nonsplit forms, rings, or subgroups
properly contained in P_U. A polynomial matrix-arithmetic implementation
plus standard approximate additive Fourier transforms suffices in the
stated oracle model; no scalable quantum compiler is supplied here.

## 1. The Probe And All Three Kernels

Choose a nonzero singular e. Public linear algebra finds a singular f0 with
B(e,f0)=1: take v with B(e,v)=1 and set f0=v-Q(v)e. Set
W=<e,f0>^perp. For w in W define

    E_e(w)z = z + B(z,e)w - B(z,w)e - Q(w)B(z,e)e.

Direct substitution gives E_e(w)E_e(w')=E_e(w+w'). The map is injective,
orthogonal, unipotent and determinant one. Thus w -> f(E_e(w)) hides the
F_q-linear kernel K_e of the intersection with P_U, without an ambient
orthogonal-group Fourier transform.

Write pi(z)=z-B(f0,z)e for z in e^perp. The complete classification is:

1. e in U: K_e=W, dimension 2n-2.
2. e in U^perp but not U: K_e=(pi U)^perp_W, dimension 2n-2-k.
3. e outside U^perp: K_e=pi(U intersect e^perp), dimension k-1.

Proof of case 1: B(u,e)=0 and E_e(w)u-u is a multiple of e in U.
In case 2 the same difference is -B(u,w)e, which belongs to U exactly
when it vanishes for every u. Projection of U is injective and W is
nondegenerate, giving the stated dimension. In case 3 put H0=U intersect
e^perp and choose u0 in U with B(e,u0)=1. If E_e(w) preserves U, its
difference on u0 is in H0 and projects to w, proving necessity. Conversely
write h=w+a e in H0. Then Q(w)=0, B(u0,w)=-a and B(H0,w)=0. The action
fixes H0 and maps u0 to u0+h, proving sufficiency. Projection on H0 is
injective since e is not in U.

For a good probe (case 3) we therefore learn the singular k-space

    S_e=<e>+K_e=<e>+(U intersect e^perp),

where K_e is embedded in the public complement W.

## 2. Three Good Probes Recover U

Let lambda_i=B(e_i,.) restricted to U, for i=1,2,3. If these functionals
are independent, then the e_i are independent modulo U: a relation modulo
U would give a relation among the lambda_i, since B(U,U)=0. Hence

    S_i intersect S_j = U intersect ker(lambda_i) intersect ker(lambda_j),
    U = (S_1 intersect S_2)+(S_1 intersect S_3)+(S_2 intersect S_3).

For the second identity choose coordinates on U whose first three
coordinates are the lambda_i. The three pairwise kernels together span
every coordinate. This is why k>=3 is required. This extends the existing
maximal-only proof; maximality is not used in these identities.

## 3. A Containment Certificate, Not An Equality Oracle

For any public singular candidate R of dimension r>=3, construct a Witt
decomposition V=R+M+R*, with B(R,R*) the identity. The middle form may be
arbitrary nondegenerate; it need not be converted to hyperbolic coordinates.
Use the following r(r-1)+1+2(n-r) matrices, all in SO and preserving R:

* Levi matrices diag(I+E_ij,I_M,I-E_ji), for every i!=j in R;
* one central radical matrix (r,m,y) -> (r+D y,m,y),
  D=E_12-E_21;
* E_e1(w) for each element w of a basis of M, with e1 the first basis
  vector of R (the same intrinsic formula as in Section 1).

Compare each f(g) to f(I). For every NONZERO totally singular U, all tests
pass **if and only if R is contained in U**. They do not certify equality.

Proof of necessity: both A=U intersect R and the projection Y of U onto
R* are invariant under the displayed Levi matrices. Their only invariant
F_q-linear subspaces in the natural and dual modules are zero and the
whole module. This follows directly from the elementary transvections;
coefficient 1 suffices even over extension fields. If Y=R*, isotropy forces
A=0, but the central matrix gives a nonzero vector D y in A, a
contradiction. Thus Y=0 and U lies in R+M. If A=0, the elementary Levi
differences force every R component of U to be zero, so U lies in M.
The cross-probe differences -B(u,w)e1 then force u=0 for every u in U,
by nondegeneracy of M, a contradiction. Therefore A=R.

For sufficiency, R subset U and isotropy imply U subset R^perp=R+M.
Levi and central tests fix U modulo R and cross tests change vectors only
by multiples of e1. Thus they all preserve U. This also explicitly
explains why a smaller candidate can pass the certificate on its own.

## 4. Unknown Rank And The Misleading n-1 Case

In one trial, learn three probe kernels. Reject the trial unless all have
the same dimension d with 2<=d<=n-1 and each embedded <e_i>+K_i is
totally singular. Form the pairwise-intersection sum R. Require R singular
of dimension r=d+1 and apply the containment certificate. Return R only
if it passes.

For exact kernels, case 1 always fails the dimension gate. If k<=n-2,
case 2 has dimension >=n and also fails it. If k=n-1, case 2 instead has
d=n-1, and can produce a perfectly singular MAXIMAL neighbor. This is a
real trap: repeated probes in one maximal extension can reconstruct that
extension, not U. But its candidate rank n is too large for containment
in U, so the certificate rejects it. Good probes have d=k-1, a different
dimension. Mixed good/bad triples cannot pass the equal-dimension gate.
For k=n the only nongood case is e in U. Thus every returned candidate
is U, while three independent good probes return U.

There is a useful extra safety fact: exact Fourier samples with insufficient
rank give a SUPERSPACE of the true kernel. Thus any dimension-gated
candidate has r>=k, whereas the certificate implies r<=k. Even with
undersampling, a returned answer is correct. Undersampling can cause
failure to return. This soundness statement does not apply to arbitrary
malformed learner outputs or approximate Fourier errors; those are charged
separately below.

## 5. Success, Query Count And Approximation

There are N=(q^n-1)(q^(n-1)+1) nonzero singular vectors. A uniform sampler
chooses y=0 with probability 1/(q^(n-1)+1), then uniform x!=0; otherwise
chooses uniform y!=0 and uniform x in y^perp. It requires no 1/q-rejection.
In coordinates with U=<e1,...,ek>, for each nonzero lambda in U*, exactly
q^(2n-k-1) singular vectors restrict to lambda. Therefore

    a_k = (q^k-1)q^(2n-k-1)/N,
    Pr[three independent lambda_i]
      = a_k^3 (q^k-q)(q^k-q^2)/(q^k-1)^2 > 1/3.

Indeed a_k >= (1-1/27)/(1+1/9)=13/15, and the remaining two factors are
at least 12/13 and 9/13, giving the lower bound 52/125 > 1/3.

Choose B trials with (2/3)^B<=epsilon/4. Each of at most 3B additive
HSP learners uses m=2n-2+s independent Fourier samples, with
3B/((q-1)q^s)<=epsilon/4. The chance that these samples fail to span any
annihilator is bounded by the union over its hyperplanes. Over F_q use
trace characters and a supplied field basis/dual basis; the annihilator
is F_q-linear because the actual kernel is F_q-linear. Recovery uses
F_q-linear, not merely prime-field, spans.

Each sample costs one original f call. The certificate has at most
n(n-1)+1 queries. Cache f(I) once. Total original queries are at most

    3B(2n-2+s) + B[n(n-1)+1] + 1.

Allocate epsilon/(4*3B*m) complete-instrument error per Fourier sample
(including preparation, arithmetic, oracle cleanup and transform), and
epsilon/4 total variation to capped classical samplers. A hybrid argument
and the two failure bounds above give failure <=epsilon. Effective finite
field linear algebra and reversible matrix arithmetic cost polynomially;
usual precision overhead is polynomial in log(1/epsilon), n and log q.
Dense reference table queries cost q^(2n-2) PER probe and are expressly
not this quantum budget. No efficient classical simulation is inferred.

## 6. Classical Comparator And Corrections To Old Notes

With the O oracle, a nonsingular reflection r_v belongs to P_U iff
v belongs to U^perp. For k<n the exact probability, when v is uniform
among nonsingular vectors in V, is

    (q^(n-k)-1)/(q^n-1).

This follows from the split nonsingular count
(q-1)q^(a-1)(q^a-1) in dimension 2a, multiplied by q^k for the radical
of U^perp. Conditional accepted vectors span U^perp. More explicitly,
their probability of leaving any proper linear subspace of U^perp is
at least 1/3: a functional nonzero on the radical has uniform value,
and otherwise one counts nonsingular vectors in a hyperplane of the
split quotient. For quotient dimension >=4, its total hyperplane size
is at most q^(2a-1), while its nonsingular count is
(q-1)q^(a-1)(q^a-1), giving fraction at most 9/16 for q>=3,a>=2.
For a=1, a hyperplane meets the nonsingular vectors in at most q-1 out
of (q-1)^2, a fraction at most 1/2. Thus O(n q^k) expected queries
learn a basis, and ordinary linear algebra recovers U.

Consequences and strict boundaries:
* This is an UPPER bound, not a classical lower bound or an optimal attack.
* At fixed q and k=O(log n), it is polynomial in n. With growing q,
  even constant k can give exponential dependence on log q.
* At k=n the success probability is ZERO. U^perp=U is totally singular;
  nonsingular reflections cannot reconstruct it.
* A single reflection has determinant -1. The SO oracle does not permit
  this test. Multiplication by a known nonsingular vector in U^perp would
  repair it, but acquiring that reference vector is not free.
* The existing maximal-only fixed-point-ratio lower bound and birthday
  attack are not transferred here to nonmaximal hidden ranks.

The historical body of main-repository
`ORTHOGONAL_PARABOLIC_HSP_OBSTRUCTION_QUADRATIC_INVARIANT.md` incorrectly
promotes q^k to poly(log q) without fixing q, and applies the reflection
density to the maximal case. Its overriding 2026-10-23 banner and
`PARABOLIC_CUT_LIST_CORRECTION.md` ALREADY withdraw these claims. Their
rejection is not new here; the exact nonmaximal hit probability and spanning
argument above refine the comparator. Other old claims remain unreviewed.

## 7. Prior Art, Impact And Decisive Falsifiers

The local `orthogonal-three-probe-2026-10-23/THREE_PROBE_REDUCTION.md`
expressly restricts to maximal U. The present kernel classification,
containment certificate and unknown-rank gate remove that restriction for
3<=k<=n. Independent bounded local search found no duplicate extension.

[Decker et al., 2014](https://arxiv.org/abs/1406.6511) solve hidden
parabolics in GL_n(F_q) without knowing the flag parameter.
[Imran, 2026](https://arxiv.org/abs/2610.28368) gives a GL_n finite-chain-ring
algorithm. Their stated GL domains do not by themselves give our
orthogonal-domain oracle: extending f to GL is an additional reduction,
not permission to call it outside SO/O. This bounded comparison is NOT
a literature novelty certification. No general-rank classical lower bound
is proved, and no natural hard task has been reduced to this oracle promise.

Highest-value falsifiers: a legal probe contradicting one of the three
kernel identities; a nonzero singular U passing the certificate without
containing R; an ideal-sample wrong-rank return; or a paid, input-preserving
published algorithm already covering this exact orthogonal contract.
The high-probability geometry is a theorem, not an extrapolation from
finite fixtures. No Shor-level impact follows from the theorem alone.

Stop after the narrow proof/control/review pass. Do not turn it into an
unmotivated flag/ring/nonsplit program. The corrected broad Rees theorem
still has higher strategic priority for specialist correctness/novelty
assessment; contact or submission requires separate user authorization.
