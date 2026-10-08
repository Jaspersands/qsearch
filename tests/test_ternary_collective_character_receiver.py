from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import subprocess

import numpy as np
import pytest

from ternary_collective_character_receiver import (
    DERIVATION, REPORT, all_outcome_likelihood_reference, character_corrections, instrument_replay,
    joint_fiber_reference, scaling_ledger,
)
from ternary_ridge_cancellation import cancel, native_cohort


@dataclass(frozen=True)
class TableCalibration:
    """A finite instrument control, never a candidate or supplied source."""
    table: tuple
    phase_digits: int

    @property
    def width(self): return 1

    @property
    def components(self): return len(self.table[0])

    @property
    def modulus(self): return 3**self.phase_digits

    def value(self,z): return self.table[z[0]]


def control(values,r=2):
    return TableCalibration(tuple((x,) for x in values),r)


@pytest.mark.parametrize("values",[(0,1,2),(0,2,4),(0,1,7),(0,0,0)])
def test_direct_erasure_joint_success_is_exactly_inverse_secret_count(values):
    phases=(control(values),);c=character_corrections(phases);f=joint_fiber_reference(phases)
    for s in range(9):
        replay=instrument_replay(f,c,(s,))
        assert replay["branches"][0]["joint_correct_probability"]==pytest.approx(1/9)
    assert Fraction(f["zero_erasure_joint_correct_probability"])==Fraction(1,9)
    assert Fraction(f["zero_erasure_conditional_correct_probability"])==1/(1+Fraction(f["frequency_chi_square_from_uniform"]))


def test_nonzero_uncorrected_erasure_cannot_be_called_success():
    phase=control((0,1,2));D=3;q=9;s=8
    for t in (1,2):
        amplitude=sum(np.exp(-2j*math.pi*t*x/3) for x in range(3))/math.sqrt(q)/D
        assert abs(amplitude)**2<1e-25


@pytest.mark.parametrize("r,seed",[(1,89000),(2,89000),(3,89003),(5,89006)])
def test_true_native_nonzero_character_is_compiled_and_corrected(r,seed):
    # Seeds are fixed structural controls, not population success estimates.
    programs=native_cohort(1,1,r,seed);phase,_=cancel(programs,((2,),))
    c=character_corrections((phase,));f=joint_fiber_reference((phase,))
    assert c["complete_correction_image_certified"]
    assert c["word_character_image_rank"]==1
    assert Fraction(c["joint_correct_and_accepted_probability"])==Fraction(3,3**r)
    assert c["full_root_secret_corrections"]==[(3**(r-1),)]
    for s in (0,3**r-1):
        replay=instrument_replay(f,c,(s,))
        assert any(any(x["erasure_word"]) for x in replay["branches"])
        assert all(x["joint_correct_probability"]==pytest.approx(1/3**r) for x in replay["branches"])


def test_arbitrary_single_block_root_preserving_phase_does_not_grant_character():
    c=character_corrections((control((0,1,7)),))
    assert c["complete_correction_image_certified"]
    assert c["all_exact_rescuable_erasure_outcomes"]=="1"
    assert not c["approximate_or_noncharacter_outcome_corrections_ruled_out"]


def test_full_span_is_checked_instead_of_assumed_and_zero_image_is_not_counted_twice():
    c=character_corrections((control((0,3,6)),))
    assert not c["complete_correction_image_certified"]
    assert c["all_exact_rescuable_erasure_outcomes"] is None
    assert c["order_three_secret_correction_basis"]
    assert not c["word_character_basis"] and not c["full_root_secret_corrections"]
    assert c["implemented_rescuable_erasure_outcomes"]=="1"


def test_joint_higher_secret_is_shared_and_not_refreshed_per_program():
    phases=(control((0,1,2)),control((0,2,4)))
    singles=[joint_fiber_reference((p,))["ideal_lowest_digit_success_shared_high_secret"] for p in phases]
    assert singles==pytest.approx([1/3,1/3])
    f=joint_fiber_reference(phases)
    assert f["ideal_lowest_digit_success_shared_high_secret"]==pytest.approx((15+4*math.sqrt(2))/27)
    assert f["ideal_lowest_digit_success_shared_high_secret"]>0.7
    assert not f["independent_high_secret_twirl_per_program_used"]


def test_pairwise_collision_source_law_suffices_for_pgm_information_bound():
    # Complete independent random-frequency calibration, not physical IID proof.
    q=3;D=3;G=3;chi=[];fail=[]
    for a,b in product(range(q),repeat=2):
        f=joint_fiber_reference((control((0,a,b),1),))
        chi.append(Fraction(f["frequency_chi_square_from_uniform"]))
        fail.append(1-f["ideal_full_secret_PGM_success"])
        assert fail[-1]<=float(chi[-1])+1e-12
    assert sum(chi)/len(chi)==Fraction(G-1,D)
    assert sum(fail)/len(fail)<=float(Fraction(G-1,D))


