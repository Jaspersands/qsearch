#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""One F3 modular-descent falsifier, using explicit cellular cohomology.

No parameter sweep. One regular SL2(F3) cover of the thrice-punctured sphere.
Writes sibling result.json. No claim about all surface algorithms follows.
"""
from collections import Counter
from itertools import product
import hashlib
import json
from pathlib import Path

from sage.all import GF, identity_matrix, matrix, vector


def main():
    F = GF(3)
    I2 = identity_matrix(F, 2)
    a = matrix(F, [[1, 2], [0, 1]])
    b = matrix(F, [[1, 0], [-2, 1]])
    c = (a * b).inverse()
    zero2 = matrix(F, 2, 2)

    def key(g):
        return tuple(int(x) for x in g.list())

    def rows(g):
        return [[int(x) for x in row] for row in g.rows()]

    def order(g):
        v = I2
        for e in range(1, 49):
            v = v * g
            if v == I2:
                return e
        raise AssertionError("Order exceeds finite group-size guard")

    group = [I2]
    seen = {key(I2)}
    for g in group:
        for generator in [a, b]:
            nxt = g * generator
            if key(nxt) not in seen:
                seen.add(key(nxt))
                group.append(nxt)
    # Verify that the generated matrices are exactly SL2(F3), not a quotient.
    all_SL2 = {tuple(int(x) for x in g.list())
               for entries in product(range(3), repeat=4)
               for g in [matrix(F, 2, 2, entries)] if g.det() == 1}
    assert seen == all_SL2
    ng = len(group)
    gi = {key(g): i for i, g in enumerate(group)}
    edges = [(g, j) for g in group for j in range(2)]
    ne = len(edges)
    ei = {(key(g), j): i for i, (g, j) in enumerate(edges)}
    boundary1 = matrix(F, ng, ne)
    for col, (g, j) in enumerate(edges):
        h = g * [a, b][j]
        boundary1[gi[key(h)], col] += 1
        boundary1[gi[key(g)], col] -= 1

    face_boundaries = []
    face_labels = []
    orbits_by_inertia = {}
    for name, t in [("a", a), ("b", b), ("c=(ab)^-1", c)]:
        used = set()
        orbit_sizes = []
        for start in group:
            if key(start) in used:
                continue
            chain = vector(F, ne)
            g = start
            length = 0
            while key(g) not in used:
                used.add(key(g))
                length += 1
                if name == "a":
                    chain[ei[(key(g), 0)]] += 1
                elif name == "b":
                    chain[ei[(key(g), 1)]] += 1
                else:
                    # c=b^-1 a^-1: traverse backwards along a b-edge,
                    # then backwards along an a-edge, preserving the word order.
                    middle = g * b.inverse()
                    endpoint = middle * a.inverse()
                    assert endpoint == g * c
                    chain[ei[(key(middle), 1)]] -= 1
                    chain[ei[(key(endpoint), 0)]] -= 1
                g = g * t
            assert g == start
            assert length == order(t)
            assert boundary1 * chain == vector(F, ng)
            orbit_sizes.append(length)
            face_boundaries.append(chain)
            face_labels.append({"inertia": name, "start_matrix": rows(start),
                                "orbit_size": length})
        orbits_by_inertia[name] = dict(Counter(orbit_sizes))
    boundary2 = matrix(F, face_boundaries).transpose()
    assert boundary1 * boundary2 == matrix(F, ng, len(face_boundaries))
    d0 = boundary1.transpose()
    d1 = boundary2.transpose()
    cocycles = d1.right_kernel()
    coboundaries = d0.column_space()
    assert all(v in cocycles for v in coboundaries.basis())
    open_h1 = ne - d0.rank()

    # Quotient coordinates: first coboundary basis, then a complement in ker d1.
    basis = list(coboundaries.basis())
    base_rank = len(basis)
    for v in cocycles.basis():
        if matrix(F, basis + [v]).rank() > len(basis):
            basis.append(v)
    assert len(basis) == cocycles.dimension()
    basis_matrix = matrix(F, basis)
    hdim = len(basis) - base_rank
    deck_actions = {}
    for name, h in [("a", a), ("b", b)]:
        edge_action = matrix(F, ne, ne)
        for col, (g, j) in enumerate(edges):
            edge_action[ei[(key(h * g), j)], col] = 1
        # Cochains act by pullback along L_h^-1. Thus a basis cochain at g
        # moves to h*g, exactly the displayed coordinate permutation.
        assert d1 * edge_action * basis_matrix.transpose() == matrix(F, d1.nrows(), len(basis))
        all_coefficients = basis_matrix.transpose().solve_right(edge_action * basis_matrix.transpose())
        assert all_coefficients[base_rank:, :base_rank] == matrix(F, hdim, base_rank)
        quotient = all_coefficients[base_rank:, base_rank:]
        assert quotient.is_invertible()
        deck_actions[name] = quotient

    def tensor_invariant_dimension(actions):
        equations = [actions[name].tensor_product(natural) - identity_matrix(F, 2 * hdim)
                     for name, natural in [("a", a), ("b", b)]]
        stacked = equations[0].stack(equations[1])
        return stacked.right_kernel().dimension(), stacked.rank()

    tensor_dimension, tensor_rank = tensor_invariant_dimension(deck_actions)
    # Independently record the dual homology action, instead of confusing it
    # with the cochain coordinate permutation. The natural module is self-dual.
    homology_actions = {name: action.inverse().transpose()
                        for name, action in deck_actions.items()}
    homology_tensor_dimension, _ = tensor_invariant_dimension(homology_actions)
    J = matrix(F, [[0, 1], [-1, 0]])
    assert all(g.transpose() * J * g == J for g in [a, b])
    assert all(deck_actions[name] ** order(g) == identity_matrix(F, hdim)
               for name, g in [("a", a), ("b", b)])

    # Natural local system on a free group with generators a,b.
    # A 1-cocycle is (x=f(a), y=f(b)). Its c-value is -c*(x+a*y).
    # Restriction vanishes in H1(<t>,V) iff f(t) lies in im(t-I).
    zero22 = matrix(F, 2, 2)
    restriction_blocks = []
    inertia_data = []
    for name, t, evaluation in [
        ("a", a, I2.augment(zero22)),
        ("b", b, zero22.augment(I2)),
        ("c=(ab)^-1", c, (-c).augment(-c * a)),
    ]:
        e = order(t)
        norm = sum((t ** power for power in range(e)), zero2)
        annihilators = (t - I2).left_kernel().basis_matrix()
        restriction_blocks.append(annihilators * evaluation)
        inertia_data.append({"name": name, "matrix": rows(t), "order": e,
                             "coinvariant_dimension": 2 - (t - I2).rank(),
                             "norm_sum": rows(norm), "norm_sum_is_zero": norm == zero2})
    restrictions = restriction_blocks[0].stack(restriction_blocks[1]).stack(restriction_blocks[2])
    local_coboundaries = (a - I2).stack(b - I2)
    assert restrictions * local_coboundaries == matrix(F, restrictions.nrows(), 2)
    parabolic_cocycles = restrictions.right_kernel().dimension()
    local_h1_open = 4 - local_coboundaries.rank()
    local_h1_parabolic = parabolic_cocycles - local_coboundaries.rank()
    global_invariants = (a - I2).stack(b - I2).right_kernel().dimension()
    euler_characteristic = ng - ne + len(face_boundaries)
    genus = (2 - euler_characteristic) // 2
    assert hdim == 2 * genus
    result = {
        "status": "PASS_FINITE_EXACT",
        "arithmetic": "Sage GF(3); exact ranks, kernels, quotients and finite group enumeration",
        "group": {"name": "SL2(F3)", "order": ng,
                  "generated_group_equals_all_det_one_matrices": True,
                  "a": rows(a), "b": rows(b), "c=(ab)^-1": rows(c),
                  "boundary_word_product_abc_identity": a * b * c == I2},
        "inertia_natural_module": inertia_data,
        "compact_cover": {"vertices": ng, "directed_edges": ne,
                          "filled_faces": len(face_boundaries),
                          "face_orbits_by_inertia": orbits_by_inertia,
                          "Euler_characteristic": euler_characteristic, "genus": genus,
                          "boundary1_rank": boundary1.rank(), "boundary2_rank": boundary2.rank(),
                          "d1_d0_zero": True, "open_H1_dimension": open_h1,
                          "compact_cocycle_dimension": cocycles.dimension(),
                          "coboundary_dimension": base_rank,
                          "compact_H1_cohomology_dimension": hdim,
                          "left_deck_cohomology_a": rows(deck_actions["a"]),
                          "left_deck_cohomology_b": rows(deck_actions["b"]),
                          "tensor_invariant_equation_rank": tensor_rank,
                          "compact_H1_cohomology_tensor_natural_invariant_dimension": tensor_dimension,
                          "dual_homology_tensor_natural_invariant_dimension": homology_tensor_dimension,
                          "natural_selfdual_alternating_form_verified": True,
                          "convention": "Edges right-multiply; left deck cochains pull back by inverse left multiplication. Homology action is separately computed as inverse transpose of cohomology action."},
        "natural_local_system": {"free_group_cocycle_dimension": 4,
                                 "global_invariant_dimension": global_invariants,
                                 "coboundary_dimension": local_coboundaries.rank(),
                                 "H1_open_dimension": local_h1_open,
                                 "inertia_restriction_rank": restrictions.rank(),
                                 "parabolic_cocycle_dimension": parabolic_cocycles,
                                 "H1_parabolic_dimension": local_h1_parabolic,
                                 "restriction_convention": "f(c)=-c*(f(a)+a*f(b)); quotient each inertia value by im(t-I)"},
        "comparison": {"compact_tensor_invariant_dimension": tensor_dimension,
                       "parabolic_local_system_dimension": local_h1_parabolic,
                       "ordinary_invariant_descent_identity_holds": tensor_dimension == local_h1_parabolic,
                       "explicit_finite_representation_identity_falsified": tensor_dimension != local_h1_parabolic,
                       "anticipated_values_observed": tensor_dimension == 2 and local_h1_parabolic == 0,
                       "values_computed_not_imposed": True},
        "claim_gates": {"finite_control_only": True, "all_surface_result": False,
                        "general_algorithm_refutation": False, "new_quantum_algorithm": False,
                        "classical_hardness": False, "separation": False,
                        "asymptotic_complexity_claim": False},
        "control_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    path = Path(__file__).with_name("result.json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True, default=int) + "\n")
    print(json.dumps({"status": result["status"], "result": str(path),
                      "group_order": ng, "compact_H1": hdim, "open_H1": open_h1,
                      "inertia_orders": [x["order"] for x in inertia_data],
                      "tensor_invariant_dimension": tensor_dimension,
                      "parabolic_dimension": local_h1_parabolic,
                      "dual_homology_tensor_invariant_dimension": homology_tensor_dimension}, default=int))


if __name__ == "__main__":
    main()
