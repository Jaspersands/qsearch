# Bounded-Index HSP: A Uniform Terminal Reduction

2026-10-23. Local proof and public arithmetic controls; independent review
pending. CONDITIONAL on the proposed Rees theorem and the previously audited
opaque-group/normalizer interface. No natural hard source, quantum receiver,
classical lower bound, novelty certification, or Shor-level result.

This bundle is outside the source and staging repositories while their copy
is active. It is not integrated, committed, or pushed. It replaces neither
the original Rees whole-proof audit nor the earlier normalizer audit.

## What Was Missing

The previous bounded-index reduction leaves a group Q with

    |Q| = p^m,  m <= k(k+1)/2,  class(Q) <= 2k-1,
    [Q:J] <= p^k.

The central-rank improvement proves an explicit exponent-p Lie terminal
bound 2^O(k^2 log(k+2)), but did not extend that bound to all primes or
higher-exponent opaque groups. Importing a fixed-class polynomial theorem
is insufficient: a cost (log p)^c would not give the desired uniform bound.
Reducing to a hidden cyclic subgroup can also replace k by an index of
order m. The following construction avoids both losses.

The native inverse-trace problem was triaged first. Conic parametrization,
low-degree multiples, list-recovery keywords and known accepted flats did
not produce a new solver. No new dequantization or hardness claim is made.
This pass instead closes a specific parameter-accounting gap in a live
algorithmic proposal; it is not another source assumption or oracle family.

## 1. Small Primes Are A Bounded Enumeration

If Q is abelian use known abelian HSP. Otherwise let c be a known valid
class bound no larger than 2k-1. If p<=c, enumerate Q from paid normal-word
coordinates, evaluate the original hiding function on each representative,
and retain its identity fiber. Generator extraction is charged too. Then

    |Q| <= (2k)^(k(k+1)/2) = 2^O(k^2 log(k+2)).

This is a CLASSICAL terminal branch. It does not enumerate the original
potentially much larger group. Nor does it claim a quantum advantage when
the original prime or index is small. An unnecessarily loose c may select
this branch, but the displayed cost remains valid.

## 2. Large Primes: Complete Order-p Intersections Preserve k

Suppose p>c. The elements of order dividing p form the characteristic
subgroup A=Omega_1(Q), of exponent p. This is the familiar regular/Lazard
case; it is not true for every p-group. Restrict the ordinary oracle to A
and find the COMPLETE K=J intersect A by the proposed exponent-p solver.

The injection A/K -> Q/J on left cosets gives [A:K] <= [Q:J] <= p^k.
If K=1 then J=1, since every nontrivial finite p-group contains an element
of order p. Otherwise set S=N_Q(K). Since A is characteristic in Q and J
normalizes itself, J normalizes J intersect A; hence J<=S. Now K is normal
in S and contained in J. Replace

    (Q,J) by (S/K,J/K),
    k by k-log_p[Q:S].

The quotient p-length strictly decreases. Repeat at most the original m
times. Its class never increases, and its hidden index exponent never
increases. Pull back the final result along the known sections and include
every learned K. A section need not be homomorphic: the original f is
constant on the divided-out subgroup. Maintain an original-group pair S/B
instead of nested encodings, as in the prior quotient bridge.

This is different from restricting once and stopping. In C_(p^4) with
J=Q, a single call returns only p elements. Repeated quotients recover the
full subgroup. It also differs from normalizing an arbitrary known piece
of J: only completeness makes J normalize K. A proper subset can pass all
membership checks and cause loss of genuine hidden directions.

The earlier normalizer audit already pays for known subgroup normalizers
using collection and existing solvable-group quantum preprocessing. That
interface is inherited, not re-proved or implemented by this bundle.

## 3. Construct Omega_1 Without Hiding A Class-Dependent Bit Exponent

