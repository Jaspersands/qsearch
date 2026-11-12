# Claude research agents in the autonomous discovery loop

Owner authorization: 6 November 2026, prepaid $200 credit, no automatic
reload. This supplements the existing Codex theory / Gemini mechanical
division; it does not replace GOAL.md, STATE.md or TRAPS.md.

Owner update, 6 November 2026: USD189.47 remains, nothing else needs the
credit, and it expires in seven days. The explicit direction is to use it
wisely AND use it all. Treat this as a research allocation to spend before
expiry (approximately 13 November), not money to conserve indefinitely.
Increase useful independent hypothesis generation, focused proof attacks,
classical-counterpart searches and source audits. Prefer several distinct
scientific obligations over redundant agreement or oversized empty requests.
A provider refusal is not a result and is not retried by rephrasing it.
The owner-reported USD189.47 is a balance anchor, not a balance measured by
this runner. Record subsequent usage estimates separately; do not claim an
exact remaining balance by subtracting estimates. No new infrastructure or
automation is needed to spend this research budget.

Owner update, 12 November2026: OpenAIUSD142 expires in9days (approximately
21November); AnthropicUSD136 also dedicated to this research. Explicitly use
both wisely and use the allocations, including concentrated work in one day
when useful. These are owner-reported balance anchors, not API measurements.
OpenAI requests use tools/openai_research_agent.py (Responses API, gpt-6-astra,
max reasoning for core mathematics, no tools/retries, saved context/usage).
Model access and official price10USD/input-million,50USD/output-million were
checked Nov12. The same explicit-context, advisory-review and unknown-billing
rules apply. Credentials are read only by clients, never attached to prompts.
A local PDF control-character validation failure made NO API call; sanitized
excerpts were then submitted. The recovered Nov7 sampler report completed at
estimatedUSD0.277960; include it at the next ledger milestone.

Usage checkpoint, 12November2026, after the closed OPI pass: Anthropic82
saved nonpartial estimates totalUSD62.891114;40 completed/nonempty reports.
Two older terminal ReadTimeout totals remain UNKNOWN and excluded; partial
countersUSD0.006250/0.027600 are not final charges. OpenAI2 completed/nonempty
reports totalUSD3.302960. Saved provider-separated audit:
audits/controls/opi_tilted_walk/usage.json. These historical totals are neither
invoices nor remaining balances and must not be subtracted from owner anchors.
OPI added/recovered AnthropicUSD2.529980 and OpenAIUSD3.302960. Four complete
reports and one truncated source report were parent-read; source mistakes and
finite-clock overstatement were rejected, substantive fixes recorded. No retry.
The minimal OpenAI runner passed syntax and one offline overbudget guard.

## Scientific placement

1. Start from STATE and TRAPS and refresh a stale state from the latest
   handoff entry. Check corpus been-tried, then actual primary literature,
   and the corpus baselines for the precise candidate.
2. Select ONE externally motivated scientific question. Use a Claude agent
   when independent reasoning can falsify the mechanism, remove a named
   blocker, identify a stronger classical attack, or change the direction.
   Do not run reviews merely to accumulate agreement.
3. Send a task-specific brief and explicit research context: current state
   excerpt, target note, precise source excerpts and relevant existing
   controls. State input/output, access, quantifiers, resource target,
   unresolved proof obligation and cheapest falsifier. Prior acceptance
   labels are not evidence. Fetch primary sources with the parent tools;
   this runner gives Claude no filesystem, shell, browsing or action tools.
4. Normally use one or two independent tasks. Keep a proof attack separate
   from a constructive or classical-counterpart search. These are independent
   requests; their prompts should not contain one another's conclusions.
5. Inspect the saved response and stop reason. Reproduce concrete
   counterexamples or check the cited source scope before acting. Mark each
   substantive finding accepted, repaired, rejected with reason, or open.
   A truncated or empty report is not a completed review. Do not silently
   retry a failed request whose billing outcome is unknown.
6. Record the result and run artifact in the topic note/handoff, put only
   mechanical work in Gemini's queue, and update STATE at the pass boundary.
   Agent approval alone never establishes a theorem, novelty or separation.

## Model and effort choices

The account's Models API was checked on 2026-11-06. Route difficult
mathematical questions to `claude-fable-5-1` or `claude-opus-5-5`, and
narrow source comparisons to `claude-sonnet-5-5`. Start a narrowly scoped
Claude review with explicit `--effort high` (omitting it leaves the provider
default, for compatibility with older models). Keep the parent's core derivation at top effort.
Use Claude `max` only when its additional reasoning is worth a substantial
risk of getting no report; it is not a productive default in this setup.

