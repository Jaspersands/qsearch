
SOURCE research/audits/sources/dissipative_selection/rapid.txt; url=https://arxiv.org/pdf/2503.15827; SHA256=8115a7a3f5a509cf003393b35eea3a6d68bbe0f6666da673905ad20e8ac429b9


Original LF lines 77-168:
lies in the invertibility of thermal states, which is essen-   We refer to Ka as a jump operator, P −i[H, ρ] as the coher-
tial for the concept of quantum detailed balance condi-        ent part of the dynamics, and a Ka ρKa† − 21 Ka† Ka , ρ
tions (DBC) [3, 8, 10, 22, 24]. In contrast, the density       as the dissipative part of the dynamics, respectively.
matrix of a pure ground state has rank one and is there-          Starting from a set of coupling operators {Aa }, whose
fore non-invertible, which makes most existing theoreti-       selection will be discussed in detail later, the correspond-
cal tools inapplicable in this setting. Numerically, these     ing jump operator Ka is engineered to “shovel” high en-
protocols can also be difficult to simulate for systems be-    ergy components in the density matrix towards lower en-
yond the reach of exact diagonalization methods, as con-       ergy ones (Fig. 1a). The success of the ground state
structing the corresponding Lindblad jump operators is         preparation algorithm relies on the assumption that,
significantly more complex than that in typical Lindblad       starting from a simple initial state (e.g. the all-zero state
dynamics.                                                      or the maximally mixed state), which contains contri-
   In this work, we make significant progress in under-        butions from many high energy states such as |ψj1 ⟩ for
standing the capabilities of dissipative ground state pro-     some j1 > 0, there exist efficient transition pathways
tocols through both analytical and numerical investiga-        ψj1 → ψj2 → · · · → ψ0 .
tions. A concise overview of the numerical and theoretical        In the energy eigenbasis, the jump operator takes the
results is provided in Section III.                            form
   The rest of the paper is organized as follows. In
                                                                                  fˆ (λi − λj ) |ψi ⟩ ⟨ψi |Aa |ψj ⟩ ⟨ψj | .
                                                                              X
Section II, we review the Lindblad-based ground-state                  Ka =                                                 (2)
preparation algorithm, introducing the notion of mixing                        i,j
time and discussing considerations for estimating the re-
source requirements of dissipative protocols. Before the       Here {λi , |ψi ⟩} represent eigenpairs of the system Hamil-
full discussion, Section III provides an overview of the       tonian H ordered such that λ0 < λ0 + ∆ = λ1 ≤ · · · , and
main results. We develop a tensor-network method for           fˆ (ω) is a filter function in the frequency domain. The
simulating general Lindblad dynamics on classical com-         filter function fˆ(ω) is supported only on the negative axis
puters in Section IV. In Section V A, we present the per-      (−ωmax , 0) for some ωmax to be specified later. As a re-
formance of the ground-state preparation protocol for a        sult, in the energy eigenbasis, only transitions from |ψj ⟩
variety of systems governed by quasi-free Lindblad dy-         to |ψi ⟩ satisfying −ωmax ≤ λi − λj ≤ 0 are allowed. The
namics. In Section V B, we report the numerical perfor-        parameter ωmax therefore characterizes the maximal en-
mance of the tensor-network method for simulating the          ergy change per application of the jump operator. More-
ground state preparation process beyond quasi-free sys-        over, for any choice of Aa , we have Ka |ψ0 ⟩ = 0, since
tems. Section V C provides a concrete example compar-          there is no eigenstate with energy lower than λ0 . Hence,
ing dissipative protocols with adiabatic state preparation     the ground state σ = |ψ0 ⟩⟨ψ0 | is always a fixed point, or
methods for preparing ground states. On the theoretical        stationary state of the dynamics.
side, in Section VI A we estimate the convergence rate in          Eq. (2) expresses the jump operator Ka using the
trace distance for quasi-free systems, confirming the nu-      eigendecomposition of H. It can be equivalently repre-
merical results of Section V A. Our rigorous analysis of       sented in the time domain as follows. By expressing fˆ(ω)
rapid mixing for ground-state preparation is presented in      as a filter function in the time domain via the Fourier
Section VI B. Background material, detailed proofs, and        transform
additional numerical results are collected in the Appen-
                                                                                          1
                                                                                            Z
dices.                                                                          f (s) :=       fˆ(ω)e−iωs dω,           (3)
                                                                                         2π R

                                                               and using the spectral decomposition of H, we obtain
    II.   LINDBLAD-BASED GROUND STATE
           PREPARATION ALGORITHM                                                 Z ∞
                                                                           Ka =        f (s)eiHs Aa e−iHs ds.      (4)
                                                                                     −∞
   The main goal of this work is to examine the perfor-
mance of the Lindblad-based ground state preparation           Although the construction may appear relatively compli-
algorithm introduced in Ref. [19]. This dissipative algo-      cated, we can represent the jump operator coherently on
rithm, inspired by gradient descent dynamics in classical      a quantum computer using a block encoding [31]. The re-
systems, employs carefully designed jump operators to          sulting linear combination of Heisenberg evolutions of Aa
iteratively reduce the system’s energy and can prepare         involves only queries to Hamiltonian simulation and does
ground states for noncommuting Hamiltonians.                   not require diagonalizing the Hamiltonian H. This, in
   Algorithmic construction— The Lindblad master               turn, requires efficiently approximating the integral in (4)
equation for ground state preparation proposed in [19,         through an appropriate numerical quadrature scheme.
Eq. (1)] takes the form                                           Let ∥H∥ and ∆ denote the spectral radius and the
                                                               spectral gap of the Hamiltonian H, respectively. To con-
 dρ                     X           1  †                       struct this quadrature, f (s) should decay rapidly as |s| →
    = L[ρ] = −i[H, ρ] +   Ka ρKa† −   Ka Ka , ρ . (1)
 dt                     a
                                    2                          ∞ so that the integration range can be truncated. By the
                                                                                                                                 3

duality between the real-space and frequency-space rep-          forms of Lindblad dynamics. For example, high-order al-
resentations of a function, fˆ(ω) should be as smooth as         gorithms [14, 21, 48] can achieve near-optimal simulation
possible in the frequency domain, while still allowing the       cost per unit time. Both the construction of Ka and the
jump operator to efficiently induce a transition from |ψ1 ⟩      simulation algorithms [14, 21, 48] can use multiple an-
to |ψ0 ⟩. This implies that fˆ(λ0 − λ1 ) = fˆ(−∆) should         cilla qubits, complex control logic and are suitable only
have a non-negligible value. Together with fˆ(0) = 0, the        on full fault-tolerant quantum computers.
function fˆ must make a sharp transition within an en-              The second, and simpler, strategy for simulating the
ergy window of size ∆. This implies that in the time             Lindblad dynamics in (1) is to exploit the specific form
domain, f (s) is approximately supported on an interval          of the jump operator in Eq. (4). In particular, this ap-
whose size is proportional to ∆−1 .                              proach does not explicitly construct Ka but instead em-
   For efficient discretization of the integral, we note that    beds it directly into the simulation algorithm. This in
