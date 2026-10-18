# Mixed Quadratic OPI: Perfect Classical Norm Witnesses And A Source Bound

2026-10-17. Standard polynomial-factorization/norm machinery; local
application REVIEW PENDING. No novelty, all-input dequantization or new
quantum algorithm is claimed.

FIXED-INPUT FOLLOW-UP: the [Morse progression solver](PRIME_CHARACTER_MORSE_ATTACK.md)
now provides a separate fixed-input guarantee under explicit degree-slack
and sufficiently-large-field conditions. It checks the geometry and field
bound, not an IID-input assumption. This does not certify the original61-bit
large examples or prove a general theorem for the smaller pencil below.

## Research Decision

The [previous prime-field experiment](PRIME_CHARACTER_OPI.md) solved common
cosets classically but left mixed high-rate controls at124/127 and122/127.
The new attack solves BOTH saved N127,K77 mixed inputs perfectly, including
strict nonzero variants, without changing their public shifts/orientations.
It does not apply to the saved K39 inputs under its degree budget.

There is also a useful mathematical result independent of those examples:
one trial has inverse-polynomial perfect-solution probability over an IID
uniform-shift population with suitable fixed orientations. That is a
population theorem, NOT a success bound for each fixed input or PRNG seed.

The quantum OPI guarantees and oracle separation in
[Sun-Wootters](https://arxiv.org/html/2610.12357) are not refuted. Our predicates
are explicit translated power cosets, not random hidden membership tables.
This classical attack narrows which structured instantiations could support
a separation. A fixed-rate low-rate advantage remains unsettled.

## Problem And Exact Degree Budget

Input is the SAME public prime-field OPI specification: p odd prime, N<p,
evaluation points1,...,N, dimension K, public shifts t_i, orientations0/1,
and a verified nonsquare nu. Maximize acceptance of

    Q(a_i)-t_i in (Fp)^2             for i in A,
    Q(a_i)-t_i in nu*(Fp)^2          for i in B,
    deg Q<K.

The zero-inclusion convention is explicit. Strict mode requires every tested
root nonzero. No secret shift, field table, random oracle or acceptance-list
materialization is supplied. Modular exponentiation implements membership.
The reference inherits N<=4096 from the existing source. The arbitrary127-bit
prime cap was removed to execute the explicit Morse field regime; prime
validation remains. Exact large population counts use FLINT decimal rendering
instead of Python's limited decimal-int conversion. Operational limits are
not evidence of hardness or assumptions of the algebraic/population proof.

Interpolate T_A(a_i)=t_i on A and V_A=product_(i in A)(X-a_i). Choose public
lambda and nonzero rho, and set Q0=T_A+lambda*V_A. On B interpolate
F0(a_i)=t_i-Q0(a_i). If |B| is odd, include point0 with an independently
chosen auxiliary value, padding the interpolation to even size

    D=|B|+(|B| mod2).

Let V_B vanish on these B/auxiliary points and put F=F0+rho^2*V_B. Seek

    F=R^2-nu*Z^2,                  Q=Q0+R^2.

Then Q-t_i=R(a_i)^2 on A and Q-t_i=nu*Z(a_i)^2 on B. Both groups are
accepted if zero is included. The exact sufficient degree condition is

    K>max(|A|,D).

The norm factors have degree<=D/2, so this budget is verified BEFORE search.
The auxiliary point is part of a public algebraic construction, not a new
oracle problem or a replacement of any native constraint.

## Classical Norm Construction

In the CONSTANT quadratic extension F_(p^2)=Fp[u]/(u^2-nu), an irreducible
over Fp splits into a conjugate pair exactly when its degree is even.
Odd-degree irreducibles stay inert. Thus a monic polynomial is a norm
exactly when every odd-degree irreducible has even multiplicity.

Factor F/rho^2 over Fp. Reject THIS target when an inert multiplicity is odd.
Otherwise factor over F_(p^2), choose one canonical member of each conjugate
pair, and half of each inert even multiplicity. Their product H satisfies
H*bar(H)=F/rho^2. Writing rho*H=R+uZ gives the required base-field norm.
Both extension and base-field polynomial identities are checked exactly.

These splitting/norm facts are standard, not a new algorithm claim; see
[Kuo-Liu-Totani](https://doi.org/10.1016/j.ffa.2026.102812). The implementation
uses [FLINT finite-field polynomial algorithms](https://flintlib.org/doc/fq_default_poly.html),
not a home-grown factorization or a claimed quantum subroutine.

Finite-field factorization is randomized expected polynomial time in degree
and log p. Each trial also pays polynomial interpolation, exact products,
Frobenius conjugations and independent native Horner/membership verification.
The records charge base/extension factorizations and keep EVERY rejected
target. Those counters are not a complete bit/gate budget or a quantum
performance comparison. A bounded-search failure is UNKNOWN, not hardness.

## Strict Roots Without A Field-Size Search

If F vanishes at any native point, nonsquareness forces R=Z=0 there. Reject
that strict norm TARGET, not the original OPI problem. Otherwise multiply
R+uZ by the norm-one Cayley element

    alpha_s=(1+s*u)/(1-s*u)=a_s+b_s*u,
    a_s=(1+nu*s^2)/(1-nu*s^2), b_s=2s/(1-nu*s^2).

The denominator never vanishes in Fp. Rotate

    R'=a_s*R+nu*b_s*Z,       Z'=b_s*R+a_s*Z.

The norm and degree budget stay unchanged. Each forbidden R'(a_i)=0 on A
or Z'(a_i)=0 on B has a NONZERO quadratic numerator in s, since the original
pair is nonzero. At most2N parameters are forbidden. For p>2N, one of
0,...,2N works. This is a deterministic polynomial-size candidate set, not
a full-field scan when p is large. Every actual rotation is stored and checked.

## Try To Disprove The Pencil, Then Repair It

The first implementation fixed rho=1. That restriction has an explicit
ALL-PARAMETER failure, even on a strictly easy input:

    p23,N8,K5,nu5,
    A={1,2,3,4}, B={5,6,7,8},
    t_A=(0,0,0,0), t_B=(19,22,8,6).

The constant Q=13 is a perfect STRICT solution. But D0=V_A-V_B has three
distinct linear roots0,9,16 and coefficients(0,4,14,16). Every monic-pencil
target is

    F_lambda=D0*(X/16-lambda).

The moving linear factor can make at most one fixed root's multiplicity
even. At least two inert multiplicities stay odd. Thus NONE of the23
parameters is a norm, although OPI itself is easy. The proof is algebraic;
the full23-case replay is an independent calibration, not the sole evidence.

The revised attack varies rho^2 as well. This removes that fixed divisor;
the counterexample now gets a perfect strict witness in5 paid trials.
For even |B|, gcd(V_A mod V_B,V_B)=1, and p>=5 supplies two different nonzero
square leading coefficients, so the expanded family has no fixed irreducible
divisor. Absence of a fixed divisor does NOT prove irreducibility, adequate
norm frequency or an inverse-polynomial success rate on every fixed input.
Odd-|B| auxiliary values introduce additional explicitly charged parameters.

## A Rigorous One-Trial Average-Case Statement

Assume truly IID uniform shifts, fixed orientations satisfying the degree
budget, and trial/auxiliary parameters independent of those shifts. Condition
on ALL A shifts and lambda,rho. The B values t_i-Q0(a_i) remain independent
uniform. If padding is needed, its independent uniform auxiliary value supplies
the remaining coordinate. Interpolation is a linear bijection, so F/rho^2
is a uniform monic degree-D polynomial.

Every irreducible degree-D polynomial works: D is even, so it splits in the
quadratic extension. It has no Fp root, also licensing strict Cayley avoidance
when p>2N. Therefore first-trial success is at least

    I_p(D)/p^D,       I_p(D)=(1/D)*sum_(d|D) mobius(d)*p^(D/d).

The producer records this EXACT rational population lower bound. For the
two saved orientation patterns D=58 and64, it is approximately1/58 and1/64.
These numbers are NOT probabilities certified for those particular saved
shifts. Seeded replays are not IID-source certificates. `attack(...,seed=None)`
uses system randomness under the usual uniform-bit assumption; producers
use explicit fixed seeds for deterministic replay.

For p>2N the elementary irreducible-count bound gives at least1/(2N).
With independent fair orientations and fixed rate K/N>1/2, the degree budget
holds with probability approaching1 exponentially fast; e.g. it suffices
that both groups have size<=K-2, an ordinary binomial-tail condition.
Thus the structured IID-shift high-rate population does NOT have negligible
classical perfect-solution success. This is NOT a high-probability or worst-
case classical solver, nor a dequantization of general OPI/oracle inputs.

Do not amplify this into a per-instance guarantee. Even independent trial
coins do not let one replace q(input) by its population mean in
E_input[(1-q(input))^T]. The fixed-monic counterexample illustrates the danger.
An argument about correlations or fixed-instance norm frequency is still
needed. Expected polynomial factorization work can be truncated at a
polynomially larger budget while preserving inverse-polynomial population
success; the prototype counters themselves are not a certified bit bound.
Subtracting a random degree<K polynomial from all shifts is NOT a free
worst-case-to-IID reduction: it preserves the N-K RS syndrome coordinates
and moves only within a K-dimensional orbit, not all Fp^N shift vectors.

## Executed Evidence And Decision

The unchanged N127,K77 seeds29/71 now have perfect127/127 classical witnesses
in1 and15 paid expanded-pencil trials. Both zero-including and strict versions
are retained. Their degrees69 and64 respect the predeclared K77 bound. The
same-input test checks specifications against the ORIGINAL source artifact.
Saved K39 siblings are NOT APPLICABLE, not declared hard or unsatisfiable.

Tests independently verify polynomial products/native Horner witnesses without
new factorization, exhaustively compare norm representability through degree4
over F3, check the all-parameter counterexample, and enumerate the121 B-shift
sources over F11 in the degree2 strict calibration. Exactly55 irreducible
targets yield perfect strict witnesses, matching I_11(2)/11^2=55/121.

Next high-value mathematics: establish or falsify useful fixed-input norm
frequency for the expanded family, with its exceptional pencils and actual
field-size requirements, OR find a genuinely lower-rate mechanism. Do not
replace that problem with more seeds, trial budgets or a claim that random-
polynomial statistics already prove a fixed-pencil theorem. No new central
candidate/negative/proof is promoted. Application remains REVIEW PENDING.

```text
python theorems/prime_character_norm_attack.py --write
python -m pytest -q tests/test_prime_character_norm_attack.py
```
