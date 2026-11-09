# Canonical Half-Factorial By Compact Quadratic Arithmetic

2026-11-06. WRITTEN bounded-error quantum composition under GRH, using
published number-field primitives and classical congruences. This is not
a new period-finding primitive, a novelty claim, a proved quantum/classical
separation or an executed quantum algorithm. Independent derivation and
source checks and actual-note core review accepted. Eight finite classical
controls are recorded separately from the written algorithm.

## 1. Question, Selection And Native Input

Given a prime p in binary, compute the canonical residue

    F(p) = ((p-1)/2)! mod p,        0 <= F(p) < p.

For p=2 interpret the factorial as 0!=1. No character oracle, class group,
unit, fundamental solution of Pell's equation or factorization of p-1 is
provided. The target is bounded-error time polynomial in log p and
log(1/eta), for error tolerance 0<eta<1/2. The exact output has O(log p)
bits. Direct verification by multiplying the specified integers costs
O(p) modular operations; no polynomial classical certificate for the
canonical sign is claimed. Wilson's square check is insufficient.

This is an explicit arithmetic-output question selected against the two
failed proposals in LEVI_TENSOR_AND_MQ_ADMISSION.md. The corpus query
`half factorial modulo prime fundamental unit class number Chowla quantum`
returned the existing unit/regulator and compact-residue notes, which are
reused. The baselines lookup identifies classical number-field relation
algorithms, which must replace brute multiplication in any comparison.

The mechanism is to compute class numbers and compact quadratic units,
then use Mordell's/Chowla's congruences. Its intended asymptotic comparison
is polynomial in log p against the applicable classical factorial and
class-group/unit algorithms, including subexponential relation methods.
Those upper bounds establish no lower bound for this particular output.
The purpose of this pass is to settle the paid composition, not to claim
that it supplies a new algorithmic mechanism.

## 2. Actual Primary Sources And Their Scope

