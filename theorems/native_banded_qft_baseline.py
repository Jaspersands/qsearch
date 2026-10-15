"""Dense-free, certified finite-precision sampling of two-call banded QFT schedules.

Public digit phases enter; hidden secrets, oracle truth and dense word tables do
not. Exact Gaussian integers contract the doubled network for prefix masses.
Arb certifies root approximations before sampling; bit precision and caps are
charged separately from structural contraction width. This is not a solver.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import random
import secrets

from flint import acb, ctx, fmpq

from native_response_fourier_factorization_audit import site_phase_tables

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_BANDED_QFT_BASELINE.md"
CONTRACT = ROOT / "research/hypotheses/native_banded_qft_baseline_contract.json"
REPORT = ROOT / "research/classical_baselines/native_banded_qft_baseline.json"


def positive(value, name, minimum=1):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def ceil_log2(value):
    positive(value, "positive logarithm argument")
    return (value - 1).bit_length()


def flint_fraction(value):
    return Fraction(int(value.numerator), int(value.denominator))


def certified_dyadic_root(turn, bits, max_enclosure_bits):
    """Reusable exact-input root enclosure; no probability normalization."""
    positive(bits,"phase grid bits");positive(max_enclosure_bits,"enclosure cap")
    if type(turn) is not int and not isinstance(turn,Fraction):
        raise ValueError("exact integer or Fraction turn required, not float angles")
    turn=Fraction(turn)%1;scale=1<<bits;prec=bits+16
    while prec<=max_enclosure_bits:
        with ctx.workprec(prec):
            z=acb(fmpq(2*turn.numerator,turn.denominator)).exp_pi_i()
            nums,distances=[],[]
            for component in (z.real,z.imag):
                mid=flint_fraction(component.mid().fmpq());value=(mid*scale).__floor__()
                lo,hi=flint_fraction(component.lower().fmpq()),flint_fraction(component.upper().fmpq())
                distances.append(max(abs(lo-Fraction(value,scale)),abs(hi-Fraction(value,scale))))
                nums.append(value)
        err=sum(distances)
        if err<=Fraction(4,scale):
            return {"turn":str(turn),"integer_value":tuple(nums),
                "Arb_complex_l1_error_upper":str(err),"enclosure_bits":prec}
        if prec==max_enclosure_bits:break
        prec=min(2*prec,max_enclosure_bits)
    raise BaselineResourceLimit("UNKNOWN_ROOT_ENCLOSURE_PRECISION_CAP")


class BaselineResourceLimit(RuntimeError):
    """Operational UNKNOWN, never evidence of classical hardness."""


@dataclass(frozen=True)
class ContractionPolicy:
    max_boundary_states: int = 100000
    max_phase_entries: int = 100000
    max_total_window_evaluations: int = 50000000
    max_enclosure_bits: int = 4096

    def __post_init__(self):
        for key, value in asdict(self).items():
            positive(value, key)


def gaussian_multiply(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gaussian_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gaussian_conjugate(a):
    return (a[0], -a[1])


def error_ledger(M, failure_bits):
    positive(M, "word sites")
    positive(failure_bits, "failure bits")
    P = failure_bits + ceil_log2(32 * M * 3 ** M)
    K = failure_bits + ceil_log2(4 * M)
    epsilon = Fraction(4, 2 ** P)
    norm_error = 2 * 3 ** M * M * epsilon
    phase_TV = 2 * norm_error
    grid_TV = Fraction(2 * M, 2 ** K)
    assert M * epsilon <= Fraction(1, 2) and norm_error < 1
    assert phase_TV + grid_TV <= Fraction(1, 2 ** failure_bits)
    return {"word_sites_M": M, "failure_bits": failure_bits,
        "phase_grid_bits_P": P, "random_bits_per_digit_K": K,
        "root_complex_error_upper": str(epsilon),
        "unnormalized_state_2norm_error_upper": str(norm_error),
        "normalized_phase_approximation_TV_upper": str(phase_TV),
        "finite_uniform_grid_TV_upper": str(grid_TV),
        "per_complete_sample_TV_upper": str(phase_TV + grid_TV),
        "ideal_independent_uniform_bits_required": True,
        "rare_prefix_conditional_precision_assumed": False,
        "numerical_or_work_cap_is_hardness_evidence": False}


def cyclic_cutoff_ledger(M, failure_bits):
    """Two qutrit QFT truncations: operator-norm telescope, not gate fidelity."""
    positive(M,"word sites");positive(failure_bits,"failure bits")
    target=64*M*2**failure_bits
    b,power3=1,3
    while b<M and power3<target:
        b+=1;power3*=3
    omitted=sum((Fraction(M-d,3**(d+1)) for d in range(b,M)),Fraction(0))
    # Each omitted CP has max digit product4: |exp(i theta)-1|<=|theta|.
    # pi<22/7 gives8*pi<176/7; forward and adjoint EACH pay this norm loss.
    per_transform=Fraction(176,7)*omitted
    joint=min(Fraction(1),2*per_transform)
    arithmetic=Fraction(error_ledger(M,failure_bits+1)["per_complete_sample_TV_upper"])
    assert joint<=Fraction(1,2**(failure_bits+1))
    assert joint+arithmetic<=Fraction(1,2**failure_bits)
    return {"word_sites_M":M,"failure_bits":failure_bits,"selected_bandwidth_b":b,
        "integer_cutoff_threshold_64_M_times2_pow_f":str(target),
        "exact_omitted_weight_sum":str(omitted),
        "single_QFT_operator_norm_error_upper":str(per_transform),
        "forward_and_adjoint_QFTs_charged":2,
        "joint_Born_TV_truncation_upper":str(joint),
        "classical_phase_and_grid_TV_upper":str(arithmetic),
        "complete_full_cyclic_sample_TV_upper":str(joint+arithmetic),
        "exact_untruncated_sampler_supplied":False,
        "inverse_polynomial_accuracy_gives_logarithmic_bandwidth":True,
        "small_work_caps_disprove_this_constructive_bound":False}


class BandedQFTBaseline:
    """Two-call public-phase schedule, with whole-sample resource preflight."""

    def __init__(self, phase_tables, q, bandwidth, second_call_sign=1,
                 failure_bits=32, policy=None):
        positive(q, "phase modulus", 2)
        phases = tuple(tuple(row) for row in phase_tables)
        if not phases or any(len(row) != 3 or any(
                type(x) is not int or not 0 <= x < q for x in row) for row in phases):
            raise ValueError("nonempty canonical public three-digit phase tables required")
        self.M, self.q, self.phases = len(phases), q, phases
        positive(bandwidth, "bandwidth")
        if bandwidth > self.M or type(second_call_sign) is not int or second_call_sign not in (-1, 1):
            raise ValueError("1 <= bandwidth <= M and sign in {-1,+1} required")
        self.b, self.sign = bandwidth, second_call_sign
        self.policy = policy or ContractionPolicy()
        if not isinstance(self.policy, ContractionPolicy):
            raise ValueError("typed resource policy required")
        # Reject oversized width before constructing an exponential-size table.
        width = 1
        for _ in range(self.b - 1):
            width *= 27
            if width > self.policy.max_boundary_states:
                raise BaselineResourceLimit("UNKNOWN_BOUNDARY_STATE_CAP")
        if 9 * self.M * 3 ** self.b > self.policy.max_phase_entries:
            raise BaselineResourceLimit("UNKNOWN_PHASE_ENTRY_CAP")
        self.ledger = error_ledger(self.M, failure_bits)
        self.P, self.K = self.ledger["phase_grid_bits_P"], self.ledger["random_bits_per_digit_K"]
        if self.P + 16 > self.policy.max_enclosure_bits:
            raise BaselineResourceLimit("UNKNOWN_ROOT_ENCLOSURE_PRECISION_CAP")
        self.scale = 1 << self.P
        self.roots, self._local, self._weights = {}, {}, {}
        self.stats = {"window_evaluations": 0, "prefix_contractions": 0,
            "peak_boundary_states": 0, "root_enclosures_computed": 0,
            "maximum_enclosure_bits_used": 0, "maximum_integer_bits_seen": 0,
            "random_bits_consumed": 0, "dense_word_rows_allocated": 0,
            "all_outcomes_enumerated_by_sampler": False,
            "hidden_truth_used": False}
        # Every needed phase is certified before any outcome-dependent randomness.
        for k in range(self.M):
            for w, t, r in product(range(3), range(3), range(3 ** self.b)):
                self._root(Fraction(self.phases[k][w] + self.sign * self.phases[self.M - 1 - k][t], q)
                           + Fraction(r, 3 ** self.b))

    @classmethod
    def from_records(cls, records, mask, bandwidth, **kwargs):
        records = tuple(records)
        tables = site_phase_tables(records, mask)
        return cls(tuple(s["digit_phases"] for s in tables), records[0].modulus,
                   bandwidth, **kwargs)

    def _root(self, turn):
        turn %= 1
        if turn in self.roots:
            return self.roots[turn]["integer_value"]
        receipt=certified_dyadic_root(turn,self.P,self.policy.max_enclosure_bits)
        self.roots[turn]=receipt
        self.stats["root_enclosures_computed"]+=1
        self.stats["maximum_enclosure_bits_used"]=max(
            self.stats["maximum_enclosure_bits_used"],receipt["enclosure_bits"])
        return receipt["integer_value"]

    def _factor(self, k, w, x):
        key = (k, w, x)
        if key not in self._local:
            turn = sum((a - c) * 3 ** (self.b - 1 - j)
                       for j, (a, c) in enumerate(zip(w, x)))
            out = (0, 0)
            for t in range(3):
                phase = Fraction(self.phases[k][w[0]] + self.sign * self.phases[self.M - 1 - k][t], self.q)
                out = gaussian_add(out, self._root(phase + Fraction(t * turn, 3 ** self.b)))
            self._local[key] = out
        return self._local[key]

    def _preflight(self, samples):
        positive(samples, "sample count")
        worst = samples * (3 * self.M + 1) * self.M * 27 ** self.b
        if self.stats["window_evaluations"] + worst > self.policy.max_total_window_evaluations:
            raise BaselineResourceLimit("UNKNOWN_COMPLETE_SAMPLE_WORK_CAP")
        return worst

    def prefix_weight(self, prefix):
        """Exact nonnegative mass numerator, marginalizing all unspecified outputs."""
        prefix = tuple(prefix)
        if len(prefix) > self.M or any(type(x) is not int or x not in (0, 1, 2) for x in prefix):
            raise ValueError("canonical leading site-digit prefix required")
        if prefix in self._weights:
            return self._weights[prefix]
        bound = self.M * 27 ** self.b
        if self.stats["window_evaluations"] + bound > self.policy.max_total_window_evaluations:
            raise BaselineResourceLimit("UNKNOWN_PREFIX_CONTRACTION_WORK_CAP")
        alphabets = tuple(tuple(product(range(3), range(3),
                         (prefix[j],) if j < len(prefix) else range(3))) for j in range(self.M))
        init_len = self.b - 1
        state = {s: (1, 0) for s in product(*alphabets[:init_len])}
        peak, windows = len(state), 0
        for k in range(self.M):
            win_len, prev_len = min(self.b, self.M - k), min(self.b - 1, self.M - k)
            nxt = {}
            for win in product(*alphabets[k:k + win_len]):
                w, wp, x = tuple(zip(*win))
                a = self._factor(k, w, x)
                ap = self._factor(k, wp, x)
                factor = gaussian_multiply(a, gaussian_conjugate(ap))
                term = gaussian_multiply(state[win[:prev_len]], factor)
                key = win[1:]
                nxt[key] = gaussian_add(nxt.get(key, (0, 0)), term)
                windows += 1
            state = nxt
            peak = max(peak, len(state))
            self.stats["maximum_integer_bits_seen"] = max(
                self.stats["maximum_integer_bits_seen"],
                max(max(abs(a).bit_length(), abs(b).bit_length()) for a, b in state.values()))
        value, imaginary = state[()]
        if imaginary != 0 or value < 0:
            raise ArithmeticError("doubled contraction must be real and nonnegative")
        self.stats["window_evaluations"] += windows
        self.stats["prefix_contractions"] += 1
        self.stats["peak_boundary_states"] = max(self.stats["peak_boundary_states"], peak)
        self._weights[prefix] = value
        return value

    def prefix_probability(self, prefix):
        z = self.prefix_weight(())
        if z <= 0:
            raise ArithmeticError("certified approximate state cannot be zero")
        return Fraction(self.prefix_weight(prefix), z)

    def sample_many(self, count, randbits=None, record_trace=False):
        """Preflight an entire batch; injected bits are diagnostics unless IID."""
        self._preflight(count)
        bit_source = secrets.randbits if randbits is None else randbits
        z = self.prefix_weight(())
        if z <= 0:
            raise ArithmeticError("zero normalized approximate state")
        samples = []
        for _ in range(count):
            prefix, trace = (), []
            for k in range(self.M):
                weights = tuple(self.prefix_weight(prefix + (d,)) for d in range(3))
                parent = self.prefix_weight(prefix)
                if sum(weights) != parent or parent <= 0:
                    raise ArithmeticError("exact prefix normalization or positive parent failed")
                u = bit_source(self.K)
                if type(u) is not int or not 0 <= u < 2 ** self.K:
                    raise ValueError("bit source must return a canonical K-bit integer")
                self.stats["random_bits_consumed"] += self.K
                cumulative = 0
                for d, weight in enumerate(weights):
                    cumulative += weight
                    if u * parent < cumulative * 2 ** self.K:
                        break
                if record_trace:
                    trace.append({"prefix": prefix, "child_weights": tuple(str(w) for w in weights),
                        "uniform_grid_integer": str(u), "selected_digit": d})
                prefix += (d,)
            samples.append({"site_digits_MSB_first": prefix, "trace": tuple(trace)})
        return {"status": "COMPLETED_PUBLIC_PHASE_CLASSICAL_SAMPLING",
            "samples": tuple(samples), "random_source": "SYSTEM_RANDOM_BITS" if randbits is None else "INJECTED_BITS_DIAGNOSTIC",
            "injected_PRNG_is_a_formal_IID_certificate": False,
            "joint_batch_TV_upper_under_IID_bits": str(min(Fraction(1), count * Fraction(self.ledger["per_complete_sample_TV_upper"]))),
            "resource_cap_aborts_are_not_conditioned_away": True}

    def public_record(self):
        return {"modulus_q": str(self.q), "public_digit_phase_tables": tuple(
                tuple(str(x) for x in row) for row in self.phases),
            "twiddle_bandwidth_b": self.b, "second_call_sign": self.sign,
            "accuracy_ledger": self.ledger, "resource_policy": asdict(self.policy),
            "phase_grid": tuple({**self.roots[t], "integer_value": tuple(
                str(x) for x in self.roots[t]["integer_value"])} for t in sorted(self.roots)),
            "observed_work": dict(self.stats),
            "local_factor_cache_entries": len(self._local),
            "local_factor_cache_entries_upper": self.M * 9 ** self.b,
            "cached_prefix_weights": len(self._weights),
            "exact_integer_arithmetic_bit_cost_is_not_unit_cost": True,
            "intermediate_integer_bits_upper": self.M * (2 * self.P + 8) + 2,
            "max_prefix_boundary_states_upper": 27 ** (self.b - 1),
            "prefix_window_evaluations_upper": self.M * 27 ** self.b,
            "complete_sample_window_evaluations_upper": (3 * self.M + 1) * self.M * 27 ** self.b,
            "general_quantum_lower_bound_claimed": False,
            "hidden_secret_recovery_algorithm_supplied": False}


class FullCyclicQFTBaseline:
    """Approximate FULL two-call ideal distribution; caps remain operational."""
    def __init__(self,phase_tables,q,second_call_sign=1,failure_bits=32,policy=None):
        phase_tables=tuple(phase_tables)
        self.cutoff=cyclic_cutoff_ledger(len(phase_tables),failure_bits)
        self.banded=BandedQFTBaseline(phase_tables,q,self.cutoff["selected_bandwidth_b"],
            second_call_sign,failure_bits+1,policy)

    def sample_many(self,count,randbits=None,record_trace=False):
        result=self.banded.sample_many(count,randbits,record_trace)
        result["target_distribution"]="IDEAL_FULL_CYCLIC_TWO_CALL_QFT_BORN_DISTRIBUTION"
        result["joint_batch_TV_upper_under_IID_bits"]=str(min(Fraction(1),
            count*Fraction(self.cutoff["complete_full_cyclic_sample_TV_upper"])))
        result["full_cyclic_cutoff_ledger"]=self.cutoff
        return result


def finite_control(M, q, b, sign, failure_bits, seed, samples=1):
    from native_full_root_slice import source_data
    raw, mask, _, _ = source_data(1, 1 if q == 3 else 2, M, True, seed)
    model = BandedQFTBaseline.from_records(raw, mask, b,
        second_call_sign=sign, failure_bits=failure_bits)
    rng = random.Random(seed + 1)
    outcome = model.sample_many(samples, rng.getrandbits, record_trace=M <= 3)
    probabilities = ()
    if M <= 3:
        probabilities = tuple(str(model.prefix_probability(x)) for x in product(range(3), repeat=M))
    return {"original_records": tuple(r.public() for r in raw), "public_mask": tuple(mask),
        "model": model.public_record(), "sampling": outcome,
        "small_calibration_only_all_outcome_probabilities": probabilities,
        "private_truth_or_errors_supplied_to_baseline": False}


def build_report():
    controls = tuple(finite_control(M, q, b, sign, 20, seed, samples)
        for M, q, b, sign, seed, samples in (
            (2, 9, 1, 1, 100201, 2), (2, 9, 2, 1, 100202, 2),
            (2, 9, 1, -1, 100203, 2), (2, 9, 2, -1, 100204, 2),
            (3, 9, 2, -1, 100205, 1), (32, 9, 2, 1, 100206, 1),
            (64, 3, 1, -1, 100207, 1)))
    deps = ("native_response_fourier_factorization_audit.py", "native_basis_lottery.py",
            "native_full_root_slice.py", "ternary_noise_degradation.py")
    return {"status": "CERTIFIED_DENSE_FREE_TWO_CALL_BANDED_QFT_CLASSICAL_BASELINE",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in deps},
        "controls": controls, "accepted_speedup_candidate": False,
        "full_cyclic_approximation_profiles":tuple(cyclic_cutoff_ledger(M,f) for M,f in
            ((2,8),(3,8),(32,2),(64,20),(1024,10))),
        "new_active_negative_result_created": False,
        "exact_full_bandwidth_polynomial_sampler_claimed": False,
        "full_cyclic_inverse_polynomial_accuracy_structural_sampler_bound": True,
        "three_or_more_calls_covered": False,
        "research_decision": "TWO_CALL_PUBLIC_PHASE_CYCLIC_QFT_HAS_A_PAID_CLASSICAL_APPROXIMATE_SAMPLER_AT_INVERSE_POLYNOMIAL_ACCURACY"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(report["status"])
    print("Live public-phase controls:", len(report["controls"]))
    print("Full cyclic approximation is paid; exact full-bandwidth sampling is not claimed. No secret solver or new active negative.")


if __name__ == "__main__":
    main()
