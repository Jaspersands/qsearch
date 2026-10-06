import itertools
from fractions import Fraction

import pytest

from dcp_carry_packets import compile_packet
from dcp_dense_phase_transport import group_index
from dcp_physical_phase_noise import read
from dcp_partial_witness_readout import (
    PartialWitnessSelector, _full_target_source_control, _origin,
    bounded_selector_control, complete_block_resource_certificate,
    correlated_attempt_failure_bound, integer_fault_survival_lower_bound,
    legal_target_coverage_transfer, orient_measured_packet,
    partial_witness_resource_certificate, physical_finder_wrapper,
    selector_interface_gate, target_source_transform,
)


def selector_for(packet, cutoff=None):
    witnesses = {}
    Q = packet.modulus // 2
    for word in range(1 << packet.retained_qubits):
        target = packet.residual(word)
        if cutoff is None or group_index(target, Q) < cutoff:
            witnesses.setdefault(target, word)
    return PartialWitnessSelector(packet, lambda target: witnesses.get(tuple(target)))


@pytest.mark.parametrize("cutoff", [0, 1, 2, 4])
def test_complete_basis_permutation_and_every_fixed_secret_readout(cutoff):
    selector = selector_for(compile_packet([[1, 1, 2, 4]], 8), cutoff)
    row = bounded_selector_control(selector)
    assert row["full_basis_forward_inverse_checks"] == 64
    assert row["fixed_secret_QFT_controls"] == 4
    assert read(row["herald_probability"]) == Fraction(cutoff, 8)
    assert read(row["correct_readout_probability_for_every_secret"]) == Fraction(cutoff**2, 32)
    assert read(row["conditional_correct_readout_given_herald"]) == Fraction(cutoff, 4)
    assert not row["reference_finder_is_a_uniform_polynomial_algorithm"]


@pytest.mark.parametrize("output", [None, -1, 8, True, 0])
def test_invalid_witnesses_fail_closed_without_breaking_full_basis_inverse(output):
    packet = compile_packet([[1, 1, 2, 4]], 8)
    selector = PartialWitnessSelector(packet, lambda target: output)
    assert not selector.witness(1)[1]
    for word, target, flag in itertools.product(range(8), range(4), (0, 1)):
        assert selector.inverse_basis(*selector.forward_basis(word, target, flag)) == (word, target, flag)


def test_which_target_history_destroys_the_required_coherence():
    row = bounded_selector_control(selector_for(compile_packet([[1, 1, 2, 4]], 8)))
    assert read(row["correct_readout_probability_for_every_secret"]) == Fraction(1, 2)
    assert read(row["which_path_history_not_uncomputed_correct_readout_probability"]) == Fraction(1, 8)
    assert not selector_interface_gate()["obligations_satisfied_as_declared"]
    declarations = dict(deterministic_given_explicit_seed=True,
                        seed_independent_of_target_and_fault_data=True,
                        uniform_bounded_time_algorithm=True, verified_one_word_or_failure=True,
                        reversible_transcript_uncomputation=True, independent_target_coverage_proved=True)
    gate = selector_interface_gate(**declarations)
    assert gate["obligations_satisfied_as_declared"]
    assert not gate["declarations_programmatically_proven"]
    assert not gate["candidate_record_accepted"]
    declarations["reversible_transcript_uncomputation"] = False
    assert "all target-dependent finder history uncomputed" in selector_interface_gate(**declarations)["issues"]


def test_original_row_syndrome_is_not_rref_syndrome():
    packet = compile_packet([[0, 1, 3], [1, 1, 2]], 4)
    for sigma in range(4):
        origin = _origin(packet, sigma)
        actual = tuple(sum((a & 1) * (origin >> i & 1) for i, a in enumerate(row)) % 2 for row in packet.labels)
        assert actual == tuple(sigma >> j & 1 for j in range(2))
    rref_packet = compile_packet(packet.labels, 4, 1)
    rref_origin = sum(o << i for i, o in enumerate(rref_packet.origin))
    assert _origin(packet, 1) != rref_origin


