"""Version and physical-channel controls, not a scalable DCP simulation."""

from fractions import Fraction
from hashlib import sha256
from itertools import product
from itertools import combinations
from pathlib import Path
import re

import numpy as np
from pypdf import PdfReader
import pytest

from dcp_label_digest_audit import physical_observation_counts


ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    ("eprint_2026_1591_20260811.pdf", 16,
     "e84834fb205d00e87facbcee67310b17251b496e3547874d239d8fe679efbaec"),
    ("eprint_2026_1591_20261008.pdf", 18,
     "5e827802a7cd2351ce8561f4fbd55b44df2c79aae12fa6b176bcd85eda6714ed"),
)


def _distance(a, b):
    return float(np.abs(np.linalg.eigvalsh(a - b)).sum() / 2)


def _pure_subnormalized_distance(a, b):
    p, q = float(np.vdot(a, a).real), float(np.vdot(b, b).real)
    return np.sqrt(max(0.0, (p + q)**2 - 4 * abs(np.vdot(a, b))**2)) / 2


def test_archived_algorithm_steps_are_unchanged_in_october_revision():
    blocks = []
    for filename, pages, digest in SOURCES:
        path = ROOT / "research/literature_cache" / filename
        assert sha256(path.read_bytes()).hexdigest() == digest
        reader = PdfReader(path)
        assert len(reader.pages) == pages
        text = "\n".join(page.extract_text() for page in reader.pages)
        block = text[text.index("In Step 1"):text.index("Lemma 3.")]
        block = re.sub(r"(?m)^\d+\s*$", "", block)
        blocks.append(re.sub(r"\s+", "", block))
    assert blocks[0] == blocks[1]
    assert sha256(blocks[0].encode()).hexdigest() == (
        "9345666fdb53203f2693dbcbfc4b527fb5c486827fe6e126d078f9d7b39ee8ea"
    )


@pytest.mark.parametrize("n,top,kept,width", [(3, 1, 2, 2), (4, 1, 3, 2),
                                              (4, 2, 3, 2), (5, 1, 4, 2)])
