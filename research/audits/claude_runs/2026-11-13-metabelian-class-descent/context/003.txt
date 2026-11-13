ACTUAL primary arxiv1503.09016v2, parent read these passages.

where the existence of the solution is guaranteed by the fact that in every finite graph the number of vertices
with odd degree is even. This implies that it cannot be NP-hard unless NP = co-NP. It is also unlikely that
the problem is in P since Alon has shown [3] that this would imply that there are no one-way permutations.
    Let us come back to our special system of equations (3). In the case m = 1, a nonzero solution can be
found in polynomial time for a single equation which satisfies the Chevalley condition due to the remarkable
work of van de Woestijne [28] where he proves the following.
Fact 2. In deterministic polynomial time in d and log q we can find a nontrivial solution for

                                             a1 xd1 + . . . + ad+1 xdd+1 = 0.


                                                             2

    In the case of more than one equation we don’t know how to find a nonzero solution for system (3) under
just the Chevalley condition. However, if we relax the problem, and take much more variables than are
required for the existence of a nonzero solution, we are able to give a polynomial time solution. Using van
de Woestijne’s result for the one dimensional case, a simple recursion based on reducing one big system with
m equations into d + 1 subsystems with m − 1 equations shows that if n ≥ (d + 1)m then SDE(Fq , n, m, d)
can be solved in deterministic polynomial time in n and log q. The time complexity of this algorithm is
therefore polynomial for any fixed m. The case when d is fixed and m grows appears to be more difficult.
To our knowledge, the only existing result in this direction is the case d = 2 for which it was shown in the
paper [15] by the authors and Sanselme that there exists a (randomized) algorithm that, when n = Ω(m2 ),
solves SDE(Fq , n, m, d) in polynomial time in n and log q. In the main result of this paper we generalize this
result by showing, for every constant d, the existence of a deterministic algorithm that, for every n larger
than some polynomial function of m, solves SDE(Fq , n, m, d) in polynomial time in n and log q.
                                              2
Theorem 3. Let d be constant. For n > dd log d (m + 1)d log d , the problem SDE(Fq , n, m, d) can be solved
in time polynomial in n and log q.
    The large number of variables that makes a polynomial time solution possible, unfortunately also makes
our algorithm most probably irrelevant for cryptographic applications. Nonetheless, it turns out that the
algorithm is widely applicable in quantum computing for solving efficiently various algebraic hidden structure
problems. We now explain this connection.

constant terms, and therefore the value of the constant term can not be recovered.
     It will be convenient for us to consider a slight variant of the hidden polynomial graph problem which we
denote by HPGP′ . The only difference between the two problems is that in the case of HPGP′ the input
is not given by an oracle function but by the ability to access random level set states, which are quantum
states of the form                               X
                                                      |xi|u + Q(x)i,                                        (5)
                                             x∈Fn
                                                q


where u is a random element of Fm      q . Given an oracle input f for HPGP, a simple and efficient quantum
algorithm can create such a random coset state. Therefore an efficient quantum algorithm for HPGP′
immediately provides an efficient quantum algorithm for HPGP.
    In [9] the authors with Decker and Høyer showed that HPGP′ (Fq , 1, m, d) is solvable in quantum poly-
nomial time when d and m are both constant. Part of the quantum algorithm repeatedly solved instances
of SDE(Fq , n, m, d) under such conditions. We present here a modification of this method which works in
polynomial time even if m is not constant. For simplicity, here we restrict ourselves to prime fields. This
will be still sufficient for application to a hidden subgroup problem.
Theorem 5. Let d be constant and p be a prime. If SDE(Fp , n, m, d) is solvable in (randomized) polynomial
time for some n, then HPGP′ (Fp , 1, m, d) is solvable in quantum polynomial time.
   Using Theorem 3 it is possible to dispense in the result of the authors with Decker and Høyer [9] with
the assumption that m is constant.
Corollary 6. If d is constant then HPGP′ (Fp , 1, m, d) is solvable in quantum polynomial time.
    Bacon, Childs and van Dam in [5] have considered the HSP in p-groups of the form G = Fp ⋉ Fm    p when
the hidden subgroup belongs to the family H of subgroups of order p which are not subgroups of the normal
subgroup 0 × Fm p . They have found an efficient quantum algorithm for such groups as long as m is constant.
In [10], based on arguments from [5] the authors with Decker and Høyer sketched how the HSP(G, H) can
be translated into a hidden polynomial graph problem. For the sake of completeness we state here and prove
the exact statement about such a reduction.

                                                      4

Proposition 7. Let d be the nilpotency class of a group G of the form Fp ⋉ Fm
                                                                            p . There is a polynomial time
quantum algorithm which reduces HSP(G, H) to HPGP′ (Fp , 1, m, d).
   Putting together Corollary 6 and Proposition 7, it is also possible to get rid of the assumption that m is
constant in the result of [5].
Corollary 8. If the nilpotency class of the group G of the form Fp ⋉ Fm

Actual Decker-Hoyer-Ivanyos-Santha1305.1543v2 section2.1 was read in arxivHTML: append a uniform register, subtract public scaled fresh coordinate from old coordinates, then measure old registers. It supplies the known phase-linearization operation, not the new mixed unknown-support invariant. Actual Morales2608.05321v1 section1.1 and AppendixA.3 concern scalar-action semidirect products or quasi-Hamiltonian groups, not a general fixed-class metabelian theorem. No novelty inference from that scoped comparison.