@pytest.mark.parametrize("n,width,q,tables,good,images", [(1, 3, 4, 64, 56, 224), (2, 3, 4, 4096, 2688, 43008)])
def test_complete_independent_full_target_joint_source_is_a_bijection(n, width, q, tables, good, images):
    row = _full_target_source_control(n, width, q)
    assert row["complete_label_tables"] == tables
    assert row["full_binary_rank_label_tables"] == good
    assert row["parity_wrapper_domain_and_uniform_full_target_image_pairs"] == images


def test_all_measured_syndromes_are_kept_without_hidden_exponential_rejection():
    labels = ((0, 1, 3, 2), (1, 1, 2, 3))
    for syndrome in range(4):
        measured = compile_packet(labels, 8, syndrome)
        oriented = orient_measured_packet(measured)
        assert oriented.syndrome == 0
        assert oriented.kernel_rows == measured.kernel_rows
        for word in range(4):
            assert oriented.residual(word) == measured.residual(word)
    # At fixed binary labels, the orientation is a permutation of ALL higher labels.
    B = ((0, 1), (1, 1))
    for syndrome in range(4):
        images = set()
        for high in itertools.product(range(2), repeat=4):
            A = tuple(tuple(B[l][i] + 2 * high[2*l+i] for i in range(2)) for l in range(2))
            images.add(orient_measured_packet(compile_packet(A, 4, syndrome)).labels)
        assert len(images) == 16


def test_physical_partial_finder_wrapper_verifies_seeded_outputs_and_covariance():
    packet = compile_packet([[0, 1, 3, 2], [1, 1, 2, 3]], 4)
    seen_seeds = []

    def bounded_finder(A, q, target, seed):
        seen_seeds.append(seed)
        if sum(target) % 2 != seed:
            return None
        return next((word for word in range(16) if tuple(
            sum(a * (word >> i & 1) for i, a in enumerate(row)) % q for row in A) == target), None)

    for sigma, seed in itertools.product(range(4), (0, 1)):
        wrapped = physical_finder_wrapper(packet, bounded_finder, raw_syndrome=sigma, shared_seed=seed)
        for target in itertools.product(range(2), repeat=2):
            word = wrapped(target)
            if word is not None:
                assert packet.residual(word) == target
            signed, shifted, origin = target_source_transform(packet, sigma, target)
            for raw in range(16):
                y = raw ^ origin
                assert tuple(sum(a * (y >> i & 1) for i, a in enumerate(row)) % 4 for row in packet.labels) == tuple(
                    (sum(a * (raw >> i & 1) for i, a in enumerate(row)) + sum(a * (origin >> i & 1) for i, a in enumerate(original))) % 4
                    for row, original in zip(signed, packet.labels))
        assert set(seen_seeds[-4:]) == {seed}
    for invalid in (True, -1, 16, 0):
        wrapped = physical_finder_wrapper(packet, lambda *args, invalid=invalid: invalid, raw_syndrome=0, shared_seed=0)
        assert wrapped((1, 1)) is None


def test_conditional_fair_physical_fault_coins_preserve_an_ideal_component():
    selector = selector_for(compile_packet([[1, 0, 2, 4]], 8))
    accepted = [selector.witness(t)[0] for t in range(4)]
    ideal = Fraction(len(accepted)**2, 32)
    for bad_mask in range(16):
        coins = [z for z in range(16) if z & ~bad_mask == 0]
        probabilities = []
        for z in coins:
            logical = selector.packet.logical_z_mask(z)
            amplitude = sum((-1)**((word & logical).bit_count() % 2) for word in accepted)
            probabilities.append(Fraction(amplitude**2, 32))
        assert sum(probabilities) / len(coins) >= ideal / 2**bad_mask.bit_count()
    # A deterministic error has no ideal-component guarantee, even with one bad bit.
    logical = selector.packet.logical_z_mask(1 << 3)
    assert sum((-1)**((word & logical).bit_count() % 2) for word in accepted) == 0
    assert ideal / 2 > 0


