# Hidden cubic phase learning: an admission experiment

Status7 November2026: reviewed admission pass complete; candidate PARKED.
The factored-event detection lemma is proved; no paid phase-frame extractor
or learner is established. Independently choose the next mechanism.
The single question is whether fresh copies of an unknown-Clifford bounded-occurrence
cubic phase state permit polynomial-time recovery of a usable phase frame.

## Native contract and choice

For every growing n, input fresh exact IID copies of
psi=C 2^(-n/2) sum_x (-1)^f(x)|x>, unknown Clifford C and unknown homogeneous
cubic Boolean f with maximum hyperedge occurrence Delta=2. Return a known
polynomial-size circuit within pure-state trace distance epsilon, failure<=eta,
using poly(n,1/epsilon,log1/eta) copies/gates/classical time. Lower-degree phase
terms may be absorbed in C. No unknown inverse, conjugate source, channel,
chosen-state oracle, hidden axes or supplied stabilizer group.

The proposed mechanism is to recover local factored constraints in an affine
Clifford relabeling of Bell outcomes, recover a valid commuting phase frame,
then apply the known-frame cubic learner and fresh-copy verification by the
returned circuit's KNOWN inverse. Target benefit: polynomial learning beyond
product blocks or few magic gates. This is quantum-device learning; no classical
input separation, novelty, Shor-level result or proved advantage is claimed.

Comparison: recent arithmetic constructions are complete and do not justify
an adjacent extension. Independent OPI/DQI screens have no new paid decoder;
a sequential bosonic-current character sampler would reproduce the already
available QCT endpoint. This candidate has a concrete exact observable and a
specific algebraic blocker, so it is selected for one admission experiment.
It does not earn an indefinite line of nearby barriers.

## Prior work and strongest classical attacks

Corpus been-tried and baselines were checked before selection. Similarity hits
include the previous one-rotation learner and old DCP hypergraph constructions;
none is evidence for this contract. Actual primary texts reviewed:

- ABB2208.07851v2 Sec3.1 Algorithm1/Theorem3: known-frame single-qubit X/Z
  derivative samples and classical F2 elimination learn cubic phases. The
  frame must be paid before invocation. Source under
  audits/sources/hidden_cubic_learning/phase_learning.*.
- Haug2609.27128v1 Theorem2, full-tomography paragraph and AppendixI: hidden
  product blocks, exponential block-width tomography, and classical Bell
  sampling from a SUPPLIED MPS with KNOWN Clifford. No frame inside an
  arbitrary irreducible block is supplied. Reuse one_rotation_learning sources.
- Fechisin2610.00464v1 SecIV.B Algorithm1: supplied classical stabilizer subgroup,
  and explicit enumeration over F_p^ell. It is not copy-based frame recovery.
  Source under audits/sources/hidden_cubic_learning/hierarchy_stabilizers.*.

Actual source review: audits/reviews/2026-11-07-hidden-cubic-source.md.

A stronger classical baseline than generic tensor contraction is available for
this exact Bell experiment when f,C are SUPPLIED. Write Q_a(x)=f(x)+f(x+a).
For uniform a, Q_a is quadratic. Let B_a be its alternating polar matrix,
R=ker(B_a), rank r. Its Fourier support is the affine solution space
    b dot z = Q_a(z)+Q_a(0), z in R.
The right side is linear on R. Gaussian elimination computes a point and basis;
choose b uniformly from this affine space, then apply the known Clifford's
affine Bell-label map. The normalized quadratic Fourier magnitude squared is
2^-r on support, so the exact joint law is
    p_f(a,b)=2^(-3n) [sum_x (-1)^(Q_a(x)+b dot x)]^2
             =2^(-n-r) on support, 0 otherwise.
This is polynomial classical time with explicit f,C. It is NOT a method to
learn unknown f,C from copies. The offset cannot in general be replaced by
Q_a's linear coefficient: characteristic2 quadratics can be nonzero on their
polar radical. No lower bound against classical inference from measured data.

## Local constraints and the unresolved extraction

Let N(i) be the other vertices in the cubic triples incident to i, |N(i)|<=4.
If a_j=0 for all j in N(i), Q_a is independent of x_i. Therefore
    R_i(a,b)=b_i product_{j in N(i)}(1+a_j)=0
