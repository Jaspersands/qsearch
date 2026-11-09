"""Exact finite Fock operator controls, not a quantum/cutoff implementation.

Sage algebra: /opt/anaconda3/envs/qsearch-cas/bin/python.
"""
import json
from pathlib import Path
from sage.all import (QQ, QQbar, binomial, block_diagonal_matrix, diagonal_matrix,
                      factorial, identity_matrix, matrix, vector)

F = QQbar
sqrt2 = F(2).sqrt()
c, s = sqrt2/2, sqrt2/2


def beamsplitter(total, cosine, sine):
    """Symmetric power of exp(theta(a†b-b†a)); basis (n_a,total-n_a)."""
    B = matrix(F, total+1, total+1)
    for na in range(total+1):
        nb = total-na
        for chosen_a in range(na+1):
            for chosen_b in range(nb+1):
                out_a = chosen_a+chosen_b
                normalization = F(QQ(factorial(out_a)*factorial(total-out_a))
                                  / (factorial(na)*factorial(nb))).sqrt()
                B[out_a, na] += normalization*binomial(na, chosen_a)*binomial(nb, chosen_b)*(
                    cosine**chosen_a*(-sine)**(na-chosen_a)
                    * sine**chosen_b*cosine**(nb-chosen_b))
    assert B.conjugate_transpose()*B == identity_matrix(F, total+1)
    return B


def kerr(occupation):
    return F((-1)**(occupation*(occupation-1)//2))


assert beamsplitter(1, c, s) == matrix(F, [[c, -s], [s, c]])
cz_cases = []
for na, nb in [(0, 0), (1, 0), (0, 1), (1, 1)]:
    total = na+nb
    B = beamsplitter(total, c, s)
    Kpair = diagonal_matrix(F, [kerr(a)*kerr(total-a) for a in range(total+1)])
    gadget = B.conjugate_transpose()*Kpair*B
    initial = vector(F, [1 if a == na else 0 for a in range(total+1)])
    phase = -1 if na == nb == 1 else 1
    assert gadget*initial == phase*initial
    cz_cases.append({'input': [na, nb], 'exact_phase': phase,
                     'leakage_amplitude_exactly_zero': True})

q, zeta = 4, F.zeta(4)
coefficients = [sum(kerr(u)*zeta**(-r*u) for u in range(q))/q for r in range(q)]
weights = [coefficient*coefficient.conjugate() for coefficient in coefficients]
assert sum(weights) == 1
assert coefficients == [0, (1-zeta)/2, 0, (1+zeta)/2]
for occupation in range(13):
    assert kerr(occupation) == sum(coefficients[r]*zeta**(r*occupation) for r in range(q))
    assert kerr(occupation+q) == kerr(occupation)

# One fixed nontrivial Kerr witness; no search/sweep.
total = 2
witness_basis = [[a, total-a] for a in range(total+1)]
Bin = beamsplitter(total, c, s)
cosout, sinout = (F(2)+sqrt2).sqrt()/2, (F(2)-sqrt2).sqrt()/2
Bout = beamsplitter(total, cosout, sinout)
initial = vector(F, [0, 0, 1])  # |2,0> in the chosen basis.
Kone = diagonal_matrix(F, [kerr(a) for a in range(total+1)])
rotations = [diagonal_matrix(F, [zeta**(r*a) for a in range(total+1)]) for r in range(q)]
assert Kone == sum((coefficient*rotation for coefficient, rotation in zip(coefficients, rotations)), matrix(F, 3, 3))
coherent = Bout.conjugate_transpose()*Kone*Bin*initial
assert coherent == vector(F, [0, -1, 0])
coherent_probabilities = [amplitude*amplitude.conjugate() for amplitude in coherent]
mixture_probabilities = [F(0)]*3
for weight, rotation in zip(weights, rotations):
    branch = Bout.conjugate_transpose()*rotation*Bin*initial
    for j, amplitude in enumerate(branch):
        mixture_probabilities[j] += weight*amplitude*amplitude.conjugate()
assert coherent_probabilities == [0, 1, 0]
assert mixture_probabilities == [QQ(1)/4, QQ(1)/2, QQ(1)/4]

period_cases = []
for total in range(5):
    B = beamsplitter(total, c, s)
    shifted = beamsplitter(total, -c, -s)
    assert shifted == (-1)**total*B
    period_cases.append({'pair_photons': total, 'shift_phase': (-1)**total})
# Pair sectors0,1 coexist while global total remains1, using a third mode.
ordinary = block_diagonal_matrix(beamsplitter(1, c, s), matrix(F, [[1]]))
shifted = block_diagonal_matrix(beamsplitter(1, -c, -s), matrix(F, [[1]]))
superposition = vector(F, [0, 1/sqrt2, 1/sqrt2])
left, right = ordinary*superposition, shifted*superposition
overlap = sum(a.conjugate()*b for a, b in zip(left, right))
assert overlap == 0

result = {
    'status': 'PASS', 'scope': 'Exact finite symmetric-power/Kerr/operator identities only.',
    'beamsplitter_convention': 'B(theta)=exp(theta(a†b-b†a)); basis ordered by n_a increasing.',
    'dual_rail_CZ': {'theta': 'pi/4', 'operator': 'B† K(n_a) K(n_b) B',
        'cases': cz_cases, 'logical_phases_00_10_01_11': [1, 1, 1, -1],
        'known_universality_composition_claimed_new': False},
    'Kerr_Fourier': {'period': q, 'coefficients_c0_c1_c2_c3': ['0', '(1-i)/2', '0', '(1+i)/2'],
        'coherent_operator_identity_verified_occupations': list(range(13)),
        'mixture_witness': {'input': [2, 0], 'input_beamsplitter_angle': 'pi/4',
            'single_Kerr_on_mode': 'a', 'inverse_output_beamsplitter_angle': 'pi/8',
            'output_basis': witness_basis,
            'exact_coherent_state': ['0', '-1', '0'],
            'coherent_count_probabilities': [str(QQ(p)) for p in coherent_probabilities],
            'incoherent_count_probabilities': [str(QQ(p)) for p in mixture_probabilities],
            'total_variation_distance': '1/2', 'classical_mixture_shortcut_refuted': True}},
    'angle_period': {'exact_identity': 'B(theta+pi)=(-1)^(pair photon number) B(theta)',
        'tested_pair_sectors': period_cases, 'spectator_witness_global_photons': 1,
        'spectator_basis': [[0, 1, 0], [1, 0, 0], [0, 0, 1]],
        'initial_state': '(|100>+|001>)/sqrt2',
        'outputs_exact_inner_product': str(overlap), 'pi_reduction_changes_relative_phase': True},
    'claim_gates': {'full_binary_cutoff_theorem_from_control': False, 'quantum_execution': False,
        'QHT_simulation': False, 'hardness': False, 'novelty': False, 'speedup': False},
}
Path(__file__).with_name('result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'CZ_phases': [1, 1, 1, -1],
    'coherent_count_distribution': result['Kerr_Fourier']['mixture_witness']['coherent_count_probabilities'],
    'incoherent_count_distribution': result['Kerr_Fourier']['mixture_witness']['incoherent_count_probabilities'],
    'fixed_global_total_pi_shift_output_overlap': str(overlap)}, indent=2))
