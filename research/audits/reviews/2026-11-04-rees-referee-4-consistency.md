# Rees paper, referee pass 4: consistency (2026-11-04)

Scope: `docs/papers/rees-hsp/main.tex` and `appendix-*.tex` as of 2026-11-04,
with `README.md` of the same folder. I read every line of `main.tex` and the
free-coordinate and Schedule-2 appendices, and grepped all six appendices.
A helper agent read `appendix-schedule3.tex`, `appendix-subspace.tex`,
`appendix-torsion-blackbox.tex` and `appendix-codimension.tex` against a
fact sheet of today's edits. I spot-checked its findings in the source and
marked them below.

I did not read the integration log, the handoff archive or any 2026-11-04
review before writing these verdicts. No `.tex` file was edited.

This is an AI-run consistency check, not a human review.

Line numbers refer to physical lines. `main.tex:764` is the single line that
holds the whole "Gate-level control" paragraph; "S*n*" is its *n*-th sentence,
counting from 0, as produced by splitting on ". " before a capital letter or
backslash.

## Mechanical checks that passed

- **Labels and references.** All `\ref`/`\eqref` targets exist, and no label
  is duplicated. Every `\cite` key is in `references.bib`. Every `\file{}`
  path resolves, relative to the cited folder.
- **Old E_2(8)/E_2(9) numbers.** None of 8009, 17551, 9473, 9769, 17623 or the
  old "decided up to" bounds 4201/5689/9649/12799/12979 occurs in any `.tex`
  file or in `numbers.tex`.
- **Quoted primes.** 10433, 10321 and 49417 are primes ≡ 1 (mod 8), and
  13537 and 17659 are primes ≡ 1 (mod 9). The ratios check:
  10321/8^4.5 = 0.891, 17659/9^5 = 0.299, and T_A(8)/(8^8/2) = 13.95 ("about 14").
