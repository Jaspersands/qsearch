# Independent review: native Legendre bounded-adjoint receiver

2026-11-05. Scope: the written end-to-end composition in
QUADRATIC_LEGENDRE_SPHERICAL_READOUT.md, for an original coherent BIT/XOR
oracle for the quadratic character of a monic irreducible quadratic over
a growing odd prime field. No archive, Git, network or external-service
action was used. Main interpreter: /opt/anaconda3/bin/python; the one
exact control used /opt/anaconda3/envs/qsearch-cas/bin/python.

## Verdict

**ACCEPT the corrected written polynomial-time composition.** The native
growing-prime BIT problem may move from "polynomial receiver open" to
"accounted-for written quantum algorithm", with its explicit dependence
on the GL2 QFT toolbox Theorem 6.1 and the separately checked character-sum
theorem. The source theorem is unconditional as stated; it does not supply
a secret basis, target-dependent advice, a hidden oracle extension, or a
postselection primitive. Its operator-norm, uniform-circuit guarantee is
the guarantee used here. This review checks its applicability and relevant
basis conventions, not an independent reproof of the complete QFT paper.

This verdict is NOT a compiled/executed quantum receiver, novelty claim,
speedup/separation claim, or evidence of classical hardness. The strongest
same-native classical comparison and priority audit remain separate work.
The accepted access model is the BIT/XOR oracle. A homogeneous lift from
an uncontrolled raw phase oracle is not silently included.

The proof depends on the separately recorded exact kernel/scalar review
and principal-mass review. Both were read after their writers finished.
The checks below independently verify their use in the circuit composition.

## Corrections found and incorporated

1. The correct toolbox principal model for the displayed fixed vectors is
   I_{alpha,alpha^-1}, not I_{alpha^-1,alpha}. Direct multiplication with
   t_x=[[x,1],[1,0]] gives the upper-triangular diagonal
   (cx+d,det(g)/(cx+d)). Thus the finite-chart cocycle is
   alpha(det(g))^-1 alpha(cx+d)^2. In a canonical ordered QFT label
   (A,B), set alpha=A and B=alpha^-1.
2. Toolbox Equation (97) uses the INVERSE additive basis

       v_t = p^-1/2 sum_x conjugate(psi(tx)) |x>,
       w_delta = (p-1)^-1/2 sum_(t!=0) delta(t) alpha(t) v_t.

   The original PDF page 32 was rendered and inspected. The text extractor
   drops the conjugation bars; its apparent sign inconsistency in Equation
   (96) is therefore not an error in the PDF. The induced-to-GT conversion
   must use this actual formula. A plus-sign additive basis would require
   additional known label phases and is not the stated basis.
3. The source chooses compatible field generators h of F_(p^2)^* and
   g=Norm(h) of F_p^*. The initial nonsquare lambda used to construct the
   extension can be chosen independently; use the certified norm generator
   consistently for character and discrete-log coordinates.
4. Verification points must be exactly uniform for the stated 14/25 bound.
   Cap classical rejection sampling globally and charge its abort event;
   a fixed-error approximate quantum uniform state is not a substitute.

The parent incorporated all four corrections before this verdict.

## Partial spherical transforms are paid and coherent

Let N_s=p(p+1)/2, M=p(p-1)/2. Use GL2 with subgroups containing its center:
H_s is the diagonal/antidiagonal subgroup, of order 2(p-1)^2, and H_n is
the nonsplit torus plus its reflection, of order 2(p^2-1). Uniform subgroup
states require only a public uniform bit and uniform nonzero field-element
registers. They do not require the unknown quadratic.

For H_s, the two canonical rational projective columns give a reversible
coset representative. The inverse computes the unordered pair
{g(infinity),g(0)} and then r_R^-1 g. For H_n, Q=(X-z)^2-d is represented
by r_Q=[[r,z],[0,1]], where r is the canonical square root of d/lambda.
For g=[[a,b],[c,d]], its target root pair has

    z=(bd-ac lambda)/(d^2-c^2 lambda),
    w=(ad-bc)/(d^2-c^2 lambda),
    Q=(X-z)^2-lambda*w^2.

