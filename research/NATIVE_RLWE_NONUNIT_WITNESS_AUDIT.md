# Native Ring-LWE: Nonunit Syndromes Spend The Decoder Margin

Date: 2026-10-04. LOCAL DERIVATION / REVIEW PENDING.

Follow-up to NATIVE_RLWE_ROTATIONAL_WITNESS_REDUCTION and the sparse audit.
No independent verification, novelty, quantum algorithm, security estimate
or all-decoder lower bound. This excludes an OUTPUT CERTIFICATE CLASS on
the specified native label law. It does not prove general lattice hardness.

## 1. Decision And Scope

The rational decoder accepts nonunit syndrome polynomials in principle.
They escape the sparse audit's uniform-unit density argument. However,
in the high-residue-degree native family they consume too much scalar
spacing to help this particular worst-case-noise decoder on typical inputs.
The exclusion below covers ALL adaptively selected nonunit h, not merely
a fixed catalogue. No independence of the generator's choices is assumed.

Retain q prime, d a power of two, q=3 mod 8, residue degree f=d/2 and two
degree-f CRT factors. Let a_1 be uniform conditioned to be a unit, a_2
independently uniform in the whole ring. Retain actual original F,b.
Let R_s>=1 and E_max>=1 be the stated ORIGINAL secret-box and total-
noise-norm contracts, and write P=R_s*E_max.

The output class consists of integer c,h,t with h!=0 over Q, h NONUNIT
mod q, F*c=t*h mod q, and the rotational certificate

    U=R_s*||h||_1, 2*U<q,
    min_(1<=Delta<=2*U) ||Delta*t||_q>2*E_max*||c||.        (1)

Using a certified R>=||c|| only makes this condition stricter. This is
the conservative deterministic box/norm decoder, NOT every decoder using
Gaussian moments, many samples, tailored noise directions or another prior.

## 2. Nonunit Norm Lower Bound In The ORIGINAL Metric

For nonzero integer h of degree <d, C_h is invertible over Q because
X^d+1 is irreducible there. If h is nonunit modulo q, it vanishes in
at least one degree-f CRT field component. Thus C_h mod q has nullity
at least f. Integer Smith normal form gives

    q^f divides det(C_h), |det(C_h)|>=q^f.

Every column of C_h is a signed monomial rotation of h, hence has norm
||h||_2. Hadamard then gives

    q^f<=|det(C_h)|<=||h||_2^d,
    ||h||_1>=||h||_2>=q^(f/d)=sqrt(q).                    (2)

More generally the last exponent is f/d. The sqrt(q) statement is FALSE
for low-residue-degree families. No extension-field canonical metric or
independent-coefficient approximation is used.

The optimal-spacing packing result in the rotational note bounds (1)'s
left side by q/(2*R_s*||h||_1+1). Therefore every valid certificate needs

    ||c||<q/[4*P*||h||_1]<=sqrt(q)/(4*P).                 (3)

Every nonzero block of c is consequently a UNIT modulo q: a nonunit
block would also have norm >=sqrt(q) by (2). Moreover c_1 cannot be zero.
Otherwise a_1^*c_0 is either zero or a unit, never the nonzero nonunit
t*h required by (1). The prior inequality rules out h=0 mod q, and the
spacing inequality rules out t=0. Thus c_1 is a nonzero unit.

For EVERY fixed such c, multiplication of the uniform a_2 by c_1^*
makes F*c UNIFORM in all q^d syndromes, even conditioned on a_1 being a
unit. Hence for every fixed h its nonzero scalar line has probability
(q-1)/q^d. No second-label unit event needs to be discarded in this proof.

## 3. Fixed Nonunit h Is Already Unlikely To Work

For a fixed h independent of labels, (3) and the preceding uniformity give

    Pr[exists a valid certificate for this h]
      <=(q-1)*N_(2*d)(sqrt(q)/(4*P))/q^d.                 (4)

For a purely integer upper bound let

    L=floor(sqrt((q-1)/(16*P^2))).

Strict inequality (3) implies every coefficient is in [-L,L]. Thus

    Pr[exists a valid certificate for fixed h]
      <=(q-1)*(2*L+1)^(2*d)/q^d.                         (5)

A polynomial-size fixed catalogue is handled by multiplying its size.
Adaptive choice among a catalogue does not need query independence. The
stronger next section also permits arbitrary adaptive h outside a catalogue.

## 4. Packing Covers ALL Adaptive Nonunit h

Each of the two CRT prime ideals I_i is an integer lattice. Distinct
points in I_i differ by a nonzero nonunit polynomial, so (2) gives
minimum Euclidean distance at least sqrt(q). Disjoint radius-sqrt(q)/2
balls centered on ideal points in a radius-H ball imply

    #{h in I_i: ||h||_2<=H}<=(1+2*H/sqrt(q))^d.           (6)

All nonunits belong to I_1 union I_2, giving a factor two. This is a
packing bound in coefficient space, not a Gaussian-heuristic estimate.