- **Explicit-QFT bounds** (S11–S18), recomputed from Lemma `lem:qft-mod`:
  - (t,r,τ) = (26,19,15) and (32,22,18).
  - 3π2^-τ = 2.876e-4 and 3.595e-5.
  - Per-sample bounds 0.014177, 0.011178 and 0.012321, giving the run bounds
    0.09924, 0.08943 and 0.09857 (the text says 0.0993, 0.0895 and 0.0986).
  - Per-transform gates 7873 ≤ 8405 and 13303 ≤ 14948 (the lemma's bound).
  - 115282 + 188952 = 304234, and 2694596 + 176·13303 = 5035924.
  - The ancilla pool 4b+2t+1 together with the data register and the 3b+5
    arithmetic ancillas gives the lemma's 8b+2t+6 qubits.
  - The gate-count expansion 420b² + 187bL + 4L² is consistent with the
    exact count.
- **Lemma `lem:coherent-linear-sde`.** P = 2n_F + 2(g+1)ℓ(e) expands to the
  stated g³ + 2g² + 5g + 4gℓ(p−2) + 2(g+1)ℓ(e).
- **Merge arities quoted in S9, S10 and S33.** CW = κ_d g_d + 1 and
  triangular = (g+1)(g+2)/2 match every quoted pair:
  - 6 vs 5;
  - 3, 6 vs 4, 5;
  - 3, 6, 10 vs 3, 7, 7.
- **Instance counts.** 30 oracle calls, 60 BCH passes and the bound 880;
  arities (2,5) and (5,3,7).
- **Lean.** Table `tab:lean-modules` sums to 417, the class-five rows sum to
  21, and `formal/Formal/Audit.lean` has 455 `#print axioms` lines
  (417 + 38).
- **Exponents.** `\ReesClassNineQueryExp` = 145, and 1 + Σ_{d≤9} d⌈log₂(d+1)⌉
  = 145. E_W(9) = 143, and E_W(9)+1 = 144 versus 146: consistent in all four
  places.
- **`numbers.tex`.** 163 macros = 148 + 15, as stated in the Reproducibility
  section.
- **Claim gates.** No sentence claims a human or independent review, novelty,
  a speedup, a general coherent receiver, a general SDE implementation or a
  checked formal compiler. "We claim no speedup" (rem:query-separation(c))
  and "only the use of the cover ... may be new, and this has not been
  established" are both present. See G1, G3, G9, G10 and I8 for wording that
  weakens these gates.

## Error (false or contradictory)

**E1. `main.tex:764` S38: the scope sentence is now false for the coherent
backends.**
- Quote: "with a classical solve between quantum segments".
- Why: the fourth and fifth backends, `rees_circuit_full.py` and
  `rees_circuit_coherent_c4.py` measure nothing before the final Fourier
  sampling and solve coherently (S8, S10, S16 and S33). Also, "the explicit
  transform is covered by the bound above" holds only for the F_3/F_5
  instances of the third backend and of `rees_circuit_full.py`. The F_7
  coherent circuits and the class-four circuits are counted with exact
  transforms only.
- Fix (replace S38–S39):
  ```latex
  These are fixed finite instances. The first three backends solve the diagonal equation classically between quantum segments; the coherent-label backends (the fourth, the fifth, \file{theorems/rees_circuit_full.py} and \file{theorems/rees_circuit_coherent_c4.py}) solve it coherently. Every exact simulation uses the exact Fourier transform; the explicit transform of Lemma~\ref{lem:qft-mod} is covered by the total-variation bounds above only for the third backend and \file{theorems/rees_circuit_full.py} at their instances over $\mathbb{F}_3$ and $\mathbb{F}_5$. None of these circuits is a coherent receiver for general $(G,H)$, and they test no asymptotic cost.
  ```

**E2. `main.tex:764` S22: the merge arities are misstated for the coherent
backends, and the "except" clause is ill-posed.**
- Quote: "the merge arities are the Chevalley--Warning arities, not the
  $B_d(g_d)$".
- Why: the coherent-label backends run at (g_d+1)(g_d+2)/2 when κ_d ≥ 2.
  S9 says "6 instead of 5", S10 "3 and 6 instead of 4 and 5", and S33
  "3, 6 and 10 instead of 3, 7 and 7". The clause "except that at grades with
  $p\notin E_2(\kappa_d)$ a coherent solve exists" makes the exception sound
  like a property of grades, when it is a property of backends. It also
  omits κ_d = 1, where E_2 is undefined and Lemma `lem:coherent-linear-sde`
  applies.
- Fix (replace S22):
  ```latex
  In the first three backends the diagonal equation is solved classically between quantum segments, at the Chevalley--Warning arities $\kappa_dg_d+1$, not the $B_d(g_d)$ of Theorem~\ref{thm:main}; the deterministic solver of Section~\ref{sec:sde} is used where the arity reaches its column count, exhaustive search otherwise. The coherent-label backends below solve it coherently instead, by Lemma~\ref{lem:coherent-linear-sde} at arity $g_d+1$ when $\kappa_d=1$ and by Lemmas~\ref{lem:coherent-quadratic-sde} and~\ref{lem:coherent-power-sde} at the arity $(g_d+1)(g_d+2)/2$ of Proposition~\ref{prop:triangular-sde} when $\kappa_d\ge2$ and $p\notin E_2(\kappa_d)$.
  ```

**E3. `appendix-schedule2.tex:473`: "Not shown" contradicts the exact E_2(7).**
- Quote: "does not determine $E_2(\kappa)$ for $\kappa \ge 7$".
- Why: line 470 of the same list, and `main.tex:626`, give E_2(7) exactly: 56
  primes, from an exact search below 5·10^6 > T_A(7) = 4.94·10^6.
- Fix: `does not determine $E_2(\kappa)$ for $\kappa \ge 8$;`

**E4. `main.tex:597`: "the reduction does not call it" conflicts with the
artifacts.**
- Quote: "It is a classical solver only: the reduction does not call it".
- Why: `theorems/rees_end_to_end_ext.py` and `theorems/rees_circuit_general.py`
  both import `rees_is_sde_solver`. `main.tex:486` ("the deterministic
  Ivanyos--Santha solver") and S22 ("the deterministic solver of Section
  sec:sde is used") say so too.
- Fix:
  ```latex
  It is a classical solver only: no proof in this paper depends on it, although the finite artifacts \file{theorems/rees_end_to_end_ext.py} and the measured-label circuit backends of Section~\ref{sec:uniform-compilation} call it; it has had no human review, and the general SDE step is not counted as implemented.
  ```

**E5. `appendix-subspace.tex:423` and `main.tex:1030`: "no quantum
implementation of ... the core/receiver exists".**
- Quote: "No quantum implementation of the preparer or of the core exists."
  and "no quantum implementation of the growth instrument or the receiver
  exists".
- Why: S0 generates explicit circuits "for the whole procedure", and four
  backends are coherent-label ones on small instances. The two places also
  word the same limit differently. The helper found the appendix instance; I
  verified it.
- Fix (both places, adapted):
  ```latex
  No implementation of the preparer (growth instrument) exists, and the core has explicit circuits only for the small fixed instances of the gate-level-control paragraph of Section~\ref{sec:uniform-compilation}, not for this source or for general $(G,H)$.
  ```

**E6. `appendix-torsion-blackbox.tex:729–733` (rem:tb-compiler): stale
implementation status.** Found by the helper; I verified it.
- Quote: "reduced exponents modulo $p$, so its certified prime-power coverage
  is $c \le 4$".
- Why: `main.tex:960` says the evaluator "now takes an annihilating modulus
  $p^e$". It agrees with the matrix logarithm and exponential at six test
  points with c ≤ 6.
- Fix:
  ```latex
  The project's implemented compiler (\file{theorems/universal_lazard_words.py}) originally reduced exponents modulo $p$, which limited its certified prime-power coverage to $c \le 4$ with $p > 4$ (\file{research/CLASS_FOUR_PRIME_POWER_INPUT.md}); it now takes an annihilating modulus $p^e$ and agrees with matrix logarithm and exponential in $\UT_{c+1}(\mathbb{Z}/p^e)$ at six test points with $c \le 6$ (\file{research/audits/reviews/2026-11-02-rees-prime-power-compiler.md}, Section~6); these are tests, not a proof of its contract.
  ```

**E7. `main.tex:652` (rem:triangular-scope): "the counts quoted in this paper
do not use that" is no longer true.**
- Why: the qubit and gate counts of the coherent-label backends (S9, S10, S16
  and S33) and Lemmas `lem:coherent-quadratic-sde` and
  `lem:coherent-power-sde` all run at (a+1)(a+2)/2.
- Fix:
  ```latex
  the query counts of Theorem~\ref{thm:main}, Remark~\ref{rem:combined-schedule} and Tables~\ref{tab:main-regimes}, \ref{tab:fcs-budget} and~\ref{tab:query-crossover} do not use that (only the coherent-label circuits of Section~\ref{sec:uniform-compilation} and Lemmas~\ref{lem:coherent-quadratic-sde} and~\ref{lem:coherent-power-sde} run at that arity), and adopting it is the owner's decision.
  ```

**E8. `main.tex:1241`: the reports are misdated.**
- Quote: "The numbers quoted from the AI-only reports of 1--2 November".
- Why: the list includes the gate counts of the Gate-level paragraph (3–4
  November reports) and the guard counts (class-five count of 4 November).
  The non-macro numbers of today's edits are missing from the list: the
  constants of Lemma `lem:qft-mod`, the coherent-lemma counts, the E_2(8)
  range from `2026-11-04-rees-threshold-5`, Table `tab:fcs-budget` and the
  zero-sum-node log₂Q values.
- Fix: `The numbers quoted from the AI-only reports of 1--4 November (for example ...`.
  Then add to the parenthetical list: `the constants of Lemma~\ref{lem:qft-mod}, the counts of Lemmas~\ref{lem:coherent-linear-sde}--\ref{lem:coherent-power-sde}, the zero-sum-node counts after Corollary~\ref{cor:fpt-r},`.

## Gap

**G1. The coherent-receiver scope is under-stated (`main.tex:775, 786, 797`).**
- The text says "it makes the solve ... coherent at every grade with
  $p\notin E_2(\kappa_d)$, in particular at every grade of every class-three
  instance". Its only stated reason that "the receiver is coherent there, not
  in general" is which instances are wired.
- A reader can then infer a general coherent receiver at every p outside
  ∪_d E_2(κ_d), which a claim gate forbids. The real missing pieces are not
  named:
  - the coherently controlled dilation (its cost "is not counted here");
  - the composition and error/gate analysis for general (G,H);
  - the grades with p ∈ E_2(κ_d), which include every κ_d = p−1 with p ≥ 5;
  - the fact that the arity is Prop. `prop:triangular-sde`'s, not
    Theorem `thm:main`'s.
- Fix (append after the first clause of line 797, before "it is wired only"):
  ```latex
  We do not claim a general coherent receiver: the coherently controlled dilation, the composition over all grades and its error and gate analysis for general $(G,H)$ are not carried out here; grades with $p\in E_2(\kappa_d)$, among them every grade with $\kappa_d=p-1$ and $p\ge5$, still need a classical solve; and these circuits run at the arity of Proposition~\ref{prop:triangular-sde}, not at the arities of Theorem~\ref{thm:main} or Remark~\ref{rem:combined-schedule}.
  ```

**G2. The QFT is still described only as imported (`main.tex:188`, `main.tex:571`).**
- Quotes: "a standard compilation of the quantum Fourier transform over $\Fp$
  (Theorem~\ref{thm:uniform-compilation}(iii))" and "the compilation of the
  quantum Fourier transform, imported".
- Why: Thm `thm:uniform-compilation`(iii) now also points to the explicit
  Lemma `lem:qft-mod`, and Thm `thm:bb-envelope` says that (H1) "is proved as
  Lemma qft-mod". The list of imported ingredients should say which option is
  meant.
- Fix at line 188:
  ```latex
  and a compilation of the quantum Fourier transform over $\Fp$ (Theorem~\ref{thm:uniform-compilation}(iii)), either imported from~\cite{Kitaev1995} or given explicitly by Lemma~\ref{lem:qft-mod} (AI-checked, pending human review)
  ```
  Fix at line 571: `and the compilation of the quantum Fourier transform, imported as stated after Theorem~\ref{thm:main} or supplied by Lemma~\ref{lem:qft-mod};`

**G3. The Lean boundary does not exclude the circuit material (`main.tex:1237`).**
- The "Outside the boundary" list does not mention Lemma `lem:qft-mod`, the
  coherent witness circuits or the generated circuits. Without that, a reader
  could take the Lean section and the gate lists together as a checked
  compiler.
- Fix (append to the list):
  ```latex
  , Lemma~\ref{lem:qft-mod}, the coherent witness circuits of Lemmas~\ref{lem:coherent-linear-sde}--\ref{lem:coherent-power-sde} and every generated circuit of Section~\ref{sec:uniform-compilation}; no formally checked compiler is claimed
  ```

**G4. It is unclear whether `Audit.lean` was rebuilt after the class-five guards
were added (`main.tex:1187`).**
- Quote: "a \texttt{lake build} of them succeeded ..., their $21$ guards were
  then added".
- Why: the claim that all 417 guards permit only propext, Classical.choice and
  Quot.sound needs `Audit.lean` to be built after those 21 guards were added.
  The text does not say that it was.
- Fix: say explicitly whether an in-place `lake build --wfail` of
  `formal/`, including `Formal/Audit.lean`, ran after the guards were added.
  If none did, add `; the guards themselves have not been built`.

**G5. `main.tex:764` S35: the ninth subgroup of the class-four coherent run is
unexplained.**
- Quote: "for eight of the nine hidden subgroups".
- Fix: state what happened to the ninth (not run, time-out or failure), for
  example `(the ninth was not run: <reason>)`.

**G6. Lemmas `lem:coherent-*` have only proof sketches but state exact counts
(`main.tex:766–797`).**
- Their exact multiply-accumulate, Toffoli and qubit counts rest on a "Proof
  sketch" and on gate lists checked only on small (p,a).
- Lemma `lem:coherent-power-sde` also depends on Props. `prop:triangular-sde`
  and `prop:decoupled-sde`, which are themselves AI-checked and conditional.
- Fix: in all three headers write `[...; proof sketch, counts from the
  generated gate lists; AI-checked, pending human review]`. In
  `lem:coherent-power-sde` add `conditional on
  Proposition~\ref{prop:triangular-sde}`.

**G7. The Organization paragraph omits today's additions (`main.tex:232`).**
- Quote: "discusses gate compilation and the benchmark resource profiles".
- Fix:
  ```latex
  Section~\ref{sec:uniform-compilation} discusses gate compilation, an explicit approximate Fourier transform (Lemma~\ref{lem:qft-mod}), coherent witness circuits for the diagonal equation (Lemmas~\ref{lem:coherent-linear-sde}--\ref{lem:coherent-power-sde}), finite circuit artifacts and the benchmark resource profiles.
  ```

**G8. `appendix-torsion-blackbox.tex:45` overstates what the appendix proves.**
Found by the helper; I verified it.
- Quote: "Everything else below is proved here."
- Why: Lemma `lem:tb-small-primes` imports Imran–Ivanyos, and Lemma
  `lem:tb-sylow`(d) imports Shor's algorithm and AKS.
- Fix:
  ```latex
  Everything else below is proved here, except the cited results of Imran and Ivanyos (Lemma~\ref{lem:tb-small-primes}), Shor's order finding and factoring, and the AKS test (Lemma~\ref{lem:tb-sylow}(d)).
  ```

**G9. `appendix-codimension.tex:278`: a result title carries no AI caveat.**
Found by the helper; I verified it.
- Quote: "[Classical collision learner; proved]".
- Fix: `[Classical collision learner; proved here, AI-checked, pending human review]`

**G10. `appendix-codimension.tex:327`: an AI check is called "independent"
(claim gate).** Found by the helper; I verified it.
- Quote: "an independent check (…2026-11-03-rees-check-app-e.md)".
- Fix: `a separate AI check (\file{research/audits/reviews/2026-11-03-rees-check-app-e.md}; AI-checked, pending human review)`

**G11. Rabin's splitting step is not credited (`appendix-schedule3.tex:150–158`,
Lemma `lem:s3-root`).** Found by the helper. I verified that the
only "Rabin" strings in the file are in source comments.
- Fix: after the statement add `This is Rabin's splitting procedure~\cite{Rabin1980}, with explicit caps.`

**G12. Some propositions carry no per-result AI caveat.**
- Props. `prop:single-evaluation` and `prop:refresh` are not in the "steps
  behind Theorem main" list of line 571. Prop. `prop:conjugation` (line 1058)
  has no AI caveat either. Only the status box covers them.
- Fix: add `(AI-checked, pending human review)` to their headers, or extend the
  list in line 571.

**G13. (H2) is still a hypothesis although its main case is now constructed
(`appendix-torsion-blackbox.tex:1226`).**
- Why: Lemma `lem:qft-mod`'s proof and the second backend build modular
  multiplication from cited adders, in at most 158b²+46b gates. Inversion,
  at O(log³ p), is the case not covered.
- Fix (optional): `(H2) a field operation modulo $p$ costs $O(\log^2 p)$ gates (multiplication is constructed in the proof of Lemma~\ref{lem:qft-mod}; inversion by Fermat exponentiation costs $O(\log^3 p)$, which does not change the stated exponents)`.
  The parenthetical is valid only if that last clause is true; check it
  against Proposition `prop:tb-count-gates`(a).

## Imprecision

**I1. `main.tex:764` S11–S15: the explicit-transform error block is misplaced.**
- The block starts "By a hybrid argument over the transforms ..." and ends
  "... at most $0.6$ times the proved bounds". It sits after the fifth
  (F_7) backend but concerns the third backend at F_3/F_5: 148 transforms,
  154 and 835 qubits, measured labels.
- Fix: move it directly after S7 and start it
  `For the third backend, by a hybrid argument over the transforms, ...`.
  See S1 below.

**I2. `main.tex:764` S23: "proved" is used for finite checks.**
- Quote: "Each merge gate list is proved, on all canonical inputs, ... by
  exhaustive checks ... and a symbolic replay".
- Fix: `Each merge gate list of the first backend is checked, on all canonical inputs, ...`

**I3. `main.tex:764` S9: the parenthetical is ambiguous.**
- Quote: "($3$, resp.\ $6$ instead of $5$)".
- Fix: `($3$ over $\mathbb{F}_3$, equal to the Chevalley--Warning arity, and $6$ instead of $5$ over $\mathbb{F}_5$)`

**I4. `main.tex:790`: the symbol m is undefined in `lem:coherent-power-sde`.**
- Quote: "The circuit takes $m$, $g$ and $(\alpha,\beta)$ as classical
  parameters".
- Why: m (the non-residue of Lemma `lem:coherent-quadratic-sde`) does not
  occur in this lemma.
- Fix: `The circuit takes $g$ and $(\alpha,\beta)$ as classical parameters`.

**I5. The trial ranges differ between body and appendix.**
- `main.tex:675` gives "between $2^{223.8}$ and $2^{236.0}$ ... at the four
  primes of that table". `appendix-free-coordinate.tex:312` gives "between
  $2^{193.9}$ and $2^{236.0}$ ... at the six primes of~(b)".
- Both may be right, for different prime sets, but read as a contradiction.
- Fix (appendix): `between $2^{193.9}$ and $2^{236.0}$ at the six primes of~(b) (between $2^{223.8}$ and $2^{236.0}$ at the four of them in Table~\ref{tab:fcs-budget})`

**I6. `appendix-schedule2.tex:470`: an unclear parenthetical.**
- Quote: "(primes below $2442$ for $\kappa = 8$ and below $3584$ for
  $\kappa = 9$: ...)".
