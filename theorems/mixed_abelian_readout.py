"""Exact annihilator of supplied mixed-modulus labels, not an HSP sampler.

The pilot compiler's contract applies: an odd prime and a nonempty tuple of
positive exponents. Labels may be empty. Pairings are sum(a_i*x_i/p**e_i)
modulo one, not dot products reduced modulo p. Missing Fourier support can
only enlarge the returned annihilator; no source law or hidden subgroup is
certified here.
"""
from collections import Counter
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from math import prod

from flint import fmpq_mat, fmpz_mat

from theorems.pilot_submodule import (
    PilotFrame, _diagonal, _integer, _matrix, _rows,
    compile_pilot_frame, verify_pilot_frame,
)


@dataclass(frozen=True)
class AnnihilatorDualityCertificate:
    """Row-wise integer matrices; label_pairings has one row per label.

    With H the pilot lattice basis, D the ambient diagonal, B the dual_basis,
    K the returned HNF and U the canonical_transform, the checked identities
    are H^T D^-1 B = I, K = B U, det(U) = +/-1, and K A = D, where A is
    ambient_relations. The integral label_pairings equal labels * D^-1 * K.
    """

    pilot_frame: PilotFrame
    dual_basis: tuple
    canonical_transform: tuple
    ambient_relations: tuple
    label_pairings: tuple


@dataclass(frozen=True)
class AnnihilatorReadout:
    """Canonical full preimage lattice and its subgroup modulo D Z^n.

    lattice_basis is a row-wise matrix in column HNF. generator_columns is
    column-wise, with each coordinate reduced modulo its own ambient modulus;
    zero or redundant columns are retained. subgroup_order counts the output
    annihilator, whereas observed_span_order counts the supplied label span.
    """

    prime: int
    ambient_exponents: tuple
    fourier_labels: tuple
    lattice_basis: tuple
    generator_columns: tuple
    subgroup_order: int
    observed_span_order: int
    duality_certificate: AnnihilatorDualityCertificate
    observed_span_only: bool = True
    hidden_subgroup_recovery_certified: bool = False
    source_law_certified: bool = False

    @property
    def canonical_token(self):
        """Comparable lattice token within this fixed ambient module."""
        return self.lattice_basis

    def certificate(self):
        """Return plain structured data after exact certificate replay."""
        verify_annihilator(self)
        return dict(asdict(self), certificate_verified=True)


def _sequence(value, name):
    if isinstance(value, (str, bytes, Mapping)):
        raise ValueError(f"{name} must be an iterable of exact integers or labels")
    try:
        return tuple(value)
    except TypeError as error:
        raise ValueError(f"{name} must be an iterable") from error


def _pairings(labels, inverse_diagonal, basis):
    if not labels:
        return ()
    return _rows(_integer(fmpq_mat(labels) * inverse_diagonal * fmpq_mat(basis)))


def recover_annihilator(*, prime, ambient_exponents, fourier_labels):
    """Return the exact annihilator of the observed span, without enumeration.

    Integers must be Python ints (not bools, floats, or modularly normalized
    inputs), and 0 <= label[i] < prime**ambient_exponents[i]. The inherited
    pilot-frame compiler checks primality and positive ambient exponents.
    """
    exponents = _sequence(ambient_exponents, "ambient_exponents")
    labels = tuple(_sequence(label, "Fourier label")
                   for label in _sequence(fourier_labels, "fourier_labels"))
    frame = compile_pilot_frame(prime=prime, ambient_exponents=exponents,
                                pilot_columns=labels)
    moduli = tuple(prime**e for e in exponents)
    diagonal = _diagonal(moduli)

    # H*T=D implies B=T^T=D*H^-T, including all prime-power information.
    dual = fmpz_mat(frame.relation_matrix).transpose()
    reduced, row_transform = dual.transpose().hnf(transform=True)
    basis = reduced.transpose()
    transform = row_transform.transpose()
    ambient_relations = _integer(fmpq_mat(basis).inv() * fmpq_mat(diagonal))
    certificate = AnnihilatorDualityCertificate(
        frame, _rows(dual), _rows(transform), _rows(ambient_relations),
        _pairings(labels, fmpq_mat(diagonal).inv(), basis),
    )
    determinant = abs(int(basis.det()))
    order, remainder = divmod(prod(moduli), determinant)
    if remainder:
        raise ArithmeticError("annihilator determinant does not divide ambient order")
    result = AnnihilatorReadout(
        prime, exponents, labels, _rows(basis),
        tuple(tuple(int(basis[i, j]) % modulus for i, modulus in enumerate(moduli))
              for j in range(len(exponents))),
        order, prod(frame.smith_orders), certificate,
    )
    verify_annihilator(result)
    return result


