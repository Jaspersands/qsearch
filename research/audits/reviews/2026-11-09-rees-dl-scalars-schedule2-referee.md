# Referee: DL central scalars and Schedule 2 on invalid branches (9 Nov 2026)

Independent adversarial check of two claims added to the prepared (unapplied) revision in
`research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree/` (`core/main-core.tex`, `main.tex`).
Labels and the author's README summary were not trusted; every step below was re-derived or
recomputed. No existing file was edited. New scripts and outputs are in
`research/audits/reviews/2026-11-09-rees-dl-scalars-schedule2-referee/` (section 1.4).

| Claim | Verdict |
|---|---|
| 1. `prop:dl-central-scalars` (core l.409, main l.464) | **CORRECT** (proof complete for every field of char not 2, char 3 included); two wording GAPs in the sentences that cite it |
| 2. README 1e Task 3: worst-case cost of Theorem main with the combined rule on every oracle; e_p > 1 in `thm:bb-envelope` | **CORRECT in substance**, no promise-dependent unbounded branch found; four precision GAPs, one of which (G2.1) is a missing sentence in `main.tex` that the argument needs |

---

## 1. Proposition prop:dl-central-scalars

### 1.1 Definition

Both papers use the same bracket table (core l.387-392, main l.~440): nonzero brackets
[e1,e2]=e5, [e1,e3]=e6, [e1,e4]=e7, [e1,e5]=-e8, [e2,e3]=e8, [e2,e4]=e6, [e2,e6]=-e7,
[e3,e4]=-e5, [e3,e5]=-e7, [e4,e6]=-e8. Checked: Jacobi holds identically (0 failures over all
512 basis triples, over Q(i)); gamma2 = span(e5..e8) (directly from the table), gamma3 =
span(e7,e8) ([e1,e5], [e2,e6]), [gamma2,gamma2] = 0 (no bracket among e5..e8), gamma4 = 0.

### 1.2 Proof, line by line

- *Centre.* For x = sum c_j e_j: [e1,x] = c2 e5 + c3 e6 + c4 e7 - c5 e8 and
  [e2,x] = -c1 e5 + c4 e6 + c3 e8 - c6 e7, so c1..c6 = 0. Valid in every characteristic. OK.
- *Basis change.* u1,u3 span span(e1,e4) iff det((i,1),(-i,1)) = 2i is nonzero; u2,u4 and v+-
  likewise (determinants 2i, -2i). Needs exactly char not 2. All 15 displayed brackets
  ([u1,u2]=2v+, [u3,u4]=2v-, [u1,u3]=2ie7, [u2,u4]=-2ie8, [u1,u4]=[u2,u3]=0, [u1,v+]=-2ie8,
  [u2,v+]=-2e7, [u3,v-]=2ie8, [u4,v-]=-2e7, [U+,v-]=[U-,v+]=0, [v+,v-]=0) recomputed
  symbolically over Q(i): all correct.
- *Shape of phi.* gamma2, gamma3 are characteristic; A is the induced map on L/gamma2 (invertible),
  M the induced map on gamma2/gamma3. [phi x, phi v] = [Ax, Mv] uses [gamma2,gamma2]=0 and
  gamma3 central. OK.
- *Rank-one locus.* For x in U, ([x,L]+gamma3)/gamma3 = ([x,U]+gamma3)/gamma3 because
  [x,gamma2] is in gamma3; the only brackets of U x U not in gamma3 are [u1,u2] and [u3,u4], and
  the induced form on each U+- is a nondegenerate alternating form, so [x+,U+] = Kv+ whenever
  x+ is nonzero. Hence the dimension is (x+ != 0) + (x- != 0). The dimension depends only on
  x mod gamma2 and is phi-invariant (phi[x,L] = [phi x, L]). A 2-dimensional subspace inside
  U+ union U- lies in one of them (over any field). So A preserves or swaps U+-. OK.