on every Bell outcome. This has Boolean degree<=5. A Clifford relabels Bell
labels affinely preserving the universal swap quadratic q=a dot b; the local
constraints become products of at most5 affine forms in physical coordinates.
This is an exact identity, not an algorithm for finding its hidden factors.

A naive plan learns all degree<=5 equations K5 by evaluation nullspace. The
uniform gap for EVERY nonzero degree5 polynomial is not established. More
narrowly, the following factored-event gap would ensure that a polynomial
sample nullspace contains NO false product of<=5 affine forms, even if it
contains false unfactored equations. Factor extraction inside this polynomial
space is still an unproved operation. Generic Boolean solving, hidden-matrix
enumeration and rank-minimization are not polynomial subroutines by default.

## Factored-event gap: independently reviewed derivation

For ANY Boolean phase f of degree d, not necessarily bounded occurrence, and
ANY product P of k affine forms in its two-copy Bell labels, either Pr[P=1]=0
or
    Pr[P=1] >= gamma(d,k)=2^(-2k-(d-1)(2^k-1)).
The same holds after an arbitrary unknown Clifford, because its affine Bell
relabeling preserves a product of k affine forms. Inconsistent/dependent
parity equations reduce to a rank t<=k projector or the zero event.

Proof: P=1 is a joint eigenvalue event for t independent commuting Bell
parities, hence a projector Pi=2^-t sum_{s in F2^t} G_s onto t prescribed
Pauli eigenspaces on2n qubits. All G_s are REAL signed Paulis: Bell parities
are generated by X_j X'_j and Z_j Z'_j. Write G_s=eps_s X^u_s Z^v_s with
eps_s=+/-1, accounting for the action on basis states. Put F(z)=f(x)+f(y),
z=(x,y). The projected amplitude at z is
    2^(-n-t) (-1)^F(z) S(z),
where S(z)=sum_s (-1)^r_s(z), r_0=0, and explicitly
r_s(z)=F(z+u_s)+F(z)+v_s dot(z+u_s)+e_s, eps_s=(-1)^e_s.
Each r_s has Boolean degree<=d-1
for d>=2: F(z+u_s)+F(z) is a derivative and the Pauli phase adds only an
affine term. Let h(z) indicate S(z)!=0. As a Boolean function of at most
2^t-1 bits r_s, h has a multilinear ANF of degree<=2^t-1. Thus its composed
Boolean degree is at most(d-1)(2^t-1). If h is nonzero, the Reed-Muller minimum
weight bound gives E_z h >=2^(-(d-1)(2^t-1)); this remains a valid weaker
bound when the degree bound exceeds2n. Since nonzero integer S has |S|>=1,
    ||Pi psi^tensor2||^2=2^-2t E_z S(z)^2 >=gamma(d,t)>=gamma(d,k).
This proves the asserted dichotomy for d>=2; d=1 can be treated as stabilizer
learning separately. No typical-instance or finite-size premise is used.

For d=3,k=5 the deliberately loose constant is2^-72. There are at most
2^((2n+1)k) ordered affine-factor products. Therefore
    M>=gamma^-1*((2n+1)k ln2+ln(1/eta))
IID Bell samples exclude every false such product with probability>=1-eta.
The evaluation matrix has O(n^5) columns and M=O(n+log1/eta) with an enormous
constant; Gaussian elimination is polynomial. This does NOT say its whole
nullspace equals K5, does NOT locate factored elements, and does NOT learn a
state. For shorter products take all lengths<=5 and add ln5 to the bound,
or pad with affine constant1 so the displayed count already covers them.

## Prescribed-value factor search contains graph coloring

This only attacks an UNRESTRICTED replacement subroutine, not the native
quantum family. For a simple graph G on m vertices, form the explicit point
set S_G={e_u+e_v : uv in E(G)} in F2^m. Compute the complete degree<=2
vanishing space V_G by polynomial-size evaluation and Gaussian elimination.
Ask whether V_G contains P=(1+ell_1)(1+ell_2), with homogeneous linear ell_i.
The condition P(e_u+e_v)=0 is exactly
    (ell_1(e_u),ell_2(e_u)) != (ell_1(e_v),ell_2(e_v)).