f (s) oscillates in the time domain with a wavelength            turn can lead to algorithms that overall use only a single
on the order of ωmax −1
                         , which implies that ωmax should        ancilla qubit and can be much more suitable for early
not be chosen excessively large. Naturally, we choose            fault-tolerant quantum devices. We will not discuss such
ωmax ≤ 2 ∥H∥, since no energy transition beyond this             algorithms in detail and refer the reader to [19, Section
range can occur. For simplicity of the analysis, in this         III] for descriptions of such algorithms. We note that
work we always choose ωmax = 2 ∥H∥. In practice, it is           while the simulation algorithm proposed in [19, Section
often sufficient to choose ωmax to be much smaller and in-       III] is designed for simulating a single jump operator us-
dependent of the system size. The behavior of fˆ(ω) and          ing a single ancilla, when multiple jump operators are
f (s) is illustrated in Fig. 1 (b),(c), respectively. Based      present, operator splitting can be applied to handle each
on the discussion above, the construction of this filter         jump operator separately.
function requires only a lower-bound estimate for ∆, and
                                                                    Mixing time— Dissipative protocols prepare the


Original LF lines 246-279:
ated with constructing the Lindbladian and in particular
jump operators Ka , denoted by CL ; the cost of simu-
lating Lindblad dynamics per unit time denoted by CS ,
using a Lindblad simulation algorithm as discussed ear-       Figure 1: (a) Schematic representation of the ground state
lier; and τmix , an upper bound on the total simulation       preparation algorithm, in which high-energy components are
time. Given these factors, the end-to-end resource cost       systematically dissipated into lower-energy states until
                                                              convergence to the ground state is achieved. (b) and (c)
is
                                                              depict the associated filter function in the frequency and
                                                              time domains, respectively.
           End-to-end cost = CL × CS × τmix .          (9)

   Using the standard approach for simulating the Lind-                  III.   SUMMARY OF RESULTS
