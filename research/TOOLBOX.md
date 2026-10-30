# Toolbox

The computer algebra tools live in their own conda environment, separate
from the repo's Python. Call them by full path:

    E=/opt/anaconda3/envs/qsearch-cas/bin    # Sage 10.9 on Python 3.14

| Tool | How to call it | Use it for |
|---|---|---|
| Sage 10.9 (bundles GAP 4.15, PARI 2.17, Singular 4.4, FLINT) | `$E/sage script.sage`, `$E/sage -c "..."`, or `$E/python` with `from sage.all import *` | number fields, class groups, quaternion algebras and orders, genus-2 curves and Jacobians, finite fields, codes, Gröbner bases |
| GAP | `libgap` inside Sage, or `printf 'Display(...);\nQUIT;\n' \| $E/gap -q` | groups, subgroup lattices, representations |
| PARI/GP | `pari("...")` inside Sage, or `echo '...' \| $E/gp -q` | factoring, `bnfisnorm` norm equations, `qfsolve`, class groups, elliptic curves |
| Singular | Sage's `R.ideal(...).groebner_basis()`, or `$E/Singular -q < file` | Gröbner bases, elimination, varieties over F_p |
| fpylll | `from fpylll import IntegerMatrix, LLL, BKZ` (also inside Sage) | LLL/BKZ, SVP/CVP lattice attacks |
| cvc5 1.4 (Python API) | `$E/python -c "import cvc5"` | SMT over integers and bit-vectors. It was built without CoCoA, so it has **no finite-field theory**: use Gröbner bases instead. |
| pdftotext (poppler 26.10) | `$E/pdftotext -layout paper.pdf -` | reading papers as text |

The repo's own code and tests still run on `/opt/anaconda3/bin/python`
(flint, z3, sympy). Don't mix the two environments, and don't install into
either one without the owner's say-so: the disk is about 98% full.

## Gotchas

- Sage takes about 8 seconds to start, so put many computations in one
  script rather than making many `sage -c` calls.
- In `sage -c`, `x` is not predefined. Declare rings and variables first,
  e.g. `R.<t> = QQ[]` or `var('y')`.
- Running `foo.sage` writes `foo.sage.py` beside it. Keep scratch scripts
  out of `research/` and `theorems/`, or write `.py` files with
  `from sage.all import *`.
- In the owner's interactive shell, `gap` and `gp` are git aliases. Always
  use the full `$E/...` path.
- GAP prints a harmless "#I ... package ... not present" line.

## Classical-attack recipes (each tested 2026-10-30)

```python
# Lattice reduction
A = IntegerMatrix.random(20, "qary", k=10, bits=30); LLL.reduction(A); BKZ.reduction(A, BKZ.Param(10))
# Groebner basis and points over F_p
R = PolynomialRing(GF(101), 'x', 3); x0, x1, x2 = R.gens()
I = R.ideal([x0^2 - x1, x1^2 - x2, x0*x2 - 1]); I.groebner_basis(); I.variety()
# Norm equations and class groups
pari('bnfisnorm(bnfinit(y^2+5), 6)'); NumberField(QQ['y']([5, 0, 1]), 'a').class_group()
# Quaternion algebras and orders
B.<i,j,k> = QuaternionAlgebra(-1, -11); O = B.maximal_order(); (1+i).reduced_norm(); O.discriminant()
# Groups via GAP
G = libgap.SmallGroup(64, 10); G.ConjugacyClassesSubgroups()
# Factoring and discrete logs
factor(2^128 + 1); p = next_prime(10^12); g = GF(p).multiplicative_generator(); (g^12345).log(g)
# Genus-2 Jacobian order over F_p
C = HyperellipticCurve(GF(103)['t']([1, 0, 3, 0, 1, 0, 1])); C.frobenius_polynomial()(1)
```

Corpus lookups (repo Python): `tools/corpus/cli.py been-tried "<idea>"` and
`tools/corpus/cli.py baselines "<idea>"`. The baselines catalog now has
Siegel reverse-transport, endomorphism-transport and KLPT entries.
