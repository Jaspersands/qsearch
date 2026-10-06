# Circuit State Isomorphism Does Not Supply A Native DHSP Decoder

LOCAL DERIVATION / REVIEW PENDING. No paper refutation, accepted candidate,
generic state-only impossibility, polynomial hidden-shift algorithm or novelty
claim. This is a transfer audit and a correction of a misleading literature
record, not a new oracle problem or restoration of circuit search.

## Research Decision

Keep circuit state isomorphism as an access-sensitive framework and source of
complexity barriers. Remove its attribution as Gowers-norm phase sieving or a
ready-to-use state-only cyclic hidden-element decoder. Three obligations must
remain separate: decision versus witness recovery, native copies versus
preparation circuits, and cyclic order versus exponent-two group structure.

[Gheorghiu et al., arXiv2605.12615v2](https://arxiv.org/html/2605.12615v2)
defines a circuit-input orbit decision problem. Section4.3 lifts it to a
generalized-dihedral StateHSP; section4.4 gives the efficient pure Pauli case.
Lemma4.3 uses conjugate circuits. These statements/proofs and relevant input
definitions were inspected; the entire paper and all hardness proofs were not.
The local checks below must not be advertised as new theorems from that paper.

## Native Packet: Gap Is Not The Missing Algorithm

For IID native DCP labels K=(k_1,...,k_r), let reference psi_0=|+>^r and
psi_s=R_K(s)psi_0, with public rotation action
`R_K(g)=tensor_i diag(1,exp(2*pi*i*k_i*g/N))`.
The supplied phase packet is psi_s, not a classical description of its
preparation circuit. The reference and controlled group action are known.

The exact magnitude of an orbit overlap is

`|<psi_0|R_K(delta)|psi_0>|=product_i |cos(pi*k_i*delta/N)|`.

For every nonzero delta modN, IID uniform labels give expected SQUARED overlap
2^-r: each cos squared has mean1/2 by character orthogonality. Markov and a
union bound therefore give

`Pr_K[max_(delta!=0) overlap>alpha] <= (N-1)*2^-r/alpha^2`.

For alpha=1/2 and failure budget1/1024, r=log2(N)+12 suffices. This separates
all orbit points with high source probability, but supplies no receiver or
inverse preparation. Public labels remain part of the instance; the bound is
neither a computational hardness theorem nor an efficient recovery algorithm.
No exponential list of all candidates is presented as polynomial processing.

Let d=gcd(N,k_1,...,k_r). The rotation stabilizer is multiples of N/d and the
action image has order N/d. The phase-invariant conjugate tensor lift has the
SAME image order: it includes eigenvalues exp(plus-or-minus2*pi*i*k_i/N),
so its kernel remains the same. Scalar cocycle cancellation does not turn
generic cyclic order N into order two.

For d=1, every secret is a YES instance of unrestricted orbit DECISION, but
there are N different witnesses. Thus the answer YES itself says nothing about
which hidden element generated the packet. A promised decision-to-search
reduction might be useful, but its restricted actions, gap and access costs
must be proved. We do not rule out such reductions.

The order-two counterfamily k_i in{0,N/2} retains at most parity of s. It does
not cover generic public labels or recover the remaining hidden-shift bits.
The all-zero packet has no outside stabilizer, so its off-stabilizer gap is
reported as null, not promoted as a favorable benchmark. Even-label packets
have an explicit alias subgroup. All eight unfiltered nondegenerate controls
are retained alongside these negative controls.

## What Copies Do Not Grant

Drawing a fresh ordered r-label packet that exactly repeats K has probability
N^-r under the native IID source. That is a cost of LITERAL rejection matching,
not an optimal lower bound: reordering, collisions, collective operations,
approximate or heralded transformations may use another interface. Nor does
it prove that duplicate conditional states are absolutely impossible.

Conjugating a native phase state is a particularly simple special case:
X|phi_(k,s)> equals |phi_(k,-s)> up to a global phase. It consumes an actual
additional register if both factors are needed. This does not provide the
unknown circuit, its inverse or the coherent relative phase needed to place
a known reference and unknown state in controlled alternative branches.
Circuit conjugation is also not the same operation as circuit inversion.

There is a sharp EXACT guard. Take native k=1 states at s=0 and s=1. Their
finite-t-copy program overlap is nonzero, with absolute value cos(pi/N)^t.
The corresponding reflection operators U_s=2|phi_s><phi_s|-I are distinct up
to global phase: the distance of U_0^dagger U_1 from its closest scalar matrix
is sqrt(2)*|sin(2*pi/N)|>0 for N>=8.

An exact deterministic processor implementing a unitary on arbitrary target
data must leave a target-independent program output. Inner-product preservation
would require `<P_0|P_1>*I=<P'_0|P'_1>*U_0^dagger U_1`; the nonzero input
overlap makes that impossible for these nonscalar unitary products. This is
the scoped [Nielsen-Chuang no-programming result](https://arxiv.org/pdf/quant-ph/9703032)
applied to the stated finite-copy programs, not to all quantum algorithms.
An exact preparation unitary and inverse would supply those reflections, so
they cannot simply be declared free from finite nonorthogonal copies.

Approximate, probabilistic/heralded programs, classical circuit descriptions,
full function oracles and ordinary destructive measurements are NOT excluded.
This exact argument is not a quantitative approximate-programming bound and
not a sample/runtime lower bound for solving native DCP. A promise-specific
algorithm need not implement any unknown reflection at all.

## Full Function Oracle: Access Exists, Hard Group Remains

Use the existing injective hidden-shift source, not a new promise family.
Let pi be an arbitrary injective function and f_b(x)=pi(x+b*s). Prepare
`psi_b=N^-1/2 sum_x |x,f_b(x)>`. These are real graph states, and
`R(s)psi_1=psi_0` under the public cyclic translation of the x register.
Here s uses the state-isomorphism convention. In the project's standard
right-coset source f_b(x)=pi(x-b*t), t=-s modN. The report retains that known
invertible sign map; it does not change the source promise or discard bits.

The phase-invariant lift and coherent branch state are

`Xi=(|0>psi_0 tensor psi_0 + |1>psi_1 tensor psi_1)/sqrt(2)`.

For Gamma=Z_N semidirect Z_2, define

`R'(g,0)=|0><0| tensor R(g)tensorR(g)
        +|1><1| tensor R(-g)tensorR(-g)`,

`R'(0,1)=X tensor I`, and `R'(g,a)=R'(g,0)R'(0,a)`.

On basis coordinates (b,x,y,u,v), this swaps b when a=1, then translates x,u
by +g in branch0 and -g in branch1, without changing output labels y,v.
It obeys the genuine generalized-dihedral group law; the implementation is
checked against independent SymPy dihedral multiplication on every N4 basis
state, not merely overlap formulas on one source.

Injectivity of pi implies actual overlaps are exactly1 for (0,0) and (s,1),
and0 otherwise. Thus the lifted state's stabilizer retains the original full
hidden reflection, up to the known sign map, at gap1. The group is nonabelian for N>2 and its
reflection normal core is trivial. A solver returning only that core does
not recover s. This lift does not evade the group/target obstruction from
`STATE_HSP_DHSP_SCOPE.md`.

Preparing Xi uses two canonical selector-function XOR queries, one per graph
copy; its inverse uses two queries too, then reverses known uniform preparation.
All36 calibration controls execute label uncomputation and inverse transforms.
The source oracle can be run coherently; that is NOT the blocker in this lane.
Two separately supplied canonical XOR function oracles give a four-query
upper per preparation using controlled calls, with known workspace overhead.
This does not assume controlled access to an arbitrary unknown unitary:
canonical XOR oracles have known uniform-target fixed states, allowing such
control with public swaps and workspace.

The resource bound covers creation of the REDUCTION INSTANCE, not a runtime
for its StateHSP solution. Its controlled representation and graph access are
efficient, yet the generic growing dihedral hidden-reflection decoder remains
the same missing capability. The efficient exponent-two case is not applicable
to a faithful cyclic action of growing order. A new nonhomomorphic encoding
or structure-specific decoder could change this, but must be exhibited.

## Falsifiers And Revised Priority

- **A well-separated native orbit is enough:** show a uniform receiver under
  the supplied sample contract; the gap alone is information, not decoding.
- **Circuit access is impossible:** false for the full function-oracle lane;
  preparation/inverse are explicit and charged. Do not conflate the lanes.
- **Inverse equals conjugate access:** justify a known real or otherwise
  special source; it is false for arbitrary preparation circuits.
- **Conjugate lifting abelianizes cyclic hidden shift:** its image still has
  order N/d, and adjoining inversion is still dihedral when that order>2.
- **Decision is automatically hidden-element search:** give a promise- and
  gap-preserving search reduction; all native unrestricted orbit decisions
  are YES regardless of s.
- **Exact no-programming excludes approximate decoders:** false; its exact
  deterministic scope must not be expanded to the actual open problem.
- **The literature record correction refutes the paper:** false; it corrects
  OUR tag-based extractor. The original paper's scoped statements remain intact.

Deprioritize direct transfer of the pure Pauli solver to generic DCP. Next
high-upside work must add an actual group-specific decoder, source-legal
representation change that preserves the hidden element, or a natural
reduction exposing new structure. Blindly mining generic tags and relabeling
copies as circuit access cannot improve breakthrough probability.

## Artifacts

New module/tests `state_isomorphism_transfer`; live reduction report; independent
JS checker; matching hypothesis and source audit. `literature_pipeline.py` has
a primary override for the exact seed/paper URL, tested on versioned arXiv
URLs and against spoofed domains. The persisted literature record is corrected
without regenerating unrelated entries. Full production CLI and registry
integration remain Gemini's task.

Independent replay:36 graph controls,9,648 sparse support entries,740 exact
overlaps,352 native orbit overlaps,16 finite-program controls and5 exact gap
ledgers. Verification:18 new tests and101 related tests pass in2.86s;
Python/JS syntax,4 strict JSON artifacts and scoped whitespace checks pass.
Independent human theorem review is still pending.
