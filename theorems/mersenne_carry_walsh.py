"""Exact 2-adic moment/carry evaluation, with explicit optional work caps.

No full-field table is used. The constant-width claim concerns the fixed
canonical Mersenne family; general controls use width s. A capped run may
return WORK_CAP without any coefficient. Polynomial does not mean practical.
The mathematical construction is documented in MERSENNE_CARRY_WALSH_DRAFT.md.
"""
import argparse
from hashlib import sha256
import json
from math import comb, factorial
from pathlib import Path

from flint import fmpz_mod_poly_ctx

from theorems.balanced_codeword_filter import integer
from theorems.explicit_quadratic_opi import field
from theorems.mersenne_reciprocal_curve import _metadata, _parameters


class CarryWorkCap(RuntimeError):
    pass


class UnramifiedBinaryRing:
    """(Z/2^M)[T]/f, using the canonical field's monic irreducible lift."""

    def __init__(self, bits, precision):
        integer(bits, 3, 127, "field bits")
        integer(precision, 1, 10000, "2-adic precision")
        self.bits, self.precision = bits, precision
        self.modulus = 1 << precision
        self.context = fmpz_mod_poly_ctx(self.modulus)
        self.field_modulus = tuple(map(int, field(bits).modulus().coeffs()))
        self.polynomial = self.context(list(self.field_modulus))
        self.zero, self.one = self.context([]), self.context([1])

    def multiply(self, left, right):
        return (left*right) % self.polynomial

    def teichmuller(self, word):
        integer(word, 0, (1 << self.bits)-1, "field word")
        value = self.context([(word >> i) & 1 for i in range(self.bits)])
        # Each q-power iteration improves 2-adic agreement by at least one bit.
        for _ in range(self.bits*(self.precision-1)):
            value = self.multiply(value, value)
        if value.pow_mod(1 << self.bits, self.polynomial) != value:
            raise ArithmeticError("Teichmuller lift failed its q-power identity")
        return value

    def scalar(self, value):
        coefficients = list(map(int, value.coeffs()))
        if any(coefficients[1:]):
            raise ArithmeticError("completed trace expression is not in the base ring")
        return coefficients[0] if coefficients else 0


def parity_polynomial(precision):
    """Monomial coefficients of sum_(j<M) (-2)^j binom(Z,j), modulo 2^M.

    Cancel the factorial's power of two before inverting its odd part.
    Dividing j! inside Z/2^M is not legal.
    """
    integer(precision, 1, 10000, "2-adic precision")
    modulus = 1 << precision
    output, falling = [0]*precision, [1]
    for j in range(precision):
        fact = factorial(j)
        valuation = (fact & -fact).bit_length()-1
        scale = ((-1)**j * (1 << (j-valuation))
                 * pow(fact >> valuation, -1, modulus)) % modulus
        for k, coefficient in enumerate(falling):
            output[k] = (output[k]+scale*coefficient) % modulus
        following = [0]*(len(falling)+1)
        for k, coefficient in enumerate(falling):
            following[k] = (following[k]-j*coefficient) % modulus
            following[k+1] = (following[k+1]+coefficient) % modulus
        falling = following
    return tuple(output)


def carry_layout(bits, s):
    """Choose the smaller of the original width s and canonical width r+4."""
    _parameters(bits, s)
    canonical = _metadata(bits, s)["canonical_research_parameters"]
    remainder = bits-4*s
    if canonical and remainder+4 < s:
        return {"multiplier": 4, "width": remainder+4,
                "center_offset": -remainder, "previous_offset": -remainder-4,
                "shift_offset": 0, "canonical_constant_width": True}
    return {"multiplier": 1, "width": s,
            "center_offset": 0, "previous_offset": -1,
            "shift_offset": -s, "canonical_constant_width": canonical}


