# Conditional Noisy-Linear To Native Classical Transcript Reduction

Status: LOCAL DERIVATION / EXTERNAL REVIEW PENDING. No native quantum states
or efficient receiver are supplied. The calibration error law is NOT an LWE
hardness source. Published source parameter guards are not blanket admission.

## Forward Noise And Statistical Transfer

Take2M classical samples b_i=<a_i,s>+E_i mod q, q=3^r, with independent
uniform full-root labels and independent identically distributed symmetric
integer errors of public second moment<=V. Pair consecutive originals without
reuse. Choose a public reduction-side uniform t in (Z/q)^n and add <a_i,t>
to the values. This makes the black-box native decoder's shared hidden secret
s+t uniform, even for a fixed source s. Decode the supplied transcript ONLY;
subtract t from the returned candidate. The reduction never knows s, changes
labels, chooses queries or produces unknown native quantum states.

Add independent PUBLIC noise nu to each pair, where

    nu(u,v)=q^-2[1+(2/3)(cos(theta_u)+cos(theta_v)
                                         +cos(theta_u-theta_v))].

Its nonzero Fourier coefficients outside the origin are exactly1/3 at
+/-(1,0),+/-(0,1),+/-(1,-1). If phi=E cos(2*pi*E/q), symmetric source errors
give pair-noise coefficients phi,phi,phi^2 at these modes. Thus convolution
P*nu differs from nu by multiplying the three cosine coefficients by those
values. No inverse characteristic function or positivity repair is needed.
Character orthogonality normalizes nu for EVERY full ternary root.

Since -1<=phi<=1,

    TV(P*nu,nu) <= [2(1-phi)+(1-phi^2)]/3
                <= 4(1-phi)/3 <= 80V/(3q^2).

The last bound uses cos(x)>=1-x^2/2 and pi^2<10, on actual integer error
representatives before modular reduction. Cap at1. For a FIXED decoder
using M records, success on the source transform is at least its success on
the native measured law minus M times this bound and all charged aborts.
The same coupling bound holds for quantum postprocessing of the CLASSICAL
transcript; it does not reconstruct the original coherent states.

If labels are chosen, errors are correlated/asymmetric, originals are reused,
or V is guessed from a few observations, the theorem's premises are missing.
Schema validation cannot infer these probabilistic promises from values.

## Certified Public Sampler

Uniform proposals in (Z/q)^2 have acceptance

    A(u,v)=[3+2 cos(theta_u)+2 cos(theta_v)+2 cos(theta_u-theta_v)]/9.

This lies in[0,1] and has mean1/3. The implementation uses no floating trig
or q^2 table. A Machin enclosure pi=16 atan(1/5)-4 atan(1/239) uses alternating
series with explicit next-term remainders. Its identity follows from
tan(2 atan(1/5))=5/12 and tan(4 atan(1/5))=120/119: subtracting atan(1/239)
gives tangent1 in(0,pi/2), hence pi/4. Rational bounds establish3<pi<4.

For B requested cosine bits, each arctangent remainder is<=2^-(B+10).
The phase midpoint has argument uncertainty<=10*2^-(B+10), because its
centered residue is at most q/2. Taylor's Lagrange remainder is bounded by
4^(2N+2)/(2N+2)! and reduced below2^-(B+8); derivatives are bounded by1.
The resulting rational cosine interval has width<=2^-B. Exact root0 and
one-third-root shortcuts retain cos1 and cos(-1/2). Interval clipping is
valid only because the true cosine/acceptance already has the stated range.

A lazy uniform coin prefix defines [k/2^B,(k+1)/2^B). Accept ONLY when the
coin upper endpoint<=the acceptance lower bound, reject ONLY when its lower
endpoint>=the acceptance upper bound, otherwise refine. Decisions are exact.
At the coin-bit cap, return UNKNOWN, never compare a midpoint. At the proposal
cap, return UNKNOWN, never silently restart or drop the failed pair.

With L proposals and B maximum bits, couple to ideal unbounded rejection:

    sampler_abort_probability <= (2/3)^L + 3L*2^-B.

The precision term follows because an unresolved final coin bracket has
probability<=acceptance_interval_width+2*2^-B<=3*2^-B for any proposal.
Charge this for EVERY output record. Accepted decisions are certified, but
conditioning away aborts need not give exact nu. The complete transcript
must retain failure as failure; partial outputs cannot replace M promised
originals. Expected proposals<=3 before abort; expected refinement cost is
bounded by a geometric precision tail. Rational bit lengths and arithmetic
cost are polynomial in log(q), B and the displayed Taylor budgets.

FIXED finite precision is not an asymptotic guarantee. For M outputs and
kappa requested failure bits, the profile factory chooses

    L=2*(kappa+ceil(log2(2M))),
    B=kappa+ceil(log2(6ML)).

