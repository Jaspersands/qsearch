"""Quick regression controls for research/audits/reviews/2026-11-05-rees-receiver-general-gh.md.

(A) the general-kappa witness circuit against an independent reference (exhaustive at
p = 7, kappa = 3, a = 1), a mutant that must be detected, the static footprint scan;
(B) the class-general structural checks of TerminalSampleK on two small configurations
and the refusal at a prime of E_2(4). AI-written, pending human review. Imports the
theorems/ modules read-only.
"""
import importlib.util
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
D = ROOT/"research/audits/reviews/2026-11-05-rees-receiver-general-gh"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(D))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, D/f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def ktc():
    return _load("kappa_trace_check")


@pytest.fixture(scope="module")
def gsc():
    return _load("gh_structure_check")


def test_kappa3_trace_exhaustive_p7(ktc):
    from theorems.rees_coherent_sde_k2 import all_inputs
    r = ktc.trace_check(7, 1, 3, all_inputs(7, 1), label="test")
    assert r["all_pass"] and r["inputs"] == 343


def test_kappa3_beta_mutant_detected(ktc):
    from theorems.rees_coherent_sde_k2 import all_inputs
    from theorems.rees_coherent_sde_kappa import CoherentSDEKappa
    base = CoherentSDEKappa(7, 1, 3)
    m = {"beta": (0, (base.beta[1]+1) % 7, base.beta[2])}
    r = ktc.trace_check(7, 1, 3, all_inputs(7, 1), mutate=m, ref=ktc.Ref(7, 3), label="mutant")
    assert not r["all_pass"]


def test_kappa3_static_scan(ktc):
    s = ktc.static_scan(7, 1, 3)
    for k in ("S1_F_touches_no_S_wire", "S2_C_touches_S_only_by_M_add_scaled_coeff1",
              "S3_no_macro_target_aliases_an_operand", "S4_labels_never_target_in_flattened_U"):
        assert s[k] is True, k


@pytest.mark.parametrize("name", ["heis_f3", "n4_f5"])
def test_terminal_sample_structure(gsc, name):
    r = gsc.check_config(name)
    assert r["refused"] is None
    assert r["D1_labels_control_only_after_qft_dg"] and r["D1_oracle_outputs_written_once_never_touched"]
    assert all(r["S5_structure"].values())
    for d, row in r["D2c_blocks"].items():
        assert row["occurrences"] == row["expected"]
        assert row["all_equal_remap_of_block_prog_injective"] and row["roles_ok"]
        assert row["U_equals_remap_of_sde_prog_injective"]
    for d, row in r["D2b_blocks"].items():
        bs = row["block_structure"]
        assert bs["sde_never_writes_labels_or_Q_or_children"] and bs["child_merges_local_footprint"]
        assert row["prove_controlled_merge"]["proved"] and row["children_equal_child0_under_renaming"]
    for d, row in r["SIM"].items():
        assert row.get("passed", True) and row.get("witness_equals_canonical", True)


def test_refusal_in_E2_4(gsc):
    r = gsc.check_config("n5_f5")
    assert r["refused"] and "E_2(4)" in r["refused"]
