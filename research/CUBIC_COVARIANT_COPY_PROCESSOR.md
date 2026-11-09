# A six-copy covariant processor does not expose the cubic frame

7 November2026. Reviewed exact falsifier; focused proof/source review and
phase-sensitive classical algebra control complete. No human/formal review.
The proposed processor is already known Clifford-commutant machinery, not
a new quantum primitive. Its particular use as a hidden-frame extractor
is tested here. No general learning impossibility or novelty is claimed.

## Native question, selection and baseline

Input fresh exact IID copies of
psi=C*2^(-n/2)*sum_x (-1)^f(x)|x>, unknown Clifford C and unknown cubic
Boolean f with maximum hyperedge occurrence2. Return a known polynomial
quantum circuit approximating psi in trace distance epsilon, failure<=eta,
with polynomial copies/gates/classical time. No frame, inverse, conjugate
source, chosen-state oracle or stabilizer advice is provided. This preserves
the parked HIDDEN_CUBIC_PHASE_LEARNING.md contract, rather than weakening it.
Its known-frame learner is paid; the unknown commuting phase-frame extractor
is not. The proposed new operation uses six-copy Clifford covariance to
reduce magic or generate derivative states, followed by stabilizer recovery.
The hoped advantage is efficient copy-based device learning beyond supplied
frames/fixed magic blocks, not a classical-input separation.

STATE/TRAPS and corpus been-tried/baseline lookups preceded the actual
literature reads. Independent alternatives were compared: collaborative
scalar-OPI decoding still lacks the original support-phase erasure operation;
even perfect sparse finite-field full-value period recovery reveals only
the classical exponent gcd (general collisions need not satisfy an HSP promise); folded-DQI query separation uses joint predicates on exponential
block alphabets. Cycle-DQI has paid LP decoding but the checked cut regimes
are dominated by the source's classical comparator. None supplies a new
native endpoint. A concrete fully paid copy operation is worth this cheap
exact test; it does not justify continuing cubic barriers indefinitely.

The strongest applicable baseline for this experiment is the exact classical
Bell sampler with SUPPLIED f,C: a uniform shift gives a quadratic derivative,
whose Fourier support and uniform sampling are computed by Gaussian
elimination. This does not learn unknown f,C. Known-frame X/Z derivative
learning and supplied-product/MPS methods retain their actual access limits.
The corpus also lists tensor-network contraction; bounded occurrence does
not by itself supply small global tensor-network width. No classical
inference hardness is claimed.

## Paid processor and existing source

Let A=I_6+J_6 over F2. Coordinatewise on six n-qubit copies, apply the
reversible linear map y_i=x_i+sum_j x_j. It is an involution and has a
constant-size CNOT realization per physical qubit, hence O(n) gates.
It is orthogonal, fixes the all-ones vector and preserves Hamming weight
mod4: its columns have weight5 and pairwise intersection4. Consequently
U_A commutes with C^tensor6 for EVERY n-qubit Clifford C. One can verify
this directly on global H,S,CNOT and Pauli generators.

Gross--Nezami--Walter1712.08628v3 explicitly supplies this anti-identity:
Eq(1.4), Eq(3.12)--(3.13), Definition4.29, Lemma4.30 and Example4.32.
Its actual matrix is retained in
audits/sources/native_selection_2026_11_07/clifford_commutant.pdf/.txt.
The same paper already supplies six-copy stabilizer TESTING. Such testing
is not recovery of the missing cubic frame; no new stabilizer-test claim
is made here. Other commutant projectors, superpositions, controlled tests,
larger-copy maps and arbitrary retained quantum correlations are not covered
by the specific receiver conclusions below.

## Discarding five registers preserves only the same stabilizer group

For a density matrix rho, define Phi(rho)=Tr_(five outputs)
U_A rho^tensor6 U_A^dagger. For every Hermitian n-qubit Pauli P,

    Tr(P Phi(rho)) = Tr(P rho)^5.