- [Chowla, PNAS 47 (1961), 878](https://pmc.ncbi.nlm.nih.gov/articles/PMC221354/):
  the original one-page theorem and proof were visually inspected in the
  public [page scan](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/d6a8/221354/f21e82bd8b77/pnas00222-0138.png).
  For prime p=1 mod4, ordinary h=h(Q(sqrt p)) and its positive fundamental
  unit epsilon=(t+u sqrt p)/2>1,

      F(p) = (-1)^((h+1)/2) * t/2 mod p.                 (1)

  Here the maximal order is intended; h is odd and Norm(epsilon)=-1.
  No Ankeny--Artin--Chowla nonvanishing conjecture is used.
- [Cosgrave--Dilcher, INTEGERS 8 (2008), A39](https://ftp.gwdg.de/pub/misc/EMIS/journals/INTEGERS/papers/i39/i39.pdf),
  actual equation (8), records Mordell's theorem: for prime p=3 mod4,
  p>3, F(p)=(-1)^((h(-p)+1)/2). The exception p=3 is handled directly.
- [Biasse--Song, SODA 2016](https://fangsong.info/files/pubs/BS_SODA16.pdf),
  actual Theorem 1.1 gives compact S-unit generators in polynomial time;
  Theorem 1.2 gives class groups under GRH. Units alone use S empty;
  below one factor-base S-unit call supplies both outputs jointly.
  The detailed [2510.02280v2](https://arxiv.org/html/2510.02280v2),
  Section 8.1 Proposition 7, supplies exact compact representatives from
  approximate logs and phases; Section 8.2 Proposition 8 explicitly retains
  GRH. The full unit group includes real signs. We import these published
  primitives, not an abstract-only assertion or a new proof of their HSP.
- COMPACT_RESIDUE_CONDUCTOR_DECISION.md supplies the independently reviewed
  local evaluation of compact power products, including valuation
  cancellation and nonunit denominators. This interface is reused, not
  extended to arbitrary straight-line programs with addition.

## 3. Paid Algorithm

For p=2 or 3 return 1. For p=3 mod4, p>3, construct the explicit maximal
order of Q(sqrt(-p)), compute its ordinary class group with the published
quantum primitive, multiply its invariant factors to obtain h, and apply
Mordell's sign. Its discriminant is -p and all public input sizes are
polynomial in log p. Oddness is a useful necessary check, not a certificate
of the computed class number.

For p=1 mod4 construct

    O = Z[omega],  omega=(1+sqrt p)/2,
    omega^2 - omega + (1-p)/4 = 0,
    P = (sqrt p) = (2 omega-1),  Norm(P)=p.

This is the known maximal order and the unique prime above p; no unknown
integral basis or prime-ideal factorization is supplied as advice.

1. Construct the GRH class-group factor base and make ONE quantum
   S-unit call, as specified below. Obtain h from its valuation image.
2. Obtain a COMPLETE compact generating set for O* from the integer
   kernel of that same valuation matrix.
   Extract the primitive generator modulo torsion and normalize it to
   epsilon>1 in the embedding sqrt p>0, as proved in Section 4.
3. Evaluate epsilon modulo P by the existing compact-residue algorithm.
   O/P is explicitly Fp via omega -> 1/2, so the result is exactly t/2.
   The modulus has log norm log p. Individual compact factors need not
   be P-units: normalize their valuations before modular exponentiation.
   The total valuation is zero for the true unit. There is no expansion
   of the potentially enormous t or u.
4. Return (-1)^((h+1)/2) times that residue modulo p.

To make the joint success guarantee explicit, let b=ceil(log2 p), and
enumerate all prime ideals S of norm <=48b^2 in the relevant quadratic
maximal order. Under the cited GRH generator bound their classes generate
Cl(O). Enumeration is deterministic polynomial work in b: enumerate the
rational primes up to this bound and factor the public quadratic defining
polynomial modulo each (even exhaustive work in those small primes is
polynomial). Include precisely the resulting prime ideals within the norm
bound, with ramified and inert cases handled by their actual norms.

Run the published quantum S-unit algorithm ONCE. Append the known unit
-1 explicitly if the output lists generators modulo torsion; these
quadratic fields have no other required roots of unity (p=3 was handled
directly). Obtain a complete compact generating set beta_1,...,beta_k
for U_S. Compute its integral
valuation matrix V, with entry v_P(beta_j), by adding the small-factor
valuations times their binary exponents. All integers have polynomial
bit length. The image of V is exactly the relation lattice for the prime
ideal classes in S, so Smith/Hermite normal form gives Cl(O) and h.
Compute a full INTEGER kernel basis of V, not merely a rational nullspace.
For each kernel vector z, form the compact product product_j beta_j^z_j.
These generate O*: every ordinary unit has an expression in the complete
S-unit generators, and its valuation vector is zero. Kernel computation
and the resulting products have polynomial encoding size.

Thus the class number and complete ordinary unit set are correct on the
SAME success event of one imported primitive. The imaginary case only
needs the valuation image. This is the source's class-group reduction
with its elementary kernel retained, not an independent primitive.

These steps solve the stated function on that success event. Integral
bases, multiplication tables and P have
polynomial descriptions. Output h also has polynomial bit length. Exact
compact factors/exponents have polynomial total encoding length, so the
classical postprocessing is polynomial in log p. No external oracle,
coherent fundamental-unit advice or factorial subroutine is assumed.

## 4. Primitive Unit And Orientation Without Expanded Coefficients

An arbitrary non-torsion unit, or a generator of the totally positive
units, does not suffice. Here is explicit rank-one postprocessing when
the primitive returns a complete generating set beta_1,...,beta_k.
Write beta_i=s_i epsilon^(a_i), with s_i in {+1,-1}, only for analysis.
Completeness gives gcd_i(a_i)=1. We do not know these exponents initially.

Each supplied compact factor is gamma=a+b sqrt p with small exact rational
a,b. If each numerator/denominator has at most H bits, the conjugate
upper bound and the nonzero rational norm give the safe bound

    |log |gamma|| <= 6H + ceil(log2 p) + 4 = B_gamma.

Thus C=max(1,max_i sum_j |e_ij| B_gamma_ij) bounds every
|lambda_i|=|log |beta_i||. C is computed in binary and has polynomial bit
length, even if its numerical value is enormous. A positive quadratic
unit above 1 is at least the golden ratio, so nonzero |lambda_i| is at
least log((1+sqrt5)/2), and |a_i|<=3C. Put B=ceil(3C).

Compute these logs with absolute error below 1/[100(B+1)^3]. Small-factor
logarithms need only polynomially many precision bits, including the
bit lengths of the exponents; interval arithmetic pays their errors.
The fixed gap distinguishes zero logs from nonzero ones. Choose a
nonzero lambda_1. The ratios lambda_i/lambda_1=a_i/a_1 can be determined
to error below 1/(4B^2). Continued-fraction rational reconstruction with
denominator bound B recovers them exactly. Reduced numerator and
denominator are bounded by B.

Clear denominators using a POSITIVE common denominator and divide by the
positive common gcd. Since the first ratio is 1, c_1>0; the resulting
primitive integer vector is c_i=sign(a_1)*a_i, because the true exponents
have gcd 1. Extended Euclid finds integers z_i with
sum_i z_i c_i=1. Their bit lengths are polynomial. The compact product
gamma=product_i beta_i^(z_i) is therefore +/-epsilon or +/-epsilon^-1.

Its exponent is sign(a_1), so use the ALREADY determined sign of lambda_1
to choose gamma or gamma^-1. This avoids reusing old log error bounds
after a potentially large Bezout combination. Finally choose the real sign so the first embedding
is positive. Signs of each small factor a+b sqrt p are determined exactly
by rational comparisons/squaring; the sign of the compact product follows
from exponent parities, even for negative exponents. The result is the
unique epsilon>1. All operations preserve a polynomial-size compact
power product. No scan through Pell solutions or expanded unit is used.

## 5. Error, Verification And Falsifiers

The one S-unit call above supplies both the correct class number and the
complete compact unit group on its common bounded-error success event.
Use the published polynomial-time primitive with constant success at
least 2/3, including its state precision and finite execution budget.
The subsequent public factor-base and arithmetic steps are deterministic;
logarithmic interval precision is paid as in Section 4. Cap the size of
malformed outputs at the primitive's polynomial resource bound. Malformed
outputs or failed necessary checks can produce a failure symbol.
Independent full blocks followed by majority of their FINAL residues
give error <=eta with O(log(1/eta)) blocks;
a failure symbol counts as an incorrect result. This is bounded-error
computation, NOT exact-on-success. Necessary norm/integrality/Wilson
checks do not certify completeness of the quantum arithmetic output.

The written cost is polynomial(log p,log(1/eta)), conditional on GRH
for the class-group primitive. Unit computation alone does not remove
that hypothesis. No unreviewed exact gate exponent is claimed.

Decisive falsifiers include using Z[sqrt p] instead of O, returning an
unoriented generator, replacing a complete generator set by an arbitrary
unit, inverting nonunit compact factors directly modulo P, dropping GRH,
or treating a square-root check as a canonical-sign certificate.

At p=5 the required epsilon=(1+sqrt5)/2 gives F=2. Its inverse or negative
instead predicts 3; BOTH answers square to -1 modulo5. Its square predicts
1 and fails even that weak check. At p=3 the unexceptional Mordell formula
would incorrectly return 2 instead of 1.

## 6. Matched Classical Baselines And Source-Circularity Check

The strongest relevant competitor is the SAME congruence composition
using classical class-group/unit algorithms, including subexponential
relation algorithms with their actual conditional/heuristic scope.
In particular, the later actual-source audit in
UNCONDITIONAL_CLASS_GENERATOR_ADMISSION.md Section4 records a rigorous
fixed-degree L_Delta(1/2) classical bound under ERH from
deBoer--PelletMary--Wesolowski Theorem1.3, without additional smoothness
heuristics. This strengthens the comparator, not a polylog solution.
[PARI's own documentation](https://pari.math.u-bordeaux.fr/dochtml/html/Quadratic_number_fields_and_binary_quadratic_forms.html)
describes its quadratic class-group algorithm as subexponential and marks
its default results GRH-conditional. Practical sieving methods and direct
factorial algorithms must also be included. We do not infer a sharp best
exponent or a half-factorial lower bound from these sources. In particular,
the direct O(p) product is not the strongest asymptotic comparator.

The actual text of [Williams 1981](https://msp.org/pjm/1981/92-1/pjm-v92-n1-p22-s.pdf)
Theorem 1 was checked as a potential class-number-mod4 shortcut. Its
equation (8) orients b in p=a^2+b^2 using the unknown half-factorial
itself. Supplying that signed b would be circular here. Its p=1 mod8
negative result concerns a specified linear congruence form, not all
algorithms. [Williams 1979](https://msp.org/pjm/1979/83-2/pjm-v83-n2-p26-p.pdf)
relates h(-p) mod4 to a real class number and unit; that relation alone
does not remove the class-number computation either. No general
classical exclusion follows from either failed shortcut.

## 7. Completed Control And Decision

`classical_baselines/half_factorial_arithmetic_control.py/.json` uses one
Sage/PARI worker, certified BNF data and maximal-order units on exactly
p=3,5,7,13,17,23,41,229. All eight formulas match direct factorials;
outputs are respectively 1,2,6,5,13,1,9,122. Both h mod4 classes occur,
including h(229)=3. Wrong unit normalizations and the p=3 exception are
explicitly retained. Parent inspected the script and exact artifact.
This is classical arithmetic only, not a compact quantum implementation
or asymptotic evidence. No larger sweep or compiler is queued.

The paid half-factorial composition is accounted for at the written level.
Its scientific limitation is clear: the mechanism is existing quantum
number-field arithmetic. A further pass must compare independent
high-upside questions before extending it. A concrete possible next
question is whether a canonical fractional-factorial ambiguity beyond
this quadratic case reduces to polynomial-size arithmetic, or whether
the exact source forces degree/output cost proportional to p. That
question requires corpus/literature and classical checks first; it is
not an admitted extension or a reason to build a generic arithmetic layer.
