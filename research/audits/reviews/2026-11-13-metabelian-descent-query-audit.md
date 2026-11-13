# Native metabelian descent, capped branches, and classical query bound

2026-11-13. Independent local audit; no API, network, Git, tests, or live
reports read. Inputs are the parent METABELIAN_NATIVE_HSP_AUDIT.md, the
177-line source audit, BOUNDED_CLASS_METABELIAN_HSP.md 407–490, and the
native-scope packet. Scope is ONLY explicit exponent-p BCH input, p>c,
fixed class c, metabelian Lie algebra of dimension D, ordinary hiding oracle.

**Disposition.** The group descent, original-oracle lifts, finite scheduling,
and stated classical query bound are sound with the guards below. The
per-packet SDE/finite-gate compiler remains separately charged; no clock is inferred from a theorem label or empty report.

## 1. Intersection, descent, and exact completion

Write K=H intersect exp([L,L]). The source audit gives exact abelian samples
for K. Their annihilator Khat contains K. Check f(exp(k_i))=f(1) on a basis
of Khat; because Khat lies in the abelian normal ideal, all checks pass iff
Khat=K. A failed check returns ABORT. This is a fixed-batch certificate in
the ideal sampling process, not an unconditional approximate-QFT certificate.

For correct K, H<=M=N_G(K), K is normal in M, and S0=M/K is legitimate.
The hidden subgroup H0=H/K is transverse to the original derived ideal
modulo K and therefore to S0'. It is abelian. Every subsequent ambient
S<=S0 has S'<=S0', so H0 intersect S'=1 whenever H0<=S. No further
normalizer quotient is required; only restrictions follow.

Let S have class r>=2 and put N=S'. The full preimage of the quotient
image U of H0 is T=H0 N. Both H0 and N are abelian and N is normal.
In Lie coordinates t=h+n, so

    t'=[h,n] subset [s,s']=gamma_3(s),
    gamma_j(t) subset gamma_(j+1)(s),  j>=2.

The second statement follows by induction using t<=s. Since gamma_(r+1)(s)
is zero, class(T)<=r-1. This proves a STRICT class drop, not merely a
dimension drop or an unsupported claim that every such T is class two.

Every exact erased Fourier sample lies in U^perp. The annihilator Uhat
of any accumulated batch therefore contains U. Its full preimage That
is a public Lie subalgebra: it contains S', so it is closed under brackets.
It contains H0. Compute its lower central series from public brackets and
accept the restriction whenever class(That)<class(S). Exact recovery of U
is unnecessary; accepting a larger image that drops the class is valid.
If the test fails through the fixed rank cap, ABORT. There are at most c-1
accepted nonabelian restrictions, and transversality persists throughout.

In the terminal abelian S, ordinary Fourier sampling gives Rhat>=H0.
Basis membership checks through the original oracle pass iff Rhat=H0.
Otherwise ABORT. Lift these generators to M and append a basis of K.
Every lift lies in H because its quotient class is in H/K; together these
elements generate H. No equality with every earlier oversized Uhat is needed.

## 2. Original-oracle implementation and erroneous branches

Choose a public linear complement to K in log(M). It gives a section
sigma:S0->M of the quotient, not a claimed group homomorphism. Maintain a
matrix embedding each current Lie algebra S into S0. For an input x in S,
compute sigma(x) in original BCH coordinates, query f into a separate label
register, and uncompute the section workspace. This implements a derived
oracle with ONE original call and public polynomial field arithmetic.
The function is constant/distinct on H0-cosets because K<=H. Later
restrictions use the same section; there is no growing stack of quotient
words or a supplied hidden-subgroup membership oracle. Identity labels
are all the original f(1), which can be cached.

The process must also be defined on erroneous measurement transcripts.
A passed INITIAL membership check still proves Khat<=H, even when the
reverse inclusion fails. Since Khat<=exp([L,L]) is an abelian subgroup,
N_G(Khat)/Khat is always a valid public group. Its section oracle genuinely
hides (H intersect N_G(Khat))/Khat. It may have lost part of the desired H,
and transversality may fail; neither fact makes the circuit undefined.
Every later preimage of a quotient subspace is likewise a valid subgroup,
and restricting a hiding oracle always hides its intersection with that
subgroup. The public Kraus instrument is complete on arbitrary inputs.
Its correctness invariant is needed only on the ideal successful path.

