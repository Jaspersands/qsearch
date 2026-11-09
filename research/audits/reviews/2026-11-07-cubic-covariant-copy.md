# Six-copy cubic-frame receiver: focused final review

7 November 2026. **ACCEPT the written identities, resource bounds and restricted
receiver conclusions in CUBIC_COVARIANT_COPY_PROCESSOR.md.** The total-phase
clarification requested during review is now present. Reject the Claude report's
separate assertion that C^T C need not be Pauli up to phase. There is no remaining
mathematical blocker to closing these particular receivers. This does not accept
a learner, a general receiver impossibility, novelty, or a quantum execution.

Read current STATE/TRAPS, the actual topic note, the focused Claude response, and
the pertinent Gross--Nezami--Walter primary passages. No Git, network/API, new
implementation or extra experiment was used. The finite controls are useful
phase/normalization regressions; the all-n conclusions below follow from proofs.

## Paid covariance and one-output channel

Over F2, A=I_6+J_6 satisfies A^2=A^T A=I and A1=1. For a bit column v, it
either fixes v (even weight) or complements it (odd weight). Hence it preserves
weight modulo4. These identities give commutation with transversal H, S and
Paulis. Coordinatewise copy mixing also commutes with the CNOTs within each
copy. Thus the O(n)-gate map commutes with C^tensor6 for every n-qubit Clifford.
GNW Eq(1.4), Eq(3.12)--(3.13), and its anti-permutation discussion identify this
as known machinery. Their stabilizer tester is not a hidden-frame extractor.

Conjugating a Hermitian Pauli on one output gives that SAME Pauli on five
inputs. For P=i^(a dot b)X^a Z^b the apparent phase difference is
i^(4 a dot b)=1, so Y causes no sign defect. Consequently, for every density
matrix rho, r_P(Phi(rho))=r_P(rho)^5. Exact signed Pauli stabilizers are preserved
and no new ones appear.

For a Boolean phase of degree at most3, the relevant Walsh phase is the TOTAL
polynomial g_(a,b)=f(x+a)+f(x)+b dot x. Its nonconstant linear case has zero
mean; a genuine quadratic has alternating rank at least2 and nonzero Walsh
magnitude at most1/2. Constant total phase gives a stabilizer. In particular,
one must allow cancellation of a linear derivative by b dot x, as the revised
note does. This argument needs no bounded-occurrence promise.

After j iterations all nonstabilizer coefficients have magnitude at most
2^(-5^j). Pauli orthogonality and ||X||_1<=sqrt(2^n)||X||_2 give

    D(Phi^j(rho), sigma_stab) <= 2^(n-5^j-1).

Here sigma_stab=2^-n sum_(|r_P|=1) r_P P is the normalized projector onto the
original signed-stabilizer code. Preparing each tree from fresh copies costs
6^j copies and O(n 6^j) gates, polynomial in n+log(1/epsilon) at the stated
choice of j. Consumed copies are not silently recycled.

The product of CCZ|+++> blocks belongs to the native occurrence promise and
has trivial Pauli stabilizer, so its limit is I/2^n for every hidden Clifford.
Precisely, D(rho,I/2^n)<=epsilon implies
<phi|rho|phi><=2^-n+epsilon for every pure phi. This is the squared-fidelity
convention; using the explicit overlap avoids an ambiguity in the word
"fidelity." Neither this limit nor preservation of exact stabilizers rules
out using intermediate states, environments, or another measurement.

## Arbitrary-complex pure-state Bell instrument

With the note's bra convention, beta_(a,c) is a bilinear amplitude in the
coefficients of psi, not a conjugate-linear expression. For outcomes (a,c),
(b,d), write u=a+b and v=c+d. The output constraints give
T=y1+y6+u, independent of the two measured summation variables. Translating
those variables by T yields the two ordinary Bell amplitudes and phase
(-1)^(v dot T). The retained amplitudes are alpha_(y6+u) alpha_(y1+u).
Thus the unnormalized branch is exactly

    (-1)^(v dot u) beta_(a,c) beta_(b,d)
          (Z^v X^u psi) tensor (Z^v X^u psi).

The swap is harmless because these source states are identical. No reality,
uniform-amplitude or cubic assumption was used. Its probability is
|beta_(a,c)|^2 |beta_(b,d)|^2, including the zero-probability branches, and
Bell completeness makes the total probability1. After the known Pauli
correction the retained state is two untouched copies, independent of the
classical outcomes. This is an exact instrument equivalence, not a statement
that the source or its Bell samples can be classically simulated without advice.

As a separate consistency check, the pair operators generating each measured
Bell projector have even copy support, fixed by A and A^T. The processor
commutes with those projectors. This proves the outcome law independently of
the amplitude calculation; the latter also establishes the retained phase
and swap. No rare event, free conjugate state, or conditional re-preparation
is hidden in this operation.

## Copy-linear scope and correction to the external report

For an invertible binary copy-linear basis permutation commuting with all
sixth tensor powers of Cliffords, H implies orthogonality and S implies
weight preservation modulo4. Columns have weight1 or5. The inverse is the
transpose and has the same preservation property, so the same holds for rows.
A weight1 row e_j can be orthogonal to a weight5 row only if the latter is
1+e_j. No third distinct admissible row is orthogonal to both. Thus a full-rank
matrix cannot mix the two types: it is a permutation or anti-permutation.
Permutations act trivially on identical source copies. This proves the stated
classification, not a classification of arbitrary commutant unitaries,
projectors, controlled tests, linear combinations or larger-copy procedures.

The Claude Section3 caveat is false. For Hermitian Pauli labels v,
P_v^*=(-1)^(q(v))P_v. If C induces symplectic map F, conjugating its Pauli
action entrywise shows that C* induces the SAME F, with possibly different
Pauli signs. Therefore C^T=(C*)^dagger induces F^-1, and C^T C induces the
identity symplectic map. The Clifford kernel is the Pauli group up to global
phase, proving the topic note's correction. For example, C=SH gives
C^T C=H Z H=X. The associated Pauli is generally UNKNOWN without the frame;
this fact does not grant access to conjugate copies. It also does not alter
the exact, frame-independent instrument identity above.

## Disposition

Accept the main derivations and the restricted negative experiment: discarding
five outputs cannot expose new exact stabilizers; the specified two-Bell
instrument is ordinary Bell sampling plus unchanged copies; the six-copy
binary-linear covariant class adds no different such instrument. Reject the
external report's C^T C assertion and do not adopt its speculative universal
conditions on future receivers. The current controls do not establish
asymptotics. Close this receiver and select a different native operation; no
convolution-learning implementation or adjacent control sweep is warranted.
