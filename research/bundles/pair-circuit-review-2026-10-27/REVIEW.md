# Independent Signed-Pair Circuit Audit

Date: 2026-10-27. Scope: mathematical correctness, uniform resource bounds,
coherent inversion, precision, and the subsequently proposed sampling bound.
This is a bounded independent review, not a second implementation or test run.
Novelty is outside this review and remains for the separate literature audit.

## Verdict And Required Qualifications

**No fatal flaw found in the stated local construction.** For every integer
q>=2 it implements the signed-pair isometry on the valid zero-sum subspace,
with no measurement or postselection. Its explicit unitary extension and
inverse require no Gram inverse or alphabet-sized table. The O(log(q)^3)
arbitrary-rotation gate upper bound, O(log(q)) space bound, and polynomial
dependence on log(1/epsilon) after finite-set approximation are justified.
The newly supplied direct phi_0 preparation is also correct.

The following qualifications are substantive, not counterexamples to that
properly scoped verdict:

1. **Local efficiency is not a success guarantee.** Polynomial per-trial bit
   complexity does not remove the verified-witness repetition factor. Use a
   proved raw verified-success bound s0=p0^2/L, not merely decoder acceptance
   p0. The current parent RESULT.md makes this distinction correctly.
2. **Clean forward flags do not imply clean inverse workspace after a
   projection.** An explicit sorted-pair inverse has nonblank second-register
   probability 1-2/q. Retain every register through the actual inverse.
3. **All integers applies to the local map, not automatically to field
   elimination.** The parent's current complete resource statement is for a
   stated prime p. Extension fields need an explicit representation and the
   trace-character Fourier transform. General composite-modulus rings need
   a separate decoding argument.
4. **The ledger is an upper-bound proof, not a compiler.** The factor
   100*(controls+1) is defensible with extra clean AND workspace. In the full
   plan the maximum control count is at most max(n,3), not always n: q=2
   has a two-control comparator gate; q=3,4 have three-control gates.
   This does not invalidate resources(), which counts actual controls.
5. **The precision guarantee is a conditional contract.** Its supplied
   success_lower must bound the intended raw success event; all other
   operations must meet the reserved coherent/channel error budget. The
   helper does not certify that bound or arbitrary requested output accuracy.

No source repair or further gate-polish work is required for the mathematical
verdict. Implementation assurance remains distinct from this proof review.

## Exact Algebra

Write H_q=span{|0>,...,|q-1>} inside n=ceil(log2(q)) qubits, and
u=q^(-1/2) sum_a |a>. All ancillas initially below are zero.

### Fourier Convention And Input Promise

For a character-table Fourier transform of a finite abelian group of order q,
with identity labeled zero, F^dagger u=|0> and F^dagger|0>=u. Consequently

    |nonzero> = (sqrt(q)*u-|0>)/sqrt(q-1),
    F^dagger|nonzero> = sqrt(q/(q-1))|0>-u/sqrt(q-1).

Translation by c produces the proposed phi_c. Here |nonzero> means the
normalized uniform superposition, not an arbitrary nonzero basis state.
This works for the usual cyclic and finite-field character conventions.
Over F_(p^r), translation means field addition by c, not powers of a single
cyclic integer increment. Arbitrary Fourier basis rephasings require a
corresponding change to the source convention.

Direct calculation gives <u|phi_c>=0, norm(phi_c)=1, and
<phi_d|phi_c>=-1/(q-1) for c!=d. These are complex quantum amplitudes:
characteristic two does not turn their minus signs into plus signs.

### Register-Wide Fractional SWAP

Let S swap the two entire binary registers, and Pi_+=(I+S)/2,
Pi_-=(I-S)/2. With the phase bit written first, the spectral circuit is

    Q = H controlled-S H = I_bit tensor Pi_+ + X_bit tensor Pi_-.

It is a self-adjoint unitary. Applying Q, diag(1,i), Q gives

    |0> tensor psi -> |0> tensor (Pi_+ + i Pi_-)psi.

Thus the phase bit is clean for EVERY two-register input, including padding
and entanglement with a reference. Also

    Pi_+ + i Pi_- = exp(i*pi/4)(I-i*S)/sqrt(2).

The n controlled bit swaps sharing one control implement controlled-S.
Applying an independent fractional SWAP to each bit pair is different:
two bit-pair antisymmetric factors acquire i^2=-1, while their register-wide
SWAP eigenvalue is +1 and the required R phase is +1. Other symmetric
vectors get +1 under both, so the discrepancy is not a global phase.

