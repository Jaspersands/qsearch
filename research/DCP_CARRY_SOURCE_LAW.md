# Carry Extraction: Native Acceptance And The Exact Output Source

Status: LOCAL DERIVATION / REVIEW PENDING. No independent theorem review,
novelty, decoder, quantum speedup, standard-LWE attack or security claim.

## Decision

Conditional product-state identities are insufficient for a sieve proposal.
For fixed directions selected only from low labels and the initial syndrome,
overlapping extraction costs exponentially many native batches. At q=8 the
code now computes the EXACT acceptance and conditional joint label law.
Some accepted product states do have fresh IID labels; others have permanent
relations that survive mixing all complement outcomes. Neither constitutes
a speedup, and nonuniform labels need not be useless for a different decoder.

The new capability is a source-law certificate and falsifier, not another
candidate circuit generator. Read the earlier
[throughput gate](DCP_CARRY_THROUGHPUT_GATE.md) for its operation-class boundary.

## 1. Source And Selection Contract

Use native IID labels A=B+2H+4T over Z_8^(n by m). B, H and T are independent
fair binary matrices. Condition on B and the initial parity-measurement
syndrome. Pick independent physical directions u_1,...,u_d in ker(B), and
the complement-measurement basis, using ONLY that information.

This is a probabilistic lineage assumption. Passing a binary B to the API
does not prove that an external algorithm did not inspect H or T. The
certificate explicitly keeps that lineage unverified. It does not apply
to choosing retained directions after complement outcomes, secret-dependent
choices, or a measurement that changes the phase source.

Complement-Z outcomes are uniform and independent of H,T and the secret:
the parity-packet state has flat computational amplitudes. Let x be the
physical background and epsilon_i=(-1)^x_i. Define

    U=span(u_1,...,u_d),
    E=span(u_i*u_j : i<j),  e=dim(E), r=dim(U intersect E).

Here * is componentwise binary product, not composition of unknown gates.

## 2. Exact q=8 Native Acceptance

Product extraction for EVERY secret first requires

    B_l.u_i=0,
    B_l.(u_i*u_j)=0,
    B_l.(u_i*u_j*u_a)=0,

for every component l and distinct i,j, with arbitrary a. The first is the
parity kernel, the second a quadratic parity check, and the third includes
cubic interactions. Any failure gives zero acceptance in this declared
product-extraction class.

The remaining condition is a LINEAR system on the unconsumed middle bits:

    H_l.(u_i*u_j) = c_lij(x),
    c_lij(x)=(1/2) sum_h epsilon_h B_lh u_ih u_jh mod2. (1)

The numerator is even. A crucial extra obligation: all relations among the
pair-overlap vectors must be respected by their targets. The code tests
augmented rank; pair/triple parity alone is NOT sufficient for consistency.

If consistent, each independent native row H_l satisfies (1) with probability
2^-e. Rows are independent. Therefore

    P_native(accept | B, initial syndrome, x) = 2^(-n*e). (2)

If inconsistent it is zero. This is different from the earlier conditional
ledger's 2^(-rank R), which fixes all labels and averages only quantum
complement outcomes. Both are correct for their DISTINCT probability spaces.
Favorable fixed-high-label examples do not establish native average success.

Consistency does not depend on x: changing x changes c_lij by
`B_l.(x*(u_i*u_j))`, a linear functional of the pair-overlap vector. Hence it
preserves every linear relation. Averaging complement outcomes cannot repair
inconsistency or remove the 2^(-n*e) source penalty.

## 3. Conditional Joint Output Labels

On an accepted branch the output label for direction j is

    a'_lj=(1/2) sum_h epsilon_h A_lh u_jh mod4.

Its lower bit is `c_lj(x)+H_l.u_j`, with c_lj defined like (1).
Conditioning H_l on its values on E leaves exactly d-r free bits in its
restriction to U. The independent top bits T_l contribute
`2*(T_l.u_j)` to a'_lj. Since the directions are independent, all d top
output bits are jointly uniform, independently of the conditioned H_l.

Thus the labels are uniform on an explicitly calculated affine set with

    Shannon entropy = min-entropy = n*(2d-r) bits.     (3)

CONDITIONAL on B, the chosen directions and initial syndrome, they are
jointly IID uniform over Z_4^(n by d) IFF r=0. The implementation
computes the retained/overlap intersection and its affine lower-bit parity
constraints. Uniform marginals alone are not the certificate.

This is a stronger conditional source interface, not a necessary criterion
for every possible UNCONDITIONAL sieve. Mixing different B or bases chosen
from different initial syndromes could change the marginal law and needs a
separate proof. The certificate deliberately leaves that mixture unclassified.
Failure of this certificate cannot be substituted for that missing proof.

For a FIXED B and chosen basis, these constraints persist after mixing x.
For a relation
`sum_j lambda_j u_j = sum_a mu_a e_a`, their target is

    sum_j lambda_j c_lj(x) + sum_a mu_a c_la(x).

Its x-dependent part vanishes because the physical-vector relation is zero.
Consequently the conditional label distribution, not just its entropy, is
the same for every complement background. There is no hidden entropy gain
from averaging successful outcomes.

Positive control: E intersect U=0 can give genuinely fresh product outputs,
but still costs 2^(n*e) batches. Negative fresh-source control: nested
directions u=(1,1,0,0), v=(1,1,1,1) with B=(1,1,1,1) force the first output
label EVEN. There are only eight output pairs, not sixteen. This is not a
claim that the resulting known nonuniform source is computationally hard.

