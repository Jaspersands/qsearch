# 2026-11-13 Local ternary source compiler: source gap, with two paid subcases

Independent audit of `EXPANDED_NORM_TERNARY_TRANSPORT.md`, Beli's actual
representation paper, the additionally supplied classification paper, and First's
actual proof. No external calls, numerical controls, or source-status inference.
All locators below count physical LF with `split('\n')`; PDF form feeds account
for different `splitlines()` counts. The retained Beli representation text has
6959 LF, classification text 1091 LF, and First text 302 LF.

**Disposition.** These sources do not yet pay a uniform constructive seed for
arbitrary same-genus ternary lattices over dyadic local fields. This is a specific
missing coordinate-realization step, not a counterexample to local isometry or
to a polynomial classical/quantum compiler. The representation proof uses the
classification theorem precisely where the required coordinates would be needed;
the classification proof translates O'Meara's criterion and supplies no such
coordinates. First does pay the odd, unimodular, fixed-rank subcase, given the
already available expanded rational isometry. A finite seed-to-isometry lift
below is also paid. The full integral transporter/spinor-offset gate stays open.

## 1. The exact native operation

Let F be a finite extension of Q_p, O its valuation ring, pi a uniformizer,
v(pi)=1, e2=v(2), and q the residue-field size. A,B are nonsingular symmetric
integral 3-by-3 Gram matrices, promised integrally isometric. Local arithmetic
must use explicit finite encodings; no enumeration of q elements, or of all
matrices over O/pi^h, is allowed. Requested time is polynomial in local degree,
e2, log(q), the relevant valuations, native coefficient bits, and output precision.

The missing output can already be limited to a matrix X0 mod pi^h with

    det(X0) a unit,     X0^t A X0 = B mod pi^h,
    h = v(det B) + 2 e2 + 1.                         (1)

Such a seed suffices by section 4. Existence follows from the same-genus promise;
finding it is the issue. An arbitrary rational isometry, a list of invariant
squareclasses, or stabilizer spinor-norm generators is not this output.

## 2. Where the Beli proof stops being a coordinate construction

Read source: `audits/sources/2026-11-13-expanded-norm/beli_representation.txt`,
arXiv:1905.04552v2. The introduction explicitly formulates classification and
representation as decision problems (LF21–26). Good-BONG construction is imported
from [B2, section 7] (LF94–114); its uniform coordinate/precision clock is not
proved in this paper. Even granting a coordinate good-BONG compiler leaves the
following more substantial gap.

* Theorem 2.1 (LF491–499, printed pp10–11) is an equivalence of representation
  with valuation/defect and rational-subspace representation conditions.
* Proposition 6.4, **same rank and volume**, is the branch directly applicable
  to an isometric pair. Its proof begins “by using [B3, Theorem 3.1]” (LF2657–2674,
  printed p53), and checks the four invariant conditions. It does not output a
  matrix, vector, or change-of-BONG coordinates.
* The apparently constructive alternative, Lemma 8.14, does not remove this
  reliance even in rank three. It seeks a new first BONG value b1 (LF5320–5326).
  After the binary branch LF5404–5408, the ternary R1<R3 branch selects a unit
  eta and proposes values `(epsilon*a1, epsilon*eta*a2, eta*a3)`. At LF5423 it
  explicitly invokes **[B3, Theorem 3.1]** to prove this is another BONG of M;
  LF5424–5438 verify invariants and rational-space isometry, not coordinates.
* In the rank-three R1=R3 branch, LF5519–5536 again construct candidate values
  and invoke Lemma 7.11. Lemma 7.11 itself begins “We use [B3, Theorem 3.1]”
  (LF4151–4164). Choosing eta by LF5540–5560 therefore still leaves exactly the
  same coordinate-realization obligation.
* Section 9 uses norm generators x,y with equal norms and an isometry of their
  projected lattices (LF5755–5782, printed pp115–116). This describes how to
  assemble a map **after** those generators/maps are constructed. The preceding
  ternary existence invocations do not supply them.

The final source hop was actually checked: `beli_classification.txt`,
arXiv:0903.3726v1. Its introduction says it translates O'Meara's theorem into
BONG language (LF13–18). Section 3 explicitly imports O'Meara 93:28 (LF643–676).
The proof of Theorem 3.1 (LF688–702) reduces its conditions to those of 93:28;
Lemmas 3.3 (LF722–769) and 3.9 (LF883–918) perform those equivalences. They do
not construct an integral isometry. No assertion is made here about constructive
content in O'Meara's unread proof, and no further source hop is required by this
audit's disposition.

Thus a precise sufficient new lemma is: from a coordinate ternary good BONG and
another certified isometric good-BONG value triple, produce the coordinate
change modulo (1), with polynomial work/precision and no residue enumeration.
The cases `R1<R3` and `R1=R3` above must both be covered. Merely rechecking Beli's
classification conditions would be circular as a proposed realization algorithm.

