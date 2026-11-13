# Community recovery: actual classical theorem scope

Conclusion: NONE of the three inspected primary theorem interfaces already
states recovery for the SAME k>=3 centered-color Bernoulli-edge HSBM. Nor did
this audit find an explicit fully paid reduction of that model to one of
their recovery theorems. This preserves a model-specific recovery obligation;
it proves neither novelty nor advantage, absence of other algorithms, nor
hardness. Boolean one-particle decoding and HCE/color-coding remain strong
classical comparators and prior mechanisms, not dismissed methods.

Read STATE/TRAPS and NATIVE_COMMUNITY_RECOVERY.md. Only retained local actual
statements/model/proof interfaces were used; no network/API/Git, source
fetch, giant HCE moment derivation, numerical sweep or shared-status edit.
All line locators count physical LF characters in the retained text.

## Native model that must be preserved

Let p be fixed even>=4, k fixed>=3, q=1/4, x_i IID uniform[k], and

    f_x(E)=sum_a product_{i in E}(1[x_i=a]-1/k),
    Y_E | x ~ Bern(q+epsilon*f_x(E)), independently across p-sets E.

Only ONE edge-bit array is given. The output is one k-label assignment
with permutation agreement>=1/k+c_(p,k), not merely a detector, Boolean
parity vector, candidate list or oracle for fresh graphs. The target is
classical n^(ell+O_p(1)) at epsilon^2*D>=C_(p,k)*ell, with growing polylog ell,
D=binom(ell,p/2)binom(n-ell,p/2). The quantum composition, if admitted later,
requires the separately paid native source/precision/readout conditions.
Use p for hyperedge arity here: the XOR papers use their symbol k for ARITY,
not for a number of communities. Confusing those meanings is not a reduction.

## Actual source interfaces

| Primary source | Actual observation/hidden object | Actual recovery result | Native HSBM transfer status |
|---|---|---|---|
| Mao2604.10457v1 | Uniform p-supports plus signs z_E=(product x_i)*xi_E, ONE hidden Boolean vector, independent sign noise | Formal Theorem5.8 recovers that vector up to the even-arity global sign, with explicit sample/time/level conditions | No multi-color Bernoulli observation theorem or paid signal-to-parity reduction supplied |
| Sharp-Kikuchi2607.29672v1 Section13 | A uniform ordered tuple and a REVEALED literal vector Y_j=x'_(i_j)*W_j, known fixed joint local sign law W | Products of the revealed literals are exactly noisy XOR channels; main XOR recovery applies channelwise | Native input has one Bernoulli edge bit, not the literal vector; the extraction operation is unavailable without a new channel construction |
| HCE2610.40941v1 | IID uniform support OCCURRENCES, retained repetitions, signs b_a=eta_a*product x_i with independent eta_a | Formal Theorem4 gives even-arity weak Boolean recovery under explicit residual/SNR conditions; fixed-level corollary retains logarithmic slack | No sign-gauge identity or full operator-moment theorem supplied for the rank-k centered-color tensor |

### Mao: formal theorem, not its abstract

Retained authority:
`audits/sources/2026-11-13-community-recovery/mao.{pdf,txt,source.json}`,
<https://arxiv.org/pdf/2604.10457v1>.
Definition1.3, txt LF224--257, fixes x in {+/-1}^n and the exact parity/noise
sample law. The appendix's fixed-m/without-replacement/Bernoulli equivalences
are changes of sampling model for THIS noisy-XOR experiment; “Bernoulli” does
not mean arbitrary Bernoulli edge probabilities or arbitrary finite labels.

Formal Theorem5.8, LF2003--2022, has time n^(D+3+o(1)), D divisible by source
arity, D*Lchain<0.3log(n)/loglog(n), its displayed m-versus-bias threshold,
and success>=1-O(Lchain^(-pD)). It outputs exactly the Boolean planting for
odd arity, and up to global sign for even arity. These are substantial
stronger-output guarantees for their model. They cannot be compared as a
native HSBM runtime without a transformation paying bias, sample count,
level range and the full observation law. In particular the target permits
polylog ell not automatically covered by that D*Lchain restriction.

### Sharp-Kikuchi: Section13 means random LITERALS

