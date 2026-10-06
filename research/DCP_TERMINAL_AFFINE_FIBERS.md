# Native Terminal Fibers Cannot Usually Keep Physical Affine Tails

LOCAL DERIVATION / REVIEW PENDING. No independent mathematical review, new
decoder, accepted candidate, novelty or speedup. This is a density-scoped
obstruction to a particular terminal geometry, not a general DCP no-go.

Followup: `DCP_AFFINE_CUBE_HIERARCHY.md` tests larger cubes and dense tails.
It also supplies an actual arithmetic countercontrol showing that readable
residue phases can factor from SECRET-DEPENDENT junk without flattening it.
Clean fixed junk is optional; do not turn this note into a decoder rejection
gate when that requirement is absent.

## Research Decision

The previous first-plane work left large correlated matrix families open.
But even a successful matrix inverse does not ensure useful terminal carry
geometry. This pass tests that geometry directly, across ALL physical affine
charts in a fixed native packet, including public higher-label-adaptive charts.

For near-density-one native packets with q=2^(4n+1), m=n log2(q)+16, the
source-mean fraction of physical parity-kernel points belonging to ANY constant
two-dimensional affine plane has the following conservative bounds:

| n | Bound |
|---|---|
| 4 | 1, inconclusive |
| 8 | 2^-70 |
| 16 | 2^-372 |
| 32 | 2^-1591 |
| 64 | 2^-6487 |

These are derived source bounds, not seed statistics. At n32, Markov's inequality
also gives point fraction <=2^-795 outside a packet event of mass <=2^-796.
That does NOT certify any particular packet or prohibit rare planes somewhere.

For a public partition into physical affine 16-bit tails, clean rank-one tail
compression has uniform-secret/source-mean acceptance at most

    362/65536 + exceptional_point_mass.

At n8 this is below0.005524. Thus a nearly perfect dense phase transport cannot
end in such physical affine flat tails in this regime. Nonlinear physical
charts and quantum operations mixing different blocks remain open. The
existing background-adaptive first-bit normalizer is NOT contradicted.

## Exact Native Plane Count

Let A be IID uniform n-by-m labels modulo2^L. Test its subset-sum map

    f_a(x) = A*x mod2^a,   1<=a<=L,   x in F2^m.

Fix ANY physical anchor x. For independent binary directions u,v, partition
coordinates into P=(u=1,v=0), Q=(u=0,v=1), R=(u=1,v=1), plus unused coordinates.
Each nonempty category supplies an independent uniform modular sum S_P,S_Q,S_R,
with signs1-2x_i. Those signs preserve the IID native law. Equality of all four
corner residues is exactly

    S_P+S_R=0,  S_Q+S_R=0,  S_P+S_Q=0.

If only TWO categories are nonempty, the source probability is2^(-2an).
If all THREE are nonempty, then S_P=S_Q=-S_R and2S_R=0. Over modulus2^a there
are TWO choices per row, not one. The source probability is2^(n-3an).
Missing this two-adic torsion gives an incorrect rank-three count.

The ordered direction-pair counts are

    D = 3*(3^m-2*2^m+1),
    G = 4^m-3*3^m+3*2^m-1.

Each plane through the anchor has SIX ordered bases. Therefore the exact
expected number of constant planes through ANY fixed anchor is

    mu = D/(6*2^(2an)) + G*2^n/(6*2^(3an)).       (1)

Existence probability is at most min(1,mu). Averaging over uniform physical
anchors preserves this bound. No affine chart enumeration or random-chart
assumption is used; the incident-point event already quantifies over every
possible physical plane through each point.

## Parity Chart And Source Conditioning

The dense contract uses an invertible first-n-column binary prefix and uniform
points in C=ker(A mod2), of dimension m-n. Prefix acceptance is

    p_n = product_(j=1)^n(1-2^-j) > 1/4.

Let e(A) be the fraction of C points incident to a constant plane. Pointwise,
restricting from the full cube to C costs at most2^n. Conditioning the source
on prefix acceptance costs at most1/p_n. Consequently

    E[e(A) | accepted_prefix] <= min(1, 2^n*mu/p_n).       (2)

This deliberately loose bound does not borrow independence after conditioning.
It also holds for a label-selected parity syndrome, using its equal-size coset.
Low-only systematic row transport preserves equality of full modular residues;
it does not manufacture affine fibers. Arbitrary higher-label chart selection
WITHIN the fixed packet is already covered by e(A).

For the zero-syndrome phase packet F_A(x)=A*x/2 mod(q/2), equal F_A values mean
equal original A*x moduloq. Use a=L for the terminal gate, NOT a=L-1 without
accounting for that division. Uniform effective secrets mod(q/2) give exactly
the character orthogonality needed below. Full-modulus secret completion is
still a separate obligation.

## Polynomial Symbolic Scaling Ledger

The implementation avoids floating logarithms and gigantic decimal probabilities.
Use3^5<2^8 and G/6<4^m/4. With the conservative conditioning factor2^(n+2),

    E[e] <= 2^-b2 + 2^-b3, capped at1,
    b2 = 2an - ceil(8m/5) - n - 1,
    b3 = 3an - 2m - 2n.

