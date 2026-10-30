# Native scope and competing algorithms for noisy phase learning

2026-10-30. Read-only source audit by Zeno, primary-literature audit by
James, and native-completion attack by Ramanujan, integrated by the parent.
Analytic deductions and bounded controls are not a native quantum execution,
classical hardness proof, human review or novelty certificate.

## Classical examples do not supply the copy model

Write d=p^n. Every promised phase-diagonal source has computational diagonal
1/d. If coherent loading m examples only prepares states supported on their
coordinate set S, measurement of the projector onto S gives

    TD(sigma,rho) >= 1-|S|/d >= 1-m/d.

For Q such copies supported on S^Q, the bound is 1-(|S|/d)^Q. Keeping
and tracing the sample index can only remove the inter-example coherence;
even granting its clean erasure does not evade this support argument.

For a flat rank-r target, randomizing the support does not suffice either.
Its support projector Pi has Pi_xx=r/d. Every m-sparse pure component has
overlap at most Tr(P_S Pi)=rm/d. Thus any mixture of m-sparse states obeys
TD(tau,rho)>=max(0,1-rm/d). This is a LOADER-CLASS bound, not a lower bound
on arbitrary algorithms that could interpolate and synthesize a new state.

For the new peak-weight/full-rank source, use its retained spectral
projector P_tau instead: rank<=K<2R, mass z>=1/R, and diagonal K_actual/d.
The same calculation gives TD(tau,rho)>=z-K_actual*m/d. It is not valid
to reuse the flat-source 1-rm/d bound for an arbitrary full-rank source.

IID scalar phase errors at every input also differ from one latent linear
error. In a hypothetical FULL-DOMAIN coherent example, averaging them gives

    alpha |psi_F><psi_F| + (1-alpha) I/d,
    alpha=|E omega^xi|^2.

The prior low-rank theorem does not cover this full-rank state. The new
peak-weight theorem CAN cover it when the peak is large enough. That does
not construct it from a short classical sample table. The coherent example
and joint IID source law still require a paid preparation argument.