One can use the order-p subgroup routine in Section 3 of
[Ivanyos--Sanselme--Santha](https://arxiv.org/html/0707.1260), with its paid
collection interface. Here is an alternative making the parameter cost
explicit, including general exponents.

Let the current p-length be r<=m and use the safe exponent bound p^r.
Compile inverse-BCH addition and bracket over R=Z/(p^r), not over F_p.
Every divisor 1,...,c is a unit since c<p. The Lazard formulas consequently
act on the whole current group as Lie-ring addition and bracket. Reducing
power coefficients modulo p instead is WRONG for exponent p^2; the exact
UT_3(Z/9) control demonstrates this, even though class2<3.

The construction is the EXISTING Dynkin filtration-correction compiler,
specialized before computation to R. It is not new inverse-BCH mathematics.
Effective inverse BCH is established prior art; see the
[Cicalo--de Graaf--Vaughan-Lee abstract](https://www.sciencedirect.com/science/article/pii/S0021869311007009).
No unread complexity theorem from that article is imported here.

Retain associative words on two letters through degree c. There are
M=2^(c+1)-1. At degree d, correct the logarithm residual R_d by right-nested
group commutators with coefficients -coeff_w(R_d)/d. The Dynkin identity
reconstructs each homogeneous Lie polynomial in degrees d<p. After each
stage the previous degrees stay correct, and the final expansion is exactly
exp(X+Y) or exp([X,Y]). The group-commutator convention is xyx^-1y^-1.
The [Blessenohl--Laue survey](https://radon.mat.univie.ac.at/~slc/s/s29laue.pdf)
states the Dynkin criterion; the integral identity remains valid after
base change wherever d is invertible. The local verifier checks every
coefficient and stage over R, including the final operation.

Memoize each nested commutator by its binary word. There are at most
B=2^(c+1)-2 such words. A commutator uses three products and two powers;
each correction uses at most one power and one product. Thus the number
of straight-line instructions is at most I=7B+5. Each tensor product is
O(M^2) coefficient operations, and each formal exp/log/power uses O(c)
such products. Compilation plus verification costs

    O((I+c)*c*M^2) coefficient operations = 2^O(c)*poly(c),

up to polynomial word-index overhead. Storage is O(I*M) coefficients,
each of O(r log p) bits. Extended Euclid and arithmetic cost a fixed
polynomial in r log p. Group evaluation costs at most

    (#multiply instructions) + 2*bit_length(p^r)*(#power instructions).

No p-entry table, root oracle, rational coefficient growth or field scan
is hidden in these bounds. The cost is exponential, NOT polynomial, in c.

Prune the supplied current group generators to at most r with paid
constructive membership. Their right-nested Lie brackets of lengths <=c
span its entire Lazard Lie ring additively. There are at most
t=sum_(j=1..c) r^j=2^O(k log(k+2)) such elements. Bracket closure and the
Lazard subgroup correspondence prove completeness; the original generators
alone need not span additively.

Evaluate their Z/(p^r)-linear combinations with the compiled addition.
This is an abelian homomorphism to the uniquely encoded underlying set.
Known abelian decomposition/kernel algorithms give invariant factors and
an additive generating basis. A factor generator of order p^a contributes
its p^(a-1) multiple to the p-torsion basis. The resulting p-torsion is
exactly A=Omega_1(Q), because group powers and Lie scalar multiples agree.
It is a Lie ideal: p[x,y]=[x,py]=0 for y in the p-torsion.

These operations use quantum abelian group algorithms when the input is
opaque. They are NOT free classical coordinates. Compute the bracket
table of A using paid additive coordinates, and use the public forward
encoder for its ordinary f calls. No coherent inverse of that encoder is
assumed. General abelian decomposition and constructive quotient tools
are existing results, including
[Ivanyos--Magniez--Santha](https://arxiv.org/html/quant-ph/0102014).

All symbol dimensions and call counts in this chart construction are fixed
polynomials in t,m,c, while coefficient widths are O(m log p). Hence the
parameter factor is 2^O(k log(k+2)), with a FIXED polynomial exponent on
the original input size and log p. A small-field exhaustive chart would
not justify this conclusion; it is the construction above that does.

## 4. Rees Rank Bound Survives Every Iteration

For the exponent-p Lie algebra L of A and its hidden subalgebra h, the
local codimension k_local is at most the current k. If h=L, every derived
central label is zero. Otherwise nilpotence implies h+[L,L] != L, giving

    dim(gamma_d L / (gamma_d L intersect h)) <= k_local-1 <= k-1,
    d>=2.

This is the central-rank lemma established in the preceding bundle. Every
observed label bank has rank at most min(dim gamma_d L,k-1). This does NOT
require the observed bank to span an entire unknown annihilator. Exact
row compression preserves its kernel; all acquired copies stay charged.

Use the prior scalar-line solver with effective degree gcd(d,p-1). A
conservative sufficient bank is (d+1)^(k-1). The product across at most
c-1 nonabelian grades is bounded by

    P <= (c+1)^((c-1)*(k-1)) <= (2k)^(2*(k-1)^2).

Known uniform scalar diagonal solving, paid chart setup, public BCH and
all fresh target preparations are still required. The general scalar
backend and quantum Rees receiver are not implemented by these controls.
The scalar dependency is specifically Fact 2 of
[Ivanyos--Santha](https://arxiv.org/html/1503.09016), polynomial in both
degree and log field size, not merely a fixed-degree assertion.
For each local call, m+ceil(log2(8m/epsilon)) final Fourier samples suffice
for its ideal span error allocation; at most m calls are made. Thus a
conservative terminal original-f query cap for these Rees sources is

    m*c*(m+ceil(log2(8m/epsilon)))*P.

This cap excludes original-f queries in the preceding outer reduction;
those are separately polynomial in original input length and log(1/epsilon).
It also is not a gate count: group operations, chart acquisition, normalizers,
word compilation, Fourier transforms and cleanup all remain paid.

On classical adaptive calls, allocate union-bounded preprocessing errors.
For coherent unique-output subroutines use the already-audited retained-
input compute/copy/uncompute compiler, with per-call failure delta and
diamond error <=4T sqrt(delta). Choose delta<=epsilon^2/(constant*T^2).
There is only logarithmic amplification overhead in T and 1/epsilon.
Cap every history, including ones following an erroneous earlier setup.
For imported Las Vegas preprocessing, constant-success fixed caps followed
by independent repetitions give logarithmic failure dependence; do not
silently use an unbounded stopping time or vote on noncanonical bases.

Combining the outer reduction, both prime branches, and these costs gives
the PROPOSED CONDITIONAL uniform bound

    2^O(k^2 log(k+2)) * poly(original input size, log p, log(1/epsilon)).

The original group's class and exponent need not be bounded, but the input
must satisfy the unique-encoding/coherent-oracle contracts in the prior
normalizer audit. This does not cover the dihedral HSP at small fixed k,
nor produce a natural hard instance. For k<=2 the known nil-2 terminal
algorithm avoids the Rees dependency; that remains reuse of known results.

## 5. Self-Attack And What Remains Unproved Here

- Omega_1 need not be a subgroup at small primes: D8 supplies a failure.
  The enumeration branch handles that regime only AFTER the size reduction.
- Stopping after one Omega intersection misses higher-order hidden elements.
  C_(3^4) with hidden whole group needs four nontrivial quotient steps.
- Incomplete intersections can normalize to a proper group not containing J.
  The finite controls deliberately exhibit this false recovery.
- Mod-p inverse-BCH coefficients fail on exponent-p^2 groups. Use a valid
  full exponent bound and retain all prime-power arithmetic.
- A false class bound makes even a valid word certificate inapplicable.
  A class-four word fails against an independent class-five matrix fixture.
- The finite controller enumerates its universe and reads identity-fiber
  membership. It substitutes for, and does NOT implement, quantum recovery.
- The compiler does not certify primality, group axioms, supplied class or
  exponent promises. Its certificate proves the public formal word only.
- This audit does not independently certify the Rees whole proof or the
  Eick/Luks/IMS normalizer-collection substitution. A failure in either
  invalidates the combined theorem; passing arithmetic controls does not
  resolve that risk. Novelty remains unchecked beyond targeted searches.
- A conditional HSP theorem without a useful surviving source is not yet
  a major algorithmic application. No new candidate admission is justified.

## Files And Handoff

- modular_lazard.py: modular version of the EXISTING filtration correction,
  with formal certificates and explicit instruction/multiplication caps.
- terminal_reduction.py: scoped parameter ledger and <=1024-element finite
  normalizer/quotient controller, clearly marked as enumerated controls.
- test_terminal_fpt.py: higher-exponent, small-prime, incomplete-intersection,
  class-bound and coefficient-tampering falsifiers plus positive controls.
- replay.py / terminal_fpt_receipt.json: deterministic public receipts and
  source hashes; no candidate registry or speedup admission.

After verified migration, Gemini can integrate the compiler specialization
with the existing universal_lazard_words module, avoiding duplicate code;
keep the finite controller in bounded research controls, not candidate search.
Update the normalizer handoff's old all-prime parameter gap with this scoped
proof, preserving its independent-review obligations. No integration, UI,
central-registry, commit or push is performed by this standalone pass.

## Verification At This Checkpoint

55 dedicated tests PASS in8.99s. All five isolated bundles together:
227 tests PASS in24.68s. All four new Python files pass py_compile. The live
receipt contains eight complete formal-word/independent-matrix controls,
two exact finite subgroup-recovery controls, three scoped parameter ledgers,
and SHA256 hashes of all five source/proof files. Whitespace checks pass.

The 127-bit-prime control also uses exponent bound p^2, so its arithmetic
modulus has254 bits. No field/group enumeration is used in that word
control. The two finite recovery controls ARE enumerated and are labeled
accordingly; their success is not a scalable quantum implementation.

Reproduce from this standalone directory:

    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q
    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python replay.py
    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python -m py_compile modular_lazard.py terminal_reduction.py test_terminal_fpt.py replay.py

Full-repository tests, qsearch.py validate, and UI syntax checks were NOT
run during the active migration. No source or staging files were changed.
All owned test processes finished; no research job was left running.

The next scientific pass should not add another neighboring parameter
variant. Prefer independent attack on the complete proposed theorem or
a concrete natural source that survives the recorded classical baselines.