def verify_annihilator(result):
    """Replay exact identities, without enumeration or HNF/SNF computation."""
    if not isinstance(result, AnnihilatorReadout):
        raise ValueError("AnnihilatorReadout certificate required")
    certificate = result.duality_certificate
    if not isinstance(certificate, AnnihilatorDualityCertificate):
        raise ValueError("AnnihilatorDualityCertificate required")
    frame = certificate.pilot_frame
    verify_pilot_frame(frame)
    if (type(result.prime) is not int or result.prime != frame.prime
            or result.ambient_exponents != frame.ambient_exponents
            or any(type(e) is not int for e in result.ambient_exponents)
            or result.fourier_labels != frame.pilot_columns
            or any(type(x) is not int for label in result.fourier_labels for x in label)):
        raise ValueError("readout metadata does not match the certified pilot frame")
    if (result.observed_span_only is not True
            or result.hidden_subgroup_recovery_certified is not False
            or result.source_law_certified is not False):
        raise ValueError("observed-span readout cannot certify hidden recovery or a source law")

    rank = len(result.ambient_exponents)
    moduli = tuple(result.prime**e for e in result.ambient_exponents)
    diagonal = _diagonal(moduli)
    inverse_diagonal = fmpq_mat(diagonal).inv()
    observed = fmpz_mat(frame.lattice_basis)
    dual = _matrix(certificate.dual_basis, rank, rank)
    basis = _matrix(result.lattice_basis, rank, rank)
    transform = _matrix(certificate.canonical_transform, rank, rank)
    ambient_relations = _matrix(certificate.ambient_relations, rank, rank)
    identity = fmpq_mat(_diagonal([1] * rank))
    if (dual != fmpz_mat(frame.relation_matrix).transpose()
            or fmpq_mat(observed.transpose()) * inverse_diagonal * fmpq_mat(dual) != identity):
        raise ArithmeticError("exact mixed-modulus duality identity failed")
    if abs(int(transform.det())) != 1 or dual * transform != basis:
        raise ArithmeticError("unimodular canonical basis transformation failed")
    if not basis.transpose().is_hnf() or basis.det() <= 0:
        raise ArithmeticError("positive full-rank column HNF required")
    if basis * ambient_relations != diagonal:
        raise ArithmeticError("ambient lattice containment failed")
    pairings = _pairings(result.fourier_labels, inverse_diagonal, basis)
    if (certificate.label_pairings != pairings
            or any(type(x) is not int for row in certificate.label_pairings for x in row)):
        raise ArithmeticError("supplied-label pairing certificate failed")
    generators = tuple(tuple(int(basis[i, j]) % modulus
                             for i, modulus in enumerate(moduli)) for j in range(rank))
    if (result.generator_columns != generators
            or any(type(x) is not int for column in result.generator_columns for x in column)):
        raise ArithmeticError("canonical ambient generator columns failed")
    determinant = int(basis.det())
    ambient_order = prod(moduli)
    if (type(result.subgroup_order) is not int
            or type(result.observed_span_order) is not int
            or result.subgroup_order < 1
            or result.subgroup_order * determinant != ambient_order
            or result.observed_span_order != prod(frame.smith_orders)
            or result.observed_span_order != determinant
            or result.observed_span_order * abs(int(observed.det())) != ambient_order):
        raise ArithmeticError("determinant/annihilator order certificate failed")
    return True


def canonical_modal_token(tokens):
    """Return the unique mode, or None for a tie, no trials, or an abort mode.

    Tokens must be None or full-rank canonical column-HNF tuples, all for one
    fixed ambient module. None is counted as a real outcome. This function
    never compares arbitrary Smith bases or discards aborted trials.
    """
    counts = Counter()
    rank = None
    for token in tokens:
        if token is not None:
            if (type(token) is not tuple or not token
                    or any(type(row) is not tuple for row in token)):
                raise ValueError("canonical lattice tuple or None required")
            basis = _matrix(token, len(token), len(token))
            if not basis.transpose().is_hnf() or basis.det() <= 0:
                raise ValueError("full-rank canonical column HNF token required")
            if rank is not None and len(token) != rank:
                raise ValueError("tokens must belong to one fixed ambient module")
            rank = len(token)
        counts[token] += 1
    if not counts:
        return None
    maximum = max(counts.values())
    winners = [token for token, count in counts.items() if count == maximum]
    return winners[0] if len(winners) == 1 else None
