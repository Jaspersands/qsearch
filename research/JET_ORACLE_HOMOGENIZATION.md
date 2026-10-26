# Deterministic Oracle Homogenization

2026-10-22. Status: public query compiler, provisional constructive
reduction, and an adversarial internal audit. Not an independently
reviewed algorithm, novelty certificate or useful speedup demonstration.

## 1. Audit Result: A Stronger And Simpler Interface

The preceding NONABELIAN_JET_HOMOGENIZATION.md used random batched
regular sources, evaluation alignment and a nonnormal subgroup coset
chart. That construction remains a possible state-only route. For the
actual target input, however, we already have an ORDINARY coherent
function oracle. We can construct a new hiding function explicitly.

This removes the proposed algorithm's dependence on random alignment,
spectator measurements, factorization of N^B, and their normalization
proofs. It is not an unjustified promotion from state preparation to an
oracle. The new oracle is an ordered tuple of legal original queries.
The central quantum descent remains necessary and is not implemented by
this classical compiler.

Assume an explicit genuine Lie algebra L/F_p of fixed class c, p>c,
unique coordinates, public group operations via BCH, and an ordinary
coherent deterministic-label oracle f hiding left cosets of H. First
assume H intersects exp(N) trivially, N=L'. Recovering that intersection
for arbitrary H is a separate recursive step, not silently omitted.
Let V=L/N, U the hidden linear image, and s a PUBLIC linear Lie section.

Use the existing actual lower-central filtration to construct the public
polynomial jet group J and K=J semidirect V. Its total-degree coordinate
caps are w_i and its grading is t-degree, as in the preceding note.
The proof-only P and F(q)(u,t)=P(u)^-1 P(u+t*q) are NOT public inputs.

## 2. Deterministic Evaluation Certificate

Set m=dim(V), D=c-1. List the integer lower simplex

```
B_D = {beta in N^(m+1): |beta|<=D}.
```

For each beta set Y=beta[:-1] and s=beta[-1]+1 in F_p. The number of
points is ell=binom(m+c,m+1). All s are nonzero because 1<=s<=c<p.
There is no scan over F_p or a Cartesian grid of size c^m.

These points are unisolvent for polynomials divisible by t of total
degree at most c. Divide by t, shift v=t-1, and use the Newton basis
prod_j binom(v_j,alpha_j), |alpha|<=D. On nodes beta ordered by total
degree, evaluation is unit lower triangular: an entry vanishes unless
alpha<=beta componentwise, and the diagonal is one. All factorial
denominators are invertible. The change to ordinary monomials and the
shift t=v+1 are invertible. Multiplication by the nonzero row value t
does not change rank.

Each coordinate degree cap w_i<=c is a subspace of this design. Thus
the PUBLIC point-evaluation homomorphism

```
E:J -> N^ell,  E(a)_i = a(Y_i,s_i)
```

is injective. In log coordinates this follows coordinatewise; the Lazard
log is injective. No coefficients of P have been interpolated. This
argument needs p>c, not the p>2c used by the earlier random-rank bound.
The public algebra/certificate guard now reflects p>c. The OLD random
resource schedule still correctly requires p>2c and was not relaxed.

## 3. The New Oracle And Exact Coset Proof

For (a,q) in K, compute

```
f_hat(a,q) = ( f( E_i(a) * exp(s(Y_i+s_i*q)) ) )_(i=1..ell).
```

Here s denotes the Lie section, while s_i denotes the scalar point
coordinate. In code the section is represented by section_basis; these
are distinct objects. E_i(a) is exponentiated in the original normal
group. Multiplication is normal-FIRST. The code returns the logarithm
of this product in the original ambient coordinates, ready for f.

Fix two inputs (a,q),(b,r). The original section-word coset relation
gives, at EACH i,

