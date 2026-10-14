# HSP Campaign: Five General Conclusions Retracted

Reviewed2026-10-13. This audit removes overbroad conclusions from active search
guidance; it does not discover a new quantum algorithm. Original records for
Investigations33 and38-41 are preserved in
`registry/quarantined_campaign_negatives.json`. The restoration guard added
by the preceding campaign audit applies to all eight quarantined IDs.
Unreviewed records are not implicitly endorsed.

## Constant Class Is Not The Heisenberg Boundary

[Imran and Ivanyos](https://arxiv.org/abs/2304.08376) give an exact polynomial
quantum HSP algorithm for nilpotent groups of constant nilpotency class whose
order has only bounded prime factors. Their central-image transformation uses
zero-sum subsequences; it does not require every hidden subgroup to intersect
the first center nontrivially.

The family U4(F_(2^r)) satisfies those hypotheses for growing r:

    nilpotency class3, order2^(6r), encoding length6r,
    sole prime divisor2, field size2^r.

Thus it is a nontrivial scalable family beyond Heisenberg covered by a known
algorithm. Bounded CHARACTERISTIC is not bounded FIELD SIZE. This does not
solve growing nilpotency class or unbounded-prime regimes, and the algorithm
still requires the paper's group/oracle access assumptions. We do not claim
an implemented receiver or a new speedup from this citation.

An exact center-bypassing control takes H=<I+E12> in U4(F2), embedded in every
extension field. Its nonidentity element is not central and H cap Z={I}.
Nevertheless the published theorem applies. The producer also verifies
[I+E12,I+E23]=I+E13 and [[I+E12,I+E23],I+E34]=I+E14 overF2. This confirms
the relevant class3 geometry, not a simulation of the full HSP algorithm.

Supercharacter or weak-Fourier blindness only restricts those particular
measurements. Representation-classification wildness is not by itself a
quantum circuit/time lower bound. The old universal conclusions are therefore
not justified by those facts.

There is a SEPARATE constructive debt in the campaign's Heisenberg recipe:
for a noncentral cyclic order-p subgroup, total nontrivial1D weak-sampling
probability is(p-1)/p^2. Waiting for one such sample costs p^2/(p-1) expected
copies, not polynomial in logp. A half-success union bound already requires
at least ceil(p^2/[2(p-1)]) copies. Therefore "learn direction weakly, then
cancel a known chirp" cannot silently be called efficient at growing p.
Known efficient Heisenberg algorithms are NOT excluded; their actual
collective/algebraic mechanisms must be used rather than this free-direction
assumption.

## DHSP: Reductions Are Not Universal Hardness

[Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044) relate
specific optimal-measurement implementations to average-case subset-sum
problems. This does not make every entangling measurement NP-complete to
construct, prove worst-case hardness for the actual random source, or make
Kuperberg optimal among all algorithms. Large commutant dimension alone
cannot establish computational intractability.

For an explicit counter to that dimension inference, SUPPLY phases with
N=2^m and labels k_j=2^j. Then

    tensor_j (|0>+exp(2*pi*i*s*2^j/N)|1>)/sqrt(2)
      =1/sqrt(N) sum_(b=0..N-1) exp(2*pi*i*s*b/N)|b>.

Inverse QFT recovers s exactly with O(m^2) gates. Subset sums are simply
binary encoding; all fibers have size1 and the commutant dimension is N.
This is a known structured calibration, NOT a generic DHSP algorithm or
a new oracle problem. Ordered IID random labels equal this prescribed
sequence only with probability N^-m=2^-m^2. Obtaining a structured bank is
not free; existing native-source audits must not be bypassed.

Weak reflection-character trace vanishing remains a useful scoped fact.
Single-copy phase information is not automatically an established LPN/CLWE
reduction or an unconditional classical time lower bound. A lattice reduction
also needs its exact parameter and promise regime; it does not classify all
lattice cryptography as broken by an unspecified DHSP solver.

## Higher-Degree Bent Does Not Mean Intractable Dual

Consider the explicit Maiorana-McFarland family on two m-bit halves:

    f(x,y)=x.y+y1*y2*y3, m>=3,
    dual_f(u,v)=u.v+u1*u2*u3.

Summing the Walsh transform over x enforces y=u, proving
Walsh_f(u,v)=2^m*(-1)^dual_f(u,v). Both functions have degree3 and public
phase recipes with m CZ terms and one CCZ term. A derivative along y1 is
x1+y2*y3, demonstrably nonaffine. Thus the campaign's claims that all
efficient-dual structured bent functions have affine derivatives, or that
explicit higher-degree duals require exponential circuits, are false.

THIS family is still classically easy under matched chosen-query access.
Let g(x,y)=f(x+a,y+b). Then g(e_i,0)+g(0,0)=b_i. Once b is found,
g(0,e_i+b)+h(e_i)=a_i. This recovers both halves using2m+1 queries to g and
the known explicit h. The executable attack runs up to m512; its legality
is restricted to chosen classical queries, not random-sample-only access.
No quantum advantage is inferred from nonlinear derivatives.

[Roetteler](https://arxiv.org/abs/0811.3208) analyzes several bent-function
hidden-shift classes and their oracle/query distinctions. The campaign's
universal three-way impossibility does not follow from measuring two flat
bases or from the cost of one dual implementation. Arbitrary unknown
black-box f, known explicit f, and supplied dual access are different models.

## Legendre: Information, Computation And Oracle Access

For the complete Legendre symbol chi (including chi(0)=0) and distinct shifts
a,b, exact character orthogonality gives

    sum_x chi(x+a)*chi(x+b)=-1.

There are exactly(p-3)/2 agreeing queries: two zero locations disagree,
and on the remaining p-2 locations the agreement/disagreement difference is-1.
Thus independent uniform classical samples distinguish a fixed true shift
from every other shift except with probability at most

    (p-1)*[(p-3)/(2p)]^M < (p-1)*2^-M.

M=ceil(log2p)+confidence bits suffices for INFORMATION-THEORETIC
identifiability. The report verifies all nonzero differences at small primes
and costed bounds at127-bit p without materializing the domain. Exhaustive
candidate search may still be expensive. This is NOT an efficient classical
decoder or a refutation of any properly stated computational assumption.
Holevo bounds alone cannot turn this into a universal operation lower bound.
Classical samples also do not forbid later quantum computation on those
samples; any claimed speedup still needs a matched best classical attack.
Binary-valued PRF variants need their own collision calculation.

Jacobi(a,N) is computable without factoring odd N, by stripping powers of2,
quadratic reciprocity and Euclidean remainders. The producer implements a
counted arithmetic replay and compares it with FLINT's independent Jacobi
routine. Reversible arithmetic can compute/uncompute this known predicate;
no unknown-function superposition oracle is supplied thereby. Zero symbols,
precision and a physical gate compiler remain explicit obligations. This
does NOT validate arbitrary-composite Gauss phase-cancellation formulas.

For N=9,25,45 the Jacobi shift oracles have identical full-table equivalence
classes of sizes3,5,3 respectively. Even coherent queries cannot distinguish
members of a class; uniform full-modulus recovery is bounded by1/3,1/5,1/3.
For N=9 that contradicts a general totient-success claim of phi(9)/9=2/3.
Primitive-character and squarefree assumptions cannot be omitted. These are
source-identifiability countercontrols, never candidate toy oracle problems.

## Next Research Decision

Retain scoped weak-measurement failures and matched classical attacks. Do not
retain general HSP bans derived from them. Published bounded-class,
bounded-prime-factor algorithms are calibration successes to reproduce under
honest access, not new discoveries. The open unbounded-prime and growing-class
regimes need explicit complexity analysis; do not import either easy or hard
classification without its parameters.

The next constructive audit should examine the existing nil3 StateHSP source
and receiver contracts, particularly growing-prime zero-sum cost, subgroup-image
creation, and whether all required group actions have lawful input access.
The general random-label DHSP receiver remains open. No empirical signal,
special supplied source, or publication abstract substitutes for that receiver.
