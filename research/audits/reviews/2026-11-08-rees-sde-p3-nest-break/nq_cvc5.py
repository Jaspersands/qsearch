"""cvc5 (nonlinear real arithmetic) checks of the two analytic inequalities of Theorem A.
  (a) N = 1.5q + 2 sqrt(q) + 5 + e, 0 <= e < 1 (the ceiling), q >= 4  =>  N - 1.5q >= 3 + sqrt(N).
      Negation must be UNSAT.  (This gives N(q) <= 1.5q + 2 sqrt(q) + 6.)
  (b) 4 <= q, N <= 1.5q + 2 sqrt(q) + 6  =>  2N/3 + (2/3) sqrt(N) <= q + (8/3) sqrt(q) + 4.
      Negation must be UNSAT.
  (c) the closed form: sum bound.  Not an SMT problem; done exactly in tables_break.py.
Interpreter: /opt/anaconda3/envs/qsearch-cas/bin/python (cvc5 1.4)."""
import cvc5
from cvc5 import Kind

def solver():
    s = cvc5.Solver()
    s.setOption("produce-models", "true")
    s.setLogic("QF_NRA")
    return s

def check_a():
    s = solver(); R = s.getRealSort()
    q, sq, N, sN, e = (s.mkConst(R, x) for x in "q sq N sN e".split())
    four = s.mkReal(4)
    s.assertFormula(s.mkTerm(Kind.GEQ, q, four))
    s.assertFormula(s.mkTerm(Kind.EQUAL, s.mkTerm(Kind.MULT, sq, sq), q))
    s.assertFormula(s.mkTerm(Kind.GEQ, sq, s.mkReal(0)))
    s.assertFormula(s.mkTerm(Kind.EQUAL, s.mkTerm(Kind.MULT, sN, sN), N))
    s.assertFormula(s.mkTerm(Kind.GEQ, sN, s.mkReal(0)))
    s.assertFormula(s.mkTerm(Kind.GEQ, e, s.mkReal(0)))
    s.assertFormula(s.mkTerm(Kind.LT, e, s.mkReal(1)))
    expr = s.mkTerm(Kind.ADD, s.mkTerm(Kind.MULT, s.mkReal(3, 2), q), s.mkTerm(Kind.MULT, s.mkReal(2), sq), s.mkReal(5), e)
    s.assertFormula(s.mkTerm(Kind.EQUAL, N, expr))
    # negation: N - 1.5 q < 3 + sqrt N
    s.assertFormula(s.mkTerm(Kind.LT, s.mkTerm(Kind.SUB, N, s.mkTerm(Kind.MULT, s.mkReal(3, 2), q)),
                             s.mkTerm(Kind.ADD, s.mkReal(3), sN)))
    r = s.checkSat()
    print("(a) N(q) <= 1.5q + 2sqrt(q) + 6 for all real q >= 4: negation is", r)
    if r.isSat():
        print("   model q =", s.getValue(q), "N =", s.getValue(N))

def check_b():
    s = solver(); R = s.getRealSort()
    q, sq, N, sN = (s.mkConst(R, x) for x in "q sq N sN".split())
    s.assertFormula(s.mkTerm(Kind.GEQ, q, s.mkReal(4)))
    s.assertFormula(s.mkTerm(Kind.EQUAL, s.mkTerm(Kind.MULT, sq, sq), q))
    s.assertFormula(s.mkTerm(Kind.GEQ, sq, s.mkReal(0)))
    s.assertFormula(s.mkTerm(Kind.EQUAL, s.mkTerm(Kind.MULT, sN, sN), N))
    s.assertFormula(s.mkTerm(Kind.GEQ, sN, s.mkReal(0)))
    s.assertFormula(s.mkTerm(Kind.GEQ, N, s.mkReal(1)))
    s.assertFormula(s.mkTerm(Kind.LEQ, N, s.mkTerm(Kind.ADD, s.mkTerm(Kind.MULT, s.mkReal(3, 2), q),
                                                        s.mkTerm(Kind.MULT, s.mkReal(2), sq), s.mkReal(6))))
    lhs = s.mkTerm(Kind.ADD, s.mkTerm(Kind.MULT, s.mkReal(2, 3), N), s.mkTerm(Kind.MULT, s.mkReal(2, 3), sN))
    rhs = s.mkTerm(Kind.ADD, q, s.mkTerm(Kind.MULT, s.mkReal(8, 3), sq), s.mkReal(4))
    s.assertFormula(s.mkTerm(Kind.GT, lhs, rhs))
    r = s.checkSat()
    print("(b) 2N/3 + (2/3)sqrt N <= q + (8/3)sqrt q + 4 whenever N <= 1.5q+2sqrt q+6, q >= 4: negation is", r)
    if r.isSat():
        print("   model q =", s.getValue(q), "N =", s.getValue(N))

if __name__ == "__main__":
    check_a(); check_b()
