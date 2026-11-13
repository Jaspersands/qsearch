# Balanced expanded Witt decomposition

2026-11-13. Full native expanded decomposition/isometry CLOSED WRITTEN under
the retained GRH arithmetic interfaces. Full337LF fixed-rank and250LF balanced
proofs, plus651LF paid alternative, parent read and checked. Start STATE/TRAPS, then corpus
been-tried/baselines for balanced Witt decomposition and actual primary
sources. The previous ternary INTEGRAL-isometry seed remains open; this is
a different native output over a field, not a claim that its gate disappeared.

## Problem, mechanism, and reason to test it

Native input: a totally imaginary number field K of growing degree N,
explicit compatible defining polynomial/maximal-order basis/table, and a
nonsingular symmetric d-by-d matrix Q over K, expanded binary coordinates.
Output a FULL EXPANDED basis W with W^T Q W equal to a sum of canonical
hyperbolic planes and an anisotropic form of rank <=4. Both N,d grow. A
subsequent exact rational isometry of two such forms is also covered;
integral isometry, real-field extension, short lattice witnesses, novelty,
hardness, implementation and quantum execution are not claimed.

Target quantum polynomial(native bits,log(1/eta)) BIT/gates/output under
the explicit GRH of the admitted scalar norm backend. The expected benefit
is replacing the same classical class/unit/norm arithmetic by known quantum
arithmetic. No proven classical lower bound or asymptotic separation follows.
Supplied quadratic towers retain the stronger existing ERH factoring baseline.

The new norm-residue operation first upgrades the existing single-five-plane
isotropic-vector construction to expanded output: only one constant-rank
quaternion splitting and its fixed-size descent follow the expanded front end.
This is a direct consequence, not a reason to spend another paid confirmation.
The NEW operation to test is height-controlled composition of many such calls.

Diagonalize once. Each leaf is a one-dimensional form. At each node merge
the two surviving anisotropic cores, of total rank <=8, and split off all
hyperbolic planes. Carry only the new core of rank <=4. A balanced tree has
depth ceil(log2 d). The bound on anisotropic rank uses the totally imaginary
number-field Hasse principle and finite u-invariant4; it fails over real fields.

The decisive lemma, now independently derived and parent checked, is a
native fixed-rank <=8 reduction whose
coefficients AND change-of-basis have extensive absolute height

    H_out <= C H_in + P(charged field data),

with an ABSOLUTE constant C, independent of N,d and coefficient heights.
Here H_K(x)=N h(x), summed only over bounded-rank tuples. A factor N in C
would leave N^O(log d), and a nonlinear power of H would be worse. Neither
is acceptable. The expanded norm solver alone guarantees only a polynomial
output bound and does not prove this affine lemma.

Candidate height repair: the reviewed C1 ideal reset/C2 weighted squareclass
compression gives absolute-slope conic shortening of an ALREADY EXPANDED
witness. Its former tower root extraction can now be replaced by actual
Lenstra polynomial factoring over the original K. For q5 local gluing, take
a short nonzero gamma in the CRT ideal I by Minkowski LLL and reduce a CRT
representative modulo gamma*O_K, a SUBLATTICE of I. The basis gamma*omega_i
may yield a coefficient-height slope independent of N. These details, local
integrality, auxiliary discriminants and all fixed-rank maps need proof.

## Classical and source checks

Corpus returns existing compact isotropy, class/unit and LLL baselines;
lexical nonmatches are not novelty or hardness evidence. Actual primary
Fukshansky Theorem1.3 gives small-height Witt components by an existence
argument, starting with an existential maximal isotropic subspace. It does
not by itself supply this native polynomial compiler. Actual Koprowski–
Rothkegel assumes principal generators, S-class/S-unit computations and
Algorithm8 enlarges support until an F2 system solves. Its stated output is
an abstract anisotropic form, not a full embedded basis with this clock.
Retained PDFs/text/metadata: audits/sources/2026-11-13-balanced-witt/.
No exhaustive literature priority claim or claim their algorithms are slow.

Cheapest falsifiers: trace every height recurrence symbolically before any
quantum implementation; expose N-dependent slopes, nonlinear input-height
dependence, uncharged compact expansion, growing field towers, supplied
starting witnesses, unbounded support searches or basis reconstruction costs.
No backend or new research infrastructure is proposed. If the height lemma
fails, retain the single-vector corollary but do not promote full decomposition.

## Parent affine-height construction and checked fixed-rank proof