- *Keep case.* [Pu1,Pu2] = det(P)[u1,u2] mod gamma3 gives Mv+ = det(P)v+; then
  zeta psi+ = det(P) psi+ P with psi+ bijective forces P = mu id, det P = mu^2, mu^3 = zeta;
  same for Q. In [phi u1, phi u3] the correction terms are mu[u1,b(u3)] and -nu[u3,b(u1)];
  [u1,b] is in K[u1,v+] = Ke8 and [u3,b] in K[u3,v-] = Ke8 (because [U+,v-] = [U-,v+] = 0), and
  [b,b'] = 0, so the e7 coefficient gives zeta = mu nu. Then nu = zeta/mu = mu^2,
  zeta = nu^3 = mu^6 = zeta^2, zeta = 1. OK. (This step uses the specific vectors u1, u3: for
  general vectors of U+- the correction terms span all of gamma3, which is why the e7-coefficient
  trick needs exactly this pair. It is used correctly.)
- *Swap case.* psi-^{-1} psi+ : u1 -> -u3, u2 -> u4 (from psi+(u1) = -2ie8 = -psi-(u3),
  psi+(u2) = -2e7 = psi-(u4)), determinant -1; so P = alpha R, det P = -alpha^2,
  alpha^3 = -zeta; same for beta. phi u1 = -alpha u3 + ..., phi u3 = -beta u1 + ...;
  [-alpha u3, -beta u1] = -2i alpha beta e7, corrections again in Ke8, so zeta = -alpha beta,
  zeta^3 = -alpha^3 beta^3 = -(-zeta)(-zeta) = -zeta^2, zeta = -1. OK.
- *Converse.* The sign map (+ on e1,e3,e6; - on e2,e4,e5,e7,e8) preserves all ten brackets
  (checked by hand, each sign product). Defined over Z, so over every K. OK.
- *Reduction to K algebraically closed.* An automorphism over K extends to K-bar with the same
  zeta; the statement is "exists over K iff zeta = +-1", and both directions descend. OK.
- *Characteristic edge cases.* Nothing divides by 3 or by any prime other than 2. Char 3 is
  covered by the proof (i lies in F_9). The "in particular" is restricted to p > 3 = class, which
  is exactly the Lazard range; for p = 3 only the Lie-algebra statement is claimed. The group
  statement z -> z^zeta matches zeta times log z on the centre. No small-p issue arises.

### 1.3 Abstract / intro sentences that rely on it

- Core abstract (l.59): "the elimination ... needs automorphisms that preserve H and scale the
  centre by prescribed scalars, and such automorphisms need not exist: ... its automorphisms act
  on its centre by a scalar only when that scalar is +-1." Follows: with H = 1 the requirement is
  exactly a scalar action on the whole centre, and the solver's scalars s range over F_p.
- **GAP W1 (core l.79).** "...only when that scalar is +-1 (Proposition), so no automorphism of G
  scales the top grade as a dilation does." Literally false for theta = -1 (the sign map acts as
  delta_{-1} would, by (-1)^3) and for theta^3 = 1 (the identity). The body (core l.434, main
  l.489) has the correct qualifier "once theta^3 != +-1". Fix: append "for any theta with
  theta^3 != +-1", or say "no family of automorphisms realizes the scalings theta^3 for all
  theta".
- **GAP W2 (core l.260, main l.254).** "Proposition ... shows that some such step is needed: for
  the Dixmier-Lister algebra no automorphism of G supplies the scalars." The proposition shows
  only that automorphisms of G supply no central scalars other than +-1; it does not show that
  the cover step is necessary for every algorithm. Fix (core): "Proposition ... shows that for
  the Dixmier-Lister algebra the scalars cannot come from automorphisms of G (only +-1 occur)".
  Main l.254 ("no automorphism of G supplies the scalars") is acceptable if "beyond +-1" is
  added.
- Side remark, not a defect: when H meets the centre nontrivially the IS elimination needs
  scalar action only on the label space (characters of Z/(H cap Z)), which the proposition does
  not address. The abstract's "need not exist" is witnessed by H = 1, so nothing claimed depends
  on this. If a future text says "for every H", it would need the image group on the centre and
  its eigenvalues (order 4 at p = 5, D12 at p = 7 per GAP), not just its scalars.

### 1.4 Independent computation

