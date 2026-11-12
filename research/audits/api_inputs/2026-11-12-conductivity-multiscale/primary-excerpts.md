Mourrat, Efficient methods for estimation of homogenized coefficients.
https://arxiv.org/pdf/1609.06674
Retained text sha256 d52ee3985b531cbdd25e810c099d19e60aee63f36bb399fbbb464c8a21f3d49a
Parent checked actual text: Theorem1.2 uses IID media; general Markov identities survive but rates require (3.5) and (4.1). No rate imported for arbitrary circuits.

Physical newline lines 1-120:
                                                 EFFICIENT METHODS FOR THE ESTIMATION OF
                                                         HOMOGENIZED COEFFICIENTS

                                                                      JEAN-CHRISTOPHE MOURRAT

                                                  Abstract. The main goal of this paper is to define and study new meth-
                                                  ods for the computation of effective coefficients in the homogenization of




arXiv:1609.06674v3 [math.NA] 31 Oct 2017
                                                  divergence-form operators with random coefficients. The methods introduced
                                                  here are proved to have optimal computational complexity, and are shown
                                                  numerically to display small constant prefactors. In the spirit of multiscale
                                                  methods, the main idea is to rely on a progressive coarsening of the problem,
                                                  which we implement via a generalization of the Green-Kubo formula. The
                                                  technique can be applied more generally to compute the effective diffusivity
                                                  of any additive functional of a Markov process. In this broader context,
                                                  we also discuss the alternative possibility of using Monte-Carlo sampling,
                                                  and show how a simple one-step extrapolation can considerably improve the
                                                  performance of this alternative method.




                                                                             1. Introduction
                                              Let −∇ · a(x)∇ be a divergence-form operator with random coefficients. If
                                           the law of the matrix field (a(x)) is stationary and ergodic, then the operator
                                           homogenizes over large scales to an operator with constant, deterministic
                                           coefficients −∇ · a∇. The main goal of this paper is to explore numerical
                                           methods to estimate the homogenized matrix a. We can formalize this task as
                                           follows.
                                           Problem. Find an algorithm that, given δ > 0 and a realization of the random
                                           coefficient field (a(x)), outputs a matrix abδ such that
                                                                                         1
                                                                                   bδ |2 2 ⩽ δ.
                                                                              
                                           (1.1)                           E |a − a

                                              In (1.1), we chose to measure the quality of the approximation a   bδ in an L2
                                           sense for definiteness, but other choices (e.g. convergence in probability, or
                                           higher moments) are equally valid, and in fact would only marginally alter the
                                           results presented below. The point is that a  bδ should typically be within δ or
                                           less from a.
                                              Naturally, the real question is to find an efficient algorithm. We focus on a
                                           discrete-space setting, and assume throughout that the coefficients are uniformly
                                           elliptic, independent and identically distributed (i.i.d.). In order to measure
                                           computational effort, we use a slightly loosely defined notion of “elementary”
                                           operation: any memory access, boolean operation, floating point addition or

                                             Date: October 5, 2018.
                                             2010 Mathematics Subject Classification. 35B27.
                                             Key words and phrases. homogenization, multiscale methods.
                                                                                       1
 2                                         J.-C. MOURRAT

multiplication counts as one operation. We first give a lower bound on the
number of operations any algorithm must use.
Proposition 1.1 (Complexity lower bound). No algorithm can output an
              bδ of a in the sense of (1.1) within o(δ −2 ) operations.
approximation a
 The main method we propose to compute an approximation of a is as follows.
We fix ξ ∈ Rd of unit norm, set
                         v−1 (x) := (∇ · aξ)(x)             (x ∈ Zd ),
and for each k ∈ N, we let vk be the solution to
(1.2)               (2−k − ∇ · a∇)vk = 2−k vk−1                     on Zd .
(We refer to Section 8 for precise notation and assumptions.) Note that the
functions (vk )k⩾−1 depend on the coefficient field a, although we keep this
dependence implicit. For each r ⩾ 0, we write
                                 Br := {−brc, . . . , brc}d .
