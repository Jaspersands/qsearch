# Post-wave opportunity selection — 2026-11-13

Independent selection, not an algorithm admission. Current STATE/TRAPS/GOAL and
the compact-wave disposition were checked. No network, API, Git, numerical
sweep, or quantum implementation was used. The parent owns shared notes.

## Decision

Select ONE bounded proof attack: **a degree-uniform, factoring-only compiler
for supported squareclasses in an explicitly given quadratic tower**, using
the support-obstruction quotient kernel below and simultaneous control of the
conic/form recursions. The first deliverable is an actual recurrence and height
ledger, or an exact obstruction to that proposed recurrence. Do not select
another fixed-degree extension, a general-field isotropy oracle, or a compact
quantum norm solver already covered by existing work.

This is preferable to the three independent alternatives screened below because
it has a new, checkable algebraic operation that removes a real premise, and a
concrete externally useful endpoint: complete descent sources, hence the
existing all-prime local composition for hyperelliptic 2-Selmer computations
whose branch fields have such towers. A factoring-only result would give an
unconditional quantum endpoint by Shor, and a precise classical factoring
reduction. Neither its existence, novelty, nor an advantage beyond factoring
is asserted. If the recurrence cannot be closed, park it; do not substitute a
fixed-degree theorem or a new wrapper around GRH compact isotropy.

## Corpus and comparison

Both `been-tried` and `baselines` were run through
`/opt/anaconda3/bin/python tools/corpus/cli.py` for each of:

- `Topological data analysis Betti number sparse boundary Laplacian`
- `density of states local Hamiltonian spectral density`
- `structured exact optimization integer programming`
- `quadratic tower norm equation growing degree number field conic`
- `Kronecker tensor product irrep sampling Jucys Murphy`

Absence of a relevant hit was not treated as evidence. The broad old regulator
and tensor-network impossibility records are quarantined and were not imported.
The fresh local compendium was read by relevant sections, rather than taken as
certification of all its cited primary theorems.

**1. Structured exact optimization.** Native input is an explicit cost function
on a constrained combinatorial set, with a computable reversible walk; output
is an exact minimizer. The generalized short-path mechanism uses the walk
and a coherent stationary guiding state. The advertised improvement changes
an exponential search exponent, roughly from a stationary mass exponent
1/2 to 1/2-c/2. It does not give polynomial time for exponentially rare optima.
Preparing the stationary state, the walk/gap hypotheses, and the overlap gain
must all be paid. The strong attacks are specialized exact algorithms,
branch-and-bound and the dequantization of the original CSP regimes, not
merely stationary sampling. The cheapest rejection for this pass is already
quantitative: the proposed regime is still exponential, with no new operation
that changes that regime. Compendium §8.1, LF2831–2990, explicitly limits the
comparison and discusses Le Gall–Tamaki 2604.12131. The latter paper itself was
not supplied/read, so its scope is not enlarged to every generalized variant.

**2. High-dimensional persistent/ordinary Betti numbers.** Native input would
be a classical point cloud or graph plus a filtration and a growing degree k;
output is a specified relative-accuracy Betti estimate. The quantum mechanism
is boundary/Laplacian access and spectral filtering. It needs a paid state over
simplices, enough kernel mass, and a sufficiently large relevant spectral gap;
none is supplied free. Classical boundary reduction, discrete Morse methods,
sparsity, and fixed-dimensional geometry are the required comparisons.
The compendium's explicit random-graph example is a quartic speedup, while
its superpolynomial regime still requires the large-Betti/gap premises.
No native family and new operation paying those premises was identified.
Cheapest falsifier: calculate those two parameters on the proposed native
family before doing any circuit work. Do not fetch another TDA source merely
to restate this gate. See §9.2, LF3112–3203. Original persistent-Betti papers
were not read, so no new theorem or general lower bound is inferred.

**3. Infinite-temperature spin response via a Choi state.** This is an explicit,
well-motivated clean contract, but it fails the new-operation test. For example,
input a rational bounded-coupling spin chain
  H = sum_j [J_j(X_j X_{j+1}+Y_j Y_{j+1}) + Delta_j Z_j Z_{j+1}]
      + sum_j h_j Z_j,
