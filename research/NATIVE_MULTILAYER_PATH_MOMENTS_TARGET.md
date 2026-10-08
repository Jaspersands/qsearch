# Next Constructive Target: Native Multilayer Interference, With Torsion

RESEARCH TARGET / NOT A DECODER. Do not infer many-layer failure from the
one-layer phase/mixer bound. A specific higher-order native correlation is
now exactly checked in `ternary_hot_phase_mixer.py`.

## Implemented Two-Layer Decision (2026-10-08)

The exact engine specified below is now implemented in
`theorems/ternary_two_layer_path_transfer.py`; read
[the complete derivation](TERNARY_TWO_LAYER_PATH_TRANSFER.md). Its complete
closure has137 integer lattices and11,097 transitions. Exact signed transfer,
deleted-row Smith counts and complete native circuit censuses agree with an
independent JavaScript checker. The local derivation remains review pending.

All256 fixed quarter-angle combinations have been evaluated in three growing
regimes. The isolated torsion enhancement does not give a useful population
advantage in those circuits. Structural bounds exclude polynomial-batch
quarter-turn templates; a coarse continuous-angle bound also excludes the
near-entropy regime, including public label/target angle selection. Much
larger batches, different mixers and deeper circuits are not excluded by
that continuous bound. The historical specification below is retained as
the derivation trail, not as an outstanding implementation request.

The subsequent [exact continuous-loop supplement](TERNARY_CONTINUOUS_LOOP_CERTIFICATE.md)
certifies all137 self loops at ceiling1. It removes the larger-polynomial-
batch escape for this template and also covers coordinate-specific fixed
mixer angles and arbitrary fixed residual phase functions. Label-trained
function families, other mixer shapes and deeper circuits remain open.

## Concrete Mechanism To Test

For a two-layer phase/mixer circuit and an output word z, the squared
amplitude expansion contains four path words: two intermediate/initial
words on each branch. The uniform-target success selects y=F(z), leaving
joint residual phases on FIVE original words total. Pointed-pair uniformity
does not determine this expectation.

The actual tuple0000,0111,1011,1101,1110 gives coefficient matrix J-I on
four first native frequency rows. Its determinant is-3, so at a ternary
prime power its joint frequency law is not four independent uniform vectors.
The annihilator consists of0,(q/3)*(1,1,1,1),2*(q/3)*(1,1,1,1).
For f(d)=exp(-i*gamma*[d!=0]), write

    a=(1+(q-1)*exp(-i*gamma))/q,
    b=(1-exp(-i*gamma))/q.

Character orthogonality gives the mixed-sign four-phase moment

    E[f(D1)f(D2)conj(f(D3))conj(f(D4))]=|a|^4+2*|b|^4.

The all-same-sign moment is a^4+2*b^4; the executed pi-angle census checks
both because the phases are real then. A separate exact gamma=pi/2 census
checks the mixed-sign formula with genuinely complex phases. IID coordinates raise
these scalar moments to n. This is a real root-dependent correlation, not
a grant of matching native-state copies or a way to multiply unknown phases.

## Why It Could Fail

An interference contribution also contains mixer coefficients. Positive
phase correlation can cancel after summing COMPLETE circuit paths. A single
tuple says nothing about total multiplicity, signal normalization or growing
success. Even the relative mixed-moment boost has the uniform bound

    2*|b|^4/|a|^4 <=32/(q-2)^4,

using|a|>=(q-2)/q and|b|<=2/q. Thus the relative boost across n coordinates
is at most(1+32/(q-2)^4)^n. At q growing faster than n^(1/4), this one
torsion mechanism has vanishing relative enhancement. Small constant-root
correlation is not a growing-root algorithm. Bigger path families, adaptive
mixers or different root/coordinate regimes need their own argument.

## Highest-Leverage Next Implementation

Build a SOURCE-AWARE PATH MOMENT engine, not a generic variational optimizer:

There is a concrete finite transfer representation for TWO layers. Relabel
each coordinate of the selected output word z to0 using a native trit
permutation. The resulting two public difference rows remain IID through
an integer unit2-by-2 change of chart; product mixers are trit-permutation
invariant. Thus the uniform-target population can fix z=000...0.

Label the four branch words (x,t,x',t'). At ONE word coordinate their trits
have81 possibilities. Their native coefficient columns are two DISJOINT
four-bit masks A and B (which rows choose trit1 and trit2); a zero column
is ignored. Across M coordinates the pointed column lattice is generated
by a subset of the15 possible nonzero binary four-vectors. Repetition of
a column does not change its full-root annihilator. Therefore there are
at most2^15 seen-generator states, independently of M,n,q. Canonical integer
column HNF should merge many of them further; do not assume field rank
alone determines a state.

For a state lattice L let K be its annihilator modulo q. Four cost Fourier
coefficients depend only on whether each dual coordinate is zero. Count
that zero pattern by inclusion-exclusion on the16 coordinate subsets.
For a subset S fixed to zero, delete those matrix rows; integer Smith
invariants d_j give EXACT kernel cardinality

    q^(remaining_row_count-rank)*product_j gcd(q,d_j).

This obtains all zero-pattern counts without enumerating q^4 dual vectors.
Multiplying by a_1,a_2,conj(a_1),conj(a_2) or the corresponding b coefficients
gives the per-frequency-coordinate phase moment m_L. The full phase moment
is m_L^n, NOT a product of uncorrelated path averages.

Each81-pattern transition from L to L+span(A,B) carries the SIGNED/COMPLEX
qutrit mixer weight

    K_beta2(0,t)*K_beta1(t,x)
      *conj(K_beta2(0,t'))*conj(K_beta1(t',x')).

Run this finite weighted transfer for M word coordinates, with w_0({0})=1.
The resulting candidate exact formula is

    P_uniform(two layers)=(1/G)*sum_L w_M(L)*m_L^n.

The1/sqrt(D) initial amplitude and sum over D output words cancel as above;
no extra per-path normalization may be inserted. Transfer weights need not
be positive and are NOT Markov probabilities. Check the one-layer limit,
zero-angle limit, all-ones moment and small COMPLETE native populations
before treating this representation as verified. These checks are now
implemented for exact quarter turns. See the implemented decision above;
arbitrary-depth runtime and decoder claims remain unsupported.

- Represent a path tuple by its exact pointed one-hot coefficient matrix.
- Compute integer Smith invariants and full-root annihilator constraints;
  do not replace Z_(3^r) by F3 and lose torsion depth.
- Evaluate cost-phase expectations through the annihilator, with conjugate
  branch signs and all source coordinates retained.
- Compress path families using word-coordinate symmetry or transfer matrices
  while retaining mixer weights, multiplicities and COMPLETE raw success.
- First derive an exact two-layer population formula or a nontrivial bound
  for the actual native circuit, then test explicit label-sensitive mixers.
- Cross-check small complete label populations and independent arithmetic;
  compare classical rejection and existing Grover amplification at identical
  source density. Do not accept a fixed tuple's correlation as an algorithm.

Unknown/capped annihilator enumeration is not a zero moment. An exponential
path enumerator can be a reference but is not the compiled circuit or an
efficient research conclusion. Prioritize identifying a constructive
interference mechanism over adding validators for supplied correlations.

Falsifiers: image law fails a complete native population; omitted conjugate
signs; lost q-adic torsion; a positive isolated term disappears in the full
path sum; growing q kills the observed enhancement; a path enumerator or
phase-copy oracle supplies the claimed advantage; classical attacks exploit
the same useful relation at comparable cost.