@pytest.mark.parametrize("mu", [Fraction(0), Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(17, 4)])
def test_integer_fault_envelope_is_sharp_for_correlated_statuses(mu):
    floor = mu.numerator // mu.denominator
    theta = mu - floor
    exact_mix = (1-theta) / 2**floor + theta / 2**(floor+1)
    assert integer_fault_survival_lower_bound(mu) == exact_mix
    slope = -Fraction(1, 2**(floor+1))
    for b in range(12):
        assert Fraction(1, 2**b) >= exact_mix + slope*(b-mu)
    # Exactly one bad register in every packet: no all-good packet, but weight1/2.
    assert integer_fault_survival_lower_bound(1) == Fraction(1, 2)


def test_label_and_fault_anticorrelation_invalidates_multiplying_marginal_success():
    # Two equally likely source classes: ideal success1/0, fault count1/0.
    actual = Fraction(1, 2) * Fraction(1, 2)
    marginal_product = Fraction(1, 2) * integer_fault_survival_lower_bound(Fraction(1, 2))
    assert actual < marginal_product
    gate = selector_interface_gate(seed_independent_of_target_and_fault_data=False)
    assert "fresh seed independent of target and prelabel fault data" in gate["issues"]


def test_density_cost_rank_aborts_and_assumed_coverage_are_charged():
    low = partial_witness_resource_certificate(8, 33, 0, Fraction(1, 64))
    high = partial_witness_resource_certificate(8, 33, 16, Fraction(1, 64))
    assert low["original_phase_states_per_attempt"] == 264
    assert high["original_phase_states_per_attempt"] == 280
    assert read(low["ideal_correct_residue_probability_per_original_attempt_lower_bound"]) == Fraction(1, 16384)
    assert read(high["ideal_correct_residue_probability_per_original_attempt_lower_bound"]) == Fraction(1, 16384 * 65536)
    assert low["all_binary_prefixes_are_not_postselected"]
    assert not low["uniform_polynomial_witness_finder_constructed"]
    empty = partial_witness_resource_certificate(1, 2, 0, Fraction(1, 4))
    assert read(empty["ideal_correct_residue_probability_per_original_attempt_lower_bound"]) == 0


def test_legal_input_conditioning_is_global_not_per_label_or_planted():
    row = legal_target_coverage_transfer(Fraction(1, 16), 0)
    assert read(row["unconditional_verified_target_coverage_lower_bound"]) == Fraction(1, 32)
    assert not row["mean_of_per_label_legal_coverage_ratios_is_this_law"]
    assert not row["planted_target_coverage_automatically_transfers"]
    # One label has1/4 legal targets, the other4/4. Solver answers only the first.
    assert Fraction(1, 2) != Fraction(1, 5)
    # Complete first/second-moment controls for native independent uniform target.
    for n, width in ((1, 2), (2, 4)):
        q = 2
        total, first, second, legal = 0, 0, 0, 0
        for entries in itertools.product(range(q), repeat=n*width):
            A = tuple(tuple(entries[l*width:(l+1)*width]) for l in range(n))
            counts = dict.fromkeys(itertools.product(range(q), repeat=n), 0)
            for word in range(1 << width):
                target = tuple(sum(a*(word >> i & 1) for i,a in enumerate(row)) % q for row in A)
                counts[target] += 1
            for count in counts.values():
                total += 1; first += count; second += count**2; legal += bool(count)
        delta = width - n
        assert Fraction(first, total) == 2**delta
        assert Fraction(second, total) == 2**delta + 2**(2*delta) - Fraction(2**delta, q**n)
        assert Fraction(legal, total) >= read(legal_target_coverage_transfer(1, delta)["native_legal_pair_probability_lower_bound"])


def test_full_secret_completion_rank_and_fresh_wrong_candidate_test():
    # Completing the final secret bit: n+c IID rows fail rank <=2^-c.
    for n, c in ((1, 2), (2, 2)):
        width = n+c
        from dcp_carry_packets import binary_rank
        deficient = sum(binary_rank(rows, n) < n for rows in itertools.product(range(1 << n), repeat=width))
        assert Fraction(deficient, 2**(n*width)) <= Fraction(1, 2**c)
    # Root-of-unity orthogonality for EVERY fixed nonzero candidate error.
    import cmath
    import math
    for n, q in ((1, 8), (2, 4)):
        for difference in itertools.product(range(q), repeat=n):
            if not any(difference):
                continue
            p = sum((1+math.cos(2*math.pi*sum(a*d for a,d in zip(label, difference))/q))/2
                    for label in itertools.product(range(q), repeat=n)) / q**n
            assert abs(p-0.5) < 1e-12
            assert abs(sum(cmath.exp(2j*math.pi*sum(a*d for a,d in zip(label, difference))/q)
                           for label in itertools.product(range(q), repeat=n))) < 1e-10


