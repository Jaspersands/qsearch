# Check of the κ = 2 circuit proof (`2026-11-05-rees-kappa2-circuit-proof.md`)

5 November 2026. AI-only adversarial check (Claude Code). **Status: AI-checked, pending human review.**
Not Lean. This is a report: no paper, code, registry or handoff file was edited. Labels as in the input
report: [proved] written argument, [proof-by-computation] exhaustive over a stated finite set, [sampled].

Input: `research/audits/reviews/2026-11-05-rees-kappa2-circuit-proof.md` (below "the report").
Code read: `theorems/rees_coherent_sde_k2.py` (all of it), `theorems/rees_coherent_sde.py` (`Prog`,
`Macro`, `_fresh/_reg/_release`, `_and_into`, `_or_into`, `_cswap`, `_pow_chain`, `_pow_copy`,
`flatten`, `BitSim`), `theorems/rees_circuit_arith.py` (header contract, `add_scaled_ops`,
`add_product_ops`, `mod_add_reg`, `mod_double`, `less_than_p`, `exhaustive_macro_check`),
`theorems/rees_circuit_coherent.py` (`sde_circuit`, `remap`, `MergeBlock.__init__`),
`theorems/rees_circuit_coherent_k3.py` (`sde_circuit_k`, `coherent_config_k`), and Sections 1.1–1.3, 8, 9
of `2026-11-05-rees-receiver-general-lemma.md`.

## Verdict

**Proved, with gaps that are minor and are closed here or are presentation only.** No counterexample was
found. The statement that stands is: for every odd prime p, every a ≥ 1 and every d with
gcd(d, p−1) = 2, `CoherentSDEK2(p, a, d).prog` maps |λ⟩|0⟩_S|0⟩_W to |λ⟩|s(λ)⟩_S|0⟩_W on every
canonical λ ∈ (F_p^a)^M, with s(λ) = `canonical_witness_k2(p, λ, d)`, s ≠ 0 and Σ s_i^d λ_i = 0. It is
conditional only on the macro contract (M) on canonical words. (M) is proof-by-computation for
p ∈ {3, 5, 7, 11, 13} (repo artifact) and so covers p = 7. The consequence for (D2a) at the κ = 2
grades of n4(F_7) and of the class-four instance over F_7 holds. The report's proposed paper sentence
says too much about the class-four instance and the short alternative leaves out the macro condition
(Section 5).

## 1. Algorithm extraction (task item 1)

I extracted the algorithm from the code on my own and compared it with the report's Section 1. It matches
item by item, and no branch is missing:

- Constants: m = least non-residue, μ = m−1, (S, Q) = 2-adic split, z = m^Q, u = least positive
  inverse of d/2 mod (p−1)/2 (u = 1 at p = 3). Blocks B_k have offsets o_k = Σ_{j<k}(a+1−j).
- F: every round k = 0..a is emitted. Each runs `_fd` on V + B_k (always n = a+1 columns in R = a rows),
  then δ_i = −Z[k+i], the Euler flag nq_i, masked δ', v_{k+1} = μΣδ'λ, allP = ∧¬nq,
  F_k = run ∧ allP, run' = run ⊕ F_k. V.append(v_{k+1}) happens in **every** round, garbage rounds
  included, as the report says. After the rounds: τ_l = −XOR_{k≥l}(F_k ? Z^(k)[l−1]) and the back
  substitution l = a..1 (the flag is taken from the current τ_l; for l > 1 the masked ζ'' feeds
  τ_j += −ζ''·Z^(l−1)[j−1]; for l = 1 there is a flag only). Then the weights w = F_k + τ_{k+1}·c(nζ, nq)
  for k < a and w = F_a for k = a, and x = δ·w.
- C: per column, the oblivious Tonelli–Shanks with the fixed z (S−1 rounds; the t-update is skipped in
  the last round), then the sign register σ loaded under r's bit 0, ρ = rσ, ρ^u, S_i += res, local inverse.
- `_fd`: as in the report, including dep_R := act_R (n = R+1 always holds here), the swaps only on
  columns ≥ k, normalisation by t' = w t, t −= wi t' and release of t, and elimination with the
  multiplier stored and XORed back into W[j][k].

The only details the report leaves implicit are harmless. (i) The case flags c1/c2/c3 restore nζ and nq
through X pairs. (ii) For p = 3, (p−1)/2 = 1 and p−2 = 1 make `_pow_copy` copy or test the register
directly, with no chain. (iii) When Q = 1, x itself is the chain head (r = t = x), and when also S = 1
(p = 3) the σ load is controlled on x's bit 0. All three are read-only uses or restoring X pairs.

## 2. Proof steps (task item 2)

**Lemma 1 (contraction).** Correct. 1..m−1 are all non-zero residues by minimality, so μ ∈ P. Then
c(1, δ) ∈ {1, m} and the four sign cases give products in P ∪ {0}.

