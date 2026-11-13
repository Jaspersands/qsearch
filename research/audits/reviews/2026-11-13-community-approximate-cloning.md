# Native approximate Bernoulli cloning — independent proof, 2026-11-13

**Accepted:** the proposed single-input operation produces a frozen pair of
hypergraphs uniformly close to two conditionally independent native graphs.
The symmetric kernel halves both signals; the preferred ASYMMETRIC kernel
retains (1-t) of the matrix signal and t of the guide signal, at the SAME
baseline q. Its finite-bit preprocessing clock and nonempty vanishing-error
parameter windows are explicit below.
This closes this JOINT-LAW interface, not the Kikuchi certificate, directional
overlap, end-to-end quantum algorithm, or any advantage claim.

STATE/TRAPS and the exact repair contract were read. The actual retained
Brennan--Bresler--Huleihel 2019 primary Lemma 14 and its proof were read, rather
than treating an advisory label as evidence. No API, network, Git, quantum
implementation, new numerical control or parameter sweep was used.

## 1. Exact one-bit kernel and its approximation error

Fix 0<q<1/2 and |delta|<=q. Given Y~Bern(q+delta), generate an independent
Z~Bern(q) and an independent fair bit B. Output (Y,Z) or (Z,Y), according to B,
and forget B. Denote the output law by R_delta, and put
  r=q+delta/2, Q_delta=Bern(r) tensor Bern(r).
Each marginal of R_delta is EXACTLY Bern(r). In the order (00,01,10,11),
  R_delta-Q_delta=(delta^2/4)*(-1,+1,+1,-1).                 (1)
For example R_delta(11)=q*(q+delta)=r^2-delta^2/4. Therefore
  chi2(R_delta || Q_delta)
    =(delta^4/16)*(1/(1-r)^2+2/(r*(1-r))+1/r^2)
    =delta^4/(16*r^2*(1-r)^2).                             (2)
All Q_delta probabilities are positive: q/2<=r<=3q/2<3/4.
The concave function r*(1-r) is minimized over this interval at r=q/2,
since the difference of its endpoint values is q*(1-2q)>0. Consequently
  r*(1-r)>=q*(1-q)/2,
  chi2(R_delta || Q_delta)<=delta^4/(4*q^2*(1-q)^2).        (3)
In particular the slightly weaker bound in the contract is valid. This kernel
is generally approximate, with negative conditional covariance -delta^2/4.
It is not a claim that exact independent copies were extracted from one bit.

For the native model delta_S=epsilon*f(x_S), set
  beta=epsilon/sqrt(q*(1-q)).
The native |f|<1 follows, for example, from Holder applied to the centered
community-indicator vectors, whose l2 norms are sqrt(1-1/k)<1. Thus (3) gives
  chi2(R_deltaS || Q_deltaS)<=beta^4*f(x_S)^4/4<=beta^4.     (4)
The final relaxed constant is retained for simple parameter accounting.

### Preferred asymmetric version

Instead put the observed Y in the GUIDE position with probability t in (0,1),
and in the MATRIX position otherwise, filling the other position with the
fresh Bern(q) bit. Then
  r_G=q+t*delta, r_K=q+(1-t)*delta.
The 00- and 11-probabilities do not depend on t. The same direct calculation
as (1) gives
  R_delta,t - [Bern(r_G) tensor Bern(r_K)]
      =t*(1-t)*delta^2*(-1,+1,+1,-1),
and the EXACT divergence is
  chi2=t^2*(1-t)^2*delta^4
        /[r_G*(1-r_G)*r_K*(1-r_K)].                         (4a)
For a uniform bound impose the explicit cap epsilon_*<=q/2, hence
|delta|<=q/2. Each marginal is in [q/2,3q/2] and has variance at least
q*(1-q)/2, so
  chi2<=4*t^2*(1-t)^2*beta_*^4*f(x_S)^4
       <=4*t^2*beta_*^4.                                   (4b)
This is stronger than the proposed constant 16 once the cap is imposed.
Without a marginal-probability margin, |delta|<=q alone does NOT imply a
uniform constant times t^2*beta^4 bound as t tends to zero: a marginal can
approach zero and the denominator in (4a) loses a factor t. The explicit
small-signal windows below satisfy the cap, and stronger known input signals
can first be attenuated to it. No such extra cap was needed for the fair kernel.

