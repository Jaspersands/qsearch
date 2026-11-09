# Two-Fock learning: actual-source scope

7 November2026. Read current STATE/TRAPS and the supplied local primary
texts/PDF metadata in `audits/sources/two_fock_learning/`. No network,
Git/API, implementation, or full candidate proof audit. Line numbers below
refer to those exact `.txt` files. The candidate is an unknown Gaussian
image of a parity-definite coherent superposition of two arbitrary Fock
strings, with growing separation k, exact IID copies only.

**Scope verdict:** the checked sources do not already supply the entire
growing-k endpoint. They DO supply the small-compressibility fallback.
The new fourth-cumulant identity, spectral reconstruction, conditioning,
branch inference, and final error budget remain independent obligations;
no source open-question label establishes novelty or hardness.

## Sen2609.12219v1

`sen.txt`: Theorem1.1 at38--43 learns a k-sparse state in the GIVEN
computational basis from copies, with support size supplied. Its displayed
near-linear time/sample bounds are for infidelity epsilon and delta=1/n.
It does not learn an unknown Gaussian basis. Section1.4 at316--324
explicitly asks for learning in an "unknown Gaussian rotated Fock basis"
with polynomial modes/sparsity/accuracy resources. This motivates the
present question but is not a theorem for it, nor evidence that no other
paper answers a subclass. Here source sparsity2 must not be confused with
the candidate's Hamming separation k.

## Amidi--Asadian--Moosavian2610.08723v1

`structured.txt`: the exact model at151--191 has disjoint fixed-particle
branches F_bl in each block, |F_bl|=p_b<=r_star. The cap is explicitly
"fixed independently of the total mode number n" (176--180), although
branch counts and block counts may grow. Unknown evolution is EVEN
Gaussian, R in SO(2n), allowing pair creation but preserving parity
(167--187). Input is independent copies with calibrated Gaussian rotations
and occupation measurements (188--200), not a supplied unknown circuit.

Theorem1 at215--268 is therefore a genuine unknown-frame copy learner,
with no supplied minimum weight/covariance gap. However its adaptive copy
exponent is max(20,2r_star+6), classical-arithmetic exponent
max(22,4r_star+9), and nonadaptive exponents likewise grow with r_star.
Setting r_star=k/2 does not give a uniform polynomial bound at growing k.
Lines201--209 explicitly exclude physical gate depth and BIT complexity
from this resource comparison; do not silently upgrade those counts.

Under Pin particle-hole normalization a two-Fock cat has two disjoint
branches with k/2 particles. This map need not be EVEN: for an even vacuum/
full cat on n=k=2 modulo4 modes, the resulting fixed-particle branches
have odd parity. Thus the SO theorem cannot be imported without matching
parity/core conventions. Even disregarding that obstruction, allowing
particle cap k/2 loses its fixed-cap polynomial guarantee. Merely displaying
this representation would not exclude a different small-cap Gaussian
representation. A useful invariant excludes that
loophole for the balanced growing-k subfamily: its covariance is zero,
and for k>=6 its fourth cumulant is W(J), whose flattening on the full
bivector space has eigenvalues k-1,+1,-1 and hence full rank. In the source
model, zero covariance excludes cores and forces each branch weight1/2,
so each block has exactly two branches and at most2r_star modes. Multiple
blocks give zero connected fourth tensor on cross-block bivectors. Full
flattening rank therefore forces ONE block and r_star>=k/2. This paragraph
is an elementary model/invariant deduction, not a quoted source theorem.

Theorem2 is narrower than arbitrary quartic-tensor reconstruction:
lines242--269 define a FIXED reference consisting of B identical equal
four-mode paired blocks, (|1100>+|0011>)/sqrt2. Lines294--317 learn its full
even-Gaussian orbit, using O(n^19 epsilon^-2 log(n/delta)) quartic shots
and polynomial classical processing. The tensor/commutant calculation at
319--331 recovers eight-Majorana blocks for THAT orbit. It is not stated
for arbitrary two-branch growing cats, arbitrary amplitudes, or arbitrary
fourth tensors. Lines419--430 retain the fixed-cap/fixed-reference limits.

## Mele--Herasymenko, PRX Quantum6,010319(2025)

`compressible.txt`: Definition2 at242--248 permits an arbitrary t-mode
core followed by a Gaussian, not just a fixed number of doped gates.
Theorem2 at306--312 and exact Theorem6 at1384--1406,1451--1453 learn an
unknown PURE t-compressible state from single-copy measurements, outputting
a classical Gaussian/core preparation description (1465--1469). The
explicit sufficient count is

    256 n^5 epsilon^-4 log(12n^2/delta)
    + 2 Ntom(t,epsilon/2,delta/3) + 24 log(3/delta).

Lemma15 at1347--1358 supplies Ntom=O(2^t*t*epsilon^-4*log(1/delta))
and Ttom=O(4^t*t^3*epsilon^-5*log(1/delta)). Thus t<=4 is polynomial
without a covariance-gap promise. Source postselection is paid by the
fixed copy count/Chernoff bound, not a free conditional oracle (324--350).
For n<=4, use full constant-size tomography rather than formulas dividing
by n-t. Generic growing cats are not4-compressible: for k>=6 and both
weights nonzero, k covariance normal eigenvalues are |1-2p|<1, so their
exact Gaussian nullity is k, using the source equivalence at269--284.

ROBUST fallback: Theorem10 at2018--2041 assumes

    min_(sigma_t in G_t) Dtr(rho,sigma_t) <= epsilon^2/[4(n-t)].

It then returns a possibly MIXED estimate within epsilon, failure delta,
with polynomial covariance work plus mixed-core Ntom(t,epsilon/4,delta/2).
An arbitrary epsilon-close input promise is insufficient for this displayed
bound; the n/accuracy dependence must be paid. Theorem9 at1971--1974 and
1917--1938 alternatively uses the square-root covariance-tail penalty.
For a pure native target, a PURE preparation can be obtained separately:
if the returned mixed state is tau-close, its largest eigenvalue is at
least1-tau; replacing its fixed-size core by a top eigenvector changes it
by at most tau, hence gives distance<=2tau. This is a deduction, not the
literal mixed-output guarantee. Reserve numerical/eigenvector errors.

PARITY convention matters: this source defines Gaussian unitaries using
ALL O(2n), including determinant-1/Pin transformations (177--189,676--683),
whereas the structured source uses SO(2n)/even quadratics. Do not identify
these control models silently. For a retained core with t>=1 an odd Pin
decoder can be made even by composing a known Majorana reflection inside
that core. It preserves discarded vacuum and absorbs the parity change
into the core state. Thus a4-mode fallback admits an even-control repair;
a zero-mode vacuum convention needs separate occupied-core/parity handling.
Parity-definite two nonzero Fock branches have even Hamming separation.

## Classical comparator and boundary

With alpha,beta,x,y and G SUPPLIED, the state is a known coherent sum of
two Gaussian branches. Gaussian/Pfaffian transition amplitudes, overlaps,
and their four coherent probability terms give the matched polynomial
classical simulation route, including sequential occupation sampling with
appropriate numerical precision. This is a supplied-description baseline,
not unknown-copy inference. The structured source itself distinguishes
preparation learning from classical joint-outcome sampling at413--418.
No computing/sampling advantage is established by the candidate. No whole
learner is promoted by this source review.