Partition possible h by dyadic norm bins, w=2^ell for ell>=0:

    w*sqrt(q)<=||h||_2<2*w*sqrt(q).

Equation (3), using ||h||_1>=||h||_2, forces

    ||c||<r_w=sqrt(q)/(4*P*w).

If r_w<1 there is no nonzero integer c; discard that bin. Otherwise
the coordinate cube bound gives N_(2*d)(r_w)<=(2*r_w+1)^(2*d)
<= (3*r_w)^(2*d). From (6), the number of h in the bin is at most
2*(1+4*w)^d. All candidates in these sets are fixed BEFORE sampling
the labels; actual generators may choose any of them afterward.

Union over c,h and all nonzero t, using the uniform-syndrome argument,
bounds the bin's existence probability by

    2*(q-1)*[9*(1+4*w)/(16*P^2*w^2)]^d
      <=2*(q-1)*[45/(16*P^2*w)]^d.                       (7)

Summing the geometric series over w=2^ell, including extra empty bins
only to loosen the bound, gives

    Pr[ANY valid nonunit-h certificate exists]
      <=B_nonunit=2*(q-1)*[45/(16*P^2)]^d/(1-2^(-d)).     (8)

Cap at one. This union includes arbitrarily adaptive/correlated choices
of h,c,t based on F,b, not just classical choices or polynomial-query
generators. Its conclusion is existence on random input, NOT a quantum
query lower bound. Conditioning on observed successful inputs does not
erase their small unconditional mass.

For q polynomial in d and P>=2, the conservative bound is exponentially
small asymptotically. P=1 can be vacuous; do not silently promote it.
At actual reference rows P is much larger. The source/first-label unit,
prior, rounding and verification ledgers still require independent review.

## 5. Exact Reference Checks, Not Floating Security Estimates

The probe verifies (5) and (8) <=1e-8 at all six saved d^12 reference
lanes by EXACT integers. For (8), the test is

    10^8*2*(q-1)*45^d*2^d
      <=16^d*P^(2*d)*(2^d-1).                            (9)

The following log10 values are only numerical summaries of (8):

| d | spherical | hidden-elliptical |
| ---: | ---: | ---: |
| 64 | -704.6160 | -711.1389 |
| 256 | -3632.9841 | -3631.2843 |
| 1024 | -17518.6295 | -17287.8588 |

No tiny floating value is used to authorize a proof/algorithm claim.
The claimed finite arithmetic comparison is (9), with the local
derivation and actual source distribution still REVIEW PENDING.

These bounds do not contradict the nonunit/no-noise rational-decoder
controls. Those use E_max=0 and deliberately easy labels, outside (8)'s
noise and distribution premises. Nor do they contradict useful UNIT h
such as 2+X at the large references. That is the surviving output class.

## 6. Deliberate Falsifiers And Verification

Run the reproducible standalone probe:

    python research/certificates/native_rlwe_nonunit_witness_probe.py

- 3,912 exact nonzero polynomial Hadamard controls at d=2,4 over bounded
  coefficient boxes, with exact finite-field ranks and determinants.
  All 216 nonunit cases in admitted residue-degree families satisfied
  q^f determinant divisibility and ||h||_2^2>=q.
- Eighteen exact d=2 CRT-ideal packing controls checked point counts and
  EVERY pairwise distance, not an inferred typical shortest-vector length.
- Kept a LOW-DEGREE counterexample: d=8,q=17 and
  h=(0,0,0,1,0,1,1,1) is nonunit with ||h||_2=2<sqrt(17).
  The falsely extended sqrt(q) claim fails. A d=4,q=17 family was also
  explicitly excluded by its residue degree.
- Kept the zero-polynomial exclusion, necessary for invertibility over Q.
- Six exact fixed-h cube and six all-adaptive integer inequalities passed
  on the saved reference rows. Prime/source prerequisites are the separate
  previously saved contracts, not established by these comparisons alone.

No production CLI, live registry promotion, full suite or commit. No
efficient generator or quantum speedup has been discovered.

## 7. Research Decision And Gemini Contract

Deprioritize attempts to rescue THIS norm/box witness decoder by selecting
a nonunit CRT polynomial, whether fixed or adaptively selected. A lower-
residue-degree source or a different noise/prior decoder needs a NEW
analysis and strong classical projection attacks; it is not an exception
silently permitted by the present source contract.

The main unresolved target is dense UNIT-syndrome short relation/preimage
generation in the original metric, or a strong original-data classical
falsifier. Changed/reduced bases remain allowed. Moment-based Gaussian
decoders remain alternative targets and are not covered by (8).

Gemini: add the exact integer checker and scoped output-class exclusion,
with high-degree CRT, norm/box and input-label premises explicit. Keep the
low-degree, zero-noise/easy-input and zero-polynomial scope controls. Do
not label every nonunit decoder impossible or independent proof status
resolved. Do not discard original-data primal/LLL/BKZ baselines.
