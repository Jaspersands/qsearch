"""Ambient-filtered public compiler for the metabelian-derived HSP proposal.

This is coefficient algebra and a public Lie-coordinate certificate, not
an SDE solver or quantum receiver. A filtered ambient basis proves the
coordinate degree origin; a weighted normal chart alone does not.
"""
from dataclasses import dataclass
from collections import Counter, defaultdict
from fractions import Fraction
from functools import cached_property
from math import comb, prod

from theorems.affine_phase_erasure import monomials
from theorems.class_three_ambient_frontend import _subspace_intersection
from theorems.class_three_monomial_jet import FullTaylorJetChart
from theorems.metabelian_induced_phase import (
    InducedPhasePacket, MetabelianLieChart, _compile_induced_phase, cocycle_template,
)
from theorems.symbolic_scalar_phase_erasure import _fmpz_solve_coordinates


@dataclass(frozen=True)
class FilteredNormalChart:
    structure: MetabelianLieChart
    ambient_class: int
    coordinate_weights: tuple

    def __post_init__(self):
        st, c, weights = self.structure, self.ambient_class, self.coordinate_weights
        if type(c) is not int or c < 2 or c >= st.p:
            raise ValueError("ambient class in the Lazard range required")
        if (not isinstance(weights, tuple) or len(weights) != st.width or
                any(type(w) is not int or not 2 <= w <= c for w in weights)):
            raise ValueError("one ambient weight >=2 per normal coordinate required")
        for i, rows in enumerate(st.brackets):
            for j, row in enumerate(rows):
                if any(a and weights[t] < weights[i]+weights[j] for t, a in enumerate(row)):
                    raise ValueError("bracket violates ambient filtration")

    @property
    def a_degrees(self):
        return self.coordinate_weights[:self.structure.a_width]

    def verify_cocycle_support(self):
        """Check every formal coefficient, before substituting any potential."""
        st, weights = self.structure, self.coordinate_weights
        for out, component in enumerate(cocycle_template(st), st.a_width):
            for (alpha, parameters), coefficient in component:
                budget = sum(weights[i] for i in parameters)+sum(a*w for a, w in zip(alpha, self.a_degrees))
                if coefficient and budget > weights[out]:
                    raise ArithmeticError("cocycle violates ambient filtration")
        return True


@dataclass(frozen=True)
class AmbientFiltrationCertificate:
    filtered: FilteredNormalChart
    ambient_basis: tuple
    normal_basis: tuple
    lower_central_series: tuple

    def verify(self, algebra):
        """Verify actual filtered N=A+N', not just compatible weight numbers.

        The supplied bracket must be a genuine bilinear Lie bracket. Matrix
        fixtures establish that independently; arbitrary callables do not.
        """
        st, weights = self.filtered.structure, self.filtered.coordinate_weights
        if algebra.p != st.p:
            raise ValueError("field mismatch")
        series = algebra.lower_central_series(self.ambient_basis)
        if tuple(tuple(row) for row in series) != self.lower_central_series:
            raise ValueError("ambient lower central series mismatch")
        if len(series)-1 != self.filtered.ambient_class or len(algebra.span(self.normal_basis)) != st.width:
            raise ValueError("ambient class or normal basis rank mismatch")
        if len(algebra.span(list(self.ambient_basis)+series[1])) != len(self.ambient_basis):
            raise ValueError("ambient space is not bracket closed")
        for w in range(2, self.filtered.ambient_class+1):
            selected = [v for v, depth in zip(self.normal_basis, weights) if depth >= w]
            if len(selected) != len(series[w-1]) or len(algebra.span(selected+series[w-1])) != len(selected):
                raise ValueError("basis does not split the actual ambient filtration")
        ideal = algebra.lower_central_series(series[1])[1]
        represented = list(self.normal_basis[st.a_width:])
        if len(ideal) != len(represented) or len(algebra.span(ideal+represented)) != len(ideal):
            raise ValueError("fiber is not the full derived ideal of N")
        for i, x in enumerate(self.normal_basis):
            for j, y in enumerate(self.normal_basis):
                if _fmpz_solve_coordinates(self.normal_basis, algebra.bracket(x, y), algebra.p) != st.brackets[i][j]:
                    raise ValueError("normal structure tensor mismatch")
        return self.filtered.verify_cocycle_support()