## 2. All edges, hidden-label mixtures, and the null law

For n<p the empty output pair is exact and needs no random bits. Otherwise
let M=binom(n,p)>0. Apply the kernel independently to EVERY input hyperedge,
using fresh null bits and fair coins per edge. Conditional on ANY fixed label
assignment x, the input Y_S and the kernel randomness are independent across
S. Hence the whole actual and ideal laws are products:
  R_x=product_S R_deltaS,
  Q_x=product_S [Bern(q+epsilon*f(x_S)/2) tensor
                 Bern(q+epsilon*f(x_S)/2)].
The latter is precisely two native hypergraphs independent CONDITIONAL ON THE
SAME x, each with parameter epsilon/2. The chi-square product identity gives
  1+chi2(R_x||Q_x)=product_S(1+chi2(R_deltaS||Q_deltaS))
                  <=exp(M*beta^4),
and Cauchy--Schwarz gives the uniform bound
  TV(R_x,Q_x)<=min(1, (1/2)*sqrt(exp(M*beta^4)-1)).          (5)
For the asymmetric version, the identical product argument instead gives
  TV(R_x,t,Q_x,t)<=min(1,(1/2)*sqrt(exp(4M*t^2*beta_*^4)-1)), (5a)
where Q_x,t is the pair of conditionally independent native graphs with
signals t*epsilon_* and (1-t)*epsilon_*. The baseline is q in both.
Using a per-edge TV union bound instead would lose the useful fourth-power
scaling. Product structure conditional on x is essential to these bounds.

The same bound holds jointly with x under ANY common label prior pi, since
  TV(pi(x)R_x, pi(x)Q_x)=E_pi TV(R_x,Q_x).
The same joint-label argument applies to the asymmetric bound (5a).
It therefore holds after discarding x, including the native uniform prior
and any conditioning of that prior on balanced labels. The ideal mixture is
  E_x[ P_(x,epsilon/2) tensor P_(x,epsilon/2) ],
NOT the product of two planted mixtures with independent hidden labels.
The distinction is essential for the intended conditional overlap argument.

Under the null, delta_S=0 for every S and (1) vanishes exactly. Swapping two
independent Bern(q) bits preserves their product law. Thus the ideal-arithmetic
preprocessor produces two exactly independent null graphs, not merely a
planted-case comparison with an unspecified null error.

Centering either ideal graph at q and dividing by sqrt(q*(1-q)) gives mean
(beta/2)*f(x_S); the baseline does not change. No label-dependent centering or
knowledge of the individual delta_S is used.

## 3. Native attenuation and fixed finite-bit implementation

If the known input signal epsilon is stronger than a desired epsilon_*<=epsilon,
first set rho=epsilon_*/epsilon. Independently for every edge, retain Y_S with
probability rho and otherwise replace it with a fresh Bern(q) bit. The result
is exactly Bern(q+epsilon_* f(x_S)) conditional on x, independently across
edges. The null remains Bern(q). Apply sections 1--2 to this attenuated graph:
the ideal copies have epsilon_*/2 and beta_*/2, where
  beta_*=epsilon_*/sqrt(q*(1-q)).
Attenuation uses no labels, second planted sample or f-value oracle. If epsilon
is unknown, this adaptive-strength selection is not supplied by the present
lemma; cloning itself needs only q. No amplification is possible through rho>1.

Here is a bounded-clock bit implementation. Known q and, when used, epsilon
and epsilon_* are rational expanded parameters, with their input lengths
charged. Approximate each needed Bernoulli parameter s by
  s_hat=floor(2^b*s)/2^b.
Draw exactly b fair bits, interpreted as U in {0,...,2^b-1}, and output
1 iff U<floor(2^b*s). The per-draw coupling error is at most 2^(-b).
One edge uses at most FOUR such draws: its attenuation selector, attenuation
null bit, cloning null bit, and asymmetric orientation bit. The fair version
uses an exact orientation coin and only three approximate draws. Thus choosing
  b=ceil(log2(4M/eta_num))                                  (6)
