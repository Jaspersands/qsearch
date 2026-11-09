# Rees Schedule 1: from field operations to multitape Turing-machine steps

4 November 2026. AI-only pass (one session). No human review. Labels: **[proved]** (argument
written here, at proof-sketch level), **[source]** (cited, not re-proved), **[exact]**
(complete finite computation). No `.tex`, `.bib` or code was edited. Nothing was committed. No
network was used.

Target: `docs/papers/rees-hsp/main.tex`, Remark `rem:is-runtime`, the sentence "Granting that a
multitape Turing machine runs this level-by-level computation with constant-factor overhead (a
standard layout argument that is not written out here) ...", and its use in Proposition
`prop:coherent-receiver`. This note closes the step left **[argued]** in
`2026-11-04-rees-is-runtime.md` §5. The field-operation count of that note (§3, equation (F)
and the simple form 40κ³Nb(a²+b²)) is taken as given.

## 0. Answer

- **Closure (A), proved at proof-sketch level.** There is one fixed multitape Turing machine 𝓜.
  Its number of tapes, its alphabet and its finite control are independent of p, d and the input.
  𝓜 reads d, p, g_d, M_d and the columns, and it outputs the Schedule 1 witness within
  **T^IS_d = C₁ d³ M_d b³ (g_d² + b²)** steps, for an **absolute** constant C₁. The displayed
  bound of the remark is therefore **unchanged**.
  - The machine 𝓜_d of `prop:coherent-receiver` is 𝓜 with d fixed in its finite control (it
    writes d on a work tape in its first O(log d) steps). Its finite control depends only on d,
    as G1 requires.
  - Per field operation, the overhead is not constant uniformly in κ. Several passes move the
    heads by up to poly(κ) cells per operation (§5). Every such term is absorbed by the κ³
    already in the bound, with an absolute constant.
- **One clause of the remark must change.** "O(M_d b²(g_d²+b)) when ν is bounded" does not
  follow. The zero-sum step costs Θ_κ(b²) field operations even when ν = O(1), which is O(b⁴)
  TM steps. That term is independent of M_d, so it is not covered by M_d b³ once b > M_d. The
  correct statement is **O(M_d b²(g_d²+b) + b⁴)**. The same correction applies to the refined
  form in `2026-11-04-rees-is-runtime.md` §0 item 2 and §6: add (ν+1)b⁴ there.
- **Closure (B), fallback.** It uses a cited RAM-to-TM simulation with cubic overhead
  (Papadimitriou, Section 2.6) and gives T^IS_d = C_B d⁹ M_d³ b⁶ (g_d²+b²)³. It is not needed
  if (A) is accepted (§8).
- **G1 consistency.** The remark should say "one fixed machine". With that, its wording matches
  `prop:coherent-receiver`. The machine may return a different valid witness than the Python
  reference, because the order of evaluation differs (§6). The proposition only uses that F_d is
  a fixed deterministic map to nonzero solutions, so this is harmless (§7).

## 1. Model and conventions

- **Machine.** A deterministic multitape TM with k work tapes, k fixed (about 22 below; the
  number does not matter). The input is on a read-only tape and the output on its own tape.
