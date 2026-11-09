# Rees Manuscript: Two Exact Protocol Falsifiers

31 October 2026. Independent automated mathematical review of the local
`docs/papers/rees-hsp/main.tex`, with line numbers referring to the version
read on this date. No manuscript, formal proof, registry or implementation
was changed. These findings refute two stated protocol steps, not the
existence of a fixed-class nilpotent HSP algorithm.

## 1. Direct Pullback Does Not Supply Dilation Invariance

`main.tex:126` and `:191` use the single-evaluation oracle `f o pi` and
hidden subgroup `pi^-1(H)`, where `pi=E_1`. These pullback statements are
correct. Their compatibility with the dilations used at `:301-314` is not.

Take the Heisenberg Lie algebra over F_3 with basis x,y,z, bracket
[x,y]=z, and all other basis brackets zero. It has class c=2<p=3.
For H={1}, the positive cover is tL + t^2<z>, and

    u=tz-t^2z belongs to ker(E_1),
    Delta_2(u)=2tz-t^2z,
    E_1(Delta_2(u))=z != 0.

Thus even the kernel of evaluation is not preserved. The example is
central, so no BCH convention or left/right coset convention affects it.
More generally, for any class at least two, nonzero z in gamma_2(L),
and lambda not equal to 0 or 1, evaluation gives
(lambda-lambda^2)z != 0.

The existing replacement is `research/REES_HSP_REDUCTION.md:91-123`:
evaluate the original coherent oracle at c distinct nonzero field points.
Vandermonde interpolation makes the tuple hide exactly

    h_tilde = direct_sum_r t^r(h intersect gamma_r(L)).

For an explicit F_p Lie algebra of fixed class c<p and arbitrary H,
Lazard correspondence gives the needed F_p-linearity of h=log(H).
This subgroup is dilation invariant without learning h or its intersections.
The public compiler costs c original oracle queries per lifted source;
evaluation workspaces must be uncomputed while retaining tuple labels.
This is not a free replacement for a copy-only source. The actual
class-three formal transport scope is described in
`research/REES_CLASS_THREE_GROUP_FORMALIZATION.md:60-75` and `:113-120`.

## 2. Product-And-Measure Does Not Add Central Characters

Independently of the first issue, `main.tex:305-314` claims that the map

    |x_1,...,x_M> -> |x_1,...,x_(M-1), x_1*...*x_M>

followed by measuring preceding quotient coordinates leaves the last
register with the sum of input central characters. This is false even
when the hidden subgroup is homogeneous.

Write |chi_a>=p^(-1/2) sum_x omega^(a*x)|x> on a central F_p coordinate.
The two-input product is SUM, and direct substitution gives

    SUM(|chi_a> tensor |chi_b>)
      = |chi_(a-b)> tensor |chi_b>.

For p=5, a=1, b=4 and both dilation scales equal to one, the SDE sum is
zero but the output character is 4. Tracing or measuring the first
register does not alter this. This embeds in the class-two Heisenberg
Rees cover with the homogeneous hidden subgroup {1}: conditioned on a
central character, its coset density matrix is maximally mixed on the
three grade-one coordinates and pure Fourier on the grade-two center.
Every character tuple has positive probability. Extra zero-character
inputs can pad any larger arity while keeping a final character 4.

There is also a general operator proof. Translation of the product output
by central z pulls back through the displayed permutation to translation
of the final input alone. Consequently the last output is supported in
the final input's central eigenspace. Measurements on preceding quotient
coordinates commute with that projector and cannot change its character.
Neither nilpotence nor subgroup invariance changes this fact.

Exact Sage check, using the installed CAS rather than floating arithmetic:

```sh
/opt/anaconda3/envs/qsearch-cas/bin/sage -c 'K=CyclotomicField(5); w=K.gen(); p=5; a=1; b=4; psi=matrix(K,p,p,lambda x,y:w**(a*x+b*(y-x))/p); rho=psi.transpose()*psi.conjugate(); weights={j:sum(w**(-j*y)*rho[y,z]*w**(j*z)/p for y in range(p) for z in range(p)) for j in range(p)}; print(weights); print({"sum_input_characters":(a+b)%p,"output_character":b,"normalization":rho.trace()})'
```

Observed result:

```text
{0: 0, 1: 0, 2: 0, 3: 0, 4: 1}
{'sum_input_characters': 0, 'output_character': 4, 'normalization': 1}
```

The source replacement is the distinct controlled-right-action channel in
`research/REES_HSP_REDUCTION.md:129-184`. Initialize a fresh uniform
quotient control register, apply scale-dependent right actions to the
independent conditioned targets, and trace the targets. When the scales
solve the SDE, the product of their correlation functions yields the exact
quotient-coset density matrix. This proof uses subgroup preservation,
proper central-intersection normalization, independent target states,
and nonzero active scales; it does not multiply target registers together.
Changing only the lifted subgroup in `main.tex` therefore is insufficient.

## 3. Other Source Drift Requiring Reconciliation

These observations bound the repair task; they are not a whole-paper audit.

