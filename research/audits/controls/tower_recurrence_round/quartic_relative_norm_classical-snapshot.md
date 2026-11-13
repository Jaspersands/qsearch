# Native quartic squareclasses reduce classically to integer factoring

2026-11-13. REVIEWED WRITTEN polynomial-BIT classical algorithm with a
charged integer-factorization oracle. The complete native/support/conic
composition and its independent proof notes have been parent-read.
No full implementation, practicality, novelty, classical polynomial
factoring, hardness, separation or quantum execution claim.

## Exact scope and resource model

Input a native monic irreducible quartic h in Z[X], defining L, and a
list S_Q of rational primes containing2 and every prime ramified in L.
Suppose L contains a quadratic subfield F, where S
contains ALL F-primes above S_Q. No odd S-class hypothesis is required. Output a complete explicit basis of
L(S_L,2)={alpha modL*2 : all valuations outside S_L are even}, where
S_L contains all primes above S_Q. No subfield, generators, units, ideal
principalizations, local frames or conic solutions are supplied.

The earlier odd S-class promise is removed by the exact support-obstruction
kernel below. The result now covers EVERY irreducible quartic with a quadratic
subfield, including nonnormal cases, with the same factoring-oracle resource
model. Quartics without a quadratic subfield and growing towers remain open.
The one-finite-ramified-prime Galois family is a contained special case.

Cost is polynomial in the native coefficient/support BIT length and
log(1/eta), with polynomially many INTEGER FACTORIZATION calls on
polynomial-bit intermediates. It returns a correct complete basis, or
ABORT with probability at most eta. The exact factoring oracle is charged;
factoring only the original discriminant is NOT the resource model.
Every accepted conic witness is checked exactly. Constants from fixed
dimension<=9 isotropy may be enormous.

For native monic squarefree odddegree branch polynomial f, all support
primes divide2disc(f). If every branch field is rational, quadratic, or
a quartic containing a quadratic subfield, combine this construction with the retained
classical all-prime local Kummer compiler and global binary norm matrix.
The resulting exact Selmer-dimension computation reduces to integer
factoring in polynomial BIT time. It does not require complete S-units,
GRH, an ideal class group, a regulator or Pell solutions. This removes
the extra unit-computation primitive from that subclass; it leaves the
factoring resource explicit. General growing-degree class coverage and
classical Selmer complexity remain open.

## Native radical and local norm construction

For h=X4+aX3+bX2+cX+e form
 R(T)=T3-bT2+(ac-4e)T+4be-a2e-c2.
A rational root u specifies a quadratic subfield. Rational polynomial
factorization finds such roots; no divisor enumeration. With theta=X modh,
Ds=a2-4b+4u. If Ds!=0, put
 s=-(a theta2+2(b-u)theta+c)/(2theta2+a theta+u),
 t=(c+s*u)/(2s+a).
Then (2s+a)2=Ds, theta2-s theta+t=0 and Ds is nonsquare by irreducibility.
If Ds=0, put s=-a/2,t=s theta-theta2; then (2t-u)2=u2-4e is nonzero
nonsquare and t generates F. In both cases d=s2-4t and z=2theta-s give
L=F(z),z2=d. Squarefree extraction gives F=Q(sqrtD) and exact native
coordinate conversions; constant-size rational inverses have polynomial
bit height. Full formulas and proof: the271line native review below.

A rational resolvent root ALONE does not certify Galois (D4 quartics also
have one). With n=N_F/Q(d), n a rational square gives V4; n/D a rational
square gives C4; neither gives a nonnormal extension. The lift sends
z to c0/z with c0²=n; its square acts by tau(c0)/c0. These rational-square
tests pay exact recognition. Field ramification can be certified from
the native maximal order/discriminant, not inferred from disc(h).

Outside S, unramifiedness forces v_P(d) even. Compute complete F(S,2)
by QUADRATIC_NATIVE_SQUARECLASSES.md. The desired relative norm space is
 V=F(S,2) intersect N_L/F(L*).
