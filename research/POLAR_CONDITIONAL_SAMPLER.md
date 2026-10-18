# Polar Conditional Sampling Before Another Quantum Decoder

2026-10-17. Known SC/source-shaping mechanisms. Local Gibbs mapping, hybrid
bound and convention-specific entropy derivation require review. No new
quantum algorithm or general dequantization theorem is claimed.

FOLLOW-UP: [certified source design](POLAR_SOURCE_DESIGN.md) now constructs
an explicit non-prefix half-rate set without the exponential source table,
with average-sign TV<=0.010221 at N32768. It resolves the missing public-set
premise below for that finite family, not the worst-sign or all-code problem.

## Why This Direction Was Selected

The cubic OPI and native tail passes are complete. Rather than extending
their seed/degree scans, this pass examined a constructive alternative to
the enormous LDPC extrinsic trees and failed cyclic BPQM shortcuts: polar
successive cancellation (SC). Its synthesized message graphs are trees even
when the code has no tree Tanner graph. This is established prior art, not
our proposed new decoder: [Piveteau and Renes, Section 7.2](https://arxiv.org/pdf/2109.08170),
and [Mandal, Brandsen and Pfister](https://arxiv.org/pdf/2401.07167).

Before compiling such a receiver, test the strongest relevant classical
competitor: SC shaping for the dual source distribution. The question is
whether it solves the SAME signed code-Gibbs task, and whether correctness
holds on average or for every sign pattern.

## Input And Native Task

Let E contain N independent Bernoulli(p) bits, p=(1-c)/2, with rational
0<=c<1. N is a power of two. The public involutory polar transform gives
U=G(E). A public subset F of polar coordinates and a syndrome s impose
U_F=s. All matrices, constraints and probabilities are explicit.

Let H_F have rows giving these polar coordinates as parities of E. Given
arbitrary public clause signs J, set s=H_F J and y=E xor J. Then

```
H_F y = 0,
Pr(y) proportional to product_j(1+c*(-1)^(y_j+J_j)).
```

This is the native signed parity-Ising Gibbs law on the kernel of H_F,
not an oracle problem or a decoded-word proxy. A basis of this kernel maps
words bijectively to independent Ising spin coordinates. Tests compare this
identity against direct native weights for EVERY length-4 sign pattern.
The overlap c=13/20 corresponds here to p=7/40; it must not be confused with
the different bit-flip amplitude parameter used inside the coherent source.

## Implemented Classical Algorithm

Walk U_0,...,U_(N-1). Force coordinates in F to their specified syndrome
values; sample other coordinates from the EXACT unrestricted-source
conditional P(U_i|U_<i). Known SC plus/minus recursions compute each such
conditional with 2N-1 recursive calls. All sampling uses rational Bernoulli
draws, with no floating likelihoods or empirical mixing assumption.

The simple reference takes O(N^2) rational operations, not the optimized
O(N log N) schedule; rational bit lengths and recursion counts are exposed.
It never enumerates source words during sampling. Small exhaustive design
and diagnostic tables are SEPARATE and charged as exponential calibration.
Neither hidden frozen-set construction nor free probability tables are used.

CRITICAL: the free-bit conditional ignores FUTURE frozen constraints. This
does NOT generally sample P(E|U_F=s) exactly. For a contiguous initial frozen
prefix, however, the remaining chain is already conditioned on every
constraint, so sampling is EXACT for every syndrome and sign pattern.
A fair source p=1/2 is also exactly handled for every subset F. These are
structural exactness certificates, not conclusions from feasible samples.

The `sample_gibbs` workflow returns the actual kernel word y, signs and
constraint masks, not just a plausible noise word or its energy.

## Average-Syndrome Guarantee, Not A Worst-Case Guarantee

Write

```
epsilon_F = sum_(i in F) E_(P prefix) |P(U_i=1|prefix)-1/2|.
Qjoint(u) = 2^(-|F|) * product_(i not in F) P(u_i|u_<i).
```

A reverse-order hybrid replaces each frozen conditional by a fair bit.
Earlier prefixes still have their P distribution; later conditionals sum to
one. Thus TV(P_U,Qjoint)<=epsilon_F. The syndrome marginal discrepancy
delta=TV(P_(U_F),Uniform) is at most that joint discrepancy. Triangle
inequalities then give BOTH

```
E_(uniform s) TV(Q_s,P_(U|U_F=s)) <= epsilon_F+delta <= 2 epsilon_F,
E_(native s)  TV(Q_s,P_(U|U_F=s)) <= epsilon_F+delta <= 2 epsilon_F.
```

For a specific syndrome the resulting generic bound has an extra factor
2^|F|. Uniform clause signs give uniform syndromes because H_F has full row
rank, so the first average is exactly the uniform-sign Gibbs comparison.
There is NO claim that every adversarial sign pattern is handled well.

Entropy interpretation: Pinsker and Jensen give
E|P(U_i=1|prefix)-1/2| <= sqrt((ln 2)/2 * (1-H(U_i|U_<i))).
Consequently a supplied high-entropy set with sufficiently small summed
entropy defects gives an average-case classical approximation. Standard
source polarization supplies such regimes; efficiently constructing and
certifying the PARTICULAR public set remains a charged obligation.
Relevant source-shaping prior art includes
[Zhao and Li, Appendix A / Corollary 17](https://arxiv.org/html/2506.09239v2#A1),
which concerns averaged quantization noise, not automatic arbitrary-syndrome
conditional correctness. No new source-coding theorem is claimed here.

## Why This Is Relevant To The Quantum Proposal

For the pure-state channel
|psi_x>=sqrt(1-p)|0>+(-1)^x sqrt(p)|1>, overlap is c=1-2p.
Fixing a polar input prefix and averaging the remaining inputs dephases
the channel state into orthogonal character blocks. Its eigenvalues are
the probabilities of the source parities associated with the remaining
encoder rows. Subtracting consecutive state entropies gives the synthesized
CQ Holevo information. In the implemented convention G^T=R G R, with R
reversing coordinates. Hence the CQ information at i equals the source
conditional entropy at N-1-i. Small density matrices independently verify
this identity; they are not used as a decoder or scalable access primitive.
General channel/code duality is known: [Renes](https://arxiv.org/abs/1701.05583),
with [a semiclassical BSC/PSC treatment](https://arxiv.org/abs/2103.09225).

Therefore the natural high-information polar receiver and high-entropy SC
shaping competitor are not unrelated constructions. If the corresponding
source set has epsilon_F->0 with a polynomial construction, a claimed
uniform-random-sign Gibbs advantage is removed by this classical algorithm.
That is a CONDITIONAL, review-pending application of known mechanisms,
not a worst-case-sign no-go, not all codes, and not a result established
by the small numerics. It warrants checking this competitor before spending
main-model effort compiling a quantum polar receiver.

## Native Results And Falsifiers

All syndromes retained:

| N,F,p | Uniform-syndrome average TV | Worst TV |
| --- | --- | --- |
| 2,{1},1/10 | 0.4 | 0.72 |
| 4,{0,1},7/40 | 0 | 0 |
| 8,{0,1,2},7/40 | 0 | 0 |
| 8,{0,1,2,4},7/40 | 0.00416611 | 0.05596208 |

The last set selects the four smallest EXACT source prefix biases, with
its full 256-word design cost charged. It is not an asymptotic code design.
The prefix examples are deliberately retained as analytically easy controls,
not evidence for a quantum speedup. Native length16/32/64 workflows exercise
prefix-exact and non-prefix-uncertified families with public signs, charged
recursive work and no source-law tables. Feasibility is never used as a TV
certificate. The two small native CQ/source entropy controls agree to below
2e-12, not a formal floating-point theorem certificate.

Falsifiers of a future average-case quantum claim: a valid epsilon_F bound
plus this classical sampler on the actual code family and same signs model.
Falsifiers of an overbroad classical claim: the explicit 0.72-error syndrome,
or any adversarial-sign analysis lacking a uniform likelihood control.
The remaining useful question is a code family and signs model that avoids
this baseline while retaining a genuinely efficient phase-correct quantum
decoder. More prefix examples or unqualified polar-capacity plots will not
answer it. General LDPC/cyclic Gibbs decoding remains open.

## Execute

```
python theorems/polar_conditional_sampler.py --write
python -m pytest tests/test_polar_conditional_sampler.py -q -W error::RuntimeWarning
```

No accepted candidate, general negative entry, compiled quantum decoder or
automatic proof promotion. CLI exposure and broad production regressions
remain Gemini's mechanical work.