Observed during integration: both broad `max` audits exhausted32768
output tokens without final text, and even a narrow Opus/max residue
lemma exhausted64000. A narrow Opus/high generator audit returned useful
findings in11721 output tokens. Thinking consumes the output budget.
Later in the same day, two high-effort 64000-token searches and a
32768-token Fable proof attack also ended empty; a distinct narrow Opus/high
coordinate audit returned a useful report in12621 output tokens. High
effort alone does not prevent empty runs; sharply scoped proof obligations
have produced more usable findings.
Prefer one precise obligation per request and adapt from returned value;
do not keep doubling budgets after empty reports. A completed report
still requires mathematical verification, irrespective of effort setting.

The runner uses explicit standard-price model IDs and a price snapshot.
Refresh that snapshot from official documentation before adding a model or
relying on changed pricing. It provides no model fallback, paid tools,
automatic retry loop, fast mode or prompt-cache writes.

## Running a review

Use `/opt/anaconda3/bin/python`. Prepare a short prompt file and selected
context files under the repository; a context excerpt should retain its
source URL, original locator and source hash when applicable. Never attach
`.env`, private keys, credentials, or the whole handoff/priority archive.
For PDF text, select `sed`-style line ranges with `split("\n")`, not
`splitlines()`: the latter also counts form-feed page breaks. Inspect the
actual snapshot for the cited statement and proof. During integration this
mistake omitted Greither's proof paragraph; Claude correctly blocked on
the missing source. The corrected packet and old requests are both retained.

Example after preparing the input files:

This retained bundle illustrates the command shape; do not repeat a closed
audit merely as a smoke test.

```bash
/opt/anaconda3/bin/python tools/claude_research_agent.py \
  --prompt-file research/audits/claude_inputs/2026-11-06-prime-index/generator_gate_prompt.md \
  --context research/audits/claude_inputs/2026-11-06-prime-index/generator_gate_excerpt.md \
  --role adversarial --model claude-opus-5-5 --effort high \
  --max-tokens 32768 --max-budget-usd 1
```

`--dry-run` builds the request locally without API access. Normal runs
count input tokens, add a conservative allowance, and reject a request
whose estimated input plus maximum output cost exceeds the per-call
budget before issuing the paid generation. This is a pricing-based
preflight estimate, not an invoice guarantee or an account-balance query.
The provider's finite prepaid balance is the external spending limit.

Every run retains its exact request/context snapshots and hashes, model,
effort, timestamps, response, stop reason, usage and estimated charge under
`research/audits/claude_runs/` (or an explicit output directory). Keep
unknown-charge failures visible; never count them as zero-cost success.
The sum of recorded usage estimates is spending observed through this
runner, not the provider's exact remaining balance or other agents' usage.

## Sources for the integration

