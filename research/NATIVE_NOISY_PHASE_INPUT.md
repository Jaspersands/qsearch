# Copy-Only Approximate Native Input From Noisy Linear Values

Status: LOCAL DERIVATION / EXTERNAL REVIEW PENDING. The implementation supplies
known qutrit gate recipes and exact error ledgers, not hardware execution,
an efficient receiver, a novelty claim, or an admitted speedup.

## Source And Secret-Blind Preparation

Take2M independent records b=<a,s>+E modulo q=3^r with a uniform in Z_q^n,
the same unknown INTEGER-VECTOR secret, and IID symmetric integer errors.
A true public second-moment bound V>=E[E^2] is an input promise, not an
estimate obtained from a few values. For each DISJOINT original pair b,d:

    initialize |0>; apply F3; apply diag(1,omega^b,omega^d).

The known values determine every local gate, without knowledge of s or E.
The receiver gets ONLY the qutrit and public frequencies a,c (or their native
ring-label encoding). Values, preparation inverses and mask are retained
reduction-side. Recipe generation is deterministic given records and mask.
A uniform reduction-side t adds <a,t> to every value, so a fixed s becomes
uniform s+t; unmask the eventual answer. A supplied mask's uniformity cannot
be certified by inspecting its realized value.

No classical simulation of an unknown input is assumed. The preparation
description is known to the reduction but does NOT invert the IDEAL noiseless
state. The statement concerns a copy-only receiver, not coherent oracle
queries or ideal-purification reflection. Nor does it claim the noisy records
can be computed without a source oracle.

## Actual Even-Level Native Source, At Arbitrary Root Size

In the power basis1,zeta of Z[zeta], Z=[[0,-1],[1,-1]] and P=Z-I.
Direct multiplication gives P^2=-3Z. At even level2r, (P^(2r))=(3^r),
so both canonical ring-label coordinates lie in Z_q. The native frequency
row is q*beta=(u,v), where beta=(2,-1)P^(-(2r-1))/3. At r1 it is(-1,1).
Increasing r advances this row by T=-Z^-1=[[1,-1],[1,0]]. T^3=-I and
T^6=I, so the public map needs at most FIVE fixed2x2 steps at any root size.

    (a,c) = [[u,v],[u+v,-u]] * (y0,y1) modulo q.

The invariant u^2+u*v+v^2=1 gives determinant=-1, hence a bijection over
EVERY q. Independent uniform frequencies correspond to uniform native ring
labels. For integer-embedded secrets (s,0), the native three branches are
0,<a,s>,<c,s>. This is the original even native family, not a substitute
oracle problem. Odd-level constrained labels and arbitrary full ring secrets
are explicitly OUTSIDE this reduction. The compiler does not use the old
level512 HNF cap or a q-sized table.

## Exact Averaged Input Distance

Let phi=E exp(2*pi*i*E/q)=E cos(2*pi*E/q), real by symmetry. In the ideal
phase frame the density averaged over the TWO independent errors is

    rho_phi=(1/3)[[1,phi,phi],[phi,1,phi^2],[phi,phi^2,1]].

The noiseless pure density has all entries1/3. Write t=(phi-1)/3 and
r0=(phi^2-1)/3. Their difference has eigenvalues -r0 and
(r0 +/- sqrt(r0^2+8t^2))/2, from the antisymmetric branch and the remaining
two-dimensional block. For -1<=phi<=1, -r0>=0 and exactly one block
eigenvalue is negative (or all vanish at phi1). Therefore

    D(rho_phi,rho_ideal)
      =(1-phi)*(1+phi+sqrt((1+phi)^2+8))/6
      <=1-phi <=2*pi^2*V/q^2 <=20V/q^2,

capped at1. The intermediate inequality uses 0<=1+phi<=2 and sqrt12<4.
It is stronger than the previous three-block triangle estimate. The error
bound applies to AVERAGED densities, not individual noisy pure realizations.
Positivity follows directly from their error-averaged pure-state construction.

Conditioned on fixed labels and secret, IID source errors give a tensor
product of these averaged states. Product telescoping charges M times the
per-input distance. Averaging labels/secret preserves the bound. CPTP trace
contraction then transfers the success probability of ANY fixed copy-only
receiver, including adaptive measurements, by subtracting this total loss.
Postselection does not erase global error; conditional errors can amplify by
inverse acceptance probability. No efficient receiver follows from this fact.
The separate [fixed-bank indexed extension](NATIVE_NOISY_INDEXED_ACCESS.md)
now budgets approximate coherent phase/inverse access from the known noisy
values. That stronger interface does NOT inherit this smaller copy-only
averaged-state loss. Neither subsystem supplies an exact ideal inverse.

