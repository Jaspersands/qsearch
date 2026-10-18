from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
from math import log2
from pathlib import Path
from random import Random
import subprocess
import sys

import numpy as np
import pytest

from theorems.dcp_correlated_phase_block import (
    REPORT, block_record, build_report, density, finite_control,
    native_information_frontier, syndrome_circuit,
)
from theorems.dcp_disjoint_kernel_pairing import apply_evaluator
from theorems.dcp_nonlinear_fiber_pairing import phase_value

ROOT=Path(__file__).resolve().parents[1]
CHECKER=ROOT/"research/certificates/dcp_pairing_block_tradeoff_crosscheck.js"


def h2(p):
    return 0 if p in (0,1) else -p*log2(p)-(1-p)*log2(1-p)


@pytest.fixture(scope="module")
def report():
    return build_report()


def test_all_single_coefficient_additions_on_arbitrary_syndrome_and_inverse():
    for a in range(4):
        C=syndrome_circuit(((a,),))
        images=[]
        for x,z in product(range(2),range(4)):
            word=x | (z << 1)
            out=apply_evaluator(word,C)
            assert out==x | (((z+a*x)%4) << 1)
            assert apply_evaluator(out,C,inverse=True)==word
            images.append(out)
        assert len(set(images))==8
        assert C["extra_zero_work_qubits"]==0


def test_complete_vector_wire_permutations_all_inputs_random_coarse_labels():
    rng=Random(101517)
    for _ in range(8):
        A=[[rng.randrange(16) for _ in range(4)] for _ in range(2)]
        C=syndrome_circuit(A)
        images=[]
        for word in range(256):
            x=word&15
            z=word >> 4
            syndrome=phase_value(A,x,4)
            expected=x | sum((((z>>(2*l)&3)+syndrome[l])%4) << (4+2*l) for l in range(2))
            out=apply_evaluator(word,C)
            assert out==expected
            assert apply_evaluator(out,C,inverse=True)==word
            images.append(out)
        assert len(set(images))==256
        assert len(C["gates"])<=16
        assert C["retained_original_phase_qubits"]==4
        assert C["hardware_gate_export_implemented"] and not C["hardware_transpilation_executed"]


def test_actual_gate_isometry_measurement_all_outcomes_and_unknown_phases():
    A=((1,3,2),)
    C=syndrome_circuit(A)
    V=np.zeros((32,8),dtype=complex)
    for x in range(8):
        V[apply_evaluator(x,C),x]=1
    assert np.array_equal(V.conj().T@V,np.eye(8))
    for secret in range(8):
        source=density(A,3,(secret,),Fraction(3,4))
        expanded=V@source@V.conj().T
        mass=0
        for y in range(4):
            indices=list(range(8*y,8*y+8))
            block=expanded[np.ix_(indices,indices)]
            mask=np.array([phase_value(A,x,4)==(y,) for x in range(8)])
            expected=source*mask[:,None]*mask[None,:]
            assert np.allclose(block,expected)
            assert np.trace(block).real==pytest.approx(sum(mask)/8)
            mass+=np.trace(block).real
        assert mass==pytest.approx(1)


def test_product_dephasing_density_agrees_with_independent_explicit_Z_error_mixture():
    A=((1,2,5,12),)
    v=Fraction(7,8)
    p=(1-v)/2
    pure=density(A,5,(7,),1)
    mixed=np.zeros_like(pure)
    for e in range(16):
        weight=float(p**e.bit_count()*(1-p)**(4-e.bit_count()))
        signs=np.array([(-1)**((e&x).bit_count()%2) for x in range(16)])
        mixed+=weight*pure*signs[:,None]*signs[None,:]
    assert np.allclose(mixed,density(A,5,(7,),v),atol=1e-14)


def test_information_controls_match_exact_product_and_cat_logical_formulas(report):
    clean,noisy,cat,noninjective=report["finite_controls"]
    assert clean["retained_block_Holevo_bits"]==pytest.approx(2)
    v=7/8
    assert noisy["retained_block_Holevo_bits"]==pytest.approx(2*(1-h2((1-v)/2)),abs=1e-10)
    expected=(1-h2((1-v)/2))+(1-h2((1-v**2)/2))/2+(1-h2((1-v**3)/2))/2
    assert cat["retained_block_Holevo_bits"]==pytest.approx(expected,abs=1e-10)
    for control in (clean,noisy,cat):
        assert control["retained_block_Holevo_bits"]+1e-10>=control["scoped_Holevo_lower_bits"]
        assert control["injective_uniform_block_average_max_residual"]<1e-10
    assert noninjective["full_frequency_map_injective"] is False
    assert noninjective["scoped_Holevo_lower_bits"] is None