Ordinary LWE additionally places its secret in the linear part of F,
which these affine-noise learners cannot identify without extra promises.
Encoding it instead as F(x,t)=t(s.x) requires a new source construction;
loading m observed x-values and all t still covers only m/p^n of the domain.
See the source distinction in
[Grilo--Kerenidis--Zijlstra, Sections II--III](https://arxiv.org/html/1702.08255v2).

## An evaluator makes preparation easy and classical recovery easy

If input is an explicit resettable circuit G(x,xi)=F(x)+b_xi.x, fixing xi
through coherent evaluation/kickback/cleanup supplies a phase component.
Resampling xi between copies gives the intended distribution. But fixing
the same seed classically supplies an ordinary degree-D evaluator. At
fixed D<p, interpolation uses binomial(n+D,D) evaluations and polynomial
field arithmetic. Discard the affine coefficients and recover the target.

For a quadratic, second differences directly recover the Hessian. An
opaque quantum device that draws one inaccessible error per coherent call
is a genuinely different access model, useful for calibration but not
obtained by declaring a randomized classical sampler coherent. Fresh
randomness on an attempted inverse does not ensure cleanup.

## A matched classical vector-regression baseline

If the classical input ALREADY supplies full vector samples Z=AY+b with
A symmetric, uniform Y independent of b, and some error atom >=1/R for
integer R<p, there is a polynomial classical algorithm even with full
error support. This model is not scalar LWE.

Subtract independent samples. Candidate differences satisfy z=Ay+e with
zero-error probability sum_b w_b^2>=R^-2. Against an independent difference
validation sample, form y^T Z-z^T Y. For a wrong candidate it is uniform
and has zero probability1/p. For a correct candidate its zero probability
is the collision probability of the projected ORIGINAL noise y.b.
Projection retains an atom a>=1/R. Cauchy-Schwarz on the other p-1 bins gives

    q_y-1/p >= [p/(p-1)](a-1/p)^2 >= 1/[R^2(R+1)^2].

Thus O(R^2(n+log(1/delta))) candidates and an independent shared batch of
O(R^8 log(T/delta)) difference samples suffice, followed by linear algebra.
The consumed ORIGINAL classical samples number2(T+L), not2TL. Zeno checked
this extension independently; no noise-support list is supplied.

This does not dequantize the proposed source learner: its four-copy
instrument convolves the noise. The resulting error need not obey the
original peak promise. The [p=5 falsifier](../../PEAKED_PHASE_NOISE_LEARNING.md)
even erases the scalar Hessian from every allowed four-copy output, while
paid SWAP verification on original copies still recovers it. Dropping those
verification copies is an information-theoretic failure on that example.

## Real HPGP and discrete-log bridges: useful controls, not new speedups

An HPGP oracle E(y-F(x)) prepares a graph coset; Fourier measurement of y
gives a KNOWN uniform k and phase kF. The pure public-map learner can keep
k. Requiring k=1 by rejection costs p queries and is not efficient in log p.
For noisy sources, the pair (kF,kB) varies with k: the antisymmetrizer does
not receive identical mixed inputs merely because k is recorded.

A genuine classical-input example is discrete logarithm in an efficiently
computable cyclic group of known odd prime order p. For h=g^s, implement
H(x,y)=g^y h^(-x^2); its fibers are y-sx^2. The graph procedure gives
|psi_(ksx^2)>. Accept nonzero square k and substitute x=a t with a^2=k^-1.
Acceptance is (p-1)/(2p); the phase becomes s t^2. The noiseless four-copy
instrument yields z=2sy, so a nonzero y recovers s, checked by g^s=h.

This is a valid polynomial-time bridge, but it uses rank one and recovers
[Shor's established task](https://arxiv.org/abs/quant-ph/9508027), not a new
advantage or an application of the noisy mechanism. General fixed-degree
multivariate HPGP also has established algorithms:
[Decker et al., Theorem 5](https://arxiv.org/html/1107.2189v2#S5.SS3).

## Closest primary theorem comparisons

No exact subsumption was established in this bounded audit. That is not
evidence of priority. The precise source and growing-prime resource
dependences, rather than a generic claim of noisy-state learning, matter.

- [Allcock et al., 2510.06848v3, Sections 3--4](https://arxiv.org/html/2510.06848v3#S4)
  supplies useful skewed Bell sampling and internally creates conjugates
  from repeated PURE stabilizer copies. Do not dismiss it as needing an
  external conjugate source. Its pure-state theorem is not automatically
  a theorem for unknown, independently varying noisy eigenstate labels.
  Theorem53 already targets a phaseless group: merely dropping eigenlabels
  is not a new distinction. Its exact pure-eigenoperator support condition,
  rather than growing-prime dependence, excludes direct substitution.
- [Hinsche--Eisert--Carrasco, Section II.4](https://arxiv.org/html/2505.15770#S2.SS4)
  distinguishes mixed-state strong invariance Tr(R(h)rho)=1 from mere
  conjugation invariance. The latter is what the noisy quadratic basis
  retains; a purity-overlap gap does not establish the former condition.
- [Qi et al., Theorem 1](https://arxiv.org/html/2607.15559)
  accepts unknown PURE qudit states and displays
  (p/tau)^(O(p^2 log(1/tau))) poly(n,1/epsilon) cost. That statement does
  not imply mixed-input recovery polynomial in log p and inverse peak.
- [Chen et al., Section 6](https://arxiv.org/html/2408.06967#S6)
  genuinely includes mixed-state bootstrapping, but for qubits, with
  quasipolynomial rather than polynomial inverse-overlap dependence in
  the displayed general guarantee. It is important candidate-verifier
  precedent, not an odd-prime substitution.
- [Arunachalam et al., Theorems 8--9 and Section 6](https://arxiv.org/html/2208.07851)
  uses a Boolean computational domain for generalized phase states. Its
  stated generalized-phase dependence includes numeric alphabet size;
  the noisy quadratic result uses a subexponential classical processing
  bound. These are not the same growing-prime theorem.

For the unknown-basis consequence, the closest methodological precedent is
[Tang--Steckmann, Algorithm4/Theorem VI.2](https://arxiv.org/html/2610.03307v1#S6.SS1):
candidate generation and purity-based verification are already present for
noisy qubit stabilizer structure. The inspected theorem does not state the
odd-prime, unrestricted-rank, peak-only guarantee polynomial in log p and R.
James separately rechecked this narrower comparison after the basis
extension was proposed. Preserve this attribution and seek specialist
subsumption review; the audit is not a priority claim.

Keep one narrowly stated theorem note as a potential contribution. Attribute
antisymmetrization, SDE phase elimination, stabilizer machinery and the
candidate-verifier architecture. Human proof review and exact prior-art
review remain gates before any priority or publication claim.

## Competing native Mersenne direction: a fully paid failed route

Ramanujan tested partial parity elimination on the SAME existing native
relation, arbitrary original points/targets. For M residual coordinates,
K equations, t=M-K, reserve K-h coordinates B and let
L_B(T)=product_(i in B)(T-alpha_i). Row combinations L_B(T)T^j, j<h,
annihilate those columns. The remaining h equations are generalized RS
on the original points, with columns L_B(alpha_i)(1,alpha_i,...).

An exact conditional sampler exists by explicitly Fourier-transforming
the syndrome count tables on F_q^h, using the signed local Walsh evaluator.
It costs q^h poly(n,N) work/storage, plus enumeration of q coordinate
values per conditional draw. Solve the reserved coordinates uniquely,
then check their original predicates. If full/reduced normalized counts
are g_y and G_y', acceptance is exactly

    2^(-(K-h)) g_y/G_y'.

For M>=2K+1, the existing bounds keep both normalized counts within
constant factors, so outer trials are Theta(2^(K-h)). Polynomial rejection
cost requires h>=K-O(log n), where table construction costs 2^Omega(nK).
No new predicate, favorable layout, or free residual sampler was assumed.

Random Fourier queries do not automatically remove table cost. The
unbiased estimator 1+(q^K-1)a_Lambda(y) for normalized count g_y has variance

    (q^K-1)V_M-(g_y-1)^2.

The small supplied average-syndrome bound V_M alone does not control this
quantity polynomially. At the terminal M=K stage, counts are exactly0/1
and V_K=2^K-1. This is a concrete failed constructive route, NOT proof
that every classical algorithm is slow. Neither the native witness nor
uniform sampler was implemented or solved in this pass.

## Decision

Do not call noisy phase learning a standard-LWE, new HPGP, new discrete-log,
or native-Mersenne algorithm. Preserve the quantum-input theorem and its
new peak-weight extension, subject to review. The native Mersenne solver
remains open; better count bounds or a pre-Fourier sampler are not its
solution. Do not build a large quantum backend merely to fill that gap.