Both denominators and w are nonzero for an invertible g, since lambda is
a nonsquare. These formulas give the inverse coset encoding and subgroup
coordinate. They justify erasing the input label/subgroup registers after
forming the group element, and the reverse cleanup after the inverse QFT.
No input-dependent orbit search or inverse oracle is needed.

In the induced model, the stated vectors

    v_s(x)=alpha(x)^-1/sqrt(p-1) on F_p^*, zero at 0,infinity;
    v_n(x)=alpha(x^2-lambda)^-1/sqrt(p+1), v_n(infinity)=1/sqrt(p+1)

are fixed by their subgroups. The identity
Q0(gx)=det(g)Q0(x)/(cx+d)^2 proves invariance for the nonsplit torus;
evenness alpha(-1)=1 handles its reflection and the chart boundary.
For H_s, diagonal matrices force support on the nonzero finite orbit and
fix its amplitudes up to scale; the reflection again requires evenness.
The invariant spaces have dimension one. The characters alpha^2=1 are
excluded, so no reducible principal representation is treated as generic.

The fixed vectors can be prepared by uniform states and public character
phases. Equation (97) converts them to the actual GT coordinates using
additive/multiplicative Fourier transforms, exponentiation and clean
coherent discrete logarithms. Those operations are covered by toolbox
Lemma 6.7, Lemma 6.8 and Theorem 6.9. Their accuracy is in operator norm,
including controlled character labels, rather than a pointwise classical
success guarantee.

In the source's positive-matrix-entry Fourier convention, a coset gH
maps on a rank-one invariant sector to

    sqrt(dim(rho)/[G:H]) rho(g)v_H tensor conjugate(v_H).

Therefore unprepare conjugate(v_s) and synthesize conjugate(v_n) on the
RIGHT register. Conjugate the ENTIRE GT-coordinate preparation circuit,
not only the field-character phases. Its known scalar phase must also be
preserved under control. The same group-QFT sector phase cancels between
the two transforms. Measuring only the principal-membership flag preserves
coherence between its labels. Every retained carrier vector can be mapped
back to the nonsplit permutation module with clean subgroup workspace.

## The scalar operation has constant normalization

With beta^2=alpha and J=J(beta,chi), the forward kernel scalar in the
actual convention is

    tau_alpha=conjugate{beta(4lambda)^-1 (J^2-conjugate(J)^2)/2}.

All beta,beta*chi,alpha involved are nontrivial. The clean normalized
Gauss phases implement j=J/sqrt(p) coherently, and the successful block
of one Hadamard-control-Hadamard LCU is

    tau_alpha^*/p = beta(4lambda)^-1 (j^2-j^-2)/2.

Controlled inverses and the minus sign in the second branch are ordinary
circuit operations. This is a contraction with |tau_alpha|<=p. There is
no singular-value inversion, minimum spectral gap, individual Jacobi-value
estimation, or discarded success normalization. The wrong conjugation
would produce a tau^2 sum instead of the required positive |tau|^2 sum.

For input T|Q>/sqrt(N_s), the heralded adjoint output is exactly

    T_principal^* T_principal |Q> / (p sqrt(N_s)).

Every invariant principal projector has constant diagonal dim(rho)/M.
Writing A=sum_principal dim(rho)|tau_alpha|^2, the joint correct-output
amplitude is A/(p M sqrt(N_s)). The separate mass proof supplies
A>=p^3(p+1)/16 for every prime p>=625. Squaring and multiplying by the
distinct-pair preparation probability p/(p+1) gives a joint probability
greater than 1/32. All principal/LCU/diagonal flags are charged here.
The asymptotic probability 1/8 follows from A=p^4/8+O(p^(7/2)).

## Bounded resources and total error

The two homogeneous phase copies use two original BIT queries. Sorting
distinct x,y leaves an order bit in |+>, which is cleanly erased; only the
distinct-pair event is probabilistic. The approximate trial can be treated
as one unitary dilation, with flags measured afterward. Operator error
1/256 changes any event probability by at most 1/128, leaving success at
least 1/64 uniformly in Q and in the preceding trial transcript.

The parent's explicit bounds

    R=ceil(64 log(4/eta)),
    K=ceil(log(4R/eta)/log(25/14))

