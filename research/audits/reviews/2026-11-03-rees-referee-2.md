# Referee report 2: Rees HSP manuscript (docs/papers/rees-hsp/main.tex + appendices A-F)

Date: 2026-11-03 (written 2026-11-02 evening). Unanchored: read from the paper only, not from project audit reports.
Scripts: research/audits/reviews/2026-11-03-rees-referee-2/ (core_check.py, core_check_out.txt).
Reviewer: AI referee (not a human review).

Status: COMPLETE. Sections were appended as they were completed; numbering below follows the brief.

## 0. Summary of the submission (as I read it)

For a finite p-group G = (L, *) of class c < p given by an explicit Lazard Lie algebra L = F_p^m and an arbitrary
hidden subgroup H, the paper queries f at c evaluations E_s, s = 1..c, of the positive lower-central Rees cover
A = sum_k t^k gamma_k(L). The tuple oracle hides the homogeneous subgroup exp(sum_k t^k (h cap gamma_k)), which every
dilation preserves. Grade-by-grade central character measurement and a controlled-right-action conversion,
with dilation weights from a homogeneous system of diagonal equations solved by Ivanyos-Santha, peel off grades
c, ..., 2; grade 1 retains all of h = log H, which Fourier sampling recovers. The main claim (thm:main) is a
bounded-error algorithm polynomial in m, log p, w, log(1/eps) for each fixed c. The rest of the paper (about 90 of
106 pages) is extensions, conditional corollaries, resource tables, simulations and a Lean inventory.

Verdict: **major revision** (Section 5). Core theorem: no error found. Top findings: F1/F2 (statement), 2.1
(Appendix B hybrid), 2.5 (bb-envelope counting), 2.0 and Section 3 (labelling, form).

---
(Appended 2026-11-02, first pass through main.tex lines 1-460.)

## 1 (findings). Theorem thm:main: correctness for every H

I re-derived every step of the Schedule-1 assembly (main.tex lines 233-459) from the definitions, without
using the project's audit reports.

**1.1 Tuple lift (lem:homogeneous, lines 259-271). Correct for every H.** With C = log(a^{-1}*b) = sum_k t^k C_k,
f-hat(a) = f-hat(b) iff E_{s_i}(C) = sum_k s_i^k C_k lies in h for i = 1..c (E_s is a BCH homomorphism and
log = id on coordinates). The c x c matrix (s_i^k) is invertible for distinct nonzero s_i, and h is a subspace,
so this holds iff every C_k lies in h, i.e. C lies in h-tilde. h-tilde is a homogeneous Lie subalgebra
([t^i x, t^j y] = t^{i+j}[x,y] with [x,y] in h cap gamma_{i+j}), hence exp(h-tilde) is a subgroup, and every
delta_lambda preserves it. Nothing uses normality of H. p > c guarantees c distinct nonzero points.
Only Lazard input used: h = log H is an F_p-subalgebra for every subgroup H (exponent p, class < p). Correct.

**1.2 Copy lift (lem:copy-lift, lines 308-320). Correct.** R is a homomorphism (R_g R_h = R_{gh} for
R_g|x> = |x g^{-1}>), so tr(R_{E(a)} rho_H R_{E(b)}^dagger) = tr(rho_H R_{E(b^{-1}*a)}) = 1_H(E(b^{-1}*a)), and the
product over the c copies is 1_{exp(h-tilde)}(b^{-1}*a) by 1.1. The resulting address matrix
|G~|^{-1} 1_{H~}(b^{-1}a) is exactly the matrix of rho_{H~} = |G~|^{-1} sum_{h in H~} R_h.

