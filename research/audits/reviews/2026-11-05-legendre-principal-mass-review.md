# Principal-series mass for the quadratic Legendre receiver

Date: 2026-11-05. Independent mathematical subproblem review.
Scope: the fourth-moment and receiver-probability obligations only. This
does not certify the Fourier-basis conversion, coherent scalar circuit,
native-oracle preparation, novelty, or any complexity separation.

## Hypotheses inherited from the separate kernel calculation

Let p be an odd prime, chi its quadratic character, and

    Ns = p(p+1)/2,  M = p(p-1)/2.

The proposed two-copy kernel T has Ns rows and M columns, with every entry
of modulus one. Its principal-series summands have dimension p+1 and are
indexed by even multiplicative characters alpha, alpha^2 != 1, modulo
alpha <-> alpha^-1. The squared singular value on that summand is

    |tau_alpha|^2 = 4 d_alpha^2 (p-d_alpha^2),
    d_alpha = beta(-1) Re J(beta,chi),  beta^2 = alpha.             (1)

The eigenvalue formula for d_alpha agrees with Chen, Proposition 9.3,
as supplied in `../sources/legendre_prf/chen_cartan_9809209.txt`:
d_alpha = (1/2) sum_{x != 0} alpha(x) chi(1+x^2).
The intertwiner and its multiplicities are the separate kernel review's
obligations; they are assumptions of this mass proof.

## Source checked and precise application

Ping Xi, *Equidistributions of Jacobi sums*, arXiv:1809.04286,
Theorem 1.3 and its complete proof in Section 3.1, were read locally in
`../sources/legendre_prf/xi_jacobi_1809_04286.txt`.
The definition preceding the theorem explicitly permits s=0.
Set q=p, r=1, kappa=(4), s=0, and eta=(chi). The sole eta is nontrivial;
the disjointness condition against the empty rho tuple is vacuous.
The summed character set is exactly all beta except 1 and chi, and hence

    | sum_{beta != 1,chi} J(beta,chi)^4 | <= 12 p^(5/2).           (2)

This is a uniform moment estimate for a fixed quadratic character as p
varies. It does not require randomness of the hidden quadratic or its
coefficients. The source proves the estimate using disjoint-parameter
hypergeometric sums, so no independence of Jacobi phases is assumed here.
We use the theorem's stated constant 12, without trying to sharpen it.

## Fourfold indexing and exceptional characters

All characters are extended by zero at zero. For beta != 1,chi,
|J(beta,chi)|=sqrt(p). The Gauss-sum identity gives

    J(beta chi,chi) J(beta,chi) = chi(-1) p,
    J(beta^-1,chi) = conjugate(J(beta,chi)).

Thus Re J^4, and therefore (1), is invariant under beta -> beta chi
and beta -> beta^-1. Restrict to V={beta: beta^4 != 1}. Every orbit
under these two operations has exactly four members: a collision would
force beta^2=1 or beta^2=chi. The orbit corresponds exactly to one
principal label {alpha,alpha^-1}, alpha=beta^2.

There are r=0 extra exclusions when p=3 mod 4, and r=2 when p=1 mod 4,
beyond beta=1,chi. Consequently |V|=p-3-r. These are precisely the
quartic beta whose square gives the exceptional alpha=chi label;
no exceptional twisted-Steinberg mass is counted as principal mass.

Since beta(-1) is real and squares to one, (1) implies

    |tau_alpha|^2 = (p^2 - Re J(beta,chi)^4)/2 <= p^2.             (3)

Let A denote the trace of T^*T over the retained principal summands.
The fourfold indexing and their common dimension give the EXACT identity

    A = (p+1)/8 * ((p-3-r)p^2 - Re sum_{beta in V} J(beta,chi)^4).
                                                                    (4)

Removing the r extra terms in (2) costs at most r p^2. In particular,

    A >= (p+1)p^2/8 * (p-7-12 sqrt(p)),
    A  = p^4/8 + O(p^(7/2)).                                    (5)

For every prime p>=625 the explicit lower bound implies

    A >= p^3(p+1)/16,
    A/(M Ns) >= p/[4(p-1)] > 1/4.                               (6)

The second ratio is the principal probability in EACH normalized kernel
column. Its equality to the trace average uses the transitive action on
the M hidden quadratics and the invariant principal projection. It is
not merely an average-over-secrets guarantee. As p grows, this mass tends
to 1/2. Small primes can be dealt with separately by bounded exhaustive
work; no asymptotic claim is inferred from a small-prime scan.

## Backprojection receiver: no inverse or spectral gap

Suppose the two coherent spherical transforms and the diagonal block
tau_alpha^*/p have actually been implemented in aligned conventions.
Start from the normalized column T|Q>/sqrt(Ns), retain only principal
labels, apply that diagonal block, and invert the nonsplit transform.
On its heralded branch the output is

    (T_principal^* T_principal)|Q> / (p sqrt(Ns)).

The joint probability of the scalar block's success and the correct
label Q is EXACTLY

    P_Q = [A/(p M sqrt(Ns))]^2.                                  (7)

This charges the principal projection and the scalar block's heralding;
there is no conditioning on either event in (7). It is conditional only
on the earlier distinct-pair preparation. Formula (6) gives

    P_Q >= p(p+1)/[32(p-1)^2] > 1/32,  p>=625.

Multiplying by the distinct-pair success p/(p+1) still gives a lower
bound p^2/[32(p-1)^2] > 1/32. The exact asymptotic expression from
(4) and (7) tends to 1/8, both before and after that preparation factor.
Approximation error, bounded retries, and fresh native verification
remain part of the overall algorithm's resource/probability proof.

This is a backprojection, not an inverse singular-value operation.
There is no minimum-singular-value, conditioning, polar-phase, cutoff,
or individual-character lower-bound assumption in (4)-(7).

## Optional independent algebraic check for p=3 mod 4

The source-based proof above suffices for all growing primes. An elementary
partial-family check also exists, and is not needed by the receiver.
Put a(t)=sum_x chi(x(x-1)(x-t)). Character orthogonality gives

    sum_t a(t)^2 = p^2-2p-1,
    sum_beta J(beta,chi)^4 = (p-1) sum_{t != 0} chi(t) a(t)^2.

The first identity follows by expanding the square: the inner quadratic
sum in t is p-1 for equal x,y and -1 otherwise. The second follows by
multiplicative orthogonality and grouping the four Jacobi variables into
two pairs of reciprocal products. Under t -> 1-t and t -> 1/t,
a(t)^2 is unchanged. For t != 0,1 the average of chi over its six
Mobius transforms equals

    [chi(t)+chi(1-t)+chi(-1)chi(t)chi(1-t)]/3.

When p=3 mod 4 this is at most 1/3, so the real fourth moment cannot
concentrate at its trivial maximum. For p=1 mod 4 the maximum is 1;
this symmetry alone does NOT prove the desired mass. Equation (2) is
what closes the all-prime obligation without that detour.

## Verdict

The principal-mass and exact backprojection-success obligations are
established under the separately stated kernel/spectral identities.
The primary theorem applies to the full required character family, with
only explicitly bounded exceptional removals. The calculation is uniform
in the hidden irreducible quadratic. No efficient receiver, speedup,
novelty, classical hardness, or quantum execution follows until its
remaining coherent implementation and access obligations are reviewed.
