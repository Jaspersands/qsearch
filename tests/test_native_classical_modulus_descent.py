"""Actual parent replay, lost digits and honest conditional source/noise laws."""
from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
import subprocess

import pytest

from theorems import native_classical_modulus_descent as D
from native_full_root_slice import source_data
from ternary_noise_degradation import NoisyLinearRecord


def records(q=27, n=2, pairs=12, errors=None, secret=None):
    secret = secret or tuple(range(1, n+1))
    errors = errors or (0,)*(2*pairs)
    return tuple(NoisyLinearRecord(tuple((7*j+5*i+j*i) % q for i in range(n)),
        (sum(((7*j+5*i+j*i) % q)*secret[i] for i in range(n))+errors[j]) % q, q, f"source-{j}")
        for j in range(2*pairs))


@pytest.mark.parametrize("x", range(-40, 41))
def test_signed_exact_rounding_is_odd_nearest_and_modulus_equivariant(x):
    y = D.nearest_third(x)
    assert abs(3*y-x) <= 1
    assert D.nearest_third(-x) == -y
    for q in (9, 27, 3**64):
        assert D.nearest_third(x+q) == y+q//3


@pytest.mark.parametrize("q", (9, 27, 3**64))
def test_divisible_actual_labels_and_response_formula_without_secret_access(q):
    raw = records(q=q, errors=tuple((-1)**j*(j % 4) for j in range(24)))
    output, cost = D.descend(D.originals(raw))
    assert cost["output_pairs"] == 4 and cost["original_ancestors_paid_once"] == 24
    secret = (1, 2)
    for p in output:
        rowweights, expected = D.branch_map(tuple(s.labels for s in p.parents), p.direction, q)
        assert p.labels == expected
        for z, row in enumerate(rowweights):
            original_indices = [int(x.split("-")[1]) for s in p.parents for x in s.original_ids]
            delta_error = sum(b*((-1)**i*(i % 4)) for b, i in zip((b for w in row for b in w), original_indices))
            assert p.values[z] == (sum(a*s for a, s in zip(p.labels[z], secret))+D.nearest_third(delta_error)) % (q//3)
        assert not p.record()["pair_errors_assumed_independent"]


@pytest.mark.parametrize("q,slopes", product((9, 27, 81), ((0, 0), (1, 2), (1, 1))))
def test_exact_original_source_distribution_distinguishes_conditioning(q, slopes):
    c = D.source_law_control(q, slopes)
    assert c["conditional_on_slopes_outputs"] == (q//3)**2
    assert c["conditional_on_slopes_multiplicities"] == [3]
    assert c["conditional_on_all_low_labels_outputs"] == (q//3)**2//3
    assert c["conditional_on_all_low_labels_multiplicities"] == [3]


def test_direction_uses_only_low_slopes_not_other_low_labels_higher_digits_or_values():
    labels = (((1, 2), (0, 0)), ((2, 1), (2, 2)), ((1, 0), (2, 1)))
    v = D.low_direction(labels, 27)
    changed = tuple((tuple((a[i]+(i+1)) % 27 for i in range(2)),
                     tuple((c[i]-(i+1)+9) % 27 for i in range(2))) for a, c in labels)
    assert D.low_direction(changed, 27) == v
    raw = records()
    changed_raw = tuple(replace(s, value=(s.value+7) % s.modulus) for s in raw)
    first, _ = D.descend(D.originals(raw));second, _ = D.descend(D.originals(changed_raw))
    assert [p.direction for p in first] == [p.direction for p in second]
    assert [p.labels for p in first] == [p.labels for p in second]


def test_original_lineage_is_preserved_and_reuse_or_forged_receipts_rejected():
    first, _ = D.descend(D.originals(records(pairs=10)))
    assert len(first) == 3
    second, cost = D.descend(first)
    assert len(second) == 1 and second[0].level == 2
    assert len(second[0].original_ids) == 18 and cost["original_ancestors_paid_once"] == 18
    with pytest.raises(ValueError, match="ancestors"):
        D.descend((first[0], first[0], first[2]))
    with pytest.raises(ValueError, match="replay"):
        replace(first[0], values=tuple((v+1) % 9 for v in first[0].values))
    with pytest.raises(ValueError, match="selection"):
        replace(first[0], direction=tuple(v*2 % 3 for v in first[0].direction))
    with pytest.raises(ValueError, match="actual original"):
        D.OriginalPair(first[0], first[1])


def test_tails_zero_outputs_and_root_endpoint_are_honestly_recorded():
    output, cost = D.descend(D.originals(records(pairs=10)))
    assert cost["unused_original_source_ids"] == ("source-18", "source-19")
    assert len(output) == 3
    empty, cost = D.descend(D.originals(records(pairs=2)))
    assert not empty and cost["output_pairs"] == 0 and len(cost["unused_original_source_ids"]) == 4
    with pytest.raises(ValueError, match="below"):
        D.descend(D.originals(records(q=3)))


@pytest.mark.parametrize("q,levels", ((9, 1), (27, 1), (27, 2), (81, 3)))
def test_all_quotient_aliases_have_identical_final_observations_even_with_noise(q, levels):
    secret = (1, 2);M = 3**levels
    errors = tuple((i*13) % 17-8 for i in range(2*M))
    outputs = []
    parent_hashes = []
    remaining = q//3**levels
    for h in product(range(3**levels), repeat=2):
        other = tuple((s+remaining*b) % q for s, b in zip(secret, h))
        pairs = D.originals(records(q, pairs=M, errors=errors, secret=other))
        for _ in range(levels): pairs, _ = D.descend(pairs)
        outputs.append(tuple(p.observation() for p in pairs))
        parent_hashes.append(D.digest(pairs[0].record()))
    assert all(o == outputs[0] for o in outputs)
    assert len(set(parent_hashes)) > 1  # Receipts are not safe compressed-only inputs.


def test_reconstruction_fixture_never_enters_transformation_and_large_root_is_exact():
    c = D.control(3, 8, 64, True, 94003, 2)
    assert c["original_values_verified"] and all(a["final_observations_equal"] for a in c["alias_replays"])
    assert not c["secret_or_errors_read_by_transformation"]
    assert Fraction(c["full_secret_bound_for_compressed_only_receiver"]["alias_only_full_secret_success_upper"]) == Fraction(1, 3**6)


@pytest.mark.parametrize("direction", ((1,), (2,), (1, 2), (2, 1, 1)))
def test_exact_noise_law_is_correlated_and_respects_true_moment_budget(direction):
    law = D.joint_noise_law(direction, ((-1, "1/3"), (0, "1/3"), (1, "1/3")), 81)
    pmf = {tuple(x["errors"]): Fraction(x["probability"]) for x in law["law"]}
    assert sum(pmf.values()) == 1
    assert law["pair_max_atom"] == str(max(pmf.values()))
    marginals = [{a: sum(p for xy, p in pmf.items() if xy[z] == a) for a in {xy[z] for xy in pmf}} for z in (0, 1)]
    assert any(pmf.get((a, b), 0) != p*t for a, p in marginals[0].items() for b, t in marginals[1].items())
    budget = D.noise_ledger(81, len(direction), "2/3", True)
    def centered(e): return (e+13) % 27-13
    for z in (0, 1):
        second = sum(p*centered(e[z])**2 for e, p in pmf.items())
        assert second <= Fraction(budget["rounded_output_marginal_second_moment_upper"])


def test_recursive_noise_budget_does_not_reuse_original_scalar_independence():
    first = D.noise_ledger(81, 3, 1, True);recursive = D.noise_ledger(81, 3, 1, False)
    assert Fraction(recursive["rounded_output_marginal_second_moment_upper"]) > Fraction(first["rounded_output_marginal_second_moment_upper"])
    assert not recursive["moments_infer_maximum_noise_atom"]
    capped = D.joint_noise_law((1, 1, 1), ((-1, "1/2"), (1, "1/2")), 27, 1)
    assert capped["assignments_evaluated"] == 0 and capped["pair_max_atom"] is None


def test_covariance_budget_does_not_silently_assume_identical_scalar_variances():
    # a is a random sign and c=0: Cov(c-2a,-c-a)=2, not the IID formula1.
    branch_pairs = [(-2*a, -a) for a in (-1, 1)]
    covariance = sum(x*y for x, y in branch_pairs)/2
    assert covariance == 2
    ledger = D.noise_ledger(27, 1, 1, True)
    assert Fraction(ledger["within_pair_covariance_before_rounding_upper_if_original_independent"]) >= covariance


def test_moment_upper_does_not_imply_an_atom_upper_or_recovery_feasibility():
    pointmass = D.joint_noise_law((1,), ((0, 1),), 27)
    diffuse = D.joint_noise_law((1,), tuple((e, "1/3") for e in (-1, 0, 1)), 27)
    assert pointmass["pair_max_atom"] == "1"
    assert Fraction(diffuse["pair_max_atom"]) < 1
    # Both obey the same scalar V<=1 upper bound.
    assert not D.noise_ledger(27, 1, 1, True)["moments_infer_maximum_noise_atom"]


def test_guessing_bound_matches_exact_finite_MAP_upper_for_declared_pair_noise():
    q, n = 3, 3
    labels = ((1, 0, 1), (0, 1, 1))
    law = D.joint_noise_law((1,), tuple((e, "1/3") for e in (-1, 0, 1)), 9)
    noise = {tuple(e["errors"]): Fraction(e["probability"]) for e in law["law"]}
    successes = Fraction(0)
    for y in product(range(q), repeat=2):
        successes += max(noise.get(tuple((b-sum(a*x for a, x in zip(row, secret))) % q for b, row in zip(y, labels)), 0)
                         for secret in product(range(q), repeat=n))/q**n
    b = D.guessing_bound(9, n, 1, 1, law["pair_max_atom"])
    assert successes/3**n <= Fraction(b["full_original_secret_guessing_success_upper"])
    assert Fraction(b["full_original_secret_guessing_success_upper"]) <= Fraction(1, 27)
    no_atom = D.guessing_bound(27, 8, 2, 100000)
    assert no_atom["true_conditional_pair_max_atom_upper"] is None
    assert Fraction(no_atom["full_original_secret_guessing_success_upper"]) == Fraction(1, 3**16)
    assert "value-dependent hashes/receipts" in no_atom["excluded_inputs"]
    empty = D.guessing_bound(27, 8, 2, 0)
    assert Fraction(empty["full_original_secret_guessing_success_upper"]) == Fraction(1, 27**8)
    assert not empty["independent_final_noise_pairs_given_labels_required_for_atom_bound"]


@pytest.mark.parametrize("bad", ("direction", "kernel", "shape", "modulus", "empty", "law", "atom", "level", "bool"))
def test_invalid_inputs_cannot_enter_a_claim_ledger(bad):
    with pytest.raises(ValueError):
        if bad == "direction": D.branch_map((((1,), (0,)),), (True,), 9)
        elif bad == "kernel": D.branch_map((((1,), (0,)),), (1,), 9)
        elif bad == "shape": D.low_direction((((1,), (0,)),), 9)
        elif bad == "modulus": D.guessing_bound(10, 1, 1, 1)
        elif bad == "empty": D.originals(())
        elif bad == "law": D.joint_noise_law((1,), ((0, "1/3"),), 9)
        elif bad == "atom": D.guessing_bound(9, 1, 1, 1, "1/10")
        elif bad == "level": D.guessing_bound(9, 1, 2, 1)
        elif bad == "bool": D.nearest_third(True)


@pytest.mark.parametrize("q", (9, 27, 3**64))
def test_retained_original_bank_classically_restores_top_digit_given_correct_lower(q):
    raw, mask, truth, errors = source_data(2, D.root_digits(q), 12, True, 95001)
    original = tuple((a-b) % q for a, b in zip(truth, mask))
    result = D.lift_original_top_digit(raw, tuple(a % (q//3) for a in original))
    assert result["recovered_secret"] == original
    assert result["original_records_read"] == 24
    assert not result["known_lower_correctness_established"]
    assert not result["rounding_consistency_proves_lower_input_or_noise_promise"]


def test_original_bank_lift_fails_explicitly_on_low_rank_or_bad_rounding_equations():
    raw = records(q=27)
    constant = tuple(replace(s, label=(0, 0)) for s in raw)
    rankless = D.lift_original_top_digit(constant, (1, 2))
    assert rankless["status"] == "ORIGINAL_LOW_LABEL_RANK_INSUFFICIENT" and rankless["recovered_secret"] is None
    raw, mask, truth, _ = source_data(2, 3, 12, False, 95002)
    lower = tuple((a-b) % 9 for a, b in zip(truth, mask))
    good = D.lift_original_top_digit(raw, lower)
    index = next(j for j in range(len(raw)) if j not in good["label_only_basis_rows"])
    changed = list(raw);changed[index] = replace(raw[index], value=(raw[index].value+9) % 27)
    bad = D.lift_original_top_digit(changed, lower)
    assert bad["status"] == "INCONSISTENT_ROUNDED_ORIGINAL_EQUATIONS" and bad["recovered_secret"] is None


def test_correlated_label_aligned_errors_can_forge_a_wrong_consistent_top_lift():
    raw, mask, truth, _ = source_data(2, 3, 12, False, 95003)
    original = tuple((a-b) % 27 for a, b in zip(truth, mask))
    changed = tuple(replace(s, value=(s.value+9*s.label[0]) % 27) for s in raw)
    result = D.lift_original_top_digit(changed, tuple(a % 9 for a in original))
    assert result["status"] == "CONDITIONAL_ORIGINAL_BANK_TOP_DIGIT_LIFT"
    assert result["recovered_secret"] != original
    assert not result["rounding_consistency_proves_lower_input_or_noise_promise"]


def test_original_lift_scaling_budget_charges_rank_without_enormous_denominators():
    for n in (8, 32, 64, 128):
        q = 3**n;m = 2*(n+1)**3;V = Fraction(q*q, 3*n**6)+Fraction(1, 2)
        L = D.original_lift_ledger(n, q, m, V)
        assert Fraction(L["rank_failure_upper_used_in_budget"]) == Fraction(1, 3**64)
        assert Fraction(L["conditional_rounding_failure_union_upper"]) < 1
        assert L["known_lower_correctness_is_an_external_premise"]


def test_fixed_disjoint_block_full_depth_needs_real_original_samples_not_repreparation():
    for n in (8, 32, 64, 128):
        row = D.scaling(n, n, (n+1)**3, 3)
        assert row["original_pairs_required_for_one_terminal_pair_under_this_policy"] == str((n+1)**(n-1))
        assert row["terminal_pairs_available_under_same_bank_full_depth_policy"] == 0
        assert not row["this_fixed_policy_resource_recurrence_is_a_universal_receiver_lower_bound"]


@pytest.mark.parametrize("bad", ((27,), (-1, 0), (True, 0), (9, 0)))
def test_top_lift_never_invents_or_canonically_wraps_an_invalid_known_lower(bad):
    with pytest.raises(ValueError, match="lower"):
        D.lift_original_top_digit(records(), bad)


def test_live_artifact_independent_checker_and_scope():
    path = D.REPORT
    report = json.loads(path.read_text())
    assert report["producer_sha256"] == D.hashlib.sha256(D.Path(D.__file__).read_bytes()).hexdigest()
    assert not report["accepted_speedup_candidate"] and not report["new_active_negative_result_created"]
    checked = subprocess.run(["node", "research/certificates/native_classical_modulus_descent_crosscheck.js"], cwd=D.ROOT, capture_output=True, text=True, check=True)
    assert json.loads(checked.stdout)["verified"]


@pytest.mark.parametrize("tamper", ("response", "parent", "alias", "noise", "scope", "lower"))
def test_independent_checker_rejects_modified_evidence_or_inflated_claims(tamper):
    report = json.loads(D.REPORT.read_text())
    c = report["original_data_controls"][0]
    if tamper == "response": c["histories"][0]["outputs"][0]["values"][0] += 1
    elif tamper == "parent": c["histories"][0]["outputs"][0]["parent_record_sha256"][0] = "0"*64
    elif tamper == "alias": c["full_secret_bound_for_compressed_only_receiver"]["excluded_inputs"] = []
    elif tamper == "noise": report["declared_noise_controls"][0]["pair_max_atom"] = "1"
    elif tamper == "scope": report["accepted_speedup_candidate"] = True
    elif tamper == "lower": c["conditional_original_bank_lift"]["known_lower_correctness_established"] = True
    result = subprocess.run(["node", "-e", "require('./research/certificates/native_classical_modulus_descent_crosscheck.js').verify(JSON.parse(require('fs').readFileSync(0,'utf8')))"],
        input=json.dumps(report), cwd=D.ROOT, capture_output=True, text=True)
    assert result.returncode != 0
