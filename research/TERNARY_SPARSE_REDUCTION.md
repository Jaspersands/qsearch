# Dense-To-Sparse Transfer: A Checked Failure And Its Exact Scope

2026-10-20. LOCAL DERIVATION / INDEPENDENT REVIEW PENDING. No new algorithm
or general sparsification lower bound. This audits one concrete attempt to
connect the sparse sampling target to a harder dense-code problem.

Producer: `python theorems/ternary_sparse_reduction.py --write`.
Artifact: `research/reductions/ternary_sparse_reduction.json`.
Tests: `tests/test_ternary_sparse_reduction.py`.

Constructive follow-up: TERNARY_PAIR_CONDITIONING.md avoids decoding the
local gadget subcode by preparing its known conditional source, with an
explicit conditional-syndrome sampler proof. It does not refute the full-word
bound below: it solves a different residual decoding task. Eliminating the
addition constraints recovers the original dense problem, so this does not
restore inheritance of the random-LDPC guarantee.

## Why This Question Matters

The preceding classical pass found low-memory samplers on both saved inputs
and showed that generic dense-code hardness cannot be imported into the
native LDGM distribution. A natural repair would reduce dense affine
exclusions to three-variable exclusions, then invoke the sparse quantum
decoder. That repair must preserve MORE than satisfiability: uniform output
law, the decoding code/channel, and the random-instance assumptions matter.

The paired-exclusion addition gadget preserves solutions and their relative
weights exactly. Nevertheless it creates an independent short-word subcode
that defeats the vanishing whole-word decoding premise even for an optimal
collective measurement. The source offsets also cease to be independent.
This is a rejected transfer of the current guarantee, not a rejection of
the original sparse ensemble or every alternative quantum sampler.

## Exact Classical Reduction

Start with arbitrary explicit dense constraints over F3:

    J_f + sum_i a_(f,i) x_i != 0.

For a form with w>3 nonzero terms, introduce partial-sum variables until the
remaining exclusion has at most three terms. Each addition t=a*x+b*y is
enforced by TWO affine exclusions with the SAME coefficient vector:

    E = t-a*x-b*y,
    E+1 != 0,   E+2 != 0.

Together these are exactly E=0. Every original spin assignment has one
extension satisfying all addition gadgets, including assignments that fail
the original final exclusions. Thus original and expanded solution sets
are in bijection, with no free auxiliary multiplicity or fixed gauge.
Uniform expanded solutions project to uniform original solutions and vice
versa. Unsatisfiable and tautological zero forms remain.

If g=sum_f max(w_f-3,0), the output has V+g spins and N+2g constraints. The
explicit construction is polynomial. Dense storage and the reference's
4096-spin cap are implementation limits, not a complexity theorem. The
transform does not produce the random regular (3,6) socket ensemble.

## The New Code Directions

Use the existing orientation H: one column per constraint, one row per spin.
The two copies of E give equal nonzero columns p,q in H'. Therefore

    k_g = e_p-e_q lies in C' = ker H'.

Distinct gadgets use disjoint coordinate pairs, so these vectors span a
g-dimensional subcode K. If g>0, minimum distance is AT MOST two. This is not
merely a short cycle that a better local decoder could fix.

There is also an explicit constructive quotient. For original constraint f,
its final sparse form obeys

    final_f = original_f + sum_(gadgets j in chain f) E_j.

The E_j are independent modulo the original-spin forms because their fresh
auxiliary coefficients are triangular. A sparse codeword has final
coordinates d_f in C=ker H and satisfies, for every gadget owned by f,

    d_p+d_q = -d_f.

Conversely choose any d in C and arbitrary q_j in F3; set d_p=q_j and
d_q=-d_f-q_j. This gives every sparse codeword exactly once. In particular

    C'/K is isomorphic to C,
    rank(H')=rank(H)+g,   dim(C')=dim(C)+g.

The implementation provides both directions of this map, checked against
an independent complete kernel census. Eliminating the gadget directions
returns the ORIGINAL dense decoding code; it does not supply a new certified
sparse decoder for it. This identifies a possible quotient-decoding question
without pretending that full-word decoding is necessary for every sampler.

## Any-Measurement Word-Success Bound

Keep precisely the native signed-trine output, once per coordinate:

    psi_c = (omega^c |1> + omega^(2c) |2>)/sqrt(2).

Reveal to the receiver the coset of K containing the uniformly random codeword
in C'. Such genie information can only improve whole-word success. It permits
removal of the known coset representative by local phase unitaries. The
remaining unknown symbols are g independent uniform trits, one per disjoint
pair, encoded as

    c -> psi_c tensor psi_(-c).