Current [standard prices](https://platform.claude.com/docs/en/about-claude/pricing),
[effort and thinking-token limits](https://platform.claude.com/docs/en/build-with-claude/effort),
and [token-counting API](https://platform.claude.com/docs/en/build-with-claude/token-counting)
were checked on 2026-11-06. Scientific sources belong in each task's
input bundle and are subject to the repository's normal source audit.

7 November hidden-cubic admission: two distinct general-gap/frame-extraction
requests at high32768 ended max_tokens with no report (estimate USD2.350002).
No findings or retries. Keep future briefs at one sharply isolated lemma;
a known-token-limit failure is not a reason to repeatedly double budgets.

7 November general-sparse attack: one precise derivative audit refused after
8102 output tokens; one constant-map construction exhausted32768 without a
report. Total estimate USD0.900988, no findings/retries. Direct proof review
was completed independently. Empty requests are not research evidence.

7 November two-Fock Gaussian learning: two sharply separated exact-spectrum
and stability requests both returned substantive reports. Total estimated
usage USD1.650348. Exact signs/spectrum, sequential rounding and phase
completion checked; source/parity and common-subspace transport obligations
were independently resolved. No retry, unknown charge or balance inference.

7 November sparse-Fock torus falsifier: one sharply scoped Cartan-moment/
approximate-support audit returned a useful report, estimate USD0.596230.
Its quantitative proof was checked; an unsupported extension claiming
failure for active Gaussian frames was rejected. No retry or balance claim.

7 November arbitrary-two-Gaussian learning: four distinct obligations cost
an estimated USD5.559080. Covariance and sequential-endpoint reports completed;
quartic and whole-frame-composition requests ended empty at32768 tokens.
No findings/retries from the empty calls. The positive quartic and complete
composition were derived and independently checked internally. Exact signs,
reference-branch scope, contiguous-order and compilation-error repairs were
recorded; actual MPS primary source confirms the endpoint is known machinery.
Future calls should remain sharply bounded: the two successful reports had
one isolated quantitative obligation each. No balance inference.

7 November wild-local admission: two distinct full-source resolution-cost
and conditional Picard-generator searches ended empty at32768 tokens, total
estimated USD2.759310. No findings/retries/pending calls. Independent exact
source falsifiers and primary-source scope audit support PARKING the general
Selmer candidate, not a complete algorithm or impossibility. Prefer short
explicit proposed operations/identities or bounded source comparisons for
future Claude tasks; do not rephrase these empty searches or raise their cap.

7 November mixed-Gaussian learner: a narrowly specified Fable/high16k
exterior-inverse request exhausted its output budget after a397-character
verdict/convention prefix. Estimate USD0.828720; no usable proof or completed
review, no retry/pendingcall. Core, source and numerical composition were
independently checked internally. The final output is a direct mixture of
<=4known Gaussians, so no CJ/postselection backend is needed. Short prompts
and smaller output caps do not guarantee a usable report; retain stop reasons
and assess actual returned work. Aggregate estimates are not account balance.

7 November relative norm composition: Opus compact-coordinate report completed,
estimateUSD0.312188. Its BIT, torsion and exact-lattice suggestions were checked
and integrated. Distinct Fable support request timed out without a report;
billing unknown and partialUSD0.006250 not final. No retry or claim from it.
Scientific support/source/endpoint proof has a separate completed independent
review. Prefer the productive narrow Opus/high route for the next distinct
obligation; do not spend another call retrying this support question.

7 November reduced-norm search: two narrow Opus/high reports completed,
estimated USD0.766564 total. Local root-valuation/degree proof checked and
finite clocks paid; module report identified a real unchecked-rho certificate
gap. The expanded presentation check and canonical trace/cochain/Cramer
construction repair it. Blanket general-PIT and wrong-cochain-type objections
were rejected with explicit format/type reasons. Both reports and dispositions
are retained in REDUCED_NORM_PRESCRIBED_FIELD.md. No retry/live call or balance
inference; the earlier partial timeout remains UNKNOWN, not zero cost.

7 November stabilizer-span/minimum-rank falsifier: two distinct narrow Opus/high
proof attacks completed, total estimateUSD0.506252. Support/frame/fidelity and
algebraic tagging proofs checked. Useful approximation warning retained;
incorrect conflation of polynomial BIT precision with COPY complexity rejected,
as was the overstatement that exact-rank pinning has zero robust radius.
All substantive dispositions are in STABILIZER_SPAN_RECONDITIONING.md. No
retry/pendingcall. Earlier partial timeout remains UNKNOWN; no balance claim.

7 November arbitrary-CSA minimal modules: two narrow Opus/high attacks both
completed with useful reports, estimateUSD0.860428. Local field/sign/height and
compact Hom/affine ranks checked. Clarified transcript-relative canonicity,
separate classical index certificate, exact upstream homomorphism and fresh
moduli. A splitting field alone is not a computed split map. Independent full
core/source reviews and exact classical control close the written conditional
composition; no novelty/separation/fullquantumexecution. No retry/balance claim.

7 November surface torsion-cover pass: five distinct requests estimateUSD4.303624.
The native reselection report supplied a concrete K3-P2 lead; its untwisted
permutation identity was independently refuted, and cyclic-character/explicit
twist construction was developed and reviewed separately. Two requests refused;
two ended empty at token limits (32768/24576). No findings from those four,
no retries and no live calls. The separate KS-marking request did not produce
a report; the stronger classical comparator remains open. Future briefs should
be sharply bounded and chosen for expected scientific value; increasing token
limits after empty reports is not the default. All proof status comes from
verified reasoning/source scope, not API completion or accumulated agreement.

7 November quintic-surface pass: one isolated Lie/cocharacter proof audit at
high16384 returned a useful report, estimateUSD0.512620. Core proof checked
against actualSchnell/Deligne sources; Tate-onlyMT wording repaired (Gm may
occur, Lie stillweight0). The obstruction was alreadyknown; no novelty credit
assigned. Nativequantum composition was independently reviewed separately.
No failed/live call or retry. This tightly bounded lemma produced usable
output; it does not justify repeated agreement calls or automatic promotion.

7 November folded-chain transform: two distinct high-effort16384 requests.
Fable returned a useful all-length word-bijection proof (USD0.872230), checked
against the direct native Pauli matrix and independent all-N review. Opus
unitary-composition request exhausted its cap with no report (USD0.351284);
no findings or retry. Total estimateUSD1.223514. Two initial LOCAL input-format
rejections occurred before API access; PDF layout control characters were
normalized for the first paid calls. Known bulk encoding is prior art, and
normalization/source scope plus the arbitrary-input classical-comparator
boundary were verified independently. No completion label promoted a claim.

7 November compact integral similarity: local-residue audit completed with
useful proof details (prime-norm and denominator-identity report errors were
corrected); determinant-character request truncated empty at16384. Combined
estimateUSD1.093082, both terminal, no retries. Residue machinery is prior
repo work; the full compact witness composition was independently reviewed.
An empty audit is no evidence. Keep requests distinct and sharply bounded.

7 November local halving saturation: two Fable/high32768 requests addressed
distinct index and precision obligations. Index truncated WITH partial text;
precision completed. EstimateUSD3.369280, terminal/no retries. Independently
proved Haar-volume index bound supersedes missing-index conclusions. Accepted
zero labels of initial formal seeds; rejected initial-rank/all-steps assertions
and refuted an unqualified chart-repair bound by exact all-h resultants.
Source warning and stable-half precision remain open. Partial text is not a
completed review; even substantive completed reports need direct verification.

7 November local finite-precision saturation: Opus/high Smith-kernel review
completed (estimateUSD0.378556); core lemma accepted, monic normalization
and injectivity errors corrected, generic rank-drop not a native falsifier.
Independent derivation closes exact bounded Stoll kernel shape. Fable/high
certificate request exhausted32768 with ZERO report (USD1.731690), no
findings/retry. CombinedUSD2.110246. Both terminal/reaped. Packet-control-
character validation failures occurred before API calls and were repaired.
Next useful calls should isolate a concrete conditioning/certificate identity;
no repeated full-half search or larger budget justified by this empty result.

7 November Bethe-prefix repair: one precise constructive ALL-prefix request
terminated ReadTimeout, empty response; process reaped. No findings or retry.
The partialUSD0.027600 counter has UNKNOWN billing and is excluded from the
nonpartial aggregate. The exact determinant-deletion falsifier, one-hole-dual
obstruction and one-site classical baseline were independently established.

7 November spinor-genus admission: transport/support request returned
stop_reason=refusal with empty response (USD0.034984); the distinct local
dyadic compilation attack exhausted16384tokens empty (USD0.844160). Both
terminal/reaped, no findings or retries, total estimateUSD0.879144. The
classical character falsifier and dyadic lemma were checked independently.
Do not rephrase the refused request or repeatedly enlarge the empty one.
Future spending should target a distinct operation or source question that
can change the next scientific action; no paid agreement or budget-only runs.

7 November Gaudin joint-charge traversal: two distinct high24576 obligations
estimateUSD1.796010. Opus returned8056bytes of TRUNCATED QPE critique; parent
read all and accepted tail/leakage cautions, repairing one omitted target-tail
term. It is not a completed review and is not the proof of the simpler
random-dephasing theorem. Fable gap search was TRUNCATED/EMPTY, no findings.
Both terminal/reaped, no paid retry. Initial plain-text validation failures
were local before API calls; PDF formfeeds were removed. Two complete
independent internal reviews establish only the conditional construction.
Do not infer a universal spectral gap or balance from these records.

7 November binary-Fock Kerr: one narrow Opus/high16k binomial BIT proof
attack completed, estimateUSD0.297948. Certified envelope, finite clock,
Stirling and normalization suggestions checked; parent added denominator-
bitlength precision guards and explicit outer coupling. One distinct broad
native-hypothesis request refusedEMPTY, estimateUSD0.017036, no findings or
retry. CombinedUSD0.314984. Three internal reviews separate prior-art QHT,
full quantum composition and restricted classical sampler. No general
Fock dequantization or novelty/separation follows. Terminal usage only;
the two previous unknown bills remain unknown. Dedicated expiring credit
continues allocated to distinct useful research obligations, not retries.

7 November Gaudin two-cluster gap: one distinct narrow Opus/high16384
finite-spacing fusion obligation refusedEMPTY, reported3922 input/5894
output tokens, estimateUSD0.133568. Terminal/reaped, no findings or completed
review, no retry. The saved n^-16 context remains historical; the independently
checked final proof uses n^-8. Parent and CLOSED core/source reviews plus
exact Sturm/native-bound arithmetic establish the counterfamily; nothing is
promoted from this provider refusal. Weaker polynomial gap remains OPEN.
Older unknown bills remain unknown; continue distinct useful obligations.