def ambient_filtration_certificate(algebra, ambient_basis):
    """Public descending-flag linear algebra; no H or potential input."""
    ambient = algebra.span(ambient_basis)
    series = algebra.lower_central_series(ambient)
    c, p = len(series)-1, algebra.p
    if c < 4 or p <= c:
        raise ValueError("nonabelian derived case and p>ambient class required")
    normal = series[1]
    ideal = algebra.lower_central_series(normal)[1]
    if not ideal or any(any(algebra.bracket(x, y)) for x in ideal for y in ideal):
        raise ValueError("nonzero abelian N' required")
    fibers, iw = [], []
    for w in range(c, 1, -1):
        intersection = _subspace_intersection(ideal, series[w-1], algebra.dimension, p)
        extended = algebra.span(fibers+intersection)
        iw.extend([w]*(len(extended)-len(fibers)))
        fibers = extended
    carriers, aw = [], []
    for w in range(c, 1, -1):
        for v in series[w-1]:
            if _fmpz_solve_coordinates(fibers+carriers, v, p) is None:
                carriers.append(v)
                aw.append(w)
    basis = carriers+fibers
    table = tuple(tuple(_fmpz_solve_coordinates(basis, algebra.bracket(x, y), p) for y in basis) for x in basis)
    structure = MetabelianLieChart(p, len(carriers), table)
    filtered = FilteredNormalChart(structure, c, tuple(aw+iw))
    result = AmbientFiltrationCertificate(filtered, tuple(ambient), tuple(basis), tuple(tuple(row) for row in series))
    result.verify(algebra)
    return result


@dataclass(frozen=True)
class FilteredFullJetChart(FullTaylorJetChart):
    component_degrees: tuple

    def __post_init__(self):
        super().__post_init__()
        if (not isinstance(self.component_degrees, tuple) or len(self.component_degrees) != self.noncentral_width or
                any(type(d) is not int or not 2 <= d <= self.degree for d in self.component_degrees) or
                max(self.component_degrees) != self.degree):
            raise ValueError("one filtered degree per carrier, with maximum D, required")

    @cached_property
    def indices(self):
        return tuple((alpha, k, a) for a, degree in enumerate(self.component_degrees)
                     for k in range(1, degree+1)
                     for alpha in monomials(self.quotient_width, degree-k))

    @property
    def feature_count(self):
        """One maximal-degree scalar feature design suffices for all blocks."""
        return comb(self.quotient_width+self.degree, self.quotient_width+1)


def filtered_jet_chart(filtered, quotient_width):
    return FilteredFullJetChart(filtered.structure.p, quotient_width, filtered.structure.a_width,
                                max(filtered.a_degrees), filtered.a_degrees)


@dataclass
class FilteredInducedPhasePacket(InducedPhasePacket):
    filtered: FilteredNormalChart

    @property
    def parameter_basis(self):
        return tuple((i, alpha) for i, degree in enumerate(self.filtered.coordinate_weights)
                     for alpha in monomials(self.chart.quotient_width, degree))

    @property
    def schema(self):
        return super().schema, self.filtered

    @property
    def supported_parameter_count(self):
        """Abelian-fiber overestimate using the heterogeneous coefficient pools."""
        m = self.chart.quotient_width
        sizes = [comb(m+w, m) for w in self.filtered.coordinate_weights]
        split = self.filtered.structure.a_width
        h_a, h_i = sum(sizes[:split]), sum(sizes[split:])
        return (1+h_i)*comb(h_a+self.parameter_cap-1, self.parameter_cap-1)

    def validate(self):
        ch, f = self.chart, self.filtered
        st, c, weights = f.structure, f.ambient_class, f.coordinate_weights
        if (not isinstance(ch, FilteredFullJetChart) or ch.component_degrees != f.a_degrees or
                ch.p != st.p or self.normal_width != st.width or self.parameter_cap != st.nilpotency_class):
            raise ValueError("matching filtered chart and parameter schema required")
        if ch.p <= 2*c:
            raise ValueError("conservative filtered scope requires p>2c")
        basis, m, r, k = self.parameter_basis, ch.quotient_width, st.a_width, self.parameter_cap
        for (alpha, parameters), value in self.terms.items():
            if ch.weighted_degree(alpha) > c:
                raise ValueError("phase exceeded ambient-class weighted bound")
            if (not parameters or len(parameters) > k or tuple(sorted(parameters)) != parameters or
                    any(type(i) is not int or not 0 <= i < len(basis) for i in parameters)):
                raise ValueError("canonical bounded parameter monomial required")
            ideal_count = sum(basis[i][0] >= r for i in parameters)
            if ideal_count > 1 or (not ideal_count and len(parameters) >= k):
                raise ValueError("phase violated abelian-fiber support")
            parameter_weight = sum(weights[basis[i][0]] for i in parameters)
            carrier_weight = sum(e*weights[a] for e, (_, _, a) in zip(alpha[m:], ch.indices))
            if (parameter_weight+carrier_weight > c or sum(alpha[:m]) > parameter_weight or
                    sum(alpha[m:]) > k-len(parameters)):
                raise ValueError("phase violated filtered q/jet support")
            if type(value) is not int or not 0 < value < ch.p:
                raise ValueError("nonzero canonical field coefficient required")


