# Uniform Compilation Of The Prime-Field Rees Receiver

30 October 2026. Written existence argument and primitive-resource certificate,
not a circuit generator, hardware execution, human peer review, or novelty claim.
This discharges a particular uniform-efficiency obligation of the proposed Rees
construction, conditional on its existing algebra/source identities. It does
not independently re-prove the entire HSP reduction.

## Scope And Conclusion

Supply public structure constants for an n-dimensional Lie algebra over a
verified prime field F_p, with actual nilpotency class c<p. Supply the exact
ordinary coherent, fixed-width hiding oracle from the manuscript. Its cost
T_f is separate from both label width and query count. Use the whole-grade
SDE regime accepted by `symmetric_recovery_budget`; no fallback to smaller
fields, arbitrary black-box group presentations, or prime-power rings occurs.

For these inputs, the complete bounded, abort-flagged Rees procedure has a
uniform finite-gate implementation with the same parameter dependence as
the existing source/solver bounds. Uniform receiver efficiency need not be
introduced as an additional unproved primitive. The scalable gate generator
and its machine-checked connection to the mathematical receiver are still
absent. Those implementation/formalization gaps are distinct from circuit
existence. The always-valid total-policy Lean interface is not instantiated
by a randomized controller that can abort.

The argument combines the existing [uniform BCH recurrence](DERIVED_RANK_REES_EXTENSION.md),
[bounded classical solver](POWER_SDE_RANDOMNESS_BUDGET.md), and
[whole-grade forest](REES_FULL_GRADE_PARAMETER_BOUND.md). It refines their
accounting; it is not a separate new quantum algorithm.

## Canonical Encodings And Clean Arithmetic

Encode each coordinate 0,...,p-1 in b=ceil(log_2 p) bits. Other b-bit words
are padding, not alternative encodings of field elements. Replacing every
word by its residue modulo p is not reversible: it aliases 0 and p.

At grade d put D_d=sum_{j<=d} r_j, where r_1=n and r_j=dim gamma_j(L).
Quotient projection deletes the top grade; its public section zero-pads it.
The section need not be a homomorphism. No hidden-intersection coordinates
or table indexed by group elements are required. Dilation multiplies grade
j by s^j, with s measured/classical and nonzero on active slots.

For fixed public s and a coherently controlled quotient coordinate u, define

    P_u(x) = BCH(x, -Delta_s(section(u)))

on canonical u,x when s!=0. On invalid u or x, and on every s=0 slot, set
P_u(x)=x. In particular, never interpret a zero-scale slot as Delta_0. The
inverse uses the positive translation on canonical inputs and identity
elsewhere. Both preserve canonical validity and are total binary permutations.

To implement the permutation in place with a fresh equal-width scratch:

    (x,0) -> (x,P_u(x)) -> (P_u(x),x) -> (P_u(x),0).

The first and last arrows are XOR function evaluators; each computes its
classical function, copies by XOR, then uncomputes its internal workspace.
The middle arrow swaps. Thus one controlled in-place action costs at most
four BCH arithmetic passes, not one. With nonzero initial scratch, it is
still a reversible gate composition but does not promise clean scratch.

The existing ODE recurrence evaluates one BCH operation with exactly

    B(d) = (d-1)d(d+1)(d+2)/6

bracket calls in its unoptimized schedule. A dense bracket costs O(D_d^3)
field operations; other vector arithmetic is polynomial in d,D_d. Public
denominators are integers at most d<p. Keeping all coefficients modulo p
gives a conservative Boolean size O((d+1)^4(D_d+1)^3(b+1)^3). Standard
compute/copy/uncompute with NOT, CNOT and Toffoli yields polynomial clean
reversible size/workspace. This assumes public polynomial arithmetic for
the section/bracket; an arbitrary Python callback does not itself certify
that assumption. The Rees zero-padding section and supplied structure tensor
have it. No free-Lie word expansion or p-sized lookup is involved.

