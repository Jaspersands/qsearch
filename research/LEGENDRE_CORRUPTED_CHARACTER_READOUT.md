# Decoding one fixed corrupted character function

2026-11-05. Independently reviewed written derivation; the prespecified
finite falsifier is complete. This is not device-noise tolerance,
quantum execution, novelty, a speedup or a classical lower bound.

## Scientific question and input contract

Can the explicit coefficient-space receiver solve the fixed-degree noisy
character reconstruction problem with a constant fraction of adversarial
table errors and sublinear quantum time? The external comparison is
Kopparty, arXiv:2601.07137, Algorithm A/Theorem 3.1: a classical full-table
poly(p) decoder with error radius below 1/8. The fixed-degree query/time
distinction in that paper motivates this question; source searches do not
establish priority. Corpus been-tried and baseline lookups found no exact
prior implementation. The catalog returned no matching classical baseline,
so the primary source and direct candidate enumeration were checked.

Fix d>=2. Let rho be a public rational upper bound with 0<=rho<1/4, and
put kappa=1-4rho>0. The unknown target Q is monic, squarefree, degree d over
a growing odd prime field. Define lambda(0)=+1, lambda(z)=chi(z) otherwise.
An arbitrary FIXED function F:F_p->{+1,-1} differs from lambda composed
with Q on at most rho*p points. Input consists of fresh exact tensor copies

 phi_F=p^(-1/2) sum_x F(x)|x>.

A coherent bit oracle or an uncontrolled raw phase unitary for this ONE
fixed F supplies each copy with one query. The receiver gets no correct
values, corruption labels, Q roots, hidden factorization or source inverse.
The corruption mask can be adversarial; it is not resampled at each query
or copy. Quantum inputs are pure independent copies, not an arbitrary
mixed-state or correlated-error source. Output Q with probability>=1-eta.

Proposed mechanism: the existing paid split-coefficient encoding, an EXACT
signed-subset overlap, uniform Fourier rank growth, and statistical public
candidate projection. Target resources for fixed d and rho:
C_d poly(logp,kappa^(-1),log(1/eta)) gates/copies. No polynomial-in-d bound.
Cheapest falsifiers: cancellation of signed-subset overlap; confusing
without-replacement with IID products; a missing verification gap; small-p
nonidentifiability; or importing a mixed-noise source. No new subsystem.

## 1. Exact overlap under fixed corruptions

Use the circuit and virtual state from LEGENDRE_SQUAREFREE_RESULTANT_READOUT.md.
Let r be the number of rational Q roots, n=p-r, and B the number of corrupted
NONROOT points. Write U=product_j(p^(d_j)-1), N0=(p-1)binom(p,d), and
Ngood=(p-1)binom(n,d). All are analysis quantities; none is supplied.

The d-copy distinctness flag still has success alpha=(p)_d/p^d because
every source amplitude is a sign. Clean public coefficient encoding gives
the normalized state S_F on all completely split squarefree degree-d R.
On R coprime to Q, actual/virtual phase ratio is the product of the fixed
error signs e(x)=F(x)lambda(Q(x)) over the d roots. On other R the virtual
amplitude is zero. Thus, up to the one global sign chi(-1)^d,

 <N_Q,S_F> = gamma_clean E_d,
 gamma_clean=Ngood/sqrt(N0*p*U),
 E_d = sum_(j=0)^d (-1)^j binom(B,j)binom(n-B,d-j) / binom(n,d).

This is a signed sample WITHOUT replacement. Errors at Q roots do not
change the overlap: those labels are zero in the virtual state, but remain
present in the actual state. No unknown root is detected or discarded.

Let mu=1-2B/n. IID sampling from the same n signs has expected product
mu^d. Conditional on no repeat it has expectation E_d. Since the product
has absolute value one,

 |E_d-mu^d| <= 2 Pr[repeat] <= d(d-1)/n.

For p>=4d and rho<=1/4, n>=3p/4 and mu>=1/3. If
n>=2d(d-1)3^d, then E_d>=1/(2*3^d). This is a uniform proof for every
corruption mask, not a typical-error or finite-size argument.