Indeed conjugating P on one output gives P on exactly five input copies.
The Hermitian Y phase is unchanged since i^(5a dot b)=i^(a dot b).
Therefore |Tr(P rho)|=1 iff |Tr(P Phi(rho))|=1, with the same sign.
The exact signed Pauli stabilizer group is UNCHANGED. In particular this
operation cannot expose new Pauli stabilizers representing cubic axes.

For the native Clifford-hidden cubic source every nonstabilizer Pauli
expectation has magnitude<=1/2. Before C it is the mean of the total quadratic phase
g_(a,b)(x)=f(x+a)+f(x)+b dot x, up to the Hermitian Pauli phase. A
nonconstant linear phase has zero mean; a nonconstant quadratic has
alternating rank>=2 and any nonzero Walsh magnitude2^(-rank/2)<=1/2.
A CONSTANT TOTAL phase gives exactly the signed Pauli stabilizers; a
nonconstant linear derivative can be canceled by b dot x, as for
f=x1*x2 and P=X1 Z2. Constancy of the derivative alone is not the criterion. Clifford
conjugation preserves these magnitudes. No occurrence bound is needed for
this statement; it covers every Boolean degree<=3 phase state.

After j iterations, the coefficients are r_P^(5^j). Let sigma_stab be the
normalized projector onto the original signed Pauli-stabilizer code:
sigma_stab=2^-n sum_(|r_P|=1) r_P P. Orthogonality of Paulis and the
Hilbert--Schmidt/trace-norm inequality give

    D(Phi^j(psi), sigma_stab) <= 2^(n-5^j-1).

Taking 5^j>=n+log2(1/(2epsilon)) gives error<=epsilon using6^j copies,
at most a polynomial in n+log(1/epsilon). The circuit/copy tree is paid;
this convergence is frame LOSS, not a learner. For a product of CCZ|+++>
blocks the Pauli stabilizer is trivial, so the limit is I/2^n for every C.
At trace distance<=epsilon from I/2^n, every pure-state overlap satisfies
<phi|rho|phi><=2^-n+epsilon, so a pure stabilizer-state learner is not
justified. This bound is on the squared-fidelity convention.
Intermediate states or environments could still carry information; this
does not exclude a different receiver that uses them.

## Exact Bell-conditioned instrument

The alternative is to retain TWO outputs and Bell-measure pairs(2,3) and
(4,5). This might appear to keep derivative information discarded above.
For any arbitrary pure state psi=sum_x alpha_x|x>, including complex and
nonuniform amplitudes, use the Bell bra convention

    <B_(a,c)|=2^(-n/2) sum_z (-1)^(c dot z)<z+a,z|,
    beta_(a,c)=<B_(a,c)|psi tensor psi>.

Let the two outcomes be(a,c),(b,d), and put u=a+b,v=c+d. In output
coordinates the constraints make T=sum_i y_i=y1+y6+u. Since x_i=y_i+T,
the two sums become ordinary Bell overlaps after substitutions z'=z+T
and w'=w+T. They contribute beta_(a,c)*beta_(b,d)*(-1)^(v dot T).
The remaining amplitudes are alpha_(y6+u)*alpha_(y1+u). Therefore the
UNNORMALIZED retained branch is exactly

    (-1)^(v dot u) beta_(a,c) beta_(b,d)
       * (Z^v X^u psi) tensor (Z^v X^u psi).

There is an implicit swap of the two retained registers; it is harmless
because their source states are identical. Its probability is
|beta_(a,c)|^2 |beta_(b,d)|^2. Every nonzero branch,
after the known Pauli correction, returns two unchanged copies of psi.
The classical outcomes are exactly TWO independent ordinary Bell samples.
This is an equivalence of the stated classical/quantum instrument to
ordinary Bell sampling plus untouched source copies, not classical
simulation of psi or a lower bound on general Bell-based inference.
No rare-event postselection or conditional re-preparation is hidden in
the identity: all outcomes and their probabilities are included.
Equivalently, U_A commutes with every measured Bell projector: pair
operators X_i^u X_j^u and Z_i^v Z_j^v have even copy support, which A fixes.
Measure first, then apply the known branch Pauli/swap. This gives an
independent proof of both the probability law and instrument equivalence.

