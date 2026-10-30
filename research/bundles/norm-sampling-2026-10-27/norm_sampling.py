"""Single-trial norm sampling; distribution guarantees require stated promises."""

from fractions import Fraction
from pathlib import Path
import random
import sys

from flint import fmpz, nmod_mat

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "two-component-norm-2026-10-27"))
from norm_completion import NormCompletion, affine_solution, nullspace, rank, rows


def prime(p):
    if type(p) is not int or not 3 <= p < 2**63 or not fmpz(p).is_prime():
        raise ValueError("verified odd prime below 2^63 required")


def weighted_bounds(p, k, size, restriction_rank):
    """Conditional theorem bounds, NOT a check of the universal rank premise."""
    prime(p)
    if any(type(v) is not int or v < 1 for v in (k, size, restriction_rank)):
        raise ValueError("positive integer dimensions required")
    eta = Fraction(size, p*p)
    if eta >= 1:
        return {"conditional_on_universal_rank_promise": True,
                "rank_promise_checked_by_this_function": False,
                "deficiency_moment_upper": None,
                "bad_coset_probability_upper": None,
                "zero_union_bound": eta, "trial_success_lower": Fraction(0),
                "rank_weighted_trial_success_lower": Fraction(0),
                "tv_upper": Fraction(1), "useful_certificate": False,
                "reason": "ZERO_UNION_BOUND_ALREADY_VACUOUS"}
    delta0 = Fraction(p**k-1, p**(2*restriction_rank))
    delta1 = size*p*p*delta0
    useful = delta1 < 1 and eta < 1
    alpha = (1-delta1)*(1-eta) if useful else Fraction(0)
    beta = delta1+delta0
    return {"conditional_on_universal_rank_promise": True,
            "rank_promise_checked_by_this_function": False,
            "deficiency_moment_upper": delta0,
            "bad_coset_probability_upper": min(Fraction(1), delta1),
            "zero_union_bound": eta,
            "trial_success_lower": alpha,
            "rank_weighted_trial_success_lower": alpha/(1+delta0),
            "tv_upper": beta/(alpha+beta) if useful else Fraction(1),
            "useful_certificate": useful}


