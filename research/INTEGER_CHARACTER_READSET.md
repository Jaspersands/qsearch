# Candidate Read-Set And Classical Scaling

## Question And Decision

Does the successful 65-branch classical attack already explain the
uniform quantum near-vector guarantee? No such conclusion is justified.
The frozen native threshold remains CLASSICALLY matched, but that is a
different statement from an asymptotic algorithm.

The saved basis has 834 leading integer-coordinate directions and a
190-dimensional core. Inspection of the actual exact rounding code shows
that its list of 65 scalar assignments depends only on those 190 target
coordinates. All 1024 coordinates are still scored when choosing the winner.
This distinction permits a conditional scaling test.

This note applies standard concentration, not a new quantum mechanism or
a lower bound against all classical algorithms. It adds no circuit search,
new candidate, claim admission, UI, or generic research infrastructure.
The bound is about input dependence, not the computational model: it
would also constrain a quantum factory with the same ignored coordinates.

## Explicit Model

Fix an even N and public integer labels a_1,...,a_m. The target coordinates
c_i are independently uniform modulo N. A scalar x has normalized score

```
D(x,c) = (1/m) sum_i (center_N(a_i*x-c_i)/N)^2.
```

Let I be a fixed set of r coordinates. Conditional on all coordinates
outside I and on random coins independent of the target, the algorithm
constructs a list of at most K scalars which does NOT depend on c_I.
The final selector may inspect the complete target to rank this list.

The condition concerns the entire possible list, not merely the number
of candidates visited by an adaptive algorithm. The labels, basis and I
may depend on public instance parameters, but not on c_I.

There is no hidden oracle restriction here: this is a structural property
of one implementation on an explicit input. Other classical algorithms
are allowed to use the complete target and need not satisfy it.

## Conditional Bound

For a fixed candidate and an unread coordinate, translation by a_i*x
permutes the uniform residues, even when a_i is a nonunit or zero.
The normalized squared residual X_i lies in [0,1/4] and has exact mean

```
mu_N = 1/12 + 1/(6*N^2) >= 1/12.
```

The residue convention is -N/2,...,N/2-1; summing their squares proves
the formula. Independent target coordinates give independent X_i after
conditioning on the read coordinates and random coins.

If D<=tau, then sum_(i in I) X_i<=m*tau, since all remaining terms are
nonnegative. For delta=mu_N-m*tau/r>0, the lower-tail inequality gives

```
Pr[any candidate succeeds] <= min(1, K*exp(-32*r*delta^2)).
```

No independence between different candidates is used; the final step
is a union bound. If r=0 or delta<=0, this argument gives only 1.

