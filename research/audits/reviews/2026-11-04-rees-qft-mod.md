# Approximate QFT over Z/N with explicit gate count (owner item K31, hypothesis (H1))

Date: 2026-11-04. AI session only; AI-checked, pending human review.
Status: COMPLETE (AI session; pending human review).

Scope: `thm:uniform-compilation`(iii) of `docs/papers/rees-hsp/main.tex` and
hypothesis (H1) of `prop:tb-count-gates` (`appendix-torsion-blackbox.tex`,
subsection `app:tb-counts`). No paper file, existing theorem module or
existing test was edited. New files only:
`theorems/rees_qft_mod.py`, `tests/test_rees_qft_mod.py`, this report and
the folder `research/audits/reviews/2026-11-04-rees-qft-mod/`.

Labels: **proved** (proof in this report), **exact computation** (integer /
permutation computation over all listed inputs), **float check** (double
precision numerics), **argued** (standard reasoning, not written out in full).


## 0. Result in one paragraph

For every odd N >= 3 with b = ceil(log2 N) bits (this covers N = p and
N = p^e for odd p) and every eta in (0, 1], there is an explicit circuit on
8b + 2t + 6 qubits, t <= b + 2 log2(1/eta) + 7, with at most

    G(b, eta) <= 420 b^2 + 187 b L + 4 L^2 + O((b + L) log(b + L + 2)),  L = log2(1/eta)

gates from {X, CNOT, SWAP, Toffoli, H, R_k^{+-1}, CR_k^{+-1} : k <= kappa},
kappa = O(L + log(b + L)), that implements QFT_N to operator-norm error
<= eta on the canonical subspace with every ancilla returned to |0>, global
phase included (**proved**, Theorem 6 + Proposition 7 + Corollary 8, modulo
correctness of the standard reversible arithmetic blocks, which is
**argued** in general and **exact computation** for all N tested). So
G = O((b + log(1/eta))^2). This implies the per-b (H1) of
`prop:tb-count-gates`, O(b^3 polylog(1/eta)), and improves it; over a
FIXED finite gate set (Clifford+T) the R_k still need approximate synthesis
(Solovay-Kitaev, already cited by the paper as DawsonNielsen2006), which is
**argued, not proved here**, and still gives O(b^2 + (b+L) L polylog((b+L)/eta)).

## 1. Notation and target

* X: b-qubit data register, value x = sum_i x_i 2^i; canonical subspace
  C_N = span{|x> : 0 <= x < N}. omega = e^{2 pi i/N}.
* QFT_N |x> = |chi_x> := N^{-1/2} sum_{y<N} omega^{xy} |y>.
* S |y> = |y + 1 mod N> on C_N. Then S|chi_x> = omega^{-x} |chi_x>:
  S|chi_x> = N^{-1/2} sum_y omega^{x(y-1)}|y> (**proved**, one line).
  Write k(x) = -x mod N, so the eigenvalue is e^{2 pi i k/N}.
* Goal: a unitary V on X (x) Anc with
  || V(psi (x) |0>) - (QFT_N psi) (x) |0> || <= B for all unit psi in C_N.
  This is the "isometry error on the canonical subspace with clean
  workspace" of `thm:uniform-compilation`(iii); trace distance on the
  canonical inputs is then <= B, as `lem:hybrid` needs.

Registers (`make_layout`): X, F, Z, K (b qubits each), M (t qubits),
W (t + b qubits), one qubit a, and the 3b + 5 arithmetic ancillas
(Y_s, P, r of b qubits, e, c0, f, g, h) of `theorems/rees_circuit_arith.py`.
Total 8b + 2t + 6 (**exact computation**, asserted in the test).

## 2. Construction (`theorems/rees_qft_mod.py`, `qft_mod_ops`)

V = SW . E^{-1} . DEC^{-1} . ADD . DEC . E . PH . PREP, in circuit order
PREP first:

1. PREP (on F, a; `prep_ops`): one round of exact amplitude amplification.
   A(theta) = H^{(x)b} (x) Ry(2 theta), with sin^2 theta = 2^b/(4N) in
   [1/4, 1/2), so the "good" part (F < N, a = 1) of A|0> has amplitude
   sin(alpha) = rho sin(theta) = 1/2, rho = (N/2^b)^{1/2}.
   Q = -A S_0 A^dag S_chi with S_0 = I - 2|0><0| (X layer, Toffoli-chain
   multi-controlled Z on b+1 qubits, X layer) and S_chi = I - 2 Pi_good
   (comparator [F < N] into h, CZ(h, a), comparator again). Then X on a.
   In the circuit theta is the dyadic angle theta~ = 2 pi c / 2^tp nearest
   theta; Ry is built as S H Phase(2 theta~) H S^dag = e^{i theta~} Ry(2 theta~),
   and the residual global phase e^{i theta~} (from A A^dag A) together
   with the -1 of Q are cancelled exactly by Phase(beta) X Phase(beta) =
   e^{i beta} X with beta = pi - theta~ (dyadic), which also performs the X on a.
