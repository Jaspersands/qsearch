# Native community detection: log-free classical trace bound

2026-11-13. Independent proof, with fixed even p>=4 and fixed k>=3.
The assigned primary is Schmidhuber--Hastings, arXiv:2607.29672v1,
`audits/sources/2026-11-13-community-baselines/sharp_kikuchi.txt`.
Actual sections 4.1--4.2, ALL of section 5, section 6 and Remark 2.7 were
read. Fresh STATE/TRAPS and the corpus been-tried/baseline queries preceded
the source read; those queries supplied no applicable earlier disposition.
No network, API, Git, numerical control or live paid report was used.

**Disposition.** The native classical detector has a log-free sufficient
threshold and a finite BIT clock n^(ell+O_p(1))*poly(B). No transfer of the
source's iid-clause theorem to Bernoulli supports is needed. Its active-label
lemma gives a DIRECT UNNORMALIZED trace bound for every deterministic subset
of distinct p-edges with independent signs. Analysis-only symmetrization
then handles the actual centered Bernoulli input. The detector uses Y-q,
without an additional observed graph, generated Z, gauge, labels or oracle.

The SAME bound also applies to the ordered operator in the already paid
quantum construction. Consequently the old log-squared-level quantum clock
is superseded, but classical dominance over the upgraded quantum clock is
NOT proved. Section 8 states this immediate reuse precisely.

## 1. Native statement and source scope

Let p=2d, d>=2 fixed, and let d<=ell=o(sqrt(n)). Put

    Omega=binom([n],ell), N=binom(n,ell),
    D=binom(ell,d)*binom(n-ell,d).

For a p-edge E, A_E is the symmetric partial matching with
    (A_E)_(S,T)=1[S symmetric-difference T=E].
It has norm one, A_E^2=P_E is the legal-row projector, and
    sum_E P_E=D I.
These are source equations 4.1--4.4 (physical lines 640--708).

Input consists of every edge bit Y_E and rational q=a/Q in (0,1/2), with
at most B bits in its numerator and denominator. Under the null the bits
are independent Bern(q). Under planting, conditional on arbitrary labels
x in [k]^n, they are independent Bern(q+epsilon*f_x(E)), where

    f_x(E)=sum_c product_(i in E)(1[x_i=c]-1/k),
    0<epsilon<q.

All probabilities are valid in this native range. The actual matrix is
    A=sum_E (Y_E-q) A_E.
There are constants C,c>0, depending at most on p,k, such that for all
sufficiently large n along any such ell sequence:

* Under the null, ||A||<=C sqrt(D ell) except with probability 2n^(-2ell).
* Uniformly for EVERY label vector, planting gives lambda_max(A)>=
  c epsilon D-C sqrt(D ell), with the same failure bound.
* Thus epsilon^2 D >= C_(p,k) ell suffices for strong detection.

The clock below also gives error O(n^-4)+2n^(-2ell), not merely constant
success. Since D=Theta_p(n^d ell^d), at fixed q this is

    beta=epsilon/sqrt(q(1-q))
       >= C_(p,k,q) n^(-p/4) ell^((2-p)/4).                 (1)

The classical construction itself works for variable q with the displayed
epsilon threshold; no q-uniform normalized-SNR constant is asserted.
In particular (1) and the quantum reuse below are only at fixed q, or with
a fixed positive lower bound on q; q=1/4 is the primary native example.
There is no sparse-q log-free SNR theorem in this note.
The theorem concerns DETECTION only, not recovery or refutation.

Source Theorem 5.3 (LF1117--1192) is stated for Poisson or iid uniform
physical supports; repeated supports can be distinct physical labels.
Native Bernoulli edges are a different law. Remark 2.7 (LF406--415) allows
vanishing bias in its own occurrence model, and does not itself change that
law. Section 6 uses a planted Boolean gauge unavailable for multicommunity
f. Neither is imported as a ready-made native theorem. The following direct
proof instead uses only the finite walk geometry of source Lemmas 5.1--5.2.

## 2. Deterministic-support, unnormalized trace proof

Fix ANY deterministic numbers u_E in [0,1], one per distinct p-subset, and
independent fair signs sigma_E. Write T=sum_E u_E sigma_E A_E. Conditional
on these coefficients, expand E_sigma Tr(T^(2t)). A surviving word uses
every edge an even number of times. Its nonnegative coefficient is at most
one, so it suffices to count these words. A label is active when its prior
multiplicity is odd. Each surviving length-2t word has exactly t openings
(use of an inactive label) and t closings (use of an active label), and at
most t distinct labels. Supports, rather than occurrence labels, are used.

