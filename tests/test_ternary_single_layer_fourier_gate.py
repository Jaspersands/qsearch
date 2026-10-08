from fractions import Fraction
from itertools import combinations,product
import json
from pathlib import Path
import subprocess

import numpy as np
import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates,native_source
from ternary_cyclic_extractor import random_even_source
from ternary_single_layer_fourier_gate import (
    MACROS,TRANSITIONS,census,native_control,permutation_moment,phase_values,population_certificate,routing_requirement,
)


def tight_source():
    return native_source([[inverse_frequency_coordinates(a,c,8)] for a,c in ((1,2),(26,52))],8)


@pytest.mark.parametrize("n,r",[(1,4),(1,16),(1,64),(2,16)])
def test_exact_support_sum_and_underfull_decay(n,r):
    row=population_certificate(n,r);M=n*r-2;D=3**M;G=3**(n*r)
    expected=2*sum(int(x["offsets"])*Fraction(x["second_moment_per_oriented_high_class"]) for x in row["support_moments"])
    assert Fraction(row["expected_phase_independent_offset_energy"])==expected
    assert Fraction(row["mean_raw_trit_advantage_upper_squared"])==2*expected/(9*D*D)
    expanded=Fraction(4,81)*(Fraction(5,9)**M-Fraction(1,3)**M)+Fraction(4,729)*(Fraction(1,3)**M-Fraction(5,27)**M)
    assert Fraction(row["mean_raw_trit_advantage_upper_squared"])==expanded
    assert G==9*D and not row["generic_quantum_lower_bound"]


def test_bound_does_not_silently_exclude_polynomial_surplus_sources():
    row=population_certificate(1,4,16)
    assert row["mean_raw_trit_advantage_upper_squared"]=="4/9"
    assert not row["polynomial_surplus_copies_excluded"]
    assert not row["earlier_noncommuting_mixing_or_word_permutation_covered"]


@pytest.mark.parametrize("r",[16,32,64])
def test_surviving_routing_requires_charged_macroscopic_multiplicity(r):
    epsilon=Fraction(1,r*r);row=routing_requirement(1,r,epsilon);D=3**(r-2);G=3**r
    assert Fraction(row["required_mean_phase_weighted_offset_energy_at_least"])==Fraction(9,2)*epsilon**2*D*D
    exact=Fraction(9*D*G,4*(D-1))*epsilon**2
    assert int(row["necessary_uniform_worst_case_offset_multiplicity_cap_at_least"])==(exact.numerator+exact.denominator-1)//exact.denominator
    assert not row["label_dependent_nonlinear_route_or_its_computation_supplied"]
    assert row["uniform_worst_case_cap_not_unproved_independent_average_cap"]
    with pytest.raises(ValueError):routing_requirement(1,r,Fraction(0))
    with pytest.raises(ValueError):routing_requirement(1,r,0.01)


def test_composite_native_unit_minors_and_full_directed_signature_pairs():
    for rows in TRANSITIONS:
        assert all(abs(a[0]*b[1]-a[1]*b[0])==1 for a,b in combinations(rows,2))
    directed=set(TRANSITIONS[0]+TRANSITIONS[1])
    for a,b in combinations(directed,2):
        determinant=a[0]*b[1]-a[1]*b[0]
        assert abs(determinant)==1 or b==tuple(-x for x in a)


def test_mixed_sign_two_coordinate_signature_minor_is_two_still_a_ring_unit():
    for q in (3,9,27):
        pairs=[((a+b)%q,(a-b)%q) for a,b in product(range(q),repeat=2)]
        assert len(set(pairs))==q*q


@pytest.mark.parametrize("q",[3,9])
def test_entire_native_prime_and_composite_source_censuses(q):
    row=census(q,2);expected=population_certificate(1,1 if q==3 else 2,2)
    assert row["entire_IID_frequency_cases"]==q**4
    assert row["actual_mean_offset_energy"]==expected["expected_phase_independent_offset_energy"]
    assert len(row["support_moments"])==2


def test_selected_native_control_saturates_envelope_not_a_population_algorithm():
    row=native_control(tight_source())
    assert row["exact_phase_independent_offset_energy"]=="50"
    assert row["every_phase_raw_advantage_squared_upper"]=="100/729"
    assert abs(row["phase_controls"][0]["physical_uniform_prior_raw_MAP_success"]-19/27)<3e-12
    assert row["selected_or_prespecified_labels_not_population_evidence"]
    for phase in row["phase_controls"]:
        assert phase["physical_advantage_squared"]<=100/729+3e-12
        assert phase["Parseval_residual"]<3e-12


@pytest.mark.parametrize("n,r,M,j,seed",[(1,6,4,0,99821),(2,3,4,1,99822)])
def test_higher_root_and_multivariate_all_secret_physical_macro_controls(n,r,M,j,seed):
    row=native_control(random_even_source(n,2*r,M,seed),j)
    assert row["complete_uniform_secret_count_calibration_only"]==3**(n*r)
    assert tuple(p["macro"] for p in row["phase_controls"])==MACROS
    for p in row["phase_controls"]:
        assert p["physical_advantage_squared"]<=float(Fraction(row["every_phase_raw_advantage_squared_upper"]))+3e-12
        assert p["Born_normalization_residual"]<3e-12 and not p["efficient_classical_decoder_supplied"]