**Lemmas 2–3.** Correct. The uniqueness in Lemma 2 holds because the difference of two relations
supported on positions ≤ j* with entry 1 at j* is a relation among the independent w_0..w_{j*−1}.

**Lemma 4 (sign test ⟺ stop).** Correct, and it is the crux. In the (⇒) step the relation (c, δ^P) has
entry δ_{j*−k} = 1 at j* (1 ∈ P is kept) and zeros beyond, so uniqueness forces δ^P = δ. The argument
needs exactly the first-dependency normalisation, as the report says. Controls run here: exhaustive over
every independent V (all orders) and every block at (p, a) = (3, 2), (5, 2), (7, 2), which is 1 377 /
30 625 / 232 897 cases with 0 violations. Sampled with 20 000 each, biased to blocks inside span(V)
plus perturbations and to entries in {0, ±1, ±m}, at (5, 3), (7, 3), (17, 2), (17, 3), (97, 3),
(13, 4): 0 violations. The three conditions "v_{k+1} ∈ U_k", "no δ_i ∈ N" and "v_{k+1} = 0" agree
on every case.

**Theorem A.** (i)–(v) are correct. I re-derived the telescoping in (iv): T^(l) = C_l + T^(l−1)
after the update, so R = −T^(K) = −Σ C_l. The update is masked exactly when α_{n(ζ)} = 0, and the code
does this through za. (v): (ρ^u)^d = x^{u d/2} = x because gcd(d/2, (p−1)/2) = 1 follows from
gcd(d, p−1) = 2. The even root of 1 is p−1, so s_{i*} = (−1)^u.

**B1 (FD).** Correct. When act_k = 0, piv = 0 and every flag is a conjunction with act, so the step is
the identity. When act_k = 1 and dep_k = 0, the pivot is non-zero, so the Fermat inverse is a true
inverse and the normalised t is 0 before release. dep is one-hot in all rounds, garbage rounds included,
which is what keeps the Z words canonical.

**B2–B4.** Correct. Exactly one F_k is 1, which matters: the τ selection is an XOR, and a non-one-hot F
could produce non-canonical words. Round a, if reached genuinely, always stops. For l > K, τ_l = 0, so
the garbage rounds enter only through products with 0 or under F_k = 0. One wording slip in B4:
"τ_{k+1} is last modified at back-substitution step k+1" should read "τ_{k+1} is modified only at
steps l ≥ k+2 (as a τ_j with j < l), all before step k+1, where its flag is taken, and never after".
The conclusion is unaffected.

**B5 (Tonelli–Shanks), for every p.** Correct for every S. The invariant t_j = z^{2^{j+1}⌊k/2^j⌋} and
u_j = (−1)^{bit j of k} are right, and so are the constants in code: z^{−2^{j+1}} for t (`2 << j`) and
z^{−2^j} for r (`1 << j`). The final r = r_0 z^{−k} with k < 2^{S−1} uses bits 0..S−2, which is
exactly the S−1 rounds. x = 0 gives all flags 0 and r = 0. The root circuit alone (`root_check`,
exhaustive over all of P ∪ {0}, output = even root^u from the independent reference, x restored,
workspace 0) passes at p = 3, 5, 17, 97, 193, 257, 641, 7681, 12289, 40961, 65537. That is
S = 1, 2, 4, 5, 6, 8, 7, 9, 12, 13, 16, including the Fermat primes (Q = 1, where x is the chain head).
It passes with d ∈ {2, 6, 10} wherever gcd(d, p−1) = 2 (u up to 43 at p = 257).

**Even-root choice.** Correct. p is odd and r ≠ 0, so exactly one of r and p−r is even. σ = p−1 when
r is odd.

**Degenerate inputs.** All-zero λ gives K = 0, x = e_0, s = ((−1)^u, 0, …). Zero, repeated and
proportional columns, low rank, and a = 1 (M = 3, blocks of 2 and 1) are all exercised in Section 3
and pass. At a = 1 the pairs (ζ, δ = 0) cannot occur, because K = 1 forces δ^(0)_0 ∈ N.

**Bennett cleanliness (Section 4), gap G2.** The report argues that "no item of F has an S wire as a
target". What the step needs is stronger: F's action on (L, W) must not depend on S (no item of F
*touches* S, even as a control), and C must change only S on net. Both hold by a static scan of the
programs, including macro arguments: F has 0 items touching S. C touches S only through the M
`add_scaled` items, with coefficient 1, S as target and no S operand. C touches no L wire. No macro has
its target aliased with an operand, and no macro argument meets the arithmetic ancillas or the ladder
temporaries. The pools are clean at every pop: the only releases are the normalised t (zero), chain
registers after their local inverse, and copy-stage registers after P_i⁻¹. Scanned at (7,2,2), (7,1,4),
(7,3,2), (17,1,2), (17,2,2), (97,1,2), (97,1,10), (257,1,2), (3,2,2).