- Why: it is not said what these bounds are (an earlier decided range?).
  2442 and 3584 are not primes.
- Fix: `(an earlier search had decided the primes below $2442$ for $\kappa = 8$ and below $3584$ for $\kappa = 9$: ...)`, if that is what they are.

**I7. `main.tex:626` and `appendix-schedule2.tex:470`: 17659 lies outside the
decided range.**
- Quote: "decides every prime $p \equiv 1 \pmod 9$ up to $13537$ ... and shows
  ... $17659 \in E_2(9)$".
- Why: 17659 > 13537, so it was decided individually. As written, it reads as
  part of the range.
- Fix: `and, by a separate run, shows $17659 \in E_2(9)$`.

**I8. "Independent" is used for AI-run checks (claim gate).**
- Places: `appendix-schedule2.tex:439` ("A third independent search ... run
  twice, independently"), `:470` ("independent complete search", "checked
  by an independent program") and `main.tex:76` ("Independent automated
  referee passes").
- Fix: `separately written AI-run search` / `checked by a separately written program` / `Separate automated (AI) referee passes`.

**I9. `docs/papers/rees-hsp/README.md` is stale.**
- Its status is dated 2 November and it quotes "365 guards". It does not
  mention class five, the explicit transform or the circuit backends.
- It also says "`main.tex` inputs each one only if it exists", but
  `main.tex:1252–1257` uses unconditional `\input`.
- Fix: add a 4 November update paragraph with 417/455 guards, class five, the
  explicit QFT and the coherent-label backends (AI-checked, pending human
  review). Replace the input sentence with "`main.tex` inputs each one."

**I10. `appendix-torsion-blackbox.tex:749` cites Kitaev for the transform.**
Found by the helper; I verified it.
- Quote: "(Kitaev, \arxivid{quant-ph/9511026})".
- Why: Prop. `prop:tb-count-gates`(b) counts these transforms by Lemma
  `lem:qft-mod`.
- Fix: `(coordinatewise by Lemma~\ref{lem:qft-mod} with $N = p^e$; cf.~\cite{Kitaev1995})`

**I11. `main.tex:904` and `appendix-codimension.tex:47` differ on the query
bound.** Found by the helper.
- The body says poly(m,w,log 1/ε) queries; the appendix says
  poly(m,log 1/ε). They are consistent, but the appendix bound is the one
  proved.
- Fix: in `main.tex:904` use `\poly(m,\log(1/\eps))` oracle queries.

**I12. `appendix-schedule3.tex:312`: the reason given for the growing exponent
is vague.** Found by the helper.
- Quote: "grows with $c$, because the arity depends on $g_d$".
- Fix: `because the Schedule~1 arity $B_d(g_d)$ has degree $d\lceil\log_2(d+1)\rceil$ in $g_d \le m$`.

**I13. `appendix-torsion-blackbox.tex:1283`: the justification proves less than
stated.** Found by the helper; I verified it.
- Quote: "$E_W(c) \ge \max(c, 5)$ for $c \ge 2$ because every $e_d \ge 1$".
- Why: e_d ≥ 1 gives only E_W(c) ≥ c.
- Fix: `because every $e_d \ge 1$ gives $E_W(c) \ge c$, which is at least $5$ for $c \ge 5$, and Lemma~\ref{lem:tb-count-exponent} gives $E_W(2),E_W(3),E_W(4) = 5,11,23$.`
  Do not argue by monotonicity in c: the maximum runs over p > c, so it is
  not automatically monotone.

## Style

**S1. Split the Gate-level control paragraph (`main.tex:764`, about 2000
words).**

Proposal, using the S-numbers of the sentence split defined at the top:

```latex
\paragraph{Gate-level control.} % S0, S1, S2, then S20, S21, S22 (replaced as in E2), S23 (as in I2), S24, S25, S26
...
\paragraph{Binary arithmetic and explicit transforms.} % S3, S4, S5, S6, S7, then S11 (beginning "For the third backend, by a hybrid argument over the transforms, ..."), S12, S13, S14, S15
...
\paragraph{Coherent-label backends.} % S8, S9 (as in I3), S10, then the class-four sentence below, S34, S35 (with G5), S36, S37, then S16, S17, S18, S19
...
\paragraph{Instances.} % S27 to S32, then the first half of S33 below
...
\paragraph{Scope.} % replacement text of E1
```

S33 should become two sentences. The first stays under "Instances":

```latex
The class-four circuits over $\mathbb{F}_7$ ($16302$ qubits per terminal sample, plus the $3b+5=14$ arithmetic ancillas) are generated and counted.
```

The second opens the class-four part of "Coherent-label backends":

```latex
A coherent-label version of these class-four circuits over $\mathbb{F}_7$, \file{theorems/rees_circuit_coherent_c4.py} (report \file{research/audits/reviews/2026-11-04-rees-circuit-coherent-c4.md}; finite computation, AI-checked, pending human review), uses the circuits of Lemmas~\ref{lem:coherent-quadratic-sde} and~\ref{lem:coherent-power-sde} at grades four, three and two ($\kappa_d = 2, 3, 2$; merge arities $3$, $6$ and $10$ instead of $3$, $7$ and $7$), so that one terminal sample uses $20566$ qubits ($10800$ of them oracle outputs; no reuse) and $83492540$ gates excluding the oracle and $3330$ exact transforms; its merge blocks ...
```

The rest continues as in S33.

Two notes on the move:
- With S20–S26 placed right after the first backend, "The circuits"
  refers unambiguously to the common structure.
- The forward references "the class-three filiform algebra over $\mathbb{F}_5$
  below" in S5, S8 and S12 then point to the "Instances" paragraph; replace
  "below" by "of the Instances paragraph".

**S2. Notation clashes in the coherent lemmas (`main.tex:768–797`).**
- They use m (the non-residue), g (the coset generator), ρ(x) (the root),
  P (the power subgroup, and also the multiply-accumulate count), Q (the odd
  part), S (the 2-adic valuation) and u (the Bezout exponent).
- These clash with m = dim L, g_k, ρ_H, P = ∏M_d, Q (query count),
  S (number of samples) and u (Schedule 3).
- `main.tex:243` lists u, Q, S, P but not m, g, ρ.
- Fix: add `$m$, $g$, $\rho$, $e$` to the list in line 243, or rename:
  m→ν, the count P→N_{MA}, ρ(x)→r(x).

**S3. `main.tex:783`: K in −e_{K+1} is undefined.**
- Quote: "the coordinates of $-R$ are those of $-e_{K+1}$".
- Fix: use the round index of Proposition `prop:triangular-sde`, so
  `$-e_{k+1}$`.

**S4. `main.tex:626`: the cross-reference is textual.**
- Quote: "(Appendix~\ref{app:schedule2}, scope list, with sources)", twice.
- Fix: `(Section~\ref{app:s2-scope}, with sources)`. The label `app:s2-scope`
  exists and is unused.

**S5. Minor appendix items** (found by the helper; the first two verified):
- `appendix-torsion-blackbox.tex:1151`: "checked directly" twice in a row.
- `appendix-torsion-blackbox.tex:1065`: the abbreviation "II call" is
  undefined.
- `appendix-codimension.tex:296`: a doubled comma ("$c$,,").
- `appendix-torsion-blackbox.tex:88, 749`: Trappeniers and Kitaev are cited
  inline by arXiv ID although the keys `Trappeniers2024` and `Kitaev1995`
  exist.
- `appendix-torsion-blackbox.tex:1226`: the sentence defining (H1)–(H3) runs
  to about 150 words; split it into one sentence per hypothesis.

**S6. Stale source comments** (not rendered):
- `appendix-torsion-blackbox.tex:14–15` says thm:bb-envelope "is not defined
  in main.tex yet"; it is now defined.
- `:32` suggests the key Kitaev1995 as new; it already exists.
- `appendix-schedule3.tex:15` and `appendix-free-coordinate.tex:15` say
  "B <= 7 + ...", while the proved bound is 6 + ....

## Counts

| Class | Count |
|---|---|
| Error | 8 |
| Gap | 13 |
| Imprecision | 13 |
| Style | 6 (S5 bundles 5 items, so 16 in all) |
