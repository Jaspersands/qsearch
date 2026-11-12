Primary source: Lutz et al., https://arxiv.org/pdf/2503.21741v3 ; accepted Quantum10,2032 (2026). PDF SHA256 998e88baf252eef7df682eaf771258adba37da14294d25bb02a2c08e20dfa456

Physical pdftotext lines 247-310:
completely specify an eigenstate. Using this set, we                sider the class of spin-1/2 XXX Richardson-Gaudin
                                                                                                     PN
construct the parent Hamiltonian                                    (RG) models [11, 46, 47] H RG = k=1 ωk Q(k) , where
                                   X
   HvXY (γ, h) = (Z − zv )2 +            (c†p cp − qv(p) )2 . (9)                           σkz
                                                                                                             N
                                                                                                 1 g X ⃗σk · ⃗σj − 1
                                  p∈Γzv                                       Q(k) =            + +                  .      (11)
                                                                                            2    2 4     ϵk − ϵ j
                                                                                                          j̸=k
Here zv is chosen as the desired parity of the state
to be prepared and the inclusion of the corresponding               Here, ωk and ϵk (with ϵk ̸= ϵj for k ̸= j) are arbitrary
first quadratic term serves the purpose of fixing the               parameters and g is the interaction strength. The
sector as previously described. Now, it is immedi-                  Hamiltonian commutes with the total magnetization
ate to see that the gap of this parent Hamiltonian is               M and with the operators Q(k) , which are mutually
δ(γ, h) = 1, as two different eigenvectors differ in at             commuting [Q(j) , Q(k) ] = 0 [11]. In fact, the opera-
least one mode occupation.                                          tors {Q(k) }N
                                                                                k=1 provide a complete set of conservation
   To proceed, we express c†p cp in terms of the original           laws, i.e. the set of their eigenvalues uniquely specify
spin degrees of freedom                                             an Hamiltonian eigenstate [33]. Setting ω1 = 1, ϵ1 = 0
                                                                    and ωi = 0, ϵi = −e(i−2)/N for i ̸= 1, we obtain the
             N              j−1                                     central-spin model, which is relevant in the study of
             X       e−ip(l−j) Y z
  c†p cp =                      σk                                  quantum dots like the nitrogen-vacancy defect in dia-
                        N                                           mond [11, 53]. In the RG models, each eigenstate |v⟩
             j,l=1          k=1
                                                                                                       (1)        (N )
        x T                                  l−1
                                           x Y                   is labeled by the vector q⃗v = (qv , . . . , qv )T where
        σj        1             ie2iθp      σl
                                                    σkz ,   (10)      (k)
                                                                    qv is the eigenvalue of the charge Q(k) associated
        σjy    −ie−2iθp           1          y
                                            σl
                                                 k=1                with |v⟩. The set of all possible vectors q⃗v coincides
                        γ sin(p)                                    with the set of solutions to the so-called quadratic
where tan(2θp ) = h−cos(p)       [18]. Eq. (10) makes it            Bethe equations
explicit that these charges consist of S = O(N 2 )
Pauli strings and the modulo of their coefficients is                                                    N
                                                                                        2             g X q (k) − q (j)
|bi | = O(1/N ). As the sum of squares of these terms,                              q (k) = q (k) −                     ,   (12)
                                                                                                      2      ϵk − ϵ j
the parent Hamiltonian thus has at most S = O(N 5 )                                                     j̸=k
with coefficients |bi | = O(1). In addition, the first and
                                                                    with the additional constraint k q (k) = M/2 + N/2.
                                                                                                      P
second derivatives of the parent-Hamiltonian matrix
elements with respect to γ and h are system-size in-                Eqs. (12) are equivalent to the traditional Bethe equa-
dependent, only diverging at the phase boundaries of                tions written in terms of the quasiparticle rapidi-
the XY model [1]. If the adiabatic paths are chosen to              ties [11]. At g = 0, the quadratic Bethe equations
                                                                                         2
linearly approach their final values inside the phase,              become trivial (q (k) = q (k) ) and {⃗qv }v coincides with
this will result in only a constant factor in the final             the set of binary vectors.
complexity dependent on how close the final γ, h val-                  For generic g, the solution to Eqs. (12) can be found
ues are to the phase boundary [1]. With the c†p cp as               numerically by the following procedure: starting from
above and since the qpv are constant over the adia-                 g = 0 and with a given binary vector, one iteratively
batic path, the parent Hamiltonian can be computed                  increases g by a small amount ∆g and solves Eqs. (12)
efficiently. In conclusion, we have verified that the               via a local optimization initialized with the solution
Hamiltonian (9) satisfies all the hypotheses of the adi-            of the previous step [15]. As an improvement, the
abatic theorem, implying that all eigenstates for h < 1             optimizer can also be initialized instead by computing
can be prepared efficiently. Similarly, when h > 1, one             a Taylor expansion at the previous solution, which


