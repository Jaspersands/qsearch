# Quadratic Legendre recovery: native contract and decoder test

5 November 2026. The growing-prime BIT-oracle problem now has an independently
reviewed WRITTEN polynomial-time composition in
QUADRATIC_LEGENDRE_SPHERICAL_READOUT.md. This note preserves the earlier
classical/subexponential comparisons, failed readouts, and fixed-characteristic
boundary. The new result uses a different collective spherical receiver;
it does not revive those failed readouts or claim quantum execution,
novelty, speedup, separation, or classical hardness.

## Native question and selection

For a growing public odd prime p, the secret is a monic irreducible
quadratic f(X)=X^2+bX+c over F_p. Supply coherent access to the BIT-valued
Legendre function chi(f(x)) for x in F_p, where irreducibility ensures no
zero outputs. Recover b,c. Both classical and quantum algorithms receive
this same function; no full values f(x), extension-field queries, secret
factors, input-sized advice, or supplied Fourier phases are available.
The size parameter is log p. A public p-entry truth table is a different
input model and costs p to acquire here. Q2 access is an explicit promise;
this is not an attack on classical-query-only PRFs or an actual deployment.

The question is externally motivated by published higher-degree Legendre
function reconstruction. Quadratics are a symmetry-bearing subcase, not
the stabilizer-free higher-degree keys recommended for deployment. A
poly(log p)-time decoder would improve the known exponential-in-log-p
upper bounds on this native problem. No classical lower bound is known
here, and an improvement in query count alone is insufficient.

Prior corpus lookups returned the quarantined Legendre demarcation and
unrelated full-value/bent-function controls; none resolves this input.
The baselines catalog returned no exact higher-degree match. Primary
papers, rather than those absences, supply the actual competitors below.
Compared with more OPI tie rules or another Rees receiver without a native
application, this pass tests whether a specific arithmetic kernel can pay
the missing reconstruction measurement. It does not admit a generic HSP
or PGM subsystem. A missing implementation will not be treated as hardness.

## Primary-source boundary

