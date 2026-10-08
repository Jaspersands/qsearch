# Batch Root Reduction Through Balanced Native Fibers

LOCAL DERIVATION / REVIEW PENDING. No novelty, efficient compiler, accepted
candidate or speedup is claimed. This is a conditional multi-root architecture,
not another phase scan. Existence and correct output law do NOT supply the
coherent partition program on which the architecture depends.

## Native Batch And Exact Carry Polynomials

Take M original even-level native qutrits at q=3^r with IID full rows a_i,c_i
in Z_q^n and unknown shared INTEGER secret s in Z_q^n. This is the repo's
integer-secret phase model and known DCP conversion, not a claim about every
secret in the full cyclotomic algebra. On word x in F3^M,

    F(x)=sum_i (0,a_i,c_i)[x_i] modq,
    |psi_s>=3^(-M/2) sum_x chi_q(F(x).s)|x>.

Choose1<=d<r, H=3^d, and retain the low frequency S(x)=F(x) modH in ALL n
coordinates. Work over F3 for the INPUT word variables, but keep the actual
mod-H frequency function. This is not a substitution of the ring by a field.

For one coordinate, let b_i(0)=0,b_i(1)=a_i modH,b_i(2)=c_i modH. In F3[x,z],
use the indicator polynomials

    I_0=1-x^2, I_1=2*x-x^2, I_2=(x^2-x)/2,
    G_i(x,z)=I_0+I_1*(1+z)^(b_i(1))+I_2*(1+z)^(b_i(2)).

At an actual trit, product_i G_i=(1+z)^(sum_i b_i(x_i)). By Frobenius,
(1+z)^T=product_j(1+z^(3^j))^(T_j) in characteristic3. Its coefficient of
z^(3^j) is the j-th TRUE ternary digit T_j. Hence each low digit of S has a
polynomial representation P_(coordinate,j) of degree at most2*3^j.
Each positive z-degree factor costs at most two word degrees, and obtaining
z^L involves at most L such factors. This proves the bound without expanding
the exponentially many word monomials. The implementation evaluates this
fixed-loop generating-function arithmetic circuit separately from direct
integer frequency evaluation; bounded reduced polynomials are calibration.

For a prescribed target S, the n*d equations P_(coordinate,j)=S_j have total
degree at most n*(3^d-1). If

    M > n*(H-1),

Chevalley--Warning therefore makes EVERY fiber cardinality C_S divisible by3.
An empty fiber has count0; surjectivity onto all S is NOT claimed. All occupied
fibers have at least three words. This statement holds for EVERY public native
label matrix, not only random matrices. It is a known theorem applied to a
specific carry representation, not a new existence principle.

There is also a direct group-algebra check of this threshold: in F3[S], each
factor(1+X^(a_i)+X^(c_i)) has augmentation0. For S=(Z_H)^n, substituting
X_j=1+z_j gives z_j^H=0 and maximum surviving total degree n*(H-1).
A product of more than this many augmentation-ideal factors vanishes. Its
group-basis coefficients are precisely the fiber counts modulo3. This proves
the same all-target divisibility without assuming prime-modulus frequencies.

## A Complete Conditional Extraction Architecture

Within each occupied S, sort its original words lexicographically and group
consecutive triples (x_0,x_1,x_2). Across all S this partitions ALL3^M words
into3^(M-1) triples. Define the basis permutation

    |x_j> -> |triple_tag>|j>, j in F3.

It is exactly bijective, has a clean inverse and uses the SAME M registers.
Measure the M-1 tag trits, retaining ONE physical qutrit. Every tag has Born
probability3^(1-M), independently of every secret. No failure, postselection,
cloning or unknown-state preparation inverse is involved in this IDEAL map.
The reference actually replays this complete permutation at bounded sizes.