## Correlation Falsifier

Reuse of known b,d to prepare many qutrits repeats the SAME errors. It does
not manufacture independent originals. At q3, calibration chi(0)=1/2 and
chi(+/-1)=1/4 has phi(1)=phi(2)=1/4. For the two-qutrit coherence between
branches(1,0) and(0,1), reuse has a cancelling exponent, so use instead
branches(1,1) and(0,0): its exponent is2E1. The reused entry is1/36 versus
1/144 for independent pairs, a difference1/48. This falsifies the free
IID-copy shortcut. The typed preparation rejects duplicate original IDs;
unique IDs alone do NOT prove independence of the source law.

## Precision And Physical Gate Debt

For confidence kappa, choose P=kappa+ceil(log2(2M)). Require an F3
implementation of operator error<=2^-P. Compute known diagonal angles from
the certified Machin pi interval, centered numerators, and a dyadic rounding
with P+2 fractional bits. Every angle error is explicitly bounded<=2^-P.
For a diagonal gate the operator error is the MAXIMUM branch angle error,
not their sum. Composing F3 and diagonal gives per-input state trace error
<=2^(1-P); all M preparations cost<=2^-kappa.

The scalable recipe uses O(M*n) modular operations on O(log q)-bit labels,
constant-size qutrit gate descriptions, and polynomial-bit angle computation
in P. It does NOT give a universal-gate/qubit hardware synthesis. That
implementation and its promised F3 error remain explicit physical gate debt.
No hardware states have been executed in these controls.

## Continuous Gaussian Source And Conditional Consequence

[Brakerski et al.2013 Theorem2.16](https://arxiv.org/html/1306.0281) summarizes
a worst-case GapSVP to SEARCH-LWE reduction for integer n,q and
0<alpha<1 with alpha*q>=2*sqrt(n). It also gives a classical reduction
when q>=2^(n/2). Its lattice approximation factor scales as
tilde-O(n/alpha). The Gaussian convention is continuous D_alpha proportional
to exp(-pi*x^2/alpha^2), not standard deviation alpha.

Scale the torus observation by q and nearest-integer round AFTER scaling.
The error is E=nearest(qX), with public moment

    V<=q^2*alpha^2/pi+1/2 <=q^2*alpha^2/3+1/2.

The existing exact interval adapter refuses ambiguous rounding boundaries.
For containing intervals of width h, its2M-input abort union is at most
4M*h*(q+1/alpha), capped at1. Use h=2^-H with
H=bitlen(q)+bitlen(M)+kappa+3. Under the source guard this abort is<=2^-kappa.
Charge it alongside M*min(1,20V/q^2) and ALL gate errors; do not condition
on the accepted source and declare exact IID Gaussian input.

For a hypothetical polynomial M and inverse-polynomial receiver success,
q=3^(2n), sufficiently small INVERSE-POLYNOMIAL alpha and kappa=O(log n)
can make the charged loss smaller than the success. Constants/degrees must
depend on the receiver's actual M and success bounds. Exponentially tiny
alpha cannot silently retain a polynomial lattice approximation factor.
The published source guards, finite controls and this parameter observation
are NOT an admitted composed hardness proof. Source interval access,
physical gate synthesis, external review, novelty and the receiver remain
open. In particular this routine is a reduction, not a cryptanalytic attack.

## Live Controls And Failure Criteria

Five precommitted n4,M8 controls at r1/2/16/80/300 retain80 original IDs and
40 complete native recipes. The last exceeds the previous level512 ledger.
An independent JS replay checks every label, known phase, gate interval,
source ledger, exact density entry at q3/9/27/81, seven rational trace
intervals, four matching/failing Gaussian profiles and shared-error falsifier.
Numerical eigenvalues are diagnostics, never proof certificates.

Falsifiers: noninvertible actual-source map; wrong exact averaged density;
reuse/correlated or asymmetric errors; a false moment promise; hidden ideal
state access; uncharged approximation/rounding; vacuous composed loss; failed
source guard; or an efficient native receiver requiring inputs outside this
copy-only, integer-secret, even-level source. A working source bridge alone
does not resolve ANY efficient-decoding obligation.