Theorem 1.2 (Efficient approximation of a). For each ε ∈ (0, d−1
                                                              2d
                                                                 ), there exists
a constant C < ∞ such that the following holds. Fix n ∈ N, and denote
                                      1
(1.3)                   rk := 2n−( 2 −ε)k         (k ∈ {0, . . . , n}),
                         n
                         X     1 X k
                bn2 :=                  2 vk−1 (x)vk (x) + vk2 (x) .
                                                                   
(1.4)           σ
                         k=0
                             |Brk | x∈B
                                            rk


We have
                         h                             2   i 21          dn
(1.5)               E                             bn2
                             ξ · aξ − E[ξ · aξ] + σ               ⩽ C2− 2 .

                       bn2 can be computed in at most Cn2dn operations.
Moreover, the quantity σ
   By the central limit theorem, the quantity E[ξ · aξ] can be computed at
precision δ > 0 in Cδ −2 operations. Hence, Theorem 1.2 gives us a method that
requires δ −2 log(δ −1 ) operations to compute an approximation of a at precision
δ > 0 in the sense of (1.1), essentially matching the lower bound given by
Proposition 1.1.
   For ε = 0, the statement of Theorem 1.2 remains valid provided that we
                                          dn
replace the right side of (1.5) by Cn2− 2 . I expect that the sharp upper bound
                    1    dn
in this case is Cn 2 2− 2 . Whatever may be, this additional multiplicative factor
          1
of n or n 2 does not degrade the bound much. For simplicity, it is the version
with ε = 0 that was implemented numerically.
   The proof of Theorem 1.2 relies in particular on the assumption that the law
of the coefficient field P is invariant under the action of Zd . If this assumption
is weakened and the law is only assumed to be invariant under the action of a
sublattice of Zd which may be unknown to us a priori, then one can use masks
in the spatial averages over Brk appearing in (1.4) in order to avoid boundary
layer effects. When weakening the independence assumption on the coefficients,
I expect Theorem 1.2 to remain unchanged provided that the field x 7→ a(x) is
      EFFICIENT METHODS FOR ESTIMATION OF HOMOGENIZED COEFFICIENTS                 3

sufficiently uncorrelated for partial sums over boxes to satisfy a central limit
theorem.
   The power of the method presented in Theorem 1.2 comes from the fact that
the domain of interest shrinks rapidly as k increases. Moreover, when k is of

Physical newline lines 263-367:
tive diffusivity of general additive functionals of a Markov process. Let (X(t))t⩾0
be a Feller process taking values in a metric space X , and denote the associated
family of probability laws by (Px )x∈X , with corresponding expectations (Ex )x∈X .
We assume that there exists a probability measure P on X (with corresponding
expectation E) such that the process (Xt ) is reversible and ergodic with respect
                                         5
 6                                J.-C. MOURRAT

to P; we denote the law of (X(t)) started from the measure P by PP (with
corresponding expectation EP ). The assumption of reversibility will be dropped
shortly, and is only meant to facilitate the exposition here. Given f ∈ L2 (P) of
mean zero, one can check using reversibility that the limit
                               "       ˆ t              2 #
               2                    1
(2.1)        σ (f ) := lim EP      √       f (X(s)) ds      ∈ [0, +∞]
                      t→+∞           t 0
always exists. Denote by L the (non-negative) infinitesimal generator of (X(t)),
and hf, gi := E[f g]. An equivalent characterization of σ 2 (f ) is given by
(2.2)            σ 2 (f ) = 2 f, L−1 f := 2 lim f, (λ + L)−1 f .
                                           λ→0

Kipnis and Varadhan [39] showed that the condition σ 2 (f ) < ∞ implies that
the additive functional
                                      ˆ t
                                   1
(2.3)                             √       f (X(s)) ds
                                     t 0
converges in law under PP to a centered Gaussian random variable of vari-
ance σ 2 (f ) as t tends to infinity.
   Our goal is to discuss practical ways to compute σ 2 (f ). There are two
