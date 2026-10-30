"""Bounded arithmetic controls for the written AG proof, not hard instances.

Point enumeration is deliberately confined to three fixed tiny curves.
The solver itself receives only the original parity matrix and syndrome.
"""

from itertools import product

from flint import nmod_poly

from schur_gate import FullSupportProblem, basis


def pole_evaluations(points, pole_degree, genus, p):
    # On y^2=f(x), deg(f)=2g+1, pole orders at infinity are 2 and 2g+1.
    monomials = [(i, j) for j in (0, 1)
                 for i in range(pole_degree//2+1) if 2*i+(2*genus+1)*j <= pole_degree]
    return [[pow(x, i, p)*pow(y, j, p) % p for x, y in points] for i, j in monomials]


def curve_control(genus):
    if type(genus) is not int or genus not in (1, 2, 3):
        raise ValueError("only fixed genus 1/2/3 proof controls; no unbounded curve search")
    p = 11 if genus == 1 else 19
    constant = 6 if genus == 1 else 1
    d = 2*genus+1
    polynomial = nmod_poly([constant, 1]+[0]*(d-2)+[1], p)
    if polynomial.gcd(polynomial.derivative()) != nmod_poly([1], p):
        raise ArithmeticError("singular curve control")
    points = [(x, y) for x, y in product(range(p), repeat=2)
              if (y*y-pow(x, d, p)-x-constant) % p == 0]
    problem = FullSupportProblem(p, pole_evaluations(points, d, genus, p),
                                 relation="full_support")
    if (problem.W != basis(pole_evaluations(points, 2*d, genus, p), p)
            or problem.U != basis(pole_evaluations(points, 3*d, genus, p), p)):
        raise ArithmeticError("Schur products differ from the evaluated RR spaces")
    return problem, {"genus": genus, "divisor_degree": d, "prime": p,
                     "curve_coefficients_low_first": [constant, 1]+[0]*(d-2)+[1],
                     "points": points, "point_pairs_enumerated": p*p,
                     "schur_and_rr_rowspaces_equal": True}


def annihilator_control(problem):
    """Exhaustive rank control, capped independently of the scalable solver."""
    total = problem.p**len(problem.annihilator)
    if total > 10000:
        raise ValueError("finite annihilator enumeration cap")
    failures, nonzero_failures, minimum_support = 0, 0, problem.m
    for coefficients in product(range(problem.p), repeat=len(problem.annihilator)):
        h = [sum(a*v[i] for a, v in zip(coefficients, problem.annihilator)) % problem.p
             for i in range(problem.m)]
        # from_annihilator independently checks the full cube and original equation.
        result = problem.from_annihilator(tuple(range(1, problem.k+1)), h, 2)
        if not result["witness"]:
            failures += 1
            nonzero_failures += int(any(h))
        elif any(h):
            minimum_support = min(minimum_support, result["support_size"])
    return {"annihilators_enumerated": total, "rank_failures": failures,
            "nonzero_rank_failures": nonzero_failures,
            "minimum_nonzero_support": minimum_support}
