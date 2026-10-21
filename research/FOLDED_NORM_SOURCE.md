# Folded Norm Source: Phases, Scalar Rank And Matched Attacks

2026-10-19. Executed local source tests, known classical decoder, explicit
classical attacks and local finite readout derivation. Independent mathematical
review pending. NO new quantum algorithm, novelty, classical hardness, practical
gate budget or runtime speedup is claimed. The candidate remains UNADMITTED.

Run `python theorems/folded_norm_source.py --write` and
`python theorems/folded_norm_attacks.py --write`. The decoder remains
`python theorems/folded_rs_decoder.py --write`.

The actual global native quadratic solver probe is now complete; see
[Native Global Square Completion](FOLDED_NORM_MQ.md). All three unchanged
large inputs hit the declared time budget, including the already classically
solved25-block input. This supplies an exact representation/checker, NOT
hardness or a reason to increase generic solver budgets.

## Problem And Access

Use the explicit task in FOLDED_NORM_SOURCE_DECISION.md. Public polynomials
P have F_p coefficients, degree<K, at nm distinct folded points gamma^j.
Each block is embedded into E=F_(p^m) with a specified power basis, then tested
against its PUBLIC shifted quadratic-residue coset. Input size is polynomial
in nm and log p; neither party receives a random membership oracle. Both can
evaluate the same norm predicate. Quantum coherent evaluation must be compiled
from this arithmetic, not provided as free access.

The present family uses p3mod4, odd m, common zero policy, arbitrary public
shifts and signs. K is a SCALAR F_p dimension. The code need not be E-linear.
Allowing arbitrary E coefficients in P, expanding length to p, or interpreting
E addition as cyclic addition modulo p^m changes the problem.

## Actual Public Field And Fourier Phase

The producer searches monic degree-m polynomials with a deterministic public
replay seed and TESTS irreducibility. It stores the actual modulus and number
of tests;2048 exhausted tests would be a setup failure, not problem hardness.
No field table is built for the large field. The p61,m31 record needs8 tests.

Let b_i be the basis and G_ij=Tr(b_i*b_j). Its inverse is COMPUTED and checked.
For a coordinate frequency xi, lambda has coordinates G^-1*xi, so
Tr(lambda*sum x_i b_i)=sum xi_i*x_i. A generic invertible linear map on a block
pulls frequencies back by its inverse TRANSPOSE, not by field multiplication.
Independent full-coordinate DFT tests include such a nonscalar map.

With chi(0)=0, Q=p^m, eta+1 including zero/eta-1 strict, and sign sigma,

```text
rho = (Q+eta)/(2Q),
g(z) = [Q*sigma*chi(z-t)+eta*(Q*1_(z=t)-1)] / sqrt(Q^2-1),
ghat(xi) = exp(-2*pi*i*Tr(lambda*t)/p)
           *[eta+sigma*chi(-lambda)*tau_E] / sqrt(Q^2-1), xi!=0.
ghat(0)=0.
```

The canonical Gauss phase is NOT automatically +i when Q3mod4. Directly,
tau_E=sum_z exp(2*pi*i*Tr(z^2)/p). This is the trace-form quadratic sum
with Gram matrix G. Congruence diagonalization gives

```text
tau_E = chi_p(det G) * tau_p^m.
```

