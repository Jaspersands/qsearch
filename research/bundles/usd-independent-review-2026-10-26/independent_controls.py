"""Small independent falsification controls, not a proof or scalable decoder.

All generated files stay next to this script. The reviewed bundle is read-only.
Run with: /opt/anaconda3/bin/python -B independent_controls.py
"""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "unambiguous-reduction-2026-10-26"
TOL = 2e-11


def close(actual, expected):
    error = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
    assert error < TOL, (error, actual, expected)
    return error


def matrix_sqrt(matrix):
    values, vectors = np.linalg.eigh(matrix)
    assert values.min() > -TOL
    return (vectors * np.sqrt(np.maximum(values, 0))) @ vectors.conj().T


def unequal_usd(characters, weights, probabilities, phases):
    """Explicit unitary dilation of a reciprocal-state USD contraction."""
    n = len(weights)
    source = np.sqrt(weights) * np.exp(1j * np.asarray(phases))
    # This is the input ensemble written in its Fourier eigenbasis.
    phi = source[:, None] * characters
    k = np.diag(np.sqrt(probabilities)) @ np.linalg.inv(phi)
    left = matrix_sqrt(np.eye(n) - k @ k.conj().T)
    right = matrix_sqrt(np.eye(n) - k.conj().T @ k)
    unitary = np.block([[k, left], [right, -k.conj().T]])
    unitary_error = close(unitary.conj().T @ unitary, np.eye(2*n))
    inputs = np.vstack([phi, np.zeros_like(phi)])
    outputs = unitary @ inputs
    unambiguity_error = close(outputs[:n], np.diag(np.sqrt(probabilities)))
    pbar = float(np.mean(probabilities))
    checks = []
    for s in range(n):
        character = characters[s].conj()
        a = inputs @ character / np.sqrt(n)
        lam = float(np.vdot(a, a).real)
        close(lam, n*weights[s])
        close(np.delete(a, s), 0)
        accepted = np.concatenate([np.sqrt(probabilities)*character, np.zeros(n)])
        b = unitary.conj().T @ accepted / np.sqrt(n*pbar)
        close(np.vdot(b, b), 1)
        fidelity = float(abs(np.vdot(a/np.sqrt(lam), b))**2)
        close(fidelity, pbar/lam)
        checks.append({"syndrome_index": s, "lambda": lam,
                       "joint_fidelity": fidelity,
                       "predicted": pbar/lam,
                       "dirty_workspace_probability": float(np.vdot(b[n:], b[n:]).real)})
    return {"states": n, "p_c": list(probabilities), "p_bar": pbar,
            "unitarity_max_error": unitary_error,
            "wrong_label_amplitude_max_error": unambiguity_error,
            "syndromes": checks}


def gf4_mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return result


def gf4_trace(a):
    result = a ^ gf4_mul(a, a)
    assert result in (0, 1)
    return result


def exact_unequal_and_workspace():
    gram = sp.Matrix([[1, sp.Rational(1, 2)], [sp.Rational(1, 2), 1]])
    d = sp.diag(sp.Rational(1, 4), sp.Rational(1, 2))
    assert (gram-d).det() == sp.Rational(1, 8)
    pbar = sp.trace(d)/2
    rows = []
    for sign in (1, -1):
        x = sp.Matrix([1, sign])
        lam = (x.T*gram*x)[0]/2
        clean = (x.T*d*gram.inv()*d*x)[0]/(2*pbar)
        rows.append({"character": [1, sign], "lambda": str(lam),
                     "joint_fidelity": str(pbar/lam),
                     "clean_workspace_probability": str(clean),
                     "dirty_workspace_probability": str(1-clean)})
    assert [r["joint_fidelity"] for r in rows] == ["1/4", "3/4"]
    assert [r["dirty_workspace_probability"] for r in rows] == ["2/3", "2/9"]
    return {"gram": [["1", "1/2"], ["1/2", "1"]],
            "p_c": ["1/4", "1/2"], "p_bar": str(pbar), "syndromes": rows}


