# A Direct Flux Gap For Supplied Line-Graph HDQI Inputs

Status: LOCAL MATHEMATICAL DEDUCTION, NOT independently reviewed or formally
verified. The numerical controls are not a proof. No scalable quantum circuit
has been compiled or executed. No novelty, classical hardness, useful-task
reduction, or speedup claim is made.

## Result And Native Input

The input is a supplied simple root graph R=(V,E), an ordered edge list, and
exact rational couplings |J_e|<=1. Let v=|V|, m=|E|, and c be the number of
components. The native anticommutation graph is G=L(R). Its independent
canonical generators are O_e=X_e product_{f<e,f~e} Z_f. The target is

    |pilot> = exp(-beta H/2)|0> / sqrt(tau exp(-beta H)), H=sum_e J_e O_e.

The source is not an arbitrary Hamiltonian with the same commutation graph:
independence of the canonical words matters. No root extraction, Gibbs oracle,
conditional-probability oracle, hidden basis, or sector table is supplied.

Choose a spanning forest, let r=m-v+c be its chord count, and let D be the
maximum degree of the chord subgraph. For 0<=beta<=1/8 and kappa=3D beta^2<1,
the random-scan flux heat-bath chain has spectral gap at least

    g=(1-kappa)/r.

The forest case r=0 needs no chain. Its previous classical sampler already
works at all finite temperatures. For r>0 the bound gives an ideal polynomial
coherent preparation construction when 1/(1-kappa) is polynomially bounded.
In particular, beta^2(d+1)<=1/64 for d=max degree of L(R) gives kappa<=3/64
and g>=61/(64r), even if r is extensive. This is a new parent on flux bits,
NOT a gap proof for the older general HDQI filtered parent.