**1.3 Central instrument (lem:central, lines 351-370). Correct for arbitrary H, K = H cap Z.** I recomputed:
tr(rho_H Pi_lambda) = |Z|^{-1} sum_{z in K} chi_lambda(-z) = |K|/|Z| on K^perp, 0 otherwise; Pi_lambda commutes with
rho_H since R_z is central in the image of R; tr(rho_lambda R_g) = |K|^{-1} sum over the |K| decompositions
g = h'z' of chi_lambda(z'), constant on decompositions because lambda kills K.

**1.4 Pointwise quotient conversion (prop:descent, lines 397-408). Correct, branch by branch.** The output entry is
|Q|^{-1} prod_{i active} tr(rho_{lambda_i} R_{delta_{s_i}(g)}) with g = sigma(r)^{-1} sigma(q) (again using that R
and delta are homomorphisms). If g is not in HZ, every factor vanishes (needs a nonempty active set, i.e. a
nonzero witness; stated). If g = hz, the product is chi_{sum s_i^d lambda_i}(z) = 1. The result,
|Q|^{-1} 1[r^{-1}q in HZ/Z], is rho_{HZ/Z} and is independent of the record, so disjoint blocks give independent
exact copies. No normality, transversality or basis of K is used.

**1.5 Recursion (lines 424-428).** Z_d = t^d gamma_d is central in G_d = A/(sum_{k>d} A_k) and delta_s acts on it
by s^d; the image of h-tilde in each quotient is homogeneous, and H_d Z_d / Z_d = H_{d-1}. At d = 1 the group is
additive tL and the hidden subgroup is t h (the whole of h, not its abelianization). Recovery of generators of H
from a basis of h via Lazard is correct.

**1.6 Error budget (lines 430-458).** Rank: m + t uniform vectors of h^perp (dimension <= m) fail to span with
probability <= p^{-t}/(p-1) <= eps/3. Correct. Approximation: N_instr is the correct count of leaf
preparations + merges (stage d has prod_{d'<d} M_{d'} merges per terminal sample) + readouts. The QFT allotment
eta = eps/(3 N_instr q_max) with q_max = max(n, m, max_d (2 M_d g_d + D_{d-1})) does cover the transforms of one
instrument (n for the leaf address register, 2 g_d per central instrument, D_{d-1} for the quotient address
register, m for readout). Total error 2 eps/3 <= eps. Correct.

**1.7 lem:hybrid (restricted domain, lines 440-451). Correct.** The telescoping identity places each difference
(Phi~_j - Phi_j) on the *ideal* prefix state, which lies in S_{j-1}, and the *implemented* suffix is an arbitrary
channel, which is contractive even after leakage out of the canonical subspace. That is exactly what is needed:
the hypothesis is only required on S_{j-1}, and the ideal channels only need to be defined and
subspace-preserving on S_{j-1}. Classical control and abort flags are covered because the final measurement is a
channel. The pure-to-mixed step (trace distance of pure states <= Euclidean distance, then convexity) is correct.
One point to state explicitly (gap, minor): the canonical subspace S_j of the *global* system must be a tensor product
of the local canonical subspaces, so that a local bound ||(V - U)(Pi_loc tensor I)|| <= eta applies to a global state
supported on S_{j-1}; this is true for the S_j defined at line 453 but is not said.

**1.8 Query count (lines 189-194).** c * S * prod_d B_d(g_d) with S = m + ceil(log_p(3/eps)), and the bound by
C_c c S (m+1)^{sum_d d ceil(log2(d+1))} via g_d <= m: correct.

**Conclusion on (1).** I find no error in the Schedule-1 assembly. Modulo the imported Ivanyos-Santha theorem
(deterministic, arity B_d(a), time poly(a, log p) at fixed d), the Kitaev/Solovay-Kitaev QFT compilation and the
Lazard correspondence, the theorem holds for every subgroup H, normal or not. The problems are in the statement,
not the proof:

- **F1 (gap, thm:main line 179).** "the procedure of Sections 2-4" is ambiguous: Section 4 contains three
  schedules, two of them labelled conditional, and the proof (line 458) uses Schedule 1 only, with
  M_d = B_d(g_d) (or B_{kappa_d}(g_d)). The theorem must name the schedule; otherwise it reads as covering
  Schedules 2 and 3. Fix: see Proposed paper text, item P1.
- **F2 (gap, thm:main and line 466).** The whole theorem rests on one imported statement, that the
  Ivanyos-Santha algorithm is deterministic and total at arity B_d(a) in time poly(a, log p) for fixed d. This is
  stated in prose in the Schedule-1 paragraph, interleaved with artifact remarks, and the paper itself notes that
  IS2015's printed Theorem 3 has a different (and, as the paper argues, incorrect) arity. A referee cannot accept the
  main theorem without that statement isolated as a cited theorem with the exact form used. Fix: P2 (a
  `\begin{theorem}[Ivanyos--Santha, as used]` block, cited to arXiv:1503.09016v2 Sections 3.1-3.3, with the arity
  G(d,a)^{ceil(log2(d+1))} and an explicit remark that the error budget does not need determinism: if the import
  were only Las Vegas, the solver third of the budget already covers it).
- **F3 (exposition, thm:main title and line 182).** "Proposed explicit-Lie theorem" and "the project's proposed
  justification" are review-status labels, not mathematical ones. A journal theorem is either proved (with
  imported results named) or conditional on a named hypothesis. Fix: P1.
- **F4 (gap, thm:main).** The claim "returns a basis of h" should also return generators of H, which line 428
  proves; and the coset-copy variant needs "fresh independent copies" (it is in Def. def:input-contract(iii),
  but the refresh caveat of Prop. prop:refresh shows that this matters). Fix: include in P1.

**1.9 The imported Ivanyos-Santha theorem (checked against the primary source).** I read the arXiv text of
IvanyosSantha2015 (arXiv:1503.09016v2; a local text copy exists at
research/audits/reviews/2026-11-02-rees-linear-arity/lit/is_1503.09016.txt; I read only the source paper there).
The paper's reading is accurate: Theorem 11 gives a colliding pair from G(d,m) = d^{d(d-1)/2}(m+1)^d vectors
(for d | q-1), the proof of Theorem 3 iterates it ceil(log2(d+1)) times and finishes with van de Woestijne's
deterministic solver (Fact 2), and Section 3.1 replaces nonresidues by a restartable classification, so the
procedure is deterministic. I confirm the paper's observation that IS's closing inequality
G(d,m)^{ceil(log2(d+1))} <= d^{d^2 log d}(m+1)^{d log d} is false for large m (the exponent of m+1 is
d ceil(log2(d+1)) on the left and d log2 d on the right; 4 against 2 at d = 2), so IS's printed Theorem 3 threshold is
not supported by its proof, and the paper is right to use the first inequality, which the proof does give. The gcd reduction (Section 3, first paragraph) is the Bezout lift the paper uses. One point the
paper does not state and must: IS's output coefficients are "explicit d-th powers", i.e. the algorithm returns the
roots s_i, not only s_i^d. The descent needs s_i (it applies delta_{s_i}), and deterministic root extraction is not
otherwise available. This is true of IS's construction (the weights are products of the beta_i and z_i, all
returned explicitly) and should be said (in P2).

