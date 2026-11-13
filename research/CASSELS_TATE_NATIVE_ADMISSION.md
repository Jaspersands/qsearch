# Native Cassels--Tate pairing: admission and first falsifier

2026-11-14. Native polynomial pairing endpoint NOT ADMITTED; screened and
parked pending a concrete new cochain/readout construction. This is not a
general impossibility result. Two exact native goodness shortcuts are refuted.
The retained native two-Selmer endpoint is not reopened merely for another
approval. Its targeted selection review found no new concrete defect.

## Problem, mechanism, resources and selection

Input monic squarefree f in Z[x], odd degree n=2g+1, binary coefficient
length B. Compute a basis of Sel2(J/Q) in compact branch-algebra coordinates
AND its exact Cassels--Tate pairing matrix. No Mordell--Weil basis, splitting
field, conic points, cochain, class group or units are supplied. The output
can sharpen a rank bound; it does not determine the Mordell--Weil rank.

Candidate mechanism: reuse GENERAL_NATIVE_SELMER_COMPOSITION.md and its
tracked local Kummer preimages; compute Shukla's global cochain in root/pair
etale algebras; evaluate the resulting local Hilbert symbols. Target quantum
cost poly(n,B,log(1/eta)) under the same explicitly charged GRH arithmetic.
This would be a useful additional native output. No novelty, hardness,
separation, practicality or execution is asserted. The strongest classical
comparison is the SAME pairing/descent with classical factoring, class/unit
and conic arithmetic, including the stronger factoring-only quartic and
supplied-tower reductions already retained in this repository.

Selection compared the strongest existing native surface/Selmer endpoints
against the recent physical/arithmetic source screens. The surface classical
transfer and Selmer comparator corrections do not create a new quantum
mechanism. The pairing has an additional motivated output and a specific
unpaid operation. Corpus been-tried THEN baselines were queried; the fuzzy
results did not find an exact prior direction and are not exhaustive evidence.
Actual primary source: Himanshu Shukla, thesis2024,
https://epub.uni-bayreuth.de/8348/1/thesis.pdf . PDF/text/provenance and corpus
snapshots are in audits/sources/cassels_tate_selection/.

## Source obligation that blocks the naive composition

The actual Algorithm1, printed pp106--107 (textLF5331--5386), adjoins all
root-coordinate square roots and solves cocycle/Hilbert90 problems in the
resulting field. Sections4.3.1--4.3.4 give exact cohomological formulas, not
a polynomial-in-genus representation theorem. A normal root field can have
factorial degree; even independent square roots can have exponential degree.
Its generic expanded crossed product is therefore not a paid native input.

CSA_MINIMAL_MODULE.md is polynomial in EXPANDED field/algebra dimensions.
Index1 or trivial Brauer class does not supply a small presentation of the
required compatible trivializing cochain. Merely invoking that algorithm
does not remove the expansion. This is an interface objection, not a lower
bound on every compressed construction or every pairing algorithm.

Section4.4/Algorithm2 use pair-root conics in polynomial-degree fields,
but require Assumption4.4.3. The obligation is both global compression and
compatibility with the local descent in Proposition4.3.15/Eq4.3.7, including
finite precision, bad-prime support, compact coefficient evaluation and
local half/torsion selection without exponential enumeration. A root/pair
formula must pay all of these before an end-to-end endpoint is admitted.

Cheapest falsifiers: a stronger matched classical construction; exponential
field or tensor input hidden inside a solver; unproved automatic conic
solubility; enumeration of all Selmer classes to find good generators; or
an uncharged local Hilbert90/readout field. No quantum implementation is
warranted before these gates close.

## Exact obstruction: a rational divisor need not be good

For every integer k>=1 let

    b+c*sqrt(5)=(2+sqrt(5))*(9+4*sqrt(5))^k.

Then b,c are positive integers, b>2, and b^2-5c^2=-1. Define the smooth
genus3 curve and rational Mumford pair

    f=x*(x^2-1)*(x^2-4)*(x^2-b^2),
    u=x^2+1,                  v=5c*(1-x).

Its seven roots are distinct. Modulo u, f=-10*(1+b^2)*x=-50c^2*x=v^2.
Also deg(v)<deg(u)=2<=g and gcd(u,f)=1. Thus (u,v) defines an ACTUAL
rational Jacobian divisor class, so its Kummer image belongs to Sel2,
without computing a Selmer group or assuming any local condition.

