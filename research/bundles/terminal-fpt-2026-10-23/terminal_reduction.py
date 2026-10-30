"""Terminal parameter accounting and bounded finite reduction falsifiers.

The finite controller enumerates its supplied universe. It is NOT the
scalable hidden-intersection learner or an implemented quantum algorithm.
"""

from dataclasses import dataclass
from fractions import Fraction
from modular_lazard import instruction_cap


def ceil_log2(value):
    value = Fraction(value)
    if value <= 0:
        raise ValueError("positive argument required")
    e = max(0, value.numerator.bit_length()-value.denominator.bit_length())
    return e+int((value.denominator << e) < value.numerator)


def terminal_plan(prime, dimension, class_bound, k, error=Fraction(1, 100)):
    if any(type(v) is not int for v in (prime, dimension, class_bound, k)):
        raise ValueError("integer parameters required")
    if prime < 2 or k < 1 or not 1 <= dimension <= k*(k+1)//2:
        raise ValueError("caller-verified prime and bounded terminal dimension required")
    if not 1 <= class_bound <= min(dimension, 2*k-1):
        raise ValueError("invalid terminal class bound")
    error = Fraction(error)
    if not 0 < error < 1:
        raise ValueError("error must be in (0,1)")
    report = {"prime": prime, "p_length": dimension, "class_bound": class_bound,
              "index_exponent_bound": k, "quantum_receiver_executed": False,
              "independent_proof_review_complete": False, "speedup_claim": False}
    if class_bound == 1:
        return report | {"branch": "known_abelian_hsp", "enumerated_elements": 0}
    if prime <= class_bound:
        return report | {"branch": "bounded_terminal_enumeration",
                         "enumerated_elements": prime**dimension,
                         "uniform_enumeration_cap": (2*k)**(k*(k+1)//2)}
    multiplier = (class_bound+1)**((class_bound-1)*(k-1))
    samples = dimension+ceil_log2(Fraction(8*dimension, 1)/error)
    chart_spanning_words = sum(dimension**j for j in range(1, class_bound+1))
    return report | {
        "branch": "repeated_complete_omega_intersections",
        "enumerated_elements": 0,
        "intersection_call_cap": dimension,
        "per_call_final_fourier_samples": samples,
        "per_call_source_multiplier_cap": multiplier,
        "original_f_query_cap_for_terminal_rees_sources": dimension*class_bound*samples*multiplier,
        "chart_spanning_word_cap": chart_spanning_words,
        "modular_word_instruction_cap": instruction_cap(class_bound),
        "uniform_source_multiplier_cap": (2*k)**(2*(k-1)**2),
        "preprocessing_and_coherent_compilation_paid_separately": True,
    }


@dataclass(frozen=True)
class FiniteGroup:
    elements: tuple
    identity: object
    multiply: object
    inverse: object

    def power(self, value, exponent):
        out = self.identity
        while exponent:
            if exponent & 1:
                out = self.multiply(out, value)
            value = self.multiply(value, value)
            exponent >>= 1
        return out

    def subgroup(self, generators):
        generators = tuple(generators)
        known, stack = {self.identity}, [self.identity]
        while stack:
            x = stack.pop()
            for g in generators:
                y = self.multiply(x, g)
                if y not in known:
                    known.add(y)
                    stack.append(y)
        return frozenset(known)

    def conjugate(self, x, subset):
        inverse = self.inverse(x)
        return frozenset(self.multiply(self.multiply(x, h), inverse) for h in subset)


def finite_omega_recovery(group, prime, oracle, intersection_override=None):
    """Original-group S/B invariant. Enumeration is deliberate and capped.

    override exists only for an adversarial incomplete-intersection control.
    It is not a valid backend contract. oracle is a promised ordinary HSP
    function; the test harness independently constructs and checks its fibers.
    """
    if len(group.elements) > 1024:
        raise ValueError("finite falsifier universe exceeds 1024-element cap")
    if type(prime) is not int or prime < 2:
        raise ValueError("caller-verified prime required")
    S, B = frozenset(group.elements), frozenset({group.identity})
    identity_label, queries, stages = oracle(group.identity), 1, []
    while S != B:
        omega = frozenset(x for x in S if group.power(x, prime) in B)
        if group.subgroup(omega) != omega:
            raise ValueError("order-dividing-p elements do not form a subgroup")
        K = frozenset(x for x in omega if oracle(x) == identity_label)
        queries += len(omega)
        if intersection_override is not None:
            K = frozenset(intersection_override(group, S, B, omega, K))
        if not B <= K <= omega or group.subgroup(K) != K:
            raise ValueError("invalid intersection supplied by test backend")
        stage = {"ambient_order": len(S)//len(B), "omega_order": len(omega)//len(B),
                 "intersection_order": len(K)//len(B)}
        if K == B:
            stages.append(stage | {"terminal_trivial_intersection": True})
            break
        normalizer = frozenset(x for x in S if group.conjugate(x, K) == K)
        if not K <= normalizer or len(normalizer)//len(K) >= len(S)//len(B):
            raise ArithmeticError("normalizer quotient failed to decrease")
        stages.append(stage | {"normalizer_index": len(S)//len(normalizer),
                               "next_quotient_order": len(normalizer)//len(K),
                               "terminal_trivial_intersection": False})
        S, B = normalizer, K
    return {"recovered": B, "stages": stages, "oracle_queries": queries,
            "enumerated_control": True, "quantum_receiver_executed": False}
