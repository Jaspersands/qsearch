# Unconditional Class-Generator Source Admission

Status: CLASSICAL WEIGHTED SAMPLER, SOURCE AUDIT AND SCOPED FALSIFIERS,
2026-11-06. No GENERAL unconditional class-group algorithm, speedup,
novelty, or general impossibility is claimed.
Independent core derivation and actual-note review accepted the scoped
sampler and falsifiers; the parent checked the cited primary statements.
The existing exact-L0 compositions retain their class-arithmetic GRH premise.

Separate restricted positive result: ODD_GALOIS_CLASS_GROUP_COMPOSITION.md
now pays a different random-prime source and an unconditional written
quantum composition for explicit maximal orders of Galois ODD-degree
fields. Its Section6 also covers every FIXED odd degree, charging numerical
n!, and removes the source GRH premise for all retained irreducible-cubic
Selmer dimensions. It does not resolve this note's general inverse-norm
class coverage or the even-degree CM/L0 source.

## 1. Scientific target and competing mechanisms

Input: an explicit maximal order of a number field K, with degree n and
discriminant D, in a polynomial-size integral multiplication representation.
For the L0 application, K/Q is cyclic CM of degree q=2^s and prime conductor
p, with its paid Galois action. Output: a complete finite presentation of
Cl(K), and the action when requested. Bit complexity must be polynomial in
the input length, not in D. Complete compact S-unit computation and quantum
integer factoring are allowed PAID primitives; complete class generators
are not supplied advice.

The single unresolved question for this admission check is whether a paid
sampler can escape EVERY proper class subgroup with inverse-polynomial
probability, without a Riemann-hypothesis assumption. Such a source, plus
complete S-unit relations on all sampled prime factors, would remove a
specific blocker in an existing end-to-end quantum construction. Merely
factoring the sampled norms does not answer this question.

Candidate A draws algebraic integers from a public coefficient box, factors
their norms, and retains all prime-ideal divisors. Its intended clock is
poly(n,log D,log(1/rho)), with polynomial-bit sampled elements. The missing
obligation is a uniform coverage bound for their PRIME SUPPORTS: the whole
principal ideal has class zero. A box parameter, distribution, finite clock,
and an escape bound are required. Low support coverage is a falsifier of
that source; no such universal bound or universal counterexample is proved
here. The usual classical relation collection/norm-factorization attacks
apply to exactly these samples.

Candidate B samples integral ideals uniformly with norm <=N, where log N
is polynomial in the input, then collects their prime factors. It needs
BOTH a field-uniform sampling clock AND an effective class-distribution
bound at the chosen N. Uniformity among ideals does not itself imply exact
uniformity among classes at finite N. The expected advantage, if these
obligations were met, would come from the existing quantum relation
primitive versus classical index calculus; the ideal sampler itself can be
classical. The source audit below does not discharge those obligations.

Prior-work order: corpus been-tried lookup on unconditional quantum class
generators/random integral ideals/norm sampling, then primary literature;
the baselines lookup returned index calculus. The quarantined arbitrary-
degree regulator no-go is NOT evidence against the published quantum
primitives. No quantum subsystem or large experiment was built.

## 2. What Charles's exact sampler does and does not supply

Primary source: Zachary Charles, *Generating Random Factored Ideals in
Number Fields*, Math. Comp. 87 (2018), 2047--2056,
<https://doi.org/10.1090/mcom/3283>, preprint
<https://arxiv.org/pdf/1612.06260>. The parent read the actual algorithm,
success calculation and Section6, not just the abstract.

Write a_K(r) for the number of integral ideals of norm r and
A_K(N)=sum_(r<=N) a_K(r). The displayed calculation at the end of Section3
and start of Section4 gives a per-trial acceptance probability of the form

    P_accept = c_n(N) A_K(N)/N,

