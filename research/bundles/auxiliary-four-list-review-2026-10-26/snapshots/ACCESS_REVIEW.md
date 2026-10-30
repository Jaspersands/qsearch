# Independent Check Of Auxiliary Construction Claims

Date: 2026-10-26.

Reviewed: [parent REVIEW.md](/Users/jaspersands/Developer/qsearch-research-work/auxiliary-divisor-review-2026-10-26/REVIEW.md), Sections 3-5.
SHA-256 of the reviewed file:
`cf78bdd6b8aaa4f13548ce990a29a7c6a90d76b0f0afb49c88611d0535629a5c`.

Scope: independent adversarial mathematical and primary-source check. The
tower, original auxiliary-code algebra, generic 3-torsion count, and the
parent's degree-eight matrix/classical-sampler experiment are not re-reviewed.
All created files are in this new directory. No subagents, Git, or UI actions.

## 1. Verdict

**ACCEPT the mathematical claims in Sections 3-5 under their geometric and
algorithmic access assumptions. REVISE the abbreviated runtime/access wording.
REJECT any stronger interpretation as a polynomial matrix-only algorithm.**

| Claim | Decision | Qualification |
| --- | --- | --- |
| Character and prime-count bounds with `C_n=(g+1)(n+6)` | Accept | Smooth geometrically connected curve, odd characteristic, rational base point O; use degree-zero classes |
| Every coset has a degree-a prime at existing levels e >= 16 | Accept | The stated numerical parameters and `r_2<=2g`; no construction follows from existence alone |
| Biased two-list search succeeds with constant probability at e >= 32 | Accept | Independent samples, with replacement, from the exact uniform distributions on degree-b and degree-c primes |
| Rational halving in expected polynomial time | Accept conditionally | Known exact group order, exact uniform Jacobian sampling, effective perfect order-2 pairing, bounded representations and exact group operations |
| `T_access + 2^(r_2/2) poly(g,log q)` | Revise presentation | Per-sample arithmetic must be polynomial in the displayed parameters, not merely available after unspecified preprocessing |
| Uniform polynomial construction from B alone | Reject as unestablished | Neither geometric recovery/access nor a sufficient rational 2-rank bound is supplied |

No counterexample to the stated character, second-moment, or saturation
arguments was found. In particular, the halving argument does **not** hide a
torsion-basis assumption: its relation subroutine can operate before any basis
has been computed. It also does not require a pairing of order `2^s`.

The parent already contains substantial access disclaimers. The requested
revision makes the headline complexity and the phrase "pairing computations
are preprocessing" agree with those disclaimers; it is not a retraction of
the conditional construction.

## 2. Character Counts And The e >= 16 Claim

Let `Q=J(F_q)/2J(F_q)`, `N=|Q|`, and `v(P)=[P-deg(P)O]`.
Extend a nontrivial character of Q to divisor classes by killing O. Its
unramified quadratic class-field cover has O split. This last condition
excludes a constant-field extension, so the connected cover is geometric.
Hurwitz therefore gives `g(Y)=2g-1`.

For every positive integer n, comparison of split and inert prime
contributions gives exactly

```text
#Y(F_(q^n)) - #X(F_(q^n))
  = sum_(j|n) j sum_(deg P=j) chi(v(P))^(n/j).
```

An inert degree-j prime contributes `-j` when `n/j` is odd and `+j` when
it is even. Thus the exponent in the parent's formula is necessary and
correct. Weil bounds the left side by `(6g-2)q^(n/2)`.
Each proper-divisor contribution is bounded by

```text
j B_j <= #X(F_(q^j)) <= q^j+1+2g q^(j/2)
      <= 2(g+1)q^(n/2),  j <= n/2.
```

There are at most `floor(n/2)` such terms. Consequently the character
bound follows with constant `(6g-2)+n(g+1) <= C_n`. For the trivial
character the corresponding constant is `2g+1+n(g+1) <= C_n`.
Character orthogonality divides the sum of N error bounds by N, rather
than introducing an additional N. This verifies the parent's bound (4).

If `q^(n/2)>2NC_n`, then

```text
B_n(c) > q^n/(2Nn),   B_n < 3q^n/(2n),
B_n(c)/B_n > 1/(3N).
```

This proves both existence and the rejection probability uniformly in c.
It does not enumerate the `2^r_2` covers or construct even one of them.

