Moylett actual sections3 and5 excerpts
                                                   5

Quantum Sci. Technol. 5 (2020) 015001                                                                           A E Moylett et al



in the case where some photons experience little or no loss, by extracting losses into a layer of non-uniform loss
and simulating via a generalisation of the Clifford and Clifford algorithm [43].


3. Expanding in terms of states

We will now introduce a new expression for partially distinguishable particles. We start by writing the input state
of n photons, with pairwise distinguishability parameter x as in the previous section, in ﬁrst quantisation

                                                            1⎛                        ⎞
                                                 rn, x =       ⎜⎜ å s∣sñás∣s ¢x s·s ¢⎟⎟ ,                                  (22)
                                                            n! ⎝s, s ¢Î Sn            ⎠

where we have used s · s¢ to denote the number of places where permutations σ and s¢ match. For reference,
the expansion of [29, 30] is carried out by identifying σ and s¢ that match for a ﬁxed set of i points:
                                                    ⎛                                                 ⎞
                                                    ⎜                                                 ⎟
                                                    ⎜                                                 ⎟
                                                1⎜n i                                                 ⎟
                                        rn, x =     ⎜å x                  å               s∣sñás∣s ¢ †⎟.                   (23)
                                                n ! ⎜i = 0                  -1
                                                                     s , s ¢ Î Sn                     ⎟
                                                    ⎜           $ I Í [n] s.t. ∣ I ∣= i
                                                                             -1                       ⎟
                                                             s-1 ( j ) ¹ s¢ ( j ) " j Î I
                                                    ⎜                                                 ⎟
                                                    ⎝                        - 1
                                                           s-1 ( j ) = s ¢ ( j ) " j Ï I              ⎠
Note here that the terms in the sum over permutations do not correspond to physical states. This can be seen by
the fact that for i ¹ 0 this summation has no elements along the diagonal of the density matrix, as σ and s¢ need
to differ in exactly i places.
    We instead look at an alternative expansion, in order to decompose the model into a linear combination of
physical states:

                                                    ⎛                                                       ⎞
                                                    ⎜n                                                      ⎟
                                                1⎜                                                         †⎟
                                        rn, x =       å   p
                                                n ! ⎜i = 0 i
                                                                          å
                                                                       s, s¢Î Sn
                                                                                             s∣s ñá s ∣s ¢
                                                                                                            ⎟
                                                                                                                           (24)
                                                    ⎜              $ I Í [n] s.t. ∣ I ∣= i                  ⎟
                                                    ⎝        s-1 ( j ) = s ¢-1 ( j ) " j Ï I                ⎠
                                                    ⎛                                               ⎞
                                             n      ⎜1                                              ⎟
                                    = å pi å ⎜                      å                   s∣sñás∣s ¢ †⎟                      (25)
                                      i=0  I Í [n] ⎜ n!          s, s ¢Î Sn                         ⎟
                                           ∣ I ∣= i ⎝   s-1 ( j ) = s ¢-1 ( j ) " j Ï I             ⎠
                                                                   n
                                                             = å pi å rI ,                                                 (26)
                                                                  i=0      I Í [n]
                                                                           ∣ I ∣= i

where ρI is the state where photons in modes jäI are fully indistinguishable from each other, all other photons
are fully distinguishable, and 0  pi  1 is a coefﬁcient dependent on x and n determining the probability of a
state with i indistinguishable single photons.
    Note that unlike equation (23), where permutations must differ in exactly i points, in equation (24) we allow
permutations to differ in at most i points. This means that elements closer to and along the diagonal of the density
matrix are also part of this summation, and this means that each s, s¢ Î Sn term forms a valid density matrix.
    Already we can see how a classical simulation might work—if we are able to sample pi efﬁciently, then we can
choose ρI by selecting i photons uniformly at random to be indistinguishable. These i photons can be classically
simulated using Clifford and Clifford [15], while the remaining n−i photons are treated as fully distinguishable
photons, each of which can be simulated individually in polynomial time [14, 32].

3.1. The pi are binomially distributed
Here, we will show that the coefﬁcients pi follow the binomial distribution
                                                           pi = x i (1 - x )n - i .                                        (27)

     To see that the matrix elements of equation (26) with pi binomially distributed equal those of equation (23),
consider s, s¢ which differ at points in the set I, where ∣I ∣ = i; the coefﬁcient here should be x i. Contributing to this
element of the density matrix will be the state ρI, as well as other states rI ¢ , where I Í I ¢. The number of such sets I¢
   ⎛n - i ⎞
is ⎜        ⎟, as it is equivalent to choosing i¢ from n elements when i elements have already been chosen. The
   ⎝ i¢ - i ⎠
                                                             6

Quantum Sci. Technol. 5 (2020) 015001                                                                     A E Moylett et al



