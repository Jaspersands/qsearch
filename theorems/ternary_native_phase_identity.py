"""Compact growing-depth native phase merges and randomized identity tests.

LOCAL DERIVATION / REVIEW PENDING. Public modular functions only. No unknown
phase oracle, efficient merge search, full-depth speedup or exact proof from
finite random testing. False-accept bounds require fresh independent points.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import random

import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_correlated_packet_acquisition import PacketAcquisition, integer, word
from ternary_cubic_program_factory import relation, seeded_cohort
from ternary_phase_depth import NativePhaseHierarchy, cyclic_difference

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_NATIVE_PHASE_IDENTITY.md"
REPORT = ROOT / "research/phase_workbench/ternary_native_phase_identity.json"


@dataclass(frozen=True)
class NativeProgram:
    branch: object
    width: int
    complement: tuple

    def __post_init__(self):
        integer(self.width, "native program width", 1)
        packet = self.branch.packet
        if packet.level < 3 or packet.level % 2 == 0 or packet.retained < self.width:
            raise ValueError("actual odd native packet with sufficient retained width required")
        word(self.complement, packet.retained-self.width)
        if self.branch.acquisition.source.level != packet.level+1:
            raise ValueError("original-source acquired packet lineage required")

    @property
    def phase_digits(self): return (self.branch.packet.level-1)//2

    @property
    def source_ids(self): return self.branch.acquisition.source_ids

    def original_value(self, z):
        z = word(z, self.width); q = 3**self.phase_digits
        base = self.branch.original_residual((0,)*self.width+self.complement)
        return tuple((a-b) % q for a, b in zip(self.branch.original_residual(z+self.complement), base))

    def compact(self):
        packet = self.branch.packet; hierarchy = NativePhaseHierarchy.from_packet(packet)
        base = packet.assignment((0,)*self.width+self.complement)
        columns = [tuple((a-b) % 3 for a, b in zip(packet.assignment(tuple(int(i == j) for i in range(self.width))+self.complement), base)) for j in range(self.width)]
        numerator_modulus = packet.phase_modulus; n = packet.secret_dimension; groups = {}
        for i in range(packet.consumed):
            row = tuple(column[i] for column in columns)
            if not any(row): continue
            sign = next(a for a in row if a)
            direction = tuple(sign*a % 3 for a in row)
            tables = groups.setdefault(direction, [[0,0,0] for _ in range(n)])
            for l in range(n):
                local = hierarchy.local_frequency_tables[i][l]
                for t in (1,2):
                    tables[l][t] = (tables[l][t]+local[(base[i]+sign*t) % 3]-local[base[i]]) % numerator_modulus
        return RidgePhase(self.width, n, self.phase_digits, packet.level,
                          tuple((direction, tuple(tuple(row) for row in tables)) for direction, tables in sorted(groups.items())))

    def record(self):
        source = self.branch.acquisition.source
        base = self.branch.lift((0,)*self.width+self.complement)
        columns = [tuple((a-b) % 3 for a,b in zip(self.branch.lift(tuple(int(i == j) for i in range(self.width))+self.complement),base)) for j in range(self.width)]
        exponent = len(self.branch.acquisition.active)-self.width
        return {"source": self.branch.acquisition.source_record(), "original_labels": source.labels,
                "original_frequency_pairs": source.frequencies,
                "original_affine_base": base, "original_affine_columns": columns,
                "raw_source_program_branch_probability": str(Fraction(1,3**exponent)),
                "all_source_measurement_outcomes_accepted": True,
                "compact_phase": self.compact().record(), "IID_full_depth_output_label_law_proved": False}


@dataclass(frozen=True)
class RidgePhase:
    width: int
    components: int
    phase_digits: int
    additive_degree_bound: int
    groups: tuple

    def __post_init__(self):
        for x, name in ((self.width,"width"),(self.components,"components"),(self.phase_digits,"phase digits")):
            integer(x,name,1)
        integer(self.additive_degree_bound,"additive degree bound",0)
        keys = []
        for direction, tables in self.groups:
            direction = word(direction,self.width)
            if not any(direction) or next(x for x in direction if x) != 1:
                raise ValueError("canonical nonzero projective ridge direction required")
            if len(tables) != self.components: raise ValueError("one table per component required")
            for table in tables:
                if len(table) != 3 or table[0] != 0 or any(type(x) is not int or not 0 <= x < self.numerator_modulus for x in table):
                    raise ValueError("canonical normalized modular ridge table required")
                if (table[2]-2*table[1]) % 3: raise ValueError("native low linearity required before division")
            keys.append(direction)
        if len(set(keys)) != len(keys): raise ValueError("ridge keys must be merged")
        for l in range(self.components):
            if any(sum(tables[l][1]*direction[j] for direction,tables in self.groups) % 3 for j in range(self.width)):
                raise ValueError("global native kernel needed for exact denominator3")
        # This schema retains the native degree bound; arbitrary claimed bounds
        # are not admitted by the identity tester.
        if self.additive_degree_bound != 2*self.phase_digits+1:
            raise ValueError("native additive degree2r+1 required, not an arbitrary user assertion")

    @property
    def modulus(self): return 3**self.phase_digits

    @property
    def numerator_modulus(self): return 3*self.modulus

    def derivative(self, base, directions=()):
        base = word(base,self.width); directions = tuple(word(v,self.width) for v in directions)
        if len(directions) > 512: raise ValueError("factored derivative order capped at512")
        out = [0]*self.components
        for direction,tables in self.groups:
            t = sum(a*b for a,b in zip(direction,base)) % 3
            increments = [sum(a*b for a,b in zip(direction,v)) % 3 for v in directions]
            for l, table in enumerate(tables):
                for h in increments: table = cyclic_difference(table,h,self.numerator_modulus)
                out[l] += table[t]
        out = [x % self.numerator_modulus for x in out]
        if any(x % 3 for x in out): raise ArithmeticError("native compact phase lost global divisibility")
        return tuple(x//3 for x in out)

    def value(self,z): return self.derivative(z)

    def shifted(self,m,c):
        m = word(m,self.width)
        if type(c) is not int or c not in (1,2): raise ValueError("one-use domain sign1/2 required")
        groups = []
        for direction,tables in self.groups:
            offset = sum(a*b for a,b in zip(direction,m)) % 3
            shifted = tuple(tuple((row[(offset+c*t) % 3]-row[offset]) % self.numerator_modulus for t in range(3)) for row in tables)
            groups.append((direction,shifted))
        return RidgePhase(self.width,self.components,self.phase_digits,self.additive_degree_bound,tuple(groups))

    def record(self):
        return {"width": self.width,"components": self.components,"phase_digits": self.phase_digits,
                "phase_modulus": str(self.modulus),"numerator_modulus": str(self.numerator_modulus),
                "exact_shared_denominator": 3,"additive_degree_bound": self.additive_degree_bound,
                "projective_ridge_groups": [{"direction": direction,"component_tables": tables} for direction,tables in self.groups],
                "stored_local_frequency_entries": 3*self.components*len(self.groups),
                "high_degree_tensor_expanded": False,"unknown_weighted_phase_oracle_supplied": False}

    def degree_certificate(self):
        """Exact local degrees give a global upper bound, not a global equality."""
        R = self.phase_digits+1; records = []; maximum = 0
        def valuation(x):
            if x == 0: return R
            v = 0
            while x % 3 == 0: v += 1; x //= 3
            return v
        for direction,tables in self.groups:
            local = []
            for table in tables:
                first = cyclic_difference(table,1,self.numerator_modulus)
                second = cyclic_difference(first,1,self.numerator_modulus)
                u,v = min(map(valuation,first)),min(map(valuation,second))
                degree = max(0,2*(R-u)-1,2*(R-v))
                local.append({"first_difference_min_valuation":u,"second_difference_min_valuation":v,
                              "exact_local_additive_degree":degree})
                maximum = max(maximum,degree)
            records.append({"direction":direction,"component_certificates":local})
        if maximum > self.additive_degree_bound: raise ArithmeticError("local degree exceeds verified native class")
        return {"group_certificates":records,"certified_global_degree_upper":maximum,
                "upper_bound_is_exact_global_degree":False,"tensor_entries_expanded":0,
                "basis":"Delta^(2h+1)=(-3)^h*S^h*Delta; Delta^(2h+2)=(-3)^h*S^h*Delta^2"}


def merge(programs,coefficients,outcomes):
    programs = tuple(programs)
    if not programs or len(coefficients) != len(programs): raise ValueError("full source cohort and one sign per program required")
    if any(type(c) is not int or c not in (0,1,2) for c in coefficients) or not any(coefficients):
        raise ValueError("nonzero cohort of canonical domain signs required")
    phases = [p.compact() for p in programs]; first = phases[0]
    if any((p.width,p.components,p.phase_digits) != (first.width,first.components,first.phase_digits) for p in phases):
        raise ValueError("common width, component count and modulus required")
    ids = [x for p in programs for x in p.source_ids]
    if len(set(ids)) != len(ids): raise ValueError("disjoint original ancestry required")
    selected = tuple(j for j,c in enumerate(coefficients) if c)
    if len(outcomes) != len(selected): raise ValueError("one actual measured word per consumed program required")
    groups = {}
    for j,m in zip(selected,outcomes):
        phase = phases[j].shifted(m,coefficients[j])
        for direction,tables in phase.groups:
            aggregate = groups.setdefault(direction,[[0,0,0] for _ in range(first.components)])
            for l,row in enumerate(tables):
                for t,x in enumerate(row): aggregate[l][t] = (aggregate[l][t]+x) % first.numerator_modulus
    groups = tuple((direction,tuple(tuple(row) for row in tables)) for direction,tables in sorted(groups.items()) if any(any(row) for row in tables))
    merged = RidgePhase(first.width,first.components,first.phase_digits,first.additive_degree_bound,groups)
    exponent = sum(len(p.branch.acquisition.active)-p.width for p in programs)
    record = {"coefficients": tuple(coefficients),"selected_program_indices": selected,"injection_outcomes": tuple(outcomes),
              "source_programs": [p.record() for p in programs],"merged_phase": merged.record(),
              "all_injection_outcomes_accepted": True,"each_selected_program_consumed_once": True,
              "full_original_input_cap_charged": len(ids),"physical_IID_independence_certified_by_ids": False,
              "raw_source_program_transcript_probability": str(Fraction(1,3**exponent)),
              "conditional_injection_transcript_probability": str(Fraction(1,3**(first.width*len(selected)))),
              "unknown_inverse_conjugation_or_cloning_used": False,
              "efficient_search_for_useful_merge_rule_supplied": False,"quantum_speedup_proved": False}
    return merged,record


def identity_budget(degree,kappa):
    integer(degree,"certified additive degree",0); integer(kappa,"soundness bits",1)
    return {"certified_additive_degree": degree,"nonzero_relative_support_lower": str(Fraction(1,2**degree)),
            "independent_uniform_tests_required": kappa*2**degree,
            "conditional_false_accept_probability_upper": str(Fraction(1,2**kappa)),
            "dimension_independent": True,"fresh_points_after_candidate_commit_required": True}


def test_identity(phase,order,kappa=8,max_evaluations=100000,seed=None):
    """Test an additive derivative identity without materializing its cube."""
    integer(order,"derivative order",0); integer(max_evaluations,"evaluation cap",1)
    if order > 512: raise ValueError("derivative order capped at512")
    degree_certificate = phase.degree_certificate()
    degree = degree_certificate["certified_global_degree_upper"]
    budget = identity_budget(degree,kappa)
    committed = hashlib.sha256(json.dumps({"phase":phase.record(),"order":order},sort_keys=True).encode()).hexdigest()
    rng = random.SystemRandom() if seed is None else random.Random(seed)
    if order > degree or not phase.groups:
        return {"status":"EXACT_FACTORED_IDENTITY","tested_derivative_order":order,
                "phase_commit_sha256":committed,"calibration_seed":seed,"budget":budget,
                "evaluations_used":0,"counterexample":None,"degree_certificate":degree_certificate,
                "soundness_bound_applicable_to_this_run":False,
                "deterministic_seed_is_mathematical_randomness_certificate":False,
                "exact_identity_proved_by_random_testing":False,"identity_algebraically_certified":True,
                "derivative_cube_vertices_materialized":0,"local_modular_subtractions_upper":0}
    trials = min(max_evaluations,budget["independent_uniform_tests_required"])
    witness = None; transcript = hashlib.sha256(); count = 0
    for _ in range(trials):
        base = tuple(rng.randrange(3) for _ in range(phase.width))
        directions = tuple(tuple(rng.randrange(3) for _ in range(phase.width)) for _ in range(order))
        value = phase.derivative(base,directions);count += 1
        transcript.update(json.dumps([base,directions,value],separators=(",",":")).encode())
        if any(value):
            witness = {"base":base,"directions":directions,"component_derivative":value};break
    applicable = witness is None and count == budget["independent_uniform_tests_required"] and seed is None
    status = "EXPLICIT_COUNTEREXAMPLE" if witness else ("RANDOMIZED_IDENTITY_EVIDENCE" if applicable else "UNCERTIFIED_NO_WITNESS")
    return {"status":status,"tested_derivative_order":order,"phase_commit_sha256":committed,
            "calibration_seed":seed,"budget":budget,"evaluations_used":count,"counterexample":witness,
            "soundness_bound_applicable_to_this_run":applicable,
            "deterministic_seed_is_mathematical_randomness_certificate":False,
            "complete_transcript_sha256":transcript.hexdigest(),"exact_identity_proved_by_random_testing":False,
            "identity_algebraically_certified":False,"degree_certificate":degree_certificate,
            "derivative_cube_vertices_materialized":0,
            "local_modular_subtractions_upper":3*phase.components*len(phase.groups)*order*count}


def lift_program(program,r,seed):
    """Preserve the lower original frequency chart; fresh high lifts for calibration."""
    integer(r,"retained phase digits",1)
    if r == 1: return NativeProgram(program.branch,program.width,program.complement)
    source = program.branch.acquisition.source; rng = random.Random(seed);level = 2*r+2;q = 3**(r+1)
    labels = [[inverse_frequency_coordinates(pair[0][l]+9*rng.randrange(q//9),pair[1][l]+9*rng.randrange(q//9),level) for l in range(source.dimension)] for pair in source.frequencies]
    lifted = native_source(labels,level)
    acquisition = PacketAcquisition.from_source(lifted,len(program.branch.acquisition.supports),tuple(f"lift-r{r}-{seed}-{x}" for x in program.source_ids),source.inputs)
    pointers = tuple(program.branch.anchor[i] for i in program.branch.acquisition.pointers)
    branch = acquisition.branch(pointers,program.branch.packet.syndrome)
    if acquisition.supports != program.branch.acquisition.supports or branch.packet.free != program.branch.packet.free:
        raise ArithmeticError("preserved original low chart changed standardized frame")
    return NativeProgram(branch,program.width,program.complement)


def injection_control(program,c,secret):
    d,D = program.width,3**program.width
    if d > 3: raise ValueError("bounded physical injection replay width<=3")
    q = 3**program.phase_digits; secret = tuple(secret)
    if len(secret) != program.branch.packet.secret_dimension or any(type(s) is not int or not 0 <= s < q for s in secret):
        raise ValueError("full retained-modulus calibration secret required")
    ws = tuple(product(range(3),repeat=d)); index = {z:i for i,z in enumerate(ws)}
    data = np.eye(D,dtype=complex)/math.sqrt(D); state = np.zeros((D,D,D),complex)
    for zi,z in enumerate(ws):
        for ui,u in enumerate(ws):
            m = tuple((a-c*b) % 3 for a,b in zip(u,z))
            theta = sum(s*a for s,a in zip(secret,program.original_value(u))) % q
            state[:,index[m],zi] += data[:,zi]*np.exp(2j*math.pi*theta/q)/math.sqrt(D)
    maximum = 0.
    for mi,m in enumerate(ws):
        phase = np.array([np.exp(2j*math.pi*(sum(s*a for s,a in zip(secret,program.original_value(tuple((a+c*b) % 3 for a,b in zip(m,z))))) % q)/q) for z in ws])
        maximum = max(maximum,float(np.max(abs(state[:,mi]-data*phase/math.sqrt(D)))))
        if abs(float(np.sum(abs(state[:,mi])**2))-1/D)>4e-12: raise ArithmeticError("nonuniform native injection branch")
    if maximum > 4e-12: raise ArithmeticError("native SUM phase injection replay failed")
    return {"full_retained_modulus_secret":secret,"all_injection_outcomes":D,
            "arbitrary_reference_entangled_max_error":maximum,
            "conditional_branch_probability":str(Fraction(1,D)),"reference_dimension":D}


def run_controls():
    base = seeded_cohort(2,3,88708);coefficients,certificate = relation(base)
    selected = certificate["selected_program_indices"]
    outcomes = tuple(tuple((j+i+1) % 3 for i in range(3)) for j in selected)
    controls = []
    for r in (1,2,3):
        programs = tuple(lift_program(p,r,88800+r*100+j) for j,p in enumerate(base))
        phase,record = merge(programs,coefficients,outcomes)
        ws = tuple(product(range(3),repeat=3))
        for program in programs:
            compact = program.compact()
            if any(compact.value(z) != program.original_value(z) for z in ws): raise ArithmeticError("ridge evaluator disagrees with original source")
        table = [phase.value(z) for z in ws]
        for z,actual in zip(ws,table):
            direct = tuple(sum(programs[j].original_value(tuple((a+coefficients[j]*b) % 3 for a,b in zip(m,z)))[l]-programs[j].original_value(m)[l] for j,m in zip(selected,outcomes)) % phase.modulus for l in range(2))
            if actual != direct: raise ArithmeticError("compact merge disagrees with original phases")
        record.update({"phase_digits":r,"calibration_control_kind":"preserved-low-chart-full-root-native-lifts-not-population-estimate",
                       "complete_original_word_checks":len(programs)*len(ws),"complete_merged_frequency_table":table,
                       "degree_two_probe":test_identity(phase,3,kappa=8,seed=88900+r),
                       "top_degree_probe":test_identity(phase,phase.additive_degree_bound,kappa=8,seed=88920+r),
                       "physical_injection_controls":[injection_control(programs[j],coefficients[j],(phase.modulus-1,phase.modulus//3+1 if r>1 else 2)) for j in selected]})
        controls.append(record)
    return {"status":"COMPACT_GROWING_DEPTH_PHASE_MERGES_AND_RANDOMIZED_IDENTITIES_REVIEW_PENDING",
            "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),"native_controls":controls,
            "identity_budgets":[{"phase_digits":r,**identity_budget(2*r+1,32)} for r in (1,2,4,8,16,32)],
            "candidate_record_accepted":False,"useful_full_depth_merge_rule_discovered":False,
            "quantum_speedup_proved":False,"routine_wiring_owner":"Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"report":str(REPORT) if args.write else None,
                      "degree_two_probe_statuses":[c["degree_two_probe"]["status"] for c in report["native_controls"]]},indent=2))


if __name__ == "__main__":main()
