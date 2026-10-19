# Local Resampling Removes The Field-Size Logarithm

Status: executed classical Moser-Tardos application and explicit local proof;
independent research review pending. No novelty, quantum speedup or prescribed
sampling claim. This changes the ROUNDING mechanism rather than searching
smaller-mass waveforms, whose previous certificate limit remains valid.

## Scientific Claim And Input Model

Given an ACTUALLY constructed and verified sparse prime translation frame of
moment order ell, classical interval search has an all-target expected-polynomial
algorithm at width O(sqrt(ell log ell)) for the current norm-O(ell) families.
This improves the field-dependent O(sqrt(ell log p)) certificate when p is
large relative to the support. It does NOT supply a missing public frame.

Input remains prime p, explicit block length N=p, native H_d[j,x]=x^j,
d<=ell, arbitrary fixed public word/syndrome, centered interval[-u,u]. The
split, nonsplit and completed divisor-free fiber constructions can provide
frames. All setup, exact rational coordinates, coin bit lengths and verification
costs are paid. Nothing is polynomial in log p alone or applicable to the old
N127,p=2^61-1 punctured input by changing N silently.

## Why Naive Local Resampling Would Fail

The constant basis row touches EVERY output coordinate. If its coefficient
were a shared random variable, the bad-event dependency graph could be complete,
destroying the proposed logarithmic improvement. The implementation instead
fixes its coordinate by exact nearest rounding BEFORE sampling the other rows.
This coefficient is never resampled. Its residual mean offset delta0 has
absolute value<=1/2 and is explicitly paid in the tail bound.

Fix any public y. Its rational coordinates alpha are deterministic functions
of y. The OTHER floor/ceil coins are independent product variables even though
their biases depend on that fixed y. No independence of the coordinates as
functions of a random y is required. All following guarantees are conditional
on each fixed target, hence uniform over targets.

## Correct Event Probabilities And Dependencies

Write B_0=ones and B_(t+1)(x)=w(x-t), t0..p-2, with s nonzero waveform entries
and S=sum(w^2). After fixing z0 nearest, the raw coordinate is

```text
e_raw[x] = delta0 + sum_(i>=1)(alpha_i-z_i)*B_i[x].
```

The sum is centered and its total squared range is at most S. Raw residuals
are INTEGERS. A bad centered output implies a raw magnitude at least u+1,
so a centered sum magnitude at least u+1/2. Hoeffding therefore gives

```text
Pr[bad_x] <= min(1, 2 exp(-(2u+1)^2/(2S))).
```

Using u+1 as a mean-zero threshold after fixing z0 would be unjustified.
Tests exhaust nonuniform coins and show the actual mean equals delta0, not0.
Modular centering only makes the bad event smaller.

An event depends on at most s NONCONSTANT variables, each occurring in at
most s events. A dependency-degree bound is

```text
L = min(p-1, s*(s-1)).
```

The software computes the actual variable set for coordinate x from its row
support, excluding the omitted translate and global constant. It never assumes
that disjoint random variables can still be correlated through resampling;
Moser-Tardos explicitly supplies the theorem for these product variables.

## Exact Local Lemma Certificate

Put E=floor((2u+1)^2/(2S)) and q=min(1,2/2^E), using exp(1)>2. The full
interval is directly assigned q0. Choose x=1/(L+1). The elementary bound
`(L/(L+1))^L > 1/3` implies

```text
x*(1-x)^L > 1/(3*(L+1)).
```

Thus the EXACT rational sufficient condition is `q<=1/(3*(L+1))`.
It yields the Moser-Tardos event condition for every target. Their Theorem1.2
then gives expected total resampling steps <=p/L. A finite budget B has the
conservative ideal-coin Markov failure bound min(1,p/(L*B)). These are theorem
bounds under fresh independent exact coins, NOT confidence from a seeded PRNG.
At huge analytic N a fixed default budget can have a vacuous Markov bound;
the report does not claim those inputs were executed or solved within it.

Choosing E_req=ceil(log2(6*(L+1))) and the smallest integer u with
`(2u+1)^2>=2*S*E_req` certifies the condition. The code uses only integer
bit lengths and square roots. For current frames s=O(ell), S=O(ell), so

```text
u = O(sqrt(ell log ell)), independent of p once p exceeds the dependency bound.
```

This beats the earlier nearest radiusell asymptotically without contradicting
its L1-mass lower bound: resampling creates a COUPLED final assignment, not
independent nearest choices or a claim of smaller waveform variance.

