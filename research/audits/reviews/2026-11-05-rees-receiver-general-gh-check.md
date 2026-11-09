# Check of "Rees HSP: the coherent witness circuit at every fixed κ, and the (G, H) the coherent generator covers"

5 November 2026. AI-only adversarial check (Claude Code, Opus 5.5). **Status: AI-checked, pending human review.** Not Lean, not human review.

Subject: `research/audits/reviews/2026-11-05-rees-receiver-general-gh.md` ("the report"), its folder and `tests/test_rees_receiver_general_gh.py`.

Code read:
- `theorems/rees_coherent_sde_kappa.py`: all of the constants, `CoherentSDEKappa._forward`, `_class_flags`, `_less_into`, `_qroot_chain`, `_root_chain`, `_copy_stage`;
- `theorems/rees_coherent_sde_k2.py`: constants, `first_dependency`;
- `theorems/rees_circuit_coherent.py`: `MergeBlock`, `TerminalSample`, `prove_controlled_merge`, `block_structure`, `remap`, `flatten`, `prog_counts`;
- `theorems/rees_circuit_coherent_k3.py`: all of it;
- `theorems/rees_circuit_general.py`: `bch_nodes`, `GroupLaw`, `Encoding`, `Config`;
- `theorems/rees_end_to_end_sim.make_cover`;
- `theorems/rees_circuit_arith.py`: `Anc`, `cuccaro_add`, `add_ext`, `sub_ext`, `formula_counts`.

Paper read: `main.tex` l. 374, 650–702, 810, 851–875; `appendix-schedule2.tex` l. 370–376 (`cor:app-s2-small`) and l. 716; `appendix-backends.tex` l. 40–47.

What was not done: no `.tex`, `theorems/`, `STATE.md`, registry or git change, and `make_numbers.py` was not run.

Outputs: this file, and the folder `research/audits/reviews/2026-11-05-rees-receiver-general-gh-check/`, which holds seven scripts with their `.json` and `.log` outputs. The scripts import only `theorems/`, never the report's folder. Every run used `nice -n 10`, at most 2 processes, and a peak RSS of 275 MB. The report's own test file passes (6 passed, 2.6 s).

## Verdict table

| claim | verdict | fix |
|---|---|---|
| (A) Theorem A_κ (power mode), every κ ≥ 2, p ∉ E_2(κ), every a, given (M), (M′) | **Holds** | One bullet needs a fix: "constructs iff p ∉ E_2(κ)" holds only for p ≤ 2·10⁶ (row R). |
| (A) "for every valid normalised contraction" | **Holds** | Re-derived: only α_0 = 1, β_0 = 0, the κ² coset conditions and their consequence β_ν ≠ 0 are used. The weights may also be 0. |
| (A) failure modes of the FFT-pruned search (§2.5 item 3) | **Holds with fix** | A float error could also cause a false `ValueError` refusal or an `AssertionError`, not only a non-least contraction. Under `python -O` the `contraction_valid` assert is stripped. |
| (A) `stop="general"` not covered | **Holds** (as a disclaimer) | A control run here passes (exhaustive at (31,1,3) and (41,1,4)); that is not a proof. |
| (A) §2.4 "42 normalised contractions at p = 19, 24 with all entries nonzero" | **Holds with fix** | 42 is confirmed independently. 24 is the number with α_1, α_2, β_1, β_2 all nonzero. In the paper's sense of "entry" (C_ij ∝ α_j + β_i), only **6** have every entry nonzero. |
| (D2b) general proof of the controlled BCH merge, every class | **Holds** | None. |
| (B)(S) shape (S1)–(S6), (KS), (INST), (D1), (D2c), (CLEAN) | **Holds** (read off the code; finite checks) | In the paper's convention this is "argued", unless it gets a provenance item. |
| (B)(L) readout uniform on h^⊥ | **Holds** (conditional, as stated) | List `lem:homogeneous` among the conditions in the §7.2 text as well. |
| (B)(R) "Coh is constructed **iff** every grade with κ_d ≥ 3 has p ∉ E_2(κ_d)" | **Error** for p > 2·10⁶ | The capped lazy search raises `RuntimeError` at primes **outside** E_2(κ): at κ = 6 for 2 of the first 4 primes above 2·10⁶, at κ = 7 for 4 of 4. The "iff" holds for p ≤ 2·10⁶. |
| (B) "for every fixed c all but finitely many p are covered" | **Error** for c ≥ 6 (as a statement about the generator) | It is true of the mathematics (`prop:decoupled-sde`), not of the implemented search. For c ≥ 7, every p > 2·10⁶ with p ≡ 1 (mod 7) tested was refused. |
| (B) "every class-two and class-three group, every H, every p > c" | **Holds with fix** | It is proved for p ≤ 2·10⁶. Above that it is argued (four primes tried, none refused). E_2(3) = ∅ is `cor:app-s2-small` (appendix-schedule2.tex), resting on `prop:app-s2-TA` plus a finite search, not on `prop:decoupled-sde`. E_2(2) is not needed at all, because κ = 2 grades use `CoherentSDEK2`. |
| (B)(C) gate count O_c((n^{2c+1} + n^{2c−2}b²)·b²) = poly_c(log\|G\|, log p) | **Holds** | Say "excluding the transforms **and the c·N_c oracle calls**". |
| §4 G2 (generator time) | **Gap** | It omits that `G.Config` builds `Encoding(p)` in about Θ(p³) time (49 s at p = 509), which is exponential in log p, like the FFT search. |
| §7.1 proposed Scope text | **Holds with fix** | See §6 below. Five corrections, plus consequential edits elsewhere in main.tex. |
| §7.2 proposed text | **Holds with fix** | Add `lem:homogeneous` and the fixed-instance qualifier. |
| §7.3 flag diff `wired_into_generated_receiver: True` | **Error** (inconsistent) | Do not apply it. `rees_coherent_sde.py` and `rees_coherent_sde_k2.py` are wired into a backend just as much, and both keep `False` with the same docstring. Flipping one module mis-signals. Clarify the docstrings instead (§6.3). |
| gate `coherent_receiver_implemented` | **Holds**: false (`rees_hsp_reduction.json` l. 35) and must stay false | None. |

