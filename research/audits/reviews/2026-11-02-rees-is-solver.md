# Rees Schedule 1: a deterministic Ivanyos–Santha Section 3 SDE solver

2 November 2026. Campaign item 9 of `research/REES_FULL_CAMPAIGN.md`. AI-only pass (one
session plus one independent code-review helper). It is not human review. Labels:
**[proved]** (written argument here or a cited theorem), **[exact]** (complete finite
computation or exact-arithmetic test), **[argued]** (heuristic or partial).

Files written: `theorems/rees_is_sde_solver.py`, `tests/test_rees_is_sde_solver.py`, this
report. Scripts and their outputs (outside the repo, in the shared notes folder):
`…/side-session-notes/local_82ea8e9d-…-291cbf4bed0b/rees_is_solver/` (`path_stats.py`,
`zero_sum_lengths.py` with `.out` files) and `rees_is_solver_pytest.out` next to it.

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_is_sde_solver.py
```

Result: 152 passed in 16 s **[exact]**. `git status --short` is identical before and after the run.

## 0. Answers

1. **Built.** `is_sde_solve(p, d, columns)` returns a verified s ≠ 0 with
   Σ_i s_i^d λ_i = 0 for arbitrary columns in F_p^g, for every d and every odd prime p.
   It is deterministic: no random draws, no nonresidue search, no field enumeration. Every
   step of arXiv:1503.09016v2 §3 is implemented: the gcd reduction, §3.1, Lemma 12, Theorem 11
   and §3.3. Fact 2 is van de Woestijne's zero sum of d-th powers from ISSAC 2005 §6.1–6.2,
   with one labelled substitute (item 3).
2. **Arity.** The run consumes exactly G(κ, a)^L columns, where a is the rank of the column
   matrix, G(κ, a) = κ^{κ(κ−1)/2}(a+1)^κ, L = ⌈log₂ t⌉, and t ≤ κ+1 is the length of the
   deterministic zero sum of κ-th powers. So it needs at most B_κ(a) ≤ B_d(a) columns, the
   bound of main.tex (eq:is-arity) **[proved]**, and checked for d ≤ 9, a ≤ 3 and 16 primes
   **[exact]**. Below that count it refuses with `ValueError` and never guesses.
3. **Substitute for one sub-step.** The ISSAC note states van de Woestijne's Selective Root
   Extraction (Theorem 5.1) but only sketches its own algorithm, and the thesis download
   returned an HTML page, not the PDF. `selective_root` implements the same contract over
   F_p: given d+1 nonzero elements, return i < j and β with a_i = β^d a_j. It uses the IS
   §3.1 tools instead: a generator η of the π-parts of the inputs, Pohlig–Hellman logarithms
   base η, and pigeonhole on log mod g, with g = gcd(d, ord η). An element η^k is a d-th
   power in ⟨η⟩ exactly when g | k. This is deterministic and poly(d, log p) **[proved, §3]**.
   It is a clearly labelled equivalent, not a transcription of van de Woestijne's own
   prime-by-prime Tonelli–Shanks extension.
4. **Executed range.** End-to-end with exact witnesses: κ = 1, 2, 3 at full arity B_κ(g), and
   κ = 4 whenever the deterministic zero sum has t = 2, at G(4, a) = 65536 columns for a = 1.
   Degrees d up to 9 are covered through the gcd reduction. The primes include
   p = 3, 5, 7, 13 and five 30-bit primes **[exact]**. κ = 4 with t ≥ 3, and every κ ≥ 5, are
   implemented but too large to run. At κ = 4, a = 1 they need G² ≈ 4.3·10⁹ columns or more,
   and G(5, 1) ≈ 3.1·10⁸ already. For those, only the components were executed: Theorem 11
   at d = 4 on p = 13 and a 30-bit prime, and the zero sums for κ ≤ 12 and all p < 400.
5. **Do not flip `general_sde_implemented` yet.** §8 lists what would justify it.

## 1. Sources read

- Ivanyos–Santha, arXiv:1503.09016v2 (SHA-1 `8aacdff2…`, the same file as the core check):
  §1 (Fact 2, Theorem 3), §2 (Propositions 9–10, for the pattern) and §3 in full (§3.1,
  Theorem 11, Lemma 12, the proof of (13), §3.3).
- van de Woestijne, *Deterministic equation solving over finite fields*, ISSAC 2005, all six
  pages (author's copy, opt.math.tugraz.at/~cvdwoest/maths/issac2005.pdf): Proposition 2.1,
  Theorem 2.2, §3 outline, Theorem 5.1, §5.2, Theorem 6.1, §6.1 reduction, §6.2 special
  case, Theorem 6.2. The thesis (Leiden 2006, hdl 1887/4392) is cited by IS as [28] and was
  not obtained.

## 2. Map from the paper to the code

| Paper step | Code | Notes |
|---|---|---|
| §3 opening: d′ = gcd(d, q−1); t·d ≡ d′ (mod q−1); s = x^t | `reduced_degree`, end of `is_sde_solve` | t > 0, so 0 ↦ 0 |
| §3.1: H_π × H_π′, δ′ = γ′^r with rd ≡ 1 mod \|H_π′\| | `PiParts.split`, `rest_root` | idempotent exponents by CRT |
| §3.1: η generates the π-parts seen so far; ζ_i = η^{i−1}; Pohlig–Hellman | `Classifier.classify`, `PiParts.dlog` | ζ_r may repeat, as the paper allows |
| §3.1: failure ⇒ η ← generator of ⟨η, γ⟩, restart everything | `_Restart`, `PiParts.join`, loop in `is_sde_solve` | at most Ω(\|H_π\|) restarts |
| Lemma 12, ℓ = 1 and ℓ → ℓ+1 | `lemma12` | E = d^ℓ(m+1) groups of B_ℓ |
| "arrange J_1 (resp. M_{ℓ+1}) nonempty" | `_classified_kernel` | see §4(a) |
| Theorem 11, identities (12)–(15), I = ∪_even J_a, J = ∪_odd J_a | `theorem11` | (12) and (13) are asserted on every call |
| §3.3: G^ℓ vectors give 2^ℓ disjoint representations | `_accumulate` | |
| Fact 2 (z_1^d + … + z_{d+1}^d = 0) | `zero_sum_of_powers`, `selective_root` | vdW §6.1 on −1, §6.2 for odd d |

## 3. Why every step is deterministic and polynomial for fixed d [proved]

Let a be the rank and κ = gcd(d, p−1) ≥ 2.

- **Pohlig–Hellman in ⟨η⟩.** ord η divides |H_π|, all of whose prime factors divide κ. Each
  ℓ-adic digit is found by a table of ℓ ≤ κ powers. That costs O(κ log p) exponentiations
  per logarithm.
- **Generator of ⟨η, γ⟩ in the cyclic group H_π.** For each ℓ | κ, keep the ℓ-component of
  larger order. Orders cost O(log p) exponentiations each. Each restart strictly enlarges
  ⟨η⟩ inside H_π, so restarts ≤ Ω(|H_π|) ≤ log₂ p. Tested: `_check` asserts this on every
  run, and the exhaustive classifier test reaches ⟨η⟩ = H_π.
- **Lemma 12 and Theorem 11.** These take G/(m+1) kernel computations, of dimension at most
  κ^{κ−1}a, plus one classification per kernel coefficient.
- **§3.3.** This makes Σ_{j<L} G^j calls of Theorem 11 on G·a-sized inputs, L ≤ ⌈log₂(κ+1)⌉.
- **Zero sum.** −1 = (p−1)·1^κ is kept as runs (multiplicity, y), as van de Woestijne
  prescribes ("we still remember the coefficients"). Each round splits the M terms into
  κ+1 nearly equal blocks and drops at least one block. So M falls by a factor of at least
  κ/(κ+1), and there are O(κ log p) rounds of one Selective Root Extraction each.
  Selective Root Extraction itself costs κ+1 splits, one generator and κ+1 logarithms.
- **Selective Root Extraction is correct.** Write γ_i = η^{e_i}. Some i < j has
  e_i ≡ e_j (mod κ), by pigeonhole on κ+1 values. Then
  a_i/a_j = (η^{(e_i−e_j)/κ})^κ · (γ′_i/γ′_j), and the last factor has the explicit κ-th
  root γ′^r. More generally, take logarithms mod g = gcd(κ, ord η). If e_i ≡ e_j (mod g),
  then η^{e_i−e_j} = (η^x)^κ with x = ((e_i−e_j)/g)·(κ/g)^{−1} mod (ord η)/g. ∎

Total: poly(a, log p) field operations for fixed κ, with no randomness. The κ-dependence is
the paper's: G(κ, a)^L columns, each touched a constant number of times. The algorithm
never enumerates the field.

## 4. Deviations from the papers, each sound

(a) **Rescaling without reclassifying** (`_classified_kernel`). IS say "we can arrange that
J_1 (M_{ℓ+1}) is nonempty by multiplying the coefficients simultaneously by ζ_1/ζ_r
(ζ_{ℓ+1}/ζ_r)". A naive implementation would reclassify the rescaled coefficients
canonically, with log ∈ [0, ord η). That fails when ord η < d: for example η = −1 with d = 4
gives canonical classes only {0, 1}, so class ℓ = 3 can never appear. The implementation
keeps each known form ζ_{r′}β^d instead. It rewrites ζ_{r′}·ζ_{target}/ζ_r =
η^{r′+target−r} as ζ_s·(η^q)^d with r′+target−r = dq+s. This is the reading under which
the paper's sentence is true. **[proved]** An assertion checks the identity on every
coefficient.

(b) **Kernel vector.** The paper allows any nonzero kernel vector. The default
(`spread=False`) is the basis vector of the first free column. `spread=True` sums the whole
kernel basis. Both are deterministic. The default makes Theorem 11 end with J = ∅ most of
the time (§6), so the tests run both.

(c) **Fewer levels.** §3.3 iterates ⌈log₂(d+1)⌉ times. The code iterates L = ⌈log₂ t⌉ times,
where t is the length of the zero sum it actually computed, before consuming any column.
Any t ≤ 2^L works in the final step. So the count used is at most the paper's
**[proved]**.

(d) **`shorten` (our addition).** After the §6.1 reduction reaches at most κ terms, the
code keeps reducing while Selective Root Extraction still certifies a collision among the
remaining prefix sums. A dropped prefix sum of zero is also allowed. This is the same
operation on fewer than κ+1 values, so it is sound, but it is not in the note. It lowers t
often: at κ = 4 over primes below 20000, t = 2 occurs for 387 of 1125 primes with it and 8
without it (`zero_sum_lengths.out`) **[exact]**. With `shorten=False` the output is the
plain §6.1 result, t ≤ κ+1, and it is tested too.

(e) **Preprocessing.** Columns are rewritten in a basis of their row space. This is an
equivalent system, and it makes the arity depend on the rank a, as in main.tex. A zero
column returns the unit vector at once.

(f) **Odd κ.** The finish uses 1^κ + (−1)^κ = 0, so t = 2 and L = 1. Both IS ("this part
already does the job when … d is odd") and van de Woestijne §6.2 state this.

(g) **`early_exit=False` (diagnostic).** IS stop as soon as an intermediate common vector is
zero. That is the sentence "we are done if this is the zero vector", and J = ∅ is one case
of it. The diagnostic mode does not stop. It carries u = 0 forward, so some J-side
representations may be empty. They still sum to u = 0, and reps[0] stays nonempty because
I ≠ ∅ at every level. So the witness is still nonzero and correct **[proved]**. This mode
exists only so the tests reach the full §3.3 and Fact 2 path (§6).

## 5. Tests (all exact F_p arithmetic) [exact]

- **Arity formulas.** B_2 = 4(a+1)⁴, B_3 = 729(a+1)⁶, B_4 = 4096³(a+1)¹². The test checks
  G and B for d ≤ 9, a ≤ 12. **Chevalley–Warning** is checked at every count:
  B_d(a) > da and G(d, a) > da. For 16 primes and d ≤ 9, a ≤ 3:
  κa < `columns_required` ≤ B_κ(a) ≤ B_d(a).
- **Bezout exponent.** For d ≤ 12 and 16 primes, x^{td} = x^κ, exhaustively for p < 300.
- **§3.1 classifier, exhaustive.** Every α ∈ F_p^* is written as ζ_r β^d, restarting until
  ⟨η⟩ = H_π. This runs for p ∈ {5, …, 257}, d ∈ {2, 3, 4, 6, 8}, with restarts ≤ Ω(|H_π|).
- **Zero sums.** Every prime p < 400 and every κ | p−1 with κ ≤ 12, in both modes:
  2 ≤ t ≤ κ+1, all terms nonzero, the sum is zero, and the output is deterministic. t ≥ 3
  whenever −1 is not a κ-th power, and t = p when κ = p−1.
- **Selective Root Extraction.** 20 random (d+1)-tuples each, for d ∈ {2, 3, 4, 8} and six
  primes including two 30-bit ones.
- **Theorem 11 directly.** Seven (p, d, m), including d = 4 at p = 13 and at
  p = 536871001, in both kernel modes. Supports are disjoint, I ≠ ∅, γ ≠ 0, and both sides
  equal w exactly.
- **Random columns at full arity B_κ(g).** 19 cases with p ∈ {3, 5, 7, 13, 41} and five
  30-bit primes, d ∈ {2, 3, 4, 6, 8, 9}, g ≤ 3, and up to 531441 columns. Both kernel
  modes; the output is deterministic.
- **Adversarial.** Repeated basis vectors e_{i mod g}. A single column repeated B times
  (rank 1). Rank-g columns embedded in F_p^{g+3}. Seven (p, d, g), in both modes.
- **Quartic end to end.** κ = 4 at p = 17, 41, 97, 536871001 (t = 2), on 65536 columns:
  one Theorem 11 call and L = 1.
- **Full path without early exits.** Eight cases, including L = 2 with t = 3
  (κ = 2, −1 a nonsquare: p = 3, 7, 536870951, 536871017) and L = 1 at κ = 3, 4.
  The number of Theorem 11 calls is exactly Σ_{j<L} G^j.
- **Zero-sum family of thm:power-sde (iii).** At p = 5, d = 4, the columns e_1×4, e_2×4 have
  no nonempty zero-sum subset (exhaustive), and adding (1, 1) creates one. The same
  κ = p−1 sharpness holds at (p, κ, g) = (3, 2, 3), (7, 6, 1), (5, 4, 1), (13, 12, 1).
  Chevalley–Warning at κa+1 columns is checked exhaustively on 30 random tuples. The
  solver refuses that 9-column instance: it needs G(4, 2)³ = 3.65·10¹⁶ columns, since
  t = 5 at p = 5. The analogous κ = p−1 family at p = 3, d = 2 runs at full arity B_2(g)
  for g = 1, 2, 3.
- **Linear case and refusals.** κ = 1 at a+1 columns. `ValueError` below the required count,
  for a composite modulus, and for a zero input to `selective_root`.
- **Added after review.** `shorten=False` end to end, with `columns_required(…, shorten=…)`
  matching it. Degrees d = p, d = c(p−1) and d > p−1 (for example p = 3 with d = 4 or 100,
  and p = 13 with d = 39). Restart count exactly Ω(|H_π|) when elements arrive in order of
  increasing π-part order. Zero-column metadata. `selective_root` with fewer than d+1
  values, which may correctly return None.

## 6. Which exit the runs take (`path_stats.out`, 126 runs) [exact]

| κ | L | t | kernel mode | ended by early zero | reached the Fact 2 finish |
|---|---|---|---|---|---|
| 2 | 1 | 2 | pivot / spread | 6 / 2 | 3 / 7 |
| 2 | 2 | 3 | pivot / spread | 21 / 21 | 0 / 0 |
| 3 | 1 | 2 | pivot / spread | 20 / 0 | 1 / 21 |
| 4 | 1 | 2 | pivot / spread | 12 / 1 | 0 / 11 |

Every run returned a verified witness. At L = 2, one of the G level-1 collisions almost
always has J = ∅, a zero common vector. So on random columns, the two-level accumulation
never reaches the final Fact 2 combination. This is why the `early_exit=False` test exists.
**[argued]**: this is a typical-case effect of the deterministic kernel choice and of G
being large. It is not a worst-case statement.

## 7. Exact statement that now holds

For every odd prime p, every integer d ≥ 1, and every list of M columns in F_p^g of rank a:
if M ≥ `columns_required(p, d, a)` = G(κ, a)^{⌈log₂ t(p,κ)⌉} ≤ B_κ(a) ≤ B_d(a), then
`is_sde_solve` deterministically returns s ∈ F_p^M, s ≠ 0, with Σ_i s_i^d λ_i = 0, verified
exactly on the original columns. Here κ = gcd(d, p−1), and t(p, κ) ≤ κ+1 is computed in
poly(κ, log p) time. Access model: the columns are explicit public data. No randomness or
nonresidue is used, and no field element is enumerated. Charged cost: poly(a, log p) field
operations for fixed κ, including at most log₂ p whole-run restarts. **[proved]**
correctness, with the implementation checked **[exact]** on the executed range of §0.4.
Not claimed: any running-time bound measured in practice beyond these tests, any κ ≥ 4
instance with t ≥ 3 actually run, or any quantum or end-to-end statement.

## 8. What is missing, and what would justify `general_sde_implemented = true`

Missing:
1. An independent human review of this module against IS §3. The AI review is in §9.
2. Van de Woestijne's own Selective Root Extraction is replaced by the equivalent in §0.3.
   His §6.2 linear-time variant is not implemented (only its odd-n case). Neither change
   affects correctness or polynomiality.
3. κ = 4 with t ≥ 3, and κ ≥ 5, are not executable. This is the paper's arity
   (≥ 4.3·10⁹ columns), not a code limit.
4. Nothing calls the solver yet. The end-to-end simulator (item 10) does not use it, and
   `theorems/rees_hsp_reduction.py:387` hard-codes the flag.

Recommended evidence before flipping, all four together:
(i) an independent review that accepts §§2–4;
(ii) the reduction or simulator calling `is_sde_solve` at every grade with κ_d and checking
the returned witness;
(iii) one end-to-end run on a small group where some grade has κ ≥ 2 and Schedule 1
actually supplies the witness;
(iv) a flag that says what was executed. I recommend a new flag such as
`schedule1_solver_implemented: true` with `schedule1_executed_reduced_degrees: [1, 2, 3, "4 (t=2)"]`,
rather than flipping the word "general". The solver is general in code but not in what was
run.

## 9. Independent code review

One general-purpose helper read IS §3 and the ISSAC note and reviewed the code against
them. It was given the code, not this report. It ran about 7,300 randomized solves plus
targeted edge cases:
- p = 3, 5, 7, 13, 17, 7681, 65537, 3·2³⁰+1, 2⁶¹−1 and 29·2⁵⁷+1;
- repeated, parallel, ± and zero columns, and ranks 1–3 inside g = 40;
- d > p−1, d = p, and d a multiple of p−1;
- an input built to force restarts (at most 4 seen).

**No correctness bug was found.** Every returned witness verified, and nothing crashed or
looped. It accepted (a)–(c) and (f) of §4 as faithful: the classification, the rescaling
(which it agrees is necessary when ord η < d), Lemma 12, Theorem 11 indexing and sign
identity, and the disjoint-support bookkeeping. It accepted `selective_root` as a valid
deterministic polynomial-time realization of vdW Theorem 5.1 on F_p, not vdW's own
algorithm. Its findings, all fixed:

1. `columns_required` always used `shorten=True` while `is_sde_solve(shorten=False)` used
   the longer zero sum. Smallest case: p = 73, d = 2, a = 1, where the count was 8 but the
   solver needed 64. `columns_required` now takes `shorten`, and a test covers both modes.
2. `selective_root` crashed on a zero input. It now raises `ValueError`.
3. The zero-column exit reported rank 0. It now reports the true rank.
4. Two dead branches were removed: a zero child in `_accumulate`, and the rank-0 branch.
5. Collisions were compared mod d rather than mod gcd(d, ord η), which missed some
   certified collisions, but only in `shorten`. Now mod gcd (§3).

It also confirmed what is not implemented: vdW's coefficient-size trick (O(log log q)
rounds) and the §6.2 roots-of-unity exit beyond odd d. These are optional speedups, and the
loop is O(d log p) rounds without them. Its test-gap list (no `shorten=False` solve, no
assertion of the L = 2 full path, no lower bound on restarts, no `selective_root` edge
cases, degenerate degrees) is addressed in §5. One residual point: primality of p is
checked with python-flint's `is_prime`. That is an input check, not part of the solver.

## 10. Claim gates that must stay false

`general_sde_implemented`, `coherent_receiver_implemented`, `independent_review`,
`formal_compiler_checked` (`research/reductions/rees_hsp_reduction.json`), and every Rees
novelty, priority or receiver-execution gate. This pass adds a classical solver only.

## 11. Text fixes for main.tex (listed, not applied)

1. main.tex:420, after "its last step uses van de Woestijne's deterministic solver for one
   equation in $d+1$ variables": add "(over $\Fp$ this is $z_1^d+\dots+z_{d+1}^d=0$,
   obtained by writing $-1$ as a sum of at most $d$ $d$-th powers, van de Woestijne,
   ISSAC 2005, Section 6)". The present wording is right but does not say which equation.
2. main.tex:420: add one sentence on the implementation and its executed range, for
   example: "A deterministic implementation (\file{theorems/rees_is_sde_solver.py})
   returns verified witnesses at $\kappa_d \le 3$ at full arity, and at $\kappa_d = 4$
   when the computed zero sum has two terms. Larger $\kappa_d$ exceed $10^9$ columns
   already at $a=1$."
3. Optional, main.tex:420: the deterministic run needs only
   $G(\kappa_d,a)^{\lceil\log_2 t\rceil}$ columns, where $t \le \kappa_d+1$ is the length of
   the computed zero sum. So (eq:is-arity) with $\kappa_d$ in place of $d$ also suffices. The
   paper's choice of $B_d(g_d)$ is valid and needs no change.
4. thm:power-sde (iii): the example is an existence statement. It may help to note that
   Schedule 1 needs $G(4,2)^3 \approx 3.7\cdot10^{16}$ columns there, so the small-$p$
   regime is a finding-cost problem, consistent with
   `2026-11-02-rees-small-prime-arity.md`.
