"""Public symbolic source map with varying Weyl ranks and radical characters.

This is not a quantum source preparer, proof of same-instance provenance,
or coherent HSP implementation. Hidden coefficients remain formal variables.
"""
from __future__ import annotations

from theorems.affine_phase_erasure import monomials
from theorems.class_four_matrix_source import label_coordinates, variable_jet_maps
from theorems.ut5_matrix_phase_alignment import verify_alignment
from theorems.ut5_scalar_phase_compiler import _add, _compile_weyl_phase, _shifted_component


def compile_variable_scalar_packet(alignment, forms, labels, scales, outcomes,
                                    radical_characters, spectator_outcome):
    """Compile Theta -> P(q,t) using only a checked public transcript.

    Theta lifts the fixed coefficients of Q_W (degree<=2) and Q_Z
    (degree<=4), including their pairwise products. Each input's alpha has
    the radical dimension for its own label, even when its Weyl rank is zero.
    The same oracle instance and coordinate chart remain a protocol premise.
    """
    maps = alignment.maps
    p, w, z, m = maps.p, maps.noncentral_width, len(forms), maps.quotient_width
    R, D = maps.carrier_width, maps.jet_width
    if variable_jet_maps(p, forms, labels, scales, outcomes) != maps or not verify_alignment(alignment):
        raise ValueError("verified variable-radical alignment for these public inputs required")
    if len(radical_characters) != len(labels):
        raise ValueError("one radical character per source required")
    for label, alpha in zip(labels, radical_characters):
        coordinates = label_coordinates(p, forms, label)
        if len(alpha) != len(coordinates.radical) or any(type(x) is not int or not 0 <= x < p for x in alpha):
            raise ValueError("canonical radical character of the correct label-dependent width required")
    if len(spectator_outcome) != R-D or any(type(x) is not int or not 0 <= x < p for x in spectator_outcome):
        raise ValueError("canonical spectator measurement outcome required")
    width = m+D
    basis = tuple((coordinate, exponent) for coordinate in range(w+z)
                  for exponent in monomials(m, 2 if coordinate < w else 4))
    displacement, psi, start = [{} for _ in range(2*R)], {}, 0
    for source, coordinates in zip(maps.active_indices, maps.representations):
        s, y, t = scales[source], outcomes[source], coordinates.qudits
        noncentral = [_shifted_component(p, width, basis, j, s, y) for j in range(w)]
        for j, row in enumerate(coordinates.weyl):
            target = start+j if j < t else R+start+j-t
            for coefficient, component in zip(row, noncentral):
                _add(displacement[target], component, coefficient, p)
        for j, coefficient in enumerate(labels[source]):
            _add(psi, _shifted_component(p, width, basis, w+j, s, y), coefficient, p)
        for alpha, row in zip(radical_characters[source], coordinates.radical):
            for coefficient, component in zip(row, noncentral):
                _add(psi, component, alpha*coefficient, p)
        start += t
    return _compile_weyl_phase(alignment, basis, displacement, psi, spectator_outcome)