standard methods to address this question (see for instance [22]). The first one
uses the formula (2.1) as the basis for a Markov chain Monte-Carlo (MCMC)
algorithm. The second method dispenses with the simulation of the Markov
chain, and uses the formula (2.2) instead. The problem then becomes that of
computing an approximation of L−1 f , and computing the average.
   We study MCMC methods in Section 4. The main contribution of this section
is to show that a one-step extrapolation of the naive MCMC algorithm yields
significant improvement of the approximation in most cases.
   We then explore methods based on the formula (2.2). Similarly to multiscale
methods, we aim to split the computational effort involved in the computation
of L−1 f into a hierarchy of scales. A good starting point for witnessing this
multiscale decomposition is the Green-Kubo formula, which in our present
context is a direct consequence of (2.2) and reads
                       ˆ +∞                     ˆ +∞
              2                   −tL
(2.4)       σ (f ) = 2        f, e f dt = 2           EP [f (X(0))f (X(t))] dt.
                      0                       0
We think of the part of the integral with t . 1 as carrying the small-scale
information of the process, while the part with t   1 carries the larger-scale
information. The first, very elementary but crucial, modification to (2.4) we
then bring forward is that, by reversibility,
                                      D t          t
                                                         E
(2.5)                     f, e−tL f = e− 2 L f, e− 2 L f
so that, after a change of variables,
                                  ˆ +∞
(2.6)                   2
                       σ (f ) = 4      e−tL f, e−tL f dt.
                                   0

The point of this simple modification is that in order to compute E[(e−tL f )2 ],
we need to average over samples of (e−tL f )2 , and for large t > 0, each of these
     EFFICIENT METHODS FOR ESTIMATION OF HOMOGENIZED COEFFICIENTS                7

samples will be much smaller than realizations of f e−tL f (by a square factor).
For large t > 0, we thus need much fewer samples to compute the average
on the right side of (2.5) than we do to compute the average on the left side
of (2.5). This is relevant for practical computations since it is usually more
difficult to compute samples of e−tL f when t is large. In other words, we
decomposed the problem of computing σ 2 (f ) into a small-scale part (t . 1)
which has a contribution of order one and is an average over many samples that
are relatively easy to compute, and a large-scale part (t   1) which refines the
estimate, is computationally more demanding, but requires much fewer samples
due to the own smallness of each of these samples. This is what will ultimately
allow for the rapid shrinking of the domain of interest in (1.4) as k increases.
   The second modification to the Green-Kubo formula we consider is meant to
replace the integral over time by a sum over a moderate number of terms. The
starting point is the resolvent formula, which states that for every λ, µ > 0,
(2.7)         Rλ = Rµ + (µ − λ)Rλ Rµ ,          where Rλ := (λ + L)−1 .
For any given sequence (µk )k∈N of real numbers in (0, 1], we thus apply (2.7)
recursively and obtain, at least formally,
                               +∞
                               X
(2.8)                   R0 =         µ0 · · · µk−1 Rµ0 · · · Rµk .
                               k=0

As will be explained in more details below (see Theorem 5.1), defining recursively
                 f−1 := f    and ∀k ∈ N,            fk := µk Rµk fk−1 ,
we can use the formula (2.8) and reversibility to get
                                 +∞
                                 X
(2.9)               f, L−1 f =         µ−1
                                        k (hfk−1 , fk i + hfk , fk i) .
                                 k=0

This is the variant of the Green-Kubo formula that we will use. The choice of
the parameters µk can be adjusted according to the problem at hand. Here we
mostly have in mind dynamics that relax to equilibrium at a polynomial rate.
In this case, it seems appropriate to choose µk to scale to 0 geometrically, e.g.
by fixing µk ≡ 2−k . While the series is infinite, we will show that the partial
sums typically converge to their limit exponentially fast.
   In Section 3, we drop the reversibility assumption and define our notation