def rref(matrix, q):
    a = np.array(matrix, dtype=int).copy() % q
    pivots = []
    row = 0
    for col in range(a.shape[1]):
        candidates = np.flatnonzero(a[row:, col])
        if not len(candidates):
            continue
        pivot = row + int(candidates[0])
        a[[row, pivot]] = a[[pivot, row]]
        a[row] = a[row]*pow(int(a[row, col]), -1, q) % q
        for other in range(a.shape[0]):
            if other != row:
                a[other] = (a[other] - a[other, col]*a[row]) % q
        pivots.append(col)
        row += 1
        if row == a.shape[0]:
            break
    return a, pivots


def row_basis(matrix, q):
    reduced, pivots = rref(matrix, q)
    return reduced[:len(pivots)]


def decode(transcript, basis, square, q):
    # Solve the actual linear relaxation, including inconsistency and nullity.
    pairs = np.asarray(transcript, dtype=int)
    sums = pairs.sum(axis=1) % q
    products = pairs.prod(axis=1) % q
    a = np.column_stack([-sums[:, None]*basis.T, square.T]) % q
    reduced, pivots = rref(np.column_stack([a, -products % q]), q)
    unknowns = a.shape[1]
    if unknowns in pivots or len(pivots) < unknowns:
        return None
    solution = reduced[:unknowns, -1]
    return tuple((solution[:len(basis)] @ basis % q).tolist())


