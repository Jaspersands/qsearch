"""Exact physical-Pauli pullback through an explicit verified linear HDQI decoder."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "hdqi-output-sampling-2026-10-24"))
import commuting_linear as linear
d = linear.o.d


def pullback(model, decoder, observable):
    d.validate_pauli(model.n, observable)
    if not isinstance(decoder, linear.LinearDecoder):
        raise ValueError("an explicit linear decoder matrix is required")
    if decoder.n != model.n or decoder.m != model.pilot.m:
        raise ValueError("decoder dimensions do not match")
    linear.LinearDecoder.create(model, decoder.columns)
    q = observable[0] | (observable[1] << model.n)
    h = decoder(q)
    if model.label(h) != q:
        return None

    def phase(y):
        value = d.multiply(d.dagger(model.ordered(y ^ h)),
                           d.multiply(observable, model.ordered(y)))
        if value[:2] != (0, 0):
            raise ArithmeticError("non-scalar overlap after a valid syndrome match")
        return value[2]

    p, w = phase(0), 0
    for i in range(model.pilot.m):
        change = (phase(1 << i)-p) % 4
        if change % 2:
            raise ArithmeticError("Pauli translation phase is not affine binary")
        w |= (change//2) << i
    d.validate_pauli(model.pilot.m, (h, w, p))
    return h, w, p