2. PH (on X, F, Z): Z += x*y mod N (`add_product_ops`), Phase(2 pi c_j/2^tp)
   on bit j of Z with c_j = round(2^tp (2^j mod N)/N) mod 2^tp, then the
   reversed multiplication gate list. Ideal: |x>|y> -> omega^{xy}|x>|y>,
   so PH . PREP maps |x>|0> to |x>|chi_x> (ideally).
3. E (on F, M; `pe_ops`): H^t on M; for j < t, F += (2^j mod N)
   controlled on M[j] (controlled constant load into Y_s, controlled modular
   adder, unload); then G~ = approximate inverse QFT over Z/2^t
   (`aqft_inv_ops`): for s = t-1 down to 0: H(M[s]), then CR_k^{-1}(M[j], M[s])
   for j < s with k = s + 1 - j, dropped when k > r. Output bit i of l sits
   on M[t-1-i].
4. DEC (`decoder_ops`): W := 2^{t-1}; for each set bit i of N, W[i:] += l
   (Cuccaro adder, l zero-extended with the clean Z register); K := top b
   bits of W, i.e. floor((lN + 2^{t-1})/2^t) in [0, N]; if K = N set K := 0
   (comparator flag, controlled XOR of N, flag cleared by comparing W_hi).
   So K = k~(l) := round(lN/2^t) mod N (round half up).
5. ADD: X += K mod N (modular adder). Then DEC^{-1}, E^{-1} (reversed
   lists, rotation signs flipped), and SW: swap X and F bitwise.

## 3. Proofs

### Lemma 1 (preparation). **proved**
Let alpha~ = arcsin(rho sin theta~). Then
|| PREP |0>_{F,a,anc} - |u_N>_F |0>_a |0>_anc || = 2 |sin((pi/2 - 3 alpha~)/2)|
<= 3 |theta - theta~| <= 3 pi 2^{-tp}, with u_N = N^{-1/2} sum_{y<N} |y>.

Proof. All phases cancel exactly (Section 2.1), so PREP = X_a Q(theta~) A(theta~)
with Q(theta~) = (2|psi><psi| - I)(I - 2|g><g|) restricted to the plane of
|g> = |u_N>|1>_a and |bad~>, where A(theta~)|0> = |psi> = sin(alpha~)|g> +
cos(alpha~)|bad~>. The good state |g> does not depend on theta~ (every
y < N, a = 1 has amplitude 2^{-b/2} sin theta~). Q maps |psi> to
(sin alpha~(2 cos 2alpha~ + 1))|g> + (cos alpha~(2 cos 2 alpha~ - 1))|bad~>
= sin(3 alpha~)|g> + cos(3 alpha~)|bad~> (one-line computation; at
alpha = pi/6 the result is exactly |g>). Hence the error is
sqrt((1 - sin 3alpha~)^2 + cos^2 3alpha~) = 2|sin((pi/2 - 3alpha~)/2)|
<= |pi/2 - 3alpha~| = 3|alpha - alpha~|. Since sin alpha = rho sin theta
with rho <= 1, d alpha/d theta = rho cos theta/cos alpha <= 1 (alpha <= theta),
so |alpha - alpha~| <= |theta - theta~| <= pi 2^{-tp}. The comparator and
the Toffoli chain return their ancillas to 0 on every word (block
correctness, Section 4). Float check: the simulated error equals the
formula to 1e-9 for (N, tp) in {(3,6), (5,10), (7,4), (13,12), (27,8)}.

### Lemma 2 (phase). **proved**
On X, F canonical and Z, anc clean, PH = diag(e^{i beta(xy mod N)}) with
beta(z) = 2 pi sum_j z_j c_j/2^tp, and
max_{z<N} |e^{2 pi i z/N} - e^{i beta(z)}| <= sum_{j<b} 2 pi ||(2^j mod N)/N - c_j/2^tp||
<= pi b 2^{-tp}  (||.|| = distance to the nearest integer).
Proof: e^{2 pi i z/N} = prod_j e^{2 pi i z_j (2^j mod N)/N}; each rounded
exponent errs by at most 2^{-tp-1} in units of 2 pi; |e^{iu} - e^{iv}| <= |u - v|.
The multiplication is exact on canonical inputs and its reversed gate list
is its exact inverse on all words (Section 4).