def test_retained_block_is_not_product_of_its_single_qubit_marginals():
    A=((1,2,5,12),)
    rho=density(A,5,(3,),1)
    mask=np.array([phase_value(A,x,4)==(0,) for x in range(16)])
    block=4*rho*mask[:,None]*mask[None,:]
    marginals=[]
    for i in range(4):
        marginal=np.zeros((2,2),dtype=complex)
        for x in range(16):
            if not (x >> i & 1):
                for a,b in product(range(2),repeat=2):
                    marginal[a,b]+=block[x | (a << i),x | (b << i)]
        marginals.append(marginal)
    assert all(np.allclose(m,np.eye(2)/2) for m in marginals[:3])
    product_state=np.array([[1]],dtype=complex)
    for marginal in reversed(marginals):
        product_state=np.kron(product_state,marginal)
    assert np.linalg.norm(block-product_state)>0.5
    assert np.linalg.matrix_rank(block,tol=1e-10)==1


def test_computing_quotient_and_tracing_original_address_is_secret_independent():
    A=((1,2,5,12),)
    y=0
    fiber=[x for x in range(16) if phase_value(A,x,4)==(y,)]
    outputs=[]
    for secret in range(32):
        rho=density(A,5,(secret,),Fraction(7,8))
        reduced=np.zeros((8,8),dtype=complex)
        # Trace of the original address forces x=x'; computed quotient alone
        # retains only populations, never their hidden phases.
        for x in fiber:
            g=(phase_value(A,x,32)[0]-y)//4
            reduced[g,g]+=rho[x,x]*4
        outputs.append(reduced)
    assert all(np.allclose(rho,outputs[0]) for rho in outputs)
    assert np.trace(outputs[0])==pytest.approx(1)


def test_implicit_block_schema_does_not_grant_product_source_or_inverse():
    B=block_record(((1,2,5,12),),5,(0,))
    assert B["retained_original_quantum_wires"]==4
    assert B["factored_phase_modulus_bits"]==3
    assert B["fresh_IID_product_phase_source_certified"] is False
    assert B["fiber_inverse_or_uniform_fiber_state_oracle_supplied"] is False
    assert B["compact_quantum_index_supplied"] is False
    assert B["fiber_cardinality_known_without_paid_computation"] is False
    assert B["measured_syndrome_provenance_not_certified_by_record_alone"] is True
    with pytest.raises(ValueError):
        block_record(((1,2),),3,(4,))
    with pytest.raises(ValueError):
        block_record(((8,2),),3,(0,))


def test_native_information_bound_and_entropy_inequality_with_exact_rounding():
    for n in range(2,129):
        F=native_information_frontier(n)
        assert 4*n*h2(1/(2*n))<=F["entropy_loss_bits_upper"]
        assert F["retained_block_Holevo_bits_lower_IF_injective"]==max(0,2*n-F["entropy_loss_bits_upper"])
        assert F["full_frequency_noninjectivity_probability_power_of_two_upper_exponent"]==n*n
        assert 3**(4*n)-1 < 1 << (8*n)
        assert not F["Holevo_is_accessible_information_or_efficient_decoder"]
        assert F["live_quantum_wires_after_measurement"]==4*n


def test_invalid_simulation_inputs_and_export_cap_do_not_create_proof():
    with pytest.raises(ValueError):
        density(((1,2),),3,(8,),Fraction(3,4))
    with pytest.raises(ValueError):
        density(((1,2),),3,(0,),Fraction(5,4))
    with pytest.raises(ValueError,match="UNKNOWN"):
        finite_control(((1,)*7,),3,Fraction(3,4))


def test_live_artifact_matches_finite_controls_and_checker(report):
    assert json.loads(REPORT.read_text())==report
    result=subprocess.run(["node",str(CHECKER)],capture_output=True,text=True,check=True)
    assert json.loads(result.stdout)["complete_gate_wire_checks"]>0


@pytest.mark.parametrize("field",["gates","retained_original_phase_qubits"])
def test_independent_checker_rejects_forged_gate_or_wire_export(report,tmp_path,field):
    payload=deepcopy(report)
    C=payload["finite_controls"][0]["exported_circuit"]
    if field=="gates":
        C[field].pop()
    else:
        C[field]-=1
    path=tmp_path/"forged-block.json"
    path.write_text(json.dumps(payload))
    result=subprocess.run(["node",str(CHECKER),"--block",str(path)],capture_output=True,text=True)
    assert result.returncode!=0


def test_readonly_cli_does_not_change_live_artifact():
    before=REPORT.read_bytes()
    result=subprocess.run([sys.executable,"qsearch.py","dcp-correlated-phase-block","--no-write"],cwd=ROOT,text=True,capture_output=True)
    assert result.returncode==0,result.stderr
    assert REPORT.read_bytes()==before
