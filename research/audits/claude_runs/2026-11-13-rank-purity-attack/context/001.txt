SOURCE https://arxiv.org/pdf/2610.06819v1
LOCAL research/audits/sources/stabilizer_rank_priority/extent.txt
SHA256 9390e86d5b83a56138e45ac3f34d177a0ab0ba9ba2301b1c44453897b63135f5


Physical LF 120-145
lower bound only if we can control how much this cancellation helps.
    This leads to the question studied here: how strongly does a bound on stabilizer rank constrain
extent? Mehraban–Tahmasbi [MT25] showed that bounded rank forces positive stabilizer fidelity
independent of the ambient dimension, and conjectured that FS (|ψ⟩) ≥ 2−k /C for normalized
states of stabilizer rank at most k, where C > 0 is a universal constant. Kalra–Sinha [KS26] used
Barnes–Wall lattices to control the coefficients in any supplied linearly independent stabilizer
decomposition. Their result√implies ξ(|ψ⟩) ≤ 2O(k log(k+1)) when χ(|ψ⟩) ≤ k. We obtain the
stronger bound ξ(|ψ⟩)√≤ 2O( k log(k+1)) by optimizing the decomposition. This implies stabilizer
fidelity at least 2−O( k log(k+1)) , resolving the quantitative conjecture of Mehraban–Tahmasbi
[MT25], and moreover, improving their conjectured scaling by a square-root factor in the exponent.

1.2   Main results
Theorem 1.1 (Stabilizer rank–extent bound). There is a universal constant c > 0 such that, for
every n ≥ 1, every k ≥ 1, and every vector |v⟩ on n qubits with χ(|v⟩) ≤ k,
                                             √
                                  ξ(|v⟩) ≤ 2c k log2 (k+1) ∥|v⟩∥2 .                      (1.1)

    In particular, every unit vector in the span of k stabilizer states has a decomposition of small
total coefficient size. The stabilizer states in this new decomposition may differ from those spanning
the original space. This freedom is essential to our proof: we replace groups of terms by better
decompositions inside stabilizer codes.
    The same question can be asked for operators. Let χC (A) be the minimum number of Clifford
unitaries whose linear combination equals A, and define the Clifford coefficient norm by
                                               X
                       ΛC (A) =     min
                                    P              |cj |,   Cj Clifford unitaries.

Physical LF 218-230
as a consequence of Theorem 1.2, see Theorem 7.5.

Learning. Substituting Theorem 1.1 into the bounded-extent results of [ADGG26] gives the
following upper bound on the time and sample complexity of low stabilizer rank tomography.

Corollary 1.6. Given copies of an unknown normalized n-qubit pure state |ψ⟩ with χ(|ψ⟩) ≤ k, a
classical description of a pure state within trace distance ε can be produced with failure probability
at most β with sample and time complexity
                                                           √
                                 poly(n, 1/ε, log(1/β)) 2O( k log(2k)) .

   This improves on the previous k k time complexity obtainable from the stabilizer extent bound