For this restricted family the conclusion covers every invertible binary
copy-linear six-register map commuting with all tensor-power Cliffords.
Its matrix must be orthogonal and preserve weight mod4, hence every row
has weight1 or5. A weight1 row e_j can be orthogonal to a weight5 row only
when the latter has its sole zero in position j. No further distinct row
of either allowable type is orthogonal to both, so such a mixed matrix
cannot have rank6. All rows therefore have weight1 (a permutation) or5
(an anti-permutation). Permutations act trivially on identical input
copies, so they give the same ordinary-Bell receiver. This classifies
copy-LINEAR basis permutations, NOT all unitaries in the Clifford commutant.

## Independent source screens retained with their limits

The actual folded-DQI2610.02145v1 Lemma11 pays complete canonical-list
fiber summation with fixed global padding and an explicit heralding law.
Lemma12 pays constant-size complete lists for its folded dual at fixed
slack. Constant success additionally uses its typical independent balanced
oracle concentration argument; bounded list size alone does not prove it.
Section2.4/3 uses arbitrary JOINT block predicates on an exponential
alphabet. This differs from the native full-table scalar-OPI objective and
input size. Neither its lower bound nor a new native decoder is transferred.

The actual cycle-DQI2609.40036v1 Theorem1 pays a fixed-target imperfect-
decoding law, including one-coordinate error variants; Corollary2 pays
LP decoding on its stated growing-girth ensemble. Section4's asymptotic
classical TPM cut guarantee is stronger in the compared large-degree
regime. Its random-Max2LIN annealing comparison is empirical, not a
universal classical theorem. Neither inspected source admits a new native
route in this pass. Primary texts are retained in the same source folder.

## Review and next decision

The discard-channel derivation was independently obtained by a helper.
A focused Claude check of the Bell identity and small copy-linear class
completed (estimated USD0.327524), distinct from the previous static factor-
search tasks. Accepted: projector commutation, exact global phase and swap,
complex-amplitude validity, all probabilities and the restricted O6
classification. These were checked against the direct proof and exact control.

REJECTED Claude side claim: its Section3 says C^T C is generally not a Pauli.
In fact complex conjugation changes Pauli signs, not symplectic labels, so
C and C* induce the same binary symplectic map. Thus C^T C=(C*)^dagger C
has trivial symplectic action and is a Pauli up to global phase. For example
C=SH gives C^T C=H Z H=X. The earlier exact classical Bell sampler's affine
Clifford label law remains valid; this erroneous side remark is not used.
The report's broad suggestions about necessary conditions for every future
receiver are not a theorem and are not adopted. Nonunitary commutant
projector examples in its speculation are not relied on.

The exact CAS control audits/controls/cubic_covariant_copy/control.py/.json
uses normalized complex input (3/5,(12+16i)/25). All16 Bell branches match
the unnormalized identity,9 have nonzero probability, probabilities sum1,
and X,Y,Z coefficients are their FIFTH powers. The native three-qubit CCZ
control has only the identity Pauli stabilizer and max nonstabilizer
magnitude1/2. This checks phases/normalization and a concrete counterfamily,
not the all-n convergence proof. No full learner or quantum execution.
Independent focused final review is COMPLETE and was read by the parent:
audits/reviews/2026-11-07-cubic-covariant-copy.md. It confirms the identities,
copy clock and restricted classification; its total-phase and squared-
overlap clarifications are incorporated. Aggregate44 saved reported
estimates USD35.054340,22 completed reports is NOT an invoice or remaining
balance. No pending Claude call or retry remains.
No learner, advantage, native hardness, general coherent-receiver no-go,
novelty or quantum execution is established. These two processor routes are rejected; the original unknown-frame learner
remains PARKED. Independently pivot; do not build a convolution learner or
another gap/width sweep. A new task must supply a native operation whose
charged mechanism differs from the closed receivers before implementation.
