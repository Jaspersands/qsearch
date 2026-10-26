# Fixed-Target Native Moment Search By Classical Masking

2026-10-19. LOCAL DERIVATION REVIEW PENDING. Standard Gauss sums, MDS rank,
linear algebra and polynomial norm machinery; no novelty, accepted proof or
new quantum algorithm claim. The previous goal turn was progress: scoped
sparse completion, exact GRS/OPI reduction and a fixed native norm witness.
This pass addresses its remaining population-to-fixed-target gap without
pretending the old population mean can simply be amplified.

## Problem And Decisive Change

Public prime p=3 mod4, ORIGINAL support1,...,L<p, rank r, arbitrary fixed
target b in F_p^r. Return a nontrivial native F_p vector satisfying

```text
sum_(a=1)^L a^k*x_a^2=b_k,  0<=k<r.
```

The target is NOT rerolled. Reserve s of the ORIGINAL variables, draw their
values u uniformly, compute their exact contribution D(u), then solve the
remaining equations for b-D(u). Concatenating those roots with u solves b.
Neither an extra variable nor a planted witness is introduced. Failed paid
partial assignments are algorithmic search trials, not changed inputs.

The existing norm attack only had an IID-input population bound. The new
step makes the residual target sufficiently close to uniform FOR EVERY fixed b,
then adds an independent uniform kernel polynomial. This supplies a uniform
lower bound on each complete attempt, so fresh complete attempts may genuinely
be amplified. No claim is made about the old unmasked solver's q(b).

## Exact Mixing Lemma

Let T be ANY s distinct field points and r<=s. Draw u_a independently uniform
in F_p and define D_k=sum_(a in T) a^k*u_a^2 for k<r. For coefficient vector y,
let f_y(X)=sum_(k<r) y_k X^k, and let w(y) be its nonzero evaluation count on T.
The normalized characteristic function factors into quadratic Gauss sums.
Each nonzero coefficient contributes squared magnitude1/p; zero contributes1.
Thus |E exp(2*pi*i*y.D/p)|^2=p^(-w(y)). Parseval and Cauchy--Schwarz give

```text
chi_square(law(D) || uniform F_p^r) = sum_(y!=0) p^(-w(y)) = E,
TV(law(D),uniform) <= sqrt(E)/2.
```

E has an EXACT O(r)-term expression, not p^r enumerated Fourier labels:

```text
E = p^(-s) sum_(j=0)^(r-1) binom(s,j)*(p-1)^j*(p^(r-j)-1).
```

Proof: write p^(s-w(y))=product_(a in T)[1+(p-1)*1[f_y(a)=0]]. Expand
over point subsets. A j-point Vandermonde constraint has p^(r-j) solutions
for j<r and just the zero polynomial for j>=r. Subtract the zero-polynomial
contribution product[1+(p-1)]=p^s before dividing by p^s. This also explains
why the expression is independent of T's particular distinct locations.

