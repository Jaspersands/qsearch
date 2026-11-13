SOURCE https://arxiv.org/pdf/2510.08494v1
LOCAL research/audits/sources/2026-11-13-community-selection/schmidhuber_zlokapa.txt
SHA256 c4a42b745ef40c96dcf5fa3837c2901eb0f90abdc6c212e77269adcad13b8c9c

Physical LF 184-205
 Definition 2 (𝑝-marginal HSBM with 𝑘 communities). Let 𝑝, 𝑘, 𝑛 ≥ 2 and let 𝑎 ∈ [𝑘]𝑝 . Define
                                                𝑝 (︂
                                             𝑘 ∏︁                     )︂
                                            ∑︁                    1
                   𝑓 (𝑎1 , . . . , 𝑎𝑝 ) =                1𝑎𝑗 =𝑖 −          ,        0 < 𝜃0 < 1/2,           0 < 𝜖 < 𝜃0 ,                   (1)
                                            𝑖=1 𝑗=1
                                                                  𝑘

where 𝜃0 , 𝜖 may scale nontrivially with 𝑛. For each 𝑎 ∈ [𝑘]𝑝 , define

                                      𝜇𝑎 = Bern(𝜃0 + 𝜖𝑓 (𝑎)),                   𝜇avg = Bern(𝜃0 ).                                          (2)

The 𝑝-marginal HSBM(𝑛, 𝑘, 𝜃0 , 𝜀) then consists of the following two probability measures over hypergraphs
𝑌 with vertex set 𝑉 = [𝑛] and hyperedge sets 𝐸 defined as follows.
  1. Under Q, for each 𝑆 ∈ [𝑛]
                              (︀ )︀
                                𝑝   draw hyperedges 𝑌𝑆 ∼ 𝜇avg independently and add 𝑆 to 𝐸 if 𝑌𝑆 = 1.

  2. Under P, first fix labels 𝑥 ∼ Unif([𝑘]𝑛 ). Then for each 𝑆 = {𝑠1 < · · · < 𝑠𝑝 } ∈ [𝑛]
                                                                                          (︀ )︀
                                                                                            𝑝 , draw 𝑌𝑆 ∼
     𝜇𝑥𝑠1 ,...,𝑥𝑠𝑝 independently and add 𝑆 to 𝐸 if 𝑌𝑆 = 1.

Physical LF 649-652
    • Recovery of community labels. Beyond detection, practical applications are often interested in re-
      covering the community structure. In the quantum Kikuchi algorithm for Tensor PCA, the ground
      state contains sufficient information to recover the planted spike via state tomography and a rounding
      procedure. We leave open the analogous question of recovering community labels here.

SOURCE https://arxiv.org/pdf/2607.29672v1
LOCAL research/audits/sources/2026-11-13-community-baselines/sharp_kikuchi.txt
SHA256 b050a9b9a0b443e28223ea5509d20ed0154f22ee810695ff36b6aa3a07f4e13b

Physical LF 2866-2929
12.4    Recovery from the accepted band
The guided circuit is retained coherently rather than used only as a decision procedure, so we need a
statement uniform over the whole accepted spectral band.
Proposition 12.6. On the high-probability planted event, let σ be√any density operator supported on
Ran Π− . Apply the trace-nonincreasing filter with Kraus operator d Γ−1/2 and condition on success;
equivalently, the normalized post-filter state is

                                                  Γ−1/2 σΓ−1/2
                                           σ
                                           e :=                .                                  (12.19)
                                                   Tr(Γ−1 σ)

Then apply the isometry |S⟩ 7→ L−1/2 i∈S |i⟩|S \ {i}⟩ and trace out the second register. The resulting
                                    P
one-particle state ϱ satisfies         ⋆
                                              x⋆
                                                   
                                       x
                                       √ , ϱ√       ≥ ck > 0.                                  (12.20)
                                         n      n
For even k, the conclusion is understood modulo the unavoidable global sign.
Proof. Every unit vector v ∈ Ran Π− has Rayleigh quotient at least b− ρκk , so the uniform planted
comparison shows that, after applying Γ−1/2 and the gauge in the analysis, the normalized vector has
constant positive energy in Jk/2 (even k), respectively Jk−1 (odd k). The proof of Theorem 4.10 is
sesquilinear and extends verbatim to complex   Pvectors, with transposes replaced by adjoints, giving
(12.20) for every such v. Diagonalizing σ = j qj |vj ⟩⟨vj | inside Ran Π− , the post-filter state is the
convex mixture of the normalized Γ−1/2 vj with weights proportional to qj ∥Γ−1/2 vj ∥2 ; the one-particle
channel is linear, so the planted-mass bound survives the mixture. The gauge commutes with the
diagonal filter and is used only in the analysis.
                                                                    p
    The filter is implemented by a controlled rotation of amplitude d/Γ(S, S) and succeeds on every
state with probability at least d/BΓ . To handle the coherent leakage allowed by Lemma 12.5, use the
accuracy
                                                        d 2
                                                            
                                                  1
                                          η :=               .                                    (12.21)
                                               log2 n BΓ

                                                      49
 Indeed, if Tr(Π− σ) ≥ 1 − η and σ− := Π− σΠ− / Tr(Π− σ), the gentle-measurement lemma gives
                  √
∥σ − σ− ∥1 ≤ 3 η; the trace-nonincreasing map X 7→ d Γ−1/2 XΓ−1/2 contracts trace norm while
retaining mass at least d/BΓ on σ− , so the two normalized post-filter outputs are within trace distance
            √
