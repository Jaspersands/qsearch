# Source-Conditioned Palette Compression

Status: **derived, review pending; not formally verified; novelty not established**.
This tests the live clean-subset binary proposal, not a new quantum algorithm.
Finite identities and explicit quotient-POVM extensions below are tested;
these checks do not replace independent mathematical review. The unconditioned
exact result is in `BINARY_CARRIER_INSTRUMENTS.md`; the present result is
approximate and retains every classical source label.

## Question

Can retaining all classical source irrep labels rescue a fixed palette of
large, overlapping subset-label operations at logarithmic coset-copy count?
The exact unconditioned compression fails after this conditioning. A possible
approximate replacement uses character orthogonality on large incidence cells.

Assumptions: finite G; null standard trivial-subgroup coset states; alternative
standard mixed states for H={e,h}, with h uniform in an involution class C of
size M. The same h occurs in all k inputs. First measure each source irrep
lambda, but do not use an individual physical row or further individual
quantum-register operation. Subsequent instruments/readouts lie in the
diagonal group algebra of a **fixed palette chosen before observing labels**.
Their choice within that algebra may depend arbitrarily on the source labels.
Independent ancillas and classical/quantum history are allowed within it.

The nonzero incidence cells have sizes a_1,...,a_c. Source labels on untouched
copies are still charged in the k-label classical distribution. Let L be a
certified lower bound on every nonidentity conjugacy-class size of G.

## Derivation

Put pi(lambda)=d_lambda^2/|G| and r_lambda=chi_lambda(h)/d_lambda. The alternative
source law is p(lambda)=pi(lambda)(1+r_lambda), independent of the choice of h
within C. Character orthogonality gives

    E_pi r_lambda^2 = 1/M,
    TV(p^tensor k, pi^tensor k) <= k/(2 sqrt(M)).

On a fixed source lambda of nonzero alternative mass, the informative state
is (I+rho_lambda(h))/(d_lambda+chi_lambda(h)). Its expectation of rho_lambda(g)
is

    f_lambda(g,h) = (chi_lambda(g)+chi_lambda(hg))
                   /(d_lambda+chi_lambda(h)).

On a cell these moments multiply across its independent source labels.
Use the homomorphic convention R_g|x> = |x g^-1>. The repository's old
`right_regular_matrix(g)` multiplies by g, so the verifier explicitly inverts
the argument. This distinction disappears for h but not general noncommuting
products; it is tested on every product in the finite groups.

The canonical regular lift is

    tau = (1/|G|) sum_g f_cell(g) R_(g^-1).

To see positivity, decompose the cell representation as direct sum_nu
V_nu tensor M_nu, trace the physical state over each M_nu, and replace that
factor by I_(d_nu)/d_nu in the regular representation. This gives a positive
trace-one state with exactly the specified group moments. Trace orthogonality
gives the displayed formula; absent irreps have zero weight. This is an
algebraic lift, NOT an automatically efficient physical transform. Parseval gives

    |G| Tr[(tau-rho_h)^2]
       = sum_g |product_i f_lambda_i(g,h) - 1[g in H]|^2.

At g=e,h the summands vanish exactly. Elsewhere define

    t_h(g) = E_p |f_lambda(g,h)|^2.

Split labels into |r_lambda|<=1/2 and its complement. On the good set,
`d/(d+chi(h))<=2`; column orthogonality and |x+y|^2<=2(|x|^2+|y|^2)
give a contribution at most 4(1/|C_g|+1/|C_hg|). The bad set has p-mass at
most 8/M by Markov under pi and p<=2pi. Since |f_lambda|<=1,

    t_h(g) <= t = min(1, 8/L + 8/M)  for g outside H.

Zero-weight labels d+chi(h)=0 must be omitted, not divided by zero or given
free information. Under the null, the moment is chi_lambda(g)/d_lambda and
its squared pi-average is 1/|C_g| <= 1/L for g!=e.

Trace-norm Cauchy-Schwarz and Jensen give the averaged cell bounds

    E_pi T(tau_0, I/|G|) <= e_0(a) = min(1, sqrt((|G|-1)L^-a)/2),
    E_p  T(tau_h, rho_h) <= e_1(a) = min(1, sqrt((|G|-2)t^a)/2).

Conditional on h, cells have independent source labels. Their law p is
independent of h's orientation, so these labels preserve the uniform prior.
In a common classical-label/regular-register space, the alternative source
block is the mixture of products of its cell lifts with the SAME h in every
cell. A product-state hybrid bounds its distance from
p^k tensor [average_h rho_h^tensor c] by sum_j e_1(a_j). The analogous null
distance from pi^k tensor rho_0^tensor c is at most sum_j e_0(a_j). Untouched
copies contribute their source labels but no quantum readout.

