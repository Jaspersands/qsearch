"""Replay the unchanged resident decoder body with table-free input adapters.

AST selection avoids importing unrelated, possibly offloaded research modules.
This is a classical dependency test, not reversible-circuit compilation.
"""
import ast
import hashlib
from itertools import product
from pathlib import Path

from flint import fmpz, fq_default_ctx


DECODER = Path('/Users/jaspersands/Desktop/quantum algorithm search/theorems/balanced_signed_mpi.py')


def encoded(value):
    return sum(int(c) << i for i, c in enumerate(value.to_list()))


def replay():
    bits, order = 64, (1 << 64)-1
    field = fq_default_ctx(2, bits)
    primes = (3, 5, 17, 257, 641, 65537, 6700417)
    factor_product = 1
    for prime in primes:
        assert fmpz(prime).is_prime()
        factor_product *= prime
    assert factor_product == order
    generator = None
    for offset in range(256):
        candidate = field.gen() + field([(offset >> i) & 1 for i in range(bits)])
        if candidate != 0 and all(candidate**(order//r) != 1 for r in primes):
            generator = candidate
            break
    if generator is None:
        raise RuntimeError("capped diagnostic generator construction failed")
    multiplier = order//15
    alpha = generator**multiplier
    subfield_log, points = {}, [field.zero()]
    for exponent in range(15):
        value = alpha**exponent
        subfield_log[encoded(value)] = multiplier*exponent
        points.append(value)
    if len(subfield_log) != 15:
        raise ArithmeticError("invalid subfield construction")
    supports = tuple(encoded(x) for x in points[:4])
    evaluations = tuple(encoded(x) for x in points[4:8])
    matrix = tuple(tuple(subfield_log[t ^ z] for z in evaluations) for t in supports)
    power_calls = 0

    class LazyPowers:
        def __getitem__(self, exponent):
            nonlocal power_calls
            if type(exponent) is not int or not 0 <= exponent < order:
                raise ValueError("noncanonical exponent")
            power_calls += 1
            return generator**exponent

    def element(local_bits, word):
        assert local_bits == bits
        return field([(word >> i) & 1 for i in range(bits)])

    def syndrome(local_bits, ts, zs, y):
        assert local_bits == bits and ts == supports and zs == evaluations
        return tuple(sum(y[i]*matrix[i][j] for i in range(4)) % order for j in range(4))

    source = DECODER.read_text()
    tree = ast.parse(source, filename=str(DECODER))
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name in {"license_box", "decode"}]
    assert len(nodes) == 2
    from flint import fq_default_poly_ctx
    namespace = {"field": lambda b: field if b == bits else None,
                 "element": element, "fq_default_poly_ctx": fq_default_poly_ctx,
                 "presentation": lambda b: (LazyPowers(), None, None), "syndrome": syndrome}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(DECODER), "exec"), namespace)
    decoded = 0
    for y in product((-1, 0, 1), repeat=4):
        if y.count(1) <= 1 and y.count(-1) <= 1:
            observed = syndrome(bits, supports, evaluations, y)
            if namespace["decode"](bits, supports, evaluations, observed, 1) != y:
                raise ArithmeticError("unchanged rational decoder failed")
            decoded += 1
    outside = (1, 1, 0, 0)
    rejected = namespace["decode"](bits, supports, evaluations,
                                   syndrome(bits, supports, evaluations, outside), 1) is None
    if not rejected:
        raise ArithmeticError("outside-box pattern accepted")
    return {"field_bits": bits, "cyclic_order": order, "licensed_patterns_decoded": decoded,
            "outside_box_rejected": rejected, "field_power_evaluations": power_calls,
            "full_field_log_table_entries": 0,
            "subfield_entries_used_ONLY_for_public_fixture_construction": 15,
            "source_path": str(DECODER), "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "changed_decoder_body": False, "compiled_reversible_circuit": False,
            "scope": "large-field arithmetic control on a deliberately easy public subfield fixture"}


if __name__ == '__main__':
    import json
    print(json.dumps(replay(), indent=2))
