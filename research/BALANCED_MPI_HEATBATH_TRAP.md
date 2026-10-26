# Balanced MPI: A Certified Coordinate Heat-Bath Trap

## Scope

This is a finite, fixed-start mixing obstruction for one specific classical
sampler. It is not classical hardness, a typical-start theorem, an
asymptotic lower bound, or evidence of a quantum speedup.

The producer takes the existing native classical portfolio's saved assignment
without searching for a different one. It checks the original-coordinate
heat-bath chain for the positive product target in
`BALANCED_MPI_PRODUCT_TARGET.md`, at t=1/20.

The existing literature motivates trying classical sampling but does not
supply a mixing guarantee here. In particular, the search-time diagnostics
called mixing times in parts of
[Gil-Fuster et al.](https://arxiv.org/abs/2607.28120) are not the same
quantity as total-variation mixing from every starting state.
[Mazumder and Niroula](https://arxiv.org/abs/2610.06753) also use systematic
and updated information-set directions, not just the original coordinates.
Our original-coordinate obstruction does not cover those moves.

## Fixed Input And Chain

The public native instance has m=6000,n=420,N=8191, with field supports
encoded 0..5999 and evaluations 6000..6419. The centers and the 420-entry
assignment are stored in the new artifact, along with field presentation
and source-artifact provenance. The assignment is inherited from the
other agent's systematic-basis cosine portfolio and has mean cosine
approximately 0.1166489027. It does not reach the target 0.3.

Write the unnormalized product density as

```
W(x) = product_i [sqrt(1-t)+sqrt(2*t)*cos(2*pi*((Bx)_i-c_i)/N)]^2.
pi(x) = W(x) / sum_z W(z).
```

One step of the random-scan chain picks an original coordinate j and
draws s in Z_N proportional to W(x+s*e_j). It then replaces x by x+s*e_j.
Strict positivity makes this an irreducible heat-bath chain with stationary
law pi. A step here means ONE coordinate update, not a full sweep.

## Exit Certificate

Let ell_j(s)=log W(x+s*e_j). The conditional exit probability satisfies

```
q_j = sum_(s!=0) exp(ell_j(s)-ell_j(0))
      / [1+sum_(s!=0) exp(ell_j(s)-ell_j(0))]
    <= (N-1)*exp(max_(s!=0)[ell_j(s)-ell_j(0)]).
```

The nine-harmonic approximation changes every log weight by at most
epsilon=4*m*r^10/(10*(1-r)), with r defined in the preceding product-target
note. Hence its log-difference error is at most 2*epsilon.

The producer computes all 8191 values of each of the 420 coordinate lines
using Arb complex-ball DFTs at 96-bit precision. Coefficients, roots of
unity, transforms and comparisons use directed interval bounds. The
previous floating FFT is not used as proof evidence.

For every coordinate, the outward upper bound on log(q_j) is below
-253.1492. In particular, the more conservative predeclared claim
q_j <= 2^-256 holds for all 420 coordinates. This includes both analytic
harmonic truncation and interval arithmetic error.

## Stationary Mass Certificate

A large self-loop is not enough: the state could carry almost all stationary
mass. We separately bound pi(x).

Let a=sqrt(1-t), d=sqrt(1-3*t), A=(a+d)/2 and r=sqrt(2*t)/(a+d).
Every row map x -> (Bx)_i is surjective onto Z_N; the producer verifies
gcd(N,B_i1,...,B_in)=1 for all rows. No full-column-rank assumption is needed.
Since N is odd,

```
product_(k=0)^(N-1) (1+r*exp(2*pi*i*k/N)) = 1+r^N.
E_uniform_x log W(x) = 2*m*log(A)+(4*m/N)*log(1+r^N)
                    >= 2*m*log(A).
```

Jensen therefore gives sum_x W(x) >= N^n*A^(2*m). The interval evaluation
of the starting state's log weight, including harmonic error, proves

```
log pi(x) <= log W(x)-2*m*log(A)-n*log(N),
pi(x) <= 2^-256.
```

The odd-order and row-surjectivity conditions are essential to this version
of the bound and are checked, not inferred from a matrix's dimensions.

## Finite-Time Consequence

As long as the chain stays at x, each update exits with probability at most
2^-256. Thus for T=2^250 updates,

```
P^T(x,{x}) >= 1-T*2^-256 = 63/64,
TV(P^T(x,.), pi) >= P^T(x,{x})-pi(x)
                 >= 63/64 - 2^-256 > 0.98.
```

This is a certified finite calculation plus the displayed elementary
argument. It is not a Lean formalization, and independent review remains
appropriate. No Markov chain was simulated for that enormous number of steps.

## A Stronger-Basis Countercheck

The first 420 rows give an invertible information set. A complete floating
diagnostic of its 420 systematic directions found a substantially less
suppressed move at column 238, displacement 2539. Selection of this
direction was exploratory; the saved lower bound comes from a fresh
interval DFT replay of that fixed move, not its floating estimate.

The exact matrix identity for the systematic inverse is checked. If the
move's log-weight gain is at least g, its one-direction heat bath exits
with probability at least exp(g)/(1+exp(g)); all other nonzero moves only
increase that exit probability. The interval certificate gives a bound
greater than 2^-17. Thus the systematic random-scan chain exits this
particular state in expected time at most 420*2^17 coordinate updates.

This is an UPPER bound on first-exit time, not a bound on mixing or on
finding score-0.3 assignments. It explicitly blocks extending the
2^250-step original-coordinate conclusion to the systematic chain.

## Attempts To Generalize Incorrectly

- The starting assignment is a particular polynomial-time-found witness.
  No probability that a random-start chain enters this state is proved.
- All original-coordinate lines were checked, not all directions in the
  vector space. A change of basis changes the Markov chain.
- Tempering can leave the cold distribution, so the cold-chain self-loop
  bound says nothing by itself about its round-trip or mixing time.
- Block moves, changing information sets and nonlocal proposals remain open.
- A single finite instance, even with a large bound, proves no asymptotic
  exponential-time statement.
- This obstructs sampling from this product target by this chain, not
  finding score-0.3 assignments by arbitrary classical methods.

## Reproduction

```
python theorems/balanced_mpi_heatbath_trap.py
python -m pytest -q tests/test_balanced_mpi_heatbath_trap.py -W error::RuntimeWarning
```

The report is `research/classical_baselines/balanced_mpi_heatbath_trap.json`.
The input is captured in the report. A rerun's default input is the current
portfolio artifact; changing that witness changes the question, and the
producer records its exact provenance.
