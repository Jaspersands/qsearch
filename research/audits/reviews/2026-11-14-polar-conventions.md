# Polar SC conventions and dual error normalization — 2026-11-14

**Disposition.** O1 and O2 in the paid polar review are proved for every
N=2^s, including N=1, with row vectors, G_s=F_2^{⊗s},
F_2=[[1,0],[1,1]], and natural SC input order without bit reversal.
The exact identities are

    (S_{s,i}(W))^perp ≃ S_{s,N−1−i}(W^perp),
    e_{N−1−i} = (1−Z_i)/2.

Here W is BSC(alpha), 0<alpha<1/2; Z_i is its synthesized-channel
Bhattacharyya parameter; e_j is the uniform-prior Helstrom error of the
synthesized pure-state channel, with the TRUE earlier input bits supplied
as classical output registers and all later input bits uniform.
These auxiliary errors are not fixed-frozen code/block errors.

## 1. Explicit SC registers and the all-length recursion

For any binary cq channel W with trace-one outputs, define

    S_{s,i}(W)(z) = 2^{−(N−1)} sum_{u_<i,u_>i}
       |u_<i><u_<i| tensor product_l W((uG_s)_l),  u_i=z.

The entire prefix is retained, not averaged away. The normalizer makes
each output trace one. This agrees with Korada Eq.(2), physical LF215–239,
including the factor 2^{−(N−1)}; his output includes the prefix.
Define the elementary synthesized channels, with their full outputs,

    W^−(z) = (1/2) sum_t W(z+t) tensor W(t),
    W^+(z) = (1/2) sum_a |a><a| tensor W(a+z) tensor W(z).

Let M=N/2 and u=(a,b), with a,b length M. Tensor multiplication gives

    uG_s = ((a+b)G_{s−1}, bG_{s−1}).

For i<M, sum over all b. The substitution v=bG_{s−1} is a bijection;
v is uniform and its coordinates independent. Pairing output positions
l and M+l therefore gives independent W^− uses with input aG_{s−1}.
The retained prefix is exactly a_<i. Thus

    S_{s,i}(W) ≃ S_{s−1,i}(W^−).

For i=M+j, all a are already retained. Replace their classical register
reversibly by c=aG_{s−1}. The vector c is uniform independently of b.
Pair c_l with the two physical outputs at l,M+l: this is precisely one
W^+ use with input (bG_{s−1})_l. The additional retained prefix is b_<j.
Consequently

    S_{s,M+j}(W) ≃ S_{s−1,j}(W^+).

These are exact output relabellings, valid for quantum outputs as well as
classical ones. Induction from N=1 identifies natural index i with its
MSB-first binary polarization word. No finite-case extrapolation is used.

BSC(alpha) and its pure-state dual are symmetric. Symmetry is preserved
by both operations: flip the first output of W^−, or both quantum outputs
of W^+, to flip the input. For symmetric W, the classical a in W^+ can
become independent only AFTER its controlled output-symmetry correction.
Renes Eq.(29), LF451–458, performs exactly this correction. Discarding and
reappending that independent fair register is channel equivalence; simply
discarding an uncorrected SC prefix is not.

Renes Theorem 1 / Corollary 2, LF462–520, swap minus and plus under duality
and hence complement EVERY polarization choice. Combining this with the
induction proves the displayed dual-channel identity with J(i)=N−1−i.
It includes the conjugate/past side information through channel
equivalence; it does not insert a new genie beyond the defined SC output.

## 2. Bit-order reversal, coordinate complement, and the same code

Korada uses H_s=R_s G_s, where R_s reverses the s binary digits of an
index (LF150–177). Permuting tensor factors of F_2^{⊗s} gives

    R_s G_s R_s=G_s,  so H_s=G_s R_s.

For the SAME input row u, his encoder differs only by the physical output
permutation R_s. On a memoryless channel this is an invertible output
relabeling; SC input order and its prefixes are unchanged. There is no
additional R_s(i) in the formula for e_j. R_s (digit-order reversal) and
J (digitwise complement) are different permutations.