**Macro contract, gap G1.** The circuit calls `add_product` with **aliased operands** a = b (the
squarings of `_pow_chain` and `_sqrt_chain`: 52 such items at (7, 2, 2), 94 at (7, 3, 2)). The stated
contract (M) and the repo's `exhaustive_macro_check` cover three distinct registers only. The
aliased case follows from (A1) together with (A4) "operands never targeted": the a and b wires are only
controls, so they stay constant, and identifying two constant equal wires changes nothing. The report
should say this in one line. I also checked it directly. An independent BitSim check of the gate lists
`add_scaled_ops` / `add_product_ops` on **all canonical words** passes: target correct, operands
restored, ancillas 0, the reversed list inverting. It covers every coefficient at p ∈ {3, 5, 7, 11, 13,
17}, and the aliased a = b squaring for every coefficient at those p. At p = 97 it covers the three
coefficients {1, μ = 4, 96}, which are the only ones any `CoherentSDEK2(97, ·, ·)` uses
(coefficients ∈ {1, μ, p−1} by the code).

**Is "canonical input" what the receiver feeds?** Yes. `MergeBlock` builds
`sde_circuit(p, g = dims[d−1], d)` (for n4(F_7) through `sde_circuit_k`, which sends κ ≤ 2 to the
original `sde_circuit`, i.e. `CoherentSDEK2`). It remaps L[c][r] → lam[c][r], S → S and anc → anc, and
sends the rest to fresh `sde_work`, an injective map, so the action is preserved. The label registers
hold one F_p digit per coordinate. Under (CLEAN), with exact transforms, they are supported on
canonical words, i.e. on arbitrary vectors of F_p^g per child. The theorem covers all of (F_p^g)^M,
which contains every label tuple the receiver produces (K_d^⊥ per child), and acts on superpositions by
linearity. It does **not** cover the approximate-QFT circuit (non-canonical label components). That
caveat is unchanged and already in the receiver lemma §8 item 5. Instance data read from the configs:
n4(F_7): dims (4, 2, 1), grade 2 has κ = 2, g = 2, M = 6, so 7^12 label tuples. Class four over F_7:
dims (5, 3, 2, 1), with grade 2: κ = 2, g = 3, M = 10 (7^30); grade 3: κ = 3; grade 4: κ = 2, g = 1,
M = 3 (u = 2). The exponent convention matches (D2): block of grade d = labels of grade d, exponent d.

## 3. Attempts to break it (task item 3)