- **Alphabet.** Σ = {0, 1, □, #, $, %, \*, ⊥}, the same for all p, d and inputs.
  - Field elements and integers below 2^b are fixed-width binary fields of b cells.
  - `#`, `$` and `%` separate entries, vectors and records.
  - `*` is a marker, and `⊥` means "no class / not in any set".
- **Notation.** As in the earlier note: κ = κ_d, a = g_d ≥ 1 (if g_d = 0, output e₁),
  b = ⌈log₂ p⌉, β_κ = bitlen κ, ω = number of distinct primes of κ, and ν ≤ b−1.
  - G = κ^{κ(κ−1)/2}(a+1)^κ, ℓ_z ≤ κ+1 the zero-sum length, L = ⌈log₂ ℓ_z⌉ ≤ β_κ, N = G^L ≤ M_d.
  - R_ℓ = κ^{ℓ−1}a, E_ℓ = κ^{ℓ−1}(a+1), B_ℓ = κ^{ℓ(ℓ−1)/2}(a+1)^ℓ (B₀ = 1, B_κ = G).
  - A Theorem 11 call has G/B_ℓ nodes at Lemma 12 level ℓ. A run has I = Σ_{j≤L} G^{L−j+1}
    ≤ (8/7)N call inputs in all.
- **Variant computed.** The machine runs the algorithm counted in the remark: a = g_d with no
  optional row reduction, the §3.1 classifier with whole-run restarts, Lemma 12, Theorem 11,
  the §3.3 accumulation with the early-exit test, the zero sum of the reference variant, and the
  Bezout step. The finite verification asserts of the Python code are omitted.
- **"Steps" and "movement".** Every step either does arithmetic or moves a head. Arithmetic
  steps are charged to the counted field operations (§2). Every other step is head movement,
  tallied pass by pass (§4–§5). All constants c, c′, ... below are absolute.

## 2. Arithmetic primitives [proved]

Each primitive works on dedicated arithmetic tapes A1–A4. The modulus p sits alone on tape P,
and exponents are on tape X_e. Operands are copied in and out at O(b) steps each, so a primitive
never moves a head anywhere else.

- **Addition and subtraction mod p.** Add with aligned heads, then compare with p and subtract
  conditionally: O(b).
- **Multiplication mod p (schoolbook).** For each bit of y, add x into the accumulator at the
  current offset; the offset is the relative head position. This is O(b) per bit, so O(b²) for
  the 2b-bit product. Reduction is long division by p: for each of b+1 shifts, compare and
  subtract with aligned heads, O(b) each. Total O(b²).
- **Inversion mod p.** Use binary extended Euclid on (u, v, x₁, x₂) = (x, p, 1, 0). While u is
  even, halve u and halve x₁ mod p (add p first if x₁ is odd); likewise for v. Then subtract the
  smaller of u, v from the larger, with the same update on x₁, x₂.
  - Each halving lowers bitlen(u) + bitlen(v), so there are at most 2b halvings and at most 2b
    subtractions.
  - Each iteration is O(b) sequential steps, so the total is O(b²).
- **Exponentiation x^e.** Left-to-right square-and-multiply, reading e on X_e from the top bit.
  It uses at most 2·bitlen(e) multiplications, the charge used in (F). A negative e adds one
  inversion.
- **Integers below 2^{b+1}.** These are exponents and orders, n_π, e_π, e_π′, t, Pohlig–Hellman
  x and scale, and zero-sum multiplicities. Addition, comparison, multiplication and division
  with remainder use the same routines without reduction, O(b²) each. Division by an integer
  below 2^{β_κ} is O(b β_κ).

So each counted field multiplication or inversion costs at most c_a b² steps, and each addition
at most c_a b. The earlier note's operation count therefore contributes at most

  c_a b² · F + c_a b · 2F ≤ 2c_a b² F ≤ 80 c_a κ³ N b³ (a² + b²)  steps.  (Ar)

## 3. Tape layout

| Tape | Content |
|---|---|
| IN | d, p, g_d, M_d, then M_d columns of g_d entries (read-only) |
| OUT | s₁, …, s_{M_d} |
| P | p |
| K | constants: κ, t, n_π, e_π, e_π′, the root exponent, the primes of κ with their powers in n_π, η, η⁻¹, the z_j (≤ κ+1), and G, N, B_ℓ, E_ℓ, R_ℓ in binary |
| A1–A4, X_e | arithmetic scratch, exponent register |
| V₀, V₁ | the current and the next level's records (the roles alternate) |
| X, C, RM | elimination matrix (by columns), multiplier column, row markers |
| Kv | kernel vector, then the classified pairs (r_e or ⊥, β_e) |
| W | κ^ℓ accumulator slots of a·b cells |
| S | classification stream: one record (r or ⊥, γ) per child, in tape order |
| Tg | one record per call input: tag in [κ]^{≤κ} or ⊥ (κ fields of β_κ cells), and β (b cells) |
| Ix | one record per column i < N: representation index (L cells) or ⊥, and coefficient c_i (b cells) |
| CT | block counters (binary, ≤ log₂N + 1 cells), a base-κ key counter |
| Zr, Zb | zero-sum runs (multiplicity, value), and blocks |
| TB | lookup table: Pohlig–Hellman digits, or the selective-root collision table (≤ κ+1 entries) |

**The structural fact behind all of this.** Every operation of the algorithm reads its data in
the order in which it was written. The reasons are:

- **(S1)** At Lemma 12 level ℓ, the children of a node are E_ℓ consecutive level-(ℓ−1)
  records. The level-ℓ nodes of all calls at one accumulation level are consecutive.
- **(S2)** A level-(ℓ−1) record lists its κ^{ℓ−1} vectors in lexicographic key order; this is
  the order `lemma12` concatenates them in. So the E_ℓ consecutive child records are exactly the
  node's R_ℓ × E_ℓ matrix, stored by columns.
- **(S3)** The call inputs below a level-ℓ node form a block of B_ℓ consecutive Tg records. The
  columns below the k-th input of a call at accumulation level j form a block of G^{j−1}
  consecutive Ix records.
- **(S4)** Every table the algorithm consults has at most κ+1 entries.

## 4. The passes [proved]

### 4.1 Setup (once)

1. Scan IN once: copy p to P and test every column for zero, O(M_d g_d b). If some column i is
   zero, write e_i and halt.
2. Compute κ = gcd(d, p−1): (p−1) mod d costs O(b β_d), then a gcd of small integers. Compute t
   by extended Euclid modulo (p−1)/κ, O(b²).
3. Factor κ by trial division, O(κ β_κ²).
4. Compute n_π and the rest by at most ν+ω divisions by primes of κ, O((ν+ω) b β_κ).
5. Compute e_π, e_π′, the root exponent and the prime powers. This is O(ω) inversions and
   products of integers below p, O((ω+1) b²).
6. Compute G, N, B_ℓ, E_ℓ, R_ℓ by repeated multiplication of integers of at most log₂N + 1 bits,
   poly(κ, log N). This needs ℓ_z, so it comes after §4.2.

The total is O((ν+ω+1) b² β_κ + poly(κ, log N)), well inside the target bound.

### 4.2 Zero sum (once; depends only on p and κ)

- **Runs.** The runs (k, y) are written consecutively on Zr. The split into κ+1 near-equal
  blocks (`_blocks`) is one left-to-right pass. It keeps the current run's remainder and the
  remaining block size (`need`) on scratch, at O(b) per run per round.
- **Block values.** Each block value Σ k·y^κ and each prefix sum is computed in the same pass.
- **Selective root extraction.** Each round runs it on ≤ κ+1 values, using the
  classification routine (§4.3, step 4). The collision table ("seen", keyed by e mod g with
  g ≤ κ) is on TB and is scanned linearly, O(κ(b+β_κ)) per lookup.
- **New runs.** The new run list is a sequential copy of blocks [0..i], scaled by β⁻¹, followed
  by blocks [j+1..κ]. Block indices are counted on CT.
- **Cost.** At most R_z ≤ ⌈(κ+1) b ln 2⌉ + κ + 2 rounds, with at most 1 + κR_z runs each. The
  movement is therefore O(R_z((1+κR_z) b + (κ+1) νκ(b+β_κ))) = O(κ⁴ b³ β_κ). The arithmetic is
  at most c_a b² Z.
- **Finish.** The ≤ κ+1 values z_j are written to K.

### 4.3 One run (classifier η fixed); accumulation levels j = 1, …, L

Write the run's columns, the first N columns of IN, to V₀: O(N a b). Initialise Ix to
(rep = empty, c = 1) for every i < N. For each accumulation level j, process all G^{L−j} calls
of that level together, Lemma 12 level by level.

**Level ℓ = 1, …, κ (one left-to-right pass over V_in, writing V_out).** For each node, in tape
order:

1. **Copy.** Copy the next E_ℓ records from V_in to X; this is the matrix by columns (S2). Cost
   O(R_ℓ E_ℓ b). CT counts E_ℓ records.
2. **Gauss–Jordan with row swaps, as in `_kernel_vector`.** RM carries one cell per row, with
   marks for the current row r and the pivot row.
   - For each column col: scan it for a pivot in a row ≥ r, O(R_ℓ b).
   - If there is a pivot: copy the column to C, invert the pivot, and make **one pass over all
     E_ℓ columns**. For each column, fetch its row-r and pivot-row entries through RM, swap them,
     normalise row r, rewind, then stream rows i ≠ r and update A[i][e] −= c_i·A[r][e] with c_i
     read from C in step. The head movement is O(R_ℓ b) per column, so O(R_ℓ E_ℓ b) per pivot,
     against R_ℓ E_ℓ multiplications of Θ(b²) steps each.
   - With at most R_ℓ pivots, the movement is O(R_ℓ² E_ℓ b), a factor 1/b below the arithmetic
     R_ℓ² E_ℓ b² that (F) charges.
   - The pivots occupy rows 0, 1, 2, … in column order, so the kernel vector (1 at the first
     free column, −A[i][free] at the i-th pivot column) is read off in one sequential pass of
     O(R_ℓ E_ℓ b) onto Kv.
3. **Row-major storage would cost the same.** A row-major layout costs the same O(R E b) per
   pivot. Either way the movement is dominated because the TM performs every row operation of a
   pivot, including those with zero multiplier. The comparison is with the counted bound
   R²E + R, not with the possibly smaller measured count.
4. **Classify and shift.** One pass over Kv classifies each nonzero α_e (`Classifier.classify`):
   split by two pows; Pohlig–Hellman in ⟨η⟩; the κ-th root in H_π′; the factor η^f.
   - Pohlig–Hellman: for each prime ℓ′ | κ, build the ≤ ℓ′-entry digit table (base^j, j) on TB.
     Then each of the ≤ ν digits costs two pows, one multiplication, one inversion, one linear
     scan of TB (O(κ(b+β_κ))) and O(1) integer operations on x, scale and power (O(b²)). The CRT
     costs ω+1 integer inversions.
   - Movement per classification: O(νκ(b+β_κ) + (ν+ω+1) b²).
   - A second pass applies the class shift. q = ⌊(r_e + target − r₀)/κ⌋ ∈ {−1, 0, 1}, so each
     entry needs one multiplication by η^{±1} from K, plus one ζ-power per node.
   - If a π-part escapes ⟨η⟩, the run aborts (§4.4).
5. **New vectors.** For each child e with class r_e ≠ ⊥, compute γ_e^κ. Then stream the child's
   κ^{ℓ−1} blocks from V_in (rewound over this node's E_ℓ records) and add γ_e^κ·block into slot
   (key, r_e) of W. The slots are in lexicographic order (key, r), so this is **one sweep of W
   per child**, O(κ^ℓ a b) cells.
   - Copy W to V_out as the node's record and clear W, O(κ^ℓ a b).
   - Append (r_e or ⊥, γ_e) for each child to S.
   - Per node: movement O((E_ℓ + 2) κ^ℓ a b) against E_ℓ R_ℓ + 2β_κ E_ℓ multiplications. This
     is the one place where the movement per multiplication is Θ(κ) rather than O(1/b).

**Tag pass (after level ℓ).** Merge S into Tg (S3). For each S record, a CT counter of B_{ℓ−1}
(reset in O(log N)) runs over the next B_{ℓ−1} Tg records.

- Each Tg record gets r appended to its tag (⊥ stays ⊥, and the record becomes ⊥ if r = ⊥) and
  β ← γβ (one counted multiplication).
- Movement per level: O(G^{L−j+1}(κβ_κ + b) + (G^{L−j+1}/B_{ℓ−1})(β_κ + b + log N)).
- At ℓ = 1 the tags start empty with β = 1. S is erased after the pass.

**Sign step (after level κ; one pass per call).**

- **Common vector.** The level-κ record of a call has κ^κ slots. Enumerate their keys with the
  base-κ counter on CT. For each key, decide whether it is a permutation and find its parity by
  pairwise comparison on a copy, O(κ² β_κ). Add the even slots: w = Σ_{a even} w_a. Write w to
  the next accumulation level's V₀ (in order, S1).
- **Early exit.** If w = 0 and this is the first such call in tape order, mark it for early exit.
- **Side stream.** Make one pass over the call's G Tg records. Each record gets side I (even
  permutation tag), side J (odd) or ⊥, and γ_k = β_k, written to a side stream S′.
- Movement per call: O(κ^κ(κ² β_κ + a b) + G κ² β_κ).

**Accumulation pass.** Merge S′ into Ix with block size G^{j−1} (S3).

- The representation index gets the side bit prepended (side·2^{j−1} + rep), or becomes ⊥.
- c_i ← γ_k c_i (one counted multiplication of the (L+1)N term).
- Movement per level: O(N(L + b) + G^{L−j+1} log N).
- **Early exit.** If a call was marked, make one pass that keeps exactly the columns of that
  call's block with side I and child representation 0 (`children[k][1][0]`). Zero every other
  column, then go to §4.5.

### 4.4 Restarts

- **Abort.** A classification whose π-part γ escapes ⟨η⟩ aborts the run.
- **Erase.** Every work tape except IN, P, K, Zr and OUT is erased. The cost is at most the
  number of cells written during the run, so at most the steps of the aborted run.
- **Join.** η ← join(η, γ) costs O(ω(ν+ω)) pows, O(ω(ν+ω) b³) steps. Then the run restarts
  from §4.3.
- **Bound.** ⟨η⟩ strictly grows in the cyclic group H_π of order n_π, so there are at most ν
  restarts and at most ν+1 runs, whatever the evaluation order.

### 4.5 Finish and output

- One pass over Ix. For a representation index ρ < ℓ_z, the coefficient becomes c_i z_ρ, with
  z_ρ found by a linear scan of K, O(κ b). For ρ ≥ ℓ_z or ⊥ it becomes 0; this is `zip(z, reps)`.
- Then s_i = u_i^t for u_i ≠ 0 (≤ 2b multiplications each, the Bezout term 2bN).
- Write s_0, …, s_{N−1} to OUT, then M_d − N zeros. Movement O(N(κ b + L) + M_d b).

## 5. Tally [proved]

All lines are head movement only. The arithmetic is (Ar). Per call input of one run, using
Σ_ℓ 1/B_{ℓ−1} ≤ 2 and the closed forms below:

| Pass | Movement per call input | Bound used |
|---|---|---|
| copy to X | b Σ_ℓ R_ℓE_ℓ/B_ℓ ≤ b(a + 2κ) | (i) |
| elimination | b Σ_ℓ (R_ℓ²E_ℓ + R_ℓ)/B_ℓ = bΛ ≤ b(a² + κ²a + 2κ³ + 2) | earlier note §3 |
| classification | Θ·[νκ(b+β_κ) + (ν+ω+1)b²] ≤ 1.65(κ²b² + (b+κ)b²) | Θ ≤ 1.65, ν < b, β_κ ≤ κ |
| new vectors | b Σ_ℓ (E_ℓ+2)κ^ℓ a/B_ℓ ≤ b(κa + 3κ²) | (ii) |
| tags | κ(κβ_κ + b) + 2(β_κ + b + log₂N) | (iii) |
| sign step | κ^κ(κ²β_κ + ab)/G + κ²β_κ ≤ 3κ²β_κ + b | κ^κ/G ≤ 2/(a+1)² |

Per column of the run (accumulation and finish): L(L + b) + (8/7)(b + log₂N) + κb.

Closed forms:

- **(i)** R_ℓE_ℓ/B_ℓ = aκ^{2ℓ−2−ℓ(ℓ−1)/2}/(a+1)^{ℓ−1}. Its terms are a, then ≤ κ, ≤ κ/4,
  ≤ 1/8, and then ≤ 1/16 in total.
- **(ii)** E_ℓκ^ℓa/B_ℓ = aκ^{2ℓ−1−ℓ(ℓ−1)/2}/(a+1)^{ℓ−1}. Its terms are aκ, then ≤ κ², ≤ κ²/4,
  ≤ κ/8, …. The extra 2κ^ℓa/B_ℓ sums to ≤ 3κ.
- **(iii)** log₂N = L log₂G ≤ β_κ(κ²β_κ/2 + κ log₂(a+1)) ≤ 2κ³ + κ²a, using β_κ² ≤ 4κ,
  β_κ ≤ κ and log₂(a+1) ≤ a.

Every entry is at most c κ³ b²(a² + b²), with a, κ ≥ 1, b ≥ 2 and ν < b. Multiply by
I ≤ (8/7)N per run and by at most ν+1 ≤ b runs, and add the other terms: (Ar); the restarts
(erasing ≤ the run, joins O(νω(ν+ω)b³)); the zero sum (O(κ⁴b³β_κ) movement plus c_a b²Z
arithmetic, with Z ≤ 18.3κ³Nb³ from the earlier note); setup; and input/output O(M_d(g_d+1)b).
Then, with κ ≤ d and N ≤ M_d:

  **T(𝓜, input) ≤ C κ³ N b³ (a² + b²) + C M_d (g_d+1) b ≤ C₁ d³ M_d b³ (g_d² + b²),**

with C and C₁ absolute. The machine is the same for all d, so neither the size of its finite
control nor its tape count depends on d.

**Where the overhead is larger than a constant per operation.** Honest list:

- **Elimination.** Movement per pivot is O(R E b), against R E multiplications. This is a factor
  O(1/b), so it is not a problem.
- **New vectors.** Θ(κ) cells per multiplication (the W sweep). It is absorbed by κ³.
- **Pohlig–Hellman and collision lookups.** O(κ(b+β_κ)) per digit, against O(b³) arithmetic per
  digit. That is up to a factor κ/b², absorbed.
- **Tags, the sign step and counters.** κ²β_κ, κ^{κ+2}β_κ per call and log N per block. None of
  these has a matching field operation. All are bounded by poly(κ)·(a+b) per call input, and
  absorbed.
- **Restarts.** Erasing doubles the cost of an aborted run at most.

So "constant-factor overhead" in the remark's current wording is literally false uniformly in κ.
The bound it was meant to deliver holds anyway.

**Numerical sanity check [exact].** The scratch script
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/tm_tally.py`
evaluates the movement tally of §4.3 per run, with unit constants and exact integers, divided by
κ³ N b² (a² + b²). The grid is κ ≤ 12, a ∈ {1,…,1000} (8 values), ℓ_z ∈ {2, κ+1},
b ∈ {2,3,8,32,128} and ν ∈ {0,1,b−1}. The maximum is 0.90, at κ = 2, a = 1, b = 2. This checks
the closed forms above, not the TM construction.

## 6. Evaluation order and the function computed

- **Order.** The reference code evaluates the Lemma 12 tree and the §3.3 accumulation
  depth-first. 𝓜 evaluates level by level. Nodes depend on each other only through η and their
  children's records, so every order gives a correct witness. The bound of ν+1 runs holds in
  every order (§4.4).
- **Consequence.** The first restarting classification, and the first call with w = 0, can
  differ between the two orders. So F_d := (output of 𝓜_d) is a witness of Schedule 1 at
  arity M_d, but it need not coincide with `is_sde_solve` on every input. It also differs
  because 𝓜 uses a = g_d without `_row_reduce`.
- **Matching the reference instead.** A post-order evaluation would do so at the same cost. Keep
  a stack tape of finished records: the E_ℓ children of the next node are then the top E_ℓ
  records, again contiguous, and the tag update touches the last B_ℓ Tg records. This is not
  needed.

## 7. G1 wording, C₁ and the clock

- **G1.** `prop:coherent-receiver` asks for "a fixed multitape Turing machine 𝓜_d, whose finite
  control depends only on d and κ_d and which reads p, g_d, M_d and the columns". 𝓜_d = 𝓜 with d
  hard-wired satisfies this, and its finite control depends on d only. κ_d is computed from d
  and p on the tape, so the clause "and κ_d" is redundant but harmless.
  - The remark currently says only "a multitape Turing machine". It should say one fixed machine
    (drop-in below).
- **C₁** is absolute for this construction. If someone instead builds 𝓜_d with κ-dependent
  tables in the finite control (for example permutation parity by lookup), the same tally gives
  a bound with C₁ = C₁(d). The d³ should then be dropped, writing C_d M_d b³(g_d²+b²); that is
  still enough for the proposition at fixed c. The construction above avoids this, so the
  remark's "absolute constant" stands.
- **C₀.** In (iv) of the proposition, C₀ (Pippenger–Fischer) depends on 𝓜_d, here only through
  the O(log d) states that write d. "Depending only on 𝓜_d, hence only on c" stays true.
- **Uses of F_d.** The proposition uses F_d only as a fixed deterministic map that returns a
  nonzero solution on canonical inputs at arity M_d ≥ B_{κ_d}(g_d) (items (ii), (iii)). The
  phrase "the witness s(λ) of Schedule 1" in G1 is fine when read as "the witness computed by
  𝓜_d". An optional clarifying clause is below.
- **Off-canonical words.** The clock T^IS_d covers them automatically: the circuit simulates T
  steps, whatever the tape then holds.

## 8. Closure (B): cited simulation (fallback)

**[source, number from memory]** C. H. Papadimitriou, *Computational Complexity*,
Addison-Wesley 1994, Section 2.6 ("Random access machines"), Theorem 2.5: if a RAM program
computes a function in time f(n), then a 7-string Turing machine computes it in time O(f(n)³).

- His RAM is unit-cost, with instructions READ, STORE, LOAD, ADD, SUB, HALF, jumps and indirect
  addressing, and no multiplication. n is the input length in bits.
- I am confident of the section and of the cubic overhead. The theorem number and the "7-string"
  detail are from memory and should be checked before citing them; cite only the section
  otherwise.
- Cook and Reckhow (J. Comput. Syst. Sci. 7, 1973) also simulate log-cost RAMs by multitape TMs
  with polynomial overhead. I do not recall their exponent and theorem number reliably enough to
  cite.

**Use.** Run the same algorithm as a RAM program 𝓡 that reads d.

- A field multiplication or reduction is a shift-and-add loop with HALF and conditional SUB,
  O(b) instructions. Inversion is binary extended Euclid, O(b) instructions. So the arithmetic
  is at most c b F ≤ 40c κ³ N b² (a² + b²) instructions.
- Bookkeeping is O(1) per record item touched. The items are those of §4, each counted once
  rather than b cells at a time, so bookkeeping is at most c κ³ N b² (a² + b²) over all runs.
- 𝓡 also touches every input bit (HALF loops in the zero-column test), O(M_d g_d b), so
  f(n) ≥ n.
- Hence f ≤ c′ d³ M_d b² (g_d² + b²), and

  **T^IS_d ≤ C_B d⁹ M_d³ b⁶ (g_d² + b²)³,** with C_B absolute.

- This still uses the item count of §4, but random access removes every layout question.
- Pippenger–Fischer applies to the 7-string machine as is. R_d becomes
  O(d⁹ M_d³ b⁶ (g_d²+b²)³ log(M_d b)).
- **Recommendation.** Use (A). Keep (B) in reserve if a referee rejects the layout sketch.

## 9. Drop-in LaTeX (not applied; AI-checked, pending human review)

**(1) Remark `rem:is-runtime`.** Replace the text from "With schoolbook arithmetic each operation
costs $O(b^2)$ bit operations." through "...when $\nu$ is bounded." (keep the display and the
final sentence citing the earlier report) with:

```latex
With schoolbook arithmetic and the binary extended Euclidean algorithm, each of these operations costs $O(b^2)$ steps of a multitape Turing machine that keeps its operands and $p$ on dedicated tapes. All other work is sequential data movement under the following layout (AI-checked, pending human review). The tree of \cite[Lemma~12]{IvanyosSantha2015} is evaluated level by level, for all calls of one accumulation level of \cite[Section~3.3]{IvanyosSantha2015} together. The children of a level-$\ell$ node are $\kappa^{\ell-1}(a+1)$ consecutive records of level $\ell-1$, so their concatenation is the node's matrix stored by columns, and each Gauss--Jordan pivot is one pass over it, with $O(b)$ head movement per entry against one multiplication per entry. The vectors $w_{a'}$ are accumulated in one sweep per child over $\kappa^\ell$ slots. The inputs below a node, and the columns below a call, occupy consecutive positions, so the classes, the coefficients and the representation indices are updated by merging two streams written in the same order. The Pohlig--Hellman digit tables, the collision table of the zero sum and the values $z_j$ have at most $\kappa+1$ entries and are scanned linearly, and a restart erases the work tapes at no more than the cost of the aborted run. Counted pass by pass, the head movement exceeds a constant per field operation only by factors polynomial in $\kappa$, and it stays below an absolute constant times $\kappa^3Nb^2(a^2+b^2)$ per run (\file{research/audits/reviews/2026-11-04-rees-is-runtime-tm.md}). Hence one fixed multitape Turing machine $\mathcal{M}$, with a fixed number of tapes and a fixed alphabet, which reads $d$, $p$, $g_d$, $M_d$ and the columns from its input tape, computes the witness of Schedule~1 within
\[
  T^{\mathrm{IS}}_d = C_1\, d^3\, M_d\, b^3\,(g_d^2 + b^2)
\]
steps, for an absolute constant $C_1$ that is not computed; the machine $\mathcal{M}_d$ of Proposition~\ref{prop:coherent-receiver} is $\mathcal{M}$ with $d$ fixed in its finite control. The order in which the nodes are evaluated affects neither correctness nor the bound $\nu+1$ on the number of runs. For fixed $d$ this is\[O\bigl((g_d+1)^{d\lceil\log_2(d+1)\rceil}\, b^3 (g_d^2+b^2)\bigr),\]and $O\bigl(M_d b^2(g_d^2+b)+b^4\bigr)$ when $\nu$ is bounded; the term $b^4$ is the zero sum, which depends only on $p$ and $\kappa_d$.
```

The display is unchanged. The only change to a bound is the added "$+b^4$" in the bounded-ν
clause.

**(2) Discussion after `prop:coherent-receiver`.** Replace "and the explicit bound
$T^{\mathrm{IS}}_d$ of Remark~\ref{rem:is-runtime} rests on a standard Turing-machine layout
argument that is not written out" with:

```latex
and the explicit bound $T^{\mathrm{IS}}_d$ of Remark~\ref{rem:is-runtime} rests on the tape layout sketched there, which is AI-checked, pending human review
```

**(3) Optional, in the statement of `prop:coherent-receiver`.** After "...followed by the Bezout
step of Remark~\ref{rem:is-import}(b)", add:

```latex
 (any fixed order of evaluating the nodes; only the determinism and the correctness of $s(\lambda)$ are used)