def carry_walsh(bits, s, frequency, *, precision=None, max_transitions=1_000_000):
    """Contract cyclic carry moments and return a residue, signed value, or cap.

    precision defaults to n+2, enough to recover the unique W in [-2^n,2^n].
    Smaller precision is only a congruence control, not approximate Walsh
    access. max_transitions=None runs the complete, potentially impractical
    algorithm. A cap charges boundary visits and every attempted transition;
    it is not a wall-clock or all-arithmetic instruction cap.
    """
    _parameters(bits, s)
    integer(frequency, 0, (1 << bits)-1, "Fourier frequency")
    if precision is None:
        precision = bits+2
    integer(precision, 1, 10000, "2-adic precision")
    if max_transitions is not None and (type(max_transitions) is not int or max_transitions < 1):
        raise ValueError("positive transition cap or None required")
    ring = UnramifiedBinaryRing(bits, precision)
    layout = carry_layout(bits, s)
    width, modulus = layout["width"], ring.modulus
    states = tuple((u, c) for u in range(precision)
                   for c in range(1-precision, precision))
    inverse_order = pow(layout["multiplier"], -1, bits)
    powers = []
    conjugate = ring.teichmuller(frequency)
    for _ in range(bits):
        row = [ring.one]
        for _ in range(1, precision):
            row.append(ring.multiply(row[-1], conjugate))
        powers.append(row)
        conjugate = ring.multiply(conjugate, conjugate)
    moment = [ring.zero for _ in range(precision)]
    transitions = boundaries = peak_states = 0

    def charge():
        nonlocal transitions
        if max_transitions is not None and transitions >= max_transitions:
            raise CarryWorkCap
        transitions += 1

    def boundary_values(prefix=(), total_u=0):
        if len(prefix) == width:
            yield prefix
            return
        for state in states:
            charge()
            if total_u+state[0] < precision:
                yield from boundary_values(prefix+(state,), total_u+state[0])

    def local(endpoint, lookup):
        center = (endpoint+layout["center_offset"]) % bits
        u, carry = lookup(center)
        previous = lookup((endpoint+layout["previous_offset"]) % bits)[1]
        shifted = lookup((endpoint+layout["shift_offset"]) % bits)[0]
        v = 2*carry-previous-u+shifted
        if v < 0 or u+v >= precision:
            return None
        degree = u+v
        original_index = (inverse_order*center) % bits
        return degree, comb(degree, u), powers[original_index][v]

    def next_states(window, accumulated):
        if (layout["center_offset"] == 0 and layout["previous_offset"] == -1
                and layout["shift_offset"] == -width):
            # Solve 0 <= v and u+v <= M-1-k before proposing the new carry.
            previous, shifted = window[-1][1], window[0][0]
            upper = min(precision-1, (precision-1-accumulated+previous-shifted)//2)
            for u in range(precision-accumulated):
                lower = max(1-precision, (previous+u-shifted+1)//2)
                for value in range(lower, upper+1):
                    yield u, value
        else:
            yield from states

    def finish(status, residue=None):
        signed = None
        if residue is not None and precision >= bits+2:
            signed = residue if residue <= 1 << bits else residue-modulus
            if not -(1 << bits) <= signed <= 1 << bits:
                raise ArithmeticError("completed residue is outside the Walsh interval")
        return {
            **_metadata(bits, s), "status": status, "frequency": frequency,
            "precision": precision, "modulus": modulus, "layout": layout,
            "field_modulus_coefficients": ring.field_modulus,
            "transition_cap": max_transitions, "transitions": transitions,
            "completed_boundaries": boundaries, "peak_dp_states": peak_states,
            "walsh_residue": residue, "walsh_value": signed,
            "full_precision": precision >= bits+2,
            "field_table_materialized": False, "native_completion_solver": False,
            "quantum_advantage_claimed": False, "practical_runtime_claimed": False,
        }

    try:
        for boundary in boundary_values():
            table = {(boundary, 0): ring.one}
            for endpoint in range(width, bits):
                following = {}
                for (window, accumulated), value in table.items():
                    for state in next_states(window, accumulated):
                        charge()
                        extended = window+(state,)

                        def lookup(position):
                            return extended[position-(endpoint-width)]

                        factor = local(endpoint, lookup)
                        if factor is None:
                            continue
                        added, local_binomial, power = factor
                        degree = accumulated+added
                        if degree >= precision or power == ring.zero:
                            continue
                        coefficient = ring.multiply(value, power)
                        coefficient *= local_binomial*comb(degree, added) % modulus
                        if coefficient == ring.zero:
                            continue
                        key = (extended[1:], degree)
                        following[key] = following.get(key, ring.zero)+coefficient
                table = {key: value for key, value in following.items() if value != ring.zero}
                peak_states = max(peak_states, len(table))
                if not table:
                    break
            for (window, accumulated), value in table.items():
                degree, coefficient = accumulated, value

                def lookup(position):
                    return boundary[position] if position < width else window[position-(bits-width)]

                for endpoint in range(width):
                    charge()
                    factor = local(endpoint, lookup)
                    if factor is None:
                        break
                    added, local_binomial, power = factor
                    degree += added
                    if degree >= precision:
                        break
                    coefficient = ring.multiply(coefficient, power)
                    coefficient *= local_binomial*comb(degree, added) % modulus
                else:
                    moment[degree] += coefficient
            boundaries += 1
    except CarryWorkCap:
        return finish("WORK_CAP")
    total = ring.zero
    for coefficient, value in zip(parity_polynomial(precision), moment):
        total += coefficient*value
    residue = ring.scalar(ring.one+((1 << bits)-1)*total)
    return finish("EXACT_WALSH" if precision >= bits+2 else "EXACT_CONGRUENCE", residue)


def exact_walsh_oracle(bits, s, frequency, *, max_transitions=1_000_000):
    """Sampler-compatible signed query; a work cap raises, never fabricates W.

    Set max_transitions=None explicitly for the uncapped mathematical
    algorithm. A transition cap is NOT the sampler's probabilistic ABORT.
    """
    result = carry_walsh(bits, s, frequency, max_transitions=max_transitions)
    if result["status"] != "EXACT_WALSH":
        raise CarryWorkCap("exact Walsh query exceeded its transition cap")
    return result["walsh_value"]


def build_carry_walsh_report(*, native_mod32=False):
    """Live finite controls and explicitly scoped asymptotic accounting."""
    controls = [carry_walsh(3, 1, a) for a in range(8)]
    controls.extend(carry_walsh(5, 1, a) for a in (0, 1, 2, 7))
    controls.append(carry_walsh(61, 14, 12345, max_transitions=100))
    if native_mod32:
        controls.append(carry_walsh(17, 3, 1, precision=5, max_transitions=8_000_000))
    root = Path(__file__).resolve().parents[1]
    sources = (
        "theorems/mersenne_carry_walsh.py", "tests/test_mersenne_carry_walsh.py",
        "theorems/mersenne_reciprocal_curve.py", "theorems/explicit_quadratic_opi.py",
        "theorems/balanced_codeword_filter.py", "research/MERSENNE_CARRY_WALSH_DRAFT.md",
    )
    return {
        "schema_version": 1,
        "status": "REVIEWED_LOCAL_POLYNOMIAL_CONSTRUCTION_WITH_CAPPED_IMPLEMENTATION",
        "scope": "signed local Walsh coefficients for canonical prime n, s=(n-3)//4",
        "review": "independent automated mathematical/static-code review by Jason; not human peer review",
        "theoretical_bit_time_upper": "O(n^45)",
        "theoretical_space_bits_upper": "O(n^21)",
        "canonical_carry_width_upper": 9,
        "asymptotic_scope": "written uniform algorithm; reference API currently restricts field degrees to 3..127",
        "full_precision_native_execution_completed": any(
            c["canonical_research_parameters"] and c["status"] == "EXACT_WALSH" for c in controls
        ),
        "canonical_reordered_execution_completed": any(
            c["canonical_research_parameters"] and c["layout"]["multiplier"] == 4
            and c["status"] != "WORK_CAP" for c in controls
        ),
        "native_completion_solver": False, "practical_runtime_claimed": False,
        "quantum_advantage_claimed": False, "novelty_established": False,
        "field_table_materialized": False,
        "native_mod32_requested": native_mod32,
        "source_hashes_sha256": {p: sha256((root/p).read_bytes()).hexdigest() for p in sources},
        "controls": controls,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--native-mod32", action="store_true",
                        help="also run the bounded n17 congruence control, NOT full Walsh evaluation")
    args = parser.parse_args(argv)
    payload = json.dumps(build_carry_walsh_report(native_mod32=args.native_mod32),
                         indent=2, sort_keys=True)+"\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.write_text(payload, encoding="ascii")


if __name__ == "__main__":
    main()