Check every proposed SDE vector for the public equations and nonzeroness;
invalid or timed-out results cause ABORT. Range-check measured field labels
and ABORT on invalid encodings; extend the quantum gates to all padded basis
states. All branches have the same dimension, class, and attempt caps.
Membership checks on bad branches do NOT restore completeness of the answer.

## 3. Explicit caps and the global approximation argument

For D=0 return the empty generating set. Otherwise let 0<eta<1/2 and take

    T=D+ceil(log_p(8(c+1)/eta)).

There are at most c+1 rank batches: initial intersection, at most c-1
descent stages, and terminal abelian recovery. Conditional on any ideal
successful history, t=T uniform samples in a subspace of dimension<=D
fail to span it with probability <=p^(D-T). Thus their total failure is
<=eta/8. Early class acceptance only removes work and preserves correctness.

For an explicit source bound, use the parent's conservative equation bound
E=D(D+c)^(2c), A_1(E)=E+1, A_j(E)=(2j(E+1))^(4j^3) for 2<=j<=c, and
R=product_(j=1)^c A_j(E). These are polynomial in D for fixed c, assuming
the separately checked arbitrary-column SDE arities. Uniformly using all c
degrees is harmless even when the current class is smaller. One erased
sample uses <=R original sources and <=cR merge/solver nodes. Consequently

    original oracle calls <=2T+(c-1)TR+2D+1,
    solver invocations <=B:=max(1,c(c-1)TR).

The last 2D+1 counts both membership batches and the cached identity query.
If the scalar compiler is supplied with uniform expected BIT bound P_c on
these public inputs, cut each independent attempt at 2P_c and use at most
ceil(log_2(8B/eta)) attempts per invocation. Markov's inequality gives
per-attempt failure <=1/2 and total solver exhaustion <=eta/8. All attempts
reuse public coefficient data before consuming the quantum merge inputs.
An already bounded-confidence compiler may be substituted directly.
Thus amplification is polynomial in log(1/eta), not an eta^-1 timeout.

There are <=Bq:=8(c+1)^2 T(R+1) high-level uniform-preparation/Fourier blocks
(each vector-space block is counted once, not once per bottom gate).
Compile each to channel error <=eta/(8Bq), uniformly on its input, using
the separately charged finite-bit primitive. Modular arithmetic and public
linear algebra are exact. Compare the ENTIRE capped adaptive channel with
its ideal counterpart, retaining all measurement outcomes and ABORT flags.
Contractivity and the hybrid inequality bound total channel error <=eta/8.
This includes bad Khat and Uhat branches; it never asserts they contain the
true subgroup after approximation and never divides by a branch probability.
The ideal rank/solver failure bounds plus this error are strictly below eta.
Compilation precision has logarithm O(log(Bq/eta)); its complete gate/BIT
clock is inherited from the independent compiler, not proved by this count.

## 4. Free23: adaptive classical queries to the same native oracle

For p>3 take the five-dimensional free class-three algebra on X,Y, with
Z=[X,Y], A=[X,Z], B=[Y,Z]. The cyclic subgroups generated by logarithms with
nonzero (X,Y) component number

    M=(p^5-p^3)/(p-1)=p^3(p+1).

Every nonidentity element has order p and belongs to exactly one order-p
cyclic subgroup. Thus any difference g_i^-1 g_j of distinct queried elements
belongs to at most ONE member of this hard family. Choose H uniformly from
the family and label its p^4 cosets by a uniformly random injection into a
label set of size at least p^4. The representation and BCH arithmetic remain
public; no extra information about the label assignment is supplied.

Fix the algorithm's coins and run a simulated no-collision transcript,
assigning a fresh uniformly unused label to each NEW queried group element;
repeated element queries reuse their memoized label. The path is independent
of H. Its at most binom(q,2) distinct pairs test at most that many family
members. Until the first collision between distinct elements, this transcript
couples exactly to the real random injective oracle. If H is outside the
tested family, the final single subgroup output is fixed by this transcript
and is correct for at most one H. Averaging gives

    Pr[exact recovery] <=(binom(q,2)+1)/M.

Adaptive randomness and early stopping are covered by fixing coins/padding.
For q=2p^2 uniformly sampled DISTINCT elements, no coset collision has
probability <=exp(-(p-1)q(q-1)/(2p^5))<1/3 (p>=5). A collision's
nonidentity difference generates H. Thus the matching classical oracle
query complexity is Theta(p^2); the lower bound permits unlimited computation.
Label exhaustion only affects the trivial range of the displayed bound.
This is neither a non-oracle hardness/novelty claim nor a transfer of the
native oracle algorithm to the newer labelled-copy/state-only input.
