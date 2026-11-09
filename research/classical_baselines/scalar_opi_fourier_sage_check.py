#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""Independent exact Sage check of the six retained Algorithm H witnesses.

No Algorithm H implementation is imported or rerun.  Field arithmetic uses
Sage with each original saved modulus and its polynomial-basis integer map.
Uniform affine-section means are computed from native evaluation images,
without Walsh coefficients or signed-frequency merging.
"""

import hashlib
import json
from pathlib import Path
import time

from sage.all import GF, PolynomialRing, QQ, matrix
from sage.version import version as sage_version


HERE = Path(__file__).resolve().parent
INPUT = HERE / "scalar_opi_fft_probe.json"
SAVED = HERE / "scalar_opi_fourier_elimination.json"
OUTPUT = Path(__file__).with_suffix(".json")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def set_bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask -= low


def check_case(source, saved):
    t, q, k, m = (source[key] for key in ("t", "q", "k", "m"))
    N = t * k
    for key in ("t", "q", "k", "m", "seed", "field_modulus"):
        assert saved[key] == source[key], key
    assert q == 2 ** t and m == q - 1
    B = GF(2)
    R = PolynomialRing(B, "X")
    modulus = R(source["field_modulus"])
    assert modulus.is_irreducible() and modulus.degree() == t
    F = GF(q, name="alpha", modulus=modulus)
    elements = [F.from_integer(i) for i in range(q)]
    assert all(int(x.to_integer()) == i for i, x in enumerate(elements))
    bit_vectors = [[(i >> bit) & 1 for bit in range(t)] for i in range(q)]
    # Check Sage's integer map means the stated polynomial basis.
    assert all(elements[i] == sum((F.gen() ** b for b in set_bits(i)), F.zero())
               for i in range(q))
    tables = [set(row) for row in source["tables"]]
    assert len(tables) == m and all(len(row) == q // 2 for row in tables)

    result = saved["algorithm_h_greedy"]
    coefficients = result["monomial_coefficients"]
    assert len(coefficients) <= k and all(0 <= c < q for c in coefficients)
    P = PolynomialRing(F, "Z")
    poly = P([elements[c] for c in coefficients])
    assert poly.degree() < k
    words = []
    for point in elements[1:]:
        value = F.zero()
        for coefficient in reversed(coefficients):
            value = value * point + elements[coefficient]
        assert value == poly(point)
        words.append(int(value.to_integer()))
    assert words == result["word"]
    score = sum(word in table for word, table in zip(words, tables))
    assert score == result["hits"]
    assignment = int(result["binary_assignment_hex"], 16)
    assert assignment == sum(c << (t * j) for j, c in enumerate(coefficients))
    assert assignment < 2 ** N

    # Native evaluation affine map: offset_i + sum_j column_ij * v_j.
    # Coordinates retain original positions after each least-pivot restriction.
    columns = []
    for point in elements[1:]:
        powers = [point ** degree for degree in range(k)]
        columns.append([power * elements[1 << b]
                        for power in powers for b in range(t)])
    offsets = [F.zero() for _ in range(m)]
    active = set(range(N))
    trajectory = result["trajectory"]
    assert len(trajectory) == result["steps"]
    checkpoints = (set(range(len(trajectory) + 1)) if q == 16 else
                   {0, N // 4, N // 2, 3 * N // 4, N - t, len(trajectory)})
    checkpoints = {step for step in checkpoints if step <= len(trajectory)}
    means = []
    affine_image_rows = 0

    def check_mean(step, expected_numerator):
        nonlocal affine_image_rows
        mean = QQ.zero()
        ranks = []
        rank_histogram = {}
        fully_accepted_rank_histogram = {}
        mean_sums_by_rank = {}
        for row, offset, table in zip(columns, offsets, tables):
            vectors = [bit_vectors[int(row[j].to_integer())] for j in active]
            span = matrix(B, vectors, ncols=t).row_space()
            basis = [elements[sum(int(entry) << b for b, entry in enumerate(vec))]
                     for vec in span.basis()]
            image = [F.zero()]
            for basis_element in basis:
                image += [value + basis_element for value in image]
            assert len(image) == 2 ** span.dimension()
            accepted = sum(int((offset + value).to_integer()) in table for value in image)
            row_mean = QQ(accepted) / len(image)
            mean += row_mean
            rank = int(span.dimension())
            ranks.append(rank)
            rank_histogram[rank] = rank_histogram.get(rank, 0) + 1
            if accepted == len(image):
                fully_accepted_rank_histogram[rank] = fully_accepted_rank_histogram.get(rank, 0) + 1
            mean_sums_by_rank[rank] = mean_sums_by_rank.get(rank, QQ.zero()) + row_mean
        assert mean == QQ(expected_numerator) / q, (q, source["seed"], step, mean)
        means.append({"step": step, "mean": str(mean),
                      "saved_numerator": expected_numerator, "denominator": q,
                      "minimum_row_rank": min(ranks), "maximum_row_rank": max(ranks),
                      "row_rank_histogram": rank_histogram,
                      "fully_accepted_row_rank_histogram": fully_accepted_rank_histogram,
                      "row_mean_sum_by_rank": {rank: str(total) for rank, total in mean_sums_by_rank.items()}})
        affine_image_rows += m

    numerator = m * q // 2
    if 0 in checkpoints:
        check_mean(0, numerator)
    total_gain = 0
    eliminated = set()
    for number, step in enumerate(trajectory, 1):
        assert step["step"] == number
        mask = int(step["selected_mask_hex"], 16)
        positions = list(set_bits(mask))
        assert positions and set(positions) <= active
        pivot = positions[0]
        assert step["pivot_bit"] == pivot
        parity = step["fixed_parity"]
        weight = step["selected_signed_weight"]
        assert parity in (0, 1) and weight != 0
        assert parity == int(weight < 0)
        # Every equation is checked against the saved final native witness.
        assert ((mask & assignment).bit_count() & 1) == parity
        gain = abs(weight)
        numerator += gain
        total_gain += gain
        assert step["mean_numerator"] == numerator and step["mean_denominator"] == q
        for i, row in enumerate(columns):
            pivot_column = row[pivot]
            if parity:
                offsets[i] += pivot_column
            for j in positions[1:]:
                row[j] += pivot_column
            row[pivot] = F.zero()
        active.remove(pivot)
        eliminated.add(pivot)
        if number in checkpoints:
            check_mean(number, numerator)

    assert N - len(eliminated) == result["unfixed_bits"]
    assert all(((assignment >> bit) & 1) == 0 for bit in active)
    assert total_gain == result["total_gain_numerator"]
    assert result["common_denominator"] == q
    assert numerator == score * q
    assert [int(x.to_integer()) for x in offsets] == words
    return {"q": q, "t": t, "k": k, "seed": source["seed"], "score": score,
            "native_evaluations": m, "degree": int(poly.degree()),
            "restrictions_and_native_parities_checked": len(trajectory),
            "trajectory_gain_identities_checked": len(trajectory),
            "total_gain_numerator": total_gain,
            "independent_exact_section_means": means,
            "independent_affine_image_row_checks": affine_image_rows,
            "passed": True}


def main():
    started = time.monotonic()
    source_data = json.loads(INPUT.read_text())
    saved_data = json.loads(SAVED.read_text())
    sources = {(row["q"], row["seed"]): row for row in source_data["rows"]}
    assert len(sources) == 6 and len(saved_data["rows"]) == 6
    rows = []
    for saved in saved_data["rows"]:
        checked = check_case(sources[(saved["q"], saved["seed"])], saved)
        rows.append(checked)
        print(f"q={checked['q']} seed={checked['seed']} score={checked['score']} "
              f"parities={checked['restrictions_and_native_parities_checked']} "
              f"exact_means={len(checked['independent_exact_section_means'])}", flush=True)
    report = {
        "status": "ALL_SIX_SAVED_NATIVE_WITNESSES_AND_REQUESTED_EXACT_MEANS_PASS",
        "sage_version": sage_version,
        "method": "Native Sage fields, polynomial Horner; affine field-valued evaluation "
                  "columns; Sage GF(2) row spaces and complete <=q image enumeration.",
        "scope": "No Algorithm H import/rerun, no new random seeds. All saved parity "
                 "equations and gain arithmetic checked. Independent means at every q16 "
                 "step and at {0,N/4,N/2,3N/4,N-t,final} for q64/q256; individual "
                 "selected Fourier weights outside those transitions are not independently recomputed.",
        "source_sha256": {INPUT.name: sha256(INPUT), SAVED.name: sha256(SAVED),
                          Path(__file__).name: sha256(Path(__file__))},
        "rows": rows,
        "checked_native_evaluations": sum(row["native_evaluations"] for row in rows),
        "checked_parities_and_gain_identities": sum(row["restrictions_and_native_parities_checked"] for row in rows),
        "independent_exact_mean_checks": sum(len(row["independent_exact_section_means"]) for row in rows),
        "independent_affine_image_row_checks": sum(row["independent_affine_image_row_checks"] for row in rows),
        "wall_seconds": time.monotonic() - started,
        "asymptotic_or_runtime_advantage_claimed": False,
    }
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"PASS: {len(rows)} cases, {report['checked_parities_and_gain_identities']} parities, "
          f"{report['independent_exact_mean_checks']} exact means; {OUTPUT}")


if __name__ == "__main__":
    main()
