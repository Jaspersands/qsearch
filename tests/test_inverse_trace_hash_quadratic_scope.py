"""Finite replay of the shortened-kernel obstruction, not a solving bound."""
from itertools import combinations
import json
from math import prod
from pathlib import Path
from random import Random

import pytest

from theorems.balanced_codeword_filter import trace_mask
from theorems.explicit_quadratic_opi import element, encoded, field

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("bits,beta0,violation,rank", [(11, 1374, 1995, 77),
                                                     (17, 14438, 37204, 170)])
def test_saved_shortened_kernel_prevents_arbitrary_local_xx_gluing(bits, beta0, violation, rank):
    report = json.loads((ROOT/f"research/classical_baselines/inverse_trace_hash_cells_n{bits}.json").read_text())
    instance, residual = report["instance"], report["residual"]
    points = [element(bits, instance["points"][i]) for i in residual["residual_indices"]]
    checks = instance["checks"]
    surplus = len(points)-checks
    assert len(points) < 2*checks+1
    indices = range(3*surplus-1)
    assert len(indices) <= len(points)
    one, zero = field(bits).one(), field(bits).zero()
    weights = [prod((x+y for j, y in enumerate(points) if i != j), start=one)**-1
               for i, x in enumerate(points)]
    coefficients = [weights[i]**-3 / prod((points[i]+points[j] for j in indices if i != j), start=one)
                    for i in indices]
    assert encoded(coefficients[0]) == beta0
    assert encoded(coefficients[0]*element(bits, 6)) == violation != 0
    columns = [[weights[i]*points[i]**degree*element(bits, 1 << bit) for i in indices]
               for degree in range(surplus) for bit in range(bits)]
    # A Boolean quadratic vanishing on all basis vectors and pairs is zero.
    for selected in (*((i,) for i in range(bits*surplus)),
                     *combinations(range(bits*surplus), 2)):
        difference = [sum((columns[j][i] for j in selected), zero) for i in indices]
        assert sum((c*x**3 for c, x in zip(coefficients, difference)), zero) == zero

    # Independently certify the desired local xx data is attainable in the
    # target-one quadratic lift; the obstruction is to global extension.
    rng, basis = Random(1022), {}
    pairs = list(combinations(range(bits), 2))
    mask = trace_mask(bits, 1)
    for _ in range(32*bits):
        y = rng.getrandbits(bits)
        if (y & mask).bit_count() % 2 != 1:
            y ^= mask & -mask
        x = encoded(element(bits, y)**-1)
        row = 1 | (x << 1) | (y << (bits+1))
        row |= sum((((x >> i) & (x >> j) & 1) << (1+2*bits+k))
                   for k, (i, j) in enumerate(pairs))
        while row:
            pivot = row.bit_length()-1
            if pivot not in basis:
                basis[pivot] = row
                break
            row ^= basis[pivot]
    assert len(basis) == rank == 2*bits+bits*(bits-1)//2


def test_saved_n11_hash_forces_an_additional_single_block_constraint():
    report = json.loads((ROOT/"research/classical_baselines/inverse_trace_hash_cells_n11.json").read_text())
    cell = report["cells"][2]
    selector, row = 0x15ab, 0
    for j, original in enumerate(cell["hash_rows"]):
        if (selector >> j) & 1:
            row ^= original
    assert row == 0x1d9 << 10
    assert (selector & cell["hash_rhs"]).bit_count() % 2 == 0


def test_all_three_saved_empty_n11_cells_have_checked_quadratic_duals():
    from theorems.inverse_trace_hash_quadratic import analyze_cell, verify_relaxation_certificate
    from theorems.inverse_trace_local_quadratic_span import span_certificate, verify_span_certificate
    report = json.loads((ROOT/"research/classical_baselines/inverse_trace_hash_cells_n11.json").read_text())
    residual = report["residual"]
    assert verify_span_certificate(span_certificate(11, 1))
    for cell in report["cells"]:
        # This emptiness receipt is from the earlier exhaustive hash-slice
        # reference, not inferred from the quadratic relaxation or SAT timeout.
        reference = cell["independent_reference"]
        assert reference["status"] == "EXACT_FINITE_HASH_SLICE"
        assert reference["checked"] == 32768 and reference["solutions"] == []
        result = analyze_cell(report["instance"], residual["residual_indices"],
                              residual["residual_syndrome"], cell["hash_rows"], cell["hash_rhs"])
        assert result["processed_row_count"] == result["expected_row_count"] == 1188
        assert result["quadratic_relaxation_feasible_certified"]
        assert verify_relaxation_certificate(result)
        assert not result["native_cell_empty_certified"]
        assert result["row_rank"] == 990