The inherited theorem is
[Moser-Tardos2009, Theorem1.2](https://arxiv.org/abs/0903.0544).
Their deterministic variant requires additional bounded-degree hypotheses;
we do NOT infer a uniform deterministic algorithm at growing ell from it.
The specific RS frame, fixed-constant reduction and bounds above are local
applications requiring independent review, not novelty claims.

## Exact Fixed-Target Certificates

The same producer now computes exact probabilities for each modular bad event
on the ORIGINAL public target. This is a stronger instance-specific analysis,
not a smaller all-target radius. No target or seed is selected by the certifier.
The independent all-target certificate above remains a separate artifact.

For each coordinate x, write alpha_i=floor_i+r_i/D and fix z0 nearest as above.
With B_i[x]=w(x-i+1), the INTEGER residual is

```text
b_x - T_x,  b_x = y[x] - z0 - sum_(i>=1) floor_i*B_i[x],
T_x = sum_(i>=1) Bernoulli(r_i/D)*B_i[x].
```

An integer-weighted dynamic program accumulates the mass of T_x. Each active
coin contributes integer weights D-r_i at0 and r_i at B_i[x]. Its denominator
is D^k after k coins; normalization is checked EXACTLY. Zero-remainder coins
are deterministic and removed. Sum masses only where the MODULAR CENTERED
value of b_x-T_x lies outside the requested interval; a raw tail would be a
different event. Negative and multiplicity2 coefficients are retained.

The DP's integer span is at most sum(abs(w)), so it has at most L1+1 states,
not2^s assignments. The bit length of its unreduced denominator is O(s log D).
This is pseudo-polynomial in waveform L1, polynomial for the CURRENT bounded
frames; it is not a polynomial-in-log-weight solver for arbitrary integer rows.
Public setup/inversion, probability computation, dependency construction,
rational products and the original solver work are all charged.

Remove probability-zero events, then construct dependency edges from shared
NONDETERMINISTIC coin indices. Round each computed exact probability UP to a
128-bit dyadic bound q_i. Try x_i=2*q_i, then a symmetric witness based on the
ACTUAL dependency degree. Admission checks every rational inequality

```text
q_i <= x_i * product_(j neighbouring i)(1-x_j),  0 < x_i < 1.
```

These witnesses are only two sufficient choices. Failure means neither was
certified, NOT that no Local Lemma witness exists or that the problem is hard.
For an admitted certificate, expected total resamplings are at most
sum_i x_i/(1-x_i); Markov bounds use the DECLARED budget. The solver still
resamples every variable in its support list, including harmless deterministic
ones; those extra draws change no random variable or event dependency.

Saved event upper bounds and LLL witnesses allow exact inequality replay.
An input digest binds p,d,ell,u,word,waveform; a separate digest identifies
the exact probability vector. A digest alone is NOT verification: the source
and original target must be replayed. The saved maximum marginal remains an
exact rational; probability bounds are explicitly labeled as outward dyadics.

Executed same-target controls at p347,d8:

- u5 is certified, although the conservative UNIFORM radius is9. Maximum
  event probability is about0.00170345; actual dependency degree106 versus
  the support-only upper bound240. Expected resamplings<=0.263767 and ideal
  failure within128 resamplings<=0.00206068. The replay needs0 resamplings.
- u3 still has NO certificate from the implemented witnesses. Its16-step
  successful replay is retained, with null expected-runtime/probability claims.
- A deliberately forced positive-mass p11,d3,u2 coin transcript exercises a
  real violated-event resampling on a CERTIFIED instance. It is a replay test,
  not an empirical estimate of the probability law.

Independent full-product enumeration at p11 agrees with every computed event
probability, including weighted rows, nonuniform coins, negative coefficients,
modular wrap and the full interval. A heterogeneous p11 example passes the
asymmetric condition even though substituting its maximum marginal into the
degree-based symmetric condition fails.

Further local tail/witness tuning is NOT the priority: it does not remove the
missing public-frame construction at larger degrees/rough primes, or supply
the punctured large-field receiver. No new speedup candidate is created.

## Current Literature And Scope Review

Checked2026-10-19: Chailloux--Tillich v2 (9 Mar2026), Problems6--8, still
uses full support N=q. This matches the present prime N=p search task.
Their uniform-interval fourth-moment condition is a sufficient QUANTUM search
condition, not a sampling guarantee delivered by the classical attack.

[Sun--Wootters2026](https://arxiv.org/html/2610.12357), Theorem1.8, gives
QUANTUM worst-case OPI algorithms; Theorems1.10/1.11 give existential results.
It must NOT be cited as a blanket classical OPI algorithm. Its Theorem1.12
membership-oracle separation uses a large field relative to n; the present
explicit full-field construction and runtime do not apply in that input model.
Known fixed-gap classical RS decoding or special structured-list attacks must
be justified separately. This review finds no mismatch in the local MT
application, but is not external peer review or a novelty assessment.

## Executed Algorithm And Costs

Run `python theorems/interval_local_lemma.py --write`.

1. Construct or receive the charged verified public frame; recompute its
   support, norm and native moments. Compute and reconstruct exact coordinates.
2. Fix the constant nearest; sample all nonconstant Bernoulli remainders using
   the ACTUAL common denominator, never merely the field modulus.
3. Select the smallest bad coordinate. Resample exactly its local variables,
   from the same exact coin laws, without changing y or the constant.
4. Update affected columns, directly recheck original modular equations,
   retain every step and stop only at a verified witness or the declared budget.
5. Independently reconstruct the complete raw residual, bad-coordinate set and
   RS value polynomial; check it at all field points before accepting output.

Every resampling uses <=s fresh coins and <=s^2 local integer updates. The
implementation additionally PAYS for O(p*d) full modular checks and event
bookkeeping per step; this is not advertised as a free local operation.
Coordinate numerator/denominator bits remain polynomial by the earlier cofactor
bound. The actual exact coin count and full replayable resampling transcript
are saved. Distribution after resampling is not promised to be the ideal
uniform or weighted coset distribution.

## Native Controls Versus Analytic Certificates

|p|ell=d|certified radius|native word norm|resampling steps|
|---:|---:|---:|---:|---:|
|347|8|9|5|0|
|1019|16|14|8|0|
|2017|32|21|13|0|

The small certified controls do NOT all improve the best previous radius:
nearest gives8 in the first case, and the global independent bound can give20
in the third. The contribution is the field-size-independent theorem and the
actual resampling implementation, not cherry-picked finite benchmarks.

An aggressive p347,ell8,u3 run executes16 real resamplings and returns a
verified norm3 word. Its Local Lemma criterion is INCONCLUSIVE; the expected-
time and budget probability fields remain null. A budget1 replay stays failed.
Neither success nor failure outside the criterion becomes a uniform theorem
or hardness result. Tests independently replay every variable change, affected
column, coin denominator and native equation through all16 steps.

Three records are ANALYTIC ONLY, with NO full field frame or native target run:

|prime|ell|certified radius|public-frame condition|
|---|---:|---:|---|
|2^31-1|64|33|proper nonsplit divisor of p+1|
|2^61-1|256|73|proper nonsplit divisor of p+1|
|2^127-1|32|22|positive divisor-free Weil setup bound|

The p=2^61-1 entry has block length N=2^61-1, NOT127. It is a mathematical
parameter certificate, not practical cryptanalysis or a quantum execution.
For d=ell256, its classical radius73 is below the necessary u threshold from
the earlier soft-profile ceiling d<2u+1. More generally u=o(d) when ell=Theta(d)
grows. Thus, wherever the public-frame construction applies, sufficiently
large such regimes cannot support a SEARCH advantage based only on those
soft-profile certificates. This does not settle arbitrary rates/moduli/sets,
prescribed sampling, punctured inputs or all quantum algorithms.

## Self-Critique And Next Experiment

Verification milestone:10 focused checks and259 connected tests INCLUDING
those10 pass, the connected command taking72.21s with RuntimeWarning as error.
This is not full-repository coverage. All four live producers' source/dependency
hashes, eight strict JSON files, Python/source-test compilation, site JavaScript
syntax and registry validation pass. No central claim promotion or Git commit.

- A random global constant would restore a complete dependency graph. Tests
  explicitly show that countercontrol; coefficient0 is fixed in every transcript.
- Nonuniform target-dependent coin biases are legal only with independent fresh
  draws conditional on the fixed target. Exact small product laws and a tracking
  coin source verify the implementation, not the ideal independence premise.
- Sparse support is not enough if range magnitudes are undercounted. Both
  support and squared weights are revalidated, including multiplicity2 frames.
- Finite PRNG success is not a theorem, and an uncertified aggressive run does
  not receive an expected-polynomial label. Budget exhaustion never means ISIS
  hardness. The resulting search distribution is not a faithful quantum sampler.
- Missing public setup remains missing. The uniform low-degree Weil criterion
  and divisor restrictions on the explicit torus families are not erased by LLL.
- Literature and independent expert review may show this application is known,
  or reveal a scope error. No new quantum algorithm has been discovered.

The next decisive capability is exact Poisson-binomial event probability
evaluation on the ORIGINAL target. Local events involve only s integer-weighted
Bernoullis, so a polynomial-range dynamic program can give exact rational
probabilities, potentially replacing conservative Hoeffding bounds in a
verified local-lemma certificate. This should be a real stronger classical
attack, not another seed grid or a free discrepancy oracle. Alternatively
compare independent quantum source/decoder families once this comparator stops
removing a specific remaining scientific blocker.
