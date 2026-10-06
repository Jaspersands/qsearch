# Native Cubic Tensors As Weighted Schur Products

LOCAL DERIVATION / REVIEW PENDING. Public mathematical representation and
admission checks, not a decoder, new efficient sieve or accepted candidate.
Fixed-level cubic cancellation alone is a low-ceiling result.

GROWING-DEPTH CORRECTION: see `TERNARY_PHASE_DEPTH.md`. A native subspace can
pass this exact cubic gate at L3 yet have a nonzero fifth derivative at L5.
The whole phase has nonclassical additive degree that grows with depth; forcing
constant degree can erase high secret digits. The level3 gate is not a full
depth-independent decoder admission rule.

## Exact Native Structure

Use the actual level3 packet in `TERNARY_CARRY_PACKETS.md`. Let A be its n-by-m
low-label matrix, V its m-by-h kernel chart over F3, and j=x+Vz the physical
native digits. The public divided frequencies Q_l(z) define the supplied state
with phase sum_l s_l*Q_l(z). The unknown weighted phase is NOT an oracle.

For arbitrary u,v,w in F3^h, exact native finite differences give

```text
T_l(u,v,w) = Delta_u Delta_v Delta_w Q_l(z)
           = -sum_i A_(l,i)*(Vu)_i*(Vv)_i*(Vw)_i mod3.
```

It is independent of z, syndrome and higher native label digits. This is a
factored symmetric trilinear tensor, not an arbitrary cubic coefficient table.
Its storage is O(n*m+m*h); evaluation is polynomial. Expanded entries cost
O(n*m*h^3), not3^h. The source map remains the original native map.

Proof: native scalar C_i(j) has values0,a-2b,-a-b mod9, hence
C_i(j) mod3=A_i*j. With S the cyclic shift, Delta_1^3=3(S-S^2) exactly on
three digits. After dividing by3, its action on C_i is the constant -A_i.
Delta_2=Delta_1*(S+1); each nonzero direction therefore supplies its F3 factor.
Sum over physical coordinates and use the exact native phase division.

The degree-three monomial coefficient for z_i^2*z_j is2*T(e_i,e_i,e_j);
the coefficient for distinct z_i*z_j*z_k isT(e_i,e_j,e_k). Pure cubes reduce
to linear terms on F3. The lower-degree coefficients follow from Q(e_i),
Q(2e_i),Q(e_i+e_j), after subtracting the cubic terms. Complete public
polynomials require2h+binomial(h,2) residual evaluations and polynomial
tensor arithmetic, without constructing a3^h phase table.

The new representation handles an unfiltered n4,m20,h16 source with152 public
residual evaluations rather than43,046,721 table entries. This is not a
secret decoder: those coefficients are the KNOWN component functions, not
the unknown s-weighted coefficients measured from the state.

## Characteristic-Three Falsifier

Every native kernel vector v obeys

```text
T_l(v,v,v) = -sum_i A_(l,i)*(Vv)_i^3 = -(A*Vv)_l =0.
```

Therefore testing only diagonal polarization admits EVERY kernel, including
genuinely cubic packets. Dividing by3! is also invalid. Neither diagonal
isotropy nor a homogeneous cubic evaluation on a single line certifies a
quadratic multivariate state. An unfiltered native control has all diagonal
triples zero but nonzero mixed cubic witnesses.

For a retained physical subspace W inside kerA, correct cubic cancellation is

```text
A*(u star v star w)=0 for EVERY u,v,w in W.
equivalently W^(star3) is contained in kerA.
```

Here star is coordinatewise multiplication and W^(star3) is the linear span
of all triple products. Checking all mixed basis triples suffices. This is
a weighted Schur-product code condition, not the weaker diagonal condition
or an automatic transfer of binary magic-state triorthogonal-code theorems.
For level3 cubic functions it is necessary and sufficient for every affine
restriction along W to have degree at most2.

## A Real Instrument, But An Existing Throughput Bottleneck

Partition m physical coordinates into disjoint blocks of n+1. Each block's
low-label columns have a public nonzero kernel word. These disjoint-support
words span W of dimension floor(m/(n+1)). All mixed Schur triples vanish;
diagonal triples vanish because each word lies in kerA.

Extend the logical retained frame to an invertible public matrix. A known
linear qutrit coordinate permutation measures its complement. ALL initial
kernel syndromes and ALL complement outcomes are retained with their original
mass. Each complete branch has probability3^(-(m-k)), k=dimW. The surviving
native divided phase is quadratic; disjoint physical supports additionally
remove cross-variable terms, giving product qutrit phases.

Independent replay checks two unfiltered n1,m6 native sources:1,458 complete
input words and amplitudes,54 branches, and their full output polynomials.
Input s8 mod9 is used, not merely a low-digit input. The output sees only
s mod3; changing s2 to s8 changes only each measured branch's global phase.
No full-secret recovery or uncharged coherent recombination is supplied.

This construction consumes roughly n+1 input registers per retained output.
It does NOT solve the source-throughput bottleneck or replace growing-depth
complexity with polynomial cost. Intermediate odd-level source acquisition
from the original even-level CCP is still uncharged here. The implementation
is a baseline for subspace-search proposals, not the proposed breakthrough.

## Exact Quadratic Output Source Law

