# Rees core paper: sync with the companion (rows I190-I212)

5 November 2026. AI session only (Claude Code). This is an editing pass, not a review. No
proof was re-derived, and no claim changes status. Every "AI-checked, pending human review"
label is kept. No new text claims a speedup, novelty, human review, an implemented coherent
receiver, a general SDE solver or a checked formal compiler.

- **Edited:** `docs/papers/rees-hsp/core/main-core.tex` only. `core/references.bib` and
  `core/numbers.tex` are unchanged, and `make_numbers.py` was not run.
- **Backup:** `$TMPDIR/rees-core-backup-030220/core/`
  (`/var/folders/y_/k55rjs0x7nb045dsgq61qw000000gn/T/rees-core-backup-030220/core/`).
- **Edit script:** 29 exact-string replacements, each asserted to occur once
  (`scratchpad/sync_core.py` of this session).
- **Policy:** the core stays the submission. It points to the companion by name, as "the
  full version's appendix on ...", and never by `\ref`. New companion results get at most
  one sentence, and only where the core already discusses the topic.

Decisions: **a** = a correction to text that is also in the core, applied; **b** = a new
result, given at most a one-sentence pointer; **c** = not relevant to the core.

## Row-by-row

| Row | Topic | Decision | Change in `main-core.tex` |
|---|---|---|---|
| I190 | `rem:premature`, `rem:mixed-source` wording (argued, not proved) | a | Outlook "Interfaces that measure early": "a derivation ... gives an Omega(...) lower bound" is now "a project note argues, and neither this paper nor the full version proves, that ... bounded error would need Omega(p^{(c-1)(c-2)/2}) sources", restricted to the class 3 <= c < p. Status: "argued; AI-checked, pending human review". Also states that it is not a lower bound for coherent collective receivers. "Other symmetry sources": the spectral-flag extension is "recorded there but not proved; it is argued in a project note". |
| I191 | Terminology paragraph and status convention | a (labels only) | The core has no terminology paragraph and does not name the coherent receiver or the combined rule, so nothing was imported. Status labels now follow the companion convention: every "AI-checked only" and bare "AI-checked." in the Outlook is now "AI-checked, pending human review", in 7 places (Schedule 2 refinements and status, derived dimension, torsion, black-box, classical filters, early measurement). |
| I192 | triangular-review (proof details of `prop:triangular-sde`) | c | The core gives only the arity (a+1)(a+2)/2 at p not in E_2(kappa). This still matches the companion. |
| I193 | application-3 | b | Outlook "Applications" gains one sentence: a further AI-only search found no application, and argues that black-box p-group tasks of **class less than p** reduce to linear algebra in the Lazard Lie ring after abelian quantum subroutines (IMS 2001, already in the core bib). This follows referee 13's E4 wording. |
| I194 | `rem:is-runtime` restart variant | c | The core has no run-time remark for Schedule 1. |
| I195 | Schedule 3 theorems merged | a (checked) | I198 had already applied this ("the full version states both samplers as one theorem"). The uniform-kernel numbers (4u, u >= c, a_d < u, p >= 16u^2, 2^{O(u log(u+2))} poly) and the free-coordinate arity and cost were re-checked against `thm:free-coordinate`(ii)-(iv). They match. |
| I196 | `\ref` retargets in main.tex | c | The core has no `\ref` to companion labels. No core `\ref`/`\eqref` target is unresolved (script check, and the build). |
| I197 | appendix retargets | c | — |
| I198 | Core K7 consistency; open item "Derived-dimension paragraph still gives only the old route" | a | **Open item closed.** Derived dimension: the free-coordinate sampler, with a zero-sum node at the top grade when p = c+1, gives 2^{O(r log(r+2))} poly(m, log(1/eps)) queries or copies, and the matching time, for every p > c. The old route (u = r+1 for p >= 16(r+1)^2, IMS below) is kept "for oracle input". Status "argued in the full version, AI-checked" is now "conditional on the steps behind Theorem main and on Schedule 3, whose guarantee is for the independent supply of fresh ideal sources only; proof in the full version, AI-checked, pending human review". This matches `cor:fpt-r`. |
| I199 | `rem:fc-zero-sum-sis` | b | One sentence in "Using the label law" (I199 and I200 together): at h = 2 and at kappa_d = p-1, witness finding is average-case SIS mod p. The lattice consequence carries referee 13's I12 qualifiers (abort <= 1-1/poly(g_d); quantum time if the method is quantum). |
| I200 | SIS sentence in main | b | Same sentence as I199. |
| I201 | coset-copy input for every part of Schedule 3 and `cor:fpt-r` | a | Both Schedule 3 status sentences now say "conditional on the steps behind Theorem main, for the independent supply of fresh ideal sources only, with oracle input or coset copies". The derived-dimension sentence now covers coset copies. |
| I202 | lean-c6 | a | Lean paragraph: the hypotheses are named as three (group law, additivity on commuting pairs, subgroups are subalgebras). They are discharged for **c = 3, 4, 5 and 6**; the core had said 3 and 4, which was already stale after the class-five modules of 4 Nov. The SDE content is added: Chevalley-Warning existence among gcd(d,p-1)a+1 columns, the gcd reduction (Lemma bezout), the triangular algebra, and the kappa = 2 contraction for every odd p. "Outside" now reads c >= 7, every computed solver and its arity bounds, every circuit, and "no formally checked compiler is claimed". The receiver policies are not mentioned, so referee 13's E3 rank issue cannot arise. Guard counts (450/488) are not stated in the core. |
| I203 | `rem:sde-subquadratic` | b | One sentence in "Open problems". Under a cryptographic assumption, no classical poly-time algorithm solves every solvable instance at arity a+2 for primes of size kappa^{a+O(1)}. The sentence keeps the scope caveat ("does not exclude a method at an arity at which every instance is solvable"), as referee 13's G2 asks. |
| I204 | K30 exact exponents (`rees_circuit_general.py`) | c | The core cites only `theorems/rees_circuit.py` on Heis(F_3). The companion still describes it the same way. |
| I205 | Tower (`app:s2-tower`) | b | One sentence in the Schedule 2 paragraph, with referee 13's E1 wording: threshold kappa^{q_1+O(1)}, "polynomial in kappa only when q_1 is bounded". It does not lower the Schedule 2 arity or change the exponent 143. |
| I206 | `rem:sde-block-steered` | a | Referee 13's I7 applies to the core. "Whether any polynomial-time solver works with o(a^2) columns at fixed kappa >= 2 is open" is now "no such solver is known for arbitrary columns". The full version gives randomized ones at p >= poly(a) for i.i.d. uniform columns, and for banks in general position (I211). |
| I207 | Referee 13 | a | E1: corrected wording used in the I205 pointer. E2: the core's per-grade rule already named the linear solver, Schedule 2 and Schedule 1 at degree kappa_d. "It does not use Schedule 3" was added. E3: not in the core. E4: used in the I193 sentence. G2: used in the I203 sentence. G3 and G4: not in the core (no cyclotomic coset problem, no receiver). I7: applied (I206). I12: applied (I199). S2: the status-label convention, applied (I191). I1-I6, I8-I11, I13, I14, S1, S3-S7: c (text not in the core). |
| I208 | receiver-sims | c | The core does not discuss the coherent receiver. |
| I209 | Chains (`app:s2-chains`), kappa = 7 data | b | Same sentence as I205: chains of two refinements at arity C(a+3,3) for every kappa >= 4. E_2 data were checked and corrected (see mismatch 7). |
| I210 | s3-arity (`rem:fc-zero-sum-arity`, kappa_d = p-1 node) | c | The core does not discuss zero-sum nodes beyond the I199 sentence. |
| I211 | `rem:sde-worst-case` | b | Covered by the I206 sentence ("banks in general position ... p >= poly(a)"). |
| I212 | receiver-round2 | c | The core does not discuss the coherent receiver. |

