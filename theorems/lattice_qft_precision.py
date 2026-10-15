"""Logical QFT cutoff, encoded-angle bounds, query budgets and rare-event debt."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import numpy as np
from qiskit.synthesis.qft import synth_qft_full
from qiskit.quantum_info import Operator

from ternary_flat_character_certificate import _pi_interval
from ternary_measured_lattice_decoder import exact_json

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/lattice_qft_precision.json"
DERIVATION = ROOT / "research/LATTICE_QFT_PRECISION.md"
CONTRACT = ROOT / "research/hypotheses/lattice_qft_precision_contract.json"
PI_TERMS = 16


def integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError("exact " + name + " required")
    return value


def rational(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise ValueError("exact rational " + name + " required")
    result = Fraction(value)
    if max(abs(result.numerator).bit_length(), result.denominator.bit_length()) > 4096:
        raise ValueError("UNKNOWN_PARAMETER_CERTIFICATE_CAP; no algorithmic conclusion")
    return result


def ceil_log2_rational(value):
    q = Fraction(value)
    if q <= 0:
        raise ValueError("positive exact logarithm argument required")
    b = max(0, q.numerator.bit_length()-q.denominator.bit_length())
    while (1 << b) * q.denominator < q.numerator:
        b += 1
    while b and (1 << (b-1)) * q.denominator >= q.numerator:
        b -= 1
    return b


@dataclass(frozen=True)
class QFTUsage:
    direct_forward_calls: int = 1
    direct_inverse_calls: int = 0
    phase_parent_reflections: int = 0

    def __post_init__(self):
        for value in (self.direct_forward_calls, self.direct_inverse_calls, self.phase_parent_reflections):
            integer(value, "nonnegative QFT usage")
        if not self.total_calls:
            raise ValueError("positive total QFT usage required")

    @property
    def total_calls(self):
        return self.direct_forward_calls + self.direct_inverse_calls + 2*self.phase_parent_reflections

    def record(self):
        return {"direct_forward_calls": self.direct_forward_calls, "direct_inverse_calls": self.direct_inverse_calls,
                "phase_parent_reflections": self.phase_parent_reflections,
                "total_approximate_QFT_or_inverse_calls": self.total_calls,
                "receiver_usage_bound_is_external_not_proved_here": True}


@dataclass(frozen=True)
class QFTPrecisionPlan:
    wires: int
    cutoff: int
    target: Fraction
    usage: QFTUsage
    externally_certified_per_logical_gate_error: Fraction | None = None

    def __post_init__(self):
        integer(self.wires, "positive QFT wires", 1)
        integer(self.cutoff, "nonnegative separation cutoff")
        if self.wires > 1_000_000 or self.cutoff >= self.wires or self.cutoff > 4096:
            raise ValueError("UNKNOWN_PLAN_STORAGE_CAP; no QFT lower bound")
        target = rational(self.target, "target trace error")
        if not 0 < target <= 1 or not isinstance(self.usage, QFTUsage):
            raise ValueError("positive subunit target and typed query budget required")
        object.__setattr__(self, "target", target)
        if self.externally_certified_per_logical_gate_error is not None:
            eta = rational(self.externally_certified_per_logical_gate_error, "external per-gate operator error")
            if eta < 0:
                raise ValueError("nonnegative external gate error required")
            object.__setattr__(self, "externally_certified_per_logical_gate_error", eta)

    @property
    def exact(self):
        return self.cutoff == self.wires-1

    @property
    def controlled_phases(self):
        return self.cutoff*self.wires-self.cutoff*(self.cutoff+1)//2

    @property
    def retained_angle_weight(self):
        b, ell = self.cutoff, self.wires
        return Fraction(ell-2) + Fraction(b+2-ell, 2**b)

    @property
    def truncation_operator_upper(self):
        if self.exact:
            return Fraction(0)
        if self.wires <= 4096:
            tail = Fraction(self.wires-self.cutoff-2,2**self.cutoff)+Fraction(1,2**(self.wires-1))
            return min(Fraction(2),_pi_interval(PI_TERMS)[1]*tail)
        return min(Fraction(2),Fraction(4*(self.wires-self.cutoff-1),2**self.cutoff))

    @property
    def encoded_angle_upper(self):
        if self.cutoff > 1022:
            raise ValueError("UNKNOWN_NUMERIC_ANGLE_RANGE; no encoded parameter certificate")
        lo, hi = _pi_interval(PI_TERMS)
        encoded_pi = Fraction.from_float(float(np.pi))
        delta = max(abs(encoded_pi-lo), abs(encoded_pi-hi))
        return delta*self.retained_angle_weight

    @property
    def encoded_qft_operator_upper(self):
        return min(Fraction(2), self.truncation_operator_upper + self.encoded_angle_upper)

    def record(self):
        ell, b, T = self.wires, self.cutoff, self.usage.total_calls
        lo, hi = _pi_interval(PI_TERMS)
        logical = min(Fraction(1), T*self.truncation_operator_upper)
        supported = b <= 1022
        encoded = min(Fraction(1), T*self.encoded_qft_operator_upper) if supported else None
        gates = ell+self.controlled_phases+ell//2
        eta = self.externally_certified_per_logical_gate_error
        with_external = None if eta is None or not supported else min(Fraction(1), T*(self.encoded_qft_operator_upper+gates*eta))
        return {"QFT_wires": ell, "retained_maximum_separation": b,
                "qiskit_approximation_degree": ell-1-b, "query_usage": self.usage.record(),
                "target_complete_experiment_trace_error": str(self.target),
                "logical_controlled_phases_retained": self.controlled_phases,
                "logical_controlled_phases_omitted": ell*(ell-1)//2-self.controlled_phases,
                "logical_H_gates": ell, "logical_swaps": ell//2,
                "exact_ideal_QFT_selected": self.exact,
                "retained_dyadic_angle_weight": str(self.retained_angle_weight),
                "omitted_weight_symbolic": {"coefficient_at_2_pow_minus_cutoff": ell-b-2,
                    "cutoff_exponent": b, "unit_term_exponent": ell-1},
                "single_use_ideal_truncation_operator_upper": str(self.truncation_operator_upper),
                "truncation_bound_method": "EXACT_FINITE_TAIL_MACHIN_PI_UPPER" if self.wires <= 4096 else "SYMBOLIC_TAIL_4_TIMES_REMAINING_SPAN",
                "Machin_terms": PI_TERMS, "pi_rational_lower": str(lo), "pi_rational_upper": str(hi),
                "exact_encoded_binary64_pi": str(Fraction.from_float(float(np.pi))),
                "single_use_encoded_CP_parameter_operator_error_upper": str(self.encoded_angle_upper) if supported else None,
                "single_use_encoded_QFT_operator_error_upper": str(self.encoded_qft_operator_upper) if supported else None,
                "complete_experiment_ideal_truncation_trace_upper": str(logical),
                "complete_experiment_encoded_QFT_trace_upper": str(encoded) if supported else None,
                "ideal_truncation_target_met": logical <= self.target,
                "encoded_QFT_parameter_target_met": supported and encoded <= self.target,
                "numeric_normal_angle_encoding_supported": supported,
                "external_per_logical_gate_operator_error": None if eta is None else str(eta),
                "complete_experiment_upper_IF_external_gate_bound_holds": None if with_external is None else str(with_external),
                "arithmetic_preparation_and_hardware_errors_covered": False,
                "statevector_MPS_roundoff_certified": False,
                "normalized_rare_branch_accuracy_certified_without_mass_bound": False,
                "logical_query_budget_proves_efficient_receiver": False}


def precision_plan(wires, usage=None, target="1/100", cutoff=None, external_gate_error=None):
    integer(wires, "positive QFT wires", 1)
    usage = QFTUsage() if usage is None else usage
    if not isinstance(usage, QFTUsage):
        raise ValueError("typed forward/inverse/reflection usage required")
    delta = rational(target, "target")
    if not 0 < delta <= 1:
        raise ValueError("positive subunit target required")
    if cutoff is None:
        # Half the requested error is reserved for retained-angle encoding.
        cutoff = min(wires-1, ceil_log2_rational(8*wires*usage.total_calls/delta))
    return QFTPrecisionPlan(wires, cutoff, delta, usage, external_gate_error)


@dataclass(frozen=True)
class CircuitResourcePolicy:
    max_qubits: int | None = 16384
    max_adder_bits: int | None = 1024
    max_constant_additions: int | None = 1_000_000
    max_QFT_instructions: int | None = 1_000_000

    def __post_init__(self):
        for x in (self.max_qubits, self.max_adder_bits, self.max_constant_additions, self.max_QFT_instructions):
            if x is not None:
                integer(x, "positive explicit resource policy limit", 1)

    def check(self, *, qubits, adder_bits=0, constant_additions=0, QFT_instructions=0):
        for measured, limit in ((qubits,self.max_qubits),(adder_bits,self.max_adder_bits),
                                (constant_additions,self.max_constant_additions),(QFT_instructions,self.max_QFT_instructions)):
            if limit is not None and measured > limit:
                raise ValueError("UNKNOWN_RESOURCE_POLICY; no source impossibility conclusion")


def compile_qft(plan, policy=None, inverse=False):
    if not isinstance(plan, QFTPrecisionPlan) or type(inverse) is not bool:
        raise ValueError("typed precision plan and inverse mode required")
    policy = CircuitResourcePolicy() if policy is None else policy
    if not isinstance(policy,CircuitResourcePolicy):
        raise ValueError("typed circuit resource policy required")
    if plan.cutoff > 1022:
        raise ValueError("UNKNOWN_NUMERIC_ANGLE_RANGE; symbolic/high-precision synthesis required")
    policy.check(qubits=plan.wires, QFT_instructions=plan.wires+plan.controlled_phases+plan.wires//2)
    circuit = synth_qft_full(plan.wires, do_swaps=True, approximation_degree=plan.wires-1-plan.cutoff, inverse=inverse)
    ops = circuit.count_ops()
    if (ops.get("h",0), ops.get("cp",0), ops.get("swap",0)) != (plan.wires,plan.controlled_phases,plan.wires//2):
        raise ValueError("Qiskit QFT cutoff mapping changed")
    gaps = {}
    base = Fraction.from_float(float(np.pi))
    for instruction in circuit.data:
        if instruction.operation.name == "cp":
            j,k = (circuit.find_bit(q).index for q in instruction.qubits)
            d = abs(j-k)
            if not 1 <= d <= plan.cutoff or Fraction.from_float(abs(float(instruction.operation.params[0]))) != base/(2**d):
                raise ValueError("encoded rotation is not certified dyadic pi scaling")
            gaps[d] = gaps.get(d,0)+1
    if gaps != {d:plan.wires-d for d in range(1,plan.cutoff+1)}:
        raise ValueError("QFT separation multiplicities changed")
    return circuit


class QFTUsageLedger:
    def __init__(self, plan):
        self.plan = plan
        self.forward = self.inverse = self.reflections = 0

    def charge(self, kind, count=1):
        integer(count, "positive QFT operation count", 1)
        names = {"forward":("forward",self.plan.usage.direct_forward_calls),
                 "inverse":("inverse",self.plan.usage.direct_inverse_calls),
                 "parent_reflection":("reflections",self.plan.usage.phase_parent_reflections)}
        if kind not in names:
            raise ValueError("forward/inverse/parent_reflection QFT accounting required")
        attr, cap = names[kind]
        if getattr(self,attr)+count > cap:
            raise ValueError("QFT_QUERY_BUDGET_EXCEEDED; accuracy contract no longer applies")
        setattr(self,attr,getattr(self,attr)+count)

    def record(self):
        return {"charged_forward_calls":self.forward,"charged_inverse_calls":self.inverse,
                "charged_parent_reflections":self.reflections,
                "charged_total_QFT_or_inverse_calls":self.forward+self.inverse+2*self.reflections,
                "manual_untracked_circuit_calls_are_outside_accuracy_contract":True}

    def __copy__(self):
        raise ValueError("QFT usage ledger cannot be copied or reset")

    def __deepcopy__(self,memo):
        return self.__copy__()


def conditional_accuracy(global_trace_upper, success_mass_lower=None):
    delta = rational(global_trace_upper,"global complete-instrument trace bound")
    if not 0 <= delta <= 1:
        raise ValueError("subunit global trace bound required")
    if success_mass_lower is None:
        return {"status":"UNKNOWN_CONDITIONAL_PRECISION_NO_SUCCESS_MASS_BOUND", "conditional_trace_upper":None}
    p = rational(success_mass_lower,"success mass lower bound")
    if not 0 < p <= 1:
        raise ValueError("positive success probability lower bound required")
    return {"status":"CONDITIONAL_PRECISION_BOUND_NOT_FREE_POSTSELECTION",
            "conditional_trace_upper":str(min(Fraction(1),delta/p)), "success_mass_lower":str(p)}


def build_report():
    profiles = tuple(precision_plan(ell,QFTUsage(T,7,3),target).record()
                     for ell,T,target in ((264,128,"1/100"),(65536,10000,"1/100"),
                                          (1_000_000,1_000_000,"1/100"),(256,2**80,"1/100")))
    controls = []
    for ell,b in ((3,0),(4,1),(5,2),(6,5)):
        p = precision_plan(ell,QFTUsage(),"1/10",cutoff=b)
        circuit = compile_qft(p)
        U = Operator(circuit).data
        N = 2**ell
        F = np.exp(2j*np.pi*np.outer(np.arange(N),np.arange(N))/N)/np.sqrt(N)
        controls.append({"plan":p.record(),"actual_synthesized_gate_counts":dict(circuit.count_ops()),
                         "numerical_dense_operator_difference":float(np.linalg.norm(U-F,ord=2)),
                         "numerical_check_is_a_formal_gate_error_certificate":False})
    if __package__:
        from . import lattice_cube_dcp_readout as source_module
        from . import lattice_qft_precision as plan_module
    else:
        import lattice_cube_dcp_readout as source_module
        import lattice_qft_precision as plan_module
    n = 8
    source = source_module.CubeCosetSource(tuple(tuple(int(i==j) for j in range(n)) for i in range(n)),3,1,0,2**32,2,(1,)*n)
    large_plan = plan_module.precision_plan(264,plan_module.QFTUsage(128),"1/100")
    large = source_module.compile_phase_source(source,qft_plan=large_plan)
    return {"status":"LATTICE_QFT_PRECISION_QUERY_AND_POSTSELECTION_DEBT_REVIEW_PENDING",
            "producer_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "contract_sha256":hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
            "dependency_sha256": {f:hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest()
                for f in ("ternary_flat_character_certificate.py","ternary_measured_lattice_decoder.py","lattice_cube_source_circuit.py","lattice_cube_dcp_readout.py")},
            "scaling_precision_profiles":profiles,"actual_synthesis_controls":tuple(controls),
            "actual_beyond_old_128_wire_compile":large.resource_record(),
            "large_control_is_resource_only_classically_easy_not_a_DCP_promise":True,
            "rare_postselection_countercontrols":tuple({"success_mass":str(Fraction(1,2**k)),
                "complete_accept_reject_trace_distance":str(Fraction(1,2**k)),
                "normalized_accepted_payload_trace_distance":"1", "free_conditional_accuracy_inference_valid":False}
                for k in (8,32,128)),
            "hardware_or_full_source_channel_error_certified":False,"efficient_receiver_supplied":False,
            "accepted_speedup_candidate":False,"new_active_negative_result_created":False,"novelty_claim":False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True,exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report),indent=2)+"\n")
    print(json.dumps({"status":report["status"],"scaling_profiles":len(report["scaling_precision_profiles"]),
                      "encoded_budget_met":[r["encoded_QFT_parameter_target_met"] for r in report["scaling_precision_profiles"]],
                      "accepted_speedup_candidate":False},indent=2))


if __name__=="__main__":
    main()