- `main.tex:330` calls the terminal quotient L/[L,L]. The actual positive
  cover quotient after discarding grades 2 through c is tL. The homogeneous
  tuple lift projects to th, as `REES_HSP_REDUCTION.md:186-193` states.
  The single-evaluation pullback instead projects to h+gamma_2(L), so
  final projection alone loses hidden derived-direction information.
- `main.tex:321-326` attributes arity 2*d^3*g_d and a runtime polynomial
  jointly in d,g_d,log(p) to Ivanyos--Santha. This conflicts with the
  checked sufficient bound recorded at `REES_HSP_REDUCTION.md:201-211`.
  Reconcile against the primary paper before using either attribution;
  this reviewer performed no new network literature lookup.
- `main.tex:379` claims |P_d|>=2 from p>c>=d. At d=c=p-1, |P_d|=1.
  Its solution-count second moment also does not implement or bound the
  cost of the asserted sampler conditioned on satisfying the equations.
  Existence cannot justify the claimed efficient random-column schedule.

## 4. Decision And Claim Boundary

Treat the newer manuscript as nonauthoritative pending reconciliation with
the actual source construction and channel. The existing topic-note scope
remains: "proposed fixed-class, growing-prime polynomial-time composition,
pending independent correctness and priority review". In the ordinary
coherent-oracle model, its conservative leaf envelope is

    B_d(r) = [d^(d(d-1)/2)*(r+1)^d]^ceil(log2(d+1)),
    original queries = c*(n+t)*product_(d=2..c) B_d(r_d),

with solver clocks, public arithmetic, complete-instrument approximation,
and final readout still charged as that note specifies. The two falsifiers
do not refute this different composition or establish its novelty.

Keep all claims of a verified whole manuscript, improved SDE runtime,
native application, or speedup false. Restoring source-faithful prose is
mechanical follow-up. Further research should prioritize a motivated native
source that survives its classical attacks, rather than extending receiver
infrastructure solely because the manuscript drift exposed more work.

## 5. Disposition: Manuscript Corrected (31 October 2026, Claude Code)

`docs/papers/rees-hsp/main.tex` was rewritten to the source construction.
The pre-correction file is `docs/papers/rees-hsp/archive/main-2026-10-31-before-correction.tex`.

- Section 1 is sharper than stated above. For s!=0 and lambda not in
  {0,1}, Delta_lambda preserves E_s^-1(h) IFF gamma_2(L) <= h, i.e.
  [G,G] <= H. Proof: u=s*tz-t^2z gives E_s(Delta_lambda u)=s^2(lambda-
  lambda^2)z. The direct pullback therefore works only when f
  already factors through the abelian quotient G/[G,G].
  This is now the manuscript's Proposition 2.3. It is checked exhaustively
  on 19, 39, 220 and 6453 subalgebras (Heisenberg over F3 and F5,
  filiform class 3 over F5, filiform class 4 over F7) by
  `tests/test_rees_single_evaluation_falsifier.py`. The same test checks
  that the c-point tuple set equals the homogeneous lift and is
  Delta-invariant.
- The lift, copy-only input (c copies, not p^D), branch law, quotient
  conversion and terminal tL now follow `REES_HSP_REDUCTION.md` and
  `manuscripts/rees_hsp_review.tex`. The product channel became a remark
  stating the Section 2 falsifier.
- SDE: Ivanyos--Santha arity B_d(a) per the scope audit. The symmetric
  schedule is (a+1)((delta-1)a+1) with p>=16 delta^(2 delta+2), where
  delta=gcd(d,p-1); the draft had swapped in the grade dimension. The
  random-column schedule is M=4u, p>=16u^2, kernel rejection, per
  `RANDOM_COLUMN_REES_PARAMETER_BOUND.md`.
- Withdrawn: FPT(k) as stated. The draft's proof used the pullback. For
  the homogeneous lift, filiform h=span(e_1..e_{m-2}) has k=2 but a_d=1
  at every grade. Also withdrawn: the Omega(p^55) theorem (profile data
  mismatched), the attribution of 2d^3 g_d to Ivanyos--Santha, and the
  Lean table. Ten of its seventeen modules do not exist. It is replaced by
  the sixteen actual modules, whose 180 Audit.lean guards built on
  31 October.
- Bibliography: Imran--Ivanyos is arXiv:2304.08376, "Zero sum
  subsequences and hidden subgroups". Ivanyos--Santha is TCS 2016 / FAW
  2015. ISS is nil-2. Removed as unverifiable: Roichman 1996,
  Aragon--Trias 1997, Hakim--Sandu 2020, Gell-Redman--Fehr 2025.
- Section 7.2 rewritten to `REES_SUBSPACE_SYMMETRY_SOURCE.md`. The draft
  stated naive wedge projection (success r^-r) but quoted the budgets of
  streaming growth (N=r^2 B attempts per output, Bene Watts et al.,
  arXiv:2610.06737). Its weak-Schur claim for nonflat states is withdrawn.
- Sections 5, 6.2, 7.1 and 8: re-audited later the same day; see the
  last part of this section.