It records the conservative single exponent max(0,min(b2,b3)-1), WITHOUT
underflowing a small positive probability to zero. Exact fractions are confined
to bounded calibration controls. For n16,m1056, testing a32 or a48 is
inconclusive; a56 gives a nontrivial bound. This does not impede early bit-plane
normalization. It identifies a late physical-affine closure problem.

## Clean Tail Compression: More Than An Exact-Plane Test

Consider an equal-size physical affine block of N=2^d points. Remove the e_block
points that are incident to a constant plane anywhere in the original cube.
Within each residue fiber, the remaining points contain no four distinct
points whose XOR is zero. Thus all unordered pair sums are distinct, giving

    binomial(fiber_good_size,2) <= N-1,
    fiber_good_size <= K = floor((1+sqrt(8N-7))/2).

For a uniform phase superposition on the block, averaging over uniform secrets
gives density-matrix eigenvalues equal to residue-fiber multiplicities divided
by N. The largest r eigenvalues sum to at most

    min(1, (r*K + e_block)/N).                    (3)

This bounds ANY secret-independent rank-r projection after any block-local
unitary, even with arbitrary known pointwise phases. Averaging over all blocks
and the native source yields min(1,r*K/N+E[e]). Public labels may choose both
the partition and target subspaces. The point-mass bound is uniform over those
choices. An ideal reference with a fixed clean tail lies in such a target
subspace, so its squared overlap cannot exceed that projection probability.

Clean ancillary workspace must be returned, or its FULL effective projector
rank must be included. Measuring/discarding arbitrary secret-dependent trash
can reset a register trivially and is NOT bounded as rank-one clean compression.
The argument does not rule out a decoder retaining such trash, nonlinear
block images, interblock mixing, or a different physical input distribution.
An affine operation in already NONLINEAR logical coordinates is not necessarily
a physical affine block and need not satisfy this gate.

The bound is uniform-SECRET MEAN, not an upper bound for every secret. At secret0
the packet is flat and projection onto a flat tail can succeed with probability1.
A decoder promising high success for EVERY secret must still survive the mean
gate, but no worst-case statement is inferred from an average.

## Attempt To Falsify The Direction

1. **Increase state supply.** The bound becomes vacuous as density grows. At
   n16,L65,m1248 it gives2^-65; at m1300 or m2080 it gives1. A modest polynomial
   increase in original states can therefore escape THIS obstruction. That
   does not construct usable fibers or prove a polynomial arithmetic inverse.
   Do not treat near-density-one geometry as a fundamental resource ceiling.
2. **Use nonlinear charts.** The enumerated dense matching is already such a
   chart and can achieve near-perfect transport. Its inverse is exponential.
   A compact polynomial nonlinear chart remains a serious positive target.
3. **Mix quantum branches across blocks.** The block-local spectral gate does
   not analyze that operation. It must not be relabeled a general decoder bound.
4. **Select exceptional packets/points.** Pay their source mass. A menu of R
   complete native packets costs at most R times the mean point bound. Arbitrary
   grouping from M original registers has up to M^m ordered menus: our n16,
   M=n^4 ledger correctly becomes INCONCLUSIVE. No false selection theorem.
5. **Global planes still exist.** A=(1,1,1,1),q4 has no plane through0 but has
   planes in its weight-two fiber. Small incident mass is not global absence.
   A=(1,7,2,6),q8 also preserves the constant plane(0,3,12,15).
6. **Torsion and overlap.** A=(2,2,2),q4 preserves the fully overlapping-category
   plane(0,3,5,6). It falsifies the naive q^-3 per-row source count.

Revised next research target: a polynomial NONLINEAR physical inverse with a
source-correct conditional carry law, or a genuinely interblock quantum readout.
Alternatively investigate increased-density packets with original-state costs
and real classical arithmetic baselines. Do not spend another pass perfecting
an exact first-plane matrix pencil without explaining its terminal geometry.
The classical two-forward-call baseline still applies to any classically
evaluable completed monomial transport; it does not simulate the DCP input.

## Verification

Module: `theorems/dcp_terminal_affine_fibers.py`; run it with `--save`.
Report: `research/phase_workbench/dcp_terminal_affine_fibers.json`.
Independent checker: `research/certificates/dcp_terminal_affine_crosscheck.js`.
Its distinct four-point enumeration verifies904 complete label tables and44,912
plane evaluations, exact source/prefix fractions, scaling bounds, Sidon caps,
selection ledgers and dependency hashes. Tests additionally exhaust binary caps
in dimensions2/3/4, inspect rank-r compression spectra, preserve positive trades,
and challenge density, fixed-secret, torsion and resource-scope mistakes.
These are implementation checks, NOT independent theorem peer review.
All100 focused terminal/Schur/source/pivot/carry/normalizer/dense regression
cases pass in26.08s, including22 new terminal-affine cases. Python/JS syntax,
JSON parsing and whitespace checks pass. Full production validation is not
claimed.

The quantum/lattice motivation is [Regev's primary paper](https://cims.nyu.edu/~regev/papers/quantum_average.pdf).
The plane and compression derivations here are local; that paper is not claimed
to prove this vector packet architecture, this obstruction, or its novelty.
Full registry/CLI/UI integration and production regressions remain Gemini work.
