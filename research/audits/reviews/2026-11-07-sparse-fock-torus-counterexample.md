# Exact counterexample to stabilizer-torus frame extraction

7 November 2026. Independent structural review after STATE/TRAPS. No
network, external API, Git, implementation, or finite sweep. This is a
counterexample to extracting a polynomial-support frame merely by learning
the quadratic-Hamiltonian variance kernel and diagonalizing a maximal torus.
It is NOT a lower bound for general sparse-Fock learning with other data.

## Native sparse family

Let n=p>=11 be a prime with p=3 mod4, and let D be the nonzero quadratic
residues in Z_p. Put w=(p-1)/2 and

    |psi> = p^(-1/2) sum_(a in Z_p) |D+a>.

Occupation subsets are identified with Fock strings. This is a normalized,
parity-definite state with r=n nonzero branches, each of probability 1/n.
Every passive Gaussian U gives another promised input U|psi>, still with
an n-term description in the unknown Gaussian frame U.

For nonzero h, |D intersect (D+h)|=(p-3)/4=:lambda. This follows by
expanding the two quadratic-residue indicators and using
sum_x chi(x)chi(x-h)=-1 and chi(-h)=-chi(h). Therefore distinct strings in
the support have Hamming distance

    2(w-lambda)=(p+1)/2 >= 6.

The translates form a symmetric 2-design: every coordinate lies in w
strings, and every coordinate pair lies in lambda strings. Its incidence
matrix A satisfies

    A A^T = (w-lambda) I + lambda 11^T.

It is invertible. Thus the n support vectors affinely span the entire
constant-weight hyperplane, of dimension n-1. A minimal concrete instance
is p=11, D={1,3,4,5,9}, w=5, lambda=2, and minimum distance6.

## The complete quadratic ray stabilizer is one-dimensional

Write a general Hermitian quadratic Hamiltonian, up to its fixed scalar
offset, as

    H=sum_ij h_ij a_i^dagger a_j
      +sum_(i<j) (Delta_ij a_i^dagger a_j^dagger
                   +conj(Delta_ij) a_j a_i),

with h Hermitian. Its centered variance vanishes on a pure state exactly
when that state is its eigenvector.

Each off-diagonal term flips exactly two occupation bits. Such an output
is outside the support, and outputs from distinct support strings cannot
coincide: a collision would put their distance at most4. On any one string,
the flipped pair identifies the hopping or pairing coefficient uniquely.
The design has strings with i occupied and j empty, and strings with both
empty or both occupied, for every i!=j. Consequently H|psi>=E|psi> forces
every off-diagonal h_ij and every Delta_ij to vanish.

The remaining diagonal condition is A(h_11,...,h_nn)^T=E' 1. Because
A is invertible and A1=w1, all diagonal coefficients must be equal.
Thus the compact quadratic ray-stabilizer Lie algebra is exactly

    h = R (N-n/2),      N=sum_i a_i^dagger a_i.

Its rank is1, attaining the proposed lower bound n-r+1. Its maximal torus
is the single total-number circle. Its action on Majoranas has n identical
frequency pairs and does not distinguish the n complex orbitals.

## All measured moments are blind to the remaining frame

The support distance eliminates every off-diagonal matrix element of
degree at most4 between distinct branches. The design counts give

    <a_i^dagger a_j> = (w/n) delta_ij,
    <a_i^dagger a_j^dagger a_l a_k>
       = [w(w-1)/(n(n-1))] delta_(ij),(kl),

where the second identity uses increasing ordered pairs. Number-changing
expectations vanish. These are exactly the one- and two-particle reduced
density matrices of the maximally mixed w-particle sector. Normal ordering
then determines every second and fourth Majorana moment from them.

That mixed sector is invariant under every passive U(n) transformation.
Hence the COMPLETE covariance, fourth-moment tensor, and centered
quadratic-variance Gram matrix are identical for all U|psi>. In particular,
these data contain no information selecting a passive orbital frame.

There is no small nonzero Gram gap to blame. For the passive component,

    Var(a^dagger h a)
      = [(n+1)/(4n)] (Tr(h^2)-(Tr h)^2/n).

For the pairing component the variance is

    [(n-1)/(2n)] sum_(i<j) |Delta_ij|^2.

Cross terms between these sectors vanish. Relative to these natural
quadratic-coefficient norms, nonzero variances have constant-scale lower
bounds. Only the total-number direction is null.

## Failure of the proposed structural conclusions

Any passive orbital basis diagonalizes this maximal torus. A generic such
basis gives nonzero amplitudes on ALL binom(n,w) Fock strings. To see this,
fix a target w-subset S. Its amplitude as a function of U is analytic and
not identically zero: a mode permutation can map one original support
string to S. Its zero set has Haar measure zero. Taking the finite union
over all S proves simultaneous nonvanishing for generic U. Thus compatible
torus frames can have support binom(n,w)=exp(Omega(n)), exponential in r=n.

There is also no small Gaussian-compressible core. The covariance normal
singular values are all |1-2w/n|=1/n. A pure Gaussian factor would require
at least one normal singular value1, which Gaussian changes of frame
cannot create. More strongly, any state having even one pure Gaussian
mode factor has a norm-one rotated Majorana bilinear of expectation +/-1;
its expectation on psi has magnitude at most1/n. The trace distance is
therefore at least (1-1/n)/2. Constant-accuracy O(log r)-mode compression
is excluded for this family, not merely exact compression.

This refutes an ANY-completion claim and a moment-only choice of a usable
completion. A specially chosen sparse completion certainly exists here:
the original frame has support n. The counterexample does not refute that
existential statement or algorithms using additional measurements. Rather,
the variance-kernel/maximal-torus operation leaves the entire hard choice
inside an n-dimensional degenerate frequency sector, with no frame signal
in the measured moments. No general sparse-Fock hardness claim follows.
