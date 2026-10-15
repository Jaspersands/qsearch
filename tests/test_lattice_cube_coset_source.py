"""Source geometry, Born weights, coherence loss and matched classical controls."""
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import subprocess

import numpy as np
import pytest

from theorems import lattice_cube_coset_source as L

B = ((10000, 1000), (9999, 1000))


def source(box=4, offsets=(1, 1)):
    return L.CubeCosetSource(B, 389, 1, 0, box, 128, offsets)


def stored():
    return json.loads(L.REPORT.read_text())


def node_check(payload):
    return subprocess.run(["node", "-e",
        "const X=require('./research/certificates/lattice_cube_coset_source_crosscheck.js');"
        "let s='';process.stdin.on('data',x=>s+=x);"
        "process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));"],
        input=json.dumps(payload), text=True, capture_output=True, cwd=L.ROOT)


def test_constructor_has_public_data_only_and_exact_negative_floors():
    s = L.CubeCosetSource(((-1,),), 7, 1, 0, 4, 4, (1,))
    assert s.lattice_point(0, (1,)) == (-7,)
    assert s.cell(0, (1,)) == (-2,)
    with pytest.raises(TypeError):
        L.CubeCosetSource(B, 389, 1, 0, 4, 128, (1, 1), shortest_vector=(1, 0))
    access = source().public_access()
    assert not access["shortest_vector_or_shift_given_to_constructor"]
    assert not access["normalized_conditional_state_inverse_available"]
    assert not access["scalable_coherent_evaluator_circuit_compiled"]


@pytest.mark.parametrize("kwargs", ({"prime": 9}, {"residue_guess": 0}, {"coordinate": 2},
    {"box": 3}, {"width": 127}, {"offsets": (0, 1)}, {"basis": ((1, 1), (2, 2))}))
def test_invalid_parameters_are_rejected(kwargs):
    args = dict(basis=B, prime=389, residue_guess=1, coordinate=0, box=4, width=128, offsets=(1, 1))
    args.update(kwargs)
    with pytest.raises(ValueError):
        L.CubeCosetSource(**args)


def test_complete_domain_Born_mass_common_shift_and_balanced_bad_colours():
    s = source()
    fibres = s.fibres_for_audit()
    report = s.audit()
    assert sum(len(f) for f in fibres.values()) == s.input_population
    assert sum(Fraction(r["Born_mass"]) for r in report["fibre_size_histogram"]) == 1
    assert report["valid_two_point_source_on_full_domain"]
    assert report["balanced_bad_basis_mixture_proved"]
    assert report["position_Fourier_label_uniformity_proved"]
    assert report["PRIVATE_AUDIT_ONLY_common_differences"][0]["difference"] == (0, -1)
    bad0, bad1 = report["PRIVATE_AUDIT_ONLY_singleton_colour_counts"]
    assert bad0 == bad1
    for fibre in fibres.values():
        assert len(fibre) <= 2
        if len(fibre) == 2:
            points = dict(fibre)
            delta = tuple(y-x for x,y in zip(points[0], points[1]))
            assert delta == (0, -1)
            assert tuple(y-x for x,y in zip(s.lattice_point(0, points[0]), s.lattice_point(1, points[1]))) == (1, 0)


