# Bounded-degree contraction: source audit and circuit baseline

Date: 2026-11-06. Status: reviewed written source-based composition;
fixed-field bit/space and one-amplitude scope reviews complete. No novelty, polynomial classical simulation, new quantum algorithm,
or verification of the entire ETH manuscript is claimed.

## Selection and precise question

The previous monomial Kummer pass supplied a classical counterpart. This pass
compared independent mechanisms before selecting work; it does not extend it.
Corpus been-tried lookups preceded the primary-source reads, and baselines
lookups named tensor contraction. Broad nearby negative records were not
treated as theorems about these new candidates.

| Candidate | Native task and access | Mechanism and hoped-for gain | Resources, comparator, obligation and cheapest falsifier |
|---|---|---|---|
| Weighted split-character learning | A public chosen-input evaluator of a product of differently weighted multiplicative characters of unknown independent linear forms over F_p; recover the forms up to their allowed scalings | Many-copy stabilizer reduction to a conjugate split torus; hoped-for poly(n,log p) receiver | Charge all copies, overlap errors and group arithmetic. Classical polynomial interpolation/zero search and factor-isolation attacks first. No efficient torus decoder was supplied. Additive Fourier samples of distinct cosets have distinct unknown left representatives, so pooling their annihilator equations is invalid. No theorem excluding other receivers. |
| High-dimensional SU(n) operations | Explicit angles and a specified symmetric-power occupation basis, binary total occupation | Actual arXiv:2602.15180 implements these operations with polylogarithmic dimension cost; possible receiver primitive | Actual sections 1.1 and 5 restrict the representation to symmetric powers. Compilation is prior art. Generic irreps, useful native reduction, readout and matched classical cost are still missing. It cannot be admitted merely as an efficient new subsystem. |
| Bounded-degree exact contraction | Explicit constant-arity tables over a fixed number field on Boolean variables of bounded occurrence; one exact sum-product value | Primary source's low-degree replacements, short integer measurements, finite differences and Hermite recovery; potential 2^{o(n)} classical comparator | Must pay table input, every repeated variable, measurement ranges, correction dependence and exact arithmetic. Direct enumeration and graph-width contraction are existing comparators. Check the source's two actual dependencies, then a nontrivial-kernel exact control. Selected because its validity changes externally meaningful quantum circuit comparisons. |

**Single question:** Does the supplied-design counting routine, together with
the actual replacement construction, give a paid subexponential BIT algorithm
for bounded-degree explicit tensor contraction, and hence for one amplitude of
an explicit Clifford+T circuit? This is a classical-baseline admission test,
not a claim that the circuit amplitude task is quantum polynomial-time exact.

## Source boundary

