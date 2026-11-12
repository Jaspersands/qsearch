#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""Fixed L=4 exact resistor-network energy transcription control.

Only three declared patterns, both forcing directions, one exact Sage run.
Writes sibling result.json. No matrix square roots or quantum circuits.
"""
import hashlib
import json
from pathlib import Path

from sage.all import QQ, identity_matrix, matrix, vector


def main():
    L, dimension, rho = 4, 2, QQ(2)
    N = L ** dimension
    nodes = [(x0, x1) for x0 in range(L) for x1 in range(L)]
    node_index = {x: i for i, x in enumerate(nodes)}
    edges = [(x, j) for x in nodes for j in range(dimension)]
    E = len(edges)
    D = matrix(QQ, E, N)
    for row, (x, j) in enumerate(edges):
        nxt = list(x)
        nxt[j] = (nxt[j] + 1) % L
        D[row, node_index[tuple(nxt)]] = 1
        D[row, node_index[x]] = -1
    one = vector(QQ, [1] * N)
    P0 = matrix(QQ, N, N, [QQ(1) / N] * (N * N))
    K0 = D.transpose() * D
    Pi = D * (K0 + P0).inverse() * D.transpose()
    I = identity_matrix(QQ, E)
    assert D * one == vector(QQ, E)
    assert P0 == P0.transpose() and P0 * P0 == P0
    assert Pi == Pi.transpose() and Pi * Pi == Pi
    assert Pi.rank() == N - 1
    assert K0 * P0 == matrix(QQ, N, N)
    forcing = [vector(QQ, [int(j == direction) for _, j in edges])
               for direction in range(dimension)]
    assert all(Pi * e == vector(QQ, E) for e in forcing)
    assert all(e.dot_product(e) == N for e in forcing)

    c = (rho + 1) / 2
    s0 = c / rho
    delta = (rho - 1) / (rho + 1)
    highest_power = 5  # Exactly six terms, fixed before running.
    assert delta == QQ(1) / 3 and s0 == QQ(3) / 4
    patterns = {
        "constant1": lambda x, j: 1,
        "layers": lambda x, j: 1 + int(x[0] >= 2),
        "nonlayered": lambda x, j: 1 + int((x[0] + 2 * x[1] + j) % 3 == 0),
    }
    results = []
    for name, pattern in patterns.items():
        values = vector(QQ, [pattern(x, j) for x, j in edges])
        A = matrix.diagonal(values)
        S = A / rho
        Ka = D.transpose() * A * D
        C = I + Pi * (S - I) * Pi
        # On range(Pi), C=s0*(I+T). Its complement is the identity.
        B = A / c - I
        T = Pi * B * Pi
        assert T == T.transpose()
        assert max(abs(v) for v in B.diagonal()) == delta
        assert C * Pi == s0 * (I + T) * Pi
        for direction, e in enumerate(forcing):
            phi = -(Ka + P0).solve_right(D.transpose() * A * e)
            field = e + D * phi
            assert one.dot_product(phi) == 0
            assert D.transpose() * A * field == vector(QQ, N)
            direct_K = field.dot_product(A * field) / N
            q_edge = Pi * S * e
            correction = q_edge.dot_product(C.solve_right(q_edge)) / N
            projection_K_over_rho = e.dot_product(S * e) / N - correction
            assert direct_K / rho == projection_K_over_rho
            q_squared_over_N = q_edge.dot_product(q_edge) / N
            q_zero = q_edge == vector(QQ, E)
            assert q_zero == (D.transpose() * S * e == vector(QQ, N))

            # Pi is symmetric/idempotent, hence has Euclidean norm 1.
            # B is diagonal with |B_ee|<=delta. Therefore ||T||<=delta<1.
            # On range(Pi), C^-1=s0^-1*sum_{l>=0}(-T)^l.
            # The omitted quadratic-form tail after l=p is bounded by
            # (||q_edge||²/(s0*N))*delta^(p+1)/(1-delta).
            terms = []
            v = q_edge
            for power in range(highest_power + 1):
                terms.append((-1) ** power * q_edge.dot_product(v) / (s0 * N))
                v = T * v
            partial_K_over_rho = e.dot_product(S * e) / N - sum(terms)
            tail_bound_K_over_rho = q_squared_over_N / s0 * delta ** (highest_power + 1) / (1 - delta)
            actual_error_K_over_rho = abs(partial_K_over_rho - direct_K / rho)
            assert actual_error_K_over_rho <= tail_bound_K_over_rho
            analytic_expected = None
            if name == "constant1":
                analytic_expected = QQ(1)
                assert q_zero and direct_K == analytic_expected
            elif name == "layers":
                analytic_expected = QQ(4) / 3 if direction == 0 else QQ(3) / 2
                assert direct_K == analytic_expected
            results.append({
                "pattern": name, "forcing_direction": direction,
                "edge_conductivities_in_declared_order": [str(a) for a in values],
                "direct_K": str(direct_K), "direct_K_over_rho": str(direct_K / rho),
                "projection_K_over_rho": str(projection_K_over_rho),
                "projection_equals_direct": True,
                "mean_zero_potential_in_declared_node_order": [str(x) for x in phi],
                "normal_equations_exact": True, "q_vanishes": q_zero,
                "q_edge_norm_squared_over_N": str(q_squared_over_N),
                "analytic_expected_K": None if analytic_expected is None else str(analytic_expected),
                "neumann": {
                    "highest_power": highest_power, "term_count": highest_power + 1,
                    "correction_terms_K_over_rho": [str(term) for term in terms],
                    "partial_K_over_rho": str(partial_K_over_rho),
                    "partial_K": str(rho * partial_K_over_rho),
                    "actual_absolute_error_K_over_rho": str(actual_error_K_over_rho),
                    "tail_bound_K_over_rho": str(tail_bound_K_over_rho),
                    "actual_absolute_error_K": str(rho * actual_error_K_over_rho),
                    "tail_bound_K": str(rho * tail_bound_K_over_rho),
                    "error_le_rigorous_tail_bound": True,
                },
            })
    result = {
        "status": "PASS_FINITE_EXACT", "arithmetic": "Sage QQ, no floating comparisons",
        "fixture": {"L": L, "dimension": dimension, "nodes": N, "oriented_edges": E,
                    "rho": str(rho), "node_order": [list(x) for x in nodes],
                    "edge_order": "node_order outer, direction j=0 then j=1 inner",
                    "edge_orientation": "D phi(x,j)=phi(x+e_j)-phi(x), periodic modulo L",
                    "patterns": {"constant1": "a(x,j)=1", "layers": "a(x,j)=1+(x0>=2)",
                                 "nonlayered": "a(x,j)=1+((x0+2*x1+j)%3==0)"}},
        "global_checks": {"Pi_symmetric_idempotent": True, "Pi_rank": int(Pi.rank()),
                          "constant_projector_gauge": True, "Pi_annihilates_both_forcing_vectors": True,
                          "six_cases_only": len(results) == 6},
        "projection_formula": "Pi=D*(K0+P0)^-1*D^T; C=I+Pi*(S-I)*Pi; K/rho=(e^T*S*e-(Pi*S*e)^T*C^-1*(Pi*S*e))/N",
        "neumann_derivation": {
            "c": str(c), "s0": str(s0), "delta": str(delta),
            "definitions": "B=a/c-I; T=Pi*B*Pi; q_edge=Pi*S*e; e is unnormalized direction indicator",
            "norm_bound": "Pi symmetric idempotent gives norm(Pi)=1; diagonal |B_ee|<=delta gives norm(T)<=delta=1/3",
            "inverse_on_gradient_range": "C^-1*q_edge=s0^-1*sum_{l>=0}(-T)^l*q_edge",
            "normalized_energy_tail": "abs(error in K/rho)<=||q_edge||^2/(s0*N)*delta^(p+1)/(1-delta), p=5",
            "conductivity_tail": "Multiply the normalized-energy bound by rho to bound error in K",
        },
        "cases": results,
        "claim_gates": {"finite_control_only": True, "asymptotic_scaling_claim": False,
                        "quantum_circuit_execution": False, "quantum_speedup": False,
                        "classical_hardness": False, "separation": False,
                        "succinct_all_input_estimator_implemented": False,
                        "matrix_square_root_used": False, "fixture_tuning": False},
        "control_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    path = Path(__file__).with_name("result.json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "result": str(path),
                      "exact_K": [{"pattern": x["pattern"], "direction": x["forcing_direction"],
                                   "K": x["direct_K"]} for x in results]}))


if __name__ == "__main__":
    main()
