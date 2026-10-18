# Conjugate-Chirp Repair: Constructive Erasure, Wrong Target

2026-10-17. Local derivations REVIEW PENDING, using explicit external
exponential-sum bounds. No novelty, quantum speedup or general no-go claim.
Producer: `python theorems/conjugate_chirp_repair.py --write`.
Report: `classical_baselines/conjugate_chirp_repair.json`.

## Question, Input And Intended Upside

Can a conjugate quadratic-phase register remove the failed preparation step
in quadratic DQI without losing its original nonlinear optimization target?
Input is an odd prime p, public symmetric forms C_i, and explicit lists F_i;
maximize the number of `x^T C_i x in F_i`. These controls use prescribed
Vandermonde forms and supplied public lists, not generated hard oracles.
A polynomial same-target preparation with strong classical competitors
would be interesting. It is an aspiration, not an established advantage.

The [author's correction to quadratic DQI](https://arxiv.org/html/2510.08061)
explicitly invalidates its preparation algorithm/Theorem1. The score analysis
alone does not provide the missing state preparation. This pass tests a NEW
local repair proposal, not a further refutation of that corrected paper.

## Proposed Constructive Mechanism

Start from normalized sparse-error amplitudes c_y, let C_y=sum_i y_i*C_i,
and prepare TWO controlled chirps while the public error label is available:

    sum_y c_y |y>|chi(C_y)>|chi(-C_y)>.

This is legal controlled preparation, not cloning/conjugating an unknown
state. With r=x-z, u=x+z (a bijection in odd characteristic),

    x^T C_y x-z^T C_y z = u^T C_y r.

The negative-sign QFT on u then produces `|r>|C_y*r>` with uniform r.
If B_r has columns C_i*r and a PUBLIC efficient sparse-error decoder, one
can compute y from(r,B_r*y), subtract it, and uncompute scratch. No true y
is an argument to the decoder. Outside its promise the subtraction still
extends to a permutation; it must not secretly choose a map using the label.

Two concrete families supply a scaled Vandermonde B_r:

- Diagonal C_i=diag(1,a_i,...,a_i^(n-1)): B_r=diag(r)*V. Require all r_j!=0.
- Rank-one C_i=v_i*v_i^T: B_r=V*diag(R(a_i)). Require every R(a_i)!=0.

The code implements an actual WEIGHT<=1 decoder: after the public scaling,
the syndrome s has a_i=s_1/s_0, then its nonzero coefficient is recovered and
every remaining moment checked. It neither scans the field nor receives
the true error. Higher weights can use the corresponding classical GRS
decoder, but that decoder and reversible arithmetic are NOT compiled here.

The reference executes literal pair phases, the coordinate permutation,
QFT, whole-error-register reversible subtraction, inverse QFT, all work
labels and charged good-r projection. It verifies amplitudes, not just means.
Six predeclared controls cover both families at(p,n)=(5,2),(7,2),(5,3), with
the same fixed rational weights3/5,4/5. These are physical calibrations, not
putative hard instances or optimized demonstrations.

## What The Receiver Actually Prepares

The erased output has amplitudes proportional to

    P(sum_i g_i(u^T C_i r)),

NOT `P(sum_i g_i(x^T C_i x))`. The extra register cannot be ignored as clean
scratch. Native x-marginal purities range0.074..0.201, and fidelity with the
intended pure quadratic target ranges0.112..0.323 on these controls. This
falsifies SAME-STATE preparation, not every possible optimization heuristic.
Actual original-objective scores are also retained: some finite means beat
uniform and some do not. Low fidelity alone is not a performance no-go.

For diagonal forms, the reversible change q_j=u_j*r_j gives EXACTLY a known
ordinary linear-DQI output, tensor a uniform public nonzero r. Its native
purity is1 within numerical error. The coefficients q_j are unrestricted;
60%..75% of the saved q outputs contain nonsquares. Interpreting q as the
original squared coefficients is invalid. Reporting x instead is feasible,
but gives the different distribution and measured objective retained here.
No claim that the original quadratic problem is generally easy follows.

For rank-one forms, conditioning r gives ordinary linear OPI with scaled
lists. Even the ORIGINAL rank-one constraints absorb into local predicates:
`F_i((v_i*x)^2)` equals `F'_i(v_i*x)` with `F'_i={t:t^2 in F_i}`. These forms
were not a genuinely new quadratic-DQI test. This is an exact representation
reduction, not a general classical solver or a claim about arbitrary forms.

## Diagonal Heuristic: Uniform Expected-Score Falsifier

After the q change, ANY input q distribution is followed by independent
uniform r_j in Fp* and

    x_j=(r_j+q_j/r_j)/2.

For nonzero b, its one-coordinate characteristic is

    E_r e_p(b*x_j^2)
      = e_p(b*q_j/2)/(p-1) * sum_(r!=0) e_p(b*r^2/4+b*q_j^2/(4*r^2)).

Substitute z=r^2, with multiplicity1+chi(z). The numerator splits into a
Kloosterman sum K(A,B) and a Salie sum S(A,B), A=b/4!=0, B=b*q_j^2/4.
The standard Weil bound gives |K|<=2*sqrt(p); the quadratic Gauss identity
gives |S|<=2*sqrt(p), including the B=0 control. The Kloosterman statement
is an EXTERNAL theorem, not formally verified in this repo; see
[Kowalski's authored notes](https://people.math.ethz.ch/~kowalski/elements.pdf).
Gauss/Salie definitions and evaluation are also in his
[exponential-sum notes](https://people.math.ethz.ch/~kowalski/exponential-sums-elementary.pdf).

For completeness, for B!=0 the Salie identity is
`S(A,B)=G*chi(B)*sum_(v^2=4AB) e_p(v)`, |G|=sqrt(p).
Fourier-transforming both sides in A proves it by completing the square;
for B=0 use S(A,0)=chi(A)*G. Native tests exhaust small primes in BOTH
residue classes modulo4, including q_j=0, all nonzero b and zero B.

Thus every nontrivial coordinate characteristic is at most
`eta=min(1,4*sqrt(p)/(p-1))`, uniformly in q_j. For each original diagonal
constraint ALL coefficients a_i^j are nonzero. Independence gives eta^n.
Fourier inversion and Parseval/Cauchy for an arbitrary list of density rho
give the conditional bound, uniform over EVERY q:

    |Pr_r[x^T C_i x in F_i]-rho|
       <= sqrt((p-1)*rho*(1-rho))*eta^n.

Mixing over any quantum-produced q does not weaken it. This statement is
about the computational-basis x output after discarding z. The FULL paired
quantum state still retains coherence; a different coherent joint readout
is not modeled as a classical channel or excluded by this argument.
Meanwhile the
CLASSICAL algorithm sampling uniform x has the same bound with eta replaced
by1/sqrt(p), from quadratic Gauss sums. Consequently the paired receiver's
EXPECTED satisfied-fraction advantage over this legal classical baseline
vanishes rapidly as p,n grow. This holds regardless of the input DQI shell
degree, weights or q distribution, for THIS specified randomization/readout.

The code outward-rounds square roots using integers and stores exact rational
bounds. At p101,n16 the expectation advantage bound is already below10^-4;
larger symbolic controls are smaller. Independent INTEGER convolutions check
the full scalar laws at n16 for several fixed q vectors without a101^32
statevector. These are not new quantum runs. This mean argument alone bounds neither score tails
nor full-output TV, other readouts, zero-pattern forms, or all quantum
algorithms. A zero evaluation point would break the all-coefficients-nonzero
premise and is explicitly rejected by the input schema.

## Separate Tail Falsifier For The Same Diagonal Readout

Do not infer a tail no-go from the preceding mean. A SEPARATE joint-moment
argument addresses the rare-good-output loophole for this specific receiver.
For a nonzero additive frequency on k distinct constraints, coordinate j has
coefficient `b_j=sum_i t_i*a_i^j`. A nonzero k-term exponential sequence
cannot have k consecutive zeros: the corresponding Vandermonde block is
invertible, with nonzero column factors a_i^start. Thus at least floor(n/k)
coordinates have nonzero frequency. Smaller frequency support only improves
this count. Independence and Fourier Cauchy give, for any k indicators,

    |E product(I_i)-product(rho_i)|
       <= delta_k=min(1,ceil(sqrt(p))^k*eta^floor(n/k)).

This holds for every fixed q and hence every input q distribution. The
delta bound is nondecreasing with k, so it also covers all smaller subsets.
Let k=2s, S=sum_i I_i, mu=sum_i rho_i. Expand the centered kth moment into
ordered products. Repeated Bernoulli factors reduce to `a*I_i+b` with
`|a|+|b|<=2`. There are m^k ordered terms, giving comparison error at most
`(2m)^k*delta_k` from the independent Bernoulli reference.

For that reference, Jensen symmetrization with an independent copy gives
`E(S-mu)^(2s) <= E(S-S')^(2s)`. Conditional on their magnitudes, the independent
differences are signed0/1 Rademachers. Coefficientwise
`cosh(t)<=exp(t^2/2)` bounds their even moment by `(2s-1)!!*m^s`.
Markov therefore gives the SEPARATE certificate, for fixed Delta>0,

    Pr[S/m >= mean(rho_i)+Delta]
      <= (2s-1)!!/(Delta^(2s)*m^s) + (2/Delta)^(2s)*delta_(2s).

The report stores each exact rational contribution, not a fitted exponent.
The n1024,m2048,p65537,Delta1/5,order16 control gives an upper bound below10^-6
without constructing a statevector. Native small-field full joint characters,
Vandermonde zero blocks and independent centered moments are checked separately.

At fixed rate m=Theta(n), p>=m+1, and log p polynomially bounded in n, arbitrary
fixed s makes constant-gap success negligible against any fixed polynomial
repetition budget. This is a scoped falsifier for THIS diagonal paired
randomization with fresh independent uniform nonzero r. It is not full-output
TV, a noncommuting-form theorem, a statement about all quadratic algorithms,
or an extrapolation from the mean alone. The local derivation and external
Weil dependency remain REVIEW PENDING. If log p is superpolynomial in n,
negligibility in n must not be relabeled negligibility in total input length.
The symbolic generator caps s at32; the arbitrary-fixed-s asymptotic statement
is the written derivation, not an inference from finitely many saved controls.

## Projecting The Extra Register To Zero Does Not Repair Efficiency

Setting z=0 recovers the intended amplitudes only on the remaining good-x
restriction. For normalized shell weights through degree ell, if |g_i|<=A,
Cauchy gives

    |P|^2 <= H=sum_(k<=ell) binom(m,k)*A^(2k).

The charged z=0 probability is at most H/p^n. The good-r normalization
cancels because at z0 only the corresponding good x remain. All six native
probabilities are checked against this rational bound. In fixed-rate regimes
m=Theta(n), bounded list densities and p>=m+1, H<=exp(O(n)) but p^n grows as
exp(Omega(n log n)). Straight repetitions are therefore not polynomial for
this repair. The exact general-degree bound does NOT assume a compiled
higher-weight decoder. It is not a lower bound on other state preparations.

## Resources, Failure Decision And Next Science

The mathematical mechanism uses2n field registers plus the error/scratch
registers, public field arithmetic, two controlled phases and a reversible
decoder. Diagonal good-r probability is exactly((p-1)/p)^n; rank-one rejection
must also be charged. The implementation's tables and statevectors are
EXPONENTIAL calibration, explicitly capped. Fourier input preparation,
reversible decoder compilation, precision, inverses, failed preparations and
repetitions are not silently counted as an efficient hardware implementation.

REJECT this proposal as a same-target quadratic-DQI repair. Retain the
constructive bilinear isometry/decoder as a known-mechanism reference and
its exact reductions. No central accepted candidate, proof-status promotion
or broad negative is created. The mean and separate joint-moment bounds are
local review-pending applications of standard exponential sums, not a new
general impossibility.

Do not compile more decoder weights or run larger versions of this semantic
mismatch. Re-entry requires a concrete public operation preserving the
single-register objective with polynomial charged success, or an independent
constructive mechanism. Neither a missing decoder nor another nearby barrier
is itself the next algorithm.
