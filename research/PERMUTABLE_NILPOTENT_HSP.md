# Permutable Hidden Subgroups In Finite Nilpotent Groups

31 October 2026. Written reduction, with public algorithmic imports stated
below. Two independent automated reviews accepted the group argument and
identified the essential original-ambient normalizer invariant. Final
written composition review accepted the scoped result; all four focused
exact controls passed. These are automated reviews, not a human theorem review.
No novelty, implemented quantum solver or new separation is claimed.

Subsequent same-day result: `PERMUTABLE_SYLOW_HSP.md` extends the p-group
core to all solvable ambient groups and paid permutation inputs. It uses
Sylow intersection/generation, not the direct product in Section5.

## Scientific Question And Selection

Can ordinary HSP with a permutable hidden subgroup be solved without a
bound on the nilpotency class? This is a restricted form of the independently
posed question in [Morales, v2](https://arxiv.org/html/2608.05321v2),
Introduction. The previous `PERMUTABLE_LAZARD_HSP.md` paid the case c<p.
Its proposed next obstacle, constructing Omega1 in irregular p-groups, is
bypassed here: a chain of public second centers supplies class-two probes.

The corpus been-tried searches for Omega1 access and for prime-order
permutability/Baer norm found no matching complete algorithm. Baseline
lookups do not establish absence of a classical method. Parent inspection
of GAP 4.15.1 `grppc.gi:2594-2811` found lower-bound sampling, heuristic
central-quotient descent and explicit element enumeration in Omega_Search
when class>=p. `grppcatr.gi:916-944` expands conjugacy classes. These installed
methods do NOT pay a polynomial Omega1 interface. This is an access audit,
not a hardness result. No new Omega1 subsystem is warranted.

This route is selected over additional AG parity analysis without a new
selector and over another Rees receiver audit: it directly extends a complete
ordinary-oracle algorithm toward an external HSP question.

## Input, Proposed Claim And Baselines

Input: generators of a finite NILPOTENT group G with unique ell-bit
encodings, coherent public multiplication/inversion, and an ordinary
coherent function f with polynomial-width labels satisfying

    f(x)=f(y) iff x^-1 y belongs to H.

Promise: H is PERMUTABLE, meaning HX=XH for every subgroup X<=G.
Only H has this promise. Neither a Lie chart, hidden subgroup advice,
known order, Sylow decomposition nor efficient QFT on G is supplied.
Output: generators of H in ORIGINAL encodings. The written claim is
bounded-error quantum polynomial time in the full input/encoding size
and log(1/epsilon), for 0<epsilon<1, charging all public and f gates.
Both the class and the primes may grow. The trivial group is immediate.

The mechanism uses published nil-2 HSP on public subgroups, with paid
normalizer, composition-series and quotient preprocessing. The sharper
additive-query count in PERMUTABLE_LAZARD_HSP.md is not a bound here.
For a p-group of order p^b there are at most b^2 nil-2 HSP invocations.
All other work has a uniform polynomial clock under the interfaces below.

Strong quantum baselines are abelian HSP, normal HSP in solvable groups,
and unrestricted HSP in class at most two. The previous c<p composition
and fixed-class Rees scope are also retained. Classical enumeration and
generic collisions remain competitors; the abelian hidden-line subfamily
already has its familiar classical collision-query obstruction. No new
nonabelian classical lower bound, native cryptographic application or
advantage beyond existing abelian separations is established.

Morales TheoremC uses a structured quasi-Hamiltonian presentation; its
scalar-action results have other restrictions. Neither supplies this
generic hidden-H input contract. A bounded literature lookup is not a
priority proof. Novelty remains UNKNOWN.

The primary Holt--Subramanian2609.38085v2 Theorems7.1/7.13 were checked:
normal-core sampling still needs its Fourier implementation, and the
full-recovery extension assumes polynomial Baer-norm index. Those premises
are not inferred from a promise on H alone. This is a scope comparison,
not a claim that every possible consequence of their paper was exhausted.

## 1. A Prime-Order Permutable Subgroup Lies In The Second Center

For any P<=G and C<=P,

    (H intersect P) C = (HC) intersect P.

Thus H intersect P is permutable in P. Permutability also passes to images
in quotients. These assertions do not require P to be normal in G.

Let A be a permutable subgroup of order p in a finite p-group P. For a
cyclic C<=P, either A<=C, or A intersect C=1 and AC is a subgroup with
[AC:C]=p. In the latter case C is normal in AC. Therefore A normalizes
every cyclic subgroup and hence every subgroup of P. It lies in the Baer
norm, the intersection of all subgroup normalizers. The classical theorem
Norm(P)<=Z2(P) gives

    A <= Z2(P).

This proof includes p=2. It does not enumerate subgroups or compute the
norm. The all-prime norm inclusion is stated explicitly in
[Beidleman--Heineken--Newell, Centre and norm, Introduction](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/591EE56C40B909AFBCC22D882C39F90E/S0004972700036248a.pdf/centre-and-norm.pdf),
with Schenkman/Kappe references. The exact prime-order conclusion also
appears in [Cossey--Stonehewer, Lemma2.2](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/4E89829508B46B6FD7F4E2D3BFD5088D/S1446788700002810a.pdf/cyclic-permutable-subgroups-of-finite-groups.pdf),
J. Austral. Math. Soc.71 (2001),169-176. Their neighboring odd-prime results
are NOT used to justify p=2; the norm argument above does that.

The ambient p-group premise is indispensable: A3 is normal/permutable in
S3 but Z2(S3)=1. A nonpermutable reflection in the dihedral group of order16
likewise need not lie in the second center of that p-group.

## 2. Public Class-Two Probes Find A Nontrivial Hidden Intersection

Let Q be a p-group and K<=Q a nontrivial permutable subgroup. Compute a
public refined polycyclic series

    Q=Q1 > Q2 > ... > Q_(d+1)=1,   [Qi:Q_(i+1)]=p.

Choose, for the proof only, the largest i with K intersect Qi nontrivial.
Its intersection with Q_(i+1) is trivial. Since Q_(i+1) is normal in Qi,
restriction of the quotient map injects K intersect Qi into the group
Qi/Q_(i+1) of order p. Consequently |K intersect Qi|=p.
Section1 gives K intersect Qi <= Z2(Qi).

The algorithm does not know i or K. For each i it computes T_i=Z2(Qi)
and solves the ordinary HSP on T_i by the published nil-2 algorithm.
Each T_i has class at most two: its commutators lie in Z(Qi), which is
central in T_i. At the proof-selected index the recovered subgroup is
exactly K intersect Qi, hence nontrivial. At another index a larger
nontrivial answer also suffices. Thus all answers are trivial iff K=1.

No claim that every nontrivial permutable K meets Z2(Q) is needed. No
prime-order subgroup of the hidden K is supplied to the algorithm.

## 3. Recovery Must Recompute Normalizers In The Original Group

Now let G be a p-group. Maintain ONLY B<=H in the original fixed G,
initially B=1. Do not assume B is normal in H, or H lies in N_G(B).

1. If B=G, return B. Compute S=N_G(B) in the ORIGINAL G and Q=S/B.
   Here B is known and normal in S. The hidden subgroup in Q is
   K=(H intersect S)/B=N_H(B)/B, permutable by restriction and quotient.
2. For every level Qi of a public refined series of Q, compute Z2(Qi).
   Use the original f through a paid section of Q into S to recover its
   hidden intersection with K. Stop scanning at any nontrivial answer J.
3. If a J is found, replace B by its full preimage in S, generated by oldB
   and original-encoding lifts of J. This stays inside H and grows by at
   least a factor p. Return to step1 in ORIGINAL G.
4. If all answers are trivial, K=1 by Section2. Then N_H(B)=B. The
   normalizer condition in finite p-groups says every proper subgroup of H
   has a strictly larger normalizer in H. Hence B=H; return it.

The local oracle is well-defined because B<=H, even though H may not lie
in S. If sigma is any public section of S/B, then

    f(sigma(q))=f(sigma(r)) iff q^-1 r belongs to (H intersect S)/B.

The chosen representatives need not form a subgroup or a homomorphism.

With b=log_p|G|, there are at most b rounds: if H<G, at most b-1 growth
rounds and a terminal scan; if H=G, at most b growth rounds followed by
the immediate B=G check. Each scan has at most b levels, giving b^2
nil-2 calls. Larger intersections only improve this bound.

Essential falsifier: with H=G=D8, a valid chain can first return a reflection
B of order2. Its normalizer is a proper V4, so H is not contained there.
After learning V4, its normalizer in originalG is G again. Permanently
restricting the ambient group to the first V4 would lose part of H.
The stronger B<=H<=S invariant of the old Omega1 algorithm MUST NOT be
copied into this algorithm.

## 4. Public Access And Uniform Polynomial Cost

This uses the reviewed public bridge in PERMUTABLE_LAZARD_HSP.md Section7,
not a new coordinate/advice assumption. The primary imports are
[Ivanyos--Magniez--Santha](https://arxiv.org/pdf/quant-ph/0102014)
Corollary5/Theorem6 (solvable-group constructive membership, refined
series and nice factor maps), Theorem8 (normal HSP), and Theorem10
(quotients by known solvable normal subgroups). These are quantum
algorithms with charged public operations, not free classical interfaces.

For normalizers, [Ivanyos--Sanselme--Santha](https://arxiv.org/html/0707.1260)
Section3 imports polynomial p-group normalizer algorithms given refined
polycyclic presentations and efficient collection. The original constant
class assumption pays classical collection there. Here canonical normal
words are obtained by successive paid IMS factor maps and generator-power
removal. The classical normalizer algorithm makes polynomially many calls
on classical inputs; amplified quantum collection pays those calls even
when the class grows. Source-preparation/inverse costs remain charged.

Second centers are public. One can use the IMS center routine, or implement
the conjugation tuple x -> (x g_j x^-1)_j for fixed generators g_j. It
normally hides Z(P); normal HSP recovers it. Compute the center of P/Z(P)
and lift to obtain Z2(P). Both quotient denominators are known normal
subgroups. No hidden intersection is used to construct a public probe.
ISS Theorem1 supplies ordinary nil-2 HSP, including p=2 and growing primes.

Explicit flattening: if Qi=P_i/B, lift Z(Qi) to C_i<=P_i. Its quotient is
P_i/C_i. Lift that quotient's center to D_i; the probe is D_i/B. The nil-2
solver acts on D_i/B, NOT on the possibly higher-class preimage D_i.

All subgroups and known denominators are stored with polynomially many
generators in ORIGINAL encodings. Preprocess each quotient directly as an
original subgroup modulo a known normal subgroup, rather than wrapping a
new oracle around a chain of prior quotients. Word evaluation supplies the
forward section. Canonical quotient coordinates use paid nice factor maps.

After fixing valid preprocessing, a canonical coordinate function has a
unique answer. Retain its input, compute, copy the answer and uncompute.
Worst-input answer error delta gives operator-norm error <=2sqrt(delta),
also on entangled addresses. If T bounds all compiled calls, choose
delta<=(epsilon/(16T))^2 and use a hybrid bound; distribute the remaining
error among preprocessing and HSP calls. Cap time, stages and output sizes
on incorrect histories as well. Confidence costs are logarithmic. This
gives bounded error, not a Las Vegas completeness certificate from f checks.

## 5. General Nilpotent Input

Compute and factor N=|G| by the paid order algorithm and quantum integer
factoring. For each p^b exactly dividing N, choose the CRT integer e_p
with e_p=1 mod p^b and e_p=0 mod N/p^b, with 0<=e_p<N. A finite nilpotent
G is the direct product of its Sylow subgroups P_p. Thus x->x^e_p projects
onto P_p, and powers of the supplied generators generate P_p. Each power
uses O(log N) original multiplications. The same projections preserve H
because they are powers of its elements, proving H is the product of its
Sylow intersections. Each intersection is permutable in P_p.
Run Section3 on each ordinary restriction of f and combine its original
generators. If |P_p|=p^b_p, then sum_p b_p^2 <= (log2|G|)^2.
No Sylow or class advice is added to the input.

This step uses nilpotence. It is not an algorithm for all solvable groups,
all finite groups with a permutable hidden subgroup, arbitrary nilpotent
HSP, dihedral reflection HSP or copy-only access.

## 6. Proof Obligations, Falsifiers And Next Decision

Core group argument: independently reviewed; exact norm/prime-order source
statements checked. Public imports: reuse the already reviewed bridge,
with nil-2 as the terminal solver. Final written-note review accepted the
scope, clock and Sylow extension, and suggested the explicit CRT and probe
flattening descriptions incorporated above. No numerical data supplies any
asymptotic step.

Executed command (all four controls PASSED):

    /opt/anaconda3/envs/qsearch-cas/bin/sage research/classical_baselines/permutable_nilpotent_controls.sage

Result: short exact checks of the D8 original-normalizer trap,
the D16 nonpermutable reflection, the S3 ambient-p counterexample, and
Sylow recombination. These use exposed truth solely as mathematical
falsifiers; they do not simulate hidden-oracle access or certify runtime.
Only the exact asserted identities are established by this script. Repeat
after relevant identity changes only. Do not add a source backend or sweep.

Next hard question after validation is selected by external value: whether
this nilpotent upper bound is already implied by published permutable-H
reductions, and whether a motivated residual input exists beyond it. A
further subsystem requires a specific paid end-to-end mechanism. Novelty,
new classical separation, native application and implementation gates stay
false pending their own evidence.
