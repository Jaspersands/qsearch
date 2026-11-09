"""Emit GAP code: the programs Pi_+, Pi_[] of lem:tb-words for classes 2..4 and the BCH
expansion in left-normed brackets; then a GAP test on SmallGroups of class < p, exponent >= p^2:
the word-defined (+, [,]) must satisfy the Lie ring axioms and BCH(x,y) = x*y (lem:tb-evaluation
+ Lazard). Usage: python gen_gap_words.py > words_test.g"""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, ".")
from lazard_words import TA, build_program


def gap_prog(prog):
    items = []
    for ins in prog[2:]:
        if ins[0] == "mul":
            items.append("[1,%d,%d]" % (ins[1] + 1, ins[2] + 1))
        else:
            r = ins[2]
            items.append("[2,%d,%d/%d]" % (ins[1] + 1, r.numerator, r.denominator))
    return "[" + ",".join(items) + "]"


def main():
    lines = []
    for c in (2, 3, 4):
        A = TA(c)
        U, V = {(0,): Fr(1)}, {(1,): Fr(1)}
        pp, _ = build_program(A.add(U, V), c)
        pb, _ = build_program(A.br(U, V), c)
        bch = A.bch(U, V)
        terms = []
        for w, v in sorted(bch.items()):
            if len(w) >= 2 and w[0] == w[1]:
                continue
            r = v / len(w)
            terms.append("[[%s],%d/%d]" % (",".join(str(i + 1) for i in w), r.numerator, r.denominator))
        lines.append("PROGS[%d] := rec(plus := %s, br := %s, bch := [%s]);" % (c, gap_prog(pp), gap_prog(pb), ",".join(terms)))
    print("PROGS := [];")
    print("\n".join(lines))
    print(r'''
EvalProg := function(x, y, prog, M)
  local v, ins;
  v := [x, y];
  for ins in prog do
    if ins[1] = 1 then Add(v, v[ins[2]] * v[ins[3]]);
    else Add(v, v[ins[2]] ^ (ins[3] mod M)); fi;
  od;
  return v[Length(v)];
end;

TestGroup := function(G, cw, ntr)
  local M, P, Plus, Br, Scal, LBr, BCHg, x, y, z, i, bad, e, nam;
  M := Exponent(G); P := PROGS[cw];
  Plus := function(a, b) return EvalProg(a, b, P.plus, M); end;
  Br := function(a, b) return EvalProg(a, b, P.br, M); end;
  Scal := function(r, a) return a ^ (r mod M); end;
  LBr := function(w, a, b) local r, j, ab; ab := [a, b]; r := ab[w[1]];
    for j in [2..Length(w)] do r := Br(r, ab[w[j]]); od; return r; end;
  BCHg := function(a, b) local s, t; s := One(a);
    for t in P.bch do s := Plus(s, Scal(t[2], LBr(t[1], a, b))); od; return s; end;
  bad := rec(comm := 0, assoc := 0, zero := 0, neg := 0, mult := 0, bil := 0, alt := 0, jac := 0, bch := 0);
  for i in [1..ntr] do
    x := Random(G); y := Random(G); z := Random(G);
    if Plus(x, y) <> Plus(y, x) then bad.comm := bad.comm + 1; fi;
    if Plus(Plus(x, y), z) <> Plus(x, Plus(y, z)) then bad.assoc := bad.assoc + 1; fi;
    if Plus(x, One(G)) <> x then bad.zero := bad.zero + 1; fi;
    if Plus(x, x^-1) <> One(G) then bad.neg := bad.neg + 1; fi;
    if Plus(x, x) <> x^2 then bad.mult := bad.mult + 1; fi;
    if Br(Plus(x, y), z) <> Plus(Br(x, z), Br(y, z)) then bad.bil := bad.bil + 1; fi;
    if Br(x, x) <> One(G) then bad.alt := bad.alt + 1; fi;
    if Plus(Plus(Br(x, Br(y, z)), Br(y, Br(z, x))), Br(z, Br(x, y))) <> One(G) then bad.jac := bad.jac + 1; fi;
    if BCHg(x, y) <> x * y then bad.bch := bad.bch + 1; fi;
  od;
  return bad;
end;

RunOrder := function(p, n, ntr)
  local k, G, c, e, cw, bad, tot, cnt;
  tot := 0; cnt := 0;
  for k in [1..NrSmallGroups(p^n)] do
    G := SmallGroup(p^n, k);
    c := NilpotencyClassOfGroup(G); e := Exponent(G);
    if c < p and e > p then
      for cw in [Maximum(c, 2)..Minimum(p - 1, 4)] do
        bad := TestGroup(G, cw, ntr);
        cnt := cnt + 1;
        if ForAny(RecNames(bad), r -> bad.(r) > 0) then
          Print("FAIL order ", p, "^", n, " id ", k, " class ", c, " exp ", e, " words c=", cw, " ", bad, "\n");
          tot := tot + 1;
        fi;
      od;
    fi;
  od;
  Print("order ", p, "^", n, ": ", cnt, " (group, word-class) tests, ", tot, " failures\n");
end;
''')


if __name__ == "__main__":
    main()
