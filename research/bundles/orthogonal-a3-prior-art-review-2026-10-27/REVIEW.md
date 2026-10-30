# Bounded A3 Prior-Art And Oracle-Interface Audit

27 October 2026. Only the cited papers and the SL4 input interface are
audited. No exterior-square reproof, implementation, tests, general
orthogonal-group claim, or mathematical novelty certificate.

## Verdict

**Yes.** For odd q, an ordinary coherent oracle hiding the FULL SL4(F_q)
stabilizer of a subspace or flag supports quantum recovery in
poly(log q, label width, log(1/epsilon)) time. This includes types (2),
(1,3), (1), and (3), without supplying their type. No GL4 oracle is granted.
DIKQS explicitly states the SL/PSL parabolic extension; the fixed-dimension
interface accounting below makes its use here concrete.

There is an important qualification: **Theorem 1 alone is a GL theorem.**
Section 8 states the extension without a separate numbered theorem or full
proof. Ivanyos's numbered SL theorem is for BORELS, not arbitrary partial
flags. Cite the combination, not either theorem with its scope enlarged.

## Exact Primary Scope

* [DIKQS, arXiv:1406.6511v2](https://arxiv.org/pdf/1406.6511v2):
  Section 1.1 defines ordinary coset hiding and the inversion conversion
  between left/right conventions. Theorem 1, Section 1.3, gives
  poly(n, log q) recovery of GL_n parabolics without known flag parameters;
  Section 5.1 outputs the flag. Section 3, Proposition 6 treats maximal
  parabolics. Crucially, [Section 8, PDF page 16](https://arxiv.org/pdf/1406.6511v2#page=16)
  explicitly says efficient parabolic procedures for special and projective
  special linear groups can be derived using [19], which is Ivanyos 2012.
* [Ivanyos, QIC 12 (2012), 661-669](https://www.rintonpress.com/xxqic12/qic-12-78/0661-0669.pdf):
  Section 1 specifies a coherent evaluation oracle mapping
  |x>|0> to |x>|f(x)>. [Section 4, pp. 667-668](https://www.rintonpress.com/xxqic12/qic-12-78/0661-0669.pdf#page=7)
  gives the determinant-power extension. Theorem 2 covers SL_n/PSL_n
  BORELS in time poly(n + log q + (1-q^(-1))^(-n)); Corollary 1 explicitly
  includes poly(log q) for constant n. At n=4 and odd q the extra term is
  at most 81/16. This is not, by itself, a theorem for a 2-plane or (1,3)
  flag. The parabolic extension is the DIKQS Section 8 statement.

## Paid Scalar Extension

The following are explicit audit calculations, not a claim that the papers
spell out this fixed-width circuit. Assume a public effective finite-field
presentation and matrix encoding. Write P=Stab_GL4(flag), H=P intersect SL4,
and let f hide H with f(g)=f(h) iff g^(-1)h belongs to H. Define

    D = (F_q^*)^4,                 d = gcd(4,q-1) in {2,4},
    G0 = {A in GL4 : det(A) in D} = (scalar matrices) * SL4,
    K = P intersect G0.

For A in G0, choose z with z^4=det(A), and evaluate

    F(A) = f(z^(-1) A).

Different roots differ by a scalar in the center of SL4, contained in every
full flag stabilizer. Thus F is well defined, and
F(A)=F(B) iff A^(-1)B belongs to K. This proves the hiding promise, not just
membership preservation. Determinant maps P onto F_q^*, so [P:K]=d.
Also [GL4:G0]=d, not necessarily 4. Ivanyos's general index statement should
be read with the exact index gcd(n,q-1), bounded by n.

**This is not an oracle on all GL4.** Fourth roots do not exist for the
other determinant classes. Arbitrary diagonal determinant correction is
not justified before an appropriate invariant subspace is known.

The costs and cleanup are explicit:

* Test membership in G0 by det(A)!=0 and det(A)^((q-1)/d)=1. Preparing a
  uniform matrix and conditioning on this test succeeds with probability
  product_(i=1..4)(1-q^(-i))/d > 1/16. Test before querying f; rejection is
  constant-cost in expectation and can be capped for bounded error.
* Fourth-root extraction needs only public field computation. For odd q,
  fix a verified nonsquare once, use deterministic finite-field
  Tonelli-Shanks square-root circuits twice, choosing a square first root.
  Such a choice exists for fourth powers. Finding the nonsquare by bounded
  random trials has exponentially small abort probability; all subsequent
  root computation is deterministic and reversible in poly(log q) time.
* Keep A, compute z and S=z^(-1)A in scratch registers, query f(S) once,
  and uncompute S,z and arithmetic scratch from A. Only the fixed-width
  label remains with A. Measure/discard that label for coset sampling;
  do not leave S or a determinant/root register entangled before Fourier
  sampling. No label interpretation, free label erasure, or inverse-f
  query is used. Inversion changes coset convention with the same cost.

## Why This Suffices For Unknown Flags In SL4

This is a fixed-dimension instantiation of DIKQS Sections 4-5, not a
generic inference that every finite-index HSP is easy. Let T be the
smallest nonzero hidden flag member. The relevant published ingredients
are [Proposition 7, Section 4, and Sections 5.2-5.3](https://arxiv.org/pdf/1406.6511v2#page=7).
The following calculations check their restricted-domain interface.

1. **Obtain a candidate line inside T.** Sample a random hyperplane R via
   a uniform nonzero covector, with constant-probability rejection. Its
   pointwise-unipotent stabilizer N lies in SL4. When dim(T)>1 and R does
   not contain T, the additive intersection H intersect N has image support
   R intersect T. Thus the Section 5.2 abelian probe already uses legal
   original queries; choose any line in its nonzero support.
   When dim(T)=1, use the Section 4 affine-complement Fourier procedure
   on G_R intersect G0, with G_R the pointwise stabilizer of R. Prepare this
   group directly in a public basis using parameters (b,v) in D x F_q^3;
   filtering b from F_q succeeds with probability (q-1)/(dq)>=1/6.
   No rare postselection from GL4 onto G_R is used. If R avoids T, the
   restricted oracle hides a complement whose multiplicative parameter
   runs through D. Its cosets, after subtracting I, occupy (q-1)/d points
   of the same affine q-point line used in that procedure. Each Fourier
   outcome on the correct perpendicular space therefore has weight
   (q-1)/(dq) times the uniform weight there. Three samples span that
   3-space with probability greater than

       (1/4) * ((q-1)/(d*q))^3 >= 1/864.

   R avoids T with probability greater than 2/3. This is a constant loss,
   including q=3,5, not a q-sized search. Run both candidate procedures;
   neither needs the unknown dimension. Their algebraic conclusions hold
   conditional on correct abelian learning and ideal Fourier sampling.

2. **Certify containment using only SL queries.** For a candidate line L,
   query generators of

       N_L = {I + t : image(t) contained in L, t(L)=0}.

   All have determinant one. They lie in H exactly when L is contained
   in every hidden flag member, equivalently L<=T. Indeed, if a nonzero
   flag member misses L, a suitable such transvection moves a vector out
   of it. There are 3 log_p(q) additive generators, where q=p^r.
   Compare their labels to f(I). This is an exact containment check.

3. **Now construct a genuine smaller GL oracle.** Choose a public
   complement C to the certified L. For g in GL(C), set

       iota(g) = det(g)^(-1) on L, and g on C.

   This is an explicitly computable homomorphism GL3 -> SL4. The oracle
   g -> f(iota(g)) hides the FULL quotient-flag stabilizer on E/L, with
   one original query and clean public workspace. The original DIKQS GL
   theorem now applies literally. To decide whether L is itself a flag
   member, use the reverse additive group I+Hom(L,C), fixing C pointwise.
   Its additive kernel is Hom(L,T intersect C), trivial exactly when
   L=T. Learn this kernel by abelian HSP. Lift the quotient flag, appending
   L only in that case. This is the containment/recursion distinction in
   Section 5.3; it prevents adding a spurious flag step.

Consequently the (2) case and the parent's (1,3), (1), (3) cases are covered
without type advice. In the (1,3) case, once L is the hidden line, the
smaller oracle hides the 2-plane B/L in GL3. A complete flag is also already
covered directly by Ivanyos's Theorem 2. The constant d^3 accounting here
is specific to dimension four, not a new uniform-in-n complexity proof.

Bound trials, amplify success, and budget additive-learning and entire
state-preparation/QFT instrument errors across polynomially many calls.
Total original queries and public gates are polynomial in log q,
log(1/epsilon), and label width. A pure poly(log q) gate claim additionally
requires label width polynomial in log q; the oracle's internal evaluation
cost is not silently declared free outside the oracle model.

## PSL And The Intersection Caveat

For PSL, no extra information is required: the full stabilizers contain
Z(SL4). An SL oracle descends to PSL, and a PSL oracle lifts by the public
quotient map. Matrix representatives can be canonicalized over the at most
four scalar multiples in Z(SL4), using polynomial field work and one oracle
call. This does not confer arbitrary GL access.

[Denney-Moore-Russell, arXiv:0809.2445v2](https://arxiv.org/pdf/0809.2445v2#page=2),
Section 2, begins with an unnumbered restriction observation: f restricted
to F hides H intersect F; distinguishing these intersections can reduce a
promised HSP when they identify the original candidates. Its Lemma 1 is
the k-transitive stabilizer-index calculation, not a universal solver.
Efficient subgroup access, an efficient intersection-HSP algorithm, and
efficient decoding back to the original stabilizer still need justification.
Sections 4-6 supply the PSL(2,q)-related application; Section 7 explicitly
notes that its AGL reduction does not immediately give an efficient new
algorithm. This does not itself solve orthogonal point stabilizers.

## Consequence For The Parent

Conditional only on the separately established FULL-parabolic pullback in
the parent's [RESULT.md](/Users/jaspersands/Developer/qsearch-research-work/orthogonal-a3-subsumption-2026-10-27/RESULT.md),
the prior-art SL4 solver supplies the missing interface for all four listed
types. Composing its one-query SL evaluations with the parent's one-query
pullback preserves polynomial cost. No assumption of a supplied GL4 oracle
is needed. The parent's exterior map, fiber controls, and all-rank geometric
correspondence were not re-audited here. This verdict establishes the cited
solver's applicability, not a general novelty or hardness certificate.