```
f(E_i(a)*section(Y_i+s_i*q)) = f(E_i(b)*section(Y_i+s_i*r))
iff s_i*(r-q) in U and
    E_i(b) = E_i(a) * P(Y_i+s_i*q)^-1 * P(Y_i+s_i*r).
```

Because U is linear and s_i!=0, the first condition is r-q in U.
Now P(Y_i+s_i*q)=P(Y_i)*E_i(F(q)). The common LEFT constants cancel,
and injectivity of E makes equality of the entire ordered label tuple
equivalent to

```
r-q in U,  b = a * F(q)^-1 * F(r).
```

The cocycle identity F(r)=F(q)*alpha_q(F(r-q)) says this is exactly

```
(b,r) = (a,q) * (F(r-q),r-q).
```

Consequently f_hat hides ordinary left cosets of the subgroup
H_F={(F(u),u):u in U} in K. This proof is valid for nonabelian N.
No commutative rearrangement of P, F or a is allowed.

The Lean module JetOracleHomogenization proves the abstract group-level
statement: a cocycle gives a graph subgroup in the actual Mathlib
semidirect product; an injective evaluation homomorphism, the component
hiding relations and common left normalization imply the exact tuple
oracle coset relation. Its tupleOracle definition has NO P, F or H
argument. It also proves the pointwise normalized-difference cocycle and
scaling identities. Polynomial unisolvence, the ambient Lie-to-oracle instantiation
and the quantum receiver are still outside that formal theorem.

## 4. Coherent Access And Costs

To evaluate f_hat coherently, compute each original query input into
scratch space using public arithmetic, apply the original function oracle
into that component's output register, and uncompute the scratch input
using the retained (a,q). Keep the full ORDERED tuple of output labels.
This costs exactly ell original oracle calls. Do not sort, discard or
hash labels without a separate collision argument. Reversal of this
constructed unitary uses reversed public arithmetic and inverse original
oracle calls; the current coset-state receiver only needs forward copies.

The label width is ell times the original label width. Reversible
arithmetic workspace, coordinate encodings and BCH computation are all
polynomial for fixed c, and their gates are charged. The BCH coefficient
precomputation is exponential in c, so no growing-class bound follows.
The Python implementation supplies the classical arithmetic compiler,
NOT a synthesized quantum circuit.

Starting with a uniform K register, querying f_hat and tracing its label
tuple now produces the ordinary H_F coset mixture directly. The previous
state conversion is unnecessary under this input model. Public dilation
Delta_s(a,q)=(S_s(a),s*q) preserves H_F exactly, since F(s*u)=S_s(F(u)).
The prior central-character/SDE descent therefore applies with the same
freshness and all-label requirements. It does not require distinct
scaling eigencharacters or a Vandermonde argument on hidden log(H_F).
Implement the central-character measurement nondestructively on the
source group register: Fourier-transform its public central coordinate,
copy the computational label to a fresh record, then inverse-transform
the central coordinate. Conditioning on the record gives the FULL
projected state used by the trace proof. Only then apply ordinary right
multiplication. Alternatively a compressed quotient carrier needs the
explicit phase-aware twisted action. Discarding the central coordinate
and applying plain quotient multiplication is not that instrument.
Even at c=p-1, degree-c scaling can be trivial on the top center; the
fixed-degree SDE contract still applies, with a correspondingly bounded
prime. No zero-sum algorithm for arbitrary large-degree instances follows.

For the actual c9, m2, dim(N)=17 control, each new oracle call uses165
original queries instead of a998-source random batch plus retry caps.
There are no alignment retries or spectator measurements. The remaining
eight-stage SDE tree is unchanged. A conservative single-image query
CEIL-log2 upper bound is1763 at both p43 and p=2^127-1. This is still
astronomically impractical, not a measured cost or lower bound.
The profile includes final abelian sampling, but not all arbitrary-H
recursive calls, SDE bit-operation cost or approximate gate synthesis.

## 5. Decisive Checks And Failure Cases