## 3. Scalar choices are not themselves an exponential obstruction

The source does not require a scan through all residue elements in Lemma 8.1:
its choice is just a residue outside `{0, epsilon_bar}` (LF4842–4851). Over
F_(2^f), f>1, a residue-field basis gives such a choice with O(f) elementary work.
For f=1 the proof explicitly takes the separate exceptional branch.

Lemma 8.2 (LF4863–4883) supplies prescribed-defect/Hilbert-sign elements: its
boundary case invokes [H, Lemma 3], and the other case tests two or three scalar
choices. A constructive unit-filtration/Hilbert-pairing routine could make these
choices without residue enumeration. This audit does not charge that boundary
routine merely from the existence statement. More importantly, even giving all
these scalar choices for free does not supply the ternary coordinate map above.

Quantum inversion of a quadratic norm on explicitly generated finite local unit
groups is an allowable possible ingredient. Nothing here requires a classical
solver where a quantum one would suffice. But such a reduction must specify the
lattice/order congruence constraints, truncation precision, generators, evaluation
cost, and an integral coordinate realization. Unrestricted field norm inversion
alone does not ensure that realization: in the split plane `<1,-1>`, take

    x=(pi+pi^(-1))/2,   y=(pi-pi^(-1))/2.

Then x^2-y^2=1 and `[[x,y],[y,x]]` is a rational isometry, generally nonintegral,
although the identity is an integral isometry. This only rejects the inference
“any norm witness gives the required integral map”; it rejects no norm algorithm.

## 4. A fully explicit seed-to-isometry lift

Put delta=v(det B), h=delta+2e2+1. Lift a solution of (1) to an integral X0 and
set E=X0^t A X0-B, Z=B^(-1)E. Since adj(B) is integral,

    v(Z) >= h-delta = 2e2+1,
    Z^t B = B Z.

Use the matrix series

    R=(I+Z)^(-1/2)
     = sum_(j>=0) (-1)^j binom(2j,j) Z^j / 4^j.

The j-th nonconstant term has entry valuation at least j. Thus R is defined,
R lies in I+pi*M3(O), and is B-self-adjoint. It commutes with I+Z and satisfies
R^2(I+Z)=I. Consequently X=X0 R is integral, invertible, and

    X^t A X = R^t B(I+Z)R = B.

This also proves that (1) is a finite sound certificate. For X mod pi^P retain
j<P. There are O(P) fixed-size matrix products; binomial coefficients have O(P)
bits and denominators divide 4^P. A deliberately loose working precision
`10(P+delta+e2+2)^2` pi-adic digits covers the fixed-size inversion of B (loss at
most 2delta under perturbation) and all divisions by 4^j (loss at most 2e2 P).
All local arithmetic therefore has polynomial BIT cost in the stated quantities.
No exhaustive residue search or infinitary stopping rule is used in this lift.

This does not find X0. Enumerating all its possible residues has q^(Theta(h))
candidates even at rank three, which is not the requested polynomial clock.
Properness and a spinor offset also require the chosen rational identification;
a raw isometry between A and B is not itself an orthogonal self-isometry.

## 5. What First actually pays

Read source: `first_unimodular.txt`, arXiv:1404.5022v2. Theorem 1 explicitly
requires v(2)=0 and unimodularity (LF32–42). Its proof takes a **given** rational
isometry, performs valuation-minimum matrix elimination (Proposition 2,
LF199–216), reduces its diagonal valuation patterns, and uses the displayed
rational block formula at LF174–198. The inverse `(2-pi*x-pi*z)^(-1)` there is
integral because 2 is a unit. That argument does not cover dyadic fields.

Remark 5 (LF248–275) gives arithmetic-operation counts and expressly cautions
that this is not a general BIT bound. For the present fixed rank three, however,
the proof uses a constant number of matrix operations and valuation-pattern
steps, with no iteration once per residue. Starting with the already paid
expanded rational isometry, each matrix is at most 3-by-3; rational additions,
products, inversions and valuation queries have polynomial BIT cost in the
expanded native number-field encoding. Uniformizer powers have exponents bounded
by the encountered input valuation sizes, which are charged parameters. A
constant number of such operations preserves polynomial expanded height.
Hence this is a valid polynomial native compiler for the **odd, unimodular**
subcase. It supplies neither a dyadic extension nor an arbitrary nonunimodular
block-matching theorem.

The actionable remaining gate is the coordinate ternary BONG realization in
section 2, or another explicit compiler producing (1). There is no source-backed
uniform dyadic seed theorem here, no algorithmic impossibility result, and no
promotion of the full integral ternary endpoint.
