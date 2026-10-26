# What the subfield search attack does not sample

**Proved deduction about the stated algorithms, not a classical sampling
lower bound.** The subfield solvers establish search results. Their output
laws remain far from the quantum algorithm's uniform native witness law,
even if unused coordinates are randomized and the correction positions
are chosen adaptively. This strengthens the simpler fixed-zero observation
in SUBFIELD_EXTENSION_ATTACK.md.

Write q=2^n and let U_b be the uniform law on all native witnesses for the
given points and bits. Let Z be the zero-target coordinates. If J is any
fixed subset of Z of size L, and E is a subset of the accepted zero set,
the standard fiber estimate gives

    Pr_(U_b)[x_i in E for every i in J]
       <= (2|E|/q)^L * (1+eta_(N-L))/(1-eta_N),       (1)

provided eta_N<1. Here eta_m=(q^K-1)*beta^(m-K+1), with
beta=(1+2*sqrt(q))/q, is the same conservative MDS/Fourier estimate for
any m remaining public columns and any syndrome.

To check every normalization: fix values on J. The remaining count is
at most (q/2)^(N-L)*q^(-K)*(1+eta_(N-L)), independently of the resulting
syndrome. There are |E|^L assignments on J. Divide by the full native
count, at least (q/2)^N*q^(-K)*(1-eta_N). This proves (1) without assuming
coordinate independence. A union bound then yields

    Pr_(U_b)[at least L zero-target coordinates lie in E]
       <= binom(|Z|,L)*(2|E|/q)^L
          * (1+eta_(N-L))/(1-eta_N).                 (2)

## Even degree

For method A, E=k=F_Q, q=Q^2. Every output has at least r>=K correction
coordinates in k. This remains true if the free basis, buffers, unused
positions and one-target values are randomized. Taking L=K in (2)
therefore bounds the uniform probability of the event that contains every
output by

    binom(|Z|,K)*(2/Q)^K*(1+eta_(N-K))/(1-eta_N).

At N=n^2, K=floor(N/8), this is 2^(-Omega(n^3)) for even n. The
total-variation distance of any such algorithm's output law from U_b is
at least one minus this bound.

## Relative degree three

For methods B/C with e=3, put

    E={0} union {1/v : v!=0, Tr_(F/k)(v)=0}.

This set has exactly Q^2=q/Q elements. Every selected zero line u*k lies
in E, so every output has at least 3K zero-target coordinates in E. Taking
L=3K in (2) gives the bound

    binom(|Z|,3K)*(2/Q)^(3K)
       *(1+eta_(N-3K))/(1-eta_N).

This too is 2^(-Omega(n^3)) at the native scaling. In particular, changing
which 3K coordinates perform the correction cannot make this algorithm
approximately uniform. The remaining length N-3K is about 5K, so the
displayed conservative fiber error is negligible; no estimate is used
outside its valid rate range.

## Self-attack and consequence

The event used in (2) is efficiently recognizable from the original
witness and supplied field. This proves a distributional distinction for
these algorithms; it says nothing about the running time of a different
classical sampler. It also does not require search algorithms to be
uniform: all their verified witnesses remain fully legitimate answers to
the user's native search problem.

The quantum full-list algorithm has exact conditional uniformity, by
EXACT_PATTERN_CHANNEL.md. Thus an exact or approximate native sampling
question remains after search is classically solved on these families.
Calling that a sampling advantage would require an additional classical
complexity argument. The strongest falsifier of the present limitation
would be a modification whose outputs no longer necessarily contain the
specified number of coordinates in E; it would then need a fresh analysis,
and (2) would not constrain it automatically.
