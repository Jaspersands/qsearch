# Gibbs obstruction and the search question

## Independently reconstructed result and its exact scope

**Proved deduction.** The uniform fiber count follows directly by additive
character orthogonality. Expanding the MDS weight enumerator gives the
positive bound

    E=sum_(t=0)^(K-1) binom(N,t)(1-beta)^t beta^(N-t)(q^(K-t)-1)
      <= q^K [beta+(1-beta)/q]^N.

For beta<= (1+2*ceil(sqrt(q)))/q, E vanishes at fixed K/N<1/2
in the native scaling. It holds for every target and syndrome. Consequently
pi_M proportional to M^(-defects) has full-witness probability at least
(1-E)/(1+E)*(M/(M+1))^N. For M>=N this is bounded below by a constant
once E is small. Counting is not witness sampling.

I also reconstructed the stated small-bit-block obstruction. The scalar
two-pole character sum has bound 2*sqrt(q)+3 including the two totalized
endpoints; adding a nonzero linear character introduces a third simple
pole and gives 4*sqrt(q)+2. The Artin–Schreier genera are one and two.
The simple poles rule out an Artin–Schreier coboundary. These constants
agree with the [primary curve bound](https://arxiv.org/abs/1409.3694).

Combining those scalar correlations with the MDS enumerator bounds the
average exit probability from a uniformly chosen full solution for each
fixed nonzero codeword displacement. Every displacement has support at
least K+1. A fixed k-bit heat-bath block has at most 2^k-1 nontrivial
displacements, so a union bound gives exponentially small average escape
when k is small and fixed. Stationarity then gives the stated worst-start
mixing lower bound. The stationary-flow argument remains valid even though
the distribution conditioned on not having exited need not stay uniform.

The starting law of this lower-bound argument is pi_M conditioned on full
solutions. It has already solved search. The argument does not show that
an unconditioned uniform codeword takes a long time to find its first
solution; sticky solutions could help preserve hits. It also does not
cover state-dependent block selection or parallel tempering automatically.

## Constructive attack rather than another barrier

**Proved algorithmic deduction:** CLASSICAL_SAMPLING.md gives a direct
latent-constraint sampler, specialized to this same native input. For
fixed rate 1/8 and fixed 1<=M<15, it samples pi_M to exponentially small
total-variation error in polynomial expected time, with an explicit
polynomial clock/ABORT conversion. It uses only field arithmetic, trace
hyperplane draws and invertible MDS projections. It does not run this
heat-bath chain. This is an instance of the known Prange-mixture idea,
not a new general sampling framework.

**Self-attack:** that total-variation statement does not preserve an
exponentially rare full-witness event. In fact the truncated sampler's
full success is at most (1+e_b)2^-K, exactly the systematic-root proposal's
success. At M>=N the omitted active sets are typical. Direct sampling of the
TRUNCATED law remains polynomial; only rejecting untruncated latent draws
would incur the rare-conditioning cost. The resulting law is then too far
from the desired low-temperature law. Thus the sampler neither dequantizes
full search nor contradicts the worst-start obstruction.

The exact tilted-binomial calculation now in CLASSICAL_SAMPLING.md also
gives the first-hitting law for independent trials of this sampler. At
8<M<15 it is exponentially accurate in TV yet exponentially suppresses
the rare witness event relative to the true Gibbs law. This is a precise
search limitation for the constructed sampler, not a claim about the local
chain or arbitrary classical algorithms.

## Unresolved constructive obligation

No polynomial uniform-start first-hitting theorem has been obtained for
the native small-block chain. Nor has this review proved a first-hitting
lower bound. A proof would have to control the law before the first hit,
not import the solution-conditioned escape estimate. Empirical score
improvement, detailed balance and constant stationary success are not
substitutes for this control.

The more decisive classical target is a paid sampler for the near-complete
latent constraint sets typical at M>=N, or an explicit reconstruction
method that bypasses Gibbs sampling. An assumed efficient conditional
sampler at that point already contains most of the original search problem.

## A concrete search bypass on broad native families

**Later proved algorithmic deduction:** SUBFIELD_EXTENSION_ATTACK.md now
gives a polynomial witness solver for arbitrary supplied distinct points
when n is even, n>=8, and the target has at least 2K zeros, and when
3 divides n, n>=6, and it has at least 3K zeros. The latter algorithm is
deterministic; the former pays explicitly for its coset samples. Uniform targets
meet these conditions with overwhelming probability. The algorithm uses
accepted subfield directions and linear algebra, with every sampling cost
charged; it never needs a Gibbs chain to mix or hit.

Thus the worst-start Gibbs obstruction can coexist with polynomial native
search on these entire families. It cannot establish quantum advantage
there, even in the low-temperature regime with constant stationary witness
probability. This is stronger evidence than another nearby local-chain
barrier. It still does not settle uniform-start hitting for the specified
chain, nor classical search outside the new algorithms' degree and target
conditions, including prime-degree and one-heavy instances.