The main change from the previous checkpoint is a direct DISCRETE mixed-
difference bound. The Hessian of the analytic log-partition extension cannot
simply be substituted for the multilinear-extension Hessian required in
[Anari et al., Theorem 2](https://arxiv.org/pdf/2307.10466). We do not use that
substitution or that theorem.

## Sector Normalization

The preceding FERMION_SAMPLER.md establishes the following representation,
with full Majorana trace, not a fixed-parity-sector trace. Every chord has a
sign s_i in {-1,+1}. The real skew matrix A_s has upper entry J_e on tree
edges and s_i J_e on chord i. Its nonzero eigenvalues are +/- i epsilon_j.
The represented Hamiltonian is (i/2) gamma^T A_s gamma, and

    Z_s = product_j cosh(beta epsilon_j),
    F(s)=log Z_s = (1/2) Tr log cosh(beta i A_s).

All 2^r fluxes are needed for a faithful trace of the native independent
word algebra. A single sector can turn a nonempty cycle word into identity.
The native normalized partition is 2^-r sum_s Z_s.

## Common-Resolvent Lemma

The [cosh product](https://dlmf.nist.gov/4.36.E2) gives the absolutely
convergent expansion

    F(s)=sum_{k>=0} log det(I+t_k A_s),
    t_k=2 beta/[pi(2k+1)],  sum_k t_k^2=beta^2/2.

For one term put R_s=(I+t A_s)^-1. Since A_s is real skew, ||R_s||<=1
independently of graph degree, size, or ||A_s||. Flipping chord i changes
t A_s by D_i=-2t s_i J_i E_i, where E_i has entries (u,v)=1, (v,u)=-1
and is zero elsewhere. Write P_i for its two-endpoint support projector.
Then E_i=P_i E_i P_i and ||E_i||=1.

Fix s before comparing ANY j. In a mixed cyclic trace word

    Tr(R_s E_{w_1} ... R_s E_{w_l}), w_a in {i,j},

there are transitions i->j and j->i. Insert all support projectors. Split
the cyclic word at one transition in each direction. Bound the two crossing
blocks in Frobenius norm and every other factor in operator norm. Thus

    |Tr(word)| <= b_ij(s)
      := ||P_i R_s P_j||_F ||P_j R_s P_i||_F.

Shared endpoints cause no exception. Summing with this SAME resolvent,

    sum_{j!=i} b_ij(s)
      <= sqrt[(sum_j ||P_i R_s P_j||_F^2)
              (sum_j ||P_j R_s P_i||_F^2)] <= 2D.

Indeed sum_j P_j<=D I, R_s is a contraction, and Tr P_i=2. Replacing the
summands by their separate suprema over s would destroy this argument.

Define Delta_ij F(s)=[F(s)+F(s^ij)-F(s^i)-F(s^j)]/4. Set Q_i=R_s D_i.
When 4t<1, the trace-log series for I+Q_i+Q_j converges in norm. The
determinants remain positive because I+t A has conjugate-paired eigenvalues.
In its mixed difference all pure words cancel. At order l there are 2^l-2
mixed binary words, each bounded by (2t)^l b_ij, since |J|<=1. Hence

    sum_{j!=i} |Delta_ij log det(I+t A_s)|
      <= (D/2) sum_{l>=2} (2^l-2)(2t)^l/l
      <= 4D t^2/(1-4t).

The last inequality uses (2^l-2)/l<=2^(l-1). At beta<=1/8 all t_k satisfy
4t_k<1, and absolute convergence permits summation:

    sum_{j!=i}|Delta_ij F(s)|
      <= 2D beta^2/(1-8beta/pi) <= 3D beta^2 = kappa.

The rational constant 3 uses pi>3; it is deliberately not optimized.
This is a configuration-wise bound for every s, not an asserted bound on a
matrix made of entrywise worst-case influences.

## From Coupling To A Gap

Let pi(s)=Z_s/sum_t Z_t. A heat-bath step picks i uniformly and replaces
its bit by one with probability p_i=logistic(F(bit1)-F(bit0)). Changing
another bit j changes that log-odds by magnitude 4|Delta_ij F|. Since the
logistic derivative is <=1/4, the change in p_i is <=|Delta_ij F|.

Couple neighboring configurations differing at j by picking the same update
bit and the same uniform random number. Updating j removes their discrepancy.
For any i!=j, the probability of creating a second discrepancy is at most
|Delta_ij F(s)|. Symmetry of Delta gives

    E[Hamming distance after one step] <= 1-(1-kappa)/r = 1-g.

Gluing along hypercube shortest paths extends the Wasserstein contraction
to arbitrary pairs; iterating and coupling with a stationary start gives

    TV(P^t(s,.),pi) <= r(1-g)^t <= r exp(-gt).

This is the elementary [path-coupling argument of Bubley and Dyer](https://web.stanford.edu/~montanar/TEACHING/Stat375/papers/path_coupling.pdf).
There is no hidden 1/min(pi) in it. For completeness the gap follows without
converting a mixing bound with an uncontrolled prefactor: contraction implies
Lip(Pf)<=(1-g)Lip(f). For every nonconstant eigenfunction f, Lip(f)>0, so
|lambda|<=1-g. Reversibility gives a real eigenbasis; P is also PSD as the
average of conditional-expectation projectors. Its top eigenvalue is uniquely
one since all single-bit conditional probabilities are positive.

The same bounds hold throughout the temperature path [0,beta].

## Certified Conditional Access

`flux_gap.py` accepts exact integers/Fractions and computes intervals without
sector enumeration or floating-point diagonalization. Let M=sum_e J_e^2.
For every signed A_s, sum_j epsilon_j^2=M, so log det(I+t A_s)<=t^2 M.
Truncating the cosh product before term K gives a nonnegative omitted tail

    <= 2M beta^2/[9(2K-1)].

For requested log-partition width eta<=1 choose
K=max(1,ceil(8M beta^2/(9eta))). This tail is <=eta/4. A rational Machin
interval for pi, from alternating atan series, has width
eta/[16 max(1,M beta^2)]. Replace pi by its midpoint. For denominator p>=3,
the derivative of the full determinant sum has magnitude <=M beta^2;
the crude bound sum_{k>=0}(2k+1)^-2<2 suffices. Thus the replacement error is
at most M beta^2 times the pi interval width.

Each v-dimensional determinant is an exact rational determinant. Compute
its logarithm by powers-of-two range reduction and the positive atanh
series, with a geometric tail bound; round intervals OUTWARDS to dyadics.
Each logarithm receives width eta/(8K). Add the two-sided pi error and
one-sided omitted tail. The resulting interval has width <=eta. A work-cap
failure returns INCONCLUSIVE, never an uncertified fallback value.

For a conditional query, enclose F1 and F0 at width eta/8 each. Intersect
their difference with +/-2beta|J_i|: flipping one represented term changes
H by operator norm 2|J_i|, so the Gibbs log-partition is this Lipschitz.
For beta<=1/8 the log-odds lie in [-1/4,1/4]. Taylor/geometric rational exp
bounds and a monotone logistic transform enclose the native probability
to width <=eta. These probabilities lie in [1/3,2/3].

The rational implementation costs polynomial in v, input bit length, and
1/eta. It is NOT claimed polynomial in log(1/eta). This is enough for the
inverse-polynomial precisions below, but the resulting upper bounds are
very large. Every determinant and its dimension are charged.

The implemented classical flux sampler takes
t=ceil(ceil(log2(2r/epsilon))/g) steps and per-step probability tolerance
epsilon/(2t). Ideal mixing error is <=epsilon/2, since log2 x>=ln x.
Coupling midpoint Bernoulli choices to the exact chain contributes at most
epsilon/2 more. This samples the NATIVE FLUX distribution, not the final
interference output and not a coherent source.

The TV theorem assumes independent random bits. Omitting a seed uses the
system random source; an explicit seed is a reproducible pseudorandom
control, not an information-theoretic TV guarantee for that fixed string.
Receipts retain this distinction.

## Coherent Construction And Error Budget

For fixed values of the other flux bits, define the projector block

    h_i = [[p_i,-sqrt(p_i(1-p_i))],
           [-sqrt(p_i(1-p_i)),1-p_i]],  G_beta=(1/r)sum_i h_i.

Then G_beta=I-diag(sqrt(pi)) P diag(1/sqrt(pi)). Its unique zero state is
sum_s sqrt(pi(s))|s>, norm is <=1, and gap is >=g. At beta=0 the zero state
is |+>^r. These terms are NOT spatially local: their coefficients depend on
all other flux bits. Access is nevertheless explicit via two rational
log-partitions, a controlled one-bit rotation, and clean uncomputation.
No random classical execution is claimed to prepare coherent amplitudes.

Put Lambda=sum|J_e| and parameterize beta(s)=s beta for s in [0,1].
The spectral formula gives |dF/dbeta|<=Lambda and 0<=d^2F/dbeta^2<=M.
For the conditional log-odds delta, |delta'|<=2Lambda and |delta''|<=2M.
With theta=atan exp(delta/2), h is the complementary rank-one projector
to (cos theta,sin theta). Its derivatives obey

    |theta'|<=Lambda/2,
    |theta''|<=M/2+Lambda^2/2,
    ||G'(s)||<=a=beta Lambda/2,
    ||G''(s)||<=b=beta^2(M/2+Lambda^2).

For a uniform lower gap g, the rank-one specialization of
[Jansen, Ruskai and Seiler, Theorem 3](https://arxiv.org/pdf/quant-ph/0603175)
therefore bounds leakage amplitude by B/T, where

    B=(2a+b)/g^2+7a^2/g^3.

Choose T=max(1,ceil(4B/epsilon)); pure-state trace-distance error is at most
epsilon/4, up to irrelevant global phase. Freeze the time path on N equal
intervals and use first-order products of the r terms h_i/r. The time-freezing
error is <=Ta/N and splitting error <=T^2/N: sum_i||h_i/r||<=1 bounds the
commutator sum. The ledger conservatively chooses

    N=ceil(16(T^2+Ta+1)/epsilon), L=Nr rotations.

Allocate operator error epsilon/(32L) to each controlled exponential, for
at most epsilon/32 in total. Conditional width eta=epsilon/(512L) is enough:
on [1/3,2/3], |d(asin sqrt(p))/dp|<2. Diagonalizing h with two conditional
rotations amplifies this probability error by at most 4; the remaining
rotation budget pays angle and phase synthesis. At each step each of the
two log-partitions needs at most ceil(64M beta^2/(9eta)) determinants
(zero if M beta^2=0). The code reports these arithmetic counts, NOT elementary
quantum gates. Uniform reversible implementation pads arithmetic loops and
uncomputes all scratch; neither that compilation nor its gate optimization
has been performed here. Ordinary rational algorithms can be reversibly
simulated with polynomial overhead, so this is not a free oracle assumption.

Finally use the previously derived isometry: controlled normalized Gaussian
pairing state with K_s=-i tanh(beta iA_s/2), Hadamards on the r flux bits,
incidence/chord decoding, and the known Clifford phase correction. Gaussian
state preparation is a standard mechanism, not a new discovery; see
[Bravyi's fermionic linear optics construction](https://arxiv.org/abs/quant-ph/0404180).
Allow epsilon/4 for its matrix functions, controlled gates, and cleanup.
More explicitly set the complex antisymmetric pairing matrix T_s=-iK_s.
Its singular values are <=1. A skew unitary-congruence decomposition writes
T_s=W direct_sum([[0,t_j],[-t_j,0]]) W^T with t_j>=0. Prepare normalized
two-mode states (|00>+t_j|11>)/sqrt(1+t_j^2), then implement the
number-conserving second quantization of W. This fixes vacuum amplitude
POSITIVE: number-conserving transformations fix vacuum exactly, not only
up to an unknown sector-dependent phase. Track the known scalar phases
when compiling occupation-number gates. Unpaired modes remain vacuum.

No singular-vector gap is an input promise. An approximate decomposition
with matrix backward error delta is sufficient, including at degeneracies.
For |psi(T)> proportional to exp(sum_{i<j}T_ij a_i^dag a_j^dag)|vac>, all
pair-creation terms commute. Differentiating and normalizing gives tangent
norm at most 2 sum_{i<j}|dT_ij|, since each creation operator has norm one.
Thus entrywise O(epsilon/v^2) backward accuracy suffices for the state, with
its positive-vacuum phase convention. The matrix tanh is well conditioned
in Frobenius norm on Hermitian inputs at this scale (divided differences
bounded by beta/2); also I+T^*T>=I. Standard finite-precision matrix functions,
approximate skew decompositions and Givens synthesis therefore use polynomial
work, without a hidden eigenbasis, eigenvalue-separation promise, or
exponential inverse-vacuum-amplitude precision. A compiled coherent
implementation preserving these relative phases is still absent.
Isometry preserves the flux-state error. The displayed allocations sum to
less than epsilon in trace distance. This establishes an ideal polynomial
construction under the stated local deductions, not an executed algorithm.

## Attempts To Falsify The Conclusion

1. **Analytic vs multilinear Hessian.** The previous shortcut is invalid.
   The new proof uses literal four-vertex differences and a common resolvent.
2. **Hidden exponential sector sum.** Such sums occur only in capped control
   routines. Native conditional access and the analytic ledger never use them.
3. **A sampled sector is a coherent source.** False. The classical flux chain
   is an equally important output of this pass, not the coherent construction.
4. **Uniform sector amplitudes suffice.** False already on a four-cycle.
   A small per-component error amplifies under disjoint products; tiny finite
   deviations must not be interpreted as an exact scalable replacement.
5. **One fermion sector represents the independent native algebra.** False;
   cycle words can collapse. All flux amplitudes and the signed Fourier map
   are retained in the full-state controls.
6. **A gap alone implies implementability.** False. Conditional precision,
   reversible arithmetic, annealing time, product steps, and Gaussian cleanup
   are charged separately. The conservative count is enormous but polynomial.
7. **Any extensive cycle-rank input is hard.** False. Disconnected bounded
   components factor, and the preceding exp(O(r)) sampler is polynomial for
   logarithmic r. The large ladder ledger is only a nonenumeration test,
   not a hardness benchmark. Bounded-width tensor methods also need comparison.
8. **This prepares a useful quantum advantage.** Not established. No output
   statistic or native task is proved classically hard, and no reduction to
   a consequential computational problem has been supplied.
9. **The general HDQI open problem is solved.** False. The root representation
   and skew contraction are special to supplied line graphs. Other graphs,
   the old thermal parent, larger temperatures, and other access models do
   not inherit this bound.

Finite controls test mixed-word traces, every flux influence and gap for
small roots, rational enclosures, exact-source rejection of float inputs,
and the signed canonical output after dense adiabatic evolution. These are
falsifiers for implementation errors, not all-size or independent proofs.

### A Same-Class Classical Rescue That Fails

The earlier paired-visit-support positivity counterexample contained an
induced claw, so it did not by itself rule out positive activities for line
graphs. Retesting that specific possible rescue gives a native line-graph
counterexample. Let the root be K_{2,3}, with ordered edges

    (0,2),(0,3),(0,4),(1,2),(1,3),(1,4),

unit couplings, and output Y={0,1,2,3}. Its line graph is the triangular
prism. Swapping root vertices 3 and 4 induces edge permutation
(0,2,1,3,5,4). It fixes Y and sends its ordered generator word to its
negative. Thus a_full(Y)=0 for every t=beta/2. The same symmetry on the
restriction Y gives a_Y(Y)=0. The restrictions Y+{4} and Y+{5} are
exchanged with opposite amplitudes. Consequently their paired-support
inclusion-exclusion weight satisfies the exact identity

    W(full,Y)=-2 A(t)^2, A(t)=a_(Y+{4})(Y)=t^6/45+O(t^8).

Exact matrix powers give the first numerator 16/6!=1/45. Each restricted
Hamiltonian has norm <=5; the even-order Taylor tail at t<=1/64 is less
than one eighth of t^6/45, by the preceding paired-positivity note's bound
390625/3383296<1/8. Hence W<0 throughout 0<beta<=1/32, including the
new flux-gap regime (the line graph has degree four). Exact order-20
rational intervals check three temperatures. This rules out the proposed
nonnegative colored visit-support representation EVEN IN THIS CLASS.

It does not rule out regrouping, a different sampler, or other classical
methods. In fact this root has r=2 and is ALREADY covered by the preceding
classical fermion sampler. No additional negative-family scan is needed;
the relevant positivity assumption has been decisively tested.

## Research Decision

The specific extensive-flux preparation blocker is replaced by a locally
derived ideal construction at degree-scale temperature. The proof needs
independent specialist scrutiny, particularly the common-resolvent trace
lemma, coupling-to-gap transfer, and uniformly coherent Gaussian stage.
No further independent reviewer was authorized for this pass.

The next decisive question is classical sampling of the SAME full word law
on connected high-cycle-rank roots in this regime. Classical efficient
flux sampling, efficient partition estimation, and additive observable
estimation are not that sampler; conversely, their existence makes a
speedup claim substantially harder to justify. Seek a positive full-output
representation or a charged useful-task reduction before building more
preparation benchmarks. Also compare free-fermion/matchgate and coherent
Gibbs preparation prior art before claiming originality. The source
[redundancy-free Hamiltonian paper](https://arxiv.org/html/2610.03697v1)
is context for the broader problem, not evidence of this construction's
novelty.