are sufficient. For unequal irreducible quadratics, their product is a
squarefree degree-four polynomial. Weil gives agreement at most
(1+3/sqrt(p))/2<=14/25 at p>=625. Fresh verification after candidate
generation gives total false acceptance <=eta/4 even with adaptive stopping;
all R trials missing the true candidate costs <=eta/4. Public preprocessing
abort costs <=eta/4. Exact classical rejection sampling with a cap
ceil(log2(8RK/eta)) per verification point costs at most eta/8 globally.
Thus the total is at most 7eta/8<eta, with native-query cap 2R+RK.

Certified public primitive elements and factorizations use capped known
polynomial quantum preprocessing. Tonelli--Shanks, field arithmetic,
character arithmetic and coset encodings are polynomial in log(p).
The group QFT is the uniform poly(log p,log(1/epsilon)) circuit of toolbox
Theorem 6.1. Compiling the finitely described blocks to a fixed trial
operator error therefore costs poly(log p); total time and workspace,
including bounded preprocessing, are polynomial in log(p),log(1/eta).
No length-p table, extension of the unknown oracle, or hidden advice is
present. Invalid padded encodings can always be defined to set an ABORT
flag; approximate leakage into those encodings must not be interpreted as
a valid irreducible candidate.

For the bounded set of primes below 625, the existing exact p-query
moment reconstruction applies at p>=5. At p=3, the three irreducibles
X^2+1, X^2+X+2, X^2+2X+2 have truth tables (+--),(-+-),(--+), so three
queries distinguish them. This small-prime step is a bounded constant in
the asymptotic statement and does not reuse the invalid p3 moment formula.

## Independent finite falsifier

One exact Sage control at p7, primitive generator and lambda=3, alpha of
exponent 2, constructed every split coset and every irreducible quadratic.
With the unnormalized induced fixed vectors, the full carrier frames obey

    W_s T = tau_alpha W_n,
    W_s W_s^* = W_n W_n^* = p(p-1)/2 I.

All matrix equalities held in CyclotomicField(6), for all 21 quadratic
columns. Here J=-2*zeta6-1, the receiver numerator is 4*zeta6-8, and the
forward scalar is its conjugate -4*zeta6-4. Using the receiver numerator
as the forward scalar failed. This checks the coset and scalar conventions
independently of the anchor-column control in the other review. It is not
an implementation of the quantum Fourier circuit or asymptotic evidence.

## Final claim boundary

The corrected construction is an explicit, source-based, polynomial-size
quantum circuit composition for the promised native BIT reconstruction
problem. Its paid implementation obligations are closed at the written
theorem level. A compiled device implementation, stronger classical attack,
and independent priority assessment remain distinct questions. No change
to novelty, separation, speedup or classical-hardness gates is justified.

## Addendum: fresh finite-domain phase copies suffice

Independent continuation on 2026-11-05. **ACCEPT the source weakening to
fresh independent pure copies**

    |psi_Q> = p^-1/2 sum_(x in F_p) chi(Q(x)) |x>.

The receiver does not require an oracle once these copies are supplied.
An uncontrolled raw phase oracle prepares one such copy per call from a
public uniform state, giving a further corollary with the preparation
accuracy charged below. Neither controlled use of that unknown oracle
nor a pointwise bit-oracle compiler is used in this argument.

Two copies, projected onto distinct finite x,y and folded into an unordered
pair, succeed with probability (p-1)/p. Embedded in the split-pair space,
the normalized state is

    |phi_Q> = Pi_finite T|Q>/sqrt(M),

where its infinity-containing coordinates are zero. Let
|psi_hom_Q>=T|Q>/sqrt(N_s). Their overlap is sqrt(M/N_s), so

    ||phi_Q-psi_hom_Q||^2
      =2-2sqrt((p-1)/(p+1)) <=2/(p-1)<1/256,  p>=625.

This is a comparison of states, not a claim that the homogeneous state
can be prepared from a copy. Any unobservable global phase is aligned
only for this norm calculation; the circuit needs no phase orientation.

Write K for the successful block of the already specified principal
adjoint receiver. It is a contraction. Its homogeneous correct-output
amplitude is at least 1/sqrt(32)>1/6. Therefore

    |<Q|K|phi_Q>| > 1/6-1/16 = 5/48.

Including the finite distinct-pair probability gives ideal joint correct
probability at least

    ((p-1)/p)(5/48)^2 >=13/1200>1/128.

