# Open folded XXZ: coherent transform and matched classical readouts

7 November 2026. CLOSED reviewed WRITTEN arbitrary-input unitary construction.
No novelty, classical separation, practicality, implementation, human/formal
verification or quantum execution claim. Previous pass was PROGRESS;
STATE/TRAPS matched Quintic Surface P2 Reduction before independent selection.

## Selection and candidate contracts

Selected question: does the full open folded XXZ evolution admit a uniform
polynomial BIT/gate circuit at binary-encoded time, on arbitrary quantum input,
with every conserved sector discovered coherently from the physical spins?
The new operation to audit is a complete reversible basis map, not a supplied
Bethe eigenstate or another fixed-degree arithmetic extension.

Compared alternatives before admission:
- Native integral-matrix conjugacy: expanded A,B over Z, output unimodular
  intertwiner or NO. Mechanism would combine Hom-to-principality with quantum
  factoring/units/PIP; desired polynomial input-BIT cost. BHJ2022 already gives
  the polynomial arithmetic reduction, and AMITSUR_ARITHMETIC_REUSE_AUDIT.md
  retains the compact/integral interface. No new operation; not admitted.
- Growing stabilizer-rank tomography: fresh IID copies, unknown components,
  output approximate stabilizer combination in poly(n,k,1/epsilon) resources.
  Candidate polynomial optimized extent would feed known copy-only learning;
  actual2610.06819 supplies only exp(O(sqrt(k logk))). In-span reconditioning
  already falsified; no constructive unrestricted replacement. Not admitted.
- Dihedral coset recovery: native IID labeled phase states, recover hidden
  shift in poly(logN) time/copies; collision sieving would need a new paid
  collision/decoder operation. Existing sieve/subset-sum barriers are scoped,
  not hardness. No new operation supplied; not admitted.

Corpus been-tried preceded actual literature; baselines for the precise Bethe
transform returned no catalog match, which is not evidence of hardness.
Ruiz et al.2411.15132v3 actual Eq(3.6)/(3.30) and Sections4.2/4.3 give polynomial
reversible classical gates taking Slater determinants to specified folded
chain eigenstates. Source discusses general XXZ difficulties separately;
do not transfer those difficulties to these coefficient-permuted states.
Native Hamiltonian and a prospective all-sector proof are below. Independent
selection prefers this concrete operation to the rejected alternatives.

Expected advantage is poly(log|t|) quantum evolution versus direct O(|t|)
time stepping, NOT an established advantage over strongest classical methods.
A full basis-input classical match is mandatory. Strongest attacks: free
fermion diagonalization, Slater determinant sampling, reversible bit mapping,
and computationally tractable-state estimation. Falsifiers: a missing sector,
nonunique labels, extra hopping multiplicity/phase/boundary potential,
unpaid label advice, exponentially ill-conditioned transform, or precision
cost polynomial in |t| rather than its bit length.

## 1. Exact all-sector bijection

Native contract: for every N>=2, on N+2 physical qubits define

    H_N = -(1/8) sum_(j=0)^(N-2)
          (1+Z_j Z_(j+3))(X_(j+1)X_(j+2)+Y_(j+1)Y_(j+2)).

Input is N, binary rational t, target error epsilon, and one arbitrary quantum
state on these qubits, possibly entangled with a reference. Output applies
exp(-it H_N) approximately. This quantum-input unitary task supplies neither
a classical description nor a preparation/reflection oracle for that state.
There is no claim that preparing an application-specific initial state is free.

Write L=N+1 for the number of bonds. Retain s0 and change basis to
b_i=s_i XOR s_(i+1), i=0,...,N. This invertible classical map includes all
four values of the two boundary spins; there is no periodic boundary constraint.
The source Pauli term has no diagonal entries. It exchanges a01a with a10a
with coefficient -1/2. On bonds this is exactly 011 <-> 110 at every
consecutive triple. The pair of flipped physical sites uniquely identifies
the term, so distinct terms cannot produce a repeated transition.

Parse b greedily with A=11, B=10, C=0, and one final unpaired 1 denoted D.
These three codewords are prefix-free; the only incomplete suffix is D.
Every zero terminates a run of 2a+b ones and contributes A^a C for b=0,
or A^a B for b=1. A final run contributes A^a D^d. Thus every string has
exactly one parse, including odd runs and a trailing 1.

Let m count A, let w be the ordered B/C word, h=|w|, d indicate D, and
ell=m+h. Replace A by 1 and each B/C by 0 to obtain q in {0,1}^ell of
weight m. The conserved label is (s0,w,d,m). A label is valid precisely when
L=2m+2#B+#C+d. Given the label and q, put the letters of w into successive
zeros, A into successive ones, append D^d, expand, and prefix-XOR with s0.
This proves a bijection; each label has exactly binomial(ell,m) states.
Both directions are elementary polynomial-time string computations.