def ag_sampling_bounds(p, e):
    prime(p)
    if p < 1019 or type(e) is not int or e < 8:
        raise ValueError("p>=1019 and integer e>=8 required")
    if e < 64:
        return {"p": p, "e": e, "method": "EXACT_SYSTEMATIC_REJECTION",
                "trial_success_lower": 1-Fraction(5*e+3, p-1),
                "tv_upper": Fraction(0), "ag_promise_checked": False}
    result = weighted_bounds(p, 5*e+3, 22*e-1, 3*e-e//4-11)
    result.update(p=p, e=e, method="GLOBAL_NORM_REJECTION",
                  constant_success_scope=p*p >= 44*e,
                  ag_promise_checked=False, native_matrix_adapter_implemented=False)
    return result


class GlobalNormSampler:
    def __init__(self, case):
        if not isinstance(case, NormCompletion):
            raise TypeError("verified NormCompletion data required")
        self.case = case
        self.outside = [i for i in range(case.m) if i not in case.T]
        if rank([[row[i] for i in case.T] for row in case.A], case.p) != case.r:
            raise ValueError("auxiliary must remain full row rank on support(h)")
        if any(all(row[i] == 0 for row in case.A) for i in case.T):
            raise ValueError("nonzero auxiliary columns on support(h) required")

    def prepare(self, syndrome, outside_values, a, b):
        case = self.case
        syndrome = case.vector(syndrome, case.k)
        values = case.vector(outside_values, len(self.outside))
        if not all(values):
            raise ValueError("outside coordinates must be nonzero")
        # The reused search backend fixes outside entries to1; compensate
        # its target, then restore the actual outside entries after sampling.
        target = [(s-sum(row[i]*(x-1) for i, x in zip(self.outside, values))) % case.p
                  for s, row in zip(syndrome, case.B)]
        prepared = case.prepare(target, a, b)
        if prepared["status"] == "CERTIFIED_AFFINE_FIBER":
            if any(event["rank"] != 2 for event in prepared["events"]):
                return {"status": "REJECT_MARGINAL_RANK"}
            prepared.update(outside_values=values, original_syndrome=syndrome)
        return prepared

    def one_trial(self, syndrome, rng):
        case = self.case
        syndrome = case.vector(syndrome, case.k)
        values = [rng.randrange(1, case.p) for _ in self.outside]
        a = [rng.randrange(case.p) for _ in case.T]
        b = [rng.randrange(case.p) for _ in case.T]
        prepared = self.prepare(syndrome, values, a, b)
        if prepared["status"] != "CERTIFIED_AFFINE_FIBER":
            return {"status": prepared["status"], "word": None}
        word = case.sample(prepared, rng)
        for i, x in zip(self.outside, values):
            word[i] = x
        if any(sum(x*y for x, y in zip(row, word)) % case.p != s
               for row, s in zip(case.B, syndrome)):
            raise ArithmeticError("sample violates original syndrome")
        if not all(word):
            return {"status": "REJECT_ZERO_NORM", "word": None}
        return {"status": "VERIFIED_NATIVE_WITNESS", "word": word,
                "syndrome": syndrome, "kernel_dimension": prepared["dimension"],
                "marginal_ranks": [event["rank"] for event in prepared["events"]]}

    def draw(self, syndrome, *, seed, attempts=64):
        syndrome = self.case.vector(syndrome, self.case.k)
        if type(attempts) is not int or attempts < 1:
            raise ValueError("positive attempt cap required")
        rng, statuses = random.Random(seed), []
        for _ in range(attempts):
            result = self.one_trial(syndrome, rng)
            statuses.append(result["status"])
            if result["word"] is not None:
                result.update(trials=len(statuses), trial_statuses=statuses,
                              distribution="GOOD_COSET_NORM_PUSHFORWARD",
                              exact_uniform_native_claim=False,
                              universal_rank_promise_checked=False)
                return result
        return {"status": "UNKNOWN_ATTEMPT_CAP", "word": None,
                "trial_statuses": statuses, "hardness_evidence": False,
                "exact_uniform_native_claim": False}


def systematic_draw(p, B, syndrome, *, seed, attempts=64):
    """Exact uniform conditional on success; efficiency is a separate promise."""
    prime(p)
    if type(attempts) is not int or attempts < 1:
        raise ValueError("positive attempt cap required")
    from norm_completion import checked_matrix
    B = checked_matrix(B, p)
    k, m = len(B), len(B[0])
    syndrome = list(syndrome)
    if len(syndrome) != k or any(type(x) is not int or not 0 <= x < p for x in syndrome):
        raise ValueError("canonical syndrome of required size expected")
    reduced, dimension = nmod_mat(B, p).rref()
    if dimension != k:
        raise ValueError("full row rank required")
    pivots = [next(j for j, x in enumerate(row) if x) for row in rows(reduced)]
    free = [i for i in range(m) if i not in pivots]
    inverse = nmod_mat([[row[i] for i in pivots] for row in B], p).inv()
    rng = random.Random(seed)
    for trial in range(1, attempts+1):
        word = [0]*m
        for i in free:
            word[i] = rng.randrange(1, p)
        target = nmod_mat([[int((s-sum(row[i]*word[i] for i in free)) % p)]
                           for s, row in zip(syndrome, B)], p)
        answer = inverse*target
        for j, i in enumerate(pivots):
            word[i] = int(answer[j, 0])
        if all(word):
            if any(sum(x*y for x, y in zip(row, word)) % p != s
                   for row, s in zip(B, syndrome)):
                raise ArithmeticError("systematic sample violates original relation")
            return {"status": "VERIFIED_NATIVE_WITNESS", "word": word,
                    "trials": trial, "syndrome": syndrome,
                    "exact_uniform_conditional_on_success": True,
                    "efficiency_promise_checked": False}
    return {"status": "UNKNOWN_ATTEMPT_CAP", "word": None,
            "hardness_evidence": False}


class RankWeightedNormSampler(GlobalNormSampler):
    """Exact under the declared rank promise; R=0 is always valid."""

    def __init__(self, case, restriction_rank=0):
        super().__init__(case)
        if type(restriction_rank) is not int or not 0 <= restriction_rank <= case.r:
            raise ValueError("rank promise must be an integer between0 and r")
        self.R = restriction_rank
        self.base_weight = case.p**(2*self.R)
        self.nonzero_lambdas = case.p**case.k-1

    def offset_proposal(self, rng):
        case, p = self.case, self.case.p
        if rng.randrange(self.base_weight+self.nonzero_lambdas) < self.base_weight:
            return {"branch": "BASE", "a": [rng.randrange(p) for _ in case.T],
                    "b": [rng.randrange(p) for _ in case.T]}
        number = rng.randrange(1, self.nonzero_lambdas+1)
        coefficient = []
        for _ in range(case.k):
            number, digit = divmod(number, p)
            coefficient.append(digit)
        c = [sum(coefficient[j]*case.B[j][i] for j in range(case.k)) % p for i in case.T]
        U = [[row[i]*case.h[i]*value % p for i, value in zip(case.T, c)] for row in case.A]
        actual_rank = rank(U, p)
        if actual_rank < self.R:
            raise ValueError("universal restriction-rank promise contradicted")
        if rng.randrange(p**(2*(actual_rank-self.R))) != 0:
            return {"branch": "INCIDENT", "status": "REJECT_THINNING",
                    "restriction_rank": actual_rank}
        kernel = nullspace(U, p)
        def offset():
            free = [rng.randrange(p) for _ in range(len(kernel[0]))]
            return [sum(x*y for x, y in zip(row, free)) % p for row in kernel]
        return {"branch": "INCIDENT", "a": offset(), "b": offset(),
                "restriction_rank": actual_rank, "coefficient": coefficient}

    def one_trial(self, syndrome, rng):
        case = self.case
        syndrome = case.vector(syndrome, case.k)
        values = [rng.randrange(1, case.p) for _ in self.outside]
        proposal = self.offset_proposal(rng)
        if "status" in proposal:
            return {"status": proposal["status"], "word": None, "branch": proposal["branch"]}
        target = [(s-sum(row[i]*(x-1) for i, x in zip(self.outside, values))) % case.p
                  for s, row in zip(syndrome, case.B)]
        a, b = proposal["a"], proposal["b"]
        prepared = case.prepare(target, a, b)
        matrix_rank = rank(prepared["matrix"], case.p)
        if prepared["status"] != "CERTIFIED_AFFINE_FIBER":
            base = case.evaluate([0]*(2*case.r), a, b)
            adjusted = [(s-sum(x*y for x, y in zip(row, base))) % case.p
                        for s, row in zip(target, case.B)]
            try:
                point, kernel = affine_solution(prepared["matrix"], adjusted, case.p)
            except ValueError:
                return {"status": "REJECT_INCONSISTENT_TARGET", "word": None,
                        "branch": proposal["branch"], "syndrome_rank": matrix_rank}
            prepared.update(status="CERTIFIED_AFFINE_FIBER", point=point, kernel=kernel,
                            dimension=len(kernel[0]), a=a, b=b)
        word = case.sample(prepared, rng)
        for i, value in zip(self.outside, values):
            word[i] = value
        if any(sum(x*y for x, y in zip(row, word)) % case.p != s
               for row, s in zip(case.B, syndrome)):
            raise ArithmeticError("rank-weighted sample violates original syndrome")
        if not all(word):
            return {"status": "REJECT_ZERO_NORM", "word": None, "branch": proposal["branch"]}
        return {"status": "VERIFIED_NATIVE_WITNESS", "word": word,
                "syndrome": syndrome, "syndrome_rank": matrix_rank,
                "kernel_dimension": prepared["dimension"], "branch": proposal["branch"]}

    def draw(self, syndrome, *, seed, attempts=64):
        result = super().draw(syndrome, seed=seed, attempts=attempts)
        result.update(distribution="RANK_SIZE_BIASED_NORM_LIFTS",
                      declared_restriction_rank=self.R,
                      exact_uniform_given_rank_promise=True,
                      exact_uniform_native_claim=self.R == 0,
                      universal_rank_promise_checked=self.R == 0)
        return result
