"""Literature-backed capability ledger for symmetric-group recoupling.

The ledger prevents three invalid transfers:

* an efficient S_n QFT is not an internal Kronecker transform;
* a projector or #BQP characterization of a multiplicity is not a coherent
  multiplicity-basis transform;
* a restricted multiplicity estimator is not a hidden-involution decoder, and
  many proposed restricted speedups now have polynomial classical algorithms.

Finite exact Kronecker growth data is included only as a stress test.  Large
dimensions or multiplicities are not themselves circuit lower bounds because
they can be stored in logarithmically many qubits; the missing proof is a
uniform gate construction and an end-to-end decoder.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_schur_branch_merger_polar_equivalence import (
    run_schur_branch_merger_polar_equivalence,
)
from self_dual_wreath_schur_companion_transform_scope_boundary import (
    run_schur_companion_transform_scope_boundary,
)
from self_dual_wreath_addressed_cross_map_pair_polar_gram_boundary import (
    run_addressed_cross_map_pair_polar_gram_boundary,
)
from self_dual_wreath_addressed_cross_map_linear_assembly_normalization_boundary import (
    run_linear_assembly_normalization_boundary,
)
from self_dual_wreath_natural_q_scale_spectral_window_no_go import (
    run_natural_q_scale_spectral_window_no_go,
)
from self_dual_wreath_final_root_addressed_weyl_assembly_boundary import (
    run_final_root_addressed_weyl_assembly_boundary,
)
from self_dual_wreath_recursive_polar_normalization_conservation_boundary import (
    run_recursive_polar_normalization_conservation_boundary,
)
from self_dual_wreath_affine_gpe_nodelocal_naimark_access_boundary import (
    run_affine_gpe_nodelocal_naimark_access_boundary,
)
from self_dual_wreath_positive_naimark_access_equivalence_boundary import (
    run_positive_naimark_access_equivalence_boundary,
)
from symmetric_character import kronecker_coefficient


COSET_RECOUPLING_CAPABILITY_PATH = Path(
    "research/representation/coset_recoupling_capability_ledger.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-RECOUPLING-CAPABILITY-LEDGER"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
COSET_TYPICAL_COMMUTANT_MOMENT_PATH = Path(
    "research/representation/coset_typical_commutant_moment_audit.json"
)
COSET_TYPICAL_CLASS_CONTRACTION_PATH = Path(
    "research/representation/coset_typical_class_contraction_scaling.json"
)
COSET_TYPICAL_PORTFOLIO_COLLISION_PATH = Path(
    "research/representation/coset_typical_portfolio_collision_certificate.json"
)
COSET_TYPICAL_INDEPENDENT_THIRD_GENERATOR_PATH = Path(
    "research/representation/"
    "coset_typical_independent_third_generator_certificate.json"
)
COSET_TYPICAL_HIGH_MULTIPLICITY_TRANSFER_PATH = Path(
    "research/representation/coset_typical_high_multiplicity_transfer.json"
)
COSET_TYPICAL_FIXED_SEPARATOR_GAP_PATH = Path(
    "research/representation/coset_typical_fixed_separator_gap_scaling.json"
)
COSET_TYPICAL_N9_FULL_TRANSFER_PATH = Path(
    "research/representation/coset_typical_n9_full_transfer.json"
)


@dataclass(frozen=True)
class RepresentationCapability:
    id: str
    literature_ids: list[str]
    primitive: str
    proved_scope: str
    availability: str
    uniform_polynomial_gate_complexity_proved: bool
    resolves_internal_sn_kronecker_basis: bool
    handles_overlapping_k_copy_associators: bool
    supplies_hidden_involution_decoder: bool
    classical_comparison: str
    scope_limit: str


@dataclass(frozen=True)
class KroneckerGrowthRecord:
    n: int
    partition_count: int
    partition_triple_count: int
    nonzero_kronecker_sector_count: int
    maximum_irrep_dimension: int
    log2_maximum_irrep_dimension: float
    maximum_kronecker_multiplicity: int
    maximum_multiplicity_triple: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]
    multiplicity_register_bits: int
    finite_exact_table_only: bool
    dimension_or_multiplicity_is_lower_bound: bool


@dataclass(frozen=True)
class RecouplingCapabilityReport:
    created_at: str
    literature_scope: list[dict[str, str]]
    capabilities: list[RepresentationCapability]
    growth_records: list[KroneckerGrowthRecord]
    headline_metrics: dict[str, int | float]
    false_transfer_rules: list[dict[str, str]]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


CAPABILITIES = (
    RepresentationCapability(
        id="CAP-EXACT-HOLEVO-COPY-BOUND",
        literature_ids=["project-coset-holevo-character-formula"],
        primitive="Exact character-theoretic Holevo/Fano copy-budget certificate",
        proved_scope=(
            "For uniform involution conjugacy classes, computes exact one-copy Holevo information and certifies "
            "same-hidden k-copy lower bounds by entropy subadditivity and Fano's inequality."
        ),
        availability="proved-information-bound-not-measurement",
        uniform_polynomial_gate_complexity_proved=False,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison="This is a resource lower bound, not a quantum/classical separation.",
        scope_limit=(
            "Prices copies but constructs no measurement, recoupling transform, transition filter, or decoder; "
            "the resulting hard-family bound remains polynomial."
        ),
    ),
    RepresentationCapability(
        id="CAP-SN-QFT",
        literature_ids=["beals-symmetric-qft-1997"],
        primitive="Quantum Fourier transform over the S_n regular representation",
        proved_scope="Uniform polynomial-time transform from permutation basis to Young/Fourier labels and matrix indices.",
        availability="proved-polynomial",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison="No classical analogue is required for this basis-change capability claim.",
        scope_limit="Acts on one group-algebra register; does not decompose Specht(lambda) tensor Specht(mu).",
    ),
    RepresentationCapability(
        id="CAP-SCHUR-WEYL-CG",
        literature_ids=["bacon-chuang-harrow-schur-2004", "burchardt-high-dimensional-schur-2025"],
        primitive="Schur-Weyl transform and U(d) Clebsch-Gordan recursion",
        proved_scope="Efficient Schur transforms on qudit tensor powers, with corrected multiplicity-space isometries.",
        availability="proved-polynomial-scope-mismatch",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison="Not a speedup claim; it is a known circuit primitive in a different tensor decomposition.",
        scope_limit="Schur-Weyl/U(d) coupling is not the internal Kronecker product of two S_n irreps.",
    ),
    RepresentationCapability(
        id="CAP-SCHUR-DILATED-KRONECKER-CARRIER",
        literature_ids=[
            "bacon-chuang-harrow-schur-2004",
            "burchardt-high-dimensional-schur-2025",
            "christandl-et-al-plethysm-sharp-bqp-2026",
        ],
        primitive="Separate-to-joint Schur dilation of diagonal S_n tensor products",
        proved_scope=(
            "After adjoining fixed Schur--Weyl companion states, separate inverse Schur transforms, sitewise "
            "regrouping, and one high-dimensional joint Schur transform route polynomially many Specht factors "
            "into the diagonal irrep label and an opaque companion subspace carrying the full Kronecker multiplicity."
        ),
        availability="proved-polynomial-encoded-carrier-only",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "This is a coherent access primitive, not a task separation; the companion encoding can also retain "
            "exponentially difficult state-dependent contraction data."
        ),
        scope_limit=(
            "The circuit does not factor the companion into fixed source companions and standard multiplicity "
            "coordinates. Distinct source-label tuples land in orthogonal subgroup-branch sectors, so the "
            "controlled router does not realize the physical cross-orientation Gram H_nu. A common output-coordinate "
            "isometry would preserve H_nu rather than whiten it. The branch intertwiner, orientation polar, Racah "
            "associator, and decoder remain uncompiled."
        ),
    ),
    RepresentationCapability(
        id="CAP-SCHUR-COMPANION-KNOWN-TRANSFORM-STACK",
        literature_ids=[
            "beals-symmetric-qft-1997",
            "bacon-chuang-harrow-schur-2004",
            "ikenmeyer-subramanian-kronecker-2023",
            "burchardt-high-dimensional-schur-2025",
            "christandl-et-al-plethysm-sharp-bqp-2026",
        ],
        primitive=(
            "Published Schur/QFT/CG plus invariant-projector stack on the joint "
            "companion"
        ),
        proved_scope=(
            "The cited primitives supply polynomial Schur coordinate changes, irrep/source labels, and "
            "supplied-label invariant membership reflections. Their proved typed interface is branch preserving; "
            "products, adjoints, coherent label controls, workspace extensions, and selected top blocks remain in "
            "the direct-sum source-branch algebra when the computation stays inside the companion."
        ),
        availability="proved-companion-only-stack-insufficient-global-whitening-open",
        uniform_polynomial_gate_complexity_proved=False,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "This is a quantum access-model boundary, not a quantum/classical separation or an arbitrary-circuit "
            "lower bound."
        ),
        scope_limit=(
            "Actual finite H_nu and H_nu^(+/2) controls have nonzero cross-source-branch blocks, and natural "
            "Plancherel covering makes cross overlaps density one on balanced pairs. The companion-only stack "
            "therefore does not supply the orientation whitening multiplier. A physical-interface detour does "
            "supply addressed raw cross maps, but tightly normalized metric whitening, noncommuting Racah networks, "
            "multi-round transforms, and character-retaining decoders remain open."
        ),
    ),
    RepresentationCapability(
        id="CAP-ADDRESSED-CROSS-MAP-AND-DIRECT-PAIR-POLAR",
        literature_ids=[
            "beals-symmetric-qft-1997",
            "bacon-chuang-harrow-schur-2004",
            "bravyi-et-al-kronecker-2023",
        ],
        primitive=(
            "Uniform addressed J_f^*J_e block encoding and coherent-GPE pair polar"
        ),
        proved_scope=(
            "Decode branch e through the physical Schur/Bell interface, block-encode E_f=(I+R_f)/2 with one "
            "supplied-label reflection, and encode branch f. This gives an alpha-one signal block J_f^*J_e for "
            "coherent mask queries. Coherent GPE row reassociation directly compiles polar(J_f^*J_e) on its support."
        ),
        availability="proved-polynomial-addressed-query-and-pair-polar-only",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "Finite queried cross maps are classically contractible; no polynomial all-n global kernel assembly or "
            "quantum/classical separation is proved."
        ),
        scope_limit=(
            "An alpha-one entry query is not a normalization-one dense address-transition block encoding. Replacing "
            "all positive cross metrics by pair polars makes the block kernel indefinite on nonflat holonomy cycles. "
            "Uniform linear assembly gives G/q, but the natural q-scale retained window is now falsified; "
            "hierarchical/direct whitening and decoding remain open."
        ),
    ),
    RepresentationCapability(
        id="CAP-LINEAR-DENSE-METRIC-ASSEMBLY-ALPHA-Q",
        literature_ids=[
            "bacon-chuang-harrow-schur-2004",
            "gilyen-su-low-wiebe-qsvt-2018",
        ],
        primitive=(
            "Table-free uniform linear assembly of the addressed cross-map Gram"
        ),
        proved_scope=(
            "Uniform output-address preparation, one alpha-one addressed cross-map query, and uniform input-address "
            "erasure give the exact positive dense signal G/q using O(log q) address gates. Equal-coefficient linear "
            "mixing has coefficient matrix 11^*/alpha, so contraction on identical entries proves the sharp lower "
            "bound alpha>=q."
        ),
        availability="proved-polynomial-gates-alpha-q-normalization-only",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "Finite G/q matrices are classically formable and diagonalizable with exponential address width. No "
            "all-n quantum/classical separation follows from table-free oracle access."
        ),
        scope_limit=(
            "The compiler has alpha=q=2^Theta(n log n), and the natural Omega(q/poly(n)) retained trace-mass "
            "window is now falsified by the exact sibling second moment. The lower bound and mass no-go apply only "
            "to canonical equal-coefficient linear assembly; hierarchical shorted metrics, nonlinear multi-query "
            "routing, direct global polars, the physical PGM, and decoding remain open."
        ),
    ),
    RepresentationCapability(
        id="CAP-NATURAL-Q-SCALE-SPECTRAL-WINDOW-NO-GO",
        literature_ids=["aggarwal-elboim-maximal-dimension-2026"],
        primitive=(
            "Uniform natural trace-mass no-go for inverse-polynomial functional calculus on G/q"
        ),
        proved_scope=(
            "For K=ceil(c log2(n!))+2 with fixed c>=1, the exact sibling second moment, positivity under "
            "global-distinct conditioning, a union bound over both siblings and all targets, and uniform "
            "orientation-rank concentration give native mass above q/P at most "
            "2P p(n)[(1-1/g)/q+1/g]/[delta p_cf(1-epsilon)]. For polynomial P and delta^-1 this is o(1)."
        ),
        availability="proved-natural-mass-no-go-canonical-g-over-q-only",
        uniform_polynomial_gate_complexity_proved=False,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "The second-moment and partition-count certificate is classically evaluable. It is a scoped quantum-access "
            "obstruction, not a quantum/classical separation."
        ),
        scope_limit=(
            "This falsifies only a natural Omega(q/poly(n)) retained window for the canonical one-shot G/q "
            "assembly. An absolute inverse-polynomial cutoff on S appears at inverse-factorial scale in G/q. "
            "Hierarchical recursive shorted metrics, nonlinear multi-query transforms, direct representation-specific global "
            "polars, pair-GPE transport, physical PGM implementation, and decoding remain open."
        ),
    ),
    RepresentationCapability(
        id="CAP-FINAL-ROOT-ADDRESSED-WEYL-ASSEMBLY-BOUNDARY",
        literature_ids=[
            "gilyen-su-low-wiebe-qsvt-2018",
            "bacon-chuang-harrow-schur-2004",
        ],
        primitive=(
            "Positive-child and addressed-leaf factorization of the final endpoint Weyl pair"
        ),
        proved_scope=(
            "For child metrics A_s and S=A_0+A_1, every positive-coordinate Weyl block is "
            "sqrt(A_s)S^(-1/2)US^(-1/2)sqrt(A_t), and every leaf block is "
            "J_f^*S^(-1/2)US^(-1/2)J_e. Uniform coherent leaf assembly exposes R/sqrt(w) or G/w, "
            "so bounded QSVT inherits an Omega(sqrt(w)) polar degree. Given constant-normalization "
            "aggregate sqrt(A_s) maps, the binary top merge is width independent."
        ),
        availability="proved-global-whitening-boundary-aggregate-child-access-open",
        uniform_polynomial_gate_complexity_proved=False,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "The factorization and finite controls are classically checkable. The QSVT statement is a scoped "
            "quantum-access obstruction, not a quantum/classical separation."
        ),
        scope_limit=(
            "Pair-local functional calculus and canonical uniform linear assembly do not compile the shared parent "
            "whitening. Hierarchical normalization cancellation, constant-normalization aggregate child access, "
            "direct representation-specific global polars, the physical PGM, and decoding remain open."
        ),
    ),
    RepresentationCapability(
        id="CAP-RECURSIVE-POLAR-NORMALIZATION-CONSERVATION-BOUNDARY",
        literature_ids=[
            "gilyen-su-low-wiebe-qsvt-2018",
            "bacon-chuang-harrow-schur-2004",
        ],
        primitive=(
            "Support-aware recursive polar factorization with explicit block-encoding normalization recurrence"
        ),
        proved_scope=(
            "The relative polar factors W_v=[sqrt(S_c)]_c S_v^(-1/2) telescope exactly on Moore--Penrose "
            "supports. Coefficient-only controlled stacking separately obeys the sharp law "
            "alpha_v^2=sum_c alpha_c^2, so regrouping unit leaves retains alpha_root=sqrt(w). Child polars "
            "inherit rather than erase that scale; compressed inverse shorted metrics gain alpha_c^2 while direct "
            "shorted operators lose alpha_c^2. Independently trimmed children require the exact common-parent "
            "compatibility condition direct_sum_c R_c(Pi_c-Pi_v)=0."
        ),
        availability="proved-normalization-conservation-local-relative-isometry-access-open",
        uniform_polynomial_gate_complexity_proved=False,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "The identities and finite controls are classically checkable. They separate algebraic factorization from "
            "quantum access normalization and establish no quantum/classical separation."
        ),
        scope_limit=(
            "The no-cancellation result applies to coefficient-only recursive assembly and literal nested local QSVT. "
            "Normalization-one compatible W_v oracles would compile in tree depth; structured affine GPE/Schur routers, "
            "the physical PGM, and decoding remain open."
        ),
    ),
    RepresentationCapability(
        id="CAP-AFFINE-GPE-NODELOCAL-NAIMARK-ACCESS-BOUNDARY",
        literature_ids=[
            "bacon-chuang-harrow-schur-2004",
            "gilyen-su-low-wiebe-qsvt-2018",
        ],
        primitive=(
            "Exact nested endpoint/component Naimark contract for one recursive affine/GPE local router"
        ),
        proved_scope=(
            "A scalar address PREPARE with probability p_e followed by GPE support-partial-isometry SELECT V_e "
            "has component effect p_e V_e^*V_e, so it realizes the target child component iff "
            "H_e=p_e V_e^*V_e. Flat affine fibers compile at normalization one, but matrix component effects and "
            "nonproportional endpoint short metrics require input-dependent positive Naimark dilations. Supplied endpoint "
            "and component dilations compose with GPE SELECT at normalization one and additive error."
        ),
        availability="proved-scalar-gpe-select-boundary-matrix-naimark-dilations-open",
        uniform_polynomial_gate_complexity_proved=False,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "The effect criterion and finite matrix controls are classically checkable. They specify a quantum access "
            "interface but prove no quantum/classical separation."
        ),
        scope_limit=(
            "The negative result covers scalar affine PREPARE plus support/polar/GPE transport SELECT. It does not rule "
            "out compact representation-specific matrix-POVM dilations, direct Schur/Racah routers, or a typical-node "
            "approximation after a proved negligible trim."
        ),
    ),
    RepresentationCapability(
        id="CAP-WEAK-IRREP-PROJECTION",
        literature_ids=["bacon-chuang-harrow-schur-2004", "ikenmeyer-subramanian-kronecker-2023"],
        primitive="Generalized phase estimation and invariant-space projection",
        proved_scope="Project onto irrep labels or invariant subspaces when the required group action and QFT are efficient.",
        availability="proved-label-or-projector-only",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison="Projection can estimate representation statistics but does not establish a natural-problem separation.",
        scope_limit="Does not produce a coherent orthonormal basis inside Kronecker multiplicity spaces.",
    ),
    RepresentationCapability(
        id="CAP-DIAGONAL-JM-LABEL-TRANSFORM",
        literature_ids=[
            "okounkov-vershik-yjm-2005",
            "beals-symmetric-qft-1997",
            "bravyi-et-al-kronecker-2023",
        ],
        primitive="Simultaneous diagonal Young--Jucys--Murphy target-tableau label measurement",
        proved_scope=(
            "Measure the target Gelfand--Tsetlin path in V_lambda tensor V_mu using commuting diagonal "
            "Jucys--Murphy sums, controlled diagonal S_n actions, and polynomial block encoding at integer spectral gap."
        ),
        availability="proved-polynomial-label-only",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "This is a quantum basis-label primitive, not a separation; finite spectra can be reproduced classically "
            "and the hard multiplicity-space state dependence remains untouched."
        ),
        scope_limit=(
            "The YJM algebra is identity on each g(lambda,mu,nu)-dimensional multiplicity register; it supplies no "
            "multiplicity basis, Racah associator, transition filter, or hidden-involution decoder."
        ),
    ),
    RepresentationCapability(
        id="CAP-BOUNDED-SUPPORT-COMMUTANT-BLOCK-ENCODING",
        literature_ids=["project-coset-multiplicity-commutant-search", "beals-symmetric-qft-1997"],
        primitive="LCU block encoding of bounded-support simultaneous-conjugacy orbit sums",
        proved_scope=(
            "Enumerate O(n^5) transposition/transposition and transposition/3-cycle orbit terms and implement each "
            "Young-basis factor through the solved S_n QFT and reversible multiplication."
        ),
        availability="proved-polynomial-block-encoding-only",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "Finite multiplicity spectra are classically diagonalized only as verification; no quantum advantage is "
            "claimed without an asymptotic gap and natural-problem decoder."
        ),
        scope_limit=(
            "Block encoding alone does not imply efficient eigenbasis resolution. The project now proves the needed "
            "normalized gap only for xi_n=(n-3,2,1) inside xi_n tensor (n-2,2); other sectors remain unaudited."
        ),
    ),
    RepresentationCapability(
        id="CAP-GAPPED-KRONECKER-MULTIPLICITY-TRANSFORM",
        literature_ids=["project-coset-multiplicity-commutant-search"],
        primitive="Coherent multiplicity basis from a uniformly gapped commutant Hamiltonian",
        proved_scope=(
            "For W_n=(n-2,2), final xi_n=(n-3,2,1), and every n>=8, all seven nontrivial padded stable "
            "intermediate shapes have exact characteristic polynomials, inverse-polynomial normalized spectral gaps, "
            "and shape-controlled coherent eigenlabel append procedures from a common bounded-support block encoding."
        ),
        availability="proved-bounded-stable-family-shape-local-only",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=True,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "A finite simple spectrum is not a separation; classical representation algorithms and normalized-gap "
            "scaling must be compared on every source family."
        ),
        scope_limit=(
            "Each procedure assumes the state is already coherently routed into its declared eta tensor W to xi "
            "multiplicity block. No channel-routing isometry, coupling-tree transition, Racah associator, or "
            "hidden-involution decoder has been synthesized."
        ),
    ),
    RepresentationCapability(
        id="CAP-STABLE-NINE-SHAPE-SECTOR-CLASSIFICATION",
        literature_ids=[
            "church-ellenberg-farb-fi-modules-2015",
            "project-coset-stable-shape-family-certificate",
        ],
        primitive="Exact bounded intermediate-sector family for one stable three-copy final irrep",
        proved_scope=(
            "For W_n=(n-2,2) and final xi_n=(n-3,2,1), exactly nine padded intermediate shapes with fixed "
            "multiplicity pairs exhaust the final component for every n>=9, with n=8 closed exactly."
        ),
        availability="proved-exact-structural-not-circuit",
        uniform_polynomial_gate_complexity_proved=False,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "The certificate is an exact classical character-polynomial calculation and makes no separation claim."
        ),
        scope_limit=(
            "All seven nontrivial second-stage shapes now have local coherent normalized-gap labels, but exact support "
            "and local labels do not route amplitudes into those blocks, synthesize transitions, or decode the hidden "
            "involution."
        ),
    ),
    RepresentationCapability(
        id="CAP-STABLE-ENCODED-SHAPE-ROUTER",
        literature_ids=[
            "okounkov-vershik-yjm-2005",
            "project-coset-stable-shape-family-certificate",
        ],
        primitive="Coherent central-signature routing of the stable intermediate shape",
        proved_scope=(
            "On the final xi_n branch of W_n^tensor3, transposition and 3-cycle pair class sums have a jointly "
            "collision-free integer signature on all nine allowed intermediate shapes for every n>=8."
        ),
        availability="proved-bounded-stable-family-encoded-only",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "The signatures are exact classical content invariants; the quantum capability is nondestructive coherent "
            "routing, not a separation claim."
        ),
        scope_limit=(
            "The eta carrier remains encoded in the original W_n tensor W_n registers. No compressed Clebsch "
            "isometry, left/right transition, or decoder follows from the shape label."
        ),
    ),
    RepresentationCapability(
        id="CAP-STABLE-ENCODED-TREE-TRANSITION",
        literature_ids=[
            "project-coset-multiplicity-commutant-search",
            "project-coset-stable-shape-family-certificate",
        ],
        primitive="Complete encoded stable coupling-tree labels and left/right relabelling isometry",
        proved_scope=(
            "On the final xi_n branch of W_n^tensor3, commuting shape, first-stage, and second-stage observables "
            "provide all 25 multiplicity labels on either binary tree; U_R U_L^dagger changes the encoded label interface."
        ),
        availability="proved-one-stable-final-branch-encoded-only",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=True,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "The label count and commutators are classically certifiable; no advantage exists until a state-dependent "
            "filter and decoder beat legal classical contractions."
        ),
        scope_limit=(
            "The physical state remains in W_n^tensor3, only one source/final stable branch is covered, and no "
            "compressed Racah matrix, transition filter, or hidden-involution decoder is supplied."
        ),
    ),
    RepresentationCapability(
        id="CAP-STABLE-THREE-COPY-FRAME-BLOCK-ENCODING",
        literature_ids=[
            "project-coset-covariant-frame",
            "project-coset-stable-shape-family-certificate",
        ],
        primitive="Direct LCU block encoding and conditioned inverse filter for the stable three-copy involution frame",
        proved_scope=(
            "Conditioned on W_n^tensor3 and final xi_n, the frame is identity plus three normalized overlapping pair "
            "class sums, each implemented by reversible involution-class preparation and controlled representation actions. "
            "Exact character-ratio coercivity gives an inverse-polynomial lower bound and QSVT inverse-square-root "
            "filter for t=floor(n/4) and t=floor(n/2), every n>=8."
        ),
        availability="proved-block-encoding-conditioning-and-inverse-filter",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "The same finite 25-dimensional frame spectra can be formed classically; advantage requires scalable "
            "inverse filtering and outcome decoding beyond classical contractions."
        ),
        scope_limit=(
            "No PGM outcome-information theorem, conditioned-branch probability lower bound, hidden-involution "
            "reconstruction rule, or classical separation has been proved. Moreover, the fixed W_n^tensor3/final-"
            "xi_n branch has exact natural probability at most (25/3)n^9/(n!)^3, so this primitive is currently a "
            "mechanism control rather than an end-to-end algorithmic route."
        ),
    ),
    RepresentationCapability(
        id="CAP-KRONECKER-SHARP-BQP",
        literature_ids=["ikenmeyer-subramanian-kronecker-2023"],
        primitive="#BQP characterization of exact Kronecker multiplicities",
        proved_scope="The multiplicity is the dimension of the image of a composition of implementable commuting projectors.",
        availability="counting-class-upper-bound-not-bqp-evaluation",
        uniform_polynomial_gate_complexity_proved=False,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison="#BQP membership is not an efficient exact scalar-evaluation or basis-construction algorithm.",
        scope_limit="Counts an invariant space; it does not expose its basis or state-dependent transition matrix elements.",
    ),
    RepresentationCapability(
        id="CAP-RESTRICTED-MULTIPLICITY-ESTIMATION",
        literature_ids=["larocca-havlicek-multiplicities-2024", "panova-classical-multiplicities-2025"],
        primitive="Multiplicity estimation under dimension-ratio promises",
        proved_scope="Quantum algorithms on restricted partition families with sample cost controlled by representation-dimension ratios.",
        availability="restricted-and-classically-matched-on-many-families",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison="Polynomial classical algorithms refute the proposed superpolynomial advantage on many studied families.",
        scope_limit="Outputs multiplicities under promises; it neither prepares a full Kronecker basis nor decodes a coset ensemble.",
    ),
    RepresentationCapability(
        id="CAP-INTERNAL-SN-KRONECKER-TRANSFORM",
        literature_ids=["yoshida-random-dilation-2025", "burchardt-high-dimensional-schur-2025"],
        primitive="Coherent internal S_n Kronecker transform with explicit multiplicity basis",
        proved_scope="Defined as a unitary basis change and used schematically in representation-theoretic circuit identities.",
        availability="defined-no-unrestricted-uniform-cost-proof-in-ledger",
        uniform_polynomial_gate_complexity_proved=False,
        resolves_internal_sn_kronecker_basis=True,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison="No classical comparison is meaningful until a uniform quantum implementation and task are specified.",
        scope_limit="A definition or circuit box is not a gate synthesis, precision analysis, or state-transition implementation.",
    ),
    RepresentationCapability(
        id="CAP-KCOPY-RACAH-ASSOCIATOR",
        literature_ids=["burchardt-high-dimensional-schur-2025"],
        primitive="Coherent Racah/F-move network for overlapping k-copy S_n subset class sums",
        proved_scope="No unrestricted implementation applicable to the audited hidden-involution frame is established in this ledger.",
        availability="open",
        uniform_polynomial_gate_complexity_proved=False,
        resolves_internal_sn_kronecker_basis=True,
        handles_overlapping_k_copy_associators=True,
        supplies_hidden_involution_decoder=False,
        classical_comparison="Must be compared with classical representation and invariant algorithms after a circuit exists.",
        scope_limit="The project proves that one pairwise basis is insufficient at k=3 but has no replacement circuit.",
    ),
    RepresentationCapability(
        id="CAP-HIDDEN-INVOLUTION-OUTCOME-DECODER",
        literature_ids=["symmetric-defies-fourier-2005", "hsp-survey-2010"],
        primitive="Compressed multi-register measurement outcome to hidden involution",
        proved_scope="No polynomial decoder is established for the symmetric-group involution ensembles under study.",
        availability="open",
        uniform_polynomial_gate_complexity_proved=False,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=True,
        classical_comparison="Must beat graph/code invariants and canonicalization on a natural reduction-backed family.",
        scope_limit="Information-theoretic distinguishability, QFT labels, or multiplicity estimates are not a decoder.",
    ),
)


def audit_kronecker_growth(n: int) -> KroneckerGrowthRecord:
    partitions = integer_partitions(n)
    dimensions = {partition: hook_length_dimension(partition) for partition in partitions}
    maximum = 0
    maximizing = (partitions[0], partitions[0], partitions[0])
    nonzero = 0
    for left in partitions:
        for right in partitions:
            for target in partitions:
                value = kronecker_coefficient(left, right, target)
                if value:
                    nonzero += 1
                if value > maximum:
                    maximum = value
                    maximizing = (left, right, target)
    return KroneckerGrowthRecord(
        n=n,
        partition_count=len(partitions),
        partition_triple_count=len(partitions) ** 3,
        nonzero_kronecker_sector_count=nonzero,
        maximum_irrep_dimension=max(dimensions.values()),
        log2_maximum_irrep_dimension=math.log2(max(dimensions.values())),
        maximum_kronecker_multiplicity=maximum,
        maximum_multiplicity_triple=maximizing,
        multiplicity_register_bits=max(0, math.ceil(math.log2(maximum))) if maximum else 0,
        finite_exact_table_only=True,
        dimension_or_multiplicity_is_lower_bound=False,
    )


def build_recoupling_capability_report(
    n_values: Sequence[int] = (4, 5, 6, 7, 8, 9, 10),
) -> RecouplingCapabilityReport:
    growth = [audit_kronecker_growth(n) for n in n_values]
    try:
        typical_moment_payload = (
            json.loads(COSET_TYPICAL_COMMUTANT_MOMENT_PATH.read_text())
            if COSET_TYPICAL_COMMUTANT_MOMENT_PATH.exists()
            else {}
        )
    except (json.JSONDecodeError, OSError):
        typical_moment_payload = {}
    typical_moment_metrics = typical_moment_payload.get("headline_metrics", {})
    try:
        typical_class_payload = (
            json.loads(COSET_TYPICAL_CLASS_CONTRACTION_PATH.read_text())
            if COSET_TYPICAL_CLASS_CONTRACTION_PATH.exists()
            else {}
        )
    except (json.JSONDecodeError, OSError):
        typical_class_payload = {}
    typical_class_metrics = typical_class_payload.get("headline_metrics", {})
    try:
        typical_collision_payload = (
            json.loads(COSET_TYPICAL_PORTFOLIO_COLLISION_PATH.read_text())
            if COSET_TYPICAL_PORTFOLIO_COLLISION_PATH.exists()
            else {}
        )
    except (json.JSONDecodeError, OSError):
        typical_collision_payload = {}
    typical_collision_metrics = typical_collision_payload.get(
        "headline_metrics", {}
    )
    try:
        typical_third_generator_payload = (
            json.loads(COSET_TYPICAL_INDEPENDENT_THIRD_GENERATOR_PATH.read_text())
            if COSET_TYPICAL_INDEPENDENT_THIRD_GENERATOR_PATH.exists()
            else {}
        )
    except (json.JSONDecodeError, OSError):
        typical_third_generator_payload = {}
    typical_third_generator_metrics = typical_third_generator_payload.get(
        "headline_metrics", {}
    )
    try:
        typical_high_multiplicity_payload = (
            json.loads(COSET_TYPICAL_HIGH_MULTIPLICITY_TRANSFER_PATH.read_text())
            if COSET_TYPICAL_HIGH_MULTIPLICITY_TRANSFER_PATH.exists()
            else {}
        )
    except (json.JSONDecodeError, OSError):
        typical_high_multiplicity_payload = {}
    typical_high_multiplicity_metrics = typical_high_multiplicity_payload.get(
        "headline_metrics", {}
    )
    try:
        typical_separator_gap_payload = (
            json.loads(COSET_TYPICAL_FIXED_SEPARATOR_GAP_PATH.read_text())
            if COSET_TYPICAL_FIXED_SEPARATOR_GAP_PATH.exists()
            else {}
        )
    except (json.JSONDecodeError, OSError):
        typical_separator_gap_payload = {}
    typical_separator_gap_metrics = typical_separator_gap_payload.get(
        "headline_metrics", {}
    )
    try:
        typical_n9_payload = (
            json.loads(COSET_TYPICAL_N9_FULL_TRANSFER_PATH.read_text())
            if COSET_TYPICAL_N9_FULL_TRANSFER_PATH.exists()
            else {}
        )
    except (json.JSONDecodeError, OSError):
        typical_n9_payload = {}
    typical_n9_metrics = typical_n9_payload.get("headline_metrics", {})
    schur_branch_merger_metrics = (
        run_schur_branch_merger_polar_equivalence().headline_metrics
    )
    schur_companion_scope_metrics = (
        run_schur_companion_transform_scope_boundary().headline_metrics
    )
    addressed_cross_map_metrics = (
        run_addressed_cross_map_pair_polar_gram_boundary().headline_metrics
    )
    linear_assembly_metrics = (
        run_linear_assembly_normalization_boundary().headline_metrics
    )
    q_scale_window_metrics = (
        run_natural_q_scale_spectral_window_no_go().headline_metrics
    )
    addressed_weyl_metrics = (
        run_final_root_addressed_weyl_assembly_boundary().headline_metrics
    )
    recursive_normalization_metrics = (
        run_recursive_polar_normalization_conservation_boundary().headline_metrics
    )
    nodelocal_naimark_metrics = (
        run_affine_gpe_nodelocal_naimark_access_boundary().headline_metrics
    )
    positive_naimark_access_metrics = (
        run_positive_naimark_access_equivalence_boundary().headline_metrics
    )
    unresolved = [
        capability
        for capability in CAPABILITIES
        if capability.availability == "open"
        or capability.id == "CAP-INTERNAL-SN-KRONECKER-TRANSFORM"
    ]
    metrics: dict[str, int | float] = {
        "capability_count": len(CAPABILITIES),
        "proved_polynomial_primitive_count": sum(
            capability.uniform_polynomial_gate_complexity_proved for capability in CAPABILITIES
        ),
        "internal_kronecker_transform_poly_proof_count": sum(
            capability.id == "CAP-INTERNAL-SN-KRONECKER-TRANSFORM"
            and capability.uniform_polynomial_gate_complexity_proved
            for capability in CAPABILITIES
        ),
        "diagonal_jm_label_transform_poly_proof_count": sum(
            capability.id == "CAP-DIAGONAL-JM-LABEL-TRANSFORM"
            and capability.uniform_polynomial_gate_complexity_proved
            for capability in CAPABILITIES
        ),
        "bounded_support_commutant_block_encoding_poly_proof_count": sum(
            capability.id == "CAP-BOUNDED-SUPPORT-COMMUTANT-BLOCK-ENCODING"
            and capability.uniform_polynomial_gate_complexity_proved
            for capability in CAPABILITIES
        ),
        "gapped_kronecker_multiplicity_transform_poly_proof_count": sum(
            capability.id == "CAP-GAPPED-KRONECKER-MULTIPLICITY-TRANSFORM"
            and capability.availability == "proved-unrestricted"
            and capability.uniform_polynomial_gate_complexity_proved
            for capability in CAPABILITIES
        ),
        "stable_channel_gapped_label_transform_poly_proof_count": sum(
            capability.id == "CAP-GAPPED-KRONECKER-MULTIPLICITY-TRANSFORM"
            and capability.availability == "proved-bounded-stable-family-shape-local-only"
            and capability.uniform_polynomial_gate_complexity_proved
            for capability in CAPABILITIES
        ),
        "stable_shape_local_gapped_label_transform_count": 7,
        "stable_shape_encoded_channel_router_count": 1,
        "stable_shape_compressed_channel_routing_isometry_count": 0,
        "stable_shape_encoded_coupling_tree_transition_isometry_count": 1,
        "stable_shape_compressed_racah_associator_count": 0,
        "stable_three_copy_frame_block_encoding_count": 1,
        "stable_three_copy_frame_all_n_conditioning_theorem_count": 2,
        "stable_three_copy_frame_inverse_square_root_filter_count": 2,
        "stable_branch_superpolynomial_rarity_theorem_count": 1,
        "stable_branch_natural_input_accessible_count": 0,
        "stable_branch_direct_conditioned_preparation_count": 0,
        "stable_branch_typical_irrep_transfer_count": 0,
        "bounded_tail_natural_access_no_go_theorem_count": 1,
        "typical_irrep_uniform_commutant_gap_theorem_count": 0,
        "typical_irrep_finite_non_scalar_block_count": int(
            typical_moment_metrics.get("finite_non_scalar_covered_count", 0) or 0
        ),
        "typical_irrep_primary_generator_scalar_block_count": int(
            typical_moment_metrics.get(
                "primary_generator_exact_scalar_block_count", 0
            )
            or 0
        ),
        "typical_irrep_finite_centered_covariance_rank_two_count": int(
            typical_moment_metrics.get(
                "finite_centered_covariance_rank_two_count", 0
            )
            or 0
        ),
        "typical_irrep_finite_multiplicity_two_simple_spectrum_count": int(
            typical_moment_metrics.get(
                "finite_multiplicity_two_simple_spectrum_count", 0
            )
            or 0
        ),
        "typical_irrep_uniform_commutant_non_scalar_theorem_count": int(
            typical_moment_metrics.get(
                "uniform_typical_commutant_non_scalar_theorem_count", 0
            )
            or 0
        ),
        "typical_irrep_uniform_commutant_simple_spectrum_theorem_count": int(
            typical_moment_metrics.get(
                "uniform_typical_commutant_simple_spectrum_theorem_count", 0
            )
            or 0
        ),
        "typical_irrep_class_compressed_maximum_n": int(
            typical_class_metrics.get("maximum_n", 0) or 0
        ),
        "typical_irrep_primary_generator_exact_scalar_block_count": int(
            typical_class_metrics.get("total_exact_scalar_block_count", 0) or 0
        ),
        "typical_irrep_single_generator_uniformity_falsification_count": int(
            typical_class_metrics.get(
                "single_primary_generator_uniformity_falsification_count", 0
            )
            or 0
        ),
        "typical_irrep_finite_low_support_portfolio_covered_count": int(
            typical_class_metrics.get(
                "finite_portfolio_non_scalar_covered_count", 0
            )
            or 0
        ),
        "typical_irrep_finite_low_support_portfolio_common_scalar_count": int(
            typical_class_metrics.get(
                "finite_portfolio_common_scalar_block_count", 0
            )
            or 0
        ),
        "typical_irrep_two_generator_repeated_root_target_count": int(
            typical_collision_metrics.get(
                "repeated_zero_eigenvalue_target_count", 0
            )
            or 0
        ),
        "typical_irrep_minimum_required_portfolio_generator_count": int(
            typical_collision_metrics.get(
                "minimum_required_portfolio_generator_count_on_certified_targets",
                0,
            )
            or 0
        ),
        "typical_irrep_disjoint_third_generator_repeated_root_target_count": int(
            typical_collision_metrics.get(
                "disjoint_third_generator_repeated_root_target_count", 0
            )
            or 0
        ),
        "typical_irrep_independent_third_generator_repaired_target_count": int(
            typical_third_generator_metrics.get(
                "certified_n8_collision_target_repair_count", 0
            )
            or 0
        ),
        "typical_irrep_independent_third_generator_low_multiplicity_target_count": int(
            typical_third_generator_metrics.get(
                "certified_n8_low_multiplicity_simple_spectrum_target_count", 0
            )
            or 0
        ),
        "typical_irrep_independent_third_generator_unaudited_n8_target_count": int(
            typical_third_generator_metrics.get(
                "n8_unaudited_higher_multiplicity_target_count", 0
            )
            or 0
        ),
        "typical_irrep_independent_third_generator_all_n_theorem_count": int(
            typical_third_generator_metrics.get(
                "all_n_simple_spectrum_theorem_count", 0
            )
            or 0
        ),
        "typical_irrep_independent_third_generator_gap_theorem_count": int(
            typical_third_generator_metrics.get(
                "inverse_polynomial_gap_theorem_count", 0
            )
            or 0
        ),
        "typical_irrep_fixed_c1_n8_certified_target_count": int(
            typical_high_multiplicity_metrics.get(
                "certified_n8_simple_spectrum_target_count", 0
            )
            or 0
        ),
        "typical_irrep_fixed_c1_n8_unaudited_target_count": int(
            typical_high_multiplicity_metrics.get(
                "n8_unaudited_target_count", 0
            )
            or 0
        ),
        "typical_irrep_maximum_exact_transfer_degree": int(
            typical_high_multiplicity_metrics.get(
                "maximum_exact_transfer_degree", 0
            )
            or 0
        ),
        "typical_irrep_fixed_separator_finite_split_size_count": int(
            typical_separator_gap_metrics.get(
                "finite_all_block_simple_spectrum_size_count", 0
            )
            or 0
        ),
        "typical_irrep_fixed_separator_n8_normalized_gap_lower_bound": float(
            typical_separator_gap_metrics.get(
                "n8_certified_minimum_lcu_normalized_gap_lower_bound", 0.0
            )
            or 0.0
        ),
        "typical_irrep_fixed_separator_inverse_polynomial_gap_theorem_count": int(
            typical_separator_gap_metrics.get(
                "inverse_polynomial_normalized_gap_theorem_count", 0
            )
            or 0
        ),
        "typical_irrep_n9_certified_target_count": int(
            typical_n9_metrics.get(
                "certified_n9_simple_spectrum_target_count", 0
            )
            or 0
        ),
        "typical_irrep_n9_unaudited_target_count": int(
            typical_n9_metrics.get(
                "n9_unaudited_target_count", 0
            )
            or 0
        ),
        "typical_irrep_n9_all_target_theorem_count": int(
            typical_n9_metrics.get(
                "all_n9_target_simple_spectrum_theorem_count", 0
            )
            or 0
        ),
        "typical_irrep_n9_normalized_gap_lower_bound": float(
            typical_n9_metrics.get(
                "certified_n9_minimum_lcu_normalized_gap_lower_bound", 0.0
            )
            or 0.0
        ),
        "typical_irrep_uniform_encoded_tree_transform_count": 0,
        "typical_irrep_frame_conditioning_theorem_count": 0,
        "stable_shape_transition_filter_count": 0,
        "exact_stable_nine_shape_sector_classification_count": sum(
            capability.id == "CAP-STABLE-NINE-SHAPE-SECTOR-CLASSIFICATION"
            for capability in CAPABILITIES
        ),
        "kcopy_associator_poly_proof_count": sum(
            capability.handles_overlapping_k_copy_associators
            and capability.uniform_polynomial_gate_complexity_proved
            for capability in CAPABILITIES
        ),
        "hidden_involution_decoder_count": sum(
            capability.supplies_hidden_involution_decoder
            and capability.uniform_polynomial_gate_complexity_proved
            for capability in CAPABILITIES
        ),
        "unresolved_required_capability_count": len(unresolved),
        "restricted_multiplicity_classical_match_count": 1,
        "exact_holevo_copy_budget_theorem_count": 1,
        "schur_dilated_kronecker_carrier_polynomial_count": sum(
            capability.id == "CAP-SCHUR-DILATED-KRONECKER-CARRIER"
            and capability.uniform_polynomial_gate_complexity_proved
            for capability in CAPABILITIES
        ),
        "schur_branch_merger_polar_equivalence_theorem_count": int(
            schur_branch_merger_metrics.get(
                "exact_schur_branch_polar_equivalence_theorem_count",
                0,
            )
            or 0
        ),
        "physical_invariant_schur_companion_interface_count": int(
            schur_branch_merger_metrics.get(
                "physical_invariant_schur_companion_interface_count",
                0,
            )
            or 0
        ),
        "known_schur_projector_stack_scope_boundary_theorem_count": int(
            schur_companion_scope_metrics.get(
                "known_transform_stack_scope_theorem_count",
                0,
            )
            or 0
        ),
        "known_schur_projector_stack_global_whitening_multiplier_count": int(
            schur_companion_scope_metrics.get(
                "polynomial_global_cross_branch_whitening_oracle_count",
                0,
            )
            or 0
        ),
        "addressed_raw_cross_map_block_encoding_count": int(
            addressed_cross_map_metrics.get(
                "addressed_raw_cross_map_block_encoding_theorem_count",
                0,
            )
            or 0
        ),
        "addressed_raw_cross_map_block_encoding_normalization": float(
            addressed_cross_map_metrics.get(
                "addressed_raw_cross_map_block_encoding_normalization",
                0.0,
            )
            or 0.0
        ),
        "direct_gpe_pair_polar_compiler_count": int(
            addressed_cross_map_metrics.get(
                "direct_gpe_pair_polar_compiler_count",
                0,
            )
            or 0
        ),
        "phase_only_global_pair_polar_gram_no_go_theorem_count": int(
            addressed_cross_map_metrics.get(
                "phase_only_global_pair_polar_gram_no_go_theorem_count",
                0,
            )
            or 0
        ),
        "global_operator_valued_metric_assembly_compiler_count": int(
            linear_assembly_metrics.get(
                "polynomial_normalized_global_metric_assembly_compiler_count",
                0,
            )
            or 0
        ),
        "canonical_linear_global_metric_assembly_compiler_count": int(
            linear_assembly_metrics.get(
                "canonical_linear_global_metric_assembly_compiler_count",
                0,
            )
            or 0
        ),
        "linear_dense_assembly_alpha_q_lower_bound_theorem_count": int(
            linear_assembly_metrics.get(
                "linear_dense_assembly_alpha_q_lower_bound_theorem_count",
                0,
            )
            or 0
        ),
        "natural_q_scale_spectral_window_no_go_theorem_count": int(
            q_scale_window_metrics.get(
                "natural_uniform_target_q_scale_no_go_theorem_count",
                0,
            )
            or 0
        ),
        "final_root_addressed_weyl_global_whitening_boundary_count": int(
            addressed_weyl_metrics.get(
                "exact_addressed_leaf_whitened_block_theorem_count",
                0,
            )
            or 0
        ),
        "final_root_constant_normalization_aggregate_child_compiler_count": int(
            addressed_weyl_metrics.get(
                "compiled_constant_normalization_aggregate_child_map_count",
                0,
            )
            or 0
        ),
        "recursive_polar_normalization_conservation_theorem_count": int(
            recursive_normalization_metrics.get(
                "sharp_l2_normalization_conservation_theorem_count",
                0,
            )
            or 0
        ),
        "recursive_polar_trim_compatibility_boundary_count": int(
            recursive_normalization_metrics.get(
                "independent_trim_noncomposability_theorem_count",
                0,
            )
            or 0
        ),
        "positive_component_effect_physical_formula_theorem_count": int(
            positive_naimark_access_metrics.get(
                "physical_component_effect_formula_theorem_count",
                0,
            )
            or 0
        ),
        "direct_component_naimark_restricted_polar_equivalence_count": int(
            positive_naimark_access_metrics.get(
                "direct_naimark_restricted_polar_equivalence_theorem_count",
                0,
            )
            or 0
        ),
        "positive_scalar_address_sqrt_width_boundary_count": int(
            positive_naimark_access_metrics.get(
                "scalar_address_sqrt_width_lower_bound_theorem_count",
                0,
            )
            or 0
        ),
        "compiled_positive_component_naimark_interface_count": int(
            positive_naimark_access_metrics.get(
                "compiled_positive_amplitude_interface_count",
                0,
            )
            or 0
        ),
        "recursive_shorted_metric_scale_inheritance_theorem_count": int(
            recursive_normalization_metrics.get(
                "shorted_metric_scale_inheritance_theorem_count",
                0,
            )
            or 0
        ),
        "normalization_one_local_relative_isometry_compiler_count": int(
            recursive_normalization_metrics.get(
                "compiled_normalization_one_local_relative_isometry_count",
                0,
            )
            or 0
        ),
        "scalar_gpe_prepare_select_effect_boundary_theorem_count": int(
            nodelocal_naimark_metrics.get(
                "scalar_prepare_select_effect_criterion_theorem_count",
                0,
            )
            or 0
        ),
        "normalization_one_nested_nodelocal_naimark_contract_count": int(
            nodelocal_naimark_metrics.get(
                "normalization_one_nested_naimark_contract_theorem_count",
                0,
            )
            or 0
        ),
        "uniform_nodelocal_matrix_naimark_dilation_compiler_count": int(
            nodelocal_naimark_metrics.get(
                "compiled_uniform_endpoint_metric_naimark_dilation_count",
                0,
            )
            + nodelocal_naimark_metrics.get(
                "compiled_uniform_component_effect_naimark_dilation_count",
                0,
            )
        ),
        "growth_record_count": len(growth),
        "maximum_n": max(n_values),
        "maximum_partition_count": max(record.partition_count for record in growth),
        "maximum_kronecker_multiplicity": max(
            record.maximum_kronecker_multiplicity for record in growth
        ),
        "maximum_multiplicity_register_bits": max(
            record.multiplicity_register_bits for record in growth
        ),
    }
    return RecouplingCapabilityReport(
        created_at=utc_now(),
        literature_scope=[
            {"id": literature_id, "url": url}
            for literature_id, url in (
                ("beals-symmetric-qft-1997", "https://doi.org/10.1145/258533.258548"),
                ("okounkov-vershik-yjm-2005", "https://arxiv.org/abs/math/0503040"),
                ("bravyi-et-al-kronecker-2023", "https://arxiv.org/abs/2302.11454"),
                ("bacon-chuang-harrow-schur-2004", "https://arxiv.org/abs/quant-ph/0407082"),
                ("ikenmeyer-subramanian-kronecker-2023", "https://arxiv.org/abs/2307.02389"),
                ("larocca-havlicek-multiplicities-2024", "https://arxiv.org/abs/2407.17649"),
                ("panova-classical-multiplicities-2025", "https://arxiv.org/abs/2502.20253"),
                ("burchardt-high-dimensional-schur-2025", "https://arxiv.org/abs/2509.22640"),
                ("yoshida-random-dilation-2025", "https://arxiv.org/abs/2512.21260"),
                ("christandl-et-al-plethysm-sharp-bqp-2026", "https://arxiv.org/abs/2602.08441"),
                ("aggarwal-elboim-maximal-dimension-2026", "https://arxiv.org/abs/2605.25995"),
            )
        ],
        capabilities=list(CAPABILITIES),
        growth_records=growth,
        headline_metrics=metrics,
        false_transfer_rules=[
            {
                "from": "exact Holevo/Fano copy lower bound",
                "invalid_to": "efficient collective measurement, decoder, or no-algorithm theorem",
                "reason": "The bound prices information but the certified hard-family copy count is polynomial.",
            },
            {
                "from": "efficient S_n QFT",
                "invalid_to": "efficient internal S_n Kronecker transform or hidden-involution decoder",
                "reason": "The transforms decompose different group actions and expose different multiplicity data.",
            },
            {
                "from": "all seven nontrivial stable shapes with polynomial local coherent eigenlabel transforms",
                "invalid_to": "unrestricted internal Kronecker transform, overlapping Racah associator, or decoder",
                "reason": (
                    "The shape-local procedures assume a routed input; they neither construct the routing isometry "
                    "nor transport multiplicity amplitudes between coupling trees."
                ),
            },
            {
                "from": "a coherent collision-free encoded intermediate-shape router",
                "invalid_to": "compressed Clebsch isometry, Racah associator, or decoder",
                "reason": (
                    "Central phase estimation appends eta while leaving its carrier in the original tensor encoding; "
                    "it does not transfer amplitudes to a standalone eta register or change coupling trees."
                ),
            },
            {
                "from": "complete encoded left/right stable-tree labels and U_R U_L^dagger",
                "invalid_to": "state-dependent transition filter, hidden-involution decoder, or full-sector associator",
                "reason": (
                    "The relabelling isometry preserves the physical tensor encoding and exposes no frame inverse, "
                    "outcome-information theorem, or sectors outside one stable final branch."
                ),
            },
            {
                "from": "a direct polynomial stable three-copy frame block encoding, all-n coercivity, and inverse filter",
                "invalid_to": "hidden-involution decoder or quantum speedup",
                "reason": (
                    "Measurement outcomes still need branch-probability, parameter-information, reconstruction, and "
                    "classical-separation theorems."
                ),
            },
            {
                "from": "polynomial recoupling and inverse filtering inside the fixed W_n^tensor3/final-xi_n branch",
                "invalid_to": "a polynomial algorithm from natural involution coset-state inputs",
                "reason": (
                    "The exact branch probability is at most (25/3)n^9/(n!)^3. Passive postselection and generic "
                    "amplitude amplification are superpolynomial without a new direct preparation or typical-irrep transfer."
                ),
            },
            {
                "from": "a polynomial circuit theorem on any predetermined fixed bounded-tail partition family",
                "invalid_to": "a natural-input symmetric-group Fourier algorithm",
                "reason": (
                    "For fixed tail budget K, the total weak-Fourier probability is at most "
                    "2*P_K*n^(2K)/n!. The algorithm must instead adapt uniformly to sampled typical labels."
                ),
            },
            {
                "from": "polynomial diagonal YJM target-tableau label measurement",
                "invalid_to": "coherent Kronecker multiplicity basis, Racah associator, or decoder",
                "reason": (
                    "The commuting YJM algebra is exactly degenerate on the multiplicity register and cannot choose "
                    "or manipulate a basis within it."
                ),
            },
            {
                "from": "#BQP multiplicity characterization or invariant projector",
                "invalid_to": "coherent basis of the invariant space and state-dependent transition amplitudes",
                "reason": "Subspace dimension and label projection do not construct a basis-change unitary.",
            },
            {
                "from": "efficient Schur-Weyl/U(d) Clebsch-Gordan transform",
                "invalid_to": "internal tensor product decomposition of arbitrary S_n Specht modules",
                "reason": "These are distinct representation-theoretic decompositions.",
            },
            {
                "from": "polynomial separate-to-joint Schur dilation",
                "invalid_to": "exposed Kronecker coordinates, improved orientation conditioning, or the physical PGM",
                "reason": (
                    "The multiplicity is carried by an opaque subspace of the joint companion register. Controlled "
                    "source tuples occupy orthogonal branch sectors and therefore do not realize the cross-orientation "
                    "Gram. The natural encoded merger polar is exactly the original physical orientation polar "
                    "conjugated by the branch encoder; an isometric flag embedding likewise preserves H_nu."
                ),
            },
            {
                "from": (
                    "the companion-only Schur/QFT/CG stack together with "
                    "within-branch invariant-space controls"
                ),
                "invalid_to": (
                    "the global cross-source-branch whitening multiplier or orientation polar"
                ),
                "reason": (
                    "The companion-only closure has zero Z_f O Z_e blocks for e!=f, whereas H_nu^(+/2) has "
                    "certified cross blocks. A physical-interface detour supplies raw addressed entries, but not "
                    "their global PSD metric assembly or whitening."
                ),
            },
            {
                "from": "alpha-one addressed raw cross maps and direct coherent-GPE pair polars",
                "invalid_to": "a normalization-one global orientation Gram or physical PGM polar",
                "reason": (
                    "Entry-query normalization does not normalize the dense address-transition operator. Pair "
                    "phases alone make an indefinite block kernel on nonflat holonomy cycles; the positive "
                    "operator-valued cross metrics must be retained and assembled coherently."
                ),
            },
            {
                "from": (
                    "vanishing natural trace mass at inverse-polynomial eigenvalues of the canonical G/q signal"
                ),
                "invalid_to": (
                    "an arbitrary-circuit, hierarchical-polar, direct-polar, or physical-PGM impossibility theorem"
                ),
                "reason": (
                    "The theorem charges one q-wide normalized analysis. An absolute inverse-polynomial cutoff on S "
                    "lies at scale 1/(q poly(n)) in G/q and can still be preserved by a tightly normalized "
                    "hierarchical or direct structured implementation."
                ),
            },
            {
                "from": "restricted quantum multiplicity estimator",
                "invalid_to": "superpolynomial advantage or Shor-level mechanism",
                "reason": "Many proposed restricted families now have polynomial classical algorithms.",
            },
            {
                "from": "large irrep dimension or Kronecker multiplicity",
                "invalid_to": "quantum circuit lower bound",
                "reason": "Logarithmic-size quantum registers can encode large spaces; gate lower bounds require proof.",
            },
        ],
        claim_gate={
            "sn_qft_is_open_bottleneck": False,
            "exact_holevo_copy_budget_proved": True,
            "holevo_copy_budget_constructs_measurement": False,
            "multiplicity_counting_implies_coherent_transform": False,
            "schur_transform_implies_internal_kronecker_transform": False,
            "schur_dilated_global_isotypic_router_polynomial_proved": True,
            "schur_dilated_encoded_multiplicity_carrier_proved": True,
            "schur_dilated_standard_multiplicity_coordinates_exposed": False,
            "schur_dilated_controlled_router_realizes_orientation_gram": False,
            "schur_dilated_cross_orientation_branch_intertwiner_compiled": False,
            "schur_dilation_improves_orientation_gram_conditioning": False,
            "schur_branch_merger_polar_equivalence_proved": bool(
                schur_branch_merger_metrics.get(
                    "exact_schur_branch_polar_equivalence_theorem_count",
                    0,
                )
            ),
            "physical_invariant_to_schur_companion_interface_compiled": bool(
                schur_branch_merger_metrics.get(
                    "physical_invariant_schur_companion_interface_count",
                    0,
                )
            ),
            "physical_encoded_orientation_polar_compilers_interreducible": bool(
                schur_branch_merger_metrics.get(
                    "physical_invariant_schur_companion_interface_count",
                    0,
                )
            ),
            "known_schur_projector_stack_interfaces_typed": bool(
                schur_companion_scope_metrics.get(
                    "known_transform_stack_scope_theorem_count",
                    0,
                )
            ),
            "companion_only_stack_supplies_global_cross_branch_whitening_multiplier": False,
            "known_schur_projector_stack_compiles_orientation_polar": False,
            "physical_interface_supplies_addressed_raw_cross_map_block_encoding": bool(
                addressed_cross_map_metrics.get(
                    "addressed_raw_cross_map_block_encoding_theorem_count",
                    0,
                )
            ),
            "addressed_raw_cross_map_block_encoding_normalization_one": bool(
                addressed_cross_map_metrics.get(
                    "addressed_raw_cross_map_block_encoding_normalization",
                    0.0,
                )
                == 1.0
            ),
            "direct_gpe_pair_polar_compiled": bool(
                addressed_cross_map_metrics.get(
                    "direct_gpe_pair_polar_compiler_count",
                    0,
                )
            ),
            "phase_only_pair_polar_global_gram_ansatz_refuted": bool(
                addressed_cross_map_metrics.get(
                    "phase_only_global_pair_polar_gram_no_go_theorem_count",
                    0,
                )
            ),
            "canonical_linear_global_psd_metric_assembly_compiled": bool(
                linear_assembly_metrics.get(
                    "canonical_linear_global_metric_assembly_compiler_count",
                    0,
                )
            ),
            "canonical_linear_global_metric_normalization_is_q": bool(
                linear_assembly_metrics.get(
                    "linear_dense_assembly_alpha_q_lower_bound_theorem_count",
                    0,
                )
            ),
            "linear_equal_coefficient_dense_assembly_alpha_lower_bound_q": bool(
                linear_assembly_metrics.get(
                    "linear_dense_assembly_alpha_q_lower_bound_theorem_count",
                    0,
                )
            ),
            "global_operator_valued_metric_assembly_compiled": False,
            "global_address_transition_kernel_polynomial_normalization_proved": False,
            "natural_retained_spectrum_at_q_over_polynomial_scale_proved": False,
            "natural_g_over_q_inverse_polynomial_window_positive_mass_falsified": bool(
                q_scale_window_metrics.get(
                    "natural_uniform_target_q_scale_no_go_theorem_count",
                    0,
                )
            ),
            "nonlinear_hierarchical_metric_assembly_ruled_out": False,
            "final_root_addressed_weyl_blocks_require_shared_parent_whitening": bool(
                addressed_weyl_metrics.get(
                    "exact_addressed_leaf_whitened_block_theorem_count",
                    0,
                )
            ),
            "final_root_pair_local_functional_calculus_suffices": False,
            "final_root_binary_merge_width_independent_given_aggregate_access": bool(
                addressed_weyl_metrics.get(
                    "conditional_constant_cost_binary_merge_theorem_count",
                    0,
                )
            ),
            "final_root_constant_normalization_aggregate_child_access_compiled": False,
            "recursive_polar_operator_factors_telescope_exactly": bool(
                recursive_normalization_metrics.get(
                    "exact_support_aware_recursive_polar_telescoping_theorem_count",
                    0,
                )
            ),
            "coefficient_only_recursive_normalization_cancels": False,
            "recursive_normalization_squared_sum_law_proved": bool(
                recursive_normalization_metrics.get(
                    "sharp_l2_normalization_conservation_theorem_count",
                    0,
                )
            ),
            "shorted_metrics_cancel_recursive_access_normalization": False,
            "shorted_metric_scale_inheritance_proved": bool(
                recursive_normalization_metrics.get(
                    "shorted_metric_scale_inheritance_theorem_count",
                    0,
                )
            ),
            "independent_retained_child_trims_automatically_compose": False,
            "normalization_one_local_relative_isometries_compiled": False,
            "scalar_gpe_prepare_select_effect_criterion_proved": bool(
                nodelocal_naimark_metrics.get(
                    "scalar_prepare_select_effect_criterion_theorem_count",
                    0,
                )
            ),
            "flat_affine_gpe_child_embedding_normalization_one_proved": bool(
                nodelocal_naimark_metrics.get(
                    "normalization_one_flat_affine_transport_compiler_theorem_count",
                    0,
                )
            ),
            "scalar_gpe_select_compiles_matrix_component_effects": False,
            "support_polar_gpe_transports_determine_endpoint_metric_mixer": False,
            "normalization_one_nested_nodelocal_naimark_contract_proved": bool(
                nodelocal_naimark_metrics.get(
                    "normalization_one_nested_naimark_contract_theorem_count",
                    0,
                )
            ),
            "uniform_endpoint_metric_naimark_dilation_compiled": False,
            "uniform_component_effect_naimark_dilation_compiled": False,
            "positive_component_effect_physical_formula_proved": bool(
                positive_naimark_access_metrics.get(
                    "physical_component_effect_formula_theorem_count",
                    0,
                )
            ),
            "direct_component_naimark_is_restricted_polar_equivalent": bool(
                positive_naimark_access_metrics.get(
                    "direct_naimark_restricted_polar_equivalence_theorem_count",
                    0,
                )
            ),
            "scalar_positive_address_extraction_alpha_sqrt_width_proved": bool(
                positive_naimark_access_metrics.get(
                    "scalar_address_sqrt_width_lower_bound_theorem_count",
                    0,
                )
            ),
            "pair_local_cross_data_determine_component_positive_effect": False,
            "natural_small_positive_component_effect_edge_proved": False,
            "direct_schur_racah_component_naimark_compiled": False,
            "natural_cross_orientation_overlap_density_one_proved": True,
            "schur_branch_encoding_removes_orientation_inverse_square_root": False,
            "schur_branch_structured_direct_polar_compiled": False,
            "diagonal_jm_label_transform_polynomial_proved": True,
            "diagonal_jm_labels_resolve_multiplicity_basis": False,
            "bounded_support_commutant_block_encoding_polynomial_proved": True,
            "stable_channel_gapped_multiplicity_label_polynomial_proved": True,
            "all_seven_stable_shape_local_labels_polynomial_proved": True,
            "stable_shape_encoded_channel_routing_polynomial_proved": True,
            "stable_shape_compressed_channel_routing_isometry_polynomial_proved": False,
            "stable_shape_complete_encoded_tree_labels_polynomial_proved": True,
            "stable_shape_encoded_coupling_tree_transition_polynomial_proved": True,
            "stable_shape_compressed_racah_associator_polynomial_proved": False,
            "stable_three_copy_frame_block_encoding_polynomial_proved": True,
            "stable_three_copy_frame_all_n_conditioning_proved": True,
            "stable_three_copy_frame_inverse_square_root_filter_polynomial_proved": True,
            "stable_branch_natural_input_access_polynomial_proved": False,
            "stable_branch_superpolynomial_postselection_obstruction_proved": True,
            "stable_branch_typical_irrep_transfer_proved": False,
            "bounded_tail_natural_access_no_go_proved": True,
            "typical_irrep_uniform_recoupling_transfer_proved": False,
            "typical_irrep_finite_bounded_support_non_scalarity_observed": bool(
                typical_moment_metrics.get("finite_non_scalar_covered_count", 0)
            ),
            "typical_irrep_uniform_joint_spectral_separation_proved": False,
            "stable_shape_transition_filter_polynomial_proved": False,
            "exact_bounded_stable_sector_family_proved": True,
            "gapped_kronecker_multiplicity_transform_polynomial_proved": False,
            "internal_sn_kronecker_transform_polynomial_proved": False,
            "kcopy_associator_polynomial_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_superpolynomial_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Coherent gapped eigenlabel transforms are proved for every nontrivial shape in one bounded stable "
                "family. Complete encoded labels and left/right relabelling are proved on one stable final branch, "
                "and its three-copy frame is directly block-encoded, all-n conditioned, and inverse-filterable, but "
                "the fixed branch is factorially rare under natural input. The known Schur/QFT/CG plus "
                "invariant-projector stack is now typed exactly. Its companion-only closure preserves source "
                "branches, but the physical-interface detour supplies alpha-one addressed raw cross maps and GPE "
                "supplies their pair polars. Phase-only global assembly is refuted by holonomy-induced "
                "indefiniteness. Uniform linear address mixing compiles the exact PSD Gram G/q at sharp alpha=q, "
                "but the exact natural sibling second moment now proves that every inverse-polynomial G/q spectral "
                "window retains only o(1) trace-weighted mass. The useful absolute S cutoff lies at "
                "inverse-factorial scale in G/q. A hierarchical or direct global polar, an outcome-information "
                "theorem, decoding, and separation remain open."
            ),
        },
        status="canonical-g-over-q-natural-window-falsified-hierarchical-global-polar-open",
        summary=(
            f"Classified {len(CAPABILITIES)} representation primitives and exact finite Kronecker growth through "
            f"n={max(n_values)}. Separate-to-joint Schur dilation now supplies an encoded multiplicity carrier, "
            "the physical interface supplies alpha-one addressed raw cross maps, and GPE supplies direct pair "
            "polars. Uniform linear assembly gives G/q at sharp alpha=q, but the exact natural sibling second "
            "moment now falsifies every inverse-polynomial retained G/q window. The remaining metric route is a "
            "genuinely hierarchical or direct representation-specific global polar."
        ),
        falsifiers_triggered=[
            "The S_n QFT is already polynomial and cannot be presented as the missing breakthrough.",
            "Exact Holevo/Fano accounting charges copies but does not construct a collective measurement or decoder.",
            "#BQP multiplicity counting does not construct a coherent Kronecker basis.",
            "Schur-Weyl Clebsch-Gordan circuits do not automatically solve internal Specht tensor products.",
            "Separate-to-joint Schur dilation carries fixed-source Kronecker multiplicity coherently, but its natural normalized branch merger is the original orientation polar in encoded coordinates.",
            "The companion-only Schur/QFT/CG plus projector stack is branch preserving, but a physical-interface detour does supply raw addressed cross-map entries.",
            "Normalization-one addressed pair polars cannot replace cross metrics globally: nonflat holonomy makes the phase-only block kernel indefinite.",
            "Dense natural support and exact low moments do not rescue the canonical G/q assembly: every inverse-polynomial normalized spectral window retains o(1) natural trace mass.",
            "Diagonal YJM tableau labels retain exact Kronecker multiplicity degeneracy.",
            "An encoded stable shape router does not construct a compressed Clebsch channel isometry.",
            "An encoded left/right relabelling isometry does not construct the state-dependent frame filter or decoder.",
            "An all-n conditioned and inverse-filterable stable frame still does not prove outcome decoding or separation.",
            "The solved stable W_n^tensor3 branch is factorially rare under natural coset-state preparation.",
            "Every predetermined fixed bounded-tail Fourier family has factorially small natural mass.",
            "Many restricted multiplicity speedup candidates have polynomial classical algorithms.",
            "Finite growth of dimensions or multiplicities is not a circuit lower bound.",
        ],
    )


def write_recoupling_capability_report(
    output_path: Path = COSET_RECOUPLING_CAPABILITY_PATH,
    n_values: Sequence[int] = (4, 5, 6, 7, 8, 9, 10),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_recoupling_capability_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"coset_recoupling_capability_ledger": str(output_path)},
            )
        )
        for negative in (
            NegativeResultRecord(
                id="NEG-COSET-SN-QFT-AS-MULTICOPY-DECODER",
                source=registry_experiment_id,
                claim="An efficient S_n QFT supplies the missing multiregister decoder.",
                reason_invalid=(
                    "The QFT resolves regular-representation labels and matrix indices but does not implement the "
                    "orientation polar, a multiplicity-space associator, or hidden-involution reconstruction."
                ),
                lesson="Treat the QFT as an available basis change and charge every subsequent collective operation.",
                applies_to=[registry_candidate_id, registry_experiment_id, "PO-MEASUREMENT"],
                evidence=payload["claim_gate"],
            ),
            NegativeResultRecord(
                id="NEG-COSET-KRONECKER-COUNT-AS-TRANSFORM",
                source=registry_experiment_id,
                claim="#BQP membership or a Kronecker projector supplies a coherent multiplicity transform.",
                reason_invalid=(
                    "Counting or projecting an invariant space does not expose its basis or state-dependent "
                    "transition amplitudes. Schur dilation adds fixed-source encoded carriers in orthogonal branch "
                    "sectors. A physical-interface detour supplies addressed raw cross maps, but multiplicity "
                    "counting still does not assemble their global positive metric or orientation polar."
                ),
                lesson=(
                    "Separate dimension, isotypic routing, addressed entry access, pair polars, global metric "
                    "assembly, and the physical polar."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id, "PO-MEASUREMENT"],
                evidence=payload["claim_gate"],
            ),
            NegativeResultRecord(
                id="NEG-COSET-RESTRICTED-MULTIPLICITY-AS-BREAKTHROUGH",
                source=registry_experiment_id,
                claim="Restricted multiplicity estimation alone is a Shor-level quantum advantage.",
                reason_invalid=(
                    "Known promises cover restricted dimension-ratio regimes, and polynomial classical algorithms "
                    "match many proposed families without producing a natural hidden-involution decoder."
                ),
                lesson="Require a natural input model, end-to-end decoder, and explicit classical separation.",
                applies_to=[registry_candidate_id, registry_experiment_id, "PO-CLASSICAL-BASELINE"],
                evidence=payload["claim_gate"],
            ),
            NegativeResultRecord(
                id="NEG-COSET-SCHUR-ENCODING-AS-FREE-BRANCH-POLAR",
                source=registry_experiment_id,
                claim="Polynomial Schur-dilated multiplicity access automatically compiles the cross-orientation branch merger.",
                reason_invalid=(
                    "A branchwise Schur isometry conjugates the raw merger Gram and preserves every nonzero singular "
                    "value. Its normalized merger is exactly the physical orientation polar in encoded coordinates; "
                    "the inverse-square-root operation is not removed."
                ),
                lesson=(
                    "Use Schur companion structure only if it yields a direct polar compiler or a decoder that "
                    "retains branch characters; isotypic routing alone is not the missing measurement."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id, "PO-MEASUREMENT"],
                evidence=payload["claim_gate"],
            ),
        ):
            upsert_negative_result(negative)
    return payload
