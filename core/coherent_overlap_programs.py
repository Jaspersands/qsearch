"""Costed retained-data echo programs, not a circuit-optimization search space."""

from dataclasses import dataclass
from fractions import Fraction
import math

from isotypic_instruments import _sqrt_ratio_dyadic_exponent, isotypic_label_resource_contract


@dataclass(frozen=True)
class OverlapEchoProgram:
    """Alternate disjoint odd/even bonds on a path, then undo each layer.

    In chronological order the layers are A, B, A^dagger, B^dagger.
    Each bond reflects the negative-character isotypic sectors. These are
    involutions, but the layer order is NOT reversed during the echo.
    """

    degree: int
    transpositions: int
    copies: int
    rounds: int = 1

    def __post_init__(self):
        if any(type(x) is not int for x in
               (self.degree, self.transpositions, self.copies, self.rounds)):
            raise ValueError("program parameters must be integers, not booleans")
        if (self.degree < 2 or not 1 <= self.transpositions <= self.degree // 2
                or self.copies < 3 or self.rounds < 1):
            raise ValueError("valid involution class, at least three copies and positive rounds required")

    def layers(self) -> tuple[tuple[int, bool], ...]:
        return ((0, False), (1, False), (0, True), (1, True))

    def chronological_bonds(self, *, maximum_queries: int = 10000) -> tuple[tuple[int, int], ...]:
        if type(maximum_queries) is not int or maximum_queries < 0:
            raise ValueError("nonnegative integer expansion budget required")
        if self.query_count > maximum_queries:
            raise ValueError("explicit program expansion budget exceeded; use the symbolic contract")
        return tuple((i, i + 1) for _ in range(self.rounds)
                     for parity, _inverse in self.layers()
                     for i in range(parity, self.copies - 1, 2))

    @property
    def query_count(self) -> int:
        return 2 * (self.copies - 1) * self.rounds

    def resource_contract(self, *, forward_gpe_operator_error: float = 0.0) -> dict:
        if (not isinstance(forward_gpe_operator_error, (int, float))
                or isinstance(forward_gpe_operator_error, bool)
                or not math.isfinite(forward_gpe_operator_error) or forward_gpe_operator_error < 0):
            raise ValueError("finite nonnegative GPE operator error required")
        base = isotypic_label_resource_contract(
            self.degree, 2, self.query_count, forward_gpe_operator_error)
        class_size = math.factorial(self.degree) // (
            2**self.transpositions * math.factorial(self.transpositions)
            * math.factorial(self.degree - 2*self.transpositions))
        # The known raw-copy cap is independent of query count. Avoid building
        # 2^K when it already makes the bound vacuous for the growing program.
        cap = (Fraction(1) if self.copies >= (4*class_size).bit_length()
               else min(Fraction(1), Fraction((1 << self.copies) - 1, 4*class_size)))
        return {
            "degree": self.degree, "transpositions": self.transpositions,
            "copies": self.copies, "rounds": self.rounds,
            "phase_rule": "minus_one_iff_exact_involution_character_is_negative; zero_maps_to_plus_one",
            "chronological_layer_period": ["ODD_BONDS", "EVEN_BONDS", "ODD_BONDS_ADJOINT", "EVEN_BONDS_ADJOINT"],
            "controlled_phase_queries": self.query_count,
            "group_qft_or_inverse_calls": base["group_qft_or_inverse_calls"],
            "uniform_preparation_or_inverse_calls": base["uniform_preparation_or_inverse_calls"],
            "controlled_single_copy_group_action_or_inverse_calls": base["controlled_single_copy_group_action_or_inverse_calls"],
            "character_arithmetic_or_uncomputation_calls": 2 * self.query_count,
            "data_register_qubits": self.copies * base["reference_register_qubits"],
            "reference_register_qubits": base["reference_register_qubits"],
            "readout_qubits": 1,
            "readout": "Prepare |+>, control every echo operation on this qubit, measure X; minus means NULL in the fixed decision rule.",
            "minus_probability": "(1-Re Tr[W rho])/2",
            "coset_preparations_per_trial": self.copies,
            "data_reprepared_between_queries": False,
            "source_labels_measured": False,
            "intermediate_isotypic_labels_measured_or_discarded": False,
            "free_postselection": False,
            "distinct_subset_palette_size": self.copies - 1,
            "nonempty_subset_incidence_cells": self.copies,
            "composed_channel_diamond_distance_upper_bound": base["composed_channel_diamond_distance_upper_bound"],
            "fixed_point_free_character_predicate_polynomial": 2 * self.transpositions == self.degree,
            "uniform_reduction_to_known_primitives": True,
            "gate_level_backend_supplied": False,
            "same_shared_hidden_member_across_all_copies": True,
            "known_raw_class_mixture_trace_distance_squared_cap": {
                "numerator_hex": hex(cap.numerator), "denominator_hex": hex(cap.denominator)},
            "known_raw_class_mixture_trace_distance_log2_outward_cap": _sqrt_ratio_dyadic_exponent(cap.numerator, cap.denominator),
            "raw_copy_cap_independent_of_round_count": True,
            "finite_group_enumeration_is_algorithm_runtime": False,
            "fixed_decision_rule_supplied": True,
            "inverse_polynomial_bias_proved": False,
            "useful_repetition_budget_proved": False,
            "natural_problem_reduction_proved": False,
            "speedup_claim_allowed": False,
        }