ensures TV between the finite implementation and the ideal-arithmetic kernel
is at most eta_num, uniformly for every input graph and every label choice.
Rational threshold computation uses integer multiplication/division, with
bit cost polynomial in b and the parameter input bits. There is no unbounded
rejection loop or expected-only random-bit budget.

The total preprocessing is O(M) fixed-size random operations plus polynomial
bit overhead per operation, using O(M) output bits and charged input reads.
For fixed p, this is polynomial in n, parameter bits and log(1/eta_num).
The model is an EXPLICIT hypergraph with M entries; an implicit/succinct-input
model would need a separate access analysis. At q=1/4, null bits use exactly
two fair bits, so without attenuation the whole kernel is exact in 3M fair
bits. With attenuation in the fair version, only rho needs approximation. The
asymmetric version also approximates t with the same budget. Combining
(5) and (6) gives the symmetric total source error
  eta_src <= (1/2)*sqrt(exp(M*beta_*^4)-1)+eta_num.          (7)
For the asymmetric version replace the exponent by 4M*t^2*beta_*^4. If
q=1/4 is generated exactly, the finite-bit null law stays EXACT even after
rounding rho and t: both alternatives in each relevant mixture are identical
null laws. Parameter rounding only changes the planted-law comparison.

## 4. Above-threshold signal and small total error can coexist

This section only checks parameter compatibility with the displayed Kikuchi
threshold scale, NOT the correctness of that spectral theorem or certificate.
Let K=K_(k,p)>0 be any fixed threshold coefficient for
  T_(n,ell)=K*n^(-p/4)*ell^((2-p)/4)*sqrt(log n).            (8)
This is the scale in actual Schmidhuber--Zlokapa Theorem 11, equation (15),
LF412--419, with K=3*sqrt(6)/C_(k,p). A validated certificate must separately
supply its own sufficient K. The cloning algorithm does not infer it.

### Symmetric two-above-threshold window (not a speedup claim)

If beta_*=C*n^(-p/4)*ell^((2-p)/4)*sqrt(log n) with fixed C>2K,
each ideal copy lies above (8), while
  M*beta_*^4 <= (C^4/p!)*ell^(2-p)*(log n)^2.               (9)
Consequently the total variation in (7) vanishes for
  (log n)^(2/(p-2)) << ell << sqrt(n), eta_num=o(1).         (10)
This is nonempty for every fixed even p>=4. In contrast, merely taking ell
a sufficiently large CONSTANT multiple of (log n)^(2/(p-2)) gives a tunably
small fixed TV upper bound, not by this argument an o(1) bound. Both clones
lose only the factor two in signal; an additional log(n) mask dilution is
not present in this kernel.

Here is a fully elementary rational parameter sequence, avoiding numerical
root evaluation and any threshold constant in the PREPROCESSING rule. Fix
p=4, q=1/4 and any fixed k>=3. For n>=2, put
  L=ceil(log2 n), J=ceil(sqrt(L)),
  ell=4*ceil(L^4/4), epsilon_*=1/(n*J).                    (11)
L and J are computed by integer bit-length/square-root operations. Give any
known rational epsilon in [epsilon_*,1/4); attenuation uses the rational rho
above. Each ideal clone has
  beta_copy=2/(sqrt(3)*n*J)>=1/(sqrt(3)*n*sqrt(L)),
whereas (8) is at most K/(n*L^(3/2)). Thus BOTH copies are above threshold
once L>=2K. For L>=64, ell is already less than sqrt(n)/2, and along this
sequence ell=o(sqrt(n)). The source's other scaling ranges are compatible:
q is constant, beta_copy=Theta(n^(-1)/sqrt(log n)) lies between the displayed
n^(-3/2) and n^(-1) scales for p=4, and epsilon_*<q eventually.

Since beta_*=4/(sqrt(3)*n*J) and M<=n^4/24,
  M*beta_*^4<=32/(27*J^4)<=32/(27*L^2).                    (12)
For L>=2 this exponent is below 1, and exp(t)-1<=2t gives
  TV(R_x,Q_x)<=4/(sqrt(27)*L)<1/L.                         (13)
