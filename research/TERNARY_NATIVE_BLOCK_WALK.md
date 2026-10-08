# A Costed Native Block Heat Bath, And Its Missing Moves

IMPLEMENTED / LOCAL DERIVATIONS REVIEW PENDING. This tests a concrete
conditional-fiber sampler for the source-weighted erasure target. It is NOT
a fiber eraser, new speedup, generic circuit lower bound or novelty claim.

## Actual Proposal, Without A Whole-Fiber Oracle

For the original even native source at q=3^r, take public
F(x)=sum_i(0,a_i,c_i)[x_i], x in F3^M, with IID uniform full frequency rows.
Choose k word coordinates B uniformly, hold the other coordinates fixed,
enumerate all3^k assignments on B, and choose uniformly among assignments
with the SAME F modulo a committed prefix H dividing q.

The module supplies the actual complete conditional list, exact counts,
and a random update. A single step selects ONE block; it does not enumerate
binomial(M,k) blocks. Classical cost is O(n*M+n*k*3^k), polynomial when
k=O(log n) and M=poly(n). Local count/unrank is an explicit bounded table,
NOT a q^n count oracle. Uniform-integer preparation and reversal of that
table computation specify a coherent transition program; gate export and
aggregate precision are not implemented. A random classical sampler is not
itself a clean quantum eraser.