It is the kernel of Hilbert-symbol rows (a,d)_v at S and real places;
outside S odd even-valued classes have symbol1. Quadratic Hasse norm /
Hasse--Minkowski proves completeness. Odd-place valuation/residue formulas
and exact real signs are polynomial. At2 enumerate the complete norm
image from units modulo1+P_H^(2e_H+1) and a uniformizer of each quadratic
local extension H/E. Absolute degrees<=4 give <=3840 unit representatives;
base E-frame has <=48. All labels use ONE native frame. Integral norms,
trace discriminants and local indices bound precision/conversion losses
polynomially; constant table cardinality is not free inputprecision.

## Exact sequence and the constructive support correction

The complete sequence is
 0 -> F(S,2)/<d> -> L(S_L,2) --Norm--> a(C) ->0,

where C is the support-obstruction kernel below, in coordinates of a basis
of V. It may be a proper subspace of V.
For the kernel, if N(alpha)=c², then
 (alpha+c)²=(Tr(alpha)+2c)alpha;
separate alpha=-c. Outside-S unramified valuations force the rational-
over-F representative into F(S,2). The restriction kernel is exactly<d>.

For each basis a of V, the relative conic solver below returns nonzero
beta=x+y*z with N(beta)=a*c² and polynomial-bit coordinates. It need
NOT already belong to L(S_L,2). At a split outside-S F-prime the two
beta valuations have equal parity; at an inert prime there is one parity.
These parities are the pullback of an F-ideal parity vector J. They can
be read as min(v_P(x),v_P(y)+v_P(d)/2) mod2 outside S.

Clear beta in an explicit integral order O_F[M0*z], using an integer R.
Factor R*abs(N_L/Q(R*beta)); its polynomial-bit size is paid by the conic
bound. All outside-S support is above these primes E. Compute complete
F(S union E,2) using the quadratic compiler. Let W be the image of its parity map to E outside S. For the
basis a_i of V and conic lifts beta_i, let J_i be their pulled-back parity
columns. Compute

    C=ker(c -> sum_i c_i J_i mod W).

For each basis vector c of C, solve in the enlarged quadratic basis for
gamma with parity sum c_i J_i; then gamma*product beta_i^c_i has even
outside-S valuations and norm squareclass product a_i^c_i. Conversely any
even-supported lift differs from this beta product by a square-norm element;
the trace identity expresses its squareclass by a base gamma belonging to
F(S union E,2), so its coordinate c lies in C. This proves that a(C), not
unconditionally V, is the entire norm image. No principalization or class
identity is computed. Odd S-class order is sufficient for C=V, but unnecessary
for computing C. Batch all conic supports into one enlarged quadratic matrix.

Polynomially many polynomial-bit fixed-degree products preserve bit size.
Coordinates of [d] in the original quadratic basis are obtained using
its recorded norm lifts and the same trace identity; take a complement
to<d> and append the corrected lifts for a basis of C. The exact sequence proves
spanning AND independence, not merely returned valid elements.

Strongest counterexample: the native cyclicquartic over Q(sqrt229) in
the paid relative-norm report has element-gcd1 conic coordinates but
common nonprincipal ideal(3,t), with odd numerator valuations at BOTH
primes over it. All28 exact assertions pass. Naive element-gcd or rational
prime correction fails. The enlarged-support construction escapes this example. A stronger new
complete control uses F=Q(sqrt(-14)), L=F(sqrt2), S_Q={2,7}: Cl(F,S)=(2),
V dimension4, obstruction rank1, C dimension3, and the resulting six quartic
generators have full rank in an independent complete S-squareclass space.
One obstructed lift has an odd denominator valuation at an inert prime over3.
Thus full-V surjectivity would give the wrong dimension7 instead of6.
Parent read the entire296-line proof and reproduced EXACT_CONTROL_PASS:
`audits/reviews/2026-11-13-relative-squareclass-obstruction-kernel.md`;
`audits/controls/tower_recurrence/relative_obstruction_control.py`.

## Paid relative conic backend over a quadratic base

For F=Q(sqrte) and nonsquare d in F, form quaternion A=H_F(d,a) directly.
Solubility of the norm conic is exactly splitting of A. Actual Kutas
1606.01053v2 Propositions12/15, Corollary19 and Theorem20/Remark21 reduce
this to at most three constant-dimensional rational4/6 quadratic forms.
The actual proofs were read; the GRH alternative is not used.

