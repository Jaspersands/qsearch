# Evenly spaced Gaudin branches: classical sampling audit

2026-11-12. Scoped independent classical review. No Git, network, API,
code, new numerical control, or sweep. Interpreter, if required, is
`/opt/anaconda3/bin/python`. The joint-gap question is assigned elsewhere
and is not resolved here.

## Finding

Neither efficient charge/root tracking nor the inspected determinant and
MPS formulas presently supply a uniform polynomial computational-basis
sampler for EVERY half-filled branch of the stated evenly spaced family.
This is an unclosed output obligation, not a sampling lower bound. The
current source does not even prove uniform polynomial native charge
tracking, and granting that operation would still leave conditional
Born probabilities or another fully accounted sampling method to supply.

The strongest verified formulas pay specified amplitudes, on-shell global
norms and certain unconditioned local observables under their actual data
and precision assumptions. The strongest unconditional native sampler
identified here is the trivial product-label sampler in an explicit weak
window below. Direct exponential-dimension diagonalization and amplitude
enumeration remain the general finite-resource comparators.

There is one new exact SAME-family falsifier: deleting the first site from
the Gaudin norm matrix gives the wrong empty-prefix norm already on the
`N=4`, `b=(0,1,0,1)` branch for every sufficiently small positive `t`.
It is proved symbolically below; no numerical evidence is needed.

## Contract and sources actually checked

Input is even `N`, an ordinary bit label `b` of weight `N/2`, rational
`t in [0,1]`, and the desired error. Set `eps_i=i/N`, physical `g=t/N`,
and

```
Q_i(t) = n_i + (t/2) sum_(j!=i) (SWAP_ij-I)/(i-j).
```

The target is the joint branch continuously followed from `b` at zero.
No roots, intermediate eigenvalues, prefix probabilities, or eigenstate
oracle are supplied. The classical output considered here is a bit string
whose distribution approximates computational-basis measurement of that
branch. Classical computation of its eigenvalues is a different output.

Read `STATE.md` top, the supplied
`audits/api_inputs/2026-11-12-gaudin-picket/contract.md`,
`GAUDIN_JOINT_CHARGE_TRAVERSAL.md`,
`RATIONAL_GAUDIN_PREFIX_ADMISSION.md`, and the parent's new
`GAUDIN_PICKET_FENCE_ADMISSION.md`. Source checks used:

* `audits/sources/gaudin_gap_geometry/lutz_v3.txt`, main RG discussion
  around physical lines 270-365 and the actual Section G discussion
  around 1258-1310. The source explicitly leaves classical polynomial
  complexity and uniform convergence/conditioning guarantees open.
* `audits/sources/bethe_prefix_admission/gaudin.txt`, Eqs. 49-50 at
  584-610, Eqs. 66-67 at 704-738, and Eqs. 68-69 and discussion at
  778-805. These are the eigenvalue-based amplitude, common-state dual,
  normalization, and local-form-factor results.
* `audits/sources/bethe_prefix_admission/f_basis.txt`, the explicit
  `2^M` MPS bond dimension around 669-676 and the subset Gram/Cholesky
  resource discussion at 1352-1366.
* The existing independent formula audit
  `audits/reviews/2026-11-07-bethe-prefix-sources.md` and exact two-root
  derivation in `RATIONAL_GAUDIN_PREFIX_ADMISSION.md`. The earlier
  irregular-site control was not rerun or assumed to be an instance of
  this new family.

## What the charge tracker establishes, and what it does not

For this parameterization the eigenvalue equations are

```
F_i(q,t) = q_i^2-q_i + (t/2) sum_(j!=i)(q_i-q_j)/(i-j) = 0,
sum_i q_i = N/2.
```

A Taylor/Newton continuation step evaluates a polynomial-size system
and solves a polynomial-size linear system. That bounds the work PER
step. A uniform native algorithm still needs a certified step count,
conditioning/precision, and assurance that continuation retains the
branch selected by `b`. Section G's practical method compares many
solutions to detect duplicated branches; its all-start numerical audit
is not a polynomial routine for one arbitrary supplied branch. The
source explicitly reports no formal polynomial complexity guarantee.

Even if all that tracking were paid, the vector `q(t)` would identify
the state but would not yet sample its Born law. No construction here
turns a polynomial coordinate description into a sampler merely because
the description is unique. Root conversion can itself be singular or
ill-conditioned; real charges do not imply that every rapidity remains
real and separated along the whole path.

The amplitude formulas are stronger than a claim that explicit roots
are always required. Claeys et al. Eq. 50 writes each specified Cauchy
permanent amplitude as a determinant whose diagonal depends only on
the eigenvalue-based sums `Lambda_i=sum_a 1/(eps_i-v_a)`. Thus suitable
charge data can avoid extracting all rapidities for that operation.
This does not evaluate an extensive sum of squared amplitudes over
unspecified sites. Nor does a polynomial determinant arithmetic count
by itself establish a uniform precision bound for the normalized
probabilities of every branch.

