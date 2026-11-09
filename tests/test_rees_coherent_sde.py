"""Tests for theorems/rees_coherent_sde.py (coherent linear-grade SDE solve).

Exhaustive over all canonical inputs for small (p, g), sampled beyond.
AI-checked, pending human review.
"""
import math
import os

import numpy as np
import pytest

from theorems.rees_coherent_sde import (STATUS, CoherentSDE, Macro, Prog, all_inputs,
                                        canonical_witness, canonical_witness_batch,
                                        check_circuit, closed_form_macros, closed_form_qubits,
                                        closed_form_toffoli, count_row, exhaustive_check,
                                        inverse_exponent, is_canonical_bruteforce,
                                        sampled_check, structured_inputs)

EXHAUSTIVE = [(3, 1, 1), (3, 1, 3), (5, 1, 3), (7, 1, 5), (3, 2, 1), (3, 2, 3), (5, 2, 1),
              (5, 2, 3), (7, 2, 1), (7, 2, 5), (3, 3, 3)]


def _all_ok(r):
    return (r["output_equals_canonical"] and r["inputs_restored"] and r["workspace_clean"]
            and r["witness_nonzero"] and r["equation_holds"] and r["canonical_padding_free"])


@pytest.mark.parametrize("p,g,d", EXHAUSTIVE)
def test_exhaustive(p, g, d):
    r = exhaustive_check(p, g, d)
    assert r["inputs"] == p**(g*(g+1))
    assert _all_ok(r), r


@pytest.mark.skipif(not os.environ.get("REES_SLOW"), reason="set REES_SLOW=1 (~25 s)")
@pytest.mark.parametrize("p,g,d", [(11, 2, 3), (13, 2, 5)])
def test_exhaustive_slow(p, g, d):
    r = exhaustive_check(p, g, d)
    assert r["inputs"] == p**(g*(g+1)) and _all_ok(r), r


@pytest.mark.parametrize("p,g,d", [(5, 3, 3), (7, 3, 5), (11, 2, 3)])
def test_sampled(p, g, d):
    r = sampled_check(p, g, d, n=2048, seed=p+g)
    assert _all_ok(r), r


def test_reference_matches_definition_and_bruteforce():
    for p, g, d in [(3, 2, 3), (5, 2, 3)]:
        A = all_inputs(p, g)
        if len(A) > 3000:
            A = A[np.random.default_rng(0).choice(len(A), 3000, replace=False)]
        sb = canonical_witness_batch(p, A, d)
        for n in range(len(A)):
            cols = [tuple(int(x) for x in A[n, :, c]) for c in range(g+1)]
            s, y, j = canonical_witness(p, cols, d)
            assert list(sb[n]) == s
            assert is_canonical_bruteforce(p, cols, y)
            assert y[j] == 1 and all(v == 0 for v in y[j+1:])


def test_rank_deficient_cases_explicit():
    p, d = 7, 5
    e = inverse_exponent(p, d)
    assert e == 5
    # zero first column -> j* = 0, s = e_0
    assert canonical_witness(p, [(0, 0), (1, 2), (3, 4)], d)[0] == [1, 0, 0]
    # repeated column -> j* = 1, y = (-1, 1, 0)
    s, y, j = canonical_witness(p, [(1, 2), (1, 2), (0, 1)], d)
    assert j == 1 and y == [6, 1, 0] and s == [pow(6, e, p), 1, 0]
    # full rank prefix -> j* = g
    s, y, j = canonical_witness(p, [(1, 0), (0, 1), (2, 3)], d)
    assert j == 2 and y == [5, 4, 1]


def test_mutations_are_detected():
    p, g, d = 5, 2, 3
    A = all_inputs(p, g)
    circ = CoherentSDE(p, g, d)
    saved = circ.prog
    # drop one Fredkin from the forward pass only
    i = next(i for i in range(len(saved)-2)
             if all(isinstance(x, tuple) for x in saved[i:i+3]) and saved[i][0] == "cx"
             and saved[i+1][0] == "ccx" and saved[i+2] == saved[i] and saved[i+1][1][1] == saved[i][1][1])
    circ.prog = Prog(saved[:i]+saved[i+3:])
    assert not check_circuit(circ, A)["output_equals_canonical"]
    # wrong sign on one output
    pr = Prog(saved)
    j = next(j for j, it in enumerate(pr) if isinstance(it, Macro) and it.kind == "add_scaled")
    pr[j] = Macro("add_scaled", 1, pr[j].args)
    circ.prog = pr
    assert not check_circuit(circ, A)["output_equals_canonical"]
    circ.prog = saved
    assert _all_ok(check_circuit(circ, A))


def test_inputs_never_targeted_and_copy_stage_writes_only_output():
    circ = CoherentSDE(7, 3, 5)
    inputs = {w for col in circ.L for r in col for w in r}
    outputs = {w for r in circ.S for w in r}
    for it in circ.prog:
        tgt = set(it.args[0]) if isinstance(it, Macro) else {it[1][-1]}
        assert not tgt & inputs
    allowed = outputs | set(circ.anc.all) | {w for r in circ.free for w in r}
    for it in circ.C:
        tgt = set(it.args[0]) if isinstance(it, Macro) else {it[1][-1]}
        assert tgt <= allowed      # C writes S, the shared ancillas and its own chain temps only


@pytest.mark.parametrize("p,g,d", [(3, 2, 3), (5, 3, 3), (7, 4, 5), (13, 3, 5), (101, 4, 3),
                                   (65537, 3, 5), (2**61-1, 2, 17)])
def test_counts_match_closed_forms(p, g, d):
    r = count_row(p, g, d)
    assert r["toffoli_matches"] and r["macros_match"] and r["qubits_match"], r
    b = r["b"]
    # every product costs exactly 40b^2+2b Toffoli; the products dominate
    assert r["gates"]["ccx"] >= r["add_product"]*(40*b*b+2*b)


def test_emitted_counts_equal_program_counts():
    circ = CoherentSDE(7, 2, 5)
    gates = circ.flatten()
    c = circ.counts()["gates"]
    assert len(gates) == c["total"]
    assert sum(1 for n, _ in gates if n == "ccx") == c["ccx"]


def test_macro_closed_form_values():
    m = closed_form_macros(7, 2, 5)
    # I_7 = chain(5) = 2 sq + 1 mul; n_F = 10 + 3 + 12 = 25; E_e = chain(5) = 3
    assert m == {"I_p": 3, "E_e": 3, "products_F": 25, "add_product": 2*25+2*3*3, "add_scaled": 3}
    assert closed_form_qubits(7, 2, 5) == CoherentSDE(7, 2, 5).nw
    assert closed_form_toffoli(7, 2, 5) == CoherentSDE(7, 2, 5).counts()["gates"]["ccx"]


def test_kappa_one_required():
    with pytest.raises(ValueError):
        CoherentSDE(7, 2, 3)        # gcd(3, 6) = 3
    with pytest.raises(ValueError):
        CoherentSDE(5, 2, 2)


def test_status_gates_false():
    assert STATUS["coherent_receiver_implemented"] is False
    assert STATUS["general_sde_implemented"] is False
    assert STATUS["speedup_claim_allowed"] is False
    assert STATUS["coherent_higher_kappa_sde_implemented"] is False


def test_structured_inputs_hit_all_jstar():
    p, g, d = 7, 3, 5
    A = structured_inputs(p, g, 2048, seed=1)
    js = set()
    for n in range(0, 2048, 4):
        js.add(canonical_witness(p, [tuple(int(x) for x in A[n, :, c]) for c in range(g+1)], d)[2])
    assert js == set(range(g+1))