Accepted in Quantum 2026-03-09, click title to verify. Published under CC-BY 4.0.                                             4

Physical pdftotext lines 323-394:
                                                1.0012 ± 4 × 10 4
      g, v, v0              4
                                                1.0014 ± 3 × 10 4                                 ues [1], thus further corroborating an overall 1/N
                    10 1    2
                                                                                                  lower bound for all g.
                            0
                                                                                                     To our knowledge there is no rigorous result that
                                  4     6   8     10   12    14                                   guarantees or prohibits that Eqs. (12) can be solved
                                   3            4                   6                 12          classically in polynomial time, and no runtime guar-
                                                         System Size N                            antee for the numerical technique employed here.
                                                                                                  This problem is equivalent to establishing the com-
Figure 1: The RG quadratic Bethe equations are solved nu-                                         plexity of solving the Bethe equations as a more fun-
merically for all eigenstates while dynamically adapting ∆g,                                      damental question about the Bethe ansatz and is be-
the pairwise ∥ · ∥2 -distance is computed and minimized over                                      yond the scope of our work. A sufficient condition for
the adiabatic path g ∈ [0, 10] and all eigenstate pairs [1].                                      the efficiency of the employed technique is that the
This equals the minimal gap of HvRG along the adiabatic                                           ∆g required to remain in the local minima at any it-
path for all eigenstates v and is shown against system size.
                                                                                                  eration does not vanish exponentially with increasing
Inset shows deviations of the data point from the N −1 curve
shown in black; inset legend shows fitted exponents with
                                                                                                  system size and the system of linear equations stays
standard deviation error. It can be seen that this fits the gap                                   well-conditioned. While we are not able to provide
closing for all models.                                                                           conclusive evidence thereof as part of our numerics [1],
                                                                                                  the successful application of the algorithm here and in
                                                                                                  the numerical literature [9, 15, 26] provides evidence
reduces to solving linear systems of equations as for                                             that efficient computation is possible in practice for
the quadratic Bethe equations [15].                                                               at least many eigenstates. Thus we will take the effi-
  Given a target eigenstate |v⟩, we can follow                                                    cient computability of q⃗ as a key assumption for the
our protocol and construct the parent Hamiltonian                                                 protocol.
                              (k)                    (k)
HvRG (g) = ΣNk=1 (Q
                    (k)
                        (g)−qv (g))2 , where the qv (g)                                              In conjunction with the above, this implies the ex-
are computed classically as described. Note that the                                              istence of quantum circuits for the preparation of all
spectrum of HvRG can be expressed as the distance be-                                             eigenstates with polynomial depth in N .
tween the eigenvalue vectors HvRG |v ′ ⟩ = ||⃗qv − q⃗v′ ||22 .
  For the adiabatic path, we vary g after starting at
g = 0, where all the eigenstates are product states.
By the definition of Q(k) , HvRG (g) has support on S =                                           8 The XXZ Model
O(N 3 ) Pauli strings with coefficients scaling as |bi | =
O((g 2 + 1)/ mink,j |ϵk − ϵj |2 ), which for the central-                                         We conclude by discussing why our protocol does not
spin model gives |bi | = O(N ).                                                                   apply, as is, to the XXZ chain. The main bottleneck
  Next, we study the gap of HvRG (g). It is straight-                                             comes from the structure of the conserved charges.
forward to show that states in different magnetization                                            Indeed, it is known that the k-th charge of the XXZ
sectors (M, M ′ ) are separated by an O(1/N ) energy                                              model is written in terms of a number of Pauli strings
                                                                        2                         S = O(N 2k ) [23], thus growing exponentially in k.
                                        N
                                      1 X (k)   (k)                             (M − M ′ )2       In order to build the parent Hamiltonian HvXXZ for
        ∥⃗qv − q⃗v′ ∥22 ≥                 qv − qv′                          =               .
                                      N                                            4N             all eigenstates, however, we need to include O(N )
                                            k=1
                                                                                           (13)   charges, so that S would grow exponentially in system
                                                                                                  size N , implying an O(exp (N )) circuit depth.
Moreover, in the limit g → 0, the gap can be eval-                                                   A potential modification of our protocol would be
uated rigorously via standard perturbation theory:                                                to only include the first O(log(N )) charges in a par-
              mink,j |ϵk −ϵj |                                                                                                     XXZ, log(N )
when g < 2(2+          √
                         5)N 2
                               , we find that the gap is                                          ent Hamiltonian of the form Hv                = H XXZ +
                                                                                                  P⌊log(N  )⌋   (k)     (k)    2