### Lemma 3 (approximate inverse QFT over Z/2^t). **proved**
Let G be the list of item 3 with no rotation dropped. Then G|m> =
D^{-1/2} sum_l e^{-2 pi i m l/D} |rev(l)>, D = 2^t, rev the bit reversal
(product formula: output bit i equals H on m_{t-1-i} followed by phases
e^{-2 pi i m_j 2^{j-(t-i)}} for j < t-1-i; float check against the matrix
for t <= 6). Dropping every CR_k^{-1} with k > r changes it by at most
eps_aq := sum_{k=r+1}^{t} (t-k+1) 2 sin(pi/2^k) <= 2 pi (t - r) 2^{-r}
in operator norm: G contains t - k + 1 gates CR_k^{-1}, each with
||CR_k^{-1} - I|| = 2 sin(pi/2^k); telescoping over the dropped gates.

### Lemma 4 (phase-estimation tail). **proved**
For k in Z/N let zeta_k = D^{-1/2} sum_{m<D} e^{2 pi i m k/N}|m> and
beta_k = G zeta_k, so beta_k(l) = D^{-1} sum_m e^{2 pi i m delta_l},
delta_l = k/N - l/D. Let Bad_k = {l : k~(l) != k}. With a = D/(2N),
sum_{l in Bad_k} |beta_k(l)|^2 <= (1/a + 1/a^2)/2 =: eps_pe^2.
Proof. Let d_l in (-1/2, 1/2] represent delta_l mod 1. (i) If |d_l| < 1/(2N)
then k~(l) = k: lN/D + 1/2 = (k - Nj) + (1/2 - N d_l) with j integer and
1/2 - N d_l in (0, 1), so floor gives k - Nj = k mod N. So Bad_k is inside
{|d_l| >= 1/(2N)}. (ii) |beta_k(l)| = |sin(pi D d_l)|/(D |sin(pi d_l)|)
<= 1/(2 D |d_l|) by |sin(pi u)| >= 2|u| on |u| <= 1/2. (iii) The numbers
u_l = D d_l are distinct points of one translate of Z (D delta_l = Dk/N - l),
and bad ones have |u_l| >= a. On each side the n-th such point is >= a + n,
so the sum is <= 2 . (1/4)(sum_{n>=0} (a+n)^{-2}) <= (1/2)(1/a^2 + 1/a).
Float check: the actual max_k ||Pi_Bad beta~_k|| is below eps_pe + eps_aq
in all tested cases (it is about half of it).

### Lemma 5 (coherent erasure of X). **proved**
Let V_er = E^{-1} DEC^{-1} ADD DEC E and U_er the isometry
|x>_X |chi_x>_F |0> -> |0>_X |chi_x>_F |0> on span{|x>|chi_x>|0> : x < N}.
Then ||(V_er - U_er) w|| <= sqrt(2)(eps_pe + eps_aq) ||w|| on that span.
Proof. The controlled adders implement |m>|y> -> |m>|y + m mod N> on
canonical y (block correctness), so E |chi_x>|0>_M = |chi_x> (x) beta~_k
with k = k(x) and beta~_k = G~ zeta_k (eigenvector kick-back:
S^m|chi_x> = e^{2 pi i m k/N}|chi_x>). DEC, ADD, DEC^{-1} map
|x>|l> -> |x + k~(l) mod N>|l> exactly with clean workspace. So
DEC^{-1} ADD DEC E |x>|chi_x>|0> = sum_l beta~_k(l) |x + k~(l)>|chi_x>|l>
= |0>|chi_x>beta~_k + sum_{l in Bad_k} beta~_k(l)(|x + k~(l)> - |0>)|chi_x>|l>,
because x + k = 0. The first term is mapped by E^{-1} to exactly
|0>|chi_x>|0> = U_er|x>|chi_x>|0> (E^{-1} is the exact inverse of the
implemented E, whatever r is). The second term has norm
sqrt(2) ||Pi_Bad beta~_k|| <= sqrt(2)(||Pi_Bad beta_k|| + ||beta~_k - beta_k||)
<= sqrt(2)(eps_pe + eps_aq) (orthogonal |x + k~(l)> != |0> per l; Lemmas 3, 4).
For w = sum_x c_x |x>|chi_x>|0>, the error vectors of different x carry
the orthogonal factors |chi_x> in F before the unitary E^{-1}, so they are
orthogonal and ||(V_er - U_er)w||^2 = sum |c_x|^2 ||err_x||^2.

### Theorem 6 (error of V). **proved** (given Section 4)
For all unit psi in C_N:
||V(psi (x) |0>) - (QFT_N psi) (x) |0>|| <= B := eps_prep + eps_ph + sqrt(2)(eps_pe + eps_aq),
eps_prep = 2|sin((pi/2 - 3 alpha~)/2)| <= 3 pi 2^{-tp}, eps_ph <= pi b 2^{-tp},
eps_pe = ((1/a + 1/a^2)/2)^{1/2} with a = 2^{t-1}/N, eps_aq <= 2 pi (t-r) 2^{-r}.
The same bound holds for V^dag against QFT_N^dag.
Proof. Ideally U(psi (x) 0) = SW . U_er . D . P (psi (x) 0) with P the exact
preparation and D the exact phase: P gives |x>|u_N>, D gives |x>|chi_x>,
U_er gives |0>|chi_x>, SW gives |chi_x>|0>. Telescoping,
V - U = SW[V_er PH (PREP - P) + V_er (PH - D) P + (V_er - U_er) D P] on
psi (x) 0, and the three terms are bounded by Lemmas 1, 2, 5 (Lemma 1 acts
on F, a, anc only, so it holds for every psi in X; P psi(x)0 is canonical,
as Lemma 2 needs; D P psi(x)0 lies in the span of Lemma 5). The inverse:
V^dag - U^dag = V^dag (U - V) U^dag, and U^dag maps canonical inputs with
clean workspace to the same set. `error_bound()` evaluates B.