For completeness, the concentration constant follows directly from the
moment generating function. For a centered variable Y in an interval of
length 1/4, the second derivative of log E exp(lambda*Y) is a variance
under an exponentially tilted law. That variance is at most (1/4)^2/4,
because the support does not change. Integrating twice gives
log E exp(lambda*Y)<=lambda^2/128. Applying this to the independent
negative deviations and minimizing at lambda=64*delta gives the exponent
32*r*delta^2. This is the standard bounded-variable method associated with
[Hoeffding's inequality](https://doi.org/10.1080/01621459.1963.10500830),
not a new concentration theorem.

The implementation avoids floating probability calculations:
exp(-E)<=1/(1+E) and exp(-E)<=2^(-floor(E)). It takes the minimum of those
upper bounds after multiplying by K and clamping to 1. A recorded 4096-bit
exponent cap only weakens the bound; it never rounds a positive bound to
zero. Contract conditions are written assumptions, not automatically
verified information-flow properties.

## Actual Babai Read-Set

After permuting coordinates, the saved numerator basis has the form

```
B = [N*D  0]
    [ C   E],
```

where D is a diagonal sign matrix of size r. The core nearest-plane
coefficients depend only on the projected target c_J and E. The bounded
last-plane offsets are fixed before evaluating their scores.

Changing c_I therefore changes only the prefix integer-rounding
coefficients. Those rows are multiples of N coordinate vectors and
cannot change the scalar assignment modulo N. Thus every scalar in the
fixed list is unchanged by a change in c_I, although its full score and
the winning index can change. Tests check this with signed/permuted rows
and with the coordinate carrying a_1=1 inside the eliminated prefix.

At the saved native parameters m=1024, r=834 and K=65, the certified
probability upper bound is exactly 1: it is VACUOUS. The exact witness
D=0.06266165019 remains a valid classical threshold success.

The native branch radius was selected after observing ordinary Babai's
miss and the basis profile. It is not a held-out campaign. To use this
population statement in a future experiment, freeze the factory and its
hyperparameters before drawing fresh target vectors. The bound is not a
p-value or a success probability assigned to the already fixed seed.

## What Would Follow Asymptotically

At tau=13/200, if a fixed fraction more than 78% of the target coordinates
is ignored by candidate generation, a polynomial-size list has success
probability tending to zero exponentially. Equivalently, reading a
fraction less than 22% by a fixed positive margin is insufficient within
this restricted factory model. Reading 22% is NOT sufficient by this
argument, and reading the complete target only during ranking does not
count as candidate-generation dependence.

A concrete conditional regime has fully checked rational constants:

- m>=20000;
- r>=19*m/20;
- K<=m^4;
- independent uniform centers modulo any even N;
- the candidate-pool independence contract above.

Then delta>=17/1140, and

```
32*r*delta^2 >= (289/42750)*m > m/150.
```

For m in [20000*2^h,40000*2^h), m^4<2^(64+4h). Since
64+4h <= (200/3)*(h+1) <= (200/3)*2^h <= m/300, it follows that

```
Pr[success] <= 2^(-m/300).
```

This is at most 2^-66 at the minimum length. The argument covers all
lengths in that range, not just a finite numerical scan.

CRITICAL MISSING PREMISE: no theorem or measurement establishes that
future LLL bases have r>=19*m/20, or even that r/m stays above 78%.
The observed native fraction 834/1024 is not extrapolated. This result
does NOT prove that LLL plus rounding fails on the asymptotic family.
It also does not prove any unrestricted classical lower bound or quantum
advantage. The written probability argument is not kernel-checked.

## Counterexamples To Overextension

The implementation retains two exact controls:

1. One adaptively chosen scalar can depend on the supposedly unread input.
   With m=1,N=2 and x=c, exact success is 1. Charging only one visited
   candidate falsely gives the bound 2/3. Charging the complete pre-existing
   pool {0,1} gives the valid bound 1. Polynomial visited count alone is
   therefore insufficient for this theorem.
2. Uniform marginals are not independent targets. With ten equal uniform
   bits and fixed x=0, exact zero-distance success is 1/2, whereas the
   incorrectly applied independent-coordinate bound is 1/32.

These are assumption checks, not toy advantage benchmarks.

## Research Consequences

Keep the finite negative result. Do not call the whole family dequantized,
and do not use this conditional bound to revive a quantum-advantage claim.
Both errors would overstate the available evidence.

Gemini's next campaign should record the actual integer-prefix fraction,
conditional pool size and full target dependence along with paid costs.
Increasing a target-blind fixed list alone may be a poor scaling strategy.
Target-aware basis construction, guided multilevel CVP search and
prefix-aware nonlocal moves can violate the contract and remain live
classical competitors. A naive shortest-vector embedding must also account
for the many short integer-coordinate vectors; do not assume its shortest
output solves this approximate CVP task.

The competing tracks remain conditional too: the DCP track has no new
efficient arithmetic finder, general nonabelian HSP has no efficient
joint receiver, and the natural-dynamics track has no new noncommuting
algorithmic mechanism. This bounded follow-up was chosen to resolve a
specific interpretation of an actual witness, not to keep a direction
alive through more barriers.

Do not spend another main-model pass sharpening this concentration
constant, scanning nearby blind fractions, or building metadata around it.
The next main-model contribution must be a substantive full-target-aware
classical mechanism, a meaningful external reduction, or a concrete
independent quantum candidate.

## Reproduction

```
python theorems/integer_character_readset.py
python -m pytest -q tests/test_integer_character_readset.py -W error::RuntimeWarning
```

The producer rechecks basis/input provenance, discovers the actual
coordinate prefix, and replays the native classical witness. It does not
rerun LLL, produce larger-instance measurements, or certify arbitrary
program information flow. The native report and conditional theorem
are deliberately stored as distinct records.

Verified: 18 focused tests and 305 connected tests passed with
RuntimeWarning fatal (35.36 seconds for the connected run). Python
compilation, 12 site JavaScript syntax checks, site checks and
`python qsearch.py validate` also passed, with no validation issues.
The entire repository test suite was not run.
