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
from symmetric_character import kronecker_coefficient


COSET_RECOUPLING_CAPABILITY_PATH = Path(
    "research/representation/coset_recoupling_capability_ledger.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-RECOUPLING-CAPABILITY-LEDGER"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


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
        primitive="Direct LCU block encoding of the stable three-copy involution frame",
        proved_scope=(
            "Conditioned on W_n^tensor3 and final xi_n, the frame is identity plus three normalized overlapping pair "
            "class sums, each implemented by reversible involution-class preparation and controlled representation actions."
        ),
        availability="proved-block-encoding-conditioning-open",
        uniform_polynomial_gate_complexity_proved=True,
        resolves_internal_sn_kronecker_basis=False,
        handles_overlapping_k_copy_associators=False,
        supplies_hidden_involution_decoder=False,
        classical_comparison=(
            "The same finite 25-dimensional frame spectra can be formed classically; advantage requires scalable "
            "inverse filtering and outcome decoding beyond classical contractions."
        ),
        scope_limit=(
            "No all-n positive-spectrum lower bound, inverse-square-root filter, PGM outcome-information theorem, or "
            "hidden-involution decoder has been proved."
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
        "stable_three_copy_frame_all_n_conditioning_theorem_count": 0,
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
                "from": "a direct polynomial stable three-copy frame block encoding and well-conditioned n=8 controls",
                "invalid_to": "uniform inverse-frame filter or hidden-involution decoder",
                "reason": (
                    "QSVT inversion requires an all-n lower bound on the positive frame spectrum, and measurement "
                    "outcomes still need an information and decoding theorem."
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
            "stable_three_copy_frame_all_n_conditioning_proved": False,
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
                "and its three-copy frame is directly block-encoded, but the carrier is not compressed. Known "
                "primitives still stop before an all-n conditioning theorem, inverse frame filter, full-sector "
                "coverage, hidden-involution decoding, and separation."
            ),
        },
        status="known-primitives-separated-from-open-recoupling-and-decoder",
        summary=(
            f"Classified {len(CAPABILITIES)} representation primitives and exact finite Kronecker growth through "
            f"n={max(n_values)} without transferring solved QFT/counting results to the open decoder."
        ),
        falsifiers_triggered=[
            "The S_n QFT is already polynomial and cannot be presented as the missing breakthrough.",
            "Exact Holevo/Fano accounting charges copies but does not construct a collective measurement or decoder.",
            "#BQP multiplicity counting does not construct a coherent Kronecker basis.",
            "Schur-Weyl Clebsch-Gordan circuits do not automatically solve internal Specht tensor products.",
            "Diagonal YJM tableau labels retain exact Kronecker multiplicity degeneracy.",
            "An encoded stable shape router does not construct a compressed Clebsch channel isometry.",
            "An encoded left/right relabelling isometry does not construct the state-dependent frame filter or decoder.",
            "A finite well-conditioned stable frame does not prove all-n inverse filtering or outcome decoding.",
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
        negatives = (
            (
                "NEG-COSET-SN-QFT-AS-MULTICOPY-DECODER",
                "An efficient S_n QFT supplies the missing multi-copy hidden-involution decoder.",
                "The QFT is a solved one-register basis transform and does not implement internal Kronecker recoupling or decoding.",
            ),
            (
                "NEG-COSET-KRONECKER-COUNT-AS-TRANSFORM",
                "A #BQP characterization of Kronecker coefficients supplies a coherent Kronecker transform.",
                "Counting an invariant-space dimension by projectors does not construct its basis or transition amplitudes.",
            ),
            (
                "NEG-COSET-RESTRICTED-MULTIPLICITY-AS-BREAKTHROUGH",
                "Restricted multiplicity estimation currently supports a superpolynomial representation-theoretic speedup.",
                "Polynomial classical algorithms cover many proposed restricted families, and no hidden-involution reduction is supplied.",
            ),
        )
        for negative_id, claim, reason in negatives:
            upsert_negative_result(
                NegativeResultRecord(
                    id=negative_id,
                    source=str(output_path),
                    claim=claim,
                    reason_invalid=reason,
                    lesson="Track each representation primitive by exact action, promise, circuit cost, output, and decoder role.",
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence=payload["headline_metrics"],
                )
            )
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
    return payload