- The Newton grid is independently checked in ordinary monomial and
  binomial bases, including large primes and p=c+1. Holding t=1 instead
  destroys rank: varying the auxiliary scale is essential.
- On all15,625 lifted inputs in an actual UT3 control, each full oracle
  label class is exactly a coset of H_F. Labels come from the ORIGINAL
  group cosets, constructed independently in matrix coordinates, not
  from the desired lifted relation. This is a finite falsifier, not an
  algorithm or hardness claim.
- Nonabelian-normal UT5 controls compare query products and hidden-coset
  differences against independent matrix exponentials at p5, p17 and
  p=2^127-1. The normal-first ordering is checked separately.
- Public compilation succeeds while the hidden-potential fixture is
  replaced by a function that raises immediately. This checks an actual
  implementation boundary, not merely a claim in a docstring.
- With H=N in UT3, the proposed transverse graph conclusion FAILS:
  the tuple oracle has additional collisions. The initial intersection
  recursion is mandatory. Public input checks cannot infer this hidden
  promise from L alone.
- Removing an evaluation point creates an invisible nonzero jet and
  false collisions even when the original oracle hides the trivial
  subgroup. Full injectivity is necessary, not a cosmetic rank check.

The main remaining quantum proof obligation is no longer source
alignment. It is the composition of the mixed central-character
instrument, public controlled actions, all-input diagonal solver and
fresh recursive preparation, followed by abelian recovery and the
original arbitrary-H normalizer recursion. The existing written argument
and finite controls must not be called an independent verification.

## 6. Prior Art, Novelty And Classical Alternatives

[Decker, Ivanyos, Santha and Wocjan](https://arxiv.org/abs/1107.2189)
give strong-base tuple-query reductions from hidden symmetry problems
to HSP, and polynomial function-graph semidirect products. Their
function-graph definition uses abelian domain and value groups. Thus
tuple evaluation and graph-subgroup encoding are established ingredients,
not discoveries of this repository. The proposed additional claim is
the filtered nonabelian homogenization with hidden-subgroup-preserving
dilations and its composition for ordinary nilpotent HSP. A targeted
search does not establish that this combination is new.

[Ivanyos, Sanselme and Santha](https://arxiv.org/abs/0707.1260) already
use automorphism-twisted cancellation for nil-2 HSP.
[Imran and Ivanyos](https://arxiv.org/abs/2304.08376) provide general
central subgroup-state conversion with bounded-prime guarantees and
explain the original-group automorphism obstruction.
[Ivanyos and Santha](https://arxiv.org/abs/1503.09016) supply the
fixed-degree all-input diagonal solver used here. None of these cited
ingredients alone is a new result in this project.

There is no established hard application. Arbitrary random labels can
yield black-box quantum advantages even in already-solved abelian cases;
that is not evidence of Shor-level practical significance. Any proposed
explicit-object application must survive public-circuit, low-degree,
orbit-module and problem-specific classical stabilizer algorithms.
The deterministic oracle lift does not defeat those baselines.

## 7. Reproduction And Next Work

```
python -m pytest -q tests/test_jet_oracle_homogenization.py -W error::RuntimeWarning
python -m theorems.jet_oracle_homogenization --write
```

Use the direct oracle route for the ordinary-f input. Keep the older
state-only construction separately labelled; do not claim direct query
access from mixed-state samples. The next high-value task is an adversarial
whole-descent proof/novelty review, not another polynomial family or
smaller integer resource estimate. General SDE/controller/synthesis work
remains a later mechanical task after that review.

Verification:13 new tests;192 connected Python tests pass in49.31s with
RuntimeWarning fatal. Full cached Lean build --wfail passes3470jobs;
the two new headline axiom guards admit only standard axioms. Syntax,
formal crosscheck, qsearch validation, site checks and live report
generation pass. Full-repository Python tests were not run. All owned
processes are terminal. No Git, CLI/UI or central-admission changes.