### Proposition 7 (gate count). **proved** from the block structure; **exact computation** check
With pc(n) the number of 1 bits (pc(N) <= b), the blocks cost at most
(Cuccaro adder on n bits: 2n Toffoli + 4n + 1 CNOT = 6n + 1 gates):

| block | gates (upper bound) |
|---|---|
| comparator `less_than_p` | 14b + 5 + 2 pc(N) <= 16b + 5 |
| modular adder `mod_add_reg` | 34b + 12 + 4 pc(N) <= 38b + 12 |
| multiplication `add_product_ops` | 158 b^2 + 46 b - 4 |
| PREP | 39 b + 5 tp + 30 |
| PH | 2(158 b^2 + 46 b - 4) + b tp |
| E (and E^{-1}) | t(40 b + 13) + t r |
| DEC (and DEC^{-1}) | 6 b t + 6 b^2 + 35 b + 13 |
| ADD | 38 b + 12 |
| SW | b |

Total: G <= 328 b^2 + 92 b t + 2 t r + b tp + 5 tp + 26 t + 240 b + 60
(`gate_bound`). The only non-permutation gates are H, R_k^{+-1} (k <= tp)
and CR_k^{+-1} (k <= r); there are at most 6t + 4b + 8 H gates,
at most t(r - 1) CR per E, and at most (b + 6) tp single-qubit R gates.
The test asserts count <= bound for every N tested and four (t, r, tp) each.

### Corollary 8 (parameters for eta). **proved**
For eta in (0, 1] take tp = ceil(log2(3 pi (b+3)/eta)), t = ceil(log2(36 N/eta^2)),
r = ceil(log2(6 sqrt(2) pi t/eta)). Then (3 + b) pi 2^{-tp} <= eta/3;
a = 2^{t-1}/N >= 18/eta^2 >= 1, so sqrt(2) eps_pe <= sqrt(2/a) <= eta/3;
sqrt(2) eps_aq <= sqrt(2) 2 pi t 2^{-r} <= eta/3. So B <= eta. With
L = log2(1/eta): t < b + 2L + 6.17, r < L + log2 t + 5.74,
tp < L + log2(b+3) + 4.24, kappa = max(r, tp), qubits 8b + 2t + 6 < 10b + 4L + 19,
and G <= 420 b^2 + 187 b L + 4 L^2 + O((b + L) log(b + L + 2)) = O((b + log(1/eta))^2).
(The 4L^2 comes from the t ~ 2L-qubit approximate QFT with cutoff r ~ L; the
92bt term from the t controlled modular additions.)

## 4. Correctness of the reversible arithmetic blocks

The proof uses only these properties, all of exact permutations of basis
states built from X, CNOT, Toffoli, SWAP:
(a) Cuccaro adder: (B, z) += A mod 2^{n+1}, A and c0 restored, on every
input. Standard (MAJ/UMA ripple). **exact computation** for n <= 6 on all
inputs (`test_cuccaro_adder_exhaustive_small_widths`); **argued** in general.
(b) comparator: out ^= [w < N] for every b-bit word w, ancillas restored.
**proved** from (a): subtracting N in b + 1 bits sets the sign bit iff w < N,
and the add-back restores. **exact computation** for all tested N on all words.
(c) modular adder t += y mod N for t, y < N (controlled form: identity on
every word when the control is 0, as y = 0 then). **proved** from (a):
f = [t + y < N] after the trial subtraction, the add-back of N controlled
on f gives (t + y) mod N, and f is cleared because the result r satisfies
r < y iff a wrap occurred. **exact computation** (controlled shifts by 2^j mod N)
for all tested N.
(d) multiplication Z += x y mod N on canonical inputs, ancillas clean:
shift-and-add with modular doubling (N odd). **argued** (it is the
`rees_circuit_arith.py` block, whose report checks it for primes <= 13);
**exact computation** here for all N in {3,5,7,9,11,13,25,27}, including
the composite N = 9, 25, 27, on all x, y < N and two Z values.
(e) decoder: W = lN + 2^{t-1} < 2^{t+b} for all l < 2^t when N < 2^b
(so no adder overflows), K = round(lN/2^t) mod N. **proved** from (a);
**exact computation** for (N, t) in {(3,4),(5,6),(7,7),(9,8),(13,8),(25,9),(27,10)}
on all l, together with DEC^{-1} DEC = I.