O((BΓ /d) η) = o(1), and (12.20) survives with a smaller constant.
     Standard tomography then recovers the n-dimensional one-particle state: estimating every entry of
ϱ to accuracy n−2 , by repeated measurement in the standard basis and in the O(n2 ) two-dimensional
rotated bases revealing the real and imaginary parts of one off-diagonal entry, controls the operator
norm at scale 1/n; Hoeffding’s inequality and a union bound over entries give a Hermitian estimate ϱb
with ∥b  ϱ − ϱ∥ ≤ ηtom = o(1) from nO(1) log n accepted copies, with failure probability n−1 ; all of this is
absorbed into (12.24).
     Since x⋆ is real, pass to real parts: R := Re(ϱ) is real positive semidefinite with unit trace and
x̄T Rx̄ ≥ ck by (12.20), while Rb := Re(bϱ) satisfies ∥R−R∥
                                                       b     ≤ ηtom . With α0 := ck /4 and Π
                                                                                           b := 1[α ,∞) (R),
                                                                                                    0
                                                                                                          b
Weyl’s inequality gives rank Π b ≤ 8/ck , and ck − ηtom ≤ x̄T Rx̄              b 2 + α0 (1 − ∥Πx̄∥
                                                              b ≤ (1 + ηtom )∥Πx̄∥             b 2 ) forces
       2
∥Πx̄∥ = Ωk (1). Constant rank and constant planted overlap are exactly the inputs of Lemma 4.11,
  b
applied to Ran b  Π; an independent validation pool then gives a Boolean vector of constant overlap.

Physical LF 2970-3005
The upper bounds of this paper are stated for kXOR, but fixed Boolean predicates in the uniform
random-scope/random-literal model admit an exact Fourier reduction: every nonzero Fourier character
of a known local planting law is, exactly, a noisy-XOR channel. The transfer is channelwise and carries
over the classical inference and two-sided refutation upper bounds, and, for channels of degree at least
two, the quantum detection and weak-recovery upper bound under the hypotheses of Theorem 12.7;
degree-one channels are handled directly. It does not transfer the kXOR lower bounds to procedures
that use the complete local output jointly, and it makes no quantum-refutation claim.

Related work on general CSPs. Concurrent work of Chan, d’Orsi, and Xu [20] extends sum-of-
squares and spectral refutation to general random CSPs without uniformly random literals through
odd and asymmetric Kikuchi operators; their model is substantially broader than the random-literal
reduction here, whose point is the log-free transfer of the normalized kXOR bounds.
   Fix a constant arity K. A local planting law is a known distribution W on {±1}K . A planted
constraint chooses an ordered K-tuple of distinct variables uniformly and reveals

                               Yj = x⋆ij Wj ,        W = (W1 , . . . , WK ) ∼ W.                      (13.1)

Under the null, the revealed literal vector is uniform on {±1}K . For nonempty S ⊆ [K], define
                                                        Y
                                          µS := EW ∼W      Wj .                                (13.2)
                                                               j∈S

Lemma 13.1. If µS ̸= 0, then                                    Y
                                           bSa := sign(µS )           Yaj                             (13.3)
                                                                j∈S

is exactly a planted noisy |S|XOR label of bias |µS | on support {iaj : j ∈ S}. Under the null it is exactly
an unbiased XOR label.

Proof. The identity                                                          
                                    Y                Y                Y
                                          Yaj =         Waj              x⋆iaj 
                                    j∈S           j∈S                 j∈S

is exact. Restricting a uniform ordered tuple of distinct variables to the positions in S leaves a uniform
ordered |S|-tuple, and under the null the product of a nonempty subset of uniform independent literals

SOURCE https://arxiv.org/pdf/2604.10457v1
LOCAL research/audits/sources/2026-11-13-community-recovery/mao.txt
SHA256 72f706e731ef13998365e826c747363966cd5cbe0cbf6a96beb56a1f5f54e299

Physical LF 220-254
1.1   Our results
We begin by formalizing the noisy k-XOR model and the two algorithmic tasks that will be studied
throughout the paper, namely distinguishing and recovery.

Definition 1.3 (Noisy k-XOR). Fix k ≥ 2, and let x ∈ {±1}n be an unknown planted assignment.
In the noisy k-XOR model, we observe m samples (α1 , z1 ), . . . , (αm , zm ), where each αt ∈ [n]
                                                                                                   
                                                                                                k   is
drawn uniformly at random, and
                                        Y  
                                  zt =      xi ξt ∈ {±1},
                                             i∈αt

with ξt independent and Pr[ξt = 1] = 1+δ                 1−δ
                                        2 , Pr[ξt = −1] = 2 . We denote this planted distribution
by Px . The null distribution Q is defined in the same way, except that z1 , . . . , zm are independent
uniform random signs, independent of the sampled k-tuples.
   A distinguishing algorithm outputs 0 or 1 given the samples. Its success probability is
                                     1            1
                                       Pr[A = 1] + Pr[A = 0].
                                     2 Px         2 Q

We say that A strongly distinguishes if this probability is 1 − o(1), and weakly distinguishes if it
is at least 1/2 + ε for some fixed constant ε > 0.
    A recovery algorithm outputs an estimate x  b ∈ {±1}n from samples drawn from Px . Its success
probability is
                                      Pr[b
                                         x = x]     if k is odd,
                                      Px


                                                    5
 and
                                     x ∈ {x, −x}]
                                  Pr[b                 if k is even.