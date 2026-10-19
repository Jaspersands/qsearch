# Next Constructive Test: Folded Norm-Character Source

2026-10-19. UNADMITTED research hypothesis. The known CLASSICAL folded decoder
is now executed in `theorems/folded_rs_decoder.py`. The explicit norm-character
arithmetic, bounded full-source/FFT controls, scalar-rank collision bounds and
local finite readout proof are ALSO implemented; see FOLDED_NORM_SOURCE.md.
The large reversible quantum receiver is NOT compiled. No classical hardness, novelty or
speedup is asserted. This is a DIFFERENT explicit
problem, not a repaired N127 scalar-character result. Its point is a potentially
tractable known decoder, not another conditional phase-erasure interface.

## Why Consider It

The current scalar low-rate source needs decoding beyond half distance, and
the available finite capacity compiler is not implemented. Replacing its source
by correlated copies already lost the required single-copy interference.
Folded Reed-Solomon codes instead match block-sparse errors from the outset.
They have known linear-algebraic decoding and pruning algorithms. Their costs
and the changed public problem must be explicit; neither decoder nor a generic
oracle separation is a new contribution.

Primary references checked:

- [Guruswami--Wang, linear-algebraic decoder](https://eccc.weizmann.ac.il/report/2012/073/download/).
- [Kopparty--Ron-Zewi--Saraf--Wootters, improved pruning](https://eccc.weizmann.ac.il/report/2018/091/revision/1/download).
- [Sun--Wootters, current folded/scalar OPI context](https://arxiv.org/abs/2610.12357).

The old q^(s-1) enumeration bound is NOT the best known pruning algorithm.
The local randomized-pruning argument below is known in this literature,
not a proposed new theorem.

## Explicit Public Task

Prime p=3 mod4, odd folding m, n blocks, nm DISTINCT scalar points
a_(i,r)=gamma^(mi+r), r0..m-1. Public gamma must have verified sufficient
order; finding it and an irreducible degree-m field modulus are charged setup.
Use a specified F_p basis of E=F_(p^m), not an advice field embedding.

Find P in F_p[X], deg P<K, maximizing the number of accepted blocks:

```text
Z_i(P) = sum_(r=0)^(m-1) basis_r * P(a_(i,r)) - t_i in E,
accept_i(P) iff sigma_i * chi_E(Z_i(P)) = +1, optionally also Z_i(P)=0.
```

All shifts t_i, signs sigma_i, points and field arithmetic are explicit public
input, of size polynomial in nm and log p. A predicate is computed by a field
norm followed by a base-field quadratic character. No random membership oracle
or hidden shifted function is supplied. The scalar dimension is K and rate
K/(nm); confusing it with K/n would invalidate the entire comparison.

For odd m, p^m=3 mod4. The existing quadratic-character Fourier derivation
extends over E with the additive trace pairing, giving flat nonzero Fourier
probabilities. The coordinate dot-product QFT uses the COMPUTED trace-dual
basis. A public blockwise invertible multiplier changes phases and their
computation, not uniform nonzero probabilities; it must not be silently dropped.
This extension and all phases require independent derivation/tests before use.

FOLLOW-UP COMPLETE: folded_norm_source.py now computes/validates the trace
dual, norm character and actual canonical Gauss phase. At m31 it is -i, not
the naive prime-field +i. Local coordinate DFT, nonscalar linear-map and full
native source/herald/readout controls pass; wrong phase changes TV about0.702.
The whole-ball bound uses SCALAR dimension m*(j+r)-K and a nonintegral-block-
rank counterexample. Finite scores pay the extra observable radius. Bounded
pruning is separately charged at4096 trials, including full flagged-output
trace loss. No ideal exact decoder is silently substituted in that bound.

The hoped-for algorithm is polynomial in n,m,log p for FIXED decoding gaps,
plus the explicit pruning dependence below. No asymptotic classical competitor
lower bound is known for these norm lists, so there is no established speedup.
At n25,m31,p=2^61-1 the raw block-source values alone occupy47275 qubits,
before syndrome/work/decoder registers. These are logical register sizes, not
physical-qubit or feasible fault-tolerant resource estimates.

## Decoder That Could Remove A Real Blocker

Let H have K scalar Vandermonde rows on the nm points. Its kernel is the dual
GRS code of dimension k'=nm-K; known scalar multipliers convert it to ordinary
RS and preserve zero/nonzero BLOCK positions. The ordinary code is then folded.
This is one block source, not several separately read-out row sources.

For interpolation order s<=m, put C=n*(m-s+1) and
D=floor((C-k'+1)/(s+1)), requiring D>=0. A nonzero interpolant
Q=A0(X)+sum_(j=1)^s Aj(X)*Yj has deg A0<=D+k'-1 and deg Aj<=D.
Every codeword agreeing with the received word on G whole blocks satisfies
the induced polynomial identity if

```text
G*(m-s+1) > D+k'-1.
```

Solve the resulting coefficient-linear system for an affine space of candidate
polynomials. Under the standard distinct-power hypotheses its dimension r is
at most s-1. This space is NOT the final list; returning it is not decoding.

Pruning without field enumeration: a nonzero degree<k' polynomial vanishes
on at most Z=floor((k'-1)/m) WHOLE blocks. For each actual close candidate,
at every nonzero-dimensional pruning stage at least G-Z good blocks both
agree with the received word and reduce the remaining affine dimension.
Uniformly sample a block, impose its m received values as linear equations,
and repeat at most r times. Abort inconsistent systems; validate any resulting
unique polynomial against the ORIGINAL received word. Each close candidate is
found with probability at least ((G-Z)/n)^r per trial when G>Z.
Independent T trials miss it with probability at most(1-((G-Z)/n)^r)^T.
No known-correct-position or true-error support oracle is available to the code.
Pay all failed trials and fix randomness BEFORE coherent source preparation.

A finite example, now executed as a CLASSICAL decoder, NOT a quantum receiver:
n25,m31,K310, k'465, s4, t6 erroneous blocks, G19, C700,D47.
Then G*28=532>511=D+k'-1. The block distance lower bound is11, so t6
exceeds the guaranteed unique radius5. Pruning has r<=3, Z14, and
per-candidate success at least(5/25)^3=1/125. The actual random-error control
has affine dimension0 and recovers the true six-block error. This does not
certify a quantum output score, source ambiguity, gate count or advantage.

Run `python theorems/folded_rs_decoder.py --write`. A second p1019,n10,m15,
decoded dimension60,t4,s3 input also recovers errors beyond unique radius3.
The producer COMPUTES a native Vandermonde particular word and GRS multipliers,
converts to ordinary RS, decodes, converts errors back and checks ALL original
rank-K syndrome equations. At the large input K310, nm775, p2^61-1, the field
is NOT expanded to length p. Hidden error values/support are supplied only to
the calibration comparison AFTER decoding, never to the decoder.

A real ambiguous p1019 control forces a one-dimensional affine solution space
and exercises received-block pruning. Both actual close words are recovered,
with errors of weights3 and4 and the SAME original rank90 syndrome. No source
uniqueness or generic list completeness is promoted. Enumerating the ten possible
single-block draws independently gives success probabilities3/10 and4/10 for
those two words; three rank failures remain explicitly inconclusive. Duplicate
affine directions are rejected before assigning a false dimension-based bound.

The native wrapper pays for a K-by-K Vandermonde solve, quadratic point-product
work and field inverses, plus actual interpolation/RREF/pruning and full native
checks. It neither scans F_p^r nor assumes a free list. Independent tests replay
the full interpolant and every affine-direction polynomial identity. The old
scalar n127,m1,K39,ell32 task FAILS the strict root-count gate, as it must.
This change is not a backdoor assertion that its missing decoder was solved.

## Obligations Before Accepting A Candidate

1. CLASSICAL COMPONENT IMPLEMENTED: actual interpolant, affine-space solver,
   pruning, singular/ambiguous cases, native syndrome conversion and independent
   polynomial evaluation. A reversible quantum compiler is still NOT supplied.
2. LOCALLY DERIVED AND TESTED: block-source Fourier law with the trace-dual
   basis, norm computation and nonscalar coordinate-change countercontrols.
   Native phases are computed BEFORE GRS decoder conversion, not silently
   replaced afterward. A large reversible source/compiler is still missing.
3. LOCALLY DERIVED AND TESTED: collisions against EVERY smaller block weight. Support S of
   j blocks maps injectively only when m*j<=K. At union rank K, intersection
   dimension is m*(j+r)-K over F_p, not j+r-K over E. Using the scalar formula
   with alphabet p^m and the wrong syndrome dimension is a decisive falsifier.
4. LOCALLY DERIVED: radial score and EXTRA observable-radius bound for this
   F_p-linear code, with rational-filter enclosures and the scalar-capacity
   refusal. Independent mathematical review remains required.
5. Compile bounded randomized decoding reversibly; charge seeds, trial flags,
   source failure, cleanup, rotations, field arithmetic, trace error and QFT.
6. Run classical attacks FIRST. A successful decoder alone is not progress
   toward a new quantum algorithm: it is an existing component of a new task.

## Strong Classical Falsifiers

Compare equal-input interpolation and accepted-set completion, degree-budgeted
norm reconstruction, low-degree/Morse variants, affine-flat dimension and
algebraic square-root attacks. In particular rewrite accepted blocks as
Z_i(P)=a_i*V_i^2 over E, with a_i a public square/nonsquare matching sigma_i.
This is an explicit underdetermined quadratic system over F_p; its special
folded evaluation structure could make it much easier than generic MQ.
Do not assume MQ hardness. Test structured elimination, variable fixing and
validated randomized linearization before building a quantum compiler.

Even-degree extensions contain base-field lines on which the character can
be constant; this is one reason NOT to replace odd m by even m casually.
Odd m removes that simple subfield-flat shortcut, not all classical attacks.
The many scalar coefficients relative to the number of binary constraints
are another warning, not evidence of hardness or an automatic solver.

## Why It Probably Fails / Stop Rules

The explicit norm predicates may admit perfect classical completions, decoder
constants and folding overhead may overwhelm any advantage, the finite score
law may be too weak, or code-structured collisions may invalidate the source.
Known folded DQI already covers generic oracle variants; a reimplementation
without a new explicit task consequence has limited research value.

The source/decoder/local-readout pass is complete, with native basic classical
attacks in folded_norm_attacks.py. Their unchanged-input best scores21/25,
53/65,99/127 remain below the local conditional quantum mean floors. This is
NOT a runtime comparison or serious evidence against global classical methods.
Next attempt structured quadratic/norm completion or find a meaningful natural
reduction BEFORE building a quantum compiler. Reject the route if the classical mechanism
solves its target regime, or if quantum use still assumes an unavailable
operation. No accepted candidate, central negative or speedup claim is created
by this note. Do not add a family of named bridges around it.