Taking eta_num=n^(-2) in (6) makes the total error <1/L+n^(-2)=o(1), with
b=O(log n). This gives an explicit nonempty promise window after attenuation,
for all L>=max(64,2K). If the original input is also required to obey the
source's hard-range upper bound, the subinterval
  epsilon in [1/(nJ), sqrt(3)/(4n)]
is nonempty for all sufficiently large n. Alternatively epsilon=epsilon_*
requires no attenuation, and the q=1/4 cloning is then exact finite-bit.
The example works independently of the unresolved certificate proof: whatever
fixed sufficient K that proof eventually supplies, the displayed window pays it.

### Asymmetric window and the matched classical comparison

The ASYMMETRIC route is preferred for an eventual guide/matrix construction:
only the MATRIX needs to cross the spectral threshold (8). The guide has a
smaller mean and must meet the separate covariance/overlap requirements; it
is not asserted to cross that same threshold at the same ell.

Set L=ceil(log2 n) and t=1/L. For
  beta_*=C*n^(-p/4)*ell^((2-p)/4)*sqrt(log n),
where C>K is fixed, the matrix signal (1-1/L)*beta_* eventually exceeds (8).
The exponent in (5a) is at most
  (4C^4/p!)*ell^(2-p)*(log n)^2/L^2
    <=(4C^4/p!)*ell^(2-p).                                 (14a)
Thus EVERY growing ell=o(sqrt n) at this threshold scale gives vanishing
source TV, subject to the native scaling ranges and epsilon_*<=q/2. For fixed q in
(0,1/2), this cap holds eventually. In
particular the extra symmetric requirement (10) is absent. This calculation
does not prove the weaker guide's overlap; it supplies the appropriate law.

A concrete finite-bit witness window is also available. Keep p=4,q=1/4 and
fixed k>=3, choose any fixed positive INTEGER A>=max(1,K), and set
  t=1/L, ell=4*ceil(L/4), epsilon_*=A/n.                    (14b)
For n>=8A the signal cap holds. For L>=2 the matrix SNR is at least
2A/(sqrt(3)*n), while (8) is at most K/n, so the matrix is above threshold.
Here
  4M*t^2*beta_*^4<=128*A^4/(27*L^2),                       (14c)
which tends to zero. Once this exponent is at most 1, the source TV is at
most 8*A^2/(sqrt(27)*L). Add eta_num=n^(-2) via (6). All parameters in the
preprocessor are rational, computed with O(log n+log A) bits; no algebraic
root or unknown-label value is needed. This example is a LAW/THRESHOLD window,
not a claim that its chosen ell is the optimal classical comparison point.
A comes from an actually validated sufficient spectral constant if that
certificate is invoked; (14a) also states compatibility for any such constant.

The guide mean SNR in (14b) is 4A/(sqrt(3)*n*L). At the purely arithmetic level,
  lambda^2 / [(t*beta_*)^2*M] = O(L^4/n^2) ->0,
with fixed A,p,k and lambda=ell/p. This is compatible with the proposed
conditional-covariance target. Its validity and all guide normalization
factors remain outside this cloning proof.

The symmetric baseline cost must not be hidden. At fixed original SNR and
the SAME threshold constant in (8), halving SNR increases the required ell
by a factor 2^(4/(p-2)). Comparing a formal quantum leading exponent ell/4
on the weakened instance against the original classical exponent ell gives
ratio 2^(4/(p-2))/4. At p=4 this is EXACTLY 1: the loss can erase the putative
quartic leading-exponent improvement. Merely comparing both algorithms at
the weakened hierarchy level would be misleading. The very conservative
example (11) can be slower still than the classical choice at original SNR.
No advantage is attributed to either symmetric window.

In contrast the asymmetric MATRIX loss requires only the hierarchy factor
  (1-t)^(-4/(p-2))=1+O(1/L).                               (14d)
For a lambda-fold mean tensor the guide rescaling is explicitly t^lambda;
an overlap-based amplitude cost proportional to its reciprocal would incur
  t^(-lambda)=exp(O(ell*log log n))=n^o(ell),
not a constant factor in the leading n^ell exponent. This is conditional
resource bookkeeping for a subsequently PAID overlap proof, not that proof.
It identifies why the asymmetric operation avoids the symmetric-halving
baseline cancellation. All stronger applicable classical algorithms and the
actual end-to-end quantum construction still require their own comparison.

