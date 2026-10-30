# Coset Reusable-Bank Receiver Baseline

2026-10-30. Mathematical construction independently checked by a separate
reasoning agent, with the evaluator-cost qualification corrected below. This is a
known EHK support-test plus quantum-search baseline, not a novelty claim,
implemented receiver, polynomial-time algorithm, or candidate promotion.
No module, CLI, registry, or wiring change accompanies this note.

The scoped repository search found candidate verification in
`theorems/coset_hidden_involution_binary_identification_self_reduction.py`
and noncentral readout in
`theorems/self_dual_wreath_carrier_noncentral_readout_boundary.py`.
The primary precedents are [Ettinger--Hoyer--Knill, Section 2, Lemmas 2--3](https://arxiv.org/html/quant-ph/9901034v1)
and [Brassard--Hoyer--Mosca--Tapp, Section 2](https://arxiv.org/html/quant-ph/0005055v1).
The explicit combination and resource accounting are derived below; neither
reference is being credited with this exact circuit or cost statement.

## 1. Source And Exact Candidate Test

Let n>=4 be even, G=S_n, D=n!, and C the fixed-point-free involutions, with
M=|C|=(n-1)!!. Use R_a|g>=|g a^-1> and independent native mixed coset states

\[
\rho_h=(I+R_h)/D,\qquad \sigma_h=\rho_h^{\otimes k},\qquad h\in C.
\]

For a public candidate t define Q_t=(I+R_t)/2 and P_t=Q_t^{\otimes k}.
Regular trace orthogonality, Tr(R_a)=D 1_{a=e}, proves

\[
\operatorname{Tr}(Q_t\rho_h)=\frac{1+\mathbf1_{t=h}}2,
\qquad
\operatorname{Tr}(P_t\sigma_h)=
\begin{cases}1&t=h,\\2^{-k}&t\ne h.\end{cases}                 \tag{1}
\]

The hypothetical measured candidate test has the full Luders instrument
X -> P_t X P_t or (I-P_t)X(I-P_t). The receiver below does NOT perform these
intermediate measurements or assume that (1) remains a fresh-test law after
disturbance. Under simultaneous conjugation P_t becomes P_{xtx^-1}, so a
fixed-candidate effect is not a conjugation-invariant class-sum measurement.

## 2. Full Coherent Instrument

Prepare a candidate register A in |u>=M^-1/2 sum_{t in C}|t>. For each bank
register j compute an eigenvalue flag with

\[
F_{t,j}=(H_{b_j}\otimes I)\,\mathrm{controlled}\text{-}R_t^{(j)}
        (H_{b_j}\otimes I),\qquad
F_{t,j}|0\rangle|\psi\rangle
=|0\rangle Q_t|\psi\rangle+|1\rangle(I-Q_t)|\psi\rangle.
\]

Control these computations coherently by A. Phase-flip the all-zero flag
string and uncompute every flag. They return to zero exactly, implementing

\[
V=\sum_{t\in C}|t\rangle\langle t|\otimes(I-2P_t),\quad
D_A=2|u\rangle\langle u|-I_A,\quad W=(D_A\otimes I)V.       \tag{2}
\]

Each V uses 2k controlled right multiplications and O(k) flag/reflection
work. Use the SAME bank for L iterations, then measure A. The exact complete
instrument on an arbitrary bank state X is

\[
K_t=(\langle t|\otimes I)W^L(|u\rangle\otimes I),\qquad
\mathcal J_t(X)=K_tXK_t^\dagger,\qquad
\sum_{t\in C}K_t^\dagger K_t=I.                             \tag{3}
\]

Thus p(t|h)=Tr(J_t(sigma_h)); the conditional remaining bank is
J_t(sigma_h)/p(t|h) when p>0. There is no heralding loss or discarded outcome.
The final effects E_t=K_t^dagger K_t are covariant with their retained labels,
E_{xtx^-1}=C_x^{\otimes k} E_t (C_x^dagger)^{\otimes k}, not required to be
individually invariant. No unknown-state reflection, PGM, dense Racah
transform, or free Fourier-basis conversion occurs.

## 3. Purification Hybrid And Nearest Iteration

Fix ANY purification |Psi_h>_{BE} of sigma_h. E is inaccessible and is used
only in the proof. Equation (1) implies

\[
(P_h\otimes I_E)|\Psi_h\rangle=|\Psi_h\rangle,\qquad
\|(P_t\otimes I_E)|\Psi_h\rangle\|^2=2^{-k}\quad(t\ne h).
\]

Compare W with the analysis-only ideal search W_0=(D_A O_h)\otimes I_{BE},
where O_h=I_A-2|h><h|. Write
W_0^j(|u>|Psi_h>)=sum_t a_{j,t}|t>|Psi_h>. Orthogonality of candidate labels
and unitarity of D_A give the EXACT single-hybrid-step identity

\[
\|(W-W_0)W_0^j|u,\Psi_h\rangle\|^2
=4\sum_{t\ne h}|a_{j,t}|^2\|(P_t\otimes I_E)|\Psi_h\rangle\|^2
=4\,2^{-k}(1-|a_{j,h}|^2)\le4\,2^{-k}.                   \tag{4}
\]

Here and below W acts as identity on E. Telescope
W^L-W_0^L=sum_{j=0}^{L-1} W^{L-1-j}(W-W_0)W_0^j. Consequently,

\[
\|(W^L-W_0^L)|u,\Psi_h\rangle\|\le 2L\,2^{-k/2},\qquad
\left|p(h|h)-\sin^2((2L+1)\theta)\right|\le2L\,2^{-k/2},
\quad \theta=\arcsin(M^{-1/2}).                            \tag{5}
\]

The probability bound follows from pure-state trace distance and its
contractivity under discarding E and measuring A. This is a coherent,
worst-case norm sum on one fixed purification: no fresh samples, stochastic
errors, independent error events, or commuting P_t across candidates are
assumed. The actual bank may become entangled with A and disturbed.

Take L to be a nearest integer to pi/(4 theta)-1/2. Since M>=3, L>=1, and
|(2L+1)theta-pi/2|<=theta. Hence the ideal probability is at least
cos^2(theta)=1-1/M. For 0<eta<1 choose

\[
k:=\left\lceil2\log_2(2L/\eta)\right\rceil.
\quad\Longrightarrow\quad
p(h|h)\ge1-M^{-1}-\eta,\quad
L=\Theta(\sqrt M),\quad k=\log_2M+2\log_2(1/\eta)+O(1).     \tag{6}
\]

## 4. Preparation, Gates And Errors Are Paid

One source copy comes from a clean uniform permutation register, one query
to U_f:|g,z> -> |g,z xor f(g)>, and discarding the label, where f separates
the left cosets of {e,h} exactly. All source mass is retained. There are k
queries total; no U_f or U_f^-1 is used during the receiver. If copies alone
are supplied, (2)--(6) still apply, but the oracle comparison below is a
different access contract.

Uniform preparation is structured, not a free M-entry state oracle:

- For C, prepare independent uniform mixed-radix digits of sizes
  n-1,n-3,...,1. Pair the smallest unused vertex with the digit-selected
  unused partner. This is a bijection to matchings. Reversibly compute the
  image array and erase the digits using inverse ranking.
- For G, use digits of sizes n,n-1,...,1 and reversible permutation
  unranking. Binary trees of integer prefix counts prepare each digit;
  their rotations require synthesis when the range is not a power of two.
- Linear scans implement ranking and coherent array lookup without QRAM.
  In image-array encoding, compute g(t(i)) for all i, swap output/input
  arrays and uncompute using t^2=e. Thus controlled R_t costs
  C_R(n)=O(n^2 log(n+1)) reversible gates, including cleanup.

For a concrete conservative accounting, both clean preparations can use
B(n)=O(n^3 log^2(n+1)) reversible/rotation primitives: there are only
O(n^2) prefix-tree nodes across the digit registers, O(log(n+1))-length
controls, and polynomial scans. No table has size M or n!. Compiling each
rotation to error O(delta/B(n)) gives a sufficient preparation cost
C_prep(n,delta)=O(B(n) log^4(B(n)/delta)) using
[Dawson--Nielsen's Solovay--Kitaev construction](https://arxiv.org/abs/quant-ph/0505030).
Classical angle evaluation/compilation also costs polynomial time in n and
log(1/delta); these are analytical bounds, not an implemented compiler.

Let G_f include the reversible evaluator's gate cost. With total
implementation tolerance epsilon, a sufficient gate ledger is

\[
kG_f+kC_{\rm prep}(n,O(\epsilon/k))
+(2L+1)C_{\rm prep}(n,O(\epsilon/(L+1)))
+O\!\left(L[kC_R(n)+k+n\log(n+1)]\right).                  \tag{7}
\]

The second and third terms pay respectively for uniform G preparation and
initial/reflected uniform C preparation. Bank storage is O(kn log(n+1))
qubits, plus polynomial reversible workspace, k flags and evaluator
workspace. Exact reversible gates can use standard finite-gate decompositions.
All approximate gates, including an imperfect evaluator if applicable,
must fit the error budget, not be charged only on successful branches.

More precisely, allocate total initial trace-distance error epsilon_0 and
full-unitary error delta_j to each implemented iteration. Output TV error is
at most epsilon_0+sum_j delta_j. Thus epsilon_0<=epsilon/2 and
delta_j<=epsilon/(2L) add at most epsilon to (5)--(6). This bound also allows
coherent, systematically repeated synthesis errors; approximate garbage or
invalid encodings count as error, with invalid final labels recorded as
failure. Precision grows as log(L/epsilon), not as a free exact rotation.
Receiver/non-oracle work is sqrt(M) times polynomial factors, despite
polynomial source queries. Total time retains the evaluator cost:

    T = k G_f + sqrt(M) poly(n,k,log(1/epsilon)).

Opaque random oracle labels do NOT supply a polynomial-size evaluator.
No receiver circuit or fault-tolerant benchmark has been executed.

## 5. Matched Classical Access And Its Qualifications

For the query lower bound ONLY, let h be uniform on C and assign the cosets
distinct opaque labels by a uniformly random injection into a fixed alphabet
large enough to hold them. Labels are sampled once, without replacement,
independently of h, and then fixed. Both algorithms access the SAME oracle;
quantum access is coherent, classical access is ordinary evaluation. The
classical algorithm is not given interpretable evaluator code or auxiliary
graph structure. This is an oracle distribution, not a natural efficiently
encoded hard-input claim.

Remove repeated queries, which convey no new information. Draw the algorithm's
random coins and an auxiliary all-distinct-answer coupling transcript
independently of h. The actual execution matches this auxiliary transcript
until its first collision. Conditioning the actual transcript on no collision
does update the posterior on h; no independence claim is made for that law.
For each fixed auxiliary transcript, each queried pair x,y exposes at most
the candidate x^-1 y in C, so no collision excludes at most binom(q,2)
candidates. The fixed collision-free output can correctly guess at most one
of the remaining candidates. Allowing success on every exposed candidate and
averaging over the auxiliary labels and algorithmic randomness proves

\[
\Pr[\widehat h=h]\le\min\{1,(1+\tbinom q2)/M\}.
                                                               \tag{8}
\]

Thus constant-success classical identification needs Omega(sqrt(M)) queries
under this promise. This is an exponential source-query separation, not a
total-time separation or a lower bound for arbitrary structured f.

Enumeration uses M+1 evaluations, but must not be advertised as optimal.
A stronger explicit upper bound when n=4s is split-matching collision search.
There are A=n!/[2^s s!(2s)!] involutions with s transpositions. Each hidden
perfect matching supplies B/2 disjoint colliding pairs of these, where
B=binom(2s,s): choose s of its edges and take the complementary s edges.
These are exactly the collisions between distinct members of this set,
since their supports must be disjoint to produce a fixed-point-free product.
Poissonize Q uniform draws from this set. Distinct vertices are then included
independently with p=1-exp(-Q/A), so the EXACT collision probability is

\[
1-(1-p^2)^{B/2}.
\]

Q=Theta(A/sqrt(B)) yields constant success with expected oracle-query cost

\[
O(A/\sqrt B)=O\!\left(\sqrt{M\binom n{n/2}}\right)
=2^{n/2+O(\log n)}\sqrt M.                                  \tag{9}
\]

Classical time adds polynomial factors for ranking, label length and hashing;
storage is proportional to the sampled list. Sampling/ranking avoids
enumerating A entries. Constant amplification and a constant-factor query
cap preserve the asymptotic bound. This is an explicit n=0 mod 4 upper
bound, NOT a claim about the optimal or best-known classical algorithm.
The gap between (8) and (9) is not resolved here. Even with full coherent f
access, ordinary search of f(t)=f(e) already has O(sqrt(M)) oracle cost;
the bank saves source queries, not this exponential search-time scale.

For explicit graph input the relevant comparison includes
[Babai's quasipolynomial GI algorithm](https://arxiv.org/abs/1512.03547), not
opaque labels or factorial enumeration. Conversely, comparing quantum copies
only with their uninformative computational-basis samples is not matched
classical oracle access. No best-classical total-time advantage is established.

## 6. Status And Receiver-Specific Obstruction

The independent agent review checked the hybrid constants, eigenflag cleanup,
preparation/error ledger, classical coupling and split-collision count. It
required the explicit k G_f qualification above and supplied the stronger
bound below. This is an automated adversarial review, not external peer
review or formal proof-assistant certification. Earlier finite S4/S6 algebra
controls were ephemeral, not persistent tests or a compiled receiver. No
candidate is promoted.

For THIS exact instrument, a direct branch-norm argument gives, for EVERY k,

\[
p(h|h)\le\min\left\{1,\frac{(2L+1)^2}{M}\right\}.          \tag{10}
\]

To see this, purify the initial bank and write the complete normalized state
as sum_t |t>|v_t>. V is candidate-block diagonal and unitary, so it preserves
each branch norm. Diffusion changes a chosen branch to
2/M sum_t |v_t> - |v_h>. Its norm is at most the previous branch norm plus
2/sqrt(M), by Cauchy-Schwarz and sum_t ||v_t||^2=1. The initial branch norm
is 1/sqrt(M); induction gives (2L+1)/sqrt(M). Squaring proves (10).
The proof includes an inaccessible purification and needs no assumption
on k, candidate-projector commutation, or data disturbance.

Since M=(n-1)!!, polynomial L gives vanishing success for this instrument
even with an arbitrarily large bank. An epsilon-accurate implementation
adds at most epsilon to (10). The statement only covers this candidate-
diagonal-unitary plus uniform-diffusion architecture and final candidate
measurement. It is not a general receiver or circuit lower bound. A useful
next mechanism must remove the sqrt(M) search factor through genuinely
different structured decoding, not just increase the number of copies.