### First-Register Phase And Sorting

For any unitary A_q with A_q|0>=u, the complete conjugation

    A_q [I+(-i-1)|0><0|] A_q^dagger

is exactly P=I+(-i-1)|u><u| on the ENTIRE padded space. For v perpendicular u,

    (P tensor I)R|v,u>
      = exp(i*pi/4)(|v,u>-|u,v>)/sqrt(2).

Both the register choice and the -i phase matter. Define the clean comparator
C by XORing [a>b] into orientation, then apply orientation-controlled SWAP.
For a<b, this sends

    (|a,b>-|b,a>)|0>/sqrt(2) -> |a,b>|->.

Time-ordered H then X maps |-> to |0>. Therefore the complete local map is

    v -> exp(i*pi/4) Wv,
    Wv = sum_(a<b) (v_a-v_b)/sqrt(q) |a,b>,   v in H_q, <u|v>=0.

The identity

    sum_(a<b)|v_a-v_b|^2 = q*sum_a|v_a|^2 - |sum_a v_a|^2

proves isometry on the entire promised subspace, not just ensemble members.
Substituting phi_c gives precisely +1/sqrt(q-1) for c<b and its negative
for c>b, with the common phase exp(i*pi/4). A fixed m-coordinate application
has the common phase exp(i*m*pi/4). If one later controls whether to execute
the map, this phase becomes relative and must be retained or compensated.

Each comparator is a reversible XOR oracle, its work cleared BEFORE sorting.
Uncomputing comparison history against already swapped operands would not
be justified. The inspected comparator uses the correct ordering.

## Global Extension, Padding, And Inverse Counterexamples

Every gate is a unitary on the binary space, so the circuit defines a global
unitary regardless of input promise. The sorter is not a many-to-one
classical sorting map: orientation information is coherently retained or
transformed, not erased on arbitrary inputs.

For first-register input u, before sorting the state is -i|u,u>. Its final
state, suppressing other clean flags, is

    -i [ sqrt(2)/q sum_(a<b)|a,b>|1>
         + 1/(q*sqrt(2)) sum_a |a,a>(|0>+|1>) ].

Thus Pr(orientation=1)=1-1/(2q), not zero. More generally, for normalized
psi=alpha*u+v in H_q with v perpendicular u, this probability is
|alpha|^2*(1-1/(2q)); the zero-orientation component from u is diagonal and
cannot interfere with Wv. This is an exact counterexample to universal
sorting-flag cleanup, not to the promised construction.

For a distinct sorted pair |a,b> with zero orientation, reverse sorting gives
the normalized antisymmetric pair. Its projection onto the subspace
{(|v,u>-|u,v>)/sqrt(2): v perpendicular u} has squared norm 2/q, since

    W^dagger|a,b> = (|a>-|b>)/sqrt(q).

Under the complete inverse, that component alone returns the second register
to |0>. The orthogonal antisymmetric component lies in wedge^2(u-perp), and
the inverse of (P tensor I)R preserves it up to phase; A_q^dagger maps its
second factor into |0>-perp. Hence the second register is nonblank with
probability 1-2/q (1/3 already at q=3). Projection onto decoder acceptance
can leave the original forward image, so forward round-trip checks cannot
justify resetting this work. The prior USD resolution remains applicable.

On valid promised inputs, complete R and P preserve H_q tensor H_q and
sorting only permutes valid labels; the ideal output has no diagonal or
padded-label amplitude. Individual gates inside A_q^dagger and A_q may
temporarily leave H_q. That is harmless when the whole conjugation is kept.
Nonblank inverse work can also contain padded encodings; it must be retained.
All later arithmetic must be total on invalid encodings, with their behavior
defined even though the ideal forward transcript does not encounter them.

## Interval Preparation And Resource Ledger

At a node with j remaining bits and t valid leaves, let h=2^(j-1). If t<=h,
only the zero high-bit branch is used. Otherwise the high-bit probabilities
are h/t and (t-h)/t. The first branch is a full subtree of Hadamards; only
the second needs recursion. There is at most one partial node per depth.
This proves the interval preparation without enumerating q leaves.

If f(n) bounds its number of controlled macros, f(n)<=n+f(n-1), hence
f(n)<=n(n+1)/2. There are at most n nontrivial rotations. Prefix tests use
O(n) controls, not O(q) gates hidden in a lookup. Exact rational probabilities
have O(n)-bit descriptions. Computing angles to absolute error tau takes
polynomial bit work in n+log(1/tau); small nonzero branch probabilities may
require O(n) extra working bits, not polynomially many bits in q.