Proposition12 produces a nonzero traceless l with l² rational using an
indefinite6form; zero/nilpotent and alreadyrational branches are separate.
Choose an anticommuting w by linear algebra; handle w²=0 and rational
w² immediately. Proposition15's explicit4form supplies l' with rational
square. If l'²=0 return that zero divisor. Otherwise H_Q=<1,l,l',ll'>
is a rational quaternion subalgebra. Use Remark21 ALWAYS: the soluble
form alpha*x1²+beta*x2²-alpha*beta*x3²-e*x4² gives a nilpotent if x4=0,
or an element s²=e and the zero divisor s-sqrte otherwise. No rational
split/division-oracle branch or generic number-field algebra oracle.

Given zero divisor x1+x2u+x3v+x4uv, put
 X=x1*x3-d*x2*x4, Y=x2*x3-x1*x4, Z=x3²-d*x4².
Then X²-dY²=aZ² and Z!=0 because d is nonsquare and the divisor is
nonzero. The optional square-d branch is solved directly. Constant-depth
rational/quadratic arithmetic preserves the polynomial-bit outputs.
Source indexing/Gram typos and nilpotent cases are explicitly repaired;
no at-most-two-factoring-calls claim is retained.

The rational4/6 backend is now independently assembled and parent-read:
- Direct HNF lattice sums/preimages pay minimization in original
  coordinates. At each p there are <=v_p(detQ)+n steps; Lemma6 occurs
  at most once PER PRIME, with polynomial heights.
- Strict quadratic2Sylow generators are constructed via genus characters,
  halving, primitive conics and exact integralSL3 maps. Weak binary
  reduction gives h+(D)<=6absD and <=2log2(6absD) halvings. Conductor/sign
  data retained, no Pell/classidentity or enumeration.
- For integral indefinite unimodular Q in fixed dimension<=9, ordinary
  LLL on a determinant-one definite majorant either finds a zero or
  bounds all transformed Gram entries by n*2^(n(n-1)/2). Universal
  unimodular isotropy plus FINITENESS supplies a dimension-only search
  clock. Integral projection/HNF splits hyperbolic planes and returns a
  maximal isotropic basis. No growing-dimension polynomial claim.
- Simon4 uses genus-matched binary augmentation to unimodular6 and an
  intersection of dimension>=1. Simon6 uses7 then9, yielding >=2 then>=1.
  All coordinate backmaps precede intersections. The printed dyadic form
  has its sign repaired to3X²-(delta/12)Y². Specialized odd-prime Lemma8
  steps precede dyadic Lemma9 in dimension9. Only lower dimension bounds
  are used, not the source's stronger exact-intersection assertion.

All accepted witnesses are exact. Allocate abort probability across the
polynomially many modular root/conic/local calls; all clocks are bounded
polynomials in inputbits and log(1/eta). Factoring remains an explicit
oracle (or the known charged quantum factoring primitive).

## Evidence, primary sources and boundary

All review paths below are under audits/reviews/ and fully parent-read:
- 2026-11-13-quadratic-tower-support-correction.md (254lines).
- 2026-11-13-quartic-native-radicals-norms.md (271lines).
- 2026-11-13-bosma-stevenhagen-conic-clock-repair.md (264lines).
- 2026-11-13-simon-minimization-majorant-clock.md (250lines).
- 2026-11-13-simon-four-six-composition.md (280lines).
Paid report dispositions: 2026-11-13-classical-two-family-disposition.md.
Actual sources: https://arxiv.org/pdf/1606.01053 ,
https://simond.users.lmno.cnrs.fr/maths/Dim4.pdf ,
https://jtnb.centre-mersenne.org/item/10.5802/jtnb.170.pdf .
Local PDFs/texts/hashes are retained under audits/sources/.

The two native radical controls, the28assertion229 counterexample and the
new complete sqrt(-14)/sqrt2 obstruction control were run, not the full solver. Direct-dimension reciprocity/rayclass
reformulation still requires global residue positions; it supplies no
separate algorithm and no hardness. Do not build that subsystem or extend
this fixed-degree result by inertia. NEXT_CONSTRUCTIVE_MECHANISMS.md
compares independent full sparse relations and Gaudin transport routes.
