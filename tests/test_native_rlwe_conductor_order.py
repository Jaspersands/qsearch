import itertools

import sympy as sp

from native_rlwe_conductor_order import audit_conductor_order, run_controls
from native_rlwe_quaternion_kernel import (
    add, conjugate, kernel_member, mul, multiplication_matrix,
    quaternion_multiply, reduced_norm,
)


def test_conductor_left_action_preserves_native_graph_without_hamilton_unit():
    m,q = (1,0),3
    row = audit_conductor_order(m,q)
    assert row["original_physical_metric_preserved_exactly"]
    rho = (1,0)
    for x in itertools.product(range(-2,3),repeat=4):
        pair = (x[:2],x[2:])
        if kernel_member(pair,m,q):
            assert kernel_member(quaternion_multiply(((0,0),(q,0)),pair,rho),m,q)
    assert not kernel_member(quaternion_multiply(((0,0),(1,0)),(m,(1,0)),rho),m,q)


def test_local_principal_certificate_does_not_promote_contained_ideal_to_global():
    m,q = (1,0),3
    row = audit_conductor_order(m,q)
    local = row["local_principality"]
    assert local["certificate_at_primes_dividing_q_supplied"]
    assert int(local["contained_sublattice_global_index_hex"],16)==4
    assert not local["contained_sublattice_equals_full_graph_globally"]
    assert not row["global_principality"]["principal_over_THIS_conductor_order"]
    M = multiplication_matrix(m)
    B = M.row_join(-q*sp.eye(2)).col_join(sp.eye(2).row_join(q*M.T))
    assert abs(B.det())==q**2*4
    exceptional = audit_conductor_order((1,1),3)
    assert not exceptional["local_principality"]["certificate_at_primes_dividing_q_supplied"]
    assert exceptional["local_principality"]["failed_certificate_is_not_a_local_nonprincipality_proof"]


def test_zero_ratio_is_the_actual_principal_control():
    row = audit_conductor_order((0,0,0,0),11)
    assert row["global_principality"]["principal_over_THIS_conductor_order"]
    assert row["local_principality"]["contained_sublattice_equals_full_graph_globally"]
    j = ((0,0,0,0),(1,0,0,0))
    for i in range(4):
        e = tuple(int(k==i) for k in range(4))
        assert quaternion_multiply((e,(0,0,0,0)),j,(1,0,0,0))==((0,0,0,0),e)
        assert quaternion_multiply(((0,0,0,0),tuple(11*v for v in e)),j,(1,0,0,0))==(tuple(-11*v for v in e),(0,0,0,0))


def test_real_central_units_are_not_misclassified_as_norm_one_units():
    u = (1,1,0,-1)  # 1+sqrt(2), norm -1 over the real quadratic field.
    nr = reduced_norm((u,(0,0,0,0)),(1,0,0,0))
    assert nr==(3,2,0,-2)
    assert multiplication_matrix(nr).det()==1
    assert sum(v*v for v in u)==3
    inverse = (-1,1,0,-1)
    assert mul(u,inverse)==(1,0,0,0)
    assert conjugate(u)==u
    assert not kernel_member((u,(0,0,0,0)),(1,0,0,0),3)


def test_native_exact_metric_but_nonprincipal_gate_and_bounded_units():
    report = run_controls()
    native = report["same_saved_native_d64_kernel"]
    assert native["original_physical_metric_preserved_exactly"]
    assert native["local_principality"]["certificate_at_primes_dividing_q_supplied"]
    assert not native["global_principality"]["principal_over_THIS_conductor_order"]
    assert report["bounded_d4_unit_check"]["mixed_block_units"]==0
    assert report["bounded_d4_unit_check"]["ambient_units"]>16
    assert report["published_dependency"]["not_Weber_class_number_one_conjecture"]
    assert native["ambient_order_saturation"]["M_dependent_overorder_choice_not_ruled_out"]
    assert not report["claim_gate"]["speedup_claim_allowed"]
    assert not native["all_quaternion_orders_or_short_element_algorithms_ruled_out"]


def test_ambient_saturation_erases_generic_graph_but_not_exceptional_hamilton_graph():
    generic = audit_conductor_order((1,0),3)
    assert generic["ambient_order_saturation"]["O_0_times_native_graph_equals_O_0"]
    # (M,1) and j*(M,1) span BOTH native blocks modulo q, not just the graph.
    m,q = (1,0),3
    alpha = (m,(1,0))
    jalpha = quaternion_multiply(((0,0),(1,0)),alpha,(1,0))
    for target in (((1,0),(0,0)),((0,0),(1,0))):
        r = tuple((2*v) % q for v in add(target[1],mul(conjugate(m),target[0])))
        s = tuple((v-w) % q for v,w in zip(mul(m,r),target[0]))
        g = add(mul(r,alpha[0]),mul(s,jalpha[0]))
        f = add(mul(r,alpha[1]),mul(s,jalpha[1]))
        assert all((v-w) % q==0 for block,out in zip(target,(g,f)) for v,w in zip(block,out))
    exceptional = audit_conductor_order((1,1),3)
    assert not exceptional["ambient_order_saturation"]["O_0_times_native_graph_equals_O_0"]