Put q'=q/H. Since all three words share S, the retained qutrit is, up to
a common phase,

    (|0>+chi_(q')(A.s)|1>+chi_(q')(C.s)|2>)/sqrt3,
    A=(F(x_1)-F(x_0) modq)/H,
    C=(F(x_2)-F(x_0) modq)/H.

It depends on s modq'. A tag denotes ONE measurement alternative, not an
available extra output sample. One M-input batch yields ONE qutrit, not
3^(M-1) qutrits. Different child samples require fresh independent batches.

## Correct Native Output Law From High Lifts

The partition depends ONLY on the low rows modH. Condition on those rows and
on any tag. Write each parent row as low+H*high; its high coordinates are IID
uniform in Z_(q')^n. Each child row is a known low-carry constant plus an
integer linear combination of these high rows.

For ANY THREE distinct original words, the two pointed one-hot differences
have a2-by-2 coefficient minor with determinant+/-1. If one coordinate has
all three trits, its two frequency columns give the minor. Otherwise each
coordinate has at most two values; distinct words force either two independent
changed coordinates or one common change and one different change, again
giving a unit minor. The reference checks EVERY selected triple, not just
a favorable one.

Condition also on all other high columns. The two remaining uniform high
vectors map bijectively to(A,C), including over COMPOSITE q'. Thus a single
measured child has TWO independently uniform native frequency rows at q'.
The tag's secret- and high-label-independent Born mass preserves this law.
Fresh independent parent batches give IID children. Different potential tags
within the SAME fixed batch are NOT independent samples, and a fixed full
label matrix need not give a uniform empirical child-frequency histogram.

Allowing the grouping to depend on high rows invalidates this conditioning
argument. The hypothesis contract retains this restriction explicitly.

## Where The Algorithm Is Still Missing

The reference computes all words and counts, at cost O(3^M), then exports a
complete permutation. This is NOT a polynomial-time quantum compiler.
Classically calculating S(x) is easy; computing a word's fiber rank, ranking
modulo3, unranking its two partners and erasing the original index is not
supplied efficiently. A table, QRAM load, count oracle or witness finder
cannot be declared free. Approximate maps must preserve coherence and charge
all failures and trace error.

At d=r-1, q'=3 and M=n*(q/3-1)+1. When q=poly(n), the BATCH SUPPLY is
polynomial, unlike repeatedly paying a polynomial merge fan-in at every root
level. If an efficient low-row-dependent clean compiler for this complete
partition (or a costed constant-coverage alternative with the same output law)
were found, it would deliver native field-root samples in polynomial supply.
The existing field-root learner and known-low-digit correction could then be
composed, with source consumption charged at every recovery step. This is a
conditional target, not an implemented full-secret solver or an LWE attack.
When q is exponential in log-input size, n*q supply is itself exponential.

Important alternatives to the exact lexicographic map: a different efficiently
invertible low-row-dependent fiber partition, an approximate clean quotient,
or a constructive large-coverage matching. The existence of a nonzero carry
solution alone does not construct such an instrument. Algebraic carry circuits
contain mixed-variable terms; they are not diagonal polynomial systems.
The constant-degree diagonal-equation algorithm below cannot be imported.

The [nonlinear three-cycle compiler](TERNARY_NONLINEAR_CYCLE_COMPILER.md)
now shows that global rank/unrank and compressed tags are NOT necessary:
a costed low-only order-three action with adequate moved mass supplies a
clean inverse by canonicalizing just three words. No efficient nonlinear
action is provided. The [affine-line audit](TERNARY_AFFINE_LINE_EXTRACTOR.md)
implements a simple partial alternative, but proves its polynomial classical
direction menus have superpolynomially small typical success probability.

## Self-Refutation: Do Not Target Worst-Case Exact Lexicographic Ranking

There is a concrete counting reduction even at the CONSTANT prefix H=9 and
parent q=27. Encode a3-CNF formula with V Boolean variables and C clauses
into n=V+C frequency coordinates and V+C real qutrits:

- One domain coordinate per variable has frequencies(0,1). Target0 forces
  its qutrit to be0 or1, never2.
- In each clause coordinate a variable's first frequency is its positive-
  minus-negative occurrence count. Its second frequency is immaterial after
  the domain restriction. Add one slack qutrit with frequencies(1,2).
- Set the clause target to3 minus its number of negative literals, modulo9.
  The constraint is literal_count+slack=3. Counts lie in[0,5], so no modular
  wrap can create a false solution. Every satisfying Boolean assignment has
  exactly one slack extension, and every unsatisfied clause has none.

The real target fiber therefore counts satisfying assignments exactly.
Append enough ZERO frequency qutrits at the FRONT to make M>8n. The complete
source is an allowed original native source, and all its fibers are divisible
by3. Each target fiber has3^K dummy copies of its real solutions.

Known promised query words can always be provided: gate an arbitrary formula
by a new Boolean z. Clauses of length at most2 simply acquire z. For each
length3 clause(a,b,c), introduce y=z OR a with its three standard equivalence
clauses, then require(y,b,c). Every original assignment and z has a UNIQUE
extension to y. The gated count is original_count+2^V, and z=1 gives an
explicit known satisfying assignment.

Take that real word with all dummy digits0, and with only the LAST dummy
changed to1. Their lexicographic fiber ranks differ by the real fiber count.
All preceding complete fibers have cardinality divisible by3, so the logical
output trit of the full lexicographic basis permutation is rank mod3.
Subtracting these two trits and2^V recovers the original3-CNF count modulo3.
The construction, labels, padding and two promised query words are polynomial
in the formula size. The finite controls check the count relation directly
without enumerating the enormous padded source cube.

Thus an efficient exact WORST-CASE lexicographic basis compiler would also
evaluate3-CNF model counts modulo3. This is a computational reduction, NOT
a proven impossibility, generic quantum lower bound or hardness theorem for
the IID native-source problem. An approximate compiler correct on EVERY
computational-basis input with bounded error has the same counting consequence.
The two chosen basis inputs are not original uniform-amplitude source states;
the reduction does NOT constrain approximation only on those states. It also
does not constrain a DIFFERENT fiber partition.

REVISED TARGET: retain lexicographic grouping ONLY as an exact exponential
reference. Seek a nonlexicographic low-row-dependent partition, an IID-average
compiler or a source-state-specific approximation with a clean, costed error
argument. Do not turn the reference ranker into an implementation TODO while
assuming its mathematical existence makes it cheap.

## Refutation And Literature Boundaries

[Ivanyos and Santha](https://arxiv.org/abs/1503.09016) give algorithms under a
diagonal, constant-degree premise. The generated high-carry polynomials fail
that premise in explicit native controls. Their theorem is not a solver here.
[Goos et al.](https://arxiv.org/abs/1912.04467) show that an explicit generic
Chevalley--Warning search is PPA_p-complete. This does NOT establish hardness
of this specific structured native system, nor does existence imply a cheap
algorithm for it.
[Boucher, Fouque and Shen](https://arxiv.org/html/2609.34996v1) supply the known
native sieve and distinguish sample-only access from a preparation inverse.
The batch target seeks a different costed compiler, not a silent import of
their sieve or a claim to improve its runtime.

Falsifiers: a generated digit differs from the true ring frequency; its degree
exceeds the bound; an under-threshold count is falsely guaranteed divisible;
an occupied above-threshold fiber is not divisible by3; a basis word is lost
or duplicated; a selected pointed minor is not a unit; the physical branch
has the wrong root phase or Born mass; high-label selection is called low-only;
or a full-table reference is promoted to an efficient circuit or many outputs.

```
python theorems/ternary_batch_fiber_compiler.py --write
node research/certificates/ternary_batch_fiber_compiler_crosscheck.js
python -m pytest -q tests/test_ternary_batch_fiber_compiler.py
```