## 2. Enough independent Fourier equations

At p>=4d^2, the squarefree note gives gamma_clean>=1/(4sqrt(d!)) and
U>=p^d/2. Therefore under the conditions above,

 gamma_F=|<N_Q,S_F>| >= 1/(8*3^d*sqrt(d!)).

The virtual Fourier state is supported on exactly U dual-unit labels in
H=span(Q)^perp. Every proper W<H has virtual mass <=p^(d-1)/U<=2/p.
Consequently

 Pr_(F S_F)[y in H\W] >= [gamma_F-sqrt(2/p)]_+^2.

Define L_d=512*9^d*d!. For d>=2, p>=L_d also implies all auxiliary
conditions p>=4d^2 and p-r>=2d(d-1)3^d. The resulting escape bound is at
least 1/(256*9^d*d!). Including alpha>=1/2 gives probability>=1/L_d
per attempt of a new independent genuine equation, uniformly over the
previous genuine span. A block of d attempts consumes d^2 copies and
produces Q with probability at least q0=L_d^(-d).

Solve each measured d-by-(d+1) system; reject unless it has rank d and its
kernel line has a monic degree-d squarefree representative. This is the
existing public candidate procedure, not an inlier oracle. The one shared
public signature seed pays clean factorization for all source coefficients
at once, independently of F or Q. No extension algebra is queried.

## 3. Statistical verification replaces consecutive acceptance

Set beta=1-2rho=(1+kappa)/2. Public projection onto the known candidate
state phi_C uses a fresh unknown copy phi_F and the inverse preparation
of PUBLIC C. For the true Q its ideal acceptance probability is at least
beta^2; it need not be one.

For every wrong monic squarefree degree-d C, the previous shared-factor
Weil argument gives

 |<phi_C,phi_Q>| <= b=[(2d-1)sqrt(p)+2d]/p.

Changing at most rho*p signs changes any correlation by at most 2rho.
Hence |<phi_C,phi_F>|<=b+2rho. For p>=64d^2/kappa^2, b<=kappa/2,
and the wrong-candidate acceptance probability is at most 1/4. Define

 Delta=beta^2-1/4 >= kappa/2,
 tau=(beta^2+1/4)/2.

Run K independent public-candidate projections and accept when their
empirical mean is at least tau. Compute the public rational threshold
exactly, or round it with error<=Delta/8; no exact-real advice is required.
With per-test synthesis event error<=Delta/8, true and false means remain
at least Delta/4 on their correct
side of tau. Hoeffding's inequality bounds each classification error by
exp(-K Delta^2/8). This holds conditional on any previously generated
classical candidate because every verification copy is fresh.

Do NOT reuse the earlier rule that all K tests must accept. When the
correct table has a nonzero corruption fraction, that rule rejects the
correct candidate with probability approaching one as K grows.

## 4. Complete bounded schedule

One sufficient prime threshold is

 p>=max{L_d,64d^2/kappa^2}.

Allocate total operator error <=q0/8 per d-attempt generation block;
its true-candidate probability remains at least q0/2. Set

 R=ceil((2/q0) ln(4/eta)),
 K=ceil((8/Delta^2) ln(8R/eta)).

The probability no generation block produces Q is at most eta/4. At most
R candidate tests are performed; their combined false acceptance or true
rejection probability is at most eta/8. This union bound also handles
early stopping. It does not assume candidate correctness or independent
error events. Public signature-seed failure costs <=eta/16, and its capped
classical uniform samplers cost <=eta/8, exactly as in the previous note.
The total is below eta. Copies are capped by R(d^2+K).

All coefficient maps, public root erasure and candidate squarefreeness
tests reuse the prior exact circuits. Interval states and arbitrary-modulus
Fourier transforms use the paid approximate constructions. Choose total
operator error <=Delta/16 for each public candidate projection, implying
the above event budget. Precision logarithms and bounded classical
postprocessing have the claimed polynomial dependence; constants in d
are large. There is no oracle over the extension algebra and no hidden
table of size p in the quantum circuit.