@pytest.mark.parametrize("width, displacement", ((4, -3), (4, -1), (4, 0), (4, 3), (4, 4)))
def test_discrete_uniform_offsets_exactly_pay_cube_overlap(width, displacement):
    for x in range(-8, 9):
        matches = sum((x-j)//width == (x+displacement-j)//width for j in range(1, width+1))
        assert matches == max(0, width-abs(displacement))


def test_full_relevant_offset_average_matches_exact_partner_formula():
    mean = sum(Fraction(source(offsets=(j, 1)).audit()["good_two_point_Born_mass"])
               for j in range(1, 129)) / 128
    exact = L.offset_average_pair_mass(4, 128, (0, -1), (1, 0))
    assert mean == exact == Fraction(381, 512)
    # Average is not promised for every fixed offset.
    assert Fraction(source(offsets=(1, 1)).audit()["good_two_point_Born_mass"]) != exact


@pytest.mark.parametrize("n,box", ((1, 4), (2, 4), (3, 2)))
def test_signed_embedding_and_decode_have_no_carry_advice(n, box):
    for delta in product(range(1-box, box), repeat=n):
        shift = L.encode_position(delta, box) % (2*box)**n
        assert L.decode_difference(shift, n, box) == delta
    with pytest.raises(ValueError):
        L.decode_difference(box, n, box)


def test_multipoint_cells_are_not_ordinary_bad_basis_registers():
    s = L.CubeCosetSource(B, 3, 1, 0, 16, 64, (1, 1))
    report = s.audit()
    assert any(r["size"] > 2 for r in report["fibre_size_histogram"])
    assert not report["valid_two_point_source_on_full_domain"]
    assert report["bad_register_rate"] is None
    assert not report["position_Fourier_label_uniformity_proved"]
    assert not report["balanced_bad_basis_mixture_proved"]
    assert not report["multipoint_fibres_are_valid_bad_basis_registers"]


def test_known_parent_inverse_pays_conditional_probability_not_one():
    s = source()
    fibres = s.fibres_for_audit()
    states = tuple((t, a) for t in range(2) for a in product(range(s.box), repeat=s.dimension))
    D, N = s.input_population, s.phase_modulus
    fibre = next(f for f in fibres.values() if len(f) == 2)
    # Inverse clean evaluator clears the retained measured cell. Inverse
    # uniform Hadamards then act on the actual conditional input support.
    conditional = np.array([1/np.sqrt(len(fibre)) if x in fibre else 0 for x in states])
    H = np.array([[(-1)**((i&j).bit_count())/np.sqrt(D) for j in range(D)] for i in range(D)])
    recovered = H @ conditional
    assert np.isclose(abs(recovered[0])**2, len(fibre)/D)
    assert not np.isclose(abs(recovered[0])**2, 1)
    for k in (0, 1, N//2):
        # Parent amplitudes for this actual cell AND measured Fourier label.
        parent = np.array([np.exp(2j*np.pi*k*L.encode_position(a,s.box)/N)/np.sqrt(D*N) for _,a in fibre])
        branch = parent/np.linalg.norm(parent)
        assert np.isclose(abs(np.vdot(parent, branch))**2, len(fibre)/(D*N))


def test_signed_width_plan_high_bit_copy_matches_floor_for_entire_domain():
    s = source()
    plan = s.clean_arithmetic_plan()
    assert plan["initial_uniform_source_qubits"] == 5
    assert not plan["clean_reversible_arithmetic_gates_compiled"]
    for t in (0, 1):
        for a in product(range(s.box), repeat=s.dimension):
            for i, (point, cert) in enumerate(zip(s.lattice_point(t, a), plan["coordinate_width_certificates"])):
                x = point - s.offsets[i]
                bits = cert["signed_point_workspace_bits"]
                low = cert["low_remainder_bits_to_uncompute"]
                cell_bits = cert["signed_cell_output_bits"]
                assert abs(x) <= cert["absolute_point_minus_offset_bound"] < 2**(bits-1)
                encoded = x % 2**bits
                high = encoded >> low
                decoded = high - 2**cell_bits if high >= 2**(cell_bits-1) else high
                assert decoded == s.cell(t, a)[i]
    negative = L.CubeCosetSource(((-1,),), 7, 1, 0, 4, 4, (4,))
    cert = negative.clean_arithmetic_plan()["coordinate_width_certificates"][0]
    for t, a in product((0,1), range(4)):
        x = negative.lattice_point(t,(a,))[0] - 4
        high = (x % 2**cert["signed_point_workspace_bits"]) >> 2
        cb = cert["signed_cell_output_bits"]
        decoded = high - 2**cb if high >= 2**(cb-1) else high
        assert decoded == negative.cell(t,(a,))[0]


def test_position_Fourier_readout_uses_actual_preimages_and_garbage_kills_phase():
    s = source()
    fibre = next(f for f in s.fibres_for_audit().values() if len(f) == 2)
    points = dict(fibre)
    x0,x1 = (L.encode_position(points[t],s.box) for t in (0,1))
    for k in (1, 7, s.phase_modulus//2):
        amps = np.exp(2j*np.pi*k*np.array([x0,x1])/s.phase_modulus)/np.sqrt(2*s.phase_modulus)
        assert np.isclose(sum(abs(amps)**2), 1/s.phase_modulus)
        qubit = amps/np.linalg.norm(amps)
        ratio = qubit[1]/qubit[0]
        assert np.allclose(ratio, np.exp(2j*np.pi*k*(x1-x0)/s.phase_modulus))
        # The two distinct physical points are orthogonal retained garbage.
        tagged = np.zeros((2,2), dtype=complex)
        tagged[0,0], tagged[1,1] = qubit
        reduced = tagged @ tagged.conj().T
        assert np.allclose(reduced, np.eye(2)/2)
        assert abs((np.outer(qubit,qubit.conj()))[0,1]) > 0.49


def test_public_LLL_solves_control_without_truth_and_does_not_claim_general_solver():
    result = L.classical_LLL_baseline(B)
    assert np.array_equal(np.array(result["unimodular_row_transform"],dtype=object) @ np.array(B,dtype=object), result["reduced_basis_rows"])
    assert result["squared_norm"] == 1
    assert result["norm1_in_integer_lattice_proves_global_shortest"]
    assert not result["shortest_vector_truth_given_to_baseline"]
    assert not result["LLL_solves_general_unique_SVP_claimed"]


def test_reference_cap_and_typed_input_limits_are_not_source_no_go():
    with pytest.raises(ValueError, match="UNKNOWN_REFERENCE_CAP"):
        source(256).audit(cap=10)
    with pytest.raises(ValueError):
        source().cell(True,(0,0))
    with pytest.raises(ValueError):
        source().cell(0,(4,0))


def test_independent_JS_replays_every_input_of_large_source_controls():
    result = node_check(stored())
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["original_source_inputs_replayed"] == 3*131072+512


@pytest.mark.parametrize("kind", ("Born-weight", "shift", "bad-colour", "invalid-shape", "free-inverse", "source-circuit", "baseline"))
def test_independent_JS_rejects_source_and_resource_claim_tampering(kind):
    report = deepcopy(stored())
    c = report["complete_source_controls"][0]
    if kind == "Born-weight": c["fibre_size_histogram"][0]["Born_mass"] = "0"
    elif kind == "shift": c["PRIVATE_AUDIT_ONLY_common_differences"][0]["scalar_shift"] += 1
    elif kind == "bad-colour": c["PRIVATE_AUDIT_ONLY_singleton_colour_counts"][0] += 1
    elif kind == "invalid-shape": report["invalid_geometry_countercontrol"]["valid_two_point_source_on_full_domain"] = True
    elif kind == "free-inverse": report["known_parent_inverse_prices"]["conditional_normalized_coset_inverse_is_free"] = True
    elif kind == "source-circuit": report["scalable_quantum_source_circuit_compiled"] = True
    else: report["public_classical_LLL_control"]["squared_norm"] = 0
    assert node_check(report).returncode != 0