Since(2/3)^2<1/2, the M-record proposal-cap union is<=2^-kappa/2;
the precision-cap union is also<=2^-kappa/2. Hence all sampler aborts together
cost<=2^-kappa. The exact rational ledger verifies this inequality. Bounds
from fixed64/128 calibration caps must not be extrapolated to unbounded M.

## Continuous Gaussian Source Adapter

[Brakerski et al.2013, Theorem2.16](https://arxiv.org/html/1306.0281)
states a search-LWE worst-case reduction for integer n,q and alpha in(0,1)
with alpha*q>=2 sqrt(n); it also gives a classical source reduction when
q>=2^(n/2). Its Gaussian convention is D_alpha proportional to
exp(-pi*x^2/alpha^2), not standard deviation alpha. It uses continuous
torus observations. Prime-only versions are not being imported here.

Scaling and rounding observations works because q<a,s> is an integer:
nearest(qb) mod q=<A,s>+nearest(qX) mod q. With X from D_alpha,
E[X^2]=alpha^2/(2*pi). Since |nearest(qX)-qX|<=1/2,

    E[nearest(qX)^2] <= q^2*alpha^2/pi+1/2
                     <= q^2*alpha^2/3+1/2 = V.

This is a public conservative moment bound for ROUNDED continuous Gaussian
noise, not an assertion that it equals the discrete-Gaussian distribution.
The source theorem's approximation factor and efficiency premises remain
those of the cited source. Parameter profiles test the algebraic guards;
they do not prove cryptographic hardness or source-oracle implementation.

Input b arrives in a CONTAINING rational interval of width<=h. The adapter
returns a value only if floor(q*lower+1/2)=floor(q*upper+1/2), otherwise
UNKNOWN. Wrapping representative intervals is harmless modulo integer q.
The Gaussian Y=qX has fractional-part density bounded by1+1/(q*alpha):
on each translated Gaussian sum, all terms except the closest-to-zero one
are bounded by disjoint adjacent integrals, whose total is q*alpha; the
remaining term is<=1 before normalization. An ambiguous containing interval
forces Y within qh on either side of a half-integer. Thus

    per_input_rounding_abort <= 2h(q+1/alpha),
    all2M_input_rounding_aborts <= 4Mh(q+1/alpha),

capped at1. This remains valid for adversarial placement of containing
intervals of bounded width. Their actual containment is a source-oracle
promise, not inferred by the adapter. Width
h=2^-(bitlength(q)+bitlength(M)+kappa+3) is explicit in the profiles. When
the source guard holds, 1/alpha<=q/2, so all input rounding aborts together
cost<=2^-kappa as well. Source rounding,
native-noise TV and sampler abort losses are added, NEVER erased by conditioning.

## Asymptotic Success-Transfer Scope

Suppose a FIXED native CLASSICAL-transcript decoder uses at most polynomial
M(n,log q) records and has inverse-polynomial success on uniform secrets.
For sufficiently large n, choose q=3^(2n), inverse-polynomial alpha small
enough that M*alpha^2 is below that success, and kappa=O(log n) with constants
depending on the specified record/success bounds. Both published source
guards then hold, the rounding moment contributes only O(M/q^2), and all
precision/proposal resources stay polynomial. The source theorem's lattice
approximation factor remains polynomial, but depends on the chosen alpha.
This is NOT a fixed-parameter cryptographic security theorem and requires
explicit decoder bounds; choosing exponentially small alpha to hide this
dependence would give a different, potentially trivial approximation regime.

A classical transcript decoder would therefore compose with the published
classical source reduction in this regime. A quantum decoder on CLASSICAL
input can likewise be called on the transformed transcript. A receiver
requiring unknown coherent native qutrits cannot: those are not outputs of
this reduction. Any hardness statement remains conditional on the cited
worst-case/source premise and external review, never proved by this code.

## Admission And Falsification

The live four source-transform calibrations use chi(0)=1/2, chi(+/-1)=1/4,
V=1/2, at root digits2/4/16/80. They exercise public masking, full-root labels,
original-source ancestry and every rational sampling decision. They are
arithmetic controls, NOT evidence of classical hardness or quantum recovery.
Four rounded-Gaussian profiles include matching and failing source guards,
and a large-noise profile whose transcript bound is vacuous.

An independent JS replay must check all intervals/coins, transformations,
resource counts, parameter guards and TV ledgers. Bounded cyclotomic controls
must separately check exact finite Fourier/convolution identities; the
unsmoothed inverse kernel is negative at native zeros when0<phi<1 and all
source Fourier modes are nonzero. That obstruction is scoped to exact inverse
degradation, not the implemented approximate forward convolution.

Required before admitting a full composed hardness claim: external review,
source oracle precision/containment, a specified scalable native decoder and
its success/sample premises, and a legitimate asymptotic parameter family.
An efficient native quantum receiver needs a SEPARATE coherent input bridge.
No CandidateRecord speedup is admitted by this subsystem; no classical
failure, parameter check or simulation creates one.