**1.10 Independent finite check.** Script
research/audits/reviews/2026-11-03-rees-referee-2/core_check.py, written from the paper's definitions only, on
Heis(F_3) and Heis(F_5): (a) tuple fibers equal left cosets of exp(h-tilde) for every subgroup; (b) label law from the
projector Pi_lambda (not from the formula of lem:central) is uniform on K^perp; (c) for every label triple and every
nonzero witness of sum s_i^2 lambda_i = 0 at arity 3, the descent output computed from the permutation matrices R_g
equals rho_{t h}; (d) negative control: the single-evaluation pullback is not delta_2-stable. Result: see 1.11
(appended when the run finishes).

**1.11 Result of the finite check** (output saved in
research/audits/reviews/2026-11-03-rees-referee-2/core_check_out.txt; 2.7 CPU-minutes):
- Heis(F_3): 19 subgroups (12 nonnormal); fibers, label laws and all 3198 (label triple, witness) descents exact.
- Heis(F_5): 39 subgroups (30 nonnormal); fibers, label laws and all 97092 descents exact (to 1e-9).
- Control: the single-evaluation pullback E_1^{-1}(h) is delta_2-stable only for the central line (2 of 26 and 4 of
  124 nonzero generating vectors, i.e. exactly the line spanned by z), as prop:single-evaluation predicts.
This is a class-two check only (the cover of a class-three example is too large for dense matrices at this budget);
it confirms the algebra of lem:homogeneous, lem:central and prop:descent independently of the project's code, and
proves nothing asymptotic.

## 2 (findings). Proved vs conditional labelling

**2.0 General problem (exposition, but publication-blocking).** The paper uses at least eight status tags with
different meanings: "Proposed", "conditional", "conditional, AI-checked only", "AI-checked, pending human review",
"proposed, conditional", "argued, AI-checked only", "conditional on the cited notes", "proved". Most of them
describe *who has read the proof*, not *what the statement depends on*. A reader cannot tell which results are
(a) proved in the paper, (b) proved modulo a named imported theorem, or (c) depend on an unproved claim. Examples:
- thm:ring-to-field is tagged "conditional", but its part (iii) is proved in full in Appendix E
  (prop:tb-recursion); its part (ii) depends on cor:fpt-r, which depends on thm:random-column, which is proved in
  Appendix B. So nothing in it is conditional in the mathematical sense, except through review status.
- prop:classical-query is tagged "AI-checked, pending human review" yet is fully proved on the page (lines 919-935;
  I checked it and found it correct).
- prop:decoupled-sde is tagged "conditional" although cor:app-s2-decoupled and prop:app-s2-TA/TW prove it, except
  for the explicit sets E_2(4..7), which are finite computations.
- thm:bb-envelope is tagged "conditional" on thm:power-sde(ii), which the paper says is proved in Appendix A.
Fix (P3): one convention, stated once in Section 1: "Every statement with a proof in this paper is stated as
proved. A statement that depends on a result not proved here names it in its hypothesis. Computer searches are
named as such." Remove all review-status tags from theorem headers; move provenance to an acknowledgements
or a single "Verification status" paragraph.

**2.1 (gap) Appendix B, lem:s3-hybrid (appendix-schedule3.tex lines 254-261) still assumes the diamond norm.** It
requires ||Phi_{j,R} - Phi~_{j,R}||_diamond <= 2 eta for every record, and the proof of thm:random-column(ii)
(line 283) supplies this "as in Theorem thm:uniform-compilation(iii)". But thm:uniform-compilation(iii) gives
the QFT_{F_p} error only "on its canonical subspace with clean workspace"; a QFT over F_p on ceil(log2 p) qubits has
no specified action off that subspace, so no diamond-norm bound is available. The main text was repaired
(lem:hybrid is restricted-domain), but Appendix B was not, and thm:free-coordinate(ii) reuses Appendix B
"word for word" (appendix-free-coordinate.tex line 187). The codimension appendix (line 306) invokes "the hybrid
argument over complete instruments" without saying which version. The fix is mechanical, since every ideal
Schedule-3 step (Gaussian elimination, rejection sampling, root extraction, Bezout lift) is classical and preserves
the canonical subspace. Fix (P4): replace lem:s3-hybrid by a corollary of lem:hybrid.

**2.2 (error, minor) prop:triangular-sde (main.tex lines 507-522) claims "a deterministic algorithm".** The
algorithm needs (1) the coset function cos(.), defined through a generator g of F_p^x (equivalently a
kappa-th-power nonresidue), and (2) at the end, "taking kappa-th roots" of the weights x_i in P. Neither is known to
be deterministic polynomial time without GRH; this is precisely the obstacle that IS2015 Section 3.1 circumvents.
Unless g and the roots are supplied as part of the hypothesis, the claim is unsupported. The Lean module
ReesSdeTriangular checks "algebra only", consistent with this. Fix (P5): "a Las Vegas algorithm, given a generator
g, ... in expected time poly(a, kappa, log p)" or add g and a root oracle to the hypothesis.

