# Rees Homogenization Without An Original Positive Grading

2026-10-22. Exact algebraic stress test and local written argument,
UNDER REVIEW. The source algebra is known; no new HSP algorithm, practical
speedup, independent proof review, or quantum execution is claimed here.

## 1. Scientific Question

The complete finite Rees instruments previously used naturally graded
ambient algebras, although their hidden subgroups were nonhomogeneous.
That does not test a different potential mistake: silently assuming that
the ORIGINAL nilpotent group has a useful positive grading. The theorem
claims to construct one on a larger cover without such an assumption.

Use the known eight-dimensional Dixmier--Lister algebra, with its bracket
table as reproduced in [Bahturin--Goze--Remm, Section 4.2, Example 2](https://arxiv.org/pdf/1308.2396#page=9).
This is prior art, not a discovered family. We verify the characteristic-p
obstruction directly rather than extrapolating a characteristic-zero claim.
The original 1957 AMS PDF could not be fetched; the displayed source table
and the local integer calculations, not an unread original proof, were used.

Input model: its Lazard group over any prime p>3, or an m-fold direct sum,
with public structure constants and an ordinary hiding oracle or fresh
coset copies. The hidden subgroup remains arbitrary. The proposed Rees
mechanism and all of its classical diagonal-solving, source-independence,
precision and final recovery obligations are unchanged.

## 2. An All-Prime Obstruction Certificate

In a basis e1,...,e8 the nonzero brackets with increasing indices are

```
[e1,e2]=e5,   [e1,e3]=e6,   [e1,e4]=e7,   [e1,e5]=-e8,
[e2,e3]=e8,   [e2,e4]=e6,   [e2,e6]=-e7,
[e3,e4]=-e5,  [e3,e5]=-e7,  [e4,e6]=-e8.
```

Integer Jacobi identities hold. The lower-central series has dimensions
8,4,2,0, with L'=span(e5,...,e8) and Z(L)=gamma3(L)=span(e7,e8).
These descriptions follow from brackets with coefficient +1 or -1 and
do not rely on a numerical rank estimate at one prime.

Write a general derivation as a matrix D[output,input]. All equations
D[ei,ej]=[Dei,ej]+[ei,Dej] form an integer 224-by-64 matrix A.
The new module supplies 32 REPLAYABLE integer row identities

```
multiplier * unit_coordinate(j) = sum_a coefficient(a) * A[row_a],
j = 0,...,31;  multiplier in {1,3,6}.
```

The first 32 variables are the top four rows of D. Reducing these
identities over ANY field of characteristic other than 2 or 3 proves
that every derivation maps L into L'. This argument does not merely
specialize a rational nullspace and hope that the rank stays unchanged.
The diagnostic Smith factors are 48 ones, two threes and two sixes.
The small-prime ranks really change: 50 at p=2 and 48 at p=3, versus
52 otherwise. Those primes are excluded, not silently generalized.

The derivation identity now gives

```
D(L) <= gamma2(L),
D(gamma2(L)) <= gamma3(L),
D(gamma3(L)) <= gamma4(L)=0.
```

Hence EVERY derivation has D^3=0. This is basis independent. In
particular L has no positive integer grading: such a grading produces
a diagonal Euler derivation, multiplying degree-r vectors by r. Divide
all supported integer degrees by their largest common power of p first.
The resulting Euler derivation has at least one nonzero eigenvalue,
contradicting nilpotence. This also excludes a grading after a field
extension in the allowed characteristics, since the same row identities hold.

This is NOT a claim that all finite automorphisms are trivial. The module
checks the actual order-two diagonal automorphism with signs
(+,-,+,-,-,+,-,-). Nor does it exclude every action of the finite group
F_p^*: residue-class weights can alias modulo p-1. A bounded-weight
1,2,3 action at p>=7 would have no such aliasing and would give a positive
grading, but no broader finite-action impossibility is needed here.

## 3. A Growing Family, Not Just Eight Coordinates

Let L_m be the direct sum of m copies of L. For a derivation of L_m,
each diagonal block is a derivation of L. An off-diagonal block from
copy j to copy i maps into Z(L_i): apply the derivation to [x_j,y_i]=0
and project to component i. Since Z(L_i)<=L_i', every block has image
in the total derived algebra. Consequently every derivation of L_m
again has cube zero, and no positive grading exists for any m>=1.

Nevertheless the positive Rees construction has dimensions

```
dim L_m = 8m,    dim gamma2 = 4m,    dim gamma3 = 2m,
dim A = 14m,     original calls per lifted source = 3.
```

All public arithmetic remains polynomial in m and log p. The theorem's
conservative arities give a copy bound

```
3*(8m+t)*B2(4m)*B3(2m),
B2(r)=4*(r+1)^4,   B3(r)=729*(r+1)^6,
t=ceil(log_p(3/epsilon)).
```

This is a symbolic sufficient bound, not measured scaling or total runtime.
The existing cubic arithmetic backend can improve particular regimes;
that is separate from this obstruction check. No new candidate is admitted.

The direct-sum ambient must not be mistaken for a promise that H splits.
In L plus L, the diagonal h={(x,x):x in L} is a nonabelian hidden
subalgebra, with zero intersection with either individual factor. The
test retains all eight diagonal directions after Rees homogenization.
Independent factor restrictions would learn nothing in this control.

## 4. What Was Actually Checked

`theorems/rees_nongradable_control.py` builds the public algebra, checks
all basis-pair evaluation homomorphisms on its Rees cover, and checks
the cover's scale-two dilation. Bilinearity makes basis-pair checks
complete for each supplied Lie map, not random point tests. The public
compiler receives no hidden subgroup, expected decoder, or source labels.

The original apparent weights (1,1,1,1,2,2,3,3) fail immediately:
[e1,e4]=e7 has incompatible weights. At scale s the two sides are
s^3 e7 and s^2 e7. The genuine cover instead keeps a grade-two COPY of
e7 as well as its other occurrences, so evaluation remains a homomorphism.

Tests additionally cover integer certificate replay and corruption,
all modular derivation basis vectors, a nonidentity finite automorphism,
127-bit arithmetic, multiple ambient copies, and the coupled diagonal H.
For a nonnormal nonabelian h=span(e1,e5,e8), bounded actual coset-label
fixtures check selected tuple-oracle fibers. The element t(t-1)(t-2)e7
defeats a two-evaluation shortcut. Grade one retains all of h, including
its derived directions. Enumerating that small fixture's H is test-only.

No full mixed-state instrument or whole-group density was executed on
this new input. Its cover already has p^(14m) elements. The earlier dense
instrument controls remain separate; these algebraic checks must not be
reported as an end-to-end quantum run or an IID success experiment.

Replay:

```
python -m theorems.rees_nongradable_control --write
python -m pytest tests/test_rees_nongradable_control.py -q
```

The standalone report is research/reductions/rees_nongradable_control.json.
No central-registry, qsearch or UI integration is needed for this falsifier.

## 5. Decision And Limits

The tested Rees compiler does not assume that the original ambient algebra
admits a positive grading. The stronger all-prime obstruction certificate
makes this a distinct scope test, not merely another naturally graded example.
This does not prove the full quantum theorem, establish novelty, or supply
a naturally encoded classically hard application. Fixed explicit test H's
are ground truth, not evidence against classical algorithms with access to
an actual application's structure.

Falsifiers remain a failed integer identity, nonzero Jacobi expression,
evaluation or dilation defect, hidden-preimage mismatch, or uncharged source
access. No such defect was found in this pass. Avoid extending a benchmark
grid around this family; the useful next move is to simplify or falsify an
end-to-end input/recovery dependency, not to add more prime-size examples.