def signed_pair_control(q, basis):
    basis = np.array(basis, dtype=int)
    k, m = basis.shape
    assert len(row_basis(basis, q)) == k
    square = row_basis([u*v % q for u in basis for v in basis], q)
    coefficients = np.array(list(product(range(q), repeat=k)), dtype=int)
    code = coefficients @ basis % q
    n = len(code)
    labels = {tuple(c): i for i, c in enumerate(code)}
    pairs = list(combinations(range(q), 2))
    incidence = np.array([[int(c == a)-int(c == b) for c in range(q)]
                          for a, b in pairs], dtype=int)
    transcripts = np.array(list(product(range(len(pairs)), repeat=m)), dtype=int)
    signed = np.ones((len(transcripts), n), dtype=np.int64)
    for i in range(m):
        signed *= incidence[transcripts[:, i, None], code[None, :, i]]
    accepted = np.zeros(len(transcripts), dtype=bool)
    valid_transcripts = np.any(signed != 0, axis=1)
    wrong = 0
    ambiguous = 0
    for t, row in enumerate(transcripts):
        decoded = decode([pairs[j] for j in row], basis, square, q)
        if decoded is None:
            ambiguous += int(valid_transcripts[t])
            continue
        accepted[t] = True
        d = labels[decoded]
        wrong += int(np.count_nonzero(np.delete(signed[t], d)))
    assert wrong == 0
    denominator = (q-1)**m
    gram_num = signed.T @ signed
    good_num = signed[accepted].T @ signed[accepted]
    assert np.array_equal(good_num, np.diag(np.diag(good_num)))
    expected_gram = np.array([[(-1)**np.count_nonzero(c-d)*(q-1)**(m-np.count_nonzero(c-d))
                               for d in code] for c in code], dtype=np.int64)
    assert np.array_equal(gram_num, expected_gram)
    successes = [Fraction(int(x), denominator) for x in np.diag(good_num)]
    pbar = sum(successes)/n
    assert pbar > 0
    tail = Fraction(0)
    e = Fraction(0)
    for c in code[1:]:
        weight = int(np.count_nonzero(c))
        zeros = np.flatnonzero(c == 0)
        shortening = len(square)-len(rref(square[:, zeros].T, q)[1]) if len(zeros) else len(square)
        tail += Fraction(1, (q-1)**weight)
        e += Fraction(q**shortening, (q-1)**weight)
    assert all(p >= 1-e for p in successes)

    # Complete the pair map to a unitary without assuming work is clean later.
    _, _, vh = np.linalg.svd(incidence.T.astype(float), full_matrices=True)
    null_vector = vh[q-1]
    local_columns = incidence/np.sqrt(q) + np.outer(null_vector, np.ones(q))/np.sqrt(q)
    close(local_columns.T @ local_columns, np.eye(q))
    _, _, vh = np.linalg.svd(local_columns.T, full_matrices=True)
    local_u = np.column_stack([local_columns, vh[q:].T])
    close(local_u.T @ local_u, np.eye(len(pairs)))
    transform = np.ones((1, 1))
    for _ in range(m):
        transform = np.kron(transform, local_u)
    physical_words = np.array(list(product(range(q), repeat=m)), dtype=int)
    physical_indices = np.ravel_multi_index(physical_words.T, (len(pairs),)*m)
    qft = np.exp(2j*np.pi*(physical_words @ physical_words.T)/q)/np.sqrt(q**m)
    source = np.all(physical_words != 0, axis=1).astype(float)/np.sqrt(denominator)
    qft_source = qft.conj().T @ source
    embedded_phi = np.zeros((len(transcripts), n), dtype=complex)
    word_index = {tuple(w): i for i, w in enumerate(physical_words)}
    for d, c in enumerate(code):
        embedded_phi[physical_indices, d] = [qft_source[word_index[tuple((w-c) % q)]]
                                             for w in physical_words]
    close(transform @ embedded_phi, signed/np.sqrt(denominator))
    syndromes = []
    for s in coefficients:
        character = np.exp(-2j*np.pi*(coefficients @ s)/q)
        a = embedded_phi @ character/np.sqrt(n)
        lam = float(np.vdot(a, a).real)
        post = signed @ character/np.sqrt(denominator*n*float(pbar))
        post[~accepted] = 0
        b = transform.T @ post
        close(np.vdot(b, b), 1)
        fidelity = float(abs(np.vdot(a/np.sqrt(lam), b))**2)
        close(fidelity, float(pbar)/lam)
        fiber = np.all(physical_words != 0, axis=1) & np.all(physical_words @ basis.T % q == s, axis=1)
        output_clean = qft @ b[physical_indices]
        valid_clean = float(np.sum(abs(output_clean[fiber])**2))
        assert valid_clean + TOL >= fidelity
        syndromes.append({"s": s.tolist(), "lambda": lam, "joint_fidelity": fidelity,
                          "valid_output_with_blank_ancilla": valid_clean,
                          "dirty_ancilla_probability": float(1-np.sum(abs(b[physical_indices])**2))})
    return {"q": q, "basis": basis.tolist(), "schur_dimension": len(square),
            "pair_transcripts": len(transcripts), "ensemble_transcripts": int(valid_transcripts.sum()),
            "ensemble_transcripts_rejected": ambiguous,
            "wrong_label_nonzero_integer_amplitudes": wrong,
            "p_c": [str(x) for x in successes], "p_bar": str(pbar),
            "A_tail": str(tail), "E": str(e), "syndromes": syndromes}


