# Independent USD Review: Accepted Argument, Corrected Interpretation

This addendum supersedes ambiguous workspace and restart-cost wording in
the frozen unambiguous-reduction-2026-10-26 bundle. Its original files and
receipt remain untouched. The independent review is in
usd-independent-review-2026-10-26/REVIEW.md. It found no counterexample to
the exact ideal transfer theorem or the signed-pair unique-decoding argument.
This is mathematical review, not a general compiled-circuit verification.

## Joint State, Not An Automatically Clean Workspace

All input ensemble states phi_c include initially blank work. With exact
unambiguity, P=U^dagger Pi_success U is a projector satisfying
<phi_d|P|phi_c>=delta_dc p_c. For a=N^(-1/2) sum_c z_c phi_c,
lambda=||a||^2 and unit-modulus z_c, ||Pa||^2=p_bar. The accepted, inverted
state is b=Pa/sqrt(p_bar). Thus its SQUARED JOINT-STATE fidelity with
a/sqrt(lambda) is p_bar/lambda.

The target has blank work; b need not. The valid-data projector tensored
with identity on work contains the joint target, so data validity is at
least p_bar/lambda. Reduced-data fidelity is also at least that ratio,
not necessarily equal. Never reset or postselect work to manufacture a
clean output. The retained external label is erased coherently before
U^dagger, using the decoded label. Internal transcripts, arithmetic,
decoder label and coherent coins must remain available for that inverse.

The independent feasible example G=[[1,1/2],[1/2,1]], p=(1/4,1/2)
has joint fidelities1/4,3/4 and nonblank-work probabilities2/3,2/9 for
the two characters. resource_bounds.py reproduces these exact rational
quantities. The reviewer separately constructed and tested a unitary dilation.

## Count Raw Trials To A Verified Witness

Suppose proved bounds give p_bar>=p0>0 and lambda_s<=L. A raw trial
accepts its decoder branch with probability p_bar. Given acceptance,
validity is at least p_bar/lambda_s. Consequently a raw trial returns a
verified witness with probability at least p0^2/L. Independent repetition
has expected cost at most L/p0^2 raw trials, not merely1/p0. A cap
ceil((L/p0^2) ln(1/eta)) suffices in the ideal model. The exact helper uses
the slightly larger cap ceil(bits*L/p0^2), guaranteeing failure<=2^(-bits)
without floating-point logarithms. Cap exhaustion means UNKNOWN, not
infeasibility. Each output is checked against the ORIGINAL native relation.

For full support, p0=1-E and L=1+A_tail<=1+E are permitted when E<1.
A known inverse-polynomial margin1-E is required; strict E<1 alone is
not a polynomial-time certificate. The reviewed near-canonical tower
also has a deterministic classical attack, so this correction does not
create a speedup claim for it.

If the ENTIRE compiled raw-trial outcome distribution (failure included)
is within TV distance delta of its ideal version, raw verified success is
at least p0^2/L-delta. Charge synthesis precision so delta is below this
margin. This is an explicit premise, not a consequence of average decoder
accuracy. A telescoping uniform channel/operator error bound can establish
it; per-basis-state error or small wrong-answer probability alone cannot.
No physical noise tolerance is claimed.

Per raw trial charge source and character preparation, coherent pair map,
reversible elimination, acceptance test, retained-label erasure, inverse
decoder, final Fourier transform and native verification, with every
ancilla. The published pair construction is polynomial in q, not automatically
in log(q). For fixed prime q this distinction does not add an asymptotic
input-size factor, but the constant and compilation burden remain. General
gate-level compilation is still absent. Do not infer uniform sampling of
valid witnesses from a validity or fidelity lower bound.

## Literature And Scope

The reviewer checked the current
[Ragavan-Shutty v2](https://arxiv.org/html/2610.00502v2), not only v1;
its relevant decoder and transfer sections are unchanged and still use
the generic code-size-loss guarantee. Prior coherent USD reductions and
pair measurements already exist, including
[Chailloux-Tillich](https://arxiv.org/html/2310.20651v1) and
[Dalai-Girardi-Lami](https://arxiv.org/html/2601.09786v1).
The scoped comparison did not establish novelty. This addendum claims
neither a new general discrimination method nor a quantum advantage.