where c_n(N)>0 depends only on n and N. The accepted norm has probability
proportional to a_K(r); uniform selection within that norm fiber then gives
an exactly uniform integral ideal up to N. This is a genuine classical
sampler, not an oracle that must be implemented by quantum factoring.

The asymptotic runtime argument substitutes

    A_K(N)/N -> kappa_K = Res_(s=1) zeta_K(s)

using Wiener--Ikehara. For varying K, this hides BOTH kappa_K^{-1} and the
field-dependent onset of the asymptotic. Section6 expressly treats a fixed
field and fixed degree; the reported exponent in log N is n^2+n+7. Thus
this theorem is not, as stated, a polynomial(n,log D,log N) clock. Even
fixing n does not remove the dependence on the varying field K. This is a
missing uniform bound, not a proved superpolynomial lower bound.

For our cyclic prime-conductor family,

    kappa_K = product_(a=1,...,q-1) L(1,chi^a).

All factors except a=q/2 are nonquadratic. The effective nonquadratic
lower bound used in FIXED_ORDER_DIRICHLET_L0_RECONSTRUCTION.md Section9
controls those factors for each fixed q. The remaining factor is the
REAL quadratic character of the real quadratic subfield: q/2 is even,
so chi^(q/2)(-1)=1. That lower bound does not apply to it. No assertion
that an exceptional zero exists, that kappa_K is actually very small in
this family, or that every possible sampler must pay kappa_K^{-1}, follows.

## 3. A precise failure of the naive rational-norm lift

Choose r uniformly among the integers <=N for which a_K(r)>0, then choose
uniformly an ideal of norm r. If Z counts those valid integers, then

    P(I) = 1 / (Z a_K(Norm I)),

which differs from 1/A_K(N) whenever fiber sizes differ. Shor factoring
does not repair that weight. This formula is an exact distributional
falsifier of this particular lift, not of Candidate A or other samplers.

An elementary witness is K=Q(sqrt(-5)), N=5. The norm-fiber counts are
(1,1,2,1,1). Ideals of norms1,4,5 are principal; those of norms2,3 are
nonprincipal. Hence uniform ideals give principal-class probability1/2,
whereas the naive lift gives3/5. The Minkowski bound is less than3 and
2 is not a norm of an algebraic integer, proving the stated class number2.
This finite witness checks a law, not an asymptotic class-sampling claim.

## 4. Stronger classical baseline and source-assumption boundary

Primary source: de Boer, Pellet-Mary and Wesolowski, *Rigorous Methods for
Computational Number Theory*, author-hosted full text
<https://koendeboer.com/publication/rigorousmethods/RigorousMethods.pdf>.
Actual Theorems1.1 and9.5 assume ERH, defined in Section2.2 for Hecke
L-functions. Their ideal sampler first randomizes an Arakelov class using
small-prime walks; omitting that step does not inherit its density theorem.
It therefore does not supply an unconditional repair of Candidate A.

Actual Theorem1.3 supplies a stronger classical comparison than citing only
heuristic Buchmann/Biasse--Fieker: under ERH, it computes the class group
and compact fundamental units in expected time polynomial in input length,
L_|D|(1/2), L_(n^n)(2/3), and min(kappa_K,L_|D|(2/3+o(1))). In particular,
for fixed degree the stated bound is L_|D|(1/2) under ERH without the old
additional smoothness heuristics. This remains subexponential in D, not
polynomial in log D. Its kappa_K dependence is NOT the inverse factor in
Charles's acceptance calculation. No classical polynomial-time solution or
complexity separation is inferred.

The recent Frei--Sofos--Widmer paper
<https://arxiv.org/html/2610.18491> was inspected through its actual
Introduction and Theorem1.1. It defines QRH(delta) as a fixed zero-free
half-plane and states its results CONDITIONALLY on that hypothesis. Its
authors explicitly say they have not verified the cited recent claimed
proofs. Those underlying proofs have not been audited here. Accordingly
this pass does not use the abstract's unconditional language to remove
GRH, does not certify or refute those proofs, and does not turn its
small-generator statement about FIELD ELEMENTS into a class-group sampler.