## 4. Parity-Only Triorthogonality Can Miss An Impossibility

Take the 36 points z in F_2^6 satisfying

    z_1z_2+z_3z_4+z_5z_6=0.

Let each physical coordinate have B=1, and let six directions evaluate the
six coordinate functions on those points. All degree-one, pair and triple
overlap weights are even. The three special pair vectors obey

    e_12+e_34+e_56=0,
    weight(e_12)=weight(e_34)=weight(e_56)=6.

Their targets in (1) are all one at x=0. A linear functional H cannot assign
one to all three vectors whose XOR is zero. Acceptance is therefore ZERO
at every background and for every higher-bit assignment. This is a bounded
divisibility counterexample, not a proposed toy problem or algorithm family.
It prevents importing a parity-only triorthogonal code claim without the
actual weighted phase/source constraints.

## 5. Growing Moduli And A Finite-Menu Gate

The cost obstruction is not limited to q=8. For q=2^t>=8, write A=B+2Z,
where Z is uniform modulo q/2. Any NONZERO physical overlap e=u_i*u_j
requires, on a product branch,

    sum_h epsilon_h Z_lh e_h
        = -(1/2) sum_h epsilon_h B_lh e_h mod(q/4).     (4)

An odd B numerator instead makes acceptance impossible. Otherwise (4) is
uniform modulo q/4: a nonzero overlap contains a coefficient +1 or -1.
Independent label rows give

    P_native(accepted overlapping extraction) <= (4/q)^n. (5)

Further higher-carry conditions can only lower it. This is a NECESSARY pair
bound, not a full growing-modulus source classification.

Now allow a selector to inspect ALL public label bits, but choose BEFORE
complement measurement among L subspaces defined using only B and the
initial syndrome. If every option overlaps, its native mean success is at
most (4/q)^n. For conditional success probabilities p_i(A),

    E[p_selected(A)] <= E[max_i p_i(A)]
                     <= sum_i E[p_i(A)] <= L*(4/q)^n. (6)

No simultaneous outcomes or independent counterfactual measurements are
assumed. With T supplied packet attempts, union bound gives at most
`min(1, T*L*(4/q)^n)`. At n=q=128 and L=T=n^2, this is 2^-612.
This is a SOURCE probability bound, not a universal runtime lower bound.
The menu must be defined without reading the higher bits. An algorithm that
synthesizes one subspace AFTER reading them is not an L=1 low-defined menu;
membership is explicitly an unverified external proof obligation.

Disjoint options have e=0 and no rejection, but the prior native m=3n
distance certificate caps their output count at 31 except on its stated
source event. Thus low-label-only postselection and a polynomial literal
menu do not remove the n-sized throughput bottleneck.

Escape boundaries: arbitrary efficient high-bit-dependent subspace synthesis
is NOT equivalent to a polynomial low-defined menu. Nor does this proof cover
changing the retained subspace after measurement outcomes, collective packet
measurements, partial-secret side information, or correlated decoding.

## 6. What To Research Next

Deprioritize low-label-selected overlapping product extraction. Either use
genuine outcome-adaptive quantum transformations with explicit branch laws,
construct high-bit-dependent subspaces outside the finite-menu class with
a new posterior source proof, or decode the correlated packet directly.
Known nonuniform labels may be deliberately useful; do not discard them
merely for failing an IID interface. Keep classical competitors and original
natural-problem reductions separate from state-manipulation identities.

This audit refines the fresh-label condition in
[the recent sample-only sieve, Lemma 7](https://arxiv.org/html/2609.34996v1):
low-residue selection is essential to its uniformity argument. Our overlap
postselection consumes additional higher-label information and needs the
conditional-space calculation above. We do not certify that paper here.

The next general SOURCE compiler can use integer congruence lattices instead
of large state arrays. For retained monomials of degree 2<=h<t, the carry
criterion gives a linear constraint on Z modulo 2^(t-h), plus low-bit tests.
Degree h=t contributes only a low-bit test; degrees above t vanish.
If R is that constraint matrix and D its diagonal moduli, compute the lattice
`Gamma_R=R Z^m + D Z^c`. Its index delta_R gives reachable constraint count
`prod(D)/delta_R`, and membership tests detect impossible targets.
Add output map J with modulus Q=q/2; the joint lattice index delta_joint
gives conditional output support size `Q^d*delta_R/delta_joint` per component.
With output coordinates FIRST in a column-HNF ordering, the leading output
block spans the kernel-projection lattice and has determinant
`delta_joint/delta_R`. This exposes the output subgroup without a state array.
These formulas are a derived NEXT-TASK interface, not an implemented or
independently reviewed higher-level compiler. Expansion of all monomials can
itself be exponential; the resource ledger must not hide it.

## Reproduction And Delegation

    python theorems/dcp_carry_source_law.py --save
    python -m pytest -q tests/test_dcp_carry_source_law.py
    node research/certificates/dcp_carry_source_crosscheck.js

Gemini: routine qsearch/registry integration, source-selection lineage schema,
bitmask-safe serialization and full production validation. Do not accept a
candidate solely from this certificate. No new algorithm, independent proof,
production wiring or commit is claimed by this theory pass.