and let O=Z_1. Output a sample from its infinite-temperature response measure
  mu_O = 2^(-n) sum_{a,b} |O_ab|^2 delta_(E_a-E_b),
smoothed into a specified partition of unity with frequency width delta.
There is no thermal/ground-state advice or rare-event normalization: Bell
pairs prepare |O>> of norm one, and H tensor I - I tensor H^T has exactly this
spectral measure. Ordinary simulation and phase estimation give the expected
polynomial cost for inverse-polynomial resolution/accuracy. Smoothing avoids
silently promising a spectral gap at hard bin boundaries. But this is precisely
standard simulation/QPE, not a new primitive. At Delta_j=0 the Jordan–Wigner
free-fermion reduction already gives a polynomial classical sampler: for the
one-site density response, sample two one-particle eigenvalues with weights
|v_a(1)|^2 |v_b(1)|^2 and return their difference. At nonzero interaction the
strong attacks are Krylov/KPM, tensor-network dynamics, short-time cluster
methods and hydrodynamic/coarse-response approximations; no universal match
or hardness conclusion follows. Generic BQP encoding does not repair the
research-value objection. Compendium §§6.2 and 6.4 motivate the observable
and list these limitations, especially LF2311–2334. Do not reopen the parked
driven cut-and-join universal-encoding result under this name.

A fourth apparent alternative, Kronecker irrep sampling through diagonal
Jucys–Murphy operators, is already represented by the corpus label-transform
work. It is different from the refuted RSK composition, but not a new local
operation. Label/tableau resolution also does not construct a multiplicity
basis. The revised representation-multiplicity literature/Panova match needs
its actual source before a scope claim; no such claim is made here.

## Selected native contract

Input: an explicit tower Q=F_0 subset F_1 subset ... subset F_h, with
F_j=F_(j-1)(sqrt(d_j)), each step genuinely quadratic, N=2^h, and expanded
rational tower coordinates. Count the numerical degree N, all coefficient
bits B, and the size of the explicitly listed finite rational support S.
S includes 2, ramification and the required denominators; at each level take
all primes over S. Field/ideal arithmetic and finding those primes must be
charged, not supplied as a class-group or maximal-order oracle. The native
input is not a succinct circuit hiding an exponential degree.

Output: a complete independent F_2 basis of
  F_h(S_h,2) = {a in F_h*: v_P(a) is even for P outside S_h}/F_h*^2,
with expanded polynomial-bit representatives and recorded coordinate maps
for supported input classes. Seek a finite bounded-error clock polynomial in
N, B, |S| and log(1/eta), with integer factoring as the only nontrivial
classical oracle. No GRH, class generators, fundamental units, odd class
number, or uncharged expansion of a compact witness is an input promise.

The immediate subproblem is to obtain and compose the required norm/conic
lifts along this tower. It is NOT legitimate to assume a degree-uniform
solver for arbitrary 3/4/6-variable forms as an additional oracle. A result
conditional on such a solver is only a reduction, not the requested compiler.

## The new quotient-kernel operation is algebraically valid

Let L=F(sqrt(d)) and let S contain all ramified and dyadic F-primes. Assume
complete supported-squareclass presentations over F and the stated conic
witnesses are actually available. Put
  V = F(S,2) intersect N_(L/F)(L*).
Choose a basis a_i of V and beta_i with N(beta_i)=a_i times a square. At every
outside-S split prime, the two valuations of beta_i have equal parity; at an
inert prime there is a single parity. Thus the outside-S parity divisor of
beta_i is the pullback of a finitely supported F-prime vector J_i.

Collect their support in E. For expanded witnesses this is effective: clear
an integral-order denominator R and factor both R and N_(L/Q)(R beta_i),
then include all base primes above these rational primes. Norm primes alone
are insufficient: opposite split valuations can cancel in the norm.
Compute
  W = image(F(S union E,2) -> F_2^E),
  C = kernel(F_2^(dim V) -> F_2^E/W),  c |-> sum_i c_i J_i mod W.