So Theorem 6 is proved for every odd N >= 3 given (a) and (d) in general;
(a) and (d) are standard and checked exhaustively where stated.

## 5. Where Kitaev / Cleve-Watrous are no longer needed

The construction above uses only: Hadamards, dyadic phase rotations, exact
amplitude amplification with one iteration (proved in Lemma 1), reversible
binary arithmetic (Section 4), phase estimation of the cyclic shift with a
rectangular window (Lemma 4) and the Bennett-style recompute-and-subtract
erasure (Lemma 5). No step relies on a source that this session could not
read. The citation to Kitaev 1995 in `thm:uniform-compilation`(iii) can
stay as attribution of the idea (phase estimation of the shift), but the
size bound no longer depends on it.

Steps that did NOT fail: every step of the plan in the task closed. The one
place where the bound is weaker than the task's suggested form is the
L^2 = log^2(1/eta) term: with a rectangular phase-estimation window the
tail is only O(N/2^t) ,
so t ~ b + 2L and the approximate QFT on t qubits with cutoff r ~ L costs
~ 2 t r ~ 4 L^2. (That the rectangular-window tail is of order 1/a for
generic phases is **argued**, not needed.) A tapered window or median amplification could remove it
but is not needed for (H1). So what is proved is O(b^2 + b L + L^2), not
O(b^2 + b L log L).

## 6. The form (H1) needs