## 1. (A) re-derived

I read `_forward`, `_qroot_chain`, `_root_chain` and `_copy_stage` myself, and derived the algorithm and its invariants without using the report's §2.

**Correctness of the rounds and weights.** Write w_k = Σ_{i∈B_k} δ_i λ_i, so that w_k = −Σ_{l≤k} y^{(k)}_{l−1} v_l by the first dependency. The weights are:
- on block k < K, ζ_{k+1}δ_i(α_{cos ζ_{k+1}} + β_{cos δ_i});
- on block K, δ_i.

Hence Σ x_i λ_i = Σ_{k<K}(za_{k+1} w_k + ζ_{k+1} v_{k+1}) + w_K. The coefficient of v_l (l ≤ K) is

  ζ_l − y^{(K)}_{l−1} − Σ_{l′=l+1}^{K} za_{l′} y^{(l′−1)}_{l−1}.

The back substitution sets exactly this to 0: τ_l starts at y^{(K)}_{l−1} and receives +za_{l′}y^{(l′−1)}_{l−1} from each step l′ > l. The code writes `add_product(τ_j, za, Z, −1)` with Z = −y.

**Lemma 4′.** δ is a minimal dependency with δ_{j*−k} = 1 and a prefix that is independent modulo U_k. So v_{k+1} ∈ U_k forces β_{cos δ_i}δ_i = 0 for i < j*−k. The coefficient at j*−k is β_{cos 1} = β_0 = 0. Since β_ν ≠ 0 for ν ≠ 0 (the j = 0 condition), every nonzero δ_i lies in P, and so v_{k+1} = 0.

**One-hot stop.** F_k = run_k ∧ stop_k with run_{k+1} = run_k ⊕ F_k. Rounds after K only reach later gates multiplied by F_k = 0 or by τ_{k+1} = za_{k+1} = 0. τ_l = 0 for l > K holds because nothing writes it except steps l′ > l, all of which have za = 0. The toggled bit 0 of ga at k = K turns 0 into 1 and back.

**Copy stage.** AMM invariant: t_j = z^{q^{j+1}⌊k/q^j⌋} and r_j^q = x·t_j. After S−1 rounds t = z^{q^S·(…)} = 1. Note that z = g^Q has order q^S because g^{(p−1)/q} ≠ 1. The chain for κ runs over the prime factors with multiplicity. A q-th root of a κ′-th power is a (κ′/q)-th power, because μ_q ⊂ (F_p^×)^{κ′/q}.

