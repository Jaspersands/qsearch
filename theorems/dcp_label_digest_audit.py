"""Physical DCP label-discard controls, not a new decoder or general no-go.

GRZ Theorem 1.1 supplies the coordinatewise bound. The joint-slice extension
is derived in research/DCP_LABEL_DIGEST_AUDIT.md and remains review-pending.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
from math import isqrt, log2
from pathlib import Path
from typing import Callable, Hashable
import json

import numpy as np

from research_registry import (
    ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result,
    upsert_negative_result, utc_now,
)

REPORT_PATH = Path("research/phase_workbench/dcp_label_digest_audit.json")
EXPERIMENT_ID = "EXP-DHS-DCP-LABEL-DIGEST-AUDIT"
CANDIDATE_ID = "DHS-GOWERS-SIEVE"
LITERATURE_ID = "gupte-ragavan-zhandry-dcp-digest-2026"
Digest = Callable[[tuple[int, ...]], Hashable]
REQUIRED_SCOPE = (
    "independent_uniform_fourier_labels",
    "standard_low_subset_sum_bits_measured",
    "digest_rule_fixed_before_labels_and_measurements",
    "no_other_label_dependent_workspace_or_access",
    "all_born_branches_and_failures_charged",
)


def scope_issues(contract: dict) -> list[str]:
    """These are declared premises, not an automatic circuit-access proof."""
    return [key for key in REQUIRED_SCOPE if contract.get(key) is not True]


def _integer(value: int, name: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def sqrt_upper(value: Fraction, precision: int = 96) -> Fraction:
    """Outward dyadic square-root cap, with integer-only rounding."""
    _integer(precision, "precision", 1)
    if value < 0:
        raise ValueError("negative radicand")
    scale = 1 << precision
    numerator = value.numerator * scale * scale
    floor = isqrt(numerator // value.denominator)
    if floor * floor * value.denominator != numerator:
        floor += 1
    return Fraction(floor, scale)


def _fraction(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def coordinate_bit_bound(n: int, retained_bits: tuple[int, ...]) -> Fraction:
    """T <= sum_i 2^((k_i-n)/2), for fixed coordinatewise k_i-bit digests."""
    _integer(n, "n", 1)
    for bits in retained_bits:
        _integer(bits, "retained bits")
        if bits > n:
            raise ValueError("retained bits exceed label width")
    precision = max(96, n + 32)
    return min(Fraction(1), sum(
        (count * sqrt_upper(Fraction(1, 1 << (n - bits)), precision)
         for bits, count in Counter(retained_bits).items()),
        Fraction(0),
    ))


def _digest_table(n: int, m: int, digest: Digest) -> dict[tuple[int, ...], Hashable]:
    _integer(n, "n", 1)
    _integer(m, "sample count", 1)
    if n * m > 13 or m > 7 or (1 << (n*m + 2*m)) > 2_000_000:
        raise ValueError("exhaustive physical control budget exceeded; use analytic scaling")
    table = {}
    for labels in product(range(1 << n), repeat=m):
        value = digest(labels)
        try:
            hash(value)
        except TypeError as exc:
            raise ValueError("digest outcomes must be hashable") from exc
        if value != digest(labels):
            raise ValueError("digest must be deterministic after fixing public randomness")
        table[labels] = value
    return table


def slice_fiber_profile(n: int, m: int, table: dict) -> dict:
    """Exact counts for H(y_-i,t), not the global digest alphabet size.

    The table is a finite control. Exponential enumeration is never charged
    as an efficient classical baseline or proposed quantum preprocessing.
    """
    _integer(n, "n", 1)
    _integer(m, "sample count", 1)
    modulus = 1 << n
    if len(table) != modulus**m or any(
        not isinstance(labels, tuple) or len(labels) != m
        or any(type(a) is not int or not 0 <= a < modulus for a in labels)
        for labels in table
    ):
        raise ValueError("slice profiles require the complete uniform label table")
    histograms = []
    caps = []
    max_images = []
    for i in range(m):
        slices = defaultdict(Counter)
        for labels, value in table.items():
            slices[labels[:i] + labels[i+1:]][value] += 1
        histogram = Counter(size for counts in slices.values() for size in counts.values())
        beta = sum((multiplicity * sqrt_upper(Fraction(size))
                    for size, multiplicity in histogram.items()), Fraction(0)) / modulus**m
        histograms.append(dict(sorted(histogram.items())))
        caps.append(beta)
        max_images.append(max(map(len, slices.values())))
    return {
        "fiber_size_histograms": histograms,
        "coordinate_beta_upper": [_fraction(cap) for cap in caps],
        "maximum_slice_image_sizes": max_images,
        "trace_distance_upper": _fraction(min(Fraction(1), sum(caps, Fraction(0)))),
        "bound_arithmetic": "outward dyadic square roots of exact integer fiber counts",
    }


def low_sum_slice_profile(n: int, m: int, table: dict) -> dict:
    """H(y,z) range bound weighted by the b_i=0 low-sum distribution.

    This is not the sharper fiber-size formula for z-independent summaries.
    Keeping these expressions separate prevents a false reuse of that proof.
    """
    modulus, low = 1 << n, 1 << (n-1)
    slice_fiber_profile(n, m, table)  # Validate the complete uniform table.
    if any(not isinstance(value, tuple) or len(value) != low for value in table.values()):
        raise ValueError("expected one digest outcome for each low-sum value")
    caps, image_sizes = [], []
    for i in range(m):
        slices = {}
        for labels, summaries in table.items():
            other = labels[:i]+labels[i+1:]
            sets = slices.setdefault(other, [set() for _ in range(low)])
            for z, summary in enumerate(summaries):
                sets[z].add(summary)
        beta = Fraction(0)
        max_image = 0
        for other, sets in slices.items():
            zero_counts = Counter(sum(a for j, a in enumerate(other) if (b >> j) & 1) % low
                                  for b in range(1 << (m-1)))
            weighted_size = sum(count*len(sets[z]) for z, count in zero_counts.items())
            beta += sqrt_upper(Fraction(weighted_size, (1 << (m-1))*modulus))
            max_image = max(max_image, max(map(len, sets)))
        caps.append(beta / modulus**(m-1))
        image_sizes.append(max_image)
    return {"coordinate_beta_upper": [_fraction(cap) for cap in caps],
            "maximum_slice_image_sizes": image_sizes,
            "trace_distance_upper": _fraction(min(Fraction(1), sum(caps, Fraction(0)))),
            "bound_arithmetic": "outward roots of low-sum-weighted conditional image sizes"}


def physical_observation_counts(n: int, m: int, digest: Callable, *, condition_on_z: bool = False) -> tuple[dict, int, dict]:
    """Unnormalized integer cq blocks for parity secrets 0 and 1.

    Retain b,h and the complete classical (digest,z) outcome. Low-bit
    measurement branches are NOT individually normalized or uniformly sampled.
    """
    _integer(n, "n", 1)
    _integer(m, "sample count", 1)
    if condition_on_z and n*m+n-1 > 15:
        raise ValueError("low-sum-conditioned exhaustive table budget exceeded")
    table = _digest_table(n, m, (lambda y: tuple(digest(y, z) for z in range(1 << (n-1))))
                          if condition_on_z else digest)
    modulus, assignments = 1 << n, 1 << m
    blocks = {}
    for labels, summary in table.items():
        branches = defaultdict(list)
        for b in range(assignments):
            residue = sum(a for j, a in enumerate(labels) if (b >> j) & 1) % modulus
            branches[residue % (modulus // 2)].append(2*b + residue // (modulus // 2))
        for z, indices in branches.items():
            key = (summary[z] if condition_on_z else summary, z)
            if key not in blocks:
                if (len(blocks) + 1) * (2*assignments)**2 > 2_000_000:
                    raise ValueError("physical block storage budget exceeded")
                blocks[key] = np.zeros((2*assignments, 2*assignments), dtype=np.int64)
            blocks[key][np.ix_(indices, indices)] += 1
    return blocks, assignments * modulus**m, table


def audit_digest(n: int, m: int, digest: Callable, name: str, *, condition_on_z: bool = False) -> dict:
    blocks, denominator, table = physical_observation_counts(n, m, digest, condition_on_z=condition_on_z)
    profile = (low_sum_slice_profile if condition_on_z else slice_fiber_profile)(n, m, table)
    width = 1 << (m+1)
    signs = 1 - 2*(np.arange(width) % 2)
    secret_sign = signs[:, None] * signs[None, :]
    trace_norm = lambda matrix: float(np.abs(np.linalg.eigvalsh(matrix.astype(float))).sum())
    parity_distance = sum(trace_norm(block * (1-secret_sign)) for block in blocks.values()) / (2*denominator)
    distances = []
    for i in range(m):
        b_i = (np.arange(width) >> (i+1)) & 1
        off = b_i[:, None] != b_i[None, :]
        distances.append(sum(trace_norm(block * off) for block in blocks.values()) / (2*denominator))
    beta = [
        Fraction(row["numerator"], row["denominator"]) for row in profile["coordinate_beta_upper"]
    ]
    upper = Fraction(
        profile["trace_distance_upper"]["numerator"], profile["trace_distance_upper"]["denominator"])
    exact_mass = sum(int(np.trace(block)) for block in blocks.values())
    mass_by_z = Counter()
    for (_, z), block in blocks.items():
        mass_by_z[z] += int(np.trace(block))
    assignment = np.arange(width) // 2
    same_assignment = assignment[:, None] == assignment[None, :]
    fully_dephased_equal = all(np.all(block * (1-secret_sign) * same_assignment == 0)
                              for block in blocks.values())
    checks = {
        "source_mass_exact": exact_mass == denominator,
        "fully_dephased_secrets_exactly_equal": fully_dephased_equal,
        "coordinate_bounds_hold_numerically": all(d <= float(b)/2 + 1e-11 for d, b in zip(distances, beta)),
        "parity_bound_holds_numerically": parity_distance <= float(upper) + 1e-11,
    }
    return {
        "name": name, "n": n, "samples": m, "label_tuples": len(table),
        "digest_outcomes": len({key[0] for key in blocks}), "classical_blocks": len(blocks),
        "conditioned_on_measured_low_sum": condition_on_z,
        "normalization_denominator": denominator, "z_born_mass_numerators": dict(sorted(mass_by_z.items())),
        "parity_trace_distance": parity_distance,
        "optimal_equal_prior_success": (1+parity_distance)/2,
        "single_coordinate_dephasing_distances": distances,
        "fiber_profile": profile, "checks": checks,
        "interpretation": "Exact source counts; floating trace norms. Optimal finite discrimination is not an implemented decoder.",
    }


def run_digest_audit() -> dict:
    controls = []
    for n, m in ((2, 2), (3, 2), (3, 3), (4, 2)):
        modulus = 1 << n
        families = {
            "discard-all": lambda y: 0,
            "coordinate-top-bit": lambda y, n=n: tuple(a >> (n-1) for a in y),
            "joint-sum-top-bit": lambda y, N=modulus: (sum(y) % N) // (N//2),
            "joint-full-sum": lambda y, N=modulus: sum(y) % N,
            "full-labels": lambda y: y,
            "rare-coordinate-flag": lambda y: tuple(int(a == 0) for a in y),
        }
        controls.extend(audit_digest(n, m, digest, name) for name, digest in families.items())
        controls.append(audit_digest(n, m, lambda y, z, N=modulus: ((y[0]+z*y[1]) % N)//(N//2),
                                     "low-sum-dependent-joint-bit", condition_on_z=True))
        controls.append(audit_digest(n, m, lambda y, z, N=modulus: tuple(((a+z) % N)//(N//2) for a in y),
                                     "low-sum-dependent-coordinate-bits", condition_on_z=True))
    sweeps = []
    for n in (32, 64, 128, 256, 512):
        samples = n*n
        for name, keep in (("top-third", (n+2)//3), ("lose-two-log-bits", n-2*(n.bit_length()-1))):
            cap = coordinate_bit_bound(n, (keep,)*samples)
            sweeps.append({"n": n, "samples": samples, "retained_bits_each": keep,
                           "family": name, "tv_upper": _fraction(cap),
                           "log2_tv_upper": log2(cap.numerator)-log2(cap.denominator),
                           "vacuous": cap == 1})
    failures = sum(not all(row["checks"].values()) for row in controls)
    return {
        "created_at": utc_now(), "status": "derived-joint-slice-bound-review-pending",
        "summary": "Audited physical DCP label digests and a conditional-slice extension of GRZ; no decoder, novelty or general DCP no-go claimed.",
        "source": {
            "literature_id": LITERATURE_ID, "url": "https://eprint.iacr.org/2026/1693",
            "pdf_sha256": "66757d5e7ac99b4d30a4d6e7926185c370bcbcc7362fc0ae2f85caa65410c50d",
            "inspected_lean_commit": "6de8c1dbffec10b4b44b2cae3aeadeb1cf0cfc83",
            "lean_url": "https://github.com/sragavan99/lean-ePrint-2026-1591-refutation",
            "lean_replayed_locally": False,
            "scope": "Coordinatewise theorem is prior work. The joint-slice derivation here is not covered by the inspected Lean theorem.",
        },
        "declared_scope": {key: True for key in REQUIRED_SCOPE},
        "joint_slice_formula": "T(rho_0,rho_1) <= min(1,sum_i E_{y_-i} sum_a sqrt(|{t:H(y_-i,t)=a}|)/N)",
        "low_sum_conditioned_formula": "T <= sum_i E_u sqrt(sum_z A_u(z)*K_i(u,z)/(2^(m-1)*N)); A counts low sums with b_i=0",
        "controls": controls, "scaling": sweeps,
        "headline_metrics": {"finite_control_count": len(controls), "finite_control_failure_count": failures,
                             "analytic_scaling_count": len(sweeps), "new_quantum_algorithm_count": 0},
        "claim_gate": {"finite_controls_passed": failures == 0,
                       "joint_slice_derivation_review_pending": True,
                       "general_dcp_no_go": False, "joint_digest_bits_can_be_divided_among_coordinates": False,
                       "low_sum_conditioned_digest_covered": True,
                       "arbitrary_measurement_adaptive_digest_covered": False,
                       "efficient_decoder_implemented": False, "formal_verification": False,
                       "novelty_established": False, "speedup_claim_allowed": False},
        "falsifiers_triggered": [
            "A polynomial sample budget with a fixed coordinate digest losing a linear number of bits has vanishing parity information after this prefix.",
            "A vacuous bound for a full joint sum or retained full labels is not positive evidence for an efficient decoder.",
        ],
        "next_experiments": [
            "Test a supplied full-label-sensitive uncomputation circuit against a compressed implementation with charged trace-distance error; merely storing labels does not escape a factorization.",
            "Dependence on the measured low sum alone is not an escape: use the separately derived conditional-range bound. Other measurement-dependent summaries need their own physical analysis.",
            "Develop an actual constructive coherent matching procedure; use witness-only, not uniform-fiber, requirements where justified.",
        ],
    }


def write_digest_audit_report(path: Path = REPORT_PATH, write_registry: bool = True,
                             registry_experiment_id: str = EXPERIMENT_ID,
                             registry_candidate_id: str = CANDIDATE_ID,
                             registry_result_id: str = "") -> dict:
    payload = run_digest_audit()
    payload["artifacts"] = {"report": str(path), "derivation": "research/DCP_LABEL_DIGEST_AUDIT.md"}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    if write_registry:
        upsert_experiment_result(ExperimentResultRecord(
            id=registry_result_id or f"RESULT-{registry_experiment_id}-COSET",
            experiment_id=registry_experiment_id, candidate_id=registry_candidate_id,
            created_at=payload["created_at"], status=payload["status"], summary=payload["summary"],
            metrics=payload["headline_metrics"], falsifiers_triggered=payload["falsifiers_triggered"],
            artifacts=payload["artifacts"]))
        if payload["claim_gate"]["finite_controls_passed"] is True:
            upsert_negative_result(NegativeResultRecord(
                id="DCP-FIXED-DIGEST-INFORMATION-LOSS", source=str(path),
                claim="After the standard low-subset-sum measurement, polynomially many DCP samples still reveal parity when each public label is used only through a fixed digest discarding a linear number of bits.",
                reason_invalid="The prior-work GRZ trace-distance bound m*sqrt(K/N) vanishes; the physical prefix and all Born weights are retained in controls.",
                lesson="Require actual full-label sensitivity or a justified escape from this prefix/digest scope. Joint summaries need slice profiles, not global alphabet shortcuts.",
                applies_to=[registry_candidate_id], evidence={"artifact": str(path), "literature_id": LITERATURE_ID,
                    "scope": list(REQUIRED_SCOPE), "review_status": "prior-work-bound-with-review-pending-extension"}))
    return payload