**2.3 (gap) Unproved claims stated as facts inside remarks.**
- rem:two-level-threshold-size (line 504): "p not in E_2(kappa) for every prime ... p >= 4e ceil(ln 4 kappa)^2
  kappa^kappa + 1 when kappa >= 32", and the impossibility statements for averaging arguments, are proved only in
  the cited report files (threshold-2 Theorem 5, threshold-3 Sections 2-3). The appendix scope list
  (appendix-schedule2.tex line 472) says the opposite kind of thing ("does not prove a threshold of the observed
  order").
- rem:triangular-scope (line 526): "The same argument applied to Schedule 2 shows that its second level needs only
  a+1 objects, giving (a+1)^2 columns" and "Below (a+1)^2 and (a+1)(a+2)/2, no scheme built from a universal
  contraction can go" are a theorem and a lower bound without proof or precise definition of "scheme".
- rem:premature (line 380): an Omega(p^{(c-1)(c-2)/2}) lower bound in an interface, derived in a project note.
- rem:mixed-source, and the paragraph after it: an extension of cor:subspace-hsp to nonflat states, "argued".
Fix (P6): each becomes either a stated result with proof, or is rephrased as "We do not prove ... ; a computation
suggests ..." or deleted.

**2.4 (gap) prop:black-box is a Proposition "not a result of this paper".** Line 746: "The chart below comes from
project notes that are still under review; it is not a result of this paper." Yet it is stated as a Proposition, and
item (iv) (chart cost O_c(s^c l^3 + l^4)) is labelled in Appendix E (line 815) as "argued; AI-checked, pending
human review". Either prove (iv) in the appendix as a lemma or demote it.

**2.5 (gap) thm:bb-envelope has only a proof sketch, and the appendix defers back to it.** main.tex line 773 is a
"Proof sketch" ending with "The full accounting and an exact check of the exponents are in" a report file;
appendix-torsion-blackbox.tex line 869 says "the total cost is bounded in Theorem~\ref{thm:bb-envelope}". So the
quantitative statements (i)-(iv) of thm:bb-envelope, including the exponents E_W(c) and the gate count
O_c(N^{E_W(c)+4+o(1)}), are proved nowhere in the paper. (Correctness of the composition is proved in Appendix E;
the counting is not.) The superadditivity step "x -> x(x+t)(x+1)^{E-1} is superadditive" is fine, but the chart and
gate terms are not derived. Fix: add the counting proof to Appendix E, or state the theorem qualitatively
(polynomial for fixed c) and move the exponents to a remark marked as computed.

**2.6 (exposition) Inconsistency on E_2(7).** main.tex line 500 gives E_2(7) as an exact set of 56 primes (largest
3221) and "for kappa >= 8 only bounds"; appendix-schedule2.tex line 467 says "For kappa >= 7 only bounds on
E_2(kappa) are known". Make them agree.

**2.7 (exposition) thm:uniform-compilation(iii)** defines q_max as a bound "in the note's schedule" (a project
file). Since thm:main uses it, state the per-instrument transform count in the paper: n (leaf address), 2 g_d per
central instrument, D_{d-1} (quotient address), m (readout); that gives q_max directly.

**2.8 What is genuinely proved in the paper, as I read it.** thm:rees-cover, lem:homogeneous, prop:single-evaluation,
lem:copy-lift, prop:refresh, lem:central, prop:descent, lem:hybrid, thm:main (Schedule 1, modulo IS2015 and
QFT compilation), thm:power-sde(i),(iii), thm:uniform-compilation (modulo 2.7), lem:collision,
prop:classical-query, prop:conjugation, thm:subspace-source; and, with proofs in the appendices that I spot-checked
but did not fully verify: thm:power-sde(ii), thm:random-column, thm:free-coordinate, cor:fpt-r, cor:codim,
thm:ring-to-field, prop:black-box(i)-(iii), thm:app-sub-hsp. Conditional in the real sense: thm:bb-envelope
(counting not proved, 2.5), prop:black-box(iv), the remarks in 2.3, and every use of the computed sets E_2(kappa).

## 3 (findings). Self-containedness

**3.1 (exposition, publication-blocking) Repository pointers.** main.tex has 101 `\file{...}` pointers (88
distinct targets across main and appendices), most to AI audit reports under research/audits/reviews/ and to
project notes. I checked every target: all exist in the repository, but 17 are bare basenames that resolve only by
search (e.g. `rees_nongradable_control.json`, `power_sde.json`, `random_column_rees.json` live in
research/reductions/; `birthday_crossover.json`, `filiform_check.py`, `group_check.py`, `reduction_check.py`,
`section6_bounds.py` live in audit subfolders; `Formal/Audit.lean` is formal/Formal/Audit.lean). A journal reader has
no access to these files. Load-bearing pointers, where a proof step or a stated number exists only in a file:
- thm:uniform-compilation(iii): q_max is "the note's schedule" (fix in 2.7).
- thm:bb-envelope: "The full accounting ... are in" a report (2.5).
- rem:two-level-threshold-size, rem:triangular-scope, rem:premature: results proved only in reports (2.3).
- the sets E_2(4), E_2(5), E_2(6), E_2(7) (line 500), quoted from reports.
- line 689: the scalar-flag bound $2^{O(r^2\log(r+2))}$ "of" a project note.
Fix (P7): one sentence in the introduction citing an archived, versioned snapshot of the repository (commit hash or
DOI), all artifact paths given relative to it in a single appendix table; remove all pointers to review reports from
the body; every load-bearing item above is either proved in the paper or marked "computed (see artifact X)".

**3.2 (exposition, publication-blocking) Changelog and provenance in the text.** The opening "Research status"
box, 14 lines mentioning a "previous version" or a "withdrawn" claim (e.g. lines 162, 219, 294, 322, 380, 414,
471, 546, 708, 754, 846, 979, 826), and about 58 lines of AI-review provenance ("AI-checked, pending human review",
"an AI session proved this") read as a project log, not a paper. The appendix sources also contain integrator notes
in comments (appendix-schedule2.tex lines 6-79, appendix-schedule3.tex lines 1-36). Fix: delete the changelog
material; state verification status once (P3).

**3.3 (gap) Undefined or late-defined terms.**
- "label width" (abstract, thm:main): never defined. Define in def:input-contract as the bit length w of the values
  of f.
- "lifted source", "source", "bank", "terminal sample", "merge node": used from the abstract and Table
  tab:main-regimes on, defined only implicitly (line 273, 326, 434). Add a short definition paragraph after
  lem:copy-lift (P8).
- "receiver", "coherent receiver" (lines 376, 598, 822): project jargon, never defined; and
  "coherent_receiver_implemented"-type statements are claim-gate language. Replace by "a quantum implementation".
- $G(\kappa_d, g_d)$ is used at line 376 and defined only at line 471 ("with G as below").
- $a_d$ appears in Table tab:main-regimes (line 208) and thm:random-column before its definition at line 426; the
  table is fine with a forward reference, but give one.
- $D_d$ (line 587) and $B_{\mathrm{leaf}}$ (line 814) are defined in passing; fine.
- "complete central instrument" is defined operationally in Section 3 (line 349) but never named there; the word
  "complete" appears first in the abstract.
- def:input-contract(i) says "of class $c$"; thm:main says "Fix $c$". State in thm:main that $c$ is the exact
  class (or an upper bound; the proof works with $\gamma_{c+1}=0$ only).

**3.4 (exposition) Forward references in the main statement.** thm:main refers to "the procedure of
Sections 2-4" and "the gate compilation of Section 5"; the explicit query count is displayed after the theorem,
and its proof is at the end of Section 4. Acceptable, but with 2.0 fixed the theorem should be self-contained:
name Schedule 1, the arities, and the imported theorem (P1, P2).

**3.5 (exposition) The appendix-inclusion macro.** main.tex lines 1041-1048 include each appendix only
`\IfFileExists`; a missing file silently drops an appendix that the body cites as containing proofs. Replace by
plain `\input`.

## 4. The most important remaining weakness for publication

**The publishable result is a short, correct theorem buried in a 106-page project record, and its novelty has
not been assessed by anyone who knows the area.**

The mathematical core (thm:rees-cover, lem:homogeneous, lem:copy-lift, lem:central, prop:descent, lem:hybrid and the
assembly at main.tex line 457) is about eight pages and, as far as I can verify, correct for every hidden subgroup.
Around it sit: three SDE schedules (two not used by the theorem), five conditional corollaries and theorems, a
black-box envelope whose counting is not proved in the paper (2.5), a subspace-source extension, classical filters,
a Lean inventory, simulation reports, and about 70 lines of changelog and provenance. The related-work paragraph
itself concedes that the grade-by-grade elimination is IvanyosSantha2015 Section 5 and that the only possibly new
idea is the tuple lift through the Rees cover. That idea is simple; it either resolves a question experts care
about (fixed class, growing p, arbitrary H; compare ImranIvanyos2023 Section 6) or is folklore. Only a specialist
(for instance one of the cited authors) can say which, and the paper's own literature search is explicitly not
exhaustive. A journal will judge the paper on that one point, and the present form makes it hard to see.

Concrete recommendation: split. Paper 1 (15-20 pages): def:input-contract, thm:rees-cover, lem:homogeneous,
prop:single-evaluation, lem:copy-lift, lem:central, prop:descent, lem:hybrid, the imported IS theorem (P2), thm:main
(P1) with its proof and query count, prop:classical-query and rem:query-separation, and the related-work comparison.
Everything else goes to a companion report, where the conditional statements can carry their hypotheses.

Secondary weaknesses, in order: (i) the import of IvanyosSantha2015 is the single point of failure and must be
isolated (F2, 1.9); (ii) Appendix B still uses an unrestricted-domain hybrid (2.1), so Schedule 3 and everything
built on it (cor:fpt-r, cor:codim(ii), thm:ring-to-field(ii), thm:free-coordinate(ii)) have a gap as written,
easy to close; (iii) the constants (exponent of m in the Schedule-1 query count at c = 9 is 145; crossover prime $2^{174.7}$) make the result
purely structural, which the paper says honestly; (iv) no accountable human author.

## 5. Verdict, exact statement, claim gates

**Verdict: major revision.** I found no error in the proof of thm:main (Schedule 1, every subgroup H, normal or
not, oracle or coset-copy input). The revision is major because (a) the theorem statement does not say which
procedure it covers (F1) and does not isolate its one imported theorem (F2); (b) the status labelling does not
separate proved from conditional (2.0); (c) there are real gaps outside the core: the unrestricted hybrid in
Appendix B (2.1), the unproved counting in thm:bb-envelope (2.5), the "deterministic" claim of
prop:triangular-sde (2.2), and unproved results stated in remarks (2.3); and (d) the manuscript is not in
publishable form (Section 3, Section 4). None of (c) touches thm:main.

**The exact statement I believe holds.**

> Fix an integer c >= 1. Let p > c be prime, let L = F_p^m carry the structure constants of a nilpotent Lie algebra
> with gamma_{c+1}(L) = 0, let G = (L, *) with the truncated BCH product, and let H <= G be an arbitrary subgroup.
> Assume the Ivanyos-Santha theorem in the form: for fixed d with d | p-1, from any M >= B_d(a) =
> [d^{d(d-1)/2}(a+1)^d]^{ceil(log2(d+1))} vectors lambda_i in F_p^a a deterministic algorithm computes, in time
> poly(M, log p), explicit s in F_p^M \ {0} with sum_i s_i^d lambda_i = 0. Then there is a quantum algorithm that,
> given p, the structure constants, eps in (0,1), and either a coherent oracle U_f for a function f : G -> {0,1}^w with
> f(x) = f(y) iff x^{-1} * y in H, or fresh independent copies of rho_H, outputs a basis of log H (hence generators
> of H) with probability at least 1 - eps. It makes at most c (m + ceil(log_p(3/eps))) prod_{d=2}^c B_d(g_d) queries
> (or uses that many copies), where g_d = dim gamma_d(L), and uses poly_c(m, log p, w, log(1/eps)) further gates
> from a fixed finite gate set and classical operations. The output is bounded-error, not exact.

I do not believe the paper establishes, in its present text: the numerical exponents E_W(c) and the gate bound of
thm:bb-envelope (2.5); determinism in prop:triangular-sde (2.2); the statements in rem:two-level-threshold-size,
rem:triangular-scope, rem:premature and rem:mixed-source (2.3); the computed sets E_2(kappa) beyond being computer
results; and the proofs of thm:random-column(ii) and thm:free-coordinate(ii) as written (2.1), though I expect them
to hold after the fix.

**Claim gates that must stay false:**
- independent_review: false. This report and every check the paper cites are AI-run; no human specialist has read
  the proof.
- novelty_established: false. The paper's own search is not exhaustive and concedes the mechanism is
  IvanyosSantha2015's; the tuple lift has not been assessed by a specialist (Section 4).
- speedup_claim_allowed: false. The separation is a query separation in an arbitrary-label oracle model, below
  astronomically large crossovers, with no explicit hiding function (rem:query-separation (a)-(c)).
- coherent_receiver_implemented: false. Only a fixed 82-qubit Heisenberg-over-F_3 circuit is simulated, with a
  brute-force classical solve between segments.
- general_sde_implemented: false. The IS solver artifact covers kappa <= 3 (and kappa = 4 in a special case); the
  reduction does not call it.
- formal_compiler_checked: false. The Lean boundary excludes BCH/Lazard for c >= 5, the solvers, the wiring of SDE
  witnesses, approximation and running time (main.tex line 1026).

## 6. Proposed paper text

**P1. Replace thm:main (main.tex lines 177-180).**
```latex
\begin{theorem}[Main theorem]
\label{thm:main}
Fix an integer $c \ge 1$ and assume Theorem~\ref{thm:is-import}. There is a quantum
algorithm with the following property. Its input is a prime $p > c$, the structure
constants of a nilpotent Lie algebra $\mathcal{L} \cong \Fp^m$ with
$\gamma_{c+1}(\mathcal{L}) = 0$, a real $\eps \in (0,1)$, and either
\textup{(a)} a coherent oracle $U_f$ for a function $f : G \to \{0,1\}^w$,
$G = (\mathcal{L},\ast)$, with $f(x) = f(y) \iff x^{-1}\ast y \in H$, or
\textup{(b)} fresh independent copies of $\rho_H$, where $H \le G$ is an arbitrary
subgroup. The algorithm uses the evaluation points $1,\dots,c$ and Schedule~1 with
arity $M_d = B_d(g_d)$ at every grade $d = 2,\dots,c$. With probability at least
$1-\eps$ it outputs a basis of $\hh = \log H$, and hence generators of $H$. It makes
at most
\[
  Q = c\,\bigl(m + \lceil\log_p(3/\eps)\rceil\bigr)\prod_{d=2}^{c} B_d(g_d)
\]
queries in case~\textup{(a)}, or uses $Q$ copies in case~\textup{(b)}, and
$\poly_c(m,\log p,w,\log(1/\eps))$ further gates from a fixed finite universal gate
set and classical operations. No property of $H$, such as normality, is assumed.
The guarantee is bounded-error, not exact.
\end{theorem}
```
and replace line 182 ("The proofs below are the project's proposed justification ...") by
```latex
The proof is at the end of Section~\ref{sec:recursion}. Its only imported
ingredients are Theorem~\ref{thm:is-import}, the subgroup form of the Lazard
correspondence, and a standard compilation of the quantum Fourier transform over
$\Fp$ (Theorem~\ref{thm:uniform-compilation}(iii)).
```

**P2. Insert before the Schedule 1 paragraph (main.tex line 465) and shorten that paragraph accordingly.**
```latex
\begin{theorem}[Ivanyos--Santha {\cite[Theorem~11 and the proof of Theorem~3,
Sections~3.1--3.3]{IvanyosSantha2015}}]
\label{thm:is-import}
Let $d \ge 1$ be fixed and let $p$ be a prime with $d \mid p-1$. Put
$G(d,a) = d^{d(d-1)/2}(a+1)^d$ and $B_d(a) = G(d,a)^{\lceil\log_2(d+1)\rceil}$.
There is a deterministic classical algorithm that, given any
$\lambda_1,\dots,\lambda_M \in \Fp^a$ with $M \ge B_d(a)$, outputs explicit field
elements $s_1,\dots,s_M$, not all zero, with $\sum_{i} s_i^d\lambda_i = 0$, in time
$\poly(M,\log p)$.
\end{theorem}

\begin{remark}
\label{rem:is-import}
\textup{(a)} The algorithm returns the scalars $s_i$ themselves, not only $s_i^d$;
Proposition~\ref{prop:descent} needs them, since it applies $\delta_{s_i}$.
\textup{(b)} If $d \nmid p-1$, put $\kappa = \gcd(d,p-1)$ and choose $t \ge 1$ with
$t\,d/\kappa \equiv 1 \pmod{(p-1)/\kappa}$. A solution $u$ for the exponent $\kappa$
gives the solution $s_i = u_i^{t}$ for the exponent $d$
\cite[Section~3]{IvanyosSantha2015}, and $B_\kappa(a) \le B_d(a)$.
\textup{(c)} We use the bound $C(d,a) \le G(d,a)^{\lceil\log_2(d+1)\rceil}$ that the
proof of \cite[Theorem~3]{IvanyosSantha2015} establishes. The bound printed in that
theorem, $d^{d^2\log d}(a+1)^{d\log d}$, does not follow from the proof for large $a$,
because $d\lceil\log_2(d+1)\rceil > d\log_2 d$.
\textup{(d)} Determinism is not used in Theorem~\ref{thm:main}: a Las Vegas solver of
expected time $T$ would be covered by the solver share of the error budget in
Section~\ref{sec:recursion}.
\end{remark}
```

**P3. Replace the "Research status" box (main.tex lines 62-89) by a status paragraph at the end of Section 1.1,
and drop review-status tags from all theorem headers.**
```latex
\paragraph{Status of the results.} Theorem~\ref{thm:main} is proved in
Sections~\ref{sec:rees-cover}--\ref{sec:sde} from Theorem~\ref{thm:is-import}, the
Lazard correspondence and Theorem~\ref{thm:uniform-compilation}. Every other
statement that has a proof in this paper or its appendices is stated without
qualification. A statement that depends on a claim not proved here names that
claim in its hypothesis. Results of computer searches, such as the sets
$E_2(\kappa)$ and the resource tables, are marked as computed and name the artifact
that produced them.
```
Header changes: `[Proposed explicit-Lie theorem]` -> `[Main theorem]`;
`[Two-level symmetric SDE contraction; part~(ii) conditional, ...]` -> `[Two-level symmetric SDE contraction]`;
`[Decoupled two-level contraction; conditional, AI-checked only]` -> `[Decoupled two-level contraction]`, with the
sentence "The sets $E_2(4),\dots,E_2(7)$ quoted below are computed, not proved."; `[Ring-to-field local-torsion
reduction; conditional]` -> `[Ring-to-field local-torsion reduction]`; `[Classical query complexity; AI-checked,
pending human review]` -> `[Classical query complexity]`; similarly for thm:random-column, thm:free-coordinate,
prop:rc-lower, cor:fpt-r, cor:codim, cor:subspace-hsp. Keep "conditional" only where a hypothesis is not proved here
(after P10, nowhere in the theorem headers). Put "The proofs in this paper have been checked by automated tools only"
in the acknowledgements or cover letter.

**P4. Replace lem:s3-hybrid (appendix-schedule3.tex lines 254-261).**
```latex
\begin{lemma}[Hybrid over complete instruments]
\label{lem:s3-hybrid}
Let $S_j$ be the canonical subspaces of Section~\ref{sec:recursion}. Every ideal
step of the procedure of this appendix (central instruments, kernel computation,
rejection sampling, root extraction, Bezout lift, conversion channel and abort
branches) maps states supported on $S_{j-1}$ to states supported on $S_j$.
Suppose each of the at most $N_{\mathrm{instr}}$ complete instruments
$\Phi_{j,\mathcal{R}}$ is implemented, for every record $\mathcal{R}$, by
$\widetilde\Phi_{j,\mathcal{R}}$ with
$\frac12\|(\widetilde\Phi_{j,\mathcal{R}} - \Phi_{j,\mathcal{R}})\otimes\mathrm{id}(\xi)\|_1
\le \eta$ for every state $\xi$ supported on the canonical subspace tensored with a
reference, as Theorem~\ref{thm:uniform-compilation}(iii) provides. Then the joint law
of all records, abort flags and the output moves by at most $N_{\mathrm{instr}}\eta$
in total variation.
\end{lemma}

\begin{proof}
On a dephased input $\xi = \sum_{\mathcal{R}}|\mathcal{R}\rangle\langle\mathcal{R}|
\otimes\xi_{\mathcal{R}}$ supported on $S_{j-1}$, the controlled channel acts as
$\sum_{\mathcal{R}}|\mathcal{R}\rangle\langle\mathcal{R}|\otimes
\Phi_{j,\mathcal{R}}(\xi_{\mathcal{R}})$, so the trace norm of the difference is at
most $\sum_{\mathcal{R}} 2\eta\tr\xi_{\mathcal{R}} = 2\eta$. Apply
Lemma~\ref{lem:hybrid}. Slots that an aborted tree leaves unused act as the identity
in both procedures.
\end{proof}
```
In appendix-codimension.tex line 306 replace "By the hybrid argument over complete instruments" by
"By Lemma~\ref{lem:hybrid}, with $S_j$ the canonical subspaces,".

**P5. prop:triangular-sde (main.tex line 513): replace the conclusion.**
```latex
columns $\lambda_1,\dots,\lambda_M\in\Fp^{a}$, an algorithm that is given $g$ and
uses $O(a)$ Gaussian eliminations and $O(a^2)$ evaluations of
$y\mapsto y^{(p-1)/\kappa}$ returns, deterministically, a nonzero
$x \in (P\cup\{0\})^M$ with $\sum_i x_i\lambda_i = 0$. Extracting $\kappa$-th roots
of the $x_i$ (Las Vegas, expected time $\poly(\kappa,\log p)$ each) and applying a
Bezout exponent gives a nonzero solution of~\eqref{eq:sde-target}.
```

**P6. Remarks that state unproved results.**
- rem:two-level-threshold-size, first two sentences: replace by
```latex
We do not prove a threshold of order $\kappa^{\kappa+o(1)}$. A version of the argument
of Appendix~\ref{app:s2-TA} with central moments of order $2m$ in place of the second
moment appears to give $p \notin E_2(\kappa)$ for $p \ge 4e\lceil\ln 4\kappa\rceil^2
\kappa^\kappa + 1$ when $\kappa \ge 32$; we leave this unproved.
```
  and phrase the rest of the remark ("Closing it needs information ...") as a heuristic discussion.
- rem:triangular-scope: replace "The same argument applied to Schedule~2 shows that its second level needs only
  $a+1$ objects ... can go" by "We expect, but do not prove, that the same argument lowers the second level of
  Schedule~2 to $a+1$ objects."; delete "Below $(a+1)^2$ and $(a+1)(a+2)/2$, no scheme built from a universal
  contraction can go" or define "scheme" and prove it.
- rem:premature: begin with "We record, without proof, ..." and delete the sentence on the withdrawn
  $\Omega(p^{55})$ claim.
- rem:mixed-source: retitle `[Nonflat sources by spectral flags; not proved here]`.

**P7. Repository pointers.** Add to the introduction:
```latex
All computations cited in this paper are in the repository \url{<URL>} at commit
\texttt{<hash>}, archived as \href{https://doi.org/<DOI>}{<DOI>}; Table~\ref{tab:artifacts}
lists them with paths relative to its root.
```
and replace each `\file{...}` in the body by a reference to that table, deleting every pointer to
research/audits/reviews/. Give bare artifact names their directory (research/reductions/ etc.).

**P8. Terminology, after lem:copy-lift.**
```latex
\paragraph{Terminology.} A \emph{source} on a group $\Gamma$ is one copy of a coset
state $\rho_J$ with $J \le \Gamma$. A \emph{lifted source} is a source
$\rho_{\exp(\hlift)}$ on $\widetilde G$, made by Lemma~\ref{lem:homogeneous} from $c$
queries or by Lemma~\ref{lem:copy-lift} from $c$ copies of $\rho_H$. A \emph{merge
node} at stage $d$ consumes $M_d$ sources on $G_d$, measures each with the central
instrument of Section~\ref{sec:instrument}, and applies
Proposition~\ref{prop:descent}; it outputs one source on $G_{d-1}$. A \emph{terminal
sample} is one Fourier sample of a source on $G_1 = (t\mathcal{L},+)$; it consumes
$\prod_{d=2}^c M_d$ lifted sources. A \emph{bank} is the list of sources consumed by
one node, with their measured labels. The \emph{label width} $w$ is the bit length of
the values of $f$.
```
Also replace "coherent receiver" (lines 376, 598, 822) by "quantum implementation".

**P9. lem:hybrid application (main.tex line 453), add after the first sentence.**
```latex
Each $S_j$ is the tensor product, over the registers present after step $j$, of their
canonical subspaces, so a bound $\|(V-U)(\Pi_{\mathrm{loc}}\otimes I)\| \le \eta$ for
an instrument acting on some registers applies to every global state supported on
$S_{j-1}$, the other registers playing the role of the reference.
```

**P10. thm:bb-envelope.** Either add to Appendix E a subsection "Proof of the counts of
Theorem~\ref{thm:bb-envelope}" deriving (i)-(iv) (per-prime call caps, superadditivity, the chart and gate terms,
the four-way error split), or replace the quantitative statement by
```latex
For fixed $c$, the number of queries to $f$, the number of gates and the classical
time are polynomial in $N = s\ell + w + \log(1/\eps)$.
```
and move the exponents $E_W(c)$ to a remark headed "Computed exponents". Also delete "it is not a result of this
paper" (main.tex line 746) once prop:black-box(iv) is proved as a lemma in Appendix E.

**P11. Minor.** Make the E_2(7) statements agree (main.tex line 500 vs appendix-schedule2.tex line 467); define
$G(\kappa_d,g_d)$ before line 376; replace the `\IfFileExists` appendix macro (lines 1041-1048) by plain
`\input`; remove the integrator comment blocks from the appendix sources.