This includes the principal and LCU flags; no further renormalization is
made. A full reconstruction-trial operator error <=1/1024 changes any
event probability by at most 1/512. Thus the more conservative lower
bound 1/256 remains valid for the actual correct-candidate event.

### Verification consumes fresh copies, not classical oracle values

For each candidate Q', a public circuit prepares |psi_Q'> using only its
known coefficients. Apply its inverse to a NEW unknown copy and test for
the all-zero initial state. The ideal acceptance probability is
|<psi_Q',psi_Q>|^2. It equals one for Q'=Q. For different irreducible
quadratics, the degree-four Weil bound gives

    |<psi_Q',psi_Q>|^2 <=9/p <=9/625<1/64.

The public preparation/inverse may be approximate. Require a uniform
per-test event-probability error <=1/(128K_v), where K_v is the number
of tests per candidate. On the true candidate, all K_v tests accept with
probability >=127/128. On any wrong candidate, each conditional test
acceptance is at most 1/64+1/(128K_v)<=3/128<1/32.

These conditional bounds survive adaptive candidate generation, preceding
test results and stopping because every test receives a fresh tensor-product
copy and fresh clean workspace. They do not apply to an arbitrary noisy or correlated
bank whose marginals only approximate the pure source. All copies consumed by failed
trials/tests are charged and are never reused or cloned.

For failure target 0<eta<1/2, take

    R=ceil(512 log(4/eta)),
    K_v=ceil(log(4R/eta)/log(32)).

The accepted-true probability in each fresh attempt is at least
(1/256)(127/128)>1/512. Consequently the probability of no accepted true
candidate in R attempts is <=eta/4. The probability that any wrong
candidate passes all tests is at most R*32^(-K_v)<=eta/4. The existing
capped public preprocessing costs <=eta/4. Total failure is therefore
<=3eta/4<eta, with a worst-case cap of 2R+R K_v supplied copies.

For an uncontrolled raw phase oracle, count one query per supplied copy.
Approximate public uniform-state preparation before those calls is included
in the reconstruction-trial error or the per-verification-test error,
respectively. Source calls have fixed count within each reconstruction or
verification operation, so no controlled version of the unknown phase
oracle is required. Gate and space costs remain polynomial in log(p)
and log(1/eta), including the precision log(K_v) for the verification
circuits. There is no classical random-query verification sampler in this
copy-only corollary.

### Explicit small-prime copy-only procedure

The BIT algorithm's full-data recovery cannot be used as an operation in
the copy-only model. It can, however, prove that the finite family of
states is distinguishable. For p>=5, the moment identity shows that equal
native sign tables imply equal Q. The three p3 tables were displayed
above. Opposite sign tables are impossible because each irreducible
quadratic has sum_x chi(Q(x))=-1. Hence distinct candidates cannot yield
the same state up to global phase.

More quantitatively, their Hamming distance is an integer between 1 and
p-1. Thus, for every distinct Q,Q',

    |<psi_Q',psi_Q>| <=1-2/p,
    ideal wrong-test acceptance <=(1-2/p)^2<=1-2/p.

For p<625 enumerate all M=p(p-1)/2 irreducible monic quadratics and test
each candidate on K_s fresh copies, stopping at the first full acceptance:

    K_s=ceil(p log(4M/eta)),
    per-test event error delta_s=min(1/p,eta/(4K_s)).

Each wrong test accepts with probability at most 1-1/p. A union bound
gives any false candidate acceptance <=M exp(-K_s/p)<=eta/4. The true
candidate fails one of its tests with probability at most K_s delta_s
<=eta/4. Return ABORT if all candidates fail. This explicit capped method
uses at most M K_s copies and fails with probability <=eta/2. Its
O(p^3 log(M/eta)) copy bound is a bounded constant times log(1/eta) on
the finite range p<625. All candidate circuits and irreducibility checks
are public and require no unknown-oracle access. No small-prime copy
identifiability is assumed without proof.

### Addendum verdict boundary

The growing-prime written reconstruction theorem is therefore valid under
the weaker fresh-copy source, and hence under uncontrolled raw phase
queries. The two-copy reconstruction has constant success; amplification
and verification use the explicitly bounded additional fresh copies.
This does not construct a bit oracle from copies, apply to correlated or
noisy source banks, or change execution/novelty/separation/hardness gates.