For each B, the heat-bath matrix is an orthogonal projection onto functions
constant on each conditional class. The average P is symmetric, stochastic
and PSD, with uniform stationary measure in each connected component. The
full uniform frequency fiber is uniquely stationary only if its graph is
connected. Quantizing a disconnected transition graph does not create its
missing edges. Standard quantum-walk speedups require charged transition
access and the relevant gap; they do not grant state preparation or mixing.
See [Szegedy's primary walk analysis](https://arxiv.org/abs/quant-ph/0401053).

## Exact Source-Law Obstruction To ALL Small Moves

A word pair differing at j coordinates has a nonzero difference signature
in the2M public rows. At every active coordinate the coefficient pair is
one of the SIX directed simplex differences

    (1,0), (0,1), (-1,0), (-1,1), (0,-1), (1,-1).

At least one coefficient is a unit at EVERY ternary prime-power prefix H.
Conditioning on all other rows therefore makes a fixed nonzero signature
uniform in (Z_H)^n. Its zero probability is H^-n, not a field approximation.
Opposite signatures define the same zero event. There are exactly

    V_(M,k) = (1/2) sum_(j=1..k) binomial(M,j)*6^j

unoriented signatures of support at most k. By a union bound,

    Pr[ANY nontrivial H-frequency collision within Hamming distance k]
      <= min(1,V_(M,k)/H^n).

On the complementary event EVERY native word is isolated under EVERY
exact-prefix-preserving move of support<=k. This includes block policies
depending on all labels and the current word, polynomial or exponentially
large direction menus, and implicit policies. The bound ranges over all
signatures before selecting a policy. No independence between signatures,
word edges or vertices is claimed.

When M=poly(n), H=poly(n) with H>=3 and k=O(log n), log V=O(log^2 n),
whereas log(H^n)>=n*log3. Freezing has probability1-exp(-Omega(n)) and,
for H>=n^a with fixed a>0, the exponent is Omega(n log n). Dense fibers
from an enlarged batch do not overcome this local-move obstruction.

At the informative near-entropy batch M=nr+c and FULL prefix H=q,
one can strengthen this to EXTENSIVE support, not just logarithmic support.
For k=floor(M/4), choose z=1/18 in the positive generating polynomial:

    V_(M,k) <= (1/2) z^(-M/4)*(1+6z)^M,
    V_(M,k)/G <= (3^c/2)*(512/729)^(M/4)
                 <= (3^c/2)*(11/12)^M.

The last comparison is EXACT since512/729<=(11/12)^4. For logarithmic
sample surplus c, the prefactor is polynomial while the bound decreases
exponentially in M. With that probability, ALL distinct full-fiber words
differ in MORE than a quarter of the entire input batch. Two large symbolic
controls retain the exact combinatorial bound and this rational envelope,
without enumerating their words, signatures or compatible blocks.

This stronger near-entropy statement does not assert the same quarter-
distance at an arbitrarily larger polynomial batch M. The logarithmic-
support barrier above still applies in that different regime. Large changed-
word support is not a gate-count lower bound: global affine/nonlinear macros
may have polynomial descriptions. The required advance is a costed such
macro, not brute-force enumeration of3^k block assignments.

For fixed labels with NO such collision, an operator with Hamming bandwidth
<=k that preserves the prefix is word-diagonal. Its commutation with the
secret encoding reproduces the earlier no-signal gate. This does NOT bound
a polynomial circuit whose elementary gates temporarily violate the prefix,
or a polynomial-description macro changing Omega(n/log M) coordinates.
Do not confuse register-local gates with a fiber-preserving local walk.
Ancillas or a different encoding need their own access/error argument.

## Complete Finite Native Replay, Not A Scaling Fit

The fixed native source is n2/q9/M5, with243 words and81 full frequencies.
Its one-site kernel is EXACTLY identity while233/243 of original word mass
lies in non-singleton FULL fibers. This is not a singleton-fiber artifact.
All rows and all small difference signatures are checked, not sampled.

The implementation also runs support2 and3 walks, a complete-block support5
positive reference, and a mod3 support2 contrast on the SAME original labels.
The complete-block kernel has exact fiber gap1, but pays3^M conditional
enumeration; it is not a polynomial compiler at growing M. A low-prefix
update can change the full frequency and cannot silently serve as a full-
fiber walk. Its different connectivity does not remove the existing higher-
prefix supply/coverage obligations.

For connected C-word fibers, a rational certified gap lower bound is
2*p_min/(C*(C-1)), from a path of at most C-1 edges between any pair.
For disconnected fibers an explicit component partition certifies gap0.
Single-point fibers use the trivial convention gap1. P is PSD, so no
negative-eigenvalue relaxation gap is hidden. These conservative certificates
are separate from efficient preparation and count every raw source word.

The original native family is stationary under the full-prefix kernel:
every allowed neighbor has the same F, hence the same secret phase. Merely
evolving that heat bath therefore does not decode it. Even connectedness
would only make a phase-preserving reflection/preparation ingredient possible;
one would still need initial access, inter-frequency interference and clean
source-weighted erasure. None is supplied by an existence or gap flag.

## Research Decision And Self-Critique

Cut small-support exact-full-fiber Gibbs/heat-bath proposals as a default
compiler at growing n. Their update program is real and cheap; their missing
moves, not simulator speed, are decisive. Do not simply increase a small
benchmark's block size and extrapolate its favorable gap.

The remaining constructive possibilities are NONLOCAL polynomial-description
moves, soft-constraint/intermediate-prefix-violating operations, alternative
encodings, or another noncommuting receiver. Global shallow kernel actions
already change many coordinates and are not excluded. Reusing their old
orbits at an unseen higher prefix remains blocked by its own separate law.
Any new move must expose complete reversible incoming access, coverage and
full-root error/copy costs rather than hide a partner-finding oracle.

A fresh literature check found the repo already implements the prime-field
quotient decoder and CLZ reduction from
[Kothari et al.](https://arxiv.org/html/2609.40321v1). Those field-root results
must not be advertised as a clean composite-root fiber transform. The known
[Ivanyos--Santha diagonal method](https://arxiv.org/abs/1503.09016) likewise has
constant-degree finite-field conditions; it is not an automatic full-prefix
compiler. No new implementation of either is needed in this pass.

Falsifiers: a complete kernel has a move despite a no-signature certificate;
the conditional list is truncated; symmetry/stochasticity fails; disconnected
fibers are assigned a positive full-fiber gap; prefix3 is substituted forq;
small rows hide a whole-fiber/count oracle; a bounded numerical control is
called an asymptotic compiler or a general quantum lower bound.

Gemini/Antigravity owns routine CLI/registry integration and full production
validation. Register scoped negative controls, not accepted algorithms.