## Other mismatches found and fixed

The theorem statements were checked against the companion by a helper agent and by hand.

1. **The class is at most c, not exactly c.** The core says "c may be any upper bound on the
   class", but `def:input-contract`(i) said "of class c" and `thm:rees-cover`(i) said
   "class exactly c". Both now follow the companion: "class at most c", and "class equal to
   the class of L (so at most c)". The proof uses the true class c'. Part (iii) and the
   Preliminaries now say "class at most c" and "the class of L".
2. **`thm:main`.** "a real eps" is now "a rational eps". The gate set is named: "implements X,
   CNOT and Toffoli exactly (for example Clifford+T)".
3. **Classical query sentences after `thm:main` and in the abstract.** These lacked m >= 2,
   delta < 1/2, and "L not abelian" for the non-normal case. All three were added.
4. **`prop:classical-query`(iii), normal-H clause.** "The same holds with p^{m-k} replaced by
   p^{z_k}" read as inheriting q > sqrt(2(1-delta)|G|/|H|), which is false. It now gives the
   companion's explicit bound q > sqrt(2(1-delta) p^{z_k-1}).
5. **Dixmier-Lister.** "lambda, mu, nu, rho in F_p" implied a 12-dimensional derivation
   space over F_p for every p. These parameters are now "free", and the rank 52 = 64-12
   modulo every prime 5 <= p <= 23 is added. The all-p claim rests, as before, on the row
   certificates.