```

No change is needed to (iv) of the proposition: C₁ stays absolute, so
R_d = O(d³ M_d b³ (g_d²+b²) log(M_d b)) stands.

**If closure (B) is preferred instead.** Replace the displayed bound by
$T^{\mathrm{IS}}_d = C_B\, d^9 M_d^3 b^6 (g_d^2+b^2)^3$. Replace the layout sentences by "A
random-access machine without multiplication runs this computation in $O(d^3M_db^2(g_d^2+b^2))$
steps, and a multitape Turing machine simulates it with cubic overhead
\cite[Section~2.6]{Papadimitriou1994}". Add a bib entry `Papadimitriou1994` (Addison-Wesley,
1994). In (iv), change R_d to $O(d^9M_d^3b^6(g_d^2+b^2)^3\log(M_db))$.

## 10. Status

| Part | Status |
|---|---|
| O(b²) TM primitives (mult, reduction, binary Euclid, pow, integer division) | [proved], standard |
| Sequential layout (S1)–(S4) and the passes of §4 | [proved] at sketch level; not a formal TM |
| Tally ≤ C κ³ N b³(a²+b²) + C M_d(g_d+1)b, C absolute | [proved] (closed forms (i)–(iii)); unit-constant check max 0.90 [exact] |
| Displayed T^IS_d = C₁ d³ M_d b³(g_d²+b²), C₁ absolute | [proved] modulo the earlier note's (F) and Z bounds |
| Bounded-ν clause O(M_d b²(g_d²+b)) | **unsupported as stated**: the proved zero-sum bound is Θ_κ(b²) field operations, i.e. O(b⁴) steps, not covered when b > M_d (no lower bound is proved); the corrected form with + b⁴ is proved |
| Closure (B) | [source] Papadimitriou §2.6; theorem number from memory |
| G1 consistency | holds with "one fixed machine" wording; witness may differ from the Python reference |

- **Claim gates that must stay false:** `general_sde_implemented`, `coherent_receiver_implemented`,
  `independent_review`, `formal_compiler_checked`, and every Rees novelty, priority or
  receiver-execution gate. No machine was built or run; this is a cost argument.
- **Next.** The integrator applies §9 (1) and (2), and optionally (3), to `main.tex`. Acceptance
  test: the paper builds, the displayed T^IS_d is unchanged, and the strings
  "constant-factor overhead" and "not written out" no longer occur in `main.tex`.
- **Hard question left open.** Can the zero sum be lifted out of the solver? It is public data
  of p and κ_d, so it could be computed while the circuit is generated. That would remove the b⁴
  term and the b⁵ part of Z from T^IS_d.