Primary manuscript: OpenAI, *The Exponential Time Hypothesis is False*,
25 October 2026, [official source](https://github.com/openai/math/tree/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026).
Retained original files, retrieval metadata and hashes:
`audits/sources/eth_claim/`. The official README and history obtained on
6 November do not mark this manuscript withdrawn; that is not validation.

This note uses ONLY the ordinary rational interpolation route in the main
source: `def:layout`, `lem:measurement-separation`, `lem:boolean-differences`,
`prop:general-count`, `lem:layout`, `lem:row-coefficients`, and
`lem:incidence-parameters`. It does not use the stronger headline exponent,
the separately included `quantitative-contraction.tex`, sparse parity tests,
nilpotent-ring lifts, general SAT sparsification, or a Lean formalization.
The included quantitative appendix was fetched to check scope but not audited.
No full-paper acceptance or rejection follows.

The new SU(n) source is [Iyer et al., arXiv:2602.15180](https://arxiv.org/html/2602.15180),
sections 1.1 and 5. Its actual symmetric-power restriction is explicit, not
an inferred defect. Neither that paper nor this note supplies a new native
hidden-torus receiver.

## Explicit contraction contract

Fix constants b,w. Input: n Boolean variables and m tables
f_j:{0,1}^{I_j}->K, |I_j|<=w, each variable occurring in at most b scopes.
All tables are explicit. K=Q(zeta_8) is fixed, with basis 1,zeta,zeta^2,zeta^3
and zeta^4=-1; each coordinate is an explicitly encoded rational. Let L be
the total input bit length, including an explicit list of the n variables,
scopes and rational coefficients; in particular L>=n. The variable count
is not supplied only as an uncharged binary integer.
Remove unused variables and multiply the answer by their number of assignments;
empty-scope factors are constants. Zero constants give zero immediately.
In the proof, n denotes the remaining active variable count; it is at most
the original explicitly charged count, for which the same upper bound holds.

Output the exact field element

    Z = sum_{x in {0,1}^n} product_j f_j(x|I_j).

No oracle, advice, rank decomposition, favorable contraction order or supplied
layout is part of the input. The proposed deterministic bound is

    poly(L) * 2^{O_{b,w}(n (log log n)^2 / sqrt(log n))}

time and poly(L) bits of working space, with a constant finite-size fallback.
Use n>=20 in asymptotic formulas. This is subexponential, not polynomial.
Fixed K is important; no growing-degree algebra representation is implicit.

## Paid composition

1. Replace each table by its multilinear interpolation polynomial

       Phi_j(Y) = sum_{a in {0,1}^{I_j}} f_j(a)
                  product_{v in I_j} (a_v Y_v + (1-a_v)(1-Y_v)).

   Constant w makes this a polynomial-time explicit operation. It is a
   polynomial identity on Boolean inputs, not a claim about transformed
   rational inputs. Use the TOTAL-degree upper bound d=sum_j |I_j|<=bn, even if
   a factor is zero or cancellations lower the actual degree, and a common rational coefficient denominator can
   be chosen with O(L) bits. The input has no nilpotent cancellations.

2. Write lambda=ceil(log2 n), nu=ceil(log2 lambda). The source's explicit
   construction chooses r=floor(sqrt(lambda)/nu^2),
   Q=floor(lambda/(128 nu)), R=(beta+3)ceil(sqrt(lambda)),
   tau=1/(r lambda), D=r^{2Q}, with fixed beta covering b,w. All numerical
   inequalities and the finite binomial tail are checked exactly; if they
   fail, enumerate the Boolean cube. For fixed b,w only finitely many n
   fail. D<=2^{lambda/128}, so even explicit auxiliary arrays are polynomial.

3. The essential source construction uses the commuting swaps on pairs of
   r-valued strings of length Q. Their tensor eigenbasis has entries 0,+1,-1.
   Interpolating parity on an R-point binomial central interval produces M0:
   I-M0 has at most D times the binomial tail many independent measurements,
   while nonzero entries of M0 disagree with the target group in at most
   R-1 coordinates. Multiplying each such entry by the polynomial vanishing
   at exactly its mismatching coordinates gives low-degree replacement rows.
   The residual I-M0 is determined by those measurements.

   Conditional-expectation labeling places every original factor-variable
   incidence in an auxiliary copy, with hD<=2bn. Repeated occurrences contain
   the SAME original variable. Groupwise restriction costs the FULL factor r:
   the number of measurements is at most rh*c_B<=2tau*n. Row l1-norm remains
   at most D after repeated coordinates are identified. Thus Boolean
   measurements have at most (2D+1)^{2tau*n} possible tuples. This is an
   entropy bound on explicit small integers, not merely a rank assertion.

4. Each row P_{j,v}(T) has degree<=R, restores delta_v at zero, and at
   t=1,...,Q its value depends only on the factor's assigned group and the
   other groups' measurements. Set

       H(T)=sum_x product_j Phi_j((P_{j,v}(T) x)_v).

   Then H(0)=Z and deg H<=dR. At fixed measurements, group sums factor
   exactly. Scan every group's assignments to find a representative and
   scan again for its sum. Representatives need not obey additional fixed
   bits; those constraints belong on each group's summation variable.

5. Values alone do not suffice. Put q=floor(dR/Q), J=q+1. At t+z replace
   an input by P(t)x + (P(t+z)-P(t))X. Its z^j coefficient has X-degree<=j.
   For each x separately, multilinearization and Boolean Mobius inversion
   give

       sum_x p_x(x) = sum_{|E|<=q} sum_{U subset E} (-1)^{|E|-|U|}
                     sum_{x: x_i=1 for i in E} p_x(1_U).

   The dependence of p_x on x is retained. Fixing X=1_U makes every Taylor
   correction independent of x, preserving group separation. Computing in
   K[z]/(z^J) recovers all jets with
   C_q=sum_{s<=min(q,n)} 2^s binom(n,s) pairs. There is no polynomial in
   all n formal X variables stored. Exact rational Hermite interpolation
   of the QJ>dR coefficients recovers H(0).

6. The number of examined Boolean vectors is at most

       2 Q r C_q (2D+1)^{2tau*n} 2^{2n/r}.

   Since d<=bn, log C_q=O_b(n(R/Q)log(2Q/R)). The source's parameter
   inequalities give total exponent O_{b,w}(n nu^2/sqrt(lambda)). Factors,
   inputs and all index loops contribute only polynomial overhead.

## Exact bit and space accounting for this contract

This supplies the obligation left open by an algebra-operation theorem.
The l1-norm of the four rational coordinates in K is submultiplicative:
reducing zeta^4=-1 only combines signed terms. All factor tables and their
multilinear interpolants have total coefficient height and denominator
logarithms bounded by poly(L); each factor has constant arity.

The source gives the common row denominator a=(R-1)!Q! and total numerator
coefficient norm 2^{O(Q log Q)} per row. Evaluating Boolean vectors, making
the shift T=t+z, and subtracting the constant term increase log norms by at
most O(log n + R log(Q+1)) per input, harmless even without the sharper row
norm. Every group product contains a subset of the original factors, each
at most once. Its common denominator divides B*a^d, where B is the product
of all input-coordinate denominators (log B<=L). Its coefficient norm has
logarithm poly(L+n+Q+R+J); truncation cannot increase this norm.

Accumulator sizes do not scale with the number of summands in bits. Before
cancellation, their l1-norm is at most the number of summands times the
largest term norm. Even the crude bound Q*3^n*(2D+1)^{O(n)}*2^n has polynomial
logarithm. Products of partial group sums still use disjoint sets of factors;
the same degree/denominator bound and the corresponding assignment-count
factor apply. Coefficient multiplication in K has fixed dimension four.
Thus every stored ring element has polynomially many bits.

The Hermite matrix has dimension N=QJ<=dR+Q and integer entries
binom(k,j)t^{k-j}; their bit lengths are O(N log(N+Q)). Hadamard's determinant
bound and Cramer's rule give polynomial bit lengths for its rational inverse.
Standard exact linear algebra therefore costs polynomial bit time and space.
Sequential enumeration retains only polynomially many such elements. This
closes the bit/space obligation for fixed K and explicit bounded-arity tables;
it does not do so for an arbitrary abstract Q-algebra.

## Circuit application and limits

Input a finite explicit circuit over H,T,CNOT, computational-basis input x,
and a specified computational-basis output y. Read all qubit labels and
check untouched wires; there is no succinct repetition or black-box gate.
Let G be the number of gates. Expand each gate as a constant-arity table
of matrix entries over K. Fix boundary bits and sum the Boolean internal
wire values. Each internal edge appears in two gate tensors, so b=2,w<=4,
the number n of summed bits is O(G), and the total interpolation degree is
at most 2n. The scalar contraction is exactly <y|C|x>.

The preceding composition gives one exact amplitude in
poly(input bits)*2^{O(G (log log G)^2/sqrt(log G))} time and polynomial space.
This is a literature-based composition, not a novelty claim. It is NOT a
polynomial classical simulator, all-amplitudes output, or a claim that a
quantum computer obtains one exponentially precise amplitude efficiently.
Approximate sampling, adaptive circuits and arbitrary real gate descriptions
are not established here. No implementation of this asymptotic algorithm ran.

Compare TIME against the MINIMUM of applicable baselines (their space
bounds remain distinct): state-vector
simulation exponential in the number of active qubits, contraction using an
explicit low-width order, stabilizer methods when applicable, and this
source-based asymptotic bound. For G much larger than the qubit count, the
new expression can be worse. It leaves polynomial quantum versus
superpolynomial classical performance entirely possible, and does not refute
every conditional lower bound or any Shor-type algorithm.

## Reviews, controls and next decision

- Independent Codex review of the actual layout, incidence, coefficient and
  parameter proofs found no blocker. Parent checked the same source directly.
- Claude Opus/high independently reviewed the supplied-design counting
  proposition. It found no algebraic blocker and correctly required TOTAL
  degree, rational kernels, polynomial factor evaluators, bounded element
  sizes and exact interpolation costs. The source notation confirms the
  first two; the explicit contract and bit proof above discharge the rest.
  It made no full-paper claim. Run:
  `audits/claude_runs/2026-11-06-counting-identity-opus/`; completed with
  end_turn, 10500 input and 14246 output tokens, estimated USD0.32692.
  This is a usage estimate, not remaining balance or invoice data.
- One Sage exact supplied-design control uses four variables, Q=3,R=2,J=3,
  group-sum measurements x0+x1 and x2+x3 with nontrivial kernels, and K-valued
  factors. It verifies the kernel condition, all nine jet coefficients and
  the recovered entire degree-eight polynomial. H(0)=18+7*zeta-zeta^2.
  Using the original x in corrections or dropping fixed-bit restrictions
  produces a wrong answer. Artifacts:
  `audits/controls/boolean_product_interpolation/exact_control.{py,json}`.
  This is a falsifier control, not a scaled layout, SAT or quantum run.

Final actual-text reviews accepted the fixed-field bit/space proof and circuit
reduction after requiring an explicitly charged variable list (L>=n). This
repair prevents an uncharged binary count of unused variables from demanding
an exponentially long output. The chosen degree bound is the incidence sum,
even when a factor is zero. The review ledger is
`audits/reviews/2026-11-06-bounded-degree-contraction.md`.

No broader simulator, parameter sweep, full SAT proof formalization, automatic
API retry or adjacent subsystem is queued. The next concrete research action
is a fresh native-operation admission comparison, starting from STATE/TRAPS
and corpus/literature checks. Its acceptance test is a paid constructive
operation with an end-to-end role and a stronger applicable classical
comparator; an unresolved decoder alone does not authorize an implementation.
Do not extend this source audit merely because more appendices exist.