A move 011->110 is either CA->AC or BA->AB, according to whether its zero
is a standalone C or the end of B. Conversely, in 110->011 an even preceding
1-run gives AC->CA and an odd run gives AB->BA. For AB=1110 the moved triple
is the last three bits, producing BA=1011. These exhaust all triples.
Every adjacent A/B or A/C exchange produces one such triple; B/C order and
trailing d never change. No endpoint, multiplicity, phase, or diagonal term
is omitted. Each label block is therefore exactly

    H_ell = -(1/4) sum_(r=1)^(ell-1) (X_r X_(r+1)+Y_r Y_(r+1))

on its weight-m subspace. Open-chain Jordan-Wigner has no wraparound sign.
The one-body matrix has neighboring entries -1/2 and eigenvectors
S_(rk)=sqrt(2/(ell+1))*sin(pi*r*k/(ell+1)), with eigenvalues
lambda_k=-cos(pi*k/(ell+1)). Empty/full blocks are included and have zero
energy; in the full block the sum of these eigenvalues vanishes.

## 2. Uniform clean quantum composition

Compile a reversible classical encoder into padded registers for q and the
label. Computing the encoder and its inverse pays clean conversion: compute
the code, uncompute the old physical word using its inverse, and retain all
label bits. Reversible polynomial-time evaluation uses polynomial gates and
workspace. The decoder is the inverse total unitary, with arbitrary reversible
behavior outside the valid code subspace. Never measure or discard labels.

Only ell in 0,...,N+1 controls the Gaussian transform; there are polynomially
many lengths even though there are exponentially many labels. For each length,
compile the second-quantized sine transform Gamma(S_ell), acting on the first
ell occupation qubits with padding untouched. Use its genuine Fock-space
lift with vacuum phase fixed. Nonadjacent mode rotations can be moved with
fermionic SWAPs, including their |11> sign; ordinary SWAPs would be wrong.
A polynomial Givens/Householder decomposition suffices, so no efficient Bethe
root solver, spectral-gap promise, or exponentially large dense matrix is used.
Working with the ell-by-ell one-body matrix is polynomial. Stable elimination
can choose a largest pivot, avoiding a hidden small-denominator clock.

In the mode basis, apply diag(1, exp(+i*t*cos(pi*k/(ell+1)))) for each k,
then inverse transform and decode. An uncorrected Rz gate differs by a
length-dependent global phase and is NOT interchangeable in a superposition
of sectors. The honest phase gate (or its corrected controlled synthesis) is
required. All circuit controls and their uncomputation are charged.

For 0<epsilon<1 and binary rational t, choose energy error at most
 epsilon/[16*(N+1)*max(1,|t|)] and transform/synthesis error with total norm
budget epsilon/4 at each transform and epsilon/4 for the phase stage.
Arithmetic precision O(log(N+1)+log(1+|t|)+log(1/epsilon)), plus the input
bit length of t, suffices. Multiply and reduce phases at that precision;
never iterate |t| times. Compile every gate to its share of the error budget.
A deliberately loose bound is polynomial in N, bitlength(t), log(1/epsilon)
for BOTH classical compilation and quantum gates/workspace. Enumerating all
lengths and O(ell^2) one-body rotations, including routing, remains polynomial.
No sharp gate exponent or practical-cost claim is needed.

Ideal encoding/decoding resets the ancillary registers. With approximated
universal gates, the precise guarantee is operator-norm error <=epsilon on
the input-with-clean-ancillas isometry, including all input/reference states;
final ancillary leakage is O(epsilon), not literally zero. The induced channel
is within O(epsilon) in diamond norm. Rescale the error target for a prescribed
channel tolerance. No energy-gap or measurement-success assumption enters.

## 3. Strong classical match and its scope

For a computational-basis physical input, encoding gives one known label and
one occupation set. Free evolution preserves a Slater determinant; the one-body
evolution S diag(exp(-it*lambda)) S^T is computable to exponential precision
in polynomial(N, bitlength(t), precision) time. Determinant amplitudes and
fermionic sampling are classical polynomial algorithms. Decode every sampled
occupation string. Amplitudes at arbitrary physical strings are obtained by
encoding, rejecting a different label, and evaluating the corresponding minor.
The same argument applies to a specified sine-mode eigenstate in one label.

For a fully algebraic precision construction, keep the sine matrix exact in
a cyclotomic field of degree O(N) (and at most one normalization square root).
Approximate each time phase by an exact rational point on the unit circle,
using one of finitely many bounded stereographic charts. The resulting
one-body matrix is exactly unitary over a polynomial-degree number field;
its entries and all minors have polynomial bit height. Choose approximation
error O(epsilon/[B(N+1)]) for the classical observable task. The many-body
Slater error is at most m times the one-body error, so observable bias is
controlled. Exact algebraic zero tests and polynomial precision now suffice;
no zero test for a transcendental time-evolved determinant is assumed.