Condition on low A, a LOW-DEFINED retained W and the measured affine branch.
For each component and physical coordinate write native frequencies as

```text
C1_i = a_i+3*b_i mod9
C2_i = 2*C1_i+3*d_i mod9.
```

The high variables b_i,d_i are independent uniform F3 coordinates of the
actual native source, not independently invented phase coefficients. On a
quadratic-admitted affine restriction, b supplies an independent uniform
linear coefficient vector because W has full column rank. The quadratic
coefficients are an affine image of d through the coordinatewise squares and
pairwise products of the physical W basis vectors. Diagonal columns carry
factor2; offdiagonal columns carry factor1. These factors preserve rank.

Let d2=dim(W^(star2)), e=rank of offdiagonal product columns, and k=dimW.
The full quadratic-coefficient support has dimension d2 per secret component.
In the SPECIFIED frame, zero cross terms have probability3^(-n*e) if every
known low-offset target is consistent, otherwise zero. After that filter the
diagonal-label entropy is d2-e trits per component, while linear labels have
k independent trits. IID uniform product phase labels require d2-e=k.
Rank, affine target consistency, probability and entropy are recorded exactly.

The disjoint-block frame has e0,d2=k and gives IID lower-level labels under
this conditional source law. An invertible public rotation of the SAME
two-dimensional block subspace instead has e1,d2=2: cross-term filtering costs
1/3 and leaves only one diagonal-label trit rather than two. Both frames
cancel cubic terms. Exhausting81 actual high-d assignments per frame verifies
the probabilities and correlations; linear-label enumeration verifies its
independent full rank.

This example is deliberately basis-dependent. Undoing the known rotation
restores the disjoint IID frame; it is NOT an impossibility theorem for the
subspace or a receiver. Arbitrary public Clifford changes, high-label-adaptive
selection, and keeping useful entangled quadratic states remain open. Do not
force every receiver into an IID interface. Do not apply the low-defined
source law after selecting W using higher labels without a new conditioning
proof. Physical cross filtering is not executed by this source ledger.

## Stronger Literature Baselines

The old2007 univariate quadratic/cubic paper is not the whole baseline.
[Decker, Ivanyos, Santha and Wocjan, Theorem5](https://arxiv.org/html/1107.2189v2)
reduce multivariate constant-degree HPGP to polynomially many univariate
instances. That reduction uses graph-oracle access; supplied varying packets
do not automatically provide those restricted oracle queries.

[Ivanyos and Santha, Section5](https://arxiv.org/html/1503.09016v2) explicitly
use univariate phase states psi_Y whose coefficients are known linear
combinations of shared unknown parameters. DIFFERENT known matrices Y are
allowed. Thus identical-function copies are NOT a general prerequisite for
polynomial-phase techniques. Native quadratic single-qutrit outputs fit that
algebraic interface; claiming their variation alone blocks all known decoding
would be wrong. A complete decoder must still prove informative coefficient
rank, source availability, costs and any recursion.

The illustrated degree-reduction proof treats p>d after separating constant
p by earlier methods. Its displayed failure bound may be vacuous at p3 and
growing parameter count; one cannot copy that numerical guarantee unchanged.
The paper's diagonal-equation solver does not itself find a large W satisfying
ALL mixed Schur constraints. In F3, the diagonal cubic equations simply reduce
to the original linear kernel equations. Neither result is being refuted.

Both sources give stronger fixed-field baselines, not a decoder over growing
Z_(3^t) phase depth. The previous native L5 fourth-difference falsifier still
blocks a constant classical-cubic transfer. Solve that growing-depth issue
before calling any fixed-L3 optimization high-upside algorithmic progress.

## Next Research Decisions

1. Search for source-adapted overlapping W with substantially better retention
 than disjoint blocks. Use the compact native Schur tensor and certify every
 mixed term. Charge classical construction, all outcome branches and resulting
 coefficient/source correlations. Existence alone is not an algorithm.
2. Determine whether the resulting quadratic coefficients retain enough
 information about all target secret coordinates. Compare with known varying-Y
 phase elimination, not only same-state stabilizer learners.
3. Prove an extension to growing phase depth with a complete secret-digit
 recovery and throughput ledger. Otherwise deprioritize the fixed-level route.
4. Keep implicit full-source modular decoding as a competing higher-upside
 target. No generic impossibility of improved W or alternative decoders has
 been proved by this pass.

22 focused tests pass. They check native mixed differences, nonbasis
directions, syndrome/high-label invariance, sparse versus dense coefficients,
growing-width evaluation, correct restriction admission, all physical outcomes
and top-digit loss, plus high-source entropy and filtering costs. Independent
JS checks270 mixed differences,37 sparse polynomial values and162 high-source
assignments in addition to the1,458 native words/amplitudes.
The final eight-file regression has166 passing tests; counts overlap the
earlier144-test full-source regression. Python compilation, both independent
replays, JS syntax and strict six-artifact JSON validation pass.

```sh
python theorems/ternary_schur_tensor.py
python -m pytest -q tests/test_ternary_schur_tensor.py
node research/certificates/ternary_schur_tensor_crosscheck.js
```

Gemini handles CLI/registry/full-suite wiring. No production validation, human
review, commit or push claimed. No candidate should be accepted from this
representation or its fixed-level disjoint-block baseline.