## 5. Strong classical comparators and the radius boundary

For fixed rho<1/8, Kopparty's full-table Algorithm A applies for sufficiently
large p after charging <=d root-padding discrepancies and its stricter
Theorem 3.1 degree condition. It uses p native queries and poly(p) time.
Do not extend its stated radius to the entire rho<1/4 regime here.

For every rho<1/4, classical BIT access has a low-query exhaustive decoder.
At the above threshold, every wrong candidate has Hamming distance from F
at least (1-b)/2-rho, versus <=rho for Q, a gap >=kappa/4. Sample

 T=ceil(128*kappa^(-2)*ln(2*p^d/eta))

uniform original inputs. Hoeffding plus a union bound over at most p^d
monic candidates bounds all empirical distance errors by kappa/16 with
probability>=1-eta. Enumerate monic squarefree degree-d candidates and
choose the empirical minimum. Its query count is polynomial in logp;
its time is p^d*T*poly(d,logp), not polylogarithmic. Full-table nearest
decoding is also a direct O(p^(d+1)*poly(d,logp)) upper bound. Supplied
quantum copies alone do not give the classical queries in this comparator.
No query separation or classical time lower bound follows.

For any FIXED rho>1/4, universal exact recovery is information-theoretically
impossible at sufficiently large p. Distinct monic squarefree degree-d
character tables have Hamming distance p/2+O(d sqrt(p)); split their
disagreement positions to obtain ONE function within p/4+O(d sqrt(p)) of
both. This supplies an ambiguous input. It is an asymptotic midpoint
obstruction, not an assertion that the exact finite unique radius is 1/4.

## Finite falsifier and remaining boundaries

Predeclared controls: p11 Q=X(X-1), p11 Q=X(X^2+1), p7 Q=X(X^2+1).
For each use no flips, the first nonroot, first two nonroots, and first root.
Run native table-only classical nearest decoding FIRST, then compare actual
coefficient amplitudes with the exact signed-subset overlap, virtual Fourier
support and escape bound. No broad noise grid or device simulation.

The decisive analytic countercontrol is already exact: for the p7 mixed
cubic, n=6,d=3,B=1, E_3=[binom(5,3)-binom(5,2)]/binom(6,3)=0,
whereas mu^3=(2/3)^3=8/27. The virtual overlap vanishes for one flipped
nonroot, at a prime far below the theorem threshold. This refutes the
uncontrolled IID substitution, not every receiver or the large-p theorem.

Artifacts: classical_baselines/corrupted_character_resultant_control.py/.json.
All 12 fixed controls and 808 proper-subspace checks passed. Exact E_d values
for the four masks are (1,5/9,2/9,1), (1,2/5,1/15,1), and
(1,0,-1/5,1) for the three families, respectively. Root-only flips preserve
the virtual overlap. Maximum floating overlap residual <3.4e-16. Only the
clean/root-flipped p11 quadratic has a positive coarse escape bound; the
other ten are vacuous. Every tested prime is below the theorem threshold.
No quantum circuit or root-cleanup operation is executed by these checks.

The table-only baseline also found an EXACT physical phase ambiguity at p11:

    Q=X^3+X,
    C=X^3+4X^2+3X+8,
    lambda(C(x))=-lambda(Q(x)) for every x in F_11.

Both are monic squarefree cubics. Their clean physical phase copies coincide
up to global sign, although their BIT tables differ and signed classical
nearest decoding distinguishes them. A fresh-copy projection cannot solve
this small-prime ambiguity. The parent independently reproduced this identity
and the p7 cancellation using exact Sage arithmetic.

Review: audits/reviews/2026-11-05-corrupted-character-resultant-review.md
accepts the all-parameter proof, stated threshold, uniform mask bound,
statistical verifier, classical comparator and total failure<=9eta/16.
No mixed-state/device-noise, changing oracle, correlated-bank, growing-degree,
all-small-prime or arbitrary-polynomial claim is made. Repeated factors
retain the exact indistinguishability counterexamples in the squarefree note.
