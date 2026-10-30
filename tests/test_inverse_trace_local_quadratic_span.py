from copy import deepcopy

import pytest

from theorems.inverse_trace_algebraic_audit import quadratic_lift
from theorems.inverse_trace_local_quadratic_span import (
    known_relation_rows, span_certificate, verify_span_certificate,
)


@pytest.mark.parametrize("bits,target,relations,graph", [(7, 1, 49, 57), (11, 0, 76, 178),
                                                       (11, 1, 77, 177), (17, 0, 118, 478),
                                                       (17, 1, 119, 477)])
def test_native_field_local_span_certificates(bits, target, relations, graph):
    report = span_certificate(bits, target)
    assert report["complete_local_quadratic_span"]
    assert verify_span_certificate(report)
    assert report["known_relation_rank"] == relations
    assert report["true_graph_lift_rank"] == graph
    assert not report["field_enumerated"] and not report["native_instance_resampled"]
    assert not report["native_solver"] and not report["all_degrees_covered"]
    rows = known_relation_rows(bits, target)
    assert all((row & quadratic_lift(bits, x, y)).bit_count() % 2 == 0
               for x, y in report["selected_true_graph_points"] for row in rows)


@pytest.mark.parametrize("bits,target,samples", [(5, 0, 160), (5, 1, 160), (7, 0, 224),
                                                (17, 1, 0), (17, 1, 16)])
def test_unsaturated_samples_do_not_claim_extra_relations(bits, target, samples):
    report = span_certificate(bits, target, samples=samples)
    assert not report["complete_local_quadratic_span"]
    assert report["status"] == "UNKNOWN_LOCAL_SPAN"
    assert not verify_span_certificate(report)
    assert "additional_relations_exist" not in report


@pytest.mark.parametrize("fault", ["point", "modulus", "rank", "digest", "omit", "duplicate", "flag"])
def test_span_certificate_rejects_tampering(fault):
    report = deepcopy(span_certificate(7))
    assert verify_span_certificate(report)
    if fault == "point":
        report["selected_true_graph_points"][0][0] ^= 1
    elif fault == "modulus":
        report["field_modulus_coefficients"][0] ^= 1
    elif fault == "rank":
        report["true_graph_lift_rank"] += 1
    elif fault == "digest":
        report["relation_rows_sha256"] = "invalid"
    elif fault == "omit":
        report["selected_true_graph_points"].pop()
    elif fault == "duplicate":
        report["selected_true_graph_points"].append(report["selected_true_graph_points"][0])
    else:
        report["complete_local_quadratic_span"] = False
    assert not verify_span_certificate(report)