blad dynamics, the cost for constructing Ka to precision ϵ
   e max ∆−1 log(1/ϵ)) [19] (see Section A for the mean-
is O(ω                                                                          A.   Numerical results
                    e Let ∥L∥be := ∥H∥ + 1 P ∥Ka ∥2 .
ing of the notation O).                     2    a
Using the algorithm in [48] for simulating the Lind-
                                                                 We perform numerical simulations for both quasi-free
blad dynamics    (1) up
                        to time
                                 t with precision ϵ the
            
                        t∥L∥be
                                                              and general dissipative dynamics. For general dissipative
cost is O t∥L∥be log       ϵ     . For a typical physical     dynamics, we develop a new numerical simulation algo-
Hamiltonian (spin, fermion, etc.) defined on N sites,         rithm based on tensor networks, which is described in
∥L∥be = poly(N ) and the end-to-end cost is                   Section IV.

            O(τmix ∆−1 poly(N )polylog(1/ϵ)).
            e                                         (10)    Quasi-free dynamics (Section V A):
                                                                 We begin by exploring quasi-free dissipative dynam-
The simplified algorithm in [19, Section III] combines the    ics [5, 67]. Lindblad dynamics is called quasi-free if


Original LF lines 2084-2140:
           Appendix H: Proof of rapid ground state preparation of weakly interacting spin systems

  In this section, we show the rapid ground state preparation for the perturbed Hamiltonian. First, we introduce
the assumptions of the filter function f , which is similar to that in [19, Assumption 12]. Our analysis employs the
Gevrey function, a subclass of smooth functions characterized by well-controlled decay of the Fourier coefficients.
This characteristic plays a crucial role in the quadrature analysis.
Definition 6 (Gevrey function). Let Ω ⊆ Rd be a domain. A complex-valued C ∞ function h : Ω → C is a Gevrey
function of order s ≥ 0, if there exist constants C1 , C2 > 0 such that for every d-tuple of nonnegative integers
α = (α1 , α2 , . . . , αd ),
                                                                         |α|
                                              ∥∂ α h∥L∞ (Ω) ≤ C1 C2 |α||α|s ,                                                  (H1)
           Pd                                                                                      s
where |α| = i=1 |αi |. For fixed constants C1 , C2 , s, the set of Gevrey functions is denoted by GC 1 ,C2
                                                                                                           (Ω). Furthermore,
 s             s
     S
G = C1 ,C2 >0 GC1 ,C2 .
   We refer readers to [1, 37] for background on the Gevrey class. We also note that the use of Gevrey class functions
is mainly for simplifying the discretization error analysis and not essential for the design of the Lindbladian.
Assumption 7 (Filter function in the frequency domain). Assume fˆ in the Fourier domain takes the form:

                                                    fˆ(ω) = û(ω/8)v̂(2ω) .                                                    (H2)
                                                             α
Here, û is a positive function and belongs to Gevrey class GA 1,u ,A2,u
                                                                         (R) for some A1,u , A2,u > 0 and α > 1, meaning
that
                                                 dn
                                            sup    n
                                                     (û(ω)) ≤ A1,u An2,u nnα
                                            ω∈R dω

for any n ∈ N. Also, supp(û) ⊂ [−1, 1], û(ω) = Ω(1) when ω ∈ [−1/2, 1/2], and û(−1/4) = 1. In addition, we assume
      α                 d
v̂ ∈ GA 1,v ,A2,v
                  (R), dω v̂ L1 = O(1), supp(v̂) ⊂ (−∞, 0], and v̂(−4) = 1.
  We define the perturbed Hamiltonian as
                                                           X              X
                                                  Hε = −         Zi + ε        hj .                                            (H3)
                                                            i              j

   Compared to [19, Assumption 12], the above assumption sets ∆ = 1/2 and Sω = 4, which is sufficient to en-
sure (H13). First, setting ∆ = 1/2 is adequate for our analysis since the spectral gap of H0 is one, implying that the
spectral gap of Hε remains greater than 1/2 when ε is sufficiently small. Second, choosing Sω = 4 is sufficient because
the coupling operator Ai = Xi modifies the energy of H0 by at most one, ensuring that the energy decay of Hε can
also be bounded by 4 when ε is sufficiently small.
   Now, we are ready to present the rigorous version of Theorem 2:
                                                                                                                           30

Theorem 8 (Rigorous version of Theorem 2). Assume H is a (r0 , l)-local Hamiltonian that takes the form of (42),
choose the coupling operators {Aa } = {Xi }i∈Λ , and the filter function f satisfies Assumption 7. There exists a
constant ε∗ only depends on k, l, D such that when ε < ε∗ , we have

                               ∥exp(Lt)ρ − |ψ0 ⟩ ⟨ψ0 |∥1 ≤ η, ∀t = Ω(log(N/η)) , ρ
                                                                  
where N = (L + 1)D is the system size. Here, ε∗ = Oe (r0 l)−Θ(D) .

   The proof of Theorem 8 is based on the analysis of the convergence of observables in the Heisenberg picture,


Original LF lines 2346-2360:
                                                  r      r                                                    (i,r)
Hε on a ball of radius r centered at lattice i. Ki,ε , Li,ε are defined according to (H11) and (H12) with Hε . Then
we have the following lemma:
Lemma 10. Under conditions of Theorem 8 and let J = r0D l, for any r ≥ 1, we have
                                                                                         
                                                      1
                    Lr†
                      i,ε − L r−1†
                              i,ε      ≤ ξ(r) =  O       +  exp(−C  2,f (r/(4Je))1/α
                                                                                     /2)  ,
                                   ∞→∞               2r                                                                                (H17)
                    L†i,ε − L†i,0    ≤ η(ε) = O ε(J logα (1/ε) + 1)D l .
                                                                           
                                              ∞→∞



SOURCE research/audits/sources/dissipative_selection/weak_ground.txt; url=https://arxiv.org/pdf/0707.1894; SHA256=0a06cb8e0bb61a410ebd8f2705c8daddd6d24a6c5a93ae9a4be77a6d3d488808


Original LF lines 99-161:
                                    |Ωi = |0, 0, . . . , 0i, H0 |Ωi = 0.
Most of the time, all we will need to know about H0 and V are the following parameters

                                   ∆ = min ∆u ,     J = max kVu,v k.                                 (2)
                                        u∈L               (u,v)∈E

The parameter ∆ is the gap between the smallest and the second smallest eigenvalue of H0 , while the
parameter J characterizes a strength of the perturbation V . Let d be the maximum vertex degree
of the graph G,
                                   d = max |{v : (u, v) ∈ E}| .                                  (3)
                                           u∈L

The quantity we are interested in is the smallest eigenvalue of H(ǫ), which we shall denote by E(ǫ).
Clearly, E(ǫ) is a continuous concave function of ǫ and E(0) = 0. Besides, since we assume that
∆ > 0, the standard perturbation theory arguments [3] show that E(ǫ) is analytic at ǫ = 0 and the
Taylor series
                                                  X∞
                                          E(ǫ) =      Ep ǫp                                     (4)
                                                    p=1

converges absolutely for kǫV k < ∆/2. The following theorem proved by Yarotsky [4] asserts that
E(ǫ) is non-degenerate for sufficiently small ǫ and sets a lower bound on the spectral gap.

                                                    3
 Theorem 1. Suppose |ǫ| ≤ 2ǫ0 , where
                                                  2−18 ∆
                                                ǫ0 =     .                                        (5)
                                                    dJ
Then the smallest eigenvalue E(ǫ) has multiplicity 1 and the gap between E(ǫ) and the second smallest
eigenvalue of H(ǫ) is at least ∆/2.

(The explicit value of ǫ0 has not been stated in Ref. [4].) We shall provide an alternative proof of
Theorem 1 in Sections 2,3.
    As was shown by Osborne in Ref. [5], Theorem 1 implies that expectation values of local observ-
ables on the ground state of H(ǫ) can be efficiently computed within any constant precision δ by
simulating quantum adiabatic evolution along the path connecting H(0) and H(ǫ). However, the
running time of such simulation scales exponentially as a function of δ −1 . As was noted in Ref. [5],
it means that simulation of the adiabatic evolution does not yield a polynomial-time algorithm for
computing the ground state energy.
    The perturbation theory provides an approximation to the ground state energy by truncating the
series Eq. (4) at sufficiently high order p. In order to understand whether this approach can be used
to construct an efficient computational algorithm, two separate issues have to be addressed:

 Q1: What is the convergence radius of the perturbative series?

 Q2: What is the computational cost of finding the coefficients in the perturbative series?

Note that the radius of convergence of the series Eq. (4) is a property of the Hamiltonian H(ǫ) only.
It does not depend upon what particular perturbative expansion has been used to find the coefficients
Ep . The following theorem allows one to answer the first question.

Theorem 2. The Taylor series E(ǫ) = ∞              p
                                        P
                                           p=1 Ep ǫ converges absolutely for |ǫ| ≤ 2ǫ0 . Furthermore,

                                       p
                                       X
                              E(ǫ) −         Eq ǫq ≤ n∆2−16−p   if |ǫ| ≤ ǫ0 .                          (6)
                                       q=1


    Thus if one needs to compute E(ǫ) with a specified precision δ, it suffices to compute the coeffi-
cients E1 , . . . , Ep , where p = log2 (nδ −1 ) + O(1) (assuming that ∆ is a constant that does not depend


Original LF lines 177-197:
 Theorem 3. Suppose d is a fixed constant independent of n. Then there exists an algorithm with a
running time n exp (O(p)) that takes as input a triple (H0 , V, p) and outputs E1 , . . . , Ep .
      An immediate consequence of Theorems 2,3 is
Corollary 1. Suppose ∆, J, d are fixed constants independent of n and |ǫ| ≤ ǫ0 . Then there exists
an algorithm with a running time poly(n, δ) that computes E(ǫ) with an absolute error at most δ.
    Besides, it follows from Theorems 2,3 that the energy density E(ǫ)/n can be computed with a
precision δ in a time n · poly(δ −1).
    Note that while computing the coefficients E1 , . . . , Ep we cannot afford the running time to grow
faster than exp (O(p)) (for fixed n) since we need p ∼ log (nδ −1 ) to achieve the desired accuracy. The
perturbative expansion based on the Kirkwood-Thomas ansatz has two special features that make
the scaling exp (O(p)) possible: (i) The parameters of the ansatz are complex amplitudes C(M)
assigned to subsets of vertices M ⊆ L. The recursive equations specifying the amplitudes C(M)
are described
           P∞ by a polynomial     of a constant degree, see Section 3.1; (ii) The perturbative expansion
                          p
C(M) = p=1 Cp (M) ǫ has a property known as the linked cluster theorem, namely, Cp (M) = 0
unless M can be covered by a connected subgraph of size O(p), see Section 4.1. The number of such
subgraphs grows only exponentially with p, see Section 4.2. It implies that the number of non-zero
coefficients Cp (M) grows as n exp (O(p)), see Section 5.1.
    Naturally, one could run the algorithm from Theorem 3 to compute the truncated series for E(ǫ)
even if |ǫ| > ǫ0 . The running time will be polynomial in n and δ −1 as long as |ǫ| is smaller than the


Original LF lines 226-246:
                                                       5
 law or to decide whether the ground state can be well approximated using the PEPS ansatz, see
Ref. [12].
   The Kirkwood-Thomas ansatz is not well suited for computing spin-spin correlation functions
because it provides an unnormalized ground state. We avoid this problem using the standard relation
between the correlation functions and the linear response of the ground state energy to a small
perturbation. It allows us to prove

Theorem 4. Let Ou,v be a Hermitian operator acting non-trivially only on qubits u, v ∈ L. Suppose
kOu,v k ≤ 1. The expectation value of Ou,v on the ground state of H(ǫ) can be computed with a
precision δ in a time T = poly(δ −1) as long as |ǫ| ≤ ǫ0 /2(d + 1).

Remark: After the present work has been completed, it was communicated to us by F. Verstraete [13]
that the simulation algorithm based on the Kirkwood-Thomas ansatz is closely related to the coupled
cluster method originally introduced by Coester [14]. The coupled cluster method is extensively used
for numerical simulations in quantum chemistry, see a review [15], as well as in condensed matter
physics, see a review [16] and the references therein. Accordingly, from the perspective of practical
simulations, the algorithm described in the present paper is certainly not a new one. However, we
believe that our results provide the first rigorous proof that the coupled cluster method yields a
polynomial-time simulation algorithm for spin Hamiltonians with weak interactions.
    The rest of the paper is organized as follows. Section 2 provides the necessary background on


Original LF lines 260-324:
                                                                                  Q with the identity
on all other qubits. For any non-empty subset of vertices M ⊆ L denote a†M = u∈M a†u . Note that
the operators a†M are nilpotent, (a†M )2 = 0, and that they pairwise commute: a†M a†K = a†K a†M . Also,
one can easily check that the operators {a†M }, ∅ 6= M ⊆ L are linearly independent. (All these
definitions and properties apply to a and aM operators as well).

Definition 1. A creation operator is an operator that can be written as
                                            X
                                      C=          C(M) a†M
                                             ∅6=M ⊆L


for some complex numbers C(M).


                                                  6
    For any given creation operator C the coefficients C(M) are uniquely defined by C(M) =
hΩ|aM C|Ωi.
Claim 1. Any state |ψi satisfying hΩ|ψi = 1 can be uniquely written as |ψi = exp(−C) |Ωi for some
creation operator C.
   Remark: the exponent above is defined by its Taylor series. The nilpotence of operators a†M
implies that C k = 0 for any k greater than the number of qubits n = |L|, so the Taylor series can be
truncated at k = n.
Proof: Clearly, thePstates {a†M |Ωi}, M ⊆ L, constitute the orthonormal basis of the n-qubit Hilbert
space. Let |ψi = M ⊆L ψ(M)a†M |Ωi. Equation |ψi = exp (−C) |Ωi is equivalent to a system of
equations
                                  |M |
                                  X    (−1)k       X
  ψ(∅) = 1,   C(M) = −ψ(M) +                                   C(M1 ) · · · C(Mk ),   M ⊆ L,   M 6= ∅.    (7)
                                  k=2
                                        k!     M =M1 ∪...∪Mk

Here the second summation is over all partitions of M into k disjoint non-empty sets M1 , . . . , Mk .
Suppose we have already found all coefficients C(M) with |M| ≤ p. Then Eq. (7) assigns a unique
value to all coefficients C(M) with |M| = p + 1. Thus the system Eq. (7) has a unique solution.

2.2    Ansatz for the ground state
Our goal is to find an eigenvector |ψi satisfying H(ǫ) |ψi = E(ǫ) |ψi, where E(ǫ) is the smallest
eigenvalue of H(ǫ). We shall use the following ansatz for |ψi (we don’t care about the normalization):
                                                           X
                            |ψi = exp (−C) |Ωi, C =             C(M) a†M .                         (8)
                                                             ∅6=M ⊆L

Claim 1 asserts that the ground state can be represented in this form unless it is orthogonal to |Ωi.
Since we don’t require |ψi to be a normalized state, the ansatz Eq. (8) is meaningful only if C is a
bounded operator. We shall define a norm of a creation operator as
                                                  X
                                     kCk1 = max       |C(M)|.                                     (9)
                                                u∈L
                                                      M ∋u

Thus the ansatz Eq. (8) must be supplemented by a requirement that C is a creation operator with a
finite norm kCk1 . Of course, it may happen that H has several eigenvectors of the form Eq. (8). One
has to invoke some extra arguments to select an eigenvector corresponding to the smallest eigenvalue,
see subsection 2.4.
    TheN“physical meaning” of the norm kCk1 can be illustrated by considering a product         state:
|ψi = u∈L |ψu i, where |ψu i = |0i + αu |1i. Obviously, |ψi = exp (−C) |Ωi with C = − u∈L αu a†u .
                                                                                         P
Accordingly, kCk1 = maxu∈L |αu |. Thus one can think about kCk1 as a density of quantum fluctua-
tions.
    Using the identity exp (C) exp (−C) = I valid for arbitrary operator C, see [20], one can rewrite
the Schrödinger equation H(ǫ) |ψi = E(ǫ) |ψi as

                           exp (Ĉ)(H0 )|Ωi + ǫ exp (Ĉ)(V )|Ωi = E(ǫ) |Ωi.                              (10)



Original LF lines 575-604:
Of course, formal power series do not represent an actual solution of the Kirkwood-Thomas equations
unless we prove their convergence.

3.2    Convergence of C-series
We would like to prove that the series C = ∞              p
                                                P
                                                  p=1 Cp ǫ are convergent with respect to the norm
Eq. (9) with a non-zero convergence radius. We shall need to get a lower bound on the convergence
radius in terms of ∆, d, and J. Clearly, it is enough to analyze convergence of the series
                                                  ∞
                                                  X
                                        χ(ǫ) =          χp ǫp ,         χp = kCp k1 .                                (30)
                                                  p=1

Note that kCk1 ≤ χ(|ǫ|).
                                  P∞        p
Lemma 5. The series χ(ǫ) =          p=1 χp ǫ converges absolutely for

                                                    2−17 ∆
                                                 |ǫ| ≤ 2ǫ0 =
                                                           .                                                         (31)
                                                      dJ
Besides, for any ǫ as above one has the following bounds:
                                                                    2−15
                                |χ(ǫ)| ≤ 2−15 ,         χp ≤                      for p ≥ 1.                         (32)
                                                                   (2ǫ0 )p

                                                              12
    Proof: Let us first get an upper bound on kC1 k1 . From Eq. (27) it clear that C1 (M) = 0 unless
M ⊆ {u, v} for some


Original LF lines 780-835:

Summarizing, we have proved Theorems 1,2.


4     Linked cluster theorems
Throughout this section we shall use a term linked cluster which refers to a subset of vertices inducing
a connected subgraph of G. More formally,
Definition 2. A subset M ⊆ L is called a linked cluster iff for any u, v ∈ M there exists a sequence
of vertices u0 , u1, . . . , ut ∈ M such that u0 = u, ut = v and (uj , uj+1) ∈ E for all j = 0, . . . , t − 1.
Definition 3. A connected size of a subset M ⊆ L is the minimal size of a linked cluster that
contains all vertices of M. We shall denote a connected size of M as |M|c .

4.1    Linked cluster expansion for the ground state
                            P∞           p
Lemma 7. Let C(M) =           p=1 Cp (M)ǫ be the solution of the Kirkwood-Thomas equations obtained
in Section 3. Then
                                    Cp (M) = 0 unless |M|c ≤ p + 1.                                      (47)
   Proof: We shall prove the lemma by induction in p. From Eq. (27) one infers that C1 (M) = 0
unless M ⊆ {u, v} for some edge (u, v) ∈ E. In particular, C1 (M) = 0 unless |M|c ≤ 2. It proves
the statement of the lemma for p = 1. Suppose the statement is proved for p = 1, . . . , q − 1. From
Eq. (28) one infers that Cq (M) is a linear combination of terms like

                          x = Cp1 (M1 ) · · · Cpk (Mk )hΩ|aM â†M1 · · · â†Mk (Vu,v )|Ωi,               (48)

where p1 + . . . + pk = q − 1. Let us figure out under what circumstances the matrix element in
Eq. (48) can be non-zero.
Claim 3. Let M, M1 , . . . , Mk ⊆ L be non-empty sets, N = M1 ∪ . . . ∪ Mk , (u, v) ∈ E. Denote

                                      y = hΩ|aM â†M1 · · · â†Mk (Vu,v )|Ωi.

Then y = 0 unless the following conditions are met:
(i) Each set M1 , . . . , Mk contains at least one of the vertices u, v.
(ii) N\{u, v} ⊆ M ⊆ N ∪ {u, v}.

                                                         16
     Remark: this claim is true even for M = ∅ if one adopts a convention a∅ = I.
Proof: Suppose some set Mj contains neither u nor v. Then a†Mj commutes with Vu,v as well as with
all operators a†Mi for i 6= j. Thus y = 0. Suppose condition N\{u, v} ⊆ M is violated. Then there
exists a set Mj and a vertex w ∈ Mj such that w 6= u, v and w ∈     / M. Thus a†Mj contains a factor a†w
which commutes with all other operators involved in y. By moving a†w leftwards one can show that
each of 2k terms in y starts from hΩ|a†w , that is, y = 0. Suppose condition M ⊆ N ∪{u, v} is violated,
that is, there exists a vertex w ∈ M such that w ∈    / N and w 6= u, v. Then the operator aM contains
a factor aw which commutes with all other operators involved in y. By moving aw rightwards one
can show that each of 2k terms in y tails with aw |Ωi, that is, y = 0.



Returning to Eq. (48) we conclude that x = 0 unless each set Mj contains either u or/and v, and
M ⊆ N ∪ {u, v}. Let M̃j be a linked cluster of minimal size containing Mj , that is, |Mj |c = |M̃j |.
Let Ñ = M̃1 ∪ . . . ∪ M̃k and C = Ñ ∪ {u} ∪ {v}. Then C is a linked cluster and M ⊆ C. Note that
                                           k
                                           X                        k
                                                                    X
                                   |C| ≤         |M̃j | + 2 − k =         |Mj |c + 2 − k
                                           j=1                      j=1



Original LF lines 1003-1100:


5     Computational algorithms
In this section we describe an algorithm that takes as input a description of the Hamiltonians H0 , V
and an integer p. TheP algorithm    returns a list of coefficients E1 , . . . , Ep in the series for the ground
state energy E(ǫ) = ∞      E
                        p=1 p  ǫp
                                  . The running time of the algorithm is n exp (O(p)). In Section 5.3 we
describe a generalization of the algorithm that allows one to compute spin-spin correlation functions.

5.1    Computing the coefficients Cp (M)
The first part of the algorithm is to compute the coefficients Cq (M), ∅ 6= M ⊆ L sequentially for
q = 1, . . . , p using the solution of the Kirkwood-Thomas equations, see Eqs. (27,28). This gives an
approximate description of the ground state.
    We shall store triples (M, q, Cq (M)) in n bins (memory registers) Bu labeled by vertices of the
graph u ∈ L. Once a coefficient Cq (M) is computed, the triple (M, q, Cq (M)) is placed into every
bin Bu for which u ∈ M. From Lemma 7 we learn that Cq (M) = 0 unless M is a subset of some
linked cluster M̃ of size at most q + 1. According to Lemma 8, the number of linked clusters M̃
of size q + 1 containing vertex u is bounded by exp (O(q)), where the coefficient in the exponent
depends only on d. Each linked cluster of size q + 1 containing vertex u has 2q subsets containing


                                                      20
 vertex u. Thus we can bound the number of entries P  in the bin Bu at the moment when all coefficients
C1 (M), . . . , Cp (M) have been computed as |Bu | ≤ pq=1 2q exp (O(q)) = exp (O(p)).
    Suppose we have already computed all non-zero coefficients C1 (M), . . . , Cq−1 (M), M ⊆ L. The
next step is to compute coefficients Cq (M) for all sets M ⊆ L satisfying the condition of Lemma 7,
that is |M|c ≤ q + 1. Expanding Eq. (28) one gets
                           4
                   −1
                         X X 1                 X             X
Cq (M) = E0 (M)                                                      Cp1 (M1 ) · · · Cpk (Mk ) hΩ|aM âM1 · · · âMk (Vu,v )|Ωi.
                                      k! p +...+p =q−1 M ,...,M ⊆L
                        (u,v)∈E k=1        1    k        1     k

                                                                                              (57)
Note that the right hand side of this equation involves only coefficients Cpj (Mj ) that have been
already computed. For simplicity let us assume that computation of any term in Eq. (57) requires
one unit of time4 . Denote
                                 x = hΩ|aM â†M1 · · · â†Mk (Vu,v )|Ωi.                      (58)
Recall, see Claim 3, that x = 0 unless the following conditions are met:
(i) Each set M1 , . . . , Mk contains at least one of the vertices u, v.
(ii) N\{u, v} ⊆ M ⊆ N ∪ {u, v}, where N = M1 ∪ . . . ∪ Mk .
The property (i) implies that for a fixed edge (u, v) we can restrict the three rightmost sums in
Eq. (57) by taking triples (Mj , pj , Cpj (Mj )) either from the bin Bu or from the bin Bv . Therefore for
a fixed (u, v), the overall number of non-zero terms in the three rightmost sums in Eq. (57) can be
bounded by (|Bu | + |Bv |)k ≤ (|Bu | + |Bv |)4 = exp (O(q)).
     We shall now prove that only a small number of edges (u, v) can give a non-zero contribution to
Cq (M). Indeed, there are two cases: (1) M ⊆ {u, v}; (2) There exists w ∈ M such that w ∈        / {u, v}.
Clearly only O(1) edges (u, v) can lead to the case (1), so let us focus on the case (2). Consider
any term x as in Eq. (58). Properties (i),(ii) above imply that x = 0 unless there exists a set Mj
such that w ∈ Mj and one of the vertices u, v belongs to Mj . Without loss of generality, w, u ∈ Mj .
Lemma 7 implies that Cpj (Mj ) = 0 unless |Mj |c ≤ pj + 1 ≤ q. Therefore the distance between u
and w is at most q. Taking into account that |M| ≤ |M|c ≤ q + 1, we can bound the number of
edges (u, v) that can give a non-zero contribution to Cq (M) by |M|dq+1 ≤ (q + 1)dq+1 = exp (O(q)).
Summarizing, the overall number of non-zero terms in Eq. (57) is exp (O(q)).
     In order to compute all non-zero coefficients Cq (M) we will have to repeat the procedure above
for each subset M satisfying the condition of Lemma 7, that is |M|c ≤ q + 1. By Lemma 8, the
number of such sets is n exp (O(q)). Summarizing, the overall time one needs to compute all the
coefficients C1 (M), . . . , Cp (M) is n exp (O(p)).

5.2    Computing the ground state energy
The final step of the algorithm is to compute the coefficients E1 , . . . , Ep using Eq. (29). This equation
can be expanded as
                4
              X X 1               X                 X
      Ep =                                                Cp1 (M1 ) · · · Cpk (Mk )hΩ|âM1 · · · âMk (Vu,v )|Ωi.        (59)
                           k! p +...+p =p−1 M ,...,M ⊆L
             (u,v)∈E k=1      1        k       1     k

  4
     This assumption might seem unjustified, because the precision up to which the coefficient Cq (M ) must be
computed depends upon δ. However, taking into account these subtleties will lead to an additional overhead
poly(log n, log δ −1 ) which can be neglected since the algorithm has running time poly(n, δ −1 ).

                                                             21
 Expanding the commutators in the matrix element one gets 2k terms. However, only the term in
which Vu,v is the leftmost operator gives a non-zero contribution. Thus

                         hΩ|âM1 · · · âMk (Vu,v )|Ωi = (−1)k hΩ|Vu,v a†Mk · · · a†M1 |Ωi.

In particular, we can restrict the summation over M1 , . . . , Mk by subsets of {u, v} only. There are
only 3 such subsets: {u}, {v}, and {u, v}. This observation implies that the number of terms in the
rightmost sum in Eq. (59) is O(1). Since there are O(p3 ) partitions p1 + . . . + pk = p − 1, k ≤ 4, the
overall number of terms in Eq. (59) is O(np3 ).
    Combining the results of Subsections 5.1,5.2 we conclude that the overall time needed to compute
the coefficients E1 , . . . , Ep scales as n exp (O(p)). In the above analysis we did not keep track of the
coefficients in the exponents O(p). If one computes the exact coefficient, it yields the overall running
time n215+6 log (d) , where log stands for the base two logarithm. Accordingly, the running time as a
function of n and δ scales as
                                           T (n, δ) ∼ n(nδ −1 )15+6 log (d) .
For example, implementing the algorithm on a 2D square lattice (d = 4) would require a running
time T (n, δ) ∼ n(nδ −1 )27 , which is certainly not practical. Note however, that the power of nδ −1
depends upon the ratio |ǫ|/R, where R is the convergence radius of the series Eq. (4). The power
15 + 6 log (d) corresponds to the most pessimistic scenario R = 2ǫ0 (the best lower bound on the
convergence radius that we can prove) and |ǫ| = ǫ0 .

5.3    Computing spin-spin correlation functions


SOURCE research/audits/sources/dissipative_selection/weak_classical.txt; url=https://arxiv.org/pdf/2601.21140; SHA256=5469fc02a6ee1364d3ed7cddc742aeb3a32d66547c7b5c1602548a2f481b6173


Original LF lines 124-138:
                                                               Theorem 1. Fix ∆, r ∈ Z≥2 and β > 0. Let G = (V, E)
                                                               be a multihypergraph of maximum degree at most ∆ and
           D.    Abstract Cluster Expansion                    rank at most r, and let λ be a complex number such that

                                                                                              e−2rβ
   We now define the abstract cluster expansion [15, 22].                            |λ| ≤               .
Let Γ be a non-empty ordered tuple of polymers. The                                          e4 β∆ 2r
incompatibility graph HΓ is the graph whose vertex set
is Γ and has an edge between vertices γ and γ ′ if and         Then the cluster expansion for log(ZG (β, λ)) converges
only if they are incompatible. Γ is called a cluster if its    absolutely, ZG (β, λ) ̸= 0, and there is a fully polynomial-
incompatibility graph HΓ is connected. Let GC denote           time approximation scheme for ZG (β, λ).
the set of all clusters of polymers from C. The abstract       Remark. Theorem 1 extends naturally to fermionic sys-
cluster expansion is a formal power series for log(Z(C, w))    tems where the non-interacting Hamiltonian is on-site.
in the variables wγ , defined by
                             X          Y                         We prove Theorem 1 by verifying that the conditions


Original LF lines 155-196:
                                                                      a standard reduction from approximate sampling to ap-
                                                                      proximate counting of marginal probabilities. Our result
where                                                                 is formalised in the following theorem.
                                h                             i
                              Tr e−β ( v∈V (γ) Φv +λ e∈T Ψe )         Theorem 5. Fix ∆, r ∈ Z≥2 and β > 0. Let G = (V, E)
                                      P             P
         X
wγ :=         (−1)|E(γ)\T |                                       .   be a multihypergraph of maximum degree at most ∆ and
                                            Zγ (β, 0)                 rank at most r, and let λ be a real number such that
        T ⊆E(γ)
                                                                                                      e−2rβ
  We prove Lemma 2 in Appendix A.                                                            |λ| ≤             .
                                                                                                     e4 β∆ 2r
Lemma 3. Fix ∆, r ∈ Z≥2 and β > 0. Let G = (V, E)
be a multihypergraph of maximum degree at most ∆ and                  Then there is an efficient approximate sampling scheme
rank at most r, and let λ be a complex number such that               for the thermal distribution µρG (β,λ) over the classical
                                                                      spin space [d]V .
                                 e−2rβ
                       |λ| ≤             .                            Remark. Theorem 5 extends naturally to fermionic sys-
                                e4 β∆ 2r                              tems where the non-interacting Hamiltonian is on-site.
Then, for all polymers γ ∈ C, the weight wγ satisfies                    To prove Theorem 5, we use the following lemma, which
                                                                      is standard in the theory of approximate counting and
                                           !∥γ∥                       sampling. It shows that the existence of a fully polynomial-
                                   1
                   |wγ | ≤                        .                   time approximation scheme for marginal probabilities
                                e3 ∆ 2r
                                        
                                                                      implies an efficient approximate sampling scheme for the
                                                                      distribution. We note that more general results are known
  We prove Lemma 3 in Appendix B.
                                                                      for self-reducible problems [23, 24].
Lemma 4. The weight wγ of a polymer γ can be computed                 Lemma 6. Let n ∈ N and d ∈ Z≥2 be integers, and let µ
in time exp(O(∥γ∥)).                                                  be a probability distribution over [d]n . If there exists a fully
Proof. The sum is over all subsets T of E(γ), of which                polynomial-time approximation   S scheme for the marginal
there are 2∥γ∥ . For each of these subsets T , the trace may          probabilities µ(x) for all x ∈ S⊆[n] [d]S , then there is an
be evaluated in time exp(O(∥γ∥)) by diagonalising the                 efficient approximate sampling scheme for µ.
sum of interactions and the partition function may be eval-             We prove Lemma 6 in Appendix C. We now prove
                   O(1)
uated in time ∥γ∥       by a straightforward factorisation            Theorem 5.
argument.                                                 ■
                                                                      Proof of Theorem 5. By Theorem 1, there is a fully
  We now prove Theorem 1.                                             polynomial-time approximation scheme for ZG (β, λ),


Original LF lines 223-238:

         V.   CONCLUSION & OUTLOOK                                 algorithms [26, 27]. We note that efficient algorithms
                                                                   with a bound on the perturbation parameter that is inde-
                                                                   pendent of temperature can be obtained under additional
  We have established efficient algorithms for weakly-             assumptions by applying the framework of Ref. [13].
interacting quantum spin systems at arbitrary tempera-
ture. We obtained a fully polynomial-time approximation
scheme for the partition function and an efficient approx-                           ACKNOWLEDGEMENTS
imate sampling scheme for the thermal distribution over
a classical spin space.                                              We thank Samuel Scalet for helpful discussions. RLM
                                                                   was supported by the ARC Centre of Excellence for
   It would be interesting to extend these methods to              Quantum Computation and Communication Technol-
local perturbations of free-fermionic Hamiltonians, where          ogy (CQC2T), project number CE170100012. GW was
efficient algorithms are known via the cumulant expan-             supported by a scholarship from the Sydney Quantum
sion [17]. It would also be interesting to obtain efficient        Academy and supported by the ARC Centre of Excel-
algorithms with runtime polynomial in |V | and log(1/ϵ),           lence for Quantum Computation and Communication


Original LF lines 365-407:
                                           Appendix C: Proof of Lemma 6

                                                                                                        n
Lemma 6 (restatement). Let n ∈ N and d ∈ Z≥2 be integers, and let µ be a probability distribution over
                                                                                                   S [d] . SIf there
exists a fully polynomial-time approximation scheme for the marginal probabilities µ(x) for all x ∈ S⊆[n] [d] , then
there is an efficient approximate sampling scheme for µ.
Proof. We construct an efficient approximate sampling scheme by applying the chain rule for conditional probabilities.
For a sequence x = (xi )ni=1 , we sample each xi ∈ [d] conditioned on the previously sampled values x≺i := (xj )i−1
                                                                                                                 j=1 ,
using the conditional probability
                                                                          µ̂(x≺i xi )
                                              µ̂(xi | x≺i ) := P                         ,
                                                                         y∈[d] µ̂(x≺i y)
                                                                                                                                     6

where µ̂(x≺i xi ) is an approximation to µ(x≺i xi ). These approximations are obtained via the assumed fully polynomial-
time approximation scheme to within an error of ϵ/(3n). Then, for 0 < ϵ ≤ 1,
                                                                              ϵ
                                         |µ(xi | x≺i ) − µ̂(xi | x≺i )| ≤       µ(xi | x≺i ).
                                                                              n
Hence, we sample x ∈ [d]n with probability
                                                              n
                                                              Y
                                                    µ̂(x) =         µ̂(xi | x≺i ),
                                                              i=1

such that

                                                   |µ(x) − µ̂(x)| ≤ 2ϵµ(x).

Therefore, the total variation distance between µ and µ̂ is bounded by
                                                  1 X                     X
                                  ∥µ − µ̂∥TV =         |µ(x) − µ̂(x)| ≤ ϵ    µ(x) = ϵ.
                                                  2  n                     n
                                                    x∈[d]                            x∈[d]

This establishes an efficient approximate sampling scheme for µ, completing the proof.                                             ■




 [1] T. Helmuth, W. Perkins, and G. Regts, Probability The-           [14] R. L. Mann and R. M. Minko, PRX Quantum 5, 010305


SOURCE research/audits/sources/dissipative_selection/low_temperature.txt; url=https://arxiv.org/pdf/2201.06533; SHA256=a1bd1a2d5f69336418a84dff7dbc8fcfd59e67e368b74a658a22c643ff62cd68


Original LF lines 104-127:
overcome this difficulty.                                       Zνm denote the lattice graph Zν ×(Z/mZ). The graph Zν ×
   The arguments in Ref. [23] apply in a greater generality     (Z/mZ) is periodic in the final coordinate. A sequence
than those we consider. In particular, they do not re-          (Gn )n∈N of finite induced subgraphs of Zν converges to
strict their attention to the situation in which all ground     Zν in the sense of van Hove if and only if
states are stable, and they also consider expansions for           1. (V (Gn ))n∈N is an increasing sequence of subsets,
correlation functions. We have restricted our focus to al-
                                                                   2. n∈N V (Gn ) = Zν ,
                                                                      S
gorithms for computing the partition function to simplify
the presentation as much as possible. In the stable setting,
efficient classical simulation of correlation functions could                |∂ in Gn |
                                                                   3. limn→∞ |V (Gn )| = 0.
be obtained with the methods of this paper. An exten-
sion of our methods to allow for non-stable ground states
(i.e., the full low-temperature phase diagram) should also                    B.   Quantum Spin Systems
be feasible; such an extension has been achieved in the
classical setting of the Potts model [17, 26]. We leave            A quantum spin system is formally modelled on the
such an extension, which carries an increase in combinato-      lattice graph Zν with ν ≥ 2. At each vertex v of Zν there
rial complexity, to future work. Other interesting future       is a d-dimensional Hilbert space Hv with
directions include extensions to hypergraph interactions,                                               N d < ∞. The
                                                                Hilbert space on Zν is given by H := v∈V (Zν ) Hv . In
and to analysing boundary conditions other than the pure
                                                                the sequel, we only consider systems on finite induced
boundary conditions treated in this paper.


Original LF lines 140-188:
                                                                                                                             3

function Z(β, λ) at inverse    temperature β > 0, defined        all admissible sets of polymers from C. Then the abstract
by Z(β, λ) := Tr e−βH .
                           
                                                                 polymer partition function is defined by
   We assume that the Hamiltonian HΦ has                                                      XY
translation-invariant    interactions and is of the form                           Z(C, w) :=         wγ .
             P
 ⟨s|HΦ |s⟩ = v∈V (Zν ) Φs (v), where Φs (v) is a real                                          Γ∈G γ∈Γ
number that depends on s ∈ Ω only via the spins su
for which u ∈ N [v]. We assume that the Hamiltonian
HΦ has finitely many ground states Ξ with ground state                      E.   Abstract Cluster Expansion
energy e0 . We say that a vertex v ∈ V (Zν ) is in the
ground state g if the spin su coincides with the ground             Let Γ be a non-empty ordered tuple of polymers. The
state g for all u ∈ N [v]. Otherwise, we say the vertex          incompatibility graph HΓ of Γ is the graph with vertex
is excited. We further assume that Peierls’ condition            set Γ and edges between any two polymers if and only if
holds, that is, there exists a constant α0 > 0, such that        they are incompatible. Γ is called a cluster if its incom-
Φs (v) ≥ e0 + α0 for all excited vertices v ∈ V (Zν ) of all     patibility graph HΓ is connected. Let GC denote the set
configurations s ∈ Ω.                                            of all clusters of polymers from C. The abstract cluster
   We Passume that the Hamiltonian HΨ is of the form             expansion [27, 28] is a formal power series for log Z(C, w)
HΨ = e∈E(Zν ) Ψ(e), where Ψ(e) is a self-adjoint op-             in the variables wγ , defined by
                    N
erator on He := v∈e Hv . We further assume that                                               X          Y
∥Ψ(e)∥ ≤ 1 for every e ∈ E(Zν ), where ∥ · ∥ denotes the                     log(Z(C, w)) :=      φ(HΓ )     wγ ,
operator norm. Note that this is always possible by a                                         Γ∈GC             γ∈Γ

rescaling of λ.
                                                                 where φ(H) denotes the Ursell function of a graph H:
   Let G = (V, E) be a finite subgraph   of Zν . The Hilbert
                                  N                g     g
space on G is given by HG := v∈V Hv . Let HG          , HG,Φ ,                              1        X
       g                                                                     φ(H) :=                       (−1)|E| .
and HG,Ψ denote the Hamiltonians HG , HG,Φ , and HG,Ψ                                   |V (H)|!
                                                                                                   E⊆E(H)
on HG with boundary conditions g ∈ Ξ on N (V ). This                                               spanning
               g
means that HG    is the operator on HG defined by the par-                                         connected
tial expectation value sN (V ) HZν [N [V ]] sN (V ) , where
the spin configuration sN (V ) coincides with the ground
                                      g          g                                 F.    Contour Models
state g on N (V ), and similarly for HG,Φ and HG,Ψ   . We de-
                              g
fine the partition function ZG (β, λ) on HG with boundary
                               g
                                                   h      g
                                                           i        We now introduce contour models which formalise the
conditions g ∈ Ξ on N (V ) by ZG  (β, λ) := TrHG e−βHG .         idea that spin systems have a geometric interpretation.
We assume that all ground states Ξ are stable and define         For a detailed overview of contour models, we refer the


Original LF lines 350-383:
β ≥ β ⋆ , and all |λ| ≤ λ⋆ , the cluster expansion for            Tn (ZG (β, λ)) can be approximated up to an additive ϵ-
     g                                 g
log(ZG (β, λ)) converges absolutely, ZG  (β, λ) ̸= 0, and for     error in time exp(O(n)) · |V (G)|
                                                                                                      O(1)
                                                                                                           · (1/ϵ)O(1) .
     +
n∈Z ,
                                                                    We prove Lemma 14 in Appendix E. We now establish
             g                g
       |Tn (ZG (β, λ)) − log(ZG (β, λ))| ≤ |V |e−Ω(n) .           our main result.

   We prove Lemma 8 in Appendix C. This lemma im-                 Theorem 15. Let G be a finite induced subgraph of
plies that to obtain a multiplicative ϵ-approximation             Zν . There exists constants β ⋆ = β ⋆ (ν, d, Ξ, α0 ) and
to ZG g
        (β, λ), it is sufficient to approximate the               λ⋆ = λ⋆ (ν, d, Ξ, α0 ), such that, for all g ∈ Ξ, all β ≥ β ⋆ ,
truncated cluster expansion Tn (ZG  g
                                      (β, λ)) to order            and all |λ| ≤ λ⋆ , there is a fully polynomial-time approx-
                                                                                                                   g
n = O(log(|V (G)|/ϵ)).                                            imation scheme for the partition function ZG       (β, λ) of a
                                                                  stable quantum perturbation of a classical spin system.
                                                                  Proof. Combining Lemma 8 and Lemma 14 gives a fully
       V.   APPROXIMATION ALGORITHM
                                                                  polynomial-time approximation scheme for the partition
                                                                            g
                                                                  function ZG (β, λ) for all g ∈ Ξ, all β ≥ β ⋆ , and all
   In this section we shall establish our approximation algo-            ⋆
                                                                  |λ| ≤ λ .                                            ■
             g
rithm for ZG   (β, λ). Our algorithm is based on combining
                                   g
the cluster expansion for log(ZG     (β, λ)) with the algorith-
mic framework of Helmuth, Perkins, and Regts [14] and                       VI.   CONCLUSION & OUTLOOK
Borgs et al. [17]. In particular, we shall establish an effi-
cient algorithm for approximating the truncated cluster              We have established a polynomial-time approximation
