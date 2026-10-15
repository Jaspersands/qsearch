"""Exact instrument, genuine quantum readout, privacy and destructive lineage."""
from copy import copy, deepcopy
from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
import subprocess

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

from theorems import lattice_cube_dcp_readout as P
from theorems.lattice_cube_coset_source import CubeCosetSource


def stored():
    return json.loads(P.REPORT.read_text())


def node_check(payload):
    return subprocess.run(["node", "-e",
        "const X=require('./research/certificates/lattice_cube_dcp_readout_crosscheck.js');"
        "let s='';process.stdin.on('data',x=>s+=x);"
        "process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));"],
        input=json.dumps(payload), text=True, capture_output=True, cwd=P.ROOT)


@pytest.fixture(scope="module")
def compiled():
    # A known public lattice calibration with NONZERO common scalar shift.
    return P.compile_phase_source(CubeCosetSource(((1,),),2,1,0,2,2,(1,)))


@pytest.fixture(scope="module")
def batch(compiled):
    return P.simulate_phase_batch(compiled,64,seed=99401,batch_tag="test-actual-source")


def fresh_backend(compiled,batch,seed=0):
    return P.OpaquePhaseBackend(audit_world(batch),compiled.source.audit(),seed=seed)


def audit_world(batch):
    # Isolated counterfactual test worlds reuse a privately captured fixture;
    # this is NOT a receiver operation or an extra state in one quantum run.
    return P.SimulatedPhaseBatch(tuple(batch.receipts),{k:v.copy() for k,v in batch._densities.items()},deepcopy(batch.metadata))


def physical_index(compiled,t,cell,k):
    value = t
    for register,x in zip(compiled.evaluator.cells,cell):
        x %= 2**len(register)
        for h,q in enumerate(register):
            value |= ((x>>h)&1) << compiled.coherent_parent.find_bit(q).index
    for h,q in enumerate(compiled.position_wires):
        value |= ((k>>h)&1) << compiled.coherent_parent.find_bit(q).index
    return value