At a prefix let S be its current row, S0 its initial row, a the number of
distinct exposed labels, and U their vertex union together with S0. Set
    chi=ell+d*a-|U|.
Every first-use edge has exactly d exterior vertices outside S. If h were
previously exposed, its first use increases chi by h. Thus chi>=0 is
nondecreasing, final chi is the sum of these h, and |U minus S|<=d*t.
In particular the exposed exterior set has size O_p(t), not ell+O_p(t).

Here is the source's active-label inequality, with its proof checked.
Let O be the active labels, V their support union, and Vplus=V minus S0.
The fresh exterior vertices originally introduced by active labels are
distinct and outside S0, so |Vplus|>=d|O|-chi. Write
    b=|S minus S0|=|S0 minus S|.
Parity gives S symmetric-difference S0 = symmetric-difference_(E in O) E.
Hence Vplus intersect S=S minus S0; each vertex in Vplus minus S occurs
in a positive EVEN number of active supports, and every vertex of S0
minus S occurs at least once. Of the total 2d|O| active incidences, at most
    2d|O|-2(|Vplus|-b)-b <= 2chi+b <= 2chi+ell
can lie in S. Every active legal edge consumes d such incidences. Therefore

    number of active legal edges <= (ell+2chi)/d.           (2)

This is source Lemma 5.1 (LF1076--1088), a pointwise combinatorial fact.

The extension counts are now deterministic. A previously seen inactive
opening has at most t choices. A first-use opening with exactly h recycled
exterior vertices has at most

    binom(ell,d) binom(d*t,h) binom(n-ell-h,d-h)
       <= D (2d^2 t/n)^h                                  (3)

choices, for n large, ell<=sqrt(n), and 0<=h<=d. For h=0 the bound is D.
For h>0, divide by binom(n-ell,d), use
binom(N0-h,d-h)/binom(N0,d)=(d)_h/(N0)_h, and N0-d+1>=n/2.
Counting all possible supports only enlarges any prescribed support subset.
No conditional distribution or deletion identity occurs here.

For fixed final excess chi, specify each step as new opening, old opening,
or closing: at most 3^(2t) patterns. Assign nonnegative h to the at most t
first uses, with total chi: at most 2^(chi+t) choices. Thus at most
18^t*2^chi chronologies suffice. The concrete recycled vertices are already
summed in (3); no further identity choices are hidden in this count.
Only patterns with t openings/closings and at most t first uses need be kept.

For all sufficiently large n, D>=t when t=floor(ell ln(n)/64). Each old
opening is therefore bounded by D. Using (2), final chi bounds every
closing by (ell+2chi)/d. Multiplication of these uniform extension bounds
along one chronology, then summation, proves

    E Tr(T^(2t))
      <= N (18 D ell/d)^t
            sum_(chi>=0) (4d^2 t/n)^chi (1+2chi/ell)^t.    (4)

This backward/tree counting is purely finite. Dropping terminal row and
parity restrictions during individual extensions only overcounts; completed
even-label words return to the original underlying set automatically.
In particular no exchange of incompatible branch filtrations is required.

For ell<=sqrt(n),
    (4d^2 t/n) exp(2t/ell)
       <= (d^2/16) ln(n) n^(-15/32) <= 1/2
eventually, uniformly in ell. Since (1+2chi/ell)^t<=exp(2t chi/ell),
the sum in (4) is at most two. The lower bound
t>=ell ln(n)/128 holds once ell ln(n)>=128. Taking, for example,
the deliberately enormous explicit constant C=2^300 gives

    Pr(||T||>C sqrt(D ell))
       <=2N (18/(d C^2))^t <=2n^(-2ell).                  (5)

Indeed ln(d C^2/18)>384. All sufficiently-large-n conditions are explicit
scalar inequalities depending only on fixed d. No empirical constant,
unproved small-n claim, Poissonization, normalized matrix or degree
concentration is used. This proves the needed log removal directly.

## 3. Independent-copy symmetrization: no actual Z required

Let theta_E be ANY independent-Bernoulli success probabilities, and define
    H=sum_E (Y_E-theta_E) A_E.
