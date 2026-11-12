# 2026-11-13 — Independent next-direction selection

**Recommendation: finish A's already-running condensate/full-output attack;
do not start a paid irrational-alpha quantum/compiler round now.** C has the
strongest intrinsic external value of the three, but needs a specific new
global arithmetic operation before another broad paid request is worthwhile.
B, as currently justified by removal of a rational fat hook, is a parameter
extension whose most immediate physical output already has a positive
classical sampler. Full spectral support alone is not a computational case.

This is a selection judgment, not a theorem-status promotion. STATE/TRAPS and
the newest handoff title were checked. Only pertinent topic notes, previous
checked interfaces, and the actual retained Jack source passages cited below
were read. The two live condensate reports were NOT read. No network/API/Git,
quantum implementation, or finite sweep was used.

## Three-way comparison

| Direction | Native output and external value | Available mechanism and strongest retained baseline | Decision-changing obligation |
|---|---|---|---|
| A: growing-boson Macdonald dynamics | Full occupation after explicit native NS evolution; the condensate mu=(1^D) is a simple many-boson preparation and its mode redistribution is a concrete dynamical question. | Quantum poly(D,L,b) is already written. Every fixed initial boson count k is classically matched in (D+1)^O(k)poly(D,L,b); exhaustive p(D) algebra is also polynomial in binary time. Positive condensate spectral growth is under a separately funded check, not a full-output conclusion. | Whether the pending positive path construction supplies coherent occupation conditionals, with a polynomial bit/variance clock. A spectral/return sampler alone does not settle it. |
| B: one-boson BO at alpha=sqrt(2) | A physically intelligible high-momentum density-mode pulse at a fixed coupling, followed by mode fragmentation. Energy spectroscopy alone is insufficient motivation for new quantum work. | All-alpha creation algebra is paid; an irrational-content compiler looks plausible. The positive spectral growth proved below already samples the full eigenstate label, despite support on all partitions, and estimates return amplitudes with bounded variance. Exhaustive full-output algebra remains exp(O(sqrt D)) times polynomial input/precision cost. | A scientifically specified occupation observable or full-output law requiring coherent eigenstate interference, with a fresh constructive classical attack. Merely evading H_(3k,k) does not supply this. |
| C: general native Selmer classical match | Exact dim_F2 Sel^2(Jac(y^2=f)/Q) from arbitrary monic squarefree odd-degree f; directly useful arithmetic information and an upper bound on rational rank, not a rational-point solver. | The GRH quantum composition and classical all-prime local work are paid. Classical global class/unit arithmetic remains the general comparator. Quadratic, specified quartic, split and literal cyclotomic matches are substantial but do not cover growing arbitrary branch fields. | A complete classical global squareclass/localization calculation, or a genuinely smaller direct-dimension method, with polynomial clocks and all factorization calls charged. Existing local data are not a certificate of global completeness. |

The immediate A action is to adjudicate the two tasks already funded, not to
open another nearby input family. A full classical condensate match would be
a reason to reassess the scientific objective, not automatically increase the
number of occupied modes again. Conversely, failure of that attack would not
establish hardness. C is the stronger destination for fresh effort if a new
operation becomes available; repeating the earlier global-bypass question
without one is unlikely to change the next action.

For C, the retained native f=x(x^2-17*89) warning must remain in scope:
native bad primes need not generate the required class quotient with odd
index. It falsifies that proposed global source, not every algorithm for the
final Selmer dimension. In particular, sufficient class/localization data
must not be relabelled necessary data or a hardness reduction.

## B's cheap decisive classical spectral attack

Here is an exact direct deduction for EVERY real alpha>0, using integral
Jack normalization. Write c_alpha(i,j)=alpha*j-i, with zero-based row i and
column j, and H_lambda=||J_lambda||^2 in the Hall-alpha form.

The retained primary inputs are Mickler--Moll Proposition 4.3, Eq. 4.8
(mickler_moll.txt LF 620–634), its Lax hierarchy/top-left block (LF 287–324),
and Mickler's independently stated Pieri identity, Lemma 2.8 Eq. 44
(mickler_lr.txt LF 460–480). They give

    p1 J_lambda = sum_s tau_lambda(s) J_(lambda+s),
    sum_s tau_lambda(s)=1,
    sum_s tau_lambda(s)c_alpha(s)^2=alpha*|lambda|.            (1)

The last equality is the second transfer moment: pi0 L^2 on degree n is
sum_k V_k V_-k=alpha*n I. The same principal specialization gives

    [p1^D]J_lambda=1,
    [p_D]J_lambda=product_(box!=origin) c_alpha(box).          (2)

For the normalized single-boson input p_D/sqrt(alpha D), its spectral law is

    pi_D(lambda)=alpha D
       product_(box!=origin) c_alpha(box)^2 / H_lambda.       (3)

Start at the singleton. At size n>=1 add s with probability

    K(lambda,lambda+s)=c_alpha(s)^2 tau_lambda(s)/(alpha n).  (4)

These are nonnegative and sum to one by (1). To verify their endpoint law,
ordinary tau growth from empty has weight

    Pl_D(lambda)=alpha^D D!/H_lambda.