## Paid classical formulas and remaining readout cost

For roots `v_1,...,v_M` and occupied set `S`, the Bethe coefficient is

```
A(S)=per[1/(v_a-eps_i)]_(a=1..M, i in S).
```

For regular distinct root/site data, Borchardt's identity or the
eigenvalue-based determinant pays each specified coefficient. With the
earlier rational root-input contract, its exact rational-bit cost is
polynomial. The present native input supplies neither those rationals
nor a uniform root/charge approximation guarantee; the earlier result
must retain that distinction.

The Gaudin determinant pays the FULL on-shell norm. Normal/dual
determinants also pay normalization when both descriptions are of the
SAME eigenstate with the normalization ratio accounted for. The source
does not provide a compatible on-shell/common-dual description after
every extensive string of occupation and empty-site projections.
An empty-site projection deletes a site but retains the old roots;
these generally cease to satisfy the new Bethe equations. An occupied
projection additionally sums states with different omitted roots.
Solving new Bethe equations would change this conditional state.

For a specified one-site marginal, differentiating the on-shell equations
and using Hellmann--Feynman gives a Gaudin-matrix linear solve, as already
proved in the prefix note. Local form-factor formulas provide further
specified observables. These are useful classical baselines under paid
data/conditioning; they are not arbitrary conditional marginals after
earlier measurements. Higher energy derivatives are response quantities,
not automatically joint occupation moments.

Let `Z_z` be the squared norm after a computational prefix `z`. A genuine
uniform routine for the ratios `Z_(z1)/Z_z` would immediately yield a
classical sequential sampler. Conditional error `O(eta/N)` per visited
prefix gives total variation error `O(eta)` by coupling. Zero-weight
prefixes are never visited; tiny unnormalized prefix weights still require
the requisite conditional accuracy. Fixed additive precision for every
unnormalized norm is not sufficient. Exhaustive summation of the
`binomial(N,N/2)` amplitudes pays these quantities with exponential work.

Neither a single-amplitude oracle plus a normalization nor a Metropolis
proposal alone closes this gap. Rejection needs a polynomial envelope/
acceptance bound; a Markov-chain construction needs its actual mixing
and initialization bound for every branch. No such bound is supplied
by the inspected formulas. This observation is not a no-go theorem for
either method.

## SAME-family two-root prefix counterexample

Use the spin convention in the contract. For arbitrary sites and physical
coupling `g`, the rational Bethe vector is

```
Psi = B(v_1) B(v_2) |0>,
B(v)=sum_i sigma_i^+/(v-eps_i),
sum_i 1/(v_a-eps_i) - 2 sum_(b!=a)1/(v_a-v_b) = 2/g.       (1)
```

The sign and factor in (1) agree with these charges. Indeed

```
sum_i eps_i Q_i
 = sum_i eps_i n_i + (g/2) S^+S^-
   - (g/2) M(N-M+1).
```

The last term is scalar in the fixed sector. Commuting the first two
terms through the `B` operators gives unwanted-vector coefficients
`-1+(g/2)[sum_i 1/(v_a-eps_i)-2 sum_(b!=a)1/(v_a-v_b)]`.
Their vanishing gives (1), and the standard commuting-charge calculation
gives `q_i=(g/2)sum_a 1/(v_a-eps_i)`. In particular roots approaching
specified occupied sites with displacement `g/2` reproduce the initial
bit label.

For real distinct roots put `a_i=1/(v_1-eps_i)`,
`b_i=1/(v_2-eps_i)`, `d=v_2-v_1`. For any retained site set `U` put
`A_U=sum_U a_i^2`, `B_U=sum_U b_i^2`, `K_U=sum_U a_i b_i`.
The exact physical squared norm and proposed deleted-site matrix are

```
Z_U = sum_(i<j in U)(a_i b_j+a_j b_i)^2
    = A_U B_U + K_U^2 - 2(A_U+B_U-2K_U)/d^2,

G_U = [ A_U-2/d^2    2/d^2     ],
      [   2/d^2      B_U-2/d^2 ],

Z_U-det(G_U) = K_U(K_U+4/d^2).                         (2)
```

Here `a_i-b_i=d a_i b_i` proves the displayed reduction of the quartic
sum. Subtracting the two equations (1) gives `K_full=-4/d^2`, so the
FULL on-shell norm determinant is correct. If a single site with energy
`e` is deleted, write `c=1/[(v_1-e)(v_2-e)]`. Then
`K_U=-4/d^2-c`, and (2) becomes the exact identity

```
Z_U-det(G_U)
 = c(4/d^2+c)
 = (v_1+v_2-2e)^2 /
   [(v_2-v_1)^2 (v_1-e)^2 (v_2-e)^2].                 (3)
```