The one-dimensional canonical tau_p is sqrt(p) or i*sqrt(p). At p3mod4,m31,
the actual unit is -i. This agrees with the Hasse--Davenport formula described
in [Conrad, Appendix A](https://kconrad.math.uconn.edu/blurbs/gradnumthy/Gauss-Jacobi-sums.pdf).
Thus |ghat(xi)|^2=1/(Q-1) when Q3mod4. Even m has real Gauss sum and unequal
nonzero magnitudes; the flat-source wrapper REJECTS it rather than importing
an IID error premise. All complex phases, shifts and signs remain essential.

Two complete p7,m3,n2,K4 calibrations enumerate685 source errors and2401
native coefficient messages. The actual source, syndrome coalescing, unique
herald and coordinatewise F_p FFT agree with direct native predicate filters
to about2.2e-17. Substituting the WRONG prime-field +i sign changes output TV
by about0.702. These are identity/counterexample controls, not toy speedups.
They do not establish the large algorithm by finite extrapolation.

## Correct Whole-Ball Collision Bound

On a support S of j blocks, error values are independent uniform E*, with
(Q-1)^j possibilities. H has K scalar Vandermonde rows. Its support map is
injective when m*j<=K, and a union of j+r-h blocks has scalar rank
min(K,m*(j+r-h)). For a competitor support T of size r and overlap h:

- If the union has at most K scalar columns, no distinct collision exists.
- Otherwise the syndrome-subspace intersection has dimension d=m*(j+r)-K
  OVER F_p. The shared-support image has dimension m*h. These p^(m*h)
  vectors cannot have EXACT support S and are excluded.

Hence a safe per-sphere union bound is

```text
epsilon_j <= min(1,
  sum_(r=0)^ell sum_h C(j,h)*C(n-j,r-h)
    *[p^(m*(j+r)-K)-p^(m*h)] / (Q-1)^j),
```

where max(0,j+r-n)<=h<=min(j,r,floor((m*(j+r)-K-1)/m)). Count the WHOLE
ball, not only weight-ell rivals. This bound requires m*ell<K. It uses MDS
scalar-column independence, not a fictitious E-linear parity matrix.

Exact countercontrol p5,n2,m2,K3,ell1: each support has24 nonzero errors;
4 on each collide, giving epsilon1=1/6. Rounding rank3 UP to two E symbols
would falsely report no collisions. Independent full native enumeration checks
this case. The actual folded-decoder ambiguity at weights3/4 is also retained.

At most M=sum_(r<=ell) C(n,r) errors share any syndrome, since each support
map is injective. With epsilon=max epsilon_j, the existing unique-good versus
coalesced-bad argument gives success>=1-epsilon and squared pure-distance
bound M*epsilon/(1-epsilon+M*epsilon). No random-input premise is required.

## Finite Mean Requires One More Block Radius

The binary-predicate identity g_i^2=1+beta*g_i gives the same radial Jacobi
recurrence for this F_p-linear code; it does not require E linearity. Source
radial states are orthogonal BEFORE syndrome coalescing. Multiplication by
normalized score extends radius ell to ell+1. EXACT MDS moments suffice when
m*(2ell+1)<=K. Otherwise the Gram bound must use the ENTIRE extra-radius ball
and requires m*(ell+1)<K; reaching scalar capacity stays UNKNOWN.

For that extended ball let delta=max(1,M-1)*epsilon. Coherent Cauchy gives
||G_radial-I||<=delta uniformly over radial coefficients and arbitrary phases.
When delta<1, the score expectation differs from the ambient Jacobi Rayleigh
quotient by at most2delta/(1-delta). Subtract the separate source/herald TV
bound. The implementation REUSES the existing rational Rayleigh, square-root
enclosure and integer-score tail helpers. Numerical eigenvectors only propose
saved dyadic weights; global optimality and binomial quantum tails are not
assumed. The p7 calibration has unknown mean because its observable reaches
capacity despite its correct native interference.

## A Bounded Decoder Is Not An Exact Decoder Oracle

Known interpolation/pruning is now actually implemented, but an arbitrary
unique error can still be missed by a bounded randomized pruning run. With
order s, r<=s-1, and Delta=(n-ell-floor((nm-K-1)/m))/n, each unique error is
missed with probability at most nu=(1-Delta^(s-1))^T. Charge ALL T trials.

Choose fresh classical uniform block choices BEFORE each quantum preparation.
For each resulting deterministic decoder D_R(syndrome), compute it reversibly,
subtract its selected validated error from the source register, compare to
zero, and reverse the SAME decoder workspace using the unchanged syndrome.
This is an actual specified classical function, not a history-inversion oracle.
Its source error and syndrome inputs are preserved during workspace reversal.
Success erases the source error; failure retains a nonzero register and flag.

Compare this isometry with exact unique-source erasure. They agree on all good
basis errors except pruning failures; their difference on the remaining source
has norm at most2sqrt(bad mass). Averaging over R and Jensen bounds the FULL
flagged-output trace error by2sqrt(epsilon+nu), conservatively clipped at1.
For per-attempt reward, score a failure as ZERO; subtract this trace error
from(1-epsilon) times the exact-unique-herald score/tail bound. This does not
claim that the conditional successful output has the uncorrected ideal mean.

At T1 the bound is vacuous at n25; the code preserves zero per-attempt reward.
At T4096 it is useful, with the seed length, trials and reversible work still
paid. Seeded transcripts are replays, not proof of independent uniform coins.
Any gate-synthesis/QFT/source trace error zeta must be SUBTRACTED additionally.
No such compiled implementation or machine-level gate budget is supplied here.

## Explicit End-To-End Mechanism And Resource Debt

The mathematical composition is the KNOWN DQI mechanism: prepare dyadic radial
weights and uniform supports; on selected blocks prepare uniform nonzero E
coordinates and the COMPUTABLE phase above; compute H*e; apply the specified
bounded reversible decoder/compare/uncompute; herald and F_p-Fourier read out
K coefficient registers. Uniform nonzero E can use an integer interval-prefix
state followed by base-p conversion; this is NOT a cyclic QFT modulo Q.
The field norm, trace dual, character and phases are public polynomial arithmetic.

For L=nm, B=ceil(log2 p), dense interpolation/RREF plus native conversion has
O(L^3+T*L^2) base-field operation upper scale for fixed m,s, plus support/source
preparation and precision costs. Reversible compilation can retain polynomial
history rather than assume free erasure; its space/gate constants may be huge.
This is a complexity upper scale, NOT a Toffoli count or practical runtime.
The block-value source alone occupies L*B logical qubits, before syndrome,
decoder, seed and work registers. Field setup and failed public searches count.

The exact source formulas, finite bounds and classical decoder now supply a
specific constructive route rather than an unspecified mathematical decoder.
But it is an instantiation of known algorithms, not a discovered Shor-level
mechanism. No new reduction from discrete log, natural lattice problems or
another established hard task is known for these explicit norm lists.

## Same-Input Classical Results And Limits

Classical attacks sample accepted values as a_i*V_i^2, interpolate COMPLETE
blocks with original F_p coefficients, then try accepted block-exchange repairs.
All failed proposals remain. The square-value sampler is NOT asserted uniform
on the accepted set. Fixed public shifts/signs are never rerolled.

| Blocks | Scalar K | Source Radius | Classical Best | Exact-Decoder Mean Floor | Pruning-Paid Per-Attempt Mean Floor |
| --- | --- | --- | --- | --- | --- |
|25|310|6|21|21.132867|21.132864|
|65|806|15|53|56.698728|56.698412|
|127|1550|30|99|113.302668|113.278983|

Each classical record uses32 complete-block fits plus64 repair proposals,
with original field/norm/Horner witness checks. Quantum floors assume the
specified exact-source/reversible-decoder composition, NOT executed quantum
gates. This table is NOT a runtime comparison, hardness evidence or quantum
advantage certificate. A successful word and a quantum mean lower bound are
different quantities; beating a LOWER bound would not refute the algorithm.

For a SINGLE interpolation fit on truly IID uniform public shifts, unanchored
blocks remain independent, so its POPULATION score is b+Bin(n-b,rho), b=floor
(K/m). A union bound covers NONADAPTIVE repeated fits, without assuming their
independence. It does NOT give a restart law on one fixed input, and does NOT
cover repairs selected using previous outcomes. Exact enumeration of all small
shift pairs checks that distinction. Deterministic saved sources are not an
IID certificate. No reciprocal population tail is claimed as a fixed-input cost.

## Fixed-Input Sampling Bound

There is now a SEPARATE rigorous fixed-input bound for the fresh complete-block
square fits. Unlike the population binomial reference, it requires NO random
public shifts/signs. It still does NOT cover all classical algorithms or the
implemented partial block-exchange repairs. The distinction below is essential.

Let b=floor(K/m), k0=b*m, Q=p^m, and take the ACTUAL fitted code of dimension
k0; unused K-k0 coefficients are0 in this algorithm. Uniform F_p coefficients
make any t<=b blocks jointly uniform by scalar Vandermonde independence.
For arbitrary fixed shifts/signs and ANY chosen block subset S of size t,
the indicator's zero Fourier coefficient is rho and every nonzero coefficient
has magnitude a=sqrt(Q+1)/(2Q). This follows from the retained Gauss phase and
Q3mod4; it is false for the rejected even-degree flat-source substitution.

Expand the joint acceptance probability in coordinatewise F_p Fourier series.
Terms survive averaging over coefficients only if their frequency vector is
in the scalar Vandermonde kernel. On an active support of r blocks, no nonzero
term survives if m*r<=k0. Otherwise there are at most p^(m*r-k0)-1 terms.
All public-shift phases are allowed. Therefore the joint acceptance deviation
from rho^t is at most

```text
sum_(r>b)^t C(t,r)*rho^(t-r)*a^r*(p^(m*r-k0)-1)
 <= p^(-k0) * (rho + sqrt(Q+1)/2)^t.
```

The second expression deliberately includes positive extra terms, so it is a
safe, simpler bound rather than an exact kernel count. For t<=b the error is
EXACTLY0. The software replaces sqrt(Q+1) by its integer CEILING, keeping every
subsequent inequality rational and outward. It does not enumerate subsets or
assume exact high-order independence beyond the MDS range.

Fix any b anchors A. Their acceptance probability is EXACTLY rho^b. Uniform
degree<k0 polynomials conditioned on those b predicates accepting are equivalent
to independent UNIFORM accepted block values followed by the actual native
interpolation: the map from coefficients to anchor values is a bijection.
Let Y count accepting blocks among the remaining N=n-b blocks. For r<=u,
where u=target-b>0, the factorial moment and Markov give

```text
Pr[Y>=u | all anchor predicates accept]
 <= C(N,r)/C(u,r) * [rho^r + Error(b+r)/rho^b].
```

Search integer moment orders with EXACT arithmetic; the saved order is a valid
witness, not an optimality theorem. This is an elementary factorial-moment
method, related to the standard limited-independence tail literature
([Schmidt--Siegel--Srinivasan](https://www.cs.umd.edu/~srin/PDF/ch-bounds.pdf));
the particular character/code conditioning argument above is a local derivation.
The displayed inequalities are derived here; no external tail theorem is needed.

The implemented root-square sampler is uniform on accepted values in STRICT
mode: every nonzero square has exactly2 nonzero roots. INCLUDING ZERO is not
uniform: zero has1 root and each nonzero square2. Its single-anchor TV from
uniform acceptance is (Q-1)/(Q*(Q+1)); a product hybrid adds at most b times
that amount to the tail bound. The implementation pays this correction rather
than silently treating squares as uniform. Full small polynomial/root enumeration
checks joint moments, anchor conditioning, this bias and the actual sampler.

On the fixed p61,m31 inputs, the resulting bounds at targets22/57/114 are:

| Blocks | Target | Moment Order | One Fresh Full Fit Upper | Fits Necessary For 50% Success |
| --- | --- | --- | --- | --- |
|25|22|9|0.044433594|12|
|65|57|23|0.000569869|878|
|127|114|49|8.717424e-9|57356397|

Displayed probabilities are rounded upward; fit counts use the exact saved
dyadic bounds, not the rounded table entries.

These apply uniformly to EVERY legal fixed public input. A union bound, not
independent-success multiplication, gives T times the per-fit upper bound.
The fit-count lower bound is ceil((1/2)/upper), necessary but NOT sufficient.
At127 blocks32 such fits have success upper<=2.789576e-7. The saved quantum
composition now has a separately charged LOWER success bound at the SAME114
target; no inferred binomial quantum distribution is needed.

Adaptive anchor choice can be covered IF every anchor's target/root value is
freshly resampled uniformly conditional on the past. Keeping b-1 FULL anchor
values and resampling only one is different: it conditions on VALUES rather
than only on the accepting predicates. The current block-exchange repair does
exactly that, and is NOT covered. Neither are optimized roots, chosen good seeds,
general norm solvers, or a sampler that uses additional input structure.
The saved deterministic PRNG trajectories are replays, not a law about all seeds.

Consequently this result strengthens the baseline audit on fixed inputs; it
does NOT establish a classical complexity lower bound or a quantum runtime
advantage. It gives a specific reason to pursue a stronger structural solver,
not a justification for declaring all classical attacks exhausted.

## Native Retained-Value Norm-Pencil Attack

The scientific question is whether the actual algebraic predicates permit a
stronger classical completion than fresh square interpolation. The SAME
`folded_norm_attacks.py` now implements one such attack. The input, scalar
degree bound, public shifts/signs and zero convention are unchanged. No
extension-coefficient polynomial, membership oracle or rerolled source is used.

Starting from a native word P0, retain floor((K-1)/m) accepted blocks' FULL
values, when that many are available. Complete these scalar roots to K-1
distinct public evaluation points. Compute over F_p

```text
V(X) = product_(retained scalar points a) (X-a),
P_lambda(X) = P0(X) + lambda*V(X),  lambda in F_p.
```

The degree is still <K. Preserved values are not resampled; the fresh-full-fit
tail bound above DOES NOT apply. Including lambda=0 prevents score regression.
Nonzero equal-score moves are permitted. Each subsequent line is conditioned
on the actual current word, with no asserted independent-score law.

Evaluate P0 and V on the nm public points. For each block form A_i from V's
m coordinates and B_i from P0's coordinates minus the original public shift.
Compile the exact base-field polynomial

```text
F_i(T) = Norm_(E/F_p)(A_i*T+B_i)
       = product_(j=0)^(m-1) [A_i^(p^j)*T+B_i^(p^j)].
```

Every coefficient is checked to descend to F_p; the Frobenius orbits close,
degree is m for A_i!=0, and leading/constant coefficients match the actual
norms. A_i=0 gives a constant, scored once rather than per parameter. Each
candidate parameter is scored by base-field multipoint evaluation and the
Legendre symbol, NOT another extension-field norm. The winning native
polynomial is recomputed and all block flags checked against the compiled
predicates. Tests also use independent Horner/is_square evaluation, and an
independent multiplication-matrix determinant validates norm-polynomial values.
Repeated norm polynomials are allowed; squarefreeness is never assumed.

Setup is a base-field root-product tree plus nm evaluations, n norm-polynomial
compilations (at most2m Frobenius maps and m-1 extension-polynomial products
each), and endpoint norms. A conservative parameter-scoring upper scale is
O(J*n*m) base-field operations plus O(J*n*log p) modular-multiplication work
for Legendre tests; this is not a claim about FLINT's optimal evaluation cost.
Working data include O(K+n*m+J) field/scalar entries, in addition to library
workspace. The replay artifact deliberately retains every round's direction,
norm polynomials, parameter values, scores, winners and high-level operation
counts. Public field setup is shared and recorded, not free advice. No
matched quantum wall-clock/gate comparison is claimed.

The fixed four-round,2048-parameter budget on the EXISTING saved inputs gives:

| Blocks | Basic Fits/Repairs | Native Norm Pencils | Conditional Quantum Mean Floor |
| --- | --- | --- | --- |
|25|21|25|21.132867|
|65|53|57|56.698728|
|127|99|104|113.302668|

All8192 parameter scores per input are retained, including repeated zero
controls and non-improving lines. The25-block instance is perfectly solved;
the65-block instance reaches the saved57 threshold. These finite instances
can no longer be used as evidence that the quantum score is classically
inaccessible. This does NOT refute the quantum algorithm: its mean is a LOWER
bound, costs differ and its full output distribution is not matched. The127-
block word still misses114; a finite search miss is NOT a hardness certificate.
The budgets are deliberately EXPLICIT but NOT MATCHED: the basic attack made96
full interpolation proposals, whereas the new method scored8192 line parameters
after that warm start. Thus score improvement alone cannot be attributed to
better search geometry rather than more scored proposals, or establish a time
improvement. The concrete capability is avoiding a full native interpolation
and extension norm evaluation per parameter. A cost-matched comparison would
be needed before claiming an empirical efficiency advantage. Do not hide the
warm-start cost, constant zero controls or failed rounds in that comparison.

## Fixed-Line Character Correlations And A Counting Certificate

For nonzero A, the norm polynomial is c*g(T)^e, where g is the monic minimal
polynomial of -B/A, d=deg(g) divides m, c=Norm(A), and e=m/d is ODD. This is a
standard finite-field norm identity, not a new algorithm. The implementation
computes a squarefree quotient by gcd(F,F'), checks g irreducible and verifies
the ENTIRE reconstruction F=c*g^e. Here m<p follows from the native distinct-
point geometry, so the derivative does not lose a multiplicity to characteristic.
Equal g's are a single square class; their required character includes chi(c).
Conflicting requirements and failed constant predicates cannot silently pass
an independence check. Incompatible duplicate classes give a zero NONZERO-
pattern lower bound, not an impossibility claim when including-zero is enabled.

For r distinct irreducible classes with consistent orientations, let D be the
sum of their degrees, Z the number of degree-one classes and H=ceil(sqrt(p)).
Every nonempty subset product is squarefree and nonconstant, so the known
quadratic-character Weil bound applies. Expanding the sign indicator gives

```text
N_nonzero_all_good
 >= p/2^r - (D/2 - 1 + 2^(-r))*sqrt(p) - Z
 >= [p - (2^(r-1)*D - 2^r + 1)*H]/2^r - Z.
```

At a root the indicator product can contribute at most1; subtracting all Z
distinct base-field roots is safe. Higher-degree irreducibles have no F_p
roots. Taking the ceiling of this rational lower bound and clipping at0 is
valid because N is an integer. Constant accepted predicates add no classes;
if all predicates are accepted constants, all p parameters work. The saved
certificate records actual square classes, constants, conflicts and setup
costs, not an assumed binomial distribution. Small-field ALL-parameter tests
cover signs, duplicate classes, repeated powers and both zero conventions.
The first25-block line has16 distinct classes and all-good parameter count
at least34809302503912 out of p=2305843009213693951. The65/127 first lines
have40/78 classes and the bound is0 (inconclusive), not nonexistence.

The character-sum bound is known; see the quadratic-character construction in
[Alon--Goldreich--Hastad--Peralta](https://web.math.princeton.edu/~nalon/PDFS/aghp4.pdf).
The norm-specific reduction/count application here is local and review pending.
A positive count is NOT an efficient parameter-finding algorithm. It can
justify a fresh-uniform-parameter success floor on this CHECKED fixed line,
not a probability law for a chosen deterministic seed or general classical
search. A zero lower bound is inconclusive. No novelty or hardness is claimed.

Current literature also reinforces the access distinction: the October2026
[folded-OPI separation](https://arxiv.org/abs/2610.02145v2) uses random sets and
membership oracles. Its classical lower bound cannot be imported into our
explicit arithmetic predicates. Efficient known quantum OPI mechanisms alone
do not establish that this explicit norm family yields a new speedup.

## Uniform Growing Family, Not A Finite-Size Extrapolation

`uniform_family_certificate(p,n)` now checks a closed-form ALL-n arithmetic
argument. It does not evaluate an eigenproblem, enumerate supports, allocate a
large decoder or execute a quantum circuit. Its problem family is explicit:

```text
n >= 3200, n a multiple of100; m=31;
K=62n/5, ell=n/4; p prime, p=3 mod4, p-1 >= 4(31n)^2;
any VERIFIED degree31 field modulus/basis and gamma of order >=31n;
arbitrary FIXED public shifts/signs, either stated zero convention.
```

These are NOT the parameters of the old25/65/127 finite controls, and this
theorem does not retroactively certify those inputs. Both parties receive the
same complete arithmetic input. Irreducibility, trace basis and distinct gamma
powers must actually be verified; a statement about feasible geometry is not
a verification of a supplied field/generator.

### Uniform Collision And Gram Envelope

Put a=ell+1 and g=K-ma. For any source support of j<=a blocks and competitor
support of r<=a, ignoring the favorable shared-support subtraction bounds its
bad fraction by p^(mr-K)*(1-1/Q)^(-j). There are at most2^n competing supports.
Q>=2n and Bernoulli's inequality give (1-1/Q)^(-a)<=2. Consequently

```text
epsilon_a <= 2^(n+1)*p^(-g),  M_a<=2^n,
delta_a <= 2^(2n+1)*p^(-g) <= 2^(2n+1-g).
```

Here g=93n/20-31, so the last exponent is32-53n/20. For EVERY allowed n it
is at most-8448, hence safely at most-64. This bounds the original source too.
The source/herald trace squared is at most2*delta, and the radial Gram mean
error is at most2*delta/(1-delta). The executable proof checks the rational
budgets TV<=1e-8, Gram error<=1e-12 and total source/Gram/herald mean loss<=1e-6.
It represents exponential bounds by their exponents; it never constructs2^n
support entries or an integer with exponentially many bits.

### Decoder And Explicit Radial Witness

Use the IMPLEMENTED known folded decoder, order s=4. With n=100t its decoded
dimension is1860t, C=2800t and D=188t. Its strict root-count margin is52t+1>0.
The pruning agreement gap is(15t+1)/(100t)>3/20 and affine dimension<=3.
Pay8192 independent pruning trials. Exact integer arithmetic verifies

```text
nu <= (1-(3/20)^3)^8192 = (7973/8000)^8192 < 1e-12;
2*sqrt(2^-64+nu) < 1e-5.
```

Choose weights1 on the32 spheres j=ell-31,...,ell and0 elsewhere. This is an
explicit state, not a numerical top eigenvector or optimality claim. For each
adjacent pair, (j+1)(n-j)/n^2 >=231/1280, whose square root exceeds531/1250.
For either zero policy Q>=1000 ensures diagonal>=999/2000 and
2sqrt(rho(1-rho))>=999/1000. Thus its ambient normalized Rayleigh mean is at least

```text
999/2000 + (31/32)*(999/1000)*(531/1250)
 = 36424539/40000000 = 0.910613475.
```

After source loss1e-6, decoder loss1e-5 and an ADDITIONAL TOTAL full-flagged
synthesis trace budget<=1e-3, the per-attempt mean is at least
36384099/40000000=0.909602475, safely above0.909. All failures score0.
Using only integer score support0..n, not a binomial assumption, gives

```text
Pr[score >= 9n/10] >= 9/100.
```

This is a CONDITIONAL COMPOSITIONAL statement: the specified mathematical
source/receiver must be implemented within the stated TOTAL synthesis budget.
The arithmetic checker does not verify an implementation's trace error,
prepare a3200/1e6-block state or run its huge dense decoder. Its emitted3200
and1e6 records are ANALYTIC certificates, not live algorithm-success samples.
The large-size example at n=1e12 in tests checks arithmetic compactness only.
The current finite decoder also has a4096-block implementation guard; these
arithmetic records do not bypass it. Removing a guard would not supply a
compiled circuit or make a huge dense allocation a meaningful experiment.
No classical lower bound, matched runtime advantage or new algorithm follows.

### Concrete Source-Preparation Simplification

For xi!=0, the local unit phase after removing the public shift phase is

```text
u(xi) = [eta+c(xi)*tau_E]/sqrt(Q+1),
c(xi)=sigma*chi_E(-lambda), eta=+/-1, tau_E=+/-i*sqrt(Q).
```

Replace it by v(xi)=c(xi)*tau_E/sqrt(Q), RETAINING the COMPUTED Gauss unit on
EVERY active block. With uniform nonzero E labels, chi has equal positive and
negative populations, so <v|u>=sqrt(Q/(Q+1)), real and positive, for either eta.
For any unchanged support/radial superposition of weight<=ell, its overlap is
a convex combination of powers of this quantity. Hence

```text
source pure trace distance^2
 <= 1-(Q/(Q+1))^ell <= ell/(Q+1).
```

The same full-flagged receiver cannot increase this trace distance. Conditional
postselection can amplify it, so failure flags must NOT be dropped. This
improves on a loose ell-times-local-error hybrid bound. It is a simple local
approximation lemma, not a novelty or speedup claim. Uniform independent
nonzero labels conditional on support are ESSENTIAL; arbitrary correlated
label amplitudes need not have the cancelling character average.

The approximate source uses uniform nonzero labels, a controlled sign and the
Gauss quarter-turn, plus the SAME public trace/additive phase. No tiny arctan
rotation for the eta term is needed. Equivalently, this is the EXACT normalized
Fourier source for the ternary character sigma*chi_E(z); only its comparison
with the binary accepting-indicator contrast is approximate. Its error must fit WITHIN, not on top of,
the total1e-3 synthesis budget. The support state is explicitly a uniform
superposition of32 controlled Dicke states; count weight from support to erase
the weight register, and compute nonzero labels to erase support scratch.
Finite-interval label preparation and base-p conversion have polynomial bit
cost; no Q-entry amplitude table is allowed. Field characters are computed
by the actual norm and modular exponentiation. Fourier/remaining rotations
still need their own approximation accounting.

Independent controls enumerate all729 two-block error labels with COMPLEX
radial weights and verify the overlap for both zero policies. Removing the
per-active Gauss unit instead gives trace squared>0.5, violating the claimed
small bound. Existing full p7,m3,n2 syndrome/herald/native-Fourier controls also
verify full success/failure flagged contraction; their source trace squared
is about0.001454 and flagged trace about0.034092. Wrong prime +i remains wrong.

### Resources, Literature And Falsifiers

At fixed m31,s4, the known decoder has polynomial reversible upper scale
O((31n)^3+8192*(31n)^2)*poly(log p), NOT a physical gate or memory estimate.
Public generator selection is not a hidden oracle: fewer than L^2/2 elements
have order<L, L=31n, while p-1>=4L^2, so a fresh uniform gamma fails with
probability<1/8; test its first L powers directly. This proves no property of
a fixed PRNG seed. Field construction/validation and trace-dual work are paid
separately. A valid public representation is input data, not a secret field
table. Exact zero synthesis budget is an IDEAL limit, not a finite gate claim.
Public shifts/signs can be compiled as constants on their explicit block
registers; this statement assumes no unit-cost QRAM or unknown data-loading
oracle. Native syndrome and decoding arithmetic must likewise be charged.

State-preparation ingredients are standard, including
[controlled symmetric/Dicke preparation](https://arxiv.org/abs/1904.07358).
They support polynomial existence/upper-scale arguments, not a supplied compiled
circuit. This application reuses known DQI/FRS ideas and is NOT claimed novel.

The current classical baseline is still the actual native interpolation,
repair and norm-pencil code, not generic MQ hardness. Two literature transfers
were checked and do not solve this optimization task as stated:

- [Kopparty's character decoder](https://arxiv.org/html/2601.07137v1), Theorem1,
  takes a received word on ALL q field elements and runs poly(q), not poly(log q).
  Our arbitrary prescribed signs at n points are not that received word, and
  a recovered unconstrained norm polynomial need not lift to original F_p
  coefficients. This does not exclude adapting its pseudopolynomial ideas.
- [Ivanyos--Santha](https://arxiv.org/html/1503.09016v2), Proposition9, gives
  a homogeneous DIAGONAL quadratic solver with (r+1)^2 variables for r equations.
  Our affine, base-field descended system is not automatically diagonal over
  F_p and has only a constant variable/equation ratio at the target rate.
  The theorem cannot simply be imported; its failure to apply is not hardness.

Falsifiers remain actual source/circuit error exceeding its budget, wrong
scalar rank/domain/Gauss phase, an invalid interpolation/pruning argument, a
stronger classical polynomial solver, or prior-art subsumption. The primary
scientific unknown is still coupled native square completion or a meaningful
natural application/reduction. Do not respond with more finite seed meshes,
automatic candidate admission or another conditional bridge taxonomy.

## Next Decisive Questions / Stop Rules

The implemented attacks are NOT sufficient to justify a speedup claim. A native
one-parameter norm attack now EXISTS; it is not a general global completion
solver. Highest priority is exploiting the coupled quadratic/norm system beyond
retained-value lines, or a meaningful natural reduction/application. Rewriting
Z_i(P)=a_i*V_i^2 gives an explicit structured quadratic system over F_p, with
many free variables; generic MQ hardness cannot be imported. An apparently
perfect E-coefficient polynomial is not a valid F_p solution.

Kill the claimed advantage if a polynomial classical completion covers its
target regime, if the scalar/block rank or field domain changes, if a source
phase is omitted, or if charging reversible decoding/precision removes the
comparison. Do not promote a seed sample, a conditional mean, these basic
baselines, or absence of a literature hit to novelty. Do not spend the next
pass polishing dashboards or adding named bridges around this route.
