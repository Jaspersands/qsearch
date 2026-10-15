"""Private noise subtraction cannot certify a public coordinate-recovery attack."""
import pytest
from theorems import native_retained_work_multiplicity_erasure_audit as A
from ternary_noise_degradation import NoisyLinearRecord


@pytest.mark.parametrize("error", (0,1))
def test_preimage_equation_check_distinguishes_noiseless_recovery_from_private_noise_subtraction(monkeypatch,error):
    raw=(NoisyLinearRecord((1,),error,3,"scope-0"),
         NoisyLinearRecord((0,),0,3,"scope-1"))
    monkeypatch.setattr(A,"source_data",lambda *args:(raw,(0,),(0,),(error,0)))
    result=A.retained_work_multiplicity_control((1,1,1,bool(error),0))
    preimage=result["chosen_frequency_preimage_equivalence"]
    assert preimage["all_standard_basis_frequencies_supported"]
    assert preimage["private_error_subtracted_equations_match_truth"] is True
    assert preimage["direct_classical_secret_recovered_when_supported"] is (True if error==0 else None)
    assert preimage["private_errors_used_for_equation_check_only"] is True
    assert preimage["noisy_public_secret_recovery_supplied"] is False
    assert preimage["short_preimage_sampler_alone_solves_noisy_problem"] is False
