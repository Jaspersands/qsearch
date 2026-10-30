# What Remains After Classical Native Search

30 October 2026. Hubble's focused adversarial review, retained after the
general classical-search result in INVERSE_TRACE_GENERAL_SEARCH.md.
This is not a classical sampling lower bound or a new quantum algorithm.

## Keep The Tasks Separate

The original FULL N=n^2, K=floor(N/8) construction in
EXACT_PREDICATE_CHANNEL.md and BINARY_GS_DECODER.md has an ideal coherent
uniform native sampler, with complete list decoding, cleanup, and the
full list-index projection paid. Its exact native-and-herald probability
is lambda_b*tau^2/P. At n17 the scalar budget uses w173, GS list cap7,
padding P8, and a lower bound exceeding1/9. No extra state-preparation
oracle is licensed by this statement, and no compiled native circuit or
practical quantum advantage follows.

Do not transplant w=floor(.6M), P8 to the shorter classical blocks:
M145,K36 fails that old Johnson-radius condition. The classical partition
is a search reduction; it is not the same quantum sampler analysis.

Arbitrary-target classical SEARCH is now addressed asymptotically.
Classical sampling of the full witness fiber remains unresolved. Useful
native applications and novelty also remain unestablished. These are
separate research questions, not automatic consequences of the search
result or of a deliberately biased classical sampler.

## A Larger Norm Family Still Does Not Cover The Fiber

For a FULL trace-affine native instance, let r=N-K-1 and consider ALL
pairs deg A,deg U<=r satisfying the conic constraints and one-site
exclusions. This allows all polynomial leading normalizations and all
factor allocations, not just the one normalized sampler. Fix one
matching C=cX+d0 with c!=0, and let z count zero-targets.

Put rho=min(1,(2*ceil(sqrt(q))+1)/(q-1)). The paired dual RS code gives
the explicit relative count error majorant

```
eta2 = sum_(t=0..K-1) binom(N,t)*(1-rho)^t*rho^(N-t)
                         *(q^(2*(K-t))-1).
```

This follows by expanding rho^support as a product of
rho+(1-rho)*1_(paired frequency zero). Any t<K prescribed zeros leave
q^(2*(K-t))-1 nonzero paired dual words. Never clip eta2 to one.
The total number of lifts is at most
q^(N-2K)*(1-1/q)^z*(1+eta2).

Every nonzero output has the distinct pair U and U+A. For odd N the
possible zero-output exception is absent: A=0 would force U=P', but
deg P'=N-1>r. Hence divide the lift-count upper bound by two to bound
distinct outputs.

If the binary span of alpha_i-alpha_1 has dimension d, the number of
compatible nonzero slopes is m=2^(n-d)-1_(b constant), when compatibility
is consistent. Offsets of equal trace do not add another q/2 factor:
d0'-d0=t^2+t and U'=U+tA identify their witness sets. If the full native
fiber has size at least q^(N-K)*2^(-N)*(1-eta_native), the fraction of
that fiber in the union of ALL these full-support norm families is at most

```
min(1, (m/2)*2^N*q^(-K)*(1-1/q)^z
             *(1+eta2)/(1-eta_native)).
```

For the existing n17 basis-bit8 target, d9,m256,z256. Parent replay
with conservative exact rational bounds gives eta2<2^-941,
eta_native<2^-1291, fixed-model mass<2^-324, and union mass<2^-316.
The native error used here is the safe pointwise bound
(q^K-1)*((2*ceil(sqrt(q))+1)/q)^(N-K+1), not an empirical estimate.

This support bound does NOT cover zero-extended blocks, disjoint-block
composition, arbitrary postprocessing, or every classical algorithm.
It explains why simply randomizing this norm family's scalar or slope
does not produce a uniform native sampler. It must not be promoted to a
quantum/classical sampling separation.

## Next Decisive Questions

1. Can a classical exact/approximate sampler reach the full original
   fiber with polynomial certified mixing, coupling or self-reduction
   cost? Search existence is insufficient; conditionals and distributions
   must retain the same input and all costs.
2. Does exact native uniform sampling give a useful reduction to a
   recognized problem? Do not substitute a bespoke oracle separation.
3. Does the known coherent coding/filtering literature already subsume
   the ideal sampler? A literature and reduction comparison is higher
   priority than hardware wiring or another finite witness campaign.

No new backend is justified until one of these questions has a concrete,
falsifiable route. The main result of this round is elimination of a
search-hardness rationale, not an affirmative Shor-level discovery.