For the inspected plan, the comparator has 5n-4 macros, the fractional SWAP
has 2n+5, and sorting adds n swaps and two single-qubit gates. Including
the three interval preparations and the all-zero phase gives

    macro_count <= 3*f(n)+8*n+4 = O(n^2).

For a macro with k>=1 controls, flipping negative controls costs at most 2k
X gates. A clean conjunction chain and its inverse use 2(k-1) Toffolis and
at most k-1 extra clean bits. A controlled one-qubit payload has constant
cost; controlled SWAP is two CNOTs plus a Toffoli. Using at most sixteen
basic gates for a Toffoli and six for a controlled one-qubit gate yields a
bound no worse than 2k+32(k-1)+18, comfortably below 100(k+1).
Uncontrolled macros also fit the stated bound. These exact elementary
decomposition facts are in [Barenco et al., Corollaries 5.3 and 6.2](https://arxiv.org/pdf/quant-ph/9503016).
No unchecked relative-phase Toffoli substitution is needed.

The plan has 3n+1 structural qubits, PLUS the separately reported reusable
lowering workspace. The maximum control count is <=max(n,3), so both the
total space and the extra space are O(n). The scalar ledger counts logical
arbitrary one/two-qubit operations; it is not a physical gate count, depth
bound, or emitted finite-set circuit. Its polynomial nature does not depend
on large symbolic examples or the exponentially sized statevector simulator.

### Direct phi_0 Preparation

After the proposed flag rotation and controlled nonzero-interval preparation,
the joint state is

    sqrt((q-1)/q)|0>_flag|0>_data
      - 1/sqrt(q*(q-1)) sum_(b=1)^(q-1)|1>_flag|b>_data.

XOR [data!=0] clears the flag and leaves exactly phi_0. Controlled increment
does not wrap on its occupied [0,q-2] input range. The inspected high-to-low
controlled increment preserves the required lower-bit carry predicates.
The flag-clearing XOR is X followed by X controlled on all data bits zero.
This preparation is also uniform and polynomial in n; its cost belongs in
source preparation, not implicitly in resources(pair_circuit(q)).

## Precision And Complete-Decoder Boundary

For J elementary ideal gates and approximations of operator errors delta_j,
the product error is at most sum_j delta_j. This bound holds with arbitrary
reference entanglement. Reverse the actual synthesized gate list to obtain
its actual adjoint; do not discard work or substitute a separately defined
inverse valid only on the original forward image.

If G bounds one local map's lowered elementary count, m forward maps and
their inverses use at most 2mG calls. Setting each error <=s0/(8mG) allocates
s0/4 to these calls. Another s0/4 uniform raw-channel/measurement error for
EVERYTHING else ensures compiled raw verified success >=s0/2. This is the
default precision_budget contract, provided its success_lower is s0, not p0.
Postselection need not be charged twice when comparing the whole raw outcome
law including failure. Statements about normalized accepted states require
their own conditioning bound.

For arbitrary total target accuracy epsilon, allocate errors against that
target as well as any success margin. The required synthesis precision
includes log(mG)+log(1/epsilon)+log(1/s0), when both are required. Standard
fixed-dimensional synthesis has polynomial log(1/delta) cost, so this does
not restore a polynomial-q factor. See [Dawson and Nielsen, Sections 2-4](https://arxiv.org/pdf/quant-ph/0505030).
This is an existence and uniform compilation argument, not verification of
a Clifford+T compiler or a physical-noise model.

Per-label fidelity tests are insufficient for this error contract: on N
orthogonal basis states, I-2|uniform><uniform| differs from I by only
2/sqrt(N) on each basis state, but by norm 2 on their uniform superposition.

For explicit finite-field input, Schur-square basis construction and
unique-solution-or-failure Gaussian elimination require polynomially many
field operations. Recording history, copying the result, and reversing
the Boolean arithmetic gives a polynomial reversible implementation. Guard
division by zero and retain pivot/history records until their inverse.
The parent's prime-field operation counts and grade-school polynomial bit
upper bound are consistent with this argument. They are not a compiled
general eliminator. No enumeration of codewords or of q labels is needed.

An arbitrary-order cyclic QFT admits a uniform approximation polynomial in
log(q)+log(1/epsilon), with a state-norm guarantee including ancillas, not
only a basis-output sampling guarantee; see [Cleve and Watrous, definition
following Theorem 1 and Section 7.1](https://arxiv.org/pdf/quant-ph/0006004).
For F_(p^r), use r transforms over Z_p and the invertible linear coordinate
change implementing the field trace pairing. Require the field polynomial,
basis, and arithmetic representation explicitly; binary encodings alone do
not turn the cyclic F_q into the field transform.

Accordingly the local polynomial-q synthesis obstruction is removed for
the full-support decoder. A coherent decoder call and a raw reduction trial
have polynomial(m,log(q),log(1/epsilon)) bit cost under these explicit-access
assumptions. Repeated verified output additionally costs O(L/p0^2) ideal
trials, or O(1/(p0^2/L-delta)) with raw TV error delta below the margin.

Two useful counterexamples to broader interpretations: there is no field
F_6, and elimination over Z_6 cannot invert its nonzero element 2; at q=2,
phi_1=-phi_0, so all tensor codeword states are the same ray up to sign.
No nontrivial binary code can be unambiguously distinguished by this ensemble.
An efficient local unitary therefore does not itself supply useful success.

## Qualified Sampling Consequence

The user's proposed consequence is valid, with a nonzero-success condition.
Assume the ideal post-Fourier joint target is the UNIFORM normalized fiber
state tensor blank work. Let its squared overlap with the accepted joint
state be F=p_bar/lambda, and let v be that state's valid-data probability.
The validity projector contains the target, so v>=F. Conditioning on validity
gives squared target overlap F/v. Monotonicity under measurement then gives

    TV(ideal verified output, uniform fiber)
      <= sqrt(1-F/v) <= sqrt(1-p0/L).

This does not require blank actual work; joint-state comparison is precisely
what makes the inequality valid. It also does not apply to a nonuniform
source merely by calling its target a fiber state.

Let P and Q be ideal and compiled RAW outcome laws, including failure, with
TV(P,Q)<=delta. Write A for verified outputs, z=P(A)>=s0=p0^2/L, and w=Q(A).
If delta<s0 then w>0. On A,

    TV(P(.|A), Q(.|A))
      <= ( ||P_A-Q_A||_1 + |z-w| )/(2*z)
      <= delta/z <= delta/s0.

The second inequality uses ||P_(A^c)-Q_(A^c)||_1>=|z-w|. Thus the suggested
denominator z is valid; it need not be weakened to z-delta. Combining gives

    TV(compiled verified output, uniform fiber)
      <= sqrt(1-p0/L) + delta/s0.

Independent identical restarts have this same law conditioned on returning
a witness. A cap T>=ceil(log(1/eta)/(s0-delta)) makes abort probability <=eta.
Add eta when comparing the UNCONDITIONAL capped output, including an abort
symbol, with the uniform fiber law. No eta term is needed after conditioning
on a witness actually being returned.

With p0=1-E and L<=1+E, the ideal term is at most sqrt(2E/(1+E)). Exponentially
small E, suitably small delta/s0, and small eta therefore give negligible
sampling error for such an input family. This is not exact uniform sampling,
nor a guarantee of arbitrarily small error at a fixed input by increasing
gate precision alone: the displayed ideal-error bound remains. No novelty
or classical advantage conclusion follows.

## Evidence And Scope

Read the current prior independent USD REVIEW.md and RESOLUTION.md, the
parent pair_circuit.py and test_pair_circuit.py, and the subsequently supplied
RESULT.md. The parent source locations most relevant to this review are
[local construction](/Users/jaspersands/Developer/qsearch-research-work/binary-pair-circuit-2026-10-27/pair_circuit.py:106),
[resources()](/Users/jaspersands/Developer/qsearch-research-work/binary-pair-circuit-2026-10-27/pair_circuit.py:214),
and [precision_budget()](/Users/jaspersands/Developer/qsearch-research-work/binary-pair-circuit-2026-10-27/pair_circuit.py:239)
in the inspected snapshot. The source inspection agrees with the algebra above.

The parent reports 578 combined passing tests, including 79 new controls and
nine accepted-transfer checks with the actual inverse. I did not rerun or
independently certify those results. At the earlier inspected test snapshot,
signed-pair labels were checked at q=2,3,4,5,7,8,9,13,17, not every integer
from 2 through 17. Finite tests support implementation checking, not the
all-q proof. Dirty-work observations agree with the exact counterexample.

Only this new review file was written. No implementation, test, main-repo,
Git, UI, migration, or memory changes were made. No independent subagent
facility was available; this is one independent audit, not reviewer consensus.