Indeed the sum of its path products is the coefficient of J_lambda in p1^D,
and orthogonality plus (2) gives that coefficient as alpha^D D!/H_lambda.
For (4), the extra factors along ANY singleton-to-lambda path multiply to

    product_(box!=origin)c_alpha(box)^2 / [alpha^(D-1)(D-1)!].

This factor depends only on the endpoint. Multiplication by Pl_D gives
exactly (3). Starting at singleton is essential: there is no division by
alpha*0 at the empty diagram. Rational-alpha zeros merely forbid some paths;
they do not invalidate the proof. At alpha=sqrt(2), every nonorigin content
is nonzero, so every partition has positive mass, AND the sampler still works.

There is also a polynomial finite BIT/TV clock at sqrt(2). The corner/hook
formulas for tau use O(D) linear factors a+b sqrt(2), with a,b=O(D).
Products, division by nonzero factors, and sums over at most D+1 corners
stay in Q(sqrt(2)) with polynomial bit height. Inversion uses conjugation
and the nonzero integer quadratic norm; no number field of growing degree,
factoring, or selected real root is required. Signs and dyadic-threshold
comparisons are decided exactly by rational comparisons and squaring after
checking signs. One may recompute weights from the current shape each step,
so no unbounded symbolic history is stored.

At each of at most D steps use a uniform r-bit grid against the exact
cumulative probabilities. Its conditional TV error is at most (D+1)2^-r.
Taking r=b+2ceil(log2(D+1))+3 makes the total error <2^-b. Thus the
spectral SHAPE, and hence any computable spectral energy, has a bounded-clock
poly(D,b) classical sampler. This is not a claim of bounded-fair-bit exact
sampling of irrational probabilities; (4) is the exact ideal growth law.

For an explicit time, return amplitude is

    <D|exp(-iT H_alpha)|D> = E_(lambda~pi_D) exp(-iT E_lambda).

The summand has modulus one. Additive accuracy eta with failure delta costs
O(eta^-2 log(1/delta)) samples, plus polynomial spectral/phase arithmetic.
This dependence is on eta^-1, NOT log(1/eta); no relative estimate of an
exponentially small return probability is implied. With the normalization
K_alpha=T3/alpha=sqrt(alpha)S+(alpha-1)N2, energies are
E_lambda=alpha sum_i lambda_i^2-sum_j (lambda'_j)^2. At sqrt(2) these lie in
Q(sqrt(2)); binary-time phase evaluation needs only polynomially many bits,
including the time length. Rescaling to another specified BO normalization
does not change the positive spectral sampler.

None of this samples the evolved occupation state by drawing lambda and then
an eigenstate occupation. That mixture deletes precisely the coherent cross
terms under investigation. Nor does a positive spectral sampler make the
single-boson state a positive mixture of eigenstates before evolution.

## What could justify B instead

The compiler itself is not the strongest reason to spend. For distinct content
coordinates with differences bounded by D,

    |sqrt(2)*dx-dy| >= 1/((sqrt(2)+1)D) >1/(3D)

by the nonzero integer conjugate norm. Within one diagram the interlacing
steps are at least 1 and the content span is <3D, so the existing telescoping
argument gives tau>=1/(9D^2) for D>0. These make a clean compiler extension
credible; they are not a completed re-review of that extension or a scientific
advantage argument. No new compiler is requested here.

ONE useful output that would change the recommendation is the **momentum
fragmentation full-counting law** after the single high-momentum pulse:

    M_K=sum_(k<=floor(sqrt D)) k n_k,
    output the distribution of M_K/D after exp(-iT K_(sqrt(2)))|D>.

For example its tail Pr[M_K>=D/2] measures whether a macroscopic fraction of
the initial momentum has reached soft modes. This is an operational mode
redistribution observable, not the already-easy energy spectrum or return
amplitude, and it does not require a physical-position encoding. A full
occupation sampler supplies it directly. Its coarse output also permits a
stronger classical challenge than demanding an arbitrary full partition.

If an external application actually requires this distribution, B becomes a
better-motivated fixed-coupling single-pulse problem than simply moving A beyond
a known support bound. The next paid obligation should then be a constructive
classical calculation of THESE occupation projectors/form factors, testing
whether the positive growth can be lifted to their coherent two-path kernel.
Without that application/source check, do not fund B merely because alpha is
irrational. No general obstruction follows if that one construction fails.

## Newly suggested alternating BO drive

Alternating polynomially many binary-time H3=S+2/sqrt(3)N2 and H1=S pulses
could change the scientific mechanism by leaving a single integrable evolution.
It is more than changing alpha once, but a large dynamical Lie algebra is not
a uniform computation encoding, a polynomial pulse-synthesis theorem, or a
useful output. This bounded review supplies none of those. Parent primary-
literature checks can determine whether a specified driven mode-fragmentation
experiment or uniform encoding is available; until then it does not displace
A/C on the strength of controllability alone.

Corpus checks used the local been-tried queries for irrational single-boson BO,
growing-boson Macdonald, and general native Selmer global matching, plus the
corresponding baseline query. They returned the pertinent current notes and
mostly unrelated registry leads, not an exact new comparator. That is not
literature absence evidence. Current primary-literature checks on irrational
BO correlation/form-factor samplers, the likely known z-measure interpretation
of (4), driven BO applications, and general global arithmetic remain the
parent's responsibility; no abstract-derived claim is imported here.