6. **van de Woestijne "Section 6" pin.** Added the companion's `% NEEDS HUMAN VERIFICATION`
   comment. It is a comment only, so the build is unchanged.
7. **E_2 data.** "An explicit finite exceptional set ... (computed exactly for kappa <= 7)"
   is now "a finite exceptional set E_2(kappa) ... (known exactly for kappa <= 7; for
   kappa = 8, 9 only by searches up to a bound)".
8. **`rees_is_sde_solver.py` artifact.** Added "at full arity, and at kappa_d = 4 when the
   computed zero sum has two terms", as in the companion.
9. **Date.** "3 November" is now "5 November 2026 (core version; AI-checked, pending human
   review)". The header comment records this sync.

## Checked, no change

- `numbers.tex` is byte-identical to the companion's.
- `tab:query-crossover`: the helper recomputed log2 Q_q (9.00, 27.76, 33.19, 35.06, 1572.66)
  and the LB primes (443, 337 853, 92 107, 997). The "(v) <" and "copies" columns equal the
  companion's.
- These values match the companion: 143 at c = 9 against ReesClassNineQueryExp = 145;
  E_W(9) = 143; p >= 16 kappa^{2kappa+2}; the kappa^{kappa+o(1)} threshold (argued); 4u
  columns, p >= 16u^2; the free-coordinate arity and cost.
- Left as they are, because each is internally consistent:
  - The BCH bracket count (d-1)d(d+1)/2 is valid for the memoized schedule. The artifacts
    line already gives the unmemoized (d-1)d(d+1)(d+2)/6.
  - Kitaev eps' = eta^2/(16p) differs from the companion's eta^2/(4p), but each paper's
    error split is internally consistent.
  - The phrasing of `rem:query-separation` is covered by the Verification Status section.

## Companion issue noted (not edited; main.tex is out of scope)

- `rem:premature` in `main.tex` has a doubled comma, "for $i < c$,,". It came from referee
  13's S3 insertion (row I207).

## Build

The build ran in a scratch copy of `core/`
(`PATH=/Library/TeX/texbin:$PATH latexmk -g -pdf -interaction=nonstopmode main-core.tex`).
Results:

- exit 0, **27 pp.** (26 before)
- 0 Overfull, 0 Underfull
- no undefined references or citations, no "Float too large", no `??` in the PDF text

Every `\ref`/`\eqref` in the core resolves to a core `\label`. There is no `\mathsf`,
`\mathrel`, `\begingroup` or `\aa`. No core tests exist: `ls tests/tools | grep -i core` is
empty, and no test mentions `main-core`. Nothing was committed.