def test_correlated_attempt_budget_does_not_assume_iid_faults_or_successes():
    row = correlated_attempt_failure_bound(Fraction(1, 8), Fraction(3, 2), 128, markov_factor=4, verification_states=32)
    assert row["maximum_faults_in_good_block"] == 12
    assert row["guaranteed_good_blocks_on_aggregate_budget_event"] == 64
    assert read(row["aggregate_budget_failure_probability_upper_bound"]) == Fraction(1, 4)
    assert not row["independence_of_fault_statuses_or_unconditional_attempt_success_assumed"]
    assert (1-Fraction(1, 8*4096))**64 <= read(row["no_correct_verified_candidate_on_budget_event_probability_upper_bound"])
    # One shared bad-status event can prevent naive amplification of marginals.
    assert Fraction(1, 2) > (1-Fraction(1, 2))**8
    for counts in itertools.product(range(5), repeat=4):
        if sum(counts) <= 8:
            assert sum(b <= 4 for b in counts) >= 2
    noiseless = correlated_attempt_failure_bound(1, 0, 128)
    assert read(noiseless["aggregate_budget_failure_probability_upper_bound"]) == 0


@pytest.mark.parametrize("n,delta", [(8, 0), (8, 16), (16, 0), (16, 16), (32, 0)])
def test_complete_block_ledger_charges_every_original_state_and_stays_conditional(n, delta):
    attempts = (1 << (40+delta))*n**4
    row = complete_block_resource_certificate(n, 4*n+1, delta, Fraction(1, n*n), attempts)
    assert row["original_states_preallocated_for_all_attempts"] == attempts*row["original_states_per_complete_attempt"]
    assert row["full_secret_failure_bound_below_one_third_as_declared"]
    assert read(row["amplification"]["total_algorithm_failure_probability_upper_bound"]) < Fraction(1, 3)
    assert read(row["amplification"]["any_wrong_full_candidate_passes_fresh_tests_upper_bound"]) <= Fraction(1, 1 << 32)
    assert row["finder_coverage_is_an_assumption_not_an_experimental_result"]
    assert not row["native_lattice_state_supply_gauge_lineage_and_gate_precision_composed"]
    assert not row["candidate_record_accepted"]


def test_domains_and_uncovered_interfaces_fail_closed():
    packet = compile_packet([[1, 1, 2, 4]], 8)
    with pytest.raises(ValueError):
        PartialWitnessSelector(compile_packet([[0, 2]], 4), lambda t: 0)
    with pytest.raises(ValueError):
        physical_finder_wrapper(compile_packet(packet.labels, 8, 1), lambda *args: 0, raw_syndrome=0, shared_seed=0)
    for target in ((4,), (-1,), (), (True,)):
        with pytest.raises(ValueError):
            target_source_transform(packet, 0, target)
    with pytest.raises(ValueError):
        _origin(packet, 2)
    with pytest.raises(ValueError):
        integer_fault_survival_lower_bound(-1)
    with pytest.raises(ValueError):
        partial_witness_resource_certificate(1, 1, 0, 1)
    with pytest.raises(ValueError):
        partial_witness_resource_certificate(1, 8, -1, 1)
    with pytest.raises(ValueError):
        partial_witness_resource_certificate(1, 8, 0, 2)
    with pytest.raises(ValueError):
        correlated_attempt_failure_bound(0, 0, 2)
    with pytest.raises(ValueError):
        correlated_attempt_failure_bound(1, 0, 2, markov_factor=1)
    with pytest.raises(ValueError):
        bounded_selector_control(selector_for(packet), maximum_logical_width=2)