O(1) [1]. Likewise, and with additional properties of                                                k=1      (Q (g)−qv (g)) . This way, however, only
the Gaudin magnet [20], in the limit g → ∞ we prove                                               O(poly(N )) eigenstates could be targeted, which are
minv,v′ ∥⃗qv − q⃗v′ ∥22 = 1/N [1]. For states within the                                          the lowest energy states in sectors with log(N ) fixed
same magnetization sector and away from the pertur-                                               charges. We note this has been considered from an en-
bative regimes, we were not able to rigorously bound                                              tanglement scaling perspective [2]. Making this con-
the scaling of the gap, however, we performed a nu-                                               struction precise, as well as trying to generalize the
merical analysis for different values of the parame-                                              method to prepare all eigenstates of the XXZ model,
ters εk with the technique described above [1]. The                                               are interesting directions for future research.


Accepted in Quantum 2026-03-09, click title to verify. Published under CC-BY 4.0.                                                                         5
9 Outlook                                                                309(5741):1704–1707, 2005. DOI: 10.1126/sci-

Physical pdftotext lines 1185-1295:
                                                                          14                                                                      10 2
                3 × 10 1
                              0         2       4         6    8        10     12           0         2       4         6           8   10   12                                                  0           2         4         6         8         10     12
                                                          g                                                             g                                                                                                        g
                   (c) Same data as Fig. S5a for Taylor expansion of first order, but shown against g. ∆g increases linearly for growing g.

Figure S5: Numerical behavior of quantities relevant to classical complexity of Richardson-Gaudin eigenvalue method: scaling
of iteration step size ∆g and condition number in case of Taylor expansion; for details see Sec. G.




                                               Central Spin                                           Constant Spacing: i = i                                                                              Random Uniform: i U(0, 1)
                1.0                                                                                       System Size N
                                                                                                             4         10
                                                                                                             6         12
                0.8                                                                                          8         14
                                                                                                               max| i        j|/N


min  qv qv 22
                                                                                                               min| i       j|/N
     0

                0.6

v, v            0.4
        0




                0.2


                        0.0       0.5        1.0         1.5   2.0       2.5           0          1           2              3          4                0.0                                         0.1         0.2       0.3       0.4       0.5        0.6
                                                     g                                                              g                                                                                                      g

Figure S6: HvRG smallest gap minimized over all v (not minimized over the adiabatic path) as a function of g. Black markers
show relevant orders for norms of interacting and non-interacting part of Q(k) ; see Sec. G for further details.




Accepted in Quantum 2026-03-09, click title to verify. Published under CC-BY 4.0.                                                                                                                                                                         16
                         q(1)                                    q(2)                                  q(3)                                      q(4)
 7.5
             IOM eigenvalues qv(k):
 5.0         not contributing to minimal gap
             contributing to minimal gap
 2.5
 0.0
                                                                                                                                           Orders of g for non-/
 2.5                                                                                                                                       interacting part of $Q^{(k)}
                                                                                                                                           max| i j|/N
 5.0                                                                                                                                       min| i j|/N

       0.0   0.5      1.0       1.5   2.0      2.5 0.0   0.5   1.0       1.5   2.0   2.5 0.0   0.5   1.0       1.5   2.0   2.5 0.0   0.5      1.0       1.5   2.0     2.5
                            g                                        g                                     g                                        g

Figure S7: IOM eigenvalues q⃗v (g) shown against g as an explicit example for small system size N = 4. Each line corresponds
to one eigenstate. Marked color corresponds to all eigenvectors, whose pairwise distances correspond to the overall minimum
of the parent Hamiltonian gap at the value of g.




Figure S8: Numerical results for bipartite von Neumann entanglement entropy of central-spin model for all eigenstates against
system size. The bipartition is between the N/2 more strongly and N/2 less strongly interacting sites; the central spin model
is taken at g = 1. Our numerical results do not allow us to support either a O(log(N )) of O(N ) scaling .




Accepted in Quantum 2026-03-09, click title to verify. Published under CC-BY 4.0.                                                                                     17
the central spin, constant spacing and random uniform choices of the ϵi . As we are interested in the minimal
gap of HvRG for all eigenstates v, the computation needs to be performed for all binary vectors as starting values.
To simultaneously find the maximal ∆g guaranteeing that the local solver does not leave the local minimum at
any iteration step, we adapt ∆g dynamically in the following way: (i) after any iteration, the pairwise distance
between all IOM eigenvalue vectors q⃗v and the error resulting from the local optimizer are computed. (ii) If the
former is too small (i.e. one eigenstate local minimum was left and the solver found the same solution twice),
or the latter is too large (i.e. the optimizer converged to a local minimum, which does not correspond to a
true solution of the quadratic Bethe equations) ∆g is multiplied with an adaption factor < 1. (iii) If the step
succeeds, we attempt to increase ∆g, by dividing by the adaption factor. Thus ∆g is adapted exponentially
quickly to correspond to the largest possible value of ∆g, at which the convergence radii of the local optimizer
around all solutions of the algebraic equations are never left. As an additional optimization, the initial vector
of the local optimizer can instead be chosen by computing the Taylor expansion at the previous vector to a
fixed order. As for the quadratic Bethe equations, the required derivatives reduce to linear sets of equations
[15]. Specifically, we choose an adaption factor of 0.9 and a maximal tolerance for the quadratic error in the
quadratic Bethe equations of 10−14 , while we Taylor expand to first order. To ensure the gap is sampled at
every point of the adiabatic path - as required for our proposed algorithm - we additionally set a fixed upper
threshold for the step size ∆g in some circumstances, as further explained below. This procedure results in the
O(1/N ) gap scaling data discussed in the main text Fig. 1 when minimizing over both the entire adiabatic path
as well as all pairs of eigenvectors. We will now discuss the numerical results in more detail and beyond both
these minimizations.

   Fig. S5a shows how the ∆g step resulting from the dynamical adaptation described above changes with system