This pair has Gram entry1/4 between distinct symbols. Compressing equal
frequency-difference sectors gives spectrum nu=(1/2,1/4,1/4). Its optimal
three-way success is

    s = (sum_j sqrt(nu_j))^2 / 3 = (3+2 sqrt(2))/6 < 1.

The square-root measurement's optimality for geometrically uniform pure
ensembles is known [Eldar--Forney](https://arxiv.org/abs/quant-ph/0005132).
We additionally give a direct certificate here, not just a numerical PGM
guess. In the compressed basis, let S=sum_j sqrt(nu_j) and

    Y=(S/3) diag(sqrt(nu_j)).

Weighted Cauchy-Schwarz gives Y >= |psi_c><psi_c|/3 for every c. Trace(Y)=s.
Fourier-basis measurement attains s, so primal and dual agree. Tensoring both
feasible certificates shows the optimal probability of identifying ALL g
independent symbols is exactly s^g; entangled measurements cannot improve
it. By the genie argument, for ANY receiver on the full original code,

    P_word_success <= s^g,    delta_word >= 1-s^g.

The bound does not assume BPQM, local readout, an efficient algorithm, or a
particular graph depth. Actual physical two-qutrit Gram checks, the explicit
dual, and small complete full-code Gram controls independently replay it.
Scaling certificates use outward rational sqrt/power enclosures, not the
floating eigenvalues. Extra copies or altered local spectra are a different
resource/source contract and need a new reduction analysis.

## Offset Distribution Also Changes

Each ordered gadget pair has J_q-J_p=1. For a fixed matrix and g disjoint
pairs, independent uniform offsets satisfy this invariant with probability
3^-g. A distribution guaranteed to satisfy it is consequently at TV distance
at least1-3^-g from IID uniform offsets. Random auxiliary translations do not
change this difference. Randomly swapping the pair changes the invariant to
J_p!=J_q, still of IID probability(2/3)^g.

This is directly relevant to the earlier average-offset sampler argument:
the nontrivial character corresponding to e_p-e_q no longer averages to
zero. Its expectation has modulus one on the ordered gadget distribution.
The unconditional Parseval identity cannot just be reused on these correlated
offsets. Worst-case or explicitly correlated-source sampling would require
a separate argument.

## Same-Input Controls, Not Manufactured Hard Instances

To avoid inventing new small oracle problems, the live producer uses the
EXACT saved16/32-spin inputs. A public invertible spin-basis change x=Tz makes
their forms dense while preserving every solution and the original decoding
kernel. These controls remain the same already-classically-solved problems;
they are not evidence of dense random-code hardness.

The producer then executes the gadget construction. Previously recorded native
samples are transformed through T^-1 and the actual auxiliary lift, and
checked against every new constraint. No solution pool is reconstructed.

| Original spins | Addition gadgets | Expanded spins / constraints | Any-receiver word success upper |
|---|---|---|---|
|16|256|272 /544|0.000594882|
|32|1201|1233 /2466|7.372e-16|

The nominal constraint/spin ratio happens to stay two, but regularity, minimum
distance and the source law do not survive. Rate alone does not license the
[known random-LDPC block theorem](https://arxiv.org/html/2609.05857v1#S6).
These are analytic bounds applied to recorded exact matrices, NOT executions
of a large quantum receiver. Original samples and all code-pair witnesses
are retained or reproducibly source-bound in the artifact.

## Attempt To Prove This Conclusion Wrong

- A better collective receiver cannot evade the stated full-word bound:
  the argument already gives it the coset and allows arbitrary joint POVMs.
- Dropping nuisance gadget labels is a real possible escape. The explicit
  quotient recovers C, so the present full-word premise no longer applies;
  this does not prove that no quotient sampler exists. It must explain the
  remaining dense-code operations and the correlated-offset source.
- A different sparsification may avoid these disjoint duplicate columns.
  This calculation says NOTHING universal about every such gadget family.
- Failure of decoding need not imply bad sampling. Even a single paired
  exclusion can have a unique, trivially sampled classical solution despite
  positive optimal decoding error. That countercontrol is tested explicitly.
- The artifact does not establish hardness of either source, a classical
  lower bound, novelty of the measurement theorem, or an ECDSA application.

## Revised Research Decision

Do not pursue paired-exclusion sparsification as a free bridge from hard dense
instances to the existing BPQM guarantee. Preserve the useful exact reduction,
but mark its decoder/source guarantees as non-transferring. No central
negative or proof promotion occurs without independent review.

The remaining high-value questions are now narrower: useful finite-block
decoding on the ORIGINAL source, genuinely source-aware quotient sampling,
or a different structured family with both constructive decoding and a
credible classical comparison. More threshold tables, tiny quantum examples,
or lowering the already-known compiler without addressing these questions
would not improve the scientific case. Repetitive hashed-SAT campaigns and
routine exposure remain Gemini tasks, as specified in the mechanical handoff.
