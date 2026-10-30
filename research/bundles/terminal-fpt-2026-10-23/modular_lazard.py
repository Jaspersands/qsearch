"""Prime-power specialization of the existing Dynkin inverse-BCH compiler.

Known construction, not a new group algorithm. The caller verifies primality
and the exponent-dividing-p^e/class promises. No enumeration in p, hidden oracle, or
target coordinates. Symbolic cost is exponential in class, not polynomial.
"""

from dataclasses import dataclass
from functools import lru_cache


class Tensor:
    def __init__(self, prime, degree, exponent=1):
        if (type(prime) is not int or type(degree) is not int
                or type(exponent) is not int or exponent < 1
                or not 1 <= degree < prime):
            raise ValueError("caller-verified prime p and 1 <= class < p required")
        self.p, self.c = prime**exponent, degree

    def add(self, a, b, scale=1):
        out = dict(a)
        for word, value in b.items():
            value = (out.get(word, 0) + scale*value) % self.p
            if value:
                out[word] = value
            else:
                out.pop(word, None)
        return out

    def mul(self, a, b):
        out = {}
        for u, x in a.items():
            for v, y in b.items():
                if len(u)+len(v) <= self.c:
                    word = u+v
                    out[word] = (out.get(word, 0)+x*y) % self.p
        return {w: a for w, a in out.items() if a}

    def exp(self, a):
        if a.get((), 0):
            raise ValueError("positive-degree exponential required")
        out = term = {(): 1}
        for j in range(1, self.c+1):
            term = self.mul(term, a)
            term = {w: x*pow(j, -1, self.p) % self.p for w, x in term.items()}
            out = self.add(out, term)
        return out

    def log(self, a):
        if a.get(()) != 1:
            raise ValueError("constant-one logarithm required")
        x = self.add(a, {(): 1}, -1)
        out, term = {}, {(): 1}
        for j in range(1, self.c+1):
            term = self.mul(term, x)
            out = self.add(out, term, (-1)**(j+1)*pow(j, -1, self.p))
        return out

    def power(self, a, scalar):
        return self.exp({w: x*scalar % self.p for w, x in self.log(a).items()
                         if x*scalar % self.p})

    def nested(self, word):
        if len(word) == 1:
            return {word: 1}
        left, right = {word[:1]: 1}, self.nested(word[1:])
        return self.add(self.mul(left, right), self.mul(right, left), -1)


def target(operation, degree):
    if operation == "add":
        return {(0,): 1, (1,): 1}
    if operation == "bracket":
        return {(0, 1): 1, (1, 0): -1} if degree >= 2 else {}
    raise ValueError("operation must be add or bracket")


def instruction_cap(degree):
    if type(degree) is not int or degree < 1:
        raise ValueError("positive class bound required")
    return 7*(2**(degree+1)-2)+5


@dataclass(frozen=True)
class Certificate:
    prime: int
    degree: int
    operation: str
    instructions: tuple
    output: int
    stages: tuple
    exponent: int = 1

    def verify(self):
        algebra = Tensor(self.prime, self.degree, self.exponent)
        desired = algebra.add({}, target(self.operation, self.degree))
        values = [{(): 1}, algebra.exp({(0,): 1}), algebra.exp({(1,): 1})]
        if len(self.instructions) > instruction_cap(self.degree):
            raise ValueError("word exceeds the constructive instruction cap")
        for step in self.instructions:
            if not isinstance(step, tuple) or len(step) != 3:
                raise ValueError("malformed instruction")
            kind, i, j = step
            if type(i) is not int or not 0 <= i < len(values):
                raise ValueError("instruction must reference an earlier value")
            if kind == "mul" and type(j) is int and 0 <= j < len(values):
                value = algebra.mul(values[i], values[j])
            elif kind == "pow" and type(j) is int and 0 <= j < algebra.p:
                value = algebra.power(values[i], j)
            else:
                raise ValueError("invalid multiply or noncanonical power")
            values.append(value)
        if type(self.output) is not int or not 0 <= self.output < len(values):
            raise ValueError("invalid output reference")
        if len(self.stages) != self.degree:
            raise ValueError("one stage per homogeneous degree required")
        for d, pair in enumerate(self.stages, 1):
            if (not isinstance(pair, tuple) or len(pair) != 2 or pair[0] != d
                    or type(pair[1]) is not int or not 0 <= pair[1] < len(values)):
                raise ValueError("malformed correction stage")
            actual = algebra.log(values[pair[1]])
            if {w: a for w, a in actual.items() if len(w) <= d} != {
                    w: a for w, a in desired.items() if len(w) <= d}:
                raise ValueError("filtration correction failed")
        if self.stages[-1][1] != self.output or values[self.output] != algebra.exp(desired):
            raise ValueError("wrong final inverse-BCH operation")

    def evaluate(self, left, right, identity, multiply):
        """Evaluate only the supplied public word; setup verification is separate."""
        values, calls = [identity, left, right], 0

        def mul(a, b):
            nonlocal calls
            calls += 1
            return multiply(a, b)

        for kind, i, j in self.instructions:
            if kind == "mul":
                out = mul(values[i], values[j])
            else:
                out, base, exponent = identity, values[i], j
                while exponent:
                    if exponent & 1:
                        out = mul(out, base)
                    base = mul(base, base)
                    exponent >>= 1
            values.append(out)
        return values[self.output], calls

    def multiplication_cap(self):
        return sum(1 if op == "mul" else 2*(self.prime**self.exponent).bit_length()
                   for op, _, _ in self.instructions)


@lru_cache(maxsize=None, typed=True)
def compile_word(prime, degree, operation, exponent=1):
    algebra = Tensor(prime, degree, exponent)
    modulus = algebra.p
    desired = algebra.add({}, target(operation, degree))
    values = [{(): 1}, algebra.exp({(0,): 1}), algebra.exp({(1,): 1})]
    instructions, interned, nested = [], {}, {}

    def append(step):
        if step not in interned:
            kind, i, j = step
            value = algebra.mul(values[i], values[j]) if kind == "mul" else algebra.power(values[i], j)
            interned[step] = len(values)
            instructions.append(step)
            values.append(value)
        return interned[step]

    def mul(i, j):
        return j if i == 0 else i if j == 0 else append(("mul", i, j))

    def power(i, scalar):
        scalar %= modulus
        return 0 if i == 0 or scalar == 0 else i if scalar == 1 else append(("pow", i, scalar))

    def commutator(i, j):
        if i == j or i == 0 or j == 0:
            return 0
        return mul(mul(mul(i, j), power(i, -1)), power(j, -1))

    def group_nested(word):
        if word not in nested:
            nested[word] = word[0]+1 if len(word) == 1 else commutator(word[0]+1, group_nested(word[1:]))
        return nested[word]

    result = mul(1, 2) if operation == "add" else commutator(1, 2)
    stages = []
    for d in range(1, degree+1):
        residual = algebra.add(algebra.log(values[result]), desired, -1)
        if any(len(w) < d for w in residual):
            raise ArithmeticError("lost an earlier correction")
        part = {w: a for w, a in residual.items() if len(w) == d}
        projection = {}
        for word, a in sorted(part.items()):
            bracket = algebra.nested(word)
            coefficient = a*pow(d, -1, modulus) % modulus
            projection = algebra.add(projection, bracket, coefficient)
            if bracket:
                result = mul(result, power(group_nested(word), -coefficient))
        if projection != part:
            raise ArithmeticError("Dynkin projection failed")
        stages.append((d, result))
    certificate = Certificate(prime, degree, operation, tuple(instructions), result, tuple(stages), exponent)
    certificate.verify()
    return certificate