def test_partial_block_exception_to_Taylor_is_still_inside_this_single_layer_gate():
    values=phase_values(tight_source(),0,"partial_quadratic")
    assert [values[i] for i in (0,4,8)]==[0,41,2]
    row=native_control(tight_source())
    partial=next(c for c in row["phase_controls"] if c["macro"]=="partial_quadratic")
    assert partial["physical_uniform_prior_raw_MAP_success"]<=19/27+3e-12


def test_label_free_nonlinear_routing_moment_is_checked_against_entire_source_law():
    q=3;M=3;ws=tuple(product(range(3),repeat=M));images=tuple((a,b,(c+a*b)%3) for a,b,c in ws)
    certificate=permutation_moment(q,images)
    assert Fraction(certificate["signature_bucket_square_sum"])<Fraction(certificate["identity_signature_concentration_upper"])
    inverse={w:i for i,w in enumerate(images)}
    flat=np.array(tuple(product(range(q),repeat=2*M)),dtype=int)
    incidence=np.array([[int(w[i]==d) for i in range(M) for d in (1,2)] for w in ws])
    frequencies=flat@incidence.T%q
    energy=np.zeros(len(flat),dtype=np.int64)
    for delta in ws[1:]:
        targets=[inverse[tuple((a+b)%3 for a,b in zip(w,delta))] for w in images]
        difference=(frequencies[:,targets]-frequencies)%q
        for h in (1,2):energy+=(difference==h*q//3).sum(axis=1)**2
    assert Fraction(int(energy.sum()),len(flat))==Fraction(certificate["exact_expected_offset_energy_after_permutation"])
    assert not certificate["arbitrary_label_dependent_nonlinear_permutation_covered"]


def test_any_invertible_affine_word_map_is_only_an_output_relabeling_pointwise():
    source=random_even_source(1,6,3,99825);ws=tuple(product(range(3),repeat=3));lookup={w:i for i,w in enumerate(ws)}
    A=np.array([[1,1,2],[0,1,1],[0,0,2]]);b=np.array([2,1,0]);images=(np.array(ws)@A.T+b)%3
    output_relabel=(np.array(ws)@A)%3
    for secret in (0,1,3,26):
        phase=np.array(phase_values(source,0,"word_label_coupled"))
        original=np.exp(2j*np.pi*(np.array([source.value(w)[0] for w in ws])*secret+phase)/27)/np.sqrt(27)
        permuted=np.zeros(27,dtype=complex)
        for x,image in enumerate(images):permuted[lookup[tuple(image)]]=original[x]
        original_probs=abs(np.fft.fftn(original.reshape((3,)*3),norm="ortho").ravel())**2
        permuted_probs=abs(np.fft.fftn(permuted.reshape((3,)*3),norm="ortho").ravel())**2
        assert np.max(abs(permuted_probs-np.array([original_probs[lookup[tuple(y)]] for y in output_relabel])))<3e-12


def test_domains_budgets_and_phase_policies_fail_closed():
    with pytest.raises(ValueError):population_certificate(True,4)
    with pytest.raises(ValueError):population_certificate(1,1)
    with pytest.raises(ValueError):census(9,3)
    with pytest.raises(ValueError):native_control(random_even_source(1,16,6,17))
    with pytest.raises(ValueError):phase_values(tight_source(),0,lambda secret:secret)
    with pytest.raises(ValueError):permutation_moment(9,[(0,),(0,),(1,)])


def test_independent_checker_accepts_live_report():
    root=Path(__file__).resolve().parents[1]
    result=subprocess.run(["node",str(root/"research/certificates/ternary_single_layer_fourier_gate_crosscheck.js")],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["physicalMacroLaws"]==18


@pytest.mark.parametrize("mutation",["scope","population","edge","phase","native","census","permutation","tight","score","routing"])
def test_standalone_verifier_rejects_false_counts_physics_and_claims(tmp_path,mutation):
    root=Path(__file__).resolve().parents[1]
    report=json.loads((root/"research/classical_baselines/ternary_single_layer_fourier_gate.json").read_text())
    if mutation=="scope":report["label_dependent_nonlinear_word_permutations_covered"]=True
    if mutation=="population":report["population_certificates"][0]["mean_raw_trit_advantage_upper_squared"]="0"
    if mutation=="edge":report["native_controls"][0]["offset_counts"][0]["positive_count"]+=1
    if mutation=="phase":report["native_controls"][0]["phase_controls"][2]["public_phase_numerators"][1]+=1
    if mutation=="native":report["native_controls"][0]["native_labels"][0][0][0]+=1
    if mutation=="census":report["complete_source_censuses"][1]["actual_mean_offset_energy"]="0"
    if mutation=="permutation":report["fixed_permutation_signature_controls"][1]["signature_bucket_square_sum"]="0"
    if mutation=="tight":report["tight_selected_control"]["IID_population_algorithm"]=True
    if mutation=="score":report["native_controls"][0]["phase_controls"][0]["physical_uniform_prior_raw_MAP_success"]=1
    if mutation=="routing":report["nonlinear_routing_requirements"][0]["required_mean_phase_weighted_offset_energy_at_least"]="0"
    target=tmp_path/"mutant.json";target.write_text(json.dumps(report))
    result=subprocess.run(["node",str(root/"research/certificates/ternary_single_layer_fourier_gate_crosscheck.js"),str(target)],capture_output=True,text=True)
    assert result.returncode!=0,result.stdout