In the completely split branch algebra the Kummer coordinates are
d_theta=u(theta)=theta^2+1: these are the norms of x-theta on the divisor.
For the pair theta=0, theta'=2 the Algorithm2 conic requires

    U^2-5V^2=2.

It has no Q2-point. Q2(sqrt(5))/Q2 is the unramified quadratic extension
(the minimal polynomial of (1+sqrt(5))/2 reduces to X^2+X+1), so nonzero
norms have EVEN 2-adic valuation, whereas v2(2)=1. A homogeneous point at
infinity would require sqrt(5) in Q2 and is also impossible. Multiplying
individual d_theta by rational squares merely rescales U,V, so this is a
squareclass obstruction, not an unfortunate representative or sign choice.

Therefore even native classes known to come from J(Q) can fail the source's
good-element assumption. This is NOT a failure of the source: that assumption
is explicit. It refutes deleting the assumption from a naive composition.
It does not prove no good generating basis, bad quotient coverage, hardness,
failure of a general pairing algorithm, or a nonzero pairing for this class.
Indeed a rational-point class pairs trivially; identifying that fact from
arbitrary Selmer coordinates is not supplied by the proposed native input.

Exact Sage/PARI control, run once and exited0, uses k=1,b=38,c=17:
f=x^7-1449x^5+7224x^3-5776x, u=x^2+1, v=85-85x;
the exact remainder is0 and Hilbert(5,2)_2=-1. Result:
audits/controls/cassels_tate_good_obstruction/result.json. The infinite-family
proof above is algebraic; the finite control only checks conventions.
The final135-line independent review was parent-read against the actual
source and both exact control outputs. It additionally verifies nonzero
MW/2 class, correct Kummer signs and the distinction from Definition4.4.5:
that definition already adds the entire MW image to the good-element span.

## Goodness is not a linear filter, even on the actual Selmer group

Take f=x(x^2-1)(x^2-4), genus2, and T_a=[(a,0)-infinity]. For a rational
branch root a its Kummer tuple is d_a(theta)=a-theta off a, and f'(a) at a.
Every T_a is good: when neither root equals a, U=V=1 solves the required
conic. For a pair containing a, use (0,1) or (1,0). On
A U^2-B V^2=-B, the rational parametrization

    U=2Bt/(A-Bt^2),       V=(A+Bt^2)/(A-Bt^2)

gives permitted nonzero coordinates by avoiding finitely many t. There
is no Galois compatibility issue in this split native example.

In root order(-2,-1,0,1,2),

    delta(T0)=(2,1,4,-1,-2),     delta(T2)=(4,3,2,1,24),
    delta(T0+T2)=(8,3,8,-1,-48).

The sum's root pair(-1,1) requires 3U^2+V^2=2. Its homogenization has
no Q3-point: in primitive integral coordinates mod3 forces V,W divisible
by3, and the equation then forces U divisible by3. Exact PARI reports
(-3,2)_3=-1 in nonlinear.json, run once/exit0. Thus two good actual
MW/Selmer classes have a nongood sum. A good spanning set is NOT excluded;
these two summands already span the bad element.

For expanded split-root coordinates one can see the precise classical
structure. Put c=theta_j-theta_i and write the Hilbert sign as a bit:

    q_ij,v(d)=[(d_i*d_j,c*d_i)_v].

The conic is soluble exactly when all its local q bits vanish. Hilbert
bilinearity gives

    q(dd')=q(d)+q(d')+[(d_j,d'_i)_v]+[(d'_j,d_i)_v].

Hence these conditions are quadratic in Selmer-basis exponents. The
genus2 example proves their polarization need not vanish even on Selmer.
This rejects a universal linear-kernel shortcut; it does NOT establish
generic quadratic-system hardness for the native structured equations.
Polynomial cost for compact input still needs the coefficient/support
evaluation obligations below; no expansion is declared free.

## Focused paid obligation and next experiment

One Claude Opus/high request completed, terminal/reaped0 session56155,
max48000tokens, local estimated ceiling2USD (not a provider cap/charge). Exact selected
source/interface packet: audits/api_inputs/2026-11-14-cassels-tate-descent/;
run bundle: audits/claude_runs/2026-11-14-cassels-tate-descent/.
It asked ONLY whether the global cochain has a compatible polynomial root/pair
algebra representation, without assuming good elements. No OpenAI call,
credentials attachment, automatic retry or inferred account balance.