Retained authority:
`audits/sources/2026-11-13-community-baselines/sharp_kikuchi.{pdf,txt,source.json}`,
<https://arxiv.org/pdf/2607.29672v1>.
The native XOR model is LF248--296. Section13's literal model is LF2978--2987;
Lemma13.1 LF2992--3006 performs the actual operation

    sign(mu_S)*product_{j in S} Y_j
      = (product_{j in S} x'_(i_j)) * signed product of W_j.

This is why the derived channel has independent clause noise and the desired
bias. Section13.1 LF3061--3083 enumerates the constantly many channels of a
known fixed law and applies the earlier recovery results. It does NOT say
that every scalar Bernoulli observation of a multi-color tuple can be
converted to such a literal vector. Adding independent fair bits is not a
proof of the multiplicative literal law.

Section12.4 LF2866--2929 and Proposition12.6 already prove accepted-band
one-particle mass and tomography/rounding for BOOLEAN planting. This is real
prior art for the proposed mechanism. The HSBM-specific all-label population
comparison and its output decoder must therefore carry the new burden;
partial trace or clipping cannot be claimed as a new generic technique.

### HCE: the exact gauge and formal recovery scope

Retained authority:
`audits/sources/2026-11-13-community-baselines/cycle_enumeration.{pdf,txt,source.json}`,
<https://arxiv.org/pdf/2610.40941v1>.
Its model is LF38--52; recovery's IID occurrence convention and independent
noise are explicitly restated at LF1506--1519. The decisive identity is

    product_{a in witness I} b_a = x_i*x_j*product_{a in I} eta_a

when the symmetric-difference boundary is {i,j}. This gives the sign gauge
D_x and mean rank-one matrix in LF501--520. In a multi-color centered tensor,
products along a witness instead involve sums over color indices. The
Boolean cancellation identity is not established by knowing that detection
has a positive native circuit contraction.

Formal Theorem4 is LF526--548, with explicit residual bound and condition
theta_l>(3+epsilon)*R_(n,gamma). Corollary5 LF554--569 states its recovery
curve for FIXED l, with constants/asymptotic cutoff depending on l and the
displayed logarithmic slack. Source text explicitly distinguishes this from
its log-free detection theorem. It cannot be silently promoted to all
growing polylog levels or to a different population spike. The smaller n-by-n
recovery matrix does not remove the cost of constructing its entries.

## Concrete falsifier of the naive Boolean-coarsening transfer

Here is a small exact LAW check, not a runtime or hardness argument.
Take the native p=4,k=3 model and define a putative Boolean secret g_i=+1
for color1, g_i=-1 for colors2/3. Condition six vertices to have g_i=-1.
Their residual colors are independent uniform{2,3}; write t_i=+1/-1 for
those two colors. On any four of them, direct expansion gives

    f_x(E) = (1 + sum_{i<j in E} t_i*t_j + 9*product_{i in E} t_i)/72.

Indeed w1=-1/3, w2=(1+3t)/6, w3=(1-3t)/6. Thus E[f_x(E)|g]=1/72.
For E={1,2,3,4} and F={1,2,5,6}, the only shared nonconstant Fourier
monomial in those expansions is t1*t2, with coefficient1/72. Consequently

    Cov(Y_E,Y_F | g_1=...=g_6=-1) = epsilon^2/5184 > 0.

A noisy-XOR sample model with independent edge noises has zero such
conditional covariance for distinct supports once its Boolean secret is
fixed. Merely merging colors has therefore LOST conditional independence,
even though conditional edge bits were independent given the FULL colors.
Matching some low moments or parity-looking means does not repair the law.
A nonzero per-edge affine scalar randomization retains a corresponding
nonzero covariance; independent extra coins do not simply remove it.
This falsifies that particular straightforward coarsening reduction, NOT
all possible randomized reductions or multi-color algorithms.

Likewise encoding a color by several Boolean bits changes the latent domain
and produces structured multi-bit supports/channels, not automatically
uniform noisy-XOR supports. One must construct and analyze that observation
channel, including correlations, bias loss, finite samples and runtime.
Using the same observed edge repeatedly does not supply independent noisy
labels. The cited IID occurrence formulas do not authorize fresh queries.

## What could still become a stronger native classical comparator

1. A proved native reduction that emits genuine scalar parity samples or
   revealed literals at sufficient bias/sample count would activate Mao or
   sharp-Kikuchi. None is supplied by the inspected theorems; the coarsening
   calculation above rules out one tempting shortcut only.
2. A rank-k rooted/HCE color-network analysis might produce a direct small
   recovery matrix. It would need its population eigenspace and GLOBAL
   residual operator norm, not only the old detection variance/positive
   triangle contraction. This audit does not manufacture that missing
   moment proof or extrapolate fixed-level bounds to growing levels.
3. Robust higher-rank tensor recovery, color coding or a general multi-label
   theorem elsewhere may supersede the native construction. No such theorem
   is ruled out by this audit. Stronger-signal ordinary clustering remains
   a separate comparator; its lower-order signal must actually exist here.

Thus the supplied sources do not yet falsify the native recovery obligation
or supply a strictly stronger SAME-MODEL paid clock. They DO falsify any
claim that one-particle recovery itself is new, or that Boolean-XOR sample
and access assumptions can be discarded. Retain both facts simultaneously.
The parent derivation's uniform-original-Y validation can avoid independent
validation entirely; no source result here forbids that route. Its success
must come from the separate all-label mass/rounding/score proofs, not these
XOR theorem labels. Novelty, classical hardness and quantum advantage remain
false; the three inspected papers are not an exhaustive literature search.