Replacing p^k with pi^k costs at most k/(2 sqrt(M)). The exact chi-squared
divergence of the c-copy shared-h mixture from the null is (2^c-1)/M, not
the expression for independent hidden members. The triangle inequality gives

    T_output <= min(1,
        sqrt((2^c-1)/M)/2 + k/(2 sqrt(M))
        + sum_j [e_0(a_j)+e_1(a_j)]).

For a fixed source tuple the physical algebra is a representation quotient of
C[G^c]. A finite group C*-algebra is a direct sum of full matrix algebras;
the kernel consists of the absent blocks. A positive complete physical POVM
specifies positive complete effects on each present block. Extend it to every
absent block by assigning identity to one fixed outcome and zero to the rest.
This is positive and complete, with unchanged probabilities on every lifted
physical state, whose absent blocks have zero weight. It depends on the source
tuple and protocol, NOT on h or the hypothesis. There is therefore ONE channel
on the joint classical-label/regular-register space, and data processing applies.
Independent ancillas and adaptive history within the algebra only change this
final POVM. No efficient block decomposition or physical lift is supplied or
needed for this upper bound.

## Uniform Symmetric-Group Bounds

For S_n, n>=5, every nonidentity conjugacy class has size at least n. Its
conjugation action is faithful: a nontrivial kernel would contain A_n by the
normal-subgroup theorem for S_n. An element centralizing A_n preserves the
support of every 3-cycle, forcing every point fixed when n>=5. Thus the kernel
is trivial. An embedding S_n -> S_|C| implies |C|>=n by orders. This uses the
standard simplicity of A_n, not an empirical minimum-class estimate.

For even n>=8, M=(n-1)!!>=8n (check n=8 and induct in steps of two).
Consequently t<=min(1,9/n). The implementation uses exact squared terms

    prior: k^2/(4M),       compressed state: (2^c-1)/(4M),
    null cell: (n!-1)/(4 n^a),
    alternative cell: (n!-2) 9^a/(4 n^a).

Square roots and their sum are rounded OUTWARD to powers of two by integer
comparisons. No float underflow is counted as zero signal. For each term
find b with its capped square root <=2^b. For r nonzero terms, their capped
sum is <=min(1, 2^(max b + ceil(log2 r))). Repeated cell widths are counted
with multiplicity. Exponent 0 means a vacuous bound, not evidence of success.

For fixed c and balanced cells at k=ceil(log2 M)+2, a_j=Theta(n log n).
The negative a_j log(n/9) term dominates log(n!), so both error sums vanish
superpolynomially, as do the prior and c-copy terms. This rules out the
specified fixed-palette architecture at an information-sufficient raw copy
budget. It is not a circuit lower bound for arbitrary collective measurements.

Live conservative bounds with balanced nonzero incidence cells:

| Group | Subsets | Cells | Bound on T |
| --- | ---: | ---: | --- |
| S_128 | 1 | 1 | <=2^-168 |
| S_1024 | 2 | 3 | <=2^-602 |
| S_4096 | 1 | 1 | <=2^-10795 |
| S_4096 | 3 | 7 | <=1 (vacuous) |

These exponents depend on the stated copy budget and partition. No
postselection or dense diagonalization is offered as a useful algorithm.

### Retain Small Cells Instead of Approximating Them

The balanced-cell hypothesis is unnecessary for the asymptotic exclusion.
Choose a retention threshold from the fixed cell sizes, before viewing labels.
Keep every small cell as its FULL physical input, with r raw copies in total;
lift only the l large cells. The reference binary pair now uses r+l coset
copies, all sharing h. Source labels on retained inputs are produced by their
ordinary physical QFT/label channel, not sampled independently of those
inputs. The large-cell source labels remain independent of the orientation
of h. Only those labels need the prior replacement; using k/(2 sqrt(M))
still overbounds its cost. Conditional tensoring with retained physical
states preserves trace norm, so only the large cells contribute lift errors.
The quotient-POVM extension tensored with the retained-input algebra is still
positive, complete and hypothesis-independent. Thus

    T_output <= min(1,
        sqrt((2^(r+l)-1)/M)/2 + k/(2 sqrt(M))
        + sum_(large cells j) [e_0(a_j)+e_1(a_j)]).