For each basis vector c of C, the recorded W-presentation supplies gamma_c
with that parity, so alpha_c=(product_i beta_i^c_i) gamma_c has even
outside-S valuations and norm squareclass product_i a_i^c_i.

This gives the ENTIRE norm image. Indeed, if alpha already has even support
and its norm is the same squareclass as beta=product_i beta_i^c_i, then
z=beta/alpha has square norm s^2. The elementary identity
  (z+s)^2 = (Tr(z)+2s) z
shows z=gamma delta^2 for gamma in F*, apart from z=-s, which is already
scalar. Outside S there is no ramification, so gamma has parity J_beta and
has even valuation outside S union E. Hence J_beta belongs to W and c to C.
The norm kernel is F(S,2)/<d>, by the same identity and unramified valuations.
Consequently the actual exact sequence is
  0 -> F(S,2)/<d> -> L(S_L,2) -> C -> 0.
The final term is C, not all V unless the parity obstruction vanishes.

This removes the odd-S-class premise in the FIXED quartic construction: the
base is quadratic, its complete supported-squareclass compiler is already
paid, and Kutas supplies polynomial-bit expanded conic witnesses. Polynomially
many fixed-degree products and one enlarged base support preserve the bit
clock. This is a proved correction at that scope, not a growing-degree
algorithm admission. The parent should separately record the changed scope.

## Why h=log_2 N does not yet prove a polynomial clock

Name A_j the supported-squareclass/coordinate operation over F_j, and I_j(r)
the promised-isotropic r-variable form operation, for r in {3,4,5,6}.
The actual local sources give the following dependency structure.

1. **Conic descent:** Kutas Algorithm 1 and Remark 22 reduce I_j(3) to a
   bounded number of 3-, 4-, and 6-variable form problems over F_(j-1), plus
   field arithmetic. The form dimension can remain bounded. This part is
   genuinely favorable; the dimension need not double at each level.
2. **Dimensions 5 and 6:** Koprowski Algorithms 2 and 4 use local conditions
   and weak approximation to reduce to dimension 4. Real embeddings and
   approximation bits grow with the field degree and must be bounded, but
   there are only constantly many dimension reductions here.
3. **Dimension 4:** Koprowski Algorithm 1 first constructs A_j(S), solves
   Hilbert-symbol/sign equations, may enlarge S by an auxiliary prime until
   they are soluble, and then calls TWO I_j(3) problems. Thus it does not
   furnish a constant-branch descent consisting only of lower-degree conics.
4. **Squareclasses:** A_j needs A_(j-1)(S), one I_(j-1)(3) norm lift for EACH
   basis element of V, and A_(j-1)(S union E) for the quotient-kernel step.
   The number of lifts and E are not fixed constants. Complete coordinate
   maps, not just valid output classes, have to be retained.

These dependencies are well founded in degree (with bounded dimension
reductions), so the issue is not a formal infinite recursion. The issue is
its TOTAL work and heights. Constant branching C at h levels would indeed
cost C^h=N^(log_2 C). In contrast, a naive recurrence with a polynomial-degree
factor at every level, T_j <= poly(2^j) T_(j-1), yields only a
2^{O(j^2)}=N^{O(log N)} upper bound even before support/height growth. This is
not a lower bound on every algorithm. Batching all form tasks at a level,
reusing a common support presentation, and controlling subsequent support
expansion might improve it; that is a concrete operation to prove, not a
license to count the branching as constant already.

There are two further independent gates:

- **Auxiliary primes.** Koprowski's Proposition 4.5 proves existence of one
  extra prime, not a polynomial BIT search clock. Appendix A LF847–866
  bounds a successful density by an inverse product of numerical prime norms
  and then incorrectly calls its inverse polynomial in bit-size. One large
  prime already defeats that inference. This invalidates that clock argument,
  not the algorithm or every possible faster prime-selection method. The
  fixed-base rational/quadratic routines avoid importing this claim; the
  growing-base recursion must also do so.