Scripts, kept outside the repo:
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/k2chk/circ_test.py`,
`static_macro.py`, `lemma4_roots.py` and `mut.py` in the same folder. All were run with `nice -n 19`
and `/opt/anaconda3/bin/python -B`, each run < 30 s and < 0.7 GB. Every row simulates the flattened
gate list (BitSim) and asserts: inputs restored, every non-IO wire 0, s < p, s ≠ 0,
Σ s_i^d λ_i = 0, output = the module's batched reference. Where marked, the output is also compared
with **my own reference**, `my_witness`. It uses its own elimination, the paper-faithful stop test
"v_{k+1} ∈ span(V)" with the second dependency y', and general weights δ c(1, δ). It also asserts that
x ∈ P ∪ {0} and Σ x_i λ_i = 0. "Targeted" means about 60 000–180 000 candidates (uniform, `structured_inputs`,
and entries from {0, ±1, ±m}), classified by the branch signature (K, the j*−k offset and δ sign
pattern of every round, the ζ sign pattern of the back substitution, the set of (ζ, δ) case pairs), with
at most 8 kept per signature. The hand-built degenerate inputs of `degenerate()` are always included (29 at (7, 2, 2): all-zero, all-equal, geometric multiples, ±v alternating, each column zero, each adjacent pair equal or with ratio −1, one-row inputs, unit columns).

| (p, a, d), u | inputs | coverage | result |
|---|---|---|---|
| (7, 1, 2), 1 | all 343 | | pass [proof-by-computation] |
| (17, 1, 2), 1; (17, 1, 6), 3 | all 4 913 each | S = 4, Q = 1 | pass [proof-by-computation] |
| (97, 1, 2), 1; (97, 1, 10), 29 | all 912 673 each | S = 5 | pass [proof-by-computation] |
| (7, 2, 2), 1 | 920 targeted | 115 signatures (saturated: no new ones in 180 000 candidates); all 13 ζ patterns ("", 0, P, N, and all 9 of {0,P,N}²); all 9 (ζ, δ) classes | pass, = my ref |
| (7, 2, 2), 1 | 200 029 uniform + degenerate | same 115 signatures | pass, = my ref |
| (13, 2, 2), (17, 2, 2), (97, 2, 2) | 922 / 925 / 1 000 targeted | 115 signatures each; all ζ patterns and case pairs | pass, = my ref |
| (7, 3, 2), 1 (class-four grade 2) | 21 108 targeted | 5 956 signatures; all 40 ζ patterns incl. all 27 at K = 3 | pass, = my ref |
| (193, 1, 2); (257, 1, 2); (257, 1, 6), u = 43 | 60 205 / 60 269 / 20 269 uniform + degenerate | S = 6, 8, 8 | pass, = my ref |

Harness sensitivity at (7, 2, 2) on 929 degenerate + candidate inputs: mutations `tau` (sign),
`m`, `mu` and `out` (= 2, which keeps the equation true by homogeneity) are all detected.

The (7, 2, 2) targeted and random rows are samples, not the 7^12 exhaustive run. They are controls for
the proof, as the report intends.

Macro coverage at p = 7: confirmed. The repo artifact
`research/audits/reviews/2026-11-04-rees-circuit-arith/exhaustive.json` has `ok` true for every
coefficient 1..6 of both macros at p = 7 (and at 3, 5, 11, 13). The source file was modified after that
artifact (file times 22:15 vs 10:40 on 4 Nov). I did not use git to diff. Instead I re-ran an
independent canonical-word check of the **current** gate lists (Section 2, G1), which passes at p = 7.

## 4. Gaps (none affects the conclusion)

- **G1** Aliased `add_product(t, a, a)`: not literally inside (M). It is closed by the one-line (A1)+(A4)
  argument, and here by direct check (p ≤ 17, all coefficients; p = 97 at {1, 4, 96}).
- **G2** Section 4 must say "F does not touch S at all" and "C changes only S on net", not just "no
  target on S". Both are true (static scan).
- **G3** Section 0 says the theorem is unconditional for p ∈ {5, 7}. By the report's own (M) it is
  unconditional for p ∈ {3, 5, 7, 11, 13}. With this check's canonical-word macro runs, also for p = 17
  and, at the coefficients used, p = 97. Those runs are scratchpad runs, not a repo artifact.
- **G4** B4 wording about when τ_{k+1} is last modified (see Section 2).
- **G5** The paper text overclaims (Section 5).
- Side note, not in the input report: `2026-11-05-rees-receiver-general-lemma.md` §9 says "all 7^6
  grade-2 tuples". The count is 7^12 label tuples (6 children × 2 digits).
- Not checked here: Section 6 (relation to `ReesSdeSolver.lean`). The report's own Section 5 numbers
  were not re-run; the independent runs above replace them as controls.

## 5. The proposed paper sentence (report Section 8)

The long sentence is correct on the circuit. It says "the coherent receiver's block action no longer
depends on sampled label tuples" for **both** instances, and for the class-four instance over F_7 that
goes too far. (D2) also needs (D1), (D2c) and the footprint checks, and the receiver lemma's coverage
table marks these "not run through `anatomy`" for class four. Only the witness part (D2a) is upgraded
there. For n4(F_7) at grade 2 the full (D2) follows: (D2b) is symbolic, and (D1), (D2c) and the
footprints come from round 3. The sentence also lacks the AI/pending-review label. The short
alternative ("proved … for every odd p") drops the macro condition and must not be used as written.

**Final wording (AI-checked, pending human review):**

> The κ = 2 witness circuit maps every canonical label tuple λ, with its output and workspace registers
> at zero, to λ, the canonical triangular witness s(λ) and a zero workspace, so that s(λ) ≠ 0 and
> Σ_i s_i(λ)^d λ_i = 0, for every odd prime p, every d with gcd(d, p−1) = 2 and every label dimension;
> the proof is written from the first-dependency, sign-test and Tonelli–Shanks invariants and assumes
> only the correctness of the two arithmetic macros on canonical words, which is checked exhaustively for
> p ≤ 13 (AI-written and AI-checked, pending human review; not machine-verified). Consequently hypothesis
> (D2a) holds for all 7^12 grade-2 label tuples of n4(F_7), so the grade-2 block acts as required on
> every label tuple there, and (D2a) holds at the κ = 2 grades 2 and 4 of the class-four instance over
> F_7; the exhaustive run on all 5^12 tuples at n4(F_5) and the sampled runs are controls, not the proof.

Short status form for main-core.tex: "At κ = 2 the coherent witness circuit is proved to write a valid
witness on every canonical label tuple for every odd p, given the arithmetic macros (exhaustive for
p ≤ 13); AI-written proof, AI-checked, pending human review."

## 6. Claim gates

Nothing here flips a gate. `coherent_receiver_implemented`, `general_sde_implemented`,
`speedup_claim_allowed` and `independent_review` stay false. κ ≥ 3 grades, QFT_p synthesis, the
oracle and the approximate-transform circuit are outside this check.