Its153-line nonempty report was fully read. Reported31567input/37558output
tokens, estimate0.877428USD, not invoice or balance. No retry/OpenAI call.

Material dispositions:

1. ACCEPTED: the source's generic full-field/cochain tables and Hilbert90
   sums do not supply a polynomial native representation. Cochain existence,
   global index=period, or an expanded-input CSA solver alone cannot pay it.
   Field-size examples are costs of those representations, not lower bounds
   for every algorithm. A scalar list of d_i alone need not generate all
   roots; the full generic source construction explicitly includes root data.
2. ACCEPTED algebraically: the ordered-pair conic has quaternion class
   (d_i*d_j,c*d_i); its polynomial-degree pair algebra does not require
   a normal root field. The report's quadratic-goodness expression agrees
   with the identity above; exact native nonlinearity is now established.
3. OPEN, not imported: the proposed corestriction reformulation P1 was
   explicitly unchecked in the report. Identifying restricted cyclic
   classes does not by itself establish descent with the required permutation
   equivariance and Eq4.3.7 readout. The report's headline describing the
   exact missing map overstates this conditional reformulation. Its
   triple-orbit/graph repair has no proved constructive cochain map.
4. REJECTED literal resource wording: a nonsplit quaternion has a minimal
   left ideal of dimension4 over its centre (rank1 over itself), not a
   two-dimensional module over the quaternion division algebra. Componentwise
   index/minimal-module output still does not trivialize the desired global
   cocycle. No tensor-rank lower bound is inferred from non-product data.
5. RETAINED unpaid gates: replacing compact Selmer coordinates by suitably
   small expanded conic coefficients, evaluating resulting compact witnesses
   at finite precision, and constructing a polynomial local descent model.
   The report's Minkowski/LLL suggestion is a proposal, not an algorithm proof.
   Its generic unramified lcm warning does not prove the required bad-prime
   set forces that cost; good-reduction zero contributions must be discarded.
6. No good-basis search clock is supplied. The actual Definition4.4.5 permits
   adding MW classes, but native MW generators are not input. Neither the
   source's finite empirical coverage nor our counterexamples settle global
   span coverage. No quantum advantage or all-pair complexity follows.

The current evidence does not warrant another conic wrapper, conditional
subsystem or sweep. A new continuation must give a SPECIFIC polynomial
cochain/descent representation with compatible scalar readout, or a new
independent constructive route selected by external value. No further paid
request on this line is queued merely to repeat the obstruction.

## Local review: remove the false loop barrier, retain the real interface

The final144-line independent local review was parent-read against Shukla
Proposition4.3.15 and actual Stoll Proposition5.1/proof:
audits/reviews/2026-11-14-cassels-tate-local-readout.md. The existing native
Kummer compiler supplies actual local points Q with the requested label d.
Compute r in the root algebra with r^2=mu(Q)/d. The same labelled roots
s_i=r(theta_i)*sqrt(d_i) in Stoll's halving parametrization select P with
2P=Q and sigma(P)-P=alpha(sigma), by its Weil-pairing torsor equivariance.
The printed enumeration of J[2] is therefore not an intrinsic obstruction.
This is an algebraic radical/determinant description; no finite-bit compiler
over a possibly exponential common radical field is asserted.

Even granting polynomial evaluation of the FULL local cocycle gamma, the
source still asks for the quadratic norm obstruction of the semilinear line

    h(omega)=Gamma(h)*omega,   Gamma(h)=gamma(h,-1),
    delta=gamma(g,-1)/(g(omega)*omega) in E*,
    output (delta,d'_theta)_E,  E'=E(sqrt(d'_theta)).

Changing omega by c in E'* changes delta by an E'/E norm; only that class
is required. With an expanded polynomial-degree descent field and action
matrices this is linear algebra, not a group-enumeration problem. Cochain
evaluation alone supplies neither this model nor a precision/pivot bound.
A compressed norm-class algorithm or a polynomial explicit quaternion
description would suffice; none is constructed here. No general lower bound
from a field-size bound is claimed, and good-prime zero terms must be omitted.

Once delta and its certified local digits are given, the actual root-orbit
Hilbert readout is polynomial: total orbit degree is n, and only a quadratic
extension is needed for the norm-image squareclass test. At2, unit depth
2e+1 suffices; odd primes use valuation parity/residue squareclass. This
does not charge the missing descent output or its global bad-prime support.
The native whole endpoint stays PARKED, with no subsequent subsystem queued.