The following construction is now established at the WRITTEN-proof level,
conditional on the retained GRH norm/factoring and C1/C2 interfaces. Full337LF
independent proof, parent read and checked:
audits/reviews/2026-11-13-witt-affine-height.md. Write H=N*h.
First use the existing weighted squareclass compression C2 on EACH diagonal
coefficient a_i. It returns integral a_i'=a_i*gamma_i^2 with
H(a_i')<=2H(a_i)+log|Delta_K|+O(N^2). Since gamma_i^2=a_i'/a_i,
H(gamma_i)<=(H(a_i')+H(a_i))/2. This normalizes all fixed-rank coefficients
integrally with ABSOLUTE slope, while retaining the expanded coordinate map.
It is not rational-integer denominator clearing, which can introduce N.

The conic-shortening proof in native-tower-witness-shortening.md otherwise
works over arbitrary K: replace its sole tower-specific root extraction by
Lenstra factoring. Its bound is64*(H_coeff+log|Delta_K|+N^2), independent
of the OLD expanded witness. A first expanded norm witness is now available.
For a quaternion over E, shorten the conic x^2-u*y^2=v*z^2 and use x/z,y/z
in its splitting map. Its height has absolute affine slope in H_E(u),H_E(v),
log|Delta_E| and [E:Q]^2. When E=K(sqrt(D)) is the q4 discriminant extension,
the retained order calculation gives log|Delta_E|<=2log|Delta_K|+2Nlog2+2H_K(D).
Thus no N multiplier hits coefficient height. The q3/q4 kernel/minor descent
and K+Ksqrt(D) extraction have constant algebraic degree. Expanded basis
conversion may cost polynomial work, but does not alter intrinsic height.

For q5, after integral normalization put a=a4,b=a5,delta=-b/a. Keep the
existing local binary-value chooser at every p in S (dyadic and q1 coefficient
support), but normalize its LOCAL targets before CRT as follows. If delta
is not globally square, write z=s0+t0*sqrt(delta) in O_L, L=Ksqrt(delta),
using the split/ramified/unramified ideal chooser. In the unramified case
choose from UNIT generators only: surjectivity of unit norms ensures a
nonsquare unit norm exists. Then v_p(Nz) is0 or1. Put s0,t0 := 2b*s0,2b*t0.
These lie in O_K GLOBALLY: sqrt(-ab) is integral, 2s0_old=Tr(z), and
2b*t0_old=-(z-bar(z))*sqrt(-ab). Their norm value is
a*(2b)^2*Nz, with valuation <=v_p(a)+2v_p(b)+2e+1, e=v_p(2).
The trivial s=1,t=0 branch has the same bound after the scaling. In the
globally split branch, with r^2=-b/a, use (pi+1)/2,(pi-1)/(2r), then2b
scaling: b/r has square -ab, so it is integral. The resulting norm has the
same valuation bound. Local targets can have large expanded heights, but
only their residues are propagated, never those heights.

Choose M_p=4e+v_p(a)+2v_p(b)+3. Since all local targets are integral, replacing
s0,t0 modulo p^M preserves the represented nonzero value's squareclass:
M>2e+v(c0)-min(v(a),v(b)). Let I=product_(p in S) p^M. Then

 log N(I) <=4Nlog2+H(a)+2H(b)+3*sum_(p in S)log N(p),
 sum_(p in S)log N(p)<=Nlog2+H(a1)+H(a2)+H(a3).

Every propagated coefficient therefore has an ABSOLUTE slope. Obtain CRT
representatives in O_K, choose short nonzero gamma in I by the existing
Minkowski-Gram LLL routine, and reduce each representative modulo gamma O_K
by exact coefficient rounding in gamma*omega_i. This sublattice lies in I.
For W>=max_(sigma,i)|sigma(omega_i)|, the reduced representative u obeys

 H_K(u)<=log N(I)+(1/2)log|Delta_K|+O(N^2+Nlog(NW)).

The field-basis constant belongs ONLY to the original K. Do not run this
height estimate in a coefficient-dependent quadratic field: its basis term
could reintroduce a coefficient-degree multiplier. Now c=a*s^2+b*t^2 has
absolute affine height and the old local/Hasse proof makes q1+<c> isotropic.
Apply the shortened q4 construction and lift its vector using s,t.

For rank<=8, choose any five diagonal coordinates when rank>=5 (there are
no real places), and use the same construction. Given a short isotropic x,
select e_j with B(x,e_j)!=0, let y=e_j/B(x,e_j), and replace y by
y-q(y)x/2. Then B(x,y)=1 and both norms vanish. Project remaining vectors
by z -> z-B(z,y)x-B(z,x)y; fixed-size elimination gives the complementary
basis. At most four such reductions and their constant-size diagonalizations
occur in an eight-dimensional merge. Their number and algebraic degrees are
absolute constants. Combining the stated affine subroutine bounds would
therefore yield H_out<=C H_in+P(original field) with absolute C. The exact
clock/height/reset/auxiliary-basis interfaces have the explicit bound below.

For M the maximum absolute integral multiplication-table coefficient, put
W=N*max(1,M), ell the integer binary bitlength, and
F=10+ell(|disc K|)+4N^2+N*ell(2NW). The multiplication matrices bound every
|sigma(omega_i)| by W. The complete rank<=8 basis and final core obey

    H(P)+H(C) <= C8*(H(Q)+F),
    C8=128*(43000000*3^12288)^4.

The proof counts at most4096 scalar gates for each fixed-rank diagonalization,
8192 for its return maps/hyperbolic projection, and at most4 rounds. Its huge
absolute constant is constructive, not a practical resource estimate. Raw
first norm witnesses and temporary local targets use the inherited backend
polynomial bit cap, not this propagated-output affine cap. Only shortened
output enters the recurrence. Front-end quadratic fields have degree<=4N;
the norm backend's internal fields have their separately paid polynomial bound.

## Exact cheap controls

One Sage batch completed without retries: six CRT representative reductions
in powers1,3,7 of a nonprincipal ideal of Q(sqrt(-5)); integral2b coordinate
normalization for a half-integral quadratic element; and hyperbolic/complement
projection over that imaginary field. Script/result in audits/controls/balanced_witt/.
The short gamma is supplied in this finite congruence test: it does NOT test
the Minkowski-LLL backend or prove a height bound. No native Witt or quantum
algorithm was implemented. All-input height is a separate written proof;
the full composition has its separate checked250LF proof below.

## Checked balanced composition using the constructive (W) bound

Let h_j bound the fixed-size core coefficient tuple at depth j and let g_j
bound the MAXIMUM single-coordinate height in each embedded core basis vector
(not the sum over d coordinates). In diagonal input coordinates g_0=0.
Two child cores have combined height <=2h_j, so (W) gives

 h_(j+1) <=2C h_j+P,   H(each merge coefficient)<=2C h_j+P.

Each new coordinate is a sum of at most8 products of a child coordinate and
a merge coefficient. Therefore

 g_(j+1) <=8g_j+8(2C h_j+P)+Nlog8.

For u_j=max(h_j,g_j,N,1), the loose recurrence
u_(j+1)<=(16C+16)u_j+8P+Nlog8 suffices. With depth<=ceil(log2 d), it is
polynomial jointly in d,N and the expanded input, because C is ABSOLUTE.
Unbalanced last levels pass single children through unchanged; no zero form
or false anisotropic leaf is inserted. Previously emitted hyperbolic planes
remain untouched and orthogonal to the surviving cores. Their coordinate
heights obey the bound at the depth at which they were emitted. At most d-1
merges occur; at most d^2 output coordinates carry an additional polynomial
size factor after this maximum-coordinate bound. No d multiplier is iterated.

The one initial growing-rank diagonalization is paid by fraction-free/minor
bounds, with polynomial coefficient and basis heights. Multiply its basis
by the completed balanced basis ONCE: each final coordinate sums d products,
so its height is bounded by d*(initial max height+g_depth)+Nlog d. This
factor is not fed back into the recurrence. Applying sparse merge matrices
bottom-up updates only the <=8 active core columns of the current forest;
even intermediate expanded bases have the same depth bound. No d-step dense
matrix-product height estimate or generic compact expansion is needed.

To compare two forms, unequal Witt indices reject. For common anisotropic
core rank r<=4, apply (W) once to C_A directsum (-C_B). Witt cancellation
says the cores are isometric exactly when this rank<=8 form is hyperbolic.
Choose one isotropic column from each returned H pair and write [X;Y].
Anisotropy of both cores makes the two r-by-r projections X,Y invertible:
a nonzero kernel vector would give an isotropic vector in one core. Then
X^T C_A X=Y^T C_B Y, so T=X*Y^-1 has T^T C_A T=C_B. Rank0 uses the empty
identity. If P_A^T A P_A=H^w+C_A and P_B^T B P_B=H^w+C_B, return
U=P_A*(I_(2w) directsum T)*P_B^-1. Its inverse/global products occur ONCE,
with ordinary growing-rank polynomial minor bounds, and U^TAU=B is checked.

Every FRONT-END quadratic field is temporary over ORIGINAL K with degree<=4N;
the imported norm backend's internal fields retain its separately paid
polynomial bound. No field tower follows tree depth. Allocate eta across O(d) complete
fixed-rank calls, each with its own capped arithmetic/source budget. All
branches need explicit coordinate-bit caps derived from the above bound,
the original-basis coordinate/absolute-height inequality, and a computable
upper bound on input heights. Exact norms, basis identities and declared
nonzero quantities are verified. A contradictory norm NO or oversize return
is ABORT, never an automatic retry. Bad arithmetic branches cannot feed an
unbounded next call. The stable250LF independent proof in
audits/reviews/2026-11-13-witt-balanced-clock.md instantiates this composition
with the checked C8,F and explicit trace-dual coordinate/working-bit caps.
Set a=16*C8+32 and k=ceil(log2 a), an ABSOLUTE exponent. With the proof's
polynomial diagonalization/input bound U0, every tree core and embedded
coordinate has height<=a*d^k*U0. Final original-basis multiplication/inversion
occur once. Accepted erroneous returns can have larger intrinsic height than
this correct-run cap; the proof explicitly converts their coordinate-bit cap
back to H_bad and charges all subsequent arithmetic with that larger bound.
Every nonempty next core is checked nonsingular. The result is a bounded-error
quantum polynomial-BIT/gate/workspace/output construction under the retained
GRH interfaces, for every native input in the stated scope. Exact positive
Gram identities are verified, while negative/anisotropy correctness retains
the backend error contract. The absolute exponent is enormous; no practical,
implemented, formally verified or human-refereed algorithm is asserted.

## API status

Claude balanced-composition bundle ended EMPTY at64k, estimated USD1.322232;
process reaped. It supplies NO mathematical evidence and is not retried.
The independent balanced proof was subsequently fully parent checked. The distinct
OpenAI affine-height report completed (651LF fully parent read; process reaped),
estimated USD2.666350. Its material claims have the following disposition:

- Its locally integral binary chooser is a valid alternative to global2b
  integralization: local valuations normalized to0/1, trace denominators
  bounded by e, and M=|v(a)-v(b)|+4e+2 give modulus mass<=4H_coeff+6Nlog2.
  Fractional targets are reduced using their denominator ideals locally; no
  globally clearing rational integer is propagated. The parent checked the
  squareclass, unit-generator, integrality and precision algebra.
- Its explicit two-branch q4 descent satisfies both splitting-kernel equations
  using X0*X1=u*Y0*Y1; each returned vector is nonzero. This independently
  removes any hidden choice of ruling or Hilbert90 witness. The retained
  counted C8 bound above remains the canonical bound; its smaller numeric
  constants are unnecessary and not imported as a separate resource claim.
- Its exact denominator warning is valid: for even N and prime p>=3,
  f=T^N+T+p has all roots outside the unit circle, is irreducible by its
  prime constant term, and has no real root. For K=Q(alpha), H(alpha)=log p
  and the prime (alpha) has norm p with v_(alpha)(p)=1. Clearing the tuple
  (alpha^-k,1) by a rational integer requires p^k, raising its height slope
  from k*log p to N*k*log p. This refutes that normalization, not Witt reduction.
- Its norm/C1/C2 interfaces and GRH remain imported assumptions checked in
  the prior proofs; the paid report does not independently certify them.
  No theorem follows from its opening acceptance label. Both API jobs are
  terminal; round estimate3.988582, not invoices or a measured balance.

Further classical scope check: actual Magma handbook1538 lines29-35 separates
Simon's rational-base minimization from the general-number-field Lagrange
reduction. The latter reduces via a short vector in two copies of the base
field, then either an easy search succeeds or NormEquation is called; a
class group may improve reduction. It does not state a uniform factoring-
only clock in growing degree. Actual Simon ConicsSimon.pdf sections2/3 give
the norm/S-unit and Lagrange descriptions; the phrase about reduction over
number fields is not adopted as an impossibility theorem. Actual vanHoeij–
Cremona conicFT.pdf is over F(t), with recursive base-field conic calls,
not a general-number-field constructor. These are scoped baseline checks,
not a proof that no stronger classical algorithm exists. Sources retained
in audits/sources/2026-11-13-balanced-witt/.