precisely. We discuss Monte-Carlo methods in Section 4. We then prove (2.9)
and, under suitable assumptions, give estimates on the rate of convergence
of the partial sums to their limit in Section 5. We show how to adapt these

Physical newline lines 378-450:
   From now on, we only assume that the measure P is invariant for the Markov
process X. We still denote by L the infinitesimal generator of the process, and
choose the sign convention so that (e−tL )t⩾0 is the associated semigroup. That
is, for every bounded and continuous function f : X → R and every t ⩾ 0, we
have
                          (e−tL f )(x) = Ex [f (Xt )] .
By Jensen’s inequality, for each t ⩾ 0 and p ∈ [1, ∞], we have that e−tL is
a contraction from Lp (P) to itself. It thus follows that for each λ > 0 and
p ∈ [1, ∞], the resolvent
                                   ˆ +∞
(3.1)                      Rλ :=        e−λt e−tL dt
                                       0
                                   p
is a well-defined operator from L (P) to itself, and moreover, λRλ is a contraction
from Lp (P) to itself. One can then verify that Rλ = (λ + L)−1 and that
the resolvent formula (2.7) holds (see e.g. [46, Theorem 3.16 and (3.7)]). In
particular, for every λ > 0 and µ > 0, the resolvents Rλ and Rµ commute.
                                                            ∗
We denote by L∗ the adjoint of L in L2 (P), and by (e−tL )t⩾0 and (Rλ∗ )λ>0 the
associated semigroup and resolvent.
   We fix a mean-zero function f ∈ L2 (P). In the non-reversible setting, it is
more difficult to assert whether the additive functional
                                   ˆ t
                                 1
(3.2)                           √      f (X(s)) ds
                                  t 0
satisfies a central limit theorem. We refer to [40, Chapter 2] for several results
in this direction. We only record here that under relatively weak conditions,
the limit
(3.3)                    σ 2 (f ) := 2 lim f, (λ + L)−1 f
                                       λ→0

is well-defined, and as t tends to infinity, the random variable in (3.2) converges
in law under PP to a centered Gaussian of variance σ 2 (f ) (see in particular [40,
Theorem 2.7 and (2.14)]).
   Part of the difficulty with non-reversible dynamics is that quantities such as
hf, (λ + L)−1 f i or f, e−tL f are no longer necessarily nonnegative. Since the
emphasis of the present paper is on numerical methods for the computation
of σ 2 (f ) rather than on subtleties that may arise in bordeline cases, we make
the simplifying assumption that
                            ˆ +∞
(3.4)                                f, e−tL f dt < ∞.
                            0
Under this assumption, the existence and finiteness of the limit in the definition
of σ 2 (f ), see (3.3), are easily shown using (3.1). The validity of the classical
Green-Kubo formula (2.4) is obtained similarly.
   Whenever we want to go beyond the derivation of identities and want to
discuss rates of convergence, we will assume that there exists α > 1 such that
for every t ⩾ 0,
(3.5)                           f, e−tL f    ⩽ (1 + t)−α .
     EFFICIENT METHODS FOR ESTIMATION OF HOMOGENIZED COEFFICIENTS                                              9

Note that a possible multiplicative constant in this inequality could be absorbed
after a redefinition of f . We will indicate explicitly whenever (3.4) or (3.5) is
assumed.


                                 4. Monte-Carlo methods
  In this section, we show that a single-step extrapolation of the naive Monte-
Carlo estimator for σ 2 (f ) allows for a significant improvement in computational
complexity. In addition to the quantitative assumption (3.5), we also assume
that
                                "      ˆ t              4 #
                                    1
(4.1)                 sup EP       √       f (X(s)) ds      ⩽ 1.
                      t⩾1            t 0

The assumption of (3.4) implies that the supremum on the left side of (4.1),
with the fourth power replaced by the second power, is finite. The assumption
of finiteness of the fourth moment in (4.1) (which can then normalized to be of
unit size, up to a redefinition of f ) will be used to control the fluctuating part
of the Monte-Carlo estimator.
  In order to describe MCMC methods, we assume that we are given a family