# Independent adversarial review — findings and remaining obligations

Started **2026-10-22 10:29:22 UTC**; closed **2026-10-22 16:27:20 UTC**, within the
six-hour deadline of **16:29:22 UTC** (03:29:22 Sydney, 23 October).
The bounded investigation and final proof pass are complete; the remaining
mathematical obligations below are open. All edits
are confined to this directory; no agents, other-chat messages, automations,
Git changes, or iCloud repair were used. Earlier checkpoints are preserved
in CHECKPOINT_HISTORY.md; the subject-specific proofs below supersede
their preliminary scope statements.

## Strongest finding: broad native families have polynomial classical solvers

**Proved deductions.** Retain the supplied F_(2^n), every distinct public
point alpha_i, H_(j,i)=alpha_i^j for j=0,...,K-1, and every target bit.
The task is Hx=0 and Tr(inv0(x_i))=b_i, with N=n^2, K=floor(N/8).
Neither algorithm changes this relation or assumes a supplied witness.

| Field degree | Required zero targets | Classical guarantee |
|---|---:|---|
| Even n>=8 | At least 2K | Expected polynomial time; explicit cap/failure bound |
| 3 divides n, n>=6 | At least 3K | Deterministic polynomial time |

See **SUBFIELD_EXTENSION_ATTACK.md**. The even-degree proof uses accepted
subfield values, constructive matroid union and paid coset sampling. The
degree-three proof constructs three accepted directions spanning the field,
then uses matroid intersection and one syndrome solve. A conservative
elementary bound for the latter is O(n^11) bit operations; no optimized
practical timing advantage is claimed.

Uniform independent targets meet these conditions except with probabilities
at most exp(-N/8) and exp(-N/32), respectively, for ANY supplied points.
Targets generated from a hidden uniform codeword obey the same bounds
up to the proved near-unit fiber factor; the witness is not supplied.
These algorithms rule out a superpolynomial search separation on those
distributions. They do not solve the entire worst-case native relation or
rule out smaller polynomial improvements. Prime n was not an input promise.

**Experimental observations, separately:** saved native witnesses verify
at n=20 and n=21. The n=20 control repairs the point-set rank defect that
defeated the initial single-buffer method. A deterministic n=9 control
passes at exactly 3K zero targets. All parity and trace equations were
checked; these finite controls support implementation interfaces, not the
general theorems. A separate n=6 fixture forces a matroid exchange and
also returns a native witness. See the subfield and exchange receipt files.

**Self-attack:** the proofs explicitly discharge the potentially missing
rank, trace and sampling premises. The main guarantees leave degrees not
divisible by two or three, especially prime n>3, and targets below the
required zero counts unresolved. Nor do they give uniform native samples:
even randomizing their correction positions leaves these algorithms at total-variation
distance 1-2^(-Omega(n^3)) from uniform, because many output coordinates
lie in rare subfield sets. This is an algorithm-specific limitation, not
a sampling lower bound; see SUBFIELD_SAMPLING_LIMIT.md.

## Quantum result: survives mathematically, with narrower novelty

**Proved deduction in the ideal circuit model:** source preparation,
signed cancellation, support-only truncation, complete decoding, singleton
heralding, clean uncomputation, normalization and all failure terms survive
independent reconstruction. See QUANTUM_AUDIT.md. The stronger full-list
variant has exact native success probability

    lambda_b * (1-delta)^2 / P,

where lambda_b is the native fiber count relative to its balanced baseline,
delta is the ordinary source tail, and P is the fixed padded list length.
Its conditional native output is exactly uniform. EXACT_PATTERN_CHANNEL.md
derives this identity and the full support-subspace Gram spectrum. The
directly prepared normalized ball source improves the factor (1-delta)^2
to (1-delta), with an explicitly charged polynomial preparation procedure.
Both formulas refer to their respective source protocols. The
complete arithmetic/decoding procedures have polynomial bit/circuit cost;
no executed coherent decoder or hardware claim is made.

**Verified prior art:** Jo (2026), Theorem 5.2, already supplies paid
full-list projection. Horinaga–Yamakawa (2026), Theorem 5.1, implies the
native polynomial quantum conclusion after the reconstructed estimates
are substituted. The candidate increment is the explicit inverse-trace
specialization and its analysis, not a new DQI mechanism. Novelty of that
increment remains unproved. Primary links and exact scope are in LITERATURE.md.

## Gibbs and other classical attacks

**Proved distinction:** the Gibbs obstruction concerns escape/mixing from
a law already conditioned on solutions. It supplies no uniform-start
first-witness bound. The subfield algorithms give a concrete search bypass
on the families above; see GIBBS_AUDIT.md.

**Proved but incomplete attacks:** the paid latent sampler, Fourier-side
sampler, and randomized affine restriction are recorded separately. The
last leaves Theta(n) free field variables and is extendable with overwhelming
probability, but finding the extension remains open. Low-degree inverse-trace
multiples give exact equations away from zero, not a polynomial coupled
solver. Unsaturated conic/multiplier equations and reciprocal closures have
explicit false solutions. A fixed affine parametrization of inverse
coordinates reduces to at most seven disjoint codeword groups; adaptive
and nonlinear families are not excluded. See CLASSICAL_RESTRICTION.md,
LOW_DEGREE_MULTIPLIER_AUDIT.md and AFFINE_RECIPROCAL_FAMILIES.md.

**Conditional argument:** an efficient residual solver that succeeds for
almost all uniform syndromes would compose with the proved restriction
to solve the native relation. The missing solver is not assumed to exist.

## Ranked unresolved obligations

1. **Classical search on remaining inputs.** Find a paid adaptive/algebraic
   solver beyond the covered degree/zero-count conditions, especially for
   prime-degree instances, or identify a credible hard subfamily with an
   explicit input distribution or reduction.
   The small affine residual system is a concrete next attack interface.
   Finite failures, local barriers and degree bounds are not hardness.
2. **Uniform native sampling.** Determine whether a different classical
   algorithm can reproduce or approximate the quantum conditional law.
   The new search algorithms do not answer this question; their bias is
   proved, but a general sampling separation is not.
3. **Novelty and significance.** Check the explicit specialization against
   wider primary literature and compare actual resources on a stated hard
   family. The generic quantum theorem and full-list operation are prior art.
4. **Specified-chain hitting, if still useful.** Prove an actual uniform-start
   first-hit bound for the native chain. This ranks below an algorithm that
   bypasses the chain; no additional nearby mixing barriers are needed.

**Availability:** the requested five notes and relevant resident sources
were inspected. PRIME_CHARACTER_NORM_ATTACK.md and the shared field backend
were unavailable iCloud placeholders and were skipped without repair.
Review controls use only helpers inside this new directory. No formal proof
assistant certification, general classical hardness result, or experimental
quantum speedup has been established.
