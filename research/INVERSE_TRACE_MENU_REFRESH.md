# Independent Coordinate Menus Do Not Repair Native Sampling

29 October 2026. Local deduction, independently AI-reviewed by Popper;
not human-reviewed, kernel-formalized, or claimed novel.
This tests one concrete classical sampler, not classical hardness or a
quantum advantage. It preserves the explicit inverse-trace relation and
even grants a free exact solver inside each proposed restriction.

## Model And Proposed Update

Let q=2^n, A_i={a:Tr(inv0(a))=b_i}, |A_i|=a=q/2, and

    Omega={x:Hx=s, x_i in A_i for all i},
    H[j,i]=alpha_i^j, 0<=j<K,

with arbitrary distinct public alpha_i. Assume Omega is nonempty. Given
a native solution x, independently choose a uniform L-element subset M_i
of A_i conditional on x_i in M_i. Sample uniformly from
Omega intersect product_i M_i. The old x always belongs to that fiber.
For L=2 each menu is an affine binary line through x_i. Gaussian
elimination samples that binary fiber without a field table. For larger
L the update may itself be hard; the mobility bound below grants it free.
Generating uniform accepted elements is explicit trace-hyperplane sampling
followed by inv0, not a new oracle.

The kernel is symmetric: the probability of any particular incident menu
is binom(a-1,L-1)^(-N), independent of the starting word. For two words in
the same menu fiber, the conditional output weight is the same 1/Z(M).
Thus the uniform native distribution is stationary. This alone says
nothing about a useful mixing time.

## Uniform Every-Start Mobility Bound

Any two distinct words with the same syndrome differ on at least K+1
coordinates, because every K columns of H are independent. Represent each
menu by an ordered uniform list of L-1 alternatives to x_i. Consider a
fixed changed support S of size w>K and a fixed choice of one alternative
slot at each coordinate of S. Condition on the alternatives outside K
pivot columns in S. The parity checks force all K remaining values.
Independence across coordinates bounds the chance by (a-1)^(-K).
Dependencies BETWEEN slots of a single menu do not matter for this
single-slot event. A union bound gives

    Pr[menu contains another native word] <= u,
    u=min(1, sum_(w=K+1)^N binom(N,w)(L-1)^w / (a-1)^K)
      <= min(1, L^N/(a-1)^K).

L=1 has mobility exactly zero. The bound is uniform over EVERY native x,
every target, syndrome and set of distinct evaluation points. It therefore
applies conditionally on an adaptive history of fresh independent menus.
Count every raw menu draw, including menus rejected by screening. A bound
per accepted screened menu is not supplied. The stationary-law statement
uses fixed L; adaptive state-dependent L need not preserve that law.
For T steps, Pr[ever moves] <= min(1,T*u). If the starting distribution is
supported on S0, the final distance from uniform native sampling obeys

    TV >= max(0,1-T*u-|S0|/|Omega|).

Use the event S0 union {ABORT} for this lower bound when failures occur;
the target gives ABORT zero mass. Thus aborting instead of remaining in
S0 cannot improve the guarantee.
For a known biased norm-family start, the existing whole-family mass
bound can supply the |S0|/|Omega| upper bound. No uniformity of the initial
norm sampler is required. A sampler starting in the desired uniform law
is not obstructed: obtaining that law is the unresolved task.

At N=n^2,K=floor(N/8) and L=poly(n),

    log2(u) <= N log2(L)-K log2(2^(n-1)-1)=-Omega(n^3).

This includes simultaneous changes of ALL N coordinates, unlike the
earlier fixed-small-block Gibbs obstruction. It is not a lower bound on
search, all Markov chains, correlated menus, or algebraically designed
flats. In particular, it does not cover the scalar-normalized accepted
flats in RECIPROCAL_TRACE_FLATS.md.

Exact outward-rounded upper bounds using the simpler L^N envelope:

| n | L | Per-step chance of another native word, at most |
| --- | --- | --- |
|17|2|2^-286|
|31|2|2^-2638|
|61|2|2^-24178|
|61|61|2^-5831|
|127|16129|2^-28575|

At n17,L17 or n31,L31 this bound is vacuous. That is not evidence for
mixing. These are analytic bounds, not executed large chains.

## Unanchored Menus And The Exact Repair

Instead choose each menu uniformly among ALL L-subsets of A_i, reject an
empty native fiber and output a uniform element of a nonempty fiber.
That output is generally biased by the varying inverse fiber size. Equal
point incidence in the menus does not make this law uniform.

An exact correction is to accept each whole menu with probability
Z(M)/L^N before drawing its uniform native word. For each fixed native x,
the unconditional output probability is

    Pr[x in product M_i]/L^N=(L/a)^N/L^N=a^(-N).

Thus its conditional output IS uniform, but its success per trial is
|Omega|/a^N. The existing inverse-trace fiber count gives
(1+e)q^(-K), |e|<=eta. This is independent of L and reproduces direct
product-root rejection. It is worse than the ALREADY EXISTING exact
accepted systematic-root/Prange sampler, whose success is
(1+e)2^(-K). Do not promote this correction as a new useful sampler.
Neither statement rules out a different efficient size-biased menu source.

Independent review supplied a stronger correction: MDS injectivity on
N-K information coordinates gives Z(M)<=L^(N-K). Acceptance
Z(M)/L^(N-K) is therefore legal and succeeds with probability

    |Omega| L^K/a^N = (1+e)(L/q)^K.

It also returns an exactly uniform conditional output, but remains
exponential for L=poly(n). This improves the particular rejection envelope,
not the best classical baseline. Exact counts AND uniform restricted-fiber
samples are still granted, not implemented at native scale. Furthermore,
Pr[an unanchored menu has any solution] <= E Z = (1+e)L^N q^(-K).
This last statement bounds first-witness success of THIS proposal family;
the anchored mobility theorem does not make a first-witness claim.

## Exact Finite Falsifiers

The executable reference uses actual public finite-field inverse trace,
not a toy oracle. It is explicitly exponential and capped. With F_8,
N=4,K=1,b=(1,1,1,1),s=0, the alphabet is {1,2,4,6} and |Omega|=40.

- All anchored transition matrices are exactly symmetric and stochastic.
- For L=2 the unanchored proposal has abort probability1/54 and its
  conditional output TV is39/4240, not zero.
- For L=3 there are no empty fibers, but output TV is9/3640. Empty-fiber
  rejection is therefore not the whole cause of bias.
- The volume correction gives exactly uniform outputs with success5/32
  for L=2,3,4, matching40/4^4.
- The stronger MDS correction gives success5L/32 and remains exactly
  uniform. The control checks its fiber-size envelope on every menu.
- L=1 is the identity update; L=|A_i| is a full native heat bath, whose
  missing efficient implementation must not be hidden by the notation.

## What Would Change The Conclusion

The separate [systematic-curve filter](INVERSE_TRACE_SYSTEMATIC_CURVE_FILTER.md)
examines correlated Artin-Schreier patches whose free coordinates can
cover the whole accepted alphabet. Its fixed-parameter incidence proof
still gives productivity at most q^d*|Omega|/(q/2)^(N-K) under its precise
fresh-offset contract. This is not an extension of the independent-menu
theorem to arbitrary correlated sources; solution-enriched sources and
sufficiently high-dimensional patches remain outside that falsifier.

A constructive route must exploit cross-coordinate structure, an efficient
large-fiber conditional sampler, or a menu law whose concentration is
proved while its sampling cost is paid. Recovering validity is insufficient:
write and verify the resulting full output law, including failures. The
residual-fiber transfer in INVERSE_TRACE_COMPLETION_TRANSFER.md remains a
specific open route. No general native sampler, hardness statement, or
speedup is established by this negative result.
