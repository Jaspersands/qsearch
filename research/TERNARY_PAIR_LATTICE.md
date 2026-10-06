# Native Pair Lattice Geometry And Classical Falsification

LOCAL DERIVATIONS / REVIEW PENDING. Implemented exact representation and
ordinary classical baselines, NOT a new quantum algorithm or a polynomial
coverage guarantee. Read `TERNARY_PAIR_COLLIMATION.md` for the actual receiver.

## Arithmetic Interface

Original scalar native phase access at root3^r supplies M=r-2 qutrits. Their
stripped labels are independent paired(a_i,c_i) in Z_Q, Q=3^(r-1). An ordinary
solver must find TWO DISTINCT native words with sum of selected0,a_i,c_i equal
to an independent uniform target t. It receives no unknown secret, incoming
word, high phase trits, phase evaluator or state-preparation inverse.

The lattice solver is classical public arithmetic. If its pair coverage meets
the already established source contract, it HELPS a quantum receiver. This
does not by itself classically recover the unknown quantum phase secret and
is not a dequantization of the native source.

## Exact Representation

Write each original digit as z_i=(u_i,v_i) in
{(0,0),(1,0),(0,1)}. Let A=(a_1,c_1,...,a_M,c_M). Use the A2 embedding

```text
E(a,b)=(a+b,-a,-b), blockwise.
||E(3u-1,3v-1)||^2=18*(u^2+u*v+v^2-u-v)+6.
```

The parenthesized integer equals the centered positive quadratic form minus
1/3, so it is at least-1/3 and, being integral, is nonnegative. If it is zero,
the centered form bounds each squared coordinate displacement by2/3; integer
coordinates must therefore be0 or1. Testing those four points excludes(1,1).
For every integer z, squared norm is at least6M; equality is equivalent
to a valid original native word. Every illegal point has norm at least6M+18.
This is an exact certificate. Ordinary Euclidean distance to(1/3,1/3) prefers
the zero digit; independent Boolean choices incorrectly admit(1,1).

NONUNIT CASES ARE NOW COMPLETE. Let g=gcd(Q,A_1,...,A_(2M)). If g does not
divide t, the whole integer coset is provably empty, not merely missed by an
attack. Otherwise divide A,Q,t by g. A unit exists in the quotient unless its
modulus is1, in which case the full integer kernel is immediate. This resolves
the scalar no-unit exception from the earlier target note without assuming SNF.
It is NOT a construction for vector-secret congruences.

For normalized modulus Q'=Q/g and unit pivot p, choose

```text
z0_p=(t/g)*(A_p/g)^(-1) modQ'; other coordinates0.
B_p=Q'*e_p;
B_j=e_j-((A_j/g)*(A_p/g)^(-1) modQ')*e_p, j!=p.
L_j=3*E(B_j); T=E(ones)-3*E(z0).
```

The rows B generate the FULL congruence kernel, not just a sublattice, with
index Q'. For every lattice point l,

```text
||3E(l)-T||^2=||E(3(z0+l)-ones)||^2.
det Gram(L)=3^(5M)*(Q/g)^2.
```

At unit source scale this is3^(7M+2). Integer unimodular LLL transforms and the
entire Gram determinant are verified before decoding. The reusable Bareiss
Gram-Schmidt helper now also supports rectangular full-row-rank embeddings;
the older square source-certificate wrapper remains strict.

## Attacks And Cost Accounting

`theorems/ternary_pair_lattice.py` implements two public signed/permuted LLL
bases, exact rational Babai, each single +/-1 rounding deviation with all lower
roundings recomputed, and two small public center perturbations. Acceptance
always uses the ORIGINAL norm and congruence. A perturbed good score is not a
witness. Duplicate legal outputs never count as a pair.

The complete scheduled list has6*(1+4M) decodes. Scaling uses that LINEAR cap,
so larger cases do not silently lose entire second bases to a fixed256 quota.
The earlier fixed-quota pilot is not the final scaling result. Candidate/rounding
counts, both LLL preparations, all singletons, empty targets and failures are
charged. Basis preparation is not an internal wall-time-limited operation;
the finite width guard is not a general runtime proof. Reports preserve timing
and reference-enumeration costs separately. No exact CVP guarantee is supplied.

Coordinate deflation is a stronger second-witness baseline: after a verified
first word, force each of its2M alternate native digit choices and decode the
remaining M-1 registers at the shifted target. Each suffix gets a separately
charged basis/decoder. Terminal M1 slices are direct original digit checks.
This is not two unrestricted Boolean bits or uncharged recursive search.

## Conditional Proof Target

An exact CVP oracle returning a word whenever one exists suffices for a pair
finder using at most2M+1 calls: obtain the first word; any different second
word differs at some coordinate covered by the deflation slices. A guaranteed
CVP approximation with SQUARED factor strictly less than1+3/M also forces a
legal word whenever a word exists, by the exact18 norm gap. Apply the smaller
dimension's bound on each slice; terminal dimensions are solved directly.

These are conditional reductions, not implemented oracles. The required
approximation tends to1; ordinary LLL/Babai output provides no such guarantee.
Average-case one-witness success on original independent inputs does not imply
a pointwise guarantee on adaptively selected slices. Sliced labels, target and
the first witness are correlated. No such distributional reduction is assumed.

## Evidence And Falsifiers

The exhaustive Q9/M1 census covers all81 label pairs and729 independent targets,
including nonunits. There are25 actual pair targets; the solver verifies all25.
The gcd condition certifies56 empty integer cosets. Thus exact uniform coverage
is25/729, informative source acceptance100/729, all-failure raw least-trit score
829/2187. This is a constant-size control, not an asymptotic algorithm.

The live report has96 IID fresh-label/uniform-target trials,16 each at roots
r=4,8,12,16,24,32. Pair counts are0,0,2,0,0,0; one-witness-or-pair counts are
2,3,6,3,0,0. Coordinate deflation adds ZERO pairs. All complete scheduled
lists run; there is no second-basis omission in the final report.
It preserves one-witness and pair counts separately, all caps,
all source parameters, and charged deflation calls. Small cases have exhaustive
truth only as a separate reference; unknown truth at larger sizes is NOT
interpreted as hardness. A zero-hit16-trial batch occurs with probability
(31/32)^16, about0.60, if genuine coverage is1/32, so such batches cannot rule
out even constant coverage. Empirical sample fractions are not substituted
into the population4*beta quantum theorem.

Independent JavaScript replays integer A2 identities, full kernel/coset
completeness, Gram and unimodular determinants, accepted nearest-plane basis
coefficients, every tiny source target and larger-run witness/cost contracts.
It does NOT independently run LLL or certify heuristic misses as unsatisfiable.

Falsifiers for the route:

- Any accepted point has illegal native coordinates or the wrong original sum.
- A solver returns the same word twice or reports single-witness coverage as pairs.
- Preparation, deflation, empty targets, caps or Born-weighted work disappear.
- A fixed public basis/transcript depends on phase high trits or unknown secret.
- A polynomial list/call count is called a polynomial pair-coverage theorem.
- Small positive controls or missed large targets are promoted to a speedup or hardness.

The polynomial two-witness theorem remains missing. The next substantive task
is exact Babai rounding-error/coverage analysis on known legal words and slices,
with population accounting, rather than more blind seeds or UI work.

Run `python theorems/ternary_pair_lattice.py --write`, then
`node research/certificates/ternary_pair_lattice_crosscheck.js`.
FLINT's documented transform interface is [official python-flint documentation](https://python-flint.readthedocs.io/en/latest/fmpz_mat.html#flint.fmpz_mat.lll).