Consequently such a P exists iff G is4-colorable; the factors supply the
coloring. P(0)=1 ensures P is not the zero Boolean polynomial. Allowing
arbitrary affine factors but requiring P(0)=1 gives exactly the same form.
One may add a disjoint K4 to require the two linear forms independent.
Thus even locating a nonzero two-affine-factor member with a prescribed
nonzero value is not a free generic polynomial-time operation. This is a
polynomial reduction, not an NP-hardness claim for Bell-supported spaces.
The unrestricted decision problem is in NP, and standard4-colorability
NP-completeness therefore applies. Primary benchmark: Huang1304.5808v2,
actual Theorem6 and Section2 proof, https://arxiv.org/pdf/1304.5808v2.
No inference is made that graph point sets are realizable by this native
quantum source; exploiting the phase-state promise could still succeed.
The narrower reduction is independently reviewed. The prescribed nonzero
value is ESSENTIAL: without it, sum_i x_i is already an easy linear factor
vanishing on every edge vector. We have not proved that returning just any
factored equation, or any native Bell frame, is NP-hard.

## Falsifiers and next decisive experiment

Reject promotion if the classical sampler/law or local constraints fail,
if factored-event probability can escape the proof, if the algebraic extraction
requires exponential search, or if a stronger applicable learner already
covers the full family. Finite controls only falsify formulas. No full solver,
quantum execution, classical separation, novelty, noisy-source or growing-Delta
claim. The decisive open question is a paid extraction operation returning a
valid phase frame from a sample nullspace whose factored elements are exact;
full K5 advice is a stronger conditional algebra question, not native input.

## Reviews, exact control and API outcomes

Independent proof review audits/reviews/2026-11-07-hidden-cubic-factored-gap.md
accepts the real-Pauli, derivative-degree, normalization and simultaneous
adaptive-product guarantees. The source review also independently accepts
the scoped graph-coloring reduction and PARK decision. No unconditional
hardness conclusion for the native source follows.

Exact CAS control audits/controls/hidden_cubic_learning/control.py and.json
uses six edge variables and the four vertex-star triples of K4. Each variable
has occurrence2. It checks ALL4096 Bell probabilities against the classical
quadratic-radical law: support925, derivative ranks0/2/4 occurring1/7/56 times.
All local constraints hold. A concrete radical-offset counterexample rejects
using just quadratic linear coefficients. Algebraic affine Clifford relabeling
is a swap-preserving bijection; this part is not a separate quantum simulation.
K1=0 and K2 dimension1 in this SIX-qubit instance only; by the checked Haug
classification it has no nontrivial Clifford product cut. This proves no
unbounded-width family. One three-factor event has exact probability1/8;
finite agreement does not establish the all-n gap. First execution stopped
at Sage's QQ(numerator,denominator) API; correcting rational construction
allowed the complete exact check to pass. No source formula was weakened.

Two distinct Claude requests under audits/claude_runs/
2026-11-07-hidden-cubic-{gap,extraction} are TERMINAL max_tokens with EMPTY
response files. Opus general-K5-gap:3963 input/32768 output, estimated
USD0.671212. Fable conditional exact-K5-extraction:4039 input/32768 output,
estimated USD1.67879. Total USD2.350002. No report, mathematical evidence,
refusal, retry, pending call or remaining-balance inference. Their immutable
briefs predate the narrower factored-event proof, which was derived and
reviewed independently. Future API work should isolate one precise lemma;
no automatic budget doubling or retry of these empty broad obligations.

Decision: PARK. The sampling lemma is a reusable sufficient bound for the
relevant factored equations; usable-frame extraction remains a scientific
blocker, even with full K5 advice. Do not build a generic factor backend or
perform further gap/width sweeps. Reopen only with a concrete extraction
operation or a source theorem that pays it; otherwise compare independent
externally valuable native mechanisms. All learner, novelty, speedup,
quantum-execution, noisy-source and native-hardness gates remain false.


Milestone checks: STATE/title/Now/Parked row match the newest handoff; two
primary PDF hashes, both immutable API snapshot bundles, terminal statuses,
review files, exact control values and false claim gates verified. Scoped
diff/whitespace checks passed. No full suite, unrelated rerun or Git commit.