proven in [KS26]. See Theorem 8.2. We note that the unitary and Hamiltonian results in [ADGG26,

Physical LF 650-710




                                                               12
 Lemma 3.4 (State block elimination). Suppose a code of dimension at most D contains at least
r stabilizer states in a t-term stabilizer decomposition of |v⟩. Suppose every vector with at most
t − r stabilizer summands satisfies ΛS (|w⟩)2 ≤ b∥|w⟩∥2 . Then
                                          ΛS (|v⟩)2 ≤ (D + 2b)∥|v⟩∥2 .
Proof. Split |v⟩ into its component in the selected code and its orthogonal remainder. The code-
basis bound controls the first component. To control the remainder, we express it as an average of
projections that remove the selected r stabilizer states.
    Let H be the code’s signed stabilizer group, let P be its projector, and put Qg = (I − g)/2 for
g ∈ H. Every selected stabilizer state is fixed by g, so Qg sends it to zero. By Lemma 2.9, the
other terms remain scalar multiples of stabilizer states or become zero. Thus Q√    g |v⟩ has at most
t − r stabilizer summands, and the assumption of the lemma gives ΛS (Qg |v⟩) ≤ b∥Qg |v⟩∥.
    Here Eg denotes the uniform average over H. The projector formula Eg g = P gives Eg Qg =
(I − P )/2. Also Q2g = Qg , so Eg ∥Qg |v⟩∥2 = ⟨v, (Eg Qg )v⟩. These observations yield
                    |v⟩ = P |v⟩ + 2Eg Qg |v⟩,         Eg ∥Qg |v⟩∥2 = 12 ∥(I − P )|v⟩∥2 .        (3.3)
Apply Lemma 3.1 to P |v⟩ and the preceding coefficient-norm bound to each Qg |v⟩. The triangle
inequality and Eg ∥Qg |v⟩∥ ≤ (Eg ∥Qg |v⟩∥2 )1/2 give
                                        √             √
                             ΛS (|v⟩) ≤ D∥P |v⟩∥ + 2 b Eg ∥Qg |v⟩∥
                                        √            √
                                      ≤ D∥P |v⟩∥ + 2b∥(I − P )|v⟩∥
                                        √
                                      ≤ D + 2b∥|v⟩∥.
The last step is Cauchy–Schwarz for the two terms, together with ∥P |v⟩∥2 + ∥(I − P )|v⟩∥2 =
∥|v⟩∥2 .
Theorem 3.5 (Finite stabilizer rank–extent bound). If χ(|v⟩) ≤ k, then for k ≥ 2 and every
2 ≤ r ≤ k,                                              
                           ξ(|v⟩) ≤ (2k)4r 2⌊k/r⌋+1 − 1 ∥|v⟩∥2 .                      (3.4)
For all k ≥ 1, also ξ(|v⟩) ≤ (2k − 1)∥|v⟩∥2 .
Proof. Fix K = k, r, and D = (2K)4r . Clustering either gives ΛS (|v⟩)2 ≤ D∥|v⟩∥2 directly or
supplies a block of r stabilizer states that can be eliminated. By Lemma 3.4, a bound b for the
remaining terms then gives the bound D + 2b. This suggests the following sequence, indexed by
the number of terms:
                                  ⌊t/r⌋                         
                                          2j = D 2⌊t/r⌋+1 − 1 ,
                                  X
                         bt = D                                          0 ≤ t ≤ K.
                                  j=0

It satisfies bt = D for t < r and bt = D + 2bt−r for t ≥ r.
    We prove by induction on t that every vector with at most t stabilizer summands obeys
ΛS (|v⟩)2 ≤ bt ∥|v⟩∥2 . The case t = 0 is immediate. If 0 < t < r, a cluster of r supplied stabilizer
states is impossible, so Lemma 3.3 gives the bound D = bt . For t ≥ r, the same lemma either
gives the bound D ≤ bt or provides a code containing at least r stabilizer states. In the latter
case, induction bounds every vector with at most t − r summands by bt−r , and Lemma 3.4 gives
D + 2bt−r = bt . Taking t = k and recalling ξ = Λ2S proves (3.4).
    For the second estimate, eliminate one stabilizer state at a time. Its ray is a one-dimensional
code, so Lemma 3.4 gives the recurrence c0 = 0 and ct = 1 + 2ct−1 . Hence ct = 2t − 1, as
claimed.

                                                      13
 Corollary 3.6 (Uniform stabilizer rank–extent bound). Define S(0) = 0 and, for integers k ≥ 1,
set                                           √
                                    S(k) = 212 k log2 (2k) .
Then χ(|v⟩) ≤ k implies ξ(|v⟩) ≤ S(k)∥|v⟩∥2 .
    This implies Theorem 1.1. Theplogarithm of the bound in (3.4) is at most 4rL + k/r + 1, where
L = log2 (2k); choosing r of order k/L balances the block cost against the number of elimination

Physical LF 1380-1399
9     Conclusion
Randomized Pauli projections and clustering of stabilizer codespaces give subexponential bounds
on stabilizer extent and Clifford coefficient norm in terms of rank. These bounds connect short
decompositions to small coefficient norms, yielding nearly quadratic rank lower bounds and stronger
guarantees for distinguishing and learning low-rank p states and operators.              √
    A natural question is whether the exponent O( k log(k + 1)) can be improved to O( k). This
would remove the logarithmic loss in our AND and magic-state rank lower bounds. In the present
proof, that loss comes from the dimension cost of merging codespaces; a stronger clustering bound
could therefore lead to an improvement. More broadly, is stabilizer extent polynomially bounded
in stabilizer rank, and does an analogous bound hold for the squared Clifford coefficient norm
relative to normalized Frobenius norm? Such bounds would give exponential rank lower bounds
for magic-state tensor powers and for quadratic-phase representations of AND, respectively.


References
[AD26]        Srinivasan Arunachalam and Arkopal Dutt. Tomography of quantum states with
              bounded extent, 2026. Preprint, arXiv:2606.07425v1.

[ADGG26]      Srinivasan Arunachalam, Arkopal Dutt, Sabee Grewal, and Aparna Gupte. Marton’s
              conjecture in polynomial time, 2026. Preprint, arXiv:2609.20771v1.

SOURCE https://arxiv.org/pdf/2510.05890v2
LOCAL research/audits/sources/stabilizer_rank_priority/structure.txt
SHA256 0d5f5f0c8ee6b50e7718af0b1c2b8cef78be9b67a1916cc1392f908b931b7576


Physical LF 180-214
Theorem 1.3. (Self-Correction) Let τ > 0. Let |ψ⟩ be an unknown n-qubit quantum state
such that FS (|ψ⟩) ≥ τ. Assuming the high-doubling algorithmic PFR Conjecture 1.2, there is a
protocol that with probability 1 − δ, outputs a |ϕ⟩ ∈ Stab such that |⟨ϕ|ψ⟩|2 ≥ τ C (for a universal
constant C > 1) using poly(n, 1/τ, log(1/δ)) time and copies of |ψ⟩.
    We provide the formal statement of this result in Section 4. In the table below, we compare
our work with the state-of-the-art results in this direction. Like we mentioned in the introduction,

                                                   4
                                                          Access                Time
            FS (|ψ⟩) = opt         Output
                                                         model               complexity

             [GIKL24b]         Stabilizer state                                     4
                                                     Sample access             2n/τ /ε2
               opt ≥ τ       with fidelity ≥ τ − ε

             [CGYZ25]          Stabilizer state
                                                     Sample access   poly(n, 1/ε) · (1/τ )log(1/τ )
              opt ≥ τ        with fidelity ≥ τ − ε

             This work ∗       Stabilizer state
                                                     Sample access           poly(n, 1/τ )
              opt ≥ τ         with fidelity ≥ τ C

Table 1: Summary of results. In the access model, sample access refers to an algorithm which is
only given copies of |ψ⟩ and Uψ , conUψ access refers to an algorithm which is given access to state
preparation unitary Uψ (and its controlled version conUψ ) such that Uψ |0n ⟩ = |ψ⟩. The ∗ on this
work is to indicate that it relies on the high-doubling algorithmic PFR conjecture.

in comparison to the harder task of agnostic learning [GIKL24b, CGYZ25] for which we have a
quasi-polynomial algorithm, our work can be viewed as answering a weaker question, but on the
flip-side we are able give a polynomial-time algorithm for this task (assuming the high-doubling
algorithmic PFR conjecture). Furthermore, we remark that our algorithm involves only single-copy
and two-copy measurements of the unknown quantum state.
2. Structured decomposition. In order to prove our self-correction result, our main contribution

Physical LF 932-978
2.3     Gowers norm and inverse theorems
                                    P
For any n-qubit quantum state |ψ⟩ = x∈{0,1}n f (x) |x⟩ where f = (f (x))x is an ℓ2 -normed vector,
one can define its Gowers-k norm [AD25] as follows
                                                                                                                1/2k
                                                                           Y
              Gowers (|ψ⟩, k) = 2n/2                     E                         C |ω| f (x + ω · h)                 ,                    (8)
                                             x,h1 ,h2 ,...,hk ∈{0,1}n
                                                                         ω∈{0,1}k


where C |ω| f = f if |ω|:=
                            P
                              j∈[k] ωk is even and is f if |ω| is odd with f denoting the complex
conjugate of f . We state facts about Gowers norm of quantum states, that will be useful later.
Fact 2.10 ([AD25, Lemma 3.3]). For every |ψ⟩ we have that
                                                                                                                                      2
                       8                          2
                                                                                    2
                                                                                                                             2
                                                                                                                                  
       Gowers (|ψ⟩, 3) = E            |⟨ψ|Wx |ψ⟩|         ≥ E          |⟨ψ|Wx |ψ⟩|          ≥        E         |⟨ψ|Wx |ψ⟩|                .
                           x∼pΨ                            x∼qΨ                                     x∼pΨ
                                                                                                |                 {z                  }
                                                                                                      =Gowers(|ψ⟩,3)16


    We have the following inverse theorem for the Gowers-3 norm of quantum states that was
established in [AD25].
Theorem 1.7 ([AD25]). Let γ ∈ [0, 1]. If |ψ⟩ is an n-qubit state such that Ex∼qΨ [2n pΨ (x)] ≥ γ,
then there is an n-qubit stabilizer state |ϕ⟩ such that |⟨ψ|ϕ⟩|2 ≥ Ω(γ C ) for some constant C > 1.
     As it is easier to estimate Ex∼qΨ |⟨ψ|Wx |ψ⟩|2 which is a proxy for the Gowers-3 norm given
                                                       

the relation in Fact 2.10, we also have the following inverse theorem.
Theorem 2.11. Let γ ∈ [0, 1]. If |ψ⟩ is an n-qubit quantum state such that Ex∼qΨ |⟨ψ|Wx |ψ⟩|2 ≥
                                                                                                      
                                                                           ′
γ, then there is an n-qubit stabilizer state |ϕ⟩ such that |⟨ψ|ϕ⟩|2 ≥ Ω(γ C ) for some constant C ′ > 1.

2.4     Useful facts and subroutines
Fact 2.12. Let Y be a random variable with |Y |≤ 1. If E[Y ] ≥ ε, then

                                         Pr[Y ≥ δ] ≥ (ε − δ)/(1 − δ)

Fact 2.13. (Hoeffding bound) Let Y be a random variable with |Y |≤ 1 and µ
                                                                         b is the empirical

SOURCE https://arxiv.org/pdf/2609.20771v1
LOCAL research/audits/sources/stabilizer_extent/marton.txt
SHA256 7e1ca6f73b723ad2e24703a7cb0d6f2dc1f3d6e7b6dfcd123cf85571bbc4c4ad


Physical LF 3148-3178
that in agnostic learning, for an unknown state |𝜓 ⟩ which is promised to be opt-close to a state in a class C,
the goal is, given copies of |𝜓 ⟩ output an element of C which is opt − 𝜀 close to |𝜓 ⟩. In the self-correction
task, they consider if the task becomes easier if the goal was to output an element in C which is poly(opt)
close to |𝜓 ⟩. To this end, they proved the following theorem.14
Theorem 8.5 ([AD26a]). Let τ > 0. Let |𝜓 ⟩ be an unknown 𝑛-qubit quantum state such that

                                                         max            |⟨𝜓 |𝜑⟩| 2 ≥ τ.
                                                     |𝜑 ⟩ ∈stabilizer

Assuming the approximate algorithmic PFR conjecture, there is a protocol that with probability 1 − 𝛿, outputs
a |𝜑⟩ ∈ stabilizer such that |⟨𝜑 |𝜓 ⟩| 2 ≥ 𝜏 𝐶 (for a universal constant 𝐶 > 1) using poly(𝑛, 1/τ, log(1/𝛿)) time
and copies of |𝜓 ⟩.
    Using our approximate algorithm PFR result in Theorem 8.2, we remove the assumption in their work
Corollary 8.6. The guarantees of Theorem 8.5 hold without any assumptions.

8.2.2    Improper agnostic tomography.
In a later work, [AD26b] provided a boosting framework that took the self-correction procedure to give an
algorithm for learning stabilizer decompositions of any quantum state |𝜓 ⟩ given copies. Particularly, the
following is now true as a consequence of Corollary 8.6 applied to [AD26b, Theorem 1.2].
Corollary 8.7. Let 𝜀, 𝛿 ∈ (0, 1). Suppose |𝜓 ⟩ is an unknown 𝑛-qubit state. Then, there is an algorithm that
uses copies of |𝜓 ⟩ and with probability ≥ 1 − 𝛿, outputs a list of 𝜅 = poly(1/𝜀) many states {|𝜑𝑖 ⟩}𝑖 ∈ [𝜅 ] and
coefficients 𝛽 ∈ C𝑘 such that |𝜓 ⟩ can be expressed (up to a global phase) as
                                     𝜅
                                    ∑︁
                           |𝜓 ⟩ =         𝛽𝑖 |𝜑𝑖 ⟩ + 𝛼 |𝜑𝑅 ⟩ , where |𝛼 | 2 ·           max            |⟨𝜑 |𝜓 ⟩| 2 ≤ 𝜀.
                                                                                    |𝜑 ⟩ ∈stabilizer
                                    𝑖=1

The sample and time complexity of this algorithm is poly(𝑛, 1/𝜀).
    Moreover, this implies a polynomial-time agnostic learner for the class of stabilizer states, albeit the
output of the agnostic learner is improper, i.e., need not be a stabilizer state itself. The following was shown