**Least root.** It is taken over {ω^t r}, which is all κ roots since ω = g^h has order exactly κ. The comparator is `sub_ext` then CX then `add_ext`. This is correct for all b given Cuccaro's adder: (x, e) − y mod 2^{b+1} has top bit [x < y], and adding y back restores (x, 0). I checked it exhaustively for b = 9..12 (`comparator_check.json`), extending the report's b ≤ 8.

**Exponent.** s^d = ρ^{κ·u(d/κ)} = x^{1+mh} = x on P ∪ {0}. The inverse u exists because gcd(d/κ, h) = 1.

**Bennett.** P_i never touches S and A_i touches only S_i, so (P_i; A_i; P_i^{−1}) changes S_i alone. F touches no S wire, so F^{−1} restores the rest.

**Hidden assumptions checked.**
- α_0 = 1 and β_0 = 0 are hard-coded (as `X` on bit 0 and an initial 0). `contraction_valid` enforces them for any supplied contraction.
- h = 1 occurs only at p = 3, κ = 2. I ran it exhaustively (a = 1) and on 1200 samples (a = 2): it passes.
- u ≠ 1: I ran it exhaustively at (31,1,9) with u = 7 and at (41,1,12) with u = 7.
- Composite κ: κ = 4 exhaustive at p = 61 and p = 41, sampled at p = 73 with a = 2; κ = 6 sampled at p = 229.
- At κ = 2 the module itself (not the receiver's `CoherentSDEK2`) passes exhaustively at p = 3, 5, 7, 13, 17.

No unhandled branch was found. The weak point is in the specialisation bullets, not in the proof: "constructs iff p ∉ E_2(κ)" fails above 2·10⁶ (§3).

**Does "any normalised contraction" suffice?** Yes. The proof uses the contraction only through:
- α_0 = 1, β_0 = 0;
- the κ² conditions α_j + β_i ∈ g^{−(i+j)}P ∪ {0};
- β_ν ≠ 0.

The contraction must be normalised relative to the module's own g (the least coset generator). That is what `contraction_valid` checks.

## 2. (A) independent computations (`indep_kappa.py`)

The script has its own primitive root and discrete logs and its own coset map. Its contraction search is a plain exact DFS with bitset pruning (no FFT). The reference solver is written from the proof of `prop:triangular-sde`: rank-based stop test v_{k+1} ∈ U_k, back substitution by coordinate solves, least root by table, u by search. The script also has its own bit-sliced simulator. The circuit is `CoherentSDEKappa(...).prog` flattened by `rees_circuit_coherent.flatten`.

Each row checks four things: labels restored, S equal to the paper-faithful witness, every other wire 0, and Lemma 4′. It also scans that no flattened gate targets a label wire and that no item of F touches an S wire.

| (p, a, d) | κ | u | inputs | mode | contraction | result |
|---|---|---|---|---|---|---|
| (31, 1, 3) | 3 | 1 | 29 791 | exhaustive | least (module = own lex search) | pass |
| (31, 1, 9) | 3 | 7 | 29 791 | exhaustive | least | pass |
| (43, 1, 3) | 3 | 1 | 79 507 | exhaustive | least | pass |
| (31, 1, 3) ×4 | 3 | 1 | 29 791 each | exhaustive | 4 non-least of 191, one with a zero C-entry | pass |
| (7, 2, 3), (31, 2, 3) | 3 | 1 | 1 500 each | sampled + rank ≤ 1 / sparse / repeated / zero | least | pass |
| (7, 2, 3) | 3 | 1 | 1 500 | sampled | lex-greatest of 2 | pass |
| (61, 1, 4) | 4 | 1 | 226 981 | exhaustive | least (p = 61: every contraction has a zero entry) | pass |
| (41, 1, 12) | 4 | 7 | 68 921 | exhaustive | least | pass |
| (41, 1, 4) | 4 | 1 | 68 921 | exhaustive | 40th in lex order | pass |
| (73, 2, 4) | 4 | 1 | 600 | sampled | least | pass |
| (229, 1, 6) | 6 | 1 | 1 200 | sampled | least | pass |
| κ = 2 via this module: p = 3 (a = 1, 2), 5, 7, 13, 17 | 2 | 1 | all / 1 200 | exhaustive / sampled | least | pass |
| `stop="general"`: (31,1,3), (41,1,4), (7,2,3) | 3, 4 | 1 | exh / exh / 1 500 | control | least | pass |

Mutants at (13,1,3), all detected (S ≠ reference): β_1 + 1, α_2 + 1, the least-root step skipped, and output coefficient 2.

Contraction counts at κ = 3: p = 7: 2; p = 13: 2; p = 19: 42; p = 31: 191 (116 with a zero C-entry). The report's 42 at p = 19 is confirmed, against the κ report's "40".

**Refusals.** My own exact search agrees with the module's `kappa_constants`, and the module's contraction equals my lexicographically least one at every prime:

| κ | primes scanned | own E_2(κ) | module refuses |
|---|---|---|---|
| 3 | p ≤ 400 | none | none |
| 4 | p ≤ 400 | {5, 13, 17, 29, 37, 53} | the same |
| 5 | p ≤ 200 | {11, 31, 41, 61, 71, 101, 131, 151, 181} | the same |
| 6 | p ≤ 240 | the same 23 primes | the same 23 |

These match the paper's lists (`main.tex` l. 674). The κ = 4 scan at d = 12 also agrees. The constructor itself refuses (13,4), (53,4), (11,5), (181,5), (7,6) and (859,6), each with `ValueError`.

**(M) re-run** with an own simulator (`macro_check_indep.json`): `add_product`, aliased `add_product(t,a,a)` and `add_scaled`, ancillas back to 0 and operands unchanged:
- p = 61: every coefficient, all words;
- p = 131: every coefficient; the product with t ∈ {0, 1, 2} and all (a, b), the squaring and the scaled macro on all words;
- p = 191: 16 coefficients, all words.

All pass. p = 131 and p = 191 lie beyond the report's exhaustive range.

## 3. (B) re-derived, and the refusal error

**(S), (D1), (D2c).** Read off `TerminalSample._emit` and `MergeBlock`; I agree with the report's reading.
- A label register is touched by QFT, by the instrument macro as an operand (`args[1]`), by QFT^†, and then only inside its parent's U and U^{−1}.
- `ctrl` and `bch` never touch labels.
- The pool is shared, but blocks are sequential (depth first), not nested.

**(D2b), re-derived.**
- `ctrl` computes pw_k = s^k for k = 2..d−1 and G_j = −s^{deg j}q_j.
- `bch` runs: bracket pass at (x, sign_g = +1); linear pass W += BCH_d(x, G); reverse bracket pass; swap; bracket pass at (x′, −G), where the code multiplies by sign_g once per G-letter, hence [w](x′, −G); W −= BCH_d(x′, −G) = x; reverse bracket pass.
- Suffixes are computed before parents and uncomputed after them. Targets never alias operands, apart from the pw_2 squaring, which (M) covers.
- Support pruning is a superset computation from T, so dropped coordinates are identically 0.
- BCH denominators involve only primes ≤ d < p.

The proof holds for every class. I found no gap.

**(R): the error.** `_kappa_constants` calls `canonical_contraction(p, κ, g, scan_cap = 10⁵ if p ≥ 10⁶)`. For p > 2·10⁶ this is `_canonical_contraction_lazy`. Its DFS chooses each β_i by the j = 0 condition alone, and at the leaf calls `least_alpha(j)` with the cap. If any α_j has no admissible value below 10⁵, it **raises at once instead of backtracking to the next β**.

A random α satisfies the κ conditions with probability about κ^{−κ}, so:
- for κ ≤ 5 the cap is almost never hit;
- for κ = 6 it is hit often, and for κ = 7 almost always.

`large_p_search.json`, the first four primes above 2·10⁶ in each class:

| κ | constructed | `RuntimeError: alpha scan cap hit` |
|---|---|---|
| 3 | 4 / 4 | none |
| 4 | 4 / 4 | none |
| 5 | 4 / 4 | none |
| 6 | 2000029, 2000113 | 2000083, 2000107 |
| 7 | none | 2000083, 2000153, 2000209, 2000293 |

All of these primes lie outside E_2(κ): the paper gives max E_2(6) = 859 and max E_2(7) = 3221 (exact below 5·10⁶).

So:
- Theorem B(R)'s "iff" is false above 2·10⁶;
- §3.1's "for every fixed c all but finitely many p are covered" is false for the implemented generator when c ≥ 6. For c ≥ 6 every p ≡ 1 (mod 3) has κ_6 = 6, and for c ≥ 7 every p ≡ 1 (mod 7) has κ_7 = 7.

The report's parenthesis "(or `RuntimeError` for p > 2·10⁶ if the α-scan cap is hit)" names the branch but does not withdraw the "iff" or the cofinite claim. The circuits that are emitted are still correct, so the refusal is safe; only the coverage statement is wrong.

**E_2(2) and E_2(3) in the paper.**
- `cor:app-s2-small` (appendix-schedule2.tex l. 370) states E_2(2) = E_2(3) = ∅.
- κ = 2: `prop:app-s2-TW` for p ≥ 7, plus exhaustive search at p = 3, 5.
- κ = 3: `prop:app-s2-TA` (T_A(3) = 79.04), plus exhaustive search at the ten primes p ≡ 1 (mod 3) up to 79.
- Provenance item `prov:s2-small`. Status: AI-checked, pending human review.
- `main.tex` l. 674 and l. 870 restate the result. `prop:decoupled-sde` itself does not prove it.
- The generator needs only E_2(3) at κ = 3 grades. κ = 2 grades use `CoherentSDEK2`, which has no contraction search and exists for every odd p (κ = 2 check report, accepted).

So "every class-two and class-three instance at every p > c" is proved for p ≤ 2·10⁶. That uses `cor:app-s2-small`, Theorem A_κ, the κ = 2 proof and the exact FFT search, with the caveat that the search is exact up to floating-point `rint`. Above 2·10⁶ it is argued: no κ = 3 refusal was observed, but the cap is not excluded by proof.

**Generator time (an addition to G2).** `G.Config` builds `Encoding(p)`, whose minimal value tests cost about p³ operations:

| p | 61 | 127 | 251 | 509 |
|---|---|---|---|---|
| seconds | 0.09 | 0.8 | 5.7 | 49 |

So, besides the coset-generator scan and the contraction search, the generator as implemented runs in time polynomial in p, that is exponential in log p, for every L. This changes no circuit-size claim.

## 4. (C) gate count on configurations the report did not list (`indep_generator.py`)

My macro formula is written independently:
- own arities and N_d;
- BCH bracket supports recomputed from the cover tensor (only the α coefficients come from `bch_nodes`);
- SDE macro counts taken from each emitted SDE program. For every SDE I tried, these equal the modules' `closed_form_macros`: (61,2,3), (61,1,4), (73,1,3), (229,2,6), (73,2,4), and K2 (61,3,2).

| config | κ by grade | arities | macros (formula = emitted, by component) | gates | raw / gates | gates ≤ (158b²+46b)·macros + raw | QFT calls | oracle = c·N_c | D1 scan |
|---|---|---|---|---|---|---|---|---|---|
| Heis(F_7) | 2:2 | 3 | 375 ✓ | 450 026 | 0.16 % | ✓ | 24 | ✓ (6) | pass |
| n4(F_73) | 2:2, 3:3 | 6, 3 | 6 818 ✓ | 40 183 090 | 0.10 % | ✓ | 230 | ✓ (54) | pass |
| n5(F_61) | 2:2, 3:3, 4:4 | 10, 6, 3 | 109 262 ✓ | 477 005 772 | 0.10 % | ✓ | 3 330 | ✓ (720) | pass (1 980 label wires, 21 600 oracle wires) |

n5(F_61) is the first program here with κ = 2, 3 and 4 grades in one program. The report's QFT-call formula gives 1980 + 660 + 685 + 5 = 3330, which matches. The report's coarse bounds BR_d ≤ 2^{d−1}nnz(T_d) and LIN_d ≤ 2n + 2^{d−1}n hold on all three configurations. `structure()` is all true.

**Asymptotics re-derived.**
- N_d ≤ μ^{d−1}, with μ = (n+1)(n+2)/2.
- Sources: ≤ 2c·m·n·N_c, which is O(n^{2c}).
- BCH merges: N_{d−1}M_d(4BR_d + 2LIN_d), which is O(n^{2c−2}·n³).
- SDEs: N_{d−1}·O_κ(g⁴ + g²b²), which is O(n^{2c} + n^{2c−2}b²). For κ ≥ 3 the AMM chains need T = O(b²) products, because S_q ≤ log_q p.
- Controls: O(n^{2c−1}).

With ≤ 158b² + 46b gates per macro and raw gates of lower order (0.1 % measured), the total is O_c((n^{2c+1} + n^{2c−2}b²)b²). Since n ≤ cm and log|G| = m log p, this is poly_c(log|G|, log p).

The count excludes the exact transforms (O_c(n^{2c−1}) calls) and the oracle, which is a table call made c·N_c times. Any paper sentence must say both.

## 5. Paper text and flag

### 5.1 Problems in the report's §7.1 sentence

1. "one Adleman–Manders–Miller extraction per prime factor of κ_d": it should be per prime factor *counted with multiplicity* (`lem:coherent-power-sde` says v_q(κ) extractions per q). The comparator-based least-root choice should also be named.
2. "the generator refuses every other instance": true. But "applies to … every Lie algebra … at which every grade … p ∉ E_2(κ_d)" is false above 2·10⁶ (§3). Restrict it to p ≤ 2·10⁶.
3. "in particular to every class-two and class-three instance": needs the same restriction, and the citation `cor:app-s2-small`.
4. "poly_c(log|G|, log p) gates, excluding the transforms": add "and the oracle calls".
5. "the classical search for its constants is not shown to run in polynomial time": too narrow. The whole classical generator is not, because `Encoding` is about Θ(p³) (§3).

The structural facts (S1)–(S6), (D1) and (D2c) are read off the code. Their proof is not in the paper, so in the paper's own label convention (`main.tex` l. 374) they are "argued" unless a provenance item is added. The κ = 2 precedent sentence uses an item (`prov:gc-kappa2-proof`); this one needs a new item too. The macro range should cite it.

**Consequential edits the integrator must make** (otherwise the paper contradicts itself):
- `main.tex` l. 374: "A backend … each run on fixed finite instances"; "none is built or implemented here".
- `main.tex` l. 810: "They establish nothing more: they are finite computations on fixed instances, … not a coherent receiver for general (G,H)". This stays true for *general* (G,H), but the "fixed instances" part needs the exception.
- `main.tex` l. 870: "wired only into `rees_circuit_coherent_k3.py`, on that algebra over F_7, and into `rees_circuit_coherent_c4.py`".
- The Table `tab:backends` row for `coherent_k3`.
- The module STATUS of `rees_circuit_coherent_k3.py` (`"scope": "n4(F_7) only"`, `"general_instances": False`), which a reader of the code will find contradicting the new sentence. Code edits are outside this check; flag them for the code owner.

### 5.2 The §7.3 flag diff

All three SDE modules carry `"wired_into_generated_receiver": False` and the docstring "Does NOT: wire into the generated receiver":
- `rees_coherent_sde.py` l. 63;
- `rees_coherent_sde_k2.py` l. 62 and 38;
- `rees_coherent_sde_kappa.py` l. 75.

The κ = 1 and κ = 2 modules are wired into the fourth backend exactly as the κ module is wired into the fifth. The family convention therefore reads "generated receiver" as a general receiver, which does not exist.

Flipping only the κ module makes STATUS say this module is in "the generated receiver" while its siblings are not, and it invites the reading `coherent_receiver_implemented`. **Do not apply it.** What I endorse is §6.3.

### 5.3 Gate

`research/reductions/rees_hsp_reduction.json` l. 35: `"coherent_receiver_implemented": false`. It must stay false, for these reasons:
- grades with p ∈ E_2(κ_d) have no coherent solver;
- the implemented search also refuses some primes outside E_2 (κ_d ≥ 6, p > 2·10⁶);
- the arities and query count are not those of `thm:main`;
- the transforms are exact;
- the generator is not polynomial-time.

## 6. Paper text endorsed for the integrator

### 6.1 `appendix-backends.tex` l. 45: replace the last two sentences ("For the coherent class-four circuit over $\mathbb{F}_7$ … no generator of coherent receivers for general $(G,H)$ exists.") by

> The same written argument, with the coset flags, the two-level contraction, Adleman--Manders--Miller extractions for the prime factors of $\kappa_d$ counted with multiplicity and a choice of the least root by comparators in place of the sign test and Tonelli--Shanks, proves that the witness circuit of Lemma~\ref{lem:coherent-power-sde} maps every canonical label tuple, with its output and workspace registers at zero, to the label tuple, the witness of that lemma computed with the normalised contraction it is given (any one) and a zero workspace, at every $\kappa_d \ge 3$ with $p \notin E_2(\kappa_d)$; it assumes only the correctness of the two arithmetic macros on canonical words, checked exhaustively for $p \le 127$, and of the comparator, checked exhaustively for $b \le 12$ (Appendix~\ref{app:provenance}, item~\ref{prov:gc-kappa-proof}; AI-written and AI-checked, pending human review; not machine-verified). With it, and with the shape, footprint and wiring properties of the emitted programs, which are read off the generator code and checked on the generated programs of ten configurations (argued, same item), the deferred-measurement proof applies, for every subgroup $H$, to every program that \texttt{rees\_circuit\_\allowbreak coherent\_k3.py} emits. For $p \le 2\cdot10^6$ it emits one for every Lie algebra over $\mathbb{F}_p$ of class $c<p$ at which every grade with $\kappa_d \ge 3$ has $p \notin E_2(\kappa_d)$, in particular for every class-two and class-three instance (Corollary~\ref{cor:app-s2-small}) and for the class-four instance over $\mathbb{F}_7$, and it refuses every instance with a grade at which $p \in E_2(\kappa_d)$; above $2\cdot10^6$ its search for the contraction is capped and also refuses some primes outside $E_2(\kappa_d)$, for example at $\kappa_d \in \{6,7\}$. Excluding the transforms and the oracle calls, each emitted program has $\poly_c(\log|G|,\log p)$ gates. This is not the receiver of Theorem~\ref{thm:main}: its merge arities are the coherent ones, it uses exact transforms, it does not cover the primes in $E_2(\kappa_d)$, and its classical generator, including the search for its constants, is not shown to run in time polynomial in $\log p$.

The label `prov:gc-kappa-proof` is a **new provenance item** the integrator must create. It should point to the report, this check and their folders. "Ten configurations" means the report's ten, which carry the full structural checks (D1, D2c roles, footprints, `prove_controlled_merge`). The three of §4 here carry only D1, `structure()` and counts.

### 6.2 `appendix-backends.tex` l. 47: replace "None of these circuits is a coherent receiver for general $(G,H)$, and they test no asymptotic cost." by

> Apart from the programs of \texttt{rees\_circuit\_\allowbreak coherent\_k3.py} described in the preceding paragraph, whose output law is uniform on $\hh^\perp$ conditionally on Lemmas~\ref{lem:homogeneous} and~\ref{lem:central}, Proposition~\ref{prop:descent} and exact transforms, these circuits are checked only on their fixed instances; none of them is a coherent receiver for general $(G,H)$, since grades with $p \in E_2(\kappa_d)$ have no coherent witness circuit, and the runs test no asymptotic cost.

Keep the following sentence ("Proposition~\ref{prop:coherent-receiver} shows … That is a statement of existence: no circuit generator for it has been implemented."). It stays true.

### 6.3 Code docs (for the code owner; not a paper change)

Leave all three `wired_into_generated_receiver` flags as `False`. In each of the three module docstrings, replace "Does NOT: wire into the generated receiver" by a precise statement of which backend wires the module, through which function, and that it is not a general coherent receiver:
- κ = 1 and κ = 2: `rees_circuit_coherent.sde_circuit`;
- κ module: `rees_circuit_coherent_k3.sde_circuit_k`.

## 7. Files (folder `2026-11-05-rees-receiver-general-gh-check/`)

- `indep_kappa.py`, with `indep_k3.{json,log}`, `indep_k4.{json,log}` and `indep_refuse.{json,log}`: the (A) checks, mutants, contraction counts and refusals.
- `indep_edge.{json,log}`: κ = 2 through `CoherentSDEKappa`, the refusal at p = 19 with κ = 6, and p = 229 with κ = 6. Produced by an inline driver of `indep_kappa.py`.
- `indep_general_mode.{json,log}`: `stop="general"` control (inline driver).
- `indep_generator.py`, with `indep_generator.{json,log}`: (B) counts, D1, structure and seven refusals (n5 over F_17, F_29, F_37, F_53; n6 over F_11, F_31; Q5 over F_13), all `ValueError` with the predicted E_2 set.
- `large_p_search.py`, with `.json` and `.log`: the `RuntimeError` refusals above 2·10⁶ and the cost of `Encoding`.
- `comparator_check.py`, with `.json` and `.log`: (M′) for b = 9..12.
- `macro_check_indep.py`, with `.json` and `.log`: (M) at p = 61, 131, 191.