These are computationally tractable states in the sense of Van den Nest,
0911.1624 Definition1 and Theorem3: efficient basis sampling and amplitudes
computed to exponentially fine additive accuracy. Hence efficiently computable
row-AND-column-sparse bounded observables admit classical additive estimation.
All Pauli strings, independent of spatial length, and polynomial Pauli sums
with charged coefficient/norm bound are covered. Precision is polynomial in
1/epsilon and log(1/eta), not polynomial in log(1/epsilon) for this sampling task.
For exact samples a useful identity is

    L(x)=sum_y O_xy psi_y/psi_x,
    E L = <psi|O|psi>,  E |L|^2 <= ||O||^2.

The identity alone does not authorize unstable exact division. Source
Theorem3 uses bounded importance estimators and permits exponential-precision
amplitudes (Definition1 discussion); equivalently one may clip the ratio and
truncate exponentially small total-mass coordinates at polynomial bit precision.
For a Pauli involution x->f(x), sampling the equal mixture of |psi_x|^2 and
|psi_f(x)|^2 allows estimator 2*conj(psi_x)*P_(x,f(x))*psi_f(x) divided by their
probability sum, whose magnitude is <=1. Coordinates below a threshold of
order epsilon^2/2^(N+2) have controlled total mass; this only needs O(N+log1/epsilon)
bits, with additional polynomial precision for the orbital arithmetic.

Ruiz et al.2411.15132 Eq(3.6)/(3.30) supplies a separate known classical match
for its specified folded eigenbasis states: U_D is a reversible classical
permutation applied to a Slater state, with fixed final ancillas. That basis
need not coincide with the basis of the bond encoding in a degenerate energy
space. Do not assert that EVERY vector in a degenerate eigenspace is Slater-
permuted. The source also discusses selected fragment superpositions; it is not limited
to preparing one isolated fragment. This does not supply arbitrary-input
reversible label extraction. The paper's generic XXZ correlator difficulty also
does not establish difficulty for these folded states.

This falsifies a proposed additive-correlator/sampling advantage on these
specified inputs. It does not match arbitrary unknown quantum input, prove
hardness for succinct superposed inputs, cover generic finite-anisotropy XXZ,
periodic boundaries, or exponentially small relative-error readout. No classical
separation follows from the arbitrary-input unitary theorem.

## 4. Closed evidence and next decision

Two independent CLOSED reviews were read completely by the parent:
audits/reviews/2026-11-07-folded-chain-core.md and
audits/reviews/2026-11-07-folded-chain-source.md. The all-N mathematical proof,
resource ledger and source scope establish the WRITTEN construction; neither
agent acceptance nor finite controls constitute its proof.
Exact Sage control is CLOSED, one run: N=2..8, independent Pauli Hamiltonian
versus path adjacency, all states/boundaries/jammed sectors and exact binomial
block sizes. N=8 checks 1024 states, 286 blocks, 1792 directed transitions
and 180 jammed states. A BC-labeled N=6 two-particle Slater eigenstate passes
H psi=E psi; a long Z-string determinant expectation equals dense evaluation.
Parent read control.py/result.json; finite evidence can only falsify.

Claude Fable/high completed the isolated all-N word-bijection audit,
estimate USD0.872230. Its core proof was checked; informal examples and a
basis-identification aside are not needed or used as proof. Opus/high exhausted
16384 output tokens with no final report, estimate USD0.351284; no findings
or retry. Total estimate USD1.223514. Both calls terminal. Two earlier local
plain-text validation rejections made no API calls. Prior partial timeout
billing remains UNKNOWN. Cumulative nonpartial estimate USD50.664820 over
66 records, 34 completed reports; this is not provider balance.

Four used primary sources and two unused selection leads (f_basis, adiabatic)
are retained as six PDF/text snapshots in audits/sources/bethe_transform_selection/.
The exact token alphabet and bond transformation have prior literature;
closed source review distinguishes the stochastic dimer diagonal/Heisenberg model
from the pure-hopping quantum Hamiltonian. No novelty or priority claim.

Actual source normalization discrepancy: folded2411.15132 Eq(3.1) prints the
native -1/8 Pauli Hamiltonian, but Eq(3.16) prints E=-2 sum cos(p_a).
For the stated Pauli convention the direct matrix element is -1/2 and the
one-body energy is -cos(p). Parent checked both passages; source reviewer
also inspected the PDF equation visually. The proof and control use the
explicit native Hamiltonian throughout, not the inconsistent energy formula.
Eigenvector permutations are unaffected by this overall normalization issue.

Prior art is explicit: dimers cond-mat/9703059 lines535-560 gives A=11,
B=10,C=0 and conserved B/C order, while fixing the last bit to0 to avoid a
lone terminal1. The quantum bond/MM mapping in2105.02252 SectionsVI--VII
uses the same bulk encoding and explicitly leaves the finite-chain terminal
bit problem open at lines1030-1037. Our all-sector D bookkeeping must be
proved directly; a missing case in those sources is not evidence of novelty.

Do not extend to periodic boundaries, nearby integrable deformations or a
quantum backend by inertia. After the written contract and classical match are
settled, independently choose the next external-value question. A future
classical/quantum comparison must specify an actual succinct initial-state and
observable family outside the matched Slater/permutation inputs.