Take an independent copy Y' solely in the proof. Convexity of the
Schatten-2t norm to its 2t power gives, conditioning first on Y,

    E Tr(H^(2t))
       <= E Tr((sum_E (Y_E-Y'_E) A_E)^(2t)).               (6)

Each difference is 0 or +/-1. Conditional on the entire unsigned support,
its nonzero signs are independent fair signs. Thus (4)--(5) apply uniformly
to every support; averaging introduces no loss. Equation (5) holds for H.
This is valid conditional on EVERY planted label vector, even though the
theta_E differ across edges. No covariance approximation is used.

Under the null theta_E=q and H=A. Under planting
    A=epsilon M_x+H,  M_x=sum_E f_x(E) A_E.
The alternative actual Y-Z proposal also satisfies (5) under the null,
since its support is Bern(2q(1-q)) and its signs are fair conditionally.
It is unnecessary once (6) is used. In particular the native algorithm
neither requests nor fabricates a second statistical instance.

## 4. All-label planted witness on the SET slice

This pays the multicommunity signal without a Boolean gauge or block-slice
invariance claim. Fix any community c and let
    w_a(i)=1[x_i=a]-1/k,  v0=(w_c/||w_c||)^tensor(ell).
For every label vector, ||w_c||^2>=n/k^2 and |w_c(i)|<=1.
On the full ordered tensor space define the PSD lift

    B_lift=sum_(J subset [ell], |J|=d) sum_a
              (tensor_(j in J) |w_a><w_a|) tensor I_(J complement).

Its norm is at most k binom(ell,d)n^d. Retaining community c alone gives
    <v0,B_lift v0>>=binom(ell,d)n^d/k^(2d).                (7)

Let Pi be collision-free projection. Each coordinate marginal of v0 has
maximum mass <=k^2/n, so
    1-||Pi v0||^2 <= binom(ell,2)k^2/n.
The normalized v=Pi v0/||Pi v0|| satisfies
    ||v-v0||<=k ell/sqrt(n).
It is fully symmetric under all ell coordinate permutations.

Let K_x be the ORDERED native matrix with coefficient f_x(E) when exactly
d positions change, with all 2d changed vertex labels distinct, and zero
otherwise. It is not literally Pi B_lift Pi. For each row and choice of J,
an unwanted term must place one new vertex in the old J vertices, giving
at most d^2 n^(d-1) assignments, each of magnitude at most k. Symmetry and
the row-sum bound therefore give

    ||Pi B_lift Pi-K_x||<=k d^2 binom(ell,d)n^(d-1).       (8)

By (7)--(8),
    <v,K_x v> >= binom(ell,d)n^d
          [k^(-2d)-2k^2 ell/sqrt(n)-k d^2/n].             (9)
For ell=o(sqrt(n)) the bracket is eventually at least k^(-2d)/2,
uniformly over all labels. This supplies a concrete sufficient-n condition.

Define the genuine isometry from the ell-SET slice by
    W|S>=(ell!)^(-1/2) sum_(orderings of S) |ordered S>.
Every legal set transition has exactly d! ordered target lifts for each
ordered source. Therefore, EXACTLY,
    W* K_x W=d! M_x.                                    (10)
Since v is symmetric, z=W*v is a unit vector. Using
D<=binom(ell,d)n^d/d!, equations (9)--(10) yield

    <z,M_x z> >= D/(2k^p).                              (11)

This vector is an analysis witness only. The algorithm never learns c,
x, w_c or z. In particular (10) does not conflate the ell-set isometry W
with the p-block isometry J in the earlier guide certificate.

## 5. Detection and completely finite integer clock

Set c=1/(2k^p), C=2^300, and T0=C*ceil(sqrt(D ell)), an integer. The preceding
bounds give null norm <=T0, and planted largest eigenvalue >=4T0 whenever,
for example,
    epsilon^2 D >= (12C/c)^2 ell.                        (12)
The margin uses ceil(sqrt(D ell))<=2sqrt(D ell). Weyl's inequality and (11)
apply on the uniform centered-noise event (5). A Rayleigh concentration
argument is not required; it would also follow from sum_E P_E=D I.

Work with the exact INTEGER matrix
    Z=Q A=sum_E (QY_E-a) A_E,  H0=Q T0.
Let s=ceil(log2 N)+2. Draw a uniform Rademacher vector r in {+/-1}^N,
compute Z^s r by s exact matrix-vector products, and accept planting if
    ||Z^s r||^2 > N H0^(2s).                             (13)
Under null norm <=H0 this cannot accept. If Z has an eigenvalue >=4H0,
let e be a corresponding unit eigenvector. For this fixed e,
    E(e.r)^2=1,  E(e.r)^4<=3,
so Paley--Zygmund gives Pr(|e.r|>=1/sqrt(2))>=1/12. On that event
||Z^s r||^2>=(4H0)^(2s)/2>N H0^(2s), proving (13).
Repeating ceil(48 ln n) times gives failure at most n^-4. Logarithms in
the algorithm can be replaced by integer bit lengths with larger constants.
No numerical eigenvectors, inverse square roots, tolerances or variable
random-bit rejection loops occur.

Each row has exactly D possible neighbors, enumerated by deleting d
vertices and inserting d new vertices. Entries have <=B+1 bits. A coordinate
after s multiplications has O(s(B+log D)+1) bits, since the absolute row sum
is <=QD. Squaring, summing and comparing in (13) preserves polynomial bit
length. Combinatorial ranking/unranking and edge lookup are explicit and
polynomial in n,ell,B. Reading/storing all binom(n,p) observations is charged.
The full clock is n^(ell+O_p(1))*poly(B), with finite random-bit usage and
no factoring, spectral, matrix or statistical oracle. All error bounds
are asymptotic for the sufficient-n scope already stated; no unverified
small-n threshold is claimed.

## 6. What happened to the proposed normalization transfer?

The proposed floor Gamma=sum_E |X_E|P_E+D I indeed obeys
D I<=Gamma<=2D I for every realization. A conditional uniform m-subset
would have remaining inclusion probability (m-a)/(M-a)<=m/M, and the
source's first-use geometry gives the required recycling count. But that
probabilistic transfer is avoidable: (3) is a deterministic upper bound.
Even Gamma itself is avoidable because old openings number at most t<=D.
This is why the present native proof does not need to resolve or assume
any additional interpretation of the source's branch-recursion lemma.
The source's sparse-occurrence normalization remains useful at its own
smaller density floor; no result about that separate scope is asserted here.

## 7. Same-input classical comparison

At p=4, fixed q, beta=Theta(1/(n sqrt(log n))), the sufficient classical
level is ell=Theta(log n), with a large enough constant. Thus the prior
repaired quantum bound using ell=Theta(log^2 n) is not a useful matched
comparison. This is an upper-bound comparison, not a runtime lower bound.
Moreover the very same trace improvement changes that quantum upper bound,
as follows; omitting this consequence would give a misleading final verdict.

## 8. Immediate ORDERED-operator and existing-compiler corollary

Repeat section 2 on ordered injective ell-tuples. There are (n)_ell<=n^ell
starting rows. Each legal set-edge transition has exactly d! ordered lifts.
Ignoring final ordering closure costs at most (d!)^(2t) for a length-2t
word. Underlying even-label set words still obey the identical excess and
active-label argument. Therefore (4) gains (d!)^(2t) and N is replaced by
(n)_ell; the norm constant in (5) only gains d!. In particular the starting
ell! multiplicity does not change the exponent or insert log n.
Independent-copy symmetrization (6) works on this Hermitian ordered matrix
as well, uniformly over all conditional Bernoulli parameters and labels.

Consequently the already established all-label ordered guide certificate
in `2026-11-13-community-classical-certificate.md`, section 8, can use this
bound instead of Bernstein. At fixed q its required matrix SNR loses the
sqrt(log n) factor. This is a substitution into the already paid compiler,
not an assertion that a slice-only norm controls an unexamined ordered sector.

For the existing asymmetric clone, let L=ceil(log2 n), t_clone=1/L,
matrix SNR b=(1-t_clone)beta and guide SNR h=t_clone beta. At the new scale
beta=Theta(n^(-p/4)ell^((2-p)/4)), the existing source-TV exponent and
conditional covariance error parameter become respectively

    binom(n,p)*t_clone^2*beta^4 = O(ell^(2-p)/L^2),
    lambda^2/(h^2 binom(n,p)) = O(ell^(d+1)L^2/n^d),
    lambda=ell/p.

Both vanish for growing polylogarithmic ell. The paid repetition factor is
h^(-lambda)*exp(O_(p,k)(ell))*poly(L). At ell=Theta(log n), it is
    n^(ell/4)*exp(O_(p,k)(ell log ell))*poly(L),
and the already paid arithmetic/precision length remains O(B+ell log n).
For other polylog regimes the explicit subleading exponent is
O(ell(log ell+log log n)); it should not silently be dropped.
The source law is still charged once on the frozen instance, and all earlier
matching-covariance, J-compression, norm-Markov and clean-circuit obligations
remain premises of that existing compiler.

Hence BOTH level exponents are now Theta(log n) in the p=4 example.
Their sufficient constants have not been optimized or matched, and no
unrestricted classical lower bound, quantum advantage, novelty, recovery,
implementation or practical-resource conclusion follows. The classical
log-free native gate is closed by the proof above; an alleged classical
dominance over every quantum repair is not an admitted consequence.