Current (H1) of `prop:tb-count-gates` (re-read 2026-11-04 after the
coordinator's change): "a single-coordinate quantum Fourier transform over
F_p, or over Z/p^e, on b <= l bits, to isometry error eta compiles into
O(b^3 polylog(1/eta)) gates".

What is proved (Theorem 6, Proposition 7, Corollary 8): for every odd N on
b bits, in the gate set Gamma_kappa = {X, CNOT, SWAP, Toffoli, H,
R_k^{+-1}, CR_k^{+-1} : k <= kappa}, kappa = max(r, tp) = O(L + log(b + L)),

    gates <= 328 b^2 + 92 b t + 2 t r + (b+5) tp + 26 t + 240 b + 60 = O((b + log(1/eta))^2),

with operator-norm error <= eta on the canonical subspace, ancillas clean,
global phase included. Since (b + L)^2 <= 4 b^2 L^2 for b, L >= 1, this
**implies** the per-b (H1) (and is better by a factor ~ b / polylog). The
constants are not small: the count is about 420 b^2 for small L, so the
b^2 bound is below b^3 only for b > ~420; this does not affect any
O-statement (exact computation, `count_table.json`).

Gate-set caveat (**argued**, not proved): over a FIXED finite gate set such
as Clifford+T, the R_k with 4 <= k <= kappa must be synthesized. There are
at most 2 t (r-1) + (b+5) tp + 6 = O((b+L)(L + log(b+L))) rotations
(exact computation: e.g. 3399 at b=64, eta=1e-3; 12834 at b=64,
eta=2^-40). Synthesizing each to error eta/(2 #rot) with the
Solovay-Kitaev algorithm the paper already cites (DawsonNielsen2006)
multiplies each by polylog(#rot/eta) = polylog(b/eta), so the total stays
O(b^2 + (b+L)(L + log(b+L)) polylog(b/eta)) = O(b^3 polylog(1/eta)), and
(H1) holds over the finite set too, CONDITIONAL on that cited synthesis
theorem. Whether the paper counts gates over a finite set or over
Gamma_kappa is for the owner to state; the proposed text says both.

How (H1) is used in `prop:tb-count-gates` (re-grepped): (a) needs a
transform over F_p at error eta with log(1/eta) = O_c(log(l/eps)); the
lemma gives O((log p + log(l/eps))^2) <= O((log p)^3 polylog(l/eps)), so
the rest of (a) is unchanged. (b) needs 2 sum_p k d transforms over
Z/p^{e_p} on b_M <= l bits at eta = eps/(16 l k d); the lemma gives
O((l + log(16 l k d/eps))^2) = O_c((l + log(s+1))^2) each when
log2(8l/eps) <= l, and with 2 sum_p k d <= 4 d Lambda l the transforms
cost O_c(s^c l^2 (l + log(s+1))^2), inside the stated O_c(s^c l^5 polylog(s l)).
The current proof text of (b) still reads "sum_p k d l^3 ... O_c(s^c l^5)";
the proposed replacement (b3) below supersedes that sentence.

## 7. Numerical verification (float check unless stated)

Method. `operator_error` builds the Qiskit circuit, then simulates the
EMITTED Qiskit instruction list gate by gate with an exact sparse
basis-state simulator (`SparseState`: permutation gates act on keys,
phases on amplitudes, H merges equal keys; it matches
`qiskit.quantum_info.Statevector` to 1e-12 on random 7-qubit circuits of
the same gate types, test `test_sparse_simulator_matches_qiskit_statevector`).
For each x < N it computes the full output vector V|x>|0> over ALL qubits
(ancilla garbage included), subtracts (QFT_N|x>)|0>, and takes the largest
singular value of the resulting N-column error matrix (Gram matrix), i.e.
the operator norm on the canonical subspace. Amplitudes below 1e-11 (1e-13
in the sweep) are dropped after an H; the sum of the square roots of the
dropped masses bounds the deviation of each column, and
sigma_upper = sigma_max + sqrt(N) * that sum is compared with B. Dropped
mass was below 1e-20 in every run, so sigma_upper = sigma_max to 8 digits.

Results:
* Every run satisfies sigma_upper <= B (proved bound) and
  gate count <= `gate_bound`. Typical ratio sigma/B ~ 0.5 when r = t
  (the PE tail dominates; actual ~ sqrt(2) x actual tail mass).
* Corollary-8 parameters (`eta_runs.json`): N = 3, eta = 0.25 and 0.1;
  N = 5, eta = 0.25 and 0.1; N = 7, eta = 0.25: measured error 0.030,
  0.012, 0.031, 0.012, 0.037, i.e. about eta/8, with B about eta/3.5.
  The runs N = 9, 11, 13 at eta = 0.25 and N = 3 at eta = 0.05 were killed by
  a session restart and NOT rerun: they are nice-to-have (the same N are
  covered at other (t, r, tp) in the sweep and the slow tests, and B <= eta
  is proved, not measured).
* Sweep over t and r (`sweep_t_r.json`, tp = 28; `sweep_27.json`):
  N in {3, 5, 7, 9, 11, 13, 25, 27}, t = b+1, b+3, b+5 (N = 27: b+1, b+3),
  r in {3, t}. N = 25 at t = 10 was lost in the restart and not rerun; it is
  covered by the slow test (25, 9, 5).
* Low-precision rotations (tp = 4..14) for N = 3, 5, 7 (fast tests) and
  N = 9 (tp 6), 13 (tp 8) (slow tests): bound holds; there the prep leak
  onto padding words F >= N spreads into many dirty-ancilla branches,
  which the bound covers (Lemma 1 is a vector bound).
* Slow tests (REES_SLOW=1, 12 cases including N = 25, 27 at t up to 10):
  12 passed in 445 s (`slow_tests.log`). Fast suite: 74 tests pass in
  about 10 s.
* Larger N (`large_runs.json`): see the table.
* Gate counts at Corollary-8 parameters for b = 2..64 and
  eta in {1e-3, 1e-6, 2^-40} (`count_table.json`, exact computation from the
  generated gate lists, b = 64 lists have up to 2.1 M gates): count <= bound
  in all 18 cases; B_simple <= eta in all; max rotation index 52 at eta = 2^-40.

All full-operator runs with saved records (`set` = source file; duplicates where r was capped at t removed; sigma_upper <= B in every row):

| set | N | t | r | tp | eta | sigma_max (float) | B (proved) | ok | gates | gate bound | qubits |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sweep | 3 | 3 | 3 | 28 |  | 0.5239 | 1.1456 | yes | 2552 | 2696 | 28 |
| sweep | 3 | 5 | 3 | 28 |  | 0.4353 | 1.8527 | yes | 2976 | 3128 | 32 |
| sweep | 3 | 5 | 5 | 28 |  | 0.2360 | 0.4719 | yes | 2982 | 3148 | 32 |
| sweep | 3 | 7 | 3 | 28 |  | 0.4242 | 3.6074 | yes | 3400 | 3560 | 36 |
| sweep | 3 | 7 | 7 | 28 |  | 0.1148 | 0.2215 | yes | 3420 | 3616 | 36 |
| sweep | 5 | 4 | 3 | 28 |  | 0.5044 | 1.5596 | yes | 4720 | 5188 | 38 |
| sweep | 5 | 4 | 4 | 28 |  | 0.4946 | 1.0078 | yes | 4722 | 5196 | 38 |
| sweep | 5 | 6 | 3 | 28 |  | 0.5621 | 2.7737 | yes | 5280 | 5804 | 42 |
| sweep | 5 | 6 | 6 | 28 |  | 0.2433 | 0.4250 | yes | 5292 | 5840 | 42 |
| sweep | 5 | 8 | 3 | 28 |  | 0.5707 | 4.6593 | yes | 5844 | 6420 | 46 |
| sweep | 5 | 8 | 8 | 28 |  | 0.1179 | 0.2015 | yes | 5874 | 6500 | 46 |
| sweep | 7 | 4 | 3 | 28 |  | 0.6559 | 1.8327 | yes | 4938 | 5188 | 38 |
| sweep | 7 | 4 | 4 | 28 |  | 0.5971 | 1.2809 | yes | 4940 | 5196 | 38 |
| sweep | 7 | 6 | 3 | 28 |  | 0.6326 | 2.8650 | yes | 5538 | 5804 | 42 |
| sweep | 7 | 6 | 6 | 28 |  | 0.2909 | 0.5163 | yes | 5550 | 5840 | 42 |
| sweep | 7 | 8 | 3 | 28 |  | 0.6250 | 4.6980 | yes | 6138 | 6420 | 46 |
| sweep | 7 | 8 | 8 | 28 |  | 0.1451 | 0.2402 | yes | 6168 | 6500 | 46 |
| sweep | 9 | 5 | 3 | 28 |  | 0.5539 | 2.3183 | yes | 7563 | 8520 | 48 |
| sweep | 9 | 5 | 5 | 28 |  | 0.4363 | 0.9375 | yes | 7569 | 8540 | 48 |
| sweep | 9 | 7 | 3 | 28 |  | 0.7108 | 3.7864 | yes | 8263 | 9320 | 52 |
| sweep | 9 | 7 | 7 | 28 |  | 0.2356 | 0.4005 | yes | 8283 | 9376 | 52 |
| sweep | 9 | 9 | 3 | 28 |  | 0.7046 | 5.7379 | yes | 8959 | 10120 | 56 |
| sweep | 9 | 9 | 9 | 28 |  | 0.1179 | 0.1908 | yes | 9001 | 10228 | 56 |
| sweep | 11 | 5 | 3 | 28 |  | 0.6854 | 2.4579 | yes | 7861 | 8520 | 48 |
| sweep | 11 | 5 | 5 | 28 |  | 0.6087 | 1.0771 | yes | 7867 | 8540 | 48 |
| sweep | 11 | 7 | 3 | 28 |  | 0.7198 | 3.8347 | yes | 8605 | 9320 | 52 |
| sweep | 11 | 7 | 7 | 28 |  | 0.2560 | 0.4488 | yes | 8625 | 9376 | 52 |
| sweep | 11 | 9 | 3 | 28 |  | 0.7446 | 5.7588 | yes | 9353 | 10120 | 56 |
| sweep | 11 | 9 | 9 | 28 |  | 0.1309 | 0.2117 | yes | 9395 | 10228 | 56 |
| sweep | 13 | 5 | 3 | 28 |  | 0.7287 | 2.5944 | yes | 7855 | 8520 | 48 |
| sweep | 13 | 5 | 5 | 28 |  | 0.6103 | 1.2135 | yes | 7861 | 8540 | 48 |
| sweep | 13 | 7 | 3 | 28 |  | 0.7553 | 3.8802 | yes | 8599 | 9320 | 52 |
| sweep | 13 | 7 | 7 | 28 |  | 0.2815 | 0.4944 | yes | 8619 | 9376 | 52 |
| sweep | 13 | 9 | 3 | 28 |  | 0.7498 | 5.7781 | yes | 9347 | 10120 | 56 |
| sweep | 13 | 9 | 9 | 28 |  | 0.1409 | 0.2310 | yes | 9389 | 10228 | 56 |
| sweep | 25 | 6 | 3 | 28 |  | 0.8098 | 3.5283 | yes | 11423 | 12692 | 58 |
| sweep | 25 | 6 | 6 | 28 |  | 0.6141 | 1.1797 | yes | 11435 | 12728 | 58 |
| sweep | 25 | 8 | 3 | 28 |  | 0.8581 | 4.9410 | yes | 12307 | 13676 | 62 |
| sweep | 25 | 8 | 8 | 28 |  | 0.2835 | 0.4832 | yes | 12337 | 13756 | 62 |
| sweep | 27 | 6 | 3 | 28 |  | 0.8094 | 3.5959 | yes | 11792 | 12692 | 58 |
| sweep | 27 | 6 | 6 | 28 |  | 0.6143 | 1.2473 | yes | 11804 | 12728 | 58 |
| sweep | 27 | 8 | 3 | 28 |  | 0.8765 | 4.9632 | yes | 12712 | 13676 | 62 |
| sweep | 27 | 8 | 8 | 28 |  | 0.2836 | 0.5054 | yes | 12742 | 13756 | 62 |
| eta | 3 | 11 | 11 | 8 | 0.25 | 0.0296 | 0.0670 | yes | 4248 | 4460 | 44 |
| eta | 3 | 14 | 12 | 9 | 0.1 | 0.0116 | 0.0306 | yes | 4939 | 5191 | 50 |
| eta | 5 | 12 | 11 | 8 | 0.25 | 0.0311 | 0.0717 | yes | 6972 | 7684 | 54 |
| eta | 5 | 15 | 12 | 10 | 0.1 | 0.0119 | 0.0311 | yes | 7871 | 8702 | 60 |
| eta | 7 | 12 | 11 | 8 | 0.25 | 0.0367 | 0.0728 | yes | 7357 | 7684 | 54 |
| large | 31 | 7 | 7 | 28 |  | 0.4451 | 0.8479 | yes | 12626 | 13240 | 60 |
| large | 31 | 9 | 4 | 28 |  | 0.4937 | 2.6048 | yes | 13570 | 14186 | 64 |
| large | 49 | 8 | 8 | 28 |  | 0.3797 | 0.7276 | yes | 16204 | 18368 | 70 |


## 8. Exact statement that now holds

**Theorem (AI-checked, pending human review).** For every odd N >= 3,
b = ceil(log2 N), and eta in (0, 1], the circuit `qft_mod_ops(N, t, r, tp)`
with (t, r, tp) = `params_for_eta(N, eta)` acts on 8b + 2t + 6 qubits, uses at
most 328b^2 + 92bt + 2tr + (b+5)tp + 26t + 240b + 60 = O((b + log(1/eta))^2)
gates from {X, CNOT, SWAP, Toffoli, H, R_k^{+-1}, CR_k^{+-1} : k <= max(r, tp)},
max(r, tp) = O(log(1/eta) + log(b + log(1/eta))), and satisfies
||V(psi (x) |0>) - (QFT_N psi) (x) |0>|| <= eta for every unit psi in
span{|0>,...,|N-1>}, all ancillas included, global phase included; likewise
for V^dag and QFT_N^dag. Status: **proved** in Sections 3-4, given the
correctness of the ripple-carry adder for all widths and of the shift-and-add
multiplier for all odd N (standard; **exact computation** for widths <= 6
and for N in {3,5,7,9,11,13,25,27}); **float check** of the operator-norm
error for N in {3,5,7,9,11,13,25,27,31,49}.
Consequence: hypothesis (H1) of `prop:tb-count-gates` in its per-b form
holds in this gate set; over a fixed finite gate set it holds given the cited
Solovay-Kitaev synthesis (argued).

## 9. Still missing

1. Human review of Sections 3-4 and of the proposed LaTeX.
2. A proof (or exhaustive check beyond the listed N) of the arithmetic
   blocks for general widths; they are standard, and the paper already relies
   on the same backend.
3. Fixed finite gate set: no Clifford+T synthesis is implemented or proved
   here; the reduction cites DawsonNielsen2006.
4. The Rees circuit generator (`rees_circuit_general.py`,
   `rees_circuit_arith.py`) still uses QFT_p as one exact b-qubit unitary;
   wiring this module in (a Builder whose `qft` emits `qft_mod_ops`, with its
   own ancillas) was not done, since editing those files was out of scope.
5. Nothing is optimized: the constant ~420 b^2 is far from the best known;
   an O(b^2 + bL log L) form would need a tapered PE window (Section 5).
6. The killed nice-to-have eta runs (N = 9, 11, 13 at eta = 0.25; N = 3 at
   eta = 0.05) and the N = 25, t = 10 sweep point were not rerun; N = 81 was
   dropped as too slow.

## 10. Claim gates that stay false

`coherent_receiver_implemented`, `general_sde_implemented`,
`formal_compiler_checked`, `independent_review`, `novelty_established`,
`speedup_claim_allowed` all stay False (asserted in
`test_status_gates_stay_false`). New module flags: `rees_generator_uses_this_qft`
= False, `fixed_finite_gate_set` = False; `qft_poly_log_p_implemented` = True
for this standalone module only (the generator's own `ARITH_STATUS` flag is
unchanged and stays False). No novelty claim: approximate QFT over Z/N by
phase estimation is classical (Kitaev 1995); what is new here is only the
explicit, self-contained count and its check.

## 11. Proposed paper text (AI-checked, pending human review)

(a) Lemma `lem:qft-mod` with proof, to insert in `main.tex` directly after
the proof of `thm:uniform-compilation`, plus one sentence for the end of
item (iii): `research/audits/reviews/2026-11-04-rees-qft-mod/proposed_lemma.tex`.
It uses only existing labels/keys (`thm:uniform-compilation`,
`DawsonNielsen2006`) and defines the new label `lem:qft-mod`.

(b) Changes to `prop:tb-count-gates` that discharge (H1), written against
the current per-b (H1) and the 2 sum_p k d transforms at error
eps/(16 l k d): `research/audits/reviews/2026-11-04-rees-qft-mod/proposed_tb_change.tex`
((b1) statement: (H1) becomes a consequence of `lem:qft-mod`, only (H2)-(H3)
stay assumed; (b2) proof of (a); (b3) proof of (b), replacing the stale
"sum_p k d l^3" sentence; (b4) the two "(H1)--(H3)" mentions in main.tex).
Existing labels used: `prop:tb-count-gates`, `thm:bb-envelope`,
`thm:uniform-compilation`, `DawsonNielsen2006`; new: `lem:qft-mod`.
No paper file was edited.