**Degree-parity countercontrol.** Replacing Q by `Pic(X)/2Pic(X)` would
be wrong: its degree coordinate excludes half the classes at every fixed
degree; here a is odd. Similarly a constant quadratic cover has a
degree-parity restriction. Neither objection applies to the actual
`[P-nO]` and O-split formulation. The density theorem in
[Czogala--Koprowski, Theorem 1 and Section 3](https://arxiv.org/html/1904.12177v1)
is not a replacement for this fixed-degree estimate. The point-count
and prime-count framework agrees with
[Elkies et al., Lemma 2.1](https://arxiv.org/html/math/0208060).

At e=16 the independently computed integer part of
`100003^23/(2*2^162*2378)^2` is **12,944,860,411**.
Here `C_a(e)=(5e+2)(2e-3)`, and for e>=16,

```text
C_a(e+1)/C_a(e)
 = ((5e+7)/(5e+2))*((2e-1)/(2e-3)) < 2.
```

The squared inequality's ratio grows by more than
`100003^2/(4*2^20)>1` per unit increment. Thus the assertion holds at
every existing certified level with e>=16, not only at tested levels.
No assumption about typical G or small actual r_2 was used.

## 3. Biased Birthday Search

Write `mu=mu_b`, `nu=mu_c`, and `L=ceil(sqrt(N))`. The character estimate
and the lower bound on B_n give the stated
`|mu_hat(chi)|<=epsilon_b`, and similarly for nu. Fourier inversion gives

```text
p = Pr(X+Y=t) >= (1-(N-1)epsilon_b epsilon_c)/N >= 15/(16N),
max(mu) <= 1/N+epsilon_b,   max(nu) <= 1/N+epsilon_c.
```

Here all nontrivial Fourier coefficients are bounded; the distributions
need not be close to uniform pointwise on the scale `1/N`.

Define

```text
A = sum_x mu(x) nu(t-x)^2,
B = sum_x mu(x)^2 nu(t-x).
```

Counting ordered pairs of collision indicators gives the exact formula

```text
E[Z]   = L^2 p,
E[Z^2] = L^2 p + L^2(L-1)^2 p^2 + L^2(L-1)(A+B).
```

Since `A<=max(nu)*p` and `B<=max(mu)*p`, the parent's inequality follows.
In fact its stated hypotheses imply the explicit uniform estimate

```text
E[Z^2]/E[Z]^2
 <= 1 + 16/15 + 32/(15L) + 8 sqrt(N)/(15L)
 <= 71/15 < 5.
```

Therefore `Pr(Z>0)>=15/71>1/5`. This includes N=1; that case also
succeeds trivially. Duplicate samples are harmless, but treating all
`L^2` indicators as independent would not be harmless.

At e=32 the independently computed integer part of
`100003^27/(64*5346^2*2^322)` is
**64,040,584,432,915,384,358,798,429,809**.
For b=e-5, `C_b=(5e+2)(e+1)` has successive ratio below 2; the normalized
birthday bound grows by more than `100003/(4*2^10)>1`. The c-side is
easier because its ratio to the b-side is
`100003*((e+1)/(e+2))^2>1`. The all-level e>=32 assertion follows.

## 4. Primary-Source Hypotheses

The following is the operative contract in
[Bruin, Sections 2.1 and 3.2-3.9](https://arxiv.org/html/1003.2563):

- Curve: smooth, complete, geometrically connected; embedding line bundle
  L of degree ell>=2g+1, with explicit truncated graded multiplication.
- Algorithm 3.2: degree n, integer i, `n<=i*ell-2g`, and `S_X^(2i+2)`;
  exact uniform primes, expected polynomial cost when nonempty; no zeta input.
- Algorithm 3.5/Section 3.5: the zeta numerator and graded algebra provide
  exact uniform effective-divisor/Jacobian sampling, not merely the group order.
- Algorithm 3.8: `S_X^(7)`, represented x,y, `nx=0`, and `n|(q-1)`;
  evaluates the perfect pairing `J[n](F_q) x J(F_q)/nJ(F_q) -> mu_n`.
- Algorithm 3.10: verified relations between supplied torsion points;
  its sampling step inherits Section 3.5's zeta requirement.
- Algorithm 3.11: `S_X^(7)` and Frobenius characteristic polynomial;
  computes rational l-torsion. At l=2 its auxiliary extension has degree
  less than 4g when nontrivial, not the full torsion splitting-field degree.

These are explicit geometric inputs, not a reconstruction theorem from B.

Independently substituting `L=O_X((2g+1)O)` and i=2 shows that all the
requested degrees a,b,c fit the prime-sampling degree condition. Graded
pieces through degree 7 then have O(g) dimensions, by Riemann--Roch.
This removes a possible hidden exponential tensor-power cost **if those
spaces and multiplication maps can actually be constructed**. An existence
statement for L does not construct the algebra.

[Couveignes, Introduction and Section 8](https://arxiv.org/html/0706.0272)
assumes a plane model, singularity information, and Frobenius polynomial;
the stated complexity for l^k-torsion is polynomial in l^k, not its
logarithm. Substituting `l^k=2^s` would therefore not prove the desired
polynomial halving bound. The independent argument below avoids that move.

[Kyng, Theorem 1.1](https://link.springer.com/article/10.1007/s40993-022-00398-7)
takes an explicit absolutely irreducible plane polynomial of degree Delta
over F_(p^f) and states cost `f^O(1) Delta^O(1) p^(1/2+o(1))` for the
smooth model's zeta function. The paper explicitly does not supply a complete
complexity proof. This supports the parent's carefully qualified fixed-p
observation, not free zeta computation, polynomial dependence on log p, or
polynomial conversion from an unspecified tower certificate or B.

## 5. Halving: Independent Proof Of The Reduction

### Exact Access Assumptions

For this abstract reduction assume a finite abelian group `J=J(F_q)` with:

1. Exact identity tests, addition, inverses and scalar multiplication in
   bounded-size representations, with charged expected polynomial costs.
2. Its exact order `h=2^s M`, M odd. Finding this order is outside the reduction.
3. Independent exact uniform samples from J, at charged expected polynomial cost.
4. An evaluable perfect pairing `J[2] x J/2J -> {+1,-1}` for individually
   represented order-2 inputs. No torsion basis or class coordinates are assumed.

The concrete implementation of assumption 3 described above requires more
input than h. Assumption 4 is the order-2 Tate/Frey--Ruck pairing, not an
alternating Weil pairing restricted to rational 2-torsion.

### Relations Without A Basis

For supplied `T_1,...,T_t in J[2]`, let U be their span and let W map
`F_2^t -> U` by group addition. Evaluating against independent uniform J
points gives independent uniform linear functionals on U, by perfectness.
Every true relation is in the sampled sign-matrix kernel. If every vector
in a basis of that kernel evaluates to zero in J, the reverse inclusion
is also certified. Thus no incorrect relation can be accepted.

After m rows the probability that a nonzero element of U remains
undetected is at most `(2^dim(U)-1)2^(-m)`. With `m=t+2`, this is below
1/4. Fresh batches and exact verification give a Las Vegas algorithm of
polynomial expected cost. This argument never requests a basis of U.

### Saturation Without Group Division

Let `H=J[2^infinity]`, let h_1,...,h_t be any elements of H, let
`phi:Z^t -> H` be their evaluation map, and write `K=ker(phi)`.
Start at `L_0=2^s Z^t subset K`. All quotients involved are finite 2-groups.

There is a particularly explicit way to compute the parent's V_i. If the
columns of an integer matrix B form a basis of L_i, compute
`ker(B mod 2)` by binary elimination. For each basis vector u of that
kernel, `v=B*u/2` is an **integer vector**, and these v give an F_2-basis
of `(Z^t/L_i)[2]`. This divides known even integers, not points of H.

Their images phi(v) have order dividing 2. The preceding relation routine
computes exactly which combinations vanish, and adjoining those lifts
to L_i preserves `L_i subset K`. If K/L_i is nontrivial, it has an
order-2 element, so an enlargement must occur. Hence stopping certifies
`L_i=K`, not merely a plausible list of relations.

The initial index is `2^(st)`. Every strict enlargement divides the index
by at least 2, giving at most st strict stages. Normalize by HNF after
each stage: its entries are bounded in terms of the index, so they have
O(st) bits; intermediate binary-kernel lifts also have polynomial bit
length. Standard integer linear algebra and repeated doubling therefore
have polynomial bit complexity. No enumeration of `2^s` vectors occurs.

### Generation, Target Solving, And Odd Part

Multiplication by M maps uniform J samples onto uniform H samples.
The saturated relation lattice certifies the order of the generated
subgroup by its index in Z^t. Keep a sample only when it increases that
order. There are at most s such increases. While the subgroup is proper,
the probability of an increase is at least 1/2. Thus at most 2s samples
are needed in expectation, and retained lists have length at most s.
Equality with the known order `2^s` certifies generation of all H.

To find a half of `z in H`, append z to a certified generating list and
saturate its relation lattice K. Let e_z be the last standard vector.
One can bypass even the coordinate-conversion details of SNF: if B is
a basis matrix for K, solve

```text
B*c = e_z (mod 2),
v = (e_z+B*c)/2 in Z^(t+1).
```

Then `2phi(v)=z`. Conversely any half in H supplies such a congruence
because the list generates H. Failure of the binary system proves
nondivisibility in H. A basis of H[2] for later coset labels can also be
extracted from this now-certified presentation; it was not needed to
obtain the presentation.

Finally solve `2u=Mx` in H and set `y=u-((M-1)/2)x`. Direct calculation
gives `2y=Mx-(M-1)x=x`. If the H equation has no solution, neither does
`2y=x` in J. For s=0, H is trivial and the same formula applies with u=0.
No odd-part factorization or odd-part discrete logarithm is involved.
Although `v_2(100003-1)=1`, only order-2 pairings were used; high-order
roots of unity and exponential extension degrees are unnecessary.

### Failed Shortcuts

- In `H=C_4`, the nonzero T=2 pairs trivially against the subgroup
  `{0,2}` under the perfect pairing `e(T,y)=(-1)^y`. Sampling only that
  current subgroup cannot detect T; full J sampling is essential.
- In `H=C_4 x C_2`, s=3, so multiplication by `2^(s-1)=4` kills everything.
  That shortcut does not produce a rational 2-torsion basis.
- In `C_4`, x=2 has halves in H but none in `<x>`. Solving only in the
  target's cyclic subgroup would give a false nondivisibility result.
- Random sections of one fixed line bundle all have divisors in one
  fixed class. They cannot replace a uniform Jacobian sampler.

These falsify tempting replacements for the actual algorithm, not the
algorithm as written. Exact verification prevents false acceptance, but
does not rescue the running time of a sampler confined to a subgroup.

## 6. Required Access Accounting

The passage at [parent line 307](/Users/jaspersands/Developer/qsearch-research-work/auxiliary-divisor-review-2026-10-26/REVIEW.md:307)
should distinguish setup from recurring cost: a precomputed torsion basis
does not evaluate the r_2 pairings needed for each newly sampled prime.
The [headline bound](/Users/jaspersands/Developer/qsearch-research-work/auxiliary-divisor-review-2026-10-26/REVIEW.md:14)
should state that the representation size and each primitive cost are
polynomial in g and log q, or expose those costs separately.

A precise conditional construction bound is

```text
T_setup + O(sqrt(N)) * (T_prime(b)+T_prime(c)+r_2*T_pair
                       +T_class+poly(r_2)) + T_half,
```

with dictionary/sorting overhead absorbed into the polynomial. Storage
includes `O(sqrt(N))` represented primes and r_2-bit labels, besides setup
and arithmetic workspace. T_half is polynomial under Section 5's access
contract. If the model has size R not known to be polynomial in g, the
primitive costs must retain their R dependence. Their repeated use cannot
simply be renamed one-time preprocessing.

T_setup must include actual geometric input generation or recovery,
representation conversions, order/zeta acquisition where required, and
certified torsion/presentation construction. The target class from G must
also be computed in that same model. A new generic G requires its own
effective-A search; reusable curve data do not supply A for every G.
Turning the class half into F, principal witnesses and the auxiliary
evaluation data remains charged downstream work, outside this narrow audit.

The stated search still costs `2^(r_2/2)` even when all this access is
polynomial. Neither linear r_2 nor an exponential access cost is proved
for the specified source. Conversely neither is ruled out by this review.
An existential tower certificate and a matrix B alone meet none of these
algorithmic obligations automatically.

## 7. Exact Controls And Limits

[exact_controls.py](/Users/jaspersands/Developer/qsearch-research-work/auxiliary-construction-check-2026-10-26/exact_controls.py)
uses exact integers/rationals and SymPy 1.14.0 HNF. Run with
`python3 -B exact_controls.py` from this directory. The successful output
is recorded in
[exact_controls.json](/Users/jaspersands/Developer/qsearch-research-work/auxiliary-construction-check-2026-10-26/exact_controls.json).

- Cutoff inequalities reproduced at e=8,16,32,64, including both quoted
  large integer ratios. At e=16 only the degree-11 birthday side fails.
- Biased laws `(1-alpha)Uniform(Q)+alpha*delta_0`, with
  `alpha=1/(4sqrt(N))`, were checked for every target at N=4,16,64. Every
  nontrivial Fourier coefficient equals the allowed upper bound.
- At N=4 all pairs of length-two lists were enumerated exactly. The
  minimum success probability is `172487/262144`, and the directly
  counted moments equal the overlap-aware formula.
- Saturation recovered the exact relation-lattice indices for six
  small 2-group fixtures, including dependent generators and a proper
  subgroup. All 62 targets across the five full-group fixtures gave
  correct half/nondivisibility decisions against exhaustive checking.
- All 24 targets in `C_4 x C_6` passed the odd-part recombination check.
  The first three failed shortcuts above also have exact controls.

The finite group tests use an explicit perfect pairing as a test oracle;
they do not implement a curve, zeta computation, or Frey--Ruck arithmetic.
They support the algebraic audit but are not its asymptotic proof.
No actual tower-level auxiliary F or B-only solver was constructed.

**Decisive conclusion:** retain the every-coset theorem, the biased birthday
guarantee, and the conditional polynomial rational-halving reduction.
Do not charge an intrinsic `2^r_2` halving search when the stated pairing
access is available. Do not remove the `2^(r_2/2)` representative search,
the geometric-access requirements, or the zeta/sampler obligations. There
is no resulting hardness theorem or demonstrated quantum advantage.
