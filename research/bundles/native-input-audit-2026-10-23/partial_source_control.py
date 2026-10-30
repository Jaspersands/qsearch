"""Bounded linear-algebra control of one-sided source-action blindness.

No hiding function, candidate oracle problem, or isogeny is generated.
The general result is the subspace proof in NATIVE_INPUT_GATE.md.
"""

from functools import lru_cache
from itertools import product


def _pair(v, w, p):
    return sum(v[i]*w[i+1]-v[i+1]*w[i] for i in range(0, len(v), 2)) % p


def _act(columns, vector, p):
    return tuple(sum(column[i]*coefficient for column, coefficient in zip(columns, vector)) % p
                 for i in range(len(vector)))


def symplectic_columns_three():
    """Enumerate Sp4(F3) through complete ordered symplectic bases."""
    vectors = tuple(product(range(3), repeat=4))
    for v in vectors:
        if not any(v):
            continue
        for w in vectors:
            if _pair(v, w, 3) != 1:
                continue
            complement = [x for x in vectors if _pair(v, x, 3) == _pair(w, x, 3) == 0]
            for x in complement:
                if not any(x):
                    continue
                for y in complement:
                    if _pair(x, y, 3) == 1:
                        yield v, w, x, y


def anti_isometry_columns_three():
    for a, b, c, d in product(range(3), repeat=4):
        if (a*d-b*c) % 3 == 2:
            yield (a, c, 0, 0), (b, d, 0, 0)


def stabilizes_padded_graph(columns, gluing_columns):
    """K_f={(f(u)+l,u)}; L=<e_3> in known V=F3^4, unknown U=F3^2."""
    if any(columns[2][i] for i in (0, 1, 3)):
        return False
    for vector in gluing_columns:
        image = _act(columns, vector, 3)
        if any((image[i]-vector[i]) % 3 for i in (0, 1, 3)):
            return False
    return True


@lru_cache(maxsize=1)
def partial_source_control():
    gluings = tuple(anti_isometry_columns_three())
    if len(gluings) != 24 or len(set(gluings)) != 24:
        raise AssertionError("anti-isometry count")
    # Appending the unknown u coordinates makes each graph isotropic.
    if not all((_pair(f[0], f[1], 3)+1) % 3 == 0 for f in gluings):
        raise AssertionError("gluing is not anti-symplectic")
    group_count, subgroup_sizes, mismatch = 0, [0]*len(gluings), 0
    for columns in symplectic_columns_three():
        group_count += 1
        decisions = tuple(stabilizes_padded_graph(columns, f) for f in gluings)
        mismatch += int(len(set(decisions)) != 1)
        for i, decision in enumerate(decisions):
            subgroup_sizes[i] += int(decision)
    if group_count != 51840 or mismatch or set(subgroup_sizes) != {54}:
        raise AssertionError((group_count, subgroup_sizes, mismatch))
    return {"field_prime": 3, "known_space_dimension": 4, "fixed_unknown_space_dimension": 2,
            "distinct_lagrangian_gluings": len(gluings),
            "symplectic_group_elements_checked": group_count,
            "shared_stabilizer_size": subgroup_sizes[0],
            "orbit_index": group_count//subgroup_sizes[0],
            "stabilizer_disagreement_count": mismatch,
            "same_coset_state_for_every_gluing": True,
            "geometric_label_values_used": False,
            "no_go_for_all_quantum_algorithms": False,
            "isogeny_source_executed": False}