## 5. A paid classical inverse-norm ideal sampler

There IS a constructive operation that avoids Charles's fixed-field
acceptance factor, but samples a DIFFERENT law. For explicit maximal-order
K of degree n, integer B>=1, s=1+1/B, and 0<epsilon<1/4, a classical
algorithm samples, within total variation epsilon, the law

    Pr(I) = Norm(I)^(-s) / zeta_K(s)                         (1)

on nonzero integral ideals, returning their prime-ideal factorization.
It has a clock polynomial in the field input, n, B and log(1/epsilon).
Dependence on B is numerical, not logarithmic. No zeta value, class group,
regulator, uniform class, quantum factoring or GRH is supplied.

### Rational source and its finite clock

Set r=2^(-1/B). Draw j>=0 with probability(1-r)r^j. Draw a uniform
FACTORED integer k in [2^j,2^(j+1)-1], then accept with probability
(2^j/k)^s. Its one-trial accepted mass is exactly

    (1-r) r^j 2^(-j) (2^j/k)^s = (1-r) k^(-s).

Acceptance is at least1/4, so repetition gives the rational zeta law
k^(-s)/zeta(s). Factored uniform integers are classical: the parent read
Kalai's actual one-page algorithm/proof, *Generating Random Factored
Numbers, Easily*, author page
<https://www.cs.cmu.edu/afs/cs/user/akalai/genfactor/web/factor/factor.html>,
PDF <https://mit6875.github.io/FA23HANDOUTS/adam-kalai-generating-factored-numbers.pdf>.
Use N=2^(j+1)-1 and restrict its output to k>=2^j. This loses at most a
factor2 in acceptance. Deterministic polynomial primality testing removes
any primality-error premise; no integer-factorization call is needed.

Here is a finite clock rather than an uncharged exact-real sampler. Cap
the outer attempts per stream at T=ceil(4 log(8n/epsilon)); their failure
is <=epsilon/(8n). Cap j at

    J=ceil(B log2(8nT/epsilon)).

Across nT attempts the geometric-tail error is <=epsilon/8. Implement
the capped geometric draw and acceptance Bernoulli probabilities to total
coupling error <=epsilon/8, using O(log(nT(J+1)/epsilon)) precision bits.
These probabilities are powers of positive rationals in bounded ranges,
so their evaluation costs polynomial(J,log B,log(1/epsilon)).

For completeness, a bound on EXPECTED runtime is not by itself a
logarithmic-confidence cap: timeouts can correlate with the returned
integer. Kalai's particular algorithm supplies a direct cap. Each trial
accepts a uniform dyadic-block integer with probability at least
(1/2) product_(ell<=N)(1-1/ell), which is >=c/log(N+2) for an effective
absolute c>0. Thus O((J+1)log(1/delta)) trials suffice. Its descending
uniform chain moves to at most ceil(current/2) with probability at least1/2
at each nonterminal step, giving an exponential tail after
O(J+log(1/delta)) steps.
Uniform integer rejection draws also have an exponential tail. Cap these
operations and couple them to the uncapped exact algorithm, assigning
delta=epsilon/(32nT) per factored-block call and reducing individual
sub-budgets by the polynomial number of operations. Every recognized
arithmetic failure or exhausted clock returns the UNIT ideal with its
empty factorization, so the approximate law is on integral ideals. Such
outputs are charged to the coupling error. No claim of exact
uniformity CONDITIONED on a timeout is needed. These caps, plus the
prime-ideal decomposition error budget below, leave total error <epsilon.

### Lifting independent streams to ideals

Take n INDEPENDENT rational zeta integers a_1,...,a_n. For each rational
prime ell appearing in their factorizations, compute

    ell O_K = product_(i=1,...,g) P_i^(e_i),
    Norm(P_i)=ell^(f_i),   g<=n,