Referee pass (31 October, independent automated subagent, Sections 1-4 and
6.1 only). No fatal error. It hand-derived each lemma and simulated the
Heisenberg F3 cover with explicit right-regular matrices. Fixed in
`main.tex`:
- Dixmier--Lister table: it omitted [e2,e4]=e6 and printed [e2,e6]=-e8
  instead of -e7, so it failed Jacobi at (e1,e2,e3). Now matches
  `theorems/rees_nongradable_control.py` BRACKETS.
- Check counts: 273 = 91 pairs x 3 points; 91 is all pairs; 4620 = 3 x 1540.
- Error budget: solver aborts are now charged (eps/(3 N_solver), Markov
  cap at 2T), per `REES_HSP_REDUCTION.md`. Schedule 1 is charged as Las
  Vegas because the notes disagree on whether it is deterministic.
- Theorem 4.4 now defines mu, states the root and fair-bit caps, and gives
  the eps/3 + eps/3 + eps/3 success conclusion.
- Smaller fixes: gcd(d,p-1) renamed kappa_d (delta is the dilation);
  "abelian case" became "f factors through G/[G,G]"; top-degree component
  replaces L_c; gcd step for no positive grading; Theorem 1.2 now depends
  on Section 5; table caption; filiform brackets and p>m-1; test coverage
  wording; the finite-control arity 5 is Chevalley--Warning, not a
  schedule; the scale/label slip in Remark 4.2.
Not verified, offline: the exact Ivanyos--Santha arity and
Ivanyos--Magniez--Santha Theorem 11. Both rely on the project's own reading
of the primary sources.

Re-audit of Sections 5, 6.2, 7.1 and 8, and primary-source citation
check (31 October, three independent automated subagents plus direct
reading of arXiv:1503.09016v2 and quant-ph/0102014). No fatal error.
- Citations. Ivanyos--Santha Theorem 11 gives G(d,m)=d^(d(d-1)/2)(m+1)^d
  and Section 3.3 gives C(d,m)<=G^ceil(log2(d+1)), exactly B_d. Theorem 3
  is deterministic (only Props 9-10 are randomized), so Schedule 1 has no
  solver term. The TCS title is "Solving systems ...", vol 657, 73-85,
  2017 (Crossref). IMS Theorem 11: HSP in time poly(input + |G'|) for
  unique encoding, as cited.
- Section 5. Every number reproduces from its JSON. Fixed: the QFT
  precision formula (unsourced) became the note's eta statement and the
  row now says ceil(log2(1/eta)); the depth-first bound is 2+sum(M_d-1),
  matching the table; the "104-bit primes" sentence is a 104-bit encoding
  of p^m with b-exponent 147; row labels; eps=1/3 and padded m+4 samples
  stated; the class-9 solver model marked conservative; the BCH recursion
  is the note's ODE with (c-1)c(c+1)(c+2)/6 brackets.
- Section 6.2. The class-4 example is Z/625 (exponents (4,4)), not Z/25;
  the readout example is Z/3 x Z/9 with an incomplete label set; the
  artifact executes no recursion, and its caps are b(b+1)/2 of the note's
  flag scan while Theorem 6.3(iii) needs <= b calls. The theorem is now
  conditional, states its input, and gives the quotient oracle
  f_loc(t)=f(sigma(t)) and the normalizer proof.
- Section 7.1. For e>1 the free-Lie chart is not an F_p algebra, so it
  goes through Theorem 6.3(iii), not Section 2. The metacyclic claim was
  false (Phi(p x_1)=a^p); the true failure is that b has no order-p
  preimage.
- Section 8. The conjugation proof assumed exp(x)M exp(-x)=exp(ad_x)M,
  false for N<=p<2N-1 (counterexample p=N=3, M=E31, reproduced); the
  statement is true by a commutant argument under N<=p. Items (i)-(iii)
  became a remark faithful to their notes; Luks 1982 replaced by Luks,
  FOCS 1992 (Crossref); the transporter local-global clause removed.
Scratch scripts of the reviewers: /private/tmp/claude-501/rees_ref2/.
- Related work (added before outreach). Section 1.1 now compares scope
  with FIMSS (SIAM J. Comput. 43, 2014), DHIS (QIC 14, 2014),
  Ivanyos-Santha Corollary 8, Imran-Ivanyos Theorem 1 (now cited as QIP
  23:14, 2024; their Section 6 asks for bounded class and smooth order),
  Morales arXiv:2608.05321 and Holt-Subramanian arXiv:2609.38085. Scope
  witness: the free 2-generator class-3 exponent-p group has no abelian
  maximal subgroup, since [ax+by,[x,y]] != 0, and <exp x>, <exp y> do
  not permute. Not an exhaustive search. ISS Section 3 checked on
  arXiv:0707.1260: Algorithm 1/Lemma 2 is the normalizer recursion and
  Lemma 3 gives Omega_1 for p > class, as cited.
Not done: human specialist review of any section.

All claim gates stay false: no verified whole manuscript, no novelty, no
speedup, no application. Outreach drafts 04/05 now ask about the
corrected construction and say to attach only the corrected version.