def compile_filtered_induced_phase(alignment, spectator, filtered):
    if alignment.structure != filtered.structure:
        raise ValueError("matching filtered normal structure required")
    ch, st = alignment.chart, alignment.structure
    # The first J columns are the component-separated displacement map.
    # Arbitrary later mixing of jet components would destroy this bound.
    for row_index, row in enumerate(alignment.inverse):
        a = row_index % st.a_width
        for coefficient, (_, k, b) in zip(row[:ch.jet_width], ch.indices):
            if coefficient and (a != b or k > filtered.a_degrees[a]):
                raise ValueError("alignment does not preserve carrier filtration")
    packet = FilteredInducedPhasePacket(ch, st.width, st.nilpotency_class, {}, filtered)
    return _compile_induced_phase(alignment, spectator, packet)


def filtered_equation_bounds(filtered, quotient_width):
    """Exact generating-function counts for a conservative invariant support.

    Parameter monomials record count, ambient cost and ideal count. Jet
    monomials record count, ambient component cost and actual scale weight.
    This counts possible pairs, not independent unknown potential values.
    """
    ch = filtered_jet_chart(filtered, quotient_width)
    st, c, m = filtered.structure, filtered.ambient_class, quotient_width
    k, r = st.nilpotency_class, st.a_width
    parameter_types = Counter()
    for i, w in enumerate(filtered.coordinate_weights):
        parameter_types[w, int(i >= r)] += comb(m+w, m)
    parameters = {(0, 0, 0): 1}
    for (w, ideal), number in sorted(parameter_types.items()):
        updated = defaultdict(int)
        for (h, budget, ideals), count in parameters.items():
            cap = min(k-h, (c-budget)//w, 1-ideals if ideal else k)
            for used in range(cap+1):
                updated[h+used, budget+w*used, ideals+ideal*used] += count*comb(number+used-1, used)
        parameters = updated
    parameter_counts = defaultdict(int)
    for (h, budget, ideals), count in parameters.items():
        if h and (ideals or h < k):
            parameter_counts[h, budget] += count
    jet_types = Counter((filtered.a_degrees[a], weight) for _, weight, a in ch.indices)
    jets = {(0, 0, 0): 1}
    for (cost, weight), number in sorted(jet_types.items()):
        updated = defaultdict(int)
        for (degree, budget, scale_weight), count in jets.items():
            for used in range(min(k-1-degree, (c-budget)//cost)+1):
                updated[degree+used, budget+cost*used, scale_weight+weight*used] += count*comb(number+used-1, used)
        jets = updated
    weighted = {d: 0 for d in range(1, c+1)}
    for (h, parameter_cost), count in parameter_counts.items():
        for (t, jet_cost, scale_weight), jcount in jets.items():
            if t <= k-h and parameter_cost+jet_cost <= c:
                for qdegree in range(parameter_cost+1):
                    degree = qdegree+scale_weight
                    if 1 <= degree <= c:
                        weighted[degree] += count*jcount*comb(m+qdegree-1, qdegree)
    ordinary = {d: comb(m+d-1, d)*sum(comb(m+w, m) for w in filtered.a_degrees if w >= d)
                for d in range(1, ch.degree+1)}
    return weighted, ordinary


def filtered_resource_report(filtered, quotient_width, epsilon=Fraction(1, 8)):
    """Reconstructible capped schedule. No solver or receiver is executed."""
    from theorems.full_jet_resource_certificate import sde_arity, tree_schedule
    from theorems.induced_resource_certificate import exact_ceil_log

    if not isinstance(epsilon, Fraction) or not 0 < epsilon < 1:
        raise ValueError("exact error budget in (0,1) required")
    ch = filtered_jet_chart(filtered, quotient_width)
    p, m, c, st = ch.p, ch.quotient_width, filtered.ambient_class, filtered.structure
    if p <= 2*c:
        raise ValueError("filtered resource scope requires p>2c")
    weighted, ordinary = filtered_equation_bounds(filtered, m)
    specs = tuple((kind, j, values[j], sde_arity(j, values[j]))
                  for kind, values in (("weighted", weighted), ("ordinary", ordinary))
                  for j in sorted(values, reverse=True) if values[j])
    roots = m+exact_ceil_log(p, 4/epsilon)
    stages, leaves = tree_schedule(specs, roots)
    batch = (ch.feature_count+1)*p.bit_length()+2
    scale_cap = exact_ceil_log(p, 8*batch)
    retries = exact_ceil_log(2, 4*leaves/epsilon)
    queries = leaves*retries*batch
    field_draws = queries*scale_cap
    binary_cap = exact_ceil_log(2, 8*field_draws/epsilon)
    curve_readouts = roots*prod(s.arity for s in stages if s.kind == "ordinary")
    instruments = queries+leaves*retries+sum(s.nodes for s in stages)+curve_readouts+roots
    registers = (m+ch.jet_width)*(1+sum(s.arity-1 for s in stages))+batch*(m+st.width)+m
    failures = [Fraction(leaves, 2**retries), Fraction(p**m-1, (p-1)*p**roots),
                Fraction(field_draws, 2**binary_cap), epsilon/8]
    if sum(failures) > 3*epsilon/4 or Fraction(batch, p**scale_cap)+Fraction(1, 4*p) >= Fraction(1, 2):
        raise ArithmeticError("filtered schedule error accounting failed")
    if sum(s.nodes*(s.arity-1) for s in stages) != leaves-roots:
        raise ArithmeticError("tree node accounting failed")
    counts = {"leaves": leaves, "queries": queries, "field_draws": field_draws,
              "merge_calls": sum(s.nodes for s in stages), "curve_readouts": curve_readouts,
              "instruments": instruments, "logical_registers": registers}
    return {"p": p, "ambient_class": c, "normal_class": st.nilpotency_class, "quotient_width": m,
            "coordinate_weights": filtered.coordinate_weights, "epsilon": str(epsilon),
            "weighted_degree": c, "ordinary_degree": ch.degree, "jet_width": ch.jet_width,
            "scalar_features": ch.feature_count, "batch": batch, "roots": roots,
            "scale_draw_cap": scale_cap, "leaf_retries": retries, "binary_rejections": binary_cap,
            "counts_upper_power_of_two_exponents": {key: exact_ceil_log(2, value) for key, value in counts.items()},
            "stages": [{"kind": s.kind, "degree": s.degree, "equations": s.equations,
                        "arity_upper_power_of_two_exponent": exact_ceil_log(2, s.arity)} for s in stages],
            "joint_failure_upper_bound": str(3*epsilon/4),
            "required_instrument_precision_bits": exact_ceil_log(2, 8*instruments/epsilon),
            "receiver_executed": False, "claim": "conditional sufficient bounds, not lower bounds or timings"}


def main():
    import argparse
    import json
    from pathlib import Path
    from theorems.right_abelian_induced_source import derived_length_three_witness
    from theorems.induced_resource_certificate import induced_resource_certificate, report

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    controls = []
    for p in (43, 2**127-1):
        algebra, basis, witness = derived_length_three_witness(p)
        certificate = ambient_filtration_certificate(algebra, basis)
        f = certificate.filtered
        previous = report(induced_resource_certificate(p=p, ambient_class=f.ambient_class,
                          normal_class=f.structure.nilpotency_class, quotient_width=2,
                          a_width=f.structure.a_width, ideal_width=f.structure.ideal_width))
        current = filtered_resource_report(f, 2)
        controls.append({"witness": witness, "ambient_filtration_verified": certificate.verify(algebra),
                         "universal_template_support_verified": f.verify_cocycle_support(),
                         "previous": previous, "filtered": current})
    result = {"schema": "ambient_filtered_induced_v1", "controls": controls,
              "status": "public algebra and conditional resource improvement; not an executed receiver",
              "remaining": ["full adaptive implementation", "general SDE execution", "physical synthesis",
                            "independent end-to-end review", "novelty and useful hard application"]}
    encoded = json.dumps(result, indent=2)+"\n"
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/ambient_filtered_induced.json"
        path.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