Consequently E<=2^s*p^(r-s). Unlike the crude minimum-distance bound needing
about2r reserved variables, this can work with r+1 variables over large fields.
The implementation uses the exact sum, integer square-root comparisons and
OUTWARD96-bit dyadic rounding. No floating-root or statistical certificate.
The Gauss and MDS ingredients are standard; see the character-sum context in
[Zhu--Liao](https://arxiv.org/abs/2112.14067) and the existing GRS-duality notes.
The local combination and quantifiers still need independent review.

## Fixed-Target Success Transfer

Let n=L-s. On points1,...,n, build the triangular target lift B_c from the
previous pass for c=b-D(u), so all native square-coordinate solutions have

```text
z_a=(B_c(a)+P(a))/A'(a),   deg(P)<K=n-r,
A=product_(a=1)^n(X-a).
```

Draw an INDEPENDENT uniform polynomial M of degree<K. The map
(c,M)->B_c+M->its n evaluations is a linear bijection. For uniform c, the
induced OPI shifts -(B_c(a)+M(a)) are IID uniform. For c within TV delta of
uniform, the joint shift law stays within delta, as do ALL subsequent
randomized norm decisions. Adding M is a kernel move and preserves c.

The orientations are fixed by character(A'(a)); let a,beta_count denote the
square/nonsquare group sizes, and put D=beta_count+(beta_count mod2). Under
the EXISTING norm attack's explicit gate

```text
a>0, beta_count>0, K>max(a,D),
```

one trial on IID shifts succeeds with probability at least

```text
mu = I_p(D)/p^D,
I_p(D)=(1/D)*sum_(d|D) mobius(d)*p^(D/d).
```

This is the existing even-degree irreducible subevent, not a conjectured
norm frequency in a fixed pencil. The current code uses the zero-allowing
convention, so the strict Cayley-rotation field restriction is unnecessary.

Reject a paid all-zero reserved assignment to guarantee a nontrivial output
even at b=0. That event has probability p^(-s). Combining ALL losses yields

```text
for EVERY fixed original b:
Pr[one complete attempt solves b] >= gamma = mu-delta-p^(-s).
```

The certifier rounds mu DOWN and both losses UP. If gamma<=0 or the degree
gate fails, it reports UNKNOWN; it does not infer hardness or infeasibility.
If gamma>0, independent complete attempts obey failure<=(1-gamma)^T and
expected attempts<=1/gamma. T=ceil(f/gamma) gives failure<=exp(-f)<2^(-f).
These statements rely on actual uniform independent coins, not PRNG seeds.
Standard Las Vegas finite-field factorizations have expected polynomial work
in degree/log p; no full library-level bit-cost certification is supplied.

This is a genuinely FIXED-target bound for the NEW algorithm. The inference
E_b[q(b)]>=mu -> failure=(1-mu)^T for the OLD unmasked algorithm is still false.
The crucial added randomness is carried by actual original output variables;
a kernel mask alone does not randomize a fixed syndrome.

## Actual Original-Field Controls

For p=2^61-1,L127,r31,s32, the remaining support has n95,K64,48 square and
47 nonsquare derivative orientations, and D48. All gates hold in the ORIGINAL
61-bit field, unlike the old large-degree Morse/exterior probability bound.

| Quantity | Conservative Value, Approximately |
|---|---|
| Exact MDS chi-square energy | 1.86265e-9 |
| TV upper bound delta | 2.15792e-5 |
| IID norm lower bound mu | 0.0208333333 |
| Uniform fixed-target attempt floor gamma | 0.0208117541 |
| Expected attempts upper bound | 48.04977 |
| Budget for the stated2^-10 guarantee | 481 |

The JSON stores exact directed bounds, not these rounded displays. The actual
producer runs ONE fixed nonzero public target and the homogeneous target,
seeds7711/7712, and finds native witnesses after6 paid attempts EACH.
Every prefix, residual syndrome, kernel mask, rejected norm polynomial,
factorization and winning127-vector is saved. All31 ORIGINAL equations are
independently replayed. Seeds are reproducible transcripts, not measured
confidence estimates; the stated probability guarantee comes from the local
proof under uniform coins. No full-field enumeration or field lift occurs.

## Try To Falsify It

- The finite p7,L6,r1,s2 calibration enumerates all7 fixed targets, all49
  reserved assignments and all7 relevant quadratic masks. Constant/linear
  masks cancel exactly with first-group interpolation, representing49 more
  masks per case. The2401 explicitly evaluated cases give irreducible hits
  136,144,136,144,144,168,136 out of343 per target, all above the bound.
- Omitting the native-variable mask leaves target5 with ZERO irreducible
  members in its seven-element monic pencil. The native task still has the
  explicit witness(1,2,0,0,0,0). This refutes the old amplification inference,
  not every expanded norm pencil or the original problem.
- Tests independently enumerate native moment laws and recover the exact
  Fourier-energy identity and TV inequality on small supports. They do not
  accept an MDS label, report status or successful seed as a proof.
- The remaining norm degree gate is essential. The same L127 with r50,s51
  fails it and is UNKNOWN; this does NOT solve the older N127,K77 mixed OPI
  family or the unrelated folded m31 norm system.
- Independent mask coefficients are essential. Replacing a uniform mask by
  zero or by a low-entropy seed invalidates the IID/TV transfer as a theorem,
  even though some seeded executions still return valid witnesses.
- The result covers search with zeros allowed, not exact/uniform solution
  sampling and not every-coordinate-nonzero output. Sampling may remain a
  separate question; it must not be declared hard from this biased solver.
- Scope is an explicitly CERTIFIED SPLIT on consecutive native supports with
  gamma inverse-polynomial. No all-support/all-rank/all-field dequantization,
  accepted proof, novelty or Shor-level result is inferred.

## Research Decision And Next Work

Retain the native masking reduction and solver. Do not build another quantum
search receiver for the certified moment families by relabeling them as
general MQ. The fixed-input probability gap has been bypassed constructively
in this regime, not resolved by more seeds or looser geometry constants.

The literature refresh also found
[Horinaga--Yamakawa](https://arxiv.org/abs/2607.14650): a known worst-case
OPI route with list selection and additional source/error conditions. It
does not justify applying our earlier generic average bound targetwise.
It reinforces the need to compare complete published mechanisms, not claim
our list/OPI coordinate change is a new quantum algorithm. No content from
that paper is used as a proof of this classical masking construction.

Next high-reasoning work should compare an independent constructive direction
or a genuinely stronger native sampling objective with matched classical
baselines and a natural reduction. Do not continue high-rate OPI by inertia.
Independent mathematical review of the new fixed-target transfer is required
before using it in a preprint or central accepted theorem.

Initial v1 verification:14 focused masking tests within138 connected tests
passed6.39s. That350344-byte report bound its producer and four dependencies. Python
compilation, recursive site JavaScript syntax, site checks, whitespace and
actual registry validation pass (valid:true,issues:[]). This is not the full
repository suite. No GPT commit/push or central claim promotion.

## Uniform Family Closure: No Favorable Profile Assumption

Follow-up pass, still LOCAL DERIVATION REVIEW PENDING. The prior numerical
split had an explicit public orientation gate. This section removes that
profile assumption for consecutive supports and gives a uniform growing-rank
statement. It is not a new field-size scan or a claim derived from seeds.

### Reflection Lemma

Let A_n(X)=product_(a=1)^n(X-a), n even, and p>n with p=3 mod4. At every
point a, A_n'(a)=(-1)^(n-a)*(a-1)!*(n-a)!, so

```text
A_n'(n+1-a) = -A_n'(a).
```

All values are nonzero, reflection pairs have no fixed point, and -1 is a
nonsquare. Hence EXACTLY n/2 derivative values are square and n/2 nonsquare.
This is an all-n algebraic fact, not an observed balanced random pattern.
It fails for arbitrary supports and for p=1 mod4; tests retain both traps.

Thus the remaining norm task has groups a=b=n/2 and D=n/2+(n/2 mod2).
The easy sufficient gate n>=2r+4 implies K=n-r>max(n/2,D).

### Explicit Uniform Parameters

For L>=16, p>L prime3mod4, define

```text
ell=ceil(log2 L), h=floor(log2 p)-1,
t=ceil((r+2ell+6)/h),
s=r+t, increased by at most1 so n=L-s is even.
```

The scalar-only constructor refuses the uniform claim unless n>=2r+4.
It builds no derivative table, matrix, prefix source or norm polynomial.

Since p>=2^(h+1) and h*t>=r+2ell+6, the previous exact energy obeys

```text
E <= 2^s*p^(r-s) <= 2^(-2ell-6) <= 1/(64L^2).
```

The optional parity increment only multiplies this upper bound by2/p<1.
Therefore delta<=1/(16L). Also s>=2 and p>L imply p^-s<=1/(16L) for L>=16.

For every even D>=2, the usual irreducible-polynomial count gives
I_p(D)/p^D>=1/(2D). One elementary justification counts elements in F_(p^D)
outside all proper subfields: the excluded count is at most
sum_(j=1)^(D/2) p^j<=p^D/2 for p>=3. Each degree-D irreducible has D roots.
No large extension is constructed by the algorithm. Since D<=L, mu>=1/(2L).

Use bound precision B with2^B>=64L. The population downward rounding and two
losses' upward rounding cost at most3*2^-B. The ACTUAL one-attempt success
floor consequently satisfies

```text
gamma >= 1/(2L)-1/(16L)-1/(16L)-3/(64L)
      = 21/(64L) > 1/(4L).
```

Thus expected attempts<=4L, and4Lf independent complete attempts give
failure<2^-f. Every attempt uses polynomially many field/poly operations and
standard expected-polynomial finite-field factorization in L and log p.
This is a uniform growing-degree argument, not a fixed-degree constant hidden
in an asymptotic prime count. The implementation uses the stronger exact
MDS/population certificate for its actual budget. The old arbitrary4096-trial
ceiling was removed; the reference4096-coordinate limit remains operational,
not a theorem boundary or evidence of hardness beyond it.

### Entire Proposed Quarter-Rate Window Is Covered

For EVERY L>=64, EVERY prime p>L with p=3 mod4, and1<=r<=floor(L/4), the
constructor satisfies n>=2r+4. Here is an explicit bound, not a plotted trend.
We have h>=5 and ell<=L/8; hence

```text
s <= (6/5)r+(2/5)ell+16/5 <= 7L/20+16/5,
n >= 13L/20-16/5 >= L/2+4 >= 2r+4.
```

The middle inequality holds already for L>=48. Therefore the new native
classical algorithm has a uniform expected-polynomial SEARCH guarantee for
the WHOLE canonical quarter-rate chirp family above, for EVERY target.
This does not depend on p being exponentially large or a selected seed.
More generally, for any fixed r/L<1/3 the gate eventually holds as L grows:
t=O(r/log L+1)=o(L), so n=L-r-o(L)>2r+4. That is a further sufficient regime,
not a claim of optimal classical rank threshold.

No novelty or independent proof acceptance is asserted. The earlier corpus /
literature search identified general diagonal-equation algorithms and standard
norm/GRS machinery, but not a substitute for reviewing this exact construction.
Search failure is not a novelty certificate. The claim remains scoped to
unweighted consecutive native moments, zeros allowed, nontrivial vector.

### Executed Versus Analytic Controls

The SAME producer now exposes `uniform_family_parameters` and `attack_uniform`:

- p=2^61-1,L127,r31 chooses s33,n94 and groups47/47. The actual nonzero and
  homogeneous targets produce native witnesses in18 and17 paid attempts.
  This does not make their probabilistic guarantee empirical.
- p8191,L320,r80 chooses s90,n230 and groups115/115. One unchanged public
  target produces a verified320-coordinate /80-equation witness in24 attempts.
  This is a separate field/input, not a lift of the old61-bit instance.
- L1024/r256 at p8191 and L4096/r1024 at p=2^31-1 are SCALAR PARAMETER
  certificates ONLY. No corresponding matrix, decoder, norm search or quantum
  state was executed. Tests ensure the constructor cannot call matrix setup.

Direct derivative-product controls check reflection/class counts. Exact
integer inequalities check energy, parity, precision and degree budgets;
additional small-field quarter-window checks run the smallest eligible prime
for each L64..512. Those finite checks support implementation correctness,
not the general proof above. Existing manual-split witnesses remain saved.

## Portfolio Decision After Closing This Family

The stop rule is active: no more high-rate moment/OPI modules by inertia.

| Direction | Concrete Mechanism And Present Decision |
|---|---|
| Canonical chirp SEARCH | Known list-decoder reduction exists, but the entire quarter-rate consecutive native family now has the local uniform classical solver. Retire it as advantage evidence; retain the falsifier. |
| Native solution SAMPLING | The classical norm output is biased, so search does not settle uniform sampling. A known quantum sampler is not by itself a new algorithm; require a natural reduction and matched classical sampling attacks before re-entry. |
| DCP / lattice source | High upside and natural reductions, but no new uniform arithmetic finder or useful-bit receiver is supplied. Reserve, not another bridge/barrier campaign. |
| Folded extension-norm task | Different base-field/extension-block geometry, not solved here. Conditional quantum scores and failed global MQ runs do not establish hardness or a natural application. Re-enter only for a concrete new solver/reduction, not a compiler around an unadmitted benchmark. |
| Cyclic BPQM / noncommuting dynamics | Independent known mechanisms exist, but this repo still lacks the relevant cyclic/global receiver or a new noncommuting observable algorithm with matched classical costs. Do not replace that missing mechanism by more tree or small-state tests. |

The next main-model pass should select a genuinely different constructive
question, or review a precise remaining proof dependency. Routine CLI/EXP
wiring and further quarter-rate parameter scans do not merit high-end
reasoning time. No central candidate/negative/proof claim is auto-promoted.

Uniform-family v2 verification:26 focused masking tests within150 connected
tests pass6.37s. The2256768-byte live report binds the SAME producer and four
dependencies and retains all failed paid attempts. Registry validation,
Python compilation, recursive site JavaScript syntax, site and whitespace
checks pass. This is NOT the full repository suite. No GPT commit/push or
accepted mathematical claim promotion.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python theorems/moment_target_masking.py --write
python -m pytest -q tests/test_moment_target_masking.py
```
