"""Exact binary permutation semantics only; no circuit or source proof.

Promises: prime is verified, bracket is a deterministic genuine Lie bracket
of class at most nilpotency_class < prime, and section and positive weights
describe the supplied section/dilation. Shape checks do not prove these
promises. The section need not be a homomorphism. No field enumeration or
truth-table backend is used; work depends on dimensions, class and bit sizes.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

from theorems.uniform_bch_rees import Bracket, Vector, bch_via_ode


@dataclass(frozen=True)
class GuardedBCHPermutation:
    """Fixed public parameters for a controlled right translation.

    Limb 0 occupies the least significant b = bit_length(p-1) bits.
    All in-width words are accepted, including noncanonical limbs >= p.
    Out-of-width words are malformed registers, not padded encodings.
    Control dimension zero is allowed for the trivial quotient.
    """

    prime: int
    nilpotency_class: int
    group_dimension: int
    control_dimension: int
    section: Callable[[Vector], Sequence[int]]
    weights: tuple[int, ...]
    scale: int
    bracket: Bracket

    def __post_init__(self) -> None:
        if type(self.prime) is not int or self.prime < 2:
            raise ValueError("a supplied verified prime is required")
        if (type(self.nilpotency_class) is not int
                or not 1 <= self.nilpotency_class < self.prime):
            raise ValueError("require 1 <= nilpotency_class < prime")
        if type(self.group_dimension) is not int or self.group_dimension < 1:
            raise ValueError("positive group dimension required")
        if (type(self.control_dimension) is not int
                or not 0 <= self.control_dimension <= self.group_dimension):
            raise ValueError("require 0 <= control dimension <= group dimension")
        if type(self.scale) is not int or not 0 <= self.scale < self.prime:
            raise ValueError("canonical scale required")
        if not callable(self.section) or not callable(self.bracket):
            raise ValueError("section and bracket callbacks required")
        try:
            weights = tuple(self.weights)
        except TypeError as exc:
            raise ValueError("positive integer weights required") from exc
        if len(weights) != self.group_dimension or any(
            type(w) is not int or w < 1 for w in weights
        ):
            raise ValueError("one positive integer weight per group coordinate required")
        object.__setattr__(self, "weights", weights)

    @property
    def limb_bits(self) -> int:
        return (self.prime - 1).bit_length()

    def pack(self, limbs: Sequence[int], *, control: bool = False) -> int:
        """Pack raw b-bit limbs without reducing them modulo p."""
        dimension = self.control_dimension if control else self.group_dimension
        limbs = tuple(limbs)
        if len(limbs) != dimension or any(
            type(v) is not int or not 0 <= v < 1 << self.limb_bits for v in limbs
        ):
            raise ValueError("raw b-bit limbs of the stated register dimension required")
        return sum(v << (i * self.limb_bits) for i, v in enumerate(limbs))

    def unpack(self, word: int, *, control: bool = False) -> Vector:
        """Decode a fixed-width word, preserving noncanonical field limbs."""
        dimension = self.control_dimension if control else self.group_dimension
        if type(word) is not int or not 0 <= word < 1 << (self.limb_bits * dimension):
            raise ValueError("integer within the register width required")
        mask = (1 << self.limb_bits) - 1
        return tuple((word >> (i * self.limb_bits)) & mask for i in range(dimension))

    def permutation(self, control: int, target: int, *, inverse: bool = False) -> int:
        """P_u(x) = BCH(x, -Delta_s(section(u))); inverse uses +Delta_s.

        Scale zero and noncanonical controls/targets act as the identity.
        In particular, scale zero never evaluates section, dilation or BCH.
        """
        u = self.unpack(control, control=True)
        x = self.unpack(target)
        if self.scale == 0 or any(v >= self.prime for v in u + x):
            return target
        try:
            value = tuple(self.section(u))
        except TypeError as exc:
            raise ValueError("section must return a canonical group vector") from exc
        if len(value) != self.group_dimension or any(
            type(v) is not int or not 0 <= v < self.prime for v in value
        ):
            raise ValueError("section must return a canonical group vector")
        sign = 1 if inverse else -1
        translation = tuple(sign * v * pow(self.scale, w, self.prime) % self.prime
                            for v, w in zip(value, self.weights))
        return self.pack(bch_via_ode(
            x, translation, prime=self.prime,
            nilpotency_class=self.nilpotency_class, bracket=self.bracket,
        ))

    def lift(
        self, control: int, target: int, auxiliary: int = 0, *, inverse: bool = False,
    ) -> tuple[int, int, int]:
        """Return (control, target, auxiliary) after the reversible lift.

        Forward: XOR P(target) into auxiliary; SWAP; XOR P^-1(target)
        into auxiliary. Fresh auxiliary zero finishes zero with target P(x).
        Arbitrary auxiliary need not clean, but the gate composition remains
        bijective. Its inverse reverses the gates, not just the translation.
        """
        self.unpack(control, control=True)
        self.unpack(target)
        self.unpack(auxiliary)
        if inverse:
            auxiliary ^= self.permutation(control, target, inverse=True)
            target, auxiliary = auxiliary, target
            auxiliary ^= self.permutation(control, target)
        else:
            auxiliary ^= self.permutation(control, target)
            target, auxiliary = auxiliary, target
            auxiliary ^= self.permutation(control, target, inverse=True)
        return control, target, auxiliary
