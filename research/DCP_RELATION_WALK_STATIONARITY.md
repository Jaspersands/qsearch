# Native Signed-Relation Walk: An Executed Falsifier

LOCAL DERIVATION / REVIEW PENDING. No independent theorem review, native
polynomial witness finder, accepted candidate, novelty or quantum speedup.

## Why Test This

The decoder frontier leaves an arithmetic collision walk as an open route.
The existing `dcp_linear_depth_fiber_walk_no_go.py` rejects explicit small-block
moves; the existing short-relation theorem finds many weight-m/4 relations
that undermine an SVP embedding. Neither settles what a label-adaptive
dictionary of LONG relations does to the supplied quantum state.

This pass implements that primitive and tests its actual action, not merely
its abstract graph gap. It does not audit or refute quantum subset-sum walks
that search a different vertex space with marked vertices and memory. Preserve
the separate primary-source conformance audit for those algorithms.

The [Bacon--Childs--van Dam measurement connection](https://arxiv.org/abs/quant-ph/0501044)
is prior work. A favorable collective measurement exists information-theoretically;
that fact does not make within-fiber mixing an efficient implementation.

## Actual Reversible Move

Let F_A(x)=A*x modulo q for physical Boolean x. A signed relation
delta in {-1,0,1}^m satisfies A*delta=0 modulo q. Let P be its positive support,
N its negative support, r=|P|+|N|. Swap the two patterns

    x_P=1,x_N=0  <-->  x_P=0,x_N=1,

leaving all other bits free and fixing words that match neither pattern.
This is a complete basis involution with known inverse, not a partial map.
Verify the relation in polynomial arithmetic time; the conditional swap has
polynomial known-circuit cost with reversible pattern-check ancillas.
`signed_relation_swap` implements the complete basis map.

The move preserves F_A on EVERY physical word. Therefore it also preserves
the supplied state, for EVERY fixed full secret s:

    |psi_s> = 2^(-m/2) sum_x chi_s(F_A(x))|x>.

Its active fraction on uniform physical words is EXACTLY2^(1-r). Postselecting
the two endpoints or compressing their redundant bit must charge that Born
probability. Long relations do not become cheap just because verifying them is.

## Nonzero Walks Can Have Exactly Zero Effect

For any undirected, positively weighted equal-sum graph, define its Laplacian

    L_A = sum_(x,y edges) w_xy (|x>-|y>)(<x|-<y|).

Every edge has F_A(x)=F_A(y). The unknown input amplitudes are equal on that
edge, hence L_A|psi_s>=0 EXACTLY for every s. Thus

    exp(-i*time*L_A)|psi_s>=|psi_s>

at every time. Phase estimation of this Laplacian yields eigenvalue zero,
independent of s. This remains true on a COMPLETE fiber graph, even with large
spectral gaps, nonconstant degrees or label-adaptive weights. Faster mixing
is not the missing resource: the input already is uniform inside each fiber.

The module constructs three actual nonzero weighted full-fiber Laplacians on
IID native matrices, including vector labels, and diagonalizes them. For every
secret the residual and positive-eigenvalue source mass are below numerical
tolerance. The graph enumeration is a bounded verifier, not a uniform algorithm.

This stationarity statement is specific to the graph Laplacian and the raw
clean input. A non-Laplacian adjacency Hamiltonian on an irregular graph need
not fix the state. Nevertheless, any unitary that preserves each F_A fiber
commutes with the diagonal character action. Computational-basis measurement
after that unitary alone has probabilities independent of s: its amplitudes
are chi_s(t) times a secret-independent transformed vector in fiber t.
This does not prohibit a later inter-fiber coherent measurement.
The report records a strictly positive adjacency energy variance for the
SAME graphs as a countercontrol: it does not label all fiber Hamiltonians
stationary just because their Laplacians are.

Do NOT generalize the argument to arbitrary coined/Szegedy walks, transverse
drives, marked-vertex search, or arbitrary fiber-preserving unitary PLUS a
subsequent noncommuting readout. Their initialization and readout need separate
analysis. The desired uniform-fiber erasure is not supplied by mixing: it must
coherently identify/relabel fibers without retaining distinguishing histories.

## Label-Adaptive Dictionary Source Gate

Let G=q^n=2^(nL), m=nL+Delta. For every fixed nonzero signed relation delta,
one coefficient is a unit, so A*delta is exactly uniform over the full group
on IID native A. The probability that it vanishes is1/G. Quotient by global
negation; the number of classes with support at most w is

    C_(m,w)=sum_(k=1..w) binomial(m,k)*2^(k-1).

Union bound gives Pr(any relation of support<=w)<=min(1,C_(m,w)/G).
This counts ALL supports and signs before sampling A, so it covers arbitrary
label-adaptive selection of an explicit dictionary. It is not restricted to
a predetermined set of small blocks.

On the complementary event, EVERY relation has r>=w+1. Any explicit dictionary
of K relations therefore touches at most K*2^-w of uniform physical words.
The same number is the squared norm of the raw phase state projected onto
the dictionary's applicability set, since its word probabilities are uniform.

The module uses exact integer binomial sums, not approximate entropy, and
charges capped rational probabilities. At n=8,16,32, L=4n+1, Delta=16,
w=floor(m/5), K=m^4, source failure is bounded by2^-10,2^-72,2^-316.
On good source matrices, applicability remains K*2^-w, exponentially small.
Asymptotically, H_2(1/5)+1/5<1 explains the constant-fraction threshold.
This does not contradict the earlier existence theorem at support near m/4:
that larger fraction has entropy H_2(1/4)+1/4>1.

The unconditional probability that a clean-state applicability measurement
succeeds is at most source_failure+K*2^-w, capped at1. No IID assumption across
different move tests or fixed dictionary independent of A is used.

## Surviving Research Directions

- A genuinely implicit WORD-dependent neighbor algorithm is not an explicit
  polynomial dictionary. Construct it with charged arithmetic/runtime; it is
  closely related to the unresolved physical witness problem, not free access.
- A transverse drive or subgroup-covariant inter-fiber operation can change
  the unknown state. Give the actual operator, initialization and readout;
  a mixing-time proof for a fiber graph is insufficient.
- Ancilla coupling can be nontrivial; do not claim stationarity after changing
  the prepared state or Hamiltonian. Derive its actual source amplitudes.
- Known marked-target arithmetic search is a different task; compare its cost
  with Grover, lattice and subset-sum baselines before proposing a speedup.

The next serious walk construction must name which of these boundaries it
crosses and demonstrate the resulting unknown-state dynamics. Do not merely
add longer known relations to an otherwise stationary fiber walk.

## Artifacts

    python theorems/dcp_relation_walk_stationarity.py --save
    PYTHONPATH=theorems python -m pytest -q tests/test_dcp_relation_walk_stationarity.py
    node research/certificates/dcp_relation_walk_crosscheck.js

The live report stores the complete swap, actual graph edges, native source
controls and scaling ledgers. The tests and crosscheck are targeted code
verification, not independent theorem review. Gemini owns production wiring.
