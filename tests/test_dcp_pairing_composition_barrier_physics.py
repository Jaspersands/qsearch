from copy import deepcopy
from fractions import Fraction
from math import comb
from pathlib import Path
import json
import subprocess
import sys

import numpy as np
import pytest

from theorems.dcp_adaptive_direction_rank_gate import decode_dyadic
from theorems.dcp_correlated_phase_block import density
from theorems.dcp_nonlinear_fiber_pairing import compiler_certificate
from theorems.dcp_pairing_composition_barrier import (
    PREMISES, REPORT, build_report, exact_short_union, native_short_census,
    require_premises, short_threshold, two_level_bound,
)

ROOT=Path(__file__).resolve().parents[1]
CHECKER=ROOT/"research/certificates/dcp_pairing_block_tradeoff_crosscheck.js"


def test_exact_short_union_bound_covers_all_small_threshold_recipes():
    for n in range(2,65):
        for m in range(2,65):
            R=short_threshold(n,m)
            r=R["long_mask_minimum_width"]
            assert R["counting_exponent_check"] is True
            assert exact_short_union(n,m,r) <= Fraction(1,1 << n)
            assert r==min(m,(n+(m-1).bit_length()-1)//(m-1).bit_length())


def test_native_census_mean_degrees_and_short_events_are_not_pointwise_claims():
    C=native_short_census(2,2,2)
    assert C["all_native_label_assignments_and_basis_endpoints"]==1024
    assert decode_dyadic(C["short_endpoint_probability"])==Fraction(31,256)
    assert decode_dyadic(C["expected_short_degree"])==Fraction(1,8)
    P={"kind":"PUBLIC_SINGLE_FLIP","width":2,"mask":1,
       "table_lookup_is_a_free_coherent_oracle":False,"uniform_efficient_program_supplied":True}
    K=compiler_certificate(((4,1),(0,1)),3,2,P)
    assert decode_dyadic(K["useful_descent_probability"])==1
    assert len(K["pairs"])==2


def test_rounded_signal_and_collective_readout_bounds_dominate_exact_rationals():
    for n in (2,3,4,8,16,32,64,128):
        for m in (n, n*n):
            R=max(m,n**4)
            Q=n*n
            B=two_level_bound(n,m,m,R,Q,premises=PREMISES)
            r=B["first_pool"]["long_mask_minimum_width"]
            exact=min(Fraction(1),Fraction(R+1,1 << n)+(1-Fraction(1,n))**(r*r))
            upper=Fraction(1,1 << B["unconditional_final_visibility_power_of_two_upper_exponent"])
            readout=Fraction(1,1 << B["joint_output_distance_from_secret_independent_reference_power_of_two_upper_exponent"])
            assert exact<=upper
            assert min(Fraction(1),Q*upper/2)<=readout


def test_elementary_inverse_n_power_bound_including_integer_edges():
    for n in range(2,65):
        v=1-Fraction(1,n)
        assert v**(n-1)<=Fraction(1,2)
        for weight in (0,1,n-2,n-1,n,n*n):
            assert v**weight<=Fraction(1,1 << (weight//(n-1)))


@pytest.mark.parametrize("premise",list(PREMISES))
def test_missing_or_contradicted_source_or_output_premise_fails_closed(premise):
    for mode in ("missing","changed","wrong_type"):
        P=deepcopy(PREMISES)
        if mode=="missing":
            del P[premise]
        elif mode=="changed":
            P[premise]=not P[premise] if type(P[premise]) is bool else "correlated-noise"
        else:
            P[premise]=int(P[premise]) if type(P[premise]) is bool else True
        with pytest.raises(ValueError,match="UNKNOWN_OUTSIDE"):
            two_level_bound(64,4096,4096,64**8,premises=P)


def test_all_or_none_noise_has_same_marginals_but_evades_width_product():
    A=((1,1,1,1),)
    pure=density(A,3,(1,),1)
    correlated=(pure+np.eye(16)/16)/2
    independent=density(A,3,(1,),Fraction(1,2))
    for i in range(4):
        def offdiag(rho):
            return sum(rho[x,x | (1 << i)] for x in range(16) if not (x >> i & 1))
        assert 2*abs(offdiag(correlated))==pytest.approx(1/2)
        assert np.allclose(offdiag(correlated),offdiag(independent))
    assert 16*abs(correlated[0,15])==pytest.approx(1/2)
    assert 16*abs(independent[0,15])==pytest.approx(1/16)
    P=dict(PREMISES,original_noise="all-or-none-correlated")
    with pytest.raises(ValueError):
        require_premises(P)


def test_heterogeneous_public_tags_multiply_only_on_actual_physical_support():
    v=Fraction(3,4)
    tags=(2,3,4,5)
    source=np.ones((16,16),dtype=float)/16
    for x in range(16):
        for y in range(16):
            source[x,y]*=float(v**sum(e for i,e in enumerate(tags) if (x^y) >> i & 1))
    assert 16*source[0,5]==pytest.approx(float(v**6))
    assert 16*source[0,15]==pytest.approx(float(v**sum(tags)))
    assert float(v**6) <= float((v**2)**2)


def test_inverse_quadratic_noise_is_an_explicit_escape_not_the_same_converse():
    n=64
    r=short_threshold(n,n*n)["long_mask_minimum_width"]
    assert (1-Fraction(1,n*n))**(r*r)>Fraction(9,10)
    P=dict(PREMISES,original_noise="independent-balanced-dephasing-with-visibility-1-minus-1-over-n-squared")
    with pytest.raises(ValueError):
        require_premises(P)


def test_large_frontiers_have_conservative_vacuous_and_nonvacuous_regions():
    report=build_report()
    first,last=report["polynomial_budget_frontiers"][0],report["polynomial_budget_frontiers"][-1]
    assert first["unconditional_final_visibility_power_of_two_upper_exponent"]==0
    assert last["joint_output_distance_from_secret_independent_reference_power_of_two_upper_exponent"]==575
    assert all(not C["general_DHSP_or_retained_block_no_go"] for C in report["polynomial_budget_frontiers"])


def test_live_artifact_and_independent_replay():
    report=build_report()
    assert json.loads(REPORT.read_text())==report
    assert not report["new_active_negative_result_created"]
    result=subprocess.run(["node",str(CHECKER)],text=True,capture_output=True,check=True)
    assert json.loads(result.stdout)["native_censuses_replayed"]==3


@pytest.mark.parametrize("field",["short_relation_endpoint_count","sum_short_relation_degrees"])
def test_independent_checker_rejects_forged_census(tmp_path,field):
    report=build_report()
    report["native_short_mask_censuses"][1][field]+=1
    path=tmp_path/"forged.json"
    path.write_text(json.dumps(report))
    result=subprocess.run(["node",str(CHECKER),str(path)],text=True,capture_output=True)
    assert result.returncode!=0


def test_cli_no_write_keeps_live_artifact_unchanged():
    before=REPORT.read_bytes()
    result=subprocess.run([sys.executable,"qsearch.py","dcp-pairing-composition-barrier","--no-write"],cwd=ROOT,text=True,capture_output=True)
    assert result.returncode==0,result.stderr
    assert REPORT.read_bytes()==before