Also F_2^2=I and F_2^T=J_2 F_2 J_2, so

    G_s^{−T}=G_s^T=J G_s J.

For K={uG_s:u_F=0}, ordinary row-vector orthogonality gives

    K^perp={vG_s^{−T}:v_{F^c}=0}
          ={wG_s J:w_{J(F)^c}=0}.

Thus the dual code is exactly the polar information set J(F), followed
by the public coordinate permutation J; no separately chosen code appears.

## 3. The BSC dual, including its classical flag

Renes Eq.(22), LF342–362, outputs a classical channel-output flag y and
a phase-modulated pure posterior state. For BSC(alpha) with uniform
input, y is fair. For y=0 that pure state is

    |psi_z> = sqrt(1−alpha)|0> + (−1)^z sqrt(alpha)|1>.

For y=1 its coefficients are exchanged. Applying X conditional on y=1
changes that branch to (−1)^z|psi_z>, the SAME density operator.
Only then may the independent fair y be discarded/reappended. This
explicitly realizes the equivalence asserted for BSC in LF370–385.
The source's exchanged square-root convention differs by public X and
irrelevant branch phases. It gives the same binary cq channel and error.
This is a channel-statistics statement, not a coherent decoder compiler.

## 4. Exact fidelity / min-max normalization

Write V=S_{s,i}(W), T=(Y^N,U_<i), and
P(x,t)=(1/2)V(t|x). All these classical registers remain in T. Renes uses
root fidelity F and Q(V)=max_q F(P_XT,mu_X tensor q_T)^2 (LF238–241).
Dephasing the candidate q cannot decrease fidelity, so q may be classical.
Cauchy–Schwarz gives the exact optimization

    Q(V) = (1/2) sum_t (sqrt(P(0,t))+sqrt(P(1,t)))^2
         = (1+Z_i)/2,
    Z_i = sum_t sqrt(V(t|0)V(t|1)).

The maximizing q is proportional to the squared parenthesis. In general
it is NOT P_T; replacing the optimizer by P_T would be an unjustified step.
Renes LF236–241 gives P_guess=2^{−H_min} and 2^{H_max}=2Q(V)
(all logarithms base two).
Theorem 2 / Corollary 3, LF529–558, then gives

    P_guess(V^perp)=Q(V)=(1+Z_i)/2.

Together with Section 1 this proves e_{J(i)}=(1−Z_i)/2, with no lost
factor two and with the full classical-prefix register accounted for.
For p_i=P(U_i=0|T), put t_i=|2p_i−1|. Since
Z_i=E sqrt(1−t_i^2), Jensen and Cauchy–Schwarz yield

    E|p_i−1/2| <= (1/2)sqrt(1−Z_i^2)
                = sqrt(e_{J(i)}(1−e_{J(i)})) <= sqrt(e_{J(i)}).

Summing over F gives precisely the topic note's J(F)-indexed bound.

## 5. Scope and evidence

This closes only the paid review's O1/O2 (response LF206–208), by exact
induction and an explicit fidelity optimization against the actual sources.
No experiment, decoder implementation, or asymptotic construction of F is
used. Future frozen bits remain uniform in every synthesized channel here.
Consequently arbitrary PGM/block success, or an arbitrary efficient quantum
decoder for the fixed-frozen code, does not acquire this error certificate
from this proof. Joint-offset sampling, finite-bit SC arithmetic, and the
DQI target-identification obligation O3 are separate established/pending
inputs, not re-proved or silently promoted here. All source locators are
physical LF counts using split('\n') in the retained local text files.

Sources: `audits/sources/nov14_decoder_selection/renes_duality.txt` and
`audits/sources/nov14_decoder_selection/korada_source_raw.txt`; advisory
report: `audits/claude_runs/2026-11-14-polar-dqi-match/response.md`.