Now take the actual new input family with `N=4`,
`eps=(1/4,1/2,3/4,1)`, `b=(0,1,0,1)`, and `g=t/4`.
Set `v_1=1/2+g u_1`, `v_2=1+g u_2` in (1), and multiply both
equations by `g`. At `g=0` the equations are `1/u_a=2`, with
invertible diagonal Jacobian `-1/u_a^2` at `u_1=u_2=1/2`.
The real analytic implicit-function theorem therefore gives the actual
on-shell branch, for all sufficiently small positive `t`, with

```
v_1=1/2+t/8+O(t^2),
v_2=1+t/8+O(t^2).
```

The Bethe vector is nonzero: its leading product component is the
specified occupation `24`. The roots are real, distinct, and avoid
all sites for sufficiently small positive `t`. Thus no singular-root,
complex-adjoint, or branch-label assumption is hidden in this example.

Project the FIRST site EMPTY, so `e=1/4` and `U={2,3,4}`. In (3) the
numerator tends to `1`, and the denominator tends to

```
(1/2)^2 (1/4)^2 (3/4)^2 = 9/1024.
```

Hence the discrepancy tends to `1024/9` and is strictly positive for
every sufficiently small positive `t`. The direct global-norm deletion
shortcut is therefore false inside the exact equally spaced, half-filled,
ordinary-label contract. Its relative error can become small as `t` tends
to zero; this algebraic falsifier is not a sampling lower bound or a claim
that approximate sampling is difficult in that weak regime.

## Tensor-network comparison

The inspected Bethe MPS source explicitly has bond dimension `2^M`.
Its long-unitary construction stores subset Gram matrices with growing
binomial blocks and performs their Cholesky factorizations. At half
filling those written constructions have exponential resources. They
concern XXZ Bethe circuits; a rational/Gaudin limit does not automatically
provide a new polynomial approximation theorem.

One can see the basic root-subset cost directly, without importing a
cross-model claim: for a site bipartition, expand each
`B(v_a)=B_left(v_a)+B_right(v_a)`. The product has `2^M` terms indexed
by which roots are assigned to the left. This is a valid exact tensor
representation, not a polynomial bond bound. No all-branch bound on the
discarded Schmidt weight at polynomial bond dimension was found in the
inspected material. The literal exponential representation is not a lower
bound on the best exact or approximate representation. Section G's
central-spin entropy numerics also concern a different geometry and do
not resolve the present picket-fence approximation problem.

## Native weak-window classical control

The parent's elementary perturbative bounds are correct with the stated
window. Let `H=H_(N-1)` and
`h_i=H_(i-1)+H_(N-i)<=2H`. Then

```
||Q_i(t)-n_i|| <= t h_i <= 2tH.
```

For `0<=t<=1/(8H)`, each charge's two spectral bands lie within distance
`1/4` of zero or one. Their commuting band projectors vary continuously;
products indexed by bit strings have constant rank, hence rank one from
their value at zero. Same-weight distinct labels differ at at least two
coordinates. Each differing charge differs by at least `1/2`, giving
squared joint separation at least `1/2` throughout this window.

Also `||Q_i'(t)||<=2H`, so the joint-branch derivative estimate in
parallel gauge gives

```
||psi_b'(t)|| <= 2 sqrt(2N) H =: C_N,
TD(|psi_b(t)>,|b>) <= C_N t.
```

Thus the PRODUCT STATE itself meets trace error `eta` for
`t<=min{1/(8H), eta/C_N}`. For the classical sampling output there is
a slightly stronger direct conclusion:

```
TV(delta_b, Born(psi_b(t)))
  = 1-|<b|psi_b(t)>|^2
  = TD(|b>,|psi_b(t)>)^2
  <= C_N^2 t^2.
```

Returning the input string `b` is consequently a uniform polynomial
(indeed linear-output-time) sampler with TV error at most `eta` for
`t<=min{1/(8H), sqrt(eta)/C_N}`. At `t=0` it is exact. These are
sufficient matched regimes; they are not claimed optimal and must not
be extended to `t=1`. Keeping the minimum also covers small `N` and
large error tolerances without silently leaving the derivative window.

## Exact outstanding classical step and claim gates

For the full interval and every half-filled native label, classical
matching would require BOTH a paid way to recover the relevant state
data from `b` and a sampler with a uniform finite clock. An all-prefix
conditional-norm algorithm is one sufficient way to supply the latter;
a rigorously mixing chain, controlled rejection method, or a provably
accurate efficiently contracted tensor representation would be another.
The existing determinant, normalization, and local-observable results do
not supply any of those complete operations. The SAME-family calculation
above specifically blocks reusing the global norm determinant after
site deletion.

Even granting efficient certified native charge tracking, the sampler
step remains open. Conversely, its being open here is not evidence of
hardness and does not establish a quantum separation. The joint-gap
bound, a full classical sampler, a full native quantum algorithm, and
novelty remain unpromoted. No further classical control or sweep is
required for this scoped review.