def counterexamples():
    n = 8
    u = sp.eye(n)
    u[4:, 4:] = sp.eye(4)-sp.ones(4)/2
    assert u.T*u == sp.eye(n)
    diag = sp.Matrix([u[i, i] for i in range(n)])
    pbar = sum(v*v for v in diag)/n
    fidelity = sum(u.T*diag)**2/(n*n*pbar)
    assert (pbar, fidelity) == (sp.Rational(5, 8), sp.Rational(1, 10))
    plus = sp.ones(2, 1)/sp.sqrt(2)
    dephased_fidelity = (plus.T*(sp.eye(2)/2)*plus)[0]
    assert dephased_fidelity == sp.Rational(1, 2)
    incidence = sp.Matrix([[1, -1, 0], [1, 0, -1], [0, 1, -1]])
    signed_gram = incidence.T*incidence/2
    unsigned = incidence.applyfunc(abs)
    assert signed_gram[0, 1] == -sp.Rational(1, 2)
    assert (unsigned.T*unsigned/2)[0, 1] == sp.Rational(1, 2)
    assert signed_gram*sp.ones(3, 1) == sp.zeros(3, 1)
    r = sp.symbols("r", positive=True)
    high_success = (1+(1-2/r)**2)/2
    low_fidelity = sp.simplify((1-(1-2/r))**2/(4*high_success))
    assert sp.simplify(low_fidelity-1/(r*r*high_success)) == 0
    assert sp.limit(high_success, r, sp.oo) == 1
    assert sp.limit(low_fidelity, r, sp.oo) == 0
    return {"wrong_answer_decoder": {"p_bar": str(pbar), "fidelity": str(fidelity)},
            "near_perfect_wrong_answer_family": {"states": "2r", "decoder": "diag(I_r, I_r-2J_r/r)",
                                                 "p_bar": str(high_success), "fidelity": str(low_fidelity),
                                                 "r_100_p_bar": str(high_success.subs(r, 100)),
                                                 "r_100_fidelity": str(low_fidelity.subs(r, 100))},
            "measure_retained_label": {"ensemble": "two orthogonal states, perfect decoder",
                                       "correct_coherent_fidelity": "1", "dephased_fidelity": str(dephased_fidelity)},
            "drop_pair_signs": {"q": 3, "correct_off_diagonal_gram": "-1/2",
                                "unsigned_off_diagonal_gram": "1/2", "isometry_possible": False},
            "singular_orbit": {"q": 3, "length": 1, "null_vector": [1, 1, 1],
                               "lambda_zero": "0", "maximum_p_bar": "0"}}


def hashes():
    return {p.name: sha256(p.read_bytes()).hexdigest() for p in sorted(SOURCE.iterdir()) if p.is_file()}


def main():
    before = hashes()
    recorded = json.loads((SOURCE / "receipt.json").read_text())
    local_recorded = {Path(path).name: digest for path, digest in recorded["sha256"].items()
                      if Path(path).parts[0] == SOURCE.name}
    assert len(local_recorded) == 5
    assert all(before[name] == digest for name, digest in local_recorded.items())
    tmp = ROOT / "tmp"
    tmp.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
               TMPDIR=str(tmp))
    command = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
               "-W", "error", "--rootdir", str(ROOT), str(SOURCE / "test_usd_reduction.py")]
    proc = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, check=False)
    (ROOT / "source-pytest.txt").write_text(proc.stdout+proc.stderr)
    assert proc.returncode == 0, proc.stdout+proc.stderr
    elements = np.array(list(product(range(3), repeat=2)))
    chars3 = np.exp(2j*np.pi*(elements @ elements.T)/3)
    chars4 = np.array([[(-1)**gf4_trace(gf4_mul(s, c)) for c in range(4)] for s in range(4)])
    result = {
        "scope": "bounded independent controls; numerical checks are not proofs",
        "source_tests": {"command": command, "returncode": proc.returncode, "output": proc.stdout.strip()},
        "exact_unequal_workspace": exact_unequal_and_workspace(),
        "f3_squared_unequal": unequal_usd(chars3, np.arange(1, 10)/45, np.arange(1, 10)/50,
                                           np.arange(9)/7),
        "f4_trace_characters": unequal_usd(chars4, np.arange(1, 5)/10, np.arange(1, 5)/20,
                                          np.arange(4)/5),
        "pair_controls": [signed_pair_control(3, [[1,1,1,1,1,1], [0,0,1,1,2,2]]),
                          signed_pair_control(5, [[1,1,1]])],
        "counterexamples": counterexamples(),
        "source_hashes_before": before,
        "source_hashes_after": hashes(),
        "five_local_recorded_receipt_hashes_match": True,
    }
    assert result["source_hashes_before"] == result["source_hashes_after"]
    result["source_unchanged"] = True
    (ROOT / "controls.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"source_tests": result["source_tests"]["output"],
                      "source_unchanged": True,
                      "pair_controls": [{k: c[k] for k in ("q", "pair_transcripts", "p_bar", "E",
                                                           "wrong_label_nonzero_integer_amplitudes")}
                                        for c in result["pair_controls"]],
                      "report": str(ROOT / "controls.json")}, indent=2))


if __name__ == "__main__":
    main()