Independent of the author's GAP/brute-force checks: Gröbner bases (Sage 10.9 / Singular, `nice
-n 19`), with scripts and outputs in `2026-11-09-rees-dl-scalars-schedule2-referee/`
(`dl.sage`, `dl3.sage`, `der.py`, `results.out`). Unknowns: the images of e1..e4 in span(e1..e6),
with phi(e5..e8) defined as the brackets of those images; equations: every bracket of the table
(and every zero bracket) is preserved, phi(e7) = zeta e7, phi(e8) = zeta e8, t det(A) = 1. For
each zeta in F_p^x the test "the ideal plus (zeta - c) is the unit ideal" decides whether an
automorphism **over the algebraic closure of F_p** acts on the centre as c. This is stronger than
an F_p-point count.

- `dl.sage`, all 26 unknowns: p = 3: zeta in {1, 2} both occur; p = 5: only {1, 4}.
- `dl3.sage`, on a slice: the e5, e6 components of phi(e1), phi(e2) are set to 0. This is WLOG:
  `der.py` checks that De1 = l e5 + m e6, De2 = -n e5 + r e6, De3 = -r e5 - n e6,
  De4 = m e5 - l e6, De5 = m e7 + n e8, De6 = l e7 + r e8 is a derivation for all l, m, n, r. Then
  exp(D) = 1 + D + D^2/2 is an automorphism in char != 2 (brackets [D^k x, D^l y] with k + l >= 3
  vanish), it is the identity on gamma3, and phi o exp(D) changes the e5, e6 components of
  phi(e1), phi(e2) by M(l e5 + m e6) and M(-n e5 + r e6), with M invertible. Results:
  p = 3: {1, 2}; p = 5: {1, 4}; p = 7: {1, 6}; **p = 11: only {1, 10}**, so all eight other
  scalars are excluded over F_11-bar. The author's GAP run did not finish at p = 11. p = 3, 5
  agree with the unsliced run.
- Not obtained: p = 13 (600 s time-out) and the elimination over Q (300 s time-out). The direct
  enumeration of the slice variety (to recount |Aut| = 4·5^12 and 12·7^12) was also stopped
  before it produced output. These GAP orders are therefore not independently re-derived here;
  the scalar sets are.
- Total CPU for this claim: about 35 core-minutes.

These are finite controls that agree with the proof. The proof itself is the basis of the
verdict.

---

## 2. Schedule 2 / combined rule on invalid branches (README 1e Task 3)

Read: `docs/papers/rees-hsp/appendix-schedule2.tex` (identical to `tree/appendix-schedule2.tex`
apart from E2-UPDATE comments and the kappa = 8, 9 numbers paragraph; Theorem
`thm:app-s2-main` and its proof are byte-identical), `tree/main.tex` sec:recursion (l.609-641),
thm:is-import and rem:is-runtime, thm:power-sde, rem:combined-schedule (l.758), proof of
thm:main (l.1040), rem:oblivious (l.1048), thm:ring-to-field (l.1206), cor:black-box-pe
(l.1283), thm:bb-envelope (l.1307), and `tree/appendix-torsion-blackbox.tex` Prop
tb-recursion (l.407-450).

### 2.1 Branch-by-branch audit

| Step (combined rule, no block-steered option) | Cost on an arbitrary function oracle | Depends on promise? |
|---|---|---|
| Lifted sources, instruments, dilations, quotient conversion, Fourier readout | fixed gate count set by p, m, g_d, eps; recursion tree and N_instr fixed before the run | no |
| Arity choice per grade | from (p, d, g_d) only (rem:combined-schedule l.760) | no |
| Linear grade (kappa_d = 1) | one elimination on g_d + 1 columns | no |
| Schedule 1 grade (degree kappa_d, arity B_kappa(g_d)) | thm:is-import is stated for arbitrary columns; at most nu+1 internal runs (rem:is-runtime) | no |
| Schedule 2 grade (p >= 16 kappa^{2kappa+2}, public test) | Phase 0: at most J + sum K_j draws, each <= kappa coset tests; Phase 1: <= k+1 runs cut at 2T_1; exact check; "any columns" (thm:app-s2-main) | no (see G2.2 on what a "draw" costs) |
| Solver attempts per merge node | <= ceil(log2(3 N_solver/eps)), each cut at 2T; retries reuse the saved labels, no new queries | no |
| Restarts | only in prop:mixed-schedule / thm:free-coordinate(ii),(iv), not used by the rule (checked by grep: the only other "restart" is the bounded IS Section 3.1 run count) | no |
| Rank step, nullspace | m + tau samples, fixed | no |
| e_p > 1: RtF of Prop tb-recursion | <= b' <= L calls on every branch; stop rule 2 rejects non-subalgebras, so every section met is a genuine section N/K and its socle is an F_p-Lie algebra of class <= c (well-definedness paragraph, "whatever the earlier calls returned"); kernel/chart checks bound b' <= L; Howell/Smith arithmetic deterministic | no |

The hiding property enters only the correctness proofs (descent exactness, rank, Prop
tb-recursion's error bound). A wrong earlier call yields a valid instance format with a
non-hiding oracle, which is precisely the case rem:oblivious covers. So the conclusion of Task 3
holds: thm:bb-envelope's e_p > 1 case needs, beyond Theorem main, only thm:power-sde(ii)
through the combined rule (and the AI-checked Prop tb-recursion, which was already a proved
ingredient, not a condition). The query count of the combined rule is at most Q_q, since
B_kappa(g) <= B_d(g), g+1 <= B_d(g) and (g+1)((kappa-1)g+1) <= B_d(g) for kappa <= d.

### 2.2 Gaps (none changes the verdict; each has a one-sentence fix)

- **G2.1 (main.tex, needed by the argument).** README item 4 says "Measured labels are always
  canonical vectors of F_p^{g_d} ..., whatever f is". False for the *implemented* instruments:
  sec:recursion and Lemma hybrid (main l.629-640) explicitly allow implemented states to leak out
  of the canonical subspace, so a measured coordinate register (ceil(log2 p) bits) can hold an
  integer >= p, on valid and invalid oracles alike. thm:app-s2-main and thm:is-import are stated
  for columns in F_p^a, so "any columns" does not by itself cover such strings. The core paper
  has the fix (core l.650: "Classical steps are defined on every bit string: a label coordinate
  holding a value >= p is reduced modulo p before the solver runs"); main.tex has no such
  sentence (grep for "reduc* mod", "every bit string", "non-canonical": none in the relevant
  sections). Fix: add the core sentence to main sec:recursion (approximation item) or to
  rem:oblivious, and drop "always canonical" from the README.
- **G2.2 (cost of a draw; rem:oblivious "every draw loop ... is capped").** thm:app-s2-main
  counts F_p operations and treats a uniform draw from F_p^x / F_p as one step. In the paper's own
  fair-bit model (main l.767, Schedule 3: rejection from ceil(log2 p) coins, accepted when below
  p) a single draw has no worst-case bound; Schedule 3 explicitly caps fair-bit sampling and
  root extraction, Schedule 2 does not. Phase 1 is covered by its 2T_1 cut-off, and every call is
  covered by the recursion's 2T cut-off per attempt *if Phase 0 runs inside the attempt*. But
  rem:app-s2-four allows Phase 0 to be hoisted out ("run once per distinct kappa_d and reused"),
  which puts it outside any cut-off. Fix: in rem:oblivious say "each Schedule 2 call, Phase 0
  included, runs inside the per-attempt cut-off of Section recursion (or its fair-bit draws are
  capped as in Schedule 3)", or cap the draws in thm:app-s2-main.
- **G2.3 (error split, sec:recursion "Solvers" item).** "By Markov's inequality an attempt then
  fails with probability at most 1/2" is right for a Las Vegas solver that never aborts. Schedule
  2 as stated in thm:app-s2-main also aborts (<= 2^{-k}); with T its expected time, an attempt
  fails with probability up to 1/2 + 2^{-k}, and the attempt count ceil(log2(3N/eps)) is then not
  justified as written. Harmless if T is taken as the worst-case bound of thm:app-s2-main (then
  the cut-off never fires and failure is <= 2^{-k} <= 1/2) or with cut-off 4T and k >= 2. Fix: one
  clause. This is a correctness-budget slip, not a cost issue.
- **G2.4 (scope wording of rem:oblivious).** "for every unitary U_f of label width w": a literal
  arbitrary unitary may act on the address register, so the uncomputation steps leave garbage;
  gate and query counts are still fixed, and with G2.1 the classical side is total, so the bound
  survives, but every use in the paper (cor:black-box-pe, thm:bb-envelope, Prop tb-recursion)
  only needs "every function f : G -> {0,1}^w with its standard oracle U_f". Suggest that
  wording.
- **Note (explicit T).** The cut-offs at 2T and 2T_1 need T as an explicit function of the public
  data. thm:bb-envelope(iii) says "the Schedule 2 calls are not bounded here, so beta_c is not
  computed". This is not a contradiction (any fixed implementation has some explicit polynomial
  bound, and that is all an existence statement needs), but the text should say that T is the
  explicit expected-time bound of the fixed implementation, or replace the Phase 1 cut-off by an
  iteration cap on each root extraction.

### 2.3 Checked and found consistent

- thm:ring-to-field(iii) still says "Each call is stopped at the solver's time bound for valid
  inputs"; Prop tb-recursion keeps the time-out but its proof now says it is not needed for
  Solve = Theorem main. Consistent, and the time-out is harmless.
- thm:bb-envelope status line ("conditional on Theorem main and on Theorem power-sde(ii) through
  the combined rule. The primes with e_p > 1 add no condition") matches the audit, given G2.1-G2.3.
- cor:black-box-pe on erroneous kernel branches: K' subset of ker Phi is enforced by the public
  check, so Phi-bar is a homomorphism and C = F/K' a Lazard ring of class <= c with
  b' <= L; the oracle f o Phi-bar is a function. No promise-dependent branch.
- A Schedule 2 abort after all attempts: whatever the recursion outputs, in RtF it is "returning
  nothing" (U = 0) and stops; bounded either way. The paper could say once what an aborted merge
  node outputs (e.g. an abort flag, counted by Lemma hybrid).