Central measurement is cheaper: addition by an element of the highest
grade is coordinate addition, so each target needs only r_d controlled
modular subtractions. The ordinary source lift uses c public linear maps
E_s, c original oracle calls, and uncomputation of the E_s workspaces.
Extend each E_s evaluator to a total binary function, for example mapping
invalid inputs to zero in its query workspace. Always issue the ordinary
oracle call on that workspace; no coherent control of an unknown oracle
is needed. Its behavior on invalid source words need not match an ideal
Rees lift. Classical abort branches may skip calls and are charged at the
same padded cap.

## Fourier Accuracy And A Restricted-Domain Hybrid

[Cleve--Watrous, section 1 and section 7.1](https://arxiv.org/html/quant-ph/0006004v1)
provide uniform arbitrary-modulus QFT circuits, with all-input Euclidean
accuracy including ancillas, and size polynomial in b+log(1/eta). This is a
phase-sensitive isometry guarantee, not a guarantee on basis-state output
probabilities. Their arXiv and conference theorem numbering differs; the
section references here identify the imported construction unambiguously.
[Dawson--Nielsen](https://arxiv.org/abs/quant-ph/0505030) supplies efficient
finite-gate approximation with polylogarithmic precision overhead.

More explicitly, let J embed canonical coordinates with fresh zero workspace,
and let C be the compiled unitary. Require

    ||C J - J F_p||_op <= eta.

Its adjoint has the same bound because

    C^dagger J - J F_p^dagger
      = C^dagger (J F_p - C J) F_p^dagger.

Approximation only after discarding dirty workspace would not suffice for
this inference. All internally controlled, known phase gates must be
synthesized with their relative phases intact. If a preliminary QFT has q
elementary gates, allocate eta/(2q) synthesis error to each and eta/2 to
the preliminary approximation. This keeps the final size polynomial in
b+log(1/eta). No unknown-unitary control is assumed. In the outer receiver
the QFTs are not coherently controlled; the controlled operations are the
explicit arithmetic permutations above.

The QFT need not approximate identity on invalid binary strings. Here is
the sufficient replacement for an unnecessarily global error contract.
Every actual operation is a total CPTP map. Every ideal prefix preserves
its designated canonical subspace, including valid zero dummy registers
after abort. Extend ideal operations arbitrarily outside that subspace to
make them total. Pad stopped/adaptive branches to a common finite schedule.
For actual stages E_j and ideal stages I_j,

    E_N ... E_1 - I_N ... I_1
      = sum_j E_N ... E_(j+1) (E_j-I_j) I_(j-1) ... I_1.

Each local comparison has an IDEAL prefix, hence a canonical input. Its
phase-sensitive isometry error eta_j bounds half trace distance by eta_j,
also after tensoring an arbitrary reference. The actual suffix is
contractive even if actual intermediate states have leaked into padding.
Consequently the complete output channel, restricted to the canonical
input embedding, has half-diamond error at most sum_j eta_j. This is the
restricted-domain version of the standard
[composition estimate, Watrous proposition 3.48](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf).

For measured adaptive transcripts, apply the bound in each canonical
classical block uniformly; sum weighted errors, not one error per possible
record. Cover all records reachable from the claimed canonical input
domain, not only the positive-probability records for one hidden subgroup.
Malformed binary records abort deterministically. Canonical labels outside
the hidden annihilator are NOT recognizably malformed: the ordinary bounded
controller runs on them without a hidden-membership test. Their zero ideal
probability and possible approximation-induced mass are handled by the
unconditional hybrid, never by postselection or division by success mass.

For joint source error delta, including retained references, the error is
delta+sum_j eta_j. Per-marginal source errors do not imply this premise.
Alternatively, flatten all fresh preparation channels and conversions into
one forest schedule. Actual predecessors need not remain independent or
transcript-independent; only the ideal prefixes satisfy the ideal promises.
The correctness claim for independent coset states does not thereby become
a claim about arbitrary correlated input banks.

The controller uses measured labels/private coins only, verifies every
witness and its nonempty support, and consumes every target including
zero-scale targets. The existing finite random-bit/root-splitting caps
bound every branch; retries reuse classical labels, not fresh quantum
banks. Its abort event is retained in the output. Classical work is summed
over forest nodes, not multiplied by the number of possible transcripts.

## Primitive Counts And Precision

Let m be the final Fourier sample count, M_d the whole-grade arity, and

    v_d = m product_{j=2}^{d-1} M_j,
    L = m product_{j=2}^c M_j,
    T = sum_d v_d,
    I = L+T+m.

The ordinary-oracle schedule has these padded upper counts:

| Primitive | Count |
| --- | --- |
| Original coherent oracle calls | c L |
| Leaf E_s compute/uncompute pairs | c L |
| Leaf single-coordinate QFTs | D_c L |
| Grade-d single-coordinate QFTs | v_d(2 M_d r_d+D_(d-1)) |
| Final single-coordinate inverse QFTs | m n |
| Central coordinate subtractions | sum_d v_d M_d r_d |
| Noncentral controlled right actions | sum_d v_d M_d = L+T-m |
| BCH arithmetic passes | 4 sum_d v_d M_d |
| Bracket calls | 4 sum_d v_d M_d B(d) |

The quantum Fourier count N_F is the sum of its three table entries. Each
M_d>=2, so T<=L-m. Bounding dimensions by D_c and using the forest edge
identity gives N_F<=6 D_c L. This loose envelope also covers c=1, when
N_F=2nm and there are no merges.

For compatibility with the existing equal-per-instrument allocation choose

    q_max = max(D_c, n, max_d(2 M_d r_d+D_(d-1))),
    eta = epsilon/(3 I q_max).

Each instrument then has approximation error <=epsilon/(3I); the whole
Fourier schedule contributes N_F eta<=epsilon/3. The exact certificate
reports the smaller N_F eta as well as the prior conservative allocation.
Only O(log I+log q_max+log(1/epsilon)) precision bits are required. Existing
rank and bounded-SDE failure shares supply the other two thirds.

The resulting nonoracle bound consists of the charged classical SDE work,
the listed BCH/linear/central arithmetic, and

    N_F poly(log p + log(1/eta))

finite gates. Every polynomial exponent is absolute, including when c grows.
This preserves the previously derived parameter exponents. Arithmetic is
exact in the ideal gate model; physical noise is not included. If the
original oracle is approximate, its query-weighted complete-channel error
must be charged separately. A label width is not an oracle runtime bound.

## Controls, Falsifiers, And Remaining Work

`python qsearch.py power-sde --uniform-instrument --write` writes
`research/reductions/rees_uniform_instrument.json`. It computes primitive
caps and exact rational errors, not quantum output samples. Source hashes
identify the calculation; they do not certify any theorem.

`guarded_bch_permutation.py` checks binary permutation semantics. Its tests
use independent Heisenberg multiplication, a nonhomomorphic section,
all padded controls/targets over F_3, arbitrary scratch, zero scales and
sampled 127-bit field coordinates. This is not a scalable emitted circuit.
Separate bounded matrix controls expose why label-only, phase-insensitive,
or dirty-workspace checks would accept incorrect implementations.

Decisive remaining obligations are:

- Validate the underlying Rees algebra/source/correctness argument and its
  prior-art status independently. This note does not settle either.
- Build and verify an actual circuit generator and failure-aware formal
  instrument only when that has higher value than mathematical/application
  work. Do not claim those are already implemented.
- Supply a motivated native input/oracle with a paid preparation/evaluation
  cost that survives matched classical attacks. No such application follows
  from uniform compilation; the latest applications were filtered out.
- Reject any extension that needs an unknown hidden basis, group-sized
  table, hidden-label test, unbounded retries, marginal-only source promise,
  or successful-branch normalization. Those invalidate this derivation.