- **Expanded heights/support feedback.** A polynomial bound at each individual
  call is insufficient after h compositions. For example, repeated squaring
  of the bit bound gives B^(2^h), not poly(N,B); repeated multiplication by
  degree factors can also give N^{O(log N)}. One needs a bound in the ORIGINAL
  input, or a proved additive/mild recurrence, for all conic coordinates,
  norms/denominators, new primes and coordinate presentations. Compact unit
  or norm expressions cannot be factored for their full support at zero cost.

Direct corestriction of a quaternion algebra from degree N to Q has degree
2^N and dimension 4^N; it is not a substitute polynomial construction. The
quadratic step in Kutas keeps degree 4, but its compression/conic steps must
be paid each time. No general-field factorization-only conic theorem was
verified from the retained sources. This is an exact source limitation, not
a claim that no such theorem exists in the literature.

## Existing quantum endpoint and the precise next acceptance test

`GLOBAL_COMPACT_ISOTROPY.md` and `TENSOR_SQUARE_RATIONAL_NORMS.md` already give
growing-degree quantum compact-output endpoints under their written GRH and
input assumptions. Kutas–Montessinos 2307.00261v3 Theorem 4.13 also uses global
class/S-unit machinery. Reusing it here is neither an unconditional factoring
reduction nor a free source of expanded support. The proposed attack must
change that interface, rather than rename the admitted endpoint.

Next single question: **can the above mutually recursive bounded-dimension
form and quotient-kernel operations be organized with a polynomial aggregate
support/height clock for an arbitrary explicit quadratic tower?** Start by
writing its dependency DAG and proving or refuting a global batching invariant.
In parallel within that same proof obligation, identify an actual bounded
prime/local-condition selection replacing the invalid Appendix A clock.
The cheapest falsifier is a precise unavoidable use of complete class groups,
a new same-degree squareclass oracle, uncontrolled expanded witnesses, or a
non-polynomial recurrence in the proposed implementation. Such a finding
rejects THAT implementation; it is not a lower bound for all tower algorithms.

Positive acceptance requires explicit polynomials in original N,B,|S| and
log(1/eta), finite clocks, complete basis/relations, native local arithmetic,
and all witness supports. A fixed h theorem, a numerical prime-norm bound,
or a generic compact norm/isotropy oracle fails acceptance. No implementation,
full Selmer promotion, novelty, or speedup claim follows from this selection.

## Local source locators for the next proof

All line numbers here use physical LF, `split('\n')`.

- `audits/sources/selmer_classical_two/kutas_quadratic_conics.txt`:
  abstract LF19–24; general-field limitation LF183–198; quaternion descent
  Corollary 19 LF380ff; Theorem 20/Remark 21 LF417–445; crucial Remark 22
  LF446–459. This last passage explicitly says 3/4/6-variable base forms.
- `audits/sources/global_isotropy/vectors.txt` (2111.08569v2): prerequisites
  LF145–162; four-variable splitting LF197–208; Proposition 4.5 and Algorithm 1
  LF315–422; Algorithms 2 and 4 LF517–544 and LF626–660; Appendix A LF793–904.
  It explicitly imports norms and complete squareclasses. Its BIT-clock
  inference at LF859–866 is not accepted.
- `audits/sources/global_isotropy/amitsur.txt` (2307.00261v3): global class/
  S-unit interfaces LF212ff and LF1073ff; Theorem 4.13 LF1164ff. Its exact
  compact/expanded interface is recorded in `GLOBAL_COMPACT_ISOTROPY.md`.
- `QUARTIC_RELATIVE_NORM_CLASSICAL.md` LF83–113 is the existing surjective
  correction under odd S-class order. Replace only that surjectivity with
  the quotient-kernel proof above; do not assume it iterates with a good clock.
- `audits/reviews/2026-11-13-independent-upside-selection.md` LF143–182
  contains the earlier proposed kernel operation, independently checked here.
- `audits/sources/2026-11-13-opportunity-selection/compendium.txt`:
  §§6.2,6.4,8.1,9.2 at LF1985,2249,2831,3112, respectively. It is used for
  direction screening; unread cited papers are not treated as verified inputs.