It would be wrong to charge one effective sample per retained small cell:
its ENTIRE raw copy count is retained. The API reports both the incidence
cell count and the effective coset-copy count to prevent this mistake.

For a bounded number c of cells, set the threshold to 2n. Then r+l<=2cn,
whereas log2 M=Theta(n log n). Every lifted cell has width >=2n, so its
alternative squared error is bounded by (n!-2)(9/n)^(2n)/4; the logarithm
is -n log n+O(n). The null error is smaller. At ANY polynomial raw copy
budget, the prior term also vanishes superpolynomially. Hence arbitrary
fixed-cell size profiles are excluded asymptotically, not just balanced
ones. The tested finite-size contract lets the caller choose a better
threshold; 2n is a sufficient asymptotic proof device, not an optimal choice.

The live unbalanced controls use two small cells of width 1 or 10 and one
large cell, over S_128, S_1024 and S_4096. Those small cells cost 2 or 20
raw reference copies, not two compressed samples. Retaining every cell
gives the original raw-copy information bound, which is correctly vacuous
at an information-sufficient copy budget. No efficient physical compression
or additional capability for the original algorithm is inferred.

## Adaptive Catalogue Cover

The single-palette proof does NOT justify conditioning on a source-selected
palette. There is nevertheless a separate extension, including selection
from later measured outcomes, without making that invalid conditioning step.

Fix a finite catalogue P_1,...,P_R BEFORE preparing or inspecting the input.
Assume every complete execution uses operations and a final readout within
the cell algebra of at least one entire listed palette. Support choices must
be classical and observable without disturbing an unmeasured quantum selector.
Assign each complete transcript to exactly one covering palette by a specified
deterministic rule, so the sectors are disjoint. Private randomness may be included in the
classical transcript; no uniform hidden prior after measurements is assumed.

For each j, define a comparison program Q_j. It follows the actual program,
but aborts BEFORE executing any operation outside P_j. If it finishes, it
keeps the transcript only if its assigned covering index is j; other completed
transcripts also become abort outcomes. Q_j is a complete channel within the
fixed-palette access contract, so its whole output distance is at most delta_j
from the preceding derivation, including the retained-small-cell extension.

Let B_j be Q_j's successful, SUBNORMALIZED classical output sector. Every
actual transcript assigned to j agrees with B_j under BOTH hypotheses,
because its entire prefix and final readout stayed within P_j. Restricting
the output to that sector cannot increase its half trace norm. Thus

    T_actual = sum_j (1/2) ||B_j(alternative)-B_j(null)||_1
             <= sum_j T(Q_j(alternative), Q_j(null))
             <= min(1, sum_j delta_j).

The first equality uses disjoint transcript tags. Erasing them or applying
the final classical decision rule only decreases distance. There is no
division by the probability of a chosen palette, and no substitution of a
uniform prior for an actual measured posterior. Overlapping catalogue entries
require the single assignment rule; simply counting a transcript several times
would invalidate that equality. The comparison channels are a proof device,
not a way to clone inputs or obtain an end-to-end classical simulator.

If R is polynomial, the raw copy budget is polynomial, and every listed
palette has a uniformly bounded number of cells, the asymptotic bounds above
vanish uniformly over the catalogue. The sum still vanishes. This covers
classical source/transcript adaptation among such whole-execution palettes.
It does not cover a catalogue that only contains each individual step: a
single run might collectively use many cells without fitting any one entry.

The API computes per-palette bounds from the supplied subsets, then applies
exact outward max-plus-log-count rounding. With two tested S1024 palettes
(balanced and unbalanced), it gives T<=2^-601. The S128 catalogue bound is
vacuous, as it must be if one per-palette bound is vacuous. Neither using the
average nor the maximum of the delta_j values alone is generally justified.

Finite controls use all 152 natural S3/S4 source triples. A first L outcome
and a source label choose R or T; the comparison catalogues are {L,R} and
{L,T}. They check all 3368 complete branch probabilities against direct
Kraus words, and keep all abort mass. S4 has unequal selection probabilities
under the hypotheses, explicitly refuting a free-prior/renormalization shortcut.
Two classical unit controls show why the sum factor can be necessary and why
perfect distinguishability conditional on a rare event is not unit success.

Critical exclusions: a post-hoc catalogue, missing final readouts, aborting
after an outside operation, unobserved coherent support choices, or merely
stepwise rather than whole-execution coverage. A polynomial-size DESCRIPTION
can specify exponentially many possible palettes. Consequently a large
necessary catalogue does NOT imply a large selector runtime. Arbitrary
efficiently described adaptive subset rules remain open. This extension is
review-pending and its novelty has not been established.