corresponding matrix element is
                                             1 ⎛ n i¢                 ⎛ n - i ⎞⎞
                                                ⎜ å x (1 - x )n - i ¢ ⎜        ⎟⎟                                    (28)
                                             n! ⎝i ¢= i               ⎝ i¢ - i ⎠ ⎠

                                            1 ⎛ i n i ¢- i              ⎛ n - i ⎞⎞
                                        =      ⎜x å x ( 1 - x ) n - i ¢ ⎜        ⎟⎟                                  (29)
                                            n! ⎝ i ¢= i                 ⎝ i¢ - i ⎠ ⎠

                                            1 ⎛ i n- i i¢                   ⎛ n - i ⎞⎞
                                        =      ⎜x å x ( 1 - x ) n - i - i ¢ ⎜       ⎟⎟                               (30)
                                            n! ⎝ i ¢= 0                     ⎝ i¢ ⎠ ⎠
                                                         x i (x + 1 - x )n - i
                                                   =                                                                 (31)
                                                                  n!
                                                                  xi
                                                               = .                                                   (32)
                                                                  n!
It is not hard to see that the state is normalised
                                                         n
                                        Tr[rn, x ] = å x i (1 - x )n - i å Tr[rI ]                                   (33)
                                                         i=0                I Í [n]
                                                                            ∣ I ∣= i
                                                     n
                                                = å x i (1 - x )n - i å 1                                            (34)
                                                    i=0                  I Í [n]
                                                                         ∣ I ∣= i
                                                     n
                                                                        ⎛n ⎞
                                                  = å x i (1 - x )n - i ⎜ ⎟                                          (35)
                                                    i=0
                                                                        ⎝i⎠
                                                       = (x + 1 - x )n                                               (36)
                                                               = 1.                                                  (37)
Thus this model of ﬁxed pairwise distinguishability can be written as an expansion in terms of valid states, where
indistinguishable photons are drawn from a binomial distribution.

3.2. Classical simulation
We can now see explicitly how a simulation for boson sampling with distinguishable photons would work. First, we
sample an integer i ä [n] according to the Binomial distribution with coefﬁcients n and x. Next, we sample a subset I of
                                             ⎛n⎞
the photons uniformly at random from the ⎜ ⎟ possible subsets of size i. These are the indistinguishable photons of
                                             ⎝i⎠
our simulation, which we simulate using Clifford and Clifford in O (i 2i + Poly (i , m)) time. The remaining n−i
photons are considered to be distinguishable. Rather than needing to compute the output probabilities of these photons
collectively, which could take between O (n - i )4 log (n - i ) and O (n - i )7 log 4(n - i ) time via permanents of
matrices with non-negative entries [40], we can instead sample each distinguishable photon individually. To do so, we
                                                          n
                                                                                     ⎛n ⎞
                                                    =    å x i (1 - x )n- i ⎜⎝ i ⎟⎠.                                    (66)
                                                        i=k+1

    It seems like there should be some room for improvement in this bound. In particular, the use of the triangle
inequality suggests that there might be more precise approximations of the expected distance.


5. Worst case error

We shall now use a different technique to show that the above Haar average case error bound matches the worst-
case error for any linear-optical interferometer. We do so by ﬁnding an upper bound for the trace distance
between our ideal partially distinguishable state and the approximation that results from truncating at some k,
the size of the largest indistinguishable set of particles. As the trace distance is an upper bound for any POVM

                                                          9

Quantum Sci. Technol. 5 (2020) 015001                                                                                    A E Moylett et al



measurement, we know that this will provide an upper bound for the difference in distribution produced by any
interferometer.
    Denoting our truncated state

                                                           å i = 0 x i (1 - x )n - i å
                                                                 k
                                                                                                 I Í [n]    rI
                                                                                                 ∣ I ∣= i
                                           r k, x =                                                             ,                  (67)
                                                             å i = 0 x i (1 - x )n - i ( i )
                                                                         k                        n



where the denominator is a normalising factor, and similarly

                                                       å i= k + 1x i (1 - x )n- i å
                                                             n
                                                                                                    I Í [n]    rI
                                                                                                    ∣ I ∣= i
                                         r > k, x =                                                                  .              (68)
                                                            å i= k + 1x i (1 - x )n- i ( i )
                                                                     n                                n



We can now estimate the trace distance by rewriting rn, x as
                                                       k
                                                                          ⎛n ⎞
                                              rn, x = å x i (1 - x )n - i ⎜ ⎟ r k, x                                               (69)
                                                      i=0
                                                                          ⎝i⎠
                                                       n
                                                                                          ⎛n ⎞
                                               +      å x i (1 - x )n- i ⎜⎝ i ⎠⎟ r> k,x ,                                           (70)
                                                     i=k+1

which, by convexity, gives
                                                                               n
                                                                                                            ⎛n ⎞
                                        d tr (rn, x , r k, x )              å x i (1 - x )n- i ⎜⎝ i ⎟⎠.                           (71)
                                                                             i=k+1

   If we want this bound to be small, we can use techniques like those used for working out the tails of the
binomial distribution. For example, it is known that for nx<k<n that
                                                                         ⎛      ⎛ k ⎞⎞
                                           d tr (rn, x , r k, x )  exp ⎜ - nD ⎜ ∣∣x ⎟ ⎟ ,                                         (72)
                                                                         ⎝      ⎝ n ⎠⎠
