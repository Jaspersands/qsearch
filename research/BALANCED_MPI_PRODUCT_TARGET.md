# Balanced MPI: A Conditional Classical Sampling Reduction

## Status

**A classical attack target with a derived average-center transfer bound
(`balanced_mpi_product_target_v2`), exact small-chain detailed-balance
verification, and a bounded native product-target MCMC/mode campaign on the
frozen `center_seed = 20261020` instance—not a polynomial mixing theorem or
dequantization result.**
The argument needs independent review and is not part of the Lean proof.
It does not change the problem or give either solver hidden information.
It does change the source density from the previous pilot when obtaining
the useful native bound; the original pilot is retained as a comparator.

Follow-up: `BALANCED_MPI_HEATBATH_TRAP.md` certifies severe fixed-start
freezing for the naive original-coordinate heat-bath chain on a native
witness. A systematic-basis escape countercheck prevents extending that
conclusion to stronger moves. The product-target transfer still holds;
efficient sampling remains unresolved.

The MPI problem and decoder come from
[Mazumder and Niroula](https://arxiv.org/abs/2610.06753).
The classical-sampling attack is motivated by
[Gil-Fuster et al.](https://arxiv.org/abs/2607.28120), who study MCMC for DQI.
Their finite experiments are not a sampling guarantee for this MPI family.

## Exact Transfer Argument

Fix any public matrix B over Z_N, N>3. Let E be the balanced signed box,
and suppose its syndrome map y -> B^T y is injective. For ternary words y
define the product source amplitudes

```
w_y = (1-t)^((m-|y|)/2) (t/2)^(|y|/2).
G_c(x) = sum_(y in E) w_y exp(2*pi*i*y.(Bx-c)/N).
H_c(x) = sum_(y outside E) w_y exp(2*pi*i*y.(Bx-c)/N).
F_c(x) = G_c(x) + H_c(x)
       = product_i [sqrt(1-t) + sqrt(2*t)*cos(2*pi*((Bx)_i-c_i)/N)].
Z = sum_(y in E) w_y^2; delta = 1-Z.
```

Norms below use the UNIFORM measure on all x in Z_N^n. Syndrome
injectivity gives ||G_c||^2=Z for every c, regardless of matrix rank.
The quantum candidate's distribution is P_E,c(x) proportional to |G_c(x)|^2.
Define the product-weight target P_prod,c(x) proportional to |F_c(x)|^2.
For 0<t<1/3 all product factors are positive, so this distribution exists
for every center vector. Its log weight costs m scalar factor evaluations
after the public matrix product. This is not a bound on sampling cost.

Let D(c)=||H_c||^2. Projecting G_c onto the span of F_c shows that the pure
state trace distance, and hence the measured total-variation distance, obeys

```
TV(P_E,c, P_prod,c) <= min(1, sqrt(D(c)/Z)).
```

Indeed the orthogonal component of G_c is the negative of that of H_c,
whose norm is at most ||H_c||. No pointwise assumption D(c)<=delta is made.

Now draw every c_i independently and uniformly from Z_N. Distinct ternary
words give different characters of c, including when N is composite.
Character orthogonality removes all off-diagonal terms, so

```
E_c D(c) = sum_(y outside E) w_y^2 = delta.
E_c TV(P_E,c, P_prod,c) <= sqrt(delta/Z).
Pr_c[TV > epsilon] <= min(1, delta/(Z*epsilon^2)).
```

This uses independence of the FULL center vector, not a planted-center
model or randomization within an optimizer-code coset.

## Conditional Search Consequence

Assume a classical algorithm samples a law Q_c with center-averaged
TV(Q_c,P_prod,c)<=eta. No such algorithm is supplied here. For the SAME
public problem, any score event A satisfies

```
Pr_(c,x~Q_c)[A] >= E_c P_E,c(A) - sqrt(delta/Z) - eta.
```

If the readout guard holds, the source certificate gives a constant
center-independent mean mu. For the score fraction in [-1,1] and tau<mu,
P_E,c[score>=tau] >= (mu-tau)/(1-tau). Combining gives a rigorous
conditional search probability averaged over centers. It does not imply
success on every center, or high success probability for a particular
fixed center after repeated runs.

For n/m -> alpha and fixed 0<t<min(alpha,1/3), both excluded count tails
are exponentially small by binomial concentration. Thus this simpler
product target approximates this pilot exponentially well on average.
This is a sampling reduction, not a mixing-time statement.

## Native Certificate

The fixed comparison uses m=6000,n=420,cap=209,N=8191, but t=1/20 rather
than the original 13/200. The problem, decoder and score threshold remain
unchanged. Exact multinomial and outward-root arithmetic give:

- Discarded source mass about 0.00000317978164.
- Center-averaged target TV below 0.0018.
- The truncated quantum mean above 0.308.
- Conditional joint probability above 0.0089 of score>=0.3 if a classical
  sampler achieves center-averaged TV error at most 0.001.

For the original t=13/200 pilot, the source tail is too large for this
transfer bound to prove a positive search probability at threshold 0.3.
Do not claim to have classically matched its mean above 0.342.

## Fast Line Conditionals With Controlled Truncation

The log weight has more structure than a generic nonlinear score. Set

```
a = sqrt(1-t), b = sqrt(2*t), d = sqrt(1-3*t),
r = b/(a+d), A = (a+d)/2.
a+b*cos(theta) = A*(1+r*exp(i*theta))*(1+r*exp(-i*theta)).
log(weight) = 2*m*log(A)
  + 4*sum_i sum_(k>=1) (-1)^(k+1)*r^k*cos(k*theta_i)/k.
```

Here 0<r<1. Keeping k<=L changes the total log weight by at most

```
epsilon_L = 4*m*r^(L+1)/((L+1)*(1-r)).
```

This is UNIFORM over assignments and centers. Consequently the normalized
full and truncated densities have TV at most exp(2*epsilon_L)-1.
For 2*epsilon_L<1 we certify the conservative rational upper bound
2*epsilon_L/(1-2*epsilon_L), using exp(u)<=1/(1-u). This is a bound
between two stationary densities, not a convergence result for a chain.

## Small Detailed-Balance Control And Matched Native Product-Target Campaign

In `balanced_mpi_product_target_v2`, we implement exact categorical line
sampling (`categorical_line_probabilities`, `sample_categorical_step`),
verify exact detailed balance and empirical stationary histograms on a
49-state control (`bits=3, N=7, m=4, n=2`, where both original-basis and
systematic-basis random-scan transition matrices obey detailed balance to
`< 1e-17` and a 14,000-sample systematic heat-bath chain matches the
stationary law to TV `0.024675`), and execute a matched 4-chain classical
campaign (`native_product_target_campaign`) on the frozen native `m=6000,
n=420, N=8191` instance (`center_seed = 20261020`, `t = 1/20`, `L = 9`):

| Chain / Portfolio | Basis & Move Set | Line FFTs | Nontrivial Moves | First Exit Step | Initial Cosine | Best Mean Cosine | Best Product Log-Weight |
|---|---|---|---|---|---|---|---|
| `cold_original_coordinate_heatbath_from_pinned_I0` | Original $B$ columns ($\beta=1.0$) | 60 | 0 | `None` | `0.074024` | `0.074024` | `-362.6162` |
| `systematic_basis_heatbath_I0` | Systematic $G_{I_0}$ columns ($\beta=1.0$) | 80 | 9 | `1` | `0.074024` | `0.110937` | `-216.0679` |
| `two_replica_tempered_systematic_chain_I0` | Systematic $G_{I_0}$, $\beta \in \{0.2, 1.0\}$ (3/6 swaps accepted) | 120 | `[18, 5]` | `1` | `0.074024` | `0.109423` | `-218.9105` |
| `alternating_systematic_basis_product_mode_search_I0_I1` | Alternating $G_{I_0} \to G_{I_1}$ mode search (2 basis switches) | 240 | 7 | `1` | `0.074024` | **`0.117339`** | **`-188.0071`** |

All saved 420-coordinate assignments are independently replayed via both
explicit matrix multiplication and `fast_public_matvec`. None of the bounded
chains reaches the `0.3` cosine threshold (`any_chain_reached_0_3_threshold: False`),
and no mixing-time or dequantization claim is made.

## Attempts To Break The Argument

1. **Tiny discarded source mass is not a worst-case target guarantee.**
   An abstract all-ones one-column map with m=400,N=7,t=1/40000 and E={0}
   has discarded mass below 0.01 but a fixed-center target TV above 0.5.
   Coherent collisions amplify the discarded component. This is a
   counterexample to a general inference, NOT a log-Cauchy MPI instance
   and NOT a no-go theorem for its worst-case centers.
2. **Codeword masking cannot supply independent centers.**
   Replacing c by c+Bz translates both target laws by x -> x+z, leaving
   their TV and D(c) unchanged. The countercontrol verifies the permutation.
   This familiar symmetry does not turn the average-center result into
   a worst-case result.
3. **An evaluable positive density need not be easy to sample.**
   Dense modular interactions can make single-coordinate chains mix
   slowly. Positivity and detailed balance alone establish no useful
   finite-time approximation guarantee.
4. **The target is not an ordinary exp(beta*score) Gibbs law.**
   It is the square of a product of affine cosine factors. Replacing its
   log weight by a first-order cosine expansion changes the distribution
   and needs a separate error bound.
5. **Mean, tail, sampling and optimization are different claims.**
   A single successful native assignment would be a useful search result
   but would not establish sampling accuracy or asymptotic dequantization.

## Reproduction

```
python theorems/balanced_mpi_product_target.py
python -m pytest -q tests/test_balanced_mpi_product_target.py -W error::RuntimeWarning
```

The report is `research/classical_baselines/balanced_mpi_product_target.json`.
Its native inequalities use exact rational bounds. Exhaustive prime and
composite controls use floating amplitudes solely to test identities.
Enumeration is explicitly capped and is not exposed as a native sampler.
