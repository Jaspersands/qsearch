"""Conditional ECF resource plan; no graph recognition or root compiler."""

from fractions import Fraction as Q
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/"hdqi-rational-transfer-2026-10-25"))
from rational_thermal import construct
from tree_sampler import rational


def conditional_thermal_plan(decomposition, couplings, beta, error):
    """Use m as a conservative mode bound, never a path-only alpha formula."""
    couplings = tuple(rational(j) for j in couplings)
    beta, error = rational(beta), rational(error)
    m = decomposition.size
    if len(couplings) != m or any(not j or abs(j) > 1 for j in couplings):
        raise ValueError("nonzero real native couplings of magnitude <=1 required")
    if beta <= 0 or not 0 < error <= 1:
        raise ValueError("beta>0 and 0<error<=1 required; beta zero is trivial")
    scalar = construct(beta*sum(map(abs, couplings))/2, error/(4*m))
    factors = scalar["transfer_degree_upper"]
    maximum = max(map(len, decomposition.independent_masks))
    ceil_log2 = (maximum-1).bit_length()
    return {"scope": "conditional ECF full-native-word thermal sampling bound",
            "vertices": m, "mode_count_upper": m, "beta": str(beta), "error": str(error),
            "factors_upper": factors,
            "bag_independence_bound": decomposition.bound,
            "max_independent_subsets_per_bag": maximum,
            "max_pair_states_log2_upper": 2*factors*ceil_log2,
            "conditional_thermal_squared_vector_error_upper": m*scalar["uniform_error_upper"]**2,
            "scalar_approximation": scalar,
            "ecf_graph_verified": False, "conditional_on_ecf_transfer_identity": True,
            "complex_factors_compiled": False, "full_thermal_sampler_executed": False,
            "polynomial_classical_sampler_claim": False, "quantum_advantage_claim": False}