size, when we take its minimum over the adiabatic path, both for the algorithm without Taylor expansion and
with Taylor expansion to first order. While the numerics are limited by system size, it can be seen that ∆g
in general does become small and even suggests a ∆g = O(1/ exp (N )) scaling for the case without Taylor
expansion. This appears to be alleviated in the case of Taylor expansion to first order. While the required
first derivative can be computed by inverting a linear system in this case, Fig. S5b suggests, however, that
the condition number (defined as the ratio of the largest and the smallest singular value) of the respective
linear system increases with N , which presents a potential challenge for this approach. Fig. S5c shows that ∆g
increases with g, thus being consistent with the O(log(g)) scaling reported in the literature [16] and suggesting
large g are no obstacle for the method. Overall, our numerical results do not allow us to conclude whether our
numerical method to solve for the IOM eigenvalues of the Richardson-Gaudin models is classically efficient; to
our knowledge no formal complexity result is known, while the method has been applied very successfully in the
literature. It is an interesting question for future research to study this behavior analytically and investigate
whether this complexity is optimal. The extensive literature on homotopy methods for the solution of algebraic
equations as well as certified bounds for Newton-type optimizers (c.f. Sec. H) might be relevant in this regard.

Physical pdftotext lines 1346-1390:
 H Smale’s α-theory
 With the quadratic Bethe equations available for the RG model, the question of the gap of the Hamiltonian
 becomes a question of the minimal geometric distance between any root vectors of this set of algebraic equations,
 as HPRG |v ′ ⟩ = ||⃗qv − q⃗v′ ||22 . This question has been considered in the mathematical literature, and different
 lower bounds are known. Importantly, the so-called Smale’s α-theory [7, Chs. 8-14], originally developed to
 give bounds on the convergence radius of Newtons algorithm around the root of a function, appears to be
 relevant. In fact, for an analytic function f : E → F mapping between Banach spaces E, F , for any two roots
 f (ζ) = f (ζ ′ ) = 0, ζ ̸= ζ ′ , one has the following Smale’s bound
                                                       √
                                              ′     5 − 17                  1
                                       ||ζ − ζ || ≥                  Df (ζ)−1 D k f (ζ)                     (SH.25)
                                                       4   supk≥2 ||                    ||1/(k−1)
                                                                            k!

 if the inverse of the Jacobi matrix Df (ζ) exists. For the class of RG models that were considered in the main
 text, the equations are all polynomials of degree 2. For these equations the supremum over k in Eq. SH.25
 drops out, as the Dk on such polynomials becomes zero for k > 2 and the tensors can be computed explicitly:
                                                            (                        PN
                                                              k = l : 2q (k) − 1 + g2 k̸=j ϵk −ϵ
                                                                                             1
                                              
                                              i ≤ N :                                           j

                    (Df (ζ))k,l = ∂k fl (ζ) =                 k ̸= l : − g2 ϵl −ϵ
                                                                               1
                                                                                 k
                                                                                                        (SH.26)
                                              
                                                i=N +1: 1
                                              
                                                    (
                       2                              k=l=m≤N : 2
                    (D f (ζ))k,l,m = ∂k ∂l fm (ζ) =                        .                            (SH.27)
                                                      else:            0

 Lower bounding the Smale bound via submultiplicativity and using that ||M −1 || = 1/σmin (M ), one arrives at
                                                    √
                                           ′     5 − 17 σmin (Df (ζ))
                                    ||ζ − ζ || ≥                       ,                              (SH.28)
                                                    2     ||D2 f (ζ)||

 where ||D2 f (ζ)|| = 2.
    At this point we note the similarity to the Gaudin determinant expression [10, 21, 30] and the connection to
 the condition number of the linear system occurring in the Taylor expansion for the eigenvalue based solution
 of the quadratic Bethe equations discussed in Sec. G.