def test_rounding_crossing_bound_for_every_nonempty_block_string(n, top, kept, width):
    modulus, trunc_unit, bucket = 1 << n, 1 << (n - kept), 1 << (n - top)
    for bits in product((0, 1), repeat=width):
        bad = 0
        for labels in product(range(modulus), repeat=width):
            exact = sum(a*b for a, b in zip(labels, bits)) % modulus
            coarse = sum((a//trunc_unit)*trunc_unit*b
                         for a, b in zip(labels, bits)) % modulus
            if exact//bucket != coarse//bucket:
                bad += 1
                assert exact % bucket < width*trunc_unit
        probability = Fraction(bad, modulus**width)
        bound = min(Fraction(1), Fraction(width, 1 << (kept-top)))
        assert probability <= bound
        if not any(bits):
            assert probability == 0
        if bits == (1,)*width:
            assert probability > 0  # Rounding is not exactly lossless.


@pytest.mark.parametrize("labels", [(1, 3, 6), (7, 7, 7), (0, 0, 0), (1, 2, 4)])
@pytest.mark.parametrize("secret", [0, 1])
def test_summary_isometry_error_survives_exact_low_sum_measurement(labels, secret):
    n, kept, top, m = 3, 2, 1, len(labels)
    modulus, low, words = 1 << n, 1 << (n-1), 1 << m
    groups = ((0, 1), (2,))
    alphabet = 1 << (top*len(groups))
    dim = words*2*alphabet
    exact = np.zeros((low, dim), complex)
    rounded = np.zeros_like(exact)
    bad = 0
    for b in range(words):
        residue = sum(a*((b >> i) & 1) for i, a in enumerate(labels)) % modulus
        summaries = []
        for coarse in (False, True):
            values = tuple((a >> (n-kept)) << (n-kept) if coarse else a for a in labels)
            summaries.append(sum(
                ((sum(values[i]*((b >> i) & 1) for i in group) % modulus) >> (n-top))
                << (j*top) for j, group in enumerate(groups)))
        bad += summaries[0] != summaries[1]
        amplitude = np.exp(2j*np.pi*secret*residue/modulus)/np.sqrt(words)
        for target, summary in zip((exact, rounded), summaries):
            target[residue % low, (2*b + residue//low)*alphabet + summary] = amplitude
    p_bad = bad/words
    assert np.vdot(exact, rounded) == pytest.approx(1-p_bad)
    before = _pure_subnormalized_distance(exact.ravel(), rounded.ravel())
    after = sum(_pure_subnormalized_distance(a, b) for a, b in zip(exact, rounded))
    assert before == pytest.approx(np.sqrt(2*p_bad-p_bad*p_bad))
    assert after <= before + 1e-12
    assert sum(np.vdot(a, a).real for a in exact) == pytest.approx(1)


def test_first_zero_selection_keeps_one_joint_born_information_budget():
    # Actual small DCP ensemble, followed by an adaptive instrument, not a
    # miniature replacement for Simon's asymptotic parameter schedule.
    m = 2
    counts, denominator, _ = physical_observation_counts(3, m, lambda y: tuple(a >> 2 for a in y))
    h = np.array([[1, 1], [1, -1]], float)/np.sqrt(2)
    transform = np.kron(np.kron(h, h), np.eye(2))
    signs = (-1)**(np.arange(1 << (m+1)) % 2)
    inputs = [{key: value/denominator for key, value in counts.items()}, {}]
    inputs[1] = {key: value*np.outer(signs, signs) for key, value in inputs[0].items()}
    input_distance = sum(_distance(inputs[0][key], inputs[1][key]) for key in counts)
    outputs = []
    for state in inputs:
        branches = {}
        for key, matrix in state.items():
            rotated = transform @ matrix @ transform.T
            for outcome in range(1 << m):
                selected = next((i for i in range(m) if not (outcome >> i) & 1), None)
                branches[key, outcome, selected] = rotated[2*outcome:2*outcome+2,
                                                         2*outcome:2*outcome+2]
        outputs.append(branches)
        assert sum(np.trace(v) for v in branches.values()) == pytest.approx(1)
    joint = sum(_distance(outputs[0][key], outputs[1][key]) for key in outputs[0])
    assert joint <= input_distance + 1e-12
    accepted = [key for key in outputs[0] if key[-1] is not None]
    masses = [sum(np.trace(out[key]).real for key in accepted) for out in outputs]
    assert all(0 < p < 1 for p in masses)
    conditional = sum(_distance(outputs[0][key]/masses[0], outputs[1][key]/masses[1])
                      for key in accepted)
    assert max(masses)*conditional <= input_distance + 1e-12


@pytest.mark.parametrize("epsilon", [Fraction(1, 8), Fraction(1, 256), Fraction(1, 65536)])
@pytest.mark.parametrize("branches", [1, 4, 64])
def test_many_perfect_rare_branches_do_not_create_free_success(epsilon, branches):
    # Diagonal density matrices permit exact rational trace-distance checks.
    abort = 1-epsilon
    p = (abort,) + tuple(x for _ in range(branches) for x in (epsilon/branches, 0))
    q = (abort,) + tuple(x for _ in range(branches) for x in (0, epsilon/branches))
    distance = sum(abs(a-b) for a, b in zip(p, q))/2
    acceptance = sum(p[1:])
    conditional_distance = sum(abs(a/acceptance-b/acceptance)
                               for a, b in zip(p[1:], q[1:]))/2
    assert sum(p) == sum(q) == 1
    assert distance == acceptance == epsilon
    assert conditional_distance == 1
    assert acceptance*conditional_distance == distance
    assert 1/acceptance == 1/epsilon  # Fresh-copy expected retry cost.


def test_unequal_acceptance_preserves_the_abort_probability_and_prior():
    p = tuple(map(Fraction, ("0.8", "0.2", "0")))
    q = tuple(map(Fraction, ("0.7", "0", "0.3")))
    distance = sum(abs(a-b) for a, b in zip(p, q))/2
    accepted_distance = sum(abs(a-b) for a, b in zip(p[1:], q[1:]))/2
    masses = (sum(p[1:]), sum(q[1:]))
    assert distance == accepted_distance + abs(masses[0]-masses[1])/2
    assert masses[0]/sum(masses) == Fraction(2, 5)  # Not an equal conditional prior.
    conditional = sum(abs(a/masses[0]-b/masses[1]) for a, b in zip(p[1:], q[1:]))/2
    assert max(masses)*conditional == distance


def test_small_average_state_distance_is_not_a_uniform_labelwise_bound():
    zero, plus, minus = np.diag([1.0, 0]), np.array([1, 1])/np.sqrt(2), np.array([1, -1])/np.sqrt(2)
    rho, sigma = np.outer(plus, plus), np.outer(minus, minus)
    assert _distance(rho, sigma) == pytest.approx(1)
    alphabet = 64
    cq_average = (_distance(rho, sigma) + (alphabet-1)*_distance(zero, zero))/alphabet
    assert cq_average == pytest.approx(1/alphabet)
    assert cq_average < _distance(rho, sigma)


def test_selected_zero_groups_have_completion_collision_energy_not_path_count():
    # Reduced-parameter calibration: n=16, five width-4 groups, first four
    # selected. All compatible subset sums equal 22, never the zero fiber.
    completion_counts = {0: 1}
    for label in range(1, 17):
        previous = dict(completion_counts)
        for total, count in previous.items():
            if total+label <= 22:
                completion_counts[total+label] = completion_counts.get(total+label, 0)+count
    multiplicities = {
        v: completion_counts.get(22-sum((17+i)*((v >> i) & 1) for i in range(4)), 0)
        for v in range(16)
    }
    assert [value for value in multiplicities.values() if value] == [79, 3, 2, 2, 1]
    signed = [sum(count*(-1)**((v & outcome).bit_count())
                  for v, count in multiplicities.items()) for outcome in range(16)]
    assert min(signed) > 0  # All the conditional D branches have positive Born mass.
    assert sum(x*x for x in signed) == 16*sum(x*x for x in multiplicities.values()) == 100144
    assert 16*sum(multiplicities.values()) == 1392
    assert sum(x*x for x in signed) != 16*sum(multiplicities.values())
    # {1,4,17} and {2,3,17} are distinct compatible paths with identical B.
    assert 1+4+17 == 2+3+17 == 22
    signs = [((-1)**(outcome & 1), (-1)**(outcome & 1)) for outcome in range(16)]
    assert [signs.count(pair) for pair in ((1, 1), (1, -1), (-1, 1), (-1, -1))] == [8, 0, 0, 8]


def test_unrestricted_walsh_characters_are_the_positive_independence_control():
    for u, v in combinations(range(1, 16), 2):
        pairs = [((-1)**((u & d).bit_count()), (-1)**((v & d).bit_count())) for d in range(16)]
        assert all(pairs.count(pair) == 4 for pair in product((-1, 1), repeat=2))


def test_first_zero_selection_uses_its_conditioned_character_kernel():
    width, groups = 2, 3
    alphabet = 1 << width
    masks = list(product(range(alphabet), repeat=groups))
    for selected_count in range(1, groups+1):
        for selected in combinations(range(groups), selected_count):
            conditional = [d for d in masks if tuple(i for i, part in enumerate(d) if part == 0)
                           [:selected_count] == selected]
            assert conditional
            for character in masks:
                actual = Fraction(sum((-1)**sum((u & d).bit_count()
                                                 for u, d in zip(character, mask))
                                      for mask in conditional), len(conditional))
                expected = Fraction(1)
                for i, part in enumerate(character):
                    if i in selected:
                        continue
                    if i < selected[-1]:
                        expected *= 1 if part == 0 else Fraction(-1, alphabet-1)
                    elif part != 0:
                        expected = Fraction(0)
                assert actual == expected


def test_forgetting_accessible_labels_would_give_a_false_comparison():
    plus, minus = np.array([1, 1])/np.sqrt(2), np.array([1, -1])/np.sqrt(2)
    states = [np.outer(v, v) for v in (plus, minus)]
    dephased = np.eye(2)/2
    assert _distance(sum(states)/2, dephased) == pytest.approx(0)
    assert sum(_distance(state, dephased) for state in states)/2 == pytest.approx(.5)
    z = np.diag([1, -1])
    corrected = (states[0] + z @ states[1] @ z)/2
    assert _distance(corrected, dephased) == pytest.approx(.5)


def test_different_branchwise_comparators_cannot_be_spliced_for_free():
    count = 16
    rho = tuple(x for _ in range(count) for x in (Fraction(1, count), Fraction(0)))
    spliced = list(rho)
    for branch in range(count):
        sigma = list(rho)
        sigma[2*branch], sigma[2*branch+1] = sigma[2*branch+1], sigma[2*branch]
        assert sum(abs(a-b) for a, b in zip(rho, sigma))/2 == Fraction(1, count)
        spliced[2*branch:2*branch+2] = sigma[2*branch:2*branch+2]
    assert sum(abs(a-b) for a, b in zip(rho, spliced))/2 == 1
