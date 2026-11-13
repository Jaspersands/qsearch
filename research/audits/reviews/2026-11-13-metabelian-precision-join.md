# Native metabelian HSP: final precision join

2026-11-13. Local source/proof audit; no API, network, Git, tests, or report
reread. With these corrections, the admitted source/descent and published deterministic SDE interfaces compose into the WRITTEN
fixed-c native algorithm. No numerical gate exponent or executable artifact
is asserted. Source locators use LF physical text lines.

## Coherent QFT, with a harmless decoding repair

Hales's retained text places Algorithm 3/Corollary 1 in Chapter 5
(3059–3122), and Theorem 10/proof in Chapter 9 (6006–6182), rather than the
online chapter numbering. Its chosen bump b_0 is fixed by p,R,M and does
not depend on the input vector. This is the essential uniformity premise.
Literal equal-radius intervals around rounded centers can overlap at a
boundary integer; use the following disjoint interiors instead.

Choose powers of two R,M with a=M/p>=64. Set j_i=round(Mi/p), and retain
the common integer offsets |t|<=h=floor(a/2)-1, circularly modulo M.
The sets j_i+[-h,h] are disjoint; nearest-integer decoding
i=round(pj/M) mod p sends j_i+t to i. Reversible exact division computes
(i,t=j-j_i), and its inverse reconstructs j modulo M. No postselection.

In Hales's proof let Phi_i=F_M F_(Rp)^(-1)|Ri>, and restrict it to this
interior to obtain b_i. Here F_(Rp) is only an analytical identity, not a
required implemented primitive. Outside that interior |j-Mi/p|_M>=a/4.
The positive matrix of reciprocal distances, zero inside each interior,
has row sums <=8(1+log p)/a and column sums <=8(1+log p), by the harmonic
series bound for equally spaced centers and for integer distances.
Observation 2's entry bound is 2 sqrt(M/(Rp))/|j-Mi/p|_M. The Schur bound
therefore gives tail OPERATOR norm <=16(1+log p)/sqrt(R), uniformly in input.
Hales's full-vector shift comparison, restricted to these interiors, gives
||b_i-shift_(j_i)b_0||<=4Rp/M. Their disjoint supports make the same bound
valid for the operator on arbitrary coefficient superpositions. Thus the
implemented real-arithmetic isometry W satisfies

    ||W-(F_p tensor b_0)|| <= e:=16(1+log p)/sqrt(R)+4Rp/M.

Since W is an isometry, | ||b_0||-1 |<=e. Normalizing the SAME b_0 changes
this bound to 2e. Tensoring any reference preserves operator norm, and
tracing the bump gives diamond/channel error <=4e. This is stronger than
an output-distribution estimate and applies to entangled source registers.
For 0<delta<1 it suffices, with ample synthesis slack, to choose

    R >= (1024(1+log p)/delta)^2,   M >=1024Rp/delta.

Then e<=5delta/256. Both register lengths are O(log p+log(1/delta)).
Repetition uses log(R) Hadamards plus arithmetic, not R iterations; F_M
uses O(log^2 M) controlled rotations. Exact reversible integer arithmetic
has polynomial BIT/gate/workspace cost in these lengths. Applying this
channel to |0> prepares the uniform F_p state; its bump may be discarded.

## Actual finite-gate BIT interface

Dawson–Nielsen proves operator-norm synthesis and polynomial expanded word
length, but 347–354 explicitly omits arithmetic-precision cost. Do NOT cite
that discussion alone as the BIT certificate. Kuperberg 2306.13158v2 instead
supplies it: Theorems 1.1/1.4 (68–137), interval data in Section 3.1
(225–266), and the precision/runtime proof in Section 6.4 (1827–1857).
For a fixed inverse-closed dense finite gate set in SU(d), fixed local d,
n-bit synthesis requires n+O(log n) gate bits, n+O(1) target bits, polynomial
classical BIT time, and polynomial EXPANDED word length. Compactness gives
R=O(1) in that theorem; this R is unrelated to the QFT repetition parameter.
Use computable algebraic fixed gates and compute the dyadic-angle target
entries to the prescribed precision. Compile each whole local controlled
rotation (up to global phase), rather than controlling a phase-ambiguous
single-qubit approximation. Constant local dimension makes this legitimate.
If there are J local gates, allocate delta/(16J) operator error to each;
telescoping and the isometry/channel bound pay their total error. Expanding
the returned word is charged, and actual inverses reverse the same word.

## Polynomial existence and the D-coordinate join

The source-checked deterministic fixed-degree SDE algorithm is uniformly terminating in polynomial time, including its Fact 2 call.
Its published constructive polynomial bound suffices for asymptotic
existence: run that algorithm, not an unspecified oracle or unbounded retry.
A numerical exponent/circuit artifact is unnecessary for this written
theorem. There is no solver-failure event to allocate; conservative arities
and the earlier finite rank/tree caps are unchanged.

There are at most B_q vector Fourier/preparation blocks, each with <=D
coordinate primitives. Give each coordinate CHANNEL error
delta=eta/(16 max(1,D) B_q). The full capped adaptive-channel hybrid has
error <=eta/16, including all erroneous transcripts and ABORT branches.
Precision lengths are O(log p+log D+log B_q+log(1/eta)); fixed c makes B_q
polynomial in the native parameters. Add the earlier <=eta/8 rank failure.
Together with clean original XOR-oracle costs, this closes only the written
poly_c(native bits,D,log p,label bits,log(1/eta)) composition. Implementation,
practical resources, priority, useful applications, and state-only transfer
remain unclaimed. Original coset labels must still be discarded, not used
as conditioning records for the mixed-input instrument.