## Refutation Checklist

1. Build the canonical regular lift from actual finite irrep blocks and check
   positivity, trace, every group moment, and Parseval independently.
2. Check all source tuples in S3/S4, including zero alternative mass and
   characters near -d. Compare exact averaged distances to the proposed bounds.
3. Verify the source distribution, use the same h across cells, and do not
   replace a label-conditioned state by an unweighted source average.
4. Verify that source-controlled POVMs admit the required positive complete
   extension; no hidden physical row or multiplicity-space action is allowed.
5. Construct an adversarial label-dependent palette. Selecting arbitrary
   subsets AFTER viewing the labels invalidates the independence calculation.
   For a predetermined catalogue, check the separate abort-before-outside
   construction above; do not apply the iid cell calculation to selected labels.
6. Compare to existing nonabelian Fourier/sieve lower bounds and the repository's
   natural-carrier concentration results before claiming novelty.

Failure of this derivation should sharpen the positive mechanism: exploit
source-dependent grouping or actual operations outside the fixed-cell algebra,
with an outcome rule and implementation cost. A bounded number of small cells
is not by itself an asymptotic escape. Do not replace this test with more
small-group phase-word tuning.

## Persistent Refutation Controls

The verifier checks 701 positive-weight lifts: 81 for S3 (39 null and 42
alternative) and 620 for S4 (155 null and 465 alternative), across widths
one through three and every hidden member. Seventy-five S3 zero-weight tuples
are omitted only from the corresponding alternative; their null mass remains.
All source masses normalize. Positivity, every group moment, Parseval and
factorized second moments have residuals below 5e-15. There are 166 source
representations with absent irreps. Noncentral complex-coefficient polynomial
effects extend to positive complete regular-algebra POVMs and have matching
probabilities on the direct physical tensor states under every hypothesis.
A complex C3 regression tests conjugation conventions, not a candidate.

S3 transpositions have averaged lifted trace distances 4/9, 8/27, 16/81
at widths 1,2,3, with averaged Parseval squares 2,1,1/2. S4 perfect matchings
instead give distances approximately 0.7500, 0.6343, 0.5795 and Parseval
squares 8, 4.5, 3.3472. Do not infer that every finite group converges with
cell width. The normal Klein-four subgroup gives an exact obstruction in S4.
For g another nonidentity member of V4 besides h, the elements h, g and hg
all have cycle type 2^2. Source dimensions (1,3,2,3,1) and characters
(1,-1,2,-1,1) give f_lambda(g,h)=2 chi(h)/(d+chi(h)), always +1 or -1.
Thus t_h(g)=1 exactly. For every source tuple the cell moment has modulus
one, while rho_h has moment zero at g. Trace-norm duality gives conditional
distance >=1/2 for EVERY cell width, despite the source-averaged state being
exactly rho_h. The conservative bound is correctly vacuous. Merely checking
the averaged state would miss this obstruction.

An adaptive-grouping countercontrol selects only trivial S3 source labels.
Their alternative probability is 1/3 and their outside moment is one, not
the iid second moment 1/2. Subset selection after viewing labels invalidates
the independence estimate. This is not a useful symmetric-group algorithm;
those trivial sources become extremely rare with growing n.

## Prior Art and Remaining Risks

[Moore, Russell and Sniady, Sections 3 and 7](https://arxiv.org/html/quant-ph/0612089v3)
already exclude their adaptive combine-and-consume sieve architecture on
S_n wr Z_2. Here fixed overlapping subsets can be revisited coherently, but
arbitrary source-dependent regrouping is excluded. Neither theorem transfers
between these models merely by renaming the operation. This comparison does
not establish novelty; specialist review remains necessary.

[Moore and Russell](https://arxiv.org/abs/quant-ph/0511149) and
[Hallgren, Roetteler and Sen](https://arxiv.org/abs/quant-ph/0511148) already
establish the need for large entangled measurements. The repository's
`SPECTRAL_LABEL_BUDGET.md` addresses complete multiplicity-label capacity,
not this binary output law. None supplies a new positive algorithm.

Remaining risks: incorrect physical algebra membership, a hypothesis-dependent
POVM extension, correlated source selection, transfer to nonuniform priors or
pure coset inputs, and stronger prior art making this route test redundant.
Growing palettes, uncharged individual quantum operations and source-dependent
regrouping without a small whole-execution catalogue remain outside the useful
bound. They still need an explicit useful outcome rule and cost argument,
not merely an exemption.