## 5. Frozen source reuse and detection quantifiers

Preprocess ONCE, store the pair of output graphs, and give the downstream
algorithm access only to this pair and the agreed public parameters. In
particular, withhold/discard the old Y, mask and attenuation randomness from
that interface. A claim about the joint law INCLUDING these extra variables
has not been proved by (5), and need not have the same bound.

Any ensuing classical or quantum procedure, including adaptive measurements,
amplitude amplification, many preparations and many queries to the stored
arrays, is one channel applied to the same classical input distribution. The
classical diagonal input states have trace distance exactly TV; contractivity
of trace distance under a trace-preserving channel yields
  TV(actual final output, ideal final output)<=eta_src.     (15)
There is NO multiplication by the number of quantum calls. Internal circuit
approximation errors must still be charged separately. The algorithm must
include its ABORT/timeout outcome; renormalizing a rare postselection is not
a trace-preserving operation to which (15) directly applies. Regenerating the
clones during queries is a different joint-law problem and is not proposed.

If an independently proved ideal two-copy detector has error e_alg(n), the
native compiled detector has error at most e_alg(n)+eta_src(n) on the planted
law, and at most e_alg,null(n)+eta_num on the null law. Strong detection
requires these totals to be o(1); either (11)--(13) or (14a)--(14c) provides
that SOURCE contribution in its respective parameter window.
A constant source error only establishes a bounded-error transfer. Repeating
the downstream computation on the same pair can reduce its own algorithmic
error, but does not by itself erase the source-law approximation error.
No ideal quantum detector or its overlap guarantee is proved in this note.

## 6. Exact-cloning prior boundary and the multilevel obstruction

Actual prior source: Brennan--Bresler--Huleihel, *Universality of Computational
Lower Bounds for Submatrix Detection* (COLT/PMLR99, 2019), retained as
`audits/sources/2026-11-13-community-selection/brennan_clone.txt`.
Lemma 14 and its entire proof are at physical LF1682--1728, printed pp28--29.
For two input biases u<v, it constructs a single-bit kernel with outputs
Bern(Q)^tensor t at u and Bern(P)^tensor t at v, provided
  ((1-P)/(1-Q))^t >= (1-v)/(1-u), (P/Q)^t <= v/u.
Its two kernel rows are the affine interpolation of those TWO product laws;
the displayed inequalities ensure that their entries are nonnegative. This
is an exact two-bias statement. Its existence claim is not an exact cloning
result for every intermediate or multilevel native signal.

Indeed let ANY fixed single-input-bit stochastic kernel output two bits.
At source bias s, its 11-probability g(s) and its two marginal probabilities
a(s),b(s) are affine in s. If both marginal slopes are nonzero, the polynomial
  g(s)-a(s)*b(s)
is a nonzero quadratic. It cannot vanish at three distinct values of s.
Thus no such kernel gives two nonconstant affine INDEPENDENT marginals at
three or more distinct source biases simultaneously. This statement allows
arbitrary auxiliary randomness in the one-bit kernel.

For the native k=3,p=4 function, label multiplicity patterns (4,0,0), (3,1,0),
(2,2,0), (2,1,1) give respectively
  f=2/9, -1/9, 1/9, 0.
All occur with positive label probability. Since epsilon>0, these give four
distinct input biases. The exact two-bias lemma therefore cannot be applied
as one uniform two-informative-copy kernel for this native conditional law.
This is NOT a general impossibility for multi-edge processing, approximate
cloning, label-informed kernels, or an informative copy plus a signal-free
copy. Sections 1--5 supply the useful approximate operation instead.

The accepted consequence is exactly a paid native joint-law replacement in
the parameter windows above. Classical spectral/certificate validity, signed
conditional tensor covariance, guide normalization and the full quantum clock
are separate obligations. No recovery algorithm, all-algorithm classical
lower bound, novelty, useful/Shor-level advantage or implementation is asserted.

After the independent proof was written, sections 2 and 7 of the terminal
`community-native-source-compiler/response.md` were compared. Its asymmetric
law and symmetric same-input cancellation agree. Its optional sharper native
margin bound and quantum runtime claims are not needed or imported here.