- Russell--Shparlinski, [quant-ph/0212016, Section 4, Theorem 6](https://arxiv.org/pdf/quant-ph/0212016), constructs O(d) query states and proves existence
  of a successful POVM. The proof bounds an operator norm over all candidate
  polynomials; it does not implement the POVM in poly(log p) time. The
  efficient linear shifted-Legendre algorithm is a separate result.
- Kaluđerović--Kleinjung--Kostić,
  [published paper, Section 4F](https://msp.org/obs/2020/4-1/obs-v4-n1-p17-p.pdf),
  treats degree two separately with O(p) translation/centered-polynomial
  enumeration, suppressing logarithmic factors. Its short fingerprint
  uniqueness is assumed in Section 2B. The r>=3 stabilizer formula in
  Section 4B must not be substituted at r=2. Section 5A trades queries,
  table preprocessing and search work; it does not give poly(log p) time.
- Beullens et al., [Sections 4--5](https://cosicdatabase.esat.kuleuven.be/backend/publications/files/journal/3130), gives higher-degree sequence/collision
  attacks with a short-fingerprint assumption. Factor/MITM attacks require
  splitting over F_p and do not apply to the irreducible promise. Their
  introductory polynomial-time quantum statement concerns degree one.

Local primary full texts are in `audits/sources/legendre_prf/`. The separate
classical source review records exact costs, data requirements and locators.
The prime-field bit oracle cannot be replaced by a full F_(p^2) oracle
merely because f factors over that field.

## Exact full-data classical baseline

For every p>=5 and monic quadratic f, using the genuine character values,
let S_j=sum_(x in F_p) x^j chi(f(x)) in F_p. Euler's criterion gives
chi(f(x))=f(x)^h as field elements, h=(p-1)/2. For j<=2,
deg(X^j f^h)<=p+1<2(p-1). Finite-field monomial summation therefore selects
only the coefficient of X^(p-1), with a minus sign. Thus

    S_0=-1,
    S_1=-h b=b/2,
    S_2=-(h c+binom(h,2)b^2)=c/2-3b^2/8,
    b=2S_1,  c=2S_2+3b^2/4.

The attack takes exactly p classical oracle queries, O(p) field operations
and O(log p) working bits, with polynomial-logarithmic bit-operation cost
per arithmetic operation. It needs neither fingerprint heuristics nor
candidate enumeration. This is an independently derived elementary
specialization, not a novelty claim. It is still exponential in log p.
The p=3 case is excluded from these formulas; the leading X^4 term then
also contributes to S_2. Sage checked all164 irreducible quadratics at
p5/7/11/13 and retained all3 predicted p3 failures. See
`classical_baselines/quadratic_legendre_contract.py/json`. These checks
verify the identity and source boundary, not hardness or asymptotics.

## Stronger arbitrary-chosen-query classical baseline

Write a=-b/2 and d=a^2-c, so d is nonsquare and
g(x)=chi((x-a)^2-d). The reflection identity g(x)=g(2a-x) is exact.
For p>=37, take L independent uniform public offsets x_j. Put

    W(t)=(g(x_j+t))_j,
    F(t,0)=W(t),  F(t,1)=(g(-x_j+t))_j=W(2a-t).

Distinct translates correspond to distinct irreducible quadratics.
The quartic Weil bound implies pairwise agreement at most
rho=(1+3/sqrt(p))/2<=3/4. A union bound makes W injective except probability
at most p^2(3/4)^L. This is a global event about the one fixed offset list.

Let B=ceil(sqrt(p)). Store F(t,0) for t=0,...,B-1 and look up F(jB,1)
for j=0,...,B-1. The integer representative of 2a is t+jB for some such
pair, so on the injectivity event a collision necessarily returns
a=(t+jB)/2 mod p. Cost O(sqrt(p)L) native queries and stored bits up to
logarithmic factors. No birthday assumption is needed at this stage.

Choose a public nonsquare eta by charged random rejection, and write
d=eta r^2. Then h(x)=g(a+x)=phi(x/r), phi(x)=chi(x^2-eta). Both are even,
so work on G=F_p^*/{+1,-1}, with N=(p-1)/2 elements. For independent
uniform NONZERO offsets y_j, define H0(v)=(phi(v y_j))_j and
H1(u)=(h(u y_j))_j. On the corresponding injectivity event,

    H1(u)=H0(v) iff u/v is in {r,-r}.

For distinct quotient elements the agreement bound is
(p+3sqrt(p)-2)/(2(p-1))<=3/4 at p>=37: remove the value1 at zero from the
full-field quartic correlation. Reference entries at M distinct quotient
representatives and M independent uniformly sampled hidden representatives
miss a match with probability (1-M/N)^M<=exp(-M^2/N). Taking
M=ceil(sqrt(N log16)) makes this <=1/16, when M<=N; small primes can use
all N representatives. A match returns d=eta(u/v)^2. Canonical +/- field
representatives require no primitive root, factoring or discrete-log advice.

Total expected time, queries and memory are O(sqrt(p) polylog(p)); public
Legendre evaluations, hash/table construction and input arithmetic are
included. Arbitrary chosen queries are essential. KKK Section5 builds
its limited-data expansion from a consecutive interval, so that table
cannot be transferred to this chosen-query schedule or vice versa.
This is an independently derived baseline, with novelty unclaimed.

The predeclared Sage control p101/1009/10007, seeds6101/6102, retained all
six cases, with three width attempts allowed and all failures retained.
All six recovered exact native coefficients on the first width attempt.
Total oracle counts were753,941,4143,4017,17270,16796; conservative
fingerprint lengths47,63,79 make these small-instance counts exceed p.
There is no empirical scaling claim. Artifacts:
`classical_baselines/quadratic_legendre_birthday.py/json`. With ideal
independent randomness, one center and three width fingerprint sets have
total bad-event probability at most4/64. Conditional on these good events,
three width misses have probability at most1/4096. Thus failure or incorrect
output is at most257/4096. True candidates always pass the fresh checks;
false candidates already require a bad fingerprint, so verification needs
no additional term in this particular conservative bound.

The saved implementation's resource guarantee is EXPECTED, not worst-case.
On a bad fingerprint event it can retain O(p) false-candidate witnesses and
perform O(p) verification work. Each wrong center collision has probability
at most1/(64p^2), with B^2<2p pairs. Expected false center candidates are
O(1/p), and an incorrect center additionally passes its16 fresh reflection
checks with probability at most(3/4)^16. Charging even O(p) work on that
branch contributes O(1) unconditionally. Given a correct center, the three
width attempts have O(1/p) expected false matches by the same pair-count
bound. Do not reuse the nonzero-offset width bound at a wrong center:
the removed zero term can have the opposite sign. Public nonsquare rejection
uses exactly two expected trials, with unbounded worst-case length.

## Paid subexponential quantum composition

Use the standard reversible BIT-OUTPUT Q2 oracle
U_g|x,z>=|x,z xor L_g(x)>, with (-1)^L_g(x)=g(x). This sufficient access
can be weakened to an uncontrolled diagonal phase oracle: the public
reference compiler proved below supplies relative bits in one phase query.
Copies alone do not supply this coherent query construction; no general
copies-only impossibility is asserted.

Compose F with dihedral inversion:

    F'(t,0)=F(-t,0)=W(-t),  F'(t,1)=F(t,1)=W(2a-t).

On the global injectivity event, each fiber consists exactly of
(t,0),(t+2a,1). Uniform preparation, computation and measurement/discard
of the output therefore produce standard dihedral coset states. Positive
QFT on t followed by measurement of k gives a uniform k and the qubit
(|0>+exp(2pi*i*(2a)k/p)|1>)/sqrt2, with every branch retained.
Each fresh sample costs L native queries and poly(log p) arithmetic.
The fixed public offsets are not an IID bank of consumed quantum states;
each quantum sample is prepared freshly from the actual oracle.

[Kuperberg, Theorem1.1 and Section5](https://arxiv.org/pdf/quant-ph/0302112)
applies to arbitrary N, including N=p, and recovers2a in
2^O(sqrt(log p)) time, queries and quantum space. Its generic-oracle
classical lower bound does NOT transfer to the structured native g.
Choose L=O(log p+log(1/delta)) once so the global fingerprint failure is
<=delta. On the good event the induced oracle is exact; there is no
per-query fingerprint failure to multiply by the sieve's call count.

After recovering a, let S={z:chi(z)>=0}, s=|S|=(p+1)/2. Uniformly prepare
S using the public predicate at constant success cost, compute a canonical
square root z, query g(a+sqrt(z))=chi(z-d), and uncompute the root/work.
This prepares s^(-1/2)sum_(z in S) chi(z-d)|z>. Since d is nonsquare,
no missing zero-value or postselection branch is hidden here.

Define C[y,z]=chi(y-z), J the all-ones matrix, and

    U=C/sqrt(p)+J/p.

C^*C=pI-J and CJ=JC=0 imply U is unitary. It is implemented by additive
QFT, the computable quadratic-character Gauss phases on nonzero frequency,
and phase1 on frequency0. For p=3 mod4 the Gauss phase is complex; replacing
it by a real sign would be wrong. Public square-root arithmetic, character
computation and workspace cleanup have polynomial-logarithmic cost.

The amplitude at d is

    chi(-1)sqrt(s/p) + T/(p sqrt(s)),
    T=sum_(z in S)chi(z-d)=-(1+chi(-1))/2.

Thus exact success is s/p for p=3 mod4 and
(sqrt(s/p)-1/(p sqrt(s)))^2 for p=1 mod4. In particular it is at least
(s/p)(1-1/sqrt(p))^2, a constant at p>=37. Repeat and independently
verify b=-2a,c=a^2-d. The small primes p<37 may be handled directly.

This is a written end-to-end subexponential upper bound, independently
reviewed, not a polynomial-time algorithm or a new separation. It uses
known sieve/character primitives; priority is unverified. Total bounded-
error resource accounting adds fingerprint failure, sieve failure,
finite repetition/verification errors and circuit approximation error.
Per-call operator precision can be inverse in the total subexponential
call count; its logarithm remains O(sqrt(log p)), preserving the bound.

Independent mathematical review is in
`audits/reviews/2026-11-05-quadratic-legendre-quantum-review.md`. The exact
Sage control `classical_baselines/quadratic_legendre_quantum_identities.py/json`
checked p37 and43, public seed7301, center7 and the first public nonsquare
width. The original37/41 proposal was corrected to37/43 BEFORE execution
because37 and41 are both1 mod4. All80 fibers,3218 coset-phase/uniform-label
identities,80 circulant coefficients and both probability normalizations
passed exactly in cyclotomic fields. Width probabilities were
13358/26011-2sqrt(37)/1369 and22/43. Harness calls were2998 and3570;
these dense finite checks do not represent algorithmic query costs.
Omitted inversion, omitted zero-frequency correction and a real-only
Gauss phase at43 fail their controls. A Sage API mismatch was corrected
before the same fixed inputs completed; no mathematical discrepancy occurred.
No Kuperberg sieve or end-to-end quantum decoder was executed.

## Specific two-copy hypothesis and its cheapest falsifier

Two Q2 calls prepare |psi_f>^tensor2, where

    |psi_f> = p^(-1/2) sum_x chi(f(x)) |x>.

The candidate kernel on ordered pairs and coefficient labels is

    K[(x,y),(b,c)] = chi((x^2+bx+c)(y^2+by+c))/p.

For x!=y the map (b,c) -> (f(x),f(y)) is an affine bijection. It is tempting
to infer a unitary decoder from two ordinary Legendre transforms. That
inference is false: distinct irreducible f,h have overlap

    <psi_f^2|psi_h^2> = (S_fh/p)^2,
    S_fh = sum_x chi(f(x)h(x)).

S_fh is an odd integer (p nonzero signs), hence never zero. The columns
are not orthogonal. The diagonal x=y sector has input-independent
probability1/p. Removing it gives normalized overlap
(S_fh^2-p)/(p(p-1)), also nonzero because p is not an integer square.
For p5, f=X^2+2 and h=X^2+X+1 give S=-3, full overlap9/25 and projected
overlap1/5. This refutes exact kernel-as-unitary identification, not
approximate discrimination or a different collective measurement.

There are M=p(p-1)/2 irreducible monic candidates. All two-copy states have
overlap1/sqrt(p) with the known diagonal state p^(-1/2)sum_x|x,x>.
Consequently the full Gram operator has largest eigenvalue at least M/p;
small pairwise overlaps alone do not make it close to identity.

Another concrete decoder is also unpaid: uniformly prepare the M labels,
apply controlled inverse candidate-state preparation to the unknown state,
and herald the data register zero. Its exact success probability is

    P_h = (1/M)[1+sum_(f!=h)(S_fh/p)^4].

Weil's |S_fh|<=3sqrt(p) gives 1/M<=P_h<=1/M+81/p^2=Theta(p^-2).
The joint probability of the correct label is exactly1/M. Generic
amplitude amplification costs Theta(p), not poly(log p). Candidate states
can themselves be prepared efficiently by public arithmetic; that does
not remove this normalization. These are falsifiers of specified circuits,
not a general measurement lower bound.

## GL2 source check and the explicit remaining block

The full [QFT toolbox](https://arxiv.org/pdf/2608.28573), Section6.4.4,
Equations125--130 and Theorem6.33, supplies a uniform q-by-q unitary A_gamma.
Its source labels are a distinguished double-coset path and q-1
multiplicative characters; its target labels are cuspidal, principal-series
and Steinberg representations with fixed central character. The circuit
uses multiplicative Fourier transforms, Gauss phases, the roots of
X^2-X+t, and fixed/exceptional orbit corrections. These are explicit paid
operations. Its labels are not the native (a,d) labels, and its entries are
not identified with the two-copy character kernel above. Reading the hard
block proof and AppendixB.2 did not supply that conversion. This is an
unresolved matching problem, not a defect in the QFT theorem or a no-go.

For a concrete next target, use m=(x+y)/2, r=(x-y)/2 on two native copies
and apply the positive QFT only to m. The amplitude at(k,r) is

    omega^(ka) B_k(r,d),
    B_k(r,d)=p^(-3/2) sum_t
      chi((((t+r)^2-d)((t-r)^2-d))) omega^(kt).

For every nonzero k, substitution u=kt gives
B_k(r,d)=B_1(kr,k^2d). Also B_k(-r,d)=B_k(r,d), these amplitudes are real,
and B_k(0,d)=delta_(k,0)/sqrt(p). Folding +/-r multiplies nonzero-row
amplitudes by sqrt2. For k!=0, deleting the zero r=0 row yields a square
(p-1)/2-dimensional block indexed by nonzero +/-r and nonsquare d.
These identities were independently checked algebraically. They specify
the block in this translation-Fourier organization, not every possible
decoder. B_k is subnormalized, not a supplied unitary. Measuring k removes
the center phase and cannot recover a by itself.

The concrete candidate mechanism is a paid polar/isometric transform of
these blocks, coherent in k, followed by center Fourier readout and native
verification. Target cost is poly(log p), which would improve the retained
subexponential quantum upper bound; no classical lower bound is supplied.
Unpaid block synthesis, vanishing retained singular weights, discarded
workspace, or measurement of k before center readout falsify the proposed
implementation. A_gamma's existence alone pays none of those obligations.
Do not build a generic PGM framework or run a conditioning sweep in lieu
of an explicit circuit identity.

## Constructive obligations still open

An admissible decoder must supply the actual coherent kernel transform or
measurement, charge its normalization and workspace, handle its singular
sectors, and recover b,c with an inverse-polynomial success bound and
poly(log p) gates. Exact field arithmetic, uniform state preparation and
candidate validation are paid standard primitives. A nonabelian QFT or
Kloosterman-state preparation alone is not a decoder.

Fresh random classical checks can validate a returned irreducible candidate:
for distinct f,h, agreement <=1/2+3/(2sqrt(p)); use p>=37 for a uniform
constant bound below3/4 and handle the finitely many smaller primes directly.
No polynomial-time receiver, runtime separation, Q1 attack, cryptographic
deployment break or classical hardness is established. All such gates stay
false. The subexponential written composition and its finite identity checks
are distinct from an executed end-to-end quantum implementation.

Portfolio decision: the native nonlinear reconstruction question has a
paid constructive upper bound and a concrete missing operation, making it
more promising for the next hard derivation than another OPI tie-rule sweep
or a generic Rees receiver without a native application. Scalar OPI's
asymptotic classical question remains live. Weak-input isogeny conversion
remains high-impact but has no new admitted operation here. Give the block
candidate a derivation, not automatic continuation: absent a specific
gate identity, rerank independent directions instead of accumulating
nearby barriers. The next falsifying experiment is exact matrix equality
for an actually proposed circuit, including normalization and the k=0
sector; no such circuit is currently claimed.

## Follow-up: concrete affine circuit and homogeneous lift

This pass kept the same native reconstruction question and reused its
executed classical attacks. Corpus lookups for homogeneous norm characters
and tensor/Jacobi reconstruction found no matching paid decoder; that is
not evidence of hardness or novelty. The contemporary [cycle-code DQI paper](https://arxiv.org/pdf/2609.40036)
was also checked as an independent alternative: the repository's reviewed
triage already requires its LP classical baseline before extending the old
ternary route (audits/ARXIV_TRIAGE_REVIEWED.md). No new cycle-code quantum
mechanism was admitted here.
A quasipolynomial EDCP title is not a replacement for the native DCP upper
bound without a verified source conversion. These alternatives do not
justify abandoning a concrete native circuit test for another subsystem.

### A paid affine-bijection circuit, with its actual normalization

Let N=p(p-1). Prepare the pair register uniformly on x!=y. Controlled by
(x,y), reversibly replace a coefficient register(b,c) by(f(x),f(y)); this
is an invertible affine map. Project each evaluation register onto
|chi>=(p-1)^(-1/2)sum_u chi(u)|u>. The clean block is exactly

    T[(x,y),(b,c)] = chi(f(x)f(y))/((p-1)sqrt(N))
                   = K_off[(x,y),(b,c)]/alpha,
    alpha=(p-1)sqrt(N)/p = Theta(p).

This follows by multiplying the normalized preparation/projection
amplitudes, not by a norm estimate. For every irreducible basis column the
herald probability is exactly1/(p-1)^2. Running the circuit backwards on
the normalized native off-diagonal state has correct-label probability
exactly1/(p-1)^2. This explicit construction does not pay a polynomial-time
receiver; it also does not exclude a different completion.

As a separate warning against extending the promise, on ALL monic columns
let v be the normalized uniform superposition of the p perfect-square
polynomials(X-a)^2. For x!=y, (K_off v)[x,y]=(p-2)/(p sqrt(p)), hence
||K_off v||^2=(p-1)(p-2)^2/p^2=Theta(p). A constant-normalization block of
this unrestricted matrix is impossible. Those square columns are absent
from the native irreducible problem, so this is not a native no-go.

Toolbox AppendixB.2 cleans its quadratic-branching workspace because the
output root ratio r determines the input t=r/(1+r)^2 and the oriented roots
(on its stated nonboundary branches). The retained(x,y) here does not
reconstruct the two evaluations or the discarded coefficients. Thus that
specific cleanup argument cannot remove the displayed projection factor.
Independent review found no alternate paid conversion. Generic amplification
of the correct-label branch costs Theta(p), already worse than the retained
expected-sqrt(p) classical attack. Do not repeat this
circuit with a different normalization convention or build its simulator.

### Homogeneous self-duality is not coefficient recovery

The original BIT-OUTPUT oracle computes the phase of
H(u,v)=chi(u^2+buv+cv^2) using one query: route its target into |-> for
v!=0 (argument u/v) and |+> for v=0. At v=0,u!=0 its value is1, and
H(0,0)=0 is public and excluded from the phase-state domain. Thus the
lift is implementable without knowing b,c. However, its Fourier symmetry
uses no quadratic structure at all.

Let arbitrary h:P^1(F_p)->{+1,-1} satisfy sum_L h(L)=0. Extend H_h(z)=h([z])
for z!=0 and H_h(0)=0. With the unitary positive two-dimensional Fourier
transform, for k!=0,

    (F H_h)(k) = (1/p)sum_L h(L)sum_(z in L\{0}) omega^(k dot z)
                = h(k^perp),
    (F H_h)(0)=0.

Indeed, the inner sum is p-1 on the one orthogonal line and-1 on each
other line. The native coloring is balanced because sum_x chi(f(x))=-1
and its infinity value is1. Consequently its apparent dual phase oracle
is just a known perpendicular-line relabeling of the input for EVERY
balanced coloring. Direct Fourier sampling has uniform magnitude on all
nonzero frequencies and cannot read the coefficients. This falsifies
that proposed readout, not other uses of the lift or multiple-copy decoding.
For an explicit nonquadratic example at p7, assign plus to the finite lines
{0,1,3} and infinity and minus to the other four lines. Its three finite
plus points have no reflection center (none of them is the midpoint of the
other two), so it cannot be a native monic irreducible quadratic coloring;
it nevertheless has exactly the same self-duality.
The zero-vector exception must not be silently replaced by a unit-modulus
phase; uniform state preparation can exclude it explicitly. The phase-only
extension of the main algorithm below does NOT claim this homogeneous
lift: the prescribed infinity sign can depend on an unknown global
orientation of the original phase function, and the extension does not
use this lift.

### Corrected phase-oracle access: exact compiler and verification

The earlier assertion that an uncontrolled phase oracle cannot supply
fingerprints was too strong. For U_g|x>=g(x)|x>, g(x) in{+1,-1}, choose a
public computational-basis reference x0. Initialize R=x0 and apply H_B,
controlled-SWAP(X,R) on B=1, U_g on R UNCONDITIONALLY, the same controlled
swap, and H_B. On the reference subspace the middle three gates act as

    |x,B,x0> -> g(x0)[g(x)g(x0)]^B |x,B,x0>.

Conjugation by H_B therefore gives exactly

    |x,B,x0> -> g(x0)|x,B XOR L_g(x) XOR L_g(x0),x0>.

This holds for arbitrary target bits, superpositions and entanglement,
by linearity. It needs one uncontrolled phase query, two controlled swaps
of O(log p) qubits, two Hadamards, and O(log p) clean reference workspace.
The same known x0 is used throughout. A fixed query schedule accumulates
only the global factor g(x0)^Q. No controlled black-box query or value of
g(x0) is supplied. This is a general diagonal-oracle identity, not a
Legendre-specific novelty claim.

Relative fingerprint strings differ from the old ones by the same fixed
complement mask, preserving every fiber exactly. The width preparation
already uses a phase query and is unaffected. Fresh verification compares
observed relative signs with g_h(x)g_h(x0) for the public candidate h. For
a wrong irreducible h, its one-point agreement probability is

    (1+sigma S_fh/p)/2 <= 1/2+3/(2sqrt(p)),
    sigma=g_f(x0)g_h(x0),  S_fh=sum_x g_f(x)g_h(x).

The absolute quartic character-sum bound is unchanged. Thus the written
subexponential quantum composition also works with this phase interface.
The executed expected-sqrt(p) CLASSICAL baseline retains its original
ordinary bit-query model. A raw phase unitary has no ordinary classical
sign-query interpretation; do not transfer saved classical counts or
constants to a relative-bit interface without separate accounting.
Copies alone do not supply this coherent query construction, but no
information-theoretic or computational impossibility for copies is proved.
Classical-only Q1 deployment access still does not supply the quantum oracle.

The incorrect access assertion was reproduced before correction by an
exact fixed-input Sage control, now saved as
`classical_baselines/quadratic_legendre_phase_compiler.py/json`. Its first
and only execution checked all31 monic irreducible quadratics at p5/7,
all197 secret/reference pairs, and all2558 X,B basis inputs. Every case
matched the global-phase operator identity with R clean. Omitting both
controlled swaps failed1248 cases; both zero-output promise controls were
rejected. The positive and negative dense simulations each used5116
classical callback evaluations, distinct from the ONE coherent query per
compiled call. Parent inspection confirmed actual gate-by-gate propagation
and harness-only coefficients. The independent quantum review accepted
both the identity and its resource/model qualifications. No end-to-end
quantum decoder or new speedup was executed or established.

## Matrix-coset alternative: source paid, readout refuted

QUADRATIC_LEGENDRE_MATRIX_COSETS.md gives the subsequent independently
reviewed original-bit-Q2 reduction to GL2 coloring-stabilizer cosets. For
p>=41, global fingerprint failure is at most p^4(3/4)^L, with one native
query per homogeneous bit. The concrete additive-matrix Fourier readout,
after discarding the label and averaging random cosets, has a full matrix
output distribution exactly independent of the hidden coefficients. This
receiver is parked. The reduction does not by itself supply a polynomial
decoder; retained-label, coherent and collective alternatives are not
covered by the falsifier. Earlier native bounds and phase-only access
correction above are unchanged.

## Fixed-characteristic extension fields: a known-primitives positive boundary

5 November 2026. Written composition; independent adversarial review
accepted the source, orientation, transform and resource boundary. This is
an EXPLICITLY DIFFERENT parameter regime, not a solution to the growing-
prime problem above. Let q=p^n with FIXED odd prime p and n growing. Supply
an effective public field presentation, a monic irreducible quadratic over
F_q, and the same bit-output coherent character oracle on F_q. Output its
coefficients. Cost is measured in log q; no extension of the supplied query
field is allowed. The original prime-field input is not silently enlarged.

The proposed mechanism is the existing reflection fingerprint reduction,
followed by the KNOWN polynomial hidden-translation algorithm over the
additive group F_p^n, then a partial-Legendre transform to recover the width.
The source is [Friedl et al., Section3, Theorem3.5 and proof](https://www.irif.fr/~magniez/PAPIERS/fimss-sicomp13.pdf),
read in full locally. It uses degree-(p-1) linearization of sampled
nonorthogonality equations in binom(n+p-2,p-1) monomials, and has time
(n+p)^O(p). This is polynomial only when p is fixed. We supply its combined
branch oracle directly, so no controlled-access assumption about two
independent black boxes is needed.

[Decker et al., Proposition4 and Theorem2](https://arxiv.org/pdf/1107.2189)
already distinguish fixed-characteristic HQPP from growing-prime HQPP.
Their theorem cannot simply be applied to a two-color character oracle:
HQPP supplies distinct labels for different quadratic levels. Our paid
fingerprints provide the needed injective hidden-translation functions.
These are known mechanisms; no novelty or complexity separation is claimed.
The corpus lookup found no additional matching classical solver. The
catalogued prime-character norm attack receives explicit OPI shift tables,
not the secret polynomial of this oracle problem, and does not transfer.

Write f=(X-a)^2-d with d nonsquare. For q>=37, uniform independent public
x_j and W(t)=(g(x_j+t)) have global injectivity failure at most
q^2(3/4)^L. The same quartic character bound holds over F_q: the smooth
quartic curve has genus1, so its projective Hasse bound implies the looser
3sqrt(q) affine bound used here. The combined oracle is

    f0(t)=W(-t),    f1(t)=W(2a-t)=(g(-x_j+t))_j,
    f1(t+2a)=f0(t).

Each branch is implemented by L native queries, without knowing a.
Conditional on ONE good offset list, both functions are injective. The
Friedl et al. algorithm then recovers2a, including its tested zero-shift
branch, in(n+p)^O(p) time and O(L p(n+p)^(p-1)) native queries for constant
error. Its sampled nonorthogonality distribution, not arbitrary classical
disequations, is essential to its linearization proof.

After recovering a, let S contain zero and the nonzero squares, s=|S|=(q+1)/2.
Uniform preparation on S has constant-success rejection; compute a canonical
square root reversibly and query g(a+sqrt(z))=chi(z-d). Public nonsquare
rejection and finite-field square roots have charged expected poly(log q)
cost. For bounded execution cap retries and charge ABORT. The resulting
state is s^(-1/2) sum_(z in S) chi(z-d)|z>.

There is no need for a supplied Gauss phase. Let psi(x)=exp(2pi i Tr(x)/p),
let F be the positive trace-pairing additive QFT, and set D(0)=1 and
D(k)=chi(k) for k!=0. For C[y,z]=chi(y-z), J the all-ones matrix and
nonzero quadratic Gauss sum tau=sum_t chi(t)psi(t),

    U=F^dagger D F=C/tau+J/q,    |tau|=sqrt(q).

U is unitary and implementable with public character arithmetic and two
additive QFTs; the trace-pairing basis conversion is public linear algebra.
At y=d its output amplitude is

    chi(-1)*sqrt(s)/tau + T/(q sqrt(s)),
    T=sum_(z in S) chi(z-d)=-(1+chi(-1))/2.

Thus success is at least
(sqrt(s/q)-1/(q sqrt(s)))^2 >=1/3 for q>=37, regardless of the Gauss phase.
The identity for T uses the indicator(1+chi(z)+1_(z=0))/2 and the ordinary
quadratic sum sum_z chi(z(z-d))=-1. No unknown amplitude sign is erased.
Repeat, freshly verify candidates with the quartic agreement bound, and
return b=-2a,c=a^2-d. Fixed small q can be handled directly at constant cost.
Allocate error among the global list, hidden translation, repeated width
trials, verification, capped preparations and approximate gates. For fixed p,
all resources, including space and precision, are polynomial in log q and
log(1/error). This is a written bounded-error algorithm, not an executed
quantum recovery or a new primitive. The relative-bit compiler also extends
it to the same uncontrolled +/-1 phase interface: the global fingerprint
complement preserves fibers and the width step already uses phase queries.
No projective/infinity lift is used here.

The retained classical competitors extend to this field regime. Full-data
moments take O(q) queries/field operations. For the reflection stage, split
a public F_p basis into two halves; for odd n, split the middle coordinate
as i+Mj mod p, with M=ceil(sqrt(p)). This gives public sets U,V of size
O(sqrt(q)) with U+V=F_q. The two fingerprint lists therefore find2a in
O(sqrt(q)polylog(q)) work. The multiplicative quotient F_q^*/{+1,-1}
width birthday stage requires no discrete log and has the same expected
bound. These are classical upper bounds, not classical lower bounds or a
proof that no better fixed-characteristic attack exists. Old prime-field
execution counts are not repinned to extension-field inputs.

Decision: retain this positive parameter boundary and remove it from the
unsolved quantum-reconstruction queue. It does not pay a growing-prime
receiver: p=q,n=1 is not the fixed-p polynomial regime. No new simulator
or field-size sweep is warranted for this composition of published tools.
The growing-prime polynomial receiver and a sharper classical algorithm
remain unresolved scientific questions.