def test_exact_character_image_equals_exhaustive_full_ring_search():
    phases=(control((0,1,2)),control((0,2,4)))
    c=character_corrections(phases);f=joint_fiber_reference(phases);found={}
    for delta in range(9):
        t=(delta*1 % 9//3,delta*2 % 9//3)
        if all((delta*v[0]-3*sum(a*b for a,b in zip(t,z))) % 9==0
               for z,v in zip(f["joint_words"],f["joint_frequencies"])):
            found[t]=delta
    assert len(found)==int(c["all_exact_rescuable_erasure_outcomes"])==3
    for t,delta in zip(c["word_character_basis"],c["full_root_secret_corrections"]):
        assert found[t]==delta[0]


@pytest.mark.parametrize("n,d,r,B",[(8,2,3,15),(32,3,4,45),(128,5,5,130),(256,6,8,345)])
def test_polynomial_batch_can_have_information_but_exponential_readout_cost(n,d,r,B):
    x=scaling_ledger(n,d,r,B);G=3**(n*r);D=3**(d*B)
    assert Fraction(x["mean_ideal_PGM_failure_upper_under_IID_source"])==min(Fraction(1),Fraction(G-1,D))
    assert Fraction(x["best_exact_character_feedforward_joint_success_ceiling"])==Fraction(1,3**(n*(r-1)))
    assert int(x["uncorrected_expected_fresh_original_inputs_per_correct_readout"])==int(x["provided_original_inputs_per_attempt"])*G
    assert not x["population_bound_is_fixed_instance_certificate"]
    assert not x["ideal_PGM_is_an_implemented_efficient_receiver"]


def test_local_and_joint_reference_caps_do_not_return_partial_results():
    p=control((0,1,2))
    with pytest.raises(ValueError,match="local character audit cap"):
        character_corrections((p,),max_words_per_program=2)
    with pytest.raises(ValueError,match="joint reference is exponential"):
        joint_fiber_reference((p,p),max_joint_words=8)
    with pytest.raises(ValueError,match="equal widths"):
        character_corrections((p,control((0,1,2),1)))


def test_declared_phase_class_is_not_trusted_without_local_check():
    class CubicCalibration:
        width=2; components=1; modulus=9
        def value(self,z): return (z[0]*z[0]*z[1] % 9,)
    with pytest.raises(ValueError,match="not ordinary quadratic"):
        character_corrections((CubicCalibration(),))


def test_all_record_likelihood_is_not_rejected_by_character_yield_ceiling():
    phases=(control((0,1,2)),)*4
    x=all_outcome_likelihood_reference(phases)
    ceiling=float(Fraction(3,9))
    assert x["mean_all_outcome_classical_MAP_success"]>ceiling
    assert x["classical_maximization_enumerates_all_secrets"]
    assert not x["polynomial_time_classical_likelihood_optimizer_supplied"]
    assert not x["public_shared_frequency_shift_changes_uniform_prior_MAP_success"]


def test_complete_likelihood_witnesses_match_actual_erasure_and_frequency_measurement():
    phases=(control((0,1,2)),control((0,2,4)))
    f=joint_fiber_reference(phases);L=all_outcome_likelihood_reference(phases);D=9;G=9
    maxima=[]
    for witness in L["MAP_witnesses"]:
        t=tuple(a for block in witness["local_word_Fourier_outcomes"] for a in block)
        values=[]
        for u in range(9):
            amp=sum(np.exp(2j*math.pi*(u*v[0]/9-sum(a*b for a,b in zip(t,z))/3))
                    for z,v in zip(f["joint_words"],f["joint_frequencies"]))/D
            values.append(abs(amp)**2)
        assert witness["maximum_likelihood"]==pytest.approx(max(values))
        maxima.append(max(values))
    assert L["mean_all_outcome_classical_MAP_success"]==pytest.approx(sum(maxima)/G)
    assert L["mean_all_outcome_classical_MAP_success"]<=f["ideal_full_secret_PGM_success"]+1e-12
    with pytest.raises(ValueError,match="enumerates all secrets"):
        all_outcome_likelihood_reference(phases,max_entries=80)


def test_report_pins_derivation_and_does_not_promote_the_receiver():
    import hashlib
    report=json.loads(REPORT.read_text())
    assert report["derivation_sha256"]==hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    assert not report["quantum_speedup_proved"] and not report["candidate_record_accepted"]
    assert not report["general_collective_receiver_ruled_out"]
    assert any(x["corrections"]["word_character_image_rank"] for x in report["native_controls"])
    for x in report["native_controls"]:
        ids=[i for cohort in x["source_cohorts"] for i in cohort["original_ancestry_ids"]]
        assert len(ids)==len(set(ids))
        assert sum(y["source_cap"] for y in x["source_cohorts"])==int(x["ledger"]["provided_original_inputs_per_attempt"])
        for cohort in x["source_cohorts"]:
            assert not cohort["source_premise_physically_certified"]


CHECKER=Path(__file__).resolve().parents[1]/"research/certificates/ternary_collective_character_receiver_crosscheck.js"


def test_independent_receiver_checker_passes_live_artifact():
    result=subprocess.run(["node",str(CHECKER)],capture_output=True,text=True,check=True)
    output=json.loads(result.stdout)
    assert output["status"]=="PASS" and output["all_record_MAP_witnesses"]==825
    assert not output["upstream_source_law_independently_certified"]


@pytest.mark.parametrize("mutation",["character","herald","map","scope","cost","span"])
def test_independent_receiver_checker_rejects_corrupted_evidence(tmp_path,mutation):
    report=json.loads(REPORT.read_text());c=report["native_controls"][1]
    if mutation=="character":c["corrections"]["full_root_secret_corrections"][0][0]=1
    elif mutation=="herald":c["joint_reference"]["zero_erasure_joint_correct_probability"]="1"
    elif mutation=="map":c["all_outcome_likelihood_reference"]["MAP_witnesses"][0]["maximum_likelihood"]=0
    elif mutation=="scope":report["general_collective_receiver_ruled_out"]=True
    elif mutation=="cost":c["ledger"]["uncorrected_expected_fresh_original_inputs_per_correct_readout"]="8"
    elif mutation=="span":c["corrections"]["complete_correction_image_certified"]=False
    path=tmp_path/"mutated.json";path.write_text(json.dumps(report))
    result=subprocess.run(["node",str(CHECKER),str(path)],capture_output=True,text=True)
    assert result.returncode!=0 and result.stderr