in a deterministic ordering of the prime ideals, and set

    v_(P_i)(I) = floor(v_ell(a_i)/f_i).                       (2)

Computing prime decomposition from an explicit maximal order uses the
usual classical polynomial-time finite-field/local factorization, with
paid bounded-error clocks. This includes ramified primes: e_i is NOT the
divisor in(2). The arithmetic input is the maximal order, not an
unverified power-basis order.

Under the exact rational source, all v_ell(a_i) are mutually independent
geometric variables with tail ell^(-st). Consequently

    Pr(v_(P_i)(I)>=t) = ell^(-s f_i t).

These are independent across ALL prime ideals, precisely the Euler-product
law(1). Also log Norm(I)<=sum_i log a_i, so the capped output has
O(n(J+1)) norm bits and a polynomial-size factorization. Coupling the
finite sources and arithmetic gives the claimed TV error and public
polynomial clock. There is no dependence on kappa_K^{-1} in this sampler.

Two cheap falsifiers explain why the construction is specific. Reusing
ONE integer stream for two split primes over ell forces their exponents
equal instead of independent. Replacing f_i by the ramification index e_i
gives the wrong geometric tail whenever these differ. Neither repair can
be justified by the equality of whole rational ideal norms.

### Exactly what remains for class generation

For an ideal-class character psi, absolute convergence gives the Fourier
coefficient of the class law

    E[psi([I])] = L_K(s,psi)/zeta_K(s).                      (3)

The one-sided character criterion in the L0 note would pay generation if
Re(3)<=e<1/2 uniformly over every nontrivial psi, with a fixed e and
numerical B polynomial in the input. No such uniform bound is proved
here. Fixed-field convergence as s decreases to1 does not give that
polynomial B. Nor is(1) uniform on ideals of bounded norm. Thus the
operation removes an unnormalized supply problem and the apparent need
for Shor factoring, but leaves the decisive normalized-coverage problem.
It is not an end-to-end unconditional class algorithm or a quantum gain.

The character condition is sufficient, NOT necessary, especially because
the sampler returns prime factorizations. For any proper class subgroup H,
independent geometric exponents give the exact idealized support law

    Pr(all prime factors of I have class in H)
        = product_([P] outside H) (1-Norm(P)^(-s)).

Thus a uniform lower bound W_H(s)=sum_([P] outside H) Norm(P)^(-s)>=w
would give support escape>=1-exp(-w). If B and1/w are polynomial in the
input, polynomially many source calls and their collected prime factors
would pay generation; finite-source TV errors must be charged per call.
No such uniform W_H bound is established here. The new odd-Galois result
uses a DIFFERENT prime source, not an unproved W_H estimate for this one.

The parent independently derived the dyadic rational law, prime-valuation
lift, output-size bound and timeout coupling. The independent reviewer
derived the ideal lift and directly checked the classical replacement and
the need for a genuine tail cap. No implementation or finite experiment
is used to infer this distributional proof; novelty remains unassessed.

## 6. Admission decision and next experiment

For general fields and the even-degree CM target, no uniform unconditional
class-generator source is admitted. The CLASSICAL weighted ideal source
in Section5 is paid, but its class-coverage bound is not. The exact
norm-fiber weight and field-uniform supply rate are distinct from the
normalized class nonconcentration lemma already proved in the L0 note.
The residue-degree>1 odd-minus obstruction from that note also remains
scoped to cyclic CM2-power fields; it is not a general class-group barrier.

Re-entry requires a concrete source and a proved bound uniform in its
stated input family, or an actual verified new source theorem. Another
finite scan of norm supports, an unweighted norm lift, or a supplied
uniform Arakelov class is insufficient. Compare independent native
directions before further arithmetic work. The next experiment must test
an explicit paid operation or classical competitor; no generic sampler
implementation or broader scan is queued by this note.
