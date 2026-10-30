# Binary Signed-Pair Construction And End-to-End Boundary

## Scientific Question And Status

Does the known signed-pair measurement require a dense alphabet-sized unitary,
or is there a uniform circuit polynomial in the alphabet bit length, with
the phases and coherent inverse required by the unambiguous-decoding proof?

The construction below gives the latter. `pair_circuit.py` emits a logical
gate plan, not a searched circuit. Its inverse is the reversed gate list.
Bounded simulations check the implementation and its use inside the transfer
identity. They are not a quantum experiment or evidence for an advantage.
The independent audit in ../pair-circuit-review-2026-10-27/REVIEW.md found no
fatal flaw in the local construction, resource argument or qualified sampling
bound. It did not independently rerun the parent suite or establish novelty.

The pair measurement itself and Schur-square decoding are prior work:
[Ragavan-Shutty, Sections 5.1-5.3](https://arxiv.org/html/2610.00502v2).
Our claim is a constructive resource refinement, with novelty unestablished.
This does not turn the current classically solved AG matrix into a hard input.

The completed novelty/usefulness review further DEMOTES the family-level
claim: the transfer mechanism has an explicit antecedent in
[DFS24, Lemma13, equation22](https://arxiv.org/pdf/2401.03807v2), and the new
matrix-only locator in ../schur-locator-decoder-2026-10-27/RESULT.md makes
ordinary classical-decoder DQI sufficient on these AG inputs. That comparator
has exactly uniform ideal output conditional on verification. This is not
a classical full-support dequantization. Read the independent comparison in
../usd-novelty-review-2026-10-27/REVIEW.md before using this bundle's bounds.

## 1. Exact Local Construction

For any integer q>=2, let n=ceil(log2(q)) and embed the alphabet in n qubits.
Define u=q^(-1/2) sum_(a<q)|a> and

    phi_c = sqrt(q/(q-1)) |c> - u/sqrt(q-1).

These states are orthogonal to u; their distinct-label inner product is
-1/(q-1). Let S exchange the TWO WHOLE n-qubit registers. With

    R = Pi_symmetric + i Pi_antisymmetric
      = exp(i*pi/4)(I-i*S)/sqrt(2),
    P = I+(-i-1)|u><u|,

every v orthogonal to u satisfies

    (P tensor I) R |v,u>
      = exp(i*pi/4) (|v,u>-|u,v>)/sqrt(2).

This follows directly: P fixes v and sends u to -i*u. It is crucial to
phase the FIRST register. For the particular phi_c, the two uniform terms
cancel, leaving exp(i*pi/4)(|c,u>-|u,c>) sqrt(q/(2(q-1))).

Implementation, starting with zero work:

1. Prepare u in the second register using A_q.
2. Compute the SWAP eigenvalue into one flag using H, controlled S, H;
   apply diag(1,i) to the flag and reverse the eigenvalue computation.
   This implements R, with that flag clean on every two-register input.
3. Apply A_q inverse on the first register, phase the all-zero state by -i,
   then apply A_q. This implements P on the full padded space.
4. Compute [a>b] into an orientation flag, swap the whole registers
   conditioned on it, then apply H followed by X to that flag.

An antisymmetric ordered pair has orientation |0>-|1>. The last two gates
return its orientation to zero. The output on phi_c is therefore

    exp(i*pi/4) / sqrt(q-1)
      sum_(b!=c) epsilon(c,b) |min(c,b), max(c,b)>,

where epsilon is +1 for c<b and -1 for c>b. All promised work is zero.
The sorting output is two binary labels, not a dense index of all q(q-1)/2
pairs. Reversible comparison is a prefix-equality Boolean circuit, not an
oracle. The implementation includes the prefix compute AND uncompute.

For a general v orthogonal to u, the sorted amplitude at a<b is
exp(i*pi/4)(v_a-v_b)/sqrt(q). On arbitrary padded inputs the entire plan is
still unitary, but the orientation need not be clean. In particular, u is
NOT in the promised subspace. Never reset a dirty flag when using the inverse.

Register-wide R is not a product of bitwise fractional SWAPs. Removing P,
using uniform 2^n instead of uniform q, or taking absolute values of the
signed output all fail explicit regression controls.

## 2. Uniformity, Precision And Local Resources

A_q is produced recursively by splitting [0,q) at the highest binary bit.
The two branch amplitudes are the square roots of their exact integer counts
divided by q. A full branch uses Hadamards; only one branch remains partial.
There are at most n nontrivial rotations and O(n^2) controlled gates, with
at most n controls. No loop of length q or table of amplitudes is used.

The simulator evaluates these rotations with floating-point square roots;
that is a numerical check, NOT exact algebra or a finite-gate compiler.
The plan itself records exact rational probabilities. Square roots/angles
can be computed to b-bit accuracy in time polynomial in n and b.
Efficient uniform interval preparation is already known; see, for example,
[Shukla-Vedula](https://arxiv.org/abs/2306.11747v2). We use a deliberately
simple recursion rather than claiming its gate count is optimal.

The full map's comparator raises the maximum control count to max(n,3) in
small alphabets; resources() counts the actual controls. With clean AND
chains, O(n) extra reusable bits suffice to lower all controls.
A conservative bound is 100*(number_of_controls+1) arbitrary-rotation
one/two-qubit gates per macro. This allows negative-control flips, compute
and uncompute of an AND chain, and a constant-sized controlled elementary
operation. Toffoli and controlled SWAP have constant decompositions.
Consequently the whole map has O(n^3) such gates and O(n) qubits.
This is an upper-bound argument, NOT an emitted Clifford+T netlist or a
physical qubit estimate. Finite-set gate synthesis adds a factor polynomial
in log(1/epsilon); every rotation and all lowering ancillas must be charged.

For m coordinate maps and their inverses, uniform operator errors telescope
over 2m calls, even with entangled inputs. `precision_budget` assigns one
quarter of a supplied raw-success margin to these local operations and
reserves another quarter for all other operations. If BOTH budgets hold,
the compiled raw success remains at least half the ideal lower bound.
The helper does not prove its supplied margin or synthesize the rotations.

An additional constructive control prepares phi_0 without an initial QFT:
prepare a flag with amplitudes sqrt((q-1)/q), -sqrt(1/q); conditioned on
flag1 prepare uniform [0,q-1) then increment, obtaining uniform [1,q).
XOR [data!=0] into the flag to clear it. The zero and nonzero amplitudes
then equal phi_0 exactly in the ideal rotation model. No postselection.

## 3. Complete Algorithmic Resource Argument, Not A Complete Compiler

Input: explicit full-row-rank B in F_p^(k by m), a stated prime p, arbitrary
syndrome s in F_p^k, and proved numerical bounds p_bar>=p0>0 and
lambda_s<=L for the IDEAL unambiguous decoder. The task is to output
y in (F_p minus zero)^m with B y=s, checked on the original input.

Precompute a basis of W=span(rowspan(B)*rowspan(B)), of rank w, by streaming
the k(k+1)/2 coordinatewise products through elimination. This costs
O(k^2*w*m) field operations and O((k+w)*m) field storage. No q^k enumeration.
Let r=k+w. Prepare a uniform retained label u in F_p^k, its syndrome
character exp(-2*pi*i*u.s/p), and the m states phi_0; shift them by c=uB.
All preparation and shifts have uniform polynomial bit cost.

After the signed-pair maps return (a_i,b_i), solve the m by r linear system

    wword_i - (a_i+b_i) vword_i = -a_i*b_i,
    vword=u' B, wword=t W.

Accept only a UNIQUE consistent solution. The true pair (c,c*c) always
solves it on the ideal transcript support. Thus an accepted u' is never
incorrect. An underdetermined system returns FAILURE, not an arbitrary
solution. Check pair validity and define behavior on every padded bit string.

Bounded Gaussian elimination takes O(m*r^2) field operations. Make it
reversible by retaining pivot choices and arithmetic history. Use a total
inverse operation that sends zero to zero; guard its use by nonzero tests.
Grade-school field arithmetic gives a conservative polynomial bit cost,
for example O(m*r^2*(log p)^3), and a polynomial history-space construction.
No optimized reversible elimination netlist is implemented in this bundle.

Keep all decoder workspace. Test acceptance/equality, erase the external u
using u', apply the COMPLETE inverse decoder, apply the final Fourier
transform on the data, and verify the measured y. Work after inversion may
be nonblank. Do not measure transcripts or decoded labels along the way.
The known cyclic QFT has polynomial cost in log p and log(1/epsilon):
[Hales, Chapters 2.4 and 4, especially Corollary 1.12](https://arxiv.org/html/quant-ph/0212002v1).
Its accuracy must cover entangled data and retained work, not just basis
states. Efficient Fourier sampling is sufficient for the final measurement.

The reviewed transfer bound gives raw verified success at least p0^2/L,
not p0/L. A total raw-trial TV error delta reduces it by at most delta.
Expected trials are at most 1/(p0^2/L-delta); an independent restart cap
adds log(1/eta) for failure probability eta. Polynomial runtime requires a
proved inverse-polynomial success margin, not merely E<1. This bundle removes
the local poly(p) synthesis dependence, but does not automatically establish
the source, decoder-bound or useful-problem promises.

## 4. Approximate Uniform Sampling, With Its Error Floor

For the FULL-SUPPORT set source, the normalized target after the final Fourier
transform is the uniform pure state on the original syndrome fiber, with
blank work. Write F=p_bar/lambda_s for the joint target fidelity and v for
the actual data-valid probability after accepted inversion. Projection onto
valid data leaves the target fixed, so the conditioned joint fidelity is
F/v, which is at least F since v<=1. Measurement and trace-distance bounds give

    TV(ideal verified output, uniform fiber)
      <= sqrt(1-F/v) <= sqrt(1-p0/L).

This uses the JOINT fidelity to the specified uniform target, not merely a
high probability of validity. Dirty work is retained throughout. It is not
an assertion that a valid-output algorithm is automatically a uniform sampler.
The finite binary-inverse controls compute the entire verified data law and
check this inequality. This is a standard fidelity consequence, not a claimed
new sampling reduction or proof of classical hardness.

For compiled raw trials, collapse every non-witness outcome to FAILURE.
Let mu,nu be ideal and compiled laws, with valid masses z,z', and total TV
at most delta. If delta<z, then z'>0. The triangle inequality gives

    2 TV(mu|valid,nu|valid)
      <= (||mu_valid-nu_valid||_1 + |z-z'|)/z
      <= 2 delta/z.

Since z>=s0=p0^2/L, the verified conditional sampler has TV at most

    sqrt(1-p0/L) + delta/s0.

Fresh identical independent trials stopped at the first verified witness
have that same conditional output law. A cap with abort probability eta
adds at most eta when compared to the no-abort target distribution. The
cap costs O(log(1/eta)/(s0-delta)); all trial costs from Section3 remain.
`sampling_bounds.py` provides exact rational upper bounds (including a
rounded-UP square root), not verification of the supplied premises.

For p0=1-E and L=1+A, the intrinsic squared TV bound is
(E+A)/(1+A). A family with proved exponentially small E,A therefore admits
negligible-error sampling at polynomial precision/repetition cost. Increasing
precision or retrying does NOT remove this intrinsic error floor on a fixed
input. This is NOT an arbitrary-epsilon sampler for every finite instance.

Classical fiber repair solves search but does not by itself reproduce this
law. Uniform affine-fiber rejection does produce the exact uniform law, at
expected cost inverse to the full-support mass. Both must be compared on
the SAME B,s. Fixed-bank mixing failures remain insufficient evidence against
all classical samplers. No native higher-level sampling separation is shown.
This argument also does not transfer the local pair map to the distinct
inverse-trace ensemble, whose Gram structure need not be the simplex above.

## 5. Strongest Falsifiers And Research Decision

The immediate construction falsifiers are the sign, padding, inverse,
orientation and uniform-error controls above. They pass locally; independent
review and a documented run are separate gates.

The broader claim still faces these decisive objections:

- Prior work may subsume the transfer theorem or this elementary circuit.
  Novelty is explicitly unestablished; consult the separate literature audit.
- A polynomial quantum solver for this promise family is not a classical
  separation. Two-basis greedy avoidance already handles the covered
  large-field regime. Fiber repair solves the actual43-by-176 AG example.
- The generic closed-prime divisor source is not the easy11I-E source.
  Its higher-level backend remains absent. A parameter forecast is not an input.
- Full Schur cube, failure of short moves and first-witness/mixing obstructions
  do not rule out global classical solvers, particularly multibasis extraction.
- No reduction from a recognized useful hard task to the promised AG family
  has been supplied. Reverse reductions do not establish usefulness/hardness.

Therefore do not promote a candidate, build a UI feature, or enlarge toy
controls because the local map is efficient. The completed comparison supplies
no distinct new AG algorithmic regime: ordinary matrix-only classical-decoder
DQI already covers it. Further work needs a genuinely new task/reduction or
a receiver outside known decoding coverage, not more gate-count polish or
an AG source expansion justified by the now-false quantum-only-decoding premise.
