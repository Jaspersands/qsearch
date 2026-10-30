"""Replay the norm-flat attack on fixed native inputs and save its scope."""

import argparse
from dataclasses import asdict
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

import numpy as np
from flint import nmod_mat

import norm_flat as n

ROOT = Path(__file__).resolve().parent
NPZ_HASH = "f33a15681f41d581023812364c6c42587e571ac616fb11452cef7cd7325913cf"
PARENT_HASH = "7e805dda45ab9ce18f6e727135a30dda3beb8f21dfb2cb9acd9381ec935af51d"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def native_input():
    if digest(ROOT/"data/native.npz") != NPZ_HASH or digest(ROOT/"data/cubic-parent.json") != PARENT_HASH:
        raise ValueError("frozen native provenance changed")
    parent = json.loads((ROOT/"data/cubic-parent.json").read_text())["native"]
    domain = parent["domain"]
    g = n.Geometry(domain["p"],3,domain["zeta"],tuple(o[0] for o in domain["orbits"]),570)
    if g.points != tuple(map(tuple,domain["orbits"])):
        raise ValueError("original native orbit order changed")
    with np.load(ROOT/"data/native.npz",allow_pickle=False) as data:
        if data["allowed"].shape != (2051,2053) or data["allowed"].dtype != np.bool_:
            raise ValueError("original explicit table shape changed")
        b = tuple(map(int,data["residual_coefficients"][:684]))
        if b != tuple(parent["multipliers"]):
            raise ValueError("original native multipliers changed")
        allowed = tuple(tuple(map(int,np.flatnonzero(row))) for row in data["allowed"][:684])
    return g,b,domain["eta_nonsquare"],allowed


def exact_controls():
    g,b,nu,allowed = n.fixture(19,5,917)
    s = n.build(g,b,nu)
    ranks = []
    for pivot in range(3):
        for tail in product(range(19),repeat=2-pivot):
            ranks.append(n.dual_derivative(s,[0]*pivot+[1]+list(tail)).rank())
    if len(ranks)!=381 or set(ranks)!={4}:
        raise ArithmeticError("projective rank proof control failed")
    derivative = n.dual_derivative(s,[1,0,0])
    center,_ = n.full_row_solve(derivative,n.vector([-int(s.linear[0,j]) for j in range(4)],19))
    failed = n.attempt(s,allowed,center)
    if failed["status"]!="RETRY_RANK":
        raise ArithmeticError("the deliberately singular center was not rejected")
    krylov = []
    for t in range(3):
        rows = [[pow(g.points[i][2],j,19)*int(matrix[i,a])%19
                 for j in range(t+1) for a in range(4)]
                for matrix in (s.wx,s.wy) for i in range(6)]
        krylov.append(nmod_mat(rows,19).rank())
    if krylov != [4,6,8]:
        raise ArithmeticError("extension-linear Krylov dimension control failed")
    return {"p":19,"M":6,"dimension":15,"projective_vectors":len(ranks),
            "all_dual_derivative_ranks":4,"exact_projective_union_bound":str(Fraction(381,19**4)),
            "reported_coarse_bound":"1/342","deliberate_failed_center":center,
            "failed_center_result":failed,"Fp_Krylov_dimensions":krylov,
            "optimality_claim_scope":"E_linear_common_norm_flats_only_LOCAL_UNREVIEWED"}


def receipt():
    paths = ("norm_flat.py","test_norm_flat.py","make_receipt.py","RESULT.md","HANDOFF.md",
             "data/native.npz","data/cubic-parent.json",
             "../orbit-residual-decoder-2026-10-24/orbit_decoder.py",
             "../orbit-residual-decoder-2026-10-24/ORBIT_DECODER.md",
             "../orbit-residual-decoder-2026-10-24/source_context.json")
    before = {path:digest(ROOT/path) for path in paths}
    rows = []
    for p,K in ((19,5),(31,9),(43,12),(97,27),(193,54),(769,214)):
        g,b,nu,allowed = n.fixture(p,K,917)
        specification = {"geometry":asdict(g),"multipliers":b,"nu":nu,"halfsets":allowed}
        rows.append({"p":p,"M":len(g.points),"dimension":g.dimension,"input_seed":917,
                     "input_sha256":hashlib.sha256(json.dumps(specification,sort_keys=True).encode()).hexdigest(),
                     "algorithm_seed":918,"result":n.solve(g,b,nu,allowed,seed=918)})
    g,b,nu,allowed = native_input()
    native = n.solve(g,b,nu,allowed,seed=271026)
    if native["status"]!="VERIFIED_NATIVE_PERFECT":
        raise ArithmeticError("fixed native run did not solve; keep the failed input, do not reroll")
    ledger = n.parameters(n.geometry(12289,3,3276))
    result = {"status":"LOCAL_UNREVIEWED_CLASSICAL_HIGH_RATE_FALSIFIER",
              "native_synthetic_inputs":rows,
              "frozen_author_table_run":{
                  "p":2053,"M":684,"original_cubic_dimension":204,"new_dimension":1710,
                  "rate":"5/6","old_n204_task_solved":False,"algorithm_seed":271026,
                  "same_original_halfsets_multipliers_nonsquare_and_orbits":True,
                  "parent_snapshot_sha256":PARENT_HASH,"input_npz_sha256":NPZ_HASH,"result":native},
              "exact_controls":exact_controls(),
              "existing_rate_point_eight_case":{**ledger,"status":"OUTSIDE_CERTIFIED_RANK_GATE"},
              "scope":{"fixed_input_bound":"LOCAL_UNREVIEWED",
                       "all_cubic_rates_dequantized":False,"uniform_sampler":False,
                       "quantum_algorithm_executed":False,"new_candidate_admitted":False,
                       "independent_review_or_novelty_claimed":False,"main_checkout_changed":False},
              "source_sha256":before}
    if before != {path:digest(ROOT/path) for path in paths}:
        raise RuntimeError("source or frozen input changed during the run")
    return result


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    data = receipt()
    rendered = json.dumps(data,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered,end="")
    print("Native n1710: ",data["frozen_author_table_run"]["result"]["verification"]["score"],"/684;",
          "rate0.8 remains outside the proven classical gate.")
