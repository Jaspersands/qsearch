"""Controller boundary controls; opaque fixtures are not quantum simulations."""
from dataclasses import replace
from itertools import product
import random

import pytest

from theorems.phase_copy_statevector_backend import StateVectorPhaseSource
from theorems.polynomial_phase_copy_learning import LearningFrame, PhaseCopyController


def test_controller_enforces_its_own_cap_without_a_backend_cap():
    source = StateVectorPhaseSource(1049, 1, 2, (11, 7), rng=random.Random(91))
    controller = PhaseCopyController(1049, 1, 2, source, rng=random.Random(92))
    controller.budget = replace(controller.budget, copy_cap=1)
    result = controller.learn()
    assert result.status == "ABORT"
    assert result.ledger.drawn == source.draw_count == 1
    assert result.ledger.aborted_leaves == 1
    result.ledger.check_balance()


class OpaqueBranchFixture:
    """Forces one legal measurement branch, checking linear handle ownership."""
    fourier_convention = 1

    def __init__(self, *, mixed=False, lower_index=0):
        self.live = set()
        self.next_handle = 0
        self.merges = 0
        self.measured = 0
        self.mixed = mixed
        self.lower_index = lower_index

    def draw(self):
        self.next_handle += 1
        self.live.add(self.next_handle)
        return self.next_handle

    def consume(self, handle):
        assert handle in self.live, "returned a consumed quantum handle"
        self.live.remove(handle)

    def measure_all_but(self, handle, axis):
        self.consume(handle)
        assert axis == 0
        observed = int(self.mixed and self.measured != self.lower_index)
        self.measured += 1
        return (observed,), self.draw()

    def apply_known_phase(self, handle, correction):
        self.consume(handle)
        return self.draw()

    def shear_merge(self, handles, scales):
        self.merges += 1
        for handle in handles:
            self.consume(handle)
        return tuple((5,) if scale else (0,) for scale in scales), self.draw()


@pytest.mark.parametrize("mixed,lower_index", [(False, 0), (True, 0), (True, 5)])
def test_lower_degree_child_is_used_without_sde_and_with_translation(mixed, lower_index, monkeypatch):
    import theorems.weighted_two_erasure_cascade as cascade

    def unnecessary_sde(*args, **kwargs):
        raise AssertionError("a lower-degree child was already available")

    monkeypatch.setattr(cascade, "solve_bezout_sde_weights", unnecessary_sde)
    p, width, degree = 1000003, 2, 4
    initial = LearningFrame.initial(p, width, degree)
    rows = tuple(tuple(int(alpha == selected) for alpha in initial.indices)
                 for selected in ((3, 1), (2, 0)))
    frame = LearningFrame(p, width, degree, initial.known, rows)
    source = OpaqueBranchFixture(mixed=mixed, lower_index=lower_index)
    controller = PhaseCopyController(p, width, degree, source)
    handle, packet, leaves = controller._produce(frame, 0, object(), target=2)
    # The selected y=0 slice lost the cubic term. Keeping it still translates
    # its x^2 phase to (x+5)^2, whose linear coefficient must be retained.
    assert source.merges == 1
    assert controller.ledger.solver_calls == 0
    assert handle in source.live, "returned a consumed quantum handle"
    assert packet.coefficients[(2,)] == (0, 1)
    assert packet.coefficients[(1,)] == (0, 10)
    assert leaves == 1
    source.consume(handle)
    assert not source.live
    controller.ledger.used_in_relations += leaves
    controller.ledger.check_balance()


def test_small_field_closure_failure_is_not_sde_nonexistence():
    # Every five scalar columns over F5 have a nonempty zero subsum.
    # They fit inside the symmetric arity M=(r+1)((d-1)r+1)=8 at r1,d4.
    for columns in product(range(5), repeat=5):
        prefixes, value = {0: 0}, 0
        for end, column in enumerate(columns, 1):
            value = (value+column) % 5
            if value in prefixes:
                start = prefixes[value]
                witness = tuple(int(start <= j < end) for j in range(5))
                assert any(witness)
                assert sum(a*pow(s, 4, 5) for a, s in zip(columns, witness)) % 5 == 0
                break
            prefixes[value] = end
        else:
            raise AssertionError("five-step prefix sums must collide over F5")