@pytest.mark.parametrize("root", (2,4,8,16,32))
def test_dyadic_cyclotomic_relation_is_exact(root):
    c = [Fraction(0)]*root
    c[0]=c[root//2]=1
    assert P.dyadic_polynomial(c,root)==()
    c[root//2]=0
    assert P.dyadic_polynomial(c,root)==("1",)


@pytest.mark.parametrize("root", (1,3,False,64))
def test_exact_reference_caps_do_not_silently_change_root(root):
    with pytest.raises(ValueError):
        P.dyadic_polynomial([0]*max(1,int(root)),root)


def test_actual_dense_phase_parent_matches_every_amplitude_without_position_garbage(compiled):
    s=compiled.source
    actual=Statevector.from_instruction(compiled.coherent_parent).data
    expected=np.zeros_like(actual)
    for cell,fibre in s.fibres_for_audit().items():
        for k in range(s.phase_modulus):
            for t,a in fibre:
                expected[physical_index(compiled,t,cell,k)] += np.exp(2j*np.pi*k*P.encode_position(a,s.box)/s.phase_modulus)/np.sqrt(s.input_population*s.phase_modulus)
    assert np.linalg.norm(actual-expected)<1e-11
    # All original a wires are in the QFT position list; no duplicate exists.
    assert set(compiled.evaluator.input_register[1:]).issubset(compiled.position_wires)
    assert len(set(compiled.position_wires))==len(compiled.position_wires)


def test_full_phase_parent_inverse_pays_specified_cell_and_label_mass(compiled):
    parent=Statevector.from_instruction(compiled.coherent_parent).data
    conditioned=np.zeros_like(parent)
    indices=[physical_index(compiled,t,(0,),1) for t in (0,1)]
    conditioned[indices]=parent[indices]
    probability=float(np.linalg.norm(conditioned)**2)
    assert abs(probability-2/(compiled.source.input_population*compiled.source.phase_modulus))<1e-11
    conditioned/=np.sqrt(probability)
    inverse=Statevector(conditioned).evolve(compiled.coherent_parent.inverse()).data
    assert abs(abs(inverse[0])**2-probability)<1e-11
    assert abs(abs(inverse[0])**2-1)>0.1


def test_compilation_and_sampler_do_not_enumerate_private_preimages(monkeypatch,compiled):
    def forbidden(*args,**kwargs):
        raise AssertionError("preimage oracle used by compiler or emitter")
    monkeypatch.setattr(CubeCosetSource,"fibres_for_audit",forbidden)
    c=P.compile_phase_source(compiled.source)
    emitted=P.simulate_phase_batch(c,8,seed=99402,batch_tag="no-preimage-advice")
    assert len(emitted.receipts)==8


def test_complete_exact_instrument_normalizes_and_uniform_labels_are_not_assumed():
    for control in stored()["actual_lattice_source_controls"]:
        ref=control["exact_Born_reference"]
        total=sum(P.polynomial_value(row["joint_Born_probability"],ref["modulus"]) for row in ref["all_cell_label_outcomes"])
        assert abs(total-1)<1e-12
        shape=ref["full_domain_source_shape_audit"]
        assert ref["label_distribution_uniform"]==shape["position_Fourier_label_uniformity_proved"]
    invalid=stored()["actual_lattice_source_controls"][-1]["exact_Born_reference"]
    assert not invalid["label_distribution_uniform"]
    assert not invalid["full_domain_source_shape_audit"]["valid_two_point_source_on_full_domain"]


def test_good_shift_phase_and_bad_basis_states_come_from_actual_compiled_source(compiled,batch):
    ref=P.exact_born_reference(compiled.source)
    report=P.audit_simulation(compiled,ref,batch)
    assert report["exact_reference_agrees_for_every_emitted_register"]
    assert report["private_audit_max_conditional_density_error"]<P.NUMERICAL_TOLERANCE
    shift=compiled.source.audit()["PRIVATE_AUDIT_ONLY_common_differences"][0]["scalar_shift"]
    assert shift==3
    good=bad=0
    for r in batch.receipts:
        rho=batch._densities[r.id]
        if abs(rho[0,1])>0.4:
            expected=np.exp(-2j*np.pi*r.label*shift/r.modulus)/2
            assert abs(rho[0,1]-expected)<P.NUMERICAL_TOLERANCE
            good+=1
        else:
            assert np.allclose(rho,np.diag([1,0]),atol=P.NUMERICAL_TOLERANCE) or np.allclose(rho,np.diag([0,1]),atol=P.NUMERICAL_TOLERANCE)
            bad+=1
    assert good and bad


def test_whole_register_conditioned_snapshots_and_public_Z_frame_are_correct(compiled,batch):
    assert batch.metadata["conditioned_snapshot_key_and_count_checks_passed"]
    assert batch.metadata["public_Z_frame_snapshot_then_correction_used"]
    zero=[r for r in batch.receipts if r.measured_cells==((0,),) and r.label==0]
    assert zero  # These snapshots are Z-flipped before the public correction.
    for r in zero:
        assert np.allclose(batch._densities[r.id],np.ones((2,2))/2,atol=P.NUMERICAL_TOLERANCE)
    with pytest.raises(ValueError,match="SNAPSHOT_REJECTED"):
        P.simulate_phase_batch(compiled,8,seed=99403,force_conditioned_snapshots=False)


def test_public_receipts_exclude_private_phases_flags_and_density(compiled,batch):
    backend=fresh_backend(compiled,batch)
    allowed={"id","modulus","label","measured_cells","original_source_receipts","merge_depth"}
    for r in batch.receipts:
        assert set(backend.public_view(r.id))==allowed
        assert backend.public_view(r.id)==r.public_view()
    assert batch.metadata["actual_compiled_source_preparations_charged"]==len(batch.receipts)==64
    assert not batch.metadata["numerical_error_is_a_formally_certified_channel_bound"]


def test_literal_Qiskit_CNOT_instrument_matches_backend_and_consumes_parents(compiled,batch):
    backend=fresh_backend(compiled,batch)
    left,right=batch.receipts[:2]
    circuit=QuantumCircuit(2)
    circuit.cx(1,0) # np.kron(left,right) orders left as the higher qubit.
    U=Operator(circuit).data
    joint=U@np.kron(batch._densities[left.id],batch._densities[right.id])@U.conj().T
    result=backend.merge(left.id,right.id)
    assert result["status"]=="PHYSICAL_BRANCH_SAMPLED"
    b=result["branch"]
    block=joint[np.ix_((b,2+b),(b,2+b))]
    child=result["output"]
    assert np.allclose(backend._states[child["id"]],block/np.trace(block),atol=P.NUMERICAL_TOLERANCE)
    assert child["label"]==(left.label+(right.label if b==0 else -right.label))%left.modulus
    assert set(child["original_source_receipts"])=={left.id,right.id}
    with pytest.raises(ValueError): backend.public_view(left.id)
    with pytest.raises(ValueError): backend.merge(left.id,right.id)


def test_bad_basis_pairs_have_actual_deterministic_branches_not_half(compiled,batch):
    bad0=[r for r in batch.receipts if np.allclose(batch._densities[r.id],np.diag([1,0]),atol=P.NUMERICAL_TOLERANCE)]
    bad1=[r for r in batch.receipts if np.allclose(batch._densities[r.id],np.diag([0,1]),atol=P.NUMERICAL_TOLERANCE)]
    assert len(bad0)>=3 and len(bad1)>=1
    backend=fresh_backend(compiled,batch)
    same=backend.merge(bad0[0].id,bad0[1].id)
    different=backend.merge(bad0[2].id,bad1[0].id)
    assert same["branch"]==0
    assert different["branch"]==1
    for result in (same,different):
        assert np.allclose(backend._states[result["output"]["id"]],np.diag([1,0]),atol=P.NUMERICAL_TOLERANCE)


def test_no_cloning_free_retry_or_non_destructive_measurement(compiled,batch):
    backend=fresh_backend(compiled,batch)
    r=batch.receipts[0]
    with pytest.raises(ValueError): backend.merge(r.id,r.id)
    assert backend.public_view(r.id)
    outcome=backend.measure(r.id,"Z")
    assert outcome["outcome"] in (0,1)
    with pytest.raises(ValueError): backend.measure(r.id,"Z")
    with pytest.raises(ValueError): backend.public_view(r.id)


def test_disjoint_ids_do_not_override_overlapping_ancestry(compiled,batch):
    backend=fresh_backend(compiled,batch)
    left,right=batch.receipts[:2]
    backend._receipts[right.id]=replace(right,ancestors=left.ancestors)
    with pytest.raises(ValueError,match="disjoint"):
        backend.merge(left.id,right.id)
    assert backend.public_view(left.id)
    assert backend.public_view(right.id)


def test_original_receipts_cannot_impersonate_cloned_children(compiled,batch):
    altered=audit_world(batch)
    altered.receipts=(replace(altered.receipts[0],merge_depth=1),*altered.receipts[1:])
    with pytest.raises(ValueError,match="impersonate"):
        P.OpaquePhaseBackend(altered,compiled.source.audit())


def test_unresolved_rare_branch_consumes_roots_without_normalized_output(compiled,batch):
    backend=fresh_backend(compiled,batch)
    left,right=batch.receipts[:2]
    # Audit-only perturbation of private states exercises the numerical gate,
    # not a source promise or an algorithm candidate.
    backend._states[left.id]=np.diag([1.,0.])
    backend._states[right.id]=np.diag([P.NUMERICAL_TOLERANCE/10,1-P.NUMERICAL_TOLERANCE/10])
    class ForceRare:
        def random(self): return 0.0
    backend._rng=ForceRare()
    result=backend.merge(left.id,right.id)
    assert result["status"]=="UNKNOWN_RARE_BRANCH_NUMERICS"
    assert result["output"] is None
    with pytest.raises(ValueError): backend.public_view(left.id)
    with pytest.raises(ValueError): backend.public_view(right.id)


def test_independence_cost_and_source_provenance_are_required(compiled,batch):
    shape=compiled.source.audit()
    altered=audit_world(batch)
    altered.metadata["source_shots_independent_given_public_parameters"]=False
    with pytest.raises(ValueError,match="conditional-product"):
        P.OpaquePhaseBackend(altered,shape)
    altered=audit_world(batch)
    altered.metadata["actual_compiled_source_preparations_charged"]=1
    with pytest.raises(ValueError,match="charged"):
        P.OpaquePhaseBackend(altered,shape)
    wrong=CubeCosetSource(((-1,),),3,1,0,2,2,(2,)).audit()
    with pytest.raises(ValueError,match="not for the emitted"):
        P.OpaquePhaseBackend(batch,wrong)


def test_batch_and_backend_cannot_be_copied_or_reinstantiated(compiled,batch):
    world=audit_world(batch)
    backend=P.OpaquePhaseBackend(world,compiled.source.audit())
    for copier in (copy,deepcopy):
        with pytest.raises(ValueError): copier(world)
        with pytest.raises(ValueError): copier(backend)
    with pytest.raises(ValueError,match="already claimed"):
        P.OpaquePhaseBackend(world,compiled.source.audit())


def test_invalid_source_and_budget_failures_are_not_hidden_by_shape_claims():
    controls=stored()["actual_lattice_source_controls"]
    nontrivial=controls[2]
    assert nontrivial["exact_Born_reference"]["full_domain_source_shape_audit"]["valid_two_point_source_on_full_domain"]
    assert not nontrivial["compiled_source_sampling_audit"]["finite_f1_bad_register_budget_met"]
    assert not nontrivial["compiled_source_sampling_audit"]["full_Regev_growing_family_reduction_certified"]
    with pytest.raises(ValueError,match="MULTIPOINT"):
        P.OpaquePhaseBackend(None,controls[-1]["exact_Born_reference"]["full_domain_source_shape_audit"])


def test_large_compile_and_numeric_caps_are_not_algorithmic_lower_bounds():
    large=stored()["large_compiled_not_simulated_phase_source"]
    assert large["compiled_phase_parent_qubits"]==127
    assert large["position_qubits"]==18
    assert large["logical_QFT_controlled_phase_gates"]==153
    s=CubeCosetSource(((10000,1000),(9999,1000)),389,1,0,256,128,(1,1))
    with pytest.raises(ValueError,match="UNKNOWN_EXACT_READOUT_CAP"):
        P.exact_born_reference(s)
    with pytest.raises(ValueError,match="UNKNOWN_SIMULATOR_CAP"):
        P.simulate_phase_batch(P.compile_phase_source(s))


def test_independent_JS_checker_accepts_complete_source_instrument():
    result=node_check(stored())
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["actual_compiled_source_controls"]==5


@pytest.mark.parametrize("kind", ("label-probability","joint-density","uniform-invalid","numeric-density","snapshot-guard","preparation-cost","in-place","source-budget","speedup","hash"))
def test_independent_JS_checker_rejects_instrument_or_resource_tampering(kind):
    report=deepcopy(stored())
    c=report["actual_lattice_source_controls"][2]
    ref=c["exact_Born_reference"]
    sim=c["compiled_source_sampling_audit"]
    if kind=="label-probability": ref["all_label_Born_probabilities"][0]=["1"]
    elif kind=="joint-density": ref["all_cell_label_outcomes"][0]["unnormalized_colour_density"][0][0]=["1"]
    elif kind=="uniform-invalid": report["actual_lattice_source_controls"][-1]["exact_Born_reference"]["label_distribution_uniform"]=True
    elif kind=="numeric-density": next(iter(sim["PRIVATE_AUDIT_ONLY_emitted_density_matrices"].values()))[0][0][0]+=0.1
    elif kind=="snapshot-guard": sim["simulation_metadata"]["conditioned_snapshot_key_and_count_checks_passed"]=False
    elif kind=="preparation-cost": sim["simulation_metadata"]["actual_compiled_source_preparations_charged"]=1
    elif kind=="in-place": c["compiled_resources"]["copied_original_position_garbage_retained"]=True
    elif kind=="source-budget": sim["finite_f1_bad_register_budget_met"]=True
    elif kind=="speedup": report["accepted_speedup_candidate"]=True
    else: report["producer_sha256"]="0"*64
    assert node_check(report).returncode!=0
