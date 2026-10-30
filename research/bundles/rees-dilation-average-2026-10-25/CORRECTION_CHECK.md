# Bounded Correction Check: F1

2026-10-25. Same single independently authorized reviewer. This is an addendum to the preserved REVIEW.md, not a replacement review or a new full audit. No other agent was used.

## Verdict

**F1 is resolved by the revised access and resource-accounting text.** The revision explicitly charges native width and uniform coherent-action cost, separates copy/query complexity from elementary-gate complexity, and uses a consistent complete-channel error allocation. No further issue was identified within this correction's narrow scope.

This closes the resource/accounting qualification in the original review. It does not turn the source planner into a total gate-cost certificate or extend the original mathematical review to unrelated new work.

## Checked Repair

1. **Access promise.** [DILATION_AVERAGED_SOURCE.md:18](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md:18) now specifies a q-qubit native register and uniform coherent SELECT(U), retains an exact linear representation as the ideal comparison, defines the implementation cost C_U(eta), and explicitly excludes inferring SELECT access from separately indexed classical-g circuits. Native-copy acquisition is paid, and no inverse preparation is granted. This addresses both the access and omitted-width parts of F1.

2. **Query and gate costs.** [DILATION_AVERAGED_SOURCE.md:267](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md:267) reports Q=B*k*M as a cap on both native copies and SELECT calls. The Q*C_U(eta_U) action cost is separate from public arithmetic, address preparation, design, sampling, copy acquisition and the receiver. The polynomial-time statement is now conditional on the supplied polynomial-cost uniform action and receiver, and includes q and the action description in the complete input size. In particular, the original fixed-L, growing-q example is no longer a counterexample: its growing action cost is explicitly charged. Unit-cost SELECT access is correctly described as query complexity, not a gate implementation.

3. **Half-diamond normalization.** Let E_i and U_i be the implemented and ideal SELECT channels, with

       (1/2) ||E_i - U_i||_diamond <= eta_U.

   In a computation with at most Q such uses, telescope one replacement at a time. Surrounding channels, including classical histories, reference systems, feed-forward and discarded registers, are completely positive and trace preserving. Contractivity and the triangle inequality give a half-diamond error at most Q*eta_U, and hence output trace distance at most Q*eta_U. A variable-length adaptive computation is covered by its deterministic Q cap. Thus eta_U=epsilon/(8Q) contributes at most epsilon/8, with no additional factor of two. This is a bound for the complete process, not each normalized postselected branch. It presupposes the stated per-use channel guarantee, not an arbitrary correlated-noise model.

   Keeping the pre-existing amplification allocation epsilon/4 leaves exactly epsilon-epsilon/4-epsilon/8=5epsilon/8. [DILATION_AVERAGED_SOURCE.md:282](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md:282) correctly labels that remainder as available for separately charged implementation/receiver errors, not as an already validated budget. No full end-to-end error certificate follows solely from this split.

4. **Planner correspondence.** Static inspection of [dilation_average.py:184](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/dilation_average.py:184) through its return dictionary confirms that `queries=leaves*packets*design_size`, both copy and query fields use this value, the per-query field is the exact rational `error/(8*queries)`, and the total action allocation is `error/8`. Its positive-cap validation makes Q nonzero on accepted inputs. It exposes the uniform coherent interface, unpriced resources, and `total_gate_cost_certified=False`. These fields match the revised statement; they do not validate the design, robustness promise, receiver cap or C_U. I did not execute the planner or any tests in this correction check.

5. **Response consistency.** [REVIEW_RESPONSE.md:23](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/REVIEW_RESPONSE.md:23) accurately describes this repair and the budget split. Its reports about parent tests and executions were not inspected or adopted as evidence.

The only mathematical reasoning newly checked here is the query/action accounting and the elementary channel-hybrid calculation above. No new imported theorem or literature verification was needed. The spectral, twirl, cancellation and source-amplification results retain the status and imported dependencies recorded in the original review; they were not re-proved in this check.

## Version Checks

I compared the live proof and planner against their archived originals. The proof diff consists of the access/accounting repair and review-status wording; the planner diff exposes the corresponding resource/error fields and limitations. This comparison was not a fresh audit of unchanged content.

The four archived proof/code hashes exactly match the values recorded in the original REVIEW.md. The `.py.txt` suffixes do not change their bytes:

```text
d22c012b2e395738223094f7a8bf48f3210e64c80b78b238828f1d7c96dd9688  reviewed_snapshot/DILATION_AVERAGED_SOURCE.md
fba379dc5cb6240cfe0209408bdc6769b60a77568a94f6ebf3e1af0702a283f4  reviewed_snapshot/dilation_average.py.txt
d3603cf2ffd8aeea0822bfad928a0c1aed0fc58764f7d3cd4d84219d0c8c96c4  reviewed_snapshot/test_dilation_average.py.txt
db4bc69012937f382349407f5fe34d82e07fe48fcdc9f84d48d0bd5c04797e9f  reviewed_snapshot/replay.py.txt
```

The archived receipt hashes to `9a6f31f65bafa3d9a4fc90e5917245819b2320cfff422f9b9727890c9b96a590`, matching REVIEW_RESPONSE.md:43. I checked its hash only, not its execution claims. The original review's proof/code line numbers should be resolved against these archived versions, not the revised live files.

This correction check concerns these live versions:

```text
ac7e78705bf5172a3b2f0a0f527dcded72fed1a52d0aa859eddd388acd8d022b  DILATION_AVERAGED_SOURCE.md
440533c3be6d453957a735d41a99ab0020c89683ad125cf4cfde71b8efe92714  dilation_average.py
fb4b2a4028d392399863baf9bfec7d4187125fbfccf6c47503e9caa5f0a4af34  REVIEW_RESPONSE.md
```

## Limits And Changes

- This is only an F1 correction check. It is not another mathematical audit, formal verification, implementation certification or endorsement of the complete Rees result.
- Actual C_U(eta), native state supply, synthesis, public-operation budgets, design validity and a sufficient receiver cap remain supplied or separately verified obligations. A declared cost function and planner fields do not prove their realizability.
- Original pure-state, linear-action, robustness, fresh-copy/scale and discarded-record promises remain substantive. No new physical-source or noise guarantee was checked.
- No parent tests, new independence controls, original reviewer controls or full review were rerun. No test result was used to establish the correction.
- The sole file created by this check is CORRECTION_CHECK.md, using apply_patch in the isolated bundle. REVIEW.md, reviewer controls, proof/code under review, archived snapshot, main/migrating repositories and staging were not edited.